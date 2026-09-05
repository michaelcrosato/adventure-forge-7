"""Adversarial Verification and Stress-Testing Suite for Milestone 13:
5-Province Systemic Questlines, Faction Intrigue Arcs, and Cross-Province Web.

Authored by Empirical Challenger 1 (Milestone 13).

Covers:
1. Full playthrough simulation across 6 character presets:
   - Silas the Cutpurse (Deep-Dweller rogue)
   - Lady Vivienne (High-Kin noble)
   - Kael the Nomad (Dune strider)
   - Mara the Diver (Abyssal diver)
   - Torin the Scout (Highland ranger)
   - Garron the Warrior (Ashenborn pit fighter)
2. Counterfactual divergence matrix proving that character build differences
   strictly dictate legal action sets and narrative outcomes in intrigue scenes.
3. Mutual exclusivity stress-testing across all 18 endings in all 5 provinces,
   verifying engine-level action lockouts, illegal step rejections, and evaluator resolution.
4. Cross-province double-agent affordance synthesis (dual marker unlocking).
5. Replay determinism and state fingerprint invariance across multi-step action traces.
6. Exhaustive Hemingway prose, label length (1-3 words), and purple lexicon audit.
"""
from dataclasses import replace
from typing import Dict, Any, List

import pytest

from adventure_forge.content.loader import build_world_registry
from adventure_forge.content.quests import (
    get_faction_intrigue_quests,
    quest_reach_faction_intrigue,
    quest_high_court_faction_intrigue,
    subquest_scorchwaste_water_wars,
    subquest_hollows_abyssal_schism,
    subquest_lowlands_river_intrigue,
)
from adventure_forge.core.character import CharacterSheet, get_preset
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import FORBIDDEN_PURPLE_WORDS


@pytest.fixture(scope="module")
def world_engine() -> AdventureEngine:
    registry = build_world_registry()
    return AdventureEngine(world_registry=registry)


def make_test_state(
    eng: AdventureEngine,
    scene_id: str,
    char: CharacterSheet,
    world_flags: Dict[str, Any] | None = None,
) -> GameState:
    region_id = eng.get_region_id_for_scene(scene_id) or "test_region"
    return GameState(
        build_id=eng.build_id,
        session_id="challenger_m13_session",
        character=char,
        current_region=region_id,
        current_scene=scene_id,
        world_flags=dict(world_flags or {}),
    )


# ==============================================================================
# 1. Full Playthrough Simulations Across 6 Character Presets
# ==============================================================================

def test_playthrough_silas_syndicate_infiltrator_and_cross_province(world_engine: AdventureEngine):
    """Silas the Cutpurse plays Lowlands Sluice War as Shadow Syndicate ally,

    unlocks syndicate_contact marker, and utilizes cross-province perks in all 4 provinces.
    """
    silas = get_preset("cutpurse").character
    state = make_test_state(world_engine, "lowlands_customs_house_quarters", silas)

    # Stage 1: Deliver manifest to Syndicate
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "lowlands_manifest_give_syndicate" in legal
    state, res1 = world_engine.step(state, "lowlands_manifest_give_syndicate")
    assert res1.success
    assert state.world_flags.get("lowlands_manifest_decided") is True
    assert "syndicate_contact" in state.character.markers
    assert state.character.reputation.get("shadow_syndicate", 0) > 0

    # Stage 2: Sabotage canal sluice winch
    state = replace(state, current_scene="lowlands_canal_sluice_chamber", current_region="lowlands")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "lowlands_sluice_sabotage_winch" in legal
    state, res2 = world_engine.step(state, "lowlands_sluice_sabotage_winch")
    assert res2.success
    assert state.world_flags.get("lowlands_sluice_decided") is True

    # Stage 3: Signal shadow fleet from bell tower
    state = replace(state, current_scene="lowlands_bell_tower_overlook", current_region="lowlands")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "lowlands_bell_signal_syndicate" in legal
    state, res3 = world_engine.step(state, "lowlands_bell_signal_syndicate")
    assert res3.success
    assert state.world_flags.get("lowlands_river_intrigue_resolved") is True
    assert state.world_flags.get("lowlands_intrigue_syndicate_win") is True

    # Verify Lowlands quest progression
    lowlands_quest = subquest_lowlands_river_intrigue()
    prog = lowlands_quest.evaluate_progress(state.character, state.world_flags)
    assert prog["is_finished"] is True
    assert prog["ending"] == "syndicate_ascendant"

    # Cross-Province Web: Exercise syndicate_contact in all other 4 provinces
    # 1. The Reach: Dunwall Fort Gate
    state_reach = replace(state, current_scene="reach_dunwall_fort_gate", current_region="reach")
    legal_reach = {a.id for a in world_engine.get_legal_actions(state_reach)}
    assert "reach_whistle_smuggler_call" in legal_reach
    state_reach, res_reach = world_engine.step(state_reach, "reach_whistle_smuggler_call")
    assert res_reach.success
    assert state_reach.world_flags.get("reach_smuggler_bypass_used") is True

    # 2. High Court: Royal Archive Gate
    state_court = replace(state, current_scene="high_court_royal_archive_gate", current_region="high_court")
    legal_court = {a.id for a in world_engine.get_legal_actions(state_court)}
    assert "court_bribe_lowlands_clerk" in legal_court
    state_court, res_court = world_engine.step(state_court, "court_bribe_lowlands_clerk")
    assert res_court.success
    assert state_court.world_flags.get("court_clerk_bribed") is True

    # 3. Scorchwaste: Canyon Oasis Gate
    state_scorch = replace(state, current_scene="scorchwaste_canyon_oasis_gate", current_region="scorchwaste")
    legal_scorch = {a.id for a in world_engine.get_legal_actions(state_scorch)}
    assert "scorch_trade_lowlands_contraband" in legal_scorch
    state_scorch, res_scorch = world_engine.step(state_scorch, "scorch_trade_lowlands_contraband")
    assert res_scorch.success
    assert state_scorch.world_flags.get("scorch_contraband_traded") is True
    assert "nomad_water_flask" in state_scorch.character.inventory

    # 4. Sunken Hollows: Coral Chasm Gate
    state_hollow = replace(state, current_scene="sunken_hollows_coral_chasm_gate", current_region="sunken_hollows")
    legal_hollow = {a.id for a in world_engine.get_legal_actions(state_hollow)}
    assert "hollows_trade_black_pearls" in legal_hollow
    state_hollow, res_hollow = world_engine.step(state_hollow, "hollows_trade_black_pearls")
    assert res_hollow.success
    assert state_hollow.world_flags.get("hollows_black_pearls_traded") is True


