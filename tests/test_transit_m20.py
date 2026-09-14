"""Tests for Continental Chartered Transit & Regional Caravan Network (Milestone 20).

Verifies:
1. Complete 10-route bidirectional transit network linking Central Bazaar to 5 provinces.
2. Strict Hemingway prose linter compliance (FKGL 6-8, <=18 words/sent, <=3 words/label, no purple words).
3. 7-axis reactivity (currency, traits, backgrounds, gear) for boarding transit.
4. Dynamic affordance synthesis in origin scenes.
5. Clean scene transitions and automatic region resolution.
6. Continental Wayfarer milestone upon traveling all five provincial routes.
7. Bit-for-bit replay determinism and state fingerprint fidelity.
8. ASGI REST API (/api/game/transit).
"""
import asyncio
import json
import pytest
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.actions import synthesize_affordances
from adventure_forge.core.character import get_preset
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.state import GameState
from adventure_forge.core.transit import (
    CHARTERED_ROUTES,
    evaluate_transit_progress,
)
from adventure_forge.linter.prose_linter import ProseLinter


@pytest.fixture
def registry():
    return build_world_registry()


@pytest.fixture
def engine(registry):
    return AdventureEngine(registry)


def test_transit_network_structure(registry):
    """Ensure all 10 chartered transit routes have valid origins, destinations, and labels."""
    all_scenes = {s for reg in registry.values() for s in reg.scenes.keys()}
    assert len(CHARTERED_ROUTES) == 10

    outbound = [r for r in CHARTERED_ROUTES if r.origin_scene == "bazaar_center"]
    inbound = [r for r in CHARTERED_ROUTES if r.destination_scene == "bazaar_center"]
    assert len(outbound) == 5
    assert len(inbound) == 5

    for route in CHARTERED_ROUTES:
        assert route.origin_scene in all_scenes, f"Origin '{route.origin_scene}' not in registry!"
        assert route.destination_scene in all_scenes, f"Destination '{route.destination_scene}' not in registry!"
        assert len(route.action_label.split()) <= 3
        assert route.stamina_cost >= 1
        assert route.category == "movement"


def test_transit_hemingway_prose_compliance():
    """Ensure all transit result texts and labels pass the Hemingway prose linter."""
    linter = ProseLinter()
    for route in CHARTERED_ROUTES:
        # Label length: 1-3 words
        label_words = route.action_label.split()
        assert 1 <= len(label_words) <= 3, f"Label '{route.action_label}' exceeds 3 words"

        # Result text: <= 18 words/sent, active voice, zero purple words
        errs = linter.lint_text(route.result_text, context=route.id)
        assert not errs, f"Prose errors in {route.id}: {errs}"


def test_transit_affordance_synthesis(registry):
    """Verify that transit affordances are synthesized in bazaar_center and provincial hubs."""
    bazaar = registry["stress_market"].scenes["bazaar_center"]
    silas = get_preset("cutpurse").character.modify(inventory=["silver_coin"])

    # Silas in bazaar_center with coin sees all 5 outbound routes
    bazaar_actions = synthesize_affordances(
        bazaar.base_actions,
        bazaar.entities,
        silas,
        {},
        region_id="stress_market",
        scene_id="bazaar_center",
    )
    transit_acts = [a for a in bazaar_actions if a.id.startswith("transit_")]
    assert len(transit_acts) == 5
    route_ids = {a.id for a in transit_acts}
    assert "transit_cable_to_reach" in route_ids
    assert "transit_barge_to_lowlands" in route_ids
    assert "transit_skiff_to_scorchwaste" in route_ids
    assert "transit_carriage_to_court" in route_ids
    assert "transit_ferry_to_hollows" in route_ids

    # In a non-transit scene, no transit actions are synthesized
    shrine = registry["province_reach"].scenes["reach_secret_shrine"]
    shrine_actions = synthesize_affordances(
        shrine.base_actions,
        shrine.entities,
        silas,
        {},
        region_id="province_reach",
        scene_id="reach_secret_shrine",
    )
    assert not any(a.id.startswith("transit_") for a in shrine_actions)


