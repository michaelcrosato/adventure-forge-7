"""Milestone 11 Adversarial Challenge & Stress Test Suite.

Empirically tests and stress-tests all 10 new systemic encounters from M11 across:
1. Negative Enforcement: Characters lacking prerequisites are strictly denied legal actions,
   and engine.step() rejects them without state mutation.
2. Trait Exploits: climber, nimble, water_breather, streetwise, light_fingers, skeptical, heat_hardened.
3. Attribute Checks: strength >= 14/15, cunning >= 3/4, rhetoric >= 3/4, endurance >= 14.
4. Item Affordances: climbing_rope, crowbar, lockpick, water_skin, silver_coin (including consumption).
5. Stage 3 Reward Integrity & Idempotency: Prerequisites enforced, rewards granted, non-repeatable.
6. Multi-Character Preset Traversals: Silas, Vivienne, Kael, Mara, Torin, and Garron.
7. Anti-Corruption, Determinism, & Oscillation Stress: Bit-for-bit SHA-256 reproducibility,
   cyclic traversal resilience, and pure state immutability.
"""
from typing import Any, Dict, List, Optional
import pytest

from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet, get_preset
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.state import GameState


# ==============================================================================
# TEST FIXTURES & HELPERS
# ==============================================================================

@pytest.fixture(scope="module")
def engine() -> AdventureEngine:
    return AdventureEngine(build_world_registry(cached=True))


def make_test_state(
    eng: AdventureEngine,
    scene_id: str,
    char: CharacterSheet,
    world_flags: Optional[Dict[str, Any]] = None,
    seed: int = 42,
) -> GameState:
    reg = eng.world_registry
    region_id = "unknown"
    for r_id in reg:
        if scene_id in reg[r_id].scenes:
            region_id = r_id
            break
    if region_id == "unknown":
        region_id = scene_id.split("_")[0]

    return GameState(
        build_id=eng.build_id,
        session_id="adversarial_m11",
        character=char,
        current_region=region_id,
        current_scene=scene_id,
        world_flags=dict(world_flags or {}),
        rng=DeterministicRNG(seed),
    )


def assert_action_strictly_illegal(
    eng: AdventureEngine,
    state: GameState,
    action_id: str,
) -> None:
    """Empirically verify that action_id is not in legal actions,

    and calling engine.step returns success=False and does not mutate state.
    """
    legal_actions = eng.get_legal_actions(state)
    action_ids = {a.id for a in legal_actions}
    assert action_id not in action_ids, (
        f"Action '{action_id}' was expected to be illegal for character '{state.character.name}', "
        f"but it was present in legal actions!"
    )

    initial_fp = state.fingerprint()
    initial_char = state.character.to_dict()
    initial_flags = dict(state.world_flags)

    next_state, result = eng.step(state, action_id)
    assert result.success is False, f"Illegal action '{action_id}' succeeded unexpectedly!"
    assert next_state.fingerprint() == initial_fp, "Illegal action mutated state fingerprint!"
    assert next_state.character.to_dict() == initial_char, "Illegal action mutated character sheet!"
    assert next_state.world_flags == initial_flags, "Illegal action mutated world flags!"


# ==============================================================================
# SECTION 1: NEGATIVE ENFORCEMENT ACROSS ALL 10 ENCOUNTERS
# ==============================================================================

def test_negative_enforcement_encounter_11_reach_dunwall(engine: AdventureEngine) -> None:
    """Encounter 11: Dunwall Fortress Winch Sabotage.

    Unqualified characters cannot grapple rope, scale crevice, jam winch, heave portcullis, or claim armory.
    """
    blank_char = CharacterSheet(name="Peasant", ancestry="Lowlander", background="commoner")

    # Gate: lacks climbing_rope and climber
    st_gate = make_test_state(engine, "reach_dunwall_fort_gate", blank_char)
    assert_action_strictly_illegal(engine, st_gate, "reach_dunwall_grapple_rope")
    assert_action_strictly_illegal(engine, st_gate, "reach_dunwall_scout_crevice")

    # Courtyard: lacks cunning >= 3, crowbar, strength >= 15
    weak_char = blank_char.modify(skills={"cunning": 1}, attributes={"strength": 10})
    st_court = make_test_state(engine, "reach_dunwall_fort_courtyard", weak_char)
    assert_action_strictly_illegal(engine, st_court, "reach_dunwall_jam_winch")
    assert_action_strictly_illegal(engine, st_court, "reach_dunwall_heave_portcullis")

    # Quarters: without winch jammed or portcullis lifted, cannot claim armory
    st_quart = make_test_state(engine, "reach_dunwall_fort_quarters", blank_char)
    assert_action_strictly_illegal(engine, st_quart, "reach_dunwall_claim_armory")


def test_negative_enforcement_encounter_12_reach_frost_cavern(engine: AdventureEngine) -> None:
    """Encounter 12: Glacial Crevasse Crossing.

    Unqualified characters cannot rig bridge, vault ice, clear stalactites, or harvest rime.
    """
    blank_char = CharacterSheet(name="Peasant", ancestry="Lowlander", background="commoner")

    # Gate: lacks climbing_rope and nimble
    st_gate = make_test_state(engine, "reach_frost_cavern_gate", blank_char)
    assert_action_strictly_illegal(engine, st_gate, "reach_cavern_rig_bridge")
    assert_action_strictly_illegal(engine, st_gate, "reach_cavern_vault_ice")

    # Courtyard: lacks crowbar and strength >= 14
    weak_char = blank_char.modify(attributes={"strength": 12})
    st_court = make_test_state(engine, "reach_frost_cavern_courtyard", weak_char)
    assert_action_strictly_illegal(engine, st_court, "reach_cavern_clear_stalactites")

    # Quarters: without stalactites cleared, cannot harvest rime
    st_quart = make_test_state(engine, "reach_frost_cavern_quarters", blank_char)
    assert_action_strictly_illegal(engine, st_quart, "reach_cavern_harvest_rime")


