"""Milestone 21 Verification: Continental Trade Economy & Commodity Exchange.

Tests:
1. Commodity catalogue & provincial trade hubs structure.
2. Hemingway prose compliance (<= 18 words/sent, 1-3 sent, FKGL 6-8, <= 3 words/label, 0 purple words).
3. Affordance synthesis in Central Bazaar and provincial gates.
4. 7-axis reactivity, barter alternatives, and clan/archetype discounts.
5. Arbitrage execution: buy at origin/crossroads, travel to import hub, sell at premium demand.
6. Merchant Consortium and Master Trader milestone achievements.
7. Deterministic replay fidelity across trade sequences.
8. ASGI endpoint GET/HEAD /api/game/trade and payload inclusion.
"""
import asyncio
from typing import Dict, Any
import pytest
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.actions import synthesize_affordances
from adventure_forge.core.character import get_preset
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.state import GameState
from adventure_forge.core.trade import (
    COMMODITIES,
    TRADE_HUBS,
    COMMODITY_LABELS,
    evaluate_trade_progress,
    get_trade_affordances_for_scene,
)
from adventure_forge.linter.prose_linter import ProseLinter


@pytest.fixture
def registry():
    return build_world_registry()


@pytest.fixture
def engine(registry):
    return AdventureEngine(registry)


def test_trade_catalogue_structure():
    """Verify all 5 provincial commodities and 6 trade hubs exist with proper metadata."""
    assert len(COMMODITIES) == 5
    expected_commodities = {"iron_ore", "bog_whiskey", "sunfire_spice", "silk_bolt", "pearl_essence"}
    assert set(COMMODITIES.keys()) == expected_commodities

    for cid, comm in COMMODITIES.items():
        assert comm.id == cid
        assert comm.name
        assert comm.origin_province
        assert comm.origin_scene
        assert comm.base_buy_price >= 1
        assert comm.base_sell_price >= 1
        assert len(comm.import_bonuses) >= 2
        assert comm.barter_item
        assert comm.buy_result_text
        assert comm.sell_result_text

    # 6 trade hubs: Central Bazaar + 5 provincial gates
    assert len(TRADE_HUBS) == 6
    assert "bazaar_center" in TRADE_HUBS
    assert len(TRADE_HUBS["bazaar_center"]["available_commodities"]) == 5

    provincial_gates = [
        "reach_dunwall_fort_gate",
        "lowlands_oakhaven_port_gate",
        "scorchwaste_ashen_gate_gate",
        "high_court_grand_basilica_gate",
        "sunken_hollows_glow_grotto_gate",
    ]
    for gate in provincial_gates:
        assert gate in TRADE_HUBS
        assert len(TRADE_HUBS[gate]["available_commodities"]) >= 1


def test_trade_hemingway_prose_compliance():
    """Verify that commodity descriptions, result texts, and labels strictly adhere to Hemingway constraints."""
    linter = ProseLinter(max_grade=8.0)
    errors = []

    for cid, comm in COMMODITIES.items():
        # Description
        errs = linter.lint_text(comm.description, context=f"{cid}_desc")
        if errs:
            errors.extend(errs)

        # Buy result text
        errs = linter.lint_text(comm.buy_result_text, context=f"{cid}_buy")
        if errs:
            errors.extend(errs)

        # Sell result text
        errs = linter.lint_text(comm.sell_result_text, context=f"{cid}_sell")
        if errs:
            errors.extend(errs)

    for cid, labels in COMMODITY_LABELS.items():
        for act, lbl in labels.items():
            words = lbl.split()
            if len(words) < 1 or len(words) > 3:
                errors.append(f"Label '{lbl}' ({cid}_{act}) must be 1-3 words.")

    assert len(errors) == 0, f"Prose linter errors found: {errors}"


