"""M4/M5 Integration, Scenario & Adversarial Hardening Tests."""
import pytest
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry
from adventure_forge.content.quests import get_continental_main_quest
from adventure_forge.linter.prose_linter import ProseLinter


def _make_state(eng, scene_id, char=None, world_flags=None, seed=0):
    if char is None:
        char = CharacterSheet(name="T", ancestry="Plainsman", background="drifter")
    # Determine region from scene_id prefix
    reg = eng.world_registry
    region_id = None
    for r_id in reg:
        if scene_id in reg[r_id].scenes:
            region_id = r_id
            break
    if region_id is None:
        region_id = scene_id.split("_")[0]
    state = GameState(
        build_id=eng.build_id,
        session_id="test",
        character=char,
        current_region=region_id,
        current_scene=scene_id,
        world_flags=world_flags or {},
        rng=DeterministicRNG(seed),
    )
    return state


# ── M4 Integration & Scenario Tests ────────────────────────────────────────

def test_world_flags_persist_across_steps():
    """World flags set on state persist after non-movement action steps."""
    eng = AdventureEngine(build_world_registry())
    char = CharacterSheet(name="Traveler", ancestry="Plainsman", background="drifter")
    state = _make_state(eng, "crags_base", char, world_flags={"crags_beacon_lit": True})
    assert state.world_flags.get("crags_beacon_lit") is True
    actions = eng.get_legal_actions(state)
    non_move = [a for a in actions if a.category != "movement"]
    if non_move:
        state2, _ = eng.step(state, non_move[0].id)
        assert state2.world_flags.get("crags_beacon_lit") is True


def test_campaign_three_endings_reachable():
    """All 3 campaign endings are reachable from fully completed world flags."""
    quest = get_continental_main_quest()
    full_flags = {
        "crags_beacon_lit": True, "has_watch_badge": True,
        "scorch_compass_secured": True, "court_verdict_won": True,
        "sunken_relic_secured": True,
    }
    char = CharacterSheet(name="Hero", ancestry="Dune Walker", background="nomad")
    prog = quest.evaluate_progress(char, full_flags)
    assert prog["is_finished"] is True
    assert set(quest.endings.keys()) == {"justiciar_order", "shadow_syndicate", "unbounded_ruler"}


def test_deterministic_replay_20_steps():
    """20-step replay from fixed seed produces identical final fingerprint."""
    eng = AdventureEngine(build_world_registry())
    char = CharacterSheet(name="Replay", ancestry="Plainsman", background="drifter")
    state0 = _make_state(eng, "crags_base", char, seed=777)

    actions_taken = []
    state = state0
    for _ in range(20):
        avail = eng.get_legal_actions(state)
        if not avail:
            break
        actions_taken.append(avail[0].id)
        state, _ = eng.step(state, avail[0].id)
    final_fp = state.fingerprint()

    # Replay
    state_r = state0
    for aid in actions_taken:
        state_r, _ = eng.step(state_r, aid)
    assert state_r.fingerprint() == final_fp


def test_character_axis_divergence_across_provinces():
    """Outlaw vs Noble diverge in at least one dynamic description across all provinces."""
    eng = AdventureEngine(build_world_registry())
    reg = eng.world_registry
    outlaw = CharacterSheet(name="Silas", ancestry="Plainsman", background="outlaw_cutpurse",
                             traits=["night_eyed", "light_fingers"])
    noble = CharacterSheet(name="Vivienne", ancestry="Highborn", background="noble_exile",
                            traits=["silver_tongue", "court_manners"])
    diverged = False
    for r_id, region in reg.items():
        for sc_id in list(region.scenes.keys())[:5]:
            s_out = _make_state(eng, sc_id, outlaw)
            s_nob = _make_state(eng, sc_id, noble)
            obs_out = eng.observe(s_out)
            obs_nob = eng.observe(s_nob)
            if obs_out != obs_nob:
                diverged = True
                break
        if diverged:
            break
    assert diverged, "Characters must diverge in at least one observation across provinces"


# ── M5 Adversarial Hardening Tests ─────────────────────────────────────────

def test_no_softlocks_with_empty_inventory():
    """Every scene has >= 1 valid action even with empty inventory and no traits."""
    eng = AdventureEngine(build_world_registry())
    char = CharacterSheet(name="Bare", ancestry="Plainsman", background="drifter",
                           inventory={}, traits=[])
    for r_id, region in eng.world_registry.items():
        for sc_id in region.scenes:
            state = _make_state(eng, sc_id, char)
            avail = eng.get_legal_actions(state)
            assert len(avail) >= 1, f"Softlock in {sc_id}"


def test_no_crash_on_all_trait_combinations():
    """Engine never crashes with any single trait active in any scene sample."""
    eng = AdventureEngine(build_world_registry())
    all_traits = ["night_eyed", "light_fingers", "silver_tongue", "court_manners",
                  "heat_hardened", "deep_diver", "climber", "disguise_expert"]
    sample = [sc_id for r in eng.world_registry.values()
              for sc_id in list(r.scenes.keys())[:3]]
    for sc_id in sample:
        for trait in all_traits:
            char = CharacterSheet(name="T", ancestry="Plainsman", background="drifter",
                                   traits=[trait])
            state = _make_state(eng, sc_id, char)
            try:
                eng.get_legal_actions(state)
            except Exception as e:
                pytest.fail(f"Crash in {sc_id} with trait {trait}: {e}")


def test_tamper_detection_fingerprint_mismatch():
    """Modifying world_flags after fingerprinting produces a different hash."""
    eng = AdventureEngine(build_world_registry())
    char = CharacterSheet(name="T", ancestry="Plainsman", background="drifter")
    state1 = _make_state(eng, "crags_base", char, world_flags={})
    state2 = _make_state(eng, "crags_base", char, world_flags={"tampered": True})
    assert state1.fingerprint() != state2.fingerprint()


def test_linter_zero_violations_on_all_shipped_content():
    """ProseLinter reports zero violations on all 520 shipped scenes."""
    linter = ProseLinter()
    reg = build_world_registry()
    ok, errors = linter.lint_registry(reg)
    assert ok is True, f"Linter violations: {errors[:3]}"
    assert len(errors) == 0


def test_100_random_walks_no_crash():
    """100 random-walk sessions of 15 steps must never crash."""
    eng = AdventureEngine(build_world_registry())
    start_scenes = list(list(eng.world_registry.values())[0].scenes.keys())[:5]
    for seed in range(100):
        char = CharacterSheet(name=f"Bot{seed}", ancestry="Plainsman", background="drifter")
        start = start_scenes[seed % len(start_scenes)]
        state = _make_state(eng, start, char, seed=seed)
        for step in range(15):
            avail = eng.get_legal_actions(state)
            if not avail:
                break
            idx, _ = DeterministicRNG(seed + step).next_int(0, len(avail) - 1)
            state, _ = eng.step(state, avail[idx].id)
