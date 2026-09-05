"""Tests for the Flywheel Defect Triage Harness (adventure_forge.flywheel.triage).

Validates:
- Empty action trace execution without UnboundLocalError
- Illegal action defect confirmation (VERIFIED_DEFECT)
- Unreplayable/fabricated defect rejection (REJECTED_UNREPLAYABLE)
- Deadlock detection with playtester telemetry phrasing ("Dead end: No legal actions")
- Engine crash resilience (CRASH_DEFECT)
- PlaytesterDefectReport and TriageReport serialization
- Integration with BlindPlaytester session telemetry
- Replay determinism (identical SHA-256 fingerprints across runs)
- Multi-axis character state divergence during triage
"""
from adventure_forge.core.character import CharacterSheet, get_preset
from adventure_forge.core.engine import StepResult
from adventure_forge.flywheel.triage import (
    triage_defect_report,
    triage_playtester_report,
    triage_session_telemetry,
    reproduce_trace,
    PlaytesterDefectReport,
    TriageReport,
)
from adventure_forge.flywheel.playtester import BlindPlaytester


def test_triage_empty_trace_no_crash():
    """Empty action trace does not raise UnboundLocalError and reports cleanly."""
    char = get_preset("cutpurse").character
    report = triage_defect_report(
        initial_char=char,
        start_scene="warrens_gate",
        action_trace=[],
        claimed_defect="Nothing happened"
    )
    assert report.verified is False
    assert report.status == "REJECTED_UNREPLAYABLE"
    assert len(report.final_fingerprint) == 64


def test_triage_reproduces_invalid_action_defect():
    """Illegal action in trace is caught and verified as a defect."""
    char = get_preset("cutpurse").character
    report = triage_defect_report(
        initial_char=char,
        start_scene="warrens_gate",
        action_trace=["invalid_action_verb_xyz"],
        claimed_defect="Action failed"
    )
    assert report.verified is True
    assert report.status == "VERIFIED_DEFECT"
    assert "invalid_action_verb_xyz" in report.details
    assert report.error_step == 0


def test_triage_rejects_unreplayable_claim():
    """Valid trace with fabricated defect claim is rejected as unreplayable."""
    char = get_preset("cutpurse").character
    # In warrens_gate, slip_into_alley or examine_iron_bars is legal
    report = triage_defect_report(
        initial_char=char,
        start_scene="warrens_gate",
        action_trace=["slip_past_watch"],
        claimed_defect="Game crashed completely"
    )
    assert report.verified is False
    assert report.status == "REJECTED_UNREPLAYABLE"
    assert "Report rejected" in report.details


def test_triage_deadlock_detection(monkeypatch):
    """Detect deadlocks using both keyword and playtester 'Dead end: No legal actions' phrasing."""
    import adventure_forge.flywheel.triage as triage_mod

    # Mock engine.observe to simulate a scene with zero legal actions and not terminal
    orig_engine_cls = triage_mod.AdventureEngine

    class MockEngine(orig_engine_cls):
        def observe(self, state, events=None):
            obs = super().observe(state, events)
            # Force empty legal actions in non-terminal scene
            return StepResult(
                success=True,
                message="",
                scene_id=obs.scene_id,
                region_id=obs.region_id,
                title=obs.title,
                description=obs.description,
                events=obs.events,
                legal_actions=[],
                turn_count=obs.turn_count,
                is_terminal=False,
                outcome=None,
                fingerprint=obs.fingerprint
            )

    monkeypatch.setattr(triage_mod, "AdventureEngine", MockEngine)

    char = get_preset("cutpurse").character

    # Test with playtester telemetry phrasing
    playtester_claim = "Dead end: No legal actions at scene cell_101"
    report = triage_defect_report(char, "warrens_gate", [], playtester_claim)
    assert report.verified is True
    assert report.status == "VERIFIED_DEFECT"
    assert "Deadlock confirmed" in report.details

    # Test with standard deadlock phrasing
    report_std = triage_defect_report(char, "warrens_gate", [], "deadlock detected")
    assert report_std.verified is True
    assert report_std.status == "VERIFIED_DEFECT"


