"""Tier 1 & Tier 2: Macro-World Graph & 5 Regional Mechanics (Feature 5 / R5) Test Suite.

Satisfies TEST_INFRA.md:
- Tier 1 Coverage (>= 5 tests)
- Tier 2 Boundary & Corner (>= 5 tests)
"""
from adventure_forge.content.loader import build_world_registry, validate_world_links
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.schema import SceneNode, RegionManifest
from adventure_forge.core.actions import Action


def _make_engine():
    return AdventureEngine(build_world_registry())


# ── Tier 1: Unit Coverage (>= 5 tests) ───────────────────────────────────────

def test_mechanic_iron_crags_verticality():
    """Iron Crags implements verticality, rope mechanics, and climbing hazards."""
    engine = _make_engine()
    char = CharacterSheet(name="Climber", ancestry="Plainsman", background="drifter",
                          traits=["climber"], inventory=["climbing_rope"])
    state = GameState(
        build_id=engine.build_id, session_id="s", character=char,
        current_region="iron_crags", current_scene="crags_base",
        world_flags={}, history=[], event_log=[], turn_count=0, rng=DeterministicRNG(1)
    )

    legal = [a.id for a in engine.get_legal_actions(state)]
    assert "climb_cliff_face" in legal

    state2, res = engine.step(state, "climb_cliff_face")
    assert res.success is True
    assert state2.current_scene == "crags_ridge"


def test_mechanic_warrens_social_stealth():
    """Lower Warrens implements social stealth, smuggler signs, and disguise kits."""
    engine = _make_engine()
    char = CharacterSheet(name="Rogue", ancestry="Deep-Dweller", background="cutpurse",
                          traits=["light_fingers", "night_eyed"])
    state = GameState(
        build_id=engine.build_id, session_id="s", character=char,
        current_region="lower_warrens", current_scene="warrens_gate",
        world_flags={}, history=[], event_log=[], turn_count=0, rng=DeterministicRNG(1)
    )

    legal = [a.id for a in engine.get_legal_actions(state)]
    assert "flash_thief_signet" in legal

    state2, res = engine.step(state, "flash_thief_signet")
    assert res.success is True
    assert state2.current_scene == "warrens_black_market"
    assert state2.character.get_reputation("smugglers") > 0


def test_mechanic_scorchwaste_heat_survival():
    """The Scorchwaste implements ambient heat, waterskin hydration, and shade survival."""
    engine = _make_engine()
    char = CharacterSheet(name="Nomad", ancestry="Dune Walker", background="nomad",
                          inventory=["water_skin"], traits=["heat_hardened"])
    state = GameState(
        build_id=engine.build_id, session_id="s", character=char,
        current_region="scorchwaste_local", current_scene="scorch_dunes",
        world_flags={}, history=[], event_log=[], turn_count=0, rng=DeterministicRNG(1)
    )

    legal = [a.id for a in engine.get_legal_actions(state)]
    assert len(legal) >= 2
    assert "drink_canteen" in legal
    assert "march_to_oasis" in legal


def test_mechanic_high_court_legal_intrigue():
    """High Crown of Veras implements legal evidence, testimonies, and aristocratic decorum."""
    engine = _make_engine()
    char = CharacterSheet(name="Noble", ancestry="Highborn", background="noble_exile",
                          skills={"rhetoric": 3}, inventory=["legal_dossier"])
    state = GameState(
        build_id=engine.build_id, session_id="s", character=char,
        current_region="high_court_local", current_scene="court_antechamber",
        world_flags={}, history=[], event_log=[], turn_count=0, rng=DeterministicRNG(1)
    )

    legal = [a.id for a in engine.get_legal_actions(state)]
    assert len(legal) >= 2
    assert "present_writ" in legal
    assert "plead_urgent_case" in legal


def test_mechanic_sunken_hollows_buoyancy():
    """The Sunken Abyss implements water buoyancy, depth pressure, and diving routes."""
    engine = _make_engine()
    char = CharacterSheet(name="Diver", ancestry="Deep-Dweller", background="drifter",
                          attributes={"endurance": 14}, traits=["deep_diver"])
    state = GameState(
        build_id=engine.build_id, session_id="s", character=char,
        current_region="sunken_hollows_local", current_scene="hollows_grotto",
        world_flags={}, history=[], event_log=[], turn_count=0, rng=DeterministicRNG(1)
    )

    legal = [a.id for a in engine.get_legal_actions(state)]
    assert len(legal) >= 2
    assert "dive_into_pool" in legal


def test_macro_world_graph_scale_520_nodes():
    """World registry contains exactly 520 interconnected nodes across all regions."""
    registry = build_world_registry()
    total_scenes = sum(len(r.scenes) for r in registry.values())
    assert total_scenes == 520, f"Expected exactly 520 scenes, got {total_scenes}"


# ── Tier 2: Boundary & Corner Tests (>= 5 tests) ─────────────────────────────

