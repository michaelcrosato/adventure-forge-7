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
from typing import Dict, List, Set, Any
import copy


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
        return trait.lower() in [t.lower() for t in self.traits]

    def has_flaw(self, flaw: str) -> bool:
        return flaw.lower() in [f.lower() for f in self.flaws]

    def has_marker(self, marker: str) -> bool:
        return marker.lower() in [m.lower() for m in self.markers]

    def has_item(self, item: str) -> bool:
        return item.lower() in [i.lower() for i in self.inventory]

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

    def modify(self, **kwargs) -> "CharacterSheet":
        """Return a new CharacterSheet with specified fields modified."""
        d = self.to_dict()
        for k, v in kwargs.items():
            if k in ("attributes", "skills", "reputation"):
                merged = dict(d[k])
                merged.update(v)
                d[k] = merged
            else:
                d[k] = v
        return CharacterSheet.from_dict(d)
