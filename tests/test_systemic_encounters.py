"""Tests for M7 Systemic Encounters across all 5 provinces.

Verifies condition gates (skill, attribute, trait, item), trait exploits,
state mutations (items, flags, markers, reputation, health/stamina),
dynamic descriptions, and regional mechanics across all 10 systemic encounters:
  1. The Reach: Eagle Wing Pass (reach_high_pass)
  2. The Reach: Ancient Iron Spire (reach_iron_spire)
  3. The Lowlands: River Customs Quarantine (lowlands_customs_house)
  4. The Lowlands: Shadow Cellar Syndicate Heist (lowlands_thieves_hall)
  5. The Scorchwaste: Sandswept Crypt (scorchwaste_buried_tomb)
  6. The Scorchwaste: White Salt Flats (scorchwaste_salt_pan)
  7. The High Court: Hall of Justiciars Tribunal (high_court_justiciar_hall)
  8. The High Court: Ambassador Salon Blackmail (high_court_diplomat_lounge)
  9. The Sunken Hollows: Flooded Siphon Plunge (sunken_hollows_deep_siphon)
  10. The Sunken Hollows: Drowned Shrine Submersion (sunken_hollows_drowned_temple)
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
        session_id="test_systemic",
        character=char,
        current_region=region_id,
        current_scene=scene_id,
        world_flags=world_flags or {},
        rng=DeterministicRNG(42),
    )


# ==============================================================================
# Encounter 1: Eagle Wing Pass (Reach: reach_high_pass)
# ==============================================================================

def test_encounter_1_reach_high_pass():
    eng = AdventureEngine(build_world_registry())

    # Gate 1: Item affordance with climbing_rope
    base_char = CharacterSheet(name="Hiker", ancestry="Highlander", background="scout")
    state_no_item = _make_state(eng, "reach_high_pass_gate", base_char)
    actions_no_item = {a.id for a in eng.get_legal_actions(state_no_item)}
    assert "reach_pass_anchor_rope" not in actions_no_item

    equipped_char = base_char.modify(inventory=["climbing_rope"])
    state_item = _make_state(eng, "reach_high_pass_gate", equipped_char)
    actions_item = {a.id for a in eng.get_legal_actions(state_item)}
    assert "reach_pass_anchor_rope" in actions_item

    # Trait exploit: nimble vaults cable
    nimble_char = base_char.modify(traits=["nimble"])
    state_nimble = _make_state(eng, "reach_high_pass_gate", nimble_char)
    actions_nimble = {a.id for a in eng.get_legal_actions(state_nimble)}
    assert "reach_pass_vault_cable" in actions_nimble

    # Step via cable to courtyard
    state_stage2, _ = eng.step(state_nimble, "reach_pass_vault_cable")
    assert state_stage2.current_scene == "reach_high_pass_courtyard"

    # Stage 2: Attribute check strength >= 14 hauls courier
    weak_char = nimble_char.modify(attributes={"strength": 10})
    state_st2_weak = _make_state(eng, "reach_high_pass_courtyard", weak_char)
    assert "reach_pass_haul_courier" not in {a.id for a in eng.get_legal_actions(state_st2_weak)}

    strong_char = nimble_char.modify(attributes={"strength": 15})
    state_st2_strong = _make_state(eng, "reach_high_pass_courtyard", strong_char)
    assert "reach_pass_haul_courier" in {a.id for a in eng.get_legal_actions(state_st2_strong)}

    # Haul courier to quarters
    state_stage3, _ = eng.step(state_st2_strong, "reach_pass_haul_courier")
    assert state_stage3.current_scene == "reach_high_pass_quarters"
    assert state_stage3.world_flags.get("courier_rescued") is True

    # Stage 3: Claim satchel
    actions_st3 = {a.id for a in eng.get_legal_actions(state_stage3)}
    assert "reach_pass_receive_satchel" in actions_st3
    state_resolved, _ = eng.step(state_stage3, "reach_pass_receive_satchel")
    assert "frontier_mail" in state_resolved.character.inventory
    assert state_resolved.character.reputation.get("iron_guard") == 15
    assert state_resolved.world_flags.get("frontier_mail_taken") is True


# ==============================================================================
# Encounter 2: Ancient Iron Spire (Reach: reach_iron_spire)
# ==============================================================================

def test_encounter_2_reach_iron_spire():
    eng = AdventureEngine(build_world_registry())

    # Item affordance: crowbar grounds cable
    char = CharacterSheet(name="Tech", ancestry="Ironborn", background="artisan", inventory=["crowbar"], skills={"cunning": 4})
    state_gate = _make_state(eng, "reach_iron_spire_gate", char)
    actions_gate = {a.id for a in eng.get_legal_actions(state_gate)}
    assert "reach_spire_ground_cable" in actions_gate

    state_grounded, _ = eng.step(state_gate, "reach_spire_ground_cable")
    assert state_grounded.world_flags.get("spire_cable_grounded") is True

    # Scale to courtyard
    state_stage2, _ = eng.step(state_grounded, "reach_spire_begin_climb")
    assert state_stage2.current_scene == "reach_iron_spire_courtyard"

    # Skill check: cunning >= 3 shorts sentry
    actions_stage2 = {a.id for a in eng.get_legal_actions(state_stage2)}
    assert "reach_spire_short_sentry" in actions_stage2

    state_stage3, _ = eng.step(state_stage2, "reach_spire_short_sentry")
    assert state_stage3.current_scene == "reach_iron_spire_quarters"
    assert state_stage3.world_flags.get("spire_sentry_disabled") is True

    # Resolution: take conductive core
    actions_stage3 = {a.id for a in eng.get_legal_actions(state_stage3)}
    assert "reach_spire_take_core" in actions_stage3

    state_resolved, _ = eng.step(state_stage3, "reach_spire_take_core")
    assert "conductive_core" in state_resolved.character.inventory
    assert "storm_strider" in state_resolved.character.markers
    assert state_resolved.world_flags.get("spire_core_harvested") is True


# ==============================================================================
# Encounter 3: River Customs Quarantine (Lowlands: lowlands_customs_house)
# ==============================================================================

def test_encounter_3_lowlands_customs_house():
    eng = AdventureEngine(build_world_registry())

    # Item affordance: legal_dossier shows pass
    char = CharacterSheet(name="Trader", ancestry="Riverfolk", background="merchant", inventory=["legal_dossier"], skills={"rhetoric": 4})
    state_gate = _make_state(eng, "lowlands_customs_house_gate", char)
    actions_gate = {a.id for a in eng.get_legal_actions(state_gate)}
    assert "lowlands_customs_show_pass" in actions_gate

    state_stage2, _ = eng.step(state_gate, "lowlands_customs_show_pass")
    assert state_stage2.current_scene == "lowlands_customs_house_courtyard"

    # Skill check: rhetoric >= 3 bluffs inspector Vance
    actions_stage2 = {a.id for a in eng.get_legal_actions(state_stage2)}
    assert "lowlands_customs_bluff_vance" in actions_stage2

    state_stage3, _ = eng.step(state_stage2, "lowlands_customs_bluff_vance")
    assert state_stage3.current_scene == "lowlands_customs_house_quarters"
    assert state_stage3.world_flags.get("customs_cleared") is True
    assert state_stage3.character.reputation.get("smugglers") == 15

    # Resolution: take clearance stamp
    actions_stage3 = {a.id for a in eng.get_legal_actions(state_stage3)}
    assert "lowlands_customs_take_stamp" in actions_stage3

    state_resolved, _ = eng.step(state_stage3, "lowlands_customs_take_stamp")
    assert "customs_stamp" in state_resolved.character.inventory
    assert state_resolved.world_flags.get("customs_stamp_taken") is True


# ==============================================================================
# Encounter 4: Shadow Cellar Syndicate Heist (Lowlands: lowlands_thieves_hall)
# ==============================================================================

def test_encounter_4_lowlands_thieves_hall():
    eng = AdventureEngine(build_world_registry())

    # Skill check: stealth >= 3 slips past lookout
    char = CharacterSheet(name="Rogue", ancestry="Shadowkin", background="thief", inventory=["lockpick"], skills={"stealth": 3})
    state_gate = _make_state(eng, "lowlands_thieves_hall_gate", char)
    actions_gate = {a.id for a in eng.get_legal_actions(state_gate)}
    assert "lowlands_thief_slip_past" in actions_gate

    state_stage2, _ = eng.step(state_gate, "lowlands_thief_slip_past")
    assert state_stage2.current_scene == "lowlands_thieves_hall_courtyard"

    # Item affordance: lockpick picks strongbox
    actions_stage2 = {a.id for a in eng.get_legal_actions(state_stage2)}
    assert "lowlands_thief_pick_chest" in actions_stage2

    state_stage3, _ = eng.step(state_stage2, "lowlands_thief_pick_chest")
    assert state_stage3.current_scene == "lowlands_thieves_hall_quarters"
    assert state_stage3.world_flags.get("strongbox_opened") is True

    # Resolution: take watch ledger
    actions_stage3 = {a.id for a in eng.get_legal_actions(state_stage3)}
    assert "lowlands_thief_take_ledger" in actions_stage3

    state_resolved, _ = eng.step(state_stage3, "lowlands_thief_take_ledger")
    assert "watch_patrol_ledger" in state_resolved.character.inventory
    assert state_resolved.character.reputation.get("smugglers") == 25
    assert state_resolved.world_flags.get("patrol_ledger_taken") is True


# ==============================================================================
# Encounter 5: Sandswept Sun Temple (Scorchwaste: scorchwaste_buried_tomb)
# ==============================================================================

def test_encounter_5_scorchwaste_buried_tomb():
    eng = AdventureEngine(build_world_registry())

    # Item affordance: crowbar pries bronze door
    char = CharacterSheet(name="Excavator", ancestry="Dune Walker", background="nomad", inventory=["crowbar"], skills={"cunning": 4})
    state_gate = _make_state(eng, "scorchwaste_buried_tomb_gate", char)
    actions_gate = {a.id for a in eng.get_legal_actions(state_gate)}
    assert "scorch_tomb_force_door" in actions_gate

    state_stage2, _ = eng.step(state_gate, "scorch_tomb_force_door")
    assert state_stage2.current_scene == "scorchwaste_buried_tomb_courtyard"

    # Skill check: cunning >= 3 aligns mirrors
    actions_stage2 = {a.id for a in eng.get_legal_actions(state_stage2)}
    assert "scorch_tomb_align_mirrors" in actions_stage2

    state_stage3, _ = eng.step(state_stage2, "scorch_tomb_align_mirrors")
    assert state_stage3.current_scene == "scorchwaste_buried_tomb_quarters"
    assert state_stage3.world_flags.get("solar_lock_solved") is True

    # Resolution: take solar amulet
    actions_stage3 = {a.id for a in eng.get_legal_actions(state_stage3)}
    assert "scorch_tomb_take_amulet" in actions_stage3

    state_resolved, _ = eng.step(state_stage3, "scorch_tomb_take_amulet")
    assert "solar_amulet" in state_resolved.character.inventory
    assert state_resolved.world_flags.get("solar_amulet_taken") is True


# ==============================================================================
# Encounter 6: White Salt Flats (Scorchwaste: scorchwaste_salt_pan)
# ==============================================================================

def test_encounter_6_scorchwaste_salt_pan():
    eng = AdventureEngine(build_world_registry())

    # Trait exploit: nimble treads fragile salt
    char = CharacterSheet(name="Scout", ancestry="Dune Walker", background="nomad", inventory=["climbing_rope"], traits=["nimble"])
    state_gate = _make_state(eng, "scorchwaste_salt_pan_gate", char)
    actions_gate = {a.id for a in eng.get_legal_actions(state_gate)}
    assert "scorch_salt_tread_carefully" in actions_gate

    state_stage2, _ = eng.step(state_gate, "scorch_salt_tread_carefully")
    assert state_stage2.current_scene == "scorchwaste_salt_pan_courtyard"

    # Item affordance: climbing_rope rescues merchant
    actions_stage2 = {a.id for a in eng.get_legal_actions(state_stage2)}
    assert "scorch_salt_throw_rope" in actions_stage2

    state_stage3, _ = eng.step(state_stage2, "scorch_salt_throw_rope")
    assert state_stage3.current_scene == "scorchwaste_salt_pan_quarters"
    assert state_stage3.world_flags.get("merchant_rescued") is True

    # Resolution: reward
    actions_stage3 = {a.id for a in eng.get_legal_actions(state_stage3)}
    assert "scorch_salt_reward" in actions_stage3

    state_resolved, _ = eng.step(state_stage3, "scorch_salt_reward")
    assert "refined_salt_crystals" in state_resolved.character.inventory
    assert state_resolved.character.reputation.get("caravaneers") == 20
    assert state_resolved.world_flags.get("salt_reward_taken") is True


# ==============================================================================
# Encounter 7: Hall of Justiciars (High Court: high_court_justiciar_hall)
# ==============================================================================

def test_encounter_7_high_court_justiciar_hall():
    eng = AdventureEngine(build_world_registry())

    # Skill check: rhetoric >= 3 demands standing
    char = CharacterSheet(name="Advocate", ancestry="Highborn", background="noble_exile", skills={"rhetoric": 4})
    state_gate = _make_state(eng, "high_court_justiciar_hall_gate", char)
    actions_gate = {a.id for a in eng.get_legal_actions(state_gate)}
    assert "high_justiciar_plead_standing" in actions_gate

    state_stage2, _ = eng.step(state_gate, "high_justiciar_plead_standing")
    assert state_stage2.current_scene == "high_court_justiciar_hall_courtyard"

    # Skill check: rhetoric >= 4 objects to evidence
    actions_stage2 = {a.id for a in eng.get_legal_actions(state_stage2)}
    assert "high_justiciar_object_plea" in actions_stage2

    state_stage3, _ = eng.step(state_stage2, "high_justiciar_object_plea")
    assert state_stage3.current_scene == "high_court_justiciar_hall_quarters"
    assert state_stage3.world_flags.get("court_verdict_won") is True
    assert state_stage3.character.reputation.get("justiciars") == 20

    # Resolution: take judicial seal
    actions_stage3 = {a.id for a in eng.get_legal_actions(state_stage3)}
    assert "high_justiciar_take_seal" in actions_stage3

    state_resolved, _ = eng.step(state_stage3, "high_justiciar_take_seal")
    assert "arch_justiciar_seal" in state_resolved.character.inventory
    assert "court_advocate" in state_resolved.character.markers
    assert state_resolved.world_flags.get("court_seal_taken") is True


# ==============================================================================
# Encounter 8: Ambassador Salon (High Court: high_court_diplomat_lounge)
# ==============================================================================

def test_encounter_8_high_court_ambassador_salon():
    eng = AdventureEngine(build_world_registry())

    # Skill check: stealth >= 3 slips past drapery to balcony
    char = CharacterSheet(name="Diplomat", ancestry="Highborn", background="noble_exile", skills={"stealth": 3, "rhetoric": 4})
    state_gate = _make_state(eng, "high_court_diplomat_lounge_gate", char)
    actions_gate = {a.id for a in eng.get_legal_actions(state_gate)}
    assert "high_salon_slip_balcony" in actions_gate

    state_stage2, _ = eng.step(state_gate, "high_salon_slip_balcony")
    assert state_stage2.current_scene == "high_court_diplomat_lounge_courtyard"

    # Skill check: rhetoric >= 4 blackmails envoy
    actions_stage2 = {a.id for a in eng.get_legal_actions(state_stage2)}
    assert "high_salon_blackmail_envoy" in actions_stage2

    state_stage3, _ = eng.step(state_stage2, "high_salon_blackmail_envoy")
    assert state_stage3.current_scene == "high_court_diplomat_lounge_quarters"
    assert state_stage3.world_flags.get("envoy_deal_made") is True

    # Resolution: take cipher key
    actions_stage3 = {a.id for a in eng.get_legal_actions(state_stage3)}
    assert "high_salon_take_cipher" in actions_stage3

    state_resolved, _ = eng.step(state_stage3, "high_salon_take_cipher")
    assert "royal_cipher_key" in state_resolved.character.inventory
    assert state_resolved.world_flags.get("cipher_key_taken") is True


# ==============================================================================
# Encounter 9: Flooded Siphon (Sunken Hollows: sunken_hollows_deep_siphon)
# ==============================================================================

def test_encounter_9_sunken_hollows_flooded_siphon():
    eng = AdventureEngine(build_world_registry())

    # Item affordance: waterproof_seal
    char = CharacterSheet(name="Diver", ancestry="Deep Dweller", background="diver", inventory=["waterproof_seal", "crowbar"], traits=["water_breather"])
    state_gate = _make_state(eng, "sunken_hollows_deep_siphon_gate", char)
    actions_gate = {a.id for a in eng.get_legal_actions(state_gate)}
    assert "hollows_siphon_seal_gear" in actions_gate

    state_sealed, _ = eng.step(state_gate, "hollows_siphon_seal_gear")
    assert state_sealed.world_flags.get("gear_waterproofed") is True

    # Dive to stage 2
    state_stage2, _ = eng.step(state_sealed, "hollows_siphon_dive_pool")
    assert state_stage2.current_scene == "sunken_hollows_deep_siphon_courtyard"

    # Item affordance: crowbar prying stone loose
    actions_stage2 = {a.id for a in eng.get_legal_actions(state_stage2)}
    assert "hollows_siphon_pry_crowbar" in actions_stage2

    state_stage3, _ = eng.step(state_stage2, "hollows_siphon_pry_crowbar")
    assert state_stage3.current_scene == "sunken_hollows_deep_siphon_quarters"
    assert state_stage3.world_flags.get("siphon_cleared") is True

    # Resolution: take chitin shield
    actions_stage3 = {a.id for a in eng.get_legal_actions(state_stage3)}
    assert "hollows_siphon_take_shield" in actions_stage3

    state_resolved, _ = eng.step(state_stage3, "hollows_siphon_take_shield")
    assert "chitin_shield" in state_resolved.character.inventory
    assert state_resolved.world_flags.get("chitin_shield_taken") is True


# ==============================================================================
# Encounter 10: Drowned Shrine (Sunken Hollows: sunken_hollows_drowned_temple)
# ==============================================================================

def test_encounter_10_sunken_hollows_drowned_shrine():
    eng = AdventureEngine(build_world_registry())

    # Item affordance: climbing_rope rigs descent
    char = CharacterSheet(name="Priest", ancestry="Deep Dweller", background="cleric", inventory=["climbing_rope", "lockpick"])
    state_gate = _make_state(eng, "sunken_hollows_drowned_temple_gate", char)
    actions_gate = {a.id for a in eng.get_legal_actions(state_gate)}
    assert "hollows_shrine_rig_rope" in actions_gate

    state_rigged, _ = eng.step(state_gate, "hollows_shrine_rig_rope")
    assert state_rigged.world_flags.get("shrine_rope_rigged") is True

    # Dive to stage 2
    state_stage2, _ = eng.step(state_rigged, "hollows_shrine_dive_nave")
    assert state_stage2.current_scene == "sunken_hollows_drowned_temple_courtyard"

    # Item affordance: lockpick picks altar cage
    actions_stage2 = {a.id for a in eng.get_legal_actions(state_stage2)}
    assert "hollows_shrine_pick_cage" in actions_stage2

    state_stage3, _ = eng.step(state_stage2, "hollows_shrine_pick_cage")
    assert state_stage3.current_scene == "sunken_hollows_drowned_temple_quarters"
    assert state_stage3.world_flags.get("altar_cage_opened") is True

    # Resolution: claim abyssal pearl
    actions_stage3 = {a.id for a in eng.get_legal_actions(state_stage3)}
    assert "hollows_shrine_take_pearl" in actions_stage3

    state_resolved, _ = eng.step(state_stage3, "hollows_shrine_take_pearl")
    assert "abyssal_pearl" in state_resolved.character.inventory
    assert "pearl_bearer" in state_resolved.character.markers
    assert state_resolved.character.reputation.get("hollow_dwellers") == 25


# ==============================================================================
# Cross-Regional Dynamics & Trait Reactivity
# ==============================================================================

def test_dynamic_descriptions_reactivity():
    """Verify that dynamic descriptions trigger based on character traits and background."""
    eng = AdventureEngine(build_world_registry())

    # Noble exile at high court salon
    noble = CharacterSheet(name="Exile", ancestry="Highborn", background="noble_exile")
    state_noble = _make_state(eng, "high_court_diplomat_lounge_gate", noble)
    obs_noble = eng.observe(state_noble)
    assert "ancestral name" in obs_noble.description

    # Water breather in sunken hollows
    aquatic = CharacterSheet(name="Gill", ancestry="Deep Dweller", background="diver", traits=["water_breather"])
    state_aquatic = _make_state(eng, "sunken_hollows_deep_siphon_gate", aquatic)
    obs_aquatic = eng.observe(state_aquatic)
    assert "gills pulse" in obs_aquatic.description
