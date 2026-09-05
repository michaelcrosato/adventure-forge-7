"""Comprehensive Test Suite for Generation 5 Milestone 13:
5-Province Systemic Questlines, Faction Intrigue Arcs, and Cross-Province Web.

Covers:
1. Retrieval and schema verification for all 5 new questlines.
2. Stage-by-stage progression across all 5 provinces.
3. Mutually exclusive resolution of all 18 endings across the 5 questlines.
4. AdventureEngine integration via step(), evaluating real state mutations.
5. Cross-province faction web: Syndicate Contact vs River Bailiff markers.
6. 7-axis character reactivity: counterfactual action divergence.
7. Hemingway prose compliance on all newly authored content.
8. Non-negotiable engine invariants (520 scenes, 100% reachability, 100% density).
"""
import pytest
from dataclasses import replace
from typing import Dict, Any, List

from adventure_forge.content.quests import (
    get_faction_intrigue_quests,
    get_provincial_subquests,
    get_all_quests,
    quest_reach_faction_intrigue,
    quest_high_court_faction_intrigue,
    subquest_scorchwaste_water_wars,
    subquest_hollows_abyssal_schism,
    subquest_lowlands_river_intrigue,
)
from adventure_forge.core.character import CharacterSheet, get_preset
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.content.loader import build_world_registry
from adventure_forge.linter.prose_linter import ProseLinter


@pytest.fixture
def default_hero() -> CharacterSheet:
    return CharacterSheet(
        name="IntrigueAgent",
        ancestry="Human",
        background="Diplomat",
        attributes={"strength": 14, "cunning": 14, "endurance": 14, "agility": 12, "wits": 12, "presence": 12},
        skills={"rhetoric": 4, "cunning": 4, "athletics": 3, "stealth": 3},
        traits=["night_eyed", "amphibious", "streetwise"],
        inventory=["crowbar", "torch", "tuning_fork", "climbing_rope", "chancellor_signet_ring"],
    )


@pytest.fixture
def engine() -> AdventureEngine:
    registry = build_world_registry()
    return AdventureEngine(world_registry=registry)


def make_state(
    eng: AdventureEngine,
    scene_id: str,
    char: CharacterSheet,
    world_flags: Dict[str, Any] | None = None,
) -> GameState:
    region_id = eng.get_region_id_for_scene(scene_id) or "test_region"
    return GameState(
        build_id=eng.build_id,
        session_id="test_session_m13",
        character=char,
        current_region=region_id,
        current_scene=scene_id,
        world_flags=world_flags or {},
    )


# ==============================================================================
# 1. Quest Schema & Backward Compatibility
# ==============================================================================

def test_faction_intrigue_retrieval_and_schema():
    """Verify that all 5 new faction intrigue quests are retrieved and conform to schema."""
    intrigue_quests = get_faction_intrigue_quests()
    assert len(intrigue_quests) == 5, f"Expected 5 intrigue quests, found {len(intrigue_quests)}"

    expected_quests = {
        "quest_reach_faction_intrigue": ("The Sky-Pact of the Crags", 4, 3),
        "quest_high_court_faction_intrigue": ("The Tripartite Throne", 4, 4),
        "subquest_scorchwaste_water_wars": ("The Scorchwaste Water Wars", 4, 4),
        "subquest_hollows_abyssal_schism": ("The Sunken Hollows Abyssal Schism", 4, 4),
        "subquest_lowlands_river_intrigue": ("The Lowlands Sluice War", 3, 3),
    }

    total_endings = 0
    for q_id, (expected_name, stage_count, ending_count) in expected_quests.items():
        assert q_id in intrigue_quests, f"Missing {q_id}"
        q = intrigue_quests[q_id]
        assert q.name == expected_name
        assert len(q.stages) == stage_count, f"{q_id} expected {stage_count} stages, got {len(q.stages)}"
        assert len(q.endings) == ending_count, f"{q_id} expected {ending_count} endings, got {len(q.endings)}"
        assert len(q.ending_conditions) == ending_count, f"{q_id} ending conditions mismatch"
        total_endings += ending_count

        # Every stage must have approaches and valid flags
        for s in q.stages:
            assert len(s.approaches) >= 2, f"Stage {s.id} in {q_id} has fewer than 2 approaches"
            assert len(s.completion_flags) >= 1, f"Stage {s.id} in {q_id} has empty completion flags"

    assert total_endings == 18, f"Expected exactly 18 endings across 5 intrigue arcs, got {total_endings}"


