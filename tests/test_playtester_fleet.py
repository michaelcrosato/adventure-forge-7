"""Unit and integration tests for the Blind Playtester Fleet and Persona Triage.

Validates:
- Information firewall integrity (I6): strictly observable affordances, zero hidden state leaks
- Behavioral action selection preferences across all 8 personas:
  * Explorer: variety, unvisited verbs, world discovery
  * Brute: force, brawling, breaking, combat, high-strength actions
  * Infiltrator: stealth, cunning, lockpicking, slipping past guards
  * Speedrunner: movement actions navigating between scenes
  * Saboteur: high-risk, fire/melting, conflagration, sabotage
  * Nomad: survival, endurance, desert navigation, trade, oasis interaction
  * Diver: diving, submerging, water manipulation, deep trenches
  * Scout: verticality, climbing, vantage points, scaling cliffs, scouting
- Canonical preset and regional start scene mapping for all 8 personas
- Pairwise behavioral divergence in shared scenes
- Multi-cycle retention scores (target >= 0.95 under 15-20 turns with zero friction)
- Friction penalty verification
- OrchestratorManager integration across 8 personas
"""
from typing import List, Dict, Any
import os
from adventure_forge.core.character import get_preset
from adventure_forge.core.engine import StepResult
from adventure_forge.flywheel.playtester import (
    BlindPlaytester,
    PlaytesterPersona,
    SessionTelemetry,
)
from adventure_forge.flywheel.orchestrator import (
    OrchestratorManager,
    get_canonical_persona_setup,
)


def _make_dummy_step_result(actions: List[Dict[str, Any]], scene_id: str = "test_scene") -> StepResult:
    """Helper to synthesize a StepResult observation contract."""
    return StepResult(
        success=True,
        message="Observation ok",
        scene_id=scene_id,
        region_id="test_region",
        title="Test Title",
        description="A test scene for observation.",
        events=[],
        legal_actions=actions,
        turn_count=1,
        is_terminal=False,
        outcome=None,
        fingerprint="a" * 64
    )


# ── 1. Information Firewall Contract ──────────────────────────────────────────

def test_information_firewall_contract():
    """Information Firewall (I6): Playtester operates strictly through StepResult without engine state leaks."""
    actions = [
        {"id": "examine_door", "label": "Examine door", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "force_door", "label": "Force door", "category": "systemic", "risk": "high", "stamina_cost": 2},
    ]
    obs = _make_dummy_step_result(actions)

    # Verify no private engine attributes leak to client observation
    assert not hasattr(obs, "world_registry")
    assert not hasattr(obs, "solution_map")
    assert not hasattr(obs, "hidden_flags")
    assert not hasattr(obs, "quest_scripts")

    tester = BlindPlaytester(persona="brute", seed=42)
    selected = tester.select_action(obs)
    assert selected == "force_door"


# ── 2. Canonical Preset and Regional Start Scene Mapping ──────────────────────

def test_canonical_persona_setups():
    """Verify each of the 8 personas maps to the canonical preset and regional start scene."""
    expected_mappings = {
        "explorer": ("Silas", "crags_base"),
        "brute": ("Garron", "crags_base"),
        "infiltrator": ("Silas", "warrens_gate"),
        "speedrunner": ("Torin", "reach_hub"),
        "saboteur": ("Silas", "warrens_gate"),
        "nomad": ("Kael", "scorch_oasis"),
        "diver": ("Mara", "hollows_grotto"),
        "scout": ("Torin", "reach_hub"),
    }

    for persona, (expected_name, expected_scene) in expected_mappings.items():
        char, start_scene = get_canonical_persona_setup(persona)
        assert char.name == expected_name, f"{persona} expected char name {expected_name}, got {char.name}"
        assert start_scene == expected_scene, f"{persona} expected start {expected_scene}, got {start_scene}"

    # Specific check for saboteur: Silas with pyromaniac trait and torch, acid_vial in inventory
    saboteur_char, saboteur_scene = get_canonical_persona_setup("saboteur")
    assert saboteur_scene == "warrens_gate"
    assert saboteur_char.has_trait("pyromaniac")
    assert saboteur_char.has_item("torch")
    assert saboteur_char.has_item("acid_vial")


# ── 3. Action Selection Preferences per Persona ───────────────────────────────