def test_cross_province_highway_transit():
    """Continuous unbroken transit between Reach Hub -> Bazaar -> Lowlands Hub."""
    engine = _make_engine()
    char = CharacterSheet(name="Wayfarer", ancestry="Plainsman", background="drifter")
    state = GameState(
        build_id=engine.build_id, session_id="transit-test", character=char,
        current_region="province_reach", current_scene="reach_hub",
        world_flags={}, history=[], event_log=[], turn_count=0, rng=DeterministicRNG(42)
    )

    # 1. Reach Hub -> Bazaar
    state, res = engine.step(state, "reach_to_bazaar")
    assert res.success is True
    assert state.current_scene == "bazaar_center"

    # 2. Bazaar -> Lowlands Hub
    state, res = engine.step(state, "travel_to_lowlands_hub")
    assert res.success is True
    assert state.current_scene == "lowlands_hub"

    # 3. Lowlands Hub -> Bazaar
    state, res = engine.step(state, "lowlands_to_bazaar")
    assert res.success is True
    assert state.current_scene == "bazaar_center"

    # 4. Bazaar -> Reach Hub
    state, res = engine.step(state, "travel_to_reach_hub")
    assert res.success is True
    assert state.current_scene == "reach_hub"


def test_deep_secret_shrine_reachability():
    """Node 520 (reach_secret_shrine) is reachable via night_eyed trait exploit from sanctum."""
    engine = _make_engine()
    char = CharacterSheet(name="Seeker", ancestry="Deep-Dweller", background="noble_exile",
                          traits=["night_eyed"], skills={"cunning": 2})
    state = GameState(
        build_id=engine.build_id, session_id="shrine-test", character=char,
        current_region="province_reach", current_scene="reach_frost_cavern_sanctum",
        world_flags={}, history=[], event_log=[], turn_count=0, rng=DeterministicRNG(42)
    )

    legal = [a.id for a in engine.get_legal_actions(state)]
    assert "reach_frost_cavern_to_secret_shrine" in legal

    state_shrine, res = engine.step(state, "reach_frost_cavern_to_secret_shrine")
    assert res.success is True
    assert state_shrine.current_scene == "reach_secret_shrine"
    assert "ancient ice dais" in res.description.lower() or "ice dais" in res.description.lower()

    # Verify return step
    state_back, res_back = engine.step(state_shrine, "reach_secret_shrine_to_sanctum")
    assert res_back.success is True
    assert state_back.current_scene == "reach_frost_cavern_sanctum"


def test_graph_bidirectional_traversability():
    """Sample POI traversability: from hub, forward to 3rd node and back to hub."""
    engine = _make_engine()
    char = CharacterSheet(name="Walker", ancestry="Plainsman", background="drifter")
    state = GameState(
        build_id=engine.build_id, session_id="poi-walk", character=char,
        current_region="province_lowlands", current_scene="lowlands_hub",
        world_flags={}, history=[], event_log=[], turn_count=0, rng=DeterministicRNG(42)
    )

    # Move from hub to dock POI
    state, _ = engine.step(state, "lowlands_hub_to_oakhaven_port")
    assert state.current_scene == "lowlands_oakhaven_port_gate"

    # Walk 2 nodes forward
    state, _ = engine.step(state, "lowlands_oakhaven_port_gate_to_next")
    assert state.current_scene == "lowlands_oakhaven_port_courtyard"
    state, _ = engine.step(state, "lowlands_oakhaven_port_courtyard_to_next")
    assert state.current_scene == "lowlands_oakhaven_port_quarters"

    # Walk 2 nodes back
    state, _ = engine.step(state, "lowlands_oakhaven_port_quarters_to_prev")
    assert state.current_scene == "lowlands_oakhaven_port_courtyard"
    state, _ = engine.step(state, "lowlands_oakhaven_port_courtyard_to_prev")
    assert state.current_scene == "lowlands_oakhaven_port_gate"
    state, _ = engine.step(state, "lowlands_oakhaven_port_gate_to_prev")
    assert state.current_scene == "lowlands_hub"


def test_density_threshold_per_province():
    """Every single province has >= 50% scenes with >= 3 meaningful interactables."""
    registry = build_world_registry()
    provinces = ["province_reach", "province_lowlands", "province_scorchwaste",
                 "province_high_court", "province_sunken_hollows"]

    for prov_key in provinces:
        region = registry[prov_key]
        qualifying = 0
        total = len(region.scenes)
        for sc in region.scenes.values():
            non_movement = [a for a in sc.base_actions if a.category != "movement"]
            count = len(non_movement) + len(sc.entities)
            if count >= 3:
                qualifying += 1
        ratio = qualifying / total
        assert ratio >= 0.50, f"{prov_key} interactable ratio {ratio:.2%} < 50%"


def test_orphan_and_dangling_link_detector():
    """validate_world_links catches injected dangling target_scene or climb destinations."""
    good_registry = build_world_registry()
    ok_good, errors_good = validate_world_links(good_registry)
    assert ok_good is True
    assert len(errors_good) == 0

    bad_registry = dict(good_registry)
    broken_scene = SceneNode(
        id="broken_scene_test",
        title="Broken",
        region="iron_crags",
        description="Broken place.",
        base_actions=[
            Action(id="act_broken", label="Go void", category="movement", target_scene="non_existent_scene_xyz")
        ]
    )
    bad_registry["broken_region"] = RegionManifest(
        id="broken_region", name="Broken", mechanic_name="None", mechanic_description="None",
        scenes={"broken_scene_test": broken_scene}
    )

    ok_bad, errors_bad = validate_world_links(bad_registry)
    assert ok_bad is False
    assert any("non_existent_scene_xyz" in err for err in errors_bad)
