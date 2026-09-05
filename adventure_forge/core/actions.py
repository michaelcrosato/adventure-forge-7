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
        if self.condition is None:
            return True
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

        # Scavengeable systemic affordance
        if "scavengeable" in e_tags and e_state != "scavenged":
            act_id = f"scavenge_{e_id}"
            if act_id not in seen_ids:
                words = e_name.split()
                short_target = words[0] if len(words) > 2 else e_name
                legal_actions.append(Action(
                    id=act_id,
                    label=f"Scavenge {short_target}",
                    category="systemic",
                    effects=[
                        {"set_flag": {"flag": f"entity_{e_id}_state", "value": "scavenged"}},
                        {"log_event": f"You searched the {e_name}."}
                    ],
                    result_text="You search through the debris and find useful salvage.",
                    risk="low"
                ))
                seen_ids.add(act_id)

        # Submersible systemic affordance
        if "submersible" in e_tags:
            if character.has_item("waterproof_seal") or character.has_trait("water_breather") or character.get_attribute("endurance") >= 12:
                act_id = f"dive_{e_id}"
                target_dest = entity.get("submerge_destination")
                if act_id not in seen_ids:
                    words = e_name.split()
                    short_target = words[0] if len(words) > 2 else e_name
                    legal_actions.append(Action(
                        id=act_id,
                        label=f"Board {short_target}",
                        category="systemic",
                        target_scene=target_dest,
                        effects=[
                            {"log_event": f"You boarded the {e_name}."}
                        ],
                        result_text="The craft seals tight as you plunge into water.",
                        risk="medium",
                        stamina_cost=1
                    ))
                    seen_ids.add(act_id)

        # Oily systemic affordance
        if "oily" in e_tags and e_state != "burned":
            words = e_name.split()
            short_target = words[-1] if len(words) > 2 else e_name
            has_fire = (
                character.has_item("torch")
                or character.has_item("flint")
                or character.has_trait("pyromaniac")
                or character.has_item("fire_striker")
                or character.has_item("match")
                or character.has_item("fire_flask")
                or bool(world_flags.get("has_fire"))
                or bool(world_flags.get("fire_source"))
            )
            if has_fire:
                act_id = f"ignite_{e_id}"
                if act_id not in seen_ids:
                    legal_actions.append(Action(
                        id=act_id,
                        label=f"Ignite {short_target}",
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": f"entity_{e_id}_state", "value": "burned"}},
                            {"trigger_hazard": {"hazard": "oil", "catalyst": "fire"}},
                            {"log_event": f"You ignited the {e_name}."}
                        ],
                        result_text="Flames roar across the oil and incinerate all barriers.",
                        risk="high"
                    ))
                    seen_ids.add(act_id)
            else:
                act_id = f"examine_{e_id}"
                if act_id not in seen_ids:
                    legal_actions.append(Action(
                        id=act_id,
                        label=f"Examine {short_target}",
                        category="systemic",
                        effects=[
                            {"log_event": f"You examined the {e_name}."}
                        ],
                        result_text="Thick oil coats the stone floor in dark flammable streaks.",
                        risk="low"
                    ))
                    seen_ids.add(act_id)

        # Conductive water systemic affordance
        if "conductive_water" in e_tags and e_state != "electrified":
            words = e_name.split()
            short_target = words[-1] if len(words) > 2 else e_name
            has_shock = (
                character.has_item("shock_stone")
                or character.has_item("lightning_rod")
                or character.has_item("shock_bomb")
                or character.has_item("shock_scroll")
                or character.has_trait("storm_caller")
                or character.has_trait("galvanic")
                or character.get_skill("channeling") >= 2
                or bool(world_flags.get("has_shock"))
            )
            if has_shock:
                act_id = f"shock_{e_id}"
                if act_id not in seen_ids:
                    legal_actions.append(Action(
                        id=act_id,
                        label=f"Shock {short_target}",
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": f"entity_{e_id}_state", "value": "electrified"}},
                            {"trigger_hazard": {"hazard": "conductive_water", "catalyst": "shock"}},
                            {"log_event": f"You discharged shock into the {e_name}."}
                        ],
                        result_text="Sparks leap through the water. Sentries freeze as stamina drains.",
                        risk="high",
                        stamina_cost=2
                    ))
                    seen_ids.add(act_id)
            else:
                act_id = f"wade_{e_id}"
                if act_id not in seen_ids:
                    legal_actions.append(Action(
                        id=act_id,
                        label=f"Wade {short_target}",
                        category="systemic",
                        effects=[
                            {"log_event": f"You waded through the {e_name}."}
                        ],
                        result_text="Cold water swirls around your boots as you push forward.",
                        risk="low",
                        stamina_cost=1
                    ))
                    seen_ids.add(act_id)

        # Sandstorm systemic affordance
        if "sandstorm" in e_tags and e_state != "cleared":
            words = e_name.split()
            short_target = words[-1] if len(words) > 2 else e_name
            act_id = f"brave_{e_id}"
            if act_id not in seen_ids:
                has_cloak = character.has_item("cloak") or character.has_trait("heat_tolerant")
                legal_actions.append(Action(
                    id=act_id,
                    label=f"Brave {short_target}",
                    category="systemic",
                    effects=[
                        {"trigger_hazard": "sandstorm"},
                        {"log_event": f"You stepped into the {e_name}."}
                    ],
                    result_text="Swirling sand veils your silhouette and masks your movement.",
                    risk="low" if has_cloak else "medium",
                    stamina_cost=0 if has_cloak else 1
                ))
                seen_ids.add(act_id)

        # Acid pool systemic affordance
        if "acid_pool" in e_tags and e_state != "depleted":
            words = e_name.split()
            short_target = words[-1] if len(words) > 2 else e_name
            act_id = f"corrode_{e_id}"
            if act_id not in seen_ids:
                legal_actions.append(Action(
                    id=act_id,
                    label=f"Apply {short_target}",
                    category="systemic",
                    effects=[
                        {"set_flag": {"flag": f"entity_{e_id}_state", "value": "depleted"}},
                        {"trigger_hazard": "acid"},
                        {"log_event": f"You applied acid from the {e_name}."}
                    ],
                    result_text="Fuming acid dissolves iron bars and heavy metal locks.",
                    risk="medium",
                    stamina_cost=1
                ))
                seen_ids.add(act_id)

            has_container = (
                character.has_item("empty_flask")
                or character.has_item("vial")
                or character.has_item("flask")
            )
            if has_container:
                bottle_act_id = f"bottle_{e_id}"
                if bottle_act_id not in seen_ids:
                    container = "vial" if character.has_item("vial") else (
                        "empty_flask" if character.has_item("empty_flask") else "flask"
                    )
                    legal_actions.append(Action(
                        id=bottle_act_id,
                        label=f"Bottle {short_target}",
                        category="item_affordance",
                        effects=[
                            {"remove_item": container},
                            {"add_item": "acid_vial"},
                            {"log_event": f"You bottled acid from the {e_name}."}
                        ],
                        result_text="Green acid fills the glass vial and seals tight.",
                        risk="low"
                    ))
                    seen_ids.add(bottle_act_id)

    return legal_actions