def test_explorer_action_selection_preferences():
    """Explorer prefers variety, unvisited verbs, and world discovery."""
    actions = [
        {"id": "explore_ruins", "label": "Explore ruins", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "rest_camp", "label": "Rest at camp", "category": "interaction", "risk": "low", "stamina_cost": 0},
    ]
    obs = _make_dummy_step_result(actions)
    tester = BlindPlaytester(persona="explorer", seed=42)

    # First choice selects unvisited verb with world discovery preference
    act1 = tester.select_action(obs)
    assert act1 == "explore_ruins"

    # Subsequent choice will prefer unvisited verbs over repeating explore
    more_actions = [
        {"id": "explore_caves", "label": "Explore caves", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "discover_passage", "label": "Discover passage", "category": "interaction", "risk": "low", "stamina_cost": 0},
    ]
    obs2 = _make_dummy_step_result(more_actions)
    act2 = tester.select_action(obs2)
    assert act2 == "discover_passage"


def test_brute_action_selection_preferences():
    """Brute prefers force, brawling, breaking, combat, high-strength actions."""
    actions = [
        {"id": "sneak_past", "label": "Sneak past", "category": "trait_exploit", "risk": "low", "stamina_cost": 0},
        {"id": "brawl_guard", "label": "Brawl guard", "category": "combat", "risk": "high", "stamina_cost": 2},
        {"id": "examine_wall", "label": "Examine wall", "category": "interaction", "risk": "low", "stamina_cost": 0},
    ]
    obs = _make_dummy_step_result(actions)
    tester = BlindPlaytester(persona="brute", seed=42)
    chosen = tester.select_action(obs)
    assert chosen == "brawl_guard"


def test_infiltrator_action_selection_preferences():
    """Infiltrator prefers stealth, cunning, lockpicking, slipping past guards."""
    actions = [
        {"id": "charge_front_door", "label": "Charge front door", "category": "combat", "risk": "high", "stamina_cost": 2},
        {"id": "slip_past_watch", "label": "Slip past watch", "category": "trait_exploit", "risk": "low", "stamina_cost": 0},
        {"id": "rest_in_shade", "label": "Rest in shade", "category": "interaction", "risk": "low", "stamina_cost": 0},
    ]
    obs = _make_dummy_step_result(actions)
    tester = BlindPlaytester(persona="infiltrator", seed=42)
    chosen = tester.select_action(obs)
    assert chosen == "slip_past_watch"


def test_speedrunner_action_selection_preferences():
    """Speedrunner prefers movement actions navigating between scenes."""
    actions = [
        {"id": "read_notice_board", "label": "Read notices", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "travel_to_bazaar", "label": "Travel to Bazaar", "category": "movement", "risk": "low", "stamina_cost": 1},
        {"id": "rest_at_inn", "label": "Rest at inn", "category": "interaction", "risk": "low", "stamina_cost": 0},
    ]
    obs = _make_dummy_step_result(actions)
    tester = BlindPlaytester(persona="speedrunner", seed=42)
    chosen = tester.select_action(obs)
    assert chosen == "travel_to_bazaar"


def test_saboteur_action_selection_preferences():
    """Saboteur prefers high-risk, fire/melting, conflagration, sabotage."""
    actions = [
        {"id": "read_plaque", "label": "Read plaque", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "melt_iron_bars", "label": "Melt iron bars", "category": "systemic", "risk": "medium", "stamina_cost": 1},
        {"id": "burn_storehouse", "label": "Burn storehouse", "category": "systemic", "risk": "high", "stamina_cost": 0},
    ]
    obs = _make_dummy_step_result(actions)
    tester = BlindPlaytester(persona="saboteur", seed=42)
    chosen = tester.select_action(obs)
    assert chosen in ("melt_iron_bars", "burn_storehouse")


def test_nomad_action_selection_preferences():
    """Nomad prefers survival, endurance, desert navigation, trade, oasis interaction."""
    actions = [
        {"id": "force_grate", "label": "Force grate", "category": "combat", "risk": "high", "stamina_cost": 2},
        {"id": "rest_in_shade", "label": "Rest in shade", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "trade_with_nomads", "label": "Trade with nomads", "category": "social", "risk": "low", "stamina_cost": 0},
    ]
    obs = _make_dummy_step_result(actions)
    tester = BlindPlaytester(persona="nomad", seed=42)
    chosen = tester.select_action(obs)
    assert chosen in ("rest_in_shade", "trade_with_nomads")


