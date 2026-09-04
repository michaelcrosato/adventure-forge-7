"""Tier 1 & Tier 2: Pure Deterministic Kernel (Feature 1 / R1) Test Suite.

Satisfies TEST_INFRA.md:
- Tier 1 Coverage (>= 5 tests)
- Tier 2 Boundary & Corner (>= 5 tests)
"""
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.content.loader import build_world_registry


def _create_engine_and_state(seed: int = 42, scene_id: str = "crags_base"):
    registry = build_world_registry()
    engine = AdventureEngine(registry, build_id="test-build-001")
    char = CharacterSheet(
        name="TestHero",
        ancestry="Deep-Dweller",
        background="cutpurse",
        attributes={"agility": 14, "strength": 12},
        skills={"cunning": 3, "stealth": 2},
        traits=["night_eyed", "nimble"],
        flaws=["marked_outlaw"],
        inventory=["lockpick", "silver_coin"],
        stamina=10,
        max_stamina=10,
        health=20,
        max_health=20,
    )
    region_id = engine.get_region_id_for_scene(scene_id) or "iron_crags"
    state = GameState(
        build_id=engine.build_id,
        session_id="test-session",
        character=char,
        current_region=region_id,
        current_scene=scene_id,
        world_flags={"test_flag": False},
        history=[],
        event_log=[],
        turn_count=0,
        rng=DeterministicRNG(seed),
    )
    return engine, state


# ── Tier 1: Unit Coverage (>= 5 tests) ───────────────────────────────────────

def test_prng_splitmix64_reproducibility():
    """Deterministic RNG cursor produces identical u64 sequence given same seed."""
    rng1 = DeterministicRNG(123456789)
    rng2 = DeterministicRNG(123456789)

    seq1 = []
    seq2 = []
    for _ in range(25):
        val1, rng1 = rng1.next_u64()
        val2, rng2 = rng2.next_u64()
        seq1.append(val1)
        seq2.append(val2)

    assert seq1 == seq2
    assert rng1.state == rng2.state
    assert len(set(seq1)) == 25


def test_state_fingerprint_sha256_canonical():
    """State hashing produces identical SHA-256 fingerprint regardless of dict key order."""
    _, state1 = _create_engine_and_state(seed=42)

    flags_rev = dict(reversed(list(state1.world_flags.items())))
    attrs_rev = dict(reversed(list(state1.character.attributes.items())))
    char2 = state1.character.modify(attributes=attrs_rev)
    state2 = state1.evolve(character=char2, world_flags=flags_rev)

    assert state1.fingerprint() == state2.fingerprint()
    assert len(state1.fingerprint()) == 64


def test_transition_step_purity():
    """Identical state + action yields bit-for-bit identical state and StepResult."""
    engine, state1 = _create_engine_and_state(seed=100)
    _, state2 = _create_engine_and_state(seed=100)

    legal1 = engine.get_legal_actions(state1)
    assert len(legal1) > 0
    action_id = legal1[0].id

    new_state1, res1 = engine.step(state1, action_id)
    new_state2, res2 = engine.step(state2, action_id)

    assert new_state1.fingerprint() == new_state2.fingerprint()
    assert res1.to_dict() == res2.to_dict()
    assert new_state1.turn_count == 1
    assert new_state2.turn_count == 1


def test_action_history_event_log_accumulation():
    """History and event log accumulate canonically without mutating previous state."""
    engine, state = _create_engine_and_state(seed=200)
    orig_history_len = len(state.history)
    orig_event_len = len(state.event_log)

    legal = engine.get_legal_actions(state)
    action_id = legal[0].id

    new_state, _ = engine.step(state, action_id)

    assert len(state.history) == orig_history_len
    assert len(state.event_log) == orig_event_len
    assert new_state.history == [action_id]
    assert len(new_state.event_log) > orig_event_len


