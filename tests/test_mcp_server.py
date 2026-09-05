"""Tests for the Agent MCP Player Surface (adventure_forge.player.mcp_server).

Validates:
- Module interface contracts (new_game, step_game, get_state)
- Preset routing (cutpurse, noble, warrior, pit_fighter)
- Error resilience and graceful failures
- State query idempotency
- Legal action execution and state transitions
- Illegal action rejection without state mutation
- Uninitialized session handling
- Strict I6 Information Firewall (zero engine internals or code leakage)
- Deterministic replay reproducibility over MCP surface
- JSON-RPC 2.0 protocol handling
"""
import json
from adventure_forge.player import mcp_server as mcp
from adventure_forge.player.mcp_server import MCPServer, handle_jsonrpc_request


def test_mcp_module_exports():
    """Module exports the canonical interface functions."""
    assert hasattr(mcp, "new_game"), "mcp_server must export new_game"
    assert hasattr(mcp, "step_game"), "mcp_server must export step_game"
    assert hasattr(mcp, "get_state"), "mcp_server must export get_state"
    assert callable(mcp.new_game)
    assert callable(mcp.step_game)
    assert callable(mcp.get_state)


def test_new_game_default_preset():
    """Default new_game() uses cutpurse preset at warrens_gate."""
    obs = mcp.new_game()
    assert obs["success"] is True
    assert obs["scene_id"] == "warrens_gate"
    assert obs["region_id"] == "lower_warrens"
    assert obs["status"] == "active"
    assert obs["turn_count"] == 0
    assert isinstance(obs["legal_actions"], list)
    assert len(obs["legal_actions"]) >= 4


def test_new_game_all_presets():
    """All canonical presets route to their designated starting scenes."""
    noble_obs = mcp.new_game("noble")
    assert noble_obs["success"] is True
    assert noble_obs["scene_id"] == "court_antechamber"
    assert noble_obs["region_id"] == "high_court"

    warrior_obs = mcp.new_game("warrior")
    assert warrior_obs["success"] is True
    assert warrior_obs["scene_id"] == "crags_base"
    assert warrior_obs["region_id"] == "iron_crags"

    pit_obs = mcp.new_game("pit_fighter")
    assert pit_obs["success"] is True
    assert pit_obs["scene_id"] == "crags_base"


def test_new_game_unknown_preset_graceful():
    """Unknown presets return an error observation without raising unhandled exceptions."""
    obs = mcp.new_game("unknown_wizard_archetype")
    assert obs["success"] is False
    assert obs["status"] == "error"
    assert "Unknown preset" in obs["message"]
    assert "cutpurse" in obs["message"]


def test_get_state_idempotent():
    """get_state() is a pure query; calling it repeatedly leaves state unchanged."""
    init_obs = mcp.new_game("cutpurse")
    turn = init_obs["turn_count"]
    fp = init_obs["fingerprint"]

    s1 = mcp.get_state()
    s2 = mcp.get_state()

    assert s1["turn_count"] == turn
    assert s2["turn_count"] == turn
    assert s1["fingerprint"] == fp
    assert s2["fingerprint"] == fp
    assert s1["scene_id"] == init_obs["scene_id"]


def test_step_game_legal_action():
    """Executing a legal action advances turn count and updates state fingerprint."""
    obs = mcp.new_game("cutpurse")
    assert len(obs["legal_actions"]) > 0
    action = obs["legal_actions"][0]["id"]
    initial_fp = obs["fingerprint"]

    next_obs = mcp.step_game(action)
    assert next_obs["success"] is True
    assert next_obs["turn_count"] == 1
    assert next_obs["fingerprint"] != initial_fp
    assert isinstance(next_obs["events"], list)


def test_step_game_illegal_action():
    """Executing an illegal action returns success=False and does not advance turn count."""
    obs = mcp.new_game("cutpurse")
    turn_before = obs["turn_count"]
    fp_before = obs["fingerprint"]

    res = mcp.step_game("totally_invalid_action_id_xyz")
    assert res["success"] is False
    assert res["status"] == "error"

    curr = mcp.get_state()
    assert curr["turn_count"] == turn_before
    assert curr["fingerprint"] == fp_before