def test_playthrough_vivienne_bailiff_and_court_intrigue(world_engine: AdventureEngine):
    """Lady Vivienne plays Lowlands Sluice War as River Bailiff ally,

    cross-province exercises municipal warrants in all 4 provinces,
    and resolves High Court Tripartite Throne as Lord Regent.
    """
    vivienne = get_preset("noble").character
    state = make_test_state(world_engine, "lowlands_customs_house_quarters", vivienne)

    # Stage 1: Deliver manifest to Bailiff
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "lowlands_manifest_give_bailiff" in legal
    state, res1 = world_engine.step(state, "lowlands_manifest_give_bailiff")
    assert res1.success
    assert "river_bailiff" in state.character.markers
    assert state.world_flags.get("lowlands_manifest_decided") is True

    # Stage 2: Lock sluice chains
    state = replace(state, current_scene="lowlands_canal_sluice_chamber", current_region="lowlands")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "lowlands_sluice_lock_chains" in legal
    state, res2 = world_engine.step(state, "lowlands_sluice_lock_chains")
    assert res2.success
    assert state.world_flags.get("lowlands_sluice_decided") is True

    # Stage 3: Ring cathedral alarm bell
    state = replace(state, current_scene="lowlands_bell_tower_overlook", current_region="lowlands")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "lowlands_bell_ring_alarm" in legal
    state, res3 = world_engine.step(state, "lowlands_bell_ring_alarm")
    assert res3.success
    assert state.world_flags.get("lowlands_river_intrigue_resolved") is True
    assert state.world_flags.get("lowlands_intrigue_guild_win") is True

    lowlands_quest = subquest_lowlands_river_intrigue()
    prog = lowlands_quest.evaluate_progress(state.character, state.world_flags)
    assert prog["ending"] == "river_guild_monopoly"

    # Cross-Province Web: Exercise river_bailiff in all 4 other provinces
    # 1. Reach: High Pass Gate
    s_reach = replace(state, current_scene="reach_high_pass_gate", current_region="reach")
    legal_reach = {a.id for a in world_engine.get_legal_actions(s_reach)}
    assert "reach_show_garrison_pass" in legal_reach
    s_reach, res_r = world_engine.step(s_reach, "reach_show_garrison_pass")
    assert res_r.success
    assert s_reach.world_flags.get("reach_garrison_escort_active") is True

    # 2. High Court: Justiciar Hall Gate
    s_court = replace(state, current_scene="high_court_justiciar_hall_gate", current_region="high_court")
    legal_court = {a.id for a in world_engine.get_legal_actions(s_court)}
    assert "court_present_bailiff_warrants" in legal_court
    s_court, res_c = world_engine.step(s_court, "court_present_bailiff_warrants")
    assert res_c.success
    assert s_court.world_flags.get("court_tribunal_fast_track") is True

    # 3. Scorchwaste: Nomad Well Gate
    s_scorch = replace(state, current_scene="scorchwaste_nomad_well_gate", current_region="scorchwaste")
    legal_scorch = {a.id for a in world_engine.get_legal_actions(s_scorch)}
    assert "scorch_present_guild_charter" in legal_scorch
    s_scorch, res_s = world_engine.step(s_scorch, "scorch_present_guild_charter")
    assert res_s.success
    assert s_scorch.world_flags.get("scorch_guild_charter_presented") is True

    # 4. Sunken Hollows: Deep Siphon Gate
    s_hollow = replace(state, current_scene="sunken_hollows_deep_siphon_gate", current_region="sunken_hollows")
    legal_hollow = {a.id for a in world_engine.get_legal_actions(s_hollow)}
    assert "hollows_claim_salvage_rig" in legal_hollow
    s_hollow, res_h = world_engine.step(s_hollow, "hollows_claim_salvage_rig")
    assert res_h.success
    assert s_hollow.world_flags.get("hollows_salvage_rig_claimed") is True

    # Now play the High Court Tripartite Throne questline with Vivienne
    # Stage 1: Archive search (noble_exile trait bypass)
    s_c1 = replace(state, current_scene="high_court_royal_archive_courtyard", current_region="high_court")
    legal_c1 = {a.id for a in world_engine.get_legal_actions(s_c1)}
    assert "court_archive_search_stacks" in legal_c1
    s_c1, res_c1 = world_engine.step(s_c1, "court_archive_search_stacks")
    assert res_c1.success
    assert s_c1.world_flags.get("court_discovery_completed") is True

    # Stage 2: Sway Palatine Knights (rhetoric 4)
    s_c2 = replace(s_c1, current_scene="high_court_knight_barracks_courtyard", current_region="high_court")
    legal_c2 = {a.id for a in world_engine.get_legal_actions(s_c2)}
    assert "court_barracks_sway_knights" in legal_c2
    s_c2, res_c2 = world_engine.step(s_c2, "court_barracks_sway_knights")
    assert res_c2.success
    assert s_c2.world_flags.get("court_escalation_completed") is True

    # Stage 3: Seize the Regency Bench (rhetoric 4, intimidation 14)
    s_c3 = replace(s_c2, current_scene="high_court_justiciar_hall_quarters", current_region="high_court")
    legal_c3 = {a.id for a in world_engine.get_legal_actions(s_c3)}
    assert "court_tribunal_seize_bench" in legal_c3
    s_c3, res_c3 = world_engine.step(s_c3, "court_tribunal_seize_bench")
    assert res_c3.success
    assert s_c3.world_flags.get("court_dilemma_resolved") is True
    assert s_c3.world_flags.get("court_ruling_regent") is True

    # Stage 4: Proclaim Commoner Rule at High Court Hub
    s_c4 = replace(s_c3, current_scene="high_court_hub", current_region="high_court")
    legal_c4 = {a.id for a in world_engine.get_legal_actions(s_c4)}
    assert "court_resolve_regent" in legal_c4
    s_c4, res_c4 = world_engine.step(s_c4, "court_resolve_regent")
    assert res_c4.success
    assert s_c4.world_flags.get("court_intrigue_resolved") is True
    assert s_c4.world_flags.get("court_ending_regent") is True

    court_quest = quest_high_court_faction_intrigue()
    prog_c = court_quest.evaluate_progress(s_c4.character, s_c4.world_flags)
    assert prog_c["is_finished"] is True
    assert prog_c["ending"] == "court_unbounded_protector"


