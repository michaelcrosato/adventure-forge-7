"""Tests for the stateless Vercel ASGI entry point."""

from __future__ import annotations

import asyncio
import json

import app as vercel_app


def request(path: str = "/", method: str = "GET") -> list[dict]:
    sent: list[dict] = []

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict) -> None:
        sent.append(message)

    scope = {"type": "http", "method": method, "path": path}
    asyncio.run(vercel_app.app(scope, receive, send))
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