def test_step_game_uninitialized_session():
    """Stepping before new_game() returns an error observation gracefully."""
    mcp.reset()
    res = mcp.step_game("some_action")
    assert res["success"] is False
    assert "No active game session" in res["message"]

    state_res = mcp.get_state()
    assert state_res["success"] is False
    assert "No active game session" in state_res["message"]


def test_information_firewall_top_level_and_actions():
    """Enforce I6 Information Firewall: only player-safe fields, zero engine leaks."""
    server = MCPServer(seed=42)
    obs = server.new_game("cutpurse")

    allowed_top_keys = {
        "success", "message", "status", "scene_id", "region_id",
        "title", "description", "events", "legal_actions",
        "turn_count", "is_terminal", "outcome", "fingerprint"
    }
    assert set(obs.keys()) == allowed_top_keys, f"Unexpected top-level keys: {set(obs.keys()) - allowed_top_keys}"

    forbidden_patterns = ["world_flags", "history", "rng", "engine", "conditions", "effects", "target_scene"]
    for k in obs.keys():
        for pat in forbidden_patterns:
            assert pat not in k.lower(), f"Forbidden key pattern '{pat}' leaked: {k}"

    allowed_action_keys = {"id", "label", "category", "risk", "stamina_cost"}
    for act in obs["legal_actions"]:
        assert set(act.keys()) == allowed_action_keys, f"Unexpected action keys: {set(act.keys()) - allowed_action_keys}"
        for act_k in act.keys():
            for pat in forbidden_patterns:
                assert pat not in act_k.lower(), f"Forbidden action key '{pat}' leaked: {act_k}"

    # Must serialize cleanly to standard JSON
    serialized = json.dumps(obs)
    assert isinstance(serialized, str)


def test_deterministic_replay_via_mcp():
    """Two independent MCP sessions with identical seeds and inputs produce bit-identical states."""
    srv1 = MCPServer(seed=12345)
    srv2 = MCPServer(seed=12345)

    o1 = srv1.new_game("cutpurse")
    o2 = srv2.new_game("cutpurse")
    assert o1["fingerprint"] == o2["fingerprint"]

    # Step through 3 actions
    for _ in range(3):
        assert len(o1["legal_actions"]) > 0
        action = o1["legal_actions"][0]["id"]
        o1 = srv1.step_game(action)
        o2 = srv2.step_game(action)
        assert o1["fingerprint"] == o2["fingerprint"]
        assert o1["scene_id"] == o2["scene_id"]


def test_jsonrpc_protocol_handling():
    """Test stdio JSON-RPC 2.0 initialize, tools/list, and tools/call."""
    server = MCPServer(seed=42)

    # initialize
    init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    init_res = handle_jsonrpc_request(init_req, server)
    assert init_res["id"] == 1
    assert "tools" in init_res["result"]["capabilities"]

    # tools/list
    list_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    list_res = handle_jsonrpc_request(list_req, server)
    tools = list_res["result"]["tools"]
    tool_names = [t["name"] for t in tools]
    assert "new_game" in tool_names
    assert "step_game" in tool_names
    assert "get_state" in tool_names

    # tools/call: new_game
    call_req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "new_game", "arguments": {"preset": "noble"}}
    }
    call_res = handle_jsonrpc_request(call_req, server)
    assert call_res["id"] == 3
    assert call_res["result"]["isError"] is False
    payload = json.loads(call_res["result"]["content"][0]["text"])
    assert payload["scene_id"] == "court_antechamber"


def test_mcp_server_engine_injection():
    """MCPServer reuses pre-built AdventureEngine when injected."""
    from adventure_forge.content.loader import build_world_registry
    from adventure_forge.core.engine import AdventureEngine

    reg = build_world_registry()
    eng = AdventureEngine(reg)
    srv = MCPServer(engine=eng)
    assert srv.engine is eng
    assert srv._registry is reg
    obs = srv.new_game("cutpurse")
    assert obs["success"] is True
    assert obs["scene_id"] == "warrens_gate"


def test_mcp_server_presets_schema():
    """new_game tool schema describes all playable presets."""
    srv = MCPServer()
    tools = srv.get_tools_schema()
    new_game_tool = next(t for t in tools if t["name"] == "new_game")
    desc = new_game_tool["inputSchema"]["properties"]["preset"]["description"]
    for expected in ("cutpurse", "noble", "warrior", "nomad", "diver", "scout", "pit_fighter"):
        assert expected in desc, f"Expected preset '{expected}' in schema description: {desc}"