def test_transit_7axis_reactivity(registry):
    """Verify that different character backgrounds/traits unlock specific transit routes without coins."""
    bazaar = registry["stress_market"].scenes["bazaar_center"]

    # Kael (Nomad with Dune Strider) can board the Desert Silt-Skiff without coins
    kael = get_preset("nomad").character.modify(inventory=[])
    kael_actions = synthesize_affordances(
        bazaar.base_actions,
        bazaar.entities,
        kael,
        {},
        region_id="stress_market",
        scene_id="bazaar_center",
    )
    kael_transit = {a.id for a in kael_actions if a.id.startswith("transit_")}
    assert "transit_skiff_to_scorchwaste" in kael_transit

    # Vivienne (Noble Exile with High Decorum) can board the Imperial High Carriage
    vivienne = get_preset("noble").character.modify(inventory=[])
    viv_actions = synthesize_affordances(
        bazaar.base_actions,
        bazaar.entities,
        vivienne,
        {},
        region_id="stress_market",
        scene_id="bazaar_center",
    )
    viv_transit = {a.id for a in viv_actions if a.id.startswith("transit_")}
    assert "transit_carriage_to_court" in viv_transit

    # Torin (Reachman with Mountain Scout) can board the Highland Cable Lift
    torin = get_preset("scout").character.modify(inventory=[])
    torin_actions = synthesize_affordances(
        bazaar.base_actions,
        bazaar.entities,
        torin,
        {},
        region_id="stress_market",
        scene_id="bazaar_center",
    )
    torin_transit = {a.id for a in torin_actions if a.id.startswith("transit_")}
    assert "transit_cable_to_reach" in torin_transit


def test_transit_scene_transition_and_region_resolution(engine):
    """Verify that boarding transit changes scene and auto-resolves region."""
    torin = get_preset("scout").character.modify(stamina=10)
    initial_state = GameState(
        build_id="af-build-001",
        session_id="transit-test-01",
        character=torin,
        current_region="stress_market",
        current_scene="bazaar_center",
    )

    next_state, obs = engine.step(initial_state, "transit_cable_to_reach")
    assert obs.success
    assert next_state.current_scene == "reach_dunwall_fort_gate"
    assert next_state.current_region == "province_reach"
    assert next_state.world_flags.get("route_reach") is True
    assert next_state.character.stamina == 9


def test_transit_wayfarer_milestone(engine):
    """Verify that traveling all 5 routes awards Continental Wayfarer."""
    char = get_preset("cutpurse").character.modify(inventory=["silver_coin"], stamina=10)
    state = GameState(
        build_id="af-build-001",
        session_id="transit-test-wayfarer",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
        world_flags={
            "route_reach": True,
            "route_lowlands": True,
            "route_scorchwaste": True,
            "route_high_court": True,
        },
    )

    # Board the 5th route (Sunken Hollows)
    next_state, obs = engine.step(state, "transit_ferry_to_hollows")
    assert obs.success
    assert next_state.world_flags.get("route_sunken_hollows") is True
    assert next_state.world_flags.get("continental_wayfarer_unlocked") is True
    assert next_state.character.has_marker("continental_wayfarer")
    assert any("Continental Wayfarer" in ev for ev in obs.events)

    # Progress evaluation
    progress = evaluate_transit_progress(next_state.world_flags)
    assert progress["traveled_count"] == 5
    assert progress["wayfarer_unlocked"] is True


def test_transit_replay_determinism(engine):
    """Verify bit-for-bit replay determinism across transit journeys."""
    char = get_preset("cutpurse").character.modify(inventory=["silver_coin"], stamina=10)
    state1 = GameState(
        build_id="af-build-001",
        session_id="transit-replay-01",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
    )
    state2 = GameState(
        build_id="af-build-001",
        session_id="transit-replay-02",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
    )

    next1, obs1 = engine.step(state1, "transit_skiff_to_scorchwaste")
    next2, obs2 = engine.step(state2, "transit_skiff_to_scorchwaste")

    assert obs1.success and obs2.success
    assert next1.fingerprint() == next2.fingerprint()
    assert next1.current_scene == next2.current_scene == "scorchwaste_ashen_gate_gate"
    assert next1.current_region == next2.current_region == "province_scorchwaste"


def test_transit_asgi_endpoint():
    """Test /api/game/transit returns 200 with all chartered routes."""
    from app import app

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/api/game/transit",
        "headers": [],
        "query_string": b"",
    }
    sent_messages = []

    async def send(msg):
        sent_messages.append(msg)

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    asyncio.run(app(scope, receive, send))
    assert sent_messages[0]["status"] == 200
    body = json.loads(sent_messages[1]["body"].decode("utf-8"))
    assert body["total_routes"] == 10
    assert len(body["routes"]) == 10
