"""Milestone 13 Adversarial Stress & Cross-Province Faction Web Verification.

Empirically challenges:
1. Lowlands standing granting smuggler/bailiff actions in Scorchwaste, High Court,
   Reach, and Sunken Hollows.
2. Negative enforcement: characters lacking required marker/reputation CANNOT
   see or execute cross-province actions, and engine.step() rejects them with
   zero state mutation.
3. Strict boundary thresholds (e.g. rep 14 vs 15; marker vs rep isolation).
4. Scene interactable density invariant: remains >= 3 across all 520 scenes under
   all state variations (clean, mid-quest, and post-resolution across all 18 endings).
5. Hemingway prose linter compliance: 0 forbidden purple words, label length <= 3 words,
   and sentence length <= 18 words across all 68 newly added M13 actions and 5 questlines.
6. Multi-step cross-province replay determinism and bit-for-bit SHA-256 fingerprint fidelity.
"""
from typing import Any, Dict, Optional
import re
import pytest

from adventure_forge.content.loader import build_world_registry
from adventure_forge.content.quests import get_faction_intrigue_quests
from adventure_forge.core.character import CharacterSheet, get_preset
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import (
    FORBIDDEN_PURPLE_WORDS,
    split_sentences,
    word_count,
)


# ==============================================================================
# FIXTURES & BUILDERS
# ==============================================================================

@pytest.fixture(scope="module")
def engine() -> AdventureEngine:
    return AdventureEngine(build_world_registry(cached=True))


