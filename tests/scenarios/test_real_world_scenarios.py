"""Tier 4: Real-World Application Scenarios (Scenarios 1-5).

Satisfies TEST_INFRA.md:
- Scenario 1: Silas the Cutpurse Infiltration (R1, R2, R4, R5 Social Stealth)
- Scenario 2: Vivienne the High Noble Intrigue (R1, R2, R4, R5 Court Intrigue)
- Scenario 3: Continental Expedition Across 5 Provinces (R1, R4, R5 520 nodes, all 5 mechanics)
- Scenario 4: Unbounded Bazaar Economic Trade (R1, R4 115 legal actions, pagination)
- Scenario 5: Playtester Saboteur Stress Simulation (R1, R4, R6 Flywheel triage, invalid traces)
"""
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry
from adventure_forge.player.cli import render_ui
from adventure_forge.flywheel.playtester import BlindPlaytester
from adventure_forge.flywheel.triage import triage_session_telemetry


def _make_engine():
    return AdventureEngine(build_world_registry())


def test_scenario_1_silas_cutpurse_infiltration():
    """Scenario 1: Silas the Cutpurse Infiltration in Lower Warrens."""
    engine = _make_engine()
    silas = CharacterSheet(
        name="Silas",
        ancestry="Deep-Dweller",
        background="cutpurse",
        attributes={"agility": 14, "strength": 8, "intimidation": 6},
        skills={"cunning": 4, "stealth": 3},
        traits=["night_eyed", "streetwise"],
        flaws=["marked_outlaw"],
        reputation={"smugglers": 10, "city_watch": -10},
        markers=["guild_brand"],
        inventory=["silver_coin"]
    )

    state = GameState(
        build_id=engine.build_id,
        session_id="scenario-1-silas",
        character=silas,
        current_region="lower_warrens",
        current_scene="warrens_gate",
        world_flags={},
        history=[],
        event_log=[],
        turn_count=0,
        rng=DeterministicRNG.from_seed(101)
    )

    # Turn 1: Observe thieves mark and flash thief signet
    obs1 = engine.observe(state)
    assert "thieves mark" in obs1.description.lower()
    legal1 = [a.id for a in engine.get_legal_actions(state)]
    assert "flash_thief_signet" in legal1

    state, res1 = engine.step(state, "flash_thief_signet")
    assert res1.success is True
    assert state.current_scene == "warrens_black_market"
    assert state.character.get_reputation("smugglers") == 15

    # Turn 2: Purchase lockpicks from fence
    legal2 = [a.id for a in engine.get_legal_actions(state)]
    assert "buy_lockpicks" in legal2
    state, res2 = engine.step(state, "buy_lockpicks")
    assert res2.success is True
    assert "lockpick" in state.character.inventory
    assert "silver_coin" not in state.character.inventory

    # Turn 3: Leave market to alley
    state, res3 = engine.step(state, "leave_market")
    assert res3.success is True
    assert state.current_scene == "warrens_alley"

    # Turn 4: Return to gatehouse
    state, res4 = engine.step(state, "back_to_gate")
    assert res4.success is True
    assert state.current_scene == "warrens_gate"

    # Turn 5: Pick sewer grate with acquired lockpicks
    legal5 = [a.id for a in engine.get_legal_actions(state)]
    assert "pick_sewer_grate" in legal5
    state, res5 = engine.step(state, "pick_sewer_grate")
    assert res5.success is True
    assert state.world_flags.get("entity_sewer_grate_state") == "unlocked"
    assert state.turn_count == 5


def test_scenario_2_vivienne_high_noble_intrigue():
    """Scenario 2: Lady Vivienne High Noble Intrigue in High Court."""
    engine = _make_engine()
    vivienne = CharacterSheet(
        name="Lady Vivienne",
        ancestry="High-Kin",
        background="noble_exile",
        attributes={"agility": 8, "strength": 10, "intimidation": 15},
        skills={"rhetoric": 4, "cunning": 2},
        traits=["skeptical", "court_manners"],
        flaws=["oath_bound"],
        reputation={"smugglers": -10, "city_watch": 10, "justiciars": 10},
        markers=["watch_crest"],
        inventory=["legal_dossier", "silver_coin"]
    )

    state = GameState(
        build_id=engine.build_id,
        session_id="scenario-2-vivienne",
        character=vivienne,
        current_region="high_court_local",
        current_scene="court_antechamber",
        world_flags={},
        history=[],
        event_log=[],
        turn_count=0,
        rng=DeterministicRNG.from_seed(202)
    )

    # Turn 1: Present legal dossier to Chief Bailiff
    legal1 = [a.id for a in engine.get_legal_actions(state)]
    assert "present_writ" in legal1
    state, res1 = engine.step(state, "present_writ")
    assert res1.success is True
    assert state.current_scene == "court_tribunal"
    assert state.world_flags.get("granted_court_audience") is True

    # Turn 2: Deliver persuasive argument to high tribunal
    legal2 = [a.id for a in engine.get_legal_actions(state)]
    assert "deliver_argument" in legal2
    state, res2 = engine.step(state, "deliver_argument")
    assert res2.success is True
    assert state.world_flags.get("court_verdict_won") is True
    assert state.character.get_reputation("justiciars") == 25


