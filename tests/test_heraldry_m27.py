"""Milestone 27 Verification: Provincial Faction Heraldry, Renown Orders & Continental War Banners.

Tests cover:
1. 5 Provincial Renown Orders integrity across 5 provinces and 100% Hemingway prose compliance.
2. Faction fealty pledge affordances, 7-axis qualification, banner item acquisition, and reputation gains.
3. Rejection of fealty pledge when qualifications are unmet.
4. War banner field raising affordances and provincial banner marker buffs.
5. Central Crossroads Heraldic Rally at bazaar_center.
6. Grand Marshal rank progression and defensive handling of non-standard inventory/marker types.
7. Bit-for-bit deterministic replay with heraldry actions.
8. ASGI serverless endpoint GET/HEAD /api/game/orders and /api/game/new integration.
"""
import pytest
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.heraldry import (
    FACTION_ORDERS,
    evaluate_orders_progress,
)
from adventure_forge.core.character import get_preset, CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import (
    ProseLinter,
    FORBIDDEN_PURPLE_WORDS,
    split_sentences,
    word_count,
)
from app import app


@pytest.fixture
def engine() -> AdventureEngine:
    reg = build_world_registry()
    return AdventureEngine(reg)


@pytest.fixture
def base_state() -> GameState:
    preset = get_preset("warrior")
    return GameState(
        build_id="af-m27-test",
        session_id="test-session-heraldry",
        character=preset.character,
        current_region=preset.start_region,
        current_scene=preset.start_scene,
        rng=DeterministicRNG.from_seed(42),
    )


def test_heraldry_registry_integrity_and_prose(engine: AdventureEngine) -> None:
    """Validate 5 orders, valid sanctum scenes, and 100% Hemingway prose compliance."""
    assert len(FACTION_ORDERS) == 5
    provinces = {o.province for o in FACTION_ORDERS.values()}
    assert len(provinces) == 5

    for order in FACTION_ORDERS.values():
        # Sanctum scene must exist in world graph
        scene = engine.get_scene(order.sanctum_scene)
        assert scene is not None, f"Sanctum scene {order.sanctum_scene} for {order.id} missing"

    linter = ProseLinter()

    for oid, order in FACTION_ORDERS.items():
        # Action labels must be 1-3 words
        for lbl in [order.pledge_action_label, order.raise_action_label, "Rally Order Banners"]:
            wc = len(lbl.split())
            assert 1 <= wc <= 3, f"Label '{lbl}' exceeds 3 words ({wc} words)"

        # Prose check: description, pledge_result_text, raise_result_text
        for field_name, text in [
            ("description", order.description),
            ("pledge_result_text", order.pledge_result_text),
            ("raise_result_text", order.raise_result_text),
        ]:
            errs = linter.lint_text(text, f"{oid} {field_name}")
            assert not errs, f"Prose errors in {oid} {field_name}: {errs}"

            sents = split_sentences(text)
            assert 1 <= len(sents) <= 3
            for s in sents:
                assert word_count(s) <= 18, f"Sentence '{s}' exceeds 18 words"

            for pw in FORBIDDEN_PURPLE_WORDS:
                assert pw not in text.lower(), f"Purple word '{pw}' found in {oid} {field_name}"


def test_fealty_pledge_affordance_and_acquisition(engine: AdventureEngine, base_state: GameState) -> None:
    """Test fealty pledge in sanctum scene, banner item acquisition, and rep boost."""
    order = FACTION_ORDERS["order_iron_peak"]
    # Warrior preset has strength 16 and trait 'iron_gutted', satisfying alternate criteria
    state = base_state.evolve(current_scene=order.sanctum_scene, current_region="reach")

    legal = engine.get_legal_actions(state)
    action_ids = [a.id for a in legal]
    assert order.pledge_action_id in action_ids

    init_rep = state.character.get_reputation(order.faction_key)
    new_state, obs = engine.step(state, order.pledge_action_id)
    assert obs.success
    assert order.banner_item_id in new_state.character.inventory
    assert new_state.world_flags.get(f"heraldry_pledged_{order.id}") is True
    assert new_state.character.get_reputation(order.faction_key) == init_rep + 5

    # Once sworn, action no longer offered
    legal_after = engine.get_legal_actions(new_state)
    action_ids_after = [a.id for a in legal_after]
    assert order.pledge_action_id not in action_ids_after