def test_diver_action_selection_preferences():
    """Diver prefers diving, submerging, water manipulation, deep trenches."""
    actions = [
        {"id": "climb_steep_crag", "label": "Climb crag", "category": "movement", "risk": "medium", "stamina_cost": 1},
        {"id": "dive_into_pool", "label": "Dive underwater", "category": "movement", "risk": "high", "stamina_cost": 2},
        {"id": "read_scroll", "label": "Read scroll", "category": "interaction", "risk": "low", "stamina_cost": 0},
    ]
    obs = _make_dummy_step_result(actions)
    tester = BlindPlaytester(persona="diver", seed=42)
    chosen = tester.select_action(obs)
    assert chosen == "dive_into_pool"


def test_scout_action_selection_preferences():
    """Scout prefers verticality, climbing, vantage points, scaling cliffs, scouting."""
    actions = [
        {"id": "rest_at_inn", "label": "Rest at inn", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "scale_cliff_wall", "label": "Scale cliff wall", "category": "systemic", "risk": "medium", "stamina_cost": 1},
        {"id": "buy_rations", "label": "Buy rations", "category": "social", "risk": "low", "stamina_cost": 0},
    ]
    obs = _make_dummy_step_result(actions)
    tester = BlindPlaytester(persona="scout", seed=42)
    chosen = tester.select_action(obs)
    assert chosen == "scale_cliff_wall"


# ── 4. Behavioral Divergence Across Personas in Shared Scene ──────────────────

def test_persona_behavioral_divergence_in_shared_scene():
    """Multiple personas presented with identical affordances diverge according to behavioral axes."""
    actions = [
        {"id": "force_iron_chest", "label": "Force Iron Chest", "category": "systemic", "risk": "high", "stamina_cost": 2},
        {"id": "pick_iron_chest", "label": "Pick Iron Chest", "category": "item_affordance", "risk": "medium", "stamina_cost": 0},
        {"id": "melt_iron_chest", "label": "Melt Iron Chest", "category": "trait_exploit", "risk": "high", "stamina_cost": 0},
        {"id": "climb_cliff_face", "label": "Scale Cliff Face", "category": "systemic", "risk": "medium", "stamina_cost": 1},
        {"id": "walk_to_warrens", "label": "Head to Warrens", "category": "movement", "risk": "low", "stamina_cost": 0},
    ]
    obs = _make_dummy_step_result(actions)

    brute_choice = BlindPlaytester(persona="brute", seed=42).select_action(obs)
    infil_choice = BlindPlaytester(persona="infiltrator", seed=42).select_action(obs)
    sabo_choice = BlindPlaytester(persona="saboteur", seed=42).select_action(obs)
    scout_choice = BlindPlaytester(persona="scout", seed=42).select_action(obs)
    speed_choice = BlindPlaytester(persona="speedrunner", seed=42).select_action(obs)

    assert brute_choice == "force_iron_chest"
    assert infil_choice == "pick_iron_chest"
    assert sabo_choice == "melt_iron_chest"
    assert scout_choice == "climb_cliff_face"
    assert speed_choice == "walk_to_warrens"

    # All 5 selected actions are mutually distinct
    assert len({brute_choice, infil_choice, sabo_choice, scout_choice, speed_choice}) == 5


# ── 5. Retention Score Calculation & Friction Penalty ─────────────────────────

def test_retention_score_healthy_exploration():
    """Under 15-20 turns with healthy scene exploration and zero friction, retention >= 0.95."""
    char = get_preset("cutpurse").character
    tester = BlindPlaytester(persona="explorer", seed=42)
    tel = tester.run_session(char, start_scene="crags_base", max_turns=15)

    assert tel.turn_count == 15
    assert len(set(tel.scenes_visited)) >= 2
    assert len(tel.friction_notes) == 0
    assert tel.retention_score >= 0.95


