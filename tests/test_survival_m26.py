"""Milestone 26 Verification: Continental Survival Camping, Wilderness Foraging & Field Rations System.

Tests cover:
1. 15 Provincial Foraging Sites, 6 Campsite Hearths, and 6 Cooking Recipes integrity with Hemingway prose compliance.
2. Wilderness foraging action execution and ingredient item harvesting.
3. Campsite rest action and vitality recovery (+5 HP, +5 SP).
4. Field cooking recipes at hearths, ingredient consumption, and ration item preparation.
5. Field meal consumption anywhere in the world and provincial marker buffs.
6. Continental Grand Feast cooking and Master Survivalist perks.
7. Survivalist rank progression and defensive handling of non-standard inventory types.
8. Deterministic replay fidelity with survival actions.
9. ASGI serverless endpoint GET/HEAD /api/game/survival and /api/game/new integration.
"""
import pytest
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.survival import (
    FORAGING_SPOTS,
    CAMPSITE_SCENES,
    COOKING_RECIPES,
    evaluate_survival_progress,
)
from adventure_forge.core.character import get_preset
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
        build_id="af-m26-test",
        session_id="test-session-survival",
        character=preset.character,
        current_region=preset.start_region,
        current_scene=preset.start_scene,
        rng=DeterministicRNG.from_seed(42),
    )


def test_survival_registry_integrity_and_prose(engine: AdventureEngine) -> None:
    """Validate 15 foraging spots, 6 campsites, 6 recipes, and 100% Hemingway prose compliance."""
    assert len(FORAGING_SPOTS) == 15
    for prov in ["The Reach", "The Scorchwaste", "The Lowlands", "The High Court", "The Sunken Hollows"]:
        prov_spots = [s for s in FORAGING_SPOTS.values() if s.province == prov]
        assert len(prov_spots) == 3, f"Province {prov} must have exactly 3 foraging spots"

    assert len(CAMPSITE_SCENES) == 6
    assert len(COOKING_RECIPES) == 6

    # All foraging scenes must exist in world graph
    for spot in FORAGING_SPOTS.values():
        scene = engine.get_scene(spot.scene_id)
        assert scene is not None, f"Foraging scene {spot.scene_id} missing from world graph"

    # All campsite scenes must exist in world graph
    for camp_scene_id in CAMPSITE_SCENES:
        scene = engine.get_scene(camp_scene_id)
        assert scene is not None, f"Campsite scene {camp_scene_id} missing from world graph"

    linter = ProseLinter()

    # Lint foraging spots
    for spot in FORAGING_SPOTS.values():
        wc = len(spot.action_label.split())
        assert 1 <= wc <= 3, f"Label '{spot.action_label}' exceeds 3 words"

        errs = linter.lint_text(spot.result_text, f"{spot.scene_id} result_text")
        assert not errs, f"Prose errors in {spot.scene_id}: {errs}"

        sents = split_sentences(spot.result_text)
        assert 1 <= len(sents) <= 3
        for s in sents:
            assert word_count(s) <= 18, f"Sentence '{s}' exceeds 18 words"

        for pw in FORBIDDEN_PURPLE_WORDS:
            assert pw not in spot.result_text.lower(), f"Purple word '{pw}' found in {spot.scene_id}"

    # Lint recipes
    for recipe in COOKING_RECIPES.values():
        for lbl in [recipe.cook_action_label, recipe.eat_action_label]:
            wc = len(lbl.split())
            assert 1 <= wc <= 3, f"Label '{lbl}' exceeds 3 words"

        for text_field, text in [
            ("description", recipe.description),
            ("cook_result_text", recipe.cook_result_text),
            ("eat_result_text", recipe.eat_result_text),
        ]:
            errs = linter.lint_text(text, f"{recipe.id} {text_field}")
            assert not errs, f"Prose errors in {recipe.id} {text_field}: {errs}"

            sents = split_sentences(text)
            assert 1 <= len(sents) <= 3
            for s in sents:
                assert word_count(s) <= 18, f"Sentence '{s}' exceeds 18 words"

            for pw in FORBIDDEN_PURPLE_WORDS:
                assert pw not in text.lower(), f"Purple word '{pw}' in {recipe.id} {text_field}"


