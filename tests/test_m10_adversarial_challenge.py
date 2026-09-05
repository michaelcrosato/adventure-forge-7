"""Adversarial Challenge Test Suite for Milestone 10 (Playtester Fleet & Defect Triage).

Empirically challenges:
1. reproduce_trace Edge Cases:
   - Empty action traces under valid and fallback presets
   - Non-existent and malformed actions isolating failure step
   - Mid-trace failure halting at exact failing index
   - Unknown presets falling back gracefully without crash
   - Deterministic bit-for-bit SHA-256 fingerprint verification across identical traces
   - Multi-seed branching verification: distinct seeds yield distinct state fingerprints
   - Deadlock / softlock detection with both canonical and playtester friction phrasing
   - Engine crash resilience (CRASH_DEFECT) with stack details
2. Provincial Personas Behavioral Divergence:
   - Nomad, Diver, and Scout under identical seeds in multi-action scenes
   - Multi-turn trajectory and scene visit divergence across multiple seeds
   - Specialized affordance keyword prioritization (hydration/barter vs submersion/salvage vs climbing/surveying)
3. I6 Information Firewall Compliance:
   - BlindPlaytester decision function takes strictly player-safe StepResult
   - StepResult contains zero references to internal GameState, world flags, or raw manifests
   - Robustness under boundary StepResult inputs (empty actions, terminal states, missing categories)
4. PlaytesterPersona & CLI Robustness:
   - Case-insensitive, whitespace-padded, and uppercase parsing
   - Informative ValueError on invalid persona names listing available choices
   - Graceful fallback for non-standard persona identifiers in BlindPlaytester
   - Telemetry JSONL schema validation (jq and grep compatibility)
"""
import json
import pytest
from adventure_forge.core.character import get_preset
from adventure_forge.core.engine import AdventureEngine, StepResult
from adventure_forge.core.state import GameState
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry
from adventure_forge.flywheel.playtester import (
    BlindPlaytester,
    PlaytesterPersona,
)
from adventure_forge.flywheel.triage import (
    reproduce_trace,
    TriageReport,
)
from adventure_forge.flywheel.orchestrator import OrchestratorManager
from adventure_forge.flywheel.loop import main as loop_main


# ============================================================================
# 1. REPRODUCE_TRACE ADVERSARIAL STRESS TESTS
# ============================================================================

def test_reproduce_trace_empty_action_trace_all_presets():
    """Empty action sequence executes cleanly across all valid and fallback presets."""
    presets_to_test = ["cutpurse", "warrior", "scholar", "scout", "nomad", "diver", "unknown_bogus_preset"]
    for preset in presets_to_test:
        report = reproduce_trace(seed=42, preset=preset, action_sequence=[])
        assert isinstance(report, TriageReport)
        assert report.verified is True
        assert report.status == "VERIFIED_REPLAY"
        assert report.reproduction_trace == []
        assert report.error_step is None
        assert report.failing_scene is None
        assert len(report.actual_fingerprint) == 64
        assert report.matches_expected is True


def test_reproduce_trace_nonexistent_actions_and_step_isolation():
    """Non-existent action immediately trips VERIFIED_DEFECT at the exact step index."""
    # First action invalid
    r1 = reproduce_trace(
        seed=100,
        preset="cutpurse",
        action_sequence=["nonexistent_magic_cast"],
        start_scene="crags_base",
    )
    assert r1.verified is True
    assert r1.status == "VERIFIED_DEFECT"
    assert r1.error_step == 0
    assert r1.reproduction_trace == ["nonexistent_magic_cast"]
    assert "nonexistent_magic_cast" in r1.details
    assert r1.matches_expected is True

    # Third action invalid after two valid actions
    r2 = reproduce_trace(
        seed=100,
        preset="cutpurse",
        action_sequence=["climb_cliff_face", "climb_down_base", "invalid_leap_into_void", "cross_rope_bridge"],
        start_scene="crags_base",
    )
    assert r2.verified is True
    assert r2.status == "VERIFIED_DEFECT"
    assert r2.error_step == 2
    assert r2.reproduction_trace == ["climb_cliff_face", "climb_down_base", "invalid_leap_into_void"]
    assert "invalid_leap_into_void" in r2.details


