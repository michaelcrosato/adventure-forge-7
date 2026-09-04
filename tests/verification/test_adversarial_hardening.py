"""Tier 5: Adversarial Coverage Hardening Test Suite.

Satisfies TEST_INFRA.md / Milestone M5:
- Adversarial challenger analysis, gap detection, and test coverage hardening.
- Softlock hunting, fuzzing, tamper resistance, and firewall security.
"""
import pytest
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.conditions import evaluate_condition
from adventure_forge.core.effects import apply_effects
from adventure_forge.content.loader import build_world_registry
from adventure_forge.player.mcp_server import sanitize_observation
from adventure_forge.linter.prose_linter import ProseLinter


def _make_engine():
    return AdventureEngine(build_world_registry())


def test_adversarial_unknown_condition_operator():
    """Condition DSL strictly rejects undeclared operators with ValueError."""
    char = CharacterSheet(name="T", ancestry="Plainsman", background="drifter")
    with pytest.raises(ValueError, match="Unknown condition operator"):
        evaluate_condition({"nonexistent_operator_hack": True}, char, {})


def test_adversarial_unknown_effect_operator():
    """Effect DSL strictly rejects undeclared effect operations with ValueError."""
    char = CharacterSheet(name="T", ancestry="Plainsman", background="drifter")
    with pytest.raises(ValueError, match="Unknown effect operator"):
        apply_effects([{"malicious_effect_hack": 100}], char, {})


def test_adversarial_zero_stamina_and_negative_health_clamping():
    """Health and stamina are strictly clamped within [0, max] under extreme deltas."""
    char = CharacterSheet(name="Mortal", ancestry="Plainsman", background="drifter",
                          health=20, max_health=20, stamina=10, max_stamina=10)
    
    # 1. Massive negative damage
    char_low, _, _, _ = apply_effects([{"modify_health": -9999}], char, {})
    assert char_low.health == 0

    # 2. Massive overheal
    char_high, _, _, _ = apply_effects([{"modify_health": 9999}], char, {})
    assert char_high.health == 20

    # 3. Massive negative stamina
    char_drain, _, _, _ = apply_effects([{"modify_stamina": -9999}], char, {})
    assert char_drain.stamina == 0

    # 4. Massive over-stamina
    char_boost, _, _, _ = apply_effects([{"modify_stamina": 9999}], char, {})
    assert char_boost.stamina == 10


def test_adversarial_deep_action_loop_repetition():
    """100 repetitive non-movement actions in one scene maintain purity and performance."""
    engine = _make_engine()
    char = CharacterSheet(name="Rep", ancestry="Plainsman", background="drifter")
    state = GameState(
        build_id=engine.build_id, session_id="rep-test", character=char,
        current_region="iron_crags", current_scene="crags_base",
        world_flags={}, history=[], event_log=[], turn_count=0, rng=DeterministicRNG.from_seed(42)
    )

    for _ in range(100):
        legal = engine.get_legal_actions(state)
        # Search scree action
        state, res = engine.step(state, legal[0].id)
        assert res.success is True

    assert state.turn_count == 100
    assert len(state.history) == 100
    # Replay produces identical fingerprint
    state_replay = GameState(
        build_id=engine.build_id, session_id="rep-test", character=char,
        current_region="iron_crags", current_scene="crags_base",
        world_flags={}, history=[], event_log=[], turn_count=0, rng=DeterministicRNG.from_seed(42)
    )
    for act in state.history:
        state_replay, _ = engine.step(state_replay, act)
    assert state_replay.fingerprint() == state.fingerprint()


def test_adversarial_large_state_dictionary_serialization():
    """State with 1,000 flags serializes deterministically and evaluates fast."""
    engine = _make_engine()
    char = CharacterSheet(name="Heavy", ancestry="Plainsman", background="drifter")
    massive_flags = {f"flag_{i}": (i % 2 == 0) for i in range(1000)}
    state = GameState(
        build_id=engine.build_id, session_id="heavy-test", character=char,
        current_region="iron_crags", current_scene="crags_base",
        world_flags=massive_flags, history=[], event_log=[], turn_count=0, rng=DeterministicRNG.from_seed(1)
    )

    fp1 = state.fingerprint()
    dict_payload = state.to_dict()
    restored = GameState.from_dict(dict_payload)
    fp2 = restored.fingerprint()

    assert fp1 == fp2
    assert len(restored.world_flags) == 1000


def test_adversarial_firewall_leak_sanitizer():
    """sanitize_observation strictly scrubs any unexpected keys injected into StepResult."""
    engine = _make_engine()
    char = CharacterSheet(name="Safe", ancestry="Plainsman", background="drifter")
    state = GameState(
        build_id=engine.build_id, session_id="firewall-test", character=char,
        current_region="iron_crags", current_scene="crags_base",
        world_flags={"hidden_secret_nuclear_launch_code": "classified"},
        history=[], event_log=[], turn_count=0, rng=DeterministicRNG.from_seed(1)
    )

    obs = engine.observe(state)
    sanitized = sanitize_observation(obs)

    # Convert sanitized to string and verify forbidden strings do not appear
    serialized = str(sanitized)
    assert "classified" not in serialized
    assert "nuclear" not in serialized
    assert "hidden_secret" not in serialized


def test_adversarial_simplicity_linter_smart_quotes_and_unicode():
    """ProseLinter handles smart quotes, em-dashes, and special unicode without crashing."""
    linter = ProseLinter()
    prose_smart_quotes = "“The torch flickers in the damp wind,” the sentry whispers softly."
    errors = linter.lint_text(prose_smart_quotes)
    # Should evaluate without exception
    assert isinstance(errors, list)


def test_adversarial_flesch_kincaid_grade_bounds():
    """Prose with extreme vocabulary is properly flagged for grade level violation."""
    linter = ProseLinter()
    academic_text = "The epistemological ramifications of deterministic historiography necessitate transcendental hermeneutics."
    errors = linter.lint_text(academic_text)
    assert any("readability" in e.lower() or "grade" in e.lower() or "exceeds" in e.lower() for e in errors)
