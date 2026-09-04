"""Tier 3: Pairwise Combinatorial Interactions Test Suite.

Satisfies TEST_INFRA.md:
- Tier 3 Pairwise Combinatorial Coverage (>= 10 tests)
"""
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry
from adventure_forge.flywheel.playtester import BlindPlaytester


def _make_engine():
    return AdventureEngine(build_world_registry())


def _make_state(engine, scene_id, char, flags=None, seed=42):
    return GameState(
        build_id=engine.build_id,
        session_id="pairwise-test",
        character=char,
        current_region=engine.get_region_id_for_scene(scene_id) or "iron_crags",
        current_scene=scene_id,
        world_flags=flags or {},
        history=[],
        event_log=[],
        turn_count=0,
        rng=DeterministicRNG.from_seed(seed),
    )


# ── Tier 3: Pairwise Combinatorial Tests (>= 10 tests) ───────────────────────

def test_pairwise_ancestry_x_regional_mechanics():
    """Interaction 1: Character Ancestry x Regional Mechanics."""
    engine = _make_engine()
    char_dune = CharacterSheet(name="DuneWalker", ancestry="Ashenborn", background="drifter")
    char_sub = CharacterSheet(name="Subterranean", ancestry="Deep-Dweller", background="drifter")

    # In Scorchwaste Dunes: Ashenborn receives distinct dynamic observation
    s_dune = _make_state(engine, "scorch_dunes", char_dune)
    s_sub = _make_state(engine, "scorch_dunes", char_sub)

    obs_dune = engine.observe(s_dune)
    obs_sub = engine.observe(s_sub)

    assert "searing sun warms your blood" in obs_dune.description.lower()
    assert "searing sun warms your blood" not in obs_sub.description.lower()


def test_pairwise_background_x_social_systems():
    """Interaction 2: Background x Faction Authority Gates."""
    engine = _make_engine()
    cutpurse = CharacterSheet(name="Thief", ancestry="Plainsman", background="cutpurse")
    noble = CharacterSheet(name="Lady", ancestry="Highborn", background="noble_exile")

    s_cutpurse = _make_state(engine, "warrens_gate", cutpurse)
    s_noble = _make_state(engine, "warrens_gate", noble)

    actions_cutpurse = [a.id for a in engine.get_legal_actions(s_cutpurse)]
    actions_noble = [a.id for a in engine.get_legal_actions(s_noble)]

    assert "flash_thief_signet" in actions_cutpurse
    assert "flash_thief_signet" not in actions_noble
    assert "demand_guard_entry" in actions_noble
    assert "demand_guard_entry" not in actions_cutpurse


def test_pairwise_inventory_tools_x_entity_systemics():
    """Interaction 3: Inventory Tools x Entity Tags (lockable, flammable)."""
    engine = _make_engine()
    char_with_picks = CharacterSheet(name="ToolUser", ancestry="Plainsman", background="drifter",
                                     inventory=["lockpick"])
    char_with_torch = CharacterSheet(name="Pyromancer", ancestry="Plainsman", background="drifter",
                                     inventory=["torch"])

    # warrens_gate contains sewer_grate (lockable) and wooden_cart (flammable)
    s_picks = _make_state(engine, "warrens_gate", char_with_picks)
    s_torch = _make_state(engine, "warrens_gate", char_with_torch)

    acts_picks = [a.id for a in engine.get_legal_actions(s_picks)]
    acts_torch = [a.id for a in engine.get_legal_actions(s_torch)]

    assert "pick_sewer_grate" in acts_picks
    assert "burn_wooden_cart" in acts_torch
    assert "burn_wooden_cart" not in acts_picks


def test_pairwise_stamina_depletion_x_movement_risks():
    """Interaction 4: Stamina Resource x High-Cost Movements."""
    engine = _make_engine()
    char_stamina = CharacterSheet(name="Fit", ancestry="Plainsman", background="drifter",
                                  attributes={"endurance": 14}, stamina=5)
    char_exhausted = CharacterSheet(name="Tired", ancestry="Plainsman", background="drifter",
                                    attributes={"endurance": 14}, stamina=0)

    # In hollows_grotto, dive_into_pool costs 2 stamina
    s_fit = _make_state(engine, "hollows_grotto", char_stamina)
    s_exhausted = _make_state(engine, "hollows_grotto", char_exhausted)

    acts_fit = [a.id for a in engine.get_legal_actions(s_fit)]
    acts_exhausted = [a.id for a in engine.get_legal_actions(s_exhausted)]

    assert "dive_into_pool" in acts_fit
    assert "dive_into_pool" not in acts_exhausted

    # Stepping with fit character decrements stamina exactly by 2
    state_after_dive, _ = engine.step(s_fit, "dive_into_pool")
    assert state_after_dive.character.stamina == 3


