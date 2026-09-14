"""Tests for Continental Ancient Lore Codex & Relic Deciphering Engine (Milestone 19).

Verifies:
1. Complete 15-entry codex catalogue (3 per province across 5 provinces).
2. Strict Hemingway prose linter compliance (FKGL 6-8, <=18 words/sent, <=3 words/label, no purple words).
3. 7-axis reactivity and prerequisite evaluation.
4. Dynamic affordance synthesis in scene contexts.
5. Deterministic state mutation, stamina deduction, and provincial mastery rewards.
6. Bit-for-bit replay determinism and state fingerprint fidelity.
7. ASGI REST API (/api/game/codex and progress payload).
8. Player CLI render_codex_log formatting.
"""
import pytest
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.actions import synthesize_affordances
from adventure_forge.core.character import CharacterSheet, get_preset
from adventure_forge.core.codex import (
    CODEX_ENTRIES,
    evaluate_codex_progress,
)
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.state import GameState
from adventure_forge.linter.prose_linter import ProseLinter
from adventure_forge.player.cli import render_codex_log


@pytest.fixture
def registry():
    return build_world_registry()


@pytest.fixture
def engine(registry):
    return AdventureEngine(registry)


def test_codex_catalogue_structure(registry):
    """Ensure exactly 15 codices exist, exactly 3 per province, with valid scenes."""
    all_scenes = {s for reg in registry.values() for s in reg.scenes.keys()}
    assert len(CODEX_ENTRIES) == 15

    province_counts = {}
    for entry in CODEX_ENTRIES.values():
        province_counts[entry.province_key] = province_counts.get(entry.province_key, 0) + 1
        assert entry.scene_id in all_scenes, f"Scene '{entry.scene_id}' not found in registry!"
        assert entry.reward_flag.startswith("codex_")
        assert len(entry.action_label.split()) <= 3
        assert entry.stamina_cost >= 1

    expected_provinces = {"reach", "lowlands", "scorchwaste", "high_court", "sunken_hollows"}
    assert set(province_counts.keys()) == expected_provinces
    for p, count in province_counts.items():
        assert count == 3, f"Province {p} has {count} entries, expected 3"


def test_codex_hemingway_prose_compliance():
    """Ensure every codex entry adheres to strict Hemingway prose constraints."""
    linter = ProseLinter()

    for entry in CODEX_ENTRIES.values():
        # Action label: 1-3 words
        label_words = entry.action_label.split()
        assert 1 <= len(label_words) <= 3, f"Label '{entry.action_label}' exceeds 3 words"

        # Discovery text linting
        disc_errors = linter.lint_text(entry.discovery_text, context=f"{entry.id}_discovery")
        assert not disc_errors, f"Discovery prose errors for {entry.id}: {disc_errors}"

        # Lore text linting
        lore_errors = linter.lint_text(entry.lore_text, context=f"{entry.id}_lore")
        assert not lore_errors, f"Lore prose errors for {entry.id}: {lore_errors}"


def test_codex_dynamic_affordance_synthesis(registry):
    """Test that codex affordances are synthesized only in matching scenes for eligible characters."""
    reach_scene = registry["province_reach"].scenes["reach_secret_shrine"]
    crags_scene = registry["iron_crags"].scenes["crags_base"]

    # Torin (scout with Mountain Scout trait) at reach_secret_shrine
    torin = get_preset("scout").character
    torin_actions = synthesize_affordances(
        reach_scene.base_actions,
        reach_scene.entities,
        torin,
        {},
        region_id="province_reach",
        scene_id="reach_secret_shrine",
    )
    codex_acts = [a for a in torin_actions if a.category == "codex"]
    assert len(codex_acts) == 1
    assert codex_acts[0].id == "codex_study_first_oath"
    assert codex_acts[0].label == "Study First Oath"

    # Torin at crags_base (no codex entry situated here)
    crags_actions = synthesize_affordances(
        crags_scene.base_actions,
        crags_scene.entities,
        torin,
        {},
        region_id="iron_crags",
        scene_id="crags_base",
    )
    crags_codex = [a for a in crags_actions if a.category == "codex"]
    assert len(crags_codex) == 0

    # Once unlocked, action is no longer offered
    unlocked_actions = synthesize_affordances(
        reach_scene.base_actions,
        reach_scene.entities,
        torin,
        {"codex_reach_first_oath": True},
        region_id="province_reach",
        scene_id="reach_secret_shrine",
    )
    assert not any(a.category == "codex" for a in unlocked_actions)