def test_state_serialization_roundtrip():
    """State to_dict() and from_dict() roundtrips preserve fingerprint and RNG state."""
    engine, state = _create_engine_and_state(seed=300)
    legal = engine.get_legal_actions(state)
    state, _ = engine.step(state, legal[0].id)

    state_dict = state.to_dict()
    restored = GameState.from_dict(state_dict)

    assert restored.fingerprint() == state.fingerprint()
    assert restored.turn_count == state.turn_count
    assert restored.current_scene == state.current_scene
    assert restored.rng.state == state.rng.state
    assert restored.character.inventory == state.character.inventory


# ── Tier 2: Boundary & Corner Tests (>= 5 tests) ─────────────────────────────

def test_deterministic_replay_50_steps():
    """50-step deterministic walk produces exact identical fingerprint on replay."""
    engine, state0 = _create_engine_and_state(seed=777)
    actions_taken = []
    current = state0

    for step in range(50):
        legal = engine.get_legal_actions(current)
        assert len(legal) > 0, f"No actions at step {step} in scene {current.current_scene}"
        choice_idx, _ = current.rng.next_int(0, len(legal) - 1)
        action = legal[choice_idx]
        actions_taken.append(action.id)
        current, _ = engine.step(current, action.id)

    final_fingerprint = current.fingerprint()
    assert current.turn_count == 50

    replay_state = state0
    for aid in actions_taken:
        replay_state, _ = engine.step(replay_state, aid)

    assert replay_state.fingerprint() == final_fingerprint
    assert replay_state.turn_count == 50
    assert replay_state.history == actions_taken


def test_tamper_detection_single_field_flip():
    """Altering any single field (health, flag, history, RNG) alters fingerprint."""
    _, state = _create_engine_and_state(seed=999)
    base_fp = state.fingerprint()

    char_tamp = state.character.modify(health=state.character.health - 1)
    assert state.evolve(character=char_tamp).fingerprint() != base_fp

    char_tamp2 = state.character.modify(stamina=state.character.stamina - 1)
    assert state.evolve(character=char_tamp2).fingerprint() != base_fp

    char_tamp3 = state.character.modify(inventory=["wooden_spoon"])
    assert state.evolve(character=char_tamp3).fingerprint() != base_fp

    assert state.evolve(world_flags={"tamper": True}).fingerprint() != base_fp
    assert state.evolve(rng=DeterministicRNG(1000)).fingerprint() != base_fp
    assert state.evolve(turn_count=1).fingerprint() != base_fp


def test_illegal_action_rejection_leaves_state_identical():
    """Submitting invalid action ID returns failure StepResult and exact unchanged state."""
    engine, state = _create_engine_and_state(seed=42)
    orig_fp = state.fingerprint()

    new_state, res = engine.step(state, "completely_nonexistent_action_xyz")

    assert res.success is False
    assert "rejected" in res.message.lower() or "not currently legal" in res.message.lower()
    assert new_state.fingerprint() == orig_fp
    assert new_state.turn_count == 0
    assert len(new_state.history) == 0


def test_stale_action_rejection():
    """Action valid in previous scene but invalid in current scene is rejected."""
    engine, state = _create_engine_and_state(seed=42, scene_id="crags_base")
    legal_at_base = engine.get_legal_actions(state)
    base_action = legal_at_base[0]

    state_moved, _ = engine.step(state, "walk_to_warrens")
    assert state_moved.current_scene == "warrens_gate"

    stale_state, res = engine.step(state_moved, base_action.id)
    assert res.success is False
    assert stale_state.fingerprint() == state_moved.fingerprint()


def test_prng_cursor_boundary_overflow():
    """PRNG cursor handles values near 2^64-1 with 64-bit wrap-around cleanly."""
    max_u64 = 0xFFFFFFFFFFFFFFFF
    rng = DeterministicRNG(max_u64)
    val1, rng_next = rng.next_u64()

    assert isinstance(val1, int)
    assert 0 <= val1 <= max_u64
    assert 0 <= rng_next.state <= max_u64

    for _ in range(100):
        val, rng_next = rng_next.next_u64()
        assert 0 <= val <= max_u64
