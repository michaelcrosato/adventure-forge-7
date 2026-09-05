"""Tests for the stateless Vercel ASGI entry point."""

from __future__ import annotations

import asyncio
import json
from typing import Any

import api.index as vercel_api
import app as vercel_app


def request(
    path: str = "/",
    method: str = "GET",
    body: bytes = b"",
    headers: list[tuple[bytes, bytes]] | None = None,
    target_app: Any = vercel_app.app,
) -> list[dict]:
    sent: list[dict] = []

    async def receive() -> dict:
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message: dict) -> None:
        sent.append(message)

    scope = {
        "type": "http",
        "method": method,
        "path": path,
        "headers": headers or [],
    }
    asyncio.run(target_app(scope, receive, send))
    return sent


def test_home() -> None:
    messages = request()
    assert messages[0]["status"] == 200
    assert b"AdventureForge" in messages[1]["body"]


def test_health() -> None:
    messages = request("/health")
    assert messages[0]["status"] == 200
    payload = json.loads(messages[1]["body"])
    assert payload == {
        "service": "adventure-forge",
        "status": "ok",
        "version": "0.1.0",
    }


def test_head_has_no_body() -> None:
    messages = request("/health", "HEAD")
    assert messages[0]["status"] == 200
    assert messages[1]["body"] == b""


def test_unknown_path() -> None:
    messages = request("/missing")
    assert messages[0]["status"] == 404


def test_unsupported_method() -> None:
    messages = request("/health", "POST")
    assert messages[0]["status"] == 405


def test_home_post_not_allowed() -> None:
    messages = request("/", "POST")
    assert messages[0]["status"] == 405


def test_api_index_entrypoint_parity() -> None:
    """Ensure api/index.py behaves identically to app.py."""
    home_msgs = request("/", target_app=vercel_api.app)
    assert home_msgs[0]["status"] == 200
    assert b"AdventureForge" in home_msgs[1]["body"]

    health_msgs = request("/health", target_app=vercel_api.app)
    assert health_msgs[0]["status"] == 200
    payload = json.loads(health_msgs[1]["body"])
    assert payload["status"] == "ok"


def test_cors_options() -> None:
    messages = request("/api/mcp", "OPTIONS")
    assert messages[0]["status"] == 200


def test_mcp_get_info() -> None:
    messages = request("/api/mcp", "GET")
    assert messages[0]["status"] == 200
    payload = json.loads(messages[1]["body"])
    assert payload["service"] == "adventure-forge-mcp"
    assert "tools" in payload
    tool_names = [t["name"] for t in payload["tools"]]
    assert "new_game" in tool_names


def test_mcp_post_jsonrpc_initialize() -> None:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}).encode("utf-8")
    messages = request("/api/mcp", "POST", body=body)
    assert messages[0]["status"] == 200
    payload = json.loads(messages[1]["body"])
    assert payload["id"] == 1
    assert payload["result"]["serverInfo"]["name"] == "adventure-forge-player"


def test_mcp_post_jsonrpc_tools_call() -> None:
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "new_game", "arguments": {"preset": "cutpurse"}},
    }).encode("utf-8")
    messages = request("/api/mcp", "POST", body=body)
    assert messages[0]["status"] == 200
    payload = json.loads(messages[1]["body"])
    assert payload["id"] == 2
    assert "content" in payload["result"]


def test_mcp_post_invalid_json() -> None:
    messages = request("/api/mcp", "POST", body=b"invalid-json")
    assert messages[0]["status"] == 400


def test_lifespan_handler() -> None:
    events = [
        {"type": "lifespan.startup"},
        {"type": "lifespan.shutdown"},
    ]
    received_types = []

    async def receive():
        return events.pop(0)

    async def send(message):
        received_types.append(message["type"])

    scope = {"type": "lifespan"}
    asyncio.run(vercel_app.app(scope, receive, send))
    assert received_types == [
        "lifespan.startup.complete",
        "lifespan.shutdown.complete",
    ]


