"""Comprehensive Test Suite for Environmental Hazards and Status Combos.

Verifies pure deterministic combo resolution, conditions DSL, effects DSL,
dynamic affordance synthesis, and Hemingway prose constraints.
"""
from typing import Dict, Any, List

from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.conditions import evaluate_condition
from adventure_forge.core.effects import apply_effects
from adventure_forge.core.actions import synthesize_affordances
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.state import GameState
from adventure_forge.content.schema import RegionManifest, SceneNode
from adventure_forge.linter.prose_linter import ProseLinter
from adventure_forge.core.hazards import (
    HazardCombo,
    HAZARD_COMBOS,
    normalize_element,
    get_hazard_combo,
    list_hazard_combos,
    resolve_hazard_combo,
    apply_hazard_combo,
)


def _make_hero(
    traits: List[str] | None = None,
    inventory: List[str] | None = None,
    markers: List[str] | None = None,
    skills: Dict[str, int] | None = None,
    stamina: int = 10,
    health: int = 20,
) -> CharacterSheet:
    """Create a minimal deterministic protagonist for testing."""
    return CharacterSheet(
        name="Tester",
        ancestry="Plainsman",
        background="Drifter",
        attributes={"strength": 10, "agility": 10, "endurance": 10},
        skills=skills if skills is not None else {"survival": 2, "cunning": 2},
        traits=traits or [],
        flaws=[],
        reputation={},
        markers=markers or [],
        inventory=inventory or [],
        health=health,
        max_health=20,
        stamina=stamina,
        max_stamina=10,
    )


# =============================================================================
# 1. Pure Deterministic Hazard Combos Resolver Tests
# =============================================================================

def test_oil_and_fire_conflagration_combo():
    """Oil and fire combine into a conflagration reaction."""
    combo = resolve_hazard_combo("oil", "fire")
    assert combo is not None
    assert combo.id == "conflagration"
    assert combo.resulting_status == "conflagration"
    assert combo.systemic_flags.get("oil_slick_incinerated") is True
    assert combo.systemic_flags.get("flammable_barriers_cleared") is True
    assert "oil" in combo.cleared_hazards


def test_conflagration_order_independence_and_aliases():
    """Reaction resolution is order independent and recognizes synonyms."""
    combo_rev = resolve_hazard_combo("fire", "oil")
    assert combo_rev is not None
    assert combo_rev.id == "conflagration"

    combo_alias1 = resolve_hazard_combo("oily", "flame")
    assert combo_alias1 is not None
    assert combo_alias1.id == "conflagration"

    combo_alias2 = resolve_hazard_combo(["oil_slick", "ignite"])
    assert combo_alias2 is not None
    assert combo_alias2.id == "conflagration"


def test_water_and_shock_stun_combo():
    """Water and shock combine into a stun reaction that disables sentries."""
    combo = resolve_hazard_combo("water", "shock")
    assert combo is not None
    assert combo.id == "stun"
    assert combo.resulting_status == "stun"
    assert combo.systemic_flags.get("sentries_disabled") is True
    assert combo.systemic_flags.get("sentry_active") is False
    assert combo.stamina_cost == 2


def test_stun_order_independence_and_aliases():
    """Stun combo resolves order independently with element aliases."""
    combo_rev = resolve_hazard_combo("shock", "water")
    assert combo_rev is not None
    assert combo_rev.id == "stun"

    combo_alias = resolve_hazard_combo("conductive_water", "lightning")
    assert combo_alias is not None
    assert combo_alias.id == "stun"

    combo_alias2 = resolve_hazard_combo("wet", "electric")
    assert combo_alias2 is not None
    assert combo_alias2.id == "stun"


def test_sandstorm_obscured_reaction():
    """Sandstorm hazard resolves into obscured stealth status."""
    combo = resolve_hazard_combo("sandstorm")
    assert combo is not None
    assert combo.id == "obscured"
    assert combo.resulting_status == "obscured"
    assert combo.systemic_flags.get("silhouette_obscured") is True
    assert combo.systemic_flags.get("stealth_enhanced") is True

    combo_alias = resolve_hazard_combo("grit")
    assert combo_alias is not None
    assert combo_alias.id == "obscured"


