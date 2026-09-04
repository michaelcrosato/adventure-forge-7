"""Adversarial stress challenge test suite for Milestone 3.

Empirically challenges:
1. Agent MCP Player Surface:
   - Repeated calls to step_game with random, invalid, and boundary action IDs.
   - Strict I6 Information Firewall: zero internal objects or private attributes leak.
   - Deterministic replay across independent sessions with identical seeds.
   - JSON-RPC protocol edge cases and dispatching.
2. CLI Pagination:
   - Negative pages, extreme out-of-bounds, 0-action scenes, 115-action stress scene.
3. Defect Triage Harness:
   - Empty traces, engine syntax/runtime exceptions, deadlock detection, and false claims.
   - Telemetry ingestion and PlaytesterDefectReport handling.
"""
import io
import json
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Any

from adventure_forge.core.character import get_preset, CharacterSheet
from adventure_forge.core.engine import AdventureEngine, StepResult
from adventure_forge.core.state import GameState
from adventure_forge.content.loader import build_world_registry
from adventure_forge.player.mcp_server import (
    MCPServer,
    handle_jsonrpc_request,
    run_stdio_server,
)
from adventure_forge.player.cli import render_ui
from adventure_forge.flywheel.triage import (
    triage_defect_report,
    PlaytesterDefectReport,
    triage_playtester_report,
    triage_session_telemetry,
)


# ============================================================================
# 1. MCP PLAYER SURFACE ADVERSARIAL TESTS
# ============================================================================

def test_mcp_stress_random_and_invalid_action_ids():
    """Call step_game repeatedly with extreme, boundary, and malformed action IDs."""
    srv = MCPServer(seed=777)
    obs = srv.new_game("cutpurse")
    assert obs["success"] is True
    initial_fp = obs["fingerprint"]
    initial_turn = obs["turn_count"]

    adversarial_action_ids = [
        "",
        "   ",
        "\t\n\r",
        "non_existent_action_id_xyz",
        "a" * 10000,
        "null\x00byte\x01action",
        "⚔️🔥🛡️🧙‍♂️",
        "DROP TABLE scenes; --",
        "<script>alert(1)</script>",
        "../../etc/passwd",
        "{'json': 'payload'}",
        "action_id_from_another_province_high_court_plea",
        "-1",
        "0",
        "99999999999999999999",
        "None",
        "__class__",
        "__init__",
    ]

    for bad_act in adversarial_action_ids:
        res = srv.step_game(bad_act)
        assert res["success"] is False, f"Action '{bad_act[:30]}' unexpectedly succeeded"
        assert res["status"] == "error"
        assert res["turn_count"] == initial_turn
        assert res["fingerprint"] == initial_fp
        assert json.dumps(res), "Failed JSON serialization"

    # State should remain intact and valid
    curr = srv.get_state()
    assert curr["turn_count"] == initial_turn
    assert curr["fingerprint"] == initial_fp


def test_mcp_step_game_uninitialized_and_terminal():
    """step_game behaves gracefully when uninitialized or after reaching terminal state."""
    srv = MCPServer()
    # Uninitialized
    uninit = srv.step_game("any_action")
    assert uninit["success"] is False
    assert "No active game session" in uninit["message"]

    # Terminal state simulation
    srv.new_game("cutpurse")
    srv.last_obs = StepResult(
        success=True,
        message="Adventure won",
        scene_id="end_scene",
        region_id="lower_warrens",
        title="Victory",
        description="The quest is complete.",
        events=["Won"],
        legal_actions=[],
        turn_count=20,
        is_terminal=True,
        outcome="HEROIC_VICTORY",
        fingerprint="abcd" * 16,
    )

    term_res = srv.step_game("some_action")
    assert term_res["success"] is False
    assert term_res["status"] == "terminal"
    assert "HEROIC_VICTORY" in term_res["message"]