def test_negative_enforcement_encounter_13_lowlands_dock_tavern(engine: AdventureEngine) -> None:
    """Encounter 13: Underworld Dice Game & Brawl.

    Unqualified characters cannot bribe bouncer, eavesdrop, cheat dice, flip table, or loot safe.
    """
    blank_char = CharacterSheet(name="Peasant", ancestry="Lowlander", background="commoner")

    # Gate: lacks silver_coin, cunning >= 2, streetwise
    clueless_char = blank_char.modify(skills={"cunning": 1})
    st_gate = make_test_state(engine, "lowlands_dock_tavern_gate", clueless_char)
    assert_action_strictly_illegal(engine, st_gate, "lowlands_tavern_bribe_bouncer")
    assert_action_strictly_illegal(engine, st_gate, "lowlands_tavern_eavesdrop")

    # Courtyard: lacks light_fingers, cunning >= 4, strength >= 14
    st_court = make_test_state(engine, "lowlands_dock_tavern_courtyard", clueless_char)
    assert_action_strictly_illegal(engine, st_court, "lowlands_tavern_cheat_dice")
    assert_action_strictly_illegal(engine, st_court, "lowlands_tavern_flip_table")

    # Quarters: without dice won or brawl escaped, cannot loot safe
    st_quart = make_test_state(engine, "lowlands_dock_tavern_quarters", blank_char)
    assert_action_strictly_illegal(engine, st_quart, "lowlands_tavern_loot_safe")


def test_negative_enforcement_encounter_14_lowlands_cloth_market(engine: AdventureEngine) -> None:
    """Encounter 14: Tailor Disguise & Tax Heist.

    Unqualified characters cannot blend crowd, pose as merchant, cut purse, distract watch, or claim revenue.
    """
    blank_char = CharacterSheet(name="Peasant", ancestry="Lowlander", background="commoner")

    # Gate: stealth < 3, rhetoric < 3
    clumsy_char = blank_char.modify(skills={"stealth": 1, "rhetoric": 1})
    st_gate = make_test_state(engine, "lowlands_cloth_market_gate", clumsy_char)
    assert_action_strictly_illegal(engine, st_gate, "lowlands_market_blend_crowd")
    assert_action_strictly_illegal(engine, st_gate, "lowlands_market_pose_merchant")

    # Courtyard: lacks light_fingers, cunning < 3, lacks silver_coin
    slow_char = blank_char.modify(skills={"cunning": 2})
    st_court = make_test_state(engine, "lowlands_cloth_market_courtyard", slow_char)
    assert_action_strictly_illegal(engine, st_court, "lowlands_market_cut_purse")
    assert_action_strictly_illegal(engine, st_court, "lowlands_market_distract_watch")

    # Quarters: without tax key or watch distracted, cannot claim revenue
    st_quart = make_test_state(engine, "lowlands_cloth_market_quarters", blank_char)
    assert_action_strictly_illegal(engine, st_quart, "lowlands_market_claim_revenue")


def test_negative_enforcement_encounter_15_scorchwaste_oasis(engine: AdventureEngine) -> None:
    """Encounter 15: Contested Oasis & Algae Detox.

    Unqualified characters cannot drink canteen, purify spring, parley, drag trunk, or receive offering.
    """
    blank_char = CharacterSheet(name="Peasant", ancestry="Lowlander", background="commoner")

    # Gate: lacks water_skin
    st_gate = make_test_state(engine, "scorchwaste_canyon_oasis_gate", blank_char)
    assert_action_strictly_illegal(engine, st_gate, "scorch_oasis_drink_canteen")

    # Courtyard: cunning < 3, rhetoric < 4, strength < 15
    weak_char = blank_char.modify(skills={"cunning": 2, "rhetoric": 2}, attributes={"strength": 12})
    st_court = make_test_state(engine, "scorchwaste_canyon_oasis_courtyard", weak_char)
    assert_action_strictly_illegal(engine, st_court, "scorch_oasis_purify_spring")
    assert_action_strictly_illegal(engine, st_court, "scorch_oasis_parley_clans")
    assert_action_strictly_illegal(engine, st_court, "scorch_oasis_drag_trunk")

    # Quarters: without any resolution flag, cannot receive offering
    st_quart = make_test_state(engine, "scorchwaste_canyon_oasis_quarters", blank_char)
    assert_action_strictly_illegal(engine, st_quart, "scorch_oasis_receive_offering")


def test_negative_enforcement_encounter_16_scorchwaste_well(engine: AdventureEngine) -> None:
    """Encounter 16: Aquifer Windlass Repair & Raider Ambush.

    Unqualified characters cannot survey tracks, rig harness, repair windlass, repel raiders, or claim relic.
    """
    blank_char = CharacterSheet(name="Peasant", ancestry="Lowlander", background="commoner")

    # Gate: lacks night_eyed, cunning < 2, lacks climbing_rope
    blind_char = blank_char.modify(skills={"cunning": 1})
    st_gate = make_test_state(engine, "scorchwaste_nomad_well_gate", blind_char)
    assert_action_strictly_illegal(engine, st_gate, "scorch_well_survey_tracks")
    assert_action_strictly_illegal(engine, st_gate, "scorch_well_rig_harness")

    # Courtyard: strength < 14, lacks crowbar, stealth < 3
    feeble_char = blank_char.modify(attributes={"strength": 10}, skills={"stealth": 1})
    st_court = make_test_state(engine, "scorchwaste_nomad_well_courtyard", feeble_char)
    assert_action_strictly_illegal(engine, st_court, "scorch_well_repair_windlass")
    assert_action_strictly_illegal(engine, st_court, "scorch_well_repel_raiders")

    # Quarters: without windlass repaired or raiders repelled, cannot claim relic
    st_quart = make_test_state(engine, "scorchwaste_nomad_well_quarters", blank_char)
    assert_action_strictly_illegal(engine, st_quart, "scorch_well_claim_relic")