def test_acid_corrode_reaction():
    """Acid hazard resolves into corrode reaction dissolving locks and bars."""
    combo = resolve_hazard_combo("acid")
    assert combo is not None
    assert combo.id == "corrode"
    assert combo.resulting_status == "corrode"
    assert combo.systemic_flags.get("metal_locks_dissolved") is True
    assert combo.systemic_flags.get("iron_bars_dissolved") is True

    combo_alias = resolve_hazard_combo("acid_pool")
    assert combo_alias is not None
    assert combo_alias.id == "corrode"


def test_combo_resolver_edge_cases():
    """Unknown elements, empty args, and invalid IDs return None."""
    assert resolve_hazard_combo() is None
    assert resolve_hazard_combo([]) is None
    assert resolve_hazard_combo("unknown", "weird") is None
    assert get_hazard_combo("nonexistent") is None
    assert get_hazard_combo("") is None


def test_direct_combo_id_lookup():
    """Resolving by known combo identifier returns the combo definition."""
    for combo_id in ["conflagration", "stun", "obscured", "corrode"]:
        direct = get_hazard_combo(combo_id)
        assert direct is not None
        assert direct.id == combo_id
        resolved = resolve_hazard_combo(combo_id)
        assert resolved == direct


def test_list_hazard_combos_deterministic():
    """Listing all combos returns all four reactions in stable order."""
    combos = list_hazard_combos()
    assert len(combos) == 4
    ids = [c.id for c in combos]
    assert ids == ["conflagration", "corrode", "obscured", "stun"]


def test_element_normalization_utility():
    """Synonyms for elemental triggers normalize cleanly to canonical tokens."""
    assert normalize_element("OILY") == "oil"
    assert normalize_element("lightning") == "shock"
    assert normalize_element("flames") == "fire"
    assert normalize_element("acid_pool") == "acid"
    assert normalize_element("grit") == "sandstorm"


def test_hazard_combo_to_dict_serialization():
    """HazardCombo serializes to dictionary cleanly."""
    combo = HAZARD_COMBOS["conflagration"]
    assert isinstance(combo, HazardCombo)
    data = combo.to_dict()
    assert data["id"] == "conflagration"
    assert data["resulting_status"] == "conflagration"
    assert isinstance(data["required_elements"], list)
    assert isinstance(data["systemic_flags"], dict)


def test_apply_hazard_combo_deterministic_helper():
    """apply_hazard_combo updates character and world flags correctly."""
    char = _make_hero(stamina=10)
    combo = HAZARD_COMBOS["stun"]
    new_char, new_flags, events = apply_hazard_combo(combo, char, {})
    assert new_char.has_marker("stun")
    assert new_char.stamina == 8
    assert new_flags["status_stun"] is True
    assert new_flags["sentries_disabled"] is True
    assert len(events) == 1


# =============================================================================
# 2. Conditions DSL (has_status) Tests
# =============================================================================

def test_condition_has_status_via_character_marker():
    """has_status evaluates true when character holds the status marker."""
    char = _make_hero(markers=["stun"])
    assert evaluate_condition({"has_status": "stun"}, char, {})
    assert evaluate_condition({"has_status": {"status": "stun"}}, char, {})
    assert evaluate_condition({"has_status": {"status": "stun", "target": "character"}}, char, {})


def test_condition_has_status_via_world_flag():
    """has_status evaluates true when world flags indicate the status."""
    char = _make_hero()
    flags_bool = {"status_conflagration": True}
    assert evaluate_condition({"has_status": "conflagration"}, char, flags_bool)
    assert evaluate_condition({"has_status": {"status": "conflagration", "target": "world"}}, char, flags_bool)

    flags_list = {"statuses": ["obscured"]}
    assert evaluate_condition({"has_status": "obscured"}, char, flags_list)


