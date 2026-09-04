"""Immutable GameState and Canonical Fingerprinting.

Guarantees bit-for-bit replay determinism (I1 / SYS-01 / SYS-04).
"""
from dataclasses import dataclass, field
import hashlib
import json
from typing import Dict, Any, List
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.rng import DeterministicRNG


@dataclass(frozen=True)
class GameState:
    """Immutable state snapshot of the entire active adventure session."""
    build_id: str
    session_id: str
    character: CharacterSheet
    current_region: str
    current_scene: str
    world_flags: Dict[str, Any] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)
    event_log: List[str] = field(default_factory=list)
    turn_count: int = 0
    rng: DeterministicRNG = field(default_factory=lambda: DeterministicRNG.from_seed(42))

    def fingerprint(self) -> str:
        """Compute canonical collision-resistant SHA-256 hash of this state."""
        canonical_dict = {
            "build_id": self.build_id,
            "character": self.character.to_dict(),
            "current_region": self.current_region,
            "current_scene": self.current_scene,
            "world_flags": {k: self.world_flags[k] for k in sorted(self.world_flags.keys())},
            "turn_count": self.turn_count,
            "rng_state": self.rng.state,
        }
        serialized = json.dumps(canonical_dict, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "build_id": self.build_id,
            "session_id": self.session_id,
            "character": self.character.to_dict(),
            "current_region": self.current_region,
            "current_scene": self.current_scene,
            "world_flags": dict(self.world_flags),
            "history": list(self.history),
            "event_log": list(self.event_log),
            "turn_count": self.turn_count,
            "rng": self.rng.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameState":
        return cls(
            build_id=data["build_id"],
            session_id=data["session_id"],
            character=CharacterSheet.from_dict(data["character"]),
            current_region=data["current_region"],
            current_scene=data["current_scene"],
            world_flags=dict(data.get("world_flags", {})),
            history=list(data.get("history", [])),
            event_log=list(data.get("event_log", [])),
            turn_count=int(data.get("turn_count", 0)),
            rng=DeterministicRNG.from_dict(data.get("rng", {"state": 42})),
        )

    def evolve(self, **kwargs) -> "GameState":
        """Return a new GameState with selected updated fields."""
        d = self.to_dict()
        for k, v in kwargs.items():
            if k == "character" and isinstance(v, CharacterSheet):
                d["character"] = v.to_dict()
            elif k == "rng" and isinstance(v, DeterministicRNG):
                d["rng"] = v.to_dict()
            elif k == "world_flags":
                merged = dict(d["world_flags"])
                merged.update(v)
                d["world_flags"] = merged
            else:
                d[k] = v
        return GameState.from_dict(d)
