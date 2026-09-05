"""Comprehensive Verification Suite for Cycle 2: Provincial Subquest Chains.

Tests:
- Subquest retrieval, schema, and backward compatibility.
- All 5 subquest progression paths, stage completions, and multiple endings.
- Integration with AdventureEngine.get_quest_progress.
- Hemingway prose linter verification on all quest synopses and stage descriptions.
- Scene count invariant (exactly 520 scenes).
"""
import pytest
from dataclasses import replace
from typing import Dict, Any

from adventure_forge.content.quests import (
    get_continental_main_quest,
    get_provincial_subquests,
    get_provincial_subquest,
    get_all_quests,
    evaluate_all_subquests,
    evaluate_all_quests,
    subquest_reach_smuggler_caches,
    subquest_lowlands_shadow_broker,
    subquest_scorchwaste_water_baron,
    subquest_court_decrees,
    subquest_hollows_abyssal_keystones,
)
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.content.loader import build_world_registry
from adventure_forge.linter.prose_linter import ProseLinter, word_count


@pytest.fixture
def test_character() -> CharacterSheet:
    return CharacterSheet(name="SubquestHero", ancestry="Plainsman", background="drifter")


def test_subquests_retrieval_and_schema():
    """Verify that all 5 provincial subquests are retrieved and structured correctly."""
    subquests = get_provincial_subquests()
    expected_ids = {
        "subquest_reach_smuggler_caches": "The Reach Smuggler Caches",
        "subquest_lowlands_shadow_broker": "The Lowlands Shadow Broker",
        "subquest_scorchwaste_water_baron": "The Scorchwaste Oasis Water Baron",
        "subquest_court_decrees": "High Court Decrees",
        "subquest_hollows_abyssal_keystones": "Sunken Hollows Abyssal Keystones",
    }

    assert len(subquests) == 5
    for q_id, expected_name in expected_ids.items():
        assert q_id in subquests, f"Missing quest id: {q_id}"
        q = subquests[q_id]
        assert q.name == expected_name
        assert len(q.stages) == 3, f"Expected 3 stages for {q_id}, got {len(q.stages)}"
        assert len(q.endings) >= 3, f"Expected at least 3 endings for {q_id}, got {len(q.endings)}"

    # Test individual retrieval
    assert get_provincial_subquest("subquest_reach_smuggler_caches") is not None
    assert get_provincial_subquest("reach") is not None
    assert get_provincial_subquest("non_existent_quest") is None

    # Test get_all_quests
    all_quests = get_all_quests()
    assert len(all_quests) == 6
    assert all_quests[0].id == "five_seals_campaign"


def test_backward_compatibility_main_quest(test_character: CharacterSheet):
    """Verify get_continental_main_quest retains its contract and functionality."""
    main_quest = get_continental_main_quest()
    assert main_quest.id == "five_seals_campaign"
    assert len(main_quest.stages) == 5

    prog = main_quest.evaluate_progress(test_character, {})
    assert prog["quest_id"] == "five_seals_campaign"
    assert prog["active_stage"] == "stage_crags_beacon"
    assert len(prog["completed_stages"]) == 0
    assert prog["is_finished"] is False