def test_trade_affordances_in_bazaar(registry):
    """Verify that a player in bazaar_center holding silver coins gets buy affordances for all 5 commodities."""
    bazaar = registry["stress_market"].scenes["bazaar_center"]
    char = get_preset("cutpurse").character.modify(inventory=["silver_coin"])

    actions = synthesize_affordances(
        bazaar.base_actions,
        bazaar.entities,
        char,
        {},
        region_id="stress_market",
        scene_id="bazaar_center",
    )

    trade_actions = [a for a in actions if a.category == "trade"]
    assert len(trade_actions) >= 5

    trade_ids = {a.id for a in trade_actions}
    for cid in COMMODITIES.keys():
        assert f"trade_buy_{cid}" in trade_ids


def test_trade_7axis_reactivity_and_barter():
    """Verify barter options without coins and clan/background discounts."""
    # Garron (Warrior) with no coins but carrying a crowbar gets barter affordance for iron ore
    garron = get_preset("warrior").character.modify(inventory=["crowbar"])
    garron_affordances = get_trade_affordances_for_scene("bazaar_center", garron, {})
    garron_ids = {a.id for a in garron_affordances}
    assert "trade_barter_iron_ore" in garron_ids
    assert "trade_buy_iron_ore" not in garron_ids  # Has no coin and no reachman clan discount

    # Lady Vivienne (Noble Exile with rhetoric) gets court discount to buy silk_bolt without coin
    vivienne = get_preset("noble").character.modify(inventory=[])
    viv_affordances = get_trade_affordances_for_scene("high_court_grand_basilica_gate", vivienne, {})
    viv_ids = {a.id for a in viv_affordances}
    assert "trade_buy_silk_bolt" in viv_ids

    # Kael (Nomad) gets caravan discount to buy sunfire_spice without coin
    kael = get_preset("nomad").character.modify(inventory=[])
    kael_affordances = get_trade_affordances_for_scene("scorchwaste_ashen_gate_gate", kael, {})
    kael_ids = {a.id for a in kael_affordances}
    assert "trade_buy_sunfire_spice" in kael_ids


def test_trade_arbitrage_and_profit(engine):
    """Verify full arbitrage cycle: buy at bazaar/origin, travel to import hub, sell at premium profit."""
    # Start at bazaar with 1 silver coin
    char = get_preset("cutpurse").character.modify(inventory=["silver_coin"], stamina=10)
    state = GameState(
        build_id="af-build-001",
        session_id="trade-arbitrage-01",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
    )

    # 1. Buy Highland Iron Ore at bazaar (costs 1 silver coin)
    state, obs = engine.step(state, "trade_buy_iron_ore")
    assert obs.success
    assert "iron_ore" in state.character.inventory
    assert "silver_coin" not in state.character.inventory

    # 2. Board chartered transit to The Sunken Hollows (deep import demand for iron ore!)
    state, obs = engine.step(state, "transit_ferry_to_hollows")
    assert obs.success
    assert state.current_scene == "sunken_hollows_glow_grotto_gate"

    # 3. Sell Iron Ore at Glow Grotto Quay (base price 1 + import bonus 2 = 3 silver coins!)
    state, obs = engine.step(state, "trade_sell_iron_ore")
    assert obs.success
    assert "iron_ore" not in state.character.inventory
    coins = [item for item in state.character.inventory if item == "silver_coin"]
    assert len(coins) == 3, f"Expected 3 coins from high-demand arbitrage, got {len(coins)}"

    # Check that arbitrage count incremented
    assert state.world_flags.get("arbitrage_completed", 0) >= 1
    assert bool(state.world_flags.get("arbitrage_iron_ore_sunken_hollows_glow_grotto_gate"))


