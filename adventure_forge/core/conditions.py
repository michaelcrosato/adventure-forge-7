"""Closed Condition DSL Evaluator.

Enforces deterministic condition validation over character state, world flags,
and environment context. No free-form runtime guessing.
"""
from typing import Dict, Any, List, Union
from adventure_forge.core.character import CharacterSheet


def evaluate_condition(condition: Union[Dict[str, Any], List[Any], None], character: CharacterSheet, world_flags: Dict[str, Any]) -> bool:
    """Evaluate a declarative condition tree against character and world state."""
    if condition is None:
        return True
    
    if isinstance(condition, list):
        return all(evaluate_condition(item, character, world_flags) for item in condition)
    
    if not isinstance(condition, dict):
        return False
    
    for op, operand in condition.items():
        if op == "all_of":
            if not all(evaluate_condition(c, character, world_flags) for c in operand):
                return False
        elif op == "any_of":
            if not any(evaluate_condition(c, character, world_flags) for c in operand):
                return False
        elif op == "none_of":
            if any(evaluate_condition(c, character, world_flags) for c in operand):
                return False
        elif op == "has_trait":
            if not character.has_trait(str(operand)):
                return False
        elif op == "has_flaw":
            if not character.has_flaw(str(operand)):
                return False
        elif op == "has_marker":
            if not character.has_marker(str(operand)):
                return False
        elif op == "has_item":
            if not character.has_item(str(operand)):
                return False
        elif op == "ancestry_is":
            if character.ancestry.lower() != str(operand).lower():
                return False
        elif op == "background_is":
            if character.background.lower() != str(operand).lower():
                return False
        elif op == "min_attribute":
            attr = operand.get("attribute", "").lower()
            target = int(operand.get("value", 0))
            if character.get_attribute(attr) < target:
                return False
        elif op == "min_skill":
            skill = operand.get("skill", "").lower()
            target = int(operand.get("value", 0))
            if character.get_skill(skill) < target:
                return False
        elif op == "min_reputation":
            faction = operand.get("faction", "").lower()
            target = int(operand.get("value", 0))
            if character.get_reputation(faction) < target:
                return False
        elif op == "max_reputation":
            faction = operand.get("faction", "").lower()
            target = int(operand.get("value", 0))
            if character.get_reputation(faction) > target:
                return False
        elif op == "flag_is":
            flag = operand.get("flag", "")
            target = operand.get("value")
            if world_flags.get(flag) != target:
                return False
        elif op == "min_flag":
            flag = operand.get("flag", "")
            target = operand.get("value", 0)
            if world_flags.get(flag, 0) < target:
                return False
        elif op == "has_flag":
            if str(operand) not in world_flags or not world_flags[str(operand)]:
                return False
        elif op == "lacks_flag":
            if world_flags.get(str(operand)):
                return False
        else:
            # Unknown operator rejected
            raise ValueError(f"Unknown condition operator: {op}")
    
    return True
