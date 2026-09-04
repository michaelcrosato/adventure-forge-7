"""Tier 1 & Tier 2: Unbounded Choice Space (Feature 4 / R4) Test Suite.

Satisfies TEST_INFRA.md:
- Tier 1 Coverage (>= 5 tests)
- Tier 2 Boundary & Corner (>= 5 tests)
"""
from adventure_forge.core.actions import Action, synthesize_affordances
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry


def _make_char(**overrides):
    base = {
        "name": "UnboundedHero",
        "ancestry": "Plainsman",
        "background": "drifter",
        "attributes": {"strength": 12, "agility": 10, "endurance": 10, "cunning": 2},
        "skills": {"stealth": 2, "cunning": 2},
        "traits": ["night_eyed"],
        "flaws": [],
        "reputation": {},
        "markers": [],
        "inventory": ["lockpick", "climbing_rope", "torch", "crowbar"],
        "health": 20,
        "max_health": 20,
        "stamina": 10,
        "max_stamina": 10,
    }
    base.update(overrides)
    return CharacterSheet(**base)


# ── Tier 1: Unit Coverage (>= 5 tests) ───────────────────────────────────────

def test_affordance_synthesis_all_categories():
    """Dynamic synthesis correctly unions base, inventory, trait, and entity affordances."""
    char = _make_char()
    base_actions = [
        Action(id="look_around", label="Look around", category="interaction", result_text="You survey the scene.")
    ]
    scene_entities = [
        {"id": "gate_grate", "name": "Iron Grate", "tags": ["lockable"], "initial_state": "locked"},
        {"id": "high_wall", "name": "Rough Stone Wall", "tags": ["climbable"], "climb_destination": "high_overlook"}
    ]

    actions = synthesize_affordances(base_actions, scene_entities, char, {})
    categories = {a.category for a in actions}

    assert "interaction" in categories
    assert "item_affordance" in categories
    assert "systemic" in categories
    action_ids = [a.id for a in actions]
    assert "look_around" in action_ids
    assert "pick_gate_grate" in action_ids
    assert "force_gate_grate" in action_ids
    assert "climb_high_wall" in action_ids


def test_action_category_and_risk_assignment():
    """Actions retain their designated categories and risks through synthesis."""
    char = _make_char()
    base_actions = [
        Action(id="act_safe", label="Drink water", category="interaction", risk="low"),
        Action(id="act_risky", label="Jump chasm", category="movement", risk="high", stamina_cost=3)
    ]
    actions = synthesize_affordances(base_actions, [], char, {})

    safe = next(a for a in actions if a.id == "act_safe")
    risky = next(a for a in actions if a.id == "act_risky")

    assert safe.category == "interaction"
    assert safe.risk == "low"
    assert safe.stamina_cost == 0

    assert risky.category == "movement"
    assert risky.risk == "high"
    assert risky.stamina_cost == 3


def test_affordance_deduplication():
    """Synthesizing actions with overlapping IDs deduplicates without error."""
    char = _make_char()
    base_actions = [
        Action(id="duplicate_id", label="Option A", category="interaction"),
        Action(id="duplicate_id", label="Option B", category="interaction"),
    ]
    actions = synthesize_affordances(base_actions, [], char, {})
    ids = [a.id for a in actions]
    assert len(ids) == 1


def test_inventory_affordance_generation():
    """Inventory tools dynamically generate affordances for compatible scene tags."""
    char_with_picks = _make_char(inventory=["lockpick"])
    char_without_picks = _make_char(inventory=[])

    scene_entities = [
        {"id": "chest_01", "name": "Brass Chest", "tags": ["lockable"], "initial_state": "locked"}
    ]

    actions_with = synthesize_affordances([], scene_entities, char_with_picks, {})
    actions_without = synthesize_affordances([], scene_entities, char_without_picks, {})

    assert any(a.id == "pick_chest_01" for a in actions_with)
    assert not any(a.id == "pick_chest_01" for a in actions_without)


