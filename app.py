"""Stateless ASGI entry point for Vercel deployment.

Provides:
- GET /: Full interactive Hemingway-styled playable web application.
- GET /health: Machine-readable deployment health check.
- POST /api/game/new: Pure stateless initialization of a new adventure session.
- POST /api/game/step: Pure stateless transition of an active adventure session.
- GET /api/game/presets: Metadata for all available character archetypes.
- POST /api/mcp & /mcp: Streamable JSON-RPC 2.0 Model Context Protocol endpoint.
"""

from __future__ import annotations

import json
import time
import urllib.parse
from collections.abc import Awaitable, Callable
from typing import Any

from adventure_forge import __version__
from adventure_forge.content.loader import build_world_registry
from adventure_forge.content.quests import (
    get_continental_main_quest,
    get_faction_intrigue_quests,
    get_provincial_subquests,
)
from adventure_forge.core.character import CHARACTER_PRESETS, get_preset
from adventure_forge.core.codex import CODEX_ENTRIES, PROVINCIAL_MASTERIES
from adventure_forge.core.transit import CHARTERED_ROUTES
from adventure_forge.core.trade import COMMODITIES, TRADE_HUBS
from adventure_forge.core.weather import WEATHER_CONDITIONS, get_all_provincial_weather
from adventure_forge.core.bounties import BOUNTY_CONTRACTS, BOUNTY_HUBS
from adventure_forge.core.companions import COMPANIONS
from adventure_forge.core.bestiary import APEX_BEASTS
from adventure_forge.core.survival import FORAGING_SPOTS, COOKING_RECIPES
from adventure_forge.core.heraldry import FACTION_ORDERS
from adventure_forge.core.shrines import ANCIENT_SHRINES
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.hazards import HAZARD_COMBOS
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.state import GameState
from adventure_forge.player.mcp_server import MCPServer, handle_jsonrpc_request, sanitize_observation

Send = Callable[[dict[str, Any]], Awaitable[None]]
Receive = Callable[..., Awaitable[Any]]

# Preload world content graph once at module load
_REGISTRY = build_world_registry()
_ENGINE = AdventureEngine(_REGISTRY)


