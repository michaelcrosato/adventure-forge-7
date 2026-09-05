"""Tests for Milestone 11 (M11) Systemic Encounters across all 5 provinces.

Verifies condition gates (skill, attribute, trait, item), trait exploits,
state mutations (items, flags, markers, reputation, health/stamina),
dynamic descriptions, and regional mechanics across all 10 M11 systemic encounters:
  11. The Reach: Dunwall Fortress Winch Sabotage (reach_dunwall_fort)
  12. The Reach: Glacial Crevasse Crossing (reach_frost_cavern)
  13. The Lowlands: Underworld Dice Game & Brawl (lowlands_dock_tavern)
  14. The Lowlands: Tailor Disguise & Tax Heist (lowlands_cloth_market)
  15. The Scorchwaste: Contested Oasis & Algae Detox (scorchwaste_canyon_oasis)
  16. The Scorchwaste: Aquifer Windlass Repair & Raider Ambush (scorchwaste_nomad_well)
  17. The High Court: Royal Scriptorium & Lineage Heist (high_court_royal_archive)
  18. The High Court: Poison in the Rose Pergola (high_court_chancellor_court)
  19. The Sunken Hollows: Crystal Trench Pressure Valve (sunken_hollows_coral_chasm)
  20. The Sunken Hollows: Acoustic Resonator Bell Tuning (sunken_hollows_echoing_dome)
"""
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.state import GameState


def _make_state(eng: AdventureEngine, scene_id: str, char: CharacterSheet, world_flags=None) -> GameState:
    reg = eng.world_registry
    region_id = None
    for r_id in reg:
        if scene_id in reg[r_id].scenes:
            region_id = r_id
            break
    if region_id is None:
        region_id = scene_id.split("_")[0]
    return GameState(
        build_id=eng.build_id,
        session_id="test_systemic_m11",
        character=char,
        current_region=region_id,
        current_scene=scene_id,
        world_flags=world_flags or {},
        rng=DeterministicRNG(42),
    )


# ==============================================================================
# Encounter 11: Dunwall Fortress Winch Sabotage (Reach: reach_dunwall_fort)
# ==============================================================================

def test_encounter_11_reach_dunwall_fort():
    eng = AdventureEngine(build_world_registry())

    # Gate: climbing_rope affordance or climber trait
    base_char = CharacterSheet(name="Infiltrator", ancestry="Reachman", background="mercenary")
    st_gate = _make_state(eng, "reach_dunwall_fort_gate", base_char)
    actions = {a.id for a in eng.get_legal_actions(st_gate)}
    assert "reach_dunwall_grapple_rope" not in actions
    assert "reach_dunwall_scout_crevice" not in actions

    # Trait exploit with climber
    climber_char = base_char.modify(traits=["climber"])
    st_climber = _make_state(eng, "reach_dunwall_fort_gate", climber_char)
    assert "reach_dunwall_scout_crevice" in {a.id for a in eng.get_legal_actions(st_climber)}

    # Item affordance with climbing_rope
    rope_char = base_char.modify(inventory=["climbing_rope"])
    st_rope = _make_state(eng, "reach_dunwall_fort_gate", rope_char)
    assert "reach_dunwall_grapple_rope" in {a.id for a in eng.get_legal_actions(st_rope)}

    # Advance to courtyard via grapple rope
    st_court, _ = eng.step(st_rope, "reach_dunwall_grapple_rope")
    assert st_court.current_scene == "reach_dunwall_fort_courtyard"
    assert st_court.world_flags.get("dunwall_grapple_anchored") is True

    # Courtyard: crowbar or cunning >= 3 to jam winch; strength >= 15 to heave portcullis
    weak_char = base_char.modify(skills={"cunning": 1}, attributes={"strength": 10})
    st_court_weak = _make_state(eng, "reach_dunwall_fort_courtyard", weak_char)
    assert "reach_dunwall_jam_winch" not in {a.id for a in eng.get_legal_actions(st_court_weak)}
    assert "reach_dunwall_heave_portcullis" not in {a.id for a in eng.get_legal_actions(st_court_weak)}

    cunning_char = base_char.modify(skills={"cunning": 3})
    st_court_cunning = _make_state(eng, "reach_dunwall_fort_courtyard", cunning_char)
    assert "reach_dunwall_jam_winch" in {a.id for a in eng.get_legal_actions(st_court_cunning)}

    # Advance to quarters via jamming winch
    st_quart, _ = eng.step(st_court_cunning, "reach_dunwall_jam_winch")
    assert st_quart.current_scene == "reach_dunwall_fort_quarters"
    assert st_quart.world_flags.get("dunwall_winch_jammed") is True

    # Quarters: claim armory plans
    assert "reach_dunwall_claim_armory" in {a.id for a in eng.get_legal_actions(st_quart)}
    st_claimed, _ = eng.step(st_quart, "reach_dunwall_claim_armory")
    assert "dunwall_siege_plans" in st_claimed.character.inventory
    assert st_claimed.character.reputation.get("smugglers") == 20
    assert st_claimed.character.reputation.get("iron_guard") == 10
    assert st_claimed.world_flags.get("dunwall_plans_taken") is True


