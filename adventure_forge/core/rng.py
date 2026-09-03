"""Deterministic pseudo-random number generator (PRNG) cursor.

Guarantees 100% replay reproducibility across platforms and Python versions.
No dependency on Python's ambient random state or system time.
"""
from dataclasses import dataclass
from typing import List, TypeVar, Tuple

T = TypeVar("T")


@dataclass(frozen=True)
class DeterministicRNG:
    """Immutable deterministic PRNG cursor using 64-bit SplitMix64 algorithm."""
    state: int

    @classmethod
    def from_seed(cls, seed: int) -> "DeterministicRNG":
        """Initialize PRNG from an arbitrary integer seed."""
        # Mix initial seed
        initial = (seed & 0xFFFFFFFFFFFFFFFF) ^ 0x9E3779B97F4A7C15
        return cls(state=initial)

    def next_u64(self) -> Tuple[int, "DeterministicRNG"]:
        """Advance cursor and return a 64-bit unsigned integer."""
        new_state = (self.state + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
        z = new_state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
        value = z ^ (z >> 31)
        return value, DeterministicRNG(state=new_state)

    def next_int(self, low: int, high: int) -> Tuple[int, "DeterministicRNG"]:
        """Return an integer in [low, high] inclusive and next cursor."""
        if low > high:
            raise ValueError(f"low ({low}) must be <= high ({high})")
        val, next_cursor = self.next_u64()
        span = high - low + 1
        result = low + (val % span)
        return result, next_cursor

    def next_float(self) -> Tuple[float, "DeterministicRNG"]:
        """Return a float in [0.0, 1.0) and next cursor."""
        val, next_cursor = self.next_u64()
        result = (val >> 11) * (1.0 / (1 << 53))
        return result, next_cursor

    def choose(self, seq: List[T]) -> Tuple[T, "DeterministicRNG"]:
        """Choose an element from a non-empty sequence and return next cursor."""
        if not seq:
            raise ValueError("Cannot choose from an empty sequence")
        idx, next_cursor = self.next_int(0, len(seq) - 1)
        return seq[idx], next_cursor

    def to_dict(self) -> dict:
        return {"state": self.state}

    @classmethod
    def from_dict(cls, data: dict) -> "DeterministicRNG":
        return cls(state=int(data["state"]))