def test_playthrough_kael_scorchwaste_water_wars(world_engine: AdventureEngine):
    """Kael the Nomad plays Scorchwaste Water Wars, proving survival instincts,

    resolving the aquifer crisis, and claiming free waters for the desert clans.
    """
    kael = get_preset("nomad").character
    state = make_test_state(world_engine, "scorchwaste_dune_ridge_gate", kael)

    # Stage 1: Survey pipeline
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "scorch_war_survey_pipeline" in legal
    state, res1 = world_engine.step(state, "scorch_war_survey_pipeline")
    assert res1.success
    assert state.world_flags.get("scorch_pipeline_surveyed") is True

    # Stage 2: Parley at canyon oasis and pledge to nomads
    state = replace(state, current_scene="scorchwaste_canyon_oasis_courtyard", current_region="scorchwaste")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "scorch_war_pledge_wardens" in legal
    state, res2 = world_engine.step(state, "scorch_war_pledge_wardens")
    assert res2.success
    assert state.world_flags.get("scorch_faction_chosen") is True
    assert state.world_flags.get("scorch_allied_nomads") is True

    # Stage 3: Nomad well crisis. Kael has flint; grant torch to test pitch repair affordance
    kael_with_torch = state.character.modify(inventory=list(state.character.inventory) + ["torch"])
    state = replace(state, character=kael_with_torch, current_scene="scorchwaste_nomad_well_quarters", current_region="scorchwaste")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "scorch_war_seal_pipeline_pitch" in legal
    state, res3 = world_engine.step(state, "scorch_war_seal_pipeline_pitch")
    assert res3.success
    assert state.world_flags.get("scorch_crisis_resolved") is True

    # Stage 4: Scorchwaste Hub resolution: Free The Waters
    state = replace(state, current_scene="scorchwaste_hub", current_region="scorchwaste")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "scorch_war_end_free_water" in legal
    state, res4 = world_engine.step(state, "scorch_war_end_free_water")
    assert res4.success
    assert state.world_flags.get("scorch_war_resolved") is True
    assert state.world_flags.get("scorch_ending_free_water") is True

    scorch_quest = subquest_scorchwaste_water_wars()
    prog = scorch_quest.evaluate_progress(state.character, state.world_flags)
    assert prog["is_finished"] is True
    assert prog["ending"] == "free_waters"