def test_backward_compatibility_defaults():
    """Verify default invocations retain legacy 5 subquests and 6 total quests without intrusion."""
    baseline_subquests = get_provincial_subquests()
    assert len(baseline_subquests) == 5

    baseline_all = get_all_quests()
    assert len(baseline_all) == 6

    # When include_intrigue=True, all 10 subquests and 11 all_quests appear
    full_subquests = get_provincial_subquests(include_intrigue=True)
    assert len(full_subquests) == 10

    full_all = get_all_quests(include_intrigue=True)
    assert len(full_all) == 11


# ==============================================================================
# 2. Stage Progression & Endings for All 5 Provinces
# ==============================================================================

def test_reach_faction_intrigue_full_progression(default_hero: CharacterSheet):
    """Test full 4-stage progression and 3 endings for The Reach intrigue arc."""
    quest = quest_reach_faction_intrigue()
    char = default_hero

    # Initial state
    p0 = quest.evaluate_progress(char, {})
    assert p0["active_stage"] == "reach_intrigue_stage_discovery"
    assert not p0["is_finished"]

    # Stage 1 complete
    p1 = quest.evaluate_progress(char, {"reach_discovery_completed": True})
    assert p1["active_stage"] == "reach_intrigue_stage_escalation"

    # Stage 2 complete
    p2 = quest.evaluate_progress(char, {"reach_discovery_completed": True, "reach_escalation_completed": True})
    assert p2["active_stage"] == "reach_intrigue_stage_dilemma"

    # Stage 3 complete
    p3 = quest.evaluate_progress(char, {
        "reach_discovery_completed": True,
        "reach_escalation_completed": True,
        "reach_dilemma_resolved": True,
    })
    assert p3["active_stage"] == "reach_intrigue_stage_resolution"

    # Stage 4 complete with Ending A: Storm Warden Dominance
    flags_a = {
        "reach_discovery_completed": True,
        "reach_escalation_completed": True,
        "reach_dilemma_resolved": True,
        "reach_intrigue_resolved": True,
        "reach_ending_warden": True,
    }
    pa = quest.evaluate_progress(char, flags_a)
    assert pa["is_finished"]
    assert pa["ending"] == "storm_warden_dominance"

    # Ending B: Cliff Clan Liberation
    flags_b = dict(flags_a)
    del flags_b["reach_ending_warden"]
    flags_b["reach_ending_clan"] = True
    pb = quest.evaluate_progress(char, flags_b)
    assert pb["ending"] == "cliff_clan_liberation"

    # Ending C: Ascetic Harmony
    flags_c = dict(flags_a)
    del flags_c["reach_ending_warden"]
    flags_c["reach_ending_harmony"] = True
    pc = quest.evaluate_progress(char, flags_c)
    assert pc["ending"] == "ascetic_harmony"


def test_high_court_faction_intrigue_full_progression(default_hero: CharacterSheet):
    """Test full 4-stage progression and 4 endings for High Court succession crisis."""
    quest = quest_high_court_faction_intrigue()
    char = default_hero

    # Initial state
    p0 = quest.evaluate_progress(char, {})
    assert p0["active_stage"] == "court_intrigue_stage_discovery"

    # Progress through stages 1, 2, 3
    flags = {
        "court_discovery_completed": True,
        "court_escalation_completed": True,
        "court_dilemma_resolved": True,
        "court_intrigue_resolved": True,
    }

    # Ending 1: Royalist
    p_roy = quest.evaluate_progress(char, {**flags, "court_ending_royalist": True})
    assert p_roy["is_finished"] and p_roy["ending"] == "court_royalist_ascendancy"

    # Ending 2: Ducal
    p_duc = quest.evaluate_progress(char, {**flags, "court_ending_ducal": True})
    assert p_duc["is_finished"] and p_duc["ending"] == "court_ducal_confederacy"

    # Ending 3: Guild
    p_gld = quest.evaluate_progress(char, {**flags, "court_ending_guild": True})
    assert p_gld["is_finished"] and p_gld["ending"] == "court_guild_plutocracy"

    # Ending 4: Regent
    p_reg = quest.evaluate_progress(char, {**flags, "court_ending_regent": True})
    assert p_reg["is_finished"] and p_reg["ending"] == "court_unbounded_protector"


