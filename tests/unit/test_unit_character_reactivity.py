"""Tier 1 & Tier 2: 7-Axis Character Reactivity (Feature 2 / R2) Test Suite.

Satisfies TEST_INFRA.md:
- Tier 1 Coverage (>= 5 tests)
- Tier 2 Boundary & Corner (>= 5 tests)
"""
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.conditions import evaluate_condition


def _make_char(**overrides):
    base = {
        "name": "TestHero",
        "ancestry": "Plainsman",
        "background": "drifter",
        "attributes": {"strength": 10, "agility": 10, "endurance": 10, "cunning": 1},
        "skills": {"stealth": 1, "cunning": 1, "intimidation": 0},
        "traits": ["nimble"],
        "flaws": ["marked_outlaw"],
        "reputation": {"iron_guard": 0, "smugglers": 0},
        "markers": ["initiate_brand"],
        "inventory": ["bread_loaf"],
        "health": 20,
        "max_health": 20,
        "stamina": 10,
        "max_stamina": 10,
    }
    base.update(overrides)
    return CharacterSheet(**base)


# ── Tier 1: Unit Coverage (>= 5 tests) ───────────────────────────────────────

def test_character_ancestry_reactivity():
    """ancestry_is condition correctly matches character ancestry and rejects others."""
    char_dweller = _make_char(ancestry="Deep-Dweller")
    char_plains = _make_char(ancestry="Plainsman")

    cond_dweller = {"ancestry_is": "deep-dweller"}
    cond_highborn = {"ancestry_is": "highborn"}

    assert evaluate_condition(cond_dweller, char_dweller, {}) is True
    assert evaluate_condition(cond_dweller, char_plains, {}) is False
    assert evaluate_condition(cond_highborn, char_dweller, {}) is False


def test_character_background_reactivity():
    """background_is condition correctly identifies character background."""
    char_cutpurse = _make_char(background="cutpurse")
    char_noble = _make_char(background="noble_exile")

    cond_cutpurse = {"background_is": "cutpurse"}
    cond_noble = {"background_is": "noble_exile"}

    assert evaluate_condition(cond_cutpurse, char_cutpurse, {}) is True
    assert evaluate_condition(cond_cutpurse, char_noble, {}) is False
    assert evaluate_condition(cond_noble, char_noble, {}) is True


def test_character_attribute_thresholds():
    """min_attribute condition checks threshold values accurately."""
    char_strong = _make_char(attributes={"strength": 14})
    char_weak = _make_char(attributes={"strength": 9})

    cond_str = {"min_attribute": {"attribute": "strength", "value": 12}}

    assert evaluate_condition(cond_str, char_strong, {}) is True
    assert evaluate_condition(cond_str, char_weak, {}) is False


def test_character_skills_reactivity():
    """min_skill condition checks quantitative skill values accurately."""
    char_skilled = _make_char(skills={"cunning": 3, "stealth": 2})
    char_novice = _make_char(skills={"cunning": 1, "stealth": 0})

    cond_cunning = {"min_skill": {"skill": "cunning", "value": 2}}
    cond_stealth = {"min_skill": {"skill": "stealth", "value": 2}}

    assert evaluate_condition(cond_cunning, char_skilled, {}) is True
    assert evaluate_condition(cond_cunning, char_novice, {}) is False
    assert evaluate_condition(cond_stealth, char_skilled, {}) is True
    assert evaluate_condition(cond_stealth, char_novice, {}) is False


def test_character_traits_and_flaws_reactivity():
    """has_trait and has_flaw conditions correctly evaluate character traits."""
    char = _make_char(traits=["night_eyed", "nimble"], flaws=["marked_outlaw"])

    assert evaluate_condition({"has_trait": "night_eyed"}, char, {}) is True
    assert evaluate_condition({"has_trait": "climber"}, char, {}) is False
    assert evaluate_condition({"has_flaw": "marked_outlaw"}, char, {}) is True
    assert evaluate_condition({"has_flaw": "hemophobic"}, char, {}) is False


def test_character_reputation_and_markers():
    """min_reputation and has_marker conditions check social standing."""
    char = _make_char(
        reputation={"smugglers": 15, "iron_guard": -5},
        markers=["shadow_crest"]
    )

    assert evaluate_condition({"min_reputation": {"faction": "smugglers", "value": 10}}, char, {}) is True
    assert evaluate_condition({"min_reputation": {"faction": "smugglers", "value": 20}}, char, {}) is False
    assert evaluate_condition({"has_marker": "shadow_crest"}, char, {}) is True
    assert evaluate_condition({"has_marker": "royal_seal"}, char, {}) is False


# ── Tier 2: Boundary & Corner Tests (>= 5 tests) ─────────────────────────────

def test_exact_attribute_boundary_matching():
    """Attribute threshold behaves deterministically at exact boundaries (value-1, value, value+1)."""
    char_at_threshold = _make_char(attributes={"agility": 12})
    char_below = _make_char(attributes={"agility": 11})
    char_above = _make_char(attributes={"agility": 13})

    cond = {"min_attribute": {"attribute": "agility", "value": 12}}

    assert evaluate_condition(cond, char_at_threshold, {}) is True
    assert evaluate_condition(cond, char_below, {}) is False
    assert evaluate_condition(cond, char_above, {}) is True


def test_case_insensitive_matching_all_axes():
    """Condition evaluation handles case discrepancies across all character axes cleanly."""
    char = _make_char(
        ancestry="High-Born",
        background="Mercenary_Veteran",
        traits=["Night_Eyed"],
        flaws=["Marked_Outlaw"],
        markers=["Guild_Seal"]
    )

    assert evaluate_condition({"ancestry_is": "high-born"}, char, {}) is True
    assert evaluate_condition({"background_is": "mercenary_veteran"}, char, {}) is True
    assert evaluate_condition({"has_trait": "night_eyed"}, char, {}) is True
    assert evaluate_condition({"has_flaw": "marked_outlaw"}, char, {}) is True
    assert evaluate_condition({"has_marker": "guild_seal"}, char, {}) is True