def test_fealty_pledge_unmet_requirements(engine: AdventureEngine, base_state: GameState) -> None:
    """Test fealty pledge is not offered when 7-axis criteria are not met."""
    order = FACTION_ORDERS["order_abyssal_trench"]
    unqualified_char = CharacterSheet(
        name="Novice",
        ancestry="Plainsman",
        background="drifter",
        attributes={"willpower": 8},
        skills={},
        traits=[],
        flaws=[],
        reputation={"deep_delvers": 0},
        markers=[],
        inventory=[],
        health=20,
        max_health=20,
        stamina=10,
        max_stamina=10,
    )
    state = base_state.evolve(
        character=unqualified_char,
        current_scene=order.sanctum_scene,
        current_region="sunken_hollows",
    )

    legal = engine.get_legal_actions(state)
    action_ids = [a.id for a in legal]
    assert order.pledge_action_id not in action_ids


def test_war_banner_raising_in_the_field(engine: AdventureEngine, base_state: GameState) -> None:
    """Test raising a war banner in the field grants the order's active marker buff."""
    order = FACTION_ORDERS["order_iron_peak"]
    char_with_banner = base_state.character.modify(
        inventory=list(base_state.character.inventory) + [order.banner_item_id],
        stamina=5,
    )
    state = base_state.evolve(
        character=char_with_banner,
        current_scene="reach_high_pass_gate",
        current_region="reach",
    )

    legal = engine.get_legal_actions(state)
    action_ids = [a.id for a in legal]
    assert order.raise_action_id in action_ids

    new_state, obs = engine.step(state, order.raise_action_id)
    assert obs.success
    assert order.granted_marker in new_state.character.markers
    assert new_state.character.stamina == 8

    # Once raised, raise action is not offered again
    legal_after = engine.get_legal_actions(new_state)
    action_ids_after = [a.id for a in legal_after]
    assert order.raise_action_id not in action_ids_after


def test_crossroads_bazaar_heraldic_rally(engine: AdventureEngine, base_state: GameState) -> None:
    """Test rallying provincial war banners at Central Bazaar."""
    order = FACTION_ORDERS["order_iron_peak"]
    char_with_banner = base_state.character.modify(
        inventory=list(base_state.character.inventory) + [order.banner_item_id],
        stamina=3,
    )
    state = base_state.evolve(
        character=char_with_banner,
        current_scene="bazaar_center",
        current_region="stress_market",
    )

    legal = engine.get_legal_actions(state)
    action_ids = [a.id for a in legal]
    assert "heraldry_rally_banners" in action_ids

    new_state, obs = engine.step(state, "heraldry_rally_banners")
    assert obs.success
    assert new_state.world_flags.get("heraldry_rallied_bazaar") is True
    assert new_state.character.stamina == 8


