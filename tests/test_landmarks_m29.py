"""Tests for Milestone 29: Continental Survey Landmarks, Lookout Panoramas & Master Cartographer System."""
import asyncio
import json
from typing import Dict, Any

from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.landmarks import (
    SURVEY_LANDMARKS,
    CARTOGRAPHER_RANKS,
    get_cartographer_rank,
    evaluate_landmarks_progress,
    get_landmark_affordances_for_scene,
)
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import ProseLinter, flesch_kincaid_grade, word_count
from app import app


def test_landmarks_registry_integrity():
    """Verify all 6 canonical landmarks exist, link to real summit scenes, and have valid fields."""
    assert len(SURVEY_LANDMARKS) == 6
    registry = build_world_registry()
    all_scenes = set()
    for reg in registry.values():
        all_scenes.update(reg.scenes.keys())

    for lm_id, lm in SURVEY_LANDMARKS.items():
        assert lm.id == lm_id
        assert lm.overlook_scene in all_scenes, f"Overlook scene {lm.overlook_scene} not found in world registry!"
        assert lm.name
        assert lm.province in ["The Reach", "The Scorchwaste", "The Sunken Hollows", "The High Court", "The Lowlands", "Central Crossroads"]
        assert lm.icon
        assert lm.domain
        assert lm.survey_action_id.startswith("landmark_survey_")
        assert lm.study_action_id.startswith("landmark_study_")
        assert lm.triangulate_action_id.startswith("landmark_triangulate_")
        assert lm.survey_marker.startswith("marker_survey_")
        assert lm.mastery_marker.startswith("marker_mastery_")


def test_landmarks_hemingway_compliance():
    """Verify all landmark descriptions, result texts, and rank descriptions satisfy Hemingway prose."""
    linter = ProseLinter(min_readability_grade=6.0, max_readability_grade=8.0)

    for lm_id, lm in SURVEY_LANDMARKS.items():
        # Action labels <= 3 words
        for label, lbl_name in [
            (lm.survey_action_label, f"{lm_id}_survey_label"),
            (lm.study_action_label, f"{lm_id}_study_label"),
            (lm.triangulate_action_label, f"{lm_id}_triangulate_label"),
        ]:
            wc = word_count(label)
            assert 1 <= wc <= 3, f"Label {lbl_name} '{label}' has {wc} words (must be 1-3)"

        # Text bodies: FKGL in [6.0, 8.0], <= 18 words/sent, 1-3 sentences, 0 purple words
        for text, context in [
            (lm.description, f"{lm_id}_desc"),
            (lm.survey_result_text, f"{lm_id}_survey_result"),
            (lm.study_result_text, f"{lm_id}_study_result"),
            (lm.triangulate_result_text, f"{lm_id}_triangulate_result"),
        ]:
            errs = linter.lint_text(text, context=context, check_readability=True)
            grade = flesch_kincaid_grade(text)
            assert not errs, f"Hemingway lint errors in {context}: {errs} (grade={grade})"
            assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in {context}"

    # Rank descriptions
    for tier in CARTOGRAPHER_RANKS:
        errs = linter.lint_text(tier["desc"], context=f"rank_{tier['count']}", check_readability=True)
        grade = flesch_kincaid_grade(tier["desc"])
        assert not errs, f"Hemingway lint errors in rank {tier['count']}: {errs} (grade={grade})"
        assert 6.0 <= grade <= 8.0, f"Grade {grade} out of [6.0, 8.0] in rank {tier['count']}"


