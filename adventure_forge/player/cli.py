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
    """Render a clean, high-velocity, action-first player screen."""
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
    start_idx = page * page_size
    end_idx = min(start_idx + page_size, total_actions)
    page_actions = obs.legal_actions[start_idx:end_idx]

    print(f"AVAILABLE ACTIONS ({total_actions} total, showing {start_idx + 1}-{end_idx}):")
    for i, act in enumerate(page_actions, start=start_idx + 1):
        risk_str = f" [{act['risk'].upper()}]" if act['risk'] != 'low' else ""
        cost_str = f" (Stamina -{act['stamina_cost']})" if act.get('stamina_cost', 0) > 0 else ""
        print(f"  [{i:2d}] {act['label']}{risk_str}{cost_str}")

    print("-" * 65)
    nav_hints = []
    if end_idx < total_actions:
        nav_hints.append("'n' for next page")
    if page > 0:
        nav_hints.append("'p' for prev page")
    nav_hints.append("'q' to quit")
    print("Commands: " + ", ".join(nav_hints))


def start_new_game(char_preset: str = "cutpurse") -> Tuple[AdventureEngine, GameState]:
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    if char_preset == "cutpurse":
        char = CharacterSheet(
            name="Silas",
            ancestry="Deep-Dweller",
            background="cutpurse",
            attributes={"agility": 14, "strength": 9, "intimidation": 7},
            skills={"cunning": 4, "stealth": 3},
            traits=["night_eyed", "streetwise"],
            flaws=["marked_outlaw"],
            reputation={"smugglers": 10, "city_watch": -5},
            markers=["guild_brand"],
            inventory=["lockpick", "silver_coin"]
        )
        start_scene = "warrens_gate"
        start_region = "lower_warrens"
    elif char_preset == "noble":
        char = CharacterSheet(
            name="Lady Vivienne",
            ancestry="High-Kin",
            background="noble_exile",
            attributes={"agility": 8, "strength": 10, "intimidation": 14},
            skills={"rhetoric": 4, "cunning": 2},
            traits=["skeptical"],
            flaws=["oath_bound"],
            reputation={"city_watch": 10, "smugglers": -10},
            markers=["watch_crest"],
            inventory=["silver_coin", "legal_dossier"]
        )
        start_scene = "court_antechamber"
        start_region = "high_court"
    else:
        char = CharacterSheet(
            name="Garron",
            ancestry="Ashenborn",
            background="pit_fighter",
            attributes={"strength": 16, "agility": 12, "endurance": 14},
            skills={"athletics": 4, "brawling": 4},
            traits=["iron_gutted"],
            flaws=[],
            reputation={"iron_guard": 5},
            inventory=["water_skin", "crowbar"]
        )
        start_scene = "crags_base"
        start_region = "iron_crags"

    state = GameState(
        build_id="af-build-001",
        session_id=f"cli-session-{char_preset}",
        character=char,
        current_region=start_region,
        current_scene=start_scene,
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
            if (page + 1) * page_size < len(obs.legal_actions):
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
