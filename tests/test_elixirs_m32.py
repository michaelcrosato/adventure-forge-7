"""Tests for Milestone 32: Continental Alchemical Laboratories, Distillation Alembics & Grand Master Apothecary System."""
import asyncio
import json
from typing import Dict, Any

from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.elixirs import (
    ANCIENT_ALEMBICS,
    APOTHECARY_RANKS,
    get_apothecary_rank,
    evaluate_elixirs_progress,
    get_elixir_affordances_for_scene,
)
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import ProseLinter, flesch_kincaid_grade, word_count
from app import app


def test_elixir_registry_integrity():
    """Verify all 6 canonical alembic labs exist, link to real cellar scenes, and have valid fields."""
    assert len(ANCIENT_ALEMBICS) == 6
    registry = build_world_registry()
    all_scenes = set()
    for reg in registry.values():
        all_scenes.update(reg.scenes.keys())

    for lab_id, lab in ANCIENT_ALEMBICS.items():
        assert lab.id == lab_id
        assert lab.lab_scene in all_scenes, f"Lab scene {lab.lab_scene} not found in world registry!"
        assert lab.name
        assert lab.province in [
            "The Reach",
            "The Scorchwaste",
            "The Sunken Hollows",
            "The High Court",
            "The Lowlands",
            "Central Crossroads",
        ]
        assert lab.icon
        assert lab.domain
        assert lab.distill_action_id.startswith("elixir_distill_")
        assert lab.imbibe_action_id.startswith("elixir_imbibe_")
        assert lab.refill_action_id.startswith("elixir_refill_")
        assert lab.elixir_marker.startswith("marker_elixir_")
        assert lab.mastery_marker.startswith("marker_elixir_mastery_")


def test_elixir_hemingway_compliance():
    """Verify all elixir descriptions, result texts, and rank descriptions satisfy Hemingway prose."""
    linter = ProseLinter(min_readability_grade=6.0, max_readability_grade=8.0)

    for lab_id, lab in ANCIENT_ALEMBICS.items():
        # Action labels <= 3 words
        for label, lbl_name in [
            (lab.distill_action_label, f"{lab_id}_distill_label"),
            (lab.imbibe_action_label, f"{lab_id}_imbibe_label"),
            (lab.refill_action_label, f"{lab_id}_refill_label"),
        ]:
            wc = word_count(label)
            assert 1 <= wc <= 3, f"Label {lbl_name} '{label}' has {wc} words (must be 1-3)"

        # Text bodies: FKGL in [6.0, 8.0], <= 18 words/sent, 1-3 sentences, 0 purple words
        for text, context in [
            (lab.description, f"{lab_id}_desc"),
            (lab.distill_result_text, f"{lab_id}_distill_result"),
            (lab.imbibe_result_text, f"{lab_id}_imbibe_result"),
            (lab.refill_result_text, f"{lab_id}_refill_result"),
        ]:
            errs = linter.lint_text(text, context=context, check_readability=True)
            grade = flesch_kincaid_grade(text)
            assert not errs, f"Hemingway lint errors in {context}: {errs} (grade={grade})"
            assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in {context}"

    # Rank descriptions
    for tier in APOTHECARY_RANKS:
        errs = linter.lint_text(tier["desc"], context=f"rank_{tier['count']}", check_readability=True)
        grade = flesch_kincaid_grade(tier["desc"])
        assert not errs, f"Hemingway lint errors in rank {tier['count']}: {errs} (grade={grade})"
        assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in rank {tier['count']}"