def test_landmark_survey_execution():
    """Verify surveying an overlook summit sets flags, awards markers and stamina, and logs events."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="Cartographer",
        ancestry="Highlander",
        background="surveyor",
        attributes={"strength": 12, "agility": 14, "endurance": 12},
        skills={"cunning": 3, "lore": 2},
        traits=["pathfinder"],
        stamina=5,
        max_stamina=10,
        inventory=["item_spyglass"],
    )

    state = GameState(
        build_id="af-build-001",
        session_id="survey-session",
        character=char,
        current_region="province_reach",
        current_scene="reach_high_pass_overlook",
    )

    legal_acts = [a.id for a in engine.get_legal_actions(state)]
    assert "landmark_survey_reach_pass" in legal_acts

    # Execute survey
    new_state, obs = engine.step(state, "landmark_survey_reach_pass")
    assert obs.success
    assert new_state.world_flags.get("landmark_surveyed_landmark_reach_pass") is True
    assert "marker_survey_reach_pass" in new_state.character.markers
    assert "marker_mastery_reach" in new_state.character.markers
    assert new_state.character.stamina == 8  # 5 + 3

    # Check engine progress helper
    prog = engine.get_landmarks_progress(new_state)
    assert prog["surveyed_count"] == 1
    assert prog["cartographer_rank"] == "Regional Scout"
    assert prog["active_charts_count"] == 1
    assert prog["active_masteries_count"] == 1


def test_7axis_survey_reactivity():
    """Verify 7-axis qualification (tools, traits, attributes, skills, stamina) for landmark survey."""
    lm = SURVEY_LANDMARKS["landmark_scorchwaste_dune"]

    # 1. Qualified via instrument item
    char_item = CharacterSheet(name="ItemScout", ancestry="Human", background="Scout", inventory=["continental_compass"], stamina=0)
    aff_item = get_landmark_affordances_for_scene(lm.overlook_scene, char_item, {})
    assert any(a.id == lm.survey_action_id for a in aff_item)

    # 2. Qualified via trait
    char_trait = CharacterSheet(name="TraitScout", ancestry="Human", background="Scout", traits=["far_sighted"], stamina=0)
    aff_trait = get_landmark_affordances_for_scene(lm.overlook_scene, char_trait, {})
    assert any(a.id == lm.survey_action_id for a in aff_trait)

    # 3. Qualified via high attribute
    char_attr = CharacterSheet(name="AttrScout", ancestry="Human", background="Scout", attributes={"wits": 14}, stamina=0)
    aff_attr = get_landmark_affordances_for_scene(lm.overlook_scene, char_attr, {})
    assert any(a.id == lm.survey_action_id for a in aff_attr)

    # 4. Qualified via skill
    char_skill = CharacterSheet(name="SkillScout", ancestry="Human", background="Scout", skills={"cunning": 2}, stamina=0)
    aff_skill = get_landmark_affordances_for_scene(lm.overlook_scene, char_skill, {})
    assert any(a.id == lm.survey_action_id for a in aff_skill)

    # 5. Qualified via physical stamina
    char_stam = CharacterSheet(name="StamScout", ancestry="Human", background="Scout", stamina=2)
    aff_stam = get_landmark_affordances_for_scene(lm.overlook_scene, char_stam, {})
    assert any(a.id == lm.survey_action_id for a in aff_stam)

    # 6. Unqualified character with 0 stamina, no tools, low stats
    char_none = CharacterSheet(name="Unqualified", ancestry="Human", background="Scout", stamina=0, attributes={"wits": 10}, skills={"cunning": 0})
    aff_none = get_landmark_affordances_for_scene(lm.overlook_scene, char_none, {})
    assert not any(a.id == lm.survey_action_id for a in aff_none)


def test_field_chart_study_and_triangulation():
    """Verify studying a chart in the field and re-triangulating at the overlook summit."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="FieldCartographer",
        ancestry="Highlander",
        background="surveyor",
        markers=["marker_survey_reach_pass"],
        stamina=5,
    )

    # 1. In the field (e.g. at bazaar_center or another scene)
    field_state = GameState(
        build_id="af-build-001",
        session_id="field-study-session",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
        world_flags={"landmark_surveyed_landmark_reach_pass": True},
    )

    legal_acts = [a.id for a in engine.get_legal_actions(field_state)]
    assert "landmark_study_reach_pass" in legal_acts

    # Execute study in field
    studied_state, obs = engine.step(field_state, "landmark_study_reach_pass")
    assert obs.success
    assert studied_state.world_flags.get("landmark_studied_landmark_reach_pass") is True
    assert "marker_studied_landmark_reach_pass" in studied_state.character.markers
    assert studied_state.character.stamina == 8  # 5 + 3

    # Now study is no longer available in field
    subsequent_acts = [a.id for a in engine.get_legal_actions(studied_state)]
    assert "landmark_study_reach_pass" not in subsequent_acts

    # 2. Return to reach_high_pass_overlook and re-triangulate
    summit_state = studied_state.evolve(
        current_region="province_reach",
        current_scene="reach_high_pass_overlook",
    )
    summit_acts = [a.id for a in engine.get_legal_actions(summit_state)]
    assert "landmark_triangulate_reach_pass" in summit_acts

    # Step triangulation
    renewed_state, renew_obs = engine.step(summit_state, "landmark_triangulate_reach_pass")
    assert renew_obs.success
    assert renewed_state.world_flags.get("landmark_studied_landmark_reach_pass") is False
    assert renewed_state.character.stamina == 10  # 8 + 2