def test_scorchwaste_water_wars_full_progression(default_hero: CharacterSheet):
    """Test full 4-stage progression and 4 endings for Scorchwaste Water Wars."""
    quest = subquest_scorchwaste_water_wars()
    char = default_hero

    p0 = quest.evaluate_progress(char, {})
    assert p0["active_stage"] == "scorch_war_stage_exploration"

    flags = {
        "scorch_pipeline_surveyed": True,
        "scorch_faction_chosen": True,
        "scorch_crisis_resolved": True,
        "scorch_war_resolved": True,
    }

    # 4 endings
    assert quest.evaluate_progress(char, {**flags, "scorch_ending_free_water": True})["ending"] == "free_waters"
    assert quest.evaluate_progress(char, {**flags, "scorch_ending_cartel_monopoly": True})["ending"] == "cartel_monopoly"
    assert quest.evaluate_progress(char, {**flags, "scorch_ending_concordat": True})["ending"] == "desalination_concordat"
    assert quest.evaluate_progress(char, {**flags, "scorch_ending_autocrat": True})["ending"] == "desert_autocrat"


def test_hollows_abyssal_schism_full_progression(default_hero: CharacterSheet):
    """Test full 4-stage progression and 4 endings for Sunken Hollows Abyssal Schism."""
    quest = subquest_hollows_abyssal_schism()
    char = default_hero

    p0 = quest.evaluate_progress(char, {})
    assert p0["active_stage"] == "hollows_schism_stage_exploration"

    flags = {
        "hollows_rapids_navigated": True,
        "hollows_faction_chosen": True,
        "hollows_crisis_resolved": True,
        "hollows_schism_resolved": True,
    }

    # 4 endings
    assert quest.evaluate_progress(char, {**flags, "hollows_ending_archive_sanctuary": True})["ending"] == "archive_sanctuary"
    assert quest.evaluate_progress(char, {**flags, "hollows_ending_cartel_dredge": True})["ending"] == "cartel_dredge"
    assert quest.evaluate_progress(char, {**flags, "hollows_ending_diver_commune": True})["ending"] == "diver_commune"
    assert quest.evaluate_progress(char, {**flags, "hollows_ending_deluge_unsealed": True})["ending"] == "deluge_unsealed"


def test_lowlands_river_intrigue_full_progression(default_hero: CharacterSheet):
    """Test full 3-stage progression and 3 endings for Lowlands Sluice War."""
    quest = subquest_lowlands_river_intrigue()
    char = default_hero

    p0 = quest.evaluate_progress(char, {})
    assert p0["active_stage"] == "lowlands_intrigue_stage_manifest"

    flags = {
        "lowlands_manifest_decided": True,
        "lowlands_sluice_decided": True,
        "lowlands_river_intrigue_resolved": True,
    }

    # 3 endings
    assert quest.evaluate_progress(char, {**flags, "lowlands_intrigue_syndicate_win": True})["ending"] == "syndicate_ascendant"
    assert quest.evaluate_progress(char, {**flags, "lowlands_intrigue_guild_win": True})["ending"] == "river_guild_monopoly"
    assert quest.evaluate_progress(char, {**flags, "lowlands_intrigue_compact_win": True})["ending"] == "clandestine_compact"


# ==============================================================================
# 3. AdventureEngine Live Step Transitions & State Mutations
# ==============================================================================