def _json_response(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


async def _read_body(receive: Receive) -> bytes:
    body = bytearray()
    while True:
        message = await receive()
        body.extend(message.get("body", b""))
        if not message.get("more_body", False):
            break
    return bytes(body)


async def _send_response_impl(
    send: Send,
    *,
    status: int,
    body: bytes,
    content_type: bytes,
    include_body: bool = True,
    duration_ms: float | None = None,
) -> None:
    headers = [
        (b"content-type", content_type),
        (b"content-length", str(len(body)).encode("ascii")),
        (b"cache-control", b"no-store"),
        (b"access-control-allow-origin", b"*"),
        (b"access-control-allow-methods", b"GET, POST, HEAD, OPTIONS"),
        (b"access-control-allow-headers", b"content-type, authorization"),
    ]
    if duration_ms is not None:
        headers.append((b"server-timing", f"app;dur={duration_ms:.2f}".encode("ascii")))
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": body if include_body else b""})


def _extract_path(scope: dict[str, Any]) -> str:
    """Normalize path across local ASGI, direct Vercel functions, and Vercel rewrites."""
    # 1. Check query string parameter __path passed from vercel.json rewrite
    qs = scope.get("query_string", b"")
    if qs:
        try:
            params = urllib.parse.parse_qs(qs.decode("utf-8", errors="replace"))
            if "__path" in params and params["__path"]:
                candidate = str(params["__path"][0])
                if candidate:
                    return str("/" + candidate.lstrip("/"))
        except Exception:
            pass

    # 2. Check headers
    headers = dict(scope.get("headers", []))
    for header_name in [b"x-forwarded-uri", b"x-envoy-original-path", b"x-matched-path"]:
        raw_val = headers.get(header_name)
        if raw_val:
            p = raw_val.decode("utf-8", errors="replace").split("?")[0]
            if p.startswith("/api/index.py"):
                p = p[len("/api/index.py"):] or "/"
            elif p.startswith("/api/index"):
                p = p[len("/api/index"):] or "/"
            elif p == "/api":
                p = "/"
            if p != "/":
                return str(p)

    # 3. Fallback to scope path
    p = str(scope.get("path", "/"))
    if p.startswith("/api/index.py"):
        p = p[len("/api/index.py"):] or "/"
    elif p.startswith("/api/index"):
        p = p[len("/api/index"):] or "/"
    elif p == "/api":
        p = "/"
    return str(p or "/")


_PLAYABLE_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AdventureForge: The Unbounded Action Engine</title>
<style>
:root {
  --bg: #0b0d13;
  --panel: #131722;
  --panel-border: #22293a;
  --card: #181e2e;
  --card-hover: #1f273d;
  --card-selected: #253352;
  --text: #e6edf3;
  --text-muted: #8b949e;
  --accent: #58a6ff;
  --accent-dim: #1f6feb;
  --green: #3fb950;
  --red: #f85149;
  --gold: #d29922;
  --purple: #bc8cff;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.5;
  padding: 1.5rem 1rem;
  min-height: 100vh;
}
.container { max-width: 960px; margin: 0 auto; }
header {
  border-bottom: 1px solid var(--panel-border);
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}
.title-group h1 { font-size: 1.6rem; font-weight: 700; letter-spacing: -0.02em; }
.title-group p { font-size: 0.9rem; color: var(--text-muted); }
.badge-online {
  font-size: 0.7rem;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  background: #238636;
  color: #fff;
  font-weight: 600;
  vertical-align: middle;
}
.top-links { display: flex; gap: 1rem; font-size: 0.85rem; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

/* Preset Selection Screen */
.preset-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}
.preset-card {
  background: var(--card);
  border: 2px solid var(--panel-border);
  border-radius: 8px;
  padding: 1.25rem;
  cursor: pointer;
  transition: all 0.15s ease;
}
.preset-card:hover { border-color: var(--accent-dim); background: var(--card-hover); }
.preset-card.selected { border-color: var(--accent); background: var(--card-selected); }
.preset-title { font-size: 1.2rem; font-weight: 600; color: var(--accent); margin-bottom: 0.25rem; }
.preset-meta { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }
.preset-desc { font-size: 0.9rem; color: var(--text); margin-bottom: 0.75rem; }
.tag-row { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.5rem; }
.tag { font-size: 0.75rem; padding: 0.15rem 0.45rem; border-radius: 4px; background: rgba(110,118,129,0.2); }
.tag.skill { background: rgba(88,166,255,0.2); color: var(--accent); }
.tag.trait { background: rgba(210,153,34,0.2); color: var(--gold); }

.controls-row {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}
.input-seed {
  background: var(--panel);
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  padding: 0.6rem 0.8rem;
  color: var(--text);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.9rem;
  width: 140px;
}
.btn {
  background: var(--accent-dim);
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.65rem 1.4rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s ease;
}
.btn:hover { background: #388bfd; }
.btn-secondary {
  background: var(--panel);
  color: var(--text-muted);
  border: 1px solid var(--panel-border);
}
.btn-secondary:hover { background: var(--card-hover); color: var(--text); }

/* Play View */
#play-view { display: none; }
.hud-bar {
  background: var(--panel);
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}
.hud-profile { display: flex; flex-direction: column; gap: 0.2rem; }
.hud-name { font-size: 1.1rem; font-weight: 700; color: #fff; }
.hud-stats { display: flex; gap: 1.5rem; align-items: center; font-size: 0.9rem; }
.stat-pill { display: flex; align-items: center; gap: 0.4rem; }
.bar-track { width: 80px; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.2s ease; }
.bar-hp { background: var(--red); }
.bar-sp { background: var(--green); }

.scene-panel {
  background: var(--panel);
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}
.scene-breadcrumb {
  font-size: 0.8rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}
.scene-title { font-size: 1.4rem; font-weight: 700; color: #fff; margin-bottom: 0.75rem; }
.scene-prose {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--text);
  margin-bottom: 1rem;
  font-serif: Georgia, serif;
}
.events-box {
  background: rgba(88,166,255,0.08);
  border-left: 3px solid var(--accent);
  padding: 0.75rem 1rem;
  border-radius: 0 6px 6px 0;
  font-size: 0.9rem;
  color: var(--accent);
  margin-top: 1rem;
}

/* Legal Actions */
.action-section-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
}
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.action-btn {
  background: var(--card);
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  padding: 0.85rem 1rem;
  text-align: left;
  cursor: pointer;
  color: var(--text);
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  transition: all 0.15s ease;
}
.action-btn:hover:not(:disabled) {
  border-color: var(--accent);
  background: var(--card-hover);
  transform: translateY(-1px);
}
.action-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.action-label { font-size: 0.95rem; font-weight: 600; color: #fff; }
.action-meta { display: flex; gap: 0.4rem; align-items: center; font-size: 0.75rem; color: var(--text-muted); }
.badge-category { padding: 0.1rem 0.35rem; border-radius: 3px; font-weight: 600; text-transform: uppercase; }
.cat-movement { background: rgba(63,185,80,0.2); color: var(--green); }
.cat-interaction { background: rgba(88,166,255,0.2); color: var(--accent); }
.cat-combat { background: rgba(248,81,73,0.2); color: var(--red); }
.cat-tactical { background: rgba(187,128,255,0.2); color: #d2a8ff; border: 1px solid rgba(187,128,255,0.35); }
.cat-crafting { background: rgba(56,189,248,0.2); color: #38bdf8; border: 1px solid rgba(56,189,248,0.35); }
.cat-codex { background: rgba(168,85,247,0.2); color: #c084fc; border: 1px solid rgba(168,85,247,0.35); }
.cat-transit { background: rgba(45,212,191,0.2); color: #2dd4bf; border: 1px solid rgba(45,212,191,0.35); }
.cat-trade { background: rgba(234,179,8,0.2); color: #facc15; border: 1px solid rgba(234,179,8,0.35); }
.cat-weather { background: rgba(56,189,248,0.25); color: #7dd3fc; border: 1px solid rgba(56,189,248,0.4); }
.cat-bounty { background: rgba(239, 68, 68, 0.25); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
.cat-companion { background: rgba(192, 132, 252, 0.25); color: #d8b4fe; border: 1px solid rgba(192, 132, 252, 0.45); }
.cat-bestiary { background: rgba(245, 158, 11, 0.25); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.45); }
.cat-systemic { background: rgba(251,146,60,0.2); color: #fb923c; border: 1px solid rgba(251,146,60,0.35); }
.cat-social { background: rgba(236,72,153,0.2); color: #ec4899; border: 1px solid rgba(236,72,153,0.35); }
.cat-trait_exploit { background: rgba(210,153,34,0.2); color: var(--gold); }
.cat-general { background: rgba(110,118,129,0.2); color: var(--text-muted); }
.badge-cost { color: var(--gold); }

/* Modals & Dialogs */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}
.modal-card {
  background: var(--card);
  border: 1px solid var(--panel-border);
  border-radius: 8px;
  width: 100%;
  max-width: 650px;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  display: flex;
  flex-direction: column;
}
.modal-header {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--panel-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.modal-body {
  padding: 1.25rem;
}
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 0.6rem;
}
.stat-box {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
}
.filter-btn {
  background: rgba(255,255,255,0.05);
  border: 1px solid var(--panel-border);
  color: var(--text-muted);
  border-radius: 4px;
  padding: 0.25rem 0.6rem;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.15s ease;
}
.filter-btn:hover { color: #fff; border-color: var(--accent); }
.filter-btn.active {
  background: rgba(88, 166, 255, 0.2);
  color: var(--accent);
  border-color: var(--accent);
  font-weight: 600;
}
.key-badge {
  display: inline-block;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 3px;
  padding: 0 0.3rem;
  font-size: 0.7rem;
  color: var(--gold);
  margin-right: 0.4rem;
}

/* Tabs & Navigation */
.quest-tab-bar {
  display: flex;
  border-bottom: 1px solid var(--panel-border);
  background: rgba(0, 0, 0, 0.25);
  padding: 0 0.5rem;
  gap: 0.25rem;
}
.tab-btn {
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-muted);
  padding: 0.6rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}
.tab-btn:hover { color: #fff; }
.tab-btn.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

/* Action Search Bar */
.action-search-input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--panel-border);
  border-radius: 4px;
  color: var(--text);
  font-size: 0.8rem;
  padding: 0.3rem 0.6rem;
  outline: none;
  width: 140px;
  transition: all 0.15s ease;
}
.action-search-input:focus {
  border-color: var(--accent);
  background: rgba(255, 255, 255, 0.09);
  width: 180px;
}

/* Session Resume Banner */
.resume-card {
  background: linear-gradient(135deg, rgba(88, 166, 255, 0.12), rgba(63, 185, 80, 0.08));
  border: 1px solid var(--accent-dim);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

/* Continental Map Styles */
.map-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}
.map-card {
  background: var(--card);
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  padding: 0.85rem;
  cursor: pointer;
  transition: all 0.15s ease;
  position: relative;
}
.map-card:hover {
  border-color: var(--accent);
  background: var(--card-hover);
  transform: translateY(-2px);
}
.map-card.active-region {
  border-color: var(--green);
  box-shadow: 0 0 12px rgba(63, 185, 80, 0.35);
}
.map-card.selected-province {
  border-color: var(--accent);
}
.pulse-beacon {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 0 0 rgba(63, 185, 80, 0.7);
  animation: beacon-pulse 1.8s infinite;
  margin-right: 0.4rem;
}
@keyframes beacon-pulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(63, 185, 80, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(63, 185, 80, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(63, 185, 80, 0); }
}

/* Quest Journal Styles */
.seal-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--panel-border);
  border-radius: 6px;
  padding: 0.85rem 1rem;
  margin-bottom: 0.75rem;
  transition: all 0.15s ease;
}
.seal-card.claimed {
  border-color: rgba(63, 185, 80, 0.4);
  background: rgba(63, 185, 80, 0.04);
}
.seal-card.active {
  border-color: rgba(245, 158, 11, 0.5);
  background: rgba(245, 158, 11, 0.06);
}
.progress-track {
  width: 100%;
  height: 10px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 5px;
  overflow: hidden;
  margin: 0.5rem 0 1rem 0;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #f59e0b, #3fb950);
  border-radius: 5px;
  transition: width 0.3s ease;
}

/* Terminal Screen */
.terminal-banner {
  background: #1f1414;
  border: 1px solid var(--red);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  text-align: center;
}
.terminal-banner h2 { color: var(--red); font-size: 1.4rem; margin-bottom: 0.5rem; }

footer {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--panel-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="title-group">
      <h1>AdventureForge <span class="badge-online">Online</span></h1>
      <p>Unbounded Deterministic Action Engine &bull; Skyrim Scale &bull; BG3 Depth</p>
    </div>
    <div class="top-links">
      <a href="/health" target="_blank">Health Check (/health)</a>
      <a href="/api/mcp" target="_blank">MCP Surface (/api/mcp)</a>
      <a href="https://github.com/michaelcrosato/adventure-forge-7" target="_blank" rel="noopener">GitHub</a>
    </div>
  </header>

  <!-- SELECT VIEW -->
  <section id="select-view">
    <div id="resume-session-box" class="resume-card" style="display: none;"></div>

    <div style="margin-bottom: 1rem;">
      <h2 style="font-size: 1.25rem;">Choose Protagonist Build</h2>
      <p style="color: var(--text-muted); font-size: 0.9rem;">
        Each protagonist queries orthogonal state vectors (ancestry, traits, flaws, skills) and unlocks unique narrative branches across 520 scenes.
      </p>
    </div>

    <div class="preset-grid" id="preset-container">
      <!-- Generated via JS -->
    </div>

    <div class="controls-row">
      <div>
        <label style="font-size: 0.85rem; color: var(--text-muted); display: block; margin-bottom: 0.25rem;">RNG Seed Cursor</label>
        <input type="number" id="seed-input" class="input-seed" value="42" min="1" max="999999">
      </div>
      <button class="btn" id="start-btn" onclick="startAdventure()">Embark on Adventure</button>
    </div>
  </section>

  <!-- PLAY VIEW -->
  <section id="play-view">
    <div class="hud-bar">
      <div class="hud-profile">
        <div class="hud-name" id="char-name">Character Name</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);" id="char-origin">Ancestry &bull; Background</div>
      </div>
      <div class="hud-stats">
        <div class="stat-pill">
          <span>HP</span>
          <div class="bar-track"><div class="bar-fill bar-hp" id="hp-bar" style="width: 100%;"></div></div>
          <span id="hp-text" style="font-weight: 600;">20/20</span>
        </div>
        <div class="stat-pill">
          <span>SP</span>
          <div class="bar-track"><div class="bar-fill bar-sp" id="sp-bar" style="width: 100%;"></div></div>
          <span id="sp-text" style="font-weight: 600;">10/10</span>
        </div>
        <div style="font-size: 0.85rem; color: var(--text-muted);">
          Turn: <span id="turn-display" style="color: #fff; font-weight: 600;">0</span>
        </div>
      </div>
      <div style="display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap;">
        <button class="btn btn-secondary" id="undo-btn" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="undoTurn()" disabled title="Undo last turn (Key: U)">↩ Undo (<span id="undo-count">0</span>)</button>
        <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleSheetModal()" title="View 7-Axis Character Sheet (Key: C)">📊 Sheet</button>
        <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleQuestModal()" title="View Quest Journal (Key: Q)">📜 Quests</button>
        <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleCodexModal()" title="View Ancient Lore Codex (Key: X)">📖 Codex</button>
        <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleTradeModal()" title="View Commodity Exchange (Key: T)">⚖️ Trade</button>
        <button class="btn btn-secondary" id="weather-btn" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleWeatherModal()" title="View Continental Weather Forecast (Key: W)">⛅ Weather</button>
        <button class="btn btn-secondary" id="bounty-btn" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleBountyModal()" title="View Mercenary Contract Board (Key: B)">🎯 Bounties</button>
        <button class="btn btn-secondary" id="companion-btn" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleCompanionModal()" title="View Continental Warband Fellowship (Key: P)">👥 Party</button>
        <button class="btn btn-secondary" id="bestiary-btn" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleBestiaryModal()" title="View Continental Bestiary & Apex Trophies (Key: H)">🦁 Bestiary</button>
        <button class="btn btn-secondary" id="survival-btn" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleSurvivalModal()" title="View Survival Camp & Foraging (Key: K)">🏕️ Camp</button>
        <button class="btn btn-secondary" id="orders-btn" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleOrdersModal()" title="View Continental Orders & War Banners (Key: O)">🛡️ Orders</button>
        <button class="btn btn-secondary" id="shrines-btn" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleShrinesModal()" title="View Ancient Shrines & Titan Blessings (Key: G)">🏛️ Shrines</button>
        <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleMapModal()" title="View Continental Atlas (Key: M)">🗺️ Map</button>
        <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="toggleReplayModal()" title="Export or Verify Replay">📜 Replay</button>
        <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.4rem 0.7rem;" onclick="resetToSelect()">Restart</button>
      </div>
    </div>

    <div style="margin-bottom: 0.5rem;" id="status-container" class="tag-row"></div>
    <div style="margin-bottom: 1rem;" id="inventory-container" class="tag-row"></div>

    <div id="quest-banner" style="background: rgba(217, 119, 6, 0.12); border: 1px solid rgba(217, 119, 6, 0.35); border-radius: 6px; padding: 0.6rem 0.9rem; margin-bottom: 1rem; font-size: 0.85rem; cursor: pointer;" onclick="toggleQuestModal()" title="Click to open Quest Journal (Key: Q)">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
          <span style="color: #f59e0b; font-weight: 600;">👑 Grand Campaign:</span>
          <span id="quest-stage-text" style="color: #f3f4f6; margin-left: 0.3rem;">Loading quest...</span>
        </div>
        <div id="quest-seals-count" style="font-size: 0.8rem; color: #fbbf24; font-weight: 600;">0/5 Seals</div>
      </div>
      <div id="subquest-banner" style="margin-top: 0.4rem; padding-top: 0.4rem; border-top: 1px dashed rgba(217, 119, 6, 0.25); display: none; font-size: 0.8rem;">
        <span style="color: #60a5fa; font-weight: 600;">📜 Provincial Subquest:</span>
        <span id="subquest-text" style="color: #e5e7eb; margin-left: 0.3rem;"></span>
      </div>
    </div>

    <div id="terminal-pane" class="terminal-banner" style="display: none;">
      <h2 id="terminal-title">Adventure Concluded</h2>
      <p id="terminal-desc" style="color: var(--text);"></p>
      <button class="btn" style="margin-top: 1rem;" onclick="resetToSelect()">Start New Adventure</button>
    </div>

    <div class="scene-panel">
      <div class="scene-breadcrumb" id="scene-region" style="cursor: pointer;" onclick="toggleMapModal()" title="Click to view Continental Atlas (Key: M)">Region</div>
      <h2 class="scene-title" id="scene-title">Scene Title</h2>
      <p class="scene-prose" id="scene-description">Prose loading...</p>
      <div class="events-box" id="scene-events" style="display: none;"></div>
    </div>

    <div>
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem;">
        <div class="action-section-title" style="margin-bottom: 0;">Legal Actions (<span id="action-count">0</span> Available)</div>
        <div style="display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap;">
          <input type="search" id="action-search" class="action-search-input" placeholder="🔍 Search actions..." oninput="onActionSearch(this.value)">
          <div id="category-filters" style="display: flex; gap: 0.35rem; flex-wrap: wrap;"></div>
        </div>
      </div>
      <div class="actions-grid" id="actions-container"></div>
    </div>

    <!-- CHARACTER SHEET MODAL -->
    <div id="sheet-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleSheetModal()">
      <div class="modal-card">
        <div class="modal-header">
          <h3 id="modal-sheet-title" style="margin: 0; font-size: 1.15rem; color: #fff;">Character Sheet</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleSheetModal()">✕</button>
        </div>
        <div class="modal-body" id="modal-sheet-content"></div>
      </div>
    </div>

    <!-- QUEST JOURNAL MODAL -->
    <div id="quest-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleQuestModal()">
      <div class="modal-card" style="max-width: 700px;">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">📜 Continental Quest Journal</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleQuestModal()">✕</button>
        </div>
        <div class="quest-tab-bar">
          <button class="tab-btn active" id="tab-btn-campaign" onclick="switchQuestTab('campaign')">👑 Grand Campaign</button>
          <button class="tab-btn" id="tab-btn-subquests" onclick="switchQuestTab('subquests')">📜 Provincial Subquests</button>
          <button class="tab-btn" id="tab-btn-intrigue" onclick="switchQuestTab('intrigue')">⚔️ Faction Intrigue</button>
        </div>
        <div class="modal-body" id="modal-quest-content"></div>
      </div>
    </div>

    <!-- CONTINENTAL ATLAS MODAL -->
    <div id="map-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleMapModal()">
      <div class="modal-card" style="max-width: 750px;">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">🗺️ Continental Atlas of the Five Provinces</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleMapModal()">✕</button>
        </div>
        <div class="modal-body" id="modal-map-content"></div>
      </div>
    </div>

    <!-- ANCIENT CODEX & RELICS MODAL -->
    <div id="codex-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleCodexModal()">
      <div class="modal-card" style="max-width: 720px;">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">📖 Ancient Lore Codex & Relic Archives</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleCodexModal()">✕</button>
        </div>
        <div class="modal-body" id="modal-codex-content"></div>
      </div>
    </div>

    <!-- CONTINENTAL COMMODITY EXCHANGE MODAL -->
    <div id="trade-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleTradeModal()">
      <div class="modal-card" style="max-width: 760px;">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">⚖️ Continental Commodity Exchange & Trade Registry</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleTradeModal()">✕</button>
        </div>
        <div class="modal-body" id="modal-trade-content"></div>
      </div>
    </div>

    <!-- CONTINENTAL WEATHER FORECAST MODAL -->
    <div id="weather-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleWeatherModal()">
      <div class="modal-card" style="max-width: 760px;">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">⛅ Continental Weather Dynamics & Provincial Forecast</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleWeatherModal()">✕</button>
        </div>
        <div class="modal-body" id="modal-weather-content"></div>
      </div>
    </div>

    <!-- CONTINENTAL MERCENARY CONTRACT BOARD MODAL -->
    <div id="bounty-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleBountyModal()">
      <div class="modal-card" style="max-width: 760px;">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">🎯 Continental Mercenary Contract Board</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleBountyModal()">✕</button>
        </div>
        <div class="modal-body" id="modal-bounty-content"></div>
      </div>
    </div>

    <!-- CONTINENTAL COMPANION WARBAND MODAL -->
    <div id="companion-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleCompanionModal()">
      <div class="modal-card" style="max-width: 760px;">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">👥 Continental Warband Fellowship</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleCompanionModal()">✕</button>
        </div>
        <div class="modal-body" id="modal-companion-content"></div>
      </div>
    </div>

    <!-- CONTINENTAL BESTIARY & APEX TROPHIES MODAL -->
    <div id="bestiary-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleBestiaryModal()">
      <div class="modal-card" style="max-width: 760px;">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">🦁 Continental Apex Bestiary & Trophy Hall</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleBestiaryModal()">✕</button>
        </div>
        <div class="modal-body" id="modal-bestiary-content"></div>
      </div>
    </div>

    <!-- CONTINENTAL SURVIVAL CAMP & FORAGING MODAL -->
    <div id="survival-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleSurvivalModal()">
      <div class="modal-card" style="max-width: 760px;">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">🏕️ Continental Survival Camp & Foraging</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleSurvivalModal()">✕</button>
        </div>
        <div class="modal-body" id="modal-survival-content"></div>
      </div>
    </div>

    <!-- CONTINENTAL HERALDRY & ORDERS MODAL -->
    <div id="orders-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleOrdersModal()">
      <div class="modal-card" style="max-width: 760px;">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">🛡️ Provincial Faction Heraldry & War Banners</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleOrdersModal()">✕</button>
        </div>
        <div class="modal-body" id="modal-orders-content"></div>
      </div>
    </div>

    <!-- CONTINENTAL SHRINES & TITAN BLESSINGS MODAL -->
    <div id="shrines-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleShrinesModal()">
      <div class="modal-card" style="max-width: 760px;">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">🏛️ Continental Ancient Shrines & Titan Blessings</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleShrinesModal()">✕</button>
        </div>
        <div class="modal-body" id="modal-shrines-content"></div>
      </div>
    </div>

    <!-- REPLAY TRACE MODAL -->
    <div id="replay-modal" class="modal-backdrop" style="display: none;" onclick="if(event.target===this)toggleReplayModal()">
      <div class="modal-card">
        <div class="modal-header">
          <h3 style="margin: 0; font-size: 1.15rem; color: #fff;">Deterministic Replay & Trace Verification</h3>
          <button class="btn btn-secondary" style="padding: 0.2rem 0.6rem;" onclick="toggleReplayModal()">✕</button>
        </div>
        <div class="modal-body">
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.75rem;">
            AdventureForge transitions are 100% deterministic (SplitMix64 PRNG + canonical SHA-256 state fingerprints).
          </p>
          <div style="margin-bottom: 1rem;">
            <label style="font-size: 0.8rem; color: var(--text-muted); display: block; margin-bottom: 0.25rem;">Current Action Trace JSON</label>
            <textarea id="trace-textarea" readonly style="width: 100%; height: 110px; background: #0d1117; border: 1px solid var(--panel-border); border-radius: 4px; color: #7ee787; font-family: monospace; font-size: 0.8rem; padding: 0.5rem;"></textarea>
          </div>
          <div style="display: flex; gap: 0.5rem; margin-bottom: 1.25rem;">
            <button class="btn" style="font-size: 0.85rem;" onclick="copyTraceToClipboard()">Copy Trace to Clipboard</button>
          </div>
          <div style="border-top: 1px solid var(--panel-border); padding-top: 1rem;">
            <label style="font-size: 0.8rem; color: var(--text-muted); display: block; margin-bottom: 0.25rem;">Load & Run Deterministic Replay</label>
            <textarea id="load-trace-textarea" placeholder='Paste replay trace JSON here...' style="width: 100%; height: 80px; background: #0d1117; border: 1px solid var(--panel-border); border-radius: 4px; color: #e6edf3; font-family: monospace; font-size: 0.8rem; padding: 0.5rem;"></textarea>
            <button class="btn btn-secondary" style="font-size: 0.85rem; margin-top: 0.5rem;" onclick="runImportedReplay()">Execute & Verify Replay</button>
            <div id="replay-status" style="margin-top: 0.5rem; font-size: 0.85rem;"></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <footer>
    <div>AdventureForge &bull; Zero-Config Vercel Serverless Function &bull; Latency: <span id="latency-display" style="color: #3fb950; font-weight: 600;">~1ms</span></div>
    <div>Deterministic Hash: <code id="fingerprint-display" style="font-size: 0.75rem;">initial</code></div>
  </footer>
</div>

<script>
const PRESETS = {
  "cutpurse": {
    "title": "Silas the Cutpurse",
    "meta": "Deep-Dweller &bull; Warrens Gate",
    "desc": "Agile rogue with night vision, streetwise contacts, and lockpicks. Exploits subterranean crevices and underworld fences.",
    "skills": ["cunning: 4", "stealth: 3"],
    "traits": ["night_eyed", "streetwise", "marked_outlaw"]
  },
  "noble": {
    "title": "Lady Vivienne",
    "meta": "High-Kin &bull; Court Antechamber",
    "desc": "Exiled court noble adept at aristocratic rhetoric, formal decree analysis, and diplomatic manipulation.",
    "skills": ["rhetoric: 4", "cunning: 2"],
    "traits": ["skeptical", "oath_bound"]
  },
  "warrior": {
    "title": "Garron the Sentinel",
    "meta": "Ashenborn &bull; Iron Crags Base",
    "desc": "Brute-force veteran warrior equipped with iron crowbar and water skin. Conquers sheer mountain cliff faces and martial duels.",
    "skills": ["athletics: 4", "brawling: 4"],
    "traits": ["iron_gutted"]
  },
  "nomad": {
    "title": "Kael the Dune-Strider",
    "meta": "Nomad &bull; Scorch Oasis",
    "desc": "Hardy desert survivalist equipped with sun veil and flint. Endures blistering heat and navigates shifting dunes.",
    "skills": ["survival: 4", "athletics: 3"],
    "traits": ["heat_tolerant", "iron_gutted", "keen_eyed"]
  },
  "diver": {
    "title": "Mara the Abyssal Diver",
    "meta": "Deep-Dweller &bull; Sunken Grotto",
    "desc": "Agile cavern diver equipped with waterproof sealant and crowbar. Explores submerged grottos and underwater vaults.",
    "skills": ["athletics: 4", "cunning: 3"],
    "traits": ["water_breather", "night_eyed", "nimble"]
  },
  "scout": {
    "title": "Torin the Highland Scout",
    "meta": "High-Kin &bull; Reach Central Hub",
    "desc": "Vigilant mountain ranger equipped with climbing rope and torch. Scales vertical cliffs and tracks hidden highland trails.",
    "skills": ["athletics: 4", "stealth: 3"],
    "traits": ["nimble", "keen_eyed", "marked_outlaw"]
  }
};

const PROVINCES_MAP_DATA = {
  "province_reach": {
    "id": "province_reach",
    "name": "The Reach",
    "icon": "⛰️",
    "theme": "Highland Peaks & Crags",
    "mechanic": "Verticality & Climbing Stamina",
    "hazards": "Altitude Sickness & Sheer Falls",
    "regions": ["province_reach", "iron_crags"],
    "desc": "Highland mountain range ruled by clan sentinels and sky rangers.",
    "connections": ["The Grand Bazaar", "The High Court"]
  },
  "province_sunken_hollows": {
    "id": "province_sunken_hollows",
    "name": "The Sunken Hollows",
    "icon": "🌊",
    "theme": "Flooded Vaults & Submerged Trenches",
    "mechanic": "Underwater Diving & Hydrostatic Pressure",
    "hazards": "Oxygen Depletion & Drowning",
    "regions": ["province_sunken_hollows", "sunken_hollows_local"],
    "desc": "Subterranean flooded grottoes harboring primeval abyssal secrets.",
    "connections": ["The Grand Bazaar", "The Lowlands"]
  },
  "province_scorchwaste": {
    "id": "province_scorchwaste",
    "name": "The Scorchwaste",
    "icon": "☀️",
    "theme": "Blistering Dunes & Canyon Wastes",
    "mechanic": "Heat Survival & Hydration",
    "hazards": "Sunstroke & Salt Flats",
    "regions": ["province_scorchwaste", "scorchwaste_local"],
    "desc": "Arid desert expanse where nomads trade water and survive boiling winds.",
    "connections": ["The Grand Bazaar", "The Lowlands"]
  },
  "province_high_court": {
    "id": "province_high_court",
    "name": "The High Court",
    "icon": "🏛️",
    "theme": "Imperial Spires & Tribunal Halls",
    "mechanic": "Court Intrigue & Noble Decorum",
    "hazards": "Diplomatic Contempt & Slander",
    "regions": ["province_high_court", "high_court_local"],
    "desc": "Gilded palaces and imperial courts rife with aristocratic plots.",
    "connections": ["The Grand Bazaar", "The Reach"]
  },
  "province_lowlands": {
    "id": "province_lowlands",
    "name": "The Lowlands",
    "icon": "🗝️",
    "theme": "Shadow Warrens & River Canals",
    "mechanic": "Social Stealth & Suspicion",
    "hazards": "Bounties & Watch Infiltration",
    "regions": ["province_lowlands", "lower_warrens"],
    "desc": "Dense canal city and crime syndicates thriving in shadow.",
    "connections": ["The Grand Bazaar", "The Scorchwaste", "The Sunken Hollows"]
  },
  "stress_market": {
    "id": "stress_market",
    "name": "The Grand Bazaar",
    "icon": "⚖️",
    "theme": "Continental Crossroads Hub",
    "mechanic": "Unbounded Choice Synthesis",
    "hazards": "Cutpurses & Market Chaos",
    "regions": ["stress_market"],
    "desc": "Continental crossroads linking all five provinces with open markets.",
    "connections": ["All Five Provinces"]
  }
};

const SEALS_METADATA = [
  {
    "id": "stage_crags_beacon",
    "flag": "crags_beacon_lit",
    "province": "The Reach",
    "title": "The Highland Beacon",
    "icon": "🔥",
    "desc": "Ignite the ancient beacon to rally the mountain clans.",
    "approaches": ["Climbing", "Iron Crowbar", "Martial Force"]
  },
  {
    "id": "stage_warrens_ledger",
    "flag": "warrens_ledger_recovered",
    "province": "The Lowlands",
    "title": "The Shadow Ledger",
    "icon": "📜",
    "desc": "Recover the syndicate ledger from the canal vault.",
    "approaches": ["Lockpicks", "Social Stealth", "Underworld Bribery"]
  },
  {
    "id": "stage_scorch_compass",
    "flag": "scorch_compass_acquired",
    "province": "The Scorchwaste",
    "title": "The Solar Compass",
    "icon": "🧭",
    "desc": "Secure the solar compass across the blistering salt dunes.",
    "approaches": ["Survival", "Water Conservation", "Desert Camouflage"]
  },
  {
    "id": "stage_court_verdict",
    "flag": "court_verdict_won",
    "province": "The High Court",
    "title": "The Tribunal Verdict",
    "icon": "⚖️",
    "desc": "Win tribunal judgment through aristocratic rhetoric and favor.",
    "approaches": ["Rhetoric", "Courtly Decorum", "Imperial Decrees"]
  },
  {
    "id": "stage_abyssal_pearl",
    "flag": "hollows_pearl_retrieved",
    "province": "The Sunken Hollows",
    "title": "The Sunken Pearl",
    "icon": "💎",
    "desc": "Retrieve the abyssal keystone from the submerged ocean trench.",
    "approaches": ["Diving Bell", "Waterproof Sealant", "Athletics"]
  }
];

const STORAGE_KEY = "adventureforge_saved_session_v1";
let selectedPreset = "cutpurse";
let gameState = null;
let stateHistory = [];
let activeCategoryFilter = "all";
let actionSearchQuery = "";
let currentObsActions = [];
let currentQuestData = null;
let currentCodexData = null;
let currentTradeData = null;
let lastObservation = null;
let lastCharacter = null;
let cachedQuestsMetadata = null;
let cachedCodexMetadata = null;
let cachedTradeMetadata = null;
let currentWeatherData = null;
let cachedWeatherMetadata = null;
let currentBountyData = null;
let cachedBountyMetadata = null;
let currentCompanionData = null;
let cachedCompanionMetadata = null;
let currentBestiaryData = null;
let cachedBestiaryMetadata = null;
let currentSurvivalData = null;
let cachedSurvivalMetadata = null;
let currentOrdersData = null;
let cachedOrdersMetadata = null;
let currentShrinesData = null;
let cachedShrinesMetadata = null;
let activeQuestTab = "campaign";
let selectedMapProvince = null;

function renderPresetCards() {
  const container = document.getElementById("preset-container");
  container.innerHTML = "";
  for (const [id, data] of Object.entries(PRESETS)) {
    const card = document.createElement("div");
    card.className = "preset-card" + (id === selectedPreset ? " selected" : "");
    card.onclick = () => {
      selectedPreset = id;
      renderPresetCards();
    };

    let tagsHtml = data.skills.map(s => `<span class="tag skill">${s}</span>`).join("") +
                   data.traits.map(t => `<span class="tag trait">${t}</span>`).join("");

    card.innerHTML = `
      <div class="preset-title">${data.title}</div>
      <div class="preset-meta">${data.meta}</div>
      <div class="preset-desc">${data.desc}</div>
      <div class="tag-row">${tagsHtml}</div>
    `;
    container.appendChild(card);
  }
}

function updateUndoButton() {
  const btn = document.getElementById("undo-btn");
  const countEl = document.getElementById("undo-count");
  const canUndo = stateHistory.length > 1;
  if (btn) btn.disabled = !canUndo;
  if (countEl) countEl.textContent = Math.max(0, stateHistory.length - 1);
}

async function startAdventure() {
  const seed = parseInt(document.getElementById("seed-input").value, 10) || 42;
  const startBtn = document.getElementById("start-btn");
  startBtn.disabled = true;
  startBtn.textContent = "Entering World...";

  try {
    const t0 = performance.now();
    const res = await fetch("/api/game/new", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ preset: selectedPreset, seed: seed })
    });
    const dur = (performance.now() - t0).toFixed(1);
    const latEl = document.getElementById("latency-display");
    if (latEl) latEl.textContent = `${dur}ms`;
    if (!res.ok) throw new Error("Failed to start adventure: " + res.statusText);
    const data = await res.json();
    gameState = data.state;
    stateHistory = [JSON.parse(JSON.stringify(gameState))];
    updateUndoButton();
    renderGame(data.observation, data.character, data.quest, data.codex, data.transit, data.trade, data.weather, data.bounty, data.companion, data.bestiary, data.survival, data.orders, data.shrines);
    document.getElementById("select-view").style.display = "none";
    document.getElementById("play-view").style.display = "block";
  } catch (err) {
    alert(err.message);
  } finally {
    startBtn.disabled = false;
    startBtn.textContent = "Embark on Adventure";
  }
}

async function stepAction(actionId) {
  const container = document.getElementById("actions-container");
  const btns = container.querySelectorAll("button");
  btns.forEach(b => b.disabled = true);

  try {
    const t0 = performance.now();
    const res = await fetch("/api/game/step", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ state: gameState, action_id: actionId })
    });
    const dur = (performance.now() - t0).toFixed(1);
    const latEl = document.getElementById("latency-display");
    if (latEl) latEl.textContent = `${dur}ms`;
    if (!res.ok) throw new Error("Step failed: " + res.statusText);
    const data = await res.json();
    gameState = data.state;
    stateHistory.push(JSON.parse(JSON.stringify(gameState)));
    updateUndoButton();
    renderGame(data.observation, data.character, data.quest, data.codex, data.transit, data.trade, data.weather, data.bounty, data.companion, data.bestiary, data.survival, data.orders, data.shrines);
  } catch (err) {
    alert(err.message);
    btns.forEach(b => b.disabled = false);
  }
}

async function undoTurn() {
  if (stateHistory.length <= 1) return;
  stateHistory.pop();
  const prevState = stateHistory[stateHistory.length - 1];
  gameState = JSON.parse(JSON.stringify(prevState));
  updateUndoButton();

  try {
    const t0 = performance.now();
    const res = await fetch("/api/game/observe", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ state: gameState })
    });
    const dur = (performance.now() - t0).toFixed(1);
    const latEl = document.getElementById("latency-display");
    if (latEl) latEl.textContent = `${dur}ms`;
    if (!res.ok) throw new Error("Undo observation failed: " + res.statusText);
    const data = await res.json();
    renderGame(data.observation, data.character, data.quest, data.codex, data.transit, data.trade, data.weather, data.bounty, data.companion, data.bestiary, data.survival, data.orders, data.shrines);
  } catch (err) {
    alert("Undo error: " + err.message);
  }
}