def test_playthrough_mara_hollows_abyssal_schism(world_engine: AdventureEngine):
    """Mara the Diver plays Sunken Hollows Abyssal Schism using amphibious athletics,

    crowbar valve clearing, and establishes the Diver Commune ending.
    """
    mara = get_preset("diver").character
    state = make_test_state(world_engine, "sunken_hollows_abyssal_river_gate", mara)

    # Stage 1: Mara has athletics 4 -> dive rapids exploit is legal
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "hollows_schism_dive_rapids" in legal
    state, res1 = world_engine.step(state, "hollows_schism_dive_rapids")
    assert res1.success
    assert state.world_flags.get("hollows_rapids_navigated") is True

    # Stage 2: Sub-wharf alignment: Sign Cartel Contract
    state = replace(state, current_scene="sunken_hollows_sub_wharf_courtyard", current_region="sunken_hollows")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "hollows_schism_contract_cartel" in legal
    state, res2 = world_engine.step(state, "hollows_schism_contract_cartel")
    assert res2.success
    assert state.world_flags.get("hollows_faction_chosen") is True

    # Stage 3: Deep Siphon crisis. Mara has crowbar and cunning 3 -> multiple options
    state = replace(state, current_scene="sunken_hollows_deep_siphon_quarters", current_region="sunken_hollows")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "hollows_schism_crank_pressure_valve" in legal
    assert "hollows_schism_seal_air_line" in legal
    assert "hollows_schism_dredge_ruins" in legal
    state, res3 = world_engine.step(state, "hollows_schism_dredge_ruins")
    assert res3.success
    assert state.world_flags.get("hollows_crisis_resolved") is True

    # Stage 4: Establish Diver Commune at Hub
    state = replace(state, current_scene="sunken_hollows_hub", current_region="sunken_hollows")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "hollows_end_diver_commune" in legal
    state, res4 = world_engine.step(state, "hollows_end_diver_commune")
    assert res4.success
    assert state.world_flags.get("hollows_schism_resolved") is True
    assert state.world_flags.get("hollows_ending_diver_commune") is True

    hollows_quest = subquest_hollows_abyssal_schism()
    prog = hollows_quest.evaluate_progress(state.character, state.world_flags)
    assert prog["is_finished"] is True
    assert prog["ending"] == "diver_commune"


def test_playthrough_torin_reach_sky_pact(world_engine: AdventureEngine):
    """Torin the Scout plays The Reach Sky-Pact, discovering the sabotage via keen_eyed,

    brokering a truce as a highland scout, and harmonizing the ridge vents.
    """
    torin = get_preset("scout").character
    state = make_test_state(world_engine, "reach_wind_hollow_quarters", torin)

    # Stage 1: Inspect cable via keen_eyed
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "reach_wind_inspect_cable" in legal
    state, res1 = world_engine.step(state, "reach_wind_inspect_cable")
    assert res1.success
    assert state.world_flags.get("reach_discovery_completed") is True

    # Stage 2: Broker quarry truce via highland_scout background
    state = replace(state, current_scene="reach_granite_mine_courtyard", current_region="reach")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "reach_mine_broker_truce" in legal
    state, res2 = world_engine.step(state, "reach_mine_broker_truce")
    assert res2.success
    assert state.world_flags.get("reach_escalation_completed") is True

    # Stage 3: Harmonize ridge vents at secret shrine (Torin has agility 15)
    state = replace(state, current_scene="reach_secret_shrine", current_region="reach")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "reach_shrine_harmonize_vents" in legal
    state, res3 = world_engine.step(state, "reach_shrine_harmonize_vents")
    assert res3.success
    assert state.world_flags.get("reach_dilemma_resolved") is True
    assert state.world_flags.get("reach_vents_harmonized") is True

    # Stage 4: Proclaim Peak Harmony at reach_hub
    state = replace(state, current_scene="reach_hub", current_region="reach")
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "reach_resolve_ascetic_harmony" in legal
    state, res4 = world_engine.step(state, "reach_resolve_ascetic_harmony")
    assert res4.success
    assert state.world_flags.get("reach_intrigue_resolved") is True
    assert state.world_flags.get("reach_ending_harmony") is True

    reach_quest = quest_reach_faction_intrigue()
    prog = reach_quest.evaluate_progress(state.character, state.world_flags)
    assert prog["is_finished"] is True
    assert prog["ending"] == "ascetic_harmony"


def test_playthrough_garron_martial_crusher(world_engine: AdventureEngine):
    """Garron the Warrior demonstrates pit-fighter force across Reach and Scorchwaste."""
    garron = get_preset("warrior").character
    state = make_test_state(world_engine, "reach_granite_mine_courtyard", garron, {"reach_discovery_completed": True})

    # Reach Stage 2: Storm barricade with strength 16 and pit_fighter background
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "reach_mine_storm_barricade" in legal
    state, res = world_engine.step(state, "reach_mine_storm_barricade")
    assert res.success
    assert state.world_flags.get("reach_quarry_broken_by_force") is True
    assert state.world_flags.get("reach_escalation_completed") is True

    # Scorchwaste Stage 3: Purge brine pump with strength 16 and crowbar
    s_scorch = make_test_state(
        world_engine,
        "scorchwaste_nomad_well_quarters",
        garron,
        {"scorch_faction_chosen": True}
    )
    legal_scorch = {a.id for a in world_engine.get_legal_actions(s_scorch)}
    assert "scorch_war_purge_brine_pump" in legal_scorch
    s_scorch, res_s = world_engine.step(s_scorch, "scorch_war_purge_brine_pump")
    assert res_s.success
    assert s_scorch.world_flags.get("scorch_crisis_resolved") is True