def test_elixir_distill_execution():
    """Verify distilling an ancient elixir sets flags, awards markers, and logs events."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="ApothecaryDistiller",
        ancestry="Highlander",
        background="herbalist",
        attributes={"wits": 14, "cunning": 12, "endurance": 12},
        skills={"lore": 2, "cunning": 2},
        traits=["botanist"],
        stamina=5,
        max_stamina=10,
        inventory=["alembic_vial"],
    )

    state = GameState(
        build_id="af-build-001",
        session_id="elixir-session",
        character=char,
        current_region="province_reach",
        current_scene="reach_high_pass_cellar",
    )

    legal_acts = [a.id for a in engine.get_legal_actions(state)]
    assert "elixir_distill_frostbane" in legal_acts

    # Execute distill
    new_state, obs = engine.step(state, "elixir_distill_frostbane")
    assert obs.success
    assert new_state.world_flags.get("elixir_distilled_alembic_frostbane") is True
    assert "marker_elixir_frostbane" in new_state.character.markers
    assert "marker_elixir_mastery_reach" in new_state.character.markers
    assert new_state.character.stamina == 8  # 5 + 3

    # Check engine progress helper
    prog = engine.get_elixirs_progress(new_state)
    assert prog["distilled_count"] == 1
    assert prog["apothecary_rank"] == "Journeyman Brewer"
    assert prog["active_elixirs_count"] == 1
    assert prog["active_masteries_count"] == 1


def test_7axis_elixir_reactivity():
    """Verify 7-axis qualification (tools, traits, attributes, skills, stamina) for elixir distillation."""
    lab = ANCIENT_ALEMBICS["alembic_sunfire"]

    # 1. Qualified via apothecary tool item
    char_item = CharacterSheet(
        name="ItemHerbalist", ancestry="Human", background="Scout", inventory=["potion_vial"], stamina=0
    )
    aff_item = get_elixir_affordances_for_scene(lab.lab_scene, char_item, {})
    assert any(a.id == lab.distill_action_id for a in aff_item)

    # 2. Qualified via apothecary trait
    char_trait = CharacterSheet(
        name="TraitHerbalist", ancestry="Human", background="Scout", traits=["herbalist"], stamina=0
    )
    aff_trait = get_elixir_affordances_for_scene(lab.lab_scene, char_trait, {})
    assert any(a.id == lab.distill_action_id for a in aff_trait)

    # 3. Qualified via high wits attribute
    char_attr = CharacterSheet(
        name="AttrHerbalist", ancestry="Human", background="Scout", attributes={"wits": 14}, stamina=0
    )
    aff_attr = get_elixir_affordances_for_scene(lab.lab_scene, char_attr, {})
    assert any(a.id == lab.distill_action_id for a in aff_attr)

    # 4. Qualified via skill
    char_skill = CharacterSheet(
        name="SkillHerbalist", ancestry="Human", background="Scout", skills={"lore": 2}, stamina=0
    )
    aff_skill = get_elixir_affordances_for_scene(lab.lab_scene, char_skill, {})
    assert any(a.id == lab.distill_action_id for a in aff_skill)

    # 5. Qualified via physical stamina
    char_stam = CharacterSheet(name="StamHerbalist", ancestry="Human", background="Scout", stamina=2)
    aff_stam = get_elixir_affordances_for_scene(lab.lab_scene, char_stam, {})
    assert any(a.id == lab.distill_action_id for a in aff_stam)

    # 6. Unqualified character with 0 stamina, no tools, low stats
    char_none = CharacterSheet(
        name="Unqualified", ancestry="Human", background="Scout", stamina=0, attributes={"wits": 10}, skills={"lore": 0}
    )
    aff_none = get_elixir_affordances_for_scene(lab.lab_scene, char_none, {})
    assert not any(a.id == lab.distill_action_id for a in aff_none)


def test_field_elixir_imbibing_and_refill():
    """Verify imbibing an elixir in the field and refilling at the cellar laboratory."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="FieldHerbalist",
        ancestry="Highlander",
        background="apothecary",
        markers=["marker_elixir_frostbane"],
        stamina=5,
    )

    # 1. In the field (e.g. at bazaar_center or another scene)
    field_state = GameState(
        build_id="af-build-001",
        session_id="field-elixir-session",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
        world_flags={"elixir_distilled_alembic_frostbane": True},
    )

    legal_acts = [a.id for a in engine.get_legal_actions(field_state)]
    assert "elixir_imbibe_frostbane" in legal_acts

    # Execute imbibing in field
    imbibed_state, obs = engine.step(field_state, "elixir_imbibe_frostbane")
    assert obs.success
    assert imbibed_state.world_flags.get("elixir_imbibed_alembic_frostbane") is True
    assert "marker_imbibed_alembic_frostbane" in imbibed_state.character.markers
    assert imbibed_state.character.stamina == 8  # 5 + 3

    # Now imbibing is no longer available in field (already imbibed)
    subsequent_acts = [a.id for a in engine.get_legal_actions(imbibed_state)]
    assert "elixir_imbibe_frostbane" not in subsequent_acts

    # 2. Return to reach_high_pass_cellar and refill alembic
    lab_state = imbibed_state.evolve(
        current_region="province_reach",
        current_scene="reach_high_pass_cellar",
    )
    lab_acts = [a.id for a in engine.get_legal_actions(lab_state)]
    assert "elixir_refill_frostbane" in lab_acts

    # Step refill
    renewed_state, renew_obs = engine.step(lab_state, "elixir_refill_frostbane")
    assert renew_obs.success
    assert renewed_state.world_flags.get("elixir_imbibed_alembic_frostbane") is False
    assert renewed_state.character.stamina == 10  # 8 + 2