function renderCategoryFilters(actions) {
  const filterContainer = document.getElementById("category-filters");
  if (!filterContainer) return;
  const counts = { all: actions.length };
  for (const act of actions) {
    const c = act.category || "general";
    counts[c] = (counts[c] || 0) + 1;
  }
  filterContainer.innerHTML = "";
  for (const [cat, count] of Object.entries(counts)) {
    const btn = document.createElement("button");
    btn.className = "filter-btn" + (cat === activeCategoryFilter ? " active" : "");
    btn.textContent = `${cat.toUpperCase()} (${count})`;
    btn.onclick = () => {
      activeCategoryFilter = cat;
      renderCategoryFilters(actions);
      renderActionButtons(actions);
    };
    filterContainer.appendChild(btn);
  }
}

function onActionSearch(val) {
  actionSearchQuery = (val || "").trim().toLowerCase();
  renderActionButtons(currentObsActions);
}

function renderActionButtons(actions) {
  const container = document.getElementById("actions-container");
  container.innerHTML = "";
  let filtered = activeCategoryFilter === "all"
    ? actions
    : actions.filter(a => (a.category || "general") === activeCategoryFilter);

  if (actionSearchQuery) {
    filtered = filtered.filter(a =>
      (a.label && a.label.toLowerCase().includes(actionSearchQuery)) ||
      (a.id && a.id.toLowerCase().includes(actionSearchQuery)) ||
      (a.category && a.category.toLowerCase().includes(actionSearchQuery))
    );
  }

  const countEl = document.getElementById("action-count");
  if (actionSearchQuery || activeCategoryFilter !== "all") {
    countEl.textContent = `${filtered.length} of ${actions.length}`;
  } else {
    countEl.textContent = `${actions.length}`;
  }

  if (filtered.length === 0) {
    container.innerHTML = '<div style="color: var(--text-muted); font-size: 0.9rem; padding: 1rem;">No legal actions match current filters.</div>';
    return;
  }

  filtered.forEach((act, idx) => {
    const btn = document.createElement("button");
    btn.className = "action-btn";
    btn.onclick = () => stepAction(act.id);

    const catClass = "cat-" + (act.category || "general");
    const costHtml = act.stamina_cost > 0 ? `<span class="badge-cost">⚡ ${act.stamina_cost} SP</span>` : "";
    const keyHint = (!actionSearchQuery && idx < 9) ? `<span class="key-badge">[${idx + 1}]</span>` : "";

    btn.innerHTML = `
      <div class="action-label">${keyHint}${act.label}</div>
      <div class="action-meta">
        <span class="badge-category ${catClass}">${act.category}</span>
        <span>Risk: ${act.risk}</span>
        ${costHtml}
      </div>
    `;
    container.appendChild(btn);
  });
}

function renderGame(obs, char, quest, codex, transit, trade, weather, bounty, companion, bestiary, survival, orders, shrines) {
  currentQuestData = quest;
  if (codex) currentCodexData = codex;
  if (trade) currentTradeData = trade;
  if (weather) currentWeatherData = weather;
  if (bounty) currentBountyData = bounty;
  if (companion) currentCompanionData = companion;
  if (bestiary) currentBestiaryData = bestiary;
  if (survival) currentSurvivalData = survival;
  if (orders) currentOrdersData = orders;
  if (shrines) currentShrinesData = shrines;
  lastObservation = obs;
  lastCharacter = char;
  saveSessionToLocalStorage(obs, char, quest, codex);

  // HUD
  document.getElementById("char-name").textContent = char.name;
  document.getElementById("char-origin").textContent = `${char.ancestry} &bull; ${char.background}`;
  
  const hpPct = Math.max(0, Math.min(100, (char.health / char.max_health) * 100));
  const hpBar = document.getElementById("hp-bar");
  hpBar.style.width = hpPct + "%";
  document.getElementById("hp-text").textContent = `${char.health}/${char.max_health}`;
  if (hpPct <= 25) {
    hpBar.style.boxShadow = "0 0 8px #f85149";
  } else {
    hpBar.style.boxShadow = "none";
  }

  const spPct = Math.max(0, Math.min(100, (char.stamina / char.max_stamina) * 100));
  const spBar = document.getElementById("sp-bar");
  spBar.style.width = spPct + "%";
  document.getElementById("sp-text").textContent = `${char.stamina}/${char.max_stamina}`;
  if (spPct <= 20) {
    spBar.style.boxShadow = "0 0 8px #d29922";
  } else {
    spBar.style.boxShadow = "none";
  }

  document.getElementById("turn-display").textContent = obs.turn_count;
  document.getElementById("fingerprint-display").textContent = obs.fingerprint ? obs.fingerprint.substring(0, 16) + "..." : "n/a";

  const weatherBtn = document.getElementById("weather-btn");
  if (weatherBtn && currentWeatherData) {
    weatherBtn.textContent = `⛅ ${currentWeatherData.name}`;
  }

  const bountyBtn = document.getElementById("bounty-btn");
  if (bountyBtn && currentBountyData) {
    bountyBtn.textContent = `🎯 Bounties (${currentBountyData.completed_count}/10)`;
  }

  const compBtn = document.getElementById("companion-btn");
  if (compBtn && currentCompanionData) {
    const actName = currentCompanionData.active_companion_name;
    if (actName && actName !== "None") {
      compBtn.textContent = `👥 ${actName} [Active]`;
    } else {
      compBtn.textContent = `👥 Party (${currentCompanionData.recruited_count}/5)`;
    }
  }

  const bestiaryBtn = document.getElementById("bestiary-btn");
  if (bestiaryBtn && currentBestiaryData) {
    bestiaryBtn.textContent = `🦁 Hunt (${currentBestiaryData.hunted_count}/10)`;
  }

  const survBtn = document.getElementById("survival-btn");
  if (survBtn && currentSurvivalData) {
    survBtn.textContent = `🏕️ Camp (${currentSurvivalData.meals_cooked} Cooked)`;
  }

  const ordBtn = document.getElementById("orders-btn");
  if (ordBtn && currentOrdersData) {
    ordBtn.textContent = `🛡️ Orders (${currentOrdersData.banners_held}/5 Banners)`;
  }

  const shrBtn = document.getElementById("shrines-btn");
  if (shrBtn && currentShrinesData) {
    shrBtn.textContent = `🏛️ Shrines (${currentShrinesData.consecrated_count}/6)`;
  }

  // Quest Tracker
  if (quest) {
    const stageNames = {
      "stage_crags_beacon": "Ignite Highland Beacon (The Reach)",
      "stage_warrens_ledger": "Recover Shadow Ledger (The Lowlands)",
      "stage_scorch_compass": "Acquire Solar Compass (The Scorchwaste)",
      "stage_court_verdict": "Win Tribunal Verdict (The High Court)",
      "stage_abyssal_pearl": "Retrieve Sunken Pearl (The Sunken Hollows)"
    };
    const activeText = quest.is_finished
      ? "All 5 Sovereignty Seals Claimed! The Unbounded Throne awaits."
      : (stageNames[quest.active_stage] || quest.active_stage || "Exploring Continent");
    document.getElementById("quest-stage-text").textContent = activeText;
    const completedCount = (quest.completed_stages || []).length;
    document.getElementById("quest-seals-count").textContent = `${completedCount}/5 Seals`;

    // Subquests
    const subquestBanner = document.getElementById("subquest-banner");
    const subquestText = document.getElementById("subquest-text");
    if (quest.subquests && subquestBanner && subquestText) {
      const activeSubEntry = Object.entries(quest.subquests).find(([k, v]) => !v.is_finished && v.active_stage);
      if (activeSubEntry) {
        const qName = activeSubEntry[0].replace(/^subquest_/, '').replace(/^quest_/, '').replace(/_/g, ' ').toUpperCase();
        subquestText.textContent = `${qName}: Stage ${activeSubEntry[1].active_stage}`;
        subquestBanner.style.display = "block";
      } else {
        subquestBanner.style.display = "none";
      }
    }
  }

  // Status Effects & Hazards
  const statusContainer = document.getElementById("status-container");
  if (statusContainer) {
    const statusBadges = [];
    const markers = char.markers || [];
    markers.forEach(m => {
      let bg = "rgba(168, 85, 247, 0.25)";
      let color = "#c084fc";
      if (m.startsWith("stance_")) {
        const stanceName = m.replace("stance_", "").toUpperCase();
        statusBadges.push(`<span class="tag" style="background: rgba(187, 128, 255, 0.35); color: #e2baff; font-weight: 700; border: 1px solid #c084fc;">🥋 STANCE: ${stanceName}</span>`);
        return;
      }
      if (m.includes("conflagration") || m.includes("fire")) { bg = "rgba(249, 115, 22, 0.25)"; color = "#fb923c"; }
      else if (m.includes("stun") || m.includes("shock")) { bg = "rgba(234, 179, 8, 0.25)"; color = "#facc15"; }
      else if (m.includes("water") || m.includes("wet")) { bg = "rgba(56, 189, 248, 0.25)"; color = "#38bdf8"; }
      else if (m.includes("corroded") || m.includes("acid")) { bg = "rgba(132, 204, 22, 0.25)"; color = "#a3e635"; }
      statusBadges.push(`<span class="tag" style="background: ${bg}; color: ${color}; font-weight: 600;">⚡ ${m}</span>`);
    });
    statusContainer.innerHTML = statusBadges.join("");
  }

  // Inventory & Badges
  const invContainer = document.getElementById("inventory-container");
  let invHtml = char.inventory.map(i => `<span class="tag" style="background: rgba(255,255,255,0.08);">🎒 ${i}</span>`).join("");
  invHtml += char.traits.map(t => `<span class="tag trait">✨ ${t}</span>`).join("");
  invContainer.innerHTML = invHtml;

  // Scene
  document.getElementById("scene-region").textContent = `${obs.region_id.toUpperCase()} // SCENE ${obs.scene_id}`;
  document.getElementById("scene-title").textContent = obs.title;
  document.getElementById("scene-description").textContent = obs.description;

  const eventsBox = document.getElementById("scene-events");
  if (obs.events && obs.events.length > 0) {
    eventsBox.style.display = "block";
    eventsBox.innerHTML = obs.events.map(e => `&bull; ${e}`).join("<br>");
  } else {
    eventsBox.style.display = "none";
  }

  // Terminal check
  const termPane = document.getElementById("terminal-pane");
  if (obs.is_terminal) {
    termPane.style.display = "block";
    document.getElementById("terminal-title").textContent = obs.outcome ? `Adventure Concluded (${obs.outcome})` : "Adventure Concluded";
    document.getElementById("terminal-desc").textContent = obs.message;
  } else {
    termPane.style.display = "none";
  }

  // Legal Actions with Category Filtering
  currentObsActions = obs.legal_actions || [];
  renderCategoryFilters(currentObsActions);
  renderActionButtons(currentObsActions);
}