def test_condition_has_status_targeting_boundaries():
    """has_status target filter strictly checks character or world."""
    char_with_marker = _make_hero(markers=["corrode"])
    empty_flags: Dict[str, Any] = {}

    # Target character matches
    assert evaluate_condition({"has_status": {"status": "corrode", "target": "character"}}, char_with_marker, empty_flags)
    # Target world does not match if only character has marker
    assert not evaluate_condition({"has_status": {"status": "corrode", "target": "world"}}, char_with_marker, empty_flags)

    char_clean = _make_hero()
    world_with_status = {"status_corrode": True}
    # Target world matches
    assert evaluate_condition({"has_status": {"status": "corrode", "target": "world"}}, char_clean, world_with_status)
    # Target character fails if only world has status
    assert not evaluate_condition({"has_status": {"status": "corrode", "target": "character"}}, char_clean, world_with_status)


def test_condition_has_status_negative_and_nested():
    """has_status evaluates false when absent and works inside boolean trees."""
    char = _make_hero(markers=["obscured"])
    flags = {"status_obscured": True}

    assert not evaluate_condition({"has_status": "stun"}, char, flags)

    nested_all = {
        "all_of": [
            {"has_status": "obscured"},
            {"min_skill": {"skill": "survival", "value": 1}}
        ]
    }
    assert evaluate_condition(nested_all, char, flags)

    nested_none = {
        "none_of": [
            {"has_status": "stun"}
        ]
    }
    assert evaluate_condition(nested_none, char, flags)


# =============================================================================
# 3. Effects DSL (apply_status and trigger_hazard) Tests
# =============================================================================

def test_effect_apply_status_custom_string():
    """apply_status adds marker to character and flag to world state."""
    char = _make_hero()
    effects = [{"apply_status": "blinded"}]
    new_char, new_flags, events, _ = apply_effects(effects, char, {})
    assert new_char.has_marker("blinded")
    assert new_flags["status_blinded"] is True
    assert "blinded" in new_flags["statuses"]
    assert any("blinded" in e for e in events)


def test_effect_apply_status_known_combo():
    """apply_status for a known combo triggers its systemic flags."""
    char = _make_hero(stamina=10)
    effects = [{"apply_status": "stun"}]
    new_char, new_flags, events, _ = apply_effects(effects, char, {})
    assert new_char.has_marker("stun")
    assert new_char.stamina == 8
    assert new_flags["sentries_disabled"] is True
    assert new_flags["sentry_active"] is False


def test_effect_trigger_hazard_with_catalyst_dict():
    """trigger_hazard resolves hazard and catalyst dict into conflagration."""
    char = _make_hero()
    flags = {"hazard_oil": True}
    effects = [{"trigger_hazard": {"hazard": "oil", "catalyst": "fire"}}]
    new_char, new_flags, events, _ = apply_effects(effects, char, flags)
    assert new_char.has_marker("conflagration")
    assert new_flags["status_conflagration"] is True
    assert new_flags["oil_slick_incinerated"] is True
    assert new_flags["flammable_barriers_cleared"] is True
    assert new_flags["hazard_oil_cleared"] is True
    assert new_flags["hazard_oil"] is False


def test_effect_trigger_hazard_single_string():
    """trigger_hazard resolves single hazard string into corrosion."""
    char = _make_hero()
    effects = [{"trigger_hazard": "acid"}]
    new_char, new_flags, events, _ = apply_effects(effects, char, {})
    assert new_char.has_marker("corrode")
    assert new_flags["status_corrode"] is True
    assert new_flags["metal_locks_dissolved"] is True
    assert new_flags["iron_bars_dissolved"] is True