def test_triage_engine_crash_handling(monkeypatch):
    """Unhandled engine exceptions during transition are caught as CRASH_DEFECT."""
    import adventure_forge.flywheel.triage as triage_mod

    orig_engine_cls = triage_mod.AdventureEngine

    class CrashEngine(orig_engine_cls):
        def step(self, state, action_id):
            raise RuntimeError("Synthetic physics kernel panic")

    monkeypatch.setattr(triage_mod, "AdventureEngine", CrashEngine)

    char = get_preset("cutpurse").character
    report = triage_defect_report(char, "warrens_gate", ["any_action"], "Fatal crash")
    assert report.verified is True
    assert report.status == "CRASH_DEFECT"
    assert "Synthetic physics kernel panic" in report.details


def test_triage_report_serialization():
    """TriageReport and PlaytesterDefectReport serialize cleanly to dictionaries."""
    char = get_preset("cutpurse").character
    p_report = PlaytesterDefectReport(
        claimed_defect="Blocked door",
        action_trace=["open_door"],
        start_scene="warrens_gate",
        initial_char=char,
        seed=100,
        persona="explorer"
    )
    p_dict = p_report.to_dict()
    assert p_dict["claimed_defect"] == "Blocked door"
    assert p_dict["persona"] == "explorer"

    t_report = triage_playtester_report(p_report)
    t_dict = t_report.to_dict()
    assert "verified" in t_dict
    assert "status" in t_dict
    assert "reproduction_trace" in t_dict
    assert "final_fingerprint" in t_dict
    assert len(t_dict["final_fingerprint"]) == 64


def test_triage_playtester_telemetry_integration():
    """BlindPlaytester session friction notes integrate with triage_session_telemetry."""
    char = get_preset("warrior").character
    tester = BlindPlaytester(persona="explorer", seed=42)
    telemetry = tester.run_session(char, start_scene="crags_base", max_turns=5)

    # Inject a simulated friction note
    telemetry.friction_notes.append("Stuck on steep cliff: no legal actions")

    report = triage_session_telemetry(telemetry, char, start_scene="crags_base")
    assert report is not None
    assert isinstance(report, TriageReport)
    assert report.final_fingerprint != ""


def test_triage_determinism_same_seed():
    """Triage on identical inputs yields bit-identical fingerprints across runs."""
    char = get_preset("cutpurse").character
    trace = ["slip_past_watch"]
    r1 = triage_defect_report(char, "warrens_gate", trace, "claim", seed=42)
    r2 = triage_defect_report(char, "warrens_gate", trace, "claim", seed=42)
    assert r1.final_fingerprint == r2.final_fingerprint
    assert r1.status == r2.status


def test_triage_character_trait_divergence():
    """Triage reflects character capability differences (Silas with lockpick vs character without)."""
    silas = get_preset("cutpurse").character
    # Silas has lockpick and cunning 4 -> pick_sewer_grate is legal
    r_silas = triage_defect_report(
        silas,
        "warrens_gate",
        ["pick_sewer_grate"],
        "Action was rejected",
        seed=42
    )
    # Silas can perform pick_sewer_grate, so the defect claim is rejected as unreplayable
    assert r_silas.verified is False
    assert r_silas.status == "REJECTED_UNREPLAYABLE"

    # Helpless character without lockpick and without cunning
    helpless = CharacterSheet(
        name="Helpless",
        ancestry="Plainsman",
        background="drifter",
        attributes={"agility": 8, "strength": 8},
        skills={},
        traits=[],
        flaws=[],
        inventory=[]
    )
    r_helpless = triage_defect_report(
        helpless,
        "warrens_gate",
        ["pick_sewer_grate"],
        "Action was rejected",
        seed=42
    )
    # Helpless character cannot pick the grate; action fails -> defect reproduced
    assert r_helpless.verified is True
    assert r_helpless.status == "VERIFIED_DEFECT"