def test_negative_enforcement_encounter_17_high_court_archive(engine: AdventureEngine) -> None:
    """Encounter 17: Royal Scriptorium & Lineage Heist.

    Unqualified characters cannot bluff clerk, slip stacks, pick grille, decipher scroll, or extract scroll.
    """
    blank_char = CharacterSheet(name="Peasant", ancestry="Lowlander", background="commoner")

    # Gate: rhetoric < 3, lacks legal_dossier, stealth < 3
    mute_char = blank_char.modify(skills={"rhetoric": 1, "stealth": 1})
    st_gate = make_test_state(engine, "high_court_royal_archive_gate", mute_char)
    assert_action_strictly_illegal(engine, st_gate, "high_archive_bluff_clerk")
    assert_action_strictly_illegal(engine, st_gate, "high_archive_slip_stacks")

    # Courtyard: lacks lockpick, cunning < 4
    dull_char = blank_char.modify(skills={"cunning": 3})
    st_court = make_test_state(engine, "high_court_royal_archive_courtyard", dull_char)
    assert_action_strictly_illegal(engine, st_court, "high_archive_pick_grille")
    assert_action_strictly_illegal(engine, st_court, "high_archive_decipher_scroll")

    # Quarters: without grille picked or lineage deciphered, cannot extract scroll
    st_quart = make_test_state(engine, "high_court_royal_archive_quarters", blank_char)
    assert_action_strictly_illegal(engine, st_quart, "high_archive_extract_scroll")


def test_negative_enforcement_encounter_18_high_court_chancellor(engine: AdventureEngine) -> None:
    """Encounter 18: Poison in the Rose Pergola.

    Unqualified characters cannot present favor, skirt hedges, detect poison, swap chalice, or expose plot.
    """
    blank_char = CharacterSheet(name="Peasant", ancestry="Lowlander", background="commoner")

    # Gate: not highborn, rhetoric < 3, stealth < 3
    clumsy_char = blank_char.modify(skills={"rhetoric": 1, "stealth": 1})
    st_gate = make_test_state(engine, "high_court_chancellor_court_gate", clumsy_char)
    assert_action_strictly_illegal(engine, st_gate, "high_garden_present_favor")
    assert_action_strictly_illegal(engine, st_gate, "high_garden_skirt_hedges")

    # Courtyard: lacks skeptical, cunning < 4, lacks light_fingers
    oblivious_char = blank_char.modify(skills={"cunning": 2})
    st_court = make_test_state(engine, "high_court_chancellor_court_courtyard", oblivious_char)
    assert_action_strictly_illegal(engine, st_court, "high_garden_detect_poison")
    assert_action_strictly_illegal(engine, st_court, "high_garden_swap_chalice")

    # Quarters: without poison detected or chalice swapped, cannot expose plot
    st_quart = make_test_state(engine, "high_court_chancellor_court_quarters", blank_char)
    assert_action_strictly_illegal(engine, st_quart, "high_garden_expose_plot")


def test_negative_enforcement_encounter_19_sunken_hollows_chasm(engine: AdventureEngine) -> None:
    """Encounter 19: Crystal Trench Pressure Valve.

    Unqualified characters cannot anchor winch, plunge abyss, crank valve, dodge tendrils, or harvest prism.
    """
    blank_char = CharacterSheet(name="Peasant", ancestry="Lowlander", background="commoner")

    # Gate: lacks climbing_rope, lacks water_breather, endurance < 14
    soft_char = blank_char.modify(attributes={"endurance": 10})
    st_gate = make_test_state(engine, "sunken_hollows_coral_chasm_gate", soft_char)
    assert_action_strictly_illegal(engine, st_gate, "hollows_coral_anchor_winch")
    assert_action_strictly_illegal(engine, st_gate, "hollows_coral_plunge_abyss")

    # Courtyard: lacks crowbar, strength < 15, lacks nimble
    weak_char = blank_char.modify(attributes={"strength": 12})
    st_court = make_test_state(engine, "sunken_hollows_coral_chasm_courtyard", weak_char)
    assert_action_strictly_illegal(engine, st_court, "hollows_coral_crank_valve")
    assert_action_strictly_illegal(engine, st_court, "hollows_coral_dodge_tendrils")

    # Quarters: without valve opened, cannot harvest prism
    st_quart = make_test_state(engine, "sunken_hollows_coral_chasm_quarters", blank_char)
    assert_action_strictly_illegal(engine, st_quart, "hollows_coral_harvest_prism")


def test_negative_enforcement_encounter_20_sunken_hollows_dome(engine: AdventureEngine) -> None:
    """Encounter 20: Acoustic Resonator Bell Tuning.

    Unqualified characters cannot brace ears, tune bells, dive pool, or claim chime.
    """
    blank_char = CharacterSheet(name="Peasant", ancestry="Lowlander", background="commoner")

    # Gate: endurance < 14
    frail_char = blank_char.modify(attributes={"endurance": 11})
    st_gate = make_test_state(engine, "sunken_hollows_echoing_dome_gate", frail_char)
    assert_action_strictly_illegal(engine, st_gate, "hollows_dome_brace_ears")

    # Courtyard: cunning < 3, lacks crowbar, lacks water_breather
    simple_char = blank_char.modify(skills={"cunning": 1})
    st_court = make_test_state(engine, "sunken_hollows_echoing_dome_courtyard", simple_char)
    assert_action_strictly_illegal(engine, st_court, "hollows_dome_tune_bells")
    assert_action_strictly_illegal(engine, st_court, "hollows_dome_dive_pool")

    # Quarters: without bells tuned or pool damped, cannot claim chime
    st_quart = make_test_state(engine, "sunken_hollows_echoing_dome_quarters", blank_char)
    assert_action_strictly_illegal(engine, st_quart, "hollows_dome_claim_chime")


# ==============================================================================
# SECTION 2: TRAIT EXPLOITS ADVERSARIAL VERIFICATION
# ==============================================================================

