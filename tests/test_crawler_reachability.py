"""Automated Reachability, Solvability, and Action-Execution Tests.

Proves:
- BFS crawler achieves 100% reachability across all 520 scenes.
- Queue draining: no early exit leaves leaf node actions unstepped.
- Exhaustive action stepping: every legal action across all 520 scenes executes cleanly.
- Regression verification for leaf node interactables (node 520 / secret shrine).
"""
from adventure_forge.verification.crawler import crawl_world_graph
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine


def test_graph_reachability_and_solvability():
    """Verify that BFS crawler proves 100% reachability across all 520 scenes without early truncation."""
    passed, msg, stats = crawl_world_graph()
    assert passed, f"{msg}: {stats}"
    assert stats["visited_scenes"] >= 520
    assert len(stats["unvisited_scenes"]) == 0
    # Guard against early-exit blind spot: all visited scenes must be popped and stepped
    assert stats["steps_taken"] >= stats["visited_scenes"], (
        f"Early-exit blind spot detected: only {stats['steps_taken']} scenes popped "
        f"out of {stats['visited_scenes']} visited scenes."
    )


def test_all_scenes_and_actions_execution():
    """Exhaustively step every legal action across all 520 scenes in the world graph.

    Guarantees zero unhandled runtime exceptions (e.g. invalid effect operators,
    broken scene transitions, or unhandled conditions) across all 2,220+ actions.
    """
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    # Master omni-capable character satisfying all prerequisite traits, attributes, skills, and tools
    char = CharacterSheet(
        name="Omni-Tester",
        ancestry="Deep-Dweller",
        background="noble_exile",
        attributes={"strength": 18, "agility": 18, "endurance": 18, "intimidation": 18},
        skills={"cunning": 5, "stealth": 5, "rhetoric": 5},
        traits=["night_eyed", "nimble", "streetwise", "skeptical", "water_breather"],
        flaws=["marked_outlaw"],
        reputation={"iron_guard": 10, "smugglers": 10, "city_watch": 10, "justiciars": 10},
        markers=["guild_brand", "watch_crest"],
        inventory=[
            "climbing_rope", "lockpick", "crowbar", "silver_coin",
            "water_skin", "waterproof_seal", "legal_dossier", "iron_crank"
        ]
    )

    scenes_evaluated = 0
    actions_evaluated = 0
    failed_actions = []

    for reg_id, region in registry.items():
        for scene_id, scene in region.scenes.items():
            scenes_evaluated += 1
            state = GameState(
                build_id="af-test",
                session_id=f"test-{scene_id}",
                character=char,
                current_region=reg_id,
                current_scene=scene_id
            )

            legal_actions = engine.get_legal_actions(state)
            assert len(legal_actions) > 0, f"Scene '{scene_id}' in region '{reg_id}' has zero legal actions."

            for act in legal_actions:
                actions_evaluated += 1
                try:
                    next_state, obs = engine.step(state, act.id)
                    if not obs.success:
                        failed_actions.append((scene_id, act.id, f"Action failed: {obs.message}"))
                except Exception as exc:
                    failed_actions.append((scene_id, act.id, f"{type(exc).__name__}: {exc}"))

    assert scenes_evaluated == 520, f"Expected 520 scenes evaluated, got {scenes_evaluated}"
    assert actions_evaluated >= 2220, f"Expected >= 2220 actions evaluated, got {actions_evaluated}"
    assert len(failed_actions) == 0, (
        f"Action execution failed on {len(failed_actions)} actions:\n"
        + "\n".join(f"  [{s_id}] action '{a_id}': {err}" for s_id, a_id, err in failed_actions)
    )


def test_leaf_node_interactable_effects_regression():
    """Specific regression test for node 520 (reach_secret_shrine) and other terminal interactables.

    Proves that 'reach_secret_shrine_act_1' successfully adds 'ice_lotus' to inventory
    and does not crash with ValueError on unrecognized effect operators.
    """
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    char = CharacterSheet(
        name="Tester",
        ancestry="Deep-Dweller",
        background="drifter",
        traits=["night_eyed"]
    )

    state = GameState(
        build_id="af-test",
        session_id="test-shrine",
        character=char,
        current_region="province_reach",
        current_scene="reach_secret_shrine"
    )

    # 1. Test act_0: Pray at icon
    next_state_0, obs_0 = engine.step(state, "reach_secret_shrine_act_0")
    assert obs_0.success, f"reach_secret_shrine_act_0 failed: {obs_0.message}"
    assert next_state_0.character.stamina >= state.character.stamina

    # 2. Test act_1: Search ice dais (regression target for invalid 'modify_item' operator)
    next_state_1, obs_1 = engine.step(state, "reach_secret_shrine_act_1")
    assert obs_1.success, f"reach_secret_shrine_act_1 failed: {obs_1.message}"
    assert "ice_lotus" in next_state_1.character.inventory, "Expected 'ice_lotus' in inventory after searching ice dais"

    # 3. Test movement return: Return to sanctum
    next_state_2, obs_2 = engine.step(state, "reach_secret_shrine_to_sanctum")
    assert obs_2.success, f"reach_secret_shrine_to_sanctum failed: {obs_2.message}"
    assert next_state_2.current_scene == "reach_frost_cavern_sanctum"