def test_engine_reach_intrigue_live_execution(engine: AdventureEngine, default_hero: CharacterSheet):
    """Step through Reach faction intrigue via engine.step() and verify real state mutations."""
    state = make_state(engine, "reach_wind_hollow_quarters", default_hero)

    # 1. Stage 1: Inspect cable
    legal = engine.get_legal_actions(state)
    assert any(a.id == "reach_wind_inspect_cable" for a in legal)
    state, res1 = engine.step(state, "reach_wind_inspect_cable")
    assert state.world_flags.get("reach_discovery_completed") is True
    assert state.character.reputation.get("cliff_clans", 0) > 0

    # 2. Travel to mine courtyard for Stage 2
    state = replace(state, current_scene="reach_granite_mine_courtyard", current_region="reach")
    legal = engine.get_legal_actions(state)
    assert any(a.id == "reach_mine_broker_truce" for a in legal)
    state, res2 = engine.step(state, "reach_mine_broker_truce")
    assert state.world_flags.get("reach_escalation_completed") is True

    # 3. Travel to spire quarters for Stage 3 dilemma
    state = replace(state, current_scene="reach_iron_spire_quarters", current_region="reach")
    legal = engine.get_legal_actions(state)
    assert any(a.id == "reach_spire_discharge_crags" for a in legal)
    state, res3 = engine.step(state, "reach_spire_discharge_crags")
    assert state.world_flags.get("reach_dilemma_resolved") is True
    assert state.world_flags.get("reach_diverted_to_gorge") is True

    # 4. Travel to reach_hub for Stage 4 resolution
    state = replace(state, current_scene="reach_hub", current_region="reach")
    legal = engine.get_legal_actions(state)
    assert any(a.id == "reach_resolve_warden_dominance" for a in legal)
    state, res4 = engine.step(state, "reach_resolve_warden_dominance")
    assert state.world_flags.get("reach_intrigue_resolved") is True
    assert state.world_flags.get("reach_ending_warden") is True
    assert state.character.reputation["storm_wardens"] >= 30


def test_engine_court_intrigue_live_execution(engine: AdventureEngine, default_hero: CharacterSheet):
    """Step through High Court intrigue via engine.step()."""
    state = make_state(engine, "high_court_royal_archive_courtyard", default_hero)

    # Stage 1
    state, _ = engine.step(state, "court_archive_search_stacks")
    assert state.world_flags.get("court_discovery_completed") is True

    # Stage 2
    state = replace(state, current_scene="high_court_silver_vault_gate", current_region="high_court")
    state, _ = engine.step(state, "court_vault_pick_sluice")
    assert state.world_flags.get("court_escalation_completed") is True

    # Stage 3
    state = replace(state, current_scene="high_court_justiciar_hall_quarters", current_region="high_court")
    state, _ = engine.step(state, "court_tribunal_seize_bench")
    assert state.world_flags.get("court_dilemma_resolved") is True
    assert state.world_flags.get("court_ruling_regent") is True

    # Stage 4
    state = replace(state, current_scene="high_court_hub", current_region="high_court")
    state, _ = engine.step(state, "court_resolve_regent")
    assert state.world_flags.get("court_intrigue_resolved") is True
    assert state.world_flags.get("court_ending_regent") is True


def test_engine_scorchwaste_water_wars_live_execution(engine: AdventureEngine, default_hero: CharacterSheet):
    """Step through Scorchwaste Water Wars via engine.step()."""
    state = make_state(engine, "scorchwaste_dune_ridge_gate", default_hero)

    # Stage 1
    state, _ = engine.step(state, "scorch_war_survey_pipeline")
    assert state.world_flags.get("scorch_pipeline_surveyed") is True

    # Stage 2
    state = replace(state, current_scene="scorchwaste_canyon_oasis_courtyard", current_region="scorchwaste")
    state, _ = engine.step(state, "scorch_war_pledge_wardens")
    assert state.world_flags.get("scorch_faction_chosen") is True

    # Stage 3
    state = replace(state, current_scene="scorchwaste_nomad_well_quarters", current_region="scorchwaste")
    state, _ = engine.step(state, "scorch_war_purge_brine_pump")
    assert state.world_flags.get("scorch_crisis_resolved") is True

    # Stage 4
    state = replace(state, current_scene="scorchwaste_hub", current_region="scorchwaste")
    state, _ = engine.step(state, "scorch_war_end_free_water")
    assert state.world_flags.get("scorch_war_resolved") is True
    assert state.world_flags.get("scorch_ending_free_water") is True