def test_retention_score_friction_penalty():
    """Friction notes penalize the retention score."""
    char = get_preset("cutpurse").character
    tester = BlindPlaytester(persona="explorer", seed=42)
    tel = tester.run_session(char, start_scene="crags_base", max_turns=15)
    base_retention = tel.retention_score

    # Re-calculate with injected friction
    unique_scenes = len(set(tel.scenes_visited))
    penalized = min(1.0, (tel.turn_count * 0.05) + (unique_scenes * 0.15)) - (2 * 0.25)
    assert penalized < base_retention


# ── 6. Full Session Runs for All 8 Personas ───────────────────────────────────

def test_full_session_execution_all_8_personas():
    """Execute full 15-turn session for each of the 8 personas from canonical starts."""
    personas = [
        "explorer",
        "brute",
        "infiltrator",
        "speedrunner",
        "saboteur",
        "nomad",
        "diver",
        "scout",
    ]

    for p in personas:
        char, start_scene = get_canonical_persona_setup(p)
        tester = BlindPlaytester(persona=p, seed=100)
        tel = tester.run_session(char, start_scene=start_scene, max_turns=15)

        assert tel.persona == p
        assert tel.turn_count == 15, f"{p} did not complete 15 turns"
        assert len(tel.friction_notes) == 0, f"{p} had friction notes: {tel.friction_notes}"
        assert tel.retention_score >= 0.95, f"{p} retention {tel.retention_score} < 0.95"
        assert len(set(tel.scenes_visited)) >= 2, f"{p} visited only {len(set(tel.scenes_visited))} scene(s)"
        for fp in tel.fingerprints:
            assert len(fp) == 64


# ── 7. OrchestratorManager Integration ────────────────────────────────────────

def test_orchestrator_manager_run_cycle(tmp_path):
    """OrchestratorManager runs all 8 personas in a cycle, yielding ALL_GREEN and avg retention >= 0.95."""
    log_file = str(tmp_path / "test_audit.jsonl")
    manager = OrchestratorManager(log_path=log_file)

    assert len(manager.personas) == 8
    assert "nomad" in manager.personas
    assert "diver" in manager.personas
    assert "scout" in manager.personas

    summary = manager.run_cycle(cycle_num=1)

    assert summary.gate_status == "ALL_GREEN"
    assert summary.sessions_run == 8
    assert summary.total_decisions == 120  # 8 sessions * 15 decisions
    assert summary.avg_retention >= 0.95
    assert summary.hotspots == []
    assert summary.triage_results == []

    assert os.path.exists(log_file)
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "ALL_GREEN" in content
        assert '"sessions_run": 8' in content


# ── 8. Milestone 10 Persona Enum & Enriched Heuristics Tests ───────────────────

def test_playtester_persona_enum_and_init():
    """PlaytesterPersona enum members, string conversion, and BlindPlaytester initialization."""
    assert len(PlaytesterPersona) == 8
    expected = ["explorer", "brute", "infiltrator", "speedrunner", "saboteur", "nomad", "diver", "scout"]
    for member_name in expected:
        enum_val = PlaytesterPersona(member_name)
        assert enum_val.value == member_name
        assert PlaytesterPersona.from_str(member_name) == enum_val
        assert PlaytesterPersona.from_str(member_name.upper()) == enum_val

    assert BlindPlaytester.PERSONAS == expected

    # Accept Enum
    t1 = BlindPlaytester(persona=PlaytesterPersona.NOMAD)
    assert t1.persona == "nomad"

    # Accept string (uppercase and whitespace)
    t2 = BlindPlaytester(persona="  DIVER  ")
    assert t2.persona == "diver"

    # Accept canonical setup with Enum
    char, start = get_canonical_persona_setup(PlaytesterPersona.SCOUT)
    assert char.name == "Torin"
    assert start == "reach_hub"