def test_wilderness_foraging_action_execution(engine: AdventureEngine, base_state: GameState) -> None:
    """Test foraging action availability, item acquisition, and flag persistence."""
    spot = FORAGING_SPOTS["reach_high_pass_gate"]
    state = base_state.evolve(current_scene=spot.scene_id, current_region="reach")

    legal = engine.get_legal_actions(state)
    action_ids = [a.id for a in legal]
    assert spot.action_id in action_ids

    new_state, obs = engine.step(state, spot.action_id)
    assert obs.success
    assert spot.ingredient_id in new_state.character.inventory
    assert new_state.world_flags.get(f"survival_foraged_{spot.scene_id}") is True

    # Once foraged, should no longer be offered
    legal_after = engine.get_legal_actions(new_state)
    action_ids_after = [a.id for a in legal_after]
    assert spot.action_id not in action_ids_after


def test_campsite_rest_vitality_recovery(engine: AdventureEngine, base_state: GameState) -> None:
    """Test campsite rest action restores 5 health and 5 stamina."""
    camp_scene = "reach_timber_camp_quarters"
    damaged_char = base_state.character.modify(
        health=base_state.character.max_health - 10,
        stamina=base_state.character.max_stamina - 10,
    )
    state = base_state.evolve(
        character=damaged_char,
        current_scene=camp_scene,
        current_region="reach",
    )

    legal = engine.get_legal_actions(state)
    action_ids = [a.id for a in legal]
    assert "survival_rest_camp" in action_ids

    new_state, obs = engine.step(state, "survival_rest_camp")
    assert obs.success
    assert new_state.character.health == damaged_char.health + 5
    assert new_state.character.stamina == damaged_char.stamina + 5


def test_field_cooking_and_meal_consumption(engine: AdventureEngine, base_state: GameState) -> None:
    """Test cooking at campsite, ingredient consumption, and eating in another scene."""
    recipe = COOKING_RECIPES["highland_stew"]
    camp_scene = "reach_timber_camp_quarters"

    # Add ingredient to character
    char_with_ing = base_state.character.modify(
        inventory=list(base_state.character.inventory) + ["foraged_frost_lichen"],
    )
    state = base_state.evolve(
        character=char_with_ing,
        current_scene=camp_scene,
        current_region="reach",
    )

    legal = engine.get_legal_actions(state)
    action_ids = [a.id for a in legal]
    assert recipe.cook_action_id in action_ids

    # Step cook action
    cooked_state, cook_obs = engine.step(state, recipe.cook_action_id)
    assert cook_obs.success
    assert "foraged_frost_lichen" not in cooked_state.character.inventory
    assert recipe.cooked_item_id in cooked_state.character.inventory
    assert cooked_state.world_flags.get("survival_meals_cooked") == 1

    # Move to a non-camp scene (e.g. reach_high_pass_gate)
    field_state = cooked_state.evolve(current_scene="reach_high_pass_gate")
    legal_field = engine.get_legal_actions(field_state)
    action_ids_field = [a.id for a in legal_field]
    assert recipe.eat_action_id in action_ids_field

    # Step eat action
    eaten_state, eat_obs = engine.step(field_state, recipe.eat_action_id)
    assert eat_obs.success
    assert recipe.cooked_item_id not in eaten_state.character.inventory
    assert recipe.granted_marker in eaten_state.character.markers


def test_grand_feast_preparation_and_buff(engine: AdventureEngine, base_state: GameState) -> None:
    """Test cooking Continental Grand Feast requires 3 ingredients and grants Master Survivalist."""
    feast = COOKING_RECIPES["grand_feast"]
    camp_scene = "bazaar_center"

    char_with_all = base_state.character.modify(
        inventory=list(base_state.character.inventory) + [
            "foraged_frost_lichen",
            "foraged_dune_succulent",
            "foraged_marsh_parsley",
        ],
        health=5,
        stamina=5,
    )
    state = base_state.evolve(
        character=char_with_all,
        current_scene=camp_scene,
        current_region="reach",
    )

    legal = engine.get_legal_actions(state)
    action_ids = [a.id for a in legal]
    assert feast.cook_action_id in action_ids

    # Cook Grand Feast
    state_after_cook, obs_cook = engine.step(state, feast.cook_action_id)
    assert obs_cook.success
    assert feast.cooked_item_id in state_after_cook.character.inventory
    assert "foraged_frost_lichen" not in state_after_cook.character.inventory

    # Eat Grand Feast
    state_after_eat, obs_eat = engine.step(state_after_cook, feast.eat_action_id)
    assert obs_eat.success
    assert "marker_master_survivalist" in state_after_eat.character.markers
    assert state_after_eat.character.health == 15
    assert state_after_eat.character.stamina == state_after_eat.character.max_stamina


