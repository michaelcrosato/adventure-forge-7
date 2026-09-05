"""Comprehensive Test Suite for Cycle 5: Regional Weather & Environmental Atmospheres.

Verifies:
- All 5 regional atmosphere definitions (Reach, Scorchwaste, Hollows, Lowlands, High Court).
- get_regional_atmosphere lookup, aliases, overrides, and suppression flags.
- Affordance synthesis for blizzard, heatwave, bioluminescence, miasma, and curfew.
- Character trait, item, and skill interactions for each atmospheric hazard.
- Entity atmosphere tags activating systemic affordances.
- Engine execution, state immutability, and deterministic fingerprint replay.
- 100% Hemingway prose compliance across descriptions, labels, results, and events.
"""
from typing import Dict, List, Optional

from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.actions import synthesize_affordances
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.state import GameState
from adventure_forge.content.schema import RegionManifest, SceneNode
from adventure_forge.linter.prose_linter import ProseLinter, word_count
from adventure_forge.core.hazards import (
    REGIONAL_ATMOSPHERES,
    get_regional_atmosphere,
    list_regional_atmospheres,
)


def _make_hero(
    traits: Optional[List[str]] = None,
    inventory: Optional[List[str]] = None,
    markers: Optional[List[str]] = None,
    skills: Optional[Dict[str, int]] = None,
    attributes: Optional[Dict[str, int]] = None,
    stamina: int = 10,
    health: int = 20,
) -> CharacterSheet:
    """Create a deterministic test character."""
    return CharacterSheet(
        name="Tester",
        ancestry="Plainsman",
        background="Drifter",
        attributes=attributes or {"strength": 10, "agility": 10, "endurance": 10},
        skills=skills or {"survival": 2, "cunning": 2, "stealth": 1},
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
# 1. Regional Atmosphere Definitions & Lookup Tests
# =============================================================================

def test_all_five_regional_atmospheres_defined():
    """All 5 regional atmospheres are registered with correct specs."""
    expected_atmospheres = {
        "blizzard": ("Blizzard", "reach"),
        "heatwave": ("Heatwave", "scorchwaste"),
        "bioluminescence": ("Bioluminescence", "sunken_hollows"),
        "miasma": ("Miasma", "lowlands"),
        "curfew": ("Curfew", "high_court"),
    }
    assert len(REGIONAL_ATMOSPHERES) == 5

    for atmo_id, (name, region) in expected_atmospheres.items():
        assert atmo_id in REGIONAL_ATMOSPHERES
        atmo = REGIONAL_ATMOSPHERES[atmo_id]
        assert atmo.id == atmo_id
        assert atmo.name == name
        assert atmo.region_id == region
        assert len(atmo.description) > 0
        assert isinstance(atmo.systemic_flags, dict)


def test_reach_blizzard_definition_specs():
    """Reach blizzard rewards climbing_rope and checks nimble or stamina."""
    atmo = REGIONAL_ATMOSPHERES["blizzard"]
    assert "climbing_rope" in atmo.rewarded_items
    assert "climbing_rope" in atmo.favored_items
    assert "nimble" in atmo.favored_traits
    assert "nimble" in atmo.checked_traits
    assert atmo.systemic_flags.get("weather") == "blizzard"
    assert atmo.systemic_flags.get("atmosphere_blizzard") is True


def test_scorchwaste_heatwave_definition_specs():
    """Scorchwaste heatwave rewards water_skin and checks heat_tolerant."""
    atmo = REGIONAL_ATMOSPHERES["heatwave"]
    assert "water_skin" in atmo.rewarded_items
    assert "water_skin" in atmo.favored_items
    assert "heat_tolerant" in atmo.favored_traits
    assert "heat_tolerant" in atmo.checked_traits
    assert atmo.systemic_flags.get("weather") == "heatwave"
    assert atmo.systemic_flags.get("atmosphere_heatwave") is True


def test_hollows_bioluminescence_definition_specs():
    """Hollows bioluminescence checks water_breather or night_eyed."""
    atmo = REGIONAL_ATMOSPHERES["bioluminescence"]
    assert "water_breather" in atmo.favored_traits
    assert "night_eyed" in atmo.favored_traits
    assert atmo.systemic_flags.get("weather") == "bioluminescence"
    assert atmo.systemic_flags.get("glowing_runes_revealed") is True


def test_lowlands_miasma_definition_specs():
    """Lowlands miasma checks iron_gutted trait and mask items."""
    atmo = REGIONAL_ATMOSPHERES["miasma"]
    assert "iron_gutted" in atmo.favored_traits
    assert "iron_gutted" in atmo.checked_traits
    assert any("mask" in item for item in atmo.favored_items)
    assert atmo.systemic_flags.get("weather") == "miasma"
    assert atmo.systemic_flags.get("atmosphere_miasma") is True


def test_high_court_curfew_definition_specs():
    """High Court curfew checks watch_crest item and stealth skill/trait."""
    atmo = REGIONAL_ATMOSPHERES["curfew"]
    assert "watch_crest" in atmo.favored_items
    assert "watch_crest" in atmo.rewarded_items
    assert "stealth" in atmo.favored_skills or "stealth" in atmo.checked_skills
    assert atmo.systemic_flags.get("weather") == "curfew"
    assert atmo.systemic_flags.get("martial_watch_active") is True


def test_regional_atmosphere_to_dict_and_list():
    """RegionalAtmosphere serializes cleanly and lists in deterministic order."""
    atmo = REGIONAL_ATMOSPHERES["blizzard"]
    d = atmo.to_dict()
    assert d["id"] == "blizzard"
    assert d["name"] == "Blizzard"
    assert d["region_id"] == "reach"
    assert isinstance(d["favored_items"], list)
    assert isinstance(d["favored_traits"], list)

    atmo_list = list_regional_atmospheres()
    assert len(atmo_list) == 5
    ids = [a.id for a in atmo_list]
    assert ids == sorted(ids)


def test_get_regional_atmosphere_aliases():
    """get_regional_atmosphere resolves region IDs, aliases, and direct names."""
    reach_atmo = get_regional_atmosphere("reach", {})
    assert reach_atmo is not None
    assert reach_atmo.id == "blizzard"
    prov_reach = get_regional_atmosphere("province_reach", {})
    assert prov_reach is not None
    assert prov_reach.id == "blizzard"
    the_reach = get_regional_atmosphere("the_reach", {})
    assert the_reach is not None
    assert the_reach.id == "blizzard"

    scorch_atmo = get_regional_atmosphere("scorchwaste", {})
    assert scorch_atmo is not None
    assert scorch_atmo.id == "heatwave"
    prov_scorch = get_regional_atmosphere("province_scorchwaste", {})
    assert prov_scorch is not None
    assert prov_scorch.id == "heatwave"
    scorch_local = get_regional_atmosphere("scorchwaste_local", {})
    assert scorch_local is not None
    assert scorch_local.id == "heatwave"

    hollows_atmo = get_regional_atmosphere("hollows", {})
    assert hollows_atmo is not None
    assert hollows_atmo.id == "bioluminescence"
    sunken = get_regional_atmosphere("sunken_hollows", {})
    assert sunken is not None
    assert sunken.id == "bioluminescence"
    prov_hollows = get_regional_atmosphere("province_sunken_hollows", {})
    assert prov_hollows is not None
    assert prov_hollows.id == "bioluminescence"

    lowlands_atmo = get_regional_atmosphere("lowlands", {})
    assert lowlands_atmo is not None
    assert lowlands_atmo.id == "miasma"
    prov_low = get_regional_atmosphere("province_lowlands", {})
    assert prov_low is not None
    assert prov_low.id == "miasma"

    court_atmo = get_regional_atmosphere("high_court", {})
    assert court_atmo is not None
    assert court_atmo.id == "curfew"
    prov_court = get_regional_atmosphere("province_high_court", {})
    assert prov_court is not None
    assert prov_court.id == "curfew"
    local_court = get_regional_atmosphere("court", {})
    assert local_court is not None
    assert local_court.id == "curfew"

    # Direct name resolution
    blizz = get_regional_atmosphere("blizzard", {})
    assert blizz is not None
    assert blizz.id == "blizzard"
    curf = get_regional_atmosphere("curfew", {})
    assert curf is not None
    assert curf.id == "curfew"

    # Unknown region returns None
    assert get_regional_atmosphere("iron_crags", {}) is None
    assert get_regional_atmosphere("unknown_region", {}) is None


def test_get_regional_atmosphere_suppression_and_overrides():
    """Atmosphere is suppressed by cleared/inactive flags and overridden by flags."""
    # Suppression flags
    assert get_regional_atmosphere("reach", {"blizzard_cleared": True}) is None
    assert get_regional_atmosphere("reach", {"blizzard_suppressed": True}) is None
    assert get_regional_atmosphere("reach", {"blizzard_active": False}) is None
    assert get_regional_atmosphere("scorchwaste", {"heatwave_cleared": True}) is None
    assert get_regional_atmosphere("lowlands", {"hazard_miasma_cleared": True}) is None
    assert get_regional_atmosphere("high_court", {"curfew_active": False}) is None

    # Weather override in an otherwise neutral region
    atmo = get_regional_atmosphere("iron_crags", {"weather": "blizzard"})
    assert atmo is not None
    assert atmo.id == "blizzard"


# =============================================================================
# 2. Blizzard Affordance Synthesis & Character Trait Interaction Tests
# =============================================================================

def test_blizzard_affordance_synthesis_with_climbing_rope():
    """Blizzard synthesizes Seek Shelter as item affordance with climbing_rope."""
    char = _make_hero(inventory=["climbing_rope"])
    actions = synthesize_affordances([], [], char, {}, region_id="reach")
    labels = [a.label for a in actions]
    assert "Seek Shelter" in labels
    assert "Brace Wind" in labels

    shelter_act = next(a for a in actions if a.label == "Seek Shelter")
    assert shelter_act.category == "item_affordance"
    assert shelter_act.risk == "low"
    assert shelter_act.stamina_cost == 0


def test_blizzard_affordance_synthesis_without_climbing_rope():
    """Blizzard synthesizes Seek Shelter as systemic action with stamina cost without rope."""
    char = _make_hero(inventory=[])
    actions = synthesize_affordances([], [], char, {}, region_id="reach")
    shelter_act = next(a for a in actions if a.label == "Seek Shelter")
    assert shelter_act.category == "systemic"
    assert shelter_act.risk == "medium"
    assert shelter_act.stamina_cost == 1


def test_blizzard_brace_wind_with_nimble_trait():
    """Character with nimble trait braces against wind with zero stamina drain."""
    char_nimble = _make_hero(traits=["nimble"])
    actions = synthesize_affordances([], [], char_nimble, {}, region_id="reach")
    brace_act = next(a for a in actions if a.label == "Brace Wind")
    assert brace_act.category == "trait_exploit"
    assert brace_act.risk == "low"
    assert brace_act.stamina_cost == 0


def test_blizzard_brace_wind_without_nimble_trait():
    """Character without nimble trait incurs stamina cost to brace against wind."""
    char_normal = _make_hero(traits=[], stamina=5)
    actions = synthesize_affordances([], [], char_normal, {}, region_id="reach")
    brace_act = next(a for a in actions if a.label == "Brace Wind")
    assert brace_act.category == "systemic"
    assert brace_act.risk == "medium"
    assert brace_act.stamina_cost == 1


def test_blizzard_stamina_depletion_legality():
    """Exhausted character without nimble cannot legally brace the wind."""
    char_exhausted = _make_hero(traits=[], stamina=0)
    actions = synthesize_affordances([], [], char_exhausted, {}, region_id="reach")
    labels = [a.label for a in actions]
    assert "Brace Wind" not in labels


# =============================================================================
# 3. Heatwave Affordance Synthesis & Character Trait Interaction Tests
# =============================================================================

def test_heatwave_drink_water_with_water_skin():
    """Heatwave synthesizes Drink Water as item affordance with water_skin."""
    char_hydrated = _make_hero(inventory=["water_skin"])
    actions = synthesize_affordances([], [], char_hydrated, {}, region_id="scorchwaste")
    labels = [a.label for a in actions]
    assert "Drink Water" in labels
    assert "Rest Shade" in labels

    drink_act = next(a for a in actions if a.label == "Drink Water")
    assert drink_act.category == "item_affordance"
    assert drink_act.risk == "low"
    assert drink_act.stamina_cost == 0


def test_heatwave_drink_water_without_water_skin():
    """Heatwave synthesizes Drink Water as systemic action with stamina cost if dry."""
    char_dry = _make_hero(inventory=[])
    actions = synthesize_affordances([], [], char_dry, {}, region_id="scorchwaste")
    drink_act = next(a for a in actions if a.label == "Drink Water")
    assert drink_act.category == "systemic"
    assert drink_act.risk == "medium"
    assert drink_act.stamina_cost == 1


def test_heatwave_rest_shade_with_heat_tolerant():
    """Character with heat_tolerant trait rests without risk or stamina drain."""
    char_hardened = _make_hero(traits=["heat_tolerant"])
    actions = synthesize_affordances([], [], char_hardened, {}, region_id="scorchwaste")
    shade_act = next(a for a in actions if a.label == "Rest Shade")
    assert shade_act.category == "trait_exploit"
    assert shade_act.risk == "low"
    assert shade_act.stamina_cost == 0


def test_heatwave_rest_shade_without_heat_tolerant():
    """Character without heat_tolerant trait incurs stamina drain while resting."""
    char_plain = _make_hero(traits=[])
    actions = synthesize_affordances([], [], char_plain, {}, region_id="scorchwaste")
    shade_act = next(a for a in actions if a.label == "Rest Shade")
    assert shade_act.category == "systemic"
    assert shade_act.risk == "medium"
    assert shade_act.stamina_cost == 1


# =============================================================================
# 4. Bioluminescence Affordance Synthesis & Trait Interaction Tests
# =============================================================================

def test_bioluminescence_inspect_glow_baseline():
    """Bioluminescence synthesizes Inspect Glow as safe systemic observation."""
    char = _make_hero()
    actions = synthesize_affordances([], [], char, {}, region_id="sunken_hollows")
    labels = [a.label for a in actions]
    assert "Inspect Glow" in labels
    assert "Decipher Runes" in labels

    inspect_act = next(a for a in actions if a.label == "Inspect Glow")
    assert inspect_act.category == "systemic"
    assert inspect_act.risk == "low"
    assert inspect_act.stamina_cost == 0


def test_bioluminescence_decipher_runes_with_water_breather():
    """Character with water_breather trait deciphers runes via trait exploit."""
    char_diver = _make_hero(traits=["water_breather"])
    actions = synthesize_affordances([], [], char_diver, {}, region_id="sunken_hollows")
    runes_act = next(a for a in actions if a.label == "Decipher Runes")
    assert runes_act.category == "trait_exploit"
    assert runes_act.risk == "low"
    assert runes_act.stamina_cost == 0
    assert any(
        eff.get("set_flag", {}).get("flag") == "glowing_runes_deciphered"
        and eff["set_flag"]["value"] is True
        for eff in runes_act.effects
    )


def test_bioluminescence_decipher_runes_with_night_eyed():
    """Character with night_eyed trait also deciphers runes as trait exploit."""
    char_nocturnal = _make_hero(traits=["night_eyed"])
    actions = synthesize_affordances([], [], char_nocturnal, {}, region_id="sunken_hollows")
    runes_act = next(a for a in actions if a.label == "Decipher Runes")
    assert runes_act.category == "trait_exploit"
    assert runes_act.risk == "low"
    assert runes_act.stamina_cost == 0


def test_bioluminescence_decipher_runes_without_traits():
    """Character without visual traits struggles to read runes with stamina cost."""
    char_blind = _make_hero(traits=[])
    actions = synthesize_affordances([], [], char_blind, {}, region_id="sunken_hollows")
    runes_act = next(a for a in actions if a.label == "Decipher Runes")
    assert runes_act.category == "systemic"
    assert runes_act.risk == "medium"
    assert runes_act.stamina_cost == 1


# =============================================================================
# 5. Miasma Affordance Synthesis & Character Trait Interaction Tests
# =============================================================================

def test_miasma_filter_air_with_mask():
    """Miasma synthesizes Filter Air as item affordance when equipped with mask."""
    char_masked = _make_hero(inventory=["mask"])
    actions = synthesize_affordances([], [], char_masked, {}, region_id="lowlands")
    labels = [a.label for a in actions]
    assert "Filter Air" in labels
    assert "Endure Fumes" in labels

    filter_act = next(a for a in actions if a.label == "Filter Air")
    assert filter_act.category == "item_affordance"
    assert filter_act.risk == "low"
    assert filter_act.stamina_cost == 0


def test_miasma_filter_air_with_plague_mask():
    """Miasma accepts specialized mask variants."""
    char_plague = _make_hero(inventory=["plague_mask"])
    actions = synthesize_affordances([], [], char_plague, {}, region_id="lowlands")
    filter_act = next(a for a in actions if a.label == "Filter Air")
    assert filter_act.category == "item_affordance"
    assert filter_act.risk == "low"


def test_miasma_filter_air_without_mask():
    """Miasma synthesizes Filter Air as systemic action with stamina cost without mask."""
    char_bare = _make_hero(inventory=[])
    actions = synthesize_affordances([], [], char_bare, {}, region_id="lowlands")
    filter_act = next(a for a in actions if a.label == "Filter Air")
    assert filter_act.category == "systemic"
    assert filter_act.risk == "medium"
    assert filter_act.stamina_cost == 1


def test_miasma_endure_fumes_with_iron_gutted():
    """Character with iron_gutted trait shrugs off toxic vapor with zero stamina cost."""
    char_iron = _make_hero(traits=["iron_gutted"])
    actions = synthesize_affordances([], [], char_iron, {}, region_id="lowlands")
    endure_act = next(a for a in actions if a.label == "Endure Fumes")
    assert endure_act.category == "trait_exploit"
    assert endure_act.risk == "low"
    assert endure_act.stamina_cost == 0


def test_miasma_endure_fumes_without_iron_gutted():
    """Character without iron_gutted trait suffers high risk and 2 stamina drain."""
    char_frail = _make_hero(traits=[], attributes={"endurance": 8}, stamina=5)
    actions = synthesize_affordances([], [], char_frail, {}, region_id="lowlands")
    endure_act = next(a for a in actions if a.label == "Endure Fumes")
    assert endure_act.category == "systemic"
    assert endure_act.risk == "high"
    assert endure_act.stamina_cost == 2


# =============================================================================
# 6. Curfew Affordance Synthesis & Character Trait Interaction Tests
# =============================================================================

def test_curfew_show_pass_with_watch_crest():
    """Curfew synthesizes Show Pass as item affordance with watch_crest."""
    char_official = _make_hero(inventory=["watch_crest"])
    actions = synthesize_affordances([], [], char_official, {}, region_id="high_court")
    labels = [a.label for a in actions]
    assert "Show Pass" in labels
    assert "Slip Shadows" in labels

    pass_act = next(a for a in actions if a.label == "Show Pass")
    assert pass_act.category == "item_affordance"
    assert pass_act.risk == "low"
    assert pass_act.stamina_cost == 0


def test_curfew_show_pass_with_watch_crest_marker():
    """Curfew synthesizes Show Pass if character has watch_crest marker."""
    char_marked = _make_hero(markers=["watch_crest"])
    actions = synthesize_affordances([], [], char_marked, {}, region_id="high_court")
    pass_act = next(a for a in actions if a.label == "Show Pass")
    assert pass_act.category == "item_affordance"
    assert pass_act.risk == "low"


def test_curfew_show_pass_without_crest():
    """Curfew synthesizes Show Pass as high risk social bluff without crest."""
    char_rogue = _make_hero(inventory=[])
    actions = synthesize_affordances([], [], char_rogue, {}, region_id="high_court")
    pass_act = next(a for a in actions if a.label == "Show Pass")
    assert pass_act.category == "social"
    assert pass_act.risk == "high"
    assert pass_act.stamina_cost == 1


def test_curfew_slip_shadows_with_stealth():
    """Character with high stealth slips past curfew patrol as trait exploit."""
    char_stealthy = _make_hero(skills={"stealth": 3})
    actions = synthesize_affordances([], [], char_stealthy, {}, region_id="high_court")
    slip_act = next(a for a in actions if a.label == "Slip Shadows")
    assert slip_act.category == "trait_exploit"
    assert slip_act.risk == "low"
    assert slip_act.stamina_cost == 0


def test_curfew_slip_shadows_without_stealth():
    """Character without stealth incurs medium risk and stamina cost to slip shadows."""
    char_clumsy = _make_hero(skills={"stealth": 0}, attributes={"agility": 8})
    actions = synthesize_affordances([], [], char_clumsy, {}, region_id="high_court")
    slip_act = next(a for a in actions if a.label == "Slip Shadows")
    assert slip_act.category == "systemic"
    assert slip_act.risk == "medium"
    assert slip_act.stamina_cost == 1


# =============================================================================
# 7. Entity Atmosphere Tags Tests
# =============================================================================

def test_scene_entity_with_atmosphere_tags_synthesizes_actions():
    """Scene entities with atmosphere tags trigger synthesis even without region."""
    char = _make_hero(inventory=["mask", "watch_crest"])
    entities = [
        {"id": "miasma_vent", "name": "Sewer Vent", "tags": ["miasma"]},
        {"id": "sentry_gate", "name": "Night Gate", "tags": ["curfew"]},
    ]

    actions = synthesize_affordances([], entities, char, {})
    labels = [a.label for a in actions]
    assert "Filter Air" in labels
    assert "Endure Fumes" in labels
    assert "Show Pass" in labels
    assert "Slip Shadows" in labels


def test_scene_entity_atmosphere_attribute_synthesizes_actions():
    """Scene entities with explicit atmosphere attribute trigger synthesis."""
    char = _make_hero()
    entities = [
        {"id": "frozen_rift", "name": "Chilled Crest", "atmosphere": "blizzard"},
    ]
    actions = synthesize_affordances([], entities, char, {})
    labels = [a.label for a in actions]
    assert "Seek Shelter" in labels
    assert "Brace Wind" in labels


# =============================================================================
# 8. Engine Determinism & Step Execution Invariant Tests
# =============================================================================

def test_engine_step_executes_regional_atmosphere_actions():
    """AdventureEngine steps through regional atmospheric actions deterministically."""
    char = _make_hero(inventory=["climbing_rope", "water_skin"], stamina=10)
    scene = SceneNode(
        id="pass_high",
        title="Biting Ridge",
        region="reach",
        description="Icy wind screams across the narrow rock spine.",
        entities=[],
        base_actions=[]
    )
    manifest = RegionManifest(
        id="reach",
        name="The Reach",
        mechanic_name="Verticality",
        mechanic_description="Icy mountain crags.",
        scenes={"pass_high": scene}
    )
    engine = AdventureEngine({"reach": manifest})
    state = GameState(
        build_id="test-build",
        session_id="session-atmo",
        character=char,
        current_region="reach",
        current_scene="pass_high",
        world_flags={}
    )

    legal_actions = engine.get_legal_actions(state)
    labels = [a.label for a in legal_actions]
    assert "Seek Shelter" in labels
    assert "Brace Wind" in labels

    # Step 1: Seek shelter
    new_state1, result1 = engine.step(state, "seek_shelter")
    assert result1.success is True
    assert new_state1.world_flags.get("blizzard_sheltered") is True

    # Replay determinism: identical state and action produces bit-for-bit fingerprint match
    new_state2, result2 = engine.step(state, "seek_shelter")
    assert new_state1.fingerprint() == new_state2.fingerprint()
    assert result1.fingerprint == result2.fingerprint

    # Immutability: original state untouched
    assert "blizzard_sheltered" not in state.world_flags


# =============================================================================
# 9. Hemingway Prose Linter Compliance
# =============================================================================

def test_regional_atmospheres_prose_linter_compliance():
    """All regional atmosphere descriptions strictly comply with Hemingway baseline."""
    linter = ProseLinter()
    for atmo in REGIONAL_ATMOSPHERES.values():
        errs = linter.lint_text(atmo.description)
        assert errs == [], f"Atmosphere '{atmo.id}' description failed linter: {errs}"


def test_synthesized_atmospheric_actions_prose_compliance():
    """All synthesized atmospheric action labels and result texts comply with Hemingway constraints."""
    linter = ProseLinter()
    char_equipped = _make_hero(
        traits=["nimble", "heat_tolerant", "water_breather", "iron_gutted", "night_eyed"],
        inventory=["climbing_rope", "water_skin", "mask", "watch_crest"],
        skills={"stealth": 3}
    )
    char_bare = _make_hero(traits=[], inventory=[], skills={"stealth": 0})

    for reg_id in ["reach", "scorchwaste", "sunken_hollows", "lowlands", "high_court"]:
        for c in [char_equipped, char_bare]:
            actions = synthesize_affordances([], [], c, {}, region_id=reg_id)
            assert len(actions) >= 2

            for action in actions:
                # 1. Label constraint: 1-3 words
                words = word_count(action.label)
                assert 1 <= words <= 3, f"Action label '{action.label}' has {words} words (expected 1-3)"

                # 2. Result text constraint: <= 18 words/sentence, zero purple words, readability <= 8.0
                if action.result_text:
                    errs = linter.lint_text(action.result_text)
                    assert errs == [], f"Action '{action.id}' result text '{action.result_text}' failed linter: {errs}"