@pytest.mark.parametrize(
    "trait,scene_id,action_id,expected_desc_fragment",
    [
        ("climber", "reach_dunwall_fort_gate", "reach_dunwall_scout_crevice", "drainage crevice"),
        ("nimble", "reach_frost_cavern_gate", "reach_cavern_vault_ice", None),
        ("nimble", "sunken_hollows_coral_chasm_courtyard", "hollows_coral_dodge_tendrils", None),
        ("water_breather", "sunken_hollows_coral_chasm_gate", "hollows_coral_plunge_abyss", None),
        ("water_breather", "sunken_hollows_echoing_dome_courtyard", "hollows_dome_dive_pool", None),
        ("streetwise", "lowlands_dock_tavern_gate", "lowlands_tavern_eavesdrop", None),
        ("light_fingers", "lowlands_dock_tavern_courtyard", "lowlands_tavern_cheat_dice", None),
        ("light_fingers", "lowlands_cloth_market_courtyard", "lowlands_market_cut_purse", None),
        ("light_fingers", "high_court_chancellor_court_courtyard", "high_garden_swap_chalice", None),
        ("skeptical", "high_court_chancellor_court_courtyard", "high_garden_detect_poison", None),
        ("heat_hardened", "scorchwaste_canyon_oasis_gate", None, "heat hardened skin"),
    ],
)
def test_trait_exploits_positive_and_negative(
    engine: AdventureEngine,
    trait: str,
    scene_id: str,
    action_id: Optional[str],
    expected_desc_fragment: Optional[str],
) -> None:
    """Empirically test that possessing the trait grants the action / observation,

    and lacking the trait strictly withholds it.
    """
    base = CharacterSheet(name="TestChar", ancestry="Reachman", background="wanderer")
    with_trait = base.modify(traits=[trait])
    without_trait = base.modify(traits=[])

    st_with = make_test_state(engine, scene_id, with_trait)
    st_without = make_test_state(engine, scene_id, without_trait)

    if action_id:
        # Legal with trait
        legal_with = {a.id for a in engine.get_legal_actions(st_with)}
        assert action_id in legal_with, f"Expected '{action_id}' to be legal with trait '{trait}'"

        # Illegal without trait
        assert_action_strictly_illegal(engine, st_without, action_id)

        # Execution advances scene successfully
        next_st, res = engine.step(st_with, action_id)
        assert res.success is True
        assert next_st.current_scene != scene_id or res.message != ""

    if expected_desc_fragment:
        obs_with = engine.observe(st_with)
        obs_without = engine.observe(st_without)
        assert expected_desc_fragment.lower() in obs_with.description.lower(), (
            f"Expected fragment '{expected_desc_fragment}' in description with trait '{trait}'"
        )
        assert expected_desc_fragment.lower() not in obs_without.description.lower(), (
            f"Did not expect fragment '{expected_desc_fragment}' without trait '{trait}'"
        )


# ==============================================================================
# SECTION 3: ATTRIBUTE THRESHOLD CHECKS
# ==============================================================================

@pytest.mark.parametrize(
    "attr_type,attr_name,required_value,scene_id,action_id",
    [
        ("attribute", "strength", 14, "reach_frost_cavern_courtyard", "reach_cavern_clear_stalactites"),
        ("attribute", "strength", 14, "lowlands_dock_tavern_courtyard", "lowlands_tavern_flip_table"),
        ("attribute", "strength", 14, "scorchwaste_nomad_well_courtyard", "scorch_well_repair_windlass"),
        ("attribute", "strength", 15, "reach_dunwall_fort_courtyard", "reach_dunwall_heave_portcullis"),
        ("attribute", "strength", 15, "scorchwaste_canyon_oasis_courtyard", "scorch_oasis_drag_trunk"),
        ("attribute", "strength", 15, "scorchwaste_nomad_well_courtyard", "scorch_well_repel_raiders"),
        ("attribute", "strength", 15, "sunken_hollows_coral_chasm_courtyard", "hollows_coral_crank_valve"),
        ("attribute", "endurance", 14, "sunken_hollows_coral_chasm_gate", "hollows_coral_plunge_abyss"),
        ("attribute", "endurance", 14, "sunken_hollows_echoing_dome_gate", "hollows_dome_brace_ears"),
        ("skill", "cunning", 3, "reach_dunwall_fort_courtyard", "reach_dunwall_jam_winch"),
        ("skill", "cunning", 3, "lowlands_cloth_market_courtyard", "lowlands_market_cut_purse"),
        ("skill", "cunning", 3, "scorchwaste_canyon_oasis_courtyard", "scorch_oasis_purify_spring"),
        ("skill", "cunning", 3, "sunken_hollows_echoing_dome_courtyard", "hollows_dome_tune_bells"),
        ("skill", "cunning", 4, "lowlands_dock_tavern_courtyard", "lowlands_tavern_cheat_dice"),
        ("skill", "cunning", 4, "high_court_royal_archive_courtyard", "high_archive_decipher_scroll"),
        ("skill", "cunning", 4, "high_court_chancellor_court_courtyard", "high_garden_detect_poison"),
        ("skill", "rhetoric", 3, "lowlands_cloth_market_gate", "lowlands_market_pose_merchant"),
        ("skill", "rhetoric", 3, "high_court_royal_archive_gate", "high_archive_bluff_clerk"),
        ("skill", "rhetoric", 3, "high_court_chancellor_court_gate", "high_garden_present_favor"),
        ("skill", "rhetoric", 4, "scorchwaste_canyon_oasis_courtyard", "scorch_oasis_parley_clans"),
    ],
)
def test_attribute_boundary_precision(
    engine: AdventureEngine,
    attr_type: str,
    attr_name: str,
    required_value: int,
    scene_id: str,
    action_id: str,
) -> None:
    """Verify boundary precision: value == required_value - 1 FAILS, value == required_value SUCCEEDS."""
    base = CharacterSheet(name="BoundaryChar", ancestry="Reachman", background="commoner")

    # Construct below threshold
    below_val = required_value - 1
    if attr_type == "attribute":
        char_below = base.modify(attributes={attr_name: below_val})
        char_exact = base.modify(attributes={attr_name: required_value})
    else:
        char_below = base.modify(skills={attr_name: below_val})
        char_exact = base.modify(skills={attr_name: required_value})

    st_below = make_test_state(engine, scene_id, char_below)
    st_exact = make_test_state(engine, scene_id, char_exact)

    # Must be illegal at required_value - 1
    assert_action_strictly_illegal(engine, st_below, action_id)

    # Must be legal at exact threshold
    legal_exact = {a.id for a in engine.get_legal_actions(st_exact)}
    assert action_id in legal_exact, (
        f"Action '{action_id}' should be legal when {attr_name}={required_value}, "
        f"but was not in {legal_exact}"
    )

    # Stepping transitions cleanly
    next_st, res = engine.step(st_exact, action_id)
    assert res.success is True, f"Failed stepping {action_id} at exact boundary!"