@pytest.mark.parametrize(
    "getter,quest_id,stage_flags,ending_flags,expected_ending",
    [
        # The Reach
        (
            subquest_reach_smuggler_caches,
            "subquest_reach_smuggler_caches",
            [
                {"reach_quarry_cache_found": True},
                {"reach_bluff_cache_recovered": True},
                {"reach_caches_resolved": True},
            ],
            {"reach_cache_smuggler_ending": True},
            "smuggler_syndicate",
        ),
        # The Lowlands
        (
            subquest_lowlands_shadow_broker,
            "subquest_lowlands_shadow_broker",
            [
                {"lowlands_informant_contacted": True},
                {"lowlands_cipher_decoded": True},
                {"lowlands_broker_resolved": True},
            ],
            {"lowlands_broker_allied": True},
            "broker_alliance",
        ),
        # The Scorchwaste
        (
            subquest_scorchwaste_water_baron,
            "subquest_scorchwaste_water_baron",
            [
                {"scorch_aqueduct_inspected": True},
                {"scorch_cistern_diverted": True},
                {"scorch_baron_resolved": True},
            ],
            {"scorch_water_liberated": True},
            "free_water",
        ),
        # High Court
        (
            subquest_court_decrees,
            "subquest_court_decrees",
            [
                {"court_decree_intercepted": True},
                {"court_nobles_swayed": True},
                {"court_decree_resolved": True},
            ],
            {"court_decree_reformed": True},
            "decree_reform",
        ),
        # Sunken Hollows
        (
            subquest_hollows_abyssal_keystones,
            "subquest_hollows_abyssal_keystones",
            [
                {"hollows_grotto_keystone_found": True},
                {"hollows_trench_keystone_found": True},
                {"hollows_gate_resolved": True},
            ],
            {"hollows_gate_unsealed": True},
            "gate_unsealed",
        ),
    ],
)
def test_subquest_step_by_step_progression(
    test_character: CharacterSheet,
    getter: Any,
    quest_id: str,
    stage_flags: list,
    ending_flags: Dict[str, Any],
    expected_ending: str,
):
    """Verify each stage completes sequentially and resolves the target ending."""
    quest = getter()
    flags: Dict[str, Any] = {}

    # Initial state
    prog0 = quest.evaluate_progress(test_character, flags)
    assert prog0["active_stage"] == quest.stages[0].id
    assert len(prog0["completed_stages"]) == 0
    assert prog0["is_finished"] is False

    # Stage 1 complete
    flags.update(stage_flags[0])
    prog1 = quest.evaluate_progress(test_character, flags)
    assert prog1["active_stage"] == quest.stages[1].id
    assert quest.stages[0].id in prog1["completed_stages"]
    assert len(prog1["completed_stages"]) == 1

    # Stage 2 complete
    flags.update(stage_flags[1])
    prog2 = quest.evaluate_progress(test_character, flags)
    assert prog2["active_stage"] == quest.stages[2].id
    assert quest.stages[1].id in prog2["completed_stages"]
    assert len(prog2["completed_stages"]) == 2

    # Stage 3 complete with ending
    flags.update(stage_flags[2])
    flags.update(ending_flags)
    prog3 = quest.evaluate_progress(test_character, flags)
    assert len(prog3["completed_stages"]) == 3
    assert prog3["is_finished"] is True
    assert prog3["ending"] == expected_ending
    assert prog3["active_ending"] == expected_ending


def test_multiple_endings_resolution(test_character: CharacterSheet):
    """Verify all alternate endings for all 5 subquests resolve correctly."""
    # Reach endings
    reach_q = subquest_reach_smuggler_caches()
    base_reach = {
        "reach_quarry_cache_found": True,
        "reach_bluff_cache_recovered": True,
        "reach_caches_resolved": True,
    }
    assert reach_q.evaluate_progress(test_character, {**base_reach, "reach_cache_smuggler_ending": True})["ending"] == "smuggler_syndicate"
    assert reach_q.evaluate_progress(test_character, {**base_reach, "reach_cache_guard_ending": True})["ending"] == "iron_guard_turnin"
    assert reach_q.evaluate_progress(test_character, {**base_reach, "reach_cache_hoard_ending": True})["ending"] == "black_market_hoard"

    # Lowlands endings
    lowlands_q = subquest_lowlands_shadow_broker()
    base_lowlands = {
        "lowlands_informant_contacted": True,
        "lowlands_cipher_decoded": True,
        "lowlands_broker_resolved": True,
    }
    assert lowlands_q.evaluate_progress(test_character, {**base_lowlands, "lowlands_broker_allied": True})["ending"] == "broker_alliance"
    assert lowlands_q.evaluate_progress(test_character, {**base_lowlands, "lowlands_broker_exposed": True})["ending"] == "broker_exposed"
    assert lowlands_q.evaluate_progress(test_character, {**base_lowlands, "lowlands_broker_usurped": True})["ending"] == "broker_usurped"

    # Scorchwaste endings
    scorch_q = subquest_scorchwaste_water_baron()
    base_scorch = {
        "scorch_aqueduct_inspected": True,
        "scorch_cistern_diverted": True,
        "scorch_baron_resolved": True,
    }
    assert scorch_q.evaluate_progress(test_character, {**base_scorch, "scorch_water_liberated": True})["ending"] == "free_water"
    assert scorch_q.evaluate_progress(test_character, {**base_scorch, "scorch_water_negotiated": True})["ending"] == "merchant_treaty"
    assert scorch_q.evaluate_progress(test_character, {**base_scorch, "scorch_water_claimed": True})["ending"] == "new_baron"

    # High Court endings
    court_q = subquest_court_decrees()
    base_court = {
        "court_decree_intercepted": True,
        "court_nobles_swayed": True,
        "court_decree_resolved": True,
    }
    assert court_q.evaluate_progress(test_character, {**base_court, "court_decree_reformed": True})["ending"] == "decree_reform"
    assert court_q.evaluate_progress(test_character, {**base_court, "court_decree_martialed": True})["ending"] == "decree_martial"
    assert court_q.evaluate_progress(test_character, {**base_court, "court_decree_vetoed": True})["ending"] == "decree_veto"

    # Sunken Hollows endings
    hollows_q = subquest_hollows_abyssal_keystones()
    base_hollows = {
        "hollows_grotto_keystone_found": True,
        "hollows_trench_keystone_found": True,
        "hollows_gate_resolved": True,
    }
    assert hollows_q.evaluate_progress(test_character, {**base_hollows, "hollows_gate_unsealed": True})["ending"] == "gate_unsealed"
    assert hollows_q.evaluate_progress(test_character, {**base_hollows, "hollows_gate_warded": True})["ending"] == "gate_warded"
    assert hollows_q.evaluate_progress(test_character, {**base_hollows, "hollows_power_absorbed": True})["ending"] == "power_absorbed"