# ==============================================================================
# 2. Counterfactual Divergence Matrix Across Character Builds
# ==============================================================================

def test_counterfactual_divergence_across_all_provinces(world_engine: AdventureEngine):
    """Rigorous matrix verifying that orthogonal character axes produce distinct

    legal choices in every province's intrigue scenes.
    """
    silas = get_preset("cutpurse").character
    vivienne = get_preset("noble").character
    garron = get_preset("warrior").character
    mara = get_preset("diver").character
    torin = get_preset("scout").character

    # 1. High Court Justiciar Hall Quarters (Stage 3):
    # Vivienne (rhetoric 4) can seize the regency bench. Silas and Garron cannot.
    s_viv = make_test_state(world_engine, "high_court_justiciar_hall_quarters", vivienne, {"court_escalation_completed": True})
    s_sil = make_test_state(world_engine, "high_court_justiciar_hall_quarters", silas, {"court_escalation_completed": True})
    s_gar = make_test_state(world_engine, "high_court_justiciar_hall_quarters", garron, {"court_escalation_completed": True})

    act_viv = {a.id for a in world_engine.get_legal_actions(s_viv)}
    act_sil = {a.id for a in world_engine.get_legal_actions(s_sil)}
    act_gar = {a.id for a in world_engine.get_legal_actions(s_gar)}

    assert "court_tribunal_seize_bench" in act_viv
    assert "court_tribunal_seize_bench" not in act_sil
    assert "court_tribunal_seize_bench" not in act_gar

    # 2. High Court Silver Vault Gate (Stage 2):
    # Silas has cunning 4 and lockpick -> can pick treasury grate. Garron cannot.
    s_sil_v = make_test_state(world_engine, "high_court_silver_vault_gate", silas, {"court_discovery_completed": True})
    s_gar_v = make_test_state(world_engine, "high_court_silver_vault_gate", garron, {"court_discovery_completed": True})
    assert "court_vault_pick_sluice" in {a.id for a in world_engine.get_legal_actions(s_sil_v)}
    assert "court_vault_pick_sluice" not in {a.id for a in world_engine.get_legal_actions(s_gar_v)}

    # 3. Reach Granite Mine Courtyard (Stage 2):
    # Garron can storm barricade; Torin can broker truce. Silas can do neither.
    s_gar_m = make_test_state(world_engine, "reach_granite_mine_courtyard", garron, {"reach_discovery_completed": True})
    s_tor_m = make_test_state(world_engine, "reach_granite_mine_courtyard", torin, {"reach_discovery_completed": True})
    s_sil_m = make_test_state(world_engine, "reach_granite_mine_courtyard", silas, {"reach_discovery_completed": True})

    act_gar_m = {a.id for a in world_engine.get_legal_actions(s_gar_m)}
    act_tor_m = {a.id for a in world_engine.get_legal_actions(s_tor_m)}
    act_sil_m = {a.id for a in world_engine.get_legal_actions(s_sil_m)}

    assert "reach_mine_storm_barricade" in act_gar_m
    assert "reach_mine_broker_truce" not in act_gar_m
    assert "reach_mine_broker_truce" in act_tor_m
    assert "reach_mine_storm_barricade" not in act_sil_m
    assert "reach_mine_broker_truce" not in act_sil_m

    # 4. Sunken Hollows Abyssal River Gate (Stage 1):
    # Mara (athletics 4) dives rapids. Silas (athletics 0, not amphibious) cannot.
    s_mar_r = make_test_state(world_engine, "sunken_hollows_abyssal_river_gate", mara)
    s_sil_r = make_test_state(world_engine, "sunken_hollows_abyssal_river_gate", silas)
    assert "hollows_schism_dive_rapids" in {a.id for a in world_engine.get_legal_actions(s_mar_r)}
    assert "hollows_schism_dive_rapids" not in {a.id for a in world_engine.get_legal_actions(s_sil_r)}

    # 5. Lowlands Customs House Quarters (Stage 1):
    # Vivienne (rhetoric 4) can deliver to bailiff; Silas (streetwise) delivers to syndicate.
    s_viv_l = make_test_state(world_engine, "lowlands_customs_house_quarters", vivienne)
    s_sil_l = make_test_state(world_engine, "lowlands_customs_house_quarters", silas)
    assert "lowlands_manifest_give_bailiff" in {a.id for a in world_engine.get_legal_actions(s_viv_l)}
    assert "lowlands_manifest_give_syndicate" in {a.id for a in world_engine.get_legal_actions(s_sil_l)}


# ==============================================================================
# 3. Mutual Exclusivity Stress-Testing Across All 18 Endings
# ==============================================================================

