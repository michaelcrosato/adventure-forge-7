"""Content Schema Definitions.

Validates declarative content for regions, POIs, scenes, entities, and actions.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from adventure_forge.core.actions import Action


@dataclass
class DynamicDescription:
    """Dynamic perception snippet based on character traits, skills, or history."""
    condition: Dict[str, Any]
    text: str  # 1 short sentence


@dataclass
class SceneNode:
    """A single coherent scene or room in the world graph."""
    id: str
    title: str
    region: str
    description: str  # Default Hemingway prose (1-2 sentences)
    dynamic_descriptions: List[DynamicDescription] = field(default_factory=list)
    entities: List[Dict[str, Any]] = field(default_factory=list)
    base_actions: List[Action] = field(default_factory=list)
    is_terminal: bool = False
    outcome_type: Optional[str] = None

    def render_description(self, character: Any, world_flags: Dict[str, Any]) -> str:
        """Render final scene description combining base text with character-salient observations."""
        from adventure_forge.core.conditions import evaluate_condition
        lines = [self.description.strip()]
        for dyn in self.dynamic_descriptions:
            if evaluate_condition(dyn.condition, character, world_flags):
                lines.append(dyn.text.strip())
        return " ".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "region": self.region,
            "description": self.description,
            "dynamic_descriptions": [
                {"condition": d.condition, "text": d.text}
                for d in self.dynamic_descriptions
            ],
            "entities": list(self.entities),
            "base_actions": [a.to_dict() for a in self.base_actions],
            "is_terminal": self.is_terminal,
            "outcome_type": self.outcome_type,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SceneNode":
        dyn_desc = [
            DynamicDescription(condition=d["condition"], text=d["text"])
            for d in data.get("dynamic_descriptions", [])
        ]
        actions = [
            Action.from_dict(a) for a in data.get("base_actions", [])
        ]
        return cls(
            id=data["id"],
            title=data["title"],
            region=data["region"],
            description=data["description"],
            dynamic_descriptions=dyn_desc,
            entities=list(data.get("entities", [])),
            base_actions=actions,
            is_terminal=bool(data.get("is_terminal", False)),
            outcome_type=data.get("outcome_type"),
        )


@dataclass
class RegionManifest:
    """Specification of a province or region with its defining systemic mechanic."""
    id: str
    name: str
    mechanic_name: str
    mechanic_description: str
    scenes: Dict[str, SceneNode] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "mechanic_name": self.mechanic_name,
            "mechanic_description": self.mechanic_description,
            "scenes": {k: v.to_dict() for k, v in self.scenes.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RegionManifest":
        scenes = {
            k: SceneNode.from_dict(v) for k, v in data.get("scenes", {}).items()
        }
        return cls(
            id=data["id"],
            name=data["name"],
            mechanic_name=data["mechanic_name"],
            mechanic_description=data["mechanic_description"],
            scenes=scenes
        )