def test_evaluate_all_quests_helper(test_character: CharacterSheet):
    """Verify evaluate_all_quests and evaluate_all_subquests return clean aggregated dictionaries."""
    flags = {
        "reach_quarry_cache_found": True,
        "crags_beacon_lit": True,
    }
    sub_eval = evaluate_all_subquests(test_character, flags)
    assert len(sub_eval) == 5
    assert "subquest_reach_smuggler_caches" in sub_eval
    assert sub_eval["subquest_reach_smuggler_caches"]["active_stage"] == "reach_cache_stage_recover"

    all_eval = evaluate_all_quests(test_character, flags)
    assert "main_quest" in all_eval
    assert "subquests" in all_eval
    assert all_eval["main_quest"]["quest_id"] == "five_seals_campaign"
    assert all_eval["subquest_reach_smuggler_caches"]["active_stage"] == "reach_cache_stage_recover"


def test_adventure_engine_quest_progress_integration(test_character: CharacterSheet):
    """Verify AdventureEngine.get_quest_progress provides backward compatibility and subquests."""
    engine = AdventureEngine(build_world_registry(cached=False))
    state = GameState(
        build_id=engine.build_id,
        session_id="subquest_integration_session",
        character=test_character,
        current_scene="reach_hub",
        current_region="province_reach",
        world_flags={}
    )

    progress = engine.get_quest_progress(state)

    # Top-level backward compatibility keys
    assert "quest_id" in progress
    assert progress["quest_id"] == "five_seals_campaign"
    assert "completed_stages" in progress
    assert "active_stage" in progress
    assert "is_finished" in progress

    # Subquests key
    assert "subquests" in progress
    subquests = progress["subquests"]
    assert len(subquests) == 5
    assert "subquest_reach_smuggler_caches" in subquests
    assert "subquest_lowlands_shadow_broker" in subquests
    assert "subquest_scorchwaste_water_baron" in subquests
    assert "subquest_court_decrees" in subquests
    assert "subquest_hollows_abyssal_keystones" in subquests


