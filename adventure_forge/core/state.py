"""Immutable GameState and Canonical Fingerprinting.

Guarantees bit-for-bit replay determinism (I1 / SYS-01 / SYS-04).
"""
from dataclasses import dataclass, field
import dataclasses
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
        cached = getattr(self, "_cached_fp", None)
        if isinstance(cached, str):
            return cached

        canonical_dict = {
            "build_id": self.build_id,
            "character": self.character.to_dict(),
            "current_region": self.current_region,
            "current_scene": self.current_scene,
            "world_flags": self.world_flags,
            "turn_count": self.turn_count,
            "rng_state": self.rng.state,
        }
        serialized = json.dumps(canonical_dict, sort_keys=True, separators=(",", ":"))
        fp = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        object.__setattr__(self, "_cached_fp", fp)
        return fp

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
        flags = kwargs.get("world_flags")
        if flags is not None and flags is not self.world_flags:
            merged = dict(self.world_flags)
            merged.update(flags)
            kwargs["world_flags"] = merged
        return dataclasses.replace(self, **kwargs)
