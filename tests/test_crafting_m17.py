"""Tests for Milestone 17: Master Field Crafting & Alchemical Synthesis System.

Validates:
- Ingredient requirements and inventory checks for all recipes.
- Dynamic crafting affordance synthesis in active scenes.
- Pure deterministic consumption of ingredients and item generation.
- Dynamic enable/disable of subsequent affordances (e.g. craft lockpick -> pick chest).
- Bit-for-bit SHA-256 state fingerprint reproducibility across crafting sequences.
- Strict Hemingway prose constraints, word count bounds, and label limits.
"""
from typing import List, Dict, Any
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.state import GameState
from adventure_forge.core.crafting import (
    CRAFTING_RECIPES,
    get_crafting_recipes,
)
from adventure_forge.linter.prose_linter import ProseLinter


def _create_test_engine() -> AdventureEngine:
    reg = build_world_registry()
    return AdventureEngine(reg, build_id="af-m17-test")


def _make_crafter(**overrides) -> CharacterSheet:
    base: Dict[str, Any] = {
        "name": "Artisan",
        "ancestry": "Plainsman",
        "background": "tinkerer",
        "attributes": {"strength": 10, "agility": 10, "endurance": 10, "cunning": 2},
        "skills": {"cunning": 2, "stealth": 1, "athletics": 1},
        "traits": [],
        "flaws": [],
        "reputation": {},
        "markers": [],
        "inventory": [],
        "health": 20,
        "max_health": 20,
        "stamina": 10,
        "max_stamina": 10,
    }
    base.update(overrides)
    return CharacterSheet(**base)


# ==============================================================================
# 1. Recipe Ingredient Availability & Validation
# ==============================================================================

def test_crafting_recipes_ingredient_requirements():
    """Recipes correctly evaluate ingredient availability and quantity checks."""
    recipes = get_crafting_recipes()
    assert len(CRAFTING_RECIPES) == len(recipes) == 10

    # Lockpick requires 1 scrap_metal + 1 flint
    rec_lock = recipes["lockpick"]
    char_empty = _make_crafter(inventory=[])
    assert not rec_lock.is_available(char_empty, {})

    char_partial = _make_crafter(inventory=["scrap_metal"])
    assert not rec_lock.is_available(char_partial, {})

    char_ready = _make_crafter(inventory=["scrap_metal", "flint"])
    assert rec_lock.is_available(char_ready, {})

    # Crowbar requires 2 scrap_metal
    rec_crow = recipes["crowbar"]
    assert not rec_crow.is_available(char_partial, {})  # only 1 scrap_metal

    char_two_scrap = _make_crafter(inventory=["scrap_metal", "scrap_metal"])
    assert rec_crow.is_available(char_two_scrap, {})


def test_crafting_stamina_cost_check():
    """Recipes requiring stamina are unavailable when stamina is exhausted."""
    rec_crow = get_crafting_recipes()["crowbar"]  # stamina_cost = 1

    char_tired = _make_crafter(inventory=["scrap_metal", "scrap_metal"], stamina=0)
    assert not rec_crow.is_available(char_tired, {})

    char_fresh = _make_crafter(inventory=["scrap_metal", "scrap_metal"], stamina=1)
    assert rec_crow.is_available(char_fresh, {})


# ==============================================================================
# 2. Dynamic Affordance Synthesis & Execution
# ==============================================================================

def test_crafting_affordance_synthesis_and_consumption():
    """Holding ingredients synthesizes crafting action; execution consumes materials and adds item."""
    eng = _create_test_engine()
    char = _make_crafter(inventory=["cloth_scraps", "pine_pitch", "bread_loaf"])

    state = GameState(
        build_id="af-m17-test",
        session_id="craft-test-1",
        character=char,
        current_region="iron_crags",
        current_scene="crags_base",
    )

    acts = {a.id: a for a in eng.get_legal_actions(state)}
    assert "craft_torch" in acts
    assert acts["craft_torch"].category == "crafting"
    assert acts["craft_torch"].label == "Craft Torch"

    # Step: Craft Torch
    state_after, obs = eng.step(state, "craft_torch")
    assert obs.success is True

    # Check inventory mutation
    assert "torch" in state_after.character.inventory
    assert "cloth_scraps" not in state_after.character.inventory
    assert "pine_pitch" not in state_after.character.inventory
    assert "bread_loaf" in state_after.character.inventory
    assert state_after.world_flags.get("crafted_torch") is True

    # Now that cloth_scraps and pine_pitch are spent, craft_torch is no longer legal
    acts_after = {a.id for a in eng.get_legal_actions(state_after)}
    assert "craft_torch" not in acts_after