def test_step_systemic_subquest_actions_in_engine(test_character: CharacterSheet):
    """Verify taking systemic subquest actions directly updates state and quest progress."""
    engine = AdventureEngine(build_world_registry(cached=False))
    state = GameState(
        build_id=engine.build_id,
        session_id="reach_subquest_run",
        character=test_character,
        current_scene="reach_granite_mine_vault",
        current_region="province_reach",
        world_flags={}
    )

    # 1. Take search quarry cache action
    state, obs1 = engine.step(state, "reach_search_quarry_cache")
    assert obs1.success
    assert state.world_flags.get("reach_quarry_cache_found") is True
    prog1 = engine.get_quest_progress(state)
    reach_prog1 = prog1["subquests"]["subquest_reach_smuggler_caches"]
    assert "reach_cache_stage_scout" in reach_prog1["completed_stages"]
    assert reach_prog1["active_stage"] == "reach_cache_stage_recover"

    # 2. Transition to bluff vault and take recovery action
    state = replace(state, current_scene="reach_signal_crag_vault")
    state, obs2 = engine.step(state, "reach_recover_bluff_cache")
    assert obs2.success
    assert state.world_flags.get("reach_bluff_cache_recovered") is True
    prog2 = engine.get_quest_progress(state)
    reach_prog2 = prog2["subquests"]["subquest_reach_smuggler_caches"]
    assert "reach_cache_stage_recover" in reach_prog2["completed_stages"]
    assert reach_prog2["active_stage"] == "reach_cache_stage_deliver"

    # 3. Transition to reach hub and resolve ending with smugglers
    state = replace(state, current_scene="reach_hub")
    state, obs3 = engine.step(state, "reach_cache_end_smugglers")
    assert obs3.success
    assert state.world_flags.get("reach_caches_resolved") is True
    assert state.world_flags.get("reach_cache_smuggler_ending") is True
    prog3 = engine.get_quest_progress(state)
    reach_prog3 = prog3["subquests"]["subquest_reach_smuggler_caches"]
    assert reach_prog3["is_finished"] is True
    assert reach_prog3["ending"] == "smuggler_syndicate"


def test_step_lowlands_subquest_actions_in_engine(test_character: CharacterSheet):
    """Verify taking Lowlands subquest actions updates state and subquest progress."""
    engine = AdventureEngine(build_world_registry(cached=False))
    state = GameState(
        build_id=engine.build_id,
        session_id="lowlands_subquest_run",
        character=test_character,
        current_scene="lowlands_oakhaven_port_quarters",
        current_region="province_lowlands",
        world_flags={}
    )

    state, obs1 = engine.step(state, "lowlands_bribe_informant")
    assert obs1.success
    assert state.world_flags.get("lowlands_informant_contacted") is True

    state = replace(state, current_scene="lowlands_customs_house_vault")
    state, obs2 = engine.step(state, "lowlands_steal_cipher")
    assert obs2.success
    assert state.world_flags.get("lowlands_cipher_decoded") is True

    state = replace(state, current_scene="lowlands_hub")
    state, obs3 = engine.step(state, "lowlands_broker_end_ally")
    assert obs3.success
    assert state.world_flags.get("lowlands_broker_resolved") is True
    assert state.world_flags.get("lowlands_broker_allied") is True

    prog = engine.get_quest_progress(state)["subquests"]["subquest_lowlands_shadow_broker"]
    assert prog["is_finished"] is True
    assert prog["ending"] == "broker_alliance"


def test_step_scorchwaste_subquest_actions_in_engine(test_character: CharacterSheet):
    """Verify taking Scorchwaste subquest actions updates state and subquest progress."""
    engine = AdventureEngine(build_world_registry(cached=False))
    state = GameState(
        build_id=engine.build_id,
        session_id="scorchwaste_subquest_run",
        character=test_character,
        current_scene="scorchwaste_salt_pan_vault",
        current_region="province_scorchwaste",
        world_flags={}
    )

    state, obs1 = engine.step(state, "scorch_inspect_aqueduct")
    assert obs1.success
    assert state.world_flags.get("scorch_aqueduct_inspected") is True

    state = replace(state, current_scene="scorchwaste_canyon_oasis_vault")
    state, obs2 = engine.step(state, "scorch_divert_cistern")
    assert obs2.success
    assert state.world_flags.get("scorch_cistern_diverted") is True

    state = replace(state, current_scene="scorchwaste_hub")
    state, obs3 = engine.step(state, "scorch_baron_end_liberate")
    assert obs3.success
    assert state.world_flags.get("scorch_baron_resolved") is True
    assert state.world_flags.get("scorch_water_liberated") is True

    prog = engine.get_quest_progress(state)["subquests"]["subquest_scorchwaste_water_baron"]
    assert prog["is_finished"] is True
    assert prog["ending"] == "free_water"