def test_engine_sunken_hollows_abyssal_schism_live_execution(engine: AdventureEngine, default_hero: CharacterSheet):
    """Step through Sunken Hollows Abyssal Schism via engine.step()."""
    state = make_state(engine, "sunken_hollows_abyssal_river_gate", default_hero)

    # Stage 1
    state, _ = engine.step(state, "hollows_schism_scout_currents")
    assert state.world_flags.get("hollows_rapids_navigated") is True

    # Stage 2
    state = replace(state, current_scene="sunken_hollows_sub_wharf_courtyard", current_region="sunken_hollows")
    state, _ = engine.step(state, "hollows_schism_unionize_divers")
    assert state.world_flags.get("hollows_faction_chosen") is True

    # Stage 3
    state = replace(state, current_scene="sunken_hollows_deep_siphon_quarters", current_region="sunken_hollows")
    state, _ = engine.step(state, "hollows_schism_crank_pressure_valve")
    assert state.world_flags.get("hollows_crisis_resolved") is True

    # Stage 4
    state = replace(state, current_scene="sunken_hollows_hub", current_region="sunken_hollows")
    state, _ = engine.step(state, "hollows_end_diver_commune")
    assert state.world_flags.get("hollows_schism_resolved") is True
    assert state.world_flags.get("hollows_ending_diver_commune") is True


def test_engine_lowlands_river_intrigue_live_execution(engine: AdventureEngine, default_hero: CharacterSheet):
    """Step through Lowlands River Sluice War via engine.step()."""
    state = make_state(engine, "lowlands_customs_house_quarters", default_hero)

    # Stage 1: Deliver to Syndicate
    state, _ = engine.step(state, "lowlands_manifest_give_syndicate")
    assert state.world_flags.get("lowlands_manifest_decided") is True
    assert "syndicate_contact" in state.character.markers

    # Stage 2: Sluice Winch
    state = replace(state, current_scene="lowlands_canal_sluice_chamber", current_region="lowlands")
    state, _ = engine.step(state, "lowlands_sluice_sabotage_winch")
    assert state.world_flags.get("lowlands_sluice_decided") is True

    # Stage 3: Bell Tower Showdown
    state = replace(state, current_scene="lowlands_bell_tower_overlook", current_region="lowlands")
    state, _ = engine.step(state, "lowlands_bell_signal_syndicate")
    assert state.world_flags.get("lowlands_river_intrigue_resolved") is True
    assert state.world_flags.get("lowlands_intrigue_syndicate_win") is True
    assert state.character.reputation["shadow_syndicate"] >= 30


# ==============================================================================
# 4. Cross-Province Web: Lowlands Faction Markers Grant Cross-Province Affordances
# ==============================================================================