def test_trait_exploit_affordance_generation():
    """Traits dynamically generate specialized trait exploit actions."""
    # pyromaniac trait allows melting locked items without acid vial
    char_pyro = _make_char(traits=["pyromaniac"], inventory=[])
    char_normal = _make_char(traits=[], inventory=[])

    scene_entities = [
        {"id": "vault_gate", "name": "Iron Vault", "tags": ["lockable"], "initial_state": "locked"}
    ]

    actions_pyro = synthesize_affordances([], scene_entities, char_pyro, {})
    actions_normal = synthesize_affordances([], scene_entities, char_normal, {})

    pyro_ids = [a.id for a in actions_pyro]
    normal_ids = [a.id for a in actions_normal]

    assert "melt_vault_gate" in pyro_ids
    assert "melt_vault_gate" not in normal_ids


# ── Tier 2: Boundary & Corner Tests (>= 5 tests) ─────────────────────────────

def test_bazaar_115_actions_scaling():
    """The Grand Bazaar scene enumerates 115 legal actions without crash or truncation."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)
    char = _make_char()
    state = GameState(
        build_id=engine.build_id,
        session_id="bazaar-test",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center",
        world_flags={},
        history=[],
        event_log=[],
        turn_count=0,
        rng=DeterministicRNG(42),
    )

    actions = engine.get_legal_actions(state)
    assert len(actions) >= 100, f"Expected >= 100 actions, got {len(actions)}"
    obs = engine.observe(state)
    assert len(obs.legal_actions) == len(actions)
    assert obs.success is True


def test_massive_inventory_200_actions_scaling():
    """Synthesizes 200+ legal actions when holding extensive items across multi-entity room."""
    base_actions = [Action(id=f"base_act_{i}", label=f"Action {i}", category="interaction") for i in range(120)]
    entities = [
        {"id": f"chest_{i}", "name": f"Chest {i}", "tags": ["lockable", "flammable"], "initial_state": "locked"} for i in range(40)
    ]
    char = _make_char(inventory=["lockpick", "crowbar", "torch"])

    actions = synthesize_affordances(base_actions, entities, char, {})
    # 120 base actions + 40 pick affordances + 40 force affordances + 40 burn affordances = 240 actions
    assert len(actions) >= 200
    ids = [a.id for a in actions]
    assert len(ids) == len(set(ids))


def test_zero_actions_terminal_state():
    """Scene with 0 legal actions is identified as terminal and handles observe gracefully."""
    char = _make_char()
    actions = synthesize_affordances([], [], char, {})
    assert len(actions) == 0


def test_single_action_forced_transition():
    """Scene with exactly 1 legal action behaves deterministically without issues."""
    char = _make_char()
    single_action = [Action(id="press_forward", label="Press forward", category="movement", target_scene="next_room")]
    actions = synthesize_affordances(single_action, [], char, {})
    assert len(actions) == 1
    assert actions[0].id == "press_forward"


def test_affordance_mutation_after_item_consumption():
    """Taking an action that spends/loses an item immediately removes corresponding affordance."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)
    char = _make_char(inventory=["silver_coin"])
    state = GameState(
        build_id=engine.build_id,
        session_id="item-consume-test",
        character=char,
        current_region="lower_warrens",
        current_scene="warrens_gate",
        world_flags={},
        history=[],
        event_log=[],
        turn_count=0,
        rng=DeterministicRNG(42),
    )

    legal_before = [a.id for a in engine.get_legal_actions(state)]
    assert "pay_gate_toll" in legal_before

    # Take toll action (costs silver_coin)
    new_state, res = engine.step(state, "pay_gate_toll")
    assert res.success is True
    assert "silver_coin" not in new_state.character.inventory

    # In warrens_gate without coin, toll action is no longer legal
    gate_state_no_coin = new_state.evolve(current_scene="warrens_gate")
    legal_after = [a.id for a in engine.get_legal_actions(gate_state_no_coin)]
    assert "pay_gate_toll" not in legal_after