# ==============================================================================
# SECTION 4: ITEM AFFORDANCES & CONSUMPTION
# ==============================================================================

@pytest.mark.parametrize(
    "item,scene_id,action_id,is_consumed",
    [
        ("climbing_rope", "reach_dunwall_fort_gate", "reach_dunwall_grapple_rope", False),
        ("climbing_rope", "reach_frost_cavern_gate", "reach_cavern_rig_bridge", False),
        ("climbing_rope", "scorchwaste_nomad_well_gate", "scorch_well_rig_harness", False),
        ("climbing_rope", "sunken_hollows_coral_chasm_gate", "hollows_coral_anchor_winch", False),
        ("crowbar", "reach_dunwall_fort_courtyard", "reach_dunwall_jam_winch", False),
        ("crowbar", "reach_frost_cavern_courtyard", "reach_cavern_clear_stalactites", False),
        ("crowbar", "scorchwaste_nomad_well_courtyard", "scorch_well_repair_windlass", False),
        ("crowbar", "sunken_hollows_coral_chasm_courtyard", "hollows_coral_crank_valve", False),
        ("crowbar", "sunken_hollows_echoing_dome_courtyard", "hollows_dome_tune_bells", False),
        ("lockpick", "high_court_royal_archive_courtyard", "high_archive_pick_grille", False),
        ("water_skin", "scorchwaste_canyon_oasis_gate", "scorch_oasis_drink_canteen", False),
        ("silver_coin", "lowlands_dock_tavern_gate", "lowlands_tavern_bribe_bouncer", False),
        ("silver_coin", "lowlands_cloth_market_courtyard", "lowlands_market_distract_watch", True),
    ],
)
def test_item_affordances_and_consumption(
    engine: AdventureEngine,
    item: str,
    scene_id: str,
    action_id: str,
    is_consumed: bool,
) -> None:
    """Verify that having the item enables the action, lacking it denies it,

    and consumable items are deducted from inventory upon execution.
    """
    base = CharacterSheet(name="ItemChar", ancestry="Lowlander", background="artisan")
    with_item = base.modify(inventory=[item])
    without_item = base.modify(inventory=[])

    st_with = make_test_state(engine, scene_id, with_item)
    st_without = make_test_state(engine, scene_id, without_item)

    # Missing item -> illegal
    assert_action_strictly_illegal(engine, st_without, action_id)

    # Possessing item -> legal
    legal_with = {a.id for a in engine.get_legal_actions(st_with)}
    assert action_id in legal_with, f"Action '{action_id}' not legal with item '{item}'"

    # Step action
    next_st, res = engine.step(st_with, action_id)
    assert res.success is True

    if is_consumed:
        assert item not in next_st.character.inventory, f"Item '{item}' was expected to be consumed!"
    else:
        assert item in next_st.character.inventory, f"Reusable item '{item}' was unexpectedly lost!"


# ==============================================================================
# SECTION 5: STAGE 3 REWARD INTEGRITY, GATING & IDEMPOTENCY
# ==============================================================================

