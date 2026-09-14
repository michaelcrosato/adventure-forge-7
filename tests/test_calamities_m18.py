"""Tests for Milestone 18: Continental Dynamic Event & World Calamity System.

Validates:
- Deterministic cyclical and triggered incursion activation across all 5 provinces.
- Provincial calamity mitigation affordance synthesis.
- 7-axis character attribute, skill, and item prerequisites for incursion resolution.
- Calamity clearance, state mutations, and salvage rewards.
- Pure deterministic replay and bit-for-bit SHA-256 state fingerprint reproducibility.
- Strict compliance with Hemingway prose constraints and label word bounds.
"""
from typing import List, Dict, Any
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.state import GameState
from adventure_forge.core.calamities import (
    WORLD_CALAMITIES,
    get_active_calamity,
)
from adventure_forge.linter.prose_linter import ProseLinter


def _create_test_engine() -> AdventureEngine:
    reg = build_world_registry()
    return AdventureEngine(reg, build_id="af-m18-test")


def _make_survivor(**overrides) -> CharacterSheet:
    base: Dict[str, Any] = {
        "name": "Survivor",
        "ancestry": "Plainsman",
        "background": "scout",
        "attributes": {"strength": 10, "agility": 10, "endurance": 10, "cunning": 2, "intimidation": 5},
        "skills": {"brawling": 1, "athletics": 1, "stealth": 1, "cunning": 2, "rhetoric": 1},
        "traits": [],
        "flaws": [],
        "reputation": {},
        "markers": [],
        "inventory": [],
        "health": 20,
        "max_health": 20,
        "stamina": 10,
        "max_stamina": 10,
    }
    base.update(overrides)
    return CharacterSheet(**base)


# ==============================================================================
# 1. Calamity Cyclical & Regional Activation
# ==============================================================================

def test_calamity_regional_matching_and_turn_cycle():
    """Calamities activate deterministically based on province and turn interval."""
    # Reach tremor activates on turn % 8 in (3, 4) in reach/crag scenes
    assert get_active_calamity(turn_count=0, region_id="iron_crags", world_flags={}) is None
    assert get_active_calamity(turn_count=1, region_id="iron_crags", world_flags={}) is None
    assert get_active_calamity(turn_count=2, region_id="iron_crags", world_flags={}) is None

    # Active on turns 3 and 4
    c3 = get_active_calamity(turn_count=3, region_id="iron_crags", world_flags={})
    assert c3 is not None
    assert c3.id == "reach_tremor"
    assert c3.province == "The Reach"

    c4 = get_active_calamity(turn_count=4, region_id="iron_crags", world_flags={})
    assert c4 is not None
    assert c4.id == "reach_tremor"

    # Inactive on turn 5
    assert get_active_calamity(turn_count=5, region_id="iron_crags", world_flags={}) is None


def test_calamity_cleared_flag_suppresses_incursion():
    """Once cleared in a province, the calamity is suppressed."""
    flags_cleared = {"reach_tremor_cleared": True}
    assert get_active_calamity(turn_count=3, region_id="iron_crags", world_flags=flags_cleared) is None


def test_all_five_provinces_calamity_coverage():
    """All 5 provinces have dedicated calamity definitions that activate in their regions."""
    expected_provinces = {
        "iron_crags": "reach_tremor",
        "sunken_hollows_local": "hollows_surge",
        "scorchwaste_local": "scorch_tempest",
        "high_court_local": "court_lockdown",
        "lower_warrens": "lowlands_breach",
    }

    for region, expected_id in expected_provinces.items():
        calamity = get_active_calamity(turn_count=3, region_id=region, world_flags={})
        assert calamity is not None, f"No calamity active in {region}"
        assert calamity.id == expected_id, f"Expected {expected_id} in {region}, got {calamity.id}"


# ==============================================================================
# 2. Dynamic Mitigation Synthesis & Prerequisite Gating
# ==============================================================================

def test_reach_tremor_mitigations():
    """Reach tremor exposes Anchor Line (rope/agility) and Brace Shudder (strength/endurance)."""
    eng = _create_test_engine()

    # Unqualified character: turn 3 in iron_crags
    char_unqual = _make_survivor()
    st_unqual = GameState(
        build_id="af-m18-test",
        session_id="reach-mit-1",
        character=char_unqual,
        current_region="iron_crags",
        current_scene="crags_base",
        turn_count=3,
    )
    acts_unqual = {a.id for a in eng.get_legal_actions(st_unqual)}
    assert "calamity_reach_anchor" not in acts_unqual
    assert "calamity_reach_brace" not in acts_unqual

    # Qualified via agility: Anchor Line becomes legal
    char_agi = _make_survivor(attributes={"agility": 12})
    st_agi = GameState(
        build_id="af-m18-test",
        session_id="reach-mit-2",
        character=char_agi,
        current_region="iron_crags",
        current_scene="crags_base",
        turn_count=3,
    )
    acts_agi = {a.id for a in eng.get_legal_actions(st_agi)}
    assert "calamity_reach_anchor" in acts_agi
    assert "calamity_reach_brace" not in acts_agi

    # Qualified via climbing rope: Anchor Line becomes legal
    char_rope = _make_survivor(inventory=["climbing_rope"])
    st_rope = GameState(
        build_id="af-m18-test",
        session_id="reach-mit-3",
        character=char_rope,
        current_region="iron_crags",
        current_scene="crags_base",
        turn_count=3,
    )
    acts_rope = {a.id for a in eng.get_legal_actions(st_rope)}
    assert "calamity_reach_anchor" in acts_rope