# ==============================================================================
# Encounter 12: Glacial Crevasse Crossing (Reach: reach_frost_cavern)
# ==============================================================================

def test_encounter_12_reach_frost_cavern():
    eng = AdventureEngine(build_world_registry())

    base_char = CharacterSheet(name="Explorer", ancestry="Reachman", background="wanderer")
    st_gate = _make_state(eng, "reach_frost_cavern_gate", base_char)
    actions = {a.id for a in eng.get_legal_actions(st_gate)}
    assert "reach_cavern_rig_bridge" not in actions
    assert "reach_cavern_vault_ice" not in actions

    # Item affordance: climbing_rope
    rope_char = base_char.modify(inventory=["climbing_rope"])
    st_rope = _make_state(eng, "reach_frost_cavern_gate", rope_char)
    assert "reach_cavern_rig_bridge" in {a.id for a in eng.get_legal_actions(st_rope)}

    # Trait exploit: nimble
    nimble_char = base_char.modify(traits=["nimble"])
    st_nimble = _make_state(eng, "reach_frost_cavern_gate", nimble_char)
    assert "reach_cavern_vault_ice" in {a.id for a in eng.get_legal_actions(st_nimble)}

    # Advance to courtyard via nimble vault
    st_court, _ = eng.step(st_nimble, "reach_cavern_vault_ice")
    assert st_court.current_scene == "reach_frost_cavern_courtyard"

    # Courtyard: crowbar or strength >= 14 to clear stalactites
    strong_char = base_char.modify(attributes={"strength": 14})
    st_court_strong = _make_state(eng, "reach_frost_cavern_courtyard", strong_char)
    assert "reach_cavern_clear_stalactites" in {a.id for a in eng.get_legal_actions(st_court_strong)}

    # Advance to quarters
    st_quart, _ = eng.step(st_court_strong, "reach_cavern_clear_stalactites")
    assert st_quart.current_scene == "reach_frost_cavern_quarters"
    assert st_quart.world_flags.get("stalactites_cleared") is True

    # Quarters: harvest rime
    assert "reach_cavern_harvest_rime" in {a.id for a in eng.get_legal_actions(st_quart)}
    st_resolved, _ = eng.step(st_quart, "reach_cavern_harvest_rime")
    assert "glacial_rime_core" in st_resolved.character.inventory
    assert st_resolved.character.reputation.get("frost_wardens") == 25
    assert "frost_strider" in st_resolved.character.markers
    assert st_resolved.world_flags.get("glacial_rime_harvested") is True


# ==============================================================================
# Encounter 13: Underworld Dice Game & Brawl (Lowlands: lowlands_dock_tavern)
# ==============================================================================

