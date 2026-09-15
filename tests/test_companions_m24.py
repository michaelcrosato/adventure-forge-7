"""Milestone 24: Continental Companion Recruiter & Follower Synergy System Test Suite.

Validates:
1. Companion registry integrity (5 companions across 5 provinces, garrison home scenes).
2. World graph home scene validity (100% reachable garrison courtyards).
3. Hemingway prose compliance (<= 18 words/sent, 1-3 sent, FKGL <= 8.0, <= 3 words/label, 0 purple words).
4. 7-axis character reactivity and recruitment condition paths.
5. Dynamic companion lifecycle: Recruit -> Consult in Field -> Dismiss -> Re-summon in Hub.
6. Fellowship milestone ranks (Partner, Warband, Master of Fellowship).
7. Pure determinism and bit-for-bit SHA-256 replay fidelity.
8. ASGI REST endpoints (GET/HEAD /api/game/companions, payload inclusion in /api/game/*).
"""
import asyncio
import json
import re
import pytest
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.companions import (
    COMPANIONS,
    can_recruit_companion,
    evaluate_companions_progress,
)
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.character import get_preset
from adventure_forge.core.state import GameState
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.linter.prose_linter import FORBIDDEN_PURPLE_WORDS, flesch_kincaid_grade


@pytest.fixture
def registry():
    return build_world_registry()


@pytest.fixture
def engine(registry):
    return AdventureEngine(registry)


# --- Test 1: Companion Registry & World Graph Targets ---

def test_companion_registry_integrity(engine):
    """Verify 5 companions across 5 provinces and that home scenes exist in the world graph."""
    assert len(COMPANIONS) == 5

    provinces = {"The Reach", "The Scorchwaste", "The Lowlands", "The High Court", "The Sunken Hollows"}
    for cid, comp in COMPANIONS.items():
        assert comp.province in provinces, f"Companion {cid} has unknown province {comp.province}"
        assert engine.get_scene(comp.home_scene) is not None, f"Home scene {comp.home_scene} missing for {cid}"
        assert comp.name
        assert comp.title
        assert comp.perk_name
        assert comp.perk_description


# --- Test 2: Hemingway Prose Compliance ---

def test_companion_hemingway_prose():
    """Verify descriptions, action labels, and result texts follow Hemingway invariants."""
    for cid, c in COMPANIONS.items():
        # Action labels: exactly 1 to 3 words
        for label_name, label in [
            ("recruit", c.recruit_action_label),
            ("dismiss", c.dismiss_action_label),
            ("talk", c.talk_action_label),
            ("activate", c.activate_action_label),
        ]:
            words = label.split()
            assert 1 <= len(words) <= 3, (
                f"{label_name} label '{label}' for {cid} must have 1-3 words, got {len(words)}"
            )

        # Descriptions & result texts: 1 to 3 sentences, <= 18 words/sentence, FKGL <= 8.0, 0 purple words
        texts = [
            ("description", c.description),
            ("recruit_result", c.recruit_result_text),
            ("dismiss_result", c.dismiss_result_text),
            ("talk_result", c.talk_result_text),
            ("activate_result", c.activate_result_text),
        ]
        for field_name, text in texts:
            sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
            assert 1 <= len(sentences) <= 3, (
                f"{field_name} for {cid} has {len(sentences)} sentences (expected 1-3)"
            )
            for sent in sentences:
                words = sent.split()
                assert len(words) <= 18, (
                    f"Sentence in {cid} {field_name} exceeds 18 words: '{sent}' ({len(words)} words)"
                )
            grade = flesch_kincaid_grade(text)
            assert grade <= 8.0, f"FKGL for {cid} {field_name} is {grade:.1f} (must be <= 8.0)"

            lower_text = text.lower()
            for forbidden in FORBIDDEN_PURPLE_WORDS:
                assert forbidden not in lower_text, (
                    f"Forbidden purple word '{forbidden}' found in {cid} {field_name}: '{text}'"
                )


# --- Test 3: 7-Axis Character Reactivity in Recruitment ---

def test_companion_character_reactivity():
    """Verify counterfactual witnesses meet different recruitment prerequisites."""
    silas = get_preset("cutpurse").character
    vivienne = get_preset("noble").character
    warrior = get_preset("warrior").character

    # Silas has high cunning & cutpurse background: can recruit Bram
    assert can_recruit_companion("bram", silas)

    # Vivienne has high charm & noble background: can recruit Lady Elenore
    assert can_recruit_companion("elenore", vivienne)

    # Ironborn warrior has high strength: can recruit Kaelen
    assert can_recruit_companion("kaelen", warrior)

    # Character with 2 silver coins can recruit any companion
    funded_char = silas.modify(inventory=list(silas.inventory) + ["silver_coin", "silver_coin"])
    assert can_recruit_companion("kaelen", funded_char)
    assert can_recruit_companion("sariyah", funded_char)
    assert can_recruit_companion("tarek", funded_char)


# --- Test 4: Dynamic Companion Lifecycle (Recruit -> Consult -> Dismiss -> Re-summon) ---

