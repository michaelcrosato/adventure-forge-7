"""Milestone 23: Continental Mercenary Contract Board & Faction Bounties Test Suite.

Validates:
1. Bounty contract registry integrity (10 contracts across 5 provinces, 6 hubs).
2. World graph target scene validity (100% reachable target scenes).
3. Hemingway prose compliance (<= 18 words/sent, 1-3 sent, FKGL <= 8.0, <= 3 words/label, 0 purple words).
4. Dynamic contract lifecycle: Accept in Hub -> Hunt in Target Scene -> Claim in Hub.
5. Hunter rank progression and milestone titles.
6. Pure determinism and replay fingerprint fidelity.
7. ASGI REST endpoints (GET/HEAD /api/game/bounties, payload inclusion in /api/game/*).
"""
import asyncio
import json
import re
import pytest
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.bounties import (
    BOUNTY_CONTRACTS,
    BOUNTY_HUBS,
    get_contracts_for_hub,
    evaluate_bounty_progress,
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


# --- Test 1: Bounty Registry Integrity ---

def test_bounty_registry_count_and_targets(engine):
    """Verify 10 contracts across 5 provinces and that all targets exist in the world graph."""
    assert len(BOUNTY_CONTRACTS) == 10
    assert len(BOUNTY_HUBS) == 6

    provinces = {"The Reach", "The Scorchwaste", "The Lowlands", "The High Court", "The Sunken Hollows"}
    for cid, contract in BOUNTY_CONTRACTS.items():
        assert contract.province in provinces, f"Contract {cid} has unknown province {contract.province}"
        assert engine.get_scene(contract.hub_scene) is not None, f"Hub scene {contract.hub_scene} missing for {cid}"
        assert engine.get_scene(contract.target_scene) is not None, f"Target scene {contract.target_scene} missing for {cid}"
        assert contract.reward_silver >= 1
        assert contract.reward_item
        assert contract.reputation_faction
        assert contract.reputation_value >= 5

    # Verify Central Bazaar has all contracts available
    bazaar_contracts = get_contracts_for_hub("bazaar_center")
    assert len(bazaar_contracts) == 10

    # Verify provincial hubs each have 2 contracts
    for hub_id in [
        "reach_dunwall_fort_gate",
        "scorchwaste_ashen_gate_gate",
        "lowlands_oakhaven_port_gate",
        "high_court_grand_basilica_gate",
        "sunken_hollows_glow_grotto_gate",
    ]:
        hub_c = get_contracts_for_hub(hub_id)
        assert len(hub_c) == 2, f"Hub {hub_id} should have exactly 2 contracts"


# --- Test 2: Hemingway Prose Compliance ---

def test_bounty_hemingway_prose_compliance():
    """Verify descriptions, action labels, and result texts follow Hemingway rules."""
    for cid, c in BOUNTY_CONTRACTS.items():
        # 1. Action labels: exactly 1 to 3 words
        for label_name, label in [
            ("accept", c.accept_action_label),
            ("hunt", c.hunt_action_label),
            ("claim", c.claim_action_label),
        ]:
            words = label.split()
            assert 1 <= len(words) <= 3, (
                f"{label_name} label '{label}' for {cid} must have 1-3 words, got {len(words)}"
            )

        # 2. Description, Accept Result, Hunt Result, Claim Result: 1 to 3 sentences, <= 18 words/sentence
        texts = [
            ("description", c.description),
            ("accept_result", c.accept_result_text),
            ("hunt_result", c.hunt_result_text),
            ("claim_result", c.claim_result_text),
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


# --- Test 3: Contract Lifecycle (Accept -> Hunt -> Claim) ---

def test_bounty_contract_lifecycle(engine):
    """Verify accept in hub, hunt in target scene, and claim in hub."""
    preset = get_preset("cutpurse")
    # Place character at Dunwall Fort Gate (Reach Hub)
    state = GameState(
        build_id="af-build-001",
        session_id="test-bounty-lifecycle",
        character=preset.character,
        current_region="iron_crags",
        current_scene="reach_dunwall_fort_gate",
        rng=DeterministicRNG.from_seed(42),
    )

    # 1. Hub scene should have accept affordance for reach contracts
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert "bounty_accept_reach_deserter" in action_ids

    # Step: Accept the bounty
    state, obs = engine.step(state, "bounty_accept_reach_deserter")
    assert obs.success
    assert state.world_flags.get("bounty_reach_deserter_accepted") is True
    assert not state.world_flags.get("bounty_reach_deserter_hunted")
    assert not state.world_flags.get("bounty_reach_deserter_completed")

    # 2. Cannot claim or hunt yet in the gate hub
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert "bounty_hunt_reach_deserter" not in action_ids
    assert "bounty_claim_reach_deserter" not in action_ids

    # Move to target scene: reach_dunwall_fort_quarters
    state = state.evolve(current_scene="reach_dunwall_fort_quarters")
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert "bounty_hunt_reach_deserter" in action_ids

    # Step: Hunt the deserter
    state, obs = engine.step(state, "bounty_hunt_reach_deserter")
    assert obs.success
    assert state.world_flags.get("bounty_reach_deserter_hunted") is True
    assert not state.world_flags.get("bounty_reach_deserter_completed")

    # 3. Return to hub (or Central Bazaar) to claim
    state = state.evolve(current_scene="reach_dunwall_fort_gate")
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert "bounty_claim_reach_deserter" in action_ids

    initial_coins = state.character.inventory.count("silver_coin")
    initial_ironborn_rep = state.character.reputation.get("ironborn", 0)

    # Step: Claim the bounty
    state, obs = engine.step(state, "bounty_claim_reach_deserter")
    assert obs.success
    assert state.world_flags.get("bounty_reach_deserter_completed") is True
    assert state.character.inventory.count("silver_coin") == initial_coins + 1
    assert "crowbar" in state.character.inventory
    assert state.character.reputation.get("ironborn", 0) == initial_ironborn_rep + 10

    # 4. Once completed, no more accept, hunt, or claim affordances appear
    obs = engine.observe(state)
    action_ids = [a["id"] for a in obs.legal_actions]
    assert "bounty_accept_reach_deserter" not in action_ids
    assert "bounty_hunt_reach_deserter" not in action_ids
    assert "bounty_claim_reach_deserter" not in action_ids


# --- Test 4: Hunter Rank Milestones ---

def test_hunter_rank_milestones():
    """Verify rank evaluation across completion milestones."""
    flags = {}
    p0 = evaluate_bounty_progress(flags)
    assert p0["completed_count"] == 0
    assert p0["rank_title"] == "Novice Drifter"
    assert not p0["is_rank_1"]

    # Complete 2 contracts
    flags["bounty_reach_golem_completed"] = True
    flags["bounty_reach_deserter_completed"] = True
    p2 = evaluate_bounty_progress(flags)
    assert p2["completed_count"] == 2
    assert p2["is_rank_1"]
    assert "Registered Bounty Hunter" in p2["rank_title"]

    # Complete 5 contracts
    flags["bounty_scorch_worm_completed"] = True
    flags["bounty_scorch_raider_completed"] = True
    flags["bounty_lowlands_smuggler_completed"] = True
    p5 = evaluate_bounty_progress(flags)
    assert p5["completed_count"] == 5
    assert p5["is_lawkeeper"]
    assert "Provincial Lawkeeper" in p5["rank_title"]

    # Complete all 10 contracts
    flags["bounty_lowlands_leech_completed"] = True
    flags["bounty_court_forger_completed"] = True
    flags["bounty_court_infiltrator_completed"] = True
    flags["bounty_hollows_eel_completed"] = True
    flags["bounty_hollows_cultist_completed"] = True
    p10 = evaluate_bounty_progress(flags)
    assert p10["completed_count"] == 10
    assert p10["is_master_hunter"]
    assert "Continental Master Hunter" in p10["rank_title"]


# --- Test 5: Deterministic Replay Fingerprinting ---

def test_bounty_replay_determinism(engine):
    """Verify deterministic state transitions and SHA-256 fingerprints across bounty interactions."""
    preset = get_preset("cutpurse")
    state1 = GameState(
        build_id="af-build-001",
        session_id="replay-test-1",
        character=preset.character,
        current_region="iron_crags",
        current_scene="reach_dunwall_fort_gate",
        rng=DeterministicRNG.from_seed(1337),
    )
    state2 = GameState(
        build_id="af-build-001",
        session_id="replay-test-2",
        character=preset.character,
        current_region="iron_crags",
        current_scene="reach_dunwall_fort_gate",
        rng=DeterministicRNG.from_seed(1337),
    )

    # Initial fingerprints match
    assert state1.fingerprint() == state2.fingerprint()

    # Step: accept bounty
    state1, obs1 = engine.step(state1, "bounty_accept_reach_deserter")
    state2, obs2 = engine.step(state2, "bounty_accept_reach_deserter")
    assert obs1.success and obs2.success
    assert state1.fingerprint() == state2.fingerprint()

    # Move both to quarters
    state1 = state1.evolve(current_scene="reach_dunwall_fort_quarters")
    state2 = state2.evolve(current_scene="reach_dunwall_fort_quarters")

    # Step: hunt deserter
    state1, obs1 = engine.step(state1, "bounty_hunt_reach_deserter")
    state2, obs2 = engine.step(state2, "bounty_hunt_reach_deserter")
    assert obs1.success and obs2.success
    assert state1.fingerprint() == state2.fingerprint()


# --- Test 6: ASGI REST Endpoints & Pre-Encoded Payload ---

def test_bounty_asgi_endpoints():
    """Verify GET/HEAD /api/game/bounties and payload inclusion."""
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

    # 1. GET /api/game/bounties
    res = asyncio.run(run_asgi("/api/game/bounties", "GET"))
    assert res["status"] == 200
    data = json.loads(res["body"].decode("utf-8"))
    assert data["total_contracts"] == 10
    assert len(data["contracts"]) == 10
    assert len(data["hubs"]) == 6

    # 2. HEAD /api/game/bounties
    res_head = asyncio.run(run_asgi("/api/game/bounties", "HEAD"))
    assert res_head["status"] == 200
    assert res_head["body"] == b""

    # 3. POST /api/game/new returns bounty payload
    new_req_body = json.dumps({"preset": "cutpurse", "seed": 42}).encode("utf-8")
    res_new = asyncio.run(run_asgi("/api/game/new", "POST", new_req_body))
    assert res_new["status"] == 200
    new_data = json.loads(res_new["body"].decode("utf-8"))
    assert "bounty" in new_data
    assert new_data["bounty"]["total_contracts"] == 10
    assert new_data["bounty"]["completed_count"] == 0
    assert new_data["bounty"]["rank_title"] == "Novice Drifter"