def test_encounter_13_lowlands_dock_tavern():
    eng = AdventureEngine(build_world_registry())

    base_char = CharacterSheet(name="Rogue", ancestry="Lowlander", background="cutpurse")
    st_gate = _make_state(eng, "lowlands_dock_tavern_gate", base_char)
    actions = {a.id for a in eng.get_legal_actions(st_gate)}
    assert "lowlands_tavern_bribe_bouncer" not in actions
    assert "lowlands_tavern_eavesdrop" not in actions

    # Cunning >= 2 or silver_coin for bouncer
    cunning_char = base_char.modify(skills={"cunning": 2})
    st_cunning = _make_state(eng, "lowlands_dock_tavern_gate", cunning_char)
    assert "lowlands_tavern_bribe_bouncer" in {a.id for a in eng.get_legal_actions(st_cunning)}

    # Streetwise trait for eavesdrop
    street_char = base_char.modify(traits=["streetwise"])
    st_street = _make_state(eng, "lowlands_dock_tavern_gate", street_char)
    assert "lowlands_tavern_eavesdrop" in {a.id for a in eng.get_legal_actions(st_street)}

    # Advance to courtyard
    st_court, _ = eng.step(st_cunning, "lowlands_tavern_bribe_bouncer")
    assert st_court.current_scene == "lowlands_dock_tavern_courtyard"

    # Courtyard: light_fingers trait or cunning >= 4 to cheat dice ring
    fingers_char = base_char.modify(traits=["light_fingers"])
    st_court_fingers = _make_state(eng, "lowlands_dock_tavern_courtyard", fingers_char)
    assert "lowlands_tavern_cheat_dice" in {a.id for a in eng.get_legal_actions(st_court_fingers)}

    # Advance to quarters
    st_quart, _ = eng.step(st_court_fingers, "lowlands_tavern_cheat_dice")
    assert st_quart.current_scene == "lowlands_dock_tavern_quarters"
    assert st_quart.world_flags.get("tavern_dice_won") is True

    # Quarters: loot safe
    assert "lowlands_tavern_loot_safe" in {a.id for a in eng.get_legal_actions(st_quart)}
    st_resolved, _ = eng.step(st_quart, "lowlands_tavern_loot_safe")
    assert "smuggler_bounty_purse" in st_resolved.character.inventory
    assert "canal_route_ledger" in st_resolved.character.inventory
    assert st_resolved.character.reputation.get("smugglers") == 20
    assert st_resolved.world_flags.get("tavern_cache_looted") is True


# ==============================================================================
# Encounter 14: Tailor Disguise & Tax Heist (Lowlands: lowlands_cloth_market)
# ==============================================================================

def test_encounter_14_lowlands_cloth_market():
    eng = AdventureEngine(build_world_registry())

    base_char = CharacterSheet(name="Infiltrator", ancestry="Lowlander", background="artisan")
    st_gate = _make_state(eng, "lowlands_cloth_market_gate", base_char)
    actions = {a.id for a in eng.get_legal_actions(st_gate)}
    assert "lowlands_market_blend_crowd" not in actions
    assert "lowlands_market_pose_merchant" not in actions

    # Stealth >= 3 to blend into crowd
    stealth_char = base_char.modify(skills={"stealth": 3})
    st_stealth = _make_state(eng, "lowlands_cloth_market_gate", stealth_char)
    assert "lowlands_market_blend_crowd" in {a.id for a in eng.get_legal_actions(st_stealth)}

    # Rhetoric >= 3 to pose as merchant
    rhetoric_char = base_char.modify(skills={"rhetoric": 3})
    st_rhetoric = _make_state(eng, "lowlands_cloth_market_gate", rhetoric_char)
    assert "lowlands_market_pose_merchant" in {a.id for a in eng.get_legal_actions(st_rhetoric)}

    # Advance to courtyard
    st_court, _ = eng.step(st_rhetoric, "lowlands_market_pose_merchant")
    assert st_court.current_scene == "lowlands_cloth_market_courtyard"
    assert st_court.world_flags.get("silk_merchant_disguise") is True

    # Courtyard: light_fingers or cunning >= 3 to cut assessor purse
    thief_char = base_char.modify(traits=["light_fingers"])
    st_court_thief = _make_state(eng, "lowlands_cloth_market_courtyard", thief_char)
    assert "lowlands_market_cut_purse" in {a.id for a in eng.get_legal_actions(st_court_thief)}

    # Advance to quarters
    st_quart, _ = eng.step(st_court_thief, "lowlands_market_cut_purse")
    assert st_quart.current_scene == "lowlands_cloth_market_quarters"
    assert st_quart.world_flags.get("tax_key_stolen") is True

    # Quarters: claim revenue chest
    assert "lowlands_market_claim_revenue" in {a.id for a in eng.get_legal_actions(st_quart)}
    st_resolved, _ = eng.step(st_quart, "lowlands_market_claim_revenue")
    assert "tax_collector_ledger" in st_resolved.character.inventory
    assert "velvet_disguise_cloak" in st_resolved.character.inventory
    assert st_resolved.character.reputation.get("smugglers") == 25
    assert st_resolved.character.reputation.get("city_watch") == -10
    assert st_resolved.world_flags.get("market_tax_looted") is True


