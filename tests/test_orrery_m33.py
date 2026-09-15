"""Tests for Milestone 33: Continental Celestial Orreries, Astrolabe Spheres & Master Stargazer System."""
import asyncio
import json
from typing import Dict, Any

from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.orrery import (
    ANCIENT_ORRERIES,
    STARGAZER_RANKS,
    get_stargazer_rank,
    evaluate_orrery_progress,
    get_orrery_affordances_for_scene,
)
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import ProseLinter, flesch_kincaid_grade, word_count
from app import app


def test_orrery_registry_integrity():
    """Verify all 6 canonical orreries exist, link to real chamber scenes, and have valid fields."""
    assert len(ANCIENT_ORRERIES) == 6
    registry = build_world_registry()
    all_scenes = set()
    for reg in registry.values():
        all_scenes.update(reg.scenes.keys())

    for orrery_id, orrery in ANCIENT_ORRERIES.items():
        assert orrery.id == orrery_id
        assert orrery.chamber_scene in all_scenes, f"Chamber scene {orrery.chamber_scene} not found in world registry!"
        assert orrery.name
        assert orrery.province in [
            "The Reach",
            "The Scorchwaste",
            "The Sunken Hollows",
            "The High Court",
            "The Lowlands",
            "Central Crossroads",
        ]
        assert orrery.icon
        assert orrery.domain
        assert orrery.align_action_id.startswith("orrery_align_")
        assert orrery.attune_action_id.startswith("orrery_attune_")
        assert orrery.recalibrate_action_id.startswith("orrery_recalibrate_")
        assert orrery.lens_marker.startswith("marker_lens_")
        assert orrery.mastery_marker.startswith("marker_orrery_mastery_")


def test_orrery_hemingway_compliance():
    """Verify all orrery descriptions, result texts, and rank descriptions satisfy Hemingway prose."""
    linter = ProseLinter(min_readability_grade=6.0, max_readability_grade=8.0)

    for orrery_id, orrery in ANCIENT_ORRERIES.items():
        # Action labels <= 3 words
        for label, lbl_name in [
            (orrery.align_action_label, f"{orrery_id}_align_label"),
            (orrery.attune_action_label, f"{orrery_id}_attune_label"),
            (orrery.recalibrate_action_label, f"{orrery_id}_recalibrate_label"),
        ]:
            wc = word_count(label)
            assert 1 <= wc <= 3, f"Label {lbl_name} '{label}' has {wc} words (must be 1-3)"

        # Text bodies: FKGL in [6.0, 8.0], <= 18 words/sent, 1-3 sentences, 0 purple words
        for text, context in [
            (orrery.description, f"{orrery_id}_desc"),
            (orrery.align_result_text, f"{orrery_id}_align_result"),
            (orrery.attune_result_text, f"{orrery_id}_attune_result"),
            (orrery.recalibrate_result_text, f"{orrery_id}_recalibrate_result"),
        ]:
            errs = linter.lint_text(text, context=context, check_readability=True)
            grade = flesch_kincaid_grade(text)
            assert not errs, f"Hemingway lint errors in {context}: {errs} (grade={grade})"
            assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in {context}"

    # Rank descriptions
    for tier in STARGAZER_RANKS:
        errs = linter.lint_text(tier["desc"], context=f"rank_{tier['count']}", check_readability=True)
        grade = flesch_kincaid_grade(tier["desc"])
        assert not errs, f"Hemingway lint errors in rank {tier['count']}: {errs} (grade={grade})"
        assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in rank {tier['count']}"