def test_effect_trigger_hazard_unknown_raw_hazard():
    """trigger_hazard with an unregistered hazard records a generic active hazard."""
    char = _make_hero()
    effects = [{"trigger_hazard": "poison_spores"}]
    _, new_flags, events, _ = apply_effects(effects, char, {})
    assert new_flags.get("hazard_poison_spores") is True
    assert any("poison_spores" in e for e in events)


# =============================================================================
# 4. Action Affordance Synthesis Tests (oily, conductive_water, sandstorm, acid_pool)
# =============================================================================

def test_oily_affordance_generation_with_and_without_fire():
    """Oily tag offers ignite action if equipped with fire, or examine if not."""
    char_pyro = _make_hero(inventory=["torch"])
    char_unarmed = _make_hero(inventory=[])

    entities = [
        {"id": "slick_1", "name": "Oil Slick", "tags": ["oily"], "initial_state": "intact"}
    ]

    actions_pyro = synthesize_affordances([], entities, char_pyro, {})
    actions_unarmed = synthesize_affordances([], entities, char_unarmed, {})

    pyro_ids = [a.id for a in actions_pyro]
    unarmed_ids = [a.id for a in actions_unarmed]

    assert "ignite_slick_1" in pyro_ids
    assert "ignite_slick_1" not in unarmed_ids
    assert "examine_slick_1" in unarmed_ids

    ignite_act = next(a for a in actions_pyro if a.id == "ignite_slick_1")
    assert ignite_act.label == "Ignite Oil Slick"
    assert len(ignite_act.label.split()) <= 3
    assert ignite_act.risk == "high"


def test_conductive_water_affordance_generation():
    """Conductive water offers shock action if equipped with shock item."""
    char_shock = _make_hero(inventory=["shock_stone"])
    char_wader = _make_hero(inventory=[])

    entities = [
        {"id": "water_pool", "name": "Deep Pool", "tags": ["conductive_water"], "initial_state": "intact"}
    ]

    actions_shock = synthesize_affordances([], entities, char_shock, {})
    actions_wader = synthesize_affordances([], entities, char_wader, {})

    shock_ids = [a.id for a in actions_shock]
    wader_ids = [a.id for a in actions_wader]

    assert "shock_water_pool" in shock_ids
    assert "wade_water_pool" in wader_ids
    assert "shock_water_pool" not in wader_ids

    shock_act = next(a for a in actions_shock if a.id == "shock_water_pool")
    assert shock_act.label == "Shock Deep Pool"
    assert len(shock_act.label.split()) <= 3
    assert shock_act.stamina_cost == 2


def test_sandstorm_affordance_generation():
    """Sandstorm tag generates brave action with cloak mitigating risk."""
    char_cloaked = _make_hero(inventory=["cloak"])
    char_bare = _make_hero(inventory=[])

    entities = [
        {"id": "storm_1", "name": "Sandstorm", "tags": ["sandstorm"], "initial_state": "active"}
    ]

    actions_cloaked = synthesize_affordances([], entities, char_cloaked, {})
    actions_bare = synthesize_affordances([], entities, char_bare, {})

    cloaked_act = next(a for a in actions_cloaked if a.id == "brave_storm_1")
    bare_act = next(a for a in actions_bare if a.id == "brave_storm_1")

    assert cloaked_act.label == "Brave Sandstorm"
    assert len(cloaked_act.label.split()) <= 3
    assert cloaked_act.risk == "low"
    assert cloaked_act.stamina_cost == 0

    assert bare_act.risk == "medium"
    assert bare_act.stamina_cost == 1


def test_acid_pool_affordance_generation():
    """Acid pool tag generates apply action and optional bottle action."""
    char_with_vial = _make_hero(inventory=["vial"])
    char_plain = _make_hero(inventory=[])

    entities = [
        {"id": "vat_1", "name": "Acid Pool", "tags": ["acid_pool"], "initial_state": "intact"}
    ]

    actions_vial = synthesize_affordances([], entities, char_with_vial, {})
    actions_plain = synthesize_affordances([], entities, char_plain, {})

    vial_ids = [a.id for a in actions_vial]
    plain_ids = [a.id for a in actions_plain]

    assert "corrode_vat_1" in vial_ids
    assert "bottle_vat_1" in vial_ids
    assert "corrode_vat_1" in plain_ids
    assert "bottle_vat_1" not in plain_ids

    corrode_act = next(a for a in actions_plain if a.id == "corrode_vat_1")
    assert corrode_act.label == "Apply Acid Pool"
    assert len(corrode_act.label.split()) <= 3