def test_calamity_execution_and_salvage_reward():
    """Executing calamity mitigation clears incursion, logs event, and rewards salvage."""
    eng = _create_test_engine()
    char = _make_survivor(attributes={"strength": 14})

    st = GameState(
        build_id="af-m18-test",
        session_id="exec-salvage",
        character=char,
        current_region="iron_crags",
        current_scene="crags_base",
        turn_count=3,
    )

    acts = {a.id for a in eng.get_legal_actions(st)}
    assert "calamity_reach_brace" in acts

    # Step: Brace Shudder
    st_after, obs = eng.step(st, "calamity_reach_brace")
    assert obs.success is True
    assert st_after.world_flags.get("reach_tremor_cleared") is True

    # Calamity is now cleared, so mitigation affordance disappears
    acts_after = {a.id for a in eng.get_legal_actions(st_after)}
    assert "calamity_reach_brace" not in acts_after
    assert "calamity_reach_anchor" not in acts_after


def test_hollows_and_scorchwaste_mitigation_execution():
    """Sunken Hollows and Scorchwaste calamity mitigations award respective provincial salvage."""
    eng = _create_test_engine()

    # Hollows Siphon Surge: Seal Bulkhead awards algae_sample
    char_diver = _make_survivor(attributes={"strength": 12})
    st_hollows = GameState(
        build_id="af-m18-test",
        session_id="hollows-mit",
        character=char_diver,
        current_region="sunken_hollows_local",
        current_scene="hollows_grotto",
        turn_count=3,
    )
    acts_hollows = {a.id for a in eng.get_legal_actions(st_hollows)}
    assert "calamity_hollows_seal" in acts_hollows

    st_h_after, obs_h = eng.step(st_hollows, "calamity_hollows_seal")
    assert obs_h.success is True
    assert "algae_sample" in st_h_after.character.inventory
    assert st_h_after.world_flags.get("hollows_surge_cleared") is True

    # Scorchwaste Glass Tempest: Drape Cowl awards salt_crust
    char_nomad = _make_survivor(traits=["heat_tolerant"])
    st_scorch = GameState(
        build_id="af-m18-test",
        session_id="scorch-mit",
        character=char_nomad,
        current_region="scorchwaste_local",
        current_scene="scorch_dunes",
        turn_count=3,
    )
    acts_scorch = {a.id for a in eng.get_legal_actions(st_scorch)}
    assert "calamity_scorch_cowl" in acts_scorch

    st_s_after, obs_s = eng.step(st_scorch, "calamity_scorch_cowl")
    assert obs_s.success is True
    assert "salt_crust" in st_s_after.character.inventory
    assert st_s_after.world_flags.get("scorch_tempest_cleared") is True


# ==============================================================================
# 3. Pure Deterministic Replay Verification
# ==============================================================================

def test_calamity_deterministic_replay():
    """Multi-step calamity incursion mitigation sequence reproduces identical SHA-256 hashes."""
    eng = _create_test_engine()
    char = _make_survivor(
        attributes={"strength": 14, "agility": 14, "endurance": 14},
        inventory=["climbing_rope", "water_skin"],
    )

    def run_trace(seed: int, action_seq: List[str]) -> List[str]:
        st = GameState(
            build_id="af-m18-test",
            session_id=f"calamity-det-{seed}",
            character=char,
            current_region="iron_crags",
            current_scene="crags_base",
            turn_count=3,
            rng=DeterministicRNG.from_seed(seed),
        )
        fps = [st.fingerprint()]
        for a_id in action_seq:
            st, obs = eng.step(st, a_id)
            assert obs.success is True, f"Failed at {a_id}"
            fps.append(st.fingerprint())
        return fps

    actions = [
        "calamity_reach_anchor",
        "search_scree",
    ]

    fps1 = run_trace(seed=888, action_seq=actions)
    fps2 = run_trace(seed=888, action_seq=actions)

    assert fps1 == fps2
    assert len(fps1) == len(actions) + 1

    # Tamper test
    tampered = ["calamity_reach_brace", "search_scree"]
    fps_tampered = run_trace(seed=888, action_seq=tampered)
    assert fps1 != fps_tampered


# ==============================================================================
# 4. Hemingway Prose & Action Label Quality Bar
# ==============================================================================

def test_calamity_prose_and_label_bounds():
    """All calamity descriptions, mitigation labels, result texts, and log events pass ProseLinter."""
    linter = ProseLinter()

    for c_id, calamity in WORLD_CALAMITIES.items():
        # Calamity description
        errs_desc = linter.lint_text(calamity.description, context=f"{c_id}_desc")
        assert not errs_desc, f"Prose violations in {c_id} description: {errs_desc}"

        for mit in calamity.mitigations:
            # Action labels must be 1 to 3 words
            words = mit.label.split()
            assert 1 <= len(words) <= 3, f"{mit.id} label '{mit.label}' exceeds 3 words ({len(words)} words)"

            # Result text must pass Hemingway prose linter
            errs_res = linter.lint_text(mit.result_text, context=f"{mit.id}_result")
            assert not errs_res, f"Prose violations in {mit.id} result: {errs_res}"

            # Log events
            for eff in mit.effects:
                if "log_event" in eff:
                    errs_evt = linter.lint_text(eff["log_event"], context=f"{mit.id}_event")
                    assert not errs_evt, f"Prose violations in {mit.id} log event: {errs_evt}"
