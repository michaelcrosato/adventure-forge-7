"""Tier 1 & Tier 2: Mechanical Verification Bar & Firewall (Feature 6 / R6) Test Suite.

Satisfies TEST_INFRA.md:
- Tier 1 Coverage (>= 5 tests)
- Tier 2 Boundary & Corner (>= 5 tests)
"""
from adventure_forge.verification.verify import run_all_verification
from adventure_forge.verification.crawler import crawl_world_graph
from adventure_forge.verification.counterfactual import verify_counterfactual_divergence
from adventure_forge.player import mcp_server
from adventure_forge.flywheel.playtester import BlindPlaytester, SessionTelemetry
from adventure_forge.flywheel.triage import triage_defect_report
from adventure_forge.core.character import CharacterSheet
from adventure_forge.linter.prose_linter import ProseLinter


# ── Tier 1: Unit Coverage (>= 5 tests) ───────────────────────────────────────

def test_verification_all_seven_gates_execute():
    """All 7 mechanical verification gates execute headlessly and return True."""
    passed = run_all_verification(verbose=False)
    assert passed is True


def test_information_firewall_hidden_attributes_omitted():
    """Player observation StepResult and MCP responses strictly omit privileged data."""
    mcp_server.reset()
    res = mcp_server.new_game("cutpurse")

    # Top-level keys check
    allowed_keys = {"success", "message", "status", "scene_id", "region_id",
                    "title", "description", "events", "legal_actions",
                    "turn_count", "is_terminal", "outcome", "fingerprint"}
    assert set(res.keys()).issubset(allowed_keys)

    # Privileged data forbidden
    forbidden = ["world_flags", "world_registry", "_scene_map", "engine", "DeterministicRNG", "seed"]
    for f in forbidden:
        assert f not in res

    # Action items must only have player-visible fields
    for act in res["legal_actions"]:
        assert "effects" not in act
        assert "condition" not in act


def test_playtester_persona_execution_no_privileged_access():
    """Blind playtester runs session interacting strictly via public player contract."""
    char = CharacterSheet(name="Bot", ancestry="Deep-Dweller", background="cutpurse")
    tester = BlindPlaytester(persona="explorer", seed=123)
    telemetry = tester.run_session(char, start_scene="crags_base", max_turns=5)

    assert isinstance(telemetry, SessionTelemetry)
    assert telemetry.turn_count > 0
    assert len(telemetry.decisions_made) == telemetry.turn_count
    assert 0.0 <= telemetry.retention_score <= 1.0


def test_flywheel_triage_defect_reproduction():
    """Flywheel triage reproducer verifies valid sessions and produces structured report."""
    char = CharacterSheet(name="TriageChar", ancestry="Plainsman", background="drifter")
    # Test triage with an intentional invalid action report
    report = triage_defect_report(
        initial_char=char,
        start_scene="crags_base",
        action_trace=["invalid_bogus_action"],
        claimed_defect="Action failed on illegal command"
    )

    assert report is not None
    assert report.verified is True
    assert report.status == "VERIFIED_DEFECT"
    assert "failed" in report.details.lower() or "action" in report.details.lower()


def test_tampered_playtest_report_rejected():
    """Clean trace submitted as a defect is rejected because no defect occurred."""
    char = CharacterSheet(name="TriageChar", ancestry="Plainsman", background="drifter")
    # A perfectly valid trace that does not deadlock or error
    report = triage_defect_report(
        initial_char=char,
        start_scene="crags_base",
        action_trace=["walk_to_warrens"],
        claimed_defect="Fake defect claim that the game crashed"
    )

    assert report is not None
    assert report.verified is False
    assert report.status == "REJECTED_UNREPLAYABLE"


# ── Tier 2: Boundary & Corner Tests (>= 5 tests) ─────────────────────────────

def test_minimal_proof_4_linter_failure_blocks_verify():
    """Minimal Proof #4: Injecting a simplicity linter violation fails the build."""
    linter = ProseLinter()
    # 1. Purple prose test
    bad_purple = "The dimly lit chamber exudes an ominous aura of dark malice."
    violations = linter.lint_text(bad_purple)
    assert len(violations) > 0

    # 2. Sentence length > 18 words test
    long_sentence = "The quick brown fox jumps over the lazy dog and then proceeds to run all the way down the long cobblestone road."
    violations_long = linter.lint_text(long_sentence)
    assert any("exceeds 18 words" in v for v in violations_long)


def test_crawler_bfs_reaches_100_percent_scenes():
    """SYS-05 Reachability crawler mathematically proves reachability of 520 scenes."""
    ok, msg, stats = crawl_world_graph()
    assert ok is True
    assert stats["visited_scenes"] == 520
    assert stats["total_scenes"] == 520
    assert len(stats["unvisited_scenes"]) == 0


def test_counterfactual_witness_pair_mathematical_divergence():
    """I4/G1 Counterfactual witness pair in warrens_gate proves distinct actions and prose."""
    ok, msg, evidence = verify_counterfactual_divergence()
    assert ok is True
    assert "flash_thief_signet" in evidence["build_a_actions"]
    assert "flash_thief_signet" not in evidence["build_b_actions"]
    assert "demand_guard_entry" in evidence["build_b_actions"]
    assert "demand_guard_entry" not in evidence["build_a_actions"]
    assert "thieves mark" in evidence["build_a_desc"].lower()
    assert "military salute" in evidence["build_b_desc"].lower()


def test_mcp_uninitialized_session_safety():
    """Calling step_game before new_game returns clean error response without crash."""
    mcp_server.reset()
    res = mcp_server.step_game("some_action")
    assert res["success"] is False
    assert "no active game session" in res["message"].lower()


def test_mcp_invalid_action_graceful_handling():
    """Calling step_game with illegal action returns failure StepResult without crash."""
    mcp_server.reset()
    mcp_server.new_game("cutpurse")
    res = mcp_server.step_game("bogus_invalid_action_id_123")
    assert res["success"] is False
    assert "rejected" in res["message"].lower() or "not currently legal" in res["message"].lower()
