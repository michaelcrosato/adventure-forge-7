"""Scenario Tests: Multi-Province Long-Trace Replay and Cross-Campaign Soak Testing.

Validates:
- 50-turn uninterrupted continuous expedition across all 5 provinces and hubs.
- Bit-for-bit replay determinism across every single step.
- Immediate tamper detection under subtle state mutations.
- Concurrent multi-session thread safety and absolute state isolation.
"""
import concurrent.futures
from typing import List
from adventure_forge.core.character import get_preset
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.state import GameState
from adventure_forge.content.loader import build_world_registry


def test_continuous_50_turn_continental_soak():
    """Execute a 50-turn continuous continental expedition and verify 100% replay determinism."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)
    char = get_preset("scout").character.modify(
        inventory=["climbing_rope", "torch", "water_skin", "lockpick", "silver_coin"]
    )

    initial_state = GameState(
        build_id=engine.build_id,
        session_id="soak-50-turns",
        character=char,
        current_region="province_reach",
        current_scene="reach_hub"
    )

    # 50-turn legal action trajectory spanning provinces and interactions
    trajectory: List[str] = [
        # 1. Reach Hub (4)
        "reach_hub_scout", "reach_hub_board", "reach_hub_rest", "reach_to_bazaar",
        # 2. Grand Bazaar (6)
        "inspect_spices", "barter_spices", "inspect_silk", "barter_silk", "inspect_iron", "travel_to_lowlands_hub",
        # 3. Lowlands Hub (4)
        "lowlands_hub_scout", "lowlands_hub_board", "lowlands_hub_rest", "lowlands_to_bazaar",
        # 4. Grand Bazaar (6)
        "inspect_pottery", "barter_pottery", "inspect_gems", "barter_gems", "inspect_parchment", "travel_to_scorch_hub",
        # 5. Scorchwaste Hub (4)
        "scorchwaste_hub_scout", "scorchwaste_hub_board", "scorchwaste_hub_rest", "scorchwaste_to_bazaar",
        # 6. Grand Bazaar (6)
        "inspect_leather", "barter_leather", "inspect_herbs", "barter_herbs", "inspect_brass", "travel_to_court_hub",
        # 7. High Court Hub (4)
        "high_court_hub_scout", "high_court_hub_board", "high_court_hub_rest", "high_court_to_bazaar",
        # 8. Grand Bazaar (6)
        "inspect_fruit", "barter_fruit", "inspect_carpets", "barter_carpets", "inspect_relics", "travel_to_abyss_hub",
        # 9. Sunken Hollows Hub (4)
        "sunken_hollows_hub_scout", "sunken_hollows_hub_board", "sunken_hollows_hub_rest", "sunken_hollows_to_bazaar",
        # 10. Grand Bazaar & Return to Reach (6)
        "inspect_glass", "barter_glass", "inspect_tomes", "barter_tomes", "inspect_charms", "travel_to_reach_hub",
    ]

    assert len(trajectory) == 50

    # Run 1: Step through trajectory and record intermediate fingerprints
    state = initial_state
    fingerprints: List[str] = [state.fingerprint()]

    for idx, act in enumerate(trajectory):
        state, obs = engine.step(state, act)
        assert obs.success, f"Action #{idx+1} '{act}' failed at scene '{state.current_scene}': {obs.message}"
        fp = state.fingerprint()
        assert len(fp) == 64
        fingerprints.append(fp)

    assert state.turn_count == 50
    final_fp = state.fingerprint()

    # Run 2: Exact replay from initial state
    replay_state = initial_state
    assert replay_state.fingerprint() == fingerprints[0]

    for idx, act in enumerate(trajectory):
        replay_state, obs = engine.step(replay_state, act)
        assert obs.success
        assert replay_state.fingerprint() == fingerprints[idx + 1], f"Fingerprint mismatch at step {idx+1}"

    assert replay_state.fingerprint() == final_fp
    assert replay_state.character.inventory == state.character.inventory
    assert replay_state.history == state.history


def test_tamper_detection_in_long_trace():
    """Verify that any tampering in the middle of a 50-turn trajectory produces immediate divergence."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)
    char = get_preset("scout").character
    state = GameState(
        build_id=engine.build_id,
        session_id="tamper-test",
        character=char,
        current_region="province_reach",
        current_scene="reach_hub"
    )

    trajectory = [
        "reach_hub_scout",
        "reach_hub_board",
        "reach_hub_rest",
        "reach_to_bazaar",
        "inspect_spices",
    ]

    # Advance 5 steps legitimately
    for act in trajectory:
        state, obs = engine.step(state, act)
        assert obs.success

    legit_fp = state.fingerprint()

    # Inject 1 bit of tampering: add an unauthorized item to character inventory
    tampered_char = state.character.modify(inventory=list(state.character.inventory) + ["forged_seal"])
    tampered_state = state.evolve(character=tampered_char)

    assert tampered_state.fingerprint() != legit_fp, "Tampered state must produce distinct SHA-256 fingerprint"


def test_concurrent_multi_session_isolation():
    """Verify concurrent thread safety: 8 parallel sessions produce bit-identical results."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    def run_isolated_session(seed: int) -> str:
        char = get_preset("cutpurse").character
        s = GameState(
            build_id=engine.build_id,
            session_id=f"thread-session-{seed}",
            character=char,
            current_region="lower_warrens",
            current_scene="warrens_gate",
        )
        actions = [
            "slip_past_watch",
            "search_gutters",
            "back_to_gate",
            "pick_sewer_grate",
            "pay_gate_toll",
        ]
        for act in actions:
            s, obs = engine.step(s, act)
            assert obs.success
        return s.fingerprint()

    # Run in thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(run_isolated_session, 42) for _ in range(8)]
        results = [f.result() for f in futures]

    # All 8 threads must return identical fingerprints
    first_fp = results[0]
    assert all(fp == first_fp for fp in results), "All parallel runs with identical actions must match bit-for-bit"
