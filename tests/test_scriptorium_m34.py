"""Tests for Milestone 34: Continental Scriptoriums, Illuminator Desks & Master Calligrapher System."""
import asyncio
import json
from typing import Dict, Any

from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.scriptorium import (
    CANONICAL_SCRIPTORIUMS,
    CALLIGRAPHER_RANKS,
    get_calligrapher_rank,
    evaluate_scriptorium_progress,
    get_scriptorium_affordances_for_scene,
)
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import ProseLinter, flesch_kincaid_grade, word_count
from app import app


def test_scriptorium_registry_integrity():
    """Verify all 6 canonical scriptoriums exist, link to real quarters scenes, and have valid fields."""
    assert len(CANONICAL_SCRIPTORIUMS) == 6
    registry = build_world_registry()
    all_scenes = set()
    for reg in registry.values():
        all_scenes.update(reg.scenes.keys())

    for s_id, s in CANONICAL_SCRIPTORIUMS.items():
        assert s.id == s_id
        assert s.quarters_scene in all_scenes, f"Quarters scene {s.quarters_scene} not found in world registry!"
        assert s.name
        assert s.province in [
            "The Reach",
            "The Scorchwaste",
            "The Sunken Hollows",
            "The High Court",
            "The Lowlands",
            "Central Crossroads",
        ]
        assert s.icon
        assert s.domain
        assert s.inscribe_action_id.startswith("scribe_inscribe_")
        assert s.recite_action_id.startswith("scribe_recite_")
        assert s.renew_action_id.startswith("scribe_renew_")
        assert s.manuscript_marker.startswith("marker_manuscript_")
        assert s.mastery_marker.startswith("marker_scribe_mastery_")


def test_scriptorium_hemingway_compliance():
    """Verify all scriptorium descriptions, result texts, and rank descriptions satisfy Hemingway prose."""
    linter = ProseLinter(min_readability_grade=6.0, max_readability_grade=8.0)

    for s_id, s in CANONICAL_SCRIPTORIUMS.items():
        # Action labels <= 3 words
        for label, lbl_name in [
            (s.inscribe_action_label, f"{s_id}_inscribe_label"),
            (s.recite_action_label, f"{s_id}_recite_label"),
            (s.renew_action_label, f"{s_id}_renew_label"),
        ]:
            wc = word_count(label)
            assert 1 <= wc <= 3, f"Label {lbl_name} '{label}' has {wc} words (must be 1-3)"

        # Text bodies: FKGL in [6.0, 8.0], <= 18 words/sent, 1-3 sentences, 0 purple words
        for text, context in [
            (s.description, f"{s_id}_desc"),
            (s.inscribe_result_text, f"{s_id}_inscribe_result"),
            (s.recite_result_text, f"{s_id}_recite_result"),
            (s.renew_result_text, f"{s_id}_renew_result"),
        ]:
            errs = linter.lint_text(text, context=context, check_readability=True)
            grade = flesch_kincaid_grade(text)
            assert not errs, f"Hemingway lint errors in {context}: {errs} (grade={grade})"
            assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in {context}"

    # Rank descriptions
    for tier in CALLIGRAPHER_RANKS:
        errs = linter.lint_text(tier["desc"], context=f"rank_{tier['count']}", check_readability=True)
        grade = flesch_kincaid_grade(tier["desc"])
        assert not errs, f"Hemingway lint errors in rank {tier['count']}: {errs} (grade={grade})"
        assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in rank {tier['count']}"


