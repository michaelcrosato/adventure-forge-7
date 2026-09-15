"""Tests for Milestone 31: Continental Runeforges, Ancient Crucible Anvils & Master Artificer System."""
import asyncio
import json
from typing import Dict, Any

from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.forge import (
    ANCIENT_RUNEFORGES,
    ARTIFICER_RANKS,
    get_artificer_rank,
    evaluate_forge_progress,
    get_forge_affordances_for_scene,
)
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import ProseLinter, flesch_kincaid_grade, word_count
from app import app


def test_forge_registry_integrity():
    """Verify all 6 canonical runeforges exist, link to real armory scenes, and have valid fields."""
    assert len(ANCIENT_RUNEFORGES) == 6
    registry = build_world_registry()
    all_scenes = set()
    for reg in registry.values():
        all_scenes.update(reg.scenes.keys())

    for f_id, f in ANCIENT_RUNEFORGES.items():
        assert f.id == f_id
        assert f.forge_scene in all_scenes, f"Forge scene {f.forge_scene} not found in world registry!"
        assert f.name
        assert f.province in [
            "The Reach",
            "The Scorchwaste",
            "The Sunken Hollows",
            "The High Court",
            "The Lowlands",
            "Central Crossroads",
        ]
        assert f.icon
        assert f.domain
        assert f.inscribe_action_id.startswith("forge_inscribe_")
        assert f.temper_action_id.startswith("forge_temper_")
        assert f.quench_action_id.startswith("forge_quench_")
        assert f.rune_marker.startswith("marker_rune_")
        assert f.mastery_marker.startswith("marker_forge_mastery_")


def test_forge_hemingway_compliance():
    """Verify all forge descriptions, result texts, and rank descriptions satisfy Hemingway prose."""
    linter = ProseLinter(min_readability_grade=6.0, max_readability_grade=8.0)

    for f_id, f in ANCIENT_RUNEFORGES.items():
        # Action labels <= 3 words
        for label, lbl_name in [
            (f.inscribe_action_label, f"{f_id}_inscribe_label"),
            (f.temper_action_label, f"{f_id}_temper_label"),
            (f.quench_action_label, f"{f_id}_quench_label"),
        ]:
            wc = word_count(label)
            assert 1 <= wc <= 3, f"Label {lbl_name} '{label}' has {wc} words (must be 1-3)"

        # Text bodies: FKGL in [6.0, 8.0], <= 18 words/sent, 1-3 sentences, 0 purple words
        for text, context in [
            (f.description, f"{f_id}_desc"),
            (f.inscribe_result_text, f"{f_id}_inscribe_result"),
            (f.temper_result_text, f"{f_id}_temper_result"),
            (f.quench_result_text, f"{f_id}_quench_result"),
        ]:
            errs = linter.lint_text(text, context=context, check_readability=True)
            grade = flesch_kincaid_grade(text)
            assert not errs, f"Hemingway lint errors in {context}: {errs} (grade={grade})"
            assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in {context}"

    # Rank descriptions
    for tier in ARTIFICER_RANKS:
        errs = linter.lint_text(tier["desc"], context=f"rank_{tier['count']}", check_readability=True)
        grade = flesch_kincaid_grade(tier["desc"])
        assert not errs, f"Hemingway lint errors in rank {tier['count']}: {errs} (grade={grade})"
        assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in rank {tier['count']}"