# =============================================================================
# 5. Engine Transition and Determinism Invariants
# =============================================================================

def test_engine_step_executes_hazard_combo_deterministically():
    """AdventureEngine transitions through hazard actions with pure determinism."""
    char = _make_hero(inventory=["torch"], stamina=10)
    scene = SceneNode(
        id="oil_room",
        title="Oily Chamber",
        region="dungeon",
        description="Crude oil pools on dark stone. Flammable wooden scaffolding lines the north wall.",
        entities=[
            {"id": "slick", "name": "Oil Pool", "tags": ["oily"], "initial_state": "intact"}
        ],
        base_actions=[]
    )
    manifest = RegionManifest(
        id="dungeon",
        name="Forgotten Vaults",
        mechanic_name="Hazards",
        mechanic_description="Ancient stone vaults buried underground.",
        scenes={"oil_room": scene}
    )
    engine = AdventureEngine({"dungeon": manifest})
    state = GameState(
        build_id="test-build",
        session_id="session-hazard",
        character=char,
        current_region="dungeon",
        current_scene="oil_room",
        world_flags={}
    )

    legal_actions = engine.get_legal_actions(state)
    assert any(a.id == "ignite_slick" for a in legal_actions)

    new_state1, result1 = engine.step(state, "ignite_slick")
    assert result1.success is True
    assert new_state1.character.has_marker("conflagration")
    assert new_state1.world_flags["oil_slick_incinerated"] is True
    assert new_state1.world_flags["flammable_barriers_cleared"] is True

    # Determinism replay: repeated step produces identical canonical state fingerprint
    new_state2, result2 = engine.step(state, "ignite_slick")
    assert new_state1.fingerprint() == new_state2.fingerprint()
    assert result1.fingerprint == result2.fingerprint

    # Immutability: original state was not mutated in place
    assert not state.character.has_marker("conflagration")
    assert "oil_slick_incinerated" not in state.world_flags


# =============================================================================
# 6. Prose Linter Constraints (Hemingway Baseline Verification)
# =============================================================================

def test_all_hazard_combos_pass_hemingway_linter():
    """All hazard combo descriptions strictly comply with Hemingway constraints."""
    linter = ProseLinter()
    for combo in HAZARD_COMBOS.values():
        errs = linter.lint_text(combo.description)
        assert errs == [], f"Combo '{combo.id}' description failed linter: {errs}"


def test_all_environmental_affordances_pass_hemingway_linter():
    """All synthesized hazard affordance labels and texts pass Hemingway constraints."""
    linter = ProseLinter()
    char = _make_hero(inventory=["torch", "shock_stone", "cloak", "vial"])
    entities = [
        {"id": "e_oil", "name": "Oil Slick", "tags": ["oily"]},
        {"id": "e_water", "name": "Deep Pool", "tags": ["conductive_water"]},
        {"id": "e_storm", "name": "Sandstorm", "tags": ["sandstorm"]},
        {"id": "e_acid", "name": "Acid Pool", "tags": ["acid_pool"]},
    ]

    actions = synthesize_affordances([], entities, char, {})
    assert len(actions) >= 4

    for action in actions:
        # Check action label: 1-3 words
        label_words = len(action.label.split())
        assert 1 <= label_words <= 3, f"Action label '{action.label}' has {label_words} words"

        # Check result text: Hemingway readability and word bounds
        if action.result_text:
            errs = linter.lint_text(action.result_text)
            assert errs == [], f"Action '{action.id}' result text failed linter: {errs}"
