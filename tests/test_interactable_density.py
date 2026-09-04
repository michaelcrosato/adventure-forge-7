"""Automated Verification Suite for Milestone 2: Interactable Density Enrichment.

Enforces:
- R5 / Feature 20: At least 50% (>= 260) of the 520 scenes offer >= 3 meaningful interactables.
- Invariant: sum(1 for s in scenes if len([a for a in s.base_actions if a.category != 'movement']) + len(s.entities) >= 3) >= 260.
- Cross-province density balance (all 5 provinces significantly enriched).
- Hemingway baseline compliance (1-3 word UI labels, <= 18 words/sentence, 0 purple words).
- Flawless execution of non-movement interactables in AdventureEngine.
"""
from adventure_forge.content.loader import build_world_registry
from adventure_forge.verification.density import verify_interactable_density
from adventure_forge.linter.prose_linter import ProseLinter, word_count
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine


def test_interactable_density_threshold():
    """Verify that >= 260 of 520 scenes have >= 3 non-movement interactables/entities."""
    registry = build_world_registry()
    ok, msg, stats = verify_interactable_density(registry)
    assert ok, msg
    assert stats["total_scenes"] == 520
    assert stats["dense_scenes"] >= 260
    assert stats["dense_percentage"] >= 50.0


def test_interactable_distribution_across_provinces():
    """Verify that density enrichment is distributed across all 5 major provinces."""
    registry = build_world_registry()
    provinces = [
        "province_reach",
        "province_lowlands",
        "province_scorchwaste",
        "province_high_court",
        "province_sunken_hollows",
    ]
    for prov_id in provinces:
        assert prov_id in registry, f"Province '{prov_id}' missing from world registry"
        prov = registry[prov_id]
        dense_count = sum(
            1 for s in prov.scenes.values()
            if len([a for a in s.base_actions if a.category != "movement"]) + len(s.entities) >= 3
        )
        # Every province has 101-102 scenes; each must contribute significantly (>= 50 dense scenes)
        assert dense_count >= 50, (
            f"Province '{prov_id}' has only {dense_count}/{len(prov.scenes)} dense scenes. "
            f"Expected at least 50 dense scenes per province."
        )


def test_new_interactable_actions_have_state_effects():
    """Verify that the 3rd interactables provide state mutations, items, or event logs."""
    registry = build_world_registry()
    meaningful_scenes = 0

    for region in registry.values():
        for scene in region.scenes.values():
            non_move = [a for a in scene.base_actions if a.category != "movement"]
            has_effects = any(len(a.effects) > 0 for a in non_move)
            has_entities = len(scene.entities) > 0
            if has_effects or has_entities:
                meaningful_scenes += 1

    assert meaningful_scenes >= 260, (
        f"Only {meaningful_scenes} scenes have meaningful state-mutating actions or entities. "
        f"Expected >= 260."
    )


def test_all_interactables_pass_hemingway_linter():
    """Verify that all non-movement actions strictly pass Hemingway constraints."""
    registry = build_world_registry()
    linter = ProseLinter()
    violations = []

    for reg_id, region in registry.items():
        for sc_id, scene in region.scenes.items():
            for act in scene.base_actions:
                if act.category == "movement":
                    continue
                # 1. Action label: 1-3 words
                wc = word_count(act.label)
                if wc < 1 or wc > 3:
                    violations.append(f"[{sc_id}] Action '{act.id}' label '{act.label}' has {wc} words (must be 1-3)")
                # 2. Result text: <= 18 words/sentence, zero purple prose
                if act.result_text:
                    errs = linter.lint_text(act.result_text, f"{sc_id} Action {act.id}", check_readability=False)
                    violations.extend(errs)

            for ent in scene.entities:
                # Entity description if present
                if isinstance(ent, dict) and ent.get("description"):
                    errs = linter.lint_text(ent["description"], f"{sc_id} Entity {ent.get('id')}", check_readability=False)
                    violations.extend(errs)
                # Entity name should be <= 2 words to ensure affordance labels stay <= 3 words
                name_words = word_count(ent.get("name", ""))
                if name_words > 2:
                    violations.append(f"[{sc_id}] Entity '{ent.get('id')}' name '{ent.get('name')}' has {name_words} words (max 2 recommended)")

    assert len(violations) == 0, f"Encountered {len(violations)} linter violations:\n" + "\n".join(violations[:10])


def test_interactable_actions_execution_integrity():
    """Verify that every non-movement action executes cleanly in AdventureEngine."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)
    char = CharacterSheet(
        name="DensityTester",
        ancestry="Deep-Dweller",
        background="noble_exile",
        attributes={"strength": 18, "agility": 18, "endurance": 18},
        skills={"cunning": 5},
        traits=["night_eyed", "nimble"],
        inventory=["lockpick", "crowbar", "silver_coin"]
    )

    failures = []
    actions_stepped = 0

    for reg_id, region in registry.items():
        for sc_id, scene in region.scenes.items():
            state = GameState(
                build_id="af-m2-test",
                session_id=f"test-{sc_id}",
                character=char,
                current_region=reg_id,
                current_scene=sc_id
            )
            legal_actions = engine.get_legal_actions(state)
            non_move = [a for a in legal_actions if a.category != "movement"]
            for act in non_move:
                actions_stepped += 1
                try:
                    next_state, obs = engine.step(state, act.id)
                    if not obs.success:
                        failures.append((sc_id, act.id, f"Step failed: {obs.message}"))
                except Exception as exc:
                    failures.append((sc_id, act.id, f"{type(exc).__name__}: {exc}"))

    assert actions_stepped >= 1040, f"Expected >= 1040 non-movement actions stepped, got {actions_stepped}"
    assert len(failures) == 0, f"Execution failed on {len(failures)} actions:\n" + "\n".join(str(f) for f in failures[:10])