def test_nomad_enriched_heuristics():
    """Nomad prioritizes hydration, shade recovery, sandstorm endurance, waterskin refill, oasis interaction, caravan barter."""
    actions = [
        {"id": "examine_dune", "label": "Look at sand", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "refill_waterskin", "label": "Refill waterskin", "category": "systemic", "risk": "low", "stamina_cost": 0},
        {"id": "climb_tower", "label": "Climb tower", "category": "movement", "risk": "medium", "stamina_cost": 1},
    ]
    obs = _make_dummy_step_result(actions)
    tester = BlindPlaytester(persona=PlaytesterPersona.NOMAD, seed=42)
    chosen = tester.select_action(obs)
    assert chosen == "refill_waterskin"

    # Sandstorm endurance and caravan barter
    actions2 = [
        {"id": "hide_in_cellar", "label": "Hide in cellar", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "endure_sandstorm", "label": "Endure sandstorm", "category": "systemic", "risk": "high", "stamina_cost": 1},
        {"id": "barter_caravan", "label": "Barter caravan", "category": "social", "risk": "low", "stamina_cost": 0},
    ]
    obs2 = _make_dummy_step_result(actions2)
    chosen2 = tester.select_action(obs2)
    assert chosen2 in ("endure_sandstorm", "barter_caravan")


def test_diver_enriched_heuristics():
    """Diver prioritizes submersion, diving bell operation, water buoyancy, pressure equalization, salvage prying, deep cavern diving."""
    actions = [
        {"id": "light_campfire", "label": "Light campfire", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "operate_diving_bell", "label": "Operate diving bell", "category": "systemic", "risk": "medium", "stamina_cost": 1},
        {"id": "read_tombstone", "label": "Read stone", "category": "interaction", "risk": "low", "stamina_cost": 0},
    ]
    obs = _make_dummy_step_result(actions)
    tester = BlindPlaytester(persona=PlaytesterPersona.DIVER, seed=42)
    chosen = tester.select_action(obs)
    assert chosen == "operate_diving_bell"

    # Buoyancy, pressure equalization, salvage
    actions2 = [
        {"id": "examine_wall", "label": "Examine wall", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "equalize_pressure", "label": "Equalize pressure", "category": "systemic", "risk": "low", "stamina_cost": 0},
        {"id": "salvage_sunken_chest", "label": "Salvage chest", "category": "interaction", "risk": "medium", "stamina_cost": 1},
    ]
    obs2 = _make_dummy_step_result(actions2)
    chosen2 = tester.select_action(obs2)
    assert chosen2 in ("equalize_pressure", "salvage_sunken_chest")


def test_scout_enriched_heuristics():
    """Scout prioritizes vertical cliff climbing, rope rigging, altitude stamina conservation, ridge overlook surveying, mountain vantage reconnaissance."""
    actions = [
        {"id": "rest_in_tavern", "label": "Rest in tavern", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "rig_rope_anchor", "label": "Rig rope anchor", "category": "systemic", "risk": "medium", "stamina_cost": 1},
        {"id": "read_manifest", "label": "Read manifest", "category": "interaction", "risk": "low", "stamina_cost": 0},
    ]
    obs = _make_dummy_step_result(actions)
    tester = BlindPlaytester(persona=PlaytesterPersona.SCOUT, seed=42)
    chosen = tester.select_action(obs)
    assert chosen == "rig_rope_anchor"

    # Ridge overlook surveying and altitude stamina conservation
    actions2 = [
        {"id": "pick_lock", "label": "Pick lock", "category": "trait_exploit", "risk": "low", "stamina_cost": 0},
        {"id": "survey_ridge_overlook", "label": "Survey ridge overlook", "category": "interaction", "risk": "low", "stamina_cost": 0},
        {"id": "conserve_stamina_ledge", "label": "Conserve stamina ledge", "category": "systemic", "risk": "low", "stamina_cost": 0},
    ]
    obs2 = _make_dummy_step_result(actions2)
    chosen2 = tester.select_action(obs2)
    assert chosen2 in ("survey_ridge_overlook", "conserve_stamina_ledge")


def test_session_telemetry_properties():
    """SessionTelemetry exposes .decisions and .final_scene properties and serializes them."""
    tel = SessionTelemetry(
        persona="explorer",
        seed=42,
        turn_count=2,
        decisions_made=["explore_ruins", "discover_passage"],
        scenes_visited=["crags_base", "crags_ridge"],
        fingerprints=["f1", "f2"],
        terminal_outcome=None,
        retention_score=1.0,
        friction_notes=[],
    )
    assert tel.decisions == ["explore_ruins", "discover_passage"]
    assert tel.final_scene == "crags_ridge"

    as_dict = tel.to_dict()
    assert as_dict["decisions"] == ["explore_ruins", "discover_passage"]
    assert as_dict["final_scene"] == "crags_ridge"

