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
from adventure_forge.content.quests import get_continental_main_quest, get_provincial_subquests
from adventure_forge.core.character import CHARACTER_PRESETS, get_preset
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
.cat-trait_exploit { background: rgba(210,153,34,0.2); color: var(--gold); }
.cat-general { background: rgba(110,118,129,0.2); color: var(--text-muted); }
.badge-cost { color: var(--gold); }

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
      <div>
        <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.4rem 0.8rem;" onclick="resetToSelect()">Restart</button>
      </div>
    </div>

    <div style="margin-bottom: 0.5rem;" id="status-container" class="tag-row"></div>
    <div style="margin-bottom: 1rem;" id="inventory-container" class="tag-row"></div>

    <div id="quest-banner" style="background: rgba(217, 119, 6, 0.12); border: 1px solid rgba(217, 119, 6, 0.35); border-radius: 6px; padding: 0.6rem 0.9rem; margin-bottom: 1rem; font-size: 0.85rem;">
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
      <div class="scene-breadcrumb" id="scene-region">Region</div>
      <h2 class="scene-title" id="scene-title">Scene Title</h2>
      <p class="scene-prose" id="scene-description">Prose loading...</p>
      <div class="events-box" id="scene-events" style="display: none;"></div>
    </div>

    <div>
      <div class="action-section-title">Legal Actions (<span id="action-count">0</span> Available)</div>
      <div class="actions-grid" id="actions-container"></div>
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

let selectedPreset = "cutpurse";
let gameState = null;

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
    renderGame(data.observation, data.character, data.quest);
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
    renderGame(data.observation, data.character, data.quest);
  } catch (err) {
    alert(err.message);
    btns.forEach(b => b.disabled = false);
  }
}

function renderGame(obs, char, quest) {
  // HUD
  document.getElementById("char-name").textContent = char.name;
  document.getElementById("char-origin").textContent = `${char.ancestry} &bull; ${char.background}`;
  
  const hpPct = Math.max(0, Math.min(100, (char.health / char.max_health) * 100));
  document.getElementById("hp-bar").style.width = hpPct + "%";
  document.getElementById("hp-text").textContent = `${char.health}/${char.max_health}`;

  const spPct = Math.max(0, Math.min(100, (char.stamina / char.max_stamina) * 100));
  document.getElementById("sp-bar").style.width = spPct + "%";
  document.getElementById("sp-text").textContent = `${char.stamina}/${char.max_stamina}`;

  document.getElementById("turn-display").textContent = obs.turn_count;
  document.getElementById("fingerprint-display").textContent = obs.fingerprint ? obs.fingerprint.substring(0, 16) + "..." : "n/a";

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
        const qName = activeSubEntry[0].replace(/^subquest_/, '').replace(/_/g, ' ').toUpperCase();
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

  // Legal Actions
  const actionsContainer = document.getElementById("actions-container");
  actionsContainer.innerHTML = "";
  const actions = obs.legal_actions || [];
  document.getElementById("action-count").textContent = actions.length;

  for (const act of actions) {
    const btn = document.createElement("button");
    btn.className = "action-btn";
    btn.onclick = () => stepAction(act.id);

    const catClass = "cat-" + (act.category || "general");
    const costHtml = act.stamina_cost > 0 ? `<span class="badge-cost">⚡ ${act.stamina_cost} SP</span>` : "";

    btn.innerHTML = `
      <div class="action-label">${act.label}</div>
      <div class="action-meta">
        <span class="badge-category ${catClass}">${act.category}</span>
        <span>Risk: ${act.risk}</span>
        ${costHtml}
      </div>
    `;
    actionsContainer.appendChild(btn);
  }
}

function resetToSelect() {
  document.getElementById("play-view").style.display = "none";
  document.getElementById("select-view").style.display = "block";
  renderPresetCards();
}

window.addEventListener("DOMContentLoaded", () => {
  renderPresetCards();
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
    },
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
_HAZARDS_RESPONSE_BYTES = json.dumps(
    {"hazards": {k: v.to_dict() for k, v in HAZARD_COMBOS.items()}},
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
