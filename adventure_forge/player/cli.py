"""Player Interface CLI (Interactive Terminal Runner).

Enforces:
- G2 / G5: Action-first display, concise observation, legal verb list.
- I6: Information Firewall — player sees only player-safe observations.
- I8: Observation budget with clean pagination for large action sets.
"""
import json
import sys
from typing import Tuple, Optional, Dict, Any, List
from adventure_forge.core.character import get_preset
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry


def render_character_sheet(state: GameState) -> None:
    """Display full 7-axis character state vector."""
    c = state.character
    print("\n" + "=" * 65)
    print(f" CHARACTER SHEET: {c.name.upper()} ({c.ancestry} • {c.background})")
    print("=" * 65)
    print(f" Health: {c.health}/{c.max_health} | Stamina: {c.stamina}/{c.max_stamina}")
    print("\n [ATTRIBUTES]")
    for attr, val in sorted(c.attributes.items()):
        print(f"   {attr.capitalize():14s}: {val}")
    print("\n [SKILLS]")
    for skill, val in sorted(c.skills.items()):
        print(f"   {skill.capitalize():14s}: {val}")
    print(f"\n [TRAITS]  ({len(c.traits)}): {', '.join(c.traits) if c.traits else 'None'}")
    print(f" [FLAWS]   ({len(c.flaws)}): {', '.join(c.flaws) if c.flaws else 'None'}")
    print(f" [MARKERS] ({len(c.markers)}): {', '.join(c.markers) if c.markers else 'None'}")
    print("\n [FACTION REPUTATION]")
    if c.reputation:
        for faction, rep in sorted(c.reputation.items()):
            sign = "+" if rep > 0 else ""
            print(f"   {faction.replace('_', ' ').capitalize():18s}: {sign}{rep}")
    else:
        print("   Neutral with all factions.")
    print(f"\n [INVENTORY] ({len(c.inventory)} items):")
    if c.inventory:
        for item in sorted(c.inventory):
            print(f"   • {item}")
    else:
        print("   (Empty)")
    print("=" * 65 + "\n")


def render_quest_log(quest_info: Dict[str, Any]) -> None:
    """Display comprehensive continental and provincial quest progress."""
    print("\n" + "=" * 65)
    print(" QUEST LOG: CONTINENTAL CAMPAIGN & PROVINCIAL SUBQUESTS")
    print("=" * 65)
    active_stg = quest_info.get("active_stage", "None")
    is_fin = quest_info.get("is_finished", False)
    comp_stages = quest_info.get("completed_stages", [])
    print(" Main Campaign: The Five Seals of Sovereignty")
    print(f" Status       : {'COMPLETED' if is_fin else f'Active Stage -> {active_stg}'}")
    print(f" Seals Won    : {len(comp_stages)}/5 ({', '.join(comp_stages) if comp_stages else 'None'})")

    subquests = quest_info.get("subquests", {})
    if subquests:
        print("\n [PROVINCIAL SUBQUESTS]")
        for qid, qprog in sorted(subquests.items()):
            q_name = qid.replace("subquest_", "").replace("quest_", "").replace("_", " ").title()
            if qprog.get("is_finished"):
                print(f"   • {q_name:32s}: [COMPLETED]")
            elif qprog.get("active_stage"):
                print(f"   • {q_name:32s}: Stage -> {qprog['active_stage']}")
            else:
                print(f"   • {q_name:32s}: [Undiscovered]")
    print("=" * 65 + "\n")


def render_history(state: GameState) -> None:
    """Display turn-by-turn history of actions and recent events."""
    print("\n" + "=" * 65)
    print(f" ACTION & EVENT HISTORY ({len(state.history)} steps, Turn {state.turn_count})")
    print("=" * 65)
    if not state.history:
        print("  No actions taken yet.")
    else:
        for idx, act in enumerate(state.history, start=1):
            print(f"  Turn {idx:2d}: {act}")
    if state.event_log:
        print("\n [RECENT EVENTS]")
        for ev in state.event_log[-5:]:
            print(f"  • {ev}")
    print("=" * 65 + "\n")


def render_ui(
    obs,
    page: int = 0,
    page_size: int = 15,
    state: Optional[GameState] = None,
    quest_info: Optional[Dict[str, Any]] = None
):
    """Render a clean, high-velocity, action-first player screen with categorized pagination."""
    print("\n" + "=" * 65)
    print(f" {obs.title.upper()}  [{obs.region_id}]")
    if state:
        c = state.character
        status_str = f" | Status: {', '.join(c.markers)}" if c.markers else " | Status: Normal"
        items_str = f" | Items: {len(c.inventory)}"
        print(f" HP: {c.health}/{c.max_health} | SP: {c.stamina}/{c.max_stamina}{status_str}{items_str}")
    if quest_info:
        active_stg = quest_info.get("active_stage", "Exploring Continent")
        print(f" Quest: {active_stg}")
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
    nav_hints.append("'sheet' for stats")
    nav_hints.append("'quest' for log")
    if state and state.turn_count > 0:
        nav_hints.append("'u' to undo")
    nav_hints.append("'q' to quit")
    print("Commands: " + ", ".join(nav_hints))


def start_new_game(char_preset: str = "cutpurse") -> Tuple[AdventureEngine, GameState]:
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


