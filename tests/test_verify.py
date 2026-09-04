"""Tests for the Canonical Verification Command (adventure_forge.verify and ./verify).

Validates:
- Module import and forwarding contracts
- In-process execution of run_all_verification
- Subprocess CLI execution via python -m adventure_forge.verify
- Executable ./verify script execution
- Gate failure exit code propagation
- All 7 gates coverage
- Verbose vs quiet modes
- Clean stderr invariant
"""
import os
import sys
import subprocess
import pytest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


def test_verify_module_importable():
    """Verify adventure_forge.verify imports cleanly and exposes canonical entrypoints."""
    import adventure_forge.verify as v
    assert hasattr(v, "main"), "adventure_forge.verify must expose main()"
    assert hasattr(v, "run_all_verification"), "adventure_forge.verify must expose run_all_verification()"
    assert callable(v.main)
    assert callable(v.run_all_verification)


def test_verify_run_all_verification_success():
    """In-process verification execution passes all 7 gates."""
    from adventure_forge.verify import run_all_verification
    result = run_all_verification(verbose=False)
    assert result is True, "run_all_verification must return True when all gates pass"


def test_verify_cli_module_execution():
    """CLI invocation via python3 -m adventure_forge.verify succeeds with exit code 0."""
    cmd = [sys.executable, "-m", "adventure_forge.verify"]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(WORKSPACE_ROOT)
    proc = subprocess.run(cmd, cwd=str(WORKSPACE_ROOT), capture_output=True, text=True, env=env)
    assert proc.returncode == 0, f"Process exited with {proc.returncode}. Stderr: {proc.stderr}"
    assert "VERIFICATION RESULT: ALL GATES GREEN" in proc.stdout


def test_verify_root_script_execution():
    """Root ./verify executable shell script succeeds with exit code 0."""
    script = WORKSPACE_ROOT / "verify"
    assert script.exists(), "./verify must exist"
    assert os.access(script, os.X_OK), "./verify must be executable"

    proc = subprocess.run([str(script)], cwd=str(WORKSPACE_ROOT), capture_output=True, text=True)
    assert proc.returncode == 0, f"./verify failed with {proc.returncode}. Stderr: {proc.stderr}"
    assert "ALL GATES GREEN" in proc.stdout
    assert "✓ PASS" in proc.stdout


def test_verify_gate_failure_propagates_exit_code(monkeypatch):
    """When any gate fails, run_all_verification returns False and main() exits 1."""
    import adventure_forge.verification.verify as v_mod
    import adventure_forge.verify as top_v

    # Monkeypatch a gate to return failure
    monkeypatch.setattr(
        v_mod,
        "verify_replay_determinism",
        lambda: (False, "Forced synthetic failure for gate testing")
    )

    result = v_mod.run_all_verification(verbose=False)
    assert result is False, "Verification must return False if any gate fails"

    with pytest.raises(SystemExit) as excinfo:
        top_v.main()
    assert excinfo.value.code == 1, "main() must exit with code 1 upon gate failure"


def test_verify_all_seven_gates_present(capsys):
    """Ensure all 7 verification gates execute sequentially."""
    from adventure_forge.verify import run_all_verification
    run_all_verification(verbose=True)
    captured = capsys.readouterr().out

    expected_gates = [
        "[1/7] Verifying I1 Determinism",
        "[2/7] Verifying World Graph Link Integrity",
        "[3/7] Verifying G2 High-Velocity Hemingway Prose Linter",
        "[4/7] Verifying I4/G1/G3 Counterfactual Character Divergence",
        "[5/7] Verifying G6 Unbounded Choice Scaling",
        "[6/7] Verifying SYS-05 Non-LLM Reachability Crawler",
        "[7/7] Verifying SYS-06 Macro-World Interactable Density Invariant",
    ]
    for gate in expected_gates:
        assert gate in captured, f"Missing expected gate output: {gate}"


def test_verify_verbose_and_quiet_modes():
    """Both verbose=True and verbose=False execute without error."""
    from adventure_forge.verify import run_all_verification
    assert run_all_verification(verbose=False) is True
    assert run_all_verification(verbose=True) is True


def test_verify_exit_zero_clean_stderr():
    """Running ./verify outputs zero warnings or tracebacks on stderr."""
    script = WORKSPACE_ROOT / "verify"
    proc = subprocess.run([str(script)], cwd=str(WORKSPACE_ROOT), capture_output=True, text=True)
    assert proc.returncode == 0
    assert proc.stderr.strip() == "", f"Expected clean stderr, got: {proc.stderr}"
