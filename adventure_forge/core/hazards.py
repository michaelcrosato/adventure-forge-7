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
