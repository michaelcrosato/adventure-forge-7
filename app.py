"""Stateless ASGI entry point for Vercel."""

from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from typing import Any

from adventure_forge import __version__

Send = Callable[[dict[str, Any]], Awaitable[None]]


def _json_response(payload: dict[str, str]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


async def _send_response(
    send: Send,
    *,
    status: int,
    body: bytes,
    content_type: bytes,
    include_body: bool = True,
) -> None:
    headers = [
        (b"content-type", content_type),
        (b"content-length", str(len(body)).encode("ascii")),
        (b"cache-control", b"no-store"),
    ]
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": body if include_body else b""})


async def app(scope: dict[str, Any], receive: Callable[..., Awaitable[Any]], send: Send) -> None:
    """Serve a landing page and a machine-readable deployment health check."""
    if scope["type"] == "lifespan":
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return

    if scope["type"] != "http":
        return

    method = scope.get("method", "GET").upper()
    path = scope.get("path", "/")
    include_body = method != "HEAD"

    if method not in {"GET", "HEAD"}:
        await _send_response(
            send,
            status=405,
            body=_json_response({"error": "method_not_allowed"}),
            content_type=b"application/json; charset=utf-8",
        )
        return

    if path == "/health":
        await _send_response(
            send,
            status=200,
            body=_json_response(
                {
                    "service": "adventure-forge",
                    "status": "ok",
                    "version": __version__,
                }
            ),
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    if path == "/":
        body = (
            "<!doctype html><html lang=\"en\"><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>AdventureForge</title><body>"
            "<main><h1>AdventureForge</h1>"
            "<p>The deterministic action engine is online.</p>"
            "<p><a href=\"/health\">Deployment health</a></p></main>"
            "</body></html>"
        ).encode("utf-8")
        await _send_response(
            send,
            status=200,
            body=body,
            content_type=b"text/html; charset=utf-8",
            include_body=include_body,
        )
        return

    await _send_response(
        send,
        status=404,
        body=_json_response({"error": "not_found"}),
        content_type=b"application/json; charset=utf-8",
        include_body=include_body,
    )