def test_mcp_strict_i6_firewall_zero_leakage():
    """Verify zero internal objects, private attributes, or forbidden keys leak across I6 boundary."""
    srv = MCPServer(seed=42)

    ALLOWED_TOP_KEYS = {
        "success", "message", "status", "scene_id", "region_id",
        "title", "description", "events", "legal_actions",
        "turn_count", "is_terminal", "outcome", "fingerprint"
    }
    ALLOWED_ACTION_KEYS = {"id", "label", "category", "risk", "stamina_cost"}

    FORBIDDEN_KEY_SUBSTRINGS = [
        "world_flags", "history", "rng", "engine", "conditions",
        "effects", "target_scene", "prng", "seed_cursor", "inventory",
        "sheet", "callback", "character_sheet", "raw_"
    ]

    for preset in ["cutpurse", "noble", "warrior", "pit_fighter"]:
        obs = srv.new_game(preset)
        assert set(obs.keys()) == ALLOWED_TOP_KEYS

        # Check types
        assert isinstance(obs["success"], bool)
        assert isinstance(obs["message"], str)
        assert obs["status"] in ("active", "error", "terminal")
        assert isinstance(obs["scene_id"], str)
        assert isinstance(obs["region_id"], str)
        assert isinstance(obs["title"], str)
        assert isinstance(obs["description"], str)
        assert isinstance(obs["events"], list)
        assert all(isinstance(e, str) for e in obs["events"])
        assert isinstance(obs["legal_actions"], list)
        assert isinstance(obs["turn_count"], int)
        assert isinstance(obs["is_terminal"], bool)
        assert obs["outcome"] is None or isinstance(obs["outcome"], str)
        assert isinstance(obs["fingerprint"], str)

        for act in obs["legal_actions"]:
            assert set(act.keys()) == ALLOWED_ACTION_KEYS
            for k in act.keys():
                assert not k.startswith("_")
                for f_term in FORBIDDEN_KEY_SUBSTRINGS:
                    assert f_term not in k.lower()

        # Step forward
        for step in range(5):
            if obs["is_terminal"] or not obs["legal_actions"]:
                break
            act_id = obs["legal_actions"][0]["id"]
            obs = srv.step_game(act_id)
            assert set(obs.keys()) == ALLOWED_TOP_KEYS

        # Verify full JSON serialization has zero internal class mentions
        dumped = json.dumps(obs)
        for leak in ["GameState", "AdventureEngine", "CharacterSheet", "DeterministicRNG"]:
            assert leak not in dumped


def test_mcp_deterministic_replay_stress():
    """Two independent MCP servers with identical seeds yield bit-for-bit identical state across 50 steps."""
    for test_seed in [11, 42, 999, 123456]:
        srv1 = MCPServer(seed=test_seed)
        srv2 = MCPServer(seed=test_seed)

        o1 = srv1.new_game("cutpurse", seed=test_seed)
        o2 = srv2.new_game("cutpurse", seed=test_seed)
        assert o1["fingerprint"] == o2["fingerprint"]

        for step in range(25):
            # Interleave invalid action attempts
            bad = f"bad_action_{step}"
            b1 = srv1.step_game(bad)
            b2 = srv2.step_game(bad)
            assert b1 == b2

            # Valid action
            acts = o1["legal_actions"]
            if not acts or o1["is_terminal"]:
                break
            chosen = acts[step % len(acts)]["id"]
            o1 = srv1.step_game(chosen)
            o2 = srv2.step_game(chosen)
            assert o1["fingerprint"] == o2["fingerprint"]
            assert o1["scene_id"] == o2["scene_id"]
            assert o1["turn_count"] == o2["turn_count"]


def test_mcp_jsonrpc_protocol_adversarial():
    """Adversarial JSON-RPC 2.0 payloads over MCP surface."""
    srv = MCPServer(seed=42)
    # Ping
    ping_resp = handle_jsonrpc_request({"jsonrpc": "2.0", "id": 100, "method": "ping"}, srv)
    assert ping_resp == {"jsonrpc": "2.0", "id": 100, "result": {}}

    # Missing method / unknown method
    err_resp = handle_jsonrpc_request({"jsonrpc": "2.0", "id": 101, "method": "non_standard_exec"}, srv)
    assert err_resp is not None
    assert err_resp["error"]["code"] == -32601

    # Call tool with type mismatch
    tool_resp = handle_jsonrpc_request({
        "jsonrpc": "2.0", "id": 102, "method": "tools/call",
        "params": {"name": "step_game", "arguments": {"action_id": 9999}}
    }, srv)
    assert tool_resp is not None
    assert tool_resp["result"]["isError"] is True


# ============================================================================
# 2. CLI PAGINATION ADVERSARIAL TESTS
# ============================================================================

@dataclass
class _MockObs:
    title: str = "Adversarial Arena"
    region_id: str = "stress_realm"
    description: str = "Testing pagination boundaries."
    events: List[str] = field(default_factory=list)
    legal_actions: List[Dict[str, Any]] = field(default_factory=list)


def _render_to_string(obs, page=0, page_size=15) -> str:
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        render_ui(obs, page=page, page_size=page_size)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