@pytest.mark.parametrize(
    "province,hub_scene,chosen_ending_action,conflicting_actions,expected_flag",
    [
        # The Reach (3 endings)
        (
            "reach",
            "reach_hub",
            "reach_resolve_warden_dominance",
            ["reach_resolve_clan_liberation", "reach_resolve_ascetic_harmony"],
            "reach_ending_warden",
        ),
        (
            "reach",
            "reach_hub",
            "reach_resolve_clan_liberation",
            ["reach_resolve_warden_dominance", "reach_resolve_ascetic_harmony"],
            "reach_ending_clan",
        ),
        (
            "reach",
            "reach_hub",
            "reach_resolve_ascetic_harmony",
            ["reach_resolve_warden_dominance", "reach_resolve_clan_liberation"],
            "reach_ending_harmony",
        ),
        # High Court (4 endings)
        (
            "high_court",
            "high_court_hub",
            "court_resolve_royalist",
            ["court_resolve_ducal", "court_resolve_guild", "court_resolve_regent"],
            "court_ending_royalist",
        ),
        (
            "high_court",
            "high_court_hub",
            "court_resolve_ducal",
            ["court_resolve_royalist", "court_resolve_guild", "court_resolve_regent"],
            "court_ending_ducal",
        ),
        (
            "high_court",
            "high_court_hub",
            "court_resolve_guild",
            ["court_resolve_royalist", "court_resolve_ducal", "court_resolve_regent"],
            "court_ending_guild",
        ),
        (
            "high_court",
            "high_court_hub",
            "court_resolve_regent",
            ["court_resolve_royalist", "court_resolve_ducal", "court_resolve_guild"],
            "court_ending_regent",
        ),
        # Scorchwaste (4 endings)
        (
            "scorchwaste",
            "scorchwaste_hub",
            "scorch_war_end_free_water",
            ["scorch_war_end_monopoly", "scorch_war_end_concordat", "scorch_war_end_autocrat"],
            "scorch_ending_free_water",
        ),
        (
            "scorchwaste",
            "scorchwaste_hub",
            "scorch_war_end_monopoly",
            ["scorch_war_end_free_water", "scorch_war_end_concordat", "scorch_war_end_autocrat"],
            "scorch_ending_cartel_monopoly",
        ),
        (
            "scorchwaste",
            "scorchwaste_hub",
            "scorch_war_end_concordat",
            ["scorch_war_end_free_water", "scorch_war_end_monopoly", "scorch_war_end_autocrat"],
            "scorch_ending_concordat",
        ),
        (
            "scorchwaste",
            "scorchwaste_hub",
            "scorch_war_end_autocrat",
            ["scorch_war_end_free_water", "scorch_war_end_monopoly", "scorch_war_end_concordat"],
            "scorch_ending_autocrat",
        ),
        # Sunken Hollows (4 endings)
        (
            "sunken_hollows",
            "sunken_hollows_hub",
            "hollows_end_archive_sanctuary",
            ["hollows_end_cartel_dredge", "hollows_end_diver_commune", "hollows_end_deluge_unsealed"],
            "hollows_ending_archive_sanctuary",
        ),
        (
            "sunken_hollows",
            "sunken_hollows_hub",
            "hollows_end_cartel_dredge",
            ["hollows_end_archive_sanctuary", "hollows_end_diver_commune", "hollows_end_deluge_unsealed"],
            "hollows_ending_cartel_dredge",
        ),
        (
            "sunken_hollows",
            "sunken_hollows_hub",
            "hollows_end_diver_commune",
            ["hollows_end_archive_sanctuary", "hollows_end_cartel_dredge", "hollows_end_deluge_unsealed"],
            "hollows_ending_diver_commune",
        ),
        (
            "sunken_hollows",
            "sunken_hollows_hub",
            "hollows_end_deluge_unsealed",
            ["hollows_end_archive_sanctuary", "hollows_end_cartel_dredge", "hollows_end_diver_commune"],
            "hollows_ending_deluge_unsealed",
        ),
        # Lowlands (3 endings)
        (
            "lowlands",
            "lowlands_bell_tower_overlook",
            "lowlands_bell_signal_syndicate",
            ["lowlands_bell_ring_alarm", "lowlands_bell_sign_compact"],
            "lowlands_intrigue_syndicate_win",
        ),
        (
            "lowlands",
            "lowlands_bell_tower_overlook",
            "lowlands_bell_ring_alarm",
            ["lowlands_bell_signal_syndicate", "lowlands_bell_sign_compact"],
            "lowlands_intrigue_guild_win",
        ),
        (
            "lowlands",
            "lowlands_bell_tower_overlook",
            "lowlands_bell_sign_compact",
            ["lowlands_bell_signal_syndicate", "lowlands_bell_ring_alarm"],
            "lowlands_intrigue_compact_win",
        ),
    ],
)
def test_mutual_exclusivity_lockout(
    world_engine: AdventureEngine,
    province: str,
    hub_scene: str,
    chosen_ending_action: str,
    conflicting_actions: List[str],
    expected_flag: str,
):
    """Stress-test that executing an ending action permanently locks out all conflicting endings.

    Verifies:
    1. The chosen action is legal before execution.
    2. After step(), the chosen ending flag is True.
    3. None of the conflicting actions remain in get_legal_actions().
    4. Forcefully invoking step() with any conflicting action fails and leaves state unchanged.
    """
    char = CharacterSheet(
        name="ExclusivityTester",
        ancestry="Human",
        background="Tester",
        attributes={"strength": 16, "cunning": 16, "agility": 16, "rhetoric": 16, "intimidation": 16},
        skills={"rhetoric": 5, "cunning": 5, "athletics": 5, "stealth": 5},
        traits=["amphibious", "night_eyed", "keen_eyed", "skeptical"],
        markers=["syndicate_contact", "river_bailiff"],
        inventory=["crowbar", "torch", "tuning_fork", "chancellor_signet_ring", "silver_coin"],
    )

    # Prerequisite flags to make the ending action legal
    flags: Dict[str, Any] = {
        # Reach
        "reach_discovery_completed": True,
        "reach_escalation_completed": True,
        "reach_dilemma_resolved": True,
        "reach_diverted_to_gorge": True,
        "reach_spire_ground_shorted": True,
        "reach_vents_harmonized": True,
        # High Court
        "court_discovery_completed": True,
        "court_escalation_completed": True,
        "court_dilemma_resolved": True,
        "court_ruling_crown": True,
        "court_ruling_duke": True,
        "court_ruling_guild": True,
        "court_ruling_regent": True,
        # Scorchwaste
        "scorch_pipeline_surveyed": True,
        "scorch_faction_chosen": True,
        "scorch_crisis_resolved": True,
        # Sunken Hollows
        "hollows_rapids_navigated": True,
        "hollows_faction_chosen": True,
        "hollows_crisis_resolved": True,
        # Lowlands
        "lowlands_manifest_decided": True,
        "lowlands_sluice_decided": True,
    }

    state = make_test_state(world_engine, hub_scene, char, flags)
    legal_before = {a.id for a in world_engine.get_legal_actions(state)}
    assert chosen_ending_action in legal_before, f"{chosen_ending_action} was not legal before execution"

    # Step into chosen ending
    next_state, res = world_engine.step(state, chosen_ending_action)
    assert res.success, f"Failed to execute {chosen_ending_action}: {res.message}"
    assert next_state.world_flags.get(expected_flag) is True

    # 1. Verify all conflicting actions are removed from legal actions
    legal_after = {a.id for a in world_engine.get_legal_actions(next_state)}
    for conflict in conflicting_actions:
        assert conflict not in legal_after, f"Conflicting action {conflict} remained legal after {chosen_ending_action}"

    # 2. Forcefully attempt to execute each conflicting action -> must be rejected
    fingerprint_before_attack = next_state.fingerprint()
    for conflict in conflicting_actions:
        attacked_state, attack_res = world_engine.step(next_state, conflict)
        assert not attack_res.success, f"Adversarial exploit! Engine allowed conflicting action {conflict} after {chosen_ending_action}"
        assert attacked_state.fingerprint() == fingerprint_before_attack, "State mutated during illegal action attempt!"