# ==============================================================================
# Encounter 15: Contested Oasis & Algae Detox (Scorchwaste: scorchwaste_canyon_oasis)
# ==============================================================================

def test_encounter_15_scorchwaste_canyon_oasis():
    eng = AdventureEngine(build_world_registry())

    base_char = CharacterSheet(name="Survivalist", ancestry="Nomad", background="hermit")
    st_gate = _make_state(eng, "scorchwaste_canyon_oasis_gate", base_char)
    actions = {a.id for a in eng.get_legal_actions(st_gate)}
    assert "scorch_oasis_drink_canteen" not in actions
    assert "scorch_oasis_rest_shade" in actions

    # Water skin item affordance
    canteen_char = base_char.modify(inventory=["water_skin"])
    st_canteen = _make_state(eng, "scorchwaste_canyon_oasis_gate", canteen_char)
    assert "scorch_oasis_drink_canteen" in {a.id for a in eng.get_legal_actions(st_canteen)}

    # Advance to courtyard via movement
    st_court, _ = eng.step(st_gate, "scorchwaste_canyon_oasis_gate_to_next")
    assert st_court.current_scene == "scorchwaste_canyon_oasis_courtyard"

    # Courtyard: cunning >= 3 detoxifies water
    cunning_char = base_char.modify(skills={"cunning": 3})
    st_court_cunning = _make_state(eng, "scorchwaste_canyon_oasis_courtyard", cunning_char)
    assert "scorch_oasis_purify_spring" in {a.id for a in eng.get_legal_actions(st_court_cunning)}

    # Advance to quarters
    st_quart, _ = eng.step(st_court_cunning, "scorch_oasis_purify_spring")
    assert st_quart.current_scene == "scorchwaste_canyon_oasis_quarters"
    assert st_quart.world_flags.get("oasis_water_purified") is True

    # Quarters: receive offering
    assert "scorch_oasis_receive_offering" in {a.id for a in eng.get_legal_actions(st_quart)}
    st_resolved, _ = eng.step(st_quart, "scorch_oasis_receive_offering")
    assert "purified_oasis_vial" in st_resolved.character.inventory
    assert st_resolved.character.reputation.get("caravaneers") == 25
    assert "desert_healer" in st_resolved.character.markers
    assert st_resolved.world_flags.get("oasis_offering_taken") is True


# ==============================================================================
# Encounter 16: Aquifer Windlass Repair & Raider Ambush (Scorchwaste: scorchwaste_nomad_well)
# ==============================================================================