function toggleSheetModal() {
  const modal = document.getElementById("sheet-modal");
  if (modal.style.display === "none") {
    renderSheetModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function renderSheetModalContent() {
  if (!gameState || !gameState.character) return;
  const char = gameState.character;
  document.getElementById("modal-sheet-title").textContent = `${char.name} — ${char.ancestry} (${char.background})`;
  const content = document.getElementById("modal-sheet-content");

  let attrsHtml = Object.entries(char.attributes || {}).map(([k, v]) => `
    <div class="stat-box">
      <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">${k}</div>
      <div style="font-size: 1.1rem; font-weight: 700; color: #58a6ff;">${v}</div>
    </div>
  `).join("") || '<div style="color: var(--text-muted);">None</div>';

  let skillsHtml = Object.entries(char.skills || {}).map(([k, v]) => `
    <div class="stat-box">
      <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">${k}</div>
      <div style="font-size: 1.1rem; font-weight: 700; color: #3fb950;">+${v}</div>
    </div>
  `).join("") || '<div style="color: var(--text-muted);">None</div>';

  let repHtml = Object.entries(char.reputation || {}).map(([k, v]) => {
    const col = v > 0 ? "#3fb950" : (v < 0 ? "#f85149" : "var(--text-muted)");
    const sign = v > 0 ? "+" : "";
    return `
      <div class="stat-box">
        <div style="font-size: 0.75rem; color: var(--text-muted);">${k.replace(/_/g, ' ').toUpperCase()}</div>
        <div style="font-size: 1.1rem; font-weight: 700; color: ${col};">${sign}${v}</div>
      </div>
    `;
  }).join("") || '<div style="color: var(--text-muted); font-size: 0.85rem;">Neutral with all factions</div>';

  let invHtml = (char.inventory || []).map(i => `<span class="tag" style="background: rgba(255,255,255,0.08);">🎒 ${i}</span>`).join("") || '<span style="color: var(--text-muted);">Empty</span>';
  let traitsHtml = (char.traits || []).map(t => `<span class="tag trait">✨ ${t}</span>`).join("") || '<span style="color: var(--text-muted);">None</span>';
  let flawsHtml = (char.flaws || []).map(f => `<span class="tag" style="background: rgba(248,81,73,0.15); color: #f85149;">⚠️ ${f}</span>`).join("") || '<span style="color: var(--text-muted);">None</span>';
  let markersHtml = (char.markers || []).map(m => `<span class="tag" style="background: rgba(168,85,247,0.15); color: #c084fc;">⚡ ${m}</span>`).join("") || '<span style="color: var(--text-muted);">None</span>';

  content.innerHTML = `
    <div style="margin-bottom: 1.25rem;">
      <h4 style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;">Core Attributes</h4>
      <div class="stat-grid">${attrsHtml}</div>
    </div>
    <div style="margin-bottom: 1.25rem;">
      <h4 style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;">Skills</h4>
      <div class="stat-grid">${skillsHtml}</div>
    </div>
    <div style="margin-bottom: 1.25rem;">
      <h4 style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;">Faction Standings</h4>
      <div class="stat-grid">${repHtml}</div>
    </div>
    <div style="margin-bottom: 1.25rem;">
      <h4 style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;">Traits & Flaws</h4>
      <div class="tag-row">${traitsHtml}${flawsHtml}</div>
    </div>
    <div style="margin-bottom: 1.25rem;">
      <h4 style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;">Active Markers</h4>
      <div class="tag-row">${markersHtml}</div>
    </div>
    <div>
      <h4 style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;">Inventory Items</h4>
      <div class="tag-row">${invHtml}</div>
    </div>
  `;
}

function toggleReplayModal() {
  const modal = document.getElementById("replay-modal");
  if (modal.style.display === "none") {
    const payload = {
      preset: selectedPreset,
      seed: parseInt(document.getElementById("seed-input").value, 10) || 42,
      turn_count: gameState ? gameState.turn_count : 0,
      actions: gameState ? gameState.history : [],
      fingerprint: gameState ? document.getElementById("fingerprint-display").textContent : ""
    };
    document.getElementById("trace-textarea").value = JSON.stringify(payload, null, 2);
    document.getElementById("replay-status").textContent = "";
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function copyTraceToClipboard() {
  const text = document.getElementById("trace-textarea").value;
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => {
      alert("Trace JSON copied to clipboard!");
    }).catch(() => {
      document.getElementById("trace-textarea").select();
      document.execCommand("copy");
      alert("Trace JSON copied to clipboard!");
    });
  } else {
    document.getElementById("trace-textarea").select();
    document.execCommand("copy");
    alert("Trace JSON copied to clipboard!");
  }
}

async function runImportedReplay() {
  const text = document.getElementById("load-trace-textarea").value.trim();
  const statusEl = document.getElementById("replay-status");
  if (!text) {
    statusEl.innerHTML = '<span style="color: #f85149;">Please paste a valid replay JSON payload.</span>';
    return;
  }
  try {
    const payload = JSON.parse(text);
    statusEl.innerHTML = '<span style="color: #58a6ff;">Executing replay trace on engine...</span>';
    const res = await fetch("/api/game/replay", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error("Replay verification failed: " + res.statusText);
    const data = await res.json();
    gameState = data.state;
    stateHistory = [JSON.parse(JSON.stringify(gameState))];
    updateUndoButton();
    renderGame(data.observation, data.character, data.quest, data.codex, data.transit, data.trade, data.weather, data.bounty, data.companion, data.bestiary, data.survival, data.orders, data.shrines);
    statusEl.innerHTML = `<span style="color: #3fb950;">✓ Replay verified: ${data.turn_count} turns executed. SHA: ${data.final_fingerprint.substring(0,16)}...</span>`;
    setTimeout(() => {
      document.getElementById("replay-modal").style.display = "none";
      document.getElementById("select-view").style.display = "none";
      document.getElementById("play-view").style.display = "block";
    }, 1200);
  } catch (err) {
    statusEl.innerHTML = `<span style="color: #f85149;">Error: ${err.message}</span>`;
  }
}

function saveSessionToLocalStorage(obs, char, quest, codex) {
  if (!gameState) return;
  try {
    const session = {
      state: gameState,
      history: stateHistory,
      preset: selectedPreset,
      seed: parseInt(document.getElementById("seed-input").value, 10) || 42,
      obs: obs,
      char: char,
      quest: quest,
      codex: codex || currentCodexData,
      timestamp: Date.now()
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
  } catch (e) {
    console.warn("Storage save skipped:", e);
  }
}

function checkResumeSession() {
  const box = document.getElementById("resume-session-box");
  if (!box) return;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      box.style.display = "none";
      return;
    }
    const session = JSON.parse(raw);
    if (!session || !session.state || !session.char) {
      box.style.display = "none";
      return;
    }
    const dateStr = new Date(session.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    box.innerHTML = `
      <div>
        <div style="font-size: 0.8rem; color: var(--green); font-weight: 600; text-transform: uppercase;">Saved Adventure Found</div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #fff;">${session.char.name} — ${session.char.ancestry} (${session.char.background})</div>
        <div style="font-size: 0.85rem; color: var(--text-muted);">
          Turn ${session.state.turn_count} &bull; ${session.obs ? session.obs.title : session.state.current_scene} &bull; Saved at ${dateStr}
        </div>
      </div>
      <div style="display: flex; gap: 0.5rem; align-items: center;">
        <button class="btn" style="padding: 0.45rem 0.9rem;" onclick="resumeSavedAdventure()">▶ Resume Adventure</button>
        <button class="btn btn-secondary" style="padding: 0.45rem 0.7rem;" onclick="discardSavedSession()">✕ Discard</button>
      </div>
    `;
    box.style.display = "flex";
  } catch (e) {
    box.style.display = "none";
  }
}

async function resumeSavedAdventure() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const session = JSON.parse(raw);
    gameState = session.state;
    stateHistory = session.history && session.history.length > 0 ? session.history : [JSON.parse(JSON.stringify(gameState))];
    selectedPreset = session.preset || "cutpurse";
    document.getElementById("seed-input").value = session.seed || 42;
    updateUndoButton();

    const res = await fetch("/api/game/observe", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ state: gameState })
    });
    if (!res.ok) throw new Error("Resume observation failed: " + res.statusText);
    const data = await res.json();
    renderGame(data.observation, data.character, data.quest, data.codex, data.transit, data.trade, data.weather, data.bounty, data.companion, data.bestiary, data.survival, data.orders, data.shrines);
    document.getElementById("select-view").style.display = "none";
    document.getElementById("play-view").style.display = "block";
  } catch (err) {
    alert("Could not resume saved adventure: " + err.message);
    discardSavedSession();
  }
}

function discardSavedSession() {
  localStorage.removeItem(STORAGE_KEY);
  const box = document.getElementById("resume-session-box");
  if (box) box.style.display = "none";
}

async function fetchQuestsDataIfNeeded() {
  if (cachedQuestsMetadata) return cachedQuestsMetadata;
  try {
    const res = await fetch("/api/game/quests");
    if (res.ok) {
      cachedQuestsMetadata = await res.json();
    }
  } catch (e) {
    console.warn("Quests fetch failed:", e);
  }
  return cachedQuestsMetadata;
}