def test_cartographer_rank_progression():
    """Verify progressive unlock of cartographer ranks across 0 to 6 landmarks."""
    assert get_cartographer_rank(0)["title"] == "Uncharted Drifter"
    assert get_cartographer_rank(1)["title"] == "Regional Scout"
    assert get_cartographer_rank(2)["title"] == "Topographer"
    assert get_cartographer_rank(3)["title"] == "Continental Cartographer"
    assert get_cartographer_rank(4)["title"] == "Grand Surveyor"
    assert get_cartographer_rank(5)["title"] == "Master of Five Panoramas"
    assert get_cartographer_rank(6)["title"] == "Grand Royal Cartographer"

    flags: Dict[str, Any] = {}
    markers = []
    for idx, lm in enumerate(SURVEY_LANDMARKS.values(), start=1):
        flags[f"landmark_surveyed_{lm.id}"] = True
        markers.append(lm.survey_marker)
        prog = evaluate_landmarks_progress(flags, [], markers)
        assert prog["surveyed_count"] == idx
        assert prog["active_charts_count"] == idx

    final_prog = evaluate_landmarks_progress(flags, [], markers)
    assert final_prog["cartographer_rank"] == "Grand Royal Cartographer"
    assert final_prog["progress_pct"] == 100.0


def test_landmarks_replay_determinism():
    """Verify bit-for-bit replay determinism across survey and chart study transitions."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    def run_trajectory():
        char = CharacterSheet(
            name="DeterministicSurveyor",
            ancestry="Highlander",
            background="surveyor",
            traits=["pathfinder"],
            stamina=10,
            inventory=["item_spyglass"],
        )
        s = GameState(
            build_id="af-build-001",
            session_id="det-survey-session",
            character=char,
            current_region="province_reach",
            current_scene="reach_high_pass_overlook",
        )
        s, _ = engine.step(s, "landmark_survey_reach_pass")
        s, _ = engine.step(s, "landmark_study_reach_pass")
        s, _ = engine.step(s, "landmark_triangulate_reach_pass")
        return s.fingerprint()

    fp1 = run_trajectory()
    fp2 = run_trajectory()
    assert fp1 == fp2, "Replay execution produced diverging state fingerprints!"


def test_asgi_landmarks_endpoint():
    """Verify GET and HEAD /api/game/landmarks endpoint returns correct metadata."""
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

    # 1. GET /api/game/landmarks
    status, headers, body = asyncio.run(run_asgi("/api/game/landmarks", "GET"))
    assert status == 200
    assert b"application/json" in headers.get(b"content-type", b"")
    data = json.loads(body.decode("utf-8"))
    assert data["total_landmarks"] == 6
    assert len(data["landmarks"]) == 6

    # 2. HEAD /api/game/landmarks
    h_status, h_headers, h_body = asyncio.run(run_asgi("/api/game/landmarks", "HEAD"))
    assert h_status == 200
    assert len(h_body) == 0