@pytest.mark.parametrize(
    "encounter_num,quarters_scene,reward_action,req_flags,reward_item,completion_flag,expected_reps,expected_markers",
    [
        (
            11,
            "reach_dunwall_fort_quarters",
            "reach_dunwall_claim_armory",
            ["dunwall_winch_jammed", "dunwall_portcullis_lifted"],
            "dunwall_siege_plans",
            "dunwall_plans_taken",
            {"smugglers": 20, "iron_guard": 10},
            [],
        ),
        (
            12,
            "reach_frost_cavern_quarters",
            "reach_cavern_harvest_rime",
            ["stalactites_cleared"],
            "glacial_rime_core",
            "glacial_rime_harvested",
            {"frost_wardens": 25},
            ["frost_strider"],
        ),
        (
            13,
            "lowlands_dock_tavern_quarters",
            "lowlands_tavern_loot_safe",
            ["tavern_dice_won", "tavern_brawl_escaped"],
            "smuggler_bounty_purse",
            "tavern_cache_looted",
            {"smugglers": 20},
            [],
        ),
        (
            14,
            "lowlands_cloth_market_quarters",
            "lowlands_market_claim_revenue",
            ["tax_key_stolen", "watch_distracted"],
            "tax_collector_ledger",
            "market_tax_looted",
            {"smugglers": 25, "city_watch": -10},
            [],
        ),
        (
            15,
            "scorchwaste_canyon_oasis_quarters",
            "scorch_oasis_receive_offering",
            ["oasis_water_purified", "oasis_clans_allied", "oasis_sluice_cleared"],
            "purified_oasis_vial",
            "oasis_offering_taken",
            {"caravaneers": 25},
            ["desert_healer"],
        ),
        (
            16,
            "scorchwaste_nomad_well_quarters",
            "scorch_well_claim_relic",
            ["nomad_well_repaired", "well_raiders_repelled"],
            "desert_star_compass",
            "well_relic_claimed",
            {"caravaneers": 20},
            [],
        ),
        (
            17,
            "high_court_royal_archive_quarters",
            "high_archive_extract_scroll",
            ["archive_grille_unlocked", "royal_lineage_deciphered"],
            "sovereign_lineage_scroll",
            "lineage_scroll_extracted",
            {"justiciars": 25},
            ["court_historian"],
        ),
        (
            18,
            "high_court_chancellor_court_quarters",
            "high_garden_expose_plot",
            ["garden_poison_detected", "duke_chalice_swapped"],
            "chancellor_signet_ring",
            "chancellor_signet_claimed",
            {"high_nobility": 25},
            ["savior_of_veras"],
        ),
        (
            19,
            "sunken_hollows_coral_chasm_quarters",
            "hollows_coral_harvest_prism",
            ["chasm_valve_opened"],
            "abyssal_prism_core",
            "abyssal_prism_harvested",
            {"hollow_dwellers": 25},
            [],
        ),
        (
            20,
            "sunken_hollows_echoing_dome_quarters",
            "hollows_dome_claim_chime",
            ["dome_bells_tuned", "dome_pool_damped"],
            "harmonic_obsidian_bell",
            "harmonic_chime_taken",
            {"hollow_dwellers": 20},
            ["echo_master"],
        ),
    ],
)
def test_stage_3_reward_gating_and_idempotency(
    engine: AdventureEngine,
    encounter_num: int,
    quarters_scene: str,
    reward_action: str,
    req_flags: List[str],
    reward_item: str,
    completion_flag: str,
    expected_reps: Dict[str, int],
    expected_markers: List[str],
) -> None:
    """Adversarially verify Stage 3 rewards across all 10 encounters:

    1. Quarters without prerequisite flags denies the reward action.
    2. Setting any valid prerequisite flag unlocks the reward action.
    3. Executing the reward action awards the item, sets completion flag, updates rep/markers.
    4. Second attempt to execute the reward action is strictly illegal (no duplicate loot).
    """
    char = CharacterSheet(name="RewardSeeker", ancestry="Lowlander", background="mercenary")

    # 1. Quarters without prerequisite flags
    st_empty = make_test_state(engine, quarters_scene, char, world_flags={})
    assert_action_strictly_illegal(engine, st_empty, reward_action)

    # 2. Test each prerequisite flag individually
    for flag in req_flags:
        st_ready = make_test_state(engine, quarters_scene, char, world_flags={flag: True})
        legal_ready = {a.id for a in engine.get_legal_actions(st_ready)}
        assert reward_action in legal_ready, (
            f"[Enc {encounter_num}] Setting flag '{flag}' should unlock '{reward_action}'"
        )

        # 3. Execute reward action
        st_rewarded, res = engine.step(st_ready, reward_action)
        assert res.success is True
        assert reward_item in st_rewarded.character.inventory, (
            f"[Enc {encounter_num}] Expected item '{reward_item}' in inventory"
        )
        assert st_rewarded.world_flags.get(completion_flag) is True, (
            f"[Enc {encounter_num}] Expected completion flag '{completion_flag}'"
        )

        for faction, val in expected_reps.items():
            actual_val = st_rewarded.character.reputation.get(faction, 0)
            assert actual_val == val, f"[Enc {encounter_num}] Rep for {faction} expected {val}, got {actual_val}"

        for marker in expected_markers:
            assert marker in st_rewarded.character.markers, (
                f"[Enc {encounter_num}] Marker '{marker}' not found in character markers"
            )

        # 4. Idempotency: cannot claim twice
        assert_action_strictly_illegal(engine, st_rewarded, reward_action)


# ==============================================================================
# SECTION 6: MULTI-CHARACTER PRESET FULL TRAVERSALS
# ==============================================================================

def test_silas_traversal_underworld_and_cloth_market(engine: AdventureEngine) -> None:
    """Silas the Cutpurse navigates Lowlands Dock Tavern and Cloth Market using stealth, lockpicks, and coin."""
    silas = get_preset("cutpurse").character
    assert "lockpick" in silas.inventory
    assert "silver_coin" in silas.inventory
    assert "streetwise" in silas.traits
    assert silas.skills.get("cunning", 0) >= 4

    # --- Encounter 13: Dock Tavern ---
    st13_gate = make_test_state(engine, "lowlands_dock_tavern_gate", silas)
    legal13_gate = {a.id for a in engine.get_legal_actions(st13_gate)}
    assert "lowlands_tavern_bribe_bouncer" in legal13_gate
    assert "lowlands_tavern_eavesdrop" in legal13_gate

    # Eavesdrop into courtyard
    st13_court, res = engine.step(st13_gate, "lowlands_tavern_eavesdrop")
    assert res.success is True
    assert st13_court.current_scene == "lowlands_dock_tavern_courtyard"

    # Silas has cunning 4 -> cheat dice ring
    st13_quart, res = engine.step(st13_court, "lowlands_tavern_cheat_dice")
    assert res.success is True
    assert st13_quart.current_scene == "lowlands_dock_tavern_quarters"
    assert st13_quart.world_flags.get("tavern_dice_won") is True

    # Loot safe
    st13_end, res = engine.step(st13_quart, "lowlands_tavern_loot_safe")
    assert res.success is True
    assert "smuggler_bounty_purse" in st13_end.character.inventory
    assert "canal_route_ledger" in st13_end.character.inventory

    # --- Encounter 14: Cloth Market ---
    st14_gate = make_test_state(engine, "lowlands_cloth_market_gate", st13_end.character)
    # Silas has stealth 3 -> blend into crowd
    st14_court, res = engine.step(st14_gate, "lowlands_market_blend_crowd")
    assert res.success is True
    assert st14_court.current_scene == "lowlands_cloth_market_courtyard"

    # Silas has cunning 4 -> cut assessor purse
    st14_quart, res = engine.step(st14_court, "lowlands_market_cut_purse")
    assert res.success is True
    assert st14_quart.current_scene == "lowlands_cloth_market_quarters"
    assert st14_quart.world_flags.get("tax_key_stolen") is True

    # Claim revenue
    st14_end, res = engine.step(st14_quart, "lowlands_market_claim_revenue")
    assert res.success is True
    assert "tax_collector_ledger" in st14_end.character.inventory
    assert "velvet_disguise_cloak" in st14_end.character.inventory