def test_forge_inscribe_execution():
    """Verify inscribing an ancient runeforge sets flags, awards runes and forge mastery, and logs events."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="AnvilStriker",
        ancestry="Highlander",
        background="blacksmith",
        attributes={"strength": 14, "wits": 12, "endurance": 12},
        skills={"cunning": 2, "athletics": 2},
        traits=["craftsman"],
        stamina=5,
        max_stamina=10,
        inventory=["item_hammer"],
    )

    state = GameState(
        build_id="af-build-001",
        session_id="forge-session",
        character=char,
        current_region="province_reach",
        current_scene="reach_high_pass_armory",
    )

    legal_acts = [a.id for a in engine.get_legal_actions(state)]
    assert "forge_inscribe_frost_iron" in legal_acts

    # Execute inscribe
    new_state, obs = engine.step(state, "forge_inscribe_frost_iron")
    assert obs.success
    assert new_state.world_flags.get("forge_inscribed_forge_frost_iron") is True
    assert "marker_rune_frost_iron" in new_state.character.markers
    assert "marker_forge_mastery_reach" in new_state.character.markers
    assert new_state.character.stamina == 8  # 5 + 3

    # Check engine progress helper
    prog = engine.get_forge_progress(new_state)
    assert prog["inscribed_count"] == 1
    assert prog["artificer_rank"] == "Journeyman Smith"
    assert prog["active_runes_count"] == 1
    assert prog["active_masteries_count"] == 1


def test_7axis_forge_reactivity():
    """Verify 7-axis qualification (tools, traits, attributes, skills, stamina) for forge inscription."""
    f = ANCIENT_RUNEFORGES["forge_sol_brass"]

    # 1. Qualified via smithing tool item
    char_item = CharacterSheet(
        name="ItemSmith", ancestry="Human", background="Scout", inventory=["furnace_tongs"], stamina=0
    )
    aff_item = get_forge_affordances_for_scene(f.forge_scene, char_item, {})
    assert any(a.id == f.inscribe_action_id for a in aff_item)

    # 2. Qualified via blacksmith trait
    char_trait = CharacterSheet(
        name="TraitSmith", ancestry="Human", background="Scout", traits=["blacksmith"], stamina=0
    )
    aff_trait = get_forge_affordances_for_scene(f.forge_scene, char_trait, {})
    assert any(a.id == f.inscribe_action_id for a in aff_trait)

    # 3. Qualified via high strength attribute
    char_attr = CharacterSheet(
        name="AttrSmith", ancestry="Human", background="Scout", attributes={"strength": 14}, stamina=0
    )
    aff_attr = get_forge_affordances_for_scene(f.forge_scene, char_attr, {})
    assert any(a.id == f.inscribe_action_id for a in aff_attr)

    # 4. Qualified via skill
    char_skill = CharacterSheet(
        name="SkillSmith", ancestry="Human", background="Scout", skills={"athletics": 2}, stamina=0
    )
    aff_skill = get_forge_affordances_for_scene(f.forge_scene, char_skill, {})
    assert any(a.id == f.inscribe_action_id for a in aff_skill)

    # 5. Qualified via physical stamina
    char_stam = CharacterSheet(name="StamSmith", ancestry="Human", background="Scout", stamina=2)
    aff_stam = get_forge_affordances_for_scene(f.forge_scene, char_stam, {})
    assert any(a.id == f.inscribe_action_id for a in aff_stam)

    # 6. Unqualified character with 0 stamina, no tools, low stats
    char_none = CharacterSheet(
        name="Unqualified", ancestry="Human", background="Scout", stamina=0, attributes={"strength": 10}, skills={"athletics": 0}
    )
    aff_none = get_forge_affordances_for_scene(f.forge_scene, char_none, {})
    assert not any(a.id == f.inscribe_action_id for a in aff_none)


def test_field_rune_tempering_and_quench():
    """Verify tempering a rune in the field and quenching at the armory forge."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="FieldSmith",
        ancestry="Highlander",
        background="blacksmith",
        markers=["marker_rune_frost_iron"],
        stamina=5,
    )

    # 1. In the field (e.g. at bazaar_center or another scene)
    field_state = GameState(
        build_id="af-build-001",
        session_id="field-temper-session",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
        world_flags={"forge_inscribed_forge_frost_iron": True},
    )

    legal_acts = [a.id for a in engine.get_legal_actions(field_state)]
    assert "forge_temper_frost_iron" in legal_acts

    # Execute tempering in field
    tempered_state, obs = engine.step(field_state, "forge_temper_frost_iron")
    assert obs.success
    assert tempered_state.world_flags.get("forge_tempered_forge_frost_iron") is True
    assert "marker_tempered_forge_frost_iron" in tempered_state.character.markers
    assert tempered_state.character.stamina == 8  # 5 + 3

    # Now tempering is no longer available in field
    subsequent_acts = [a.id for a in engine.get_legal_actions(tempered_state)]
    assert "forge_temper_frost_iron" not in subsequent_acts

    # 2. Return to reach_high_pass_armory and quench crucible
    forge_state = tempered_state.evolve(
        current_region="province_reach",
        current_scene="reach_high_pass_armory",
    )
    forge_acts = [a.id for a in engine.get_legal_actions(forge_state)]
    assert "forge_quench_frost_iron" in forge_acts

    # Step quench
    renewed_state, renew_obs = engine.step(forge_state, "forge_quench_frost_iron")
    assert renew_obs.success
    assert renewed_state.world_flags.get("forge_tempered_forge_frost_iron") is False
    assert renewed_state.character.stamina == 10  # 8 + 2


