"""Closed Effect DSL Evaluator.

Applies deterministic state transformations to CharacterSheet and world flags.
"""
from typing import Dict, Any, List, Tuple
from adventure_forge.core.character import CharacterSheet


def apply_effects(
    effects: List[Dict[str, Any]],
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> Tuple[CharacterSheet, Dict[str, Any], List[str], str]:
    """Apply a list of declarative effects to the character and world flags.
    
    Returns:
        (new_character, new_world_flags, emitted_events, next_scene_override)
    """
    new_char = character
    new_flags = dict(world_flags)
    events: List[str] = []
    next_scene: str = ""

    for effect in effects:
        for op, operand in effect.items():
            if op == "set_flag":
                flag = operand["flag"]
                val = operand["value"]
                new_flags[flag] = val
                events.append(f"World flag updated: {flag} = {val}")
            elif op == "add_flag":
                flag = operand["flag"]
                delta = operand.get("value", 1)
                new_flags[flag] = new_flags.get(flag, 0) + delta
                events.append(f"World flag incremented: {flag} += {delta}")
            elif op == "add_item":
                item = str(operand)
                inv = list(new_char.inventory)
                inv.append(item)
                new_char = new_char.modify(inventory=inv)
                events.append(f"Acquired item: {item}")
            elif op == "remove_item":
                item = str(operand)
                inv = list(new_char.inventory)
                if item in inv:
                    inv.remove(item)
                new_char = new_char.modify(inventory=inv)
                events.append(f"Lost item: {item}")
            elif op == "modify_health":
                delta = int(operand)
                hp = max(0, min(new_char.max_health, new_char.health + delta))
                new_char = new_char.modify(health=hp)
                events.append(f"Health changed: {delta:+d} (now {hp})")
            elif op == "modify_stamina":
                delta = int(operand)
                stam = max(0, min(new_char.max_stamina, new_char.stamina + delta))
                new_char = new_char.modify(stamina=stam)
                events.append(f"Stamina changed: {delta:+d} (now {stam})")
            elif op == "modify_reputation":
                faction = operand["faction"].lower()
                delta = int(operand["value"])
                current = new_char.get_reputation(faction)
                new_rep = dict(new_char.reputation)
                new_rep[faction] = current + delta
                new_char = new_char.modify(reputation=new_rep)
                events.append(f"Reputation with {faction}: {delta:+d}")
            elif op == "add_trait":
                trait = str(operand)
                if not new_char.has_trait(trait):
                    t = list(new_char.traits) + [trait]
                    new_char = new_char.modify(traits=t)
                    events.append(f"Gained trait: {trait}")
            elif op == "remove_trait":
                trait = str(operand)
                t = [x for x in new_char.traits if x.lower() != trait.lower()]
                new_char = new_char.modify(traits=t)
                events.append(f"Lost trait: {trait}")
            elif op == "add_marker":
                marker = str(operand)
                if not new_char.has_marker(marker):
                    m = list(new_char.markers) + [marker]
                    new_char = new_char.modify(markers=m)
                    events.append(f"Gained marker: {marker}")
            elif op == "remove_marker":
                marker = str(operand)
                m = [x for x in new_char.markers if x.lower() != marker.lower()]
                new_char = new_char.modify(markers=m)
                events.append(f"Lost marker: {marker}")
            elif op == "change_scene":
                next_scene = str(operand)
            elif op == "log_event":
                events.append(str(operand))
            else:
                raise ValueError(f"Unknown effect operator: {op}")

    return new_char, new_flags, events, next_scene
