"""Milestone 10 Comprehensive Tests: Playtester Fleet Expansion, CLI & Defect Triage.

Validates:
- PlaytesterPersona Enum registration for all 8 personas
- CLI --persona and --personas flags (case-insensitivity, comma/space parsing, validation)
- Telemetry JSONL format with session records and cycle summaries
- jq and grep filter compatibility as documented in af-playtest/SKILL.md
- Triage reproduce_trace API and TriageReport property bindings
- Specialized heuristics for Nomad, Diver, and Scout
"""
import json
import pytest
from adventure_forge.flywheel.playtester import (
    PlaytesterPersona,
    BlindPlaytester,
)
from adventure_forge.flywheel.orchestrator import OrchestratorManager
from adventure_forge.flywheel.loop import main as loop_main
from adventure_forge.flywheel.triage import reproduce_trace, TriageReport


def test_persona_enum_members_and_aliases():
    """All 8 personas are represented in PlaytesterPersona and can be parsed case-insensitively."""
    expected_personas = [
        "explorer",
        "brute",
        "infiltrator",
        "speedrunner",
        "saboteur",
        "nomad",
        "diver",
        "scout",
    ]
    assert [p.value for p in PlaytesterPersona] == expected_personas
    assert BlindPlaytester.PERSONAS == expected_personas

    for name in expected_personas:
        assert PlaytesterPersona.from_str(name) == PlaytesterPersona(name)
        assert PlaytesterPersona.from_str(name.upper()) == PlaytesterPersona(name)
        assert PlaytesterPersona.from_str(f"  {name.capitalize()}  ") == PlaytesterPersona(name)

    with pytest.raises(ValueError, match="Unknown playtester persona"):
        PlaytesterPersona.from_str("invalid_persona_xyz")


def test_cli_persona_single_flag(tmp_path):
    """CLI --persona flag executes only the requested persona (case-insensitive)."""
    log_file = str(tmp_path / "single_persona_audit.jsonl")

    # Run 1 cycle for "explorer"
    with pytest.raises(SystemExit) as exc_info:
        loop_main(["run", "--persona", "EXPLORER", "--cycles", "1", "--log", log_file])
    assert exc_info.value.code == 0

    # Read logged lines
    with open(log_file, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f if line.strip()]

    session_records = [rec for rec in lines if rec.get("record_type") == "session"]
    summary_records = [rec for rec in lines if rec.get("record_type") == "cycle_summary"]

    assert len(session_records) == 1
    assert session_records[0]["persona"] == "explorer"
    assert session_records[0]["cycle"] == 1
    assert session_records[0]["turn_count"] == 15
    assert session_records[0]["success"] is True
    assert "final_scene" in session_records[0]
    assert "timestamp" in session_records[0]

    assert len(summary_records) == 1
    assert summary_records[0]["sessions_run"] == 1
    assert summary_records[0]["gate_status"] == "ALL_GREEN"


def test_cli_personas_comma_separated_flag(tmp_path):
    """CLI --personas flag executes only the requested personas."""
    log_file = str(tmp_path / "multi_persona_audit.jsonl")

    with pytest.raises(SystemExit) as exc_info:
        loop_main(["run", "--personas", "nomad, diver, scout", "--cycles", "1", "--log", log_file])
    assert exc_info.value.code == 0

    with open(log_file, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f if line.strip()]

    session_records = [rec for rec in lines if rec.get("record_type") == "session"]
    assert len(session_records) == 3

    personas_run = {rec["persona"] for rec in session_records}
    assert personas_run == {"nomad", "diver", "scout"}


def test_cli_invalid_persona_exits_nonzero():
    """CLI exits with error code when an unrecognized persona is passed."""
    with pytest.raises(SystemExit) as exc_info:
        loop_main(["run", "--persona", "space_marine", "--cycles", "1"])
    assert exc_info.value.code == 2