def test_artificer_rank_progression():
    """Verify progressive unlock of artificer ranks across 0 to 6 runeforges."""
    assert get_artificer_rank(0)["title"] == "Apprentice Striker"
    assert get_artificer_rank(1)["title"] == "Journeyman Smith"
    assert get_artificer_rank(2)["title"] == "Anvil Craftsman"
    assert get_artificer_rank(3)["title"] == "Master Artificer"
    assert get_artificer_rank(4)["title"] == "Guild Metallurgist"
    assert get_artificer_rank(5)["title"] == "Grand Anvilmaster"
    assert get_artificer_rank(6)["title"] == "Continental Forgemaster"

    flags: Dict[str, Any] = {}
    markers = []
    for idx, f in enumerate(ANCIENT_RUNEFORGES.values(), start=1):
        flags[f"forge_inscribed_{f.id}"] = True
        markers.append(f.rune_marker)
        prog = evaluate_forge_progress(flags, [], markers)
        assert prog["inscribed_count"] == idx
        assert prog["active_runes_count"] == idx

    final_prog = evaluate_forge_progress(flags, [], markers)
    assert final_prog["artificer_rank"] == "Continental Forgemaster"
    assert final_prog["progress_pct"] == 100.0


def test_forge_replay_determinism():
    """Verify bit-for-bit replay determinism across inscribe and rune tempering transitions."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    def run_trajectory():
        char = CharacterSheet(
            name="DeterministicSmith",
            ancestry="Highlander",
            background="blacksmith",
            traits=["blacksmith"],
            stamina=10,
            inventory=["smith_hammer"],
        )
        s = GameState(
            build_id="af-build-001",
            session_id="det-forge-session",
            character=char,
            current_region="province_reach",
            current_scene="reach_high_pass_armory",
        )
        s, _ = engine.step(s, "forge_inscribe_frost_iron")
        s, _ = engine.step(s, "forge_temper_frost_iron")
        s, _ = engine.step(s, "forge_quench_frost_iron")
        return s.fingerprint()

    fp1 = run_trajectory()
    fp2 = run_trajectory()
    assert fp1 == fp2, "Replay execution produced diverging state fingerprints!"


def test_asgi_forge_endpoint():
    """Verify GET and HEAD /api/game/forge endpoint returns correct metadata."""
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

    # 1. GET /api/game/forge
    status, headers, body = asyncio.run(run_asgi("/api/game/forge", "GET"))
    assert status == 200
    assert b"application/json" in headers.get(b"content-type", b"")
    data = json.loads(body.decode("utf-8"))
    assert data["total_forges"] == 6
    assert len(data["forges"]) == 6

    # 2. HEAD /api/game/forge
    h_status, h_headers, h_body = asyncio.run(run_asgi("/api/game/forge", "HEAD"))
    assert h_status == 200
    assert len(h_body) == 0