def test_orders_progress_and_ranks() -> None:
    """Test Grand Marshal rank progression and defensive inventory/marker handling."""
    # 0 banners -> Unsworn Wayfarer
    prog0 = evaluate_orders_progress({}, inventory=[], markers=[])
    assert prog0["rank_title"] == "Unsworn Wayfarer"
    assert not prog0["is_knight"]

    # 1 banner -> Order Knight-Errant
    prog1 = evaluate_orders_progress(
        {"heraldry_pledged_order_iron_peak": True},
        inventory=["item_banner_iron_peak"],
        markers=["marker_banner_iron_valor"],
    )
    assert "Knight-Errant" in prog1["rank_title"]
    assert prog1["is_knight"]
    assert prog1["active_banner_marker"] == "marker_banner_iron_valor"

    # 2 banners -> Provincial Banneret
    prog2 = evaluate_orders_progress(
        {},
        inventory=["item_banner_iron_peak", "item_banner_sunfire_sands"],
        markers=None,
    )
    assert "Banneret" in prog2["rank_title"]

    # 3 banners -> Continental Commander
    prog3 = evaluate_orders_progress(
        {},
        inventory={"item_banner_iron_peak", "item_banner_sunfire_sands", "item_banner_salted_river"},
        markers=set(),
    )
    assert "Commander" in prog3["rank_title"]
    assert prog3["is_commander"]

    # 4 banners -> High Faction Marshal
    prog4 = evaluate_orders_progress(
        {},
        inventory=("item_banner_iron_peak", "item_banner_sunfire_sands", "item_banner_salted_river", "item_banner_gilded_rose"),
        markers=(),
    )
    assert "Marshal" in prog4["rank_title"]

    # 5 banners -> Grandmaster
    prog5 = evaluate_orders_progress(
        {},
        inventory=[o.banner_item_id for o in FACTION_ORDERS.values()],
        markers=[],
    )
    assert "Grandmaster" in prog5["rank_title"]
    assert prog5["is_grandmaster"]


def test_heraldry_deterministic_replay(engine: AdventureEngine, base_state: GameState) -> None:
    """Test deterministic replay produces identical SHA-256 fingerprint with heraldry actions."""
    def run_trace(seed: int) -> str:
        preset = get_preset("warrior")
        state = GameState(
            build_id="af-m27-replay",
            session_id=f"test-heraldry-replay-{seed}",
            character=preset.character,
            current_region="reach",
            current_scene="reach_bastion_redoubt_chamber",
            rng=DeterministicRNG.from_seed(seed),
        )
        # Step pledge fealty
        state, _ = engine.step(state, "order_pledge_iron_peak")
        # Step raise banner
        state, _ = engine.step(state, "heraldry_raise_iron_peak")
        # Move to bazaar and rally
        state = state.evolve(current_scene="bazaar_center")
        state, _ = engine.step(state, "heraldry_rally_banners")
        return state.fingerprint()

    fp1 = run_trace(42)
    fp2 = run_trace(42)
    assert fp1 == fp2, "Bit-for-bit SHA-256 fingerprint match required across deterministic runs"


def test_orders_asgi_endpoint() -> None:
    """Test ASGI serverless endpoint GET/HEAD at /api/game/orders and /api/game/new."""
    import asyncio
    import json

    async def run_asgi(path: str, method: str = "GET", body: bytes = b""):
        response_data = {"status": 0, "headers": [], "body": b""}

        async def receive():
            return {"type": "http.request", "body": body}

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
            "headers": [(b"host", b"localhost")],
        }
        await app(scope, receive, send)
        return response_data

    # 1. GET /api/game/orders
    res_get = asyncio.run(run_asgi("/api/game/orders", "GET"))
    assert res_get["status"] == 200
    assert any(k == b"content-type" and b"application/json" in v for k, v in res_get["headers"])
    body = json.loads(res_get["body"].decode("utf-8"))
    assert body["total_orders"] == 5
    assert len(body["orders"]) == 5

    # 2. HEAD /api/game/orders
    res_head = asyncio.run(run_asgi("/api/game/orders", "HEAD"))
    assert res_head["status"] == 200
    assert res_head["body"] == b""

    # 3. POST /api/game/new includes orders progress
    new_req_body = json.dumps({"preset": "warrior", "seed": 42}).encode("utf-8")
    res_new = asyncio.run(run_asgi("/api/game/new", "POST", new_req_body))
    assert res_new["status"] == 200
    new_data = json.loads(res_new["body"].decode("utf-8"))
    assert "orders" in new_data
    assert new_data["orders"]["total_orders"] == 5
    assert new_data["orders"]["banners_held"] == 0
    assert new_data["orders"]["rank_title"] == "Unsworn Wayfarer"