def execute_replay(
    replay_data: Dict[str, Any],
    engine: Optional[AdventureEngine] = None,
) -> Tuple[GameState, Any, List[str]]:
    """Deterministically execute an action trace and return final state, obs, and fingerprints."""
    if engine is None:
        registry = build_world_registry()
        engine = AdventureEngine(registry)

    preset_name = str(replay_data.get("preset", "cutpurse"))
    seed = int(replay_data.get("seed", 42))
    actions = replay_data.get("actions", replay_data.get("history", []))

    try:
        preset = get_preset(preset_name)
    except KeyError:
        preset = get_preset("cutpurse")

    state = GameState(
        build_id="af-build-001",
        session_id=f"cli-replay-{preset.id}-{seed}",
        character=preset.character,
        current_region=preset.start_region,
        current_scene=preset.start_scene,
        rng=DeterministicRNG.from_seed(seed),
    )
    obs = engine.observe(state)
    fingerprints = [state.fingerprint()]

    for act_id in actions:
        state, obs = engine.step(state, str(act_id))
        fingerprints.append(state.fingerprint())
        if not obs.success or obs.is_terminal:
            break

    return state, obs, fingerprints


def main():
    import os
    if len(sys.argv) > 1 and sys.argv[1] == "--replay":
        if len(sys.argv) < 3:
            print("Usage: python3 -m adventure_forge.player.cli --replay <replay.json>")
            sys.exit(1)
        src = sys.argv[2]
        if os.path.exists(src):
            with open(src, "r", encoding="utf-8") as f:
                replay_payload = json.load(f)
        else:
            replay_payload = json.loads(src)

        registry = build_world_registry()
        engine = AdventureEngine(registry)
        state, obs, fps = execute_replay(replay_payload, engine)

        print("\n" + "=" * 65)
        print(" ADVENTUREFORGE DETERMINISTIC REPLAY EXECUTION")
        print("=" * 65)
        print(f" Preset           : {replay_payload.get('preset', 'cutpurse')}")
        print(f" Seed             : {replay_payload.get('seed', 42)}")
        print(f" Executed Steps   : {state.turn_count}")
        print(f" Final Scene      : {state.current_scene} [{state.current_region}]")
        print(f" Final SHA-256    : {state.fingerprint()}")
        expected_fp = replay_payload.get("fingerprint")
        if expected_fp:
            matches = (expected_fp == state.fingerprint())
            status_text = "BIT-FOR-BIT IDENTICAL ✓" if matches else f"MISMATCH (expected {expected_fp})"
            print(f" Fingerprint Match: {status_text}")
        print("=" * 65 + "\n")

        if obs.is_terminal:
            print(f"*** OUTCOME REACHED: {obs.outcome or 'JOURNEY CONCLUDED'} ***\n")
            return
        preset = str(replay_payload.get("preset", "cutpurse"))
    else:
        preset = sys.argv[1] if len(sys.argv) > 1 else "cutpurse"
        engine, state = start_new_game(preset)
        obs = engine.observe(state)

    state_history: List[GameState] = [state]
    page = 0
    page_size = 15

    while True:
        quest_info = engine.get_quest_progress(state)
        render_ui(obs, page=page, page_size=page_size, state=state, quest_info=quest_info)
        try:
            choice = input("\nChoose action [number or command]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting AdventureForge.")
            break

        if choice in ("q", "quit", "exit"):
            print("Session ended.")
            break
        elif choice in ("sheet", "c", "stats"):
            render_character_sheet(state)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("quest", "quests", "log"):
            render_quest_log(quest_info)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("history", "hist"):
            render_history(state)
            input("Press Enter to return to action screen...")
            continue
        elif choice in ("u", "undo"):
            if len(state_history) > 1:
                state_history.pop()
                state = state_history[-1]
                obs = engine.observe(state)
                page = 0
                print(f"\n[✓] Turn undone. Reverted to Turn {state.turn_count}.")
            else:
                print("\n[!] Already at initial state; cannot undo further.")
            continue
        elif choice == "export":
            export_payload = {
                "preset": preset,
                "turn_count": state.turn_count,
                "history": list(state.history),
                "fingerprint": state.fingerprint(),
            }
            print("\n[Deterministic Replay Payload]:")
            print(json.dumps(export_payload, indent=2))
            input("\nPress Enter to return to action screen...")
            continue
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
                print(f"Invalid input '{choice}'. Enter a number from the action list, or 'sheet' / 'quest' / 'u'.")
                continue
        else:
            num = int(choice)
            if 1 <= num <= len(obs.legal_actions):
                selected_action_id = obs.legal_actions[num - 1]["id"]
            else:
                print(f"Choice {num} out of bounds (1..{len(obs.legal_actions)}).")
                continue

        state, obs = engine.step(state, selected_action_id)
        if obs.success:
            state_history.append(state)
        page = 0  # Reset page on state transition

        if obs.is_terminal:
            final_quest = engine.get_quest_progress(state)
            render_ui(obs, page=page, page_size=page_size, state=state, quest_info=final_quest)
            print(f"\n*** OUTCOME REACHED: {obs.outcome or 'JOURNEY CONCLUDED'} ***\n")
            break


if __name__ == "__main__":
    main()
