"""Milestone 28 Test Suite: Continental Ancient Shrines, Relic Offerings & Divine Blessings System.

Verifies:
1. Ancient Shrines Registry & Field Integrity (6 Shrines: 5 Provincial Titans + 1 Crossroads Pantheon).
2. Strict Hemingway Prose Compliance (FKGL 6.0-8.0, <= 18 words/sent, 1-3 sentences, 0 purple words, <= 3 words per label).
3. 7-Axis Consecration Affordance Synthesis & Execution at Regional Sanctums.
4. Dynamic Field Invocations Anywhere in the Continent & Aura Marker Grants.
5. Sanctum Blessing Attunement Renewal Mechanics.
6. Continental Pilgrim Rank Progression (Unanointed Wanderer to Avatar of the Five Titans).
7. Pure Determinism & Bit-for-Bit Replay Fingerprinting with Shrine Interactions.
8. Vercel Stateless ASGI Endpoints (GET/HEAD /api/game/shrines, /new, /step).
"""
import pytest
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CHARACTER_PRESETS
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.state import GameState
from adventure_forge.core.shrines import (
    ANCIENT_SHRINES,
    PILGRIM_RANKS,
    get_pilgrim_rank,
    get_shrines_progress,
    evaluate_shrines_progress,
    get_shrine_affordances_for_scene,
)
from adventure_forge.linter.prose_linter import (
    flesch_kincaid_grade,
    split_sentences,
    word_count,
    FORBIDDEN_PURPLE_WORDS,
)


@pytest.fixture
def engine():
    registry = build_world_registry()
    return AdventureEngine(registry)


@pytest.fixture
def base_state(engine):
    preset = CHARACTER_PRESETS["cutpurse"]
    return GameState(
        build_id="test-build",
        session_id="test-shrines-m28",
        character=preset.character,
        current_region=preset.start_region,
        current_scene=preset.start_scene,
        rng=DeterministicRNG.from_seed(42),
    )


def test_shrines_registry_count_and_mapping():
    """Verify all 6 shrines are registered with valid provinces, scenes, and fields."""
    assert len(ANCIENT_SHRINES) == 6
    expected_keys = {
        "shrine_khoros",
        "shrine_sol_ankh",
        "shrine_thalassa",
        "shrine_aurelius",
        "shrine_mara",
        "shrine_wayfarer",
    }
    assert set(ANCIENT_SHRINES.keys()) == expected_keys

    provinces = {s.province for s in ANCIENT_SHRINES.values()}
    assert "The Reach" in provinces
    assert "The Scorchwaste" in provinces
    assert "The Sunken Hollows" in provinces
    assert "The High Court" in provinces
    assert "The Lowlands" in provinces
    assert "Central Crossroads" in provinces

    for s in ANCIENT_SHRINES.values():
        assert s.id.startswith("shrine_")
        assert len(s.name) > 0
        assert len(s.deity) > 0
        assert len(s.domain) > 0
        assert len(s.icon) > 0
        assert len(s.sanctum_scene) > 0
        assert s.blessing_marker.startswith("marker_blessing_")
        assert s.aura_marker.startswith("marker_aura_")


def test_shrines_hemingway_prose_compliance():
    """Verify all shrine descriptions, labels, and results strictly conform to Hemingway rules."""
    for s in ANCIENT_SHRINES.values():
        # Action labels must be 1 to 3 words
        for label_name, label in [
            ("consecrate_label", s.consecrate_action_label),
            ("invoke_label", s.invoke_action_label),
            ("renew_label", s.renew_action_label),
        ]:
            words = label.split()
            assert 1 <= len(words) <= 3, f"Label '{label}' for {s.id} {label_name} must be 1-3 words"

        # Prose texts: description, consecrate_result, invoke_result, renew_result
        for text_name, text in [
            ("description", s.description),
            ("consecrate_result", s.consecrate_result_text),
            ("invoke_result", s.invoke_result_text),
            ("renew_result", s.renew_result_text),
        ]:
            sents = split_sentences(text)
            assert 1 <= len(sents) <= 3, f"Sentence count for {s.id} {text_name} must be 1-3, got {len(sents)}"
            for sent in sents:
                sent_words = sent.split()
                assert len(sent_words) <= 18, f"Sentence '{sent}' in {s.id} {text_name} exceeds 18 words ({len(sent_words)})"

            grade = flesch_kincaid_grade(text)
            assert 6.0 <= grade <= 8.0, f"FKGL for {s.id} {text_name} must be 6.0-8.0, got {grade} ('{text}')"
            assert word_count(text) > 0, "Word count must be positive"

            low = text.lower()
            for purple in FORBIDDEN_PURPLE_WORDS:
                assert purple not in low, f"Purple word '{purple}' found in {s.id} {text_name}"