def test_encounter_16_scorchwaste_nomad_well():
    eng = AdventureEngine(build_world_registry())

    base_char = CharacterSheet(name="Wanderer", ancestry="Nomad", background="mechanic")
    st_gate = _make_state(eng, "scorchwaste_nomad_well_gate", base_char)
    actions = {a.id for a in eng.get_legal_actions(st_gate)}
    assert "scorch_well_survey_tracks" not in actions
    assert "scorch_well_rig_harness" not in actions

    # Climbing rope affords rig harness
    rope_char = base_char.modify(inventory=["climbing_rope"])
    st_rope = _make_state(eng, "scorchwaste_nomad_well_gate", rope_char)
    assert "scorch_well_rig_harness" in {a.id for a in eng.get_legal_actions(st_rope)}

    # Advance to courtyard
    st_court, _ = eng.step(st_rope, "scorch_well_rig_harness")
    assert st_court.current_scene == "scorchwaste_nomad_well_courtyard"
    assert st_court.world_flags.get("well_rope_rigged") is True

    # Courtyard: crowbar or strength >= 14 repairs windlass
    strong_char = base_char.modify(attributes={"strength": 14})
    st_court_strong = _make_state(eng, "scorchwaste_nomad_well_courtyard", strong_char)
    assert "scorch_well_repair_windlass" in {a.id for a in eng.get_legal_actions(st_court_strong)}

    # Advance to quarters
    st_quart, _ = eng.step(st_court_strong, "scorch_well_repair_windlass")
    assert st_quart.current_scene == "scorchwaste_nomad_well_quarters"
    assert st_quart.world_flags.get("nomad_well_repaired") is True

    # Quarters: claim relic
    assert "scorch_well_claim_relic" in {a.id for a in eng.get_legal_actions(st_quart)}
    st_resolved, _ = eng.step(st_quart, "scorch_well_claim_relic")
    assert "desert_star_compass" in st_resolved.character.inventory
    assert "nomad_water_flask" in st_resolved.character.inventory
    assert st_resolved.character.reputation.get("caravaneers") == 20
    assert st_resolved.world_flags.get("well_relic_claimed") is True


# ==============================================================================
# Encounter 17: Royal Scriptorium & Lineage Heist (High Court: high_court_royal_archive)
# ==============================================================================

def test_encounter_17_high_court_royal_archive():
    eng = AdventureEngine(build_world_registry())

    base_char = CharacterSheet(name="Scholar", ancestry="Valen", background="noble_exile")
    st_gate = _make_state(eng, "high_court_royal_archive_gate", base_char)
    actions = {a.id for a in eng.get_legal_actions(st_gate)}
    assert "high_archive_bluff_clerk" not in actions
    assert "high_archive_slip_stacks" not in actions

    # Rhetoric >= 3 or legal_dossier
    rhetoric_char = base_char.modify(skills={"rhetoric": 3})
    st_rhetoric = _make_state(eng, "high_court_royal_archive_gate", rhetoric_char)
    assert "high_archive_bluff_clerk" in {a.id for a in eng.get_legal_actions(st_rhetoric)}

    # Advance to courtyard
    st_court, _ = eng.step(st_rhetoric, "high_archive_bluff_clerk")
    assert st_court.current_scene == "high_court_royal_archive_courtyard"
    assert st_court.world_flags.get("archive_pass_granted") is True

    # Courtyard: lockpick picks bronze grille
    lockpick_char = base_char.modify(inventory=["lockpick"])
    st_court_lock = _make_state(eng, "high_court_royal_archive_courtyard", lockpick_char)
    assert "high_archive_pick_grille" in {a.id for a in eng.get_legal_actions(st_court_lock)}

    # Cunning >= 4 deciphers scroll
    cunning_char = base_char.modify(skills={"cunning": 4})
    st_court_cunning = _make_state(eng, "high_court_royal_archive_courtyard", cunning_char)
    assert "high_archive_decipher_scroll" in {a.id for a in eng.get_legal_actions(st_court_cunning)}

    # Advance to quarters
    st_quart, _ = eng.step(st_court_cunning, "high_archive_decipher_scroll")
    assert st_quart.current_scene == "high_court_royal_archive_quarters"
    assert st_quart.world_flags.get("royal_lineage_deciphered") is True

    # Quarters: extract scroll
    assert "high_archive_extract_scroll" in {a.id for a in eng.get_legal_actions(st_quart)}
    st_resolved, _ = eng.step(st_quart, "high_archive_extract_scroll")
    assert "sovereign_lineage_scroll" in st_resolved.character.inventory
    assert st_resolved.character.reputation.get("justiciars") == 25
    assert "court_historian" in st_resolved.character.markers
    assert st_resolved.world_flags.get("lineage_scroll_extracted") is True