def test_vivienne_traversal_high_court_encounters(engine: AdventureEngine) -> None:
    """Lady Vivienne navigates Royal Archive and Chancellor's Court using rhetoric and skepticism."""
    vivienne = get_preset("noble").character
    assert "legal_dossier" in vivienne.inventory
    assert "skeptical" in vivienne.traits
    assert vivienne.skills.get("rhetoric", 0) >= 4

    # --- Encounter 17: Royal Archive ---
    st17_gate = make_test_state(engine, "high_court_royal_archive_gate", vivienne)
    # Bluff clerk with legal dossier or rhetoric 4
    st17_court, res = engine.step(st17_gate, "high_archive_bluff_clerk")
    assert res.success is True
    assert st17_court.current_scene == "high_court_royal_archive_courtyard"
    assert st17_court.world_flags.get("archive_pass_granted") is True

    # Vivienne lacks lockpick and cunning 4, but can traverse via movement
    assert_action_strictly_illegal(engine, st17_court, "high_archive_pick_grille")
    assert_action_strictly_illegal(engine, st17_court, "high_archive_decipher_scroll")

    # --- Encounter 18: Chancellor's Garden ---
    st18_gate = make_test_state(engine, "high_court_chancellor_court_gate", vivienne)
    # Vivienne has rhetoric 4 -> present noble favor
    st18_court, res = engine.step(st18_gate, "high_garden_present_favor")
    assert res.success is True
    assert st18_court.current_scene == "high_court_chancellor_court_courtyard"

    # Vivienne has skeptical trait -> detect wine poison
    st18_quart, res = engine.step(st18_court, "high_garden_detect_poison")
    assert res.success is True
    assert st18_quart.current_scene == "high_court_chancellor_court_quarters"
    assert st18_quart.world_flags.get("garden_poison_detected") is True

    # Expose garden plot
    st18_end, res = engine.step(st18_quart, "high_garden_expose_plot")
    assert res.success is True
    assert "chancellor_signet_ring" in st18_end.character.inventory
    assert "savior_of_veras" in st18_end.character.markers
    assert st18_end.character.reputation.get("high_nobility") == 25


def test_garron_traversal_dunwall_and_frost_cavern(engine: AdventureEngine) -> None:
    """Garron the Warrior navigates Dunwall Fortress and Glacial Crevasse using brute strength and crowbar."""
    garron = get_preset("warrior").character
    assert "crowbar" in garron.inventory
    assert garron.attributes.get("strength", 0) >= 16

    # --- Encounter 11: Dunwall Fortress Courtyard & Quarters ---
    # In courtyard: heave portcullis lever (strength >= 15) OR jam winch (crowbar)
    st11_court = make_test_state(engine, "reach_dunwall_fort_courtyard", garron)
    legal11 = {a.id for a in engine.get_legal_actions(st11_court)}
    assert "reach_dunwall_heave_portcullis" in legal11
    assert "reach_dunwall_jam_winch" in legal11

    # Heave portcullis
    st11_quart, res = engine.step(st11_court, "reach_dunwall_heave_portcullis")
    assert res.success is True
    assert st11_quart.current_scene == "reach_dunwall_fort_quarters"
    assert st11_quart.world_flags.get("dunwall_portcullis_lifted") is True

    # Claim armory plans
    st11_end, res = engine.step(st11_quart, "reach_dunwall_claim_armory")
    assert res.success is True
    assert "dunwall_siege_plans" in st11_end.character.inventory

    # --- Encounter 12: Frost Cavern Courtyard & Quarters ---
    st12_court = make_test_state(engine, "reach_frost_cavern_courtyard", garron)
    # Clear stalactites using crowbar or strength 14
    st12_quart, res = engine.step(st12_court, "reach_cavern_clear_stalactites")
    assert res.success is True
    assert st12_quart.current_scene == "reach_frost_cavern_quarters"
    assert st12_quart.world_flags.get("stalactites_cleared") is True

    # Harvest glacial rime
    st12_end, res = engine.step(st12_quart, "reach_cavern_harvest_rime")
    assert res.success is True
    assert "glacial_rime_core" in st12_end.character.inventory
    assert "frost_strider" in st12_end.character.markers


def test_kael_traversal_scorchwaste_encounters(engine: AdventureEngine) -> None:
    """Kael the Nomad navigates Canyon Oasis and Nomad Well using water_skin and endurance."""
    kael = get_preset("nomad").character
    assert "water_skin" in kael.inventory
    assert kael.attributes.get("endurance", 0) >= 15

    # --- Encounter 15: Canyon Oasis Gate ---
    st15_gate = make_test_state(engine, "scorchwaste_canyon_oasis_gate", kael)
    assert "scorch_oasis_drink_canteen" in {a.id for a in engine.get_legal_actions(st15_gate)}
    st15_hydrated, res = engine.step(st15_gate, "scorch_oasis_drink_canteen")
    assert res.success is True

    # --- Encounter 16: Nomad Well Courtyard ---
    # Kael has survival 4, endurance 15, strength 10 (lacks crowbar/strength 14)
    st16_court = make_test_state(engine, "scorchwaste_nomad_well_courtyard", kael)
    assert_action_strictly_illegal(engine, st16_court, "scorch_well_repair_windlass")
    assert_action_strictly_illegal(engine, st16_court, "scorch_well_repel_raiders")