def test_orrery_align_execution():
    """Verify aligning an ancient celestial orrery sets flags, awards markers, and logs events."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="StargazerAdept",
        ancestry="Highlander",
        background="scholar",
        attributes={"wits": 14, "cunning": 12, "endurance": 12},
        skills={"lore": 2, "cunning": 2},
        traits=["astronomer"],
        stamina=5,
        max_stamina=10,
        inventory=["brass_astrolabe"],
    )

    state = GameState(
        build_id="af-build-001",
        session_id="orrery-session",
        character=char,
        current_region="province_reach",
        current_scene="reach_iron_spire_chamber",
    )

    legal_acts = [a.id for a in engine.get_legal_actions(state)]
    assert "orrery_align_frost_zenith" in legal_acts

    # Execute align
    new_state, obs = engine.step(state, "orrery_align_frost_zenith")
    assert obs.success
    assert new_state.world_flags.get("orrery_aligned_orrery_frost_zenith") is True
    assert "marker_lens_frost_zenith" in new_state.character.markers
    assert "marker_orrery_mastery_reach" in new_state.character.markers
    assert new_state.character.stamina == 8  # 5 + 3

    # Check engine progress helper
    prog = engine.get_orrery_progress(new_state)
    assert prog["aligned_count"] == 1
    assert prog["stargazer_rank"] == "Apprentice Astrologer"
    assert prog["active_lenses_count"] == 1
    assert prog["active_masteries_count"] == 1


def test_7axis_orrery_reactivity():
    """Verify 7-axis qualification (tools, traits, attributes, skills, stamina) for orrery alignment."""
    orrery = ANCIENT_ORRERIES["orrery_sol_zenith"]

    # 1. Qualified via astrolabe tool item
    char_item = CharacterSheet(
        name="ItemGazer", ancestry="Human", background="Scout", inventory=["star_chart"], stamina=0
    )
    aff_item = get_orrery_affordances_for_scene(orrery.chamber_scene, char_item, {})
    assert any(a.id == orrery.align_action_id for a in aff_item)

    # 2. Qualified via astronomer trait
    char_trait = CharacterSheet(
        name="TraitGazer", ancestry="Human", background="Scout", traits=["astronomer"], stamina=0
    )
    aff_trait = get_orrery_affordances_for_scene(orrery.chamber_scene, char_trait, {})
    assert any(a.id == orrery.align_action_id for a in aff_trait)

    # 3. Qualified via high wits attribute
    char_attr = CharacterSheet(
        name="AttrGazer", ancestry="Human", background="Scout", attributes={"wits": 14}, stamina=0
    )
    aff_attr = get_orrery_affordances_for_scene(orrery.chamber_scene, char_attr, {})
    assert any(a.id == orrery.align_action_id for a in aff_attr)

    # 4. Qualified via skill
    char_skill = CharacterSheet(
        name="SkillGazer", ancestry="Human", background="Scout", skills={"lore": 2}, stamina=0
    )
    aff_skill = get_orrery_affordances_for_scene(orrery.chamber_scene, char_skill, {})
    assert any(a.id == orrery.align_action_id for a in aff_skill)

    # 5. Qualified via physical stamina
    char_stam = CharacterSheet(name="StamGazer", ancestry="Human", background="Scout", stamina=2)
    aff_stam = get_orrery_affordances_for_scene(orrery.chamber_scene, char_stam, {})
    assert any(a.id == orrery.align_action_id for a in aff_stam)

    # 6. Unqualified character with 0 stamina, no tools, low stats
    char_none = CharacterSheet(
        name="Unqualified", ancestry="Human", background="Scout", stamina=0, attributes={"wits": 10}, skills={"lore": 0}
    )
    aff_none = get_orrery_affordances_for_scene(orrery.chamber_scene, char_none, {})
    assert not any(a.id == orrery.align_action_id for a in aff_none)


def test_field_constellation_attunement_and_recalibrate():
    """Verify attuning constellation in the field and recalibrating at the chamber orrery."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="FieldStargazer",
        ancestry="Highlander",
        background="astronomer",
        markers=["marker_lens_frost_zenith"],
        stamina=5,
    )

    # 1. In the field (e.g. at bazaar_center or another scene)
    field_state = GameState(
        build_id="af-build-001",
        session_id="field-orrery-session",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
        world_flags={"orrery_aligned_orrery_frost_zenith": True},
    )

    legal_acts = [a.id for a in engine.get_legal_actions(field_state)]
    assert "orrery_attune_frost_zenith" in legal_acts

    # Execute attune in field
    attuned_state, obs = engine.step(field_state, "orrery_attune_frost_zenith")
    assert obs.success
    assert attuned_state.world_flags.get("orrery_attuned_orrery_frost_zenith") is True
    assert "marker_attuned_orrery_frost_zenith" in attuned_state.character.markers
    assert attuned_state.character.stamina == 8  # 5 + 3

    # Now attune is no longer available in field (already attuned)
    subsequent_acts = [a.id for a in engine.get_legal_actions(attuned_state)]
    assert "orrery_attune_frost_zenith" not in subsequent_acts

    # 2. Return to reach_iron_spire_chamber and recalibrate orrery
    chamber_state = attuned_state.evolve(
        current_region="province_reach",
        current_scene="reach_iron_spire_chamber",
    )
    chamber_acts = [a.id for a in engine.get_legal_actions(chamber_state)]
    assert "orrery_recalibrate_frost_zenith" in chamber_acts

    # Step recalibrate
    renewed_state, renew_obs = engine.step(chamber_state, "orrery_recalibrate_frost_zenith")
    assert renew_obs.success
    assert renewed_state.world_flags.get("orrery_attuned_orrery_frost_zenith") is False
    assert renewed_state.character.stamina == 10  # 8 + 2