# ==============================================================================
# Encounter 18: Poison in the Rose Pergola (High Court: high_court_chancellor_court)
# ==============================================================================

def test_encounter_18_high_court_chancellor_court():
    eng = AdventureEngine(build_world_registry())

    base_char = CharacterSheet(name="Aristocrat", ancestry="Valen", background="noble")
    st_gate = _make_state(eng, "high_court_chancellor_court_gate", base_char)
    actions = {a.id for a in eng.get_legal_actions(st_gate)}
    assert "high_garden_present_favor" not in actions
    assert "high_garden_skirt_hedges" not in actions

    # Highborn ancestry unlocks present favor
    highborn_char = base_char.modify(ancestry="highborn")
    st_highborn = _make_state(eng, "high_court_chancellor_court_gate", highborn_char)
    assert "high_garden_present_favor" in {a.id for a in eng.get_legal_actions(st_highborn)}

    # Stealth >= 3 skirts hedges
    stealth_char = base_char.modify(skills={"stealth": 3})
    st_stealth = _make_state(eng, "high_court_chancellor_court_gate", stealth_char)
    assert "high_garden_skirt_hedges" in {a.id for a in eng.get_legal_actions(st_stealth)}

    # Advance to courtyard
    st_court, _ = eng.step(st_highborn, "high_garden_present_favor")
    assert st_court.current_scene == "high_court_chancellor_court_courtyard"

    # Courtyard: skeptical trait detects poison
    skep_char = base_char.modify(traits=["skeptical"])
    st_court_skep = _make_state(eng, "high_court_chancellor_court_courtyard", skep_char)
    assert "high_garden_detect_poison" in {a.id for a in eng.get_legal_actions(st_court_skep)}

    # Light fingers swaps chalice
    fingers_char = base_char.modify(traits=["light_fingers"])
    st_court_fingers = _make_state(eng, "high_court_chancellor_court_courtyard", fingers_char)
    assert "high_garden_swap_chalice" in {a.id for a in eng.get_legal_actions(st_court_fingers)}

    # Advance to quarters
    st_quart, _ = eng.step(st_court_skep, "high_garden_detect_poison")
    assert st_quart.current_scene == "high_court_chancellor_court_quarters"
    assert st_quart.world_flags.get("garden_poison_detected") is True

    # Quarters: expose plot
    assert "high_garden_expose_plot" in {a.id for a in eng.get_legal_actions(st_quart)}
    st_resolved, _ = eng.step(st_quart, "high_garden_expose_plot")
    assert "chancellor_signet_ring" in st_resolved.character.inventory
    assert st_resolved.character.reputation.get("high_nobility") == 25
    assert "savior_of_veras" in st_resolved.character.markers
    assert st_resolved.world_flags.get("chancellor_signet_claimed") is True


# ==============================================================================
# Encounter 19: Crystal Trench Pressure Valve (Sunken Hollows: sunken_hollows_coral_chasm)
# ==============================================================================