def test_craft_then_use_downstream_affordance():
    """Crafting an item dynamically unlocks downstream systemic affordances."""
    eng = _create_test_engine()
    # Crafter has scrap metal and flint, but no lockpick
    char = _make_crafter(inventory=["scrap_metal", "flint"])

    state = GameState(
        build_id="af-m17-test",
        session_id="downstream-test",
        character=char,
        current_region="iron_crags",
        current_scene="crags_base",
    )

    # crags_base has an iron chest (entity_iron_chest)
    acts_0 = {a.id for a in eng.get_legal_actions(state)}
    assert "craft_lockpick" in acts_0
    # Because character does not have a lockpick and has low cunning, cannot pick chest yet
    assert "pick_iron_chest" not in acts_0

    # Craft the lockpick
    state_1, obs_1 = eng.step(state, "craft_lockpick")
    assert obs_1.success is True
    assert "lockpick" in state_1.character.inventory

    # Now pick_iron_chest is dynamically unlocked!
    acts_1 = {a.id for a in eng.get_legal_actions(state_1)}
    assert "pick_iron_chest" in acts_1

    # Execute picking the chest with the newly crafted tool
    state_2, obs_2 = eng.step(state_1, "pick_iron_chest")
    assert obs_2.success is True
    assert state_2.world_flags.get("entity_iron_chest_state") == "unlocked"


def test_crafting_all_ten_recipes():
    """All 10 crafting recipes can be executed cleanly, updating inventory and world flags."""
    eng = _create_test_engine()
    all_ingredients = [
        "scrap_metal", "flint",
        "cloth_scraps", "pine_pitch",
        "scrap_metal", "scrap_metal",
        "cloth_scraps", "charcoal",
        "algae_sample", "water_skin",
        "pine_pitch", "tallow",
        "cloth_scraps", "cloth_scraps",
        "cloth_scraps", "tallow",
        "sulfur_dust", "salt_crust", "empty_flask",
        "flint", "scrap_metal",
    ]

    char = _make_crafter(inventory=all_ingredients, stamina=10)
    state = GameState(
        build_id="af-m17-test",
        session_id="all-recipes-test",
        character=char,
        current_region="iron_crags",
        current_scene="crags_base",
    )

    recipes = get_crafting_recipes()
    for rec_id, rec in recipes.items():
        assert rec.action_id in {a.id for a in eng.get_legal_actions(state)}
        state, obs = eng.step(state, rec.action_id)
        assert obs.success is True, f"Failed crafting {rec_id}: {obs.message}"
        assert rec.produced_item in state.character.inventory
        assert state.world_flags.get(f"crafted_{rec.id}") is True


# ==============================================================================
# 3. Pure Deterministic Replay Verification
# ==============================================================================

def test_crafting_deterministic_replay():
    """Multi-step crafting and tool-use sequence yields bit-for-bit identical state fingerprints."""
    eng = _create_test_engine()
    char = _make_crafter(
        inventory=["scrap_metal", "flint", "cloth_scraps", "pine_pitch", "water_skin"],
        stamina=10,
    )

    def run_trace(seed: int, action_seq: List[str]) -> List[str]:
        st = GameState(
            build_id="af-m17-test",
            session_id=f"craft-det-{seed}",
            character=char,
            current_region="iron_crags",
            current_scene="crags_base",
            rng=DeterministicRNG.from_seed(seed),
        )
        fps = [st.fingerprint()]
        for a_id in action_seq:
            st, obs = eng.step(st, a_id)
            assert obs.success is True, f"Failed at {a_id}"
            fps.append(st.fingerprint())
        return fps

    actions = [
        "craft_lockpick",
        "craft_torch",
        "pick_iron_chest",
    ]

    fps1 = run_trace(seed=999, action_seq=actions)
    fps2 = run_trace(seed=999, action_seq=actions)

    assert fps1 == fps2
    assert len(fps1) == len(actions) + 1

    # Tamper check: altering the sequence alters fingerprints
    tampered = ["craft_torch", "craft_lockpick", "pick_iron_chest"]
    fps_tampered = run_trace(seed=999, action_seq=tampered)
    assert fps1 != fps_tampered


# ==============================================================================
# 4. Hemingway Prose & Action Label Quality Bar
# ==============================================================================

def test_crafting_prose_and_label_bounds():
    """All recipe labels, result texts, and log events satisfy Hemingway prose constraints."""
    linter = ProseLinter()
    recipes = get_crafting_recipes()

    for r_id, rec in recipes.items():
        # Action labels must be 1 to 3 words
        words = rec.label.split()
        assert 1 <= len(words) <= 3, f"{r_id} label '{rec.label}' exceeds 3 words ({len(words)} words)"

        # Result text must pass Hemingway prose linter
        errs_res = linter.lint_text(rec.result_text, context=f"{r_id}_result")
        assert not errs_res, f"Prose violations in {r_id} result: {errs_res}"

        # Log event must pass linter
        if rec.log_event:
            errs_evt = linter.lint_text(rec.log_event, context=f"{r_id}_event")
            assert not errs_evt, f"Prose violations in {r_id} log event: {errs_evt}"
