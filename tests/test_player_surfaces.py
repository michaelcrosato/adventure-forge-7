"""Tests for Player Surfaces and Vercel API Enhancements.

Validates:
- GET /api/game/quests returns campaign and all 5 provincial subquests
- GET /api/game/hazards returns canonical status effect combos
- Server-Timing header is attached to all API responses
- Sub-100ms latency guarantee (< 50ms for transitions)
- Rich HUD payload containing character attributes, markers/status, and quest progress
- Terminal CLI render_ui displays character status, items, and quest info
"""
import asyncio
import json
import time
from typing import Any, List, Dict, Optional
from app import app
from adventure_forge.core.character import get_preset
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.content.loader import build_world_registry
from adventure_forge.player.cli import render_ui


def request_sync(
    path: str,
    method: str = "GET",
    body: bytes = b"",
    headers: Optional[List[tuple]] = None
) -> Dict[str, Any]:
    if headers is None:
        headers = [(b"content-type", b"application/json")]

    scope = {
        "type": "http",
        "method": method,
        "path": path,
        "headers": headers,
        "query_string": b"",
    }

    messages = []
    async def fake_receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def fake_send(msg):
        messages.append(msg)

    async def run():
        await app(scope, fake_receive, fake_send)

    asyncio.run(run())

    status = messages[0]["status"]
    headers_dict = {k.decode("ascii").lower(): v.decode("ascii") for k, v in messages[0]["headers"]}
    resp_body = messages[1].get("body", b"")

    return {
        "status": status,
        "headers": headers_dict,
        "body": resp_body,
        "json": json.loads(resp_body.decode("utf-8")) if resp_body else None,
    }


def test_api_game_quests_endpoint():
    """GET /api/game/quests returns both the main campaign and all 5 provincial subquests."""
    res = request_sync("/api/game/quests")
    assert res["status"] == 200
    assert "server-timing" in res["headers"]
    data = res["json"]
    assert "campaign" in data
    assert data["campaign"]["id"] == "five_seals_campaign"
    assert len(data["campaign"]["stages"]) == 5

    assert "subquests" in data
    subquests = data["subquests"]
    assert len(subquests) == 5
    assert "subquest_reach_smuggler_caches" in subquests
    assert "subquest_lowlands_shadow_broker" in subquests
    assert "subquest_scorchwaste_water_baron" in subquests
    assert "subquest_court_decrees" in subquests
    assert "subquest_hollows_abyssal_keystones" in subquests


def test_api_game_hazards_endpoint():
    """GET /api/game/hazards returns all canonical elemental hazard combos."""
    res = request_sync("/api/game/hazards")
    assert res["status"] == 200
    assert "server-timing" in res["headers"]
    data = res["json"]
    assert "hazards" in data
    hazards = data["hazards"]
    assert "conflagration" in hazards
    assert "stun" in hazards
    assert "obscured" in hazards
    assert "corrode" in hazards
    assert "fire" in hazards["conflagration"]["required_elements"]
    assert "oil" in hazards["conflagration"]["required_elements"]


def test_api_sub_100ms_latency_guarantee():
    """Verify sub-100ms response time on new game and step transitions."""
    # 1. New game start
    t0 = time.perf_counter()
    new_body = json.dumps({"preset": "cutpurse", "seed": 42}).encode("utf-8")
    res_new = request_sync("/api/game/new", method="POST", body=new_body)
    dur_new_ms = (time.perf_counter() - t0) * 1000.0

    assert res_new["status"] == 200
    assert dur_new_ms < 50.0, f"New game took {dur_new_ms:.2f}ms, expected < 50ms"
    assert "server-timing" in res_new["headers"]
    assert res_new["json"]["success"] is True

    # Verify rich HUD contents
    char_data = res_new["json"]["character"]
    assert "name" in char_data
    assert "health" in char_data
    assert "stamina" in char_data
    assert "inventory" in char_data
    assert "markers" in char_data

    quest_data = res_new["json"]["quest"]
    assert "completed_stages" in quest_data
    assert "subquests" in quest_data

    legal_acts = res_new["json"]["observation"]["legal_actions"]
    assert len(legal_acts) > 0
    chosen_action = legal_acts[0]["id"]

    # 2. Step transition
    state_payload = res_new["json"]["state"]
    step_body = json.dumps({
        "state": state_payload,
        "action_id": chosen_action
    }).encode("utf-8")

    t1 = time.perf_counter()
    res_step = request_sync("/api/game/step", method="POST", body=step_body)
    dur_step_ms = (time.perf_counter() - t1) * 1000.0

    assert res_step["status"] == 200
    assert dur_step_ms < 50.0, f"Step transition took {dur_step_ms:.2f}ms, expected < 50ms"
    assert "server-timing" in res_step["headers"]
    assert res_step["json"]["success"] is True


def test_cli_render_ui_with_rich_hud(capsys):
    """Terminal CLI displays character status, items, and quest info when state is provided."""
    reg = build_world_registry()
    eng = AdventureEngine(reg)
    char = get_preset("cutpurse").character.modify(markers=["oiled", "conflagration"])
    state = GameState(
        build_id="af-001",
        session_id="test-cli",
        character=char,
        current_region="lower_warrens",
        current_scene="warrens_gate",
    )
    obs = eng.observe(state)
    quest = eng.get_quest_progress(state)

    render_ui(obs, page=0, page_size=10, state=state, quest_info=quest)
    captured = capsys.readouterr().out

    assert "THE WARRENS IRON GATE" in captured
    assert "HP: 20/20" in captured
    assert "SP: 10/10" in captured
    assert "Status: oiled, conflagration" in captured
    assert "Items: 2" in captured
    assert "Quest: stage_crags_beacon" in captured