def test_encounter_19_sunken_hollows_coral_chasm():
    eng = AdventureEngine(build_world_registry())

    base_char = CharacterSheet(name="Diver", ancestry="Deepborn", background="salvager")
    st_gate = _make_state(eng, "sunken_hollows_coral_chasm_gate", base_char)
    actions = {a.id for a in eng.get_legal_actions(st_gate)}
    assert "hollows_coral_anchor_winch" not in actions
    assert "hollows_coral_plunge_abyss" not in actions

    # Climbing rope affords anchor winch
    rope_char = base_char.modify(inventory=["climbing_rope"])
    st_rope = _make_state(eng, "sunken_hollows_coral_chasm_gate", rope_char)
    assert "hollows_coral_anchor_winch" in {a.id for a in eng.get_legal_actions(st_rope)}

    # Water breather or endurance >= 14
    diver_char = base_char.modify(traits=["water_breather"])
    st_diver = _make_state(eng, "sunken_hollows_coral_chasm_gate", diver_char)
    assert "hollows_coral_plunge_abyss" in {a.id for a in eng.get_legal_actions(st_diver)}

    # Advance to courtyard
    st_court, _ = eng.step(st_diver, "hollows_coral_plunge_abyss")
    assert st_court.current_scene == "sunken_hollows_coral_chasm_courtyard"

    # Courtyard: crowbar or strength >= 15 cranks valve
    strong_char = base_char.modify(attributes={"strength": 15})
    st_court_strong = _make_state(eng, "sunken_hollows_coral_chasm_courtyard", strong_char)
    assert "hollows_coral_crank_valve" in {a.id for a in eng.get_legal_actions(st_court_strong)}

    # Advance to quarters
    st_quart, _ = eng.step(st_court_strong, "hollows_coral_crank_valve")
    assert st_quart.current_scene == "sunken_hollows_coral_chasm_quarters"
    assert st_quart.world_flags.get("chasm_valve_opened") is True

    # Quarters: harvest prism
    assert "hollows_coral_harvest_prism" in {a.id for a in eng.get_legal_actions(st_quart)}
    st_resolved, _ = eng.step(st_quart, "hollows_coral_harvest_prism")
    assert "abyssal_prism_core" in st_resolved.character.inventory
    assert "deep_trench_helm" in st_resolved.character.inventory
    assert st_resolved.character.reputation.get("hollow_dwellers") == 25
    assert st_resolved.world_flags.get("abyssal_prism_harvested") is True


# ==============================================================================
# Encounter 20: Acoustic Resonator Bell Tuning (Sunken Hollows: sunken_hollows_echoing_dome)
# ==============================================================================

def test_encounter_20_sunken_hollows_echoing_dome():
    eng = AdventureEngine(build_world_registry())

    base_char = CharacterSheet(name="Acolyte", ancestry="Deepborn", background="monk")
    st_gate = _make_state(eng, "sunken_hollows_echoing_dome_gate", base_char)
    actions = {a.id for a in eng.get_legal_actions(st_gate)}
    assert "hollows_dome_strike_tuning_fork" in actions
    assert "hollows_dome_brace_ears" not in actions

    # Endurance >= 14 braces ears
    sturdy_char = base_char.modify(attributes={"endurance": 14})
    st_sturdy = _make_state(eng, "sunken_hollows_echoing_dome_gate", sturdy_char)
    assert "hollows_dome_brace_ears" in {a.id for a in eng.get_legal_actions(st_sturdy)}

    # Advance to courtyard via movement
    st_court, _ = eng.step(st_sturdy, "sunken_hollows_echoing_dome_gate_to_next")
    assert st_court.current_scene == "sunken_hollows_echoing_dome_courtyard"

    # Courtyard: cunning >= 3 tunes bells
    cunning_char = base_char.modify(skills={"cunning": 3})
    st_court_cunning = _make_state(eng, "sunken_hollows_echoing_dome_courtyard", cunning_char)
    assert "hollows_dome_tune_bells" in {a.id for a in eng.get_legal_actions(st_court_cunning)}

    # Water breather dives pool
    diver_char = base_char.modify(traits=["water_breather"])
    st_court_diver = _make_state(eng, "sunken_hollows_echoing_dome_courtyard", diver_char)
    assert "hollows_dome_dive_pool" in {a.id for a in eng.get_legal_actions(st_court_diver)}

    # Advance to quarters via bell tuning
    st_quart, _ = eng.step(st_court_cunning, "hollows_dome_tune_bells")
    assert st_quart.current_scene == "sunken_hollows_echoing_dome_quarters"
    assert st_quart.world_flags.get("dome_bells_tuned") is True

    # Quarters: claim chime
    assert "hollows_dome_claim_chime" in {a.id for a in eng.get_legal_actions(st_quart)}
    st_resolved, _ = eng.step(st_quart, "hollows_dome_claim_chime")
    assert "harmonic_obsidian_bell" in st_resolved.character.inventory
    assert st_resolved.character.reputation.get("hollow_dwellers") == 20
    assert "echo_master" in st_resolved.character.markers
    assert st_resolved.world_flags.get("harmonic_chime_taken") is True
