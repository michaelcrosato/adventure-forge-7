"""Action definitions and dynamic affordance synthesis.

Supports unbounded action possibility spaces (2 to 200+ actions).
Choices = Base Actions ∪ Inventory Affordances ∪ Trait Exploits ∪ Environmental Systemics.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Set
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.conditions import evaluate_condition
from adventure_forge.core.hazards import (
    get_regional_atmosphere,
    REGIONAL_ATMOSPHERES,
    REGION_TO_ATMOSPHERE,
)
from adventure_forge.core.stances import (
    TACTICAL_STANCES,
    ALL_STANCE_MARKERS,
)
from adventure_forge.core.crafting import CRAFTING_RECIPES
from adventure_forge.core.calamities import get_active_calamity
from adventure_forge.core.codex import get_codex_entries_for_scene
from adventure_forge.core.transit import get_transit_routes_for_scene
from adventure_forge.core.trade import get_trade_affordances_for_scene
from adventure_forge.core.weather import get_weather_affordance_for_scene
from adventure_forge.core.bounties import get_bounty_affordances_for_scene
from adventure_forge.core.companions import get_companion_affordances_for_scene
from adventure_forge.core.bestiary import get_bestiary_affordances_for_scene
from adventure_forge.core.survival import get_survival_affordances_for_scene
from adventure_forge.core.heraldry import get_heraldry_affordances_for_scene
from adventure_forge.core.shrines import get_shrine_affordances_for_scene


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
    world_flags: Dict[str, Any],
    region_id: Optional[str] = None,
    scene_id: Optional[str] = None,
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

    # 3. Regional Weather & Environmental Atmosphere System
    active_atmo_ids: Set[str] = set()

    # Determine region from argument or world flags
    effective_region = (
        region_id
        or world_flags.get("current_region")
        or world_flags.get("region_id")
        or world_flags.get("region")
    )
    if effective_region:
        reg_atmo = get_regional_atmosphere(str(effective_region), world_flags)
        if reg_atmo:
            active_atmo_ids.add(reg_atmo.id)

    # Check direct world flag atmospheric indicators
    for atmo_key in ("regional_atmosphere", "active_atmosphere", "atmosphere", "weather"):
        val = world_flags.get(atmo_key)
        if isinstance(val, str):
            clean_val = val.lower().strip()
            mapped = REGION_TO_ATMOSPHERE.get(clean_val, clean_val)
            if mapped in REGIONAL_ATMOSPHERES:
                if not (
                    world_flags.get(f"{mapped}_cleared") is True
                    or world_flags.get(f"{mapped}_suppressed") is True
                    or world_flags.get(f"hazard_{mapped}_cleared") is True
                    or world_flags.get(f"{mapped}_active") is False
                ):
                    active_atmo_ids.add(mapped)

    # Check entities for atmosphere tags or attributes
    for entity in scene_entities:
        e_tags = entity.get("tags", [])
        for tag in e_tags:
            clean_tag = str(tag).lower().strip()
            for prefix in ("atmosphere_", "weather_", "hazard_"):
                if clean_tag.startswith(prefix):
                    clean_tag = clean_tag[len(prefix):]
            mapped = REGION_TO_ATMOSPHERE.get(clean_tag, clean_tag)
            if mapped in REGIONAL_ATMOSPHERES:
                if not (
                    world_flags.get(f"{mapped}_cleared") is True
                    or world_flags.get(f"{mapped}_suppressed") is True
                    or world_flags.get(f"hazard_{mapped}_cleared") is True
                    or world_flags.get(f"{mapped}_active") is False
                ):
                    active_atmo_ids.add(mapped)
        ent_atmo = entity.get("atmosphere")
        if isinstance(ent_atmo, str):
            clean_ent_atmo = ent_atmo.lower().strip()
            mapped = REGION_TO_ATMOSPHERE.get(clean_ent_atmo, clean_ent_atmo)
            if mapped in REGIONAL_ATMOSPHERES:
                if not (
                    world_flags.get(f"{mapped}_cleared") is True
                    or world_flags.get(f"{mapped}_suppressed") is True
                    or world_flags.get(f"hazard_{mapped}_cleared") is True
                    or world_flags.get(f"{mapped}_active") is False
                ):
                    active_atmo_ids.add(mapped)

    # Synthesize systemic mitigation and exploitation actions for active atmospheres
    for atmo_id in sorted(active_atmo_ids):
        if atmo_id == "blizzard":
            # Mitigation: Seek Shelter (rewards climbing_rope)
            act_id = "seek_shelter"
            if act_id not in seen_ids:
                has_rope = character.has_item("climbing_rope")
                if has_rope:
                    shelter_act = Action(
                        id=act_id,
                        label="Seek Shelter",
                        category="item_affordance",
                        effects=[
                            {"set_flag": {"flag": "blizzard_sheltered", "value": True}},
                            {"log_event": "You used your climbing rope to anchor safe shelter from the blizzard."},
                        ],
                        result_text="You secure your climbing rope to the rock face and duck into a sheltered crevice.",
                        risk="low",
                        stamina_cost=0,
                    )
                else:
                    shelter_act = Action(
                        id=act_id,
                        label="Seek Shelter",
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": "blizzard_sheltered", "value": True}},
                            {"log_event": "You found rough shelter from the biting blizzard."},
                        ],
                        result_text="You scramble into a shallow hollow in the stone and wait out the wind.",
                        risk="medium",
                        stamina_cost=1,
                    )
                if shelter_act.is_legal(character, world_flags):
                    legal_actions.append(shelter_act)
                    seen_ids.add(act_id)

            # Exploitation / Endurance: Brace Wind (checks nimble or stamina)
            act_id = "brace_wind"
            if act_id not in seen_ids:
                has_nimble = character.has_trait("nimble") or character.get_attribute("agility") >= 12
                if has_nimble:
                    brace_act = Action(
                        id=act_id,
                        label="Brace Wind",
                        category="trait_exploit",
                        effects=[
                            {"set_flag": {"flag": "blizzard_braced", "value": True}},
                            {"log_event": "You braced nimbly against the freezing gale."},
                        ],
                        result_text="You lean into the gale and maintain your footing with agile balance.",
                        risk="low",
                        stamina_cost=0,
                    )
                else:
                    brace_act = Action(
                        id=act_id,
                        label="Brace Wind",
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": "blizzard_braced", "value": True}},
                            {"log_event": "You braced your footing against the harsh blizzard."},
                        ],
                        result_text="You plant your boots firmly against the freezing wind and push forward.",
                        risk="medium",
                        stamina_cost=1,
                    )
                if brace_act.is_legal(character, world_flags):
                    legal_actions.append(brace_act)
                    seen_ids.add(act_id)

        elif atmo_id == "heatwave":
            # Mitigation: Drink Water (rewards water_skin)
            act_id = "drink_water"
            if act_id not in seen_ids:
                has_water = (
                    character.has_item("water_skin")
                    or character.has_item("waterskin")
                    or character.has_item("canteen")
                )
                if has_water:
                    drink_act = Action(
                        id=act_id,
                        label="Drink Water",
                        category="item_affordance",
                        effects=[
                            {"set_flag": {"flag": "heatwave_mitigated", "value": True}},
                            {"modify_stamina": 1},
                            {"log_event": "You drank cool water and overcame the searing heat."},
                        ],
                        result_text="Cool water from your skin revives your dry mouth and restores your strength.",
                        risk="low",
                        stamina_cost=0,
                    )
                else:
                    drink_act = Action(
                        id=act_id,
                        label="Drink Water",
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": "heatwave_mitigated", "value": True}},
                            {"log_event": "You endured the searing heatwave without clean water."},
                        ],
                        result_text="You scrape sparse moisture from canteen dregs to wet your parched throat.",
                        risk="medium",
                        stamina_cost=1,
                    )
                if drink_act.is_legal(character, world_flags):
                    legal_actions.append(drink_act)
                    seen_ids.add(act_id)

            # Exploitation: Rest Shade (checks heat_tolerant trait)
            act_id = "rest_shade"
            if act_id not in seen_ids:
                has_heat = (
                    character.has_trait("heat_tolerant")
                    or character.has_trait("desert_born")
                    or character.get_attribute("endurance") >= 12
                )
                if has_heat:
                    shade_act = Action(
                        id=act_id,
                        label="Rest Shade",
                        category="trait_exploit",
                        effects=[
                            {"set_flag": {"flag": "heatwave_rested", "value": True}},
                            {"log_event": "Your heat tolerance let you rest easy in the shade."},
                        ],
                        result_text="Used to the heat, you rest in the rock shade and save your strength.",
                        risk="low",
                        stamina_cost=0,
                    )
                else:
                    shade_act = Action(
                        id=act_id,
                        label="Rest Shade",
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": "heatwave_rested", "value": True}},
                            {"log_event": "You rested in the sparse shade against the heat."},
                        ],
                        result_text="You crouch under a dry ledge, but the sweltering heat still drains you.",
                        risk="medium",
                        stamina_cost=1,
                    )
                if shade_act.is_legal(character, world_flags):
                    legal_actions.append(shade_act)
                    seen_ids.add(act_id)

        elif atmo_id == "bioluminescence":
            # Mitigation / Inspection: Inspect Glow
            act_id = "inspect_glow"
            if act_id not in seen_ids:
                inspect_act = Action(
                    id=act_id,
                    label="Inspect Glow",
                    category="systemic",
                    effects=[
                        {"set_flag": {"flag": "bioluminescence_inspected", "value": True}},
                        {"log_event": "You inspected the glowing cave moss."},
                    ],
                    result_text="Soft green light from radiant moss illuminates the wet cavern walls.",
                    risk="low",
                    stamina_cost=0,
                )
                if inspect_act.is_legal(character, world_flags):
                    legal_actions.append(inspect_act)
                    seen_ids.add(act_id)

            # Exploitation: Decipher Runes (reveals glowing runes for water_breather or night_eyed)
            act_id = "decipher_runes"
            if act_id not in seen_ids:
                has_rune_trait = (
                    character.has_trait("water_breather")
                    or character.has_trait("night_eyed")
                    or character.get_skill("cunning") >= 3
                )
                if has_rune_trait:
                    runes_act = Action(
                        id=act_id,
                        label="Decipher Runes",
                        category="trait_exploit",
                        effects=[
                            {"set_flag": {"flag": "glowing_runes_deciphered", "value": True}},
                            {"set_flag": {"flag": "abyssal_lore_known", "value": True}},
                            {"log_event": "Your keen sight deciphered the glowing runes."},
                        ],
                        result_text="Your keen sight spots the glowing runes under the cold water.",
                        risk="low",
                        stamina_cost=0,
                    )
                else:
                    runes_act = Action(
                        id=act_id,
                        label="Decipher Runes",
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": "glowing_runes_deciphered", "value": False}},
                            {"log_event": "You tried to read the faint runes in the glow."},
                        ],
                        result_text="You squint at faint symbols underwater but struggle to read them clearly.",
                        risk="medium",
                        stamina_cost=1,
                    )
                if runes_act.is_legal(character, world_flags):
                    legal_actions.append(runes_act)
                    seen_ids.add(act_id)

        elif atmo_id == "miasma":
            # Mitigation: Filter Air (checked by masks)
            act_id = "filter_air"
            if act_id not in seen_ids:
                has_mask = (
                    character.has_item("mask")
                    or character.has_item("cloth_mask")
                    or character.has_item("filter_mask")
                    or character.has_item("plague_mask")
                )
                if has_mask:
                    filter_act = Action(
                        id=act_id,
                        label="Filter Air",
                        category="item_affordance",
                        effects=[
                            {"set_flag": {"flag": "miasma_filtered", "value": True}},
                            {"log_event": "You filtered the bad sewer air with your mask."},
                        ],
                        result_text="You pull your protective mask tight and breathe clean filtered air.",
                        risk="low",
                        stamina_cost=0,
                    )
                else:
                    filter_act = Action(
                        id=act_id,
                        label="Filter Air",
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": "miasma_filtered", "value": True}},
                            {"log_event": "You covered your face to filter the bad air."},
                        ],
                        result_text="You press a damp sleeve over your mouth to block the stench.",
                        risk="medium",
                        stamina_cost=1,
                    )
                if filter_act.is_legal(character, world_flags):
                    legal_actions.append(filter_act)
                    seen_ids.add(act_id)

            # Exploitation / Resistance: Endure Fumes (checked by iron_gutted trait)
            act_id = "endure_fumes"
            if act_id not in seen_ids:
                has_iron = (
                    character.has_trait("iron_gutted")
                    or character.get_attribute("endurance") >= 14
                )
                if has_iron:
                    endure_act = Action(
                        id=act_id,
                        label="Endure Fumes",
                        category="trait_exploit",
                        effects=[
                            {"set_flag": {"flag": "miasma_endured", "value": True}},
                            {"log_event": "Your iron gut shrugged off the bad fumes."},
                        ],
                        result_text="Your iron gut fights off the bad sewer air without sickness.",
                        risk="low",
                        stamina_cost=0,
                    )
                else:
                    endure_act = Action(
                        id=act_id,
                        label="Endure Fumes",
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": "miasma_endured", "value": True}},
                            {"log_event": "You coughed while enduring the thick fumes."},
                        ],
                        result_text="You cough violently as the acrid sewer vapor burns your throat.",
                        risk="high",
                        stamina_cost=2,
                    )
                if endure_act.is_legal(character, world_flags):
                    legal_actions.append(endure_act)
                    seen_ids.add(act_id)

        elif atmo_id == "curfew":
            # Mitigation: Show Pass (checked by watch_crest)
            act_id = "show_pass"
            if act_id not in seen_ids:
                has_crest = (
                    character.has_item("watch_crest")
                    or character.has_marker("watch_crest")
                    or character.has_item("court_pass")
                    or character.has_item("legal_dossier")
                )
                if has_crest:
                    pass_act = Action(
                        id=act_id,
                        label="Show Pass",
                        category="item_affordance",
                        effects=[
                            {"set_flag": {"flag": "curfew_cleared", "value": True}},
                            {"log_event": "You flashed the watch crest to pass the curfew."},
                        ],
                        result_text="You display the watch crest. The sentries nod and let you pass.",
                        risk="low",
                        stamina_cost=0,
                    )
                else:
                    pass_act = Action(
                        id=act_id,
                        label="Show Pass",
                        category="social",
                        effects=[
                            {"set_flag": {"flag": "curfew_confronted", "value": True}},
                            {"log_event": "You talked your way past the watch patrol."},
                        ],
                        result_text="You give a quick excuse. The watchmen eye you but let you through.",
                        risk="high",
                        stamina_cost=1,
                    )
                if pass_act.is_legal(character, world_flags):
                    legal_actions.append(pass_act)
                    seen_ids.add(act_id)

            # Exploitation: Slip Shadows (checked by stealth)
            act_id = "slip_shadows"
            if act_id not in seen_ids:
                has_stealth = (
                    character.get_skill("stealth") >= 2
                    or character.has_trait("shadow_cloaked")
                    or character.has_trait("streetwise")
                    or character.get_attribute("agility") >= 12
                )
                if has_stealth:
                    slip_act = Action(
                        id=act_id,
                        label="Slip Shadows",
                        category="trait_exploit",
                        effects=[
                            {"set_flag": {"flag": "curfew_bypassed", "value": True}},
                            {"log_event": "You slipped through shadows past the watch patrol."},
                        ],
                        result_text="You glide between street shadows and bypass the watch patrol undetected.",
                        risk="low",
                        stamina_cost=0,
                    )
                else:
                    slip_act = Action(
                        id=act_id,
                        label="Slip Shadows",
                        category="systemic",
                        effects=[
                            {"set_flag": {"flag": "curfew_bypassed", "value": True}},
                            {"log_event": "You ducked into shadows to avoid the sentries."},
                        ],
                        result_text="You dart behind stone pillars, narrowly evading the sweep of sentry torches.",
                        risk="medium",
                        stamina_cost=1,
                    )
                if slip_act.is_legal(character, world_flags):
                    legal_actions.append(slip_act)
                    seen_ids.add(act_id)

    # 4. Tactical Combat Stances & Systemic Exploits (Milestone 16)
    should_synthesize_stances = (
        any(character.has_marker(m) for m in ALL_STANCE_MARKERS)
        or bool(world_flags.get("stances_enabled"))
        or bool(world_flags.get("tactical_mode"))
        or bool(world_flags.get("in_combat"))
        or (
            effective_region is not None
            and str(effective_region) != "stress_market"
            and (len(base_actions) > 0 or len(scene_entities) > 0)
        )
    )

    if should_synthesize_stances:
        # Identify active stance marker
        active_stance_id: Optional[str] = None
        for s_id, stance in TACTICAL_STANCES.items():
            if character.has_marker(stance.marker):
                active_stance_id = s_id
                break

        # Active stance exploit and drop stance affordance
        if active_stance_id and active_stance_id in TACTICAL_STANCES:
            active_stance = TACTICAL_STANCES[active_stance_id]
            if active_stance.exploit_action_id not in seen_ids:
                exploit_act = Action(
                    id=active_stance.exploit_action_id,
                    label=active_stance.exploit_label,
                    category=active_stance.exploit_category,
                    effects=list(active_stance.exploit_effects),
                    result_text=active_stance.exploit_result_text,
                    risk="low",
                    stamina_cost=active_stance.exploit_stamina_cost,
                )
                if exploit_act.is_legal(character, world_flags):
                    legal_actions.append(exploit_act)
                    seen_ids.add(active_stance.exploit_action_id)

            neutral_act_id = "stance_neutral"
            if neutral_act_id not in seen_ids:
                drop_act = Action(
                    id=neutral_act_id,
                    label="Drop Stance",
                    category="tactical",
                    effects=[
                        {"remove_marker": "stance_aggressive"},
                        {"remove_marker": "stance_defensive"},
                        {"remove_marker": "stance_elusive"},
                        {"remove_marker": "stance_focused"},
                        {"set_flag": {"flag": "active_stance", "value": ""}},
                        {"log_event": "You dropped your tactical stance."},
                    ],
                    result_text="You relax your muscles and return to a neutral posture.",
                    risk="low",
                    stamina_cost=0,
                )
                if drop_act.is_legal(character, world_flags):
                    legal_actions.append(drop_act)
                    seen_ids.add(neutral_act_id)

        # Shift actions for stances not currently active
        for s_id, stance in TACTICAL_STANCES.items():
            if s_id != active_stance_id and stance.is_available(character, world_flags):
                if stance.shift_action_id not in seen_ids:
                    shift_act = Action(
                        id=stance.shift_action_id,
                        label=stance.shift_label,
                        category=stance.category,
                        effects=list(stance.shift_effects),
                        result_text=stance.shift_result_text,
                        risk="low",
                        stamina_cost=stance.stamina_cost,
                    )
                    if shift_act.is_legal(character, world_flags):
                        legal_actions.append(shift_act)
                        seen_ids.add(stance.shift_action_id)

    # 5. Master Field Crafting & Alchemical Synthesis (Milestone 17)
    if len(base_actions) > 0 or len(scene_entities) > 0 or bool(world_flags.get("crafting_enabled")):
        for recipe in CRAFTING_RECIPES.values():
            if recipe.action_id not in seen_ids and recipe.is_available(character, world_flags):
                craft_act = Action(
                    id=recipe.action_id,
                    label=recipe.label,
                    category=recipe.category,
                    effects=recipe.build_effects(),
                    result_text=recipe.result_text,
                    risk="low",
                    stamina_cost=recipe.stamina_cost,
                )
                if craft_act.is_legal(character, world_flags):
                    legal_actions.append(craft_act)
                    seen_ids.add(recipe.action_id)

    # 6. Continental Dynamic Calamities & Incursion Events (Milestone 18)
    if effective_region and str(effective_region) != "stress_market":
        turn_count = int(world_flags.get("turn_count", 0))
        active_calamity = get_active_calamity(turn_count, str(effective_region), world_flags)
        if active_calamity:
            for mit in active_calamity.mitigations:
                if mit.action_id not in seen_ids and mit.is_legal(character, world_flags):
                    calamity_act = Action(
                        id=mit.action_id,
                        label=mit.label,
                        category=mit.category,
                        effects=list(mit.effects),
                        result_text=mit.result_text,
                        risk=mit.risk,
                        stamina_cost=mit.stamina_cost,
                    )
                    legal_actions.append(calamity_act)
                    seen_ids.add(mit.action_id)

    # 7. Ancient Lore Codex & Relic Inscription Affordances (Milestone 19)
    effective_scene_id = scene_id or str(world_flags.get("current_scene", ""))
    if effective_scene_id:
        codex_entries = get_codex_entries_for_scene(effective_scene_id)
        for entry in codex_entries:
            if entry.action_id not in seen_ids and entry.is_available(character, world_flags):
                codex_act = Action(
                    id=entry.action_id,
                    label=entry.action_label,
                    category="codex",
                    effects=entry.build_effects(world_flags),
                    result_text=entry.discovery_text,
                    risk="low",
                    stamina_cost=entry.stamina_cost,
                )
                legal_actions.append(codex_act)
                seen_ids.add(entry.action_id)

    # 8. Continental Chartered Transit & Fast-Travel Network (Milestone 20)
    if effective_scene_id:
        transit_routes = get_transit_routes_for_scene(effective_scene_id)
        for route in transit_routes:
            if route.action_id not in seen_ids and route.is_available(character, world_flags):
                transit_act = Action(
                    id=route.action_id,
                    label=route.action_label,
                    category=route.category,
                    effects=route.build_effects(world_flags),
                    target_scene=route.destination_scene,
                    result_text=route.result_text,
                    risk="low",
                    stamina_cost=route.stamina_cost,
                )
                legal_actions.append(transit_act)
                seen_ids.add(route.action_id)

    # 9. Continental Trade Economy & Regional Commodity Exchange (Milestone 21)
    if effective_scene_id:
        trade_actions = get_trade_affordances_for_scene(effective_scene_id, character, world_flags)
        for trade_act in trade_actions:
            if trade_act.id not in seen_ids and trade_act.is_legal(character, world_flags):
                legal_actions.append(trade_act)
                seen_ids.add(trade_act.id)

    # 10. Continental Weather Dynamics & Provincial Micro-Climates (Milestone 22)
    if effective_scene_id:
        turn_count = int(world_flags.get("turn_count", 0))
        weather_act = get_weather_affordance_for_scene(
            effective_scene_id,
            str(effective_region or "stress_market"),
            turn_count,
            character,
            world_flags,
        )
        if weather_act and weather_act.id not in seen_ids:
            legal_actions.append(weather_act)
            seen_ids.add(weather_act.id)

    # 11. Continental Mercenary Contract Board & Faction Bounties (Milestone 23)
    if effective_scene_id:
        bounty_actions = get_bounty_affordances_for_scene(effective_scene_id, character, world_flags)
        for bounty_act in bounty_actions:
            if bounty_act.id not in seen_ids and bounty_act.is_legal(character, world_flags):
                legal_actions.append(bounty_act)
                seen_ids.add(bounty_act.id)

    # 12. Continental Companion Recruiter & Follower Synergy System (Milestone 24)
    if effective_scene_id:
        comp_actions = get_companion_affordances_for_scene(effective_scene_id, character, world_flags)
        for comp_act in comp_actions:
            if comp_act.id not in seen_ids and comp_act.is_legal(character, world_flags):
                legal_actions.append(comp_act)
                seen_ids.add(comp_act.id)

    # 13. Continental Bestiary & Apex Trophy Hunting System (Milestone 25)
    if effective_scene_id:
        bestiary_actions = get_bestiary_affordances_for_scene(effective_scene_id, character, world_flags)
        for bestiary_act in bestiary_actions:
            if bestiary_act.id not in seen_ids and bestiary_act.is_legal(character, world_flags):
                legal_actions.append(bestiary_act)
                seen_ids.add(bestiary_act.id)

    # 14. Continental Survival Camping, Wilderness Foraging & Field Rations System (Milestone 26)
    if effective_scene_id:
        survival_actions = get_survival_affordances_for_scene(effective_scene_id, character, world_flags)
        for surv_act in survival_actions:
            if surv_act.id not in seen_ids and surv_act.is_legal(character, world_flags):
                legal_actions.append(surv_act)
                seen_ids.add(surv_act.id)

    # 15. Provincial Faction Heraldry, Renown Orders & Continental War Banners (Milestone 27)
    if effective_scene_id:
        heraldry_actions = get_heraldry_affordances_for_scene(effective_scene_id, character, world_flags)
        for h_act in heraldry_actions:
            if h_act.id not in seen_ids and h_act.is_legal(character, world_flags):
                legal_actions.append(h_act)
                seen_ids.add(h_act.id)

    # 16. Continental Ancient Shrines, Relic Offerings & Divine Blessings (Milestone 28)
    if effective_scene_id:
        shrine_actions = get_shrine_affordances_for_scene(effective_scene_id, character, world_flags)
        for sh_act in shrine_actions:
            if sh_act.id not in seen_ids and sh_act.is_legal(character, world_flags):
                legal_actions.append(sh_act)
                seen_ids.add(sh_act.id)

    return legal_actions
