"""Player Interface CLI (Interactive Terminal Runner).

Enforces:
- G2 / G5: Action-first display, concise observation, legal verb list.
- I6: Information Firewall — player sees only player-safe observations.
- I8: Observation budget with clean pagination for large action sets.
"""
import sys
from typing import Optional, List, Tuple
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry


def render_ui(obs, page: int = 0, page_size: int = 15):
    """Render a clean, high-velocity, action-first player screen with categorized pagination."""
    print("\n" + "=" * 65)
    print(f" {obs.title.upper()}  [{obs.region_id}]")
    print("=" * 65)
    print(f"\n{obs.description}\n")

    if obs.events:
        print("EVENTS:")
        for ev in obs.events:
            print(f"  • {ev}")
        print()

    total_actions = len(obs.legal_actions)
    total_pages = max(1, (total_actions + page_size - 1) // page_size)
    page = max(0, min(page, total_pages - 1))
    start_idx = page * page_size
    end_idx = min(start_idx + page_size, total_actions)
    page_actions = obs.legal_actions[start_idx:end_idx]

    if total_actions == 0:
        print("AVAILABLE ACTIONS (0 total | Page 1 of 1):")
        print("  No actions available.")
    else:
        print(f"AVAILABLE ACTIONS ({total_actions} total | Page {page + 1} of {total_pages} | Showing {start_idx + 1}-{end_idx}):")
        current_cat = None
        for i, act in enumerate(page_actions, start=start_idx + 1):
            cat = act.get("category", "interaction").replace("_", " ").upper()
            if cat != current_cat:
                current_cat = cat
                print(f"\n  [{current_cat}]")
            risk_str = f" [{act['risk'].upper()}]" if act.get('risk') and act['risk'] != 'low' else ""
            cost_str = f" (Stamina -{act['stamina_cost']})" if act.get('stamina_cost', 0) > 0 else ""
            print(f"    [{i:3d}] {act['label']}{risk_str}{cost_str}")

    print("-" * 65)
    nav_hints = []
    if page + 1 < total_pages:
        nav_hints.append("'n' for next page")
    if page > 0:
        nav_hints.append("'p' for prev page")
    if total_pages > 1:
        nav_hints.append("'page <num>' to jump")
    nav_hints.append("'q' to quit")
    print("Commands: " + ", ".join(nav_hints))


def start_new_game(char_preset: str = "cutpurse") -> Tuple[AdventureEngine, GameState]:
    from adventure_forge.core.character import get_preset
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    try:
        preset = get_preset(char_preset)
    except KeyError:
        preset = get_preset("warrior")

    state = GameState(
        build_id="af-build-001",
        session_id=f"cli-session-{preset.id}",
        character=preset.character,
        current_region=preset.start_region,
        current_scene=preset.start_scene,
        rng=DeterministicRNG.from_seed(999)
    )

    return engine, state


def main():
    preset = sys.argv[1] if len(sys.argv) > 1 else "cutpurse"
    engine, state = start_new_game(preset)
    obs = engine.observe(state)

    page = 0
    page_size = 15

    while True:
        render_ui(obs, page, page_size)
        try:
            choice = input("\nChoose action [number or command]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting AdventureForge.")
            break

        if choice in ("q", "quit", "exit"):
            print("Session ended.")
            break
        elif choice == "n":
            total_pages = max(1, (len(obs.legal_actions) + page_size - 1) // page_size)
            if page + 1 < total_pages:
                page += 1
            else:
                print("Already on last page.")
            continue
        elif choice == "p":
            if page > 0:
                page -= 1
            else:
                print("Already on first page.")
            continue
        elif choice.startswith("page ") or choice.startswith("goto "):
            parts = choice.split()
            if len(parts) == 2 and parts[1].isdigit():
                target_page = int(parts[1]) - 1
                total_pages = max(1, (len(obs.legal_actions) + page_size - 1) // page_size)
                if 0 <= target_page < total_pages:
                    page = target_page
                else:
                    print(f"Page must be between 1 and {total_pages}.")
            else:
                print("Usage: page <number> or goto <number>")
            continue

        if not choice.isdigit():
            # Check if user entered action id directly
            matches = [a for a in obs.legal_actions if a["id"] == choice]
            if matches:
                selected_action_id = matches[0]["id"]
            else:
                print(f"Invalid input '{choice}'. Enter a number from the action list.")
                continue
        else:
            num = int(choice)
            if 1 <= num <= len(obs.legal_actions):
                selected_action_id = obs.legal_actions[num - 1]["id"]
            else:
                print(f"Choice {num} out of bounds (1..{len(obs.legal_actions)}).")
                continue

        state, obs = engine.step(state, selected_action_id)
        page = 0  # Reset page on state transition

        if obs.is_terminal:
            render_ui(obs, page, page_size)
            print(f"\n*** OUTCOME REACHED: {obs.outcome or 'JOURNEY CONCLUDED'} ***\n")
            break


if __name__ == "__main__":
    main()