def test_shrine_consecration_at_sanctum(engine, base_state):
    """Verify character can consecrate a shrine at its sanctum scene and acquire the blessing marker."""
    shrine = ANCIENT_SHRINES["shrine_khoros"]
    state = base_state.evolve(current_scene=shrine.sanctum_scene)

    # Initial state: not consecrated, no blessing
    prog = engine.get_shrines_progress(state)
    assert prog["consecrated_count"] == 0
    assert prog["active_blessings_count"] == 0

    # Observe legal actions at sanctum scene
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert shrine.consecrate_action_id in action_ids

    # Step consecration action
    new_state, new_obs = engine.step(state, shrine.consecrate_action_id)
    assert new_obs.success
    assert new_state.world_flags.get(f"shrine_consecrated_{shrine.id}") is True
    assert shrine.blessing_marker in new_state.character.markers

    # Progress updated
    new_prog = engine.get_shrines_progress(new_state)
    assert new_prog["consecrated_count"] == 1
    assert new_prog["active_blessings_count"] == 1
    assert new_prog["pilgrim_rank"] == "Shrine Pilgrim"


def test_field_invocation_and_renewal_lifecycle(engine, base_state):
    """Verify full blessing lifecycle: consecration -> field invocation -> renewal at sanctum."""
    shrine = ANCIENT_SHRINES["shrine_thalassa"]
    # Start character with the blessing already consecrated
    state = base_state.evolve(
        current_scene="bazaar_center",
        character=base_state.character.modify(markers=list(base_state.character.markers) + [shrine.blessing_marker]),
        world_flags=dict(base_state.world_flags, **{f"shrine_consecrated_{shrine.id}": True}),
    )

    # In the field (bazaar_center): invocation affordance is synthesized
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert shrine.invoke_action_id in action_ids

    # Execute invocation anywhere in the field
    invoked_state, inv_obs = engine.step(state, shrine.invoke_action_id)
    assert inv_obs.success
    assert invoked_state.world_flags.get(f"blessing_invoked_{shrine.id}") is True
    assert shrine.aura_marker in invoked_state.character.markers

    # Once invoked, invocation is no longer available
    obs_after = engine.observe(invoked_state)
    action_ids_after = [a["id"] for a in obs_after.legal_actions]
    assert shrine.invoke_action_id not in action_ids_after

    # Travel to the sanctum to renew blessing
    sanctum_state = invoked_state.evolve(current_scene=shrine.sanctum_scene)
    sanctum_obs = engine.observe(sanctum_state)
    sanctum_action_ids = [a["id"] for a in sanctum_obs.legal_actions]
    assert shrine.renew_action_id in sanctum_action_ids

    # Execute renewal
    renewed_state, ren_obs = engine.step(sanctum_state, shrine.renew_action_id)
    assert ren_obs.success
    assert renewed_state.world_flags.get(f"blessing_invoked_{shrine.id}") is False

    # Invocation available again in legal actions
    obs_renewed = engine.observe(renewed_state)
    assert shrine.invoke_action_id in [a["id"] for a in obs_renewed.legal_actions]