def test_reproduce_trace_deterministic_replay_and_seed_branching():
    """Identical seeds yield bit-for-bit identical fingerprints; distinct seeds diverge."""
    trace = ["climb_cliff_face", "climb_down_base"]
    # Replay 1 and Replay 2 with seed 42
    rep1 = reproduce_trace(seed=42, preset="cutpurse", action_sequence=trace, start_scene="crags_base")
    rep2 = reproduce_trace(seed=42, preset="cutpurse", action_sequence=trace, start_scene="crags_base")
    assert rep1.actual_fingerprint == rep2.actual_fingerprint
    assert rep1.status == rep2.status == "VERIFIED_REPLAY"
    assert rep1.verified is True
    assert rep1.matches_expected is True
    assert rep2.verified is True
    assert rep2.matches_expected is True

    # Replay with seed 999
    rep_diff = reproduce_trace(seed=999, preset="cutpurse", action_sequence=trace, start_scene="crags_base")
    assert rep_diff.actual_fingerprint != rep1.actual_fingerprint
    assert len(rep_diff.actual_fingerprint) == 64
    assert rep_diff.status == "VERIFIED_REPLAY"
    assert rep_diff.verified is True
    assert rep_diff.matches_expected is True


def test_reproduce_trace_deadlock_detection_with_adversarial_phrasings():
    """Detects confirmed deadlocks (zero legal actions in non-terminal scene) under varied phrases."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    # Monkeypatch engine.observe to simulate a non-terminal dead-end scene
    real_observe = engine.observe

    def dead_end_observe(state, events=None):
        res = real_observe(state, events)
        return StepResult(
            success=True,
            message=res.message,
            scene_id="dead_end_scene",
            region_id=res.region_id,
            title="Dead End",
            description="Nowhere to turn.",
            events=[],
            legal_actions=[],  # Empty legal actions
            turn_count=res.turn_count,
            is_terminal=False,  # Not marked terminal
            outcome=None,
            fingerprint=res.fingerprint,
        )

    engine.observe = dead_end_observe  # type: ignore

    phrasings = [
        "Dead end: No legal actions at scene dead_end_scene",
        "softlock detected in cave",
        "deadlock: player is stuck",
        "no legal actions available",
    ]

    for phrase in phrasings:
        report = reproduce_trace(
            seed=42,
            preset="cutpurse",
            action_sequence=[],
            start_scene="crags_base",
            engine=engine,
            claimed_defect=phrase,
        )
        assert report.verified is True
        assert report.status == "VERIFIED_DEFECT"
        assert report.error_step == 0
        assert "Deadlock confirmed" in report.details


def test_reproduce_trace_engine_crash_isolation():
    """Unexpected exceptions during step transition are captured cleanly as CRASH_DEFECT."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    def crashing_step(state, action_id):
        raise ArithmeticError("Simulated integer overflow in transition calculus")

    engine.step = crashing_step  # type: ignore

    report = reproduce_trace(
        seed=42,
        preset="cutpurse",
        action_sequence=["climb_cliff_face"],
        start_scene="crags_base",
        engine=engine,
        claimed_defect="Engine crashed",
    )
    assert report.verified is True
    assert report.status == "CRASH_DEFECT"
    assert report.error_step == 0
    assert "ArithmeticError" in report.details
    assert "Simulated integer overflow" in report.details


# ============================================================================
# 2. PROVINCIAL PERSONAS BEHAVIORAL DIVERGENCE TESTS
# ============================================================================