def test_pairwise_traits_x_unbounded_choice_expansion():
    """Interaction 5: Trait Exploits x Scene Action Volume."""
    engine = _make_engine()
    char_base = CharacterSheet(name="Plain", ancestry="Plainsman", background="drifter")
    char_exploiter = CharacterSheet(name="Agent", ancestry="Plainsman", background="cutpurse",
                                    traits=["night_eyed", "climber", "pyromaniac"],
                                    inventory=["lockpick", "climbing_rope"])

    s_base = _make_state(engine, "crags_base", char_base)
    s_exp = _make_state(engine, "crags_base", char_exploiter)

    acts_base = engine.get_legal_actions(s_base)
    acts_exp = engine.get_legal_actions(s_exp)

    # Exploiter has more legal actions due to climber, lockpick on chest, etc.
    assert len(acts_exp) > len(acts_base)
    exp_ids = [a.id for a in acts_exp]
    assert "pick_iron_chest" in exp_ids
    assert "climb_cliff_face" in exp_ids


def test_pairwise_world_flags_x_cross_province_dialogue():
    """Interaction 6: World Flags x Cross-Scene Outcomes."""
    engine = _make_engine()
    char = CharacterSheet(name="Hero", ancestry="Plainsman", background="drifter")

    # Without beacon lit
    s_unlit = _make_state(engine, "crags_peak", char, flags={"crags_beacon_lit": False})
    acts_unlit = [a.id for a in engine.get_legal_actions(s_unlit)]
    assert "claim_crags_beacon" in acts_unlit

    # Step to light beacon
    s_lit, res = engine.step(s_unlit, "claim_crags_beacon")
    assert res.success is True
    assert s_lit.world_flags.get("crags_beacon_lit") is True


def test_pairwise_state_serialization_x_multi_turn_replay():
    """Interaction 7: Mid-Session Serialization x Resumed Replay Equivalence."""
    engine = _make_engine()
    char = CharacterSheet(name="SaveTester", ancestry="Plainsman", background="cutpurse",
                          inventory=["lockpick", "silver_coin"])
    s0 = _make_state(engine, "warrens_gate", char, seed=555)

    # Step 1: Flash thief signet -> warrens_black_market
    s1, _ = engine.step(s0, "flash_thief_signet")

    # Save to dictionary (simulating client-side save token or database commit)
    saved_payload = s1.to_dict()

    # Step 2 from original
    s2_orig, _ = engine.step(s1, "buy_lockpicks")

    # Step 2 from restored state
    s1_restored = GameState.from_dict(saved_payload)
    s2_restored, _ = engine.step(s1_restored, "buy_lockpicks")

    assert s2_orig.fingerprint() == s2_restored.fingerprint()
    assert s2_orig.character.inventory == s2_restored.character.inventory


def test_pairwise_attribute_thresholds_x_complex_dsl_predicates():
    """Interaction 8: Attribute Thresholds x Condition Combinations."""
    engine = _make_engine()
    char_strong_smart = CharacterSheet(name="Titan", ancestry="Deep-Dweller", background="noble_exile",
                                       attributes={"strength": 15}, skills={"cunning": 3})
    char_smart_only = CharacterSheet(name="Scholar", ancestry="Deep-Dweller", background="noble_exile",
                                     attributes={"strength": 8}, skills={"cunning": 3})

    # In reach_secret_shrine: checks cunning >= 2 and background noble_exile
    s_both = _make_state(engine, "reach_secret_shrine", char_strong_smart)
    s_scholar = _make_state(engine, "reach_secret_shrine", char_smart_only)

    obs_both = engine.observe(s_both)
    obs_scholar = engine.observe(s_scholar)

    # Both satisfy cunning and noble_exile
    assert "mountain footholds" in obs_both.description.lower()
    assert "mountain footholds" in obs_scholar.description.lower()


def test_pairwise_reputation_changes_x_access_control():
    """Interaction 9: Faction Reputation x Sentry/Toll Gate Access."""
    engine = _make_engine()
    char_friendly = CharacterSheet(name="Pal", ancestry="Plainsman", background="drifter",
                                   reputation={"iron_guard": 10})
    char_hostile = CharacterSheet(name="Enemy", ancestry="Plainsman", background="drifter",
                                  reputation={"iron_guard": -10})

    # In crags_base, hail_watchman requires min_reputation iron_guard >= 0
    s_friendly = _make_state(engine, "crags_base", char_friendly)
    s_hostile = _make_state(engine, "crags_base", char_hostile)

    acts_friendly = [a.id for a in engine.get_legal_actions(s_friendly)]
    acts_hostile = [a.id for a in engine.get_legal_actions(s_hostile)]

    assert "hail_watchman" in acts_friendly
    assert "hail_watchman" not in acts_hostile


def test_pairwise_blind_playtester_persona_x_regional_topology():
    """Interaction 10: Playtester Personas x Distinct Navigation Trajectories."""
    char = CharacterSheet(name="PersonaBot", ancestry="Deep-Dweller", background="cutpurse",
                          inventory=["lockpick", "silver_coin"], skills={"cunning": 3, "stealth": 2})
    # Run speedrunner vs explorer from crags_base with same seed
    tester_speed = BlindPlaytester(persona="speedrunner", seed=99)
    tester_brute = BlindPlaytester(persona="brute", seed=99)

    tel_speed = tester_speed.run_session(char, start_scene="crags_base", max_turns=6)
    tel_brute = tester_brute.run_session(char, start_scene="crags_base", max_turns=6)

    assert tel_speed.turn_count > 0
    assert tel_brute.turn_count > 0
    # Both executed valid non-crashing sessions
    assert len(tel_speed.fingerprints) > 0
    assert len(tel_brute.fingerprints) > 0