def test_pilgrim_rank_progression(base_state):
    """Verify rank tiers scale accurately from 0 to 6 consecrated shrines."""
    assert len(PILGRIM_RANKS) == 7
    assert get_pilgrim_rank(0)["title"] == "Unanointed Wanderer"
    assert get_pilgrim_rank(1)["title"] == "Shrine Pilgrim"
    assert get_pilgrim_rank(2)["title"] == "Consecrated Devotee"
    assert get_pilgrim_rank(3)["title"] == "Temple Hierophant"
    assert get_pilgrim_rank(4)["title"] == "Provincial Exarch"
    assert get_pilgrim_rank(5)["title"] == "Continental Hierarch"
    assert get_pilgrim_rank(6)["title"] == "Avatar of the Five Titans"

    # Direct evaluation function testing
    eval_prog = evaluate_shrines_progress(
        world_flags={"shrine_consecrated_shrine_khoros": True},
        inventory=["ice_lotus"],
        markers=["marker_blessing_khoros"],
        current_scene="reach_frost_cavern_sanctum",
    )
    assert eval_prog["consecrated_count"] == 1
    assert eval_prog["active_blessings_count"] == 1
    assert eval_prog["current_scene_shrine"] == "shrine_khoros"

    # GameState progress wrapper
    state_prog = get_shrines_progress(base_state)
    assert state_prog["consecrated_count"] == 0
    assert state_prog["total_shrines"] == 6

    # Direct scene affordance synthesis check
    affordances = get_shrine_affordances_for_scene(
        scene_id="reach_frost_cavern_sanctum",
        character=base_state.character,
        world_flags={},
    )
    assert any(a.id == "shrine_consecrate_khoros" for a in affordances)


def test_shrines_replay_determinism(engine, base_state):
    """Verify identical SHA-256 state fingerprints on identical action traces with shrines."""
    shrine = ANCIENT_SHRINES["shrine_wayfarer"]
    # Character starts at bazaar_center where the Wayfarer shrine is located
    state1 = base_state.evolve(current_scene="bazaar_center")
    state2 = base_state.evolve(current_scene="bazaar_center")

    assert state1.fingerprint() == state2.fingerprint()

    # Step consecration
    s1, _ = engine.step(state1, shrine.consecrate_action_id)
    s2, _ = engine.step(state2, shrine.consecrate_action_id)
    assert s1.fingerprint() == s2.fingerprint()

    # Step invocation
    s1_inv, _ = engine.step(s1, shrine.invoke_action_id)
    s2_inv, _ = engine.step(s2, shrine.invoke_action_id)
    assert s1_inv.fingerprint() == s2_inv.fingerprint()


def test_shrines_asgi_endpoint():
    """Verify GET and HEAD /api/game/shrines and integration in /api/game/new."""
    import asyncio
    import json
    from app import app

    async def run_asgi(path: str, method: str = "GET", body_bytes: bytes = b""):
        response_data = {"status": 0, "headers": [], "body": b""}

        async def receive():
            return {"type": "http.request", "body": body_bytes, "more_body": False}

        async def send(message):
            if message["type"] == "http.response.start":
                response_data["status"] = message["status"]
                response_data["headers"] = message.get("headers", [])
            elif message["type"] == "http.response.body":
                response_data["body"] += message.get("body", b"")

        scope = {
            "type": "http",
            "method": method,
            "path": path,
            "headers": [(b"host", b"localhost"), (b"content-type", b"application/json")],
        }
        await app(scope, receive, send)
        return response_data

    # 1. Test GET /api/game/shrines
    res_get = asyncio.run(run_asgi("/api/game/shrines", "GET"))
    assert res_get["status"] == 200
    data = json.loads(res_get["body"].decode("utf-8"))
    assert data["total_shrines"] == 6
    assert len(data["shrines"]) == 6

    # 2. Test HEAD /api/game/shrines
    res_head = asyncio.run(run_asgi("/api/game/shrines", "HEAD"))
    assert res_head["status"] == 200
    assert res_head["body"] == b""

    # 3. Test POST /api/game/new returns shrines progress
    new_req_body = json.dumps({"preset": "cutpurse", "seed": 42}).encode("utf-8")
    res_new = asyncio.run(run_asgi("/api/game/new", "POST", new_req_body))
    assert res_new["status"] == 200
    new_data = json.loads(res_new["body"].decode("utf-8"))
    assert "shrines" in new_data
    assert new_data["shrines"]["total_shrines"] == 6
    assert new_data["shrines"]["consecrated_count"] == 0