def test_scriptorium_inscribe_execution():
    """Verify inscribing an ancient manuscript sets flags, awards markers, and logs events."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="HighlandScholar",
        ancestry="Highlander",
        background="scholar",
        attributes={"wits": 14, "cunning": 12, "endurance": 12},
        skills={"lore": 2, "cunning": 2},
        traits=["scholar"],
        stamina=5,
        max_stamina=10,
        inventory=["quill_and_ink"],
    )

    state = GameState(
        build_id="af-build-001",
        session_id="scriptorium-session",
        character=char,
        current_region="province_reach",
        current_scene="reach_high_pass_quarters",
    )

    legal_acts = [a.id for a in engine.get_legal_actions(state)]
    assert "scribe_inscribe_glacial_chronicle" in legal_acts

    # Execute inscribe
    new_state, obs = engine.step(state, "scribe_inscribe_glacial_chronicle")
    assert obs.success
    assert new_state.world_flags.get("scribe_inscribed_scribe_glacial_chronicle") is True
    assert "marker_manuscript_glacial_chronicle" in new_state.character.markers
    assert "marker_scribe_mastery_reach" in new_state.character.markers
    assert new_state.character.stamina == 8  # 5 + 3

    # Check engine progress helper
    prog = engine.get_scriptorium_progress(new_state)
    assert prog["inscribed_count"] == 1
    assert prog["calligrapher_rank"] == "Apprentice Scribe"
    assert prog["active_manuscript_count"] == 1
    assert prog["active_masteries_count"] == 1


def test_7axis_scriptorium_reactivity():
    """Verify 7-axis qualification (tools, traits, attributes, skills, stamina) for manuscript transcription."""
    s = CANONICAL_SCRIPTORIUMS["scribe_sunfire_papyrus"]

    # 1. Qualified via calligraphy tool item
    char_item = CharacterSheet(
        name="ItemScribe", ancestry="Human", background="Scout", inventory=["parchment_roll"], stamina=0
    )
    aff_item = get_scriptorium_affordances_for_scene(s.quarters_scene, char_item, {})
    assert any(a.id == s.inscribe_action_id for a in aff_item)

    # 2. Qualified via scribe trait
    char_trait = CharacterSheet(
        name="TraitScribe", ancestry="Human", background="Scout", traits=["scribe"], stamina=0
    )
    aff_trait = get_scriptorium_affordances_for_scene(s.quarters_scene, char_trait, {})
    assert any(a.id == s.inscribe_action_id for a in aff_trait)

    # 3. Qualified via high attribute
    char_attr = CharacterSheet(
        name="AttrScribe", ancestry="Human", background="Scout", attributes={"wits": 14}, stamina=0
    )
    aff_attr = get_scriptorium_affordances_for_scene(s.quarters_scene, char_attr, {})
    assert any(a.id == s.inscribe_action_id for a in aff_attr)

    # 4. Qualified via skill
    char_skill = CharacterSheet(
        name="SkillScribe", ancestry="Human", background="Scout", skills={"lore": 2}, stamina=0
    )
    aff_skill = get_scriptorium_affordances_for_scene(s.quarters_scene, char_skill, {})
    assert any(a.id == s.inscribe_action_id for a in aff_skill)

    # 5. Qualified via physical stamina
    char_stam = CharacterSheet(name="StamScribe", ancestry="Human", background="Scout", stamina=2)
    aff_stam = get_scriptorium_affordances_for_scene(s.quarters_scene, char_stam, {})
    assert any(a.id == s.inscribe_action_id for a in aff_stam)

    # 6. Unqualified character with 0 stamina, no tools, low stats
    char_none = CharacterSheet(
        name="Unqualified", ancestry="Human", background="Scout", stamina=0, attributes={"wits": 10}, skills={"lore": 0}
    )
    aff_none = get_scriptorium_affordances_for_scene(s.quarters_scene, char_none, {})
    assert not any(a.id == s.inscribe_action_id for a in aff_none)


def test_field_manuscript_recitation_and_renewal():
    """Verify reciting manuscript in the field and renewing ink at the quarters desk."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="FieldCalligrapher",
        ancestry="Highlander",
        background="scribe",
        markers=["marker_manuscript_glacial_chronicle"],
        stamina=5,
    )

    # 1. In the field (e.g. at bazaar_center or another scene)
    field_state = GameState(
        build_id="af-build-001",
        session_id="field-scribe-session",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
        world_flags={"scribe_inscribed_scribe_glacial_chronicle": True},
    )

    legal_acts = [a.id for a in engine.get_legal_actions(field_state)]
    assert "scribe_recite_glacial_chronicle" in legal_acts

    # Execute recite in field
    recited_state, obs = engine.step(field_state, "scribe_recite_glacial_chronicle")
    assert obs.success
    assert recited_state.world_flags.get("scribe_recited_scribe_glacial_chronicle") is True
    assert "marker_recited_scribe_glacial_chronicle" in recited_state.character.markers
    assert recited_state.character.stamina == 8  # 5 + 3

    # Now recite is no longer available in field (already recited)
    subsequent_acts = [a.id for a in engine.get_legal_actions(recited_state)]
    assert "scribe_recite_glacial_chronicle" not in subsequent_acts

    # 2. Return to reach_high_pass_quarters and renew ink
    quarters_state = recited_state.evolve(
        current_region="province_reach",
        current_scene="reach_high_pass_quarters",
    )
    quarters_acts = [a.id for a in engine.get_legal_actions(quarters_state)]
    assert "scribe_renew_glacial_chronicle" in quarters_acts

    # Step renew
    renewed_state, renew_obs = engine.step(quarters_state, "scribe_renew_glacial_chronicle")
    assert renew_obs.success
    assert renewed_state.world_flags.get("scribe_recited_scribe_glacial_chronicle") is False
    assert renewed_state.character.stamina == 10  # 8 + 2