def test_reproduce_trace_api_skill_runbook():
    """Verify reproduce_trace matches the exact usage contract from af-playtest/SKILL.md."""
    result = reproduce_trace(seed=999, preset="cutpurse", action_sequence=["examine_lock", "pick_lock"])
    assert result.matches_expected is True
    assert result.actual_fingerprint == result.final_fingerprint
    assert len(result.actual_fingerprint) == 64
    assert result.status == "VERIFIED_DEFECT"
    assert "examine_lock" in result.details or "failed" in result.details


def test_reproduce_trace_valid_trace_verified():
    """A valid action trace reproduces cleanly and verifies replay execution."""
    result = reproduce_trace(
        seed=42,
        preset="cutpurse",
        action_sequence=["slip_past_watch"],
        start_scene="warrens_gate",
    )
    assert result.matches_expected is True
    assert result.verified is True
    assert result.status == "VERIFIED_REPLAY"
    assert result.actual_fingerprint == result.final_fingerprint
    assert len(result.actual_fingerprint) == 64

    # Verification with matching expected_fingerprint
    res_expected = reproduce_trace(
        seed=42,
        preset="cutpurse",
        action_sequence=["slip_past_watch"],
        start_scene="warrens_gate",
        expected_fingerprint=result.actual_fingerprint,
    )
    assert res_expected.matches_expected is True
    assert res_expected.verified is True
    assert res_expected.status == "VERIFIED_REPLAY"

    # Verification with mismatched expected_fingerprint
    res_mismatch = reproduce_trace(
        seed=42,
        preset="cutpurse",
        action_sequence=["slip_past_watch"],
        start_scene="warrens_gate",
        expected_fingerprint="0" * 64,
    )
    assert res_mismatch.matches_expected is False
    assert res_mismatch.verified is False
    assert res_mismatch.status == "FINGERPRINT_MISMATCH"

    # Defect triage preservation: explicit defect claim on clean trace is rejected
    res_unrep = reproduce_trace(
        seed=42,
        preset="cutpurse",
        action_sequence=["slip_past_watch"],
        start_scene="warrens_gate",
        claimed_defect="Alleged game crash",
    )
    assert res_unrep.matches_expected is False
    assert res_unrep.verified is False
    assert res_unrep.status == "REJECTED_UNREPLAYABLE"


def test_reproduce_trace_persona_fallback():
    """reproduce_trace handles persona names like 'nomad', 'diver', and 'scout'."""
    res_nomad = reproduce_trace(seed=100, preset="nomad", action_sequence=[])
    assert res_nomad.failing_scene is None
    assert len(res_nomad.actual_fingerprint) == 64

    res_diver = reproduce_trace(seed=101, preset="diver", action_sequence=[])
    assert len(res_diver.actual_fingerprint) == 64

    res_scout = reproduce_trace(seed=102, preset="scout", action_sequence=[])
    assert len(res_scout.actual_fingerprint) == 64


def test_triage_report_properties_and_serialization():
    """TriageReport actual_fingerprint and matches_expected properties match verified and final_fingerprint."""
    report = TriageReport(
        verified=True,
        status="VERIFIED_DEFECT",
        reproduction_trace=["step1"],
        final_fingerprint="abc" * 21 + "d",
        details="defect verified",
        error_step=1,
        failing_scene="test_scene",
    )
    assert report.matches_expected is True
    assert report.actual_fingerprint == report.final_fingerprint

    data = report.to_dict()
    assert data["matches_expected"] is True
    assert data["actual_fingerprint"] == "abc" * 21 + "d"
    assert data["verified"] is True
    assert data["final_fingerprint"] == "abc" * 21 + "d"

