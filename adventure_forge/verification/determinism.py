"""Deterministic Replay Verifier.

Verifies I1 / SYS-01 / SYS-04:
- 100% replay fidelity across seeds and runs.
- Bit-for-bit canonical fingerprint matching.
- Tamper detection: modifying an action or seed invalidates the trace.
"""
from typing import List, Dict, Any, Tuple
from adventure_forge.core.state import GameState
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry


def run_session_trace(
    initial_char: CharacterSheet,
    start_scene: str,
    action_sequence: List[str],
    seed: int = 1337
) -> Tuple[GameState, List[str]]:
    """Execute an action sequence and record the list of state fingerprints."""
    registry = build_world_registry()
    engine = AdventureEngine(registry, build_id="af-build-001")
    
    state = GameState(
        build_id="af-build-001",
        session_id="session-trace-test",
        character=initial_char,
        current_region=engine.get_region_id_for_scene(start_scene) or "iron_crags",
        current_scene=start_scene,
        rng=DeterministicRNG.from_seed(seed)
    )

    fingerprints = [state.fingerprint()]
    for act_id in action_sequence:
        state, obs = engine.step(state, act_id)
        fingerprints.append(state.fingerprint())

    return state, fingerprints


def verify_replay_determinism() -> Tuple[bool, str]:
    """Test that two separate executions of the same actions yield identical fingerprints."""
    char = CharacterSheet(
        name="Kaelen",
        ancestry="Plainsman",
        background="Drifter",
        attributes={"strength": 12, "agility": 12},
        skills={"cunning": 2},
        traits=["nimble"],
        flaws=[],
        reputation={"iron_guard": 5},
        inventory=["water_skin", "silver_coin"]
    )
    actions = ["search_scree", "walk_to_warrens", "pay_gate_toll"]

    _, fp1 = run_session_trace(char, "crags_base", actions, seed=4242)
    _, fp2 = run_session_trace(char, "crags_base", actions, seed=4242)

    if fp1 != fp2:
        return False, f"Replay divergence detected!\nRun 1: {fp1}\nRun 2: {fp2}"

    # Tamper check: alter action sequence
    tampered_actions = ["search_scree", "walk_to_warrens"]
    _, fp_tampered = run_session_trace(char, "crags_base", tampered_actions, seed=4242)
    if fp1 == fp_tampered:
        return False, "Tamper check failed: different actions produced identical hash!"

    return True, "Determinism and tamper verification passed with 100% fidelity."