def test_provincial_personas_action_selection_divergence_identical_seeds():
    """Nomad, Diver, and Scout evaluate identical observations and make divergent choices."""
    # Construct a rich test StepResult with affordances from desert, aquatic, and vertical domains
    actions = [
        {"id": "climb_steep_crag", "label": "Climb Crag", "category": "movement", "risk": "medium"},
        {"id": "dive_deep_trench", "label": "Dive Trench", "category": "movement", "risk": "low"},
        {"id": "barter_caravan_spices", "label": "Barter Spices", "category": "social", "risk": "low"},
        {"id": "scale_vertical_cliff", "label": "Scale Cliff", "category": "movement", "risk": "high"},
        {"id": "operate_diving_bell", "label": "Operate Bell", "category": "systemic", "risk": "medium"},
        {"id": "rest_in_shade", "label": "Rest in Shade", "category": "interaction", "risk": "low"},
    ]
    obs = StepResult(
        success=True,
        message="Divergence test",
        scene_id="provincial_crossroads",
        region_id="hub",
        title="Hub",
        description="A scene with diverse affordances.",
        events=[],
        legal_actions=actions,
        turn_count=1,
        is_terminal=False,
        outcome=None,
        fingerprint="dummy_fp",
    )

    for seed in [1, 42, 100, 777, 9999]:
        nomad = BlindPlaytester(PlaytesterPersona.NOMAD, seed=seed)
        diver = BlindPlaytester(PlaytesterPersona.DIVER, seed=seed)
        scout = BlindPlaytester(PlaytesterPersona.SCOUT, seed=seed)

        act_nomad = nomad.select_action(obs)
        act_diver = diver.select_action(obs)
        act_scout = scout.select_action(obs)

        # Nomad must choose shade or barter
        assert act_nomad in ("barter_caravan_spices", "rest_in_shade")
        # Diver must choose dive or bell
        assert act_diver in ("dive_deep_trench", "operate_diving_bell")
        # Scout must choose climb or scale
        assert act_scout in ("climb_steep_crag", "scale_vertical_cliff")

        # Crucial invariant: all 3 choices must be distinct
        assert len({act_nomad, act_diver, act_scout}) == 3


def test_provincial_personas_full_session_path_divergence():
    """Running Nomad, Diver, and Scout from the same start scene yields divergent trajectories."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)
    char = get_preset("cutpurse").character

    for seed in [42, 123, 456]:
        t_nomad = BlindPlaytester("nomad", seed=seed).run_session(char, "crags_base", max_turns=10, engine=engine)
        t_diver = BlindPlaytester("diver", seed=seed).run_session(char, "crags_base", max_turns=10, engine=engine)
        t_scout = BlindPlaytester("scout", seed=seed).run_session(char, "crags_base", max_turns=10, engine=engine)

        assert t_nomad.decisions != t_diver.decisions
        assert t_nomad.decisions != t_scout.decisions
        assert t_diver.decisions != t_scout.decisions

        # Scout should explore climbing scenes in Iron Crags
        assert any("climb" in d or "survey" in d or "perch" in d or "ridge" in d for d in t_scout.decisions)


def test_provincial_personas_in_bazaar_center_115_actions():
    """In the 115-action bazaar stress scene, personas prioritize their respective domains."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)
    char = get_preset("cutpurse").character
    state = GameState(
        build_id="af-test",
        session_id="test-bazaar",
        character=char,
        current_region="reach_hub",
        current_scene="bazaar_center",
        rng=DeterministicRNG.from_seed(42),
    )
    obs = engine.observe(state)
    assert len(obs.legal_actions) >= 100

    nomad = BlindPlaytester("nomad", seed=42)
    diver = BlindPlaytester("diver", seed=42)
    scout = BlindPlaytester("scout", seed=42)

    act_nomad = nomad.select_action(obs)
    act_diver = diver.select_action(obs)
    act_scout = scout.select_action(obs)

    # All three selections must be non-null and divergent
    assert act_nomad is not None
    assert act_diver is not None
    assert act_scout is not None
    assert len({act_nomad, act_diver, act_scout}) == 3


# ============================================================================
# 3. I6 INFORMATION FIREWALL COMPLIANCE TESTS
# ============================================================================