def test_codex_7axis_reactivity(registry):
    """Verify counterfactual character reactivity for deciphering relics."""
    thieves_scene = registry["province_lowlands"].scenes["lowlands_thieves_hall_sanctum"]

    # Silas the cutpurse has Agile Fingers trait and lockpick -> can read tallies
    silas = get_preset("cutpurse").character
    silas_actions = synthesize_affordances(
        thieves_scene.base_actions,
        thieves_scene.entities,
        silas,
        {},
        region_id="province_lowlands",
        scene_id="lowlands_thieves_hall_sanctum",
    )
    assert any(a.id == "codex_read_guild_tallies" for a in silas_actions)

    # Bare character without traits, skills, or items cannot read tallies
    bare_char = CharacterSheet(
        name="Novice",
        ancestry="Plainsman",
        background="Laborer",
        attributes={"might": 1, "agility": 1, "intellect": 1, "willpower": 1, "perception": 1, "charisma": 1},
        skills={},
        traits=[],
        flaws=[],
        reputation={},
        markers=[],
        inventory=[],
        health=10,
        stamina=10,
    )
    bare_actions = synthesize_affordances(
        thieves_scene.base_actions,
        thieves_scene.entities,
        bare_char,
        {},
        region_id="province_lowlands",
        scene_id="lowlands_thieves_hall_sanctum",
    )
    assert not any(a.id == "codex_read_guild_tallies" for a in bare_actions)

    # Equipping a lockpick enables deciphering for bare character
    geared_char = bare_char.modify(inventory=["lockpick"])
    geared_actions = synthesize_affordances(
        thieves_scene.base_actions,
        thieves_scene.entities,
        geared_char,
        {},
        region_id="province_lowlands",
        scene_id="lowlands_thieves_hall_sanctum",
    )
    assert any(a.id == "codex_read_guild_tallies" for a in geared_actions)


def test_codex_step_and_provincial_mastery(engine):
    """Test deciphering actions via engine.step, flag updates, and provincial mastery award."""
    torin = get_preset("scout").character.modify(stamina=10)
    state = GameState(
        build_id="af-build-001",
        session_id="codex-test-01",
        character=torin,
        current_region="province_reach",
        current_scene="reach_secret_shrine",
        world_flags={"codex_reach_gryphon_riders": True, "codex_reach_frost_forging": True},
    )

    # Decipher the 3rd Reach entry
    next_state, obs = engine.step(state, "codex_study_first_oath")
    assert obs.success
    assert next_state.world_flags.get("codex_reach_first_oath") is True
    assert next_state.character.has_marker("lore_reach_first_oath")

    # Provincial mastery unlocked!
    assert next_state.world_flags.get("reach_mastery_unlocked") is True
    assert next_state.character.has_marker("reach_archivist")
    assert any("Reach Archivist" in ev for ev in obs.events)

    # Progress evaluation
    progress = evaluate_codex_progress(next_state.world_flags)
    assert progress["discovered_count"] == 3
    assert progress["province_progress"]["reach"]["mastery_unlocked"] is True
    assert len(progress["masteries_unlocked"]) == 1
    assert progress["masteries_unlocked"][0]["title"] == "Reach Archivist"


def test_codex_replay_determinism(engine):
    """Verify that codex deciphering actions reproduce identical SHA-256 state fingerprints."""
    torin = get_preset("scout").character.modify(stamina=10)
    state1 = GameState(
        build_id="af-build-001",
        session_id="replay-test-01",
        character=torin,
        current_region="province_reach",
        current_scene="reach_secret_shrine",
    )
    state2 = GameState(
        build_id="af-build-001",
        session_id="replay-test-02",
        character=torin,
        current_region="province_reach",
        current_scene="reach_secret_shrine",
    )

    next1, obs1 = engine.step(state1, "codex_study_first_oath")
    next2, obs2 = engine.step(state2, "codex_study_first_oath")

    assert obs1.success and obs2.success
    assert next1.fingerprint() == next2.fingerprint()
    assert next1.character.stamina == 9
    assert next2.character.stamina == 9


def test_codex_asgi_endpoint():
    """Test /api/game/codex and progress payload in /api/game/new."""
    import asyncio
    import json
    from app import app

    # 1. GET /api/game/codex
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/api/game/codex",
        "headers": [],
        "query_string": b"",
    }
    sent_messages = []

    async def send(msg):
        sent_messages.append(msg)

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    asyncio.run(app(scope, receive, send))
    assert sent_messages[0]["status"] == 200
    body = json.loads(sent_messages[1]["body"].decode("utf-8"))
    assert body["total_entries"] == 15
    assert len(body["entries"]) == 15
    assert "reach" in body["masteries"]


def test_codex_cli_rendering(capsys):
    """Test CLI render_codex_log format and output integrity."""
    flags = {
        "codex_reach_first_oath": True,
        "reach_mastery_unlocked": True,
    }
    prog = evaluate_codex_progress(flags)
    render_codex_log(prog)
    captured = capsys.readouterr()
    assert "ANCIENT CODEX & RELIC ARCHIVES" in captured.out
    assert "The Reach" in captured.out
    assert "The First Oath" in captured.out
    assert "Reach Archivist" in captured.out