def test_apothecary_rank_progression():
    """Verify progressive unlock of apothecary ranks across 0 to 6 alchemical laboratories."""
    assert get_apothecary_rank(0)["title"] == "Novice Herbalist"
    assert get_apothecary_rank(1)["title"] == "Journeyman Brewer"
    assert get_apothecary_rank(2)["title"] == "Tincture Craftsman"
    assert get_apothecary_rank(3)["title"] == "Master Alchemist"
    assert get_apothecary_rank(4)["title"] == "Guild Toxicologist"
    assert get_apothecary_rank(5)["title"] == "Grand Pharmacist"
    assert get_apothecary_rank(6)["title"] == "Continental Arch-Apothecary"

    flags: Dict[str, Any] = {}
    markers = []
    for idx, lab in enumerate(ANCIENT_ALEMBICS.values(), start=1):
        flags[f"elixir_distilled_{lab.id}"] = True
        markers.append(lab.elixir_marker)
        prog = evaluate_elixirs_progress(flags, [], markers)
        assert prog["distilled_count"] == idx
        assert prog["active_elixirs_count"] == idx

    final_prog = evaluate_elixirs_progress(flags, [], markers)
    assert final_prog["apothecary_rank"] == "Continental Arch-Apothecary"
    assert final_prog["progress_pct"] == 100.0


def test_elixirs_replay_determinism():
    """Verify bit-for-bit replay determinism across distill, imbibe, and refill transitions."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    def run_trajectory():
        char = CharacterSheet(
            name="DeterministicApothecary",
            ancestry="Highlander",
            background="herbalist",
            traits=["herbalist"],
            stamina=10,
            inventory=["alembic_vial"],
        )
        s = GameState(
            build_id="af-build-001",
            session_id="det-elixir-session",
            character=char,
            current_region="province_reach",
            current_scene="reach_high_pass_cellar",
        )
        s, _ = engine.step(s, "elixir_distill_frostbane")
        s, _ = engine.step(s, "elixir_imbibe_frostbane")
        s, _ = engine.step(s, "elixir_refill_frostbane")
        return s.fingerprint()

    fp1 = run_trajectory()
    fp2 = run_trajectory()
    assert fp1 == fp2, "Replay execution produced diverging state fingerprints!"


def test_asgi_elixirs_endpoint():
    """Verify GET and HEAD /api/game/elixirs endpoint returns correct metadata."""
    async def run_asgi(path: str, method: str = "GET"):
        scope = {
            "type": "http",
            "method": method,
            "path": path,
            "query_string": b"",
            "headers": [],
        }
        messages = []

        async def receive():
            return {"type": "http.request", "body": b""}

        async def send(message):
            messages.append(message)

        await app(scope, receive, send)

        status = 0
        headers = {}
        body = b""
        for msg in messages:
            if msg["type"] == "http.response.start":
                status = msg["status"]
                headers = dict(msg.get("headers", []))
            elif msg["type"] == "http.response.body":
                body += msg.get("body", b"")
        return status, headers, body

    # 1. GET /api/game/elixirs
    status, headers, body = asyncio.run(run_asgi("/api/game/elixirs", "GET"))
    assert status == 200
    assert b"application/json" in headers.get(b"content-type", b"")
    data = json.loads(body.decode("utf-8"))
    assert data["total_labs"] == 6
    assert len(data["labs"]) == 6

    # 2. HEAD /api/game/elixirs
    h_status, h_headers, h_body = asyncio.run(run_asgi("/api/game/elixirs", "HEAD"))
    assert h_status == 200
    assert len(h_body) == 0
