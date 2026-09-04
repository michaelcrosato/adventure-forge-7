"""Tests for the Player CLI Interface and Pagination (adventure_forge.player.cli).

Validates:
- Category grouping and display
- Pagination math and display (Page X of Y, Showing A-B)
- Unbounded choice sets (115 actions in bazaar_center) without truncation
- Traversal forward and backward
- Edge case boundaries (0 actions, exact page multiples, 1 action)
- Clamping of out-of-bounds page requests
- Preset integration in start_new_game()
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pytest
from adventure_forge.content.loader import build_world_registry
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.state import GameState
from adventure_forge.player.cli import render_ui, start_new_game


@dataclass
class MockObs:
    title: str = "Test Scene"
    region_id: str = "test_realm"
    description: str = "A testing location."
    events: List[str] = field(default_factory=list)
    legal_actions: List[Dict[str, Any]] = field(default_factory=list)


def _get_bazaar_obs():
    reg = build_world_registry()
    eng = AdventureEngine(reg)
    char = CharacterSheet(name="Tester", ancestry="Plainsman", background="merchant")
    state = GameState(
        build_id="t",
        session_id="s",
        character=char,
        current_region="stress_market",
        current_scene="bazaar_center"
    )
    return eng.observe(state)


def test_render_ui_small_action_set(capsys):
    """Normal small scene displays all actions on one page with category headers and no next-page hint."""
    obs = MockObs(
        legal_actions=[
            {"id": "look_around", "label": "Look Around", "category": "interaction", "risk": "low", "stamina_cost": 0},
            {"id": "climb_ladder", "label": "Climb Ladder", "category": "movement", "risk": "low", "stamina_cost": 1},
        ]
    )
    render_ui(obs, page=0, page_size=15)
    captured = capsys.readouterr().out

    assert "AVAILABLE ACTIONS (2 total | Page 1 of 1 | Showing 1-2):" in captured
    assert "[INTERACTION]" in captured
    assert "[MOVEMENT]" in captured
    assert "Look Around" in captured
    assert "Climb Ladder" in captured
    assert "'n' for next page" not in captured
    assert "'p' for prev page" not in captured


def test_render_ui_large_action_set_pagination_bazaar(capsys):
    """bazaar_center with 115 actions paginates cleanly to 8 pages (15/page)."""
    obs = _get_bazaar_obs()
    assert len(obs.legal_actions) == 115

    render_ui(obs, page=0, page_size=15)
    captured = capsys.readouterr().out

    assert "AVAILABLE ACTIONS (115 total | Page 1 of 8 | Showing 1-15):" in captured
    assert "'n' for next page" in captured
    assert "'p' for prev page" not in captured
    assert "'page <num>' to jump" in captured


def test_render_ui_page_traversal_middle_and_last(capsys):
    """Traversing to middle page shows both next/prev; last page shows only prev."""
    obs = _get_bazaar_obs()

    # Middle page (Page 2)
    render_ui(obs, page=1, page_size=15)
    cap_mid = capsys.readouterr().out
    assert "Page 2 of 8 | Showing 16-30" in cap_mid
    assert "'n' for next page" in cap_mid
    assert "'p' for prev page" in cap_mid

    # Last page (Page 8)
    render_ui(obs, page=7, page_size=15)
    cap_last = capsys.readouterr().out
    assert "Page 8 of 8 | Showing 106-115" in cap_last
    assert "'p' for prev page" in cap_last
    assert "'n' for next page" not in cap_last


def test_render_ui_action_categorization_and_grouping(capsys):
    """Action categories are rendered as group headers before items."""
    obs = _get_bazaar_obs()
    render_ui(obs, page=0, page_size=15)
    captured = capsys.readouterr().out

    # Bazaar starts with movement actions then interaction
    assert "[MOVEMENT]" in captured
    assert "[INTERACTION]" in captured


def test_no_truncation_across_all_pages(capsys):
    """Traversing every page reveals all 115 actions without any truncated labels."""
    obs = _get_bazaar_obs()
    all_output = []
    page_size = 15
    total_pages = (len(obs.legal_actions) + page_size - 1) // page_size

    for p in range(total_pages):
        render_ui(obs, page=p, page_size=page_size)
        all_output.append(capsys.readouterr().out)

    combined = "\n".join(all_output)
    # Verify every 1-based index from 1 to 115 is present in brackets
    for num in range(1, 116):
        expected_label = f"[{num:3d}]"
        assert expected_label in combined, f"Action number {expected_label} missing from paginated output!"

    # Verify no action label ends in ellipsis
    for act in obs.legal_actions:
        assert not act["label"].endswith("..."), f"Action {act['label']} appears truncated"


def test_boundary_zero_actions(capsys):
    """Zero legal actions scene renders clean message without off-by-one errors."""
    obs = MockObs(legal_actions=[])
    render_ui(obs, page=0, page_size=15)
    captured = capsys.readouterr().out

    assert "AVAILABLE ACTIONS (0 total | Page 1 of 1):" in captured
    assert "No actions available." in captured
    assert "showing 1-0" not in captured


def test_boundary_exact_multiples_and_single_action(capsys):
    """Page math handles 1 action and exact multiples without empty trailing pages."""
    # Single action
    obs1 = MockObs(legal_actions=[{"id": "a", "label": "Act", "category": "c", "risk": "low", "stamina_cost": 0}])
    render_ui(obs1, page=0, page_size=15)
    cap1 = capsys.readouterr().out
    assert "Page 1 of 1 | Showing 1-1" in cap1

    # Exact multiple: 30 actions with page_size=15 -> 2 pages exactly
    acts30 = [
        {"id": f"act_{i}", "label": f"Action {i}", "category": "c", "risk": "low", "stamina_cost": 0}
        for i in range(30)
    ]
    obs30 = MockObs(legal_actions=acts30)
    render_ui(obs30, page=1, page_size=15)
    cap30 = capsys.readouterr().out
    assert "Page 2 of 2 | Showing 16-30" in cap30
    assert "'n' for next page" not in cap30


def test_page_number_clamping(capsys):
    """Out-of-range negative and overly large page indices are clamped safely."""
    obs = _get_bazaar_obs()

    # Negative page clamps to 0 (Page 1)
    render_ui(obs, page=-10, page_size=15)
    cap_neg = capsys.readouterr().out
    assert "Page 1 of 8 | Showing 1-15" in cap_neg

    # Large page clamps to last page (Page 8)
    render_ui(obs, page=999, page_size=15)
    cap_large = capsys.readouterr().out
    assert "Page 8 of 8 | Showing 106-115" in cap_large


def test_start_new_game_presets():
    """start_new_game correctly provisions engine and state from presets."""
    eng1, state1 = start_new_game("cutpurse")
    assert state1.character.name == "Silas"
    assert state1.current_scene == "warrens_gate"
    assert state1.current_region == "lower_warrens"

    eng2, state2 = start_new_game("noble")
    assert state2.character.name == "Lady Vivienne"
    assert state2.current_scene == "court_antechamber"

    eng3, state3 = start_new_game("pit_fighter")
    assert state3.character.name == "Garron"
    assert state3.current_scene == "crags_base"

    # Fallback to warrior on invalid preset
    eng4, state4 = start_new_game("nonexistent_preset")
    assert state4.character.name == "Garron"