def test_survival_progress_and_ranks() -> None:
    """Test survivalist ranks and defensive inventory handling."""
    # 0 meals -> Trail Wanderer
    prog0 = evaluate_survival_progress({}, inventory=[])
    assert prog0["rank_title"] == "Trail Wanderer"
    assert not prog0["is_cook"]

    # 1 meal -> Camp Cook
    prog1 = evaluate_survival_progress({"survival_meals_cooked": 1}, inventory=None)
    assert "Camp Cook" in prog1["rank_title"]
    assert prog1["is_cook"]

    # 3 meals -> Provincial Chef
    prog3 = evaluate_survival_progress({"survival_meals_cooked": 3}, inventory={"foraged_frost_lichen"})
    assert "Provincial Chef" in prog3["rank_title"]
    assert prog3["is_chef"]

    # 6 meals -> Continental Master Forager
    prog6 = evaluate_survival_progress({"survival_meals_cooked": 6}, inventory=("foraged_frost_lichen",))
    assert "Master Forager" in prog6["rank_title"]
    assert prog6["is_master"]


def test_survival_deterministic_replay(engine: AdventureEngine, base_state: GameState) -> None:
    """Test deterministic replay produces identical SHA-256 fingerprint with survival actions."""
    def run_trace(seed: int) -> str:
        preset = get_preset("warrior")
        state = GameState(
            build_id="af-m26-replay",
            session_id=f"test-survival-replay-{seed}",
            character=preset.character,
            current_region="reach",
            current_scene="reach_high_pass_gate",
            rng=DeterministicRNG.from_seed(seed),
        )
        # Step forage
        state, _ = engine.step(state, "survival_forage_high_pass")
        # Step move to camp
        state = state.evolve(current_scene="reach_timber_camp_quarters")
        # Step rest camp
        state, _ = engine.step(state, "survival_rest_camp")
        # Step cook stew
        state, _ = engine.step(state, "survival_cook_highland_stew")
        # Step eat stew
        state, _ = engine.step(state, "survival_eat_highland_stew")
        return state.fingerprint()

    fp1 = run_trace(42)
    fp2 = run_trace(42)
    assert fp1 == fp2, "Bit-for-bit SHA-256 fingerprint match required across deterministic runs"


def test_survival_asgi_endpoint() -> None:
    """Test ASGI serverless endpoint GET/HEAD at /api/game/survival and /api/game/new."""
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

    # 1. GET /api/game/survival
    res_get = asyncio.run(run_asgi("/api/game/survival", "GET"))
    assert res_get["status"] == 200
    assert any(k == b"content-type" and b"application/json" in v for k, v in res_get["headers"])
    body = json.loads(res_get["body"].decode("utf-8"))
    assert body["total_spots"] == 15
    assert len(body["spots"]) == 15
    assert body["total_recipes"] == 6
    assert len(body["recipes"]) == 6

    # 2. HEAD /api/game/survival
    res_head = asyncio.run(run_asgi("/api/game/survival", "HEAD"))
    assert res_head["status"] == 200
    assert res_head["body"] == b""

    # 3. POST /api/game/new includes survival progress
    new_req_body = json.dumps({"preset": "warrior", "seed": 42}).encode("utf-8")
    res_new = asyncio.run(run_asgi("/api/game/new", "POST", new_req_body))
    assert res_new["status"] == 200
    new_data = json.loads(res_new["body"].decode("utf-8"))
    assert "survival" in new_data
    assert new_data["survival"]["total_spots"] == 15
    assert new_data["survival"]["foraged_count"] == 0
    assert new_data["survival"]["meals_cooked"] == 0
    assert new_data["survival"]["rank_title"] == "Trail Wanderer"