def test_stargazer_rank_progression():
    """Verify progressive unlock of stargazer ranks across 0 to 6 celestial orreries."""
    assert get_stargazer_rank(0)["title"] == "Novice Gazer"
    assert get_stargazer_rank(1)["title"] == "Apprentice Astrologer"
    assert get_stargazer_rank(2)["title"] == "Constellation Seeker"
    assert get_stargazer_rank(3)["title"] == "Astromancer"
    assert get_stargazer_rank(4)["title"] == "Master Stargazer"
    assert get_stargazer_rank(5)["title"] == "High Astrologian"
    assert get_stargazer_rank(6)["title"] == "Grand Royal Stargazer"

    flags: Dict[str, Any] = {}
    markers = []
    for idx, orrery in enumerate(ANCIENT_ORRERIES.values(), start=1):
        flags[f"orrery_aligned_{orrery.id}"] = True
        markers.append(orrery.lens_marker)
        prog = evaluate_orrery_progress(flags, [], markers)
        assert prog["aligned_count"] == idx
        assert prog["active_lenses_count"] == idx

    final_prog = evaluate_orrery_progress(flags, [], markers)
    assert final_prog["stargazer_rank"] == "Grand Royal Stargazer"
    assert final_prog["progress_pct"] == 100.0


def test_orrery_replay_determinism():
    """Verify bit-for-bit replay determinism across align, attune, and recalibrate transitions."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    def run_trajectory():
        char = CharacterSheet(
            name="DeterministicStargazer",
            ancestry="Highlander",
            background="scholar",
            traits=["astronomer"],
            stamina=10,
            inventory=["brass_astrolabe"],
        )
        s = GameState(
            build_id="af-build-001",
            session_id="det-orrery-session",
            character=char,
            current_region="province_reach",
            current_scene="reach_iron_spire_chamber",
        )
        s, _ = engine.step(s, "orrery_align_frost_zenith")
        s, _ = engine.step(s, "orrery_attune_frost_zenith")
        s, _ = engine.step(s, "orrery_recalibrate_frost_zenith")
        return s.fingerprint()

    fp1 = run_trajectory()
    fp2 = run_trajectory()
    assert fp1 == fp2, "Replay execution produced diverging state fingerprints!"


def test_asgi_orrery_endpoint():
    """Verify GET and HEAD /api/game/orrery endpoint returns correct metadata."""
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

    # 1. GET /api/game/orrery
    status, headers, body = asyncio.run(run_asgi("/api/game/orrery", "GET"))
    assert status == 200
    assert b"application/json" in headers.get(b"content-type", b"")
    data = json.loads(body.decode("utf-8"))
    assert data["total_orreries"] == 6
    assert len(data["orreries"]) == 6

    # 2. HEAD /api/game/orrery
    h_status, h_headers, h_body = asyncio.run(run_asgi("/api/game/orrery", "HEAD"))
    assert h_status == 200
    assert len(h_body) == 0
