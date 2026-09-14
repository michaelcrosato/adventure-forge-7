"""Tests for Milestone 16: Tactical Combat Stances & Systemic Exploits.

Validates:
- 7-axis character sheet prerequisite gating across archetypes.
- Dynamic stance affordance synthesis and category tagging.
- Stance transitions (shift, exploit, drop/neutralize).
- Exploit execution, state mutations, and resource costs.
- Pure deterministic replay and SHA-256 fingerprint fidelity.
- Strict compliance with Hemingway prose constraints and label bounds.
"""
from typing import List, Dict, Any
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.core.state import GameState
from adventure_forge.core.stances import (
    TACTICAL_STANCES,
    ALL_STANCE_MARKERS,
    get_tactical_stances,
)
from adventure_forge.linter.prose_linter import ProseLinter


def _create_test_engine() -> AdventureEngine:
    reg = build_world_registry()
    return AdventureEngine(reg, build_id="af-m16-test")


def _make_char(**overrides) -> CharacterSheet:
    base: Dict[str, Any] = {
        "name": "Tactician",
        "ancestry": "Plainsman",
        "background": "drifter",
        "attributes": {"strength": 10, "agility": 10, "endurance": 10, "cunning": 1, "intimidation": 5},
        "skills": {"brawling": 1, "athletics": 1, "stealth": 1, "cunning": 1, "rhetoric": 1},
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
# 1. 7-Axis Prerequisite Gating Tests
# ==============================================================================

def test_aggressive_stance_prerequisites():
    """Aggressive stance gates by strength >= 12, brawling >= 3, iron_gutted, or reckless."""
    stance = TACTICAL_STANCES["aggressive"]

    # Baseline unqualified
    char_base = _make_char()
    assert not stance.is_available(char_base, {})

    # Strength qualifier
    char_str = _make_char(attributes={"strength": 12})
    assert stance.is_available(char_str, {})

    # Brawling skill qualifier
    char_brawl = _make_char(skills={"brawling": 3})
    assert stance.is_available(char_brawl, {})

    # Trait qualifier
    char_trait = _make_char(traits=["iron_gutted"])
    assert stance.is_available(char_trait, {})

    # Flaw qualifier
    char_flaw = _make_char(flaws=["reckless"])
    assert stance.is_available(char_flaw, {})


def test_defensive_stance_prerequisites():
    """Guarded stance gates by endurance >= 12, athletics >= 3, oath_bound, or iron_gutted."""
    stance = TACTICAL_STANCES["defensive"]

    char_base = _make_char()
    assert not stance.is_available(char_base, {})

    char_end = _make_char(attributes={"endurance": 12})
    assert stance.is_available(char_end, {})

    char_ath = _make_char(skills={"athletics": 3})
    assert stance.is_available(char_ath, {})

    char_oath = _make_char(flaws=["oath_bound"])
    assert stance.is_available(char_oath, {})


def test_elusive_stance_prerequisites():
    """Elusive stance gates by agility >= 12, stealth >= 3, nimble, night_eyed, or streetwise."""
    stance = TACTICAL_STANCES["elusive"]

    char_base = _make_char()
    assert not stance.is_available(char_base, {})

    char_agi = _make_char(attributes={"agility": 12})
    assert stance.is_available(char_agi, {})

    char_stl = _make_char(skills={"stealth": 3})
    assert stance.is_available(char_stl, {})

    char_nimble = _make_char(traits=["nimble"])
    assert stance.is_available(char_nimble, {})


def test_focused_stance_prerequisites():
    """Focused stance gates by cunning >= 3, rhetoric >= 3, keen_eyed, or skeptical."""
    stance = TACTICAL_STANCES["focused"]

    char_base = _make_char()
    assert not stance.is_available(char_base, {})

    char_cun = _make_char(skills={"cunning": 3})
    assert stance.is_available(char_cun, {})

    char_rhet = _make_char(skills={"rhetoric": 3})
    assert stance.is_available(char_rhet, {})

    char_skep = _make_char(traits=["skeptical"])
    assert stance.is_available(char_skep, {})


# ==============================================================================
# 2. Canonical Character Archetype Stance Availability
# ==============================================================================

def test_canonical_archetype_stance_divergence():
    """Silas (Cutpurse) vs Vivienne (Noble) exhibit demonstrably distinct stance affordances."""
    eng = _create_test_engine()

    # Silas the Rat: High Agility, High Cunning, Nimble, Streetwise
    silas = CharacterSheet(
        name="Silas",
        ancestry="Deep-Dweller",
        background="cutpurse",
        attributes={"strength": 8, "agility": 14, "endurance": 10},
        skills={"cunning": 4, "stealth": 3},
        traits=["night_eyed", "streetwise"],
        flaws=["marked_outlaw"],
    )
    state_silas = GameState(
        build_id="af-m16-test",
        session_id="silas-stance-test",
        character=silas,
        current_region="lower_warrens",
        current_scene="warrens_gate",
    )
    acts_silas = {a.id for a in eng.get_legal_actions(state_silas)}

    # Vivienne the Noble Exile: High Intimidation, Rhetoric, Skeptical, Oath-Bound
    vivienne = CharacterSheet(
        name="Vivienne",
        ancestry="High-Kin",
        background="noble_exile",
        attributes={"strength": 10, "agility": 8, "endurance": 10, "intimidation": 15},
        skills={"rhetoric": 4, "cunning": 1},
        traits=["skeptical"],
        flaws=["oath_bound"],
    )
    state_viv = GameState(
        build_id="af-m16-test",
        session_id="viv-stance-test",
        character=vivienne,
        current_region="lower_warrens",
        current_scene="warrens_gate",
    )
    acts_viv = {a.id for a in eng.get_legal_actions(state_viv)}

    # Silas has Elusive and Focused, but NOT Aggressive or Defensive
    assert "stance_elusive" in acts_silas
    assert "stance_focused" in acts_silas
    assert "stance_aggressive" not in acts_silas
    assert "stance_defensive" not in acts_silas

    # Vivienne has Defensive and Focused, but NOT Aggressive or Elusive
    assert "stance_defensive" in acts_viv
    assert "stance_focused" in acts_viv
    assert "stance_aggressive" not in acts_viv
    assert "stance_elusive" not in acts_viv


# ==============================================================================
# 3. Dynamic Stance Transitions & Exploits
# ==============================================================================

def test_stance_shift_exploit_and_drop_lifecycle():
    """Player shifts into stance, receives exploit and drop options, and drops cleanly."""
    eng = _create_test_engine()
    char = _make_char(attributes={"strength": 14, "endurance": 14})

    state = GameState(
        build_id="af-m16-test",
        session_id="lifecycle-test",
        character=char,
        current_region="iron_crags",
        current_scene="crags_base",
    )

    # Initial state: Neutral posture. Both aggressive and defensive shifts are legal.
    acts_0 = {a.id for a in eng.get_legal_actions(state)}
    assert "stance_aggressive" in acts_0
    assert "stance_defensive" in acts_0
    assert "tactical_brutal_strike" not in acts_0
    assert "stance_neutral" not in acts_0

    # Step 1: Shift to aggressive stance
    state_1, obs_1 = eng.step(state, "stance_aggressive")
    assert obs_1.success is True
    assert state_1.character.has_marker("stance_aggressive")
    assert state_1.world_flags.get("active_stance") == "aggressive"

    # In aggressive stance:
    # - Brutal Strike exploit is synthesized
    # - Drop Stance is synthesized
    # - Take Aggressive Stance is NOT synthesized (already active)
    # - Take Guarded Stance IS synthesized (switch stance)
    acts_1 = {a.id for a in eng.get_legal_actions(state_1)}
    assert "tactical_brutal_strike" in acts_1
    assert "stance_neutral" in acts_1
    assert "stance_aggressive" not in acts_1
    assert "stance_defensive" in acts_1

    # Step 2: Execute Brutal Strike exploit
    stamina_before = state_1.character.stamina
    state_2, obs_2 = eng.step(state_1, "tactical_brutal_strike")
    assert obs_2.success is True
    assert state_2.world_flags.get("tactical_strike_executed") is True
    assert state_2.character.stamina == stamina_before - 1

    # Step 3: Switch directly from aggressive to guarded stance
    state_3, obs_3 = eng.step(state_2, "stance_defensive")
    assert obs_3.success is True
    assert state_3.character.has_marker("stance_defensive")
    assert not state_3.character.has_marker("stance_aggressive")
    assert state_3.world_flags.get("active_stance") == "defensive"

    acts_3 = {a.id for a in eng.get_legal_actions(state_3)}
    assert "tactical_brace_impact" in acts_3
    assert "tactical_brutal_strike" not in acts_3
    assert "stance_defensive" not in acts_3
    assert "stance_aggressive" in acts_3

    # Step 4: Drop stance to neutral
    state_4, obs_4 = eng.step(state_3, "stance_neutral")
    assert obs_4.success is True
    assert not state_4.character.has_marker("stance_defensive")
    assert not state_4.character.has_marker("stance_aggressive")
    assert state_4.world_flags.get("active_stance") == ""

    acts_4 = {a.id for a in eng.get_legal_actions(state_4)}
    assert "stance_neutral" not in acts_4
    assert "tactical_brace_impact" not in acts_4
    assert "stance_aggressive" in acts_4
    assert "stance_defensive" in acts_4


def test_exploit_stamina_cost_exhaustion():
    """Exploits requiring stamina are rejected if stamina is insufficient."""
    eng = _create_test_engine()
    char = _make_char(attributes={"strength": 14}, stamina=0)
    # Manually grant active stance marker
    char_in_stance = char.modify(markers=["stance_aggressive"])

    state = GameState(
        build_id="af-m16-test",
        session_id="exhaustion-test",
        character=char_in_stance,
        current_region="iron_crags",
        current_scene="crags_base",
        world_flags={"active_stance": "aggressive"},
    )

    legal_acts = eng.get_legal_actions(state)
    act_map = {a.id: a for a in legal_acts}

    # tactical_brutal_strike costs 1 stamina, so with 0 stamina it must not be legal
    assert "tactical_brutal_strike" not in act_map

    # Drop stance costs 0 stamina, so it remains legal
    assert "stance_neutral" in act_map


def test_focused_stance_spot_weakness():
    """Focused stance Spot Weakness costs 0 stamina and sets tactical_weakness_spotted."""
    eng = _create_test_engine()
    char = _make_char(skills={"cunning": 3})

    state = GameState(
        build_id="af-m16-test",
        session_id="focused-test",
        character=char,
        current_region="iron_crags",
        current_scene="crags_base",
    )

    state_1, _ = eng.step(state, "stance_focused")
    assert state_1.character.has_marker("stance_focused")

    state_2, obs_2 = eng.step(state_1, "tactical_spot_weakness")
    assert obs_2.success is True
    assert state_2.world_flags.get("tactical_weakness_spotted") is True


# ==============================================================================
# 4. Pure Deterministic Replay Verification
# ==============================================================================

def test_tactical_stance_deterministic_replay():
    """Multi-step tactical stance transition sequence yields bit-for-bit identical state fingerprints."""
    eng = _create_test_engine()
    char = _make_char(attributes={"strength": 14, "agility": 14, "endurance": 14}, skills={"cunning": 3})

    def run_trace(seed: int, action_seq: List[str]) -> List[str]:
        st = GameState(
            build_id="af-m16-test",
            session_id=f"det-test-{seed}",
            character=char,
            current_region="iron_crags",
            current_scene="crags_base",
            rng=DeterministicRNG.from_seed(seed),
        )
        fps = [st.fingerprint()]
        for a_id in action_seq:
            st, obs = eng.step(st, a_id)
            assert obs.success is True, f"Failed at action {a_id}"
            fps.append(st.fingerprint())
        return fps

    actions = [
        "stance_aggressive",
        "tactical_brutal_strike",
        "stance_defensive",
        "tactical_brace_impact",
        "stance_elusive",
        "tactical_feint",
        "stance_focused",
        "tactical_spot_weakness",
        "stance_neutral",
    ]

    fps_run1 = run_trace(seed=777, action_seq=actions)
    fps_run2 = run_trace(seed=777, action_seq=actions)

    assert fps_run1 == fps_run2
    assert len(fps_run1) == len(actions) + 1

    # Tamper check: altering one action alters fingerprint stream
    tampered_actions = list(actions[:-1]) + ["stance_aggressive"]
    fps_tampered = run_trace(seed=777, action_seq=tampered_actions)
    assert fps_run1 != fps_tampered


# ==============================================================================
# 5. Hemingway Prose & Action Label Quality Bar
# ==============================================================================

def test_tactical_stance_prose_quality():
    """All stance text, shift results, and exploits conform to Hemingway prose constraints."""
    linter = ProseLinter()
    stances = get_tactical_stances()

    assert len(ALL_STANCE_MARKERS) == 4
    for marker in ALL_STANCE_MARKERS:
        assert any(s.marker == marker for s in stances.values())

    for s_id, stance in stances.items():
        # Action labels must be 1 to 3 words
        shift_words = stance.shift_label.split()
        assert 1 <= len(shift_words) <= 3, f"{s_id} shift label '{stance.shift_label}' exceeds 3 words"

        exploit_words = stance.exploit_label.split()
        assert 1 <= len(exploit_words) <= 3, f"{s_id} exploit label '{stance.exploit_label}' exceeds 3 words"

        # Shift result prose
        errs = linter.lint_text(stance.shift_result_text, context=f"{s_id}_shift")
        assert not errs, f"Prose violations in {s_id} shift: {errs}"

        # Exploit result prose
        errs = linter.lint_text(stance.exploit_result_text, context=f"{s_id}_exploit")
        assert not errs, f"Prose violations in {s_id} exploit: {errs}"

        # Log events in effects
        for eff in stance.shift_effects + stance.exploit_effects:
            if "log_event" in eff:
                errs = linter.lint_text(eff["log_event"], context=f"{s_id}_event")
                assert not errs, f"Prose violations in {s_id} log event: {errs}"