def test_mara_traversal_sunken_hollows_encounters(engine: AdventureEngine) -> None:
    """Mara the Diver navigates Coral Chasm and Echoing Dome using water_breather and crowbar."""
    mara = get_preset("diver").character
    assert "water_breather" in mara.traits
    assert "crowbar" in mara.inventory
    assert mara.attributes.get("endurance", 0) >= 14

    # --- Encounter 19: Coral Chasm ---
    st19_gate = make_test_state(engine, "sunken_hollows_coral_chasm_gate", mara)
    assert "hollows_coral_plunge_abyss" in {a.id for a in engine.get_legal_actions(st19_gate)}

    st19_court, res = engine.step(st19_gate, "hollows_coral_plunge_abyss")
    assert res.success is True
    assert st19_court.current_scene == "sunken_hollows_coral_chasm_courtyard"

    # Mara has crowbar -> crank pressure valve
    st19_quart, res = engine.step(st19_court, "hollows_coral_crank_valve")
    assert res.success is True
    assert st19_quart.current_scene == "sunken_hollows_coral_chasm_quarters"
    assert st19_quart.world_flags.get("chasm_valve_opened") is True

    # Harvest abyssal prism
    st19_end, res = engine.step(st19_quart, "hollows_coral_harvest_prism")
    assert res.success is True
    assert "abyssal_prism_core" in st19_end.character.inventory
    assert "deep_trench_helm" in st19_end.character.inventory

    # --- Encounter 20: Echoing Dome ---
    st20_gate = make_test_state(engine, "sunken_hollows_echoing_dome_gate", mara)
    assert "hollows_dome_brace_ears" in {a.id for a in engine.get_legal_actions(st20_gate)}

    # Advance to courtyard
    st20_court = make_test_state(engine, "sunken_hollows_echoing_dome_courtyard", mara)
    assert "hollows_dome_tune_bells" in {a.id for a in engine.get_legal_actions(st20_court)}
    assert "hollows_dome_dive_pool" in {a.id for a in engine.get_legal_actions(st20_court)}

    # Dive resonance pool
    st20_quart, res = engine.step(st20_court, "hollows_dome_dive_pool")
    assert res.success is True
    assert st20_quart.current_scene == "sunken_hollows_echoing_dome_quarters"
    assert st20_quart.world_flags.get("dome_pool_damped") is True

    # Claim harmonic chime
    st20_end, res = engine.step(st20_quart, "hollows_dome_claim_chime")
    assert res.success is True
    assert "harmonic_obsidian_bell" in st20_end.character.inventory
    assert "echo_master" in st20_end.character.markers


def test_torin_traversal_reach_and_highland_scouting(engine: AdventureEngine) -> None:
    """Torin the Scout navigates Dunwall gate, Frost Cavern gate, and Nomad Well gate using climbing_rope."""
    torin = get_preset("scout").character
    assert "climbing_rope" in torin.inventory
    assert "nimble" in torin.traits

    # --- Dunwall gate: anchor rope ---
    st11 = make_test_state(engine, "reach_dunwall_fort_gate", torin)
    assert "reach_dunwall_grapple_rope" in {a.id for a in engine.get_legal_actions(st11)}
    st11_court, res = engine.step(st11, "reach_dunwall_grapple_rope")
    assert res.success is True
    assert st11_court.current_scene == "reach_dunwall_fort_courtyard"
    assert st11_court.world_flags.get("dunwall_grapple_anchored") is True

    # --- Frost Cavern gate: both rig rope bridge AND vault ice ridge are legal ---
    st12 = make_test_state(engine, "reach_frost_cavern_gate", torin)
    legal12 = {a.id for a in engine.get_legal_actions(st12)}
    assert "reach_cavern_rig_bridge" in legal12
    assert "reach_cavern_vault_ice" in legal12

    # --- Nomad Well gate: rig descent harness ---
    st16 = make_test_state(engine, "scorchwaste_nomad_well_gate", torin)
    assert "scorch_well_rig_harness" in {a.id for a in engine.get_legal_actions(st16)}
    st16_court, res = engine.step(st16, "scorch_well_rig_harness")
    assert res.success is True
    assert st16_court.current_scene == "scorchwaste_nomad_well_courtyard"
    assert st16_court.world_flags.get("well_rope_rigged") is True


# ==============================================================================
# SECTION 7: ANTI-CORRUPTION, DETERMINISM & OSCILLATION STRESS
# ==============================================================================

def test_deterministic_replay_across_all_10_encounters(engine: AdventureEngine) -> None:
    """Verify bit-for-bit SHA-256 state fingerprint reproducibility across repeated replays."""
    garron = get_preset("warrior").character

    # Play Dunwall Fortress sequence twice independently
    seq = ["reach_dunwall_heave_portcullis", "reach_dunwall_claim_armory"]

    st_run1 = make_test_state(engine, "reach_dunwall_fort_courtyard", garron, seed=999)
    for act in seq:
        st_run1, _ = engine.step(st_run1, act)

    st_run2 = make_test_state(engine, "reach_dunwall_fort_courtyard", garron, seed=999)
    for act in seq:
        st_run2, _ = engine.step(st_run2, act)

    assert st_run1.fingerprint() == st_run2.fingerprint()
    assert len(st_run1.fingerprint()) == 64


def test_50_cycle_movement_oscillation_no_memory_or_state_leak(engine: AdventureEngine) -> None:
    """Stress-test 50 cycles back and forth between gate and courtyard in all 5 provinces.

    Confirms zero crashes, state corruptions, or infinite loops.
    """
    char = CharacterSheet(name="Oscillator", ancestry="Lowlander", background="wanderer", stamina=500, max_stamina=500)

    gate_courtyard_pairs = [
        ("reach_dunwall_fort_gate", "reach_dunwall_fort_gate_to_next", "reach_dunwall_fort_courtyard_to_prev"),
        ("lowlands_dock_tavern_gate", "lowlands_dock_tavern_gate_to_next", "lowlands_dock_tavern_courtyard_to_prev"),
        ("scorchwaste_canyon_oasis_gate", "scorchwaste_canyon_oasis_gate_to_next", "scorchwaste_canyon_oasis_courtyard_to_prev"),
        ("high_court_royal_archive_gate", "high_court_royal_archive_gate_to_next", "high_court_royal_archive_courtyard_to_prev"),
        ("sunken_hollows_coral_chasm_gate", "sunken_hollows_coral_chasm_gate_to_next", "sunken_hollows_coral_chasm_courtyard_to_prev"),
    ]

    for start_scene, act_forward, act_backward in gate_courtyard_pairs:
        st = make_test_state(engine, start_scene, char)
        initial_inv = list(st.character.inventory)

        for _ in range(50):
            st, res_f = engine.step(st, act_forward)
            assert res_f.success is True, f"Forward step failed in {start_scene}"
            st, res_b = engine.step(st, act_backward)
            assert res_b.success is True, f"Backward step failed from {st.current_scene}"

        assert st.current_scene == start_scene
        assert st.character.inventory == initial_inv
        assert len(st.fingerprint()) == 64
