"""Pure Deterministic Environmental Hazards and Status Combos.

Defines environmental hazard combinations and resolves status reactions:
- Oil + Fire -> Conflagration
- Water + Shock -> Stun
- Sandstorm -> Obscured
- Acid -> Corrode
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Set, Union, Iterable
from adventure_forge.core.character import CharacterSheet


@dataclass(frozen=True)
class HazardCombo:
    """Deterministic hazard combination specification."""
    id: str
    name: str
    required_elements: Tuple[str, ...]
    resulting_status: str
    description: str
    systemic_flags: Dict[str, Any] = field(default_factory=dict)
    cleared_hazards: Tuple[str, ...] = ()
    stamina_cost: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "required_elements": list(self.required_elements),
            "resulting_status": self.resulting_status,
            "description": self.description,
            "systemic_flags": dict(self.systemic_flags),
            "cleared_hazards": list(self.cleared_hazards),
            "stamina_cost": self.stamina_cost,
        }


HAZARD_COMBOS: Dict[str, HazardCombo] = {
    "conflagration": HazardCombo(
        id="conflagration",
        name="Conflagration",
        required_elements=("fire", "oil"),
        resulting_status="conflagration",
        description="Intense flames incinerate the oil slick and clear flammable barriers.",
        systemic_flags={
            "oil_slick_incinerated": True,
            "flammable_barriers_cleared": True,
            "status_conflagration": True,
        },
        cleared_hazards=("oil", "oily"),
        stamina_cost=0,
    ),
    "stun": HazardCombo(
        id="stun",
        name="Stun",
        required_elements=("shock", "water"),
        resulting_status="stun",
        description="Electric arcs surge through water. The shock stuns sentries and drains stamina.",
        systemic_flags={
            "sentries_disabled": True,
            "sentry_active": False,
            "status_stun": True,
        },
        cleared_hazards=(),
        stamina_cost=2,
    ),
    "obscured": HazardCombo(
        id="obscured",
        name="Obscured",
        required_elements=("sandstorm",),
        resulting_status="obscured",
        description="Whirling grit shrouds your silhouette and enhances stealth.",
        systemic_flags={
            "silhouette_obscured": True,
            "stealth_enhanced": True,
            "status_obscured": True,
        },
        cleared_hazards=(),
        stamina_cost=0,
    ),
    "corrode": HazardCombo(
        id="corrode",
        name="Corrode",
        required_elements=("acid",),
        resulting_status="corrode",
        description="Green acid dissolves heavy metal locks and iron bars.",
        systemic_flags={
            "metal_locks_dissolved": True,
            "iron_bars_dissolved": True,
            "status_corrode": True,
        },
        cleared_hazards=(),
        stamina_cost=0,
    ),
}

# Element synonyms mapped to canonical element names
ELEMENT_ALIASES: Dict[str, str] = {
    "oil": "oil",
    "oily": "oil",
    "oil_slick": "oil",
    "grease": "oil",
    "fire": "fire",
    "flame": "fire",
    "flames": "fire",
    "ignite": "fire",
    "pyro": "fire",
    "heat": "fire",
    "water": "water",
    "conductive_water": "water",
    "wet": "water",
    "shock": "shock",
    "lightning": "shock",
    "electric": "shock",
    "electricity": "shock",
    "galvanic": "shock",
    "sandstorm": "sandstorm",
    "sand": "sandstorm",
    "grit": "sandstorm",
    "acid": "acid",
    "acid_pool": "acid",
    "corrosive": "acid",
}


def normalize_element(element: str) -> str:
    """Normalize element synonym to canonical name."""
    clean = element.lower().strip()
    return ELEMENT_ALIASES.get(clean, clean)


def get_hazard_combo(combo_id: str) -> Optional[HazardCombo]:
    """Retrieve hazard combo definition by identifier."""
    return HAZARD_COMBOS.get(combo_id.lower().strip())


def list_hazard_combos() -> List[HazardCombo]:
    """Return all registered hazard combos sorted deterministically."""
    return [HAZARD_COMBOS[k] for k in sorted(HAZARD_COMBOS.keys())]


def resolve_hazard_combo(*elements: Union[str, Iterable[str]]) -> Optional[HazardCombo]:
    """Deterministically resolve elements or hazards into a status combo.
    
    Accepts string arguments or iterables of strings in any order.
    """
    flattened: List[str] = []
    for item in elements:
        if isinstance(item, str):
            flattened.append(item)
        elif isinstance(item, Iterable):
            for sub in item:
                if isinstance(sub, str):
                    flattened.append(sub)

    if not flattened:
        return None

    # Check for direct combo id match if single item
    if len(flattened) == 1:
        direct = get_hazard_combo(flattened[0])
        if direct:
            return direct

    normalized_set: Set[str] = {normalize_element(e) for e in flattened}

    # Evaluate combos sorted by required elements length descending
    combos_by_priority = sorted(
        HAZARD_COMBOS.values(),
        key=lambda c: (-len(c.required_elements), c.id)
    )

    for combo in combos_by_priority:
        combo_reqs = set(combo.required_elements)
        if combo_reqs.issubset(normalized_set):
            return combo

    return None


def apply_hazard_combo(
    combo: HazardCombo,
    character: CharacterSheet,
    world_flags: Dict[str, Any]
) -> Tuple[CharacterSheet, Dict[str, Any], List[str]]:
    """Deterministically apply a resolved hazard combo to state."""
    new_char = character
    new_flags = dict(world_flags)
    events: List[str] = []

    # 1. Apply resulting status to character markers
    status = combo.resulting_status
    if not new_char.has_marker(status):
        m = list(new_char.markers) + [status]
        new_char = new_char.modify(markers=m)

    # 2. Apply status to world flags
    new_flags[f"status_{status}"] = True
    statuses = list(new_flags.get("statuses", []))
    if status not in statuses:
        statuses.append(status)
        new_flags["statuses"] = statuses

    # 3. Apply systemic flags
    for flag_key, flag_val in combo.systemic_flags.items():
        new_flags[flag_key] = flag_val

    # 4. Apply stamina cost
    if combo.stamina_cost > 0:
        stam = max(0, new_char.stamina - combo.stamina_cost)
        new_char = new_char.modify(stamina=stam)

    # 5. Clear hazards
    for cleared in combo.cleared_hazards:
        new_flags[f"hazard_{cleared}_cleared"] = True
        if f"hazard_{cleared}" in new_flags:
            new_flags[f"hazard_{cleared}"] = False

    # 6. Event message
    events.append(combo.description)

    return new_char, new_flags, events


@dataclass(frozen=True)
class RegionalAtmosphere:
    """Atmospheric weather or systemic condition tied to a region."""
    id: str
    name: str
    region_id: str
    description: str
    systemic_flags: Dict[str, Any] = field(default_factory=dict)
    favored_items: Tuple[str, ...] = ()
    rewarded_items: Tuple[str, ...] = ()
    favored_traits: Tuple[str, ...] = ()
    checked_traits: Tuple[str, ...] = ()
    favored_skills: Tuple[str, ...] = ()
    checked_skills: Tuple[str, ...] = ()
    stamina_drain: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "region_id": self.region_id,
            "description": self.description,
            "systemic_flags": dict(self.systemic_flags),
            "favored_items": list(self.favored_items),
            "rewarded_items": list(self.rewarded_items),
            "favored_traits": list(self.favored_traits),
            "checked_traits": list(self.checked_traits),
            "favored_skills": list(self.favored_skills),
            "checked_skills": list(self.checked_skills),
            "stamina_drain": self.stamina_drain,
        }


REGIONAL_ATMOSPHERES: Dict[str, RegionalAtmosphere] = {
    "blizzard": RegionalAtmosphere(
        id="blizzard",
        name="Blizzard",
        region_id="reach",
        description="Severe frost and biting winds howl across the crags.",
        systemic_flags={
            "weather": "blizzard",
            "atmosphere_blizzard": True,
            "frost_severe": True,
        },
        favored_items=("climbing_rope",),
        rewarded_items=("climbing_rope",),
        favored_traits=("nimble",),
        checked_traits=("nimble",),
        favored_skills=(),
        checked_skills=(),
        stamina_drain=1,
    ),
    "heatwave": RegionalAtmosphere(
        id="heatwave",
        name="Heatwave",
        region_id="scorchwaste",
        description="Searing heat ripples across red sand and bakes the earth.",
        systemic_flags={
            "weather": "heatwave",
            "atmosphere_heatwave": True,
            "heat_searing": True,
        },
        favored_items=("water_skin", "waterskin"),
        rewarded_items=("water_skin", "waterskin"),
        favored_traits=("heat_tolerant",),
        checked_traits=("heat_tolerant",),
        favored_skills=(),
        checked_skills=(),
        stamina_drain=1,
    ),
    "bioluminescence": RegionalAtmosphere(
        id="bioluminescence",
        name="Bioluminescence",
        region_id="sunken_hollows",
        description="Radiant algae casts cold blue light across the dark cavern.",
        systemic_flags={
            "weather": "bioluminescence",
            "atmosphere_bioluminescence": True,
            "glowing_runes_revealed": True,
        },
        favored_items=(),
        rewarded_items=(),
        favored_traits=("water_breather", "night_eyed"),
        checked_traits=("water_breather", "night_eyed"),
        favored_skills=(),
        checked_skills=(),
        stamina_drain=0,
    ),
    "miasma": RegionalAtmosphere(
        id="miasma",
        name="Miasma",
        region_id="lowlands",
        description="Thick sewer vapor hangs in damp air and chokes the throat.",
        systemic_flags={
            "weather": "miasma",
            "atmosphere_miasma": True,
            "vapor_thick": True,
        },
        favored_items=("mask", "cloth_mask", "filter_mask", "plague_mask"),
        rewarded_items=(),
        favored_traits=("iron_gutted",),
        checked_traits=("iron_gutted",),
        favored_skills=(),
        checked_skills=(),
        stamina_drain=1,
    ),
    "curfew": RegionalAtmosphere(
        id="curfew",
        name="Curfew",
        region_id="high_court",
        description="Armed sentries patrol the dark streets with torches and iron spears.",
        systemic_flags={
            "weather": "curfew",
            "atmosphere_curfew": True,
            "martial_watch_active": True,
        },
        favored_items=("watch_crest", "court_pass"),
        rewarded_items=("watch_crest",),
        favored_traits=("shadow_cloaked", "stealthy"),
        checked_traits=(),
        favored_skills=("stealth",),
        checked_skills=("stealth",),
        stamina_drain=0,
    ),
}

REGION_TO_ATMOSPHERE: Dict[str, str] = {
    # Reach
    "reach": "blizzard",
    "province_reach": "blizzard",
    "the_reach": "blizzard",
    # Scorchwaste
    "scorchwaste": "heatwave",
    "province_scorchwaste": "heatwave",
    "scorchwaste_local": "heatwave",
    "the_scorchwaste": "heatwave",
    # Hollows
    "hollows": "bioluminescence",
    "sunken_hollows": "bioluminescence",
    "province_sunken_hollows": "bioluminescence",
    "sunken_hollows_local": "bioluminescence",
    "the_sunken_hollows": "bioluminescence",
    "the_hollows": "bioluminescence",
    # Lowlands
    "lowlands": "miasma",
    "province_lowlands": "miasma",
    "the_lowlands": "miasma",
    # High Court
    "high_court": "curfew",
    "province_high_court": "curfew",
    "high_court_local": "curfew",
    "court": "curfew",
    "the_high_court": "curfew",
}


def get_regional_atmosphere(region_id: str, world_flags: Dict[str, Any]) -> Optional[RegionalAtmosphere]:
    """Retrieve active regional atmosphere for a region, taking world flags into account."""
    clean_reg = region_id.lower().strip()

    atmo_id = REGION_TO_ATMOSPHERE.get(clean_reg)
    if not atmo_id and clean_reg in REGIONAL_ATMOSPHERES:
        atmo_id = clean_reg

    if not atmo_id:
        override = (
            world_flags.get(f"{clean_reg}_atmosphere")
            or world_flags.get(f"{clean_reg}_weather")
            or world_flags.get("regional_atmosphere")
            or world_flags.get("active_atmosphere")
            or world_flags.get("atmosphere")
            or world_flags.get("weather")
        )
        if isinstance(override, str):
            clean_override = override.lower().strip()
            atmo_id = REGION_TO_ATMOSPHERE.get(clean_override, clean_override)

    if not atmo_id or atmo_id not in REGIONAL_ATMOSPHERES:
        return None

    atmo = REGIONAL_ATMOSPHERES[atmo_id]

    # Check suppression or deactivation flags
    if (
        world_flags.get(f"{atmo_id}_cleared") is True
        or world_flags.get(f"{atmo_id}_suppressed") is True
        or world_flags.get(f"hazard_{atmo_id}_cleared") is True
        or world_flags.get(f"{atmo_id}_active") is False
        or world_flags.get(f"atmosphere_{atmo_id}_active") is False
        or world_flags.get(f"{clean_reg}_weather_active") is False
    ):
        return None

    return atmo


def list_regional_atmospheres() -> List[RegionalAtmosphere]:
    """Return all registered regional atmospheres sorted deterministically."""
    return [REGIONAL_ATMOSPHERES[k] for k in sorted(REGIONAL_ATMOSPHERES.keys())]