def test_scenario_3_continental_expedition_across_5_provinces():
    """Scenario 3: Continental Expedition Across 5 Provinces exercising all 5 regional mechanics."""
    engine = _make_engine()
    hero = CharacterSheet(
        name="Wayfarer",
        ancestry="Deep-Dweller",
        background="drifter",
        attributes={"strength": 14, "agility": 14, "endurance": 14},
        skills={"cunning": 3, "stealth": 3},
        traits=["climber", "deep_diver", "heat_hardened"],
        inventory=["climbing_rope", "water_skin", "silver_coin", "lockpick"]
    )

    state = GameState(
        build_id=engine.build_id,
        session_id="scenario-3-expedition",
        character=hero,
        current_region="iron_crags",
        current_scene="crags_base",
        world_flags={},
        history=[],
        event_log=[],
        turn_count=0,
        rng=DeterministicRNG.from_seed(303)
    )

    # 1. Mechanic: Verticality in Iron Crags
    state, _ = engine.step(state, "climb_cliff_face")
    assert state.current_scene == "crags_ridge"
    state, _ = engine.step(state, "climb_down_base")
    assert state.current_scene == "crags_base"

    # 2. Mechanic: Social Stealth in Warrens
    state, _ = engine.step(state, "walk_to_warrens")
    assert state.current_scene == "warrens_gate"
    state, _ = engine.step(state, "pay_gate_toll")
    assert state.current_scene == "warrens_alley"

    # 3. Enter Continental Crossroads (Bazaar)
    state, _ = engine.step(state, "head_to_market")
    assert state.current_scene == "bazaar_center"

    # 4. Mechanic: Heat Survival in Scorchwaste
    state, _ = engine.step(state, "travel_to_scorchwaste")
    assert state.current_scene == "scorch_dunes"
    state, _ = engine.step(state, "drink_canteen")
    assert state.character.stamina >= 10
    state, _ = engine.step(state, "retreat_to_bazaar")
    assert state.current_scene == "bazaar_center"

    # 5. Mechanic: Diving in Sunken Hollows
    state, _ = engine.step(state, "travel_to_hollows")
    assert state.current_scene == "hollows_grotto"
    state, _ = engine.step(state, "dive_into_pool")
    assert state.current_scene == "hollows_temple"
    state, _ = engine.step(state, "take_sunken_relic")
    assert "sunken_pearl" in state.character.inventory
    assert state.world_flags.get("sunken_relic_secured") is True


def test_scenario_4_unbounded_bazaar_economic_trade(capsys):
    """Scenario 4: Unbounded Choice Space in Bazaar with Pagination."""
    engine = _make_engine()
    merchant = CharacterSheet(
        name="Trader",
        ancestry="Plainsman",
        background="drifter",
        inventory=["silver_coin", "silver_coin"]
    )
    state = GameState(
        build_id=engine.build_id,
        session_id="scenario-4-bazaar",
        character=merchant,
        current_region="stress_market",
        current_scene="bazaar_center",
        world_flags={},
        history=[],
        event_log=[],
        turn_count=0,
        rng=DeterministicRNG.from_seed(404)
    )

    obs = engine.observe(state)
    assert len(obs.legal_actions) >= 100

    # Render page 1
    render_ui(obs, page=0, page_size=15)
    captured1 = capsys.readouterr().out
    assert "Page 1 of 8" in captured1
    assert "Showing 1-15" in captured1
    assert "'n' for next page" in captured1

    # Render page 2
    render_ui(obs, page=1, page_size=15)
    captured2 = capsys.readouterr().out
    assert "Page 2 of 8" in captured2
    assert "Showing 16-30" in captured2
    assert "'p' for prev page" in captured2


def test_scenario_5_playtester_saboteur_stress_simulation():
    """Scenario 5: Saboteur Persona with Triage Verification."""
    char = CharacterSheet(
        name="Saboteur",
        ancestry="Ashenborn",
        background="pit_fighter",
        attributes={"strength": 16, "agility": 12},
        traits=["pyromaniac"],
        inventory=["torch", "crowbar"]
    )

    tester = BlindPlaytester(persona="saboteur", seed=505)
    telemetry = tester.run_session(char, start_scene="crags_base", max_turns=6)

    assert telemetry.turn_count > 0
    assert len(telemetry.decisions_made) == telemetry.turn_count

    # Simulate a friction report and test triage
    telemetry.friction_notes.append("Attempted invalid high-risk exploit")
    report = triage_session_telemetry(telemetry, char, start_scene="crags_base")

    assert report is not None
    assert len(report.reproduction_trace) == telemetry.turn_count