async function toggleQuestModal() {
  const modal = document.getElementById("quest-modal");
  if (modal.style.display === "none") {
    await fetchQuestsDataIfNeeded();
    renderQuestModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function switchQuestTab(tab) {
  activeQuestTab = tab;
  document.querySelectorAll(".quest-tab-bar .tab-btn").forEach(b => b.classList.remove("active"));
  const btn = document.getElementById(`tab-btn-${tab}`);
  if (btn) btn.classList.add("active");
  renderQuestModalContent();
}

function renderQuestModalContent() {
  const content = document.getElementById("modal-quest-content");
  if (!content) return;
  const q = currentQuestData;
  const flags = gameState ? (gameState.world_flags || {}) : {};

  if (activeQuestTab === "campaign") {
    const completedStages = (q && q.completed_stages) || [];
    const completedCount = completedStages.length;
    const pct = Math.round((completedCount / 5) * 100);

    let sealsHtml = SEALS_METADATA.map(s => {
      const isClaimed = completedStages.includes(s.id) || flags[s.flag] === true;
      const isActive = !isClaimed && (q && q.active_stage === s.id);
      let cardClass = "seal-card";
      let statusBadge = '<span class="tag" style="background: rgba(255,255,255,0.06); color: var(--text-muted);">🔒 PENDING</span>';

      if (isClaimed) {
        cardClass += " claimed";
        statusBadge = '<span class="tag" style="background: rgba(63,185,80,0.25); color: #3fb950; font-weight: 600;">✓ CLAIMED</span>';
      } else if (isActive) {
        cardClass += " active";
        statusBadge = '<span class="tag" style="background: rgba(245,158,11,0.25); color: #f59e0b; font-weight: 600;">▶ ACTIVE OBJECTIVE</span>';
      }

      const approachesTags = s.approaches.map(a => `<span class="tag" style="background: rgba(255,255,255,0.05); font-size: 0.7rem;">${a}</span>`).join("");

      return `
        <div class="${cardClass}">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
            <div style="font-weight: 700; font-size: 0.95rem; color: #fff;">${s.icon} ${s.title} (${s.province})</div>
            <div>${statusBadge}</div>
          </div>
          <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.4rem;">${s.desc}</div>
          <div class="tag-row" style="margin-top: 0.2rem;">
            <span style="font-size: 0.75rem; color: var(--text-muted); margin-right: 0.3rem;">Viable Approaches:</span>
            ${approachesTags}
          </div>
        </div>
      `;
    }).join("");

    content.innerHTML = `
      <div style="margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <h4 style="font-size: 0.95rem; color: #fff;">The Five Seals of Sovereignty</h4>
          <span style="font-size: 0.85rem; color: #fbbf24; font-weight: 700;">${completedCount}/5 Seals (${pct}%)</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill" style="width: ${pct}%;"></div>
        </div>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1rem;">
          Unite or exploit the five regional powers of the continent to claim the Unbounded Throne.
        </p>
      </div>
      <div>${sealsHtml}</div>
    `;
  } else if (activeQuestTab === "subquests") {
    const subquestsMeta = (cachedQuestsMetadata && cachedQuestsMetadata.subquests) || {};
    const subProgress = (q && q.subquests) || {};

    let listHtml = Object.entries(subquestsMeta).map(([qid, qData]) => {
      const prog = subProgress[qid] || {};
      const isDone = prog.is_finished === true;
      const activeStage = prog.active_stage || "Stage 1";
      const badge = isDone
        ? '<span class="tag" style="background: rgba(63,185,80,0.25); color: #3fb950; font-weight: 600;">✓ COMPLETE</span>'
        : `<span class="tag" style="background: rgba(88,166,255,0.2); color: #58a6ff; font-weight: 600;">STAGE: ${activeStage}</span>`;

      return `
        <div class="seal-card" style="margin-bottom: 0.75rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
            <div style="font-weight: 700; font-size: 0.95rem; color: #fff;">📜 ${qData.name}</div>
            <div>${badge}</div>
          </div>
          <div style="font-size: 0.85rem; color: var(--text-muted);">${qData.synopsis}</div>
        </div>
      `;
    }).join("");

    content.innerHTML = `
      <div style="margin-bottom: 0.75rem;">
        <h4 style="font-size: 0.95rem; color: #fff; margin-bottom: 0.25rem;">Provincial Narrative Chains</h4>
        <p style="font-size: 0.8rem; color: var(--text-muted);">
          Deep multi-stage side quests unique to each of the 5 macro-provinces.
        </p>
      </div>
      <div>${listHtml || '<p style="color: var(--text-muted);">No subquests loaded.</p>'}</div>
    `;
  } else if (activeQuestTab === "intrigue") {
    const intrigueMeta = (cachedQuestsMetadata && cachedQuestsMetadata.intrigue_quests) || {};
    const intrigueProg = (q && q.intrigue_quests) || {};

    let listHtml = Object.entries(intrigueMeta).map(([qid, qData]) => {
      const prog = intrigueProg[qid] || {};
      const isDone = prog.is_finished === true;
      const ending = prog.ending ? `<div style="font-size: 0.8rem; color: #a3e635; margin-top: 0.3rem;">Outcome: ${prog.ending}</div>` : "";
      const badge = isDone
        ? '<span class="tag" style="background: rgba(168,85,247,0.25); color: #c084fc; font-weight: 600;">✓ RESOLVED</span>'
        : '<span class="tag" style="background: rgba(248,81,73,0.2); color: #f85149; font-weight: 600;">ACTIVE CONFLICT</span>';

      return `
        <div class="seal-card" style="margin-bottom: 0.75rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
            <div style="font-weight: 700; font-size: 0.95rem; color: #fff;">⚔️ ${qData.name}</div>
            <div>${badge}</div>
          </div>
          <div style="font-size: 0.85rem; color: var(--text-muted);">${qData.synopsis}</div>
          ${ending}
        </div>
      `;
    }).join("");

    content.innerHTML = `
      <div style="margin-bottom: 0.75rem;">
        <h4 style="font-size: 0.95rem; color: #fff; margin-bottom: 0.25rem;">Faction Intrigue Arcs</h4>
        <p style="font-size: 0.8rem; color: var(--text-muted);">
          High-stakes political conflicts with mutually exclusive endings and shifting faction balances.
        </p>
      </div>
      <div>${listHtml || '<p style="color: var(--text-muted);">No intrigue arcs loaded.</p>'}</div>
    `;
  }
}

async function fetchCodexDataIfNeeded() {
  if (cachedCodexMetadata) return cachedCodexMetadata;
  try {
    const res = await fetch("/api/game/codex");
    if (res.ok) {
      cachedCodexMetadata = await res.json();
    }
  } catch (e) {
    console.warn("Codex fetch failed:", e);
  }
  return cachedCodexMetadata;
}

async function toggleCodexModal() {
  const modal = document.getElementById("codex-modal");
  if (modal.style.display === "none") {
    await fetchCodexDataIfNeeded();
    renderCodexModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function renderCodexModalContent() {
  const content = document.getElementById("modal-codex-content");
  if (!content) return;
  const meta = cachedCodexMetadata;
  const prog = currentCodexData;
  const flags = gameState ? (gameState.world_flags || {}) : {};

  const discCount = prog ? prog.discovered_count : 0;
  const totalCount = meta ? meta.total_entries : 15;

  let html = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--panel-border);">
      <div>
        <div style="font-weight: 700; color: #fff; font-size: 1rem;">Ancient Inscriptions Discovered</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);">Decipher relics across provincial sanctums to master ancient history.</div>
      </div>
      <div style="font-size: 1.1rem; font-weight: 700; color: #c084fc;">${discCount} / ${totalCount}</div>
    </div>
  `;

  if (prog && prog.masteries_unlocked && prog.masteries_unlocked.length > 0) {
    html += `
      <div style="background: rgba(168, 85, 247, 0.12); border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 6px; padding: 0.6rem 0.9rem; margin-bottom: 1rem;">
        <div style="font-size: 0.8rem; font-weight: 700; color: #c084fc; text-transform: uppercase;">🏆 Masteries Achieved</div>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.3rem;">
          ${prog.masteries_unlocked.map(m => `
            <div class="tag" style="background: rgba(168, 85, 247, 0.25); color: #e9d5ff; border: 1px solid rgba(168, 85, 247, 0.4); font-size: 0.8rem; padding: 0.2rem 0.5rem;">
              ⭐ <strong>${m.title}</strong>: ${m.description}
            </div>
          `).join("")}
        </div>
      </div>
    `;
  }

  const allEntries = (meta && meta.entries) || (prog && prog.entries) || [];
  const provinces = [
    { name: "The Reach", key: "reach" },
    { name: "The Lowlands", key: "lowlands" },
    { name: "The Scorchwaste", key: "scorchwaste" },
    { name: "The High Court", key: "high_court" },
    { name: "The Sunken Hollows", key: "sunken_hollows" }
  ];

  provinces.forEach(p => {
    const provEntries = allEntries.filter(e => e.province_key === p.key);
    const provProg = prog && prog.province_progress && prog.province_progress[p.key];
    const provDisc = provProg ? provProg.discovered : provEntries.filter(e => flags[e.reward_flag] === true).length;
    const isMastered = provProg ? provProg.mastery_unlocked : provDisc >= 3;

    html += `
      <div style="margin-bottom: 1rem; background: var(--bg-card); border: 1px solid var(--panel-border); border-radius: 6px; padding: 0.75rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
          <span style="font-weight: 700; color: #e5e7eb; font-size: 0.9rem;">${p.name}</span>
          <span style="font-size: 0.8rem; font-weight: 600; color: ${isMastered ? '#c084fc' : 'var(--text-muted)'};">
            ${isMastered ? '🏆 MASTERED (' + provDisc + '/3)' : provDisc + '/3 Discovered'}
          </span>
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
          ${provEntries.map(e => {
            const isUnlocked = flags[e.reward_flag] === true || (prog && prog.discovered_ids && prog.discovered_ids.includes(e.id));
            if (isUnlocked) {
              const liveEntry = (prog && prog.entries && prog.entries.find(x => x.id === e.id)) || e;
              return `
                <div style="background: rgba(168, 85, 247, 0.08); border-left: 3px solid #c084fc; padding: 0.5rem 0.75rem; border-radius: 0 4px 4px 0;">
                  <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #fff; font-size: 0.85rem;">${liveEntry.title}</strong>
                    <span class="tag" style="background: rgba(168,85,247,0.2); color: #c084fc; font-size: 0.7rem;">${liveEntry.category}</span>
                  </div>
                  <div style="font-size: 0.8rem; color: #d1d5db; margin-top: 0.25rem; font-style: italic;">
                    "${liveEntry.lore_text || liveEntry.discovery_text || 'Ancient knowledge inscribed in stone.'}"
                  </div>
                  <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 0.25rem;">
                    Site: <code>${liveEntry.scene_id}</code> &bull; Action: <em>${liveEntry.action_label}</em>
                  </div>
                </div>
              `;
            } else {
              return `
                <div style="background: rgba(255, 255, 255, 0.02); border-left: 3px solid rgba(255, 255, 255, 0.1); padding: 0.4rem 0.75rem; border-radius: 0 4px 4px 0; opacity: 0.65;">
                  <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: var(--text-muted); font-size: 0.85rem;">🔒 Undeciphered Inscription</span>
                    <span class="tag" style="background: rgba(255,255,255,0.05); color: var(--text-muted); font-size: 0.7rem;">${e.category}</span>
                  </div>
                  <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.15rem;">
                    Located in <code>${e.scene_id}</code>. Requires specialized skill, trait, or gear.
                  </div>
                </div>
              `;
            }
          }).join("")}
        </div>
      </div>
    `;
  });

  content.innerHTML = html;
}

async function fetchTradeDataIfNeeded() {
  if (cachedTradeMetadata) return cachedTradeMetadata;
  try {
    const res = await fetch("/api/game/trade");
    if (res.ok) {
      cachedTradeMetadata = await res.json();
    }
  } catch (e) {
    console.warn("Trade fetch failed:", e);
  }
  return cachedTradeMetadata;
}

async function toggleTradeModal() {
  const modal = document.getElementById("trade-modal");
  if (modal.style.display === "none") {
    await fetchTradeDataIfNeeded();
    renderTradeModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function renderTradeModalContent() {
  const content = document.getElementById("modal-trade-content");
  if (!content) return;
  const meta = cachedTradeMetadata;
  const prog = currentTradeData;
  const flags = gameState ? (gameState.world_flags || {}) : {};
  const inv = (lastCharacter && lastCharacter.inventory) || [];

  const tradesCount = prog ? prog.completed_trades : (flags.completed_trades || 0);
  const arbCount = prog ? prog.arbitrage_completed : (flags.arbitrage_completed || 0);
  const hubsCount = prog ? prog.hubs_visited_count : 0;
  const isConsortium = prog ? prog.is_consortium_recognized : false;
  const isMaster = prog ? prog.is_master_trader : false;

  const commodities = (meta && meta.commodities) || [];
  const hubs = (meta && meta.hubs) || {};

  let html = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--panel-border);">
      <div>
        <div style="font-weight: 700; color: #fff; font-size: 1rem;">Continental Commodity Exchange</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);">Buy provincial goods at origin and sell at distant import hubs for profit.</div>
      </div>
      <div style="display: flex; gap: 0.6rem; align-items: center;">
        <span class="tag" style="background: rgba(234,179,8,0.2); color: #facc15; font-weight: 600; font-size: 0.8rem;">Trades: ${tradesCount}</span>
        <span class="tag" style="background: rgba(63,185,80,0.2); color: #3fb950; font-weight: 600; font-size: 0.8rem;">Arbitrage: ${arbCount}</span>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1rem;">
      <div style="background: var(--bg-card); border: 1px solid var(--panel-border); border-radius: 6px; padding: 0.6rem 0.8rem;">
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Merchant Consortium</div>
        <div style="margin-top: 0.2rem; font-size: 0.9rem; font-weight: 600; color: ${isConsortium ? '#3fb950' : 'var(--gold)'};">
          ${isConsortium ? '⭐ RECOGNIZED VENDOR' : 'LOCKED (Trade at 3+ Hubs: ' + hubsCount + '/3)'}
        </div>
      </div>
      <div style="background: var(--bg-card); border: 1px solid var(--panel-border); border-radius: 6px; padding: 0.6rem 0.8rem;">
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Master Trader Milestone</div>
        <div style="margin-top: 0.2rem; font-size: 0.9rem; font-weight: 600; color: ${isMaster ? '#c084fc' : 'var(--text-muted)'};">
          ${isMaster ? '👑 MASTER CONTINENTAL TRADER' : 'LOCKED (All 5 Goods + 2 Arbitrage)'}
        </div>
      </div>
    </div>

    <div style="margin-bottom: 1rem;">
      <div style="font-size: 0.85rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem;">Provincial Commodity Manifest</div>
      <div style="display: flex; flex-direction: column; gap: 0.6rem;">
        ${commodities.map(c => {
          const isHeld = inv.includes(c.id);
          const wasTraded = flags[`traded_${c.id}`] || flags[`sold_${c.id}`];
          const bonusDestinations = Object.entries(c.import_bonuses || {}).map(([hubKey, bonus]) => {
            const h = hubs[hubKey];
            const hName = h ? h.hub_name : hubKey;
            return `<span class="tag" style="background: rgba(63,185,80,0.15); color: #3fb950; font-size: 0.7rem;">${hName} (+${bonus}🪙)</span>`;
          }).join(" ");

          return `
            <div style="background: var(--bg-card); border: 1px solid ${isHeld ? 'rgba(234,179,8,0.5)' : 'var(--panel-border)'}; border-radius: 6px; padding: 0.6rem 0.8rem;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                  <strong style="color: #fff; font-size: 0.9rem;">${c.name}</strong>
                  <span style="font-size: 0.75rem; color: var(--text-muted); margin-left: 0.4rem;">Origin: ${c.origin_province}</span>
                </div>
                <div>
                  ${isHeld ? '<span class="tag" style="background: rgba(234,179,8,0.25); color: #facc15; font-weight: 700; font-size: 0.75rem;">IN CARGO</span>' : (wasTraded ? '<span class="tag" style="background: rgba(88,166,255,0.2); color: var(--accent); font-size: 0.75rem;">TRADED</span>' : '')}
                </div>
              </div>
              <div style="font-size: 0.8rem; color: #d1d5db; margin: 0.25rem 0;">${c.description}</div>
              <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.4rem; font-size: 0.75rem; flex-wrap: wrap; gap: 0.3rem;">
                <div>
                  <span style="color: var(--text-muted);">Base Buy:</span> <span style="color: var(--gold); font-weight: 600;">${c.base_buy_price} Silver</span>
                  <span style="color: var(--text-muted); margin-left: 0.4rem;">(or Barter: <code>${c.barter_item}</code>)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.3rem;">
                  <span style="color: var(--text-muted);">Import Demand:</span>
                  ${bonusDestinations}
                </div>
              </div>
            </div>
          `;
        }).join("")}
      </div>
    </div>
  `;

  content.innerHTML = html;
}

async function fetchWeatherDataIfNeeded() {
  if (cachedWeatherMetadata) return cachedWeatherMetadata;
  try {
    const res = await fetch("/api/game/weather");
    if (res.ok) {
      cachedWeatherMetadata = await res.json();
    }
  } catch (e) {
    console.warn("Weather fetch failed:", e);
  }
  return cachedWeatherMetadata;
}

async function toggleWeatherModal() {
  const modal = document.getElementById("weather-modal");
  if (modal.style.display === "none") {
    await fetchWeatherDataIfNeeded();
    renderWeatherModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function renderWeatherModalContent() {
  const content = document.getElementById("modal-weather-content");
  if (!content) return;
  const meta = cachedWeatherMetadata;
  const w = currentWeatherData;
  const turn = (lastObservation && lastObservation.turn_count) || (gameState && gameState.turn_count) || 0;
  const turnsInCycle = turn % 6;
  const remaining = 6 - turnsInCycle;

  let html = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--panel-border);">
      <div>
        <div style="font-weight: 700; color: #fff; font-size: 1rem;">Continental Weather Dynamics</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);">Deterministic regional micro-climates cycle every 6 turns.</div>
      </div>
      <div>
        <span class="tag" style="background: rgba(56,189,248,0.2); color: #38bdf8; font-weight: 600; font-size: 0.8rem;">
          Turn ${turn} &bull; Next Shift in ${remaining} turn${remaining === 1 ? '' : 's'}
        </span>
      </div>
    </div>
  `;

  if (w) {
    html += `
      <div style="background: var(--bg-card); border: 1px solid rgba(56,189,248,0.4); border-radius: 6px; padding: 0.8rem; margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.35rem;">
          <div style="font-size: 0.95rem; font-weight: 700; color: #fff;">
            Local Micro-Climate: <span style="color: #38bdf8;">${w.name}</span>
          </div>
          <span class="tag" style="background: rgba(234,179,8,0.15); color: #facc15; font-size: 0.75rem;">
            ${w.hazard_type ? ('Hazard: ' + w.hazard_type.toUpperCase()) : 'MILD FRONT'}
          </span>
        </div>
        <div style="font-size: 0.85rem; color: #d1d5db; margin-bottom: 0.5rem; line-height: 1.4;">${w.description}</div>
        <div style="display: flex; gap: 0.6rem; font-size: 0.75rem; align-items: center;">
          <span style="color: var(--text-muted);">Systemic Affordance:</span>
          <span class="tag" style="background: rgba(63,185,80,0.15); color: #3fb950; font-weight: 600;">${w.action_label}</span>
          <span style="color: var(--text-muted);">Province: ${w.province}</span>
        </div>
      </div>
    `;
  }

  html += `
    <div style="margin-bottom: 0.5rem; font-size: 0.85rem; font-weight: 700; color: #fff;">Provincial Micro-Climates (12 Total Fronts)</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;">
  `;

  const conditions = (meta && meta.conditions) || [];
  const provGroups = {
    "The Reach": { icon: "🏔️", list: [] },
    "The Scorchwaste": { icon: "🏜️", list: [] },
    "The Lowlands": { icon: "🌾", list: [] },
    "The High Court": { icon: "🏛️", list: [] },
    "The Sunken Hollows": { icon: "🌊", list: [] },
    "Central Crossroads": { icon: "⚖️", list: [] }
  };

  for (const c of conditions) {
    if (provGroups[c.province]) {
      provGroups[c.province].list.push(c);
    }
  }

  for (const [pName, pData] of Object.entries(provGroups)) {
    const isCurrentProv = w && w.province === pName;
    html += `
      <div style="background: var(--bg-card); border: 1px solid ${isCurrentProv ? '#38bdf8' : 'var(--panel-border)'}; border-radius: 6px; padding: 0.6rem 0.75rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
          <span style="font-weight: 700; font-size: 0.85rem; color: #fff;">${pData.icon} ${pName}</span>
          ${isCurrentProv ? '<span class="tag" style="background: rgba(56,189,248,0.25); color: #38bdf8; font-size: 0.7rem; font-weight: 700;">CURRENT</span>' : ''}
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.25rem;">
          ${pData.list.map(c => `
            <div style="font-size: 0.75rem; color: ${w && w.id === c.id ? '#7dd3fc' : 'var(--text-muted)'}; display: flex; justify-content: space-between;">
              <span>&bull; ${c.name}</span>
              <span style="font-size: 0.7rem; opacity: 0.8;">${c.action_label}</span>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  }

  html += `</div>`;
  content.innerHTML = html;
}

async function fetchBountyDataIfNeeded() {
  if (cachedBountyMetadata) return cachedBountyMetadata;
  try {
    const res = await fetch("/api/game/bounties");
    if (res.ok) {
      cachedBountyMetadata = await res.json();
    }
  } catch (e) {
    console.warn("Bounty fetch failed:", e);
  }
  return cachedBountyMetadata;
}

async function toggleBountyModal() {
  const modal = document.getElementById("bounty-modal");
  if (modal.style.display === "none") {
    await fetchBountyDataIfNeeded();
    renderBountyModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function renderBountyModalContent() {
  const content = document.getElementById("modal-bounty-content");
  if (!content) return;
  const meta = cachedBountyMetadata;
  const b = currentBountyData;
  const completedCount = (b && b.completed_count) || 0;
  const totalContracts = (b && b.total_contracts) || 10;
  const rankTitle = (b && b.rank_title) || "Novice Drifter";
  const acceptedCount = (b && b.accepted_count) || 0;
  const huntedCount = (b && b.hunted_count) || 0;

  let html = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--panel-border);">
      <div>
        <div style="font-weight: 700; color: #fff; font-size: 1rem;">Mercenary Contract Board</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);">Accept notices at regional gates or Central Bazaar. Track and claim rewards.</div>
      </div>
      <div style="text-align: right;">
        <span class="tag" style="background: rgba(239, 68, 68, 0.2); color: #f87171; font-weight: 700; font-size: 0.85rem;">
          ${rankTitle}
        </span>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">
          ${completedCount} / ${totalContracts} Completed &bull; ${huntedCount} Ready &bull; ${acceptedCount} Active
        </div>
      </div>
    </div>
  `;

  // Milestone Progress Bar
  const pct = Math.round((completedCount / totalContracts) * 100);
  html += `
    <div style="margin-bottom: 1.25rem;">
      <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">
        <span>Rank Milestones: 🗡️ 2 Hunter &bull; ⭐ 5 Lawkeeper &bull; 👑 10 Master</span>
        <span style="font-weight: 600; color: #f87171;">${pct}% Cleared</span>
      </div>
      <div style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
        <div style="height: 100%; width: ${pct}%; background: linear-gradient(90deg, #ef4444, #f59e0b); transition: width 0.3s ease;"></div>
      </div>
    </div>
  `;

  // Contracts list
  html += `
    <div style="display: flex; flex-direction: column; gap: 0.75rem;">
  `;

  const contractsMap = (b && b.contracts) || {};
  const allList = (meta && meta.contracts) || [];

  for (const c of allList) {
    const statusObj = contractsMap[c.id] || {};
    const isCompleted = statusObj.is_completed || false;
    const isHunted = statusObj.is_hunted || false;
    const isAccepted = statusObj.is_accepted || false;

    let badge = '<span class="tag" style="background: rgba(255,255,255,0.06); color: var(--text-muted); font-size: 0.7rem;">AVAILABLE AT BOARD</span>';
    let cardBorder = "var(--panel-border)";
    let bgStyle = "var(--bg-card)";

    if (isCompleted) {
      badge = '<span class="tag" style="background: rgba(63,185,80,0.25); color: #3fb950; font-weight: 700; font-size: 0.7rem;">✓ BOUNTY CLAIMED</span>';
      cardBorder = "rgba(63,185,80,0.4)";
    } else if (isHunted) {
      badge = '<span class="tag" style="background: rgba(234,179,8,0.25); color: #facc15; font-weight: 700; font-size: 0.7rem;">🎯 TARGET DEFEATED — CLAIM REWARD</span>';
      cardBorder = "rgba(234,179,8,0.5)";
      bgStyle = "rgba(234,179,8,0.03)";
    } else if (isAccepted) {
      badge = '<span class="tag" style="background: rgba(56,189,248,0.25); color: #38bdf8; font-weight: 700; font-size: 0.7rem;">⚔️ HUNT IN PROGRESS</span>';
      cardBorder = "rgba(56,189,248,0.4)";
    }

    html += `
      <div style="background: ${bgStyle}; border: 1px solid ${cardBorder}; border-radius: 6px; padding: 0.8rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.35rem; gap: 0.5rem; flex-wrap: wrap;">
          <div>
            <span style="font-weight: 700; color: #fff; font-size: 0.95rem;">${c.name}</span>
            <span style="font-size: 0.75rem; color: var(--text-muted); margin-left: 0.4rem;">&bull; ${c.province}</span>
          </div>
          ${badge}
        </div>
        <div style="font-size: 0.85rem; color: #d1d5db; margin-bottom: 0.5rem; line-height: 1.4;">${c.description}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; flex-wrap: wrap; gap: 0.4rem; padding-top: 0.4rem; border-top: 1px solid rgba(255,255,255,0.05);">
          <div>
            <span style="color: var(--text-muted);">Target Scene:</span> <code style="color: #7dd3fc;">${c.target_scene}</code>
            <span style="color: var(--text-muted); margin-left: 0.6rem;">Hub:</span> <code style="color: #cbd5e1;">${c.hub_scene}</code>
          </div>
          <div>
            <span style="color: var(--text-muted);">Bounty:</span>
            <span style="color: var(--gold); font-weight: 700;">${c.reward_silver} Silver</span>
            <span style="color: var(--text-muted); margin-left: 0.3rem;">+</span>
            <span class="tag" style="background: rgba(88,166,255,0.15); color: #58a6ff; font-size: 0.7rem;">${c.reward_item}</span>
            <span class="tag" style="background: rgba(239,68,68,0.15); color: #f87171; font-size: 0.7rem;">+${c.reputation_value} ${c.reputation_faction}</span>
          </div>
        </div>
      </div>
    `;
  }

  html += `</div>`;
  content.innerHTML = html;
}

async function fetchCompanionDataIfNeeded() {
  if (cachedCompanionMetadata) return cachedCompanionMetadata;
  try {
    const res = await fetch("/api/game/companions");
    if (res.ok) {
      cachedCompanionMetadata = await res.json();
    }
  } catch (e) {
    console.warn("Companion fetch failed:", e);
  }
  return cachedCompanionMetadata;
}

async function toggleCompanionModal() {
  const modal = document.getElementById("companion-modal");
  if (modal.style.display === "none") {
    await fetchCompanionDataIfNeeded();
    renderCompanionModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function renderCompanionModalContent() {
  const content = document.getElementById("modal-companion-content");
  if (!content) return;
  const meta = cachedCompanionMetadata;
  const cData = currentCompanionData;
  const recruitedCount = (cData && cData.recruited_count) || 0;
  const totalComps = (cData && cData.total_companions) || 5;
  const rankTitle = (cData && cData.rank_title) || "Lone Wanderer";
  const activeName = (cData && cData.active_companion_name) || "None";
  const activePerk = (cData && cData.active_companion_perk) || "None";

  let html = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--panel-border);">
      <div>
        <div style="font-weight: 700; color: #fff; font-size: 1rem;">Continental Warband Fellowship</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);">Recruit allies in garrison courtyards. Switch active follower at Central Bazaar or camps.</div>
      </div>
      <div style="text-align: right;">
        <span class="tag" style="background: rgba(192, 132, 252, 0.2); color: #d8b4fe; font-weight: 700; font-size: 0.85rem;">
          ${rankTitle}
        </span>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">
          Active: <span style="color: #58a6ff; font-weight: 600;">${activeName}</span> &bull; ${recruitedCount} / ${totalComps} Recruited
        </div>
      </div>
    </div>
  `;

  // Milestone Progress Bar
  const pct = Math.round((recruitedCount / totalComps) * 100);
  html += `
    <div style="margin-bottom: 1.25rem;">
      <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">
        <span>Fellowship Ranks: 🛡️ 1 Partner &bull; ⚔️ 3 Warband &bull; 👑 5 Master Fellowship</span>
        <span style="font-weight: 600; color: #c084fc;">${pct}% Warband Formed</span>
      </div>
      <div style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
        <div style="height: 100%; width: ${pct}%; background: linear-gradient(90deg, #c084fc, #38bdf8); transition: width 0.3s ease;"></div>
      </div>
    </div>
  `;

  // Companions list
  html += `<div style="display: flex; flex-direction: column; gap: 0.75rem;">`;

  const compsMap = (cData && cData.companions) || {};
  const allList = (meta && meta.companions) || [];

  for (const c of allList) {
    const statusObj = compsMap[c.id] || {};
    const isRecruited = statusObj.is_recruited || false;
    const isActive = statusObj.is_active || false;

    let badge = '<span class="tag" style="background: rgba(255,255,255,0.06); color: var(--text-muted); font-size: 0.7rem;">AVAILABLE IN PROVINCE</span>';
    let cardBorder = "var(--panel-border)";
    let bgStyle = "var(--bg-card)";

    if (isActive) {
      badge = '<span class="tag" style="background: rgba(56,189,248,0.25); color: #38bdf8; font-weight: 700; font-size: 0.7rem;">★ ACTIVE FOLLOWER</span>';
      cardBorder = "rgba(56,189,248,0.5)";
      bgStyle = "rgba(56,189,248,0.04)";
    } else if (isRecruited) {
      badge = '<span class="tag" style="background: rgba(63,185,80,0.25); color: #3fb950; font-weight: 700; font-size: 0.7rem;">✓ RECRUITED (IN RESERVE)</span>';
      cardBorder = "rgba(63,185,80,0.4)";
    }

    html += `
      <div style="background: ${bgStyle}; border: 1px solid ${cardBorder}; border-radius: 6px; padding: 0.8rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.35rem; gap: 0.5rem; flex-wrap: wrap;">
          <div>
            <span style="font-weight: 700; color: #fff; font-size: 0.95rem;">${c.name}</span>
            <span style="font-size: 0.8rem; color: #c084fc; margin-left: 0.4rem; font-weight: 600;">— ${c.title}</span>
            <span style="font-size: 0.75rem; color: var(--text-muted); margin-left: 0.4rem;">(${c.province})</span>
          </div>
          ${badge}
        </div>
        <div style="font-size: 0.85rem; color: #d1d5db; margin-bottom: 0.5rem; line-height: 1.4;">${c.description}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; flex-wrap: wrap; gap: 0.4rem; padding-top: 0.4rem; border-top: 1px solid rgba(255,255,255,0.05);">
          <div>
            <span style="color: var(--text-muted);">Home Garrison:</span> <code style="color: #cbd5e1;">${c.home_scene}</code>
          </div>
          <div>
            <span style="color: var(--text-muted);">Synergy Perk:</span>
            <span class="tag" style="background: rgba(192, 132, 252, 0.2); color: #d8b4fe; font-weight: 600; font-size: 0.7rem;">${c.perk_name}</span>
            <span style="color: var(--text-muted); margin-left: 0.3rem;">${c.perk_description}</span>
          </div>
        </div>
      </div>
    `;
  }

  html += `</div>`;
  content.innerHTML = html;
}

async function fetchBestiaryDataIfNeeded() {
  if (cachedBestiaryMetadata) return cachedBestiaryMetadata;
  try {
    const res = await fetch("/api/game/bestiary");
    if (res.ok) {
      cachedBestiaryMetadata = await res.json();
    }
  } catch (e) {
    console.warn("Bestiary fetch failed:", e);
  }
  return cachedBestiaryMetadata;
}

async function toggleBestiaryModal() {
  const modal = document.getElementById("bestiary-modal");
  if (modal.style.display === "none") {
    await fetchBestiaryDataIfNeeded();
    renderBestiaryModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function renderBestiaryModalContent() {
  const content = document.getElementById("modal-bestiary-content");
  if (!content) return;
  const meta = cachedBestiaryMetadata;
  const bData = currentBestiaryData;
  const huntedCount = (bData && bData.hunted_count) || 0;
  const studiedCount = (bData && bData.studied_count) || 0;
  const mountedCount = (bData && bData.mounted_count) || 0;
  const totalBeasts = (bData && bData.total_beasts) || 10;
  const rankTitle = (bData && bData.rank_title) || "Novice Trapper";

  let html = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--panel-border);">
      <div>
        <div style="font-weight: 700; color: #fff; font-size: 1rem;">Continental Apex Bestiary & Trophy Hall</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);">Track and defeat 10 legendary apex beasts. Mount harvested trophies in Central Bazaar.</div>
      </div>
      <div style="text-align: right;">
        <span class="tag" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; font-weight: 700; font-size: 0.85rem;">
          ${rankTitle}
        </span>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">
          ${huntedCount} / ${totalBeasts} Slain &bull; ${studiedCount} Studied &bull; ${mountedCount} Mounted
        </div>
      </div>
    </div>
  `;

  // Progress Bar
  const pct = Math.round((huntedCount / totalBeasts) * 100);
  html += `
    <div style="margin-bottom: 1.25rem;">
      <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">
        <span>Hunter Ranks: 🎯 1 Tracker &bull; 🏹 3 Apex Hunter &bull; ⚔️ 5 Grandmaster &bull; 👑 10 Apex Slayer</span>
        <span style="font-weight: 600; color: #fbbf24;">${pct}% Hunts Completed</span>
      </div>
      <div style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
        <div style="height: 100%; width: ${pct}%; background: linear-gradient(90deg, #f59e0b, #ef4444); transition: width 0.3s ease;"></div>
      </div>
    </div>
  `;

  // Beasts list
  html += `<div style="display: flex; flex-direction: column; gap: 0.75rem;">`;

  const beastsMap = (bData && bData.beasts) || {};
  const allList = (meta && meta.beasts) || [];

  for (const b of allList) {
    const statusObj = beastsMap[b.id] || {};
    const isStudied = statusObj.is_studied || false;
    const isHunted = statusObj.is_hunted || false;
    const isMounted = statusObj.is_mounted || false;
    const hasTrophy = statusObj.has_trophy || false;

    let badge = '<span class="tag" style="background: rgba(255,255,255,0.06); color: var(--text-muted); font-size: 0.7rem;">UNTRACKED</span>';
    let cardBorder = "var(--panel-border)";
    let bgStyle = "var(--bg-card)";

    if (isHunted) {
      const trophyTag = isMounted ? " (TROPHY MOUNTED)" : (hasTrophy ? " (TROPHY IN BAG)" : "");
      badge = `<span class="tag" style="background: rgba(245, 158, 11, 0.25); color: #fbbf24; font-weight: 700; font-size: 0.7rem;">🏆 SLAIN${trophyTag}</span>`;
      cardBorder = "rgba(245, 158, 11, 0.4)";
      bgStyle = "rgba(245, 158, 11, 0.04)";
    } else if (isStudied) {
      badge = '<span class="tag" style="background: rgba(56,189,248,0.25); color: #38bdf8; font-weight: 700; font-size: 0.7rem;">🔍 WEAKNESS STUDIED</span>';
      cardBorder = "rgba(56,189,248,0.35)";
    }

    html += `
      <div style="background: ${bgStyle}; border: 1px solid ${cardBorder}; border-radius: 6px; padding: 0.8rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.35rem; gap: 0.5rem; flex-wrap: wrap;">
          <div>
            <span style="font-weight: 700; color: #fff; font-size: 0.95rem;">${b.name}</span>
            <span style="font-size: 0.8rem; color: #fbbf24; margin-left: 0.4rem; font-weight: 600;">— ${b.title}</span>
            <span style="font-size: 0.75rem; color: var(--text-muted); margin-left: 0.4rem;">(${b.province})</span>
          </div>
          ${badge}
        </div>
        <div style="font-size: 0.85rem; color: #d1d5db; margin-bottom: 0.5rem; line-height: 1.4;">${b.description}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; flex-wrap: wrap; gap: 0.4rem; padding-top: 0.4rem; border-top: 1px solid rgba(255,255,255,0.05);">
          <div>
            <span style="color: var(--text-muted);">Lair:</span> <code style="color: #cbd5e1;">${b.lair_scene}</code>
            ${(isStudied || isHunted) ? `<span style="color: var(--text-muted); margin-left: 0.5rem;">Weakness:</span> <span style="color: #38bdf8;">${b.weakness}</span>` : ""}
          </div>
          <div>
            <span style="color: var(--text-muted);">Apex Trophy:</span>
            <span class="tag" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; font-weight: 600; font-size: 0.7rem;">${b.trophy_name}</span>
            <span style="color: var(--text-muted); margin-left: 0.3rem;">${b.trophy_perk}</span>
          </div>
        </div>
      </div>
    `;
  }

  html += `</div>`;
  content.innerHTML = html;
}

async function fetchSurvivalDataIfNeeded() {
  if (cachedSurvivalMetadata) return cachedSurvivalMetadata;
  try {
    const res = await fetch("/api/game/survival");
    if (res.ok) {
      cachedSurvivalMetadata = await res.json();
    }
  } catch (e) {
    console.warn("Survival fetch failed:", e);
  }
  return cachedSurvivalMetadata;
}

async function toggleSurvivalModal() {
  const modal = document.getElementById("survival-modal");
  if (modal.style.display === "none") {
    await fetchSurvivalDataIfNeeded();
    renderSurvivalModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function renderSurvivalModalContent() {
  const content = document.getElementById("modal-survival-content");
  if (!content) return;
  const meta = cachedSurvivalMetadata;
  const sData = currentSurvivalData;
  const foragedCount = (sData && sData.foraged_count) || 0;
  const totalSpots = (sData && sData.total_spots) || 15;
  const mealsCooked = (sData && sData.meals_cooked) || 0;
  const rankTitle = (sData && sData.rank_title) || "Trail Wanderer";

  let html = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--panel-border);">
      <div>
        <div style="font-weight: 700; color: #fff; font-size: 1rem;">Continental Survival Camp & Wilderness Rations</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);">Forage wild ingredients across 15 sites. Cook field rations at hearths to fortify health and stamina.</div>
      </div>
      <div style="text-align: right;">
        <span class="tag" style="background: rgba(34, 197, 94, 0.2); color: #4ade80; font-weight: 700; font-size: 0.85rem;">
          ${rankTitle}
        </span>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">
          ${mealsCooked} Meals Cooked &bull; ${foragedCount} / ${totalSpots} Sites Foraged
        </div>
      </div>
    </div>
  `;

  // Recipes section
  html += `
    <div style="margin-bottom: 1.25rem;">
      <h4 style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;">Survival Cooking Recipes (Hearth & Campfire)</h4>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 0.75rem;">
  `;

  const recipesMap = (sData && sData.recipes) || {};
  const allRecipes = (meta && meta.recipes) || [];

  for (const r of allRecipes) {
    const rStatus = recipesMap[r.id] || {};
    const canCook = rStatus.can_cook || false;
    const countHeld = rStatus.count_held || 0;

    let cardBorder = "var(--panel-border)";
    let bgStyle = "var(--bg-card)";
    let badge = `<span class="tag" style="background: rgba(255,255,255,0.06); color: var(--text-muted); font-size: 0.7rem;">NEEDS INGREDIENTS</span>`;

    if (countHeld > 0) {
      badge = `<span class="tag" style="background: rgba(34, 197, 94, 0.25); color: #4ade80; font-weight: 700; font-size: 0.7rem;">🎒 ${countHeld} IN PACK</span>`;
      cardBorder = "rgba(34, 197, 94, 0.4)";
      bgStyle = "rgba(34, 197, 94, 0.04)";
    } else if (canCook) {
      badge = `<span class="tag" style="background: rgba(56, 189, 248, 0.25); color: #38bdf8; font-weight: 700; font-size: 0.7rem;">READY TO COOK</span>`;
      cardBorder = "rgba(56, 189, 248, 0.35)";
    }

    const ingPills = r.required_ingredients.map(ing => `<code style="font-size: 0.75rem; color: #cbd5e1; background: rgba(255,255,255,0.06); padding: 0.1rem 0.3rem; border-radius: 3px;">${ing.replace(/^foraged_/, '').replace(/_/g, ' ')}</code>`).join(" ");

    html += `
      <div style="background: ${bgStyle}; border: 1px solid ${cardBorder}; border-radius: 6px; padding: 0.8rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.35rem; gap: 0.5rem;">
          <div>
            <span style="font-weight: 700; color: #fff; font-size: 0.95rem;">${r.name}</span>
            <span style="font-size: 0.75rem; color: var(--text-muted); margin-left: 0.4rem;">(${r.province})</span>
          </div>
          ${badge}
        </div>
        <div style="font-size: 0.82rem; color: #d1d5db; margin-bottom: 0.45rem;">${r.description}</div>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.35rem;">
          Ingredients: ${ingPills}
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #38bdf8; padding-top: 0.35rem; border-top: 1px solid rgba(255,255,255,0.05);">
          <span>Recovery: +${r.stamina_restored} SP &bull; +${r.health_restored} HP</span>
          ${r.granted_marker ? `<span style="color: #c084fc;">Perk: ${r.granted_marker}</span>` : ""}
        </div>
      </div>
    `;
  }
  html += `</div></div>`;

  // Foraging sites section
  html += `
    <div>
      <h4 style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;">Wilderness Foraging Spots (15 Continental Gateways)</h4>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.5rem;">
  `;

  const allSpots = (meta && meta.spots) || [];
  for (const s of allSpots) {
    const isHarvested = (gameState && gameState.world_flags && gameState.world_flags[\`survival_foraged_\${s.scene_id}\`]);
    const statusBadge = isHarvested
      ? `<span class="tag" style="background: rgba(34, 197, 94, 0.2); color: #4ade80; font-size: 0.7rem;">HARVESTED</span>`
      : `<span class="tag" style="background: rgba(255,255,255,0.06); color: var(--text-muted); font-size: 0.7rem;">UNHARVESTED</span>`;

    html += `
      <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--panel-border); border-radius: 4px; padding: 0.6rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
          <span style="font-weight: 600; font-size: 0.8rem; color: #fff;">${s.ingredient_name}</span>
          ${statusBadge}
        </div>
        <div style="font-size: 0.75rem; color: var(--text-muted);">${s.province}</div>
        <code style="font-size: 0.7rem; color: #94a3b8;">${s.scene_id}</code>
      </div>
    `;
  }

  html += `</div></div>`;
  content.innerHTML = html;
}

async function fetchOrdersDataIfNeeded() {
  if (cachedOrdersMetadata) return cachedOrdersMetadata;
  try {
    const res = await fetch("/api/game/orders");
    if (res.ok) {
      cachedOrdersMetadata = await res.json();
    }
  } catch (e) {
    console.warn("Orders fetch failed:", e);
  }
  return cachedOrdersMetadata;
}

async function toggleOrdersModal() {
  const modal = document.getElementById("orders-modal");
  if (modal.style.display === "none") {
    await fetchOrdersDataIfNeeded();
    renderOrdersModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function renderOrdersModalContent() {
  const content = document.getElementById("modal-orders-content");
  if (!content) return;
  const meta = cachedOrdersMetadata;
  const oData = currentOrdersData;
  const pledgedCount = (oData && oData.pledged_count) || 0;
  const totalOrders = (oData && oData.total_orders) || 5;
  const bannersHeld = (oData && oData.banners_held) || 0;
  const rankTitle = (oData && oData.rank_title) || "Unsworn Wayfarer";
  const activeMarker = (oData && oData.active_banner_marker) || null;

  let html = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--panel-border);">
      <div>
        <div style="font-weight: 700; color: #fff; font-size: 1rem;">Provincial Faction Heraldry & Renown Orders</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);">Swear fealty at provincial council sanctums, claim war banners, and assert sovereignty across the realms.</div>
      </div>
      <div style="text-align: right;">
        <span class="tag" style="background: rgba(168, 85, 247, 0.25); color: #c084fc; font-weight: 700; font-size: 0.85rem;">
          ${rankTitle}
        </span>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">
          ${bannersHeld} / ${totalOrders} Banners Claimed &bull; ${pledgedCount} Oaths Sworn
        </div>
      </div>
    </div>
  `;

  if (activeMarker) {
    html += `
      <div style="background: rgba(168, 85, 247, 0.12); border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 6px; padding: 0.6rem 0.9rem; margin-bottom: 1rem; font-size: 0.85rem;">
        <span style="color: #c084fc; font-weight: 700;">🚩 Active War Banner Raised:</span>
        <span style="color: #fff; margin-left: 0.4rem;">${activeMarker}</span>
      </div>
    `;
  }

  const pct = Math.round((bannersHeld / totalOrders) * 100);
  html += `
    <div style="margin-bottom: 1.25rem;">
      <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">
        <span>Order Ranks: 🗡️ 1 Knight-Errant &bull; 🚩 2 Banneret &bull; 🛡️ 3 Commander &bull; ⚔️ 4 Marshal &bull; 👑 5 Grandmaster</span>
        <span style="font-weight: 600; color: #c084fc;">${pct}% Banners Held</span>
      </div>
      <div style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
        <div style="height: 100%; width: ${pct}%; background: linear-gradient(90deg, #8b5cf6, #ec4899); transition: width 0.3s ease;"></div>
      </div>
    </div>
  `;

  html += `<div style="display: flex; flex-direction: column; gap: 0.75rem;">`;

  const ordersMap = (oData && oData.orders) || {};
  const allOrders = (meta && meta.orders) || [];

  for (const o of allOrders) {
    const oStatus = ordersMap[o.id] || {};
    const isPledged = oStatus.is_pledged || false;
    const hasBanner = oStatus.has_banner || false;
    const isRaised = oStatus.is_raised || false;

    let badge = '<span class="tag" style="background: rgba(255,255,255,0.06); color: var(--text-muted); font-size: 0.7rem;">UNSWORN</span>';
    let cardBorder = "var(--panel-border)";
    let bgStyle = "var(--bg-card)";

    if (isRaised) {
      badge = '<span class="tag" style="background: rgba(168, 85, 247, 0.3); color: #e2baff; font-weight: 700; font-size: 0.7rem; border: 1px solid #c084fc;">🚩 BANNER RAISED</span>';
      cardBorder = "rgba(168, 85, 247, 0.5)";
      bgStyle = "rgba(168, 85, 247, 0.05)";
    } else if (hasBanner) {
      badge = '<span class="tag" style="background: rgba(34, 197, 94, 0.25); color: #4ade80; font-weight: 700; font-size: 0.7rem;">🎒 BANNER IN PACK</span>';
      cardBorder = "rgba(34, 197, 94, 0.4)";
    } else if (isPledged) {
      badge = '<span class="tag" style="background: rgba(56, 189, 248, 0.25); color: #38bdf8; font-weight: 700; font-size: 0.7rem;">FEALTY SWORN</span>';
      cardBorder = "rgba(56, 189, 248, 0.35)";
    }

    html += `
      <div style="background: ${bgStyle}; border: 1px solid ${cardBorder}; border-radius: 6px; padding: 0.8rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.35rem; gap: 0.5rem; flex-wrap: wrap;">
          <div>
            <span style="font-size: 1.1rem; margin-right: 0.3rem;">${o.crest_icon}</span>
            <span style="font-weight: 700; color: #fff; font-size: 0.95rem;">${o.name}</span>
            <span style="font-size: 0.8rem; color: #a78bfa; margin-left: 0.4rem; font-weight: 600;">(${o.province})</span>
          </div>
          ${badge}
        </div>
        <div style="font-size: 0.85rem; color: #d1d5db; margin-bottom: 0.5rem; line-height: 1.4;">${o.description}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; flex-wrap: wrap; gap: 0.4rem; padding-top: 0.4rem; border-top: 1px solid rgba(255,255,255,0.05);">
          <div>
            <span style="color: var(--text-muted);">Sanctum:</span> <code style="color: #cbd5e1;">${o.sanctum_scene}</code>
            <span style="color: var(--text-muted); margin-left: 0.5rem;">Requirements:</span>
            <span style="color: #58a6ff;">+${o.reputation_req} Rep</span> or
            <span style="color: #3fb950;">${o.alternate_attribute.toUpperCase()} >= ${o.alternate_attr_val}</span> or
            <span style="color: #c084fc;">${o.alternate_trait}</span>
          </div>
          <div>
            <span style="color: var(--text-muted);">War Banner:</span>
            <span class="tag" style="background: rgba(168, 85, 247, 0.2); color: #c084fc; font-weight: 600; font-size: 0.7rem;">${o.banner_name}</span>
            <span style="color: #38bdf8; margin-left: 0.3rem;">Perk: ${o.granted_marker}</span>
          </div>
        </div>
      </div>
    `;
  }

  html += `</div>`;
  content.innerHTML = html;
}

async function fetchShrinesDataIfNeeded() {
  if (cachedShrinesMetadata) return cachedShrinesMetadata;
  try {
    const res = await fetch("/api/game/shrines");
    if (res.ok) {
      cachedShrinesMetadata = await res.json();
    }
  } catch (e) {
    console.warn("Shrines fetch failed:", e);
  }
  return cachedShrinesMetadata;
}

async function toggleShrinesModal() {
  const modal = document.getElementById("shrines-modal");
  if (modal.style.display === "none") {
    await fetchShrinesDataIfNeeded();
    renderShrinesModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function renderShrinesModalContent() {
  const content = document.getElementById("modal-shrines-content");
  if (!content) return;
  const meta = cachedShrinesMetadata;
  const sData = currentShrinesData;
  const consecratedCount = (sData && sData.consecrated_count) || 0;
  const totalShrines = (sData && sData.total_shrines) || 6;
  const pilgrimRank = (sData && sData.pilgrim_rank) || "Unanointed Wanderer";
  const activeBlessings = (sData && sData.active_blessings_count) || 0;
  const activeAuras = (sData && sData.active_auras_count) || 0;

  let html = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--panel-border);">
      <div>
        <div style="font-weight: 700; color: #fff; font-size: 1rem;">Continental Ancient Shrines & Titan Blessings</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);">Consecrate sacred elemental altars, receive titan blessings, and invoke celestial favors across the continent.</div>
      </div>
      <div style="text-align: right;">
        <span class="tag" style="background: rgba(245, 158, 11, 0.25); color: #fbbf24; font-weight: 700; font-size: 0.85rem;">
          ✨ ${pilgrimRank}
        </span>
        <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">
          ${consecratedCount} / ${totalShrines} Consecrated &bull; ${activeBlessings} Blessings Held
        </div>
      </div>
    </div>
  `;

  if (activeAuras > 0) {
    html += `
      <div style="background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 6px; padding: 0.6rem 0.9rem; margin-bottom: 1rem; font-size: 0.85rem;">
        <span style="color: #fbbf24; font-weight: 700;">🌟 Active Titan Invocations:</span>
        <span style="color: #fff; margin-left: 0.4rem;">${activeAuras} Celestial Aura(s) Empowering Character</span>
      </div>
    `;
  }

  const pct = Math.round((consecratedCount / totalShrines) * 100);
  html += `
    <div style="margin-bottom: 1.25rem;">
      <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.3rem;">
        <span>Pilgrim Ranks: 1 Pilgrim &bull; 2 Devotee &bull; 3 Hierophant &bull; 4 Exarch &bull; 5 Hierarch &bull; 6 Avatar</span>
        <span style="font-weight: 600; color: #fbbf24;">${pct}% Pantheon Consecrated</span>
      </div>
      <div style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden;">
        <div style="height: 100%; width: ${pct}%; background: linear-gradient(90deg, #f59e0b, #10b981); transition: width 0.3s ease;"></div>
      </div>
    </div>
  `;

  html += `<div style="display: flex; flex-direction: column; gap: 0.75rem;">`;

  const shrinesList = (sData && sData.shrines) || (meta && meta.shrines) || [];

  for (const s of shrinesList) {
    const isConsecrated = s.is_consecrated || false;
    const hasBlessing = s.has_blessing || false;
    const isInvoked = s.is_invoked || false;
    const isAuraActive = s.is_aura_active || false;

    let badge = '<span class="tag" style="background: rgba(255,255,255,0.06); color: var(--text-muted); font-size: 0.7rem;">UNCONSECRATED</span>';
    let cardBorder = "var(--panel-border)";
    let bgStyle = "var(--bg-card)";

    if (isAuraActive) {
      badge = '<span class="tag" style="background: rgba(245, 158, 11, 0.3); color: #fde68a; font-weight: 700; font-size: 0.7rem; border: 1px solid #f59e0b;">🌟 AURA ACTIVE</span>';
      cardBorder = "rgba(245, 158, 11, 0.5)";
      bgStyle = "rgba(245, 158, 11, 0.05)";
    } else if (isInvoked) {
      badge = '<span class="tag" style="background: rgba(148, 163, 184, 0.2); color: #cbd5e1; font-weight: 600; font-size: 0.7rem;">⚡ INVOKED (RENEW AT SHRINE)</span>';
      cardBorder = "rgba(148, 163, 184, 0.3)";
    } else if (hasBlessing) {
      badge = '<span class="tag" style="background: rgba(34, 197, 94, 0.25); color: #4ade80; font-weight: 700; font-size: 0.7rem;">✨ BLESSING READY</span>';
      cardBorder = "rgba(34, 197, 94, 0.4)";
    } else if (isConsecrated) {
      badge = '<span class="tag" style="background: rgba(56, 189, 248, 0.25); color: #38bdf8; font-weight: 700; font-size: 0.7rem;">CONSECRATED</span>';
      cardBorder = "rgba(56, 189, 248, 0.35)";
    }

    html += `
      <div style="background: ${bgStyle}; border: 1px solid ${cardBorder}; border-radius: 6px; padding: 0.8rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.35rem; gap: 0.5rem; flex-wrap: wrap;">
          <div>
            <span style="font-size: 1.1rem; margin-right: 0.3rem;">${s.icon}</span>
            <span style="font-weight: 700; color: #fff; font-size: 0.95rem;">${s.name}</span>
            <span style="font-size: 0.8rem; color: #fbbf24; margin-left: 0.4rem; font-weight: 600;">(${s.province})</span>
          </div>
          ${badge}
        </div>
        <div style="font-size: 0.85rem; color: #d1d5db; margin-bottom: 0.5rem; line-height: 1.4;">${s.description}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; flex-wrap: wrap; gap: 0.4rem; padding-top: 0.4rem; border-top: 1px solid rgba(255,255,255,0.05);">
          <div>
            <span style="color: var(--text-muted);">Deity:</span> <span style="color: #fff; font-weight: 600;">${s.deity}</span>
            <span style="color: var(--text-muted); margin-left: 0.5rem;">Sanctum:</span> <code style="color: #cbd5e1;">${s.sanctum_scene}</code>
            <span style="color: var(--text-muted); margin-left: 0.5rem;">Domain:</span> <span style="color: #38bdf8;">${s.domain}</span>
          </div>
          <div>
            <span style="color: var(--text-muted);">Blessing:</span>
            <span class="tag" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; font-weight: 600; font-size: 0.7rem;">${s.blessing_name}</span>
            <span style="color: #34d399; margin-left: 0.3rem;">Aura: ${s.aura_marker}</span>
          </div>
        </div>
      </div>
    `;
  }

  html += `</div>`;
  content.innerHTML = html;
}

function toggleMapModal() {
  const modal = document.getElementById("map-modal");
  if (modal.style.display === "none") {
    const currRegion = (lastObservation && lastObservation.region_id) || (gameState && gameState.current_region) || "";
    for (const [k, p] of Object.entries(PROVINCES_MAP_DATA)) {
      if (p.regions.includes(currRegion)) {
        selectedMapProvince = k;
        break;
      }
    }
    if (!selectedMapProvince) selectedMapProvince = "province_reach";
    renderMapModalContent();
    modal.style.display = "flex";
  } else {
    modal.style.display = "none";
  }
}

function selectProvinceMap(provKey) {
  selectedMapProvince = provKey;
  renderMapModalContent();
}

function renderMapModalContent() {
  const content = document.getElementById("modal-map-content");
  if (!content) return;
  const currRegion = (lastObservation && lastObservation.region_id) || (gameState && gameState.current_region) || "";

  let cardsHtml = Object.entries(PROVINCES_MAP_DATA).map(([k, p]) => {
    const isPlayerHere = p.regions.includes(currRegion);
    const isSelected = selectedMapProvince === k;
    let cardClass = "map-card";
    if (isPlayerHere) cardClass += " active-region";
    if (isSelected) cardClass += " selected-province";

    const beacon = isPlayerHere ? '<span class="pulse-beacon"></span>' : '';
    const hereBadge = isPlayerHere ? '<span class="tag" style="background: rgba(63,185,80,0.25); color: #3fb950; font-weight: 600; font-size: 0.7rem;">YOU ARE HERE</span>' : '';

    return `
      <div class="${cardClass}" onclick="selectProvinceMap('${k}')">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
          <div style="font-weight: 700; font-size: 0.95rem; color: #fff;">${beacon}${p.icon} ${p.name}</div>
          ${hereBadge}
        </div>
        <div style="font-size: 0.75rem; color: var(--text-muted);">${p.theme}</div>
      </div>
    `;
  }).join("");

  const activeProv = PROVINCES_MAP_DATA[selectedMapProvince] || PROVINCES_MAP_DATA["province_reach"];
  const isPlayerHere = activeProv.regions.includes(currRegion);
  const connPills = activeProv.connections.map(c => `<span class="tag" style="background: rgba(255,255,255,0.06); font-size: 0.75rem;">${c}</span>`).join("");

  content.innerHTML = `
    <div style="margin-bottom: 1rem;">
      <h4 style="font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;">Select Territory to Inspect</h4>
      <div class="map-grid">${cardsHtml}</div>
    </div>
    <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--panel-border); border-radius: 8px; padding: 1.25rem;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
        <div style="font-size: 1.2rem; font-weight: 700; color: #fff;">${activeProv.icon} ${activeProv.name}</div>
        ${isPlayerHere ? '<span class="tag" style="background: rgba(63,185,80,0.25); color: #3fb950; font-weight: 600;">ACTIVE LOCATION</span>' : ''}
      </div>
      <p style="font-size: 0.9rem; color: var(--text); margin-bottom: 0.75rem;">${activeProv.desc}</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.75rem; margin-bottom: 0.75rem;">
        <div class="stat-box">
          <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Regional Mechanic</div>
          <div style="font-size: 0.9rem; font-weight: 600; color: #58a6ff; margin-top: 0.2rem;">${activeProv.mechanic}</div>
        </div>
        <div class="stat-box">
          <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Environmental Hazards</div>
          <div style="font-size: 0.9rem; font-weight: 600; color: #f85149; margin-top: 0.2rem;">${activeProv.hazards}</div>
        </div>
      </div>
      <div>
        <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; margin-right: 0.4rem;">Direct Transit Connections:</span>
        <span class="tag-row" style="display: inline-flex;">${connPills}</span>
      </div>
      <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid var(--panel-border);">
        <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.4rem;">Chartered Fast-Travel Network</div>
        <div style="display: flex; gap: 0.4rem; flex-wrap: wrap;">
          <span class="tag" style="background: rgba(56,189,248,0.15); color: #38bdf8; font-size: 0.75rem;">🚠 Highland Cable Lift</span>
          <span class="tag" style="background: rgba(56,189,248,0.15); color: #38bdf8; font-size: 0.75rem;">⛵ Canal River Barge</span>
          <span class="tag" style="background: rgba(56,189,248,0.15); color: #38bdf8; font-size: 0.75rem;">🏜️ Desert Silt-Skiff</span>
          <span class="tag" style="background: rgba(56,189,248,0.15); color: #38bdf8; font-size: 0.75rem;">🎠 Imperial High Carriage</span>
          <span class="tag" style="background: rgba(56,189,248,0.15); color: #38bdf8; font-size: 0.75rem;">🤿 Submersible Siphon Ferry</span>
        </div>
      </div>
    </div>
  `;
}

function resetToSelect() {
  document.getElementById("play-view").style.display = "none";
  document.getElementById("select-view").style.display = "block";
  renderPresetCards();
  checkResumeSession();
}

window.addEventListener("keydown", (e) => {
  if (["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) return;
  if (document.getElementById("play-view").style.display !== "block") return;

  if (e.key === "Escape") {
    document.getElementById("sheet-modal").style.display = "none";
    document.getElementById("replay-modal").style.display = "none";
    document.getElementById("quest-modal").style.display = "none";
    document.getElementById("codex-modal").style.display = "none";
    document.getElementById("trade-modal").style.display = "none";
    document.getElementById("weather-modal").style.display = "none";
    document.getElementById("bounty-modal").style.display = "none";
    document.getElementById("companion-modal").style.display = "none";
    document.getElementById("bestiary-modal").style.display = "none";
    document.getElementById("survival-modal").style.display = "none";
    document.getElementById("orders-modal").style.display = "none";
    document.getElementById("shrines-modal").style.display = "none";
    document.getElementById("map-modal").style.display = "none";
    return;
  }
  if (e.key.toLowerCase() === "u") {
    undoTurn();
    return;
  }
  if (e.key.toLowerCase() === "c") {
    toggleSheetModal();
    return;
  }
  if (e.key.toLowerCase() === "q") {
    toggleQuestModal();
    return;
  }
  if (e.key.toLowerCase() === "x") {
    toggleCodexModal();
    return;
  }
  if (e.key.toLowerCase() === "t") {
    toggleTradeModal();
    return;
  }
  if (e.key.toLowerCase() === "w") {
    toggleWeatherModal();
    return;
  }
  if (e.key.toLowerCase() === "b") {
    toggleBountyModal();
    return;
  }
  if (e.key.toLowerCase() === "p") {
    toggleCompanionModal();
    return;
  }
  if (e.key.toLowerCase() === "h") {
    toggleBestiaryModal();
    return;
  }
  if (e.key.toLowerCase() === "k") {
    toggleSurvivalModal();
    return;
  }
  if (e.key.toLowerCase() === "o") {
    toggleOrdersModal();
    return;
  }
  if (e.key.toLowerCase() === "g") {
    toggleShrinesModal();
    return;
  }
  if (e.key.toLowerCase() === "m") {
    toggleMapModal();
    return;
  }
  if (e.key >= "1" && e.key <= "9") {
    const idx = parseInt(e.key, 10) - 1;
    const btns = document.querySelectorAll("#actions-container .action-btn");
    if (btns[idx] && !btns[idx].disabled) {
      btns[idx].click();
    }
  }
});

window.addEventListener("DOMContentLoaded", () => {
  renderPresetCards();
  checkResumeSession();
});
</script>
</body>
</html>
"""

_HEALTH_RESPONSE_BYTES = json.dumps(
    {"service": "adventure-forge", "status": "ok", "version": __version__},
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_PLAYABLE_HTML_BYTES = _PLAYABLE_HTML.encode("utf-8")
_PRESETS_RESPONSE_BYTES = json.dumps(
    {"presets": {k: v.to_dict() for k, v in CHARACTER_PRESETS.items() if k != "pit_fighter"}},
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_QUESTS_RESPONSE_BYTES = json.dumps(
    {
        "campaign": get_continental_main_quest().to_dict(),
        "subquests": {k: v.to_dict() for k, v in get_provincial_subquests().items()},
        "intrigue_quests": {k: v.to_dict() for k, v in get_faction_intrigue_quests().items()},
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_HAZARDS_RESPONSE_BYTES = json.dumps(
    {"hazards": {k: v.to_dict() for k, v in HAZARD_COMBOS.items()}},
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_CODEX_RESPONSE_BYTES = json.dumps(
    {
        "total_entries": len(CODEX_ENTRIES),
        "masteries": PROVINCIAL_MASTERIES,
        "entries": [entry.to_dict(unlocked=False) for entry in CODEX_ENTRIES.values()],
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_TRANSIT_RESPONSE_BYTES = json.dumps(
    {
        "total_routes": len(CHARTERED_ROUTES),
        "routes": [r.to_dict(traveled=False) for r in CHARTERED_ROUTES],
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_TRADE_RESPONSE_BYTES = json.dumps(
    {
        "total_commodities": len(COMMODITIES),
        "commodities": [
            {
                "id": c.id,
                "name": c.name,
                "origin_province": c.origin_province,
                "origin_scene": c.origin_scene,
                "description": c.description,
                "base_buy_price": c.base_buy_price,
                "base_sell_price": c.base_sell_price,
                "import_bonuses": c.import_bonuses,
                "barter_item": c.barter_item,
            }
            for c in COMMODITIES.values()
        ],
        "hubs": {
            k: {
                "hub_name": v["hub_name"],
                "factor_title": v["factor_title"],
                "available_commodities": v["available_commodities"],
            }
            for k, v in TRADE_HUBS.items()
        },
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_WEATHER_RESPONSE_BYTES = json.dumps(
    {
        "total_conditions": len(WEATHER_CONDITIONS),
        "conditions": [w.to_dict() for w in WEATHER_CONDITIONS.values()],
        "forecast": get_all_provincial_weather(0),
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_BOUNTY_RESPONSE_BYTES = json.dumps(
    {
        "total_contracts": len(BOUNTY_CONTRACTS),
        "contracts": [c.to_dict() for c in BOUNTY_CONTRACTS.values()],
        "hubs": BOUNTY_HUBS,
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_COMPANION_RESPONSE_BYTES = json.dumps(
    {
        "total_companions": len(COMPANIONS),
        "companions": [c.to_dict() for c in COMPANIONS.values()],
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_BESTIARY_RESPONSE_BYTES = json.dumps(
    {
        "total_beasts": len(APEX_BEASTS),
        "beasts": [b.to_dict() for b in APEX_BEASTS.values()],
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_SURVIVAL_RESPONSE_BYTES = json.dumps(
    {
        "total_spots": len(FORAGING_SPOTS),
        "spots": [s.to_dict() for s in FORAGING_SPOTS.values()],
        "total_recipes": len(COOKING_RECIPES),
        "recipes": [r.to_dict() for r in COOKING_RECIPES.values()],
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_ORDERS_RESPONSE_BYTES = json.dumps(
    {
        "total_orders": len(FACTION_ORDERS),
        "orders": [o.to_dict() for o in FACTION_ORDERS.values()],
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_SHRINES_RESPONSE_BYTES = json.dumps(
    {
        "total_shrines": len(ANCIENT_SHRINES),
        "shrines": [s.to_dict() for s in ANCIENT_SHRINES.values()],
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")


async def app(scope: dict[str, Any], receive: Receive, send: Send) -> None:
    """Serve the landing page, health check, REST game API, and MCP JSON-RPC endpoint."""
    start_time = time.perf_counter()

    async def _send_response(
        send_fn: Send,
        *,
        status: int,
        body: bytes,
        content_type: bytes,
        include_body: bool = True,
    ) -> None:
        dur = (time.perf_counter() - start_time) * 1000.0
        await _send_response_impl(
            send_fn,
            status=status,
            body=body,
            content_type=content_type,
            include_body=include_body,
            duration_ms=dur,
        )

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
    path = _extract_path(scope)
    include_body = method != "HEAD"

    # Handle CORS preflight
    if method == "OPTIONS":
        await _send_response(
            send,
            status=200,
            body=b"",
            content_type=b"text/plain; charset=utf-8",
            include_body=False,
        )
        return

    # Route: /health (only GET and HEAD permitted)
    if path == "/health":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_HEALTH_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: / (Interactive Playable Landing Page)
    if path == "/":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_PLAYABLE_HTML_BYTES,
            content_type=b"text/html; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/presets
    if path == "/api/game/presets":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_PRESETS_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/quests
    if path == "/api/game/quests":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_QUESTS_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/hazards
    if path == "/api/game/hazards":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_HAZARDS_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/codex
    if path == "/api/game/codex":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_CODEX_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/transit
    if path == "/api/game/transit":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_TRANSIT_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/trade
    if path == "/api/game/trade":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_TRADE_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/weather
    if path == "/api/game/weather":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_WEATHER_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/bounties
    if path == "/api/game/bounties":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_BOUNTY_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/companions
    if path == "/api/game/companions":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_COMPANION_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/bestiary
    if path == "/api/game/bestiary":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_BESTIARY_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/survival
    if path == "/api/game/survival":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_SURVIVAL_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/orders
    if path == "/api/game/orders":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_ORDERS_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/shrines
    if path == "/api/game/shrines":
        if method not in {"GET", "HEAD"}:
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=200,
            body=_SHRINES_RESPONSE_BYTES,
            content_type=b"application/json; charset=utf-8",
            include_body=include_body,
        )
        return

    # Route: /api/game/new (Pure stateless start)
    if path == "/api/game/new":
        if method != "POST":
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        raw_body = await _read_body(receive)
        try:
            req_data = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except json.JSONDecodeError:
            req_data = {}

        preset_name = str(req_data.get("preset", "cutpurse"))
        seed = req_data.get("seed")
        try:
            preset = get_preset(preset_name)
        except KeyError:
            preset = get_preset("cutpurse")

        effective_seed = int(seed) if isinstance(seed, (int, float)) else 42
        state = GameState(
            build_id="af-build-001",
            session_id=f"web-{preset.id}-{effective_seed}",
            character=preset.character,
            current_region=preset.start_region,
            current_scene=preset.start_scene,
            rng=DeterministicRNG.from_seed(effective_seed),
        )
        obs = _ENGINE.observe(state)
        response_data = {
            "success": True,
            "observation": sanitize_observation(obs),
            "character": state.character.to_dict(),
            "state": state.to_dict(),
            "quest": _ENGINE.get_quest_progress(state),
            "codex": _ENGINE.get_codex_progress(state),
            "transit": _ENGINE.get_transit_progress(state),
            "trade": _ENGINE.get_trade_progress(state),
            "weather": _ENGINE.get_weather_state(state),
            "bounty": _ENGINE.get_bounty_progress(state),
            "companion": _ENGINE.get_companion_progress(state),
            "bestiary": _ENGINE.get_bestiary_progress(state),
            "survival": _ENGINE.get_survival_progress(state),
            "orders": _ENGINE.get_orders_progress(state),
            "shrines": _ENGINE.get_shrines_progress(state),
        }
        await _send_response(
            send,
            status=200,
            body=_json_response(response_data),
            content_type=b"application/json; charset=utf-8",
        )
        return

    # Route: /api/game/step (Pure stateless step)
    if path == "/api/game/step":
        if method != "POST":
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        raw_body = await _read_body(receive)
        try:
            req_data = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except json.JSONDecodeError as exc:
            await _send_response(
                send,
                status=400,
                body=_json_response({"error": f"Invalid JSON: {exc}"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        state_dict = req_data.get("state")
        action_id = req_data.get("action_id")
        if not state_dict or not action_id:
            await _send_response(
                send,
                status=400,
                body=_json_response({"error": "Missing 'state' or 'action_id'"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        try:
            state = GameState.from_dict(state_dict)
            new_state, obs = _ENGINE.step(state, str(action_id))
        except Exception as exc:
            await _send_response(
                send,
                status=400,
                body=_json_response({"error": f"Failed to execute step: {exc}"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        response_data = {
            "success": obs.success,
            "observation": sanitize_observation(obs),
            "character": new_state.character.to_dict(),
            "state": new_state.to_dict(),
            "quest": _ENGINE.get_quest_progress(new_state),
            "codex": _ENGINE.get_codex_progress(new_state),
            "transit": _ENGINE.get_transit_progress(new_state),
            "trade": _ENGINE.get_trade_progress(new_state),
            "weather": _ENGINE.get_weather_state(new_state),
            "bounty": _ENGINE.get_bounty_progress(new_state),
            "companion": _ENGINE.get_companion_progress(new_state),
            "bestiary": _ENGINE.get_bestiary_progress(new_state),
            "survival": _ENGINE.get_survival_progress(new_state),
            "orders": _ENGINE.get_orders_progress(new_state),
            "shrines": _ENGINE.get_shrines_progress(new_state),
        }
        await _send_response(
            send,
            status=200,
            body=_json_response(response_data),
            content_type=b"application/json; charset=utf-8",
        )
        return

    # Route: /api/game/observe (Pure stateless observe)
    if path == "/api/game/observe":
        if method != "POST":
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        raw_body = await _read_body(receive)
        try:
            req_data = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except json.JSONDecodeError as exc:
            await _send_response(
                send,
                status=400,
                body=_json_response({"error": f"Invalid JSON: {exc}"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        state_dict = req_data.get("state")
        if not state_dict:
            await _send_response(
                send,
                status=400,
                body=_json_response({"error": "Missing 'state'"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        try:
            state = GameState.from_dict(state_dict)
            obs = _ENGINE.observe(state)
        except Exception as exc:
            await _send_response(
                send,
                status=400,
                body=_json_response({"error": f"Failed to observe state: {exc}"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        response_data = {
            "success": True,
            "observation": sanitize_observation(obs),
            "character": state.character.to_dict(),
            "state": state.to_dict(),
            "quest": _ENGINE.get_quest_progress(state),
            "codex": _ENGINE.get_codex_progress(state),
            "transit": _ENGINE.get_transit_progress(state),
            "trade": _ENGINE.get_trade_progress(state),
            "weather": _ENGINE.get_weather_state(state),
            "bounty": _ENGINE.get_bounty_progress(state),
            "companion": _ENGINE.get_companion_progress(state),
            "bestiary": _ENGINE.get_bestiary_progress(state),
            "survival": _ENGINE.get_survival_progress(state),
            "orders": _ENGINE.get_orders_progress(state),
            "shrines": _ENGINE.get_shrines_progress(state),
        }
        await _send_response(
            send,
            status=200,
            body=_json_response(response_data),
            content_type=b"application/json; charset=utf-8",
        )
        return

    # Route: /api/game/replay (Pure deterministic trace verification & replay)
    if path == "/api/game/replay":
        if method != "POST":
            await _send_response(
                send,
                status=405,
                body=_json_response({"error": "method_not_allowed"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        raw_body = await _read_body(receive)
        try:
            req_data = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except json.JSONDecodeError as exc:
            await _send_response(
                send,
                status=400,
                body=_json_response({"error": f"Invalid JSON: {exc}"}),
                content_type=b"application/json; charset=utf-8",
            )
            return

        preset_name = str(req_data.get("preset", "cutpurse"))
        seed = req_data.get("seed", 42)
        actions = req_data.get("actions", [])
        if not isinstance(actions, list):
            actions = []

        try:
            preset = get_preset(preset_name)
        except KeyError:
            preset = get_preset("cutpurse")

        effective_seed = int(seed) if isinstance(seed, (int, float)) else 42
        state = GameState(
            build_id="af-build-001",
            session_id=f"replay-{preset.id}-{effective_seed}",
            character=preset.character,
            current_region=preset.start_region,
            current_scene=preset.start_scene,
            rng=DeterministicRNG.from_seed(effective_seed),
        )
        obs = _ENGINE.observe(state)
        fingerprints = [state.fingerprint()]

        for act_id in actions:
            state, obs = _ENGINE.step(state, str(act_id))
            fingerprints.append(state.fingerprint())
            if not obs.success or obs.is_terminal:
                break

        response_data = {
            "success": True,
            "turn_count": state.turn_count,
            "observation": sanitize_observation(obs),
            "character": state.character.to_dict(),
            "state": state.to_dict(),
            "quest": _ENGINE.get_quest_progress(state),
            "codex": _ENGINE.get_codex_progress(state),
            "transit": _ENGINE.get_transit_progress(state),
            "trade": _ENGINE.get_trade_progress(state),
            "weather": _ENGINE.get_weather_state(state),
            "bounty": _ENGINE.get_bounty_progress(state),
            "companion": _ENGINE.get_companion_progress(state),
            "bestiary": _ENGINE.get_bestiary_progress(state),
            "survival": _ENGINE.get_survival_progress(state),
            "orders": _ENGINE.get_orders_progress(state),
            "shrines": _ENGINE.get_shrines_progress(state),
            "fingerprints": fingerprints,
            "final_fingerprint": state.fingerprint(),
        }
        await _send_response(
            send,
            status=200,
            body=_json_response(response_data),
            content_type=b"application/json; charset=utf-8",
        )
        return

    # Route: /api/mcp or /mcp (Model Context Protocol JSON-RPC)
    if path in {"/api/mcp", "/mcp"}:
        server = MCPServer(engine=_ENGINE)
        if method in {"GET", "HEAD"}:
            payload = {
                "service": "adventure-forge-mcp",
                "version": __version__,
                "tools": server.get_tools_schema(),
            }
            await _send_response(
                send,
                status=200,
                body=_json_response(payload),
                content_type=b"application/json; charset=utf-8",
                include_body=include_body,
            )
            return

        if method == "POST":
            raw_body = await _read_body(receive)
            try:
                data = json.loads(raw_body.decode("utf-8")) if raw_body else {}
            except json.JSONDecodeError as exc:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {exc}"},
                }
                await _send_response(
                    send,
                    status=400,
                    body=_json_response(err_resp),
                    content_type=b"application/json; charset=utf-8",
                )
                return

            rpc_response = handle_jsonrpc_request(data, server)
            resp_body = _json_response(rpc_response if rpc_response is not None else {})
            await _send_response(
                send,
                status=200,
                body=resp_body,
                content_type=b"application/json; charset=utf-8",
            )
            return

        await _send_response(
            send,
            status=405,
            body=_json_response({"error": "method_not_allowed"}),
            content_type=b"application/json; charset=utf-8",
        )
        return

    # Default 404 for unknown endpoints
    await _send_response(
        send,
        status=404,
        body=_json_response({"error": "not_found"}),
        content_type=b"application/json; charset=utf-8",
        include_body=include_body,
    )