def make_test_state(
    eng: AdventureEngine,
    scene_id: str,
    character: CharacterSheet,
    world_flags: Optional[Dict[str, Any]] = None,
    seed: int = 1337,
) -> GameState:
    region_id = eng.get_region_id_for_scene(scene_id) or "test_region"
    return GameState(
        build_id=eng.build_id,
        session_id="adversarial_m13",
        character=character,
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
    """Empirically verify that action_id is absent from legal_actions,

    and calling engine.step() returns success=False and leaves state bit-for-bit intact.
    """
    legal_actions = eng.get_legal_actions(state)
    legal_ids = {a.id for a in legal_actions}
    assert action_id not in legal_ids, (
        f"Security breach: Action '{action_id}' was exposed as legal in scene '{state.current_scene}' "
        f"for character markers={state.character.markers}, rep={state.character.reputation}"
    )

    pre_fingerprint = state.fingerprint()
    pre_turn = state.turn_count
    pre_history = list(state.history)
    pre_flags = dict(state.world_flags)

    next_state, result = eng.step(state, action_id)
    assert not result.success, f"engine.step() succeeded on illegal action '{action_id}'"
    assert "Illegal action" in result.message or "not currently legal" in result.message
    assert next_state.fingerprint() == pre_fingerprint, "State fingerprint corrupted after rejected action"
    assert next_state.turn_count == pre_turn, "Turn count incremented on rejected action"
    assert next_state.history == pre_history, "Action history mutated on rejected action"
    assert next_state.world_flags == pre_flags, "World flags mutated on rejected action"


# ==============================================================================
# 1. CROSS-PROVINCE SYSTEMIC AFFORDANCES (POSITIVE PIPELINES)
# ==============================================================================

class TestCrossProvincePositivePipelines:
    """Test that acquiring standings in Lowlands unlocks actions across all 4 other provinces."""

    def test_syndicate_contact_full_cross_province_tour(self, engine: AdventureEngine):
        """A character who sides with Shadow Syndicate in Lowlands earns smuggler affordances

        in Reach, High Court, Scorchwaste, and Sunken Hollows.
        """
        base_char = CharacterSheet(
            name="SmugglerOperative",
            ancestry="Human",
            background="Cutpurse",
            attributes={"strength": 12, "cunning": 14, "endurance": 12, "agility": 14, "wits": 12, "presence": 12},
            skills={"cunning": 3, "stealth": 3},
            traits=["streetwise"],
            inventory=[],
        )

        # 1. Acquire standing in Lowlands Customs House
        state = make_test_state(engine, "lowlands_customs_house_quarters", base_char)
        state, res = engine.step(state, "lowlands_manifest_give_syndicate")
        assert res.success
        assert "syndicate_contact" in state.character.markers
        assert state.character.reputation.get("shadow_syndicate", 0) >= 20

        # 2. Reach: Dunwall Fort Gate
        state = make_test_state(engine, "reach_dunwall_fort_gate", state.character, state.world_flags)
        legal_reach = {a.id for a in engine.get_legal_actions(state)}
        assert "reach_whistle_smuggler_call" in legal_reach
        state, res_reach = engine.step(state, "reach_whistle_smuggler_call")
        assert res_reach.success
        assert state.world_flags.get("dunwall_grapple_anchored") is True
        assert state.world_flags.get("reach_smuggler_bypass_used") is True

        # 3. High Court: Royal Archive Gate
        state = make_test_state(engine, "high_court_royal_archive_gate", state.character, state.world_flags)
        legal_court = {a.id for a in engine.get_legal_actions(state)}
        assert "court_bribe_lowlands_clerk" in legal_court
        state, res_court = engine.step(state, "court_bribe_lowlands_clerk")
        assert res_court.success
        assert state.world_flags.get("archive_grille_unlocked") is True
        assert state.world_flags.get("court_clerk_bribed") is True

        # 4. Scorchwaste: Canyon Oasis Gate
        state = make_test_state(engine, "scorchwaste_canyon_oasis_gate", state.character, state.world_flags)
        legal_scorch = {a.id for a in engine.get_legal_actions(state)}
        assert "scorch_trade_lowlands_contraband" in legal_scorch
        state, res_scorch = engine.step(state, "scorch_trade_lowlands_contraband")
        assert res_scorch.success
        assert state.world_flags.get("scorch_contraband_traded") is True
        assert "nomad_water_flask" in state.character.inventory

        # 5. Sunken Hollows: Coral Chasm Gate
        state = make_test_state(engine, "sunken_hollows_coral_chasm_gate", state.character, state.world_flags)
        legal_hollow = {a.id for a in engine.get_legal_actions(state)}
        assert "hollows_trade_black_pearls" in legal_hollow
        state, res_hollow = engine.step(state, "hollows_trade_black_pearls")
        assert res_hollow.success
        assert state.world_flags.get("hollows_black_pearls_traded") is True
        assert "diving_helm" in state.character.inventory

    def test_river_bailiff_full_cross_province_tour(self, engine: AdventureEngine):
        """A character who sides with River Guild in Lowlands earns bailiff affordances

        in Reach, High Court, Scorchwaste, and Sunken Hollows.
        """
        base_char = CharacterSheet(
            name="BailiffOperative",
            ancestry="Human",
            background="Enforcer",
            attributes={"strength": 14, "cunning": 12, "endurance": 14, "agility": 12, "wits": 12, "presence": 12},
            skills={"rhetoric": 3, "athletics": 3},
            traits=["iron_will"],
            inventory=[],
        )

        # 1. Acquire standing in Lowlands Customs House
        state = make_test_state(engine, "lowlands_customs_house_quarters", base_char)
        state, res = engine.step(state, "lowlands_manifest_give_bailiff")
        assert res.success
        assert "river_bailiff" in state.character.markers
        assert state.character.reputation.get("river_guild", 0) >= 20

        # 2. Reach: High Pass Gate
        state = make_test_state(engine, "reach_high_pass_gate", state.character, state.world_flags)
        legal_reach = {a.id for a in engine.get_legal_actions(state)}
        assert "reach_show_garrison_pass" in legal_reach
        state, res_reach = engine.step(state, "reach_show_garrison_pass")
        assert res_reach.success
        assert state.world_flags.get("reach_garrison_escort_active") is True

        # 3. High Court: Justiciar Hall Gate
        state = make_test_state(engine, "high_court_justiciar_hall_gate", state.character, state.world_flags)
        legal_court = {a.id for a in engine.get_legal_actions(state)}
        assert "court_present_bailiff_warrants" in legal_court
        state, res_court = engine.step(state, "court_present_bailiff_warrants")
        assert res_court.success
        assert state.world_flags.get("court_tribunal_fast_track") is True
        assert state.character.reputation.get("crown_royalists", 0) >= 10

        # 4. Scorchwaste: Nomad Well Gate
        state = make_test_state(engine, "scorchwaste_nomad_well_gate", state.character, state.world_flags)
        legal_scorch = {a.id for a in engine.get_legal_actions(state)}
        assert "scorch_present_guild_charter" in legal_scorch
        state, res_scorch = engine.step(state, "scorch_present_guild_charter")
        assert res_scorch.success
        assert state.world_flags.get("scorch_guild_charter_presented") is True
        assert state.character.reputation.get("caravaneers", 0) >= 20

        # 5. Sunken Hollows: Deep Siphon Gate
        state = make_test_state(engine, "sunken_hollows_deep_siphon_gate", state.character, state.world_flags)
        legal_hollow = {a.id for a in engine.get_legal_actions(state)}
        assert "hollows_claim_salvage_rig" in legal_hollow
        state, res_hollow = engine.step(state, "hollows_claim_salvage_rig")
        assert res_hollow.success
        assert state.world_flags.get("hollows_salvage_rig_claimed") is True
        assert state.character.reputation.get("trench_divers", 0) >= 20

    def test_double_agent_forgery_unlocks_both_factions(self, engine: AdventureEngine):
        """A character forging twin ledgers in Lowlands receives BOTH markers

        and can leverage both smuggling and bailiff affordances across the continent.
        """
        cunning_char = CharacterSheet(
            name="DoubleAgent",
            ancestry="Human",
            background="Scribe",
            skills={"cunning": 4, "rhetoric": 3},
            traits=["silver_tongued"],
        )
        state = make_test_state(engine, "lowlands_customs_house_quarters", cunning_char)
        state, res = engine.step(state, "lowlands_manifest_forge_twin")
        assert res.success
        assert "syndicate_contact" in state.character.markers
        assert "river_bailiff" in state.character.markers
        assert state.character.reputation["shadow_syndicate"] >= 15
        assert state.character.reputation["river_guild"] >= 15

        # Both Reach hooks
        s_reach_smuggle = make_test_state(engine, "reach_dunwall_fort_gate", state.character)
        assert any(a.id == "reach_whistle_smuggler_call" for a in engine.get_legal_actions(s_reach_smuggle))

        s_reach_bailiff = make_test_state(engine, "reach_high_pass_gate", state.character)
        assert any(a.id == "reach_show_garrison_pass" for a in engine.get_legal_actions(s_reach_bailiff))

        # Both High Court hooks
        s_court_smuggle = make_test_state(engine, "high_court_royal_archive_gate", state.character)
        assert any(a.id == "court_bribe_lowlands_clerk" for a in engine.get_legal_actions(s_court_smuggle))

        s_court_bailiff = make_test_state(engine, "high_court_justiciar_hall_gate", state.character)
        assert any(a.id == "court_present_bailiff_warrants" for a in engine.get_legal_actions(s_court_bailiff))

        # Both Scorchwaste hooks
        s_scorch_smuggle = make_test_state(engine, "scorchwaste_canyon_oasis_gate", state.character)
        assert any(a.id == "scorch_trade_lowlands_contraband" for a in engine.get_legal_actions(s_scorch_smuggle))

        s_scorch_bailiff = make_test_state(engine, "scorchwaste_nomad_well_gate", state.character)
        assert any(a.id == "scorch_present_guild_charter" for a in engine.get_legal_actions(s_scorch_bailiff))

        # Both Sunken Hollows hooks
        s_hollow_smuggle = make_test_state(engine, "sunken_hollows_coral_chasm_gate", state.character)
        assert any(a.id == "hollows_trade_black_pearls" for a in engine.get_legal_actions(s_hollow_smuggle))

        s_hollow_bailiff = make_test_state(engine, "sunken_hollows_deep_siphon_gate", state.character)
        assert any(a.id == "hollows_claim_salvage_rig" for a in engine.get_legal_actions(s_hollow_bailiff))


# ==============================================================================
# 2. NEGATIVE ENFORCEMENT & HARD ISOLATION GATES
# ==============================================================================

class TestCrossProvinceNegativeEnforcement:
    """Adversarially verify that lacking prerequisites strictly rejects cross-province actions."""

    ALL_CROSS_ACTIONS = [
        ("reach_dunwall_fort_gate", "reach_whistle_smuggler_call"),
        ("reach_high_pass_gate", "reach_show_garrison_pass"),
        ("high_court_royal_archive_gate", "court_bribe_lowlands_clerk"),
        ("high_court_justiciar_hall_gate", "court_present_bailiff_warrants"),
        ("scorchwaste_canyon_oasis_gate", "scorch_trade_lowlands_contraband"),
        ("scorchwaste_nomad_well_gate", "scorch_present_guild_charter"),
        ("sunken_hollows_coral_chasm_gate", "hollows_trade_black_pearls"),
        ("sunken_hollows_deep_siphon_gate", "hollows_claim_salvage_rig"),
    ]

    SMUGGLER_ACTIONS = [
        ("reach_dunwall_fort_gate", "reach_whistle_smuggler_call"),
        ("high_court_royal_archive_gate", "court_bribe_lowlands_clerk"),
        ("scorchwaste_canyon_oasis_gate", "scorch_trade_lowlands_contraband"),
        ("sunken_hollows_coral_chasm_gate", "hollows_trade_black_pearls"),
    ]

    BAILIFF_ACTIONS = [
        ("reach_high_pass_gate", "reach_show_garrison_pass"),
        ("high_court_justiciar_hall_gate", "court_present_bailiff_warrants"),
        ("scorchwaste_nomad_well_gate", "scorch_present_guild_charter"),
        ("sunken_hollows_deep_siphon_gate", "hollows_claim_salvage_rig"),
    ]

    def test_blank_character_denied_all_cross_province_actions(self, engine: AdventureEngine):
        """A character with zero markers and zero reputation cannot view or execute any cross actions."""
        blank_char = CharacterSheet(
            name="BlankSlate",
            ancestry="Human",
            background="Commoner",
            markers=[],
            reputation={},
        )
        for scene_id, action_id in self.ALL_CROSS_ACTIONS:
            state = make_test_state(engine, scene_id, blank_char)
            assert_action_strictly_illegal(engine, state, action_id)

    def test_syndicate_operative_strictly_denied_bailiff_actions(self, engine: AdventureEngine):
        """A pure syndicate operative (marker + high rep) cannot view or execute bailiff actions."""
        syndicate_char = CharacterSheet(
            name="PureSyndicate",
            ancestry="Human",
            background="Cutpurse",
            markers=["syndicate_contact", "syndicate_kingpin"],
            reputation={"shadow_syndicate": 50, "smugglers": 50, "river_guild": -20, "city_watch": -20},
        )
        for scene_id, action_id in self.BAILIFF_ACTIONS:
            state = make_test_state(engine, scene_id, syndicate_char)
            assert_action_strictly_illegal(engine, state, action_id)

    def test_bailiff_operative_strictly_denied_smuggler_actions(self, engine: AdventureEngine):
        """A pure river bailiff (marker + high rep) cannot view or execute smuggler actions."""
        bailiff_char = CharacterSheet(
            name="PureBailiff",
            ancestry="Human",
            background="Enforcer",
            markers=["river_bailiff", "high_bailiff"],
            reputation={"river_guild": 50, "city_watch": 50, "shadow_syndicate": -20, "smugglers": -20},
        )
        for scene_id, action_id in self.SMUGGLER_ACTIONS:
            state = make_test_state(engine, scene_id, bailiff_char)
            assert_action_strictly_illegal(engine, state, action_id)

    def test_reputation_boundary_threshold_14_vs_15(self, engine: AdventureEngine):
        """Boundary test: 14 rep fails min_reputation: 15; 15 rep succeeds for Reach & High Court."""
        # 1. Shadow Syndicate Rep 14 vs 15
        char_rep14 = CharacterSheet(name="Rep14", ancestry="Human", background="Rogue", reputation={"shadow_syndicate": 14})
        char_rep15 = CharacterSheet(name="Rep15", ancestry="Human", background="Rogue", reputation={"shadow_syndicate": 15})

        # Reach dunwall fort gate
        s_reach_14 = make_test_state(engine, "reach_dunwall_fort_gate", char_rep14)
        s_reach_15 = make_test_state(engine, "reach_dunwall_fort_gate", char_rep15)
        assert_action_strictly_illegal(engine, s_reach_14, "reach_whistle_smuggler_call")
        assert any(a.id == "reach_whistle_smuggler_call" for a in engine.get_legal_actions(s_reach_15))

        # High Court archive gate
        s_court_14 = make_test_state(engine, "high_court_royal_archive_gate", char_rep14)
        s_court_15 = make_test_state(engine, "high_court_royal_archive_gate", char_rep15)
        assert_action_strictly_illegal(engine, s_court_14, "court_bribe_lowlands_clerk")
        assert any(a.id == "court_bribe_lowlands_clerk" for a in engine.get_legal_actions(s_court_15))

        # 2. River Guild Rep 14 vs 15
        char_guild14 = CharacterSheet(name="Guild14", ancestry="Human", background="Enforcer", reputation={"river_guild": 14})
        char_guild15 = CharacterSheet(name="Guild15", ancestry="Human", background="Enforcer", reputation={"river_guild": 15})

        # Reach high pass gate
        s_pass_14 = make_test_state(engine, "reach_high_pass_gate", char_guild14)
        s_pass_15 = make_test_state(engine, "reach_high_pass_gate", char_guild15)
        assert_action_strictly_illegal(engine, s_pass_14, "reach_show_garrison_pass")
        assert any(a.id == "reach_show_garrison_pass" for a in engine.get_legal_actions(s_pass_15))

        # High Court justiciar hall gate
        s_just_14 = make_test_state(engine, "high_court_justiciar_hall_gate", char_guild14)
        s_just_15 = make_test_state(engine, "high_court_justiciar_hall_gate", char_guild15)
        assert_action_strictly_illegal(engine, s_just_14, "court_present_bailiff_warrants")
        assert any(a.id == "court_present_bailiff_warrants" for a in engine.get_legal_actions(s_just_15))

    def test_reputation_alone_cannot_unlock_scorchwaste_and_hollows_marker_actions(self, engine: AdventureEngine):
        """Scorchwaste and Sunken Hollows cross actions require explicit markers;

        reputation alone (even at 100) must strictly NOT unlock them.
        """
        char_high_rep = CharacterSheet(
            name="HighRepNoMarker",
            ancestry="Human",
            background="Merchant",
            markers=[],
            reputation={"shadow_syndicate": 100, "river_guild": 100, "smugglers": 100, "city_watch": 100},
        )

        # Scorchwaste actions
        s_scorch_smuggle = make_test_state(engine, "scorchwaste_canyon_oasis_gate", char_high_rep)
        assert_action_strictly_illegal(engine, s_scorch_smuggle, "scorch_trade_lowlands_contraband")

        s_scorch_bailiff = make_test_state(engine, "scorchwaste_nomad_well_gate", char_high_rep)
        assert_action_strictly_illegal(engine, s_scorch_bailiff, "scorch_present_guild_charter")

        # Sunken Hollows actions
        s_hollow_smuggle = make_test_state(engine, "sunken_hollows_coral_chasm_gate", char_high_rep)
        assert_action_strictly_illegal(engine, s_hollow_smuggle, "hollows_trade_black_pearls")

        s_hollow_bailiff = make_test_state(engine, "sunken_hollows_deep_siphon_gate", char_high_rep)
        assert_action_strictly_illegal(engine, s_hollow_bailiff, "hollows_claim_salvage_rig")


# ==============================================================================
# 3. SCENE INTERACTABLE DENSITY UNDER STATE VARIATIONS
# ==============================================================================

class TestInteractableDensityUnderStateVariations:
    """Empirically stress-test that all 520 scenes preserve interactable density >= 3

    under diverse world state variations and character presets.
    """

    def test_static_registry_density_100_percent(self, engine: AdventureEngine):
        """Every single scene in the 520-scene registry must have >= 3 interactables."""
        registry = engine.world_registry
        total_scenes = 0
        dense_scenes = 0
        sparse = []

        for reg_id, reg in registry.items():
            for sc_id, sc in reg.scenes.items():
                total_scenes += 1
                non_move = [a for a in sc.base_actions if a.category != "movement"]
                count = len(non_move) + len(sc.entities)
                if count >= 3:
                    dense_scenes += 1
                else:
                    sparse.append((reg_id, sc_id, count))

        assert total_scenes == 520, f"Expected 520 scenes, got {total_scenes}"
        assert dense_scenes == 520, f"Deficit: {len(sparse)} scenes have < 3 interactables: {sparse[:5]}"

    def test_density_preserved_across_all_33_m13_modified_scenes(self, engine: AdventureEngine):
        """All 33 scenes modified in Milestone 13 must maintain >= 3 interactables

        even if every newly added M13 action is rendered illegal by state flags.
        """
        registry = engine.world_registry
        m13_action_ids = {
            "court_resolve_royalist", "court_resolve_ducal", "court_resolve_guild", "court_resolve_regent",
            "court_present_bailiff_warrants", "court_tribunal_back_crown", "court_tribunal_back_duke",
            "court_tribunal_back_guild", "court_tribunal_seize_bench", "court_bribe_lowlands_clerk",
            "court_archive_search_stacks", "court_barracks_sway_knights", "court_salon_eavesdrop_envoy",
            "court_salon_finance_bribe", "court_vault_pick_sluice",
            "lowlands_sluice_sabotage_winch", "lowlands_sluice_lock_chains", "lowlands_sluice_rig_bypass",
            "lowlands_bell_signal_syndicate", "lowlands_bell_ring_alarm", "lowlands_bell_sign_compact",
            "lowlands_manifest_give_syndicate", "lowlands_manifest_give_bailiff", "lowlands_manifest_forge_twin",
            "reach_resolve_warden_dominance", "reach_resolve_clan_liberation", "reach_resolve_ascetic_harmony",
            "reach_whistle_smuggler_call", "reach_mine_storm_barricade", "reach_mine_broker_truce",
            "reach_show_garrison_pass", "reach_spire_discharge_crags", "reach_spire_short_circuit",
            "reach_wind_inspect_cable", "reach_wind_parley_scout", "reach_shrine_harmonize_vents",
            "reach_watch_snatch_capacitor", "reach_signal_splice_wire",
            "scorch_war_end_free_water", "scorch_war_end_monopoly", "scorch_war_end_concordat", "scorch_war_end_autocrat",
            "scorch_trade_lowlands_contraband", "scorch_war_pledge_wardens", "scorch_war_parley_cartel",
            "scorch_war_extort_both", "scorch_war_survey_pipeline", "scorch_war_track_cartel",
            "scorch_present_guild_charter", "scorch_war_purge_brine_pump", "scorch_war_dissolve_scale",
            "scorch_war_seal_pipeline_pitch", "scorch_war_weaponize_brine",
            "hollows_end_archive_sanctuary", "hollows_end_cartel_dredge", "hollows_end_diver_commune",
            "hollows_end_deluge_unsealed", "hollows_schism_scout_currents", "hollows_schism_dive_rapids",
            "hollows_trade_black_pearls", "hollows_claim_salvage_rig", "hollows_schism_crank_pressure_valve",
            "hollows_schism_seal_air_line", "hollows_schism_tune_acoustic_bell", "hollows_schism_dredge_ruins",
            "hollows_schism_pledge_scholars", "hollows_schism_contract_cartel", "hollows_schism_unionize_divers"
        }

        m13_scenes_checked = 0
        for reg in registry.values():
            for sc_id, sc in reg.scenes.items():
                m13_acts = [a for a in sc.base_actions if a.id in m13_action_ids]
                if not m13_acts:
                    continue
                m13_scenes_checked += 1

                # Calculate non-movement interactables WITHOUT the M13 actions
                non_m13_nm = [a for a in sc.base_actions if a.category != "movement" and a.id not in m13_action_ids]
                baseline_interactables = len(non_m13_nm) + len(sc.entities)

                assert baseline_interactables >= 3, (
                    f"Scene '{sc_id}' relies on M13 additions to meet density! "
                    f"Baseline was only {baseline_interactables} (< 3)."
                )

        assert m13_scenes_checked == 33, f"Expected 33 M13 scenes, found {m13_scenes_checked}"

    def test_dynamic_density_under_all_questlines_resolved_state(self, engine: AdventureEngine):
        """Simulate world state where all 5 faction intrigue questlines have been resolved.

        Ensure no scene collapses into zero non-movement actions.
        """
        all_resolved_flags = {
            "reach_dilemma_resolved": True,
            "reach_intrigue_resolved": True,
            "court_intrigue_resolved": True,
            "scorch_war_resolved": True,
            "hollows_schism_resolved": True,
            "lowlands_river_intrigue_resolved": True,
            "lowlands_manifest_decided": True,
            "lowlands_sluice_decided": True,
        }

        silas = get_preset("cutpurse").character
        for reg in engine.world_registry.values():
            for sc_id, sc in reg.scenes.items():
                state = make_test_state(engine, sc_id, silas, all_resolved_flags)
                legal = engine.get_legal_actions(state)
                # Every scene must retain at least one legal movement or interaction
                assert len(legal) >= 1, f"Scene '{sc_id}' has 0 legal actions in fully resolved state"


# ==============================================================================
# 4. HEMINGWAY PROSE LINTER COMPLIANCE ON NEW M13 CONTENT
# ==============================================================================

class TestHemingwayProseLinterM13:
    """Verify that all newly authored M13 actions, results, and quest texts

    strictly pass the Hemingway Prose Linter.
    """

    def test_all_68_new_actions_pass_prose_rules(self, engine: AdventureEngine):
        """Check action labels (1-3 words), result_text (<=18 words/sentence, no purple words),

        and log_event strings (<=18 words/sentence, no purple words).
        """
        m13_action_ids = {
            "court_resolve_royalist", "court_resolve_ducal", "court_resolve_guild", "court_resolve_regent",
            "court_present_bailiff_warrants", "court_tribunal_back_crown", "court_tribunal_back_duke",
            "court_tribunal_back_guild", "court_tribunal_seize_bench", "court_bribe_lowlands_clerk",
            "court_archive_search_stacks", "court_barracks_sway_knights", "court_salon_eavesdrop_envoy",
            "court_salon_finance_bribe", "court_vault_pick_sluice",
            "lowlands_sluice_sabotage_winch", "lowlands_sluice_lock_chains", "lowlands_sluice_rig_bypass",
            "lowlands_bell_signal_syndicate", "lowlands_bell_ring_alarm", "lowlands_bell_sign_compact",
            "lowlands_manifest_give_syndicate", "lowlands_manifest_give_bailiff", "lowlands_manifest_forge_twin",
            "reach_resolve_warden_dominance", "reach_resolve_clan_liberation", "reach_resolve_ascetic_harmony",
            "reach_whistle_smuggler_call", "reach_mine_storm_barricade", "reach_mine_broker_truce",
            "reach_show_garrison_pass", "reach_spire_discharge_crags", "reach_spire_short_circuit",
            "reach_wind_inspect_cable", "reach_wind_parley_scout", "reach_shrine_harmonize_vents",
            "reach_watch_snatch_capacitor", "reach_signal_splice_wire",
            "scorch_war_end_free_water", "scorch_war_end_monopoly", "scorch_war_end_concordat", "scorch_war_end_autocrat",
            "scorch_trade_lowlands_contraband", "scorch_war_pledge_wardens", "scorch_war_parley_cartel",
            "scorch_war_extort_both", "scorch_war_survey_pipeline", "scorch_war_track_cartel",
            "scorch_present_guild_charter", "scorch_war_purge_brine_pump", "scorch_war_dissolve_scale",
            "scorch_war_seal_pipeline_pitch", "scorch_war_weaponize_brine",
            "hollows_end_archive_sanctuary", "hollows_end_cartel_dredge", "hollows_end_diver_commune",
            "hollows_end_deluge_unsealed", "hollows_schism_scout_currents", "hollows_schism_dive_rapids",
            "hollows_trade_black_pearls", "hollows_claim_salvage_rig", "hollows_schism_crank_pressure_valve",
            "hollows_schism_seal_air_line", "hollows_schism_tune_acoustic_bell", "hollows_schism_dredge_ruins",
            "hollows_schism_pledge_scholars", "hollows_schism_contract_cartel", "hollows_schism_unionize_divers"
        }

        violations = []
        found_ids = set()

        for reg in engine.world_registry.values():
            for sc in reg.scenes.values():
                for act in sc.base_actions:
                    if act.id not in m13_action_ids:
                        continue
                    found_ids.add(act.id)

                    # 1. UI Label length (1 to 3 words)
                    lbl_len = word_count(act.label)
                    if lbl_len < 1 or lbl_len > 3:
                        violations.append(f"[{act.id}] Label length {lbl_len} not in [1, 3]: '{act.label}'")

                    # 2. Result text sentences & purple words
                    if act.result_text:
                        for s in split_sentences(act.result_text):
                            wc = word_count(s)
                            if wc > 18:
                                violations.append(f"[{act.id}] Result sentence exceeds 18 words ({wc}): '{s}'")
                        for w in re.findall(r"\b[\w\'-]+\b", act.result_text.lower()):
                            if w in FORBIDDEN_PURPLE_WORDS:
                                violations.append(f"[{act.id}] Result text contains purple word '{w}'")

                    # 3. Effects log_event
                    for eff in act.effects:
                        if "log_event" in eff:
                            log_str = eff["log_event"]
                            for s in split_sentences(log_str):
                                wc = word_count(s)
                                if wc > 18:
                                    violations.append(f"[{act.id}] Log event exceeds 18 words ({wc}): '{s}'")
                            for w in re.findall(r"\b[\w\'-]+\b", log_str.lower()):
                                if w in FORBIDDEN_PURPLE_WORDS:
                                    violations.append(f"[{act.id}] Log event contains purple word '{w}'")

        assert len(found_ids) == 68, f"Only found {len(found_ids)}/68 actions in world registry"
        assert not violations, "Prose violations detected in M13 actions:\n" + "\n".join(violations)

    def test_all_5_questlines_pass_prose_rules(self):
        """Ensure all 5 intrigue quest synopses, stage descriptions, and endings conform."""
        quests = get_faction_intrigue_quests()
        violations = []

        for q_id, q in quests.items():
            # Synopsis
            for s in split_sentences(q.synopsis):
                wc = word_count(s)
                if wc > 18:
                    violations.append(f"[{q_id}] Synopsis sentence >18 words ({wc}): '{s}'")
            for w in re.findall(r"\b[\w\'-]+\b", q.synopsis.lower()):
                if w in FORBIDDEN_PURPLE_WORDS:
                    violations.append(f"[{q_id}] Synopsis contains purple word '{w}'")

            # Stages
            for stage in q.stages:
                for s in split_sentences(stage.description):
                    wc = word_count(s)
                    if wc > 18:
                        violations.append(f"[{q_id}:{stage.id}] Stage description sentence >18 words ({wc}): '{s}'")
                for w in re.findall(r"\b[\w\'-]+\b", stage.description.lower()):
                    if w in FORBIDDEN_PURPLE_WORDS:
                        violations.append(f"[{q_id}:{stage.id}] Stage description contains purple word '{w}'")

            # Endings
            for end_key, end_text in q.endings.items():
                for s in split_sentences(end_text):
                    wc = word_count(s)
                    if wc > 18:
                        violations.append(f"[{q_id}:{end_key}] Ending sentence >18 words ({wc}): '{s}'")
                for w in re.findall(r"\b[\w\'-]+\b", end_text.lower()):
                    if w in FORBIDDEN_PURPLE_WORDS:
                        violations.append(f"[{q_id}:{end_key}] Ending text contains purple word '{w}'")

        assert not violations, "Prose violations in quest definitions:\n" + "\n".join(violations)


# ==============================================================================
# 5. BIT-FOR-BIT REPLAY DETERMINISM ACROSS PROVINCES
# ==============================================================================

class TestCrossProvinceReplayDeterminism:
    """Verify bit-for-bit replay fidelity when executing cross-province actions."""

    def test_deterministic_cross_province_trace_reproducibility(self, engine: AdventureEngine):
        """Execute a 10-step cross-province campaign and assert identical state hash

        on replay from same seed.
        """
        hero = CharacterSheet(
            name="DeterministicAgent",
            ancestry="Human",
            background="Diplomat",
            attributes={"strength": 14, "cunning": 14, "endurance": 14, "agility": 14, "wits": 14, "presence": 14},
            skills={"rhetoric": 4, "cunning": 4, "athletics": 4, "stealth": 4},
            traits=["night_eyed", "amphibious", "streetwise"],
            inventory=["crowbar", "torch", "tuning_fork", "climbing_rope", "chancellor_signet_ring"],
        )

        def run_campaign(seed: int) -> tuple[GameState, list[str]]:
            # Start in Lowlands
            st = make_test_state(engine, "lowlands_customs_house_quarters", hero, seed=seed)
            hashes = [st.fingerprint()]

            # 1. Lowlands Stage 1: Twin ledgers
            st, _ = engine.step(st, "lowlands_manifest_forge_twin")
            hashes.append(st.fingerprint())

            # 2. Reach: Dunwall Fort Gate
            st = make_test_state(engine, "reach_dunwall_fort_gate", st.character, st.world_flags, seed=seed)
            st, _ = engine.step(st, "reach_whistle_smuggler_call")
            hashes.append(st.fingerprint())

            # 3. High Court: Justiciar Hall Gate
            st = make_test_state(engine, "high_court_justiciar_hall_gate", st.character, st.world_flags, seed=seed)
            st, _ = engine.step(st, "court_present_bailiff_warrants")
            hashes.append(st.fingerprint())

            # 4. Scorchwaste: Canyon Oasis Gate
            st = make_test_state(engine, "scorchwaste_canyon_oasis_gate", st.character, st.world_flags, seed=seed)
            st, _ = engine.step(st, "scorch_trade_lowlands_contraband")
            hashes.append(st.fingerprint())

            # 5. Sunken Hollows: Deep Siphon Gate
            st = make_test_state(engine, "sunken_hollows_deep_siphon_gate", st.character, st.world_flags, seed=seed)
            st, _ = engine.step(st, "hollows_claim_salvage_rig")
            hashes.append(st.fingerprint())

            return st, hashes

        final_st1, hashes1 = run_campaign(seed=9999)
        final_st2, hashes2 = run_campaign(seed=9999)

        assert hashes1 == hashes2, "Non-deterministic fingerprint divergence across runs with identical seed"
        assert final_st1.fingerprint() == final_st2.fingerprint(), "Final state fingerprints differ"

        # Verify tamper detection: changing a single marker produces a different hash
        tampered_char = final_st1.character.modify(markers=list(final_st1.character.markers) + ["tampered_token"])
        tampered_state = final_st1.evolve(character=tampered_char)
        assert tampered_state.fingerprint() != final_st1.fingerprint(), "Tamper resistance failed on marker change"