def test_calligrapher_rank_progression():
    """Verify progressive unlock of calligrapher ranks across 0 to 6 scriptoriums."""
    assert get_calligrapher_rank(0)["title"] == "Novice Copyist"
    assert get_calligrapher_rank(1)["title"] == "Apprentice Scribe"
    assert get_calligrapher_rank(2)["title"] == "Illuminator Craftsman"
    assert get_calligrapher_rank(3)["title"] == "Master Calligrapher"
    assert get_calligrapher_rank(4)["title"] == "Charter Chancellor"
    assert get_calligrapher_rank(5)["title"] == "High Archivist"
    assert get_calligrapher_rank(6)["title"] == "Continental Grandmaster Scribe"

    flags: Dict[str, Any] = {}
    markers = []
    for idx, s in enumerate(CANONICAL_SCRIPTORIUMS.values(), start=1):
        flags[f"scribe_inscribed_{s.id}"] = True
        markers.append(s.manuscript_marker)
        prog = evaluate_scriptorium_progress(flags, [], markers)
        assert prog["inscribed_count"] == idx
        assert prog["active_manuscript_count"] == idx

    final_prog = evaluate_scriptorium_progress(flags, [], markers)
    assert final_prog["calligrapher_rank"] == "Continental Grandmaster Scribe"
    assert final_prog["progress_pct"] == 100.0


def test_scriptorium_replay_determinism():
    """Verify bit-for-bit replay determinism across inscribe, recite, and renew transitions."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    def run_trajectory():
        char = CharacterSheet(
            name="DeterministicScribe",
            ancestry="Highlander",
            background="scholar",
            traits=["scribe"],
            stamina=10,
            inventory=["quill_and_ink"],
        )
        s = GameState(
            build_id="af-build-001",
            session_id="det-scribe-session",
            character=char,
            current_region="province_reach",
            current_scene="reach_high_pass_quarters",
        )
        s, _ = engine.step(s, "scribe_inscribe_glacial_chronicle")
        s, _ = engine.step(s, "scribe_recite_glacial_chronicle")
        s, _ = engine.step(s, "scribe_renew_glacial_chronicle")
        return s.fingerprint()

    fp1 = run_trajectory()
    fp2 = run_trajectory()
    assert fp1 == fp2, "Replay execution produced diverging state fingerprints!"


def test_asgi_scriptorium_endpoint():
    """Verify GET and HEAD /api/game/scriptorium endpoint returns correct metadata."""
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

    # 1. GET /api/game/scriptorium
    status, headers, body = asyncio.run(run_asgi("/api/game/scriptorium", "GET"))
    assert status == 200
    assert b"application/json" in headers.get(b"content-type", b"")
    data = json.loads(body.decode("utf-8"))
    assert data["total_scriptoriums"] == 6
    assert len(data["scriptoriums"]) == 6

    # 2. HEAD /api/game/scriptorium
    h_status, h_headers, h_body = asyncio.run(run_asgi("/api/game/scriptorium", "HEAD"))
    assert h_status == 200
    assert len(h_body) == 0