def test_cross_province_syndicate_contact_affordances(engine: AdventureEngine):
    """Test that syndicate_contact marker from Lowlands unlocks cross-province options."""
    char_with_contact = CharacterSheet(name="SyndicateHero", ancestry="Human", background="Rogue", markers=["syndicate_contact"])
    char_without_contact = CharacterSheet(name="PlainHero", ancestry="Human", background="Rogue", markers=[])

    # 1. Reach: dunwall fort gate
    s_reach = make_state(engine, "reach_dunwall_fort_gate", char_with_contact)
    s_reach_no = make_state(engine, "reach_dunwall_fort_gate", char_without_contact)
    assert any(a.id == "reach_whistle_smuggler_call" for a in engine.get_legal_actions(s_reach))
    assert not any(a.id == "reach_whistle_smuggler_call" for a in engine.get_legal_actions(s_reach_no))

    # 2. High Court: archive gate
    s_court = make_state(engine, "high_court_royal_archive_gate", char_with_contact)
    s_court_no = make_state(engine, "high_court_royal_archive_gate", char_without_contact)
    assert any(a.id == "court_bribe_lowlands_clerk" for a in engine.get_legal_actions(s_court))
    assert not any(a.id == "court_bribe_lowlands_clerk" for a in engine.get_legal_actions(s_court_no))

    # 3. Scorchwaste: canyon oasis gate
    s_scorch = make_state(engine, "scorchwaste_canyon_oasis_gate", char_with_contact)
    s_scorch_no = make_state(engine, "scorchwaste_canyon_oasis_gate", char_without_contact)
    assert any(a.id == "scorch_trade_lowlands_contraband" for a in engine.get_legal_actions(s_scorch))
    assert not any(a.id == "scorch_trade_lowlands_contraband" for a in engine.get_legal_actions(s_scorch_no))

    # 4. Sunken Hollows: coral chasm gate
    s_hollow = make_state(engine, "sunken_hollows_coral_chasm_gate", char_with_contact)
    s_hollow_no = make_state(engine, "sunken_hollows_coral_chasm_gate", char_without_contact)
    assert any(a.id == "hollows_trade_black_pearls" for a in engine.get_legal_actions(s_hollow))
    assert not any(a.id == "hollows_trade_black_pearls" for a in engine.get_legal_actions(s_hollow_no))


def test_cross_province_river_bailiff_affordances(engine: AdventureEngine):
    """Test that river_bailiff marker from Lowlands unlocks cross-province options."""
    char_with_bailiff = CharacterSheet(name="BailiffHero", ancestry="Human", background="Enforcer", markers=["river_bailiff"])
    char_without_bailiff = CharacterSheet(name="PlainHero", ancestry="Human", background="Enforcer", markers=[])

    # 1. Reach: high pass gate
    s_reach = make_state(engine, "reach_high_pass_gate", char_with_bailiff)
    s_reach_no = make_state(engine, "reach_high_pass_gate", char_without_bailiff)
    assert any(a.id == "reach_show_garrison_pass" for a in engine.get_legal_actions(s_reach))
    assert not any(a.id == "reach_show_garrison_pass" for a in engine.get_legal_actions(s_reach_no))

    # 2. High Court: justiciar hall gate
    s_court = make_state(engine, "high_court_justiciar_hall_gate", char_with_bailiff)
    s_court_no = make_state(engine, "high_court_justiciar_hall_gate", char_without_bailiff)
    assert any(a.id == "court_present_bailiff_warrants" for a in engine.get_legal_actions(s_court))
    assert not any(a.id == "court_present_bailiff_warrants" for a in engine.get_legal_actions(s_court_no))

    # 3. Scorchwaste: nomad well gate
    s_scorch = make_state(engine, "scorchwaste_nomad_well_gate", char_with_bailiff)
    s_scorch_no = make_state(engine, "scorchwaste_nomad_well_gate", char_without_bailiff)
    assert any(a.id == "scorch_present_guild_charter" for a in engine.get_legal_actions(s_scorch))
    assert not any(a.id == "scorch_present_guild_charter" for a in engine.get_legal_actions(s_scorch_no))

    # 4. Sunken Hollows: deep siphon gate
    s_hollow = make_state(engine, "sunken_hollows_deep_siphon_gate", char_with_bailiff)
    s_hollow_no = make_state(engine, "sunken_hollows_deep_siphon_gate", char_without_bailiff)
    assert any(a.id == "hollows_claim_salvage_rig" for a in engine.get_legal_actions(s_hollow))
    assert not any(a.id == "hollows_claim_salvage_rig" for a in engine.get_legal_actions(s_hollow_no))


# ==============================================================================
# 5. 7-Axis Character Reactivity & Counterfactual Witness Proofs
# ==============================================================================