def test_cli_pagination_adversarial_page_inputs():
    """Test negative pages, extreme out-of-bounds, 0-action scenes, and 115-action stress scene."""
    # 1. 0-action scene with various page values
    zero_obs = _MockObs(legal_actions=[])
    for p in [-1000, -1, 0, 1, 100, 99999]:
        out = _render_to_string(zero_obs, page=p, page_size=15)
        assert "AVAILABLE ACTIONS (0 total | Page 1 of 1):" in out
        assert "No actions available." in out
        assert "Showing" not in out

    # 2. 115-action stress scene (bazaar_center)
    reg = build_world_registry()
    eng = AdventureEngine(reg)
    char = CharacterSheet(name="Adversary", ancestry="Plainsman", background="merchant")
    state = GameState(
        build_id="t", session_id="s", character=char,
        current_region="stress_market", current_scene="bazaar_center"
    )
    bazaar_obs = eng.observe(state)
    assert len(bazaar_obs.legal_actions) == 115

    # Negative page clamps to Page 1
    out_neg = _render_to_string(bazaar_obs, page=-50, page_size=15)
    assert "AVAILABLE ACTIONS (115 total | Page 1 of 8 | Showing 1-15):" in out_neg

    # Out of bounds positive page clamps to Page 8
    out_pos = _render_to_string(bazaar_obs, page=9999, page_size=15)
    assert "AVAILABLE ACTIONS (115 total | Page 8 of 8 | Showing 106-115):" in out_pos

    # Test all 8 pages for completeness
    for p in range(8):
        page_out = _render_to_string(bazaar_obs, page=p, page_size=15)
        assert f"Page {p + 1} of 8" in page_out

    # 3. Varying page_sizes
    for ps in [1, 10, 50, 115, 200]:
        ps_out = _render_to_string(bazaar_obs, page=0, page_size=ps)
        assert f"Showing 1-{min(ps, 115)}" in ps_out


# ============================================================================
# 3. DEFECT TRIAGE HARNESS ADVERSARIAL TESTS
# ============================================================================

def test_triage_empty_trace_adversarial():
    """Empty traces with various defect claims and scene targets."""
    char = get_preset("cutpurse").character

    # Normal scene, unreplayable claim
    r1 = triage_defect_report(char, "warrens_gate", [], "Unreplayable fantasy")
    assert r1.verified is False
    assert r1.status == "REJECTED_UNREPLAYABLE"
    assert len(r1.final_fingerprint) == 64

    # Non-existent scene should verify as initial scene defect
    r2 = triage_defect_report(char, "invalid_non_existent_scene_000", [], "Missing node")
    assert r2.verified is True
    assert r2.status == "VERIFIED_DEFECT"
    assert "Missing scene" in r2.details
    assert r2.error_step == 0


def test_triage_engine_syntax_and_runtime_exceptions(monkeypatch):
    """Engine crashes (SyntaxError, TypeError, ZeroDivisionError) triaged as CRASH_DEFECT."""
    import adventure_forge.flywheel.triage as triage_mod

    orig_engine_cls = triage_mod.AdventureEngine

    exceptions_to_test = [
        SyntaxError("Invalid condition AST"),
        TypeError("NoneType object is not subscriptable"),
        ZeroDivisionError("Division by zero in skill check"),
        KeyError("world_flags['missing_quest']"),
    ]

    for test_exc in exceptions_to_test:
        class CrashEngine(orig_engine_cls):
            def step(self, state, action_id):
                if action_id == "fatal_action":
                    raise test_exc
                return super().step(state, action_id)

        monkeypatch.setattr(triage_mod, "AdventureEngine", CrashEngine)
        char = get_preset("cutpurse").character
        report = triage_defect_report(
            initial_char=char,
            start_scene="warrens_gate",
            action_trace=["slip_past_watch", "fatal_action", "unreached_step"],
            claimed_defect="Engine crashed"
        )
        assert report.verified is True
        assert report.status == "CRASH_DEFECT"
        assert report.error_step == 1
        assert report.reproduction_trace == ["slip_past_watch", "fatal_action"]


