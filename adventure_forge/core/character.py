"""Deep Character Customization Model.

Implements the multi-axis character state vector required by G1 / G3:
1. Ancestry
2. Background
3. Attributes & Skills
4. Traits
5. Flaws
6. Social Stance & Faction Reputation
7. Markers & Attire
"""
from dataclasses import dataclass, field
import dataclasses
from typing import Dict, List, Any


@dataclass(frozen=True)
class CharacterSheet:
    """Immutable character sheet representing the protagonist's multi-axis state."""
    name: str
    ancestry: str
    background: str
    attributes: Dict[str, int] = field(default_factory=dict)
    skills: Dict[str, int] = field(default_factory=dict)
    traits: List[str] = field(default_factory=list)
    flaws: List[str] = field(default_factory=list)
    reputation: Dict[str, int] = field(default_factory=dict)
    markers: List[str] = field(default_factory=list)
    inventory: List[str] = field(default_factory=list)
    health: int = 20
    max_health: int = 20
    stamina: int = 10
    max_stamina: int = 10

    def has_trait(self, trait: str) -> bool:
        return trait.lower() in {t.lower() for t in self.traits}

    def has_flaw(self, flaw: str) -> bool:
        return flaw.lower() in {f.lower() for f in self.flaws}

    def has_marker(self, marker: str) -> bool:
        return marker.lower() in {m.lower() for m in self.markers}

    def has_item(self, item: str) -> bool:
        return item.lower() in {i.lower() for i in self.inventory}

    def get_attribute(self, attr: str, default: int = 0) -> int:
        return self.attributes.get(attr.lower(), default)

    def get_skill(self, skill: str, default: int = 0) -> int:
        return self.skills.get(skill.lower(), default)

    def get_reputation(self, faction: str, default: int = 0) -> int:
        return self.reputation.get(faction.lower(), default)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "ancestry": self.ancestry,
            "background": self.background,
            "attributes": dict(self.attributes),
            "skills": dict(self.skills),
            "traits": list(self.traits),
            "flaws": list(self.flaws),
            "reputation": dict(self.reputation),
            "markers": list(self.markers),
            "inventory": list(self.inventory),
            "health": self.health,
            "max_health": self.max_health,
            "stamina": self.stamina,
            "max_stamina": self.max_stamina,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CharacterSheet":
        return cls(
            name=data.get("name", "Wanderer"),
            ancestry=data.get("ancestry", "Plainsman"),
            background=data.get("background", "Drifter"),
            attributes=dict(data.get("attributes", {})),
            skills=dict(data.get("skills", {})),
            traits=list(data.get("traits", [])),
            flaws=list(data.get("flaws", [])),
            reputation=dict(data.get("reputation", {})),
            markers=list(data.get("markers", [])),
            inventory=list(data.get("inventory", [])),
            health=int(data.get("health", 20)),
            max_health=int(data.get("max_health", 20)),
            stamina=int(data.get("stamina", 10)),
            max_stamina=int(data.get("max_stamina", 10)),
        )

    def modify(self, **kwargs: Any) -> "CharacterSheet":
        """Return a new CharacterSheet with specified fields modified."""
        updates: Dict[str, Any] = {}
        for k, v in kwargs.items():
            if k in ("attributes", "skills", "reputation"):
                merged = dict(getattr(self, k))
                merged.update(v)
                updates[k] = merged
            else:
                updates[k] = v
        return dataclasses.replace(self, **updates)


@dataclass(frozen=True)
class CharacterPreset:
    """Canonical character preset definition for starting new games."""
    id: str
    name: str
    description: str
    character: CharacterSheet
    start_scene: str
    start_region: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "character": self.character.to_dict(),
            "start_scene": self.start_scene,
            "start_region": self.start_region,
        }


CHARACTER_PRESETS: Dict[str, CharacterPreset] = {
    "cutpurse": CharacterPreset(
        id="cutpurse",
        name="Silas",
        description="Agile Deep-Dweller cutpurse with streetwise instincts and underworld contacts.",
        character=CharacterSheet(
            name="Silas",
            ancestry="Deep-Dweller",
            background="cutpurse",
            attributes={"agility": 14, "strength": 9, "intimidation": 7},
            skills={"cunning": 4, "stealth": 3},
            traits=["night_eyed", "streetwise"],
            flaws=["marked_outlaw"],
            reputation={"smugglers": 10, "city_watch": -5},
            markers=["guild_brand"],
            inventory=["lockpick", "silver_coin"],
            health=20,
            max_health=20,
            stamina=10,
            max_stamina=10,
        ),
        start_scene="warrens_gate",
        start_region="lower_warrens",
    ),
    "noble": CharacterPreset(
        id="noble",
        name="Lady Vivienne",
        description="Exiled High-Kin noble adept at rhetoric, high-court intrigue, and legal dossiers.",
        character=CharacterSheet(
            name="Lady Vivienne",
            ancestry="High-Kin",
            background="noble_exile",
            attributes={"agility": 8, "strength": 10, "intimidation": 14},
            skills={"rhetoric": 4, "cunning": 2},
            traits=["skeptical"],
            flaws=["oath_bound"],
            reputation={"city_watch": 10, "smugglers": -10},
            markers=["watch_crest"],
            inventory=["silver_coin", "legal_dossier"],
            health=20,
            max_health=20,
            stamina=10,
            max_stamina=10,
        ),
        start_scene="court_antechamber",
        start_region="high_court",
    ),
    "warrior": CharacterPreset(
        id="warrior",
        name="Garron",
        description="Ashenborn pit fighter of brute strength and endurance from the iron crags.",
        character=CharacterSheet(
            name="Garron",
            ancestry="Ashenborn",
            background="pit_fighter",
            attributes={"strength": 16, "agility": 12, "endurance": 14},
            skills={"athletics": 4, "brawling": 4},
            traits=["iron_gutted"],
            flaws=[],
            reputation={"iron_guard": 5},
            markers=[],
            inventory=["water_skin", "crowbar"],
            health=20,
            max_health=20,
            stamina=10,
            max_stamina=10,
        ),
        start_scene="crags_base",
        start_region="iron_crags",
    ),
}

# Canonical alias: pit_fighter -> warrior
CHARACTER_PRESETS["pit_fighter"] = CHARACTER_PRESETS["warrior"]


def get_preset(preset_id: str) -> CharacterPreset:
    """Retrieve a character preset by ID (case-insensitive).

    Raises KeyError if the preset does not exist.
    """
    key = preset_id.lower().strip()
    if key in CHARACTER_PRESETS:
        return CHARACTER_PRESETS[key]
    raise KeyError(f"Unknown preset '{preset_id}'. Available presets: {list(CHARACTER_PRESETS.keys())}")


def list_presets() -> List[str]:
    """List all available character preset IDs."""
    return list(CHARACTER_PRESETS.keys())