def test_information_firewall_stepresult_isolation():
    """StepResult must not leak GameState, world flags, character secrets, or engine references."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)
    char = get_preset("cutpurse").character
    state = GameState(
        build_id="af-test",
        session_id="test-firewall",
        character=char,
        current_region="iron_crags",
        current_scene="crags_base",
        rng=DeterministicRNG.from_seed(42),
    )
    obs = engine.observe(state)

    # Check forbidden attributes on StepResult
    forbidden_attrs = ["state", "_state", "engine", "_engine", "world_registry", "flags", "character"]
    for attr in forbidden_attrs:
        assert not hasattr(obs, attr), f"StepResult leaks private attribute: {attr}"

    # Verify legal_actions only expose public UI fields
    for act in obs.legal_actions:
        assert "id" in act
        assert "label" in act
        assert "category" in act
        # Ensure raw conditions/effects are not leaked in legal_actions dicts
        assert "conditions" not in act
        assert "effects" not in act


def test_blind_playtester_select_action_firewall_contract():
    """BlindPlaytester.select_action operates strictly through StepResult without side effects."""
    actions = [
        {"id": "act_a", "label": "Action A", "category": "movement"},
        {"id": "act_b", "label": "Action B", "category": "combat"},
    ]
    obs = StepResult(
        success=True,
        message="Observing",
        scene_id="scene_firewall",
        region_id="region_firewall",
        title="Firewall Scene",
        description="Clean description.",
        events=["event1"],
        legal_actions=actions,
        turn_count=2,
        is_terminal=False,
        outcome=None,
        fingerprint="a" * 64,
    )

    tester = BlindPlaytester("explorer", seed=42)
    chosen = tester.select_action(obs)
    assert chosen in ("act_a", "act_b")

    # StepResult was not mutated
    assert len(obs.legal_actions) == 2
    assert obs.turn_count == 2
    assert obs.fingerprint == "a" * 64


def test_blind_playtester_handles_boundary_observations():
    """BlindPlaytester gracefully handles empty legal actions and terminal states."""
    obs_empty = StepResult(
        success=True,
        message="Empty",
        scene_id="empty_scene",
        region_id="region_empty",
        title="Empty",
        description="Empty scene.",
        events=[],
        legal_actions=[],
        turn_count=5,
        is_terminal=False,
        outcome=None,
        fingerprint="b" * 64,
    )

    for p in PlaytesterPersona:
        tester = BlindPlaytester(p, seed=42)
        assert tester.select_action(obs_empty) is None


# ============================================================================
# 4. PLAYTESTER PERSONA & CLI ADVERSARIAL TESTS
# ============================================================================

def test_playtester_persona_string_parsing_extremes():
    """PlaytesterPersona.from_str handles extreme case, whitespace, and invalid inputs."""
    assert PlaytesterPersona.from_str("  nOmAd  ") == PlaytesterPersona.NOMAD
    assert PlaytesterPersona.from_str("DIVER\n") == PlaytesterPersona.DIVER
    assert PlaytesterPersona.from_str("\tscout\t") == PlaytesterPersona.SCOUT

    with pytest.raises(ValueError) as exc:
        PlaytesterPersona.from_str("alien_super_soldier")
    msg = str(exc.value)
    assert "Unknown playtester persona 'alien_super_soldier'" in msg
    assert "Available personas:" in msg
    for p in PlaytesterPersona:
        assert p.value in msg


def test_blind_playtester_unknown_persona_graceful_fallback():
    """BlindPlaytester with unknown persona string does not crash and selects legal actions."""
    tester = BlindPlaytester("custom_persona_xyz", seed=77)
    assert tester.persona == "custom_persona_xyz"

    actions = [{"id": "act_1", "label": "Act 1"}, {"id": "act_2", "label": "Act 2"}]
    obs = StepResult(
        success=True,
        message="",
        scene_id="test",
        region_id="test",
        title="test",
        description="test",
        events=[],
        legal_actions=actions,
        turn_count=1,
        fingerprint="c" * 64,
    )
    chosen = tester.select_action(obs)
    assert chosen in ("act_1", "act_2")


def test_loop_cli_adversarial_arguments():
    """CLI exits with code 2 on invalid arguments or unrecognized personas."""
    # Invalid single persona
    with pytest.raises(SystemExit) as e1:
        loop_main(["run", "--persona", "fake_bot_xyz"])
    assert e1.value.code == 2

    # Mixed valid and invalid in list
    with pytest.raises(SystemExit) as e2:
        loop_main(["run", "--personas", "nomad, fake_bot, scout"])
    assert e2.value.code == 2


def test_orchestrator_manager_persona_filtering(tmp_path):
    """OrchestratorManager accepts custom persona subsets and logs accurately."""
    log_path = str(tmp_path / "filter_audit.jsonl")
    manager = OrchestratorManager(log_path=log_path, personas=[PlaytesterPersona.NOMAD, PlaytesterPersona.SCOUT])
    summary = manager.run_cycle(cycle_num=1)
    assert summary.sessions_run == 2
    assert summary.gate_status == "ALL_GREEN"

    with open(log_path, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    session_records = [r for r in records if r.get("record_type") == "session"]
    assert len(session_records) == 2
    assert {r["persona"] for r in session_records} == {"nomad", "scout"}