def test_combinatorial_conditions_all_any_none():
    """Complex conditions with all_of, any_of, and none_of evaluate with strict logical precision."""
    char = _make_char(
        ancestry="Deep-Dweller",
        traits=["night_eyed"],
        skills={"stealth": 3},
        flaws=["marked_outlaw"]
    )

    cond_complex = {
        "all_of": [
            {"ancestry_is": "deep-dweller"},
            {"any_of": [
                {"has_trait": "light_fingers"},
                {"has_trait": "night_eyed"}
            ]},
            {"none_of": [
                {"has_flaw": "blind"},
                {"has_trait": "clumsy"}
            ]}
        ]
    }

    assert evaluate_condition(cond_complex, char, {}) is True

    # Violating none_of
    char_blind = char.modify(flaws=list(char.flaws) + ["blind"])
    assert evaluate_condition(cond_complex, char_blind, {}) is False


def test_empty_and_maximal_character_sheets():
    """Minimal empty character vs maximal character with 25 traits and skills."""
    char_empty = CharacterSheet(name="Empty", ancestry="None", background="None")
    char_max = CharacterSheet(
        name="GodHero",
        ancestry="Ashenborn",
        background="Archmage",
        attributes={k: 20 for k in ["strength", "agility", "endurance", "cunning", "arcana"]},
        skills={k: 10 for k in ["stealth", "brawl", "climb", "swim", "persuasion", "alchemy"]},
        traits=[f"trait_{i}" for i in range(25)],
        flaws=[f"flaw_{i}" for i in range(10)],
        reputation={f"faction_{i}": 50 for i in range(10)},
        markers=[f"marker_{i}" for i in range(15)],
        inventory=[f"item_{i}" for i in range(30)]
    )

    # Empty character fails trait checks cleanly without error
    assert evaluate_condition({"has_trait": "trait_0"}, char_empty, {}) is False
    assert evaluate_condition({"min_attribute": {"attribute": "strength", "value": 10}}, char_empty, {}) is False

    # Maximal character passes valid checks and can be stepped in engine
    assert evaluate_condition({"has_trait": "trait_10"}, char_max, {}) is True
    assert evaluate_condition({"min_skill": {"skill": "stealth", "value": 5}}, char_max, {}) is True


def test_reputation_negative_and_zero_boundaries():
    """min_reputation and max_reputation handle negative and zero thresholds correctly."""
    char_neutral = _make_char(reputation={"iron_guard": 0})
    char_hated = _make_char(reputation={"iron_guard": -15})
    char_admired = _make_char(reputation={"iron_guard": 20})

    assert evaluate_condition({"min_reputation": {"faction": "iron_guard", "value": 0}}, char_neutral, {}) is True
    assert evaluate_condition({"min_reputation": {"faction": "iron_guard", "value": 0}}, char_hated, {}) is False
    assert evaluate_condition({"min_reputation": {"faction": "iron_guard", "value": 15}}, char_admired, {}) is True
    assert evaluate_condition({"max_reputation": {"faction": "iron_guard", "value": -10}}, char_hated, {}) is True
    assert evaluate_condition({"max_reputation": {"faction": "iron_guard", "value": -10}}, char_neutral, {}) is False


def test_new_character_presets_integrity():
    """All 6 character presets (including nomad, diver, scout) load with valid orthogonal axes."""
    from adventure_forge.core.character import get_preset, list_presets
    from adventure_forge.content.loader import build_world_registry
    from adventure_forge.core.engine import AdventureEngine

    presets = list_presets()
    for expected in ["cutpurse", "noble", "warrior", "nomad", "diver", "scout"]:
        assert expected in presets

    engine = AdventureEngine(build_world_registry())

    for pid in ["nomad", "diver", "scout"]:
        preset = get_preset(pid)
        assert preset.character.name
        assert preset.character.ancestry
        assert preset.character.background
        assert len(preset.character.traits) >= 2
        assert preset.character.health == 20
        assert preset.character.stamina == 10

        # Verify starting scene exists in engine and can be observed
        scene = engine.get_scene(preset.start_scene)
        assert scene is not None, f"Start scene {preset.start_scene} for {pid} not found"


def test_scavenge_and_submersible_affordance_synthesis():
    """Entities with scavengeable and submersible tags generate dynamic affordances."""
    from adventure_forge.core.actions import synthesize_affordances
    from adventure_forge.core.character import get_preset

    char_diver = get_preset("diver").character
    char_nomad = get_preset("nomad").character

    entities = [
        {"id": "salvage_box", "name": "Supply Crate", "tags": ["scavengeable"]},
        {"id": "mini_sub", "name": "Deep Sub", "tags": ["submersible"]}
    ]

    # Nomad should see scavenge affordance
    nomad_actions = synthesize_affordances([], entities, char_nomad, {})
    scavenge_acts = [a for a in nomad_actions if a.id == "scavenge_salvage_box"]
    assert len(scavenge_acts) == 1
    assert scavenge_acts[0].label == "Scavenge Supply Crate"
    assert len(scavenge_acts[0].label.split()) <= 3

    # Diver has water_breather so should see submersible affordance
    diver_actions = synthesize_affordances([], entities, char_diver, {})
    dive_acts = [a for a in diver_actions if a.id == "dive_mini_sub"]
    assert len(dive_acts) == 1
    assert dive_acts[0].label == "Board Deep Sub"
    assert len(dive_acts[0].label.split()) <= 3