def test_triage_deadlock_scenarios(monkeypatch):
    """Stress test deadlock verification vs false claims vs terminal states."""
    import adventure_forge.flywheel.triage as triage_mod

    orig_engine_cls = triage_mod.AdventureEngine
    char = get_preset("cutpurse").character

    # Scenario A: True deadlock (non-terminal scene, 0 legal actions)
    class DeadlockMock(orig_engine_cls):
        def observe(self, state, events=None):
            obs = super().observe(state, events)
            return StepResult(
                success=True, message="", scene_id=obs.scene_id, region_id=obs.region_id,
                title=obs.title, description=obs.description, events=obs.events,
                legal_actions=[], turn_count=obs.turn_count, is_terminal=False,
                outcome=None, fingerprint=obs.fingerprint
            )

    monkeypatch.setattr(triage_mod, "AdventureEngine", DeadlockMock)
    rep_deadlock = triage_defect_report(char, "warrens_gate", [], "Stuck with no options")
    assert rep_deadlock.verified is True
    assert rep_deadlock.status == "VERIFIED_DEFECT"
    assert "Deadlock confirmed" in rep_deadlock.details

    # Scenario B: Terminal scene with 0 legal actions (normal game over, NOT deadlock)
    class TerminalMock(orig_engine_cls):
        def observe(self, state, events=None):
            obs = super().observe(state, events)
            return StepResult(
                success=True, message="", scene_id=obs.scene_id, region_id=obs.region_id,
                title=obs.title, description=obs.description, events=obs.events,
                legal_actions=[], turn_count=obs.turn_count, is_terminal=True,
                outcome="DEFEAT", fingerprint=obs.fingerprint
            )

    monkeypatch.setattr(triage_mod, "AdventureEngine", TerminalMock)
    rep_terminal = triage_defect_report(char, "warrens_gate", [], "Softlock dead end")
    assert rep_terminal.verified is False
    assert rep_terminal.status == "REJECTED_UNREPLAYABLE"


def test_triage_playtester_telemetry_adversarial():
    """Triage ingestion with sparse, malformed, or empty telemetry."""
    char = get_preset("warrior").character

    @dataclass
    class SparseTelemetry:
        friction_notes: List[str] = field(default_factory=list)
        scenes_visited: List[str] = field(default_factory=list)
        decisions_made: List[str] = field(default_factory=list)

    # Empty telemetry
    empty_t = SparseTelemetry()
    res_empty = triage_session_telemetry(empty_t, char)
    assert res_empty is None

    # Telemetry with friction note and valid decisions
    active_t = SparseTelemetry(
        friction_notes=["Action failed unexpectedly"],
        scenes_visited=["crags_base"],
        decisions_made=["search_scree"]
    )
    res_active = triage_session_telemetry(active_t, char)
    assert res_active is not None
    # search_scree is legal in crags_base, so false defect claim is rejected
    assert res_active.verified is False
    assert res_active.status == "REJECTED_UNREPLAYABLE"

    # PlaytesterDefectReport roundtrip
    p_report = PlaytesterDefectReport(
        claimed_defect="Ghost issue",
        action_trace=["fake_step"],
        start_scene="crags_base",
        initial_char=char,
    )
    t_rep = triage_playtester_report(p_report)
    assert t_rep.verified is True
    assert t_rep.status == "VERIFIED_DEFECT"
    assert "fake_step" in t_rep.details


def test_mcp_stdio_crash_resilience(monkeypatch):
    """Ensure MCP stdio loop and request handling never crash on non-dict, non-string, or malformed input."""
    # 1. Non-dict request structure returns -32600
    res_list = handle_jsonrpc_request([1, 2, 3])  # type: ignore[arg-type]
    assert res_list is not None
    assert res_list.get("error", {}).get("code") == -32600

    res_str = handle_jsonrpc_request("hello")  # type: ignore[arg-type]
    assert res_str is not None
    assert res_str.get("error", {}).get("code") == -32600

    # 2. Non-dict params or arguments
    srv = MCPServer()
    res_bad_params = handle_jsonrpc_request(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": "invalid"},
        srv,
    )
    assert res_bad_params is not None
    assert res_bad_params.get("id") == 1

    # 3. Non-string preset defaults cleanly to cutpurse
    res_bad_preset = handle_jsonrpc_request(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "new_game", "arguments": {"preset": 12345}}},
        srv,
    )
    assert res_bad_preset is not None
    assert res_bad_preset["result"]["isError"] is False

    # 4. End-to-end stdio server loop with diverse malformed lines
    fake_input = "\n".join([
        "[1, 2, 3]",
        '{"jsonrpc": "2.0", "id": 10, "method": "ping"}',
        "not-valid-json{{{",
        '{"jsonrpc": "2.0", "id": 11, "method": "tools/call", "params": null}',
        "",
    ]) + "\n"

    fake_stdout = io.StringIO()

    monkeypatch.setattr(sys, "stdin", fake_input.splitlines(keepends=True))
    monkeypatch.setattr(sys, "stdout", fake_stdout)

    run_stdio_server(srv)
    output_lines = [json.loads(line) for line in fake_stdout.getvalue().strip().split("\n") if line.strip()]

    assert len(output_lines) == 4
    # Line 1: [1, 2, 3] -> -32600
    assert output_lines[0]["error"]["code"] == -32600
    # Line 2: ping -> result {}
    assert output_lines[1]["id"] == 10
    # Line 3: invalid JSON -> -32700
    assert output_lines[2]["error"]["code"] == -32700
    # Line 4: params null -> handles without crash
    assert output_lines[3]["id"] == 11