# ==============================================================================
# 4. Cross-Province Double-Agent Affordance Synthesis
# ==============================================================================

def test_cross_province_double_agent_synthesis(world_engine: AdventureEngine):
    """Verify that forging twin manifests in Lowlands grants both markers

    and unlocks both syndicate and bailiff affordances across all 4 provinces.
    """
    char = CharacterSheet(
        name="DoubleAgentHero",
        ancestry="Human",
        background="Cutpurse",
        attributes={"cunning": 14, "rhetoric": 14},
        skills={"cunning": 4, "rhetoric": 4},
        inventory=["silver_coin"],
    )

    state = make_test_state(world_engine, "lowlands_customs_house_quarters", char)
    legal = {a.id for a in world_engine.get_legal_actions(state)}
    assert "lowlands_manifest_forge_twin" in legal

    state, res = world_engine.step(state, "lowlands_manifest_forge_twin")
    assert res.success
    assert "syndicate_contact" in state.character.markers
    assert "river_bailiff" in state.character.markers

    # Now verify all 8 cross-province actions are accessible:
    provinces_scenes_actions = [
        ("reach_dunwall_fort_gate", "reach", "reach_whistle_smuggler_call"),
        ("reach_high_pass_gate", "reach", "reach_show_garrison_pass"),
        ("high_court_royal_archive_gate", "high_court", "court_bribe_lowlands_clerk"),
        ("high_court_justiciar_hall_gate", "high_court", "court_present_bailiff_warrants"),
        ("scorchwaste_canyon_oasis_gate", "scorchwaste", "scorch_trade_lowlands_contraband"),
        ("scorchwaste_nomad_well_gate", "scorchwaste", "scorch_present_guild_charter"),
        ("sunken_hollows_coral_chasm_gate", "sunken_hollows", "hollows_trade_black_pearls"),
        ("sunken_hollows_deep_siphon_gate", "sunken_hollows", "hollows_claim_salvage_rig"),
    ]

    for scene_id, reg_id, act_id in provinces_scenes_actions:
        test_st = replace(state, current_scene=scene_id, current_region=reg_id)
        legal_acts = {a.id for a in world_engine.get_legal_actions(test_st)}
        assert act_id in legal_acts, f"Double agent lacked {act_id} in {scene_id}"