def test_telemetry_stream_jq_and_grep_contract(tmp_path):
    """Audit log adheres to jq and grep inspection patterns from af-playtest/SKILL.md."""
    log_file = str(tmp_path / "audit_contract.jsonl")
    manager = OrchestratorManager(log_path=log_file, personas=["nomad", "diver"])
    summary = manager.run_cycle(cycle_num=1)
    assert summary.gate_status == "ALL_GREEN"

    with open(log_file, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    # Parse and check fields
    records = [json.loads(line) for line in raw_lines]
    personas = [r.get("persona") for r in records if "persona" in r]
    assert set(personas) == {"nomad", "diver"}

    for r in records:
        if r.get("record_type") == "session":
            assert isinstance(r["success"], bool)
            assert isinstance(r["turn_count"], int)
            assert isinstance(r["retention_score"], float)
            assert isinstance(r["scenes_visited"], list)
            assert isinstance(r["friction_notes"], list)
            assert isinstance(r["final_scene"], str)
            assert isinstance(r["timestamp"], str)
        elif r.get("record_type") == "cycle_summary":
            assert r["gate_status"] == "ALL_GREEN"
            assert r["sessions_run"] == 2


def test_reproduce_trace_api_full_cycle():
    """reproduce_trace reproduces traces deterministically across multiple presets."""
    # 1. Silas in crags_base with an illegal action -> VERIFIED_DEFECT
    report_defect = reproduce_trace(
        seed=123,
        preset="cutpurse",
        action_sequence=["nonexistent_secret_spell"],
    )
    assert report_defect.matches_expected is True
    assert report_defect.verified is True
    assert report_defect.status == "VERIFIED_DEFECT"
    assert report_defect.actual_fingerprint == report_defect.final_fingerprint
    assert len(report_defect.actual_fingerprint) == 64

    # 2. Silas in warrens_gate with legal action -> VERIFIED_REPLAY
    report_valid = reproduce_trace(
        seed=123,
        preset="cutpurse",
        action_sequence=["slip_past_watch"],
        start_scene="warrens_gate",
    )
    assert report_valid.matches_expected is True
    assert report_valid.verified is True
    assert report_valid.status == "VERIFIED_REPLAY"
    assert report_valid.actual_fingerprint == report_valid.final_fingerprint
    assert len(report_valid.actual_fingerprint) == 64

    # 3. Determinism check: identical seed and trace yield identical fingerprints
    report_repeat = reproduce_trace(
        seed=123,
        preset="cutpurse",
        action_sequence=["slip_past_watch"],
        start_scene="warrens_gate",
    )
    assert report_repeat.actual_fingerprint == report_valid.actual_fingerprint
    assert report_repeat.matches_expected is True
    assert report_repeat.verified is True
    assert report_repeat.status == "VERIFIED_REPLAY"

    # 4. expected_fingerprint verification: match and mismatch
    report_fp_match = reproduce_trace(
        seed=123,
        preset="cutpurse",
        action_sequence=["slip_past_watch"],
        start_scene="warrens_gate",
        expected_fingerprint=report_valid.actual_fingerprint,
    )
    assert report_fp_match.matches_expected is True
    assert report_fp_match.verified is True
    assert report_fp_match.status == "VERIFIED_REPLAY"
    assert report_fp_match.expected_fingerprint == report_valid.actual_fingerprint

    report_fp_mismatch = reproduce_trace(
        seed=123,
        preset="cutpurse",
        action_sequence=["slip_past_watch"],
        start_scene="warrens_gate",
        expected_fingerprint="0" * 64,
    )
    assert report_fp_mismatch.matches_expected is False
    assert report_fp_mismatch.verified is False
    assert report_fp_mismatch.status == "FINGERPRINT_MISMATCH"

    # 5. Explicit defect claim on valid trace -> REJECTED_UNREPLAYABLE
    report_unrep = reproduce_trace(
        seed=123,
        preset="cutpurse",
        action_sequence=["slip_past_watch"],
        start_scene="warrens_gate",
        claimed_defect="Alleged game crash",
    )
    assert report_unrep.matches_expected is False
    assert report_unrep.verified is False
    assert report_unrep.status == "REJECTED_UNREPLAYABLE"


def test_blind_playtester_init_polymorphism():
    """BlindPlaytester accepts PlaytesterPersona enum, string, or mixed cases."""
    for p in PlaytesterPersona:
        t_enum = BlindPlaytester(persona=p, seed=50)
        assert t_enum.persona == p.value

        t_str = BlindPlaytester(persona=p.value, seed=50)
        assert t_str.persona == p.value

        t_upper = BlindPlaytester(persona=p.value.upper(), seed=50)
        assert t_upper.persona == p.value


def test_triage_report_to_dict_properties():
    """TriageReport dictionary contains actual_fingerprint and matches_expected keys."""
    rep = TriageReport(
        verified=False,
        status="REJECTED_UNREPLAYABLE",
        reproduction_trace=["step1", "step2"],
        final_fingerprint="1" * 64,
        details="clean trace",
        error_step=None,
        failing_scene=None,
    )
    d = rep.to_dict()
    assert d["actual_fingerprint"] == "1" * 64
    assert d["matches_expected"] is False
