"""Action definitions and dynamic affordance synthesis.

Supports unbounded action possibility spaces (2 to 200+ actions).
Choices = Base Actions ∪ Inventory Affordances ∪ Trait Exploits ∪ Environmental Systemics.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.conditions import evaluate_condition


@dataclass(frozen=True)
class Action:
    """An engine-enumerated legal action with stable identity."""
    id: str
    label: str  # 1-3 words
    category: str  # movement, interaction, social, trait_exploit, systemic, item_affordance
    condition: Optional[Dict[str, Any]] = None
    effects: List[Dict[str, Any]] = field(default_factory=list)
    target_scene: Optional[str] = None
    result_text: str = ""
    risk: str = "low"  # low, medium, high
    stamina_cost: int = 0

    def is_legal(self, character: CharacterSheet, world_flags: Dict[str, Any]) -> bool:
        if character.stamina < self.stamina_cost:
            return False
        return evaluate_condition(self.condition, character, world_flags)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "category": self.category,
            "condition": self.condition,
            "effects": list(self.effects),
            "target_scene": self.target_scene,
            "result_text": self.result_text,
            "risk": self.risk,
            "stamina_cost": self.stamina_cost,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Action":
        return cls(
            id=data["id"],
            label=data["label"],
            category=data.get("category", "interaction"),
            condition=data.get("condition"),
            effects=list(data.get("effects", [])),
            target_scene=data.get("target_scene"),
            result_text=data.get("result_text", ""),
            risk=data.get("risk", "low"),
            stamina_cost=int(data.get("stamina_cost", 0)),
        )


def synthesize_affordances(
    base_actions: List[Action],
    scene_entities: List[Dict[str, Any]],
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> List[Action]:
    """Synthesize all available actions for a scene according to the affordance equation.
    
    Choices = Base Actions ∪ Inventory Affordances ∪ Trait Exploits ∪ Environmental Systemics.
    All legal actions are enumerated without arbitrary ceiling.
    """
    legal_actions: List[Action] = []
    seen_ids = set()

    # 1. Base scene actions (filtered by legality)
    for act in base_actions:
        if act.id not in seen_ids and act.is_legal(character, world_flags):
            legal_actions.append(act)
            seen_ids.add(act.id)

    # 2. Environmental entities and systemics
    for entity in scene_entities:
        e_id = entity.get("id", "entity")
        e_name = entity.get("name", e_id)
        e_tags = entity.get("tags", [])
        e_state = world_flags.get(f"entity_{e_id}_state", entity.get("initial_state", "intact"))

        if e_state == "destroyed" or e_state == "unusable":
            continue

        # Systemic verbs based on tags
        if "lockable" in e_tags and e_state == "locked":
            # Pick lock affordance (requires lockpicks or cunning)
            if character.has_item("lockpick") or character.get_skill("cunning") >= 3:
                act_id = f"pick_{e_id}"
                if act_id not in seen_ids:
                    legal_actions.append(Action(
                        id=act_id,
                        label=f"Pick {e_name}",
                        category="item_affordance" if character.has_item("lockpick") else "trait_exploit",
                        effects=[
                            {"set_flag": {"flag": f"entity_{e_id}_state", "value": "unlocked"}},
                            {"log_event": f"You picked open the {e_name}."}
                        ],
                        result_text="The lock tumblers click open.",
                        risk="medium"
                    ))
                    seen_ids.add(act_id)

            # Force lock affordance (requires high strength or crowbar)
            if character.has_item("crowbar") or character.get_attribute("strength") >= 14:
                act_id = f"force_{e_id}"
                if act_id not in seen_ids:
                    legal_actions.append(Action(
                        id=act_id,
                        label=f"Force {e_name}",
                        category="item_affordance" if character.has_item("crowbar") else "systemic",
                        effects=[
                            {"set_flag": {"flag": f"entity_{e_id}_state", "value": "broken"}},
                            {"log_event": f"You forced open the {e_name} with raw leverage."}
                        ],
                        result_text="The iron brackets buckle with a loud crack.",
                        risk="high",
                        stamina_cost=2
                    ))
                    seen_ids.add(act_id)

            # Melt lock affordance (requires acid vial or pyromaniac)
            if character.has_item("acid_vial") or character.has_trait("pyromaniac"):
                act_id = f"melt_{e_id}"
                if act_id not in seen_ids:
                    legal_actions.append(Action(
                        id=act_id,
                        label=f"Melt {e_name}",
                        category="trait_exploit" if character.has_trait("pyromaniac") else "item_affordance",
                        effects=[
                            {"set_flag": {"flag": f"entity_{e_id}_state", "value": "melted"}},
                            {"log_event": f"Chemical acid dissolves the latch of the {e_name}."}
                        ],
                        result_text="Acid hisses and eats through the latch.",
                        risk="low"
                    ))
                    seen_ids.add(act_id)

        # Flammable systemic affordance
        if "flammable" in e_tags and e_state != "burned":
            if character.has_item("torch") or character.has_trait("pyromaniac") or character.has_item("flint"):
                act_id = f"burn_{e_id}"
                if act_id not in seen_ids:
                    legal_actions.append(Action(
                        id=act_id,
                        label=f"Burn {e_name}",
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": f"entity_{e_id}_state", "value": "burned"}},
                            {"set_flag": {"flag": f"hazard_{e_id}_smoke", "value": True}},
                            {"log_event": f"You ignited the {e_name}."}
                        ],
                        result_text="Flames catch and spread quickly.",
                        risk="high"
                    ))
                    seen_ids.add(act_id)

        # Climbable systemic affordance
        if "climbable" in e_tags:
            if character.has_item("climbing_rope") or character.get_attribute("agility") >= 12 or character.has_trait("nimble"):
                act_id = f"climb_{e_id}"
                target_dest = entity.get("climb_destination")
                if act_id not in seen_ids:
                    legal_actions.append(Action(
                        id=act_id,
                        label=f"Scale {e_name}",
                        category="systemic",
                        target_scene=target_dest,
                        effects=[
                            {"log_event": f"You scaled the {e_name} to the upper ridge."}
                        ],
                        result_text="You find purchase on stone holds and haul yourself up.",
                        stamina_cost=1
                    ))
                    seen_ids.add(act_id)

    return legal_actions
