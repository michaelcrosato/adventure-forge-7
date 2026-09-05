"""Closed Effect DSL Evaluator.

Applies deterministic state transformations to CharacterSheet and world flags.
"""
from typing import Dict, Any, List, Tuple, Optional
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.hazards import resolve_hazard_combo, get_hazard_combo, HazardCombo


def apply_effects(
    effects: List[Dict[str, Any]],
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> Tuple[CharacterSheet, Dict[str, Any], List[str], str]:
    """Apply a list of declarative effects to the character and world flags.
    
    Returns:
        (new_character, new_world_flags, emitted_events, next_scene_override)
    """
    if not effects:
        return character, world_flags, [], ""
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
            elif op == "apply_status":
                if isinstance(operand, dict):
                    status = str(operand.get("status", "")).lower().strip()
                    target = operand.get("target")
                else:
                    status = str(operand).lower().strip()
                    target = None

                # Update character markers
                if target in ("character", None):
                    if not new_char.has_marker(status):
                        m = list(new_char.markers) + [status]
                        new_char = new_char.modify(markers=m)

                # Update world flags
                new_flags[f"status_{status}"] = True
                curr_statuses = list(new_flags.get("statuses", []))
                if status not in curr_statuses:
                    curr_statuses.append(status)
                    new_flags["statuses"] = curr_statuses

                # Apply systemic combo effects if known
                status_combo = get_hazard_combo(status)
                if status_combo:
                    for flag_key, flag_val in status_combo.systemic_flags.items():
                        new_flags[flag_key] = flag_val
                    if status_combo.stamina_cost > 0 and target != "world":
                        stam = max(0, new_char.stamina - status_combo.stamina_cost)
                        new_char = new_char.modify(stamina=stam)
                    events.append(status_combo.description)
                else:
                    events.append(f"Applied status: {status}.")
            elif op == "trigger_hazard":
                hazard_combo: Optional[HazardCombo] = None
                hazard_key = ""
                if isinstance(operand, dict):
                    if "combo" in operand:
                        hazard_key = str(operand["combo"])
                        hazard_combo = get_hazard_combo(hazard_key)
                    elif "hazard" in operand:
                        h = str(operand["hazard"])
                        hazard_key = h
                        c = operand.get("catalyst")
                        if c:
                            hazard_combo = resolve_hazard_combo(h, str(c))
                        else:
                            hazard_combo = resolve_hazard_combo(h)
                else:
                    hazard_key = str(operand)
                    hazard_combo = resolve_hazard_combo(hazard_key) or get_hazard_combo(hazard_key)

                if hazard_combo:
                    s = hazard_combo.resulting_status
                    if not new_char.has_marker(s):
                        m = list(new_char.markers) + [s]
                        new_char = new_char.modify(markers=m)
                    new_flags[f"status_{s}"] = True
                    curr_statuses = list(new_flags.get("statuses", []))
                    if s not in curr_statuses:
                        curr_statuses.append(s)
                        new_flags["statuses"] = curr_statuses

                    for flag_key, flag_val in hazard_combo.systemic_flags.items():
                        new_flags[flag_key] = flag_val

                    if hazard_combo.stamina_cost > 0:
                        stam = max(0, new_char.stamina - hazard_combo.stamina_cost)
                        new_char = new_char.modify(stamina=stam)

                    for clr in hazard_combo.cleared_hazards:
                        new_flags[f"hazard_{clr}_cleared"] = True
                        if f"hazard_{clr}" in new_flags:
                            new_flags[f"hazard_{clr}"] = False

                    events.append(hazard_combo.description)
                else:
                    new_flags[f"hazard_{hazard_key}"] = True
                    events.append(f"Hazard triggered: {hazard_key}.")
            else:
                raise ValueError(f"Unknown effect operator: {op}")

    return new_char, new_flags, events, next_scene