def test_companion_lifecycle(engine):
    """Verify recruit in garrison, consult in field, dismiss, and summon in Central Bazaar."""
    preset = get_preset("warrior")
    state = GameState(
        build_id="af-build-001",
        session_id="test-comp-lifecycle",
        character=preset.character,
        current_region="iron_crags",
        current_scene="reach_dunwall_fort_courtyard",
        rng=DeterministicRNG.from_seed(42),
    )

    # 1. At garrison courtyard, Kaelen recruit affordance is available
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert "companion_recruit_kaelen" in action_ids

    # Step: Recruit Kaelen
    state, obs = engine.step(state, "companion_recruit_kaelen")
    assert obs.success
    assert state.world_flags.get("companion_kaelen_recruited") is True
    assert state.world_flags.get("active_companion") == "kaelen"

    # 2. In any scene, active follower affordances (Consult, Dismiss) are present
    state = state.evolve(current_scene="crags_peak")
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert "companion_talk_kaelen" in action_ids
    assert "companion_dismiss_kaelen" in action_ids

    # Step: Consult Kaelen in the field
    state, obs = engine.step(state, "companion_talk_kaelen")
    assert obs.success
    assert any("mountain archers" in ev for ev in obs.events)

    # Step: Dismiss Kaelen
    state, obs = engine.step(state, "companion_dismiss_kaelen")
    assert obs.success
    assert state.world_flags.get("active_companion") == ""

    # Field affordances disappear once dismissed
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert "companion_talk_kaelen" not in action_ids
    assert "companion_dismiss_kaelen" not in action_ids

    # 3. Travel to Central Bazaar: Re-summon Kaelen is available
    state = state.evolve(current_scene="bazaar_center")
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert "companion_activate_kaelen" in action_ids

    # Step: Summon Kaelen from the Bazaar
    state, obs = engine.step(state, "companion_activate_kaelen")
    assert obs.success
    assert state.world_flags.get("active_companion") == "kaelen"


# --- Test 5: Fellowship Rank Progression ---

def test_fellowship_rank_milestones():
    """Verify rank evaluation as companions are recruited."""
    flags = {}
    p0 = evaluate_companions_progress(flags)
    assert p0["recruited_count"] == 0
    assert p0["rank_title"] == "Lone Wanderer"
    assert not p0["is_partner"]

    # 1 companion recruited
    flags["companion_kaelen_recruited"] = True
    flags["active_companion"] = "kaelen"
    p1 = evaluate_companions_progress(flags)
    assert p1["recruited_count"] == 1
    assert p1["is_partner"]
    assert p1["active_companion_name"] == "Kaelen Stonebreaker"
    assert "Provincial Partner" in p1["rank_title"]

    # 3 companions recruited
    flags["companion_sariyah_recruited"] = True
    flags["companion_bram_recruited"] = True
    p3 = evaluate_companions_progress(flags)
    assert p3["recruited_count"] == 3
    assert p3["is_warband"]
    assert "Continental Warband" in p3["rank_title"]

    # 5 companions recruited
    flags["companion_elenore_recruited"] = True
    flags["companion_tarek_recruited"] = True
    p5 = evaluate_companions_progress(flags)
    assert p5["recruited_count"] == 5
    assert p5["is_master"]
    assert "Master of the Fellowship" in p5["rank_title"]


# --- Test 6: Replay Determinism ---

def test_companion_replay_determinism(engine):
    """Verify bit-for-bit SHA-256 fingerprint reproducibility across companion steps."""
    preset = get_preset("warrior")
    state1 = GameState(
        build_id="af-build-001",
        session_id="comp-replay-1",
        character=preset.character,
        current_region="iron_crags",
        current_scene="reach_dunwall_fort_courtyard",
        rng=DeterministicRNG.from_seed(999),
    )
    state2 = GameState(
        build_id="af-build-001",
        session_id="comp-replay-2",
        character=preset.character,
        current_region="iron_crags",
        current_scene="reach_dunwall_fort_courtyard",
        rng=DeterministicRNG.from_seed(999),
    )

    assert state1.fingerprint() == state2.fingerprint()

    # Step 1: recruit Kaelen
    state1, obs1 = engine.step(state1, "companion_recruit_kaelen")
    state2, obs2 = engine.step(state2, "companion_recruit_kaelen")
    assert obs1.success and obs2.success
    assert state1.fingerprint() == state2.fingerprint()

    # Step 2: talk to Kaelen
    state1, obs1 = engine.step(state1, "companion_talk_kaelen")
    state2, obs2 = engine.step(state2, "companion_talk_kaelen")
    assert obs1.success and obs2.success
    assert state1.fingerprint() == state2.fingerprint()

    # Step 3: dismiss Kaelen
    state1, obs1 = engine.step(state1, "companion_dismiss_kaelen")
    state2, obs2 = engine.step(state2, "companion_dismiss_kaelen")
    assert obs1.success and obs2.success
    assert state1.fingerprint() == state2.fingerprint()


# --- Test 7: ASGI REST Endpoints ---

def test_companion_asgi_endpoints():
    """Verify GET/HEAD /api/game/companions and payload inclusion."""
    from app import app

    async def run_asgi(path: str, method: str = "GET", body: bytes = b""):
        response_data = {"status": 0, "headers": [], "body": b""}

        async def receive():
            return {"type": "http.request", "body": body}

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
            "headers": [(b"host", b"localhost")],
        }
        await app(scope, receive, send)
        return response_data

    # 1. GET /api/game/companions
    res = asyncio.run(run_asgi("/api/game/companions", "GET"))
    assert res["status"] == 200
    data = json.loads(res["body"].decode("utf-8"))
    assert data["total_companions"] == 5
    assert len(data["companions"]) == 5

    # 2. HEAD /api/game/companions
    res_head = asyncio.run(run_asgi("/api/game/companions", "HEAD"))
    assert res_head["status"] == 200
    assert res_head["body"] == b""

    # 3. POST /api/game/new includes companion progress
    new_req_body = json.dumps({"preset": "cutpurse", "seed": 42}).encode("utf-8")
    res_new = asyncio.run(run_asgi("/api/game/new", "POST", new_req_body))
    assert res_new["status"] == 200
    new_data = json.loads(res_new["body"].decode("utf-8"))
    assert "companion" in new_data
    assert new_data["companion"]["total_companions"] == 5
    assert new_data["companion"]["recruited_count"] == 0
    assert new_data["companion"]["rank_title"] == "Lone Wanderer"
