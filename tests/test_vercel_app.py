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
    target_app: Any = vercel_app.app,
) -> list[dict]:
    sent: list[dict] = []

    async def receive() -> dict:
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message: dict) -> None:
        sent.append(message)

    scope = {"type": "http", "method": method, "path": path}
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
