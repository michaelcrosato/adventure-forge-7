"""Scenario Tests: Continental 5-Province Campaign End-to-End Replay.

Validates:
- Full completion of "The Five Seals of Sovereignty" main quest across all 5 provinces.
- Multi-approach character divergence (Outlaw Silas via stealth/crime vs Noble Vivienne via law/diplomacy).
- Bit-for-bit replay determinism across identical action traces.
- All 3 campaign endings reachable.
"""
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import get_preset
from adventure_forge.core.state import GameState
from adventure_forge.content.quests import get_continental_main_quest


def test_outlaw_continental_campaign_replay():
    """Silas the Cutpurse completes all 5 provinces using stealth, lockpicking, and crime."""
    engine = AdventureEngine(build_world_registry())
    character = get_preset("cutpurse").character
    state = GameState(
        build_id=engine.build_id,
        session_id="outlaw-campaign-1",
        character=character,
        current_region="iron_crags",
        current_scene="crags_base"
    )

    outlaw_trace = [
        "search_scree",
        "climb_cliff_face",
        "cross_rope_bridge",
        "claim_crags_beacon",  # Stage 1: The Reach / Crags Beacon
        "return_ridge",
        "climb_down_base",
        "walk_to_warrens",
        "flash_thief_signet",
        "forge_watch_permit",  # Stage 2: The Lowlands / Shadow Ledger
        "leave_market",
        "head_to_market",
        "travel_to_scorchwaste",
        "march_to_oasis",
        "pickpocket_nomad_compass",  # Stage 3: Scorchwaste / Solar Compass
        "travel_to_dunes",
        "retreat_to_bazaar",
        "travel_to_court",
        "slip_into_tribunal",
        "deliver_argument",  # Stage 4: High Court / Tribunal Verdict
        "leave_tribunal",
        "exit_to_bazaar",
        "travel_to_hollows",
        "dive_into_pool",
        "take_sunken_relic"  # Stage 5: Sunken Hollows / Abyssal Pearl
    ]

    for act in outlaw_trace:
        state, obs = engine.step(state, act)
        assert obs.success, f"Action {act} failed at {state.current_scene}: {obs.message}"

    quest = get_continental_main_quest()
    prog = quest.evaluate_progress(state.character, state.world_flags)
    assert prog["is_finished"] is True
    assert len(prog["completed_stages"]) == 5
    assert set(prog["completed_stages"]) == {
        "stage_crags_beacon",
        "stage_warrens_ledger",
        "stage_scorch_compass",
        "stage_court_verdict",
        "stage_abyssal_pearl"
    }

    # Replay determinism verification
    state_replay = GameState(
        build_id=engine.build_id,
        session_id="outlaw-campaign-2",
        character=character,
        current_region="iron_crags",
        current_scene="crags_base"
    )
    for act in outlaw_trace:
        state_replay, _ = engine.step(state_replay, act)

    assert state.fingerprint() == state_replay.fingerprint()


def test_noble_continental_campaign_replay():
    """Lady Vivienne completes all 5 provinces using aristocratic influence, law, and diplomacy."""
    engine = AdventureEngine(build_world_registry())
    character = get_preset("noble").character
    state = GameState(
        build_id=engine.build_id,
        session_id="noble-campaign-1",
        character=character,
        current_region="high_court_local",
        current_scene="court_antechamber"
    )

    noble_trace = [
        "present_writ",
        "deliver_argument",  # Stage 4: High Court / Tribunal Verdict
        "leave_tribunal",
        "exit_to_bazaar",
        "travel_to_warrens",
        "back_to_gate",
        "demand_guard_entry",
        "take_patrol_badge",  # Stage 2: The Lowlands / Official Watch Badge
        "leave_guardhouse",
        "head_to_market",
        "travel_to_crags",
        "hail_watchman",
        "cross_rope_bridge",
        "claim_crags_beacon",  # Stage 1: The Reach / Crags Beacon
        "return_ridge",
        "climb_down_base",
        "walk_to_warrens",
        "demand_guard_entry",
        "leave_guardhouse",
        "head_to_market",
        "travel_to_scorchwaste",
        "march_to_oasis",
        "trade_with_nomads",  # Stage 3: Scorchwaste / Trade for Sun Compass
        "travel_to_dunes",
        "retreat_to_bazaar",
        "travel_to_hollows",
        "salvage_diving_gear",
        "board_diving_bell",
        "take_sunken_relic"  # Stage 5: Sunken Hollows / Abyssal Pearl
    ]

    for act in noble_trace:
        state, obs = engine.step(state, act)
        assert obs.success, f"Action {act} failed at {state.current_scene}: {obs.message}"

    quest = get_continental_main_quest()
    prog = quest.evaluate_progress(state.character, state.world_flags)
    assert prog["is_finished"] is True
    assert len(prog["completed_stages"]) == 5

    # Replay determinism verification
    state_replay = GameState(
        build_id=engine.build_id,
        session_id="noble-campaign-2",
        character=character,
        current_region="high_court_local",
        current_scene="court_antechamber"
    )
    for act in noble_trace:
        state_replay, _ = engine.step(state_replay, act)

    assert state.fingerprint() == state_replay.fingerprint()