def test_step_high_court_subquest_actions_in_engine(test_character: CharacterSheet):
    """Verify taking High Court subquest actions updates state and subquest progress."""
    engine = AdventureEngine(build_world_registry(cached=False))
    state = GameState(
        build_id=engine.build_id,
        session_id="court_subquest_run",
        character=test_character,
        current_scene="high_court_royal_archive_vault",
        current_region="province_high_court",
        world_flags={}
    )

    state, obs1 = engine.step(state, "court_intercept_edict")
    assert obs1.success
    assert state.world_flags.get("court_decree_intercepted") is True

    state = replace(state, current_scene="high_court_diplomat_lounge_vault")
    state, obs2 = engine.step(state, "court_sway_nobles")
    assert obs2.success
    assert state.world_flags.get("court_nobles_swayed") is True

    state = replace(state, current_scene="high_court_hub")
    state, obs3 = engine.step(state, "court_decree_end_reform")
    assert obs3.success
    assert state.world_flags.get("court_decree_resolved") is True
    assert state.world_flags.get("court_decree_reformed") is True

    prog = engine.get_quest_progress(state)["subquests"]["subquest_court_decrees"]
    assert prog["is_finished"] is True
    assert prog["ending"] == "decree_reform"


def test_step_sunken_hollows_subquest_actions_in_engine(test_character: CharacterSheet):
    """Verify taking Sunken Hollows subquest actions updates state and subquest progress."""
    engine = AdventureEngine(build_world_registry(cached=False))
    state = GameState(
        build_id=engine.build_id,
        session_id="hollows_subquest_run",
        character=test_character,
        current_scene="sunken_hollows_glow_grotto_vault",
        current_region="province_sunken_hollows",
        world_flags={}
    )

    state, obs1 = engine.step(state, "hollows_pry_grotto_keystone")
    assert obs1.success
    assert state.world_flags.get("hollows_grotto_keystone_found") is True

    state = replace(state, current_scene="sunken_hollows_coral_chasm_vault")
    state, obs2 = engine.step(state, "hollows_dredge_trench_keystone")
    assert obs2.success
    assert state.world_flags.get("hollows_trench_keystone_found") is True

    state = replace(state, current_scene="sunken_hollows_hub")
    state, obs3 = engine.step(state, "hollows_gate_end_unseal")
    assert obs3.success
    assert state.world_flags.get("hollows_gate_resolved") is True
    assert state.world_flags.get("hollows_gate_unsealed") is True

    prog = engine.get_quest_progress(state)["subquests"]["subquest_hollows_abyssal_keystones"]
    assert prog["is_finished"] is True
    assert prog["ending"] == "gate_unsealed"


def test_hemingway_prose_linter_on_all_quests():
    """Verify that all quest synopses, stage descriptions, and endings conform strictly to Hemingway rules."""
    linter = ProseLinter(max_sentence_words=18, max_readability_grade=8.0)
    all_quests = get_all_quests()

    violations = []
    for quest in all_quests:
        # Synopsis
        errs = linter.lint_text(quest.synopsis, context=f"Quest {quest.id} Synopsis")
        if errs:
            violations.extend(errs)

        # Stages
        for stage in quest.stages:
            s_errs = linter.lint_text(stage.description, context=f"Quest {quest.id} Stage {stage.id} Description")
            if s_errs:
                violations.extend(s_errs)
            # Stage titles should also be brief
            t_words = word_count(stage.title)
            if t_words > 6:
                violations.append(f"Stage {stage.id} title exceeds 6 words: {stage.title}")

        # Endings
        for end_id, end_desc in quest.endings.items():
            e_errs = linter.lint_text(end_desc, context=f"Quest {quest.id} Ending {end_id}")
            if e_errs:
                violations.extend(e_errs)

    assert violations == [], "Hemingway prose linter found violations in quest narrative:\n" + "\n".join(violations)


def test_scene_count_and_interactable_density_invariants():
    """Verify that adding subquest actions preserves the 520 total scene count and density invariant."""
    registry = build_world_registry()
    total_scenes = sum(len(r.scenes) for r in registry.values())
    assert total_scenes == 520, f"Critical Invariant Violated: expected 520 scenes, got {total_scenes}"

    dense_scenes = 0
    for r in registry.values():
        for s in r.scenes.values():
            meaningful = len([a for a in s.base_actions if a.category != "movement"]) + len(s.entities)
            if meaningful >= 3:
                dense_scenes += 1

    assert dense_scenes >= 260, f"Interactable density invariant violated: {dense_scenes}/520 dense scenes"