def test_trade_consortium_and_master_milestones():
    """Verify Merchant Consortium Recognition and Master Trader milestone evaluation."""
    # 0 hubs visited
    prog = evaluate_trade_progress({})
    assert not prog["is_consortium_recognized"]
    assert not prog["is_master_trader"]
    assert prog["hubs_visited_count"] == 0

    # 3 hubs visited -> Consortium Recognized
    flags_3hubs = {
        "trade_hub_bazaar_center": True,
        "trade_hub_reach_dunwall_fort_gate": True,
        "trade_hub_lowlands_oakhaven_port_gate": True,
        "completed_trades": 3,
    }
    prog_3 = evaluate_trade_progress(flags_3hubs)
    assert prog_3["is_consortium_recognized"]
    assert prog_3["hubs_visited_count"] == 3
    assert not prog_3["is_master_trader"]

    # All 5 commodities traded + 2 arbitrage -> Master Trader Achieved
    flags_master = {
        **flags_3hubs,
        "traded_iron_ore": True,
        "traded_bog_whiskey": True,
        "traded_sunfire_spice": True,
        "traded_silk_bolt": True,
        "traded_pearl_essence": True,
        "arbitrage_completed": 2,
    }
    prog_m = evaluate_trade_progress(flags_master)
    assert prog_m["is_consortium_recognized"]
    assert prog_m["is_master_trader"]


def test_trade_replay_determinism(engine):
    """Verify bit-for-bit identical state fingerprints across deterministic trade replays."""
    def run_simulation(seed: int):
        char = get_preset("cutpurse").character.modify(inventory=["silver_coin"], stamina=10)
        state = GameState(
            build_id="af-build-001",
            session_id=f"trade-replay-{seed}",
            character=char,
            current_region="stress_market",
            current_scene="bazaar_center",
        )
        # Sequence: Buy iron ore, take cable lift to reach, sell iron ore at reach
        state, _ = engine.step(state, "trade_buy_iron_ore")
        state, _ = engine.step(state, "transit_cable_to_reach")
        state, _ = engine.step(state, "trade_sell_iron_ore")
        return state.fingerprint()

    fp1 = run_simulation(42)
    fp2 = run_simulation(42)
    assert fp1 == fp2, "State fingerprints must match bit-for-bit across deterministic runs"


def test_trade_asgi_endpoint():
    """Verify ASGI route GET /api/game/trade and inclusion of trade progress in game payloads."""
    from app import app
    import json

    async def call_asgi(path: str, method: str = "GET", body: bytes = b""):
        response_data: Dict[str, Any] = {"status": 0, "headers": [], "body": b""}

        async def receive():
            return {"type": "http.request", "body": body, "more_body": False}

        async def send(message):
            if message["type"] == "http.response.start":
                response_data["status"] = message["status"]
                response_data["headers"] = message.get("headers", [])
            elif message["type"] == "http.response.body":
                response_data["body"] += message.get("body", b"")

        scope = {
            "type": "http",
            "method": method,
            "path": path,
            "raw_path": path.encode("utf-8"),
            "headers": [(b"host", b"localhost"), (b"content-type", b"application/json")],
        }
        await app(scope, receive, send)
        return response_data

    # 1. GET /api/game/trade returns catalogue
    res = asyncio.run(call_asgi("/api/game/trade", method="GET"))
    assert res["status"] == 200
    data = json.loads(res["body"].decode("utf-8"))
    assert data["total_commodities"] == 5
    assert len(data["commodities"]) == 5
    assert "bazaar_center" in data["hubs"]

    # 2. HEAD /api/game/trade returns 200 without body
    head_res = asyncio.run(call_asgi("/api/game/trade", method="HEAD"))
    assert head_res["status"] == 200
    assert len(head_res["body"]) == 0

    # 3. POST /api/game/trade rejected with 405
    post_res = asyncio.run(call_asgi("/api/game/trade", method="POST"))
    assert post_res["status"] == 405

    # 4. POST /api/game/new response contains trade progress
    new_game_res = asyncio.run(
        call_asgi("/api/game/new", method="POST", body=b'{"preset":"cutpurse","seed":42}')
    )
    assert new_game_res["status"] == 200
    new_data = json.loads(new_game_res["body"].decode("utf-8"))
    assert "trade" in new_data
    assert "completed_trades" in new_data["trade"]