def test_counterfactual_character_reactivity_in_intrigue_scenes(engine: AdventureEngine):
    """Demonstrate that distinct character builds experience divergence in intrigue scenes."""
    silas = get_preset("cutpurse").character      # cutpurse: cunning, streetwise, stealth
    vivienne = get_preset("noble").character       # noble: presence, rhetoric, decorum
    garron = get_preset("warrior").character       # warrior: high strength, athletics
    mara = get_preset("diver").character           # diver: water_breather / endurance

    # In High Court Justiciar Hall Quarters (with escalation flag):
    flags = {"court_escalation_completed": True}
    s_silas = make_state(engine, "high_court_justiciar_hall_quarters", silas, flags)
    s_viv = make_state(engine, "high_court_justiciar_hall_quarters", vivienne, flags)

    actions_silas = {a.id for a in engine.get_legal_actions(s_silas)}
    actions_viv = {a.id for a in engine.get_legal_actions(s_viv)}

    # Vivienne has high rhetoric to seize the regency, Silas lacks it unless having the ring
    assert "court_tribunal_seize_bench" in actions_viv
    assert "court_tribunal_seize_bench" not in actions_silas

    # In Sunken Hollows Abyssal River Gate:
    s_mara = make_state(engine, "sunken_hollows_abyssal_river_gate", mara)
    s_silas_sub = make_state(engine, "sunken_hollows_abyssal_river_gate", silas)
    actions_mara = {a.id for a in engine.get_legal_actions(s_mara)}
    actions_silas_sub = {a.id for a in engine.get_legal_actions(s_silas_sub)}

    # Mara has high athletics to dive the subterranean rapids immediately
    assert "hollows_schism_dive_rapids" in actions_mara
    assert "hollows_schism_dive_rapids" not in actions_silas_sub

    # In Scorchwaste Nomad Well Quarters:
    scorch_flags = {"scorch_faction_chosen": True}
    s_garron = make_state(engine, "scorchwaste_nomad_well_quarters", garron, scorch_flags)
    s_viv_scorch = make_state(engine, "scorchwaste_nomad_well_quarters", vivienne, scorch_flags)

    actions_garron = {a.id for a in engine.get_legal_actions(s_garron)}
    actions_viv_scorch = {a.id for a in engine.get_legal_actions(s_viv_scorch)}

    # Garron has brute strength 16 to purge the brine pump
    assert "scorch_war_purge_brine_pump" in actions_garron
    assert "scorch_war_purge_brine_pump" not in actions_viv_scorch


# ==============================================================================
# 6. Hemingway Prose Compliance
# ==============================================================================

def test_hemingway_prose_compliance_all_intrigue_content():
    """Verify that all newly authored intrigue quests, stages, and action texts pass ProseLinter."""
    linter = ProseLinter()
    intrigue_quests = get_faction_intrigue_quests()

    errors: List[str] = []
    for q_id, q in intrigue_quests.items():
        # Check synopsis
        errs = linter.lint_text(q.synopsis, f"Quest {q_id} Synopsis", check_readability=False)
        errors.extend(errs)

        # Check stages
        for s in q.stages:
            errs = linter.lint_text(s.description, f"Quest {q_id} Stage {s.id}", check_readability=False)
            errors.extend(errs)

        # Check endings
        for end_name, end_text in q.endings.items():
            errs = linter.lint_text(end_text, f"Quest {q_id} Ending {end_name}", check_readability=False)
            errors.extend(errs)

    assert len(errors) == 0, "Prose linter found errors in intrigue content:\n" + "\n".join(errors)


# ==============================================================================
# 7. World Scale & Invariant Incorruptibility
# ==============================================================================

def test_macro_world_invariants_preserved():
    """Ensure world scale is strictly 520 scenes and density invariant is satisfied."""
    registry = build_world_registry()
    total_scenes = sum(len(r.scenes) for r in registry.values())
    assert total_scenes == 520, f"Expected exactly 520 scenes, got {total_scenes}"

    # Density: at least 260 scenes must offer >= 3 interactables/entities
    qualifying = 0
    for r in registry.values():
        for s in r.scenes.values():
            non_movement = [a for a in s.base_actions if a.category != "movement"]
            entities = getattr(s, "entities", [])
            if len(non_movement) + len(entities) >= 3:
                qualifying += 1

    assert qualifying >= 260, f"Interactable density invariant violated: {qualifying}/520"
    assert qualifying == 520, f"Expected 100% density (520/520), got {qualifying}"