def test_vercel_rewrite_simulation() -> None:
    """Ensure Vercel rewrites to /api/index.py with x-matched-path resolve properly."""
    home_msgs = request("/api/index.py", headers=[(b"x-matched-path", b"/")])
    assert home_msgs[0]["status"] == 200
    assert b"AdventureForge" in home_msgs[1]["body"]

    health_msgs = request("/api/index.py", headers=[(b"x-matched-path", b"/health")])
    assert health_msgs[0]["status"] == 200
    payload = json.loads(health_msgs[1]["body"])
    assert payload["status"] == "ok"


def test_game_api_workflow() -> None:
    """Test full playable game API lifecycle: presets, new game, and step."""
    # 1. Presets endpoint
    preset_msgs = request("/api/game/presets")
    assert preset_msgs[0]["status"] == 200
    presets = json.loads(preset_msgs[1]["body"])["presets"]
    assert "cutpurse" in presets

    # 2. New game
    new_req = json.dumps({"preset": "cutpurse", "seed": 42}).encode("utf-8")
    new_msgs = request("/api/game/new", "POST", body=new_req)
    assert new_msgs[0]["status"] == 200
    game_data = json.loads(new_msgs[1]["body"])
    assert game_data["success"] is True
    assert "observation" in game_data
    assert "state" in game_data
    actions = game_data["observation"]["legal_actions"]
    assert len(actions) > 0

    # 3. Step action
    chosen_action = actions[0]["id"]
    step_req = json.dumps({
        "state": game_data["state"],
        "action_id": chosen_action,
    }).encode("utf-8")
    step_msgs = request("/api/game/step", "POST", body=step_req)
    assert step_msgs[0]["status"] == 200
    step_data = json.loads(step_msgs[1]["body"])
    assert step_data["success"] is True
    assert step_data["observation"]["turn_count"] == 1


def test_game_api_validation_errors() -> None:
    """Test invalid payloads return 400 Bad Request."""
    bad_step = request("/api/game/step", "POST", body=b"invalid-json")
    assert bad_step[0]["status"] == 400

    missing_fields = json.dumps({"state": {}}).encode("utf-8")
    missing_resp = request("/api/game/step", "POST", body=missing_fields)
    assert missing_resp[0]["status"] == 400


def test_game_quests_endpoint() -> None:
    """Test /api/game/quests returns campaign and subquest metadata."""
    msgs = request("/api/game/quests")
    assert msgs[0]["status"] == 200
    data = json.loads(msgs[1]["body"])
    assert "campaign" in data
    assert "subquests" in data
    assert data["campaign"]["id"] == "five_seals_campaign"
    assert len(data["subquests"]) == 5

    # HEAD method
    head_msgs = request("/api/game/quests", "HEAD")
    assert head_msgs[0]["status"] == 200
    assert head_msgs[1]["body"] == b""

    # POST method not allowed
    post_msgs = request("/api/game/quests", "POST")
    assert post_msgs[0]["status"] == 405


def test_game_hazards_endpoint() -> None:
    """Test /api/game/hazards returns hazard combos."""
    msgs = request("/api/game/hazards")
    assert msgs[0]["status"] == 200
    data = json.loads(msgs[1]["body"])
    assert "hazards" in data
    assert "conflagration" in data["hazards"]
    assert "stun" in data["hazards"]

    # HEAD method
    head_msgs = request("/api/game/hazards", "HEAD")
    assert head_msgs[0]["status"] == 200
    assert head_msgs[1]["body"] == b""

    # POST method not allowed
    post_msgs = request("/api/game/hazards", "POST")
    assert post_msgs[0]["status"] == 405


def test_method_not_allowed_endpoints() -> None:
    """Ensure disallowed HTTP verbs return 405 across endpoints."""
    # POST to presets
    assert request("/api/game/presets", "POST")[0]["status"] == 405
    # GET to game/new
    assert request("/api/game/new", "GET")[0]["status"] == 405
    # GET to game/step
    assert request("/api/game/step", "GET")[0]["status"] == 405
    # DELETE to api/mcp
    assert request("/api/mcp", "DELETE")[0]["status"] == 405