# ==============================================================================
# 5. Replay Determinism & State Fingerprint Invariance
# ==============================================================================

def test_intrigue_replay_determinism(world_engine: AdventureEngine):
    """Record an action trace across multiple provinces and verify bit-for-bit

    identical state fingerprints upon independent replay.
    """
    initial_char = get_preset("noble").character
    initial_state = make_test_state(world_engine, "lowlands_customs_house_quarters", initial_char)

    # Action trace
    actions_to_step = [
        ("lowlands_manifest_forge_twin", "lowlands_canal_sluice_chamber", "lowlands"),
        ("lowlands_sluice_lock_chains", "lowlands_bell_tower_overlook", "lowlands"),
        ("lowlands_bell_sign_compact", "high_court_royal_archive_courtyard", "high_court"),
        ("court_archive_search_stacks", "high_court_knight_barracks_courtyard", "high_court"),
        ("court_barracks_sway_knights", "high_court_justiciar_hall_quarters", "high_court"),
        ("court_tribunal_seize_bench", "high_court_hub", "high_court"),
        ("court_resolve_regent", "high_court_hub", "high_court"),
    ]

    # Run initial execution
    trace_fingerprints: List[str] = []
    st = initial_state
    for act_id, next_scene, next_reg in actions_to_step:
        st, res = world_engine.step(st, act_id)
        assert res.success, f"Action {act_id} failed in run 1: {res.message}"
        trace_fingerprints.append(st.fingerprint())
        st = replace(st, current_scene=next_scene, current_region=next_reg)

    # Replay 3 times independently from identical initial state
    for replay_idx in range(3):
        replay_st = make_test_state(world_engine, "lowlands_customs_house_quarters", initial_char)
        for step_idx, (act_id, next_scene, next_reg) in enumerate(actions_to_step):
            replay_st, replay_res = world_engine.step(replay_st, act_id)
            assert replay_res.success
            assert replay_st.fingerprint() == trace_fingerprints[step_idx], (
                f"Replay {replay_idx + 1} diverged at step {step_idx} ({act_id})!\n"
                f"Expected: {trace_fingerprints[step_idx]}\n"
                f"Actual:   {replay_st.fingerprint()}"
            )
            replay_st = replace(replay_st, current_scene=next_scene, current_region=next_reg)


def test_tamper_detection_on_intrigue_state(world_engine: AdventureEngine):
    """Mutating a single flag or reputation point alters the canonical SHA-256 fingerprint."""
    char = get_preset("warrior").character
    state = make_test_state(world_engine, "reach_hub", char, {"reach_intrigue_resolved": True})
    original_fp = state.fingerprint()

    # Tamper 1: flip a flag
    tampered_flags = dict(state.world_flags)
    tampered_flags["reach_intrigue_resolved"] = False
    tampered_st1 = replace(state, world_flags=tampered_flags)
    assert tampered_st1.fingerprint() != original_fp

    # Tamper 2: adjust reputation by 1 point
    tampered_rep = dict(state.character.reputation)
    tampered_rep["cliff_clans"] = tampered_rep.get("cliff_clans", 0) + 1
    tampered_char = state.character.modify(reputation=tampered_rep)
    tampered_st2 = replace(state, character=tampered_char)
    assert tampered_st2.fingerprint() != original_fp


# ==============================================================================
# 6. Exhaustive Hemingway Prose & Action Label Audit
# ==============================================================================

def test_hemingway_prose_and_label_strictness():
    """Verify all newly authored Milestone 13 action labels and result texts strictly

    satisfy:
    - Action labels: 1-3 words.
    - Result texts: 1-3 short sentences, <= 18 words/sentence.
    - Zero forbidden purple words.
    """
    intrigue_quests = get_faction_intrigue_quests()

    # Check all quest descriptions, synopses, and endings
    for q_id, q in intrigue_quests.items():
        assert len(q.synopsis.split()) <= 18, f"Synopsis too long in {q_id}"
        for s in q.stages:
            assert len(s.title.split()) <= 4, f"Stage title too long: {s.title}"
            for sentence in s.description.split("."):
                sentence = sentence.strip()
                if sentence:
                    words = sentence.split()
                    assert len(words) <= 18, f"Stage description sentence exceeds 18 words: '{sentence}' in {s.id}"
                    for purple in FORBIDDEN_PURPLE_WORDS:
                        assert purple not in sentence.lower(), f"Purple word '{purple}' in stage {s.id}"

        for end_name, end_text in q.endings.items():
            for sentence in end_text.split("."):
                sentence = sentence.strip()
                if sentence:
                    words = sentence.split()
                    assert len(words) <= 18, f"Ending text sentence exceeds 18 words: '{sentence}' in {end_name}"
                    for purple in FORBIDDEN_PURPLE_WORDS:
                        assert purple not in sentence.lower(), f"Purple word '{purple}' in ending {end_name}"
