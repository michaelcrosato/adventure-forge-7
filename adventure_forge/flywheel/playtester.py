"""Blind Playtester Fleet (Multi-Persona Autonomous Bots).

Enforces I6 Information Firewall:
- Agents interact STRICTLY through the player observation contract.
- Agents have zero access to source code, hidden flags, or solution maps.
- Supports divergent play personas: Speedrunner, Brute, Infiltrator, Explorer, Saboteur.
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from adventure_forge.core.state import GameState
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.engine import AdventureEngine, StepResult
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry


@dataclass
class SessionTelemetry:
    persona: str
    seed: int
    turn_count: int
    decisions_made: List[str]
    scenes_visited: List[str]
    fingerprints: List[str]
    terminal_outcome: Optional[str]
    retention_score: float
    friction_notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "persona": self.persona,
            "seed": self.seed,
            "turn_count": self.turn_count,
            "decisions_made": list(self.decisions_made),
            "scenes_visited": list(self.scenes_visited),
            "fingerprints": list(self.fingerprints),
            "terminal_outcome": self.terminal_outcome,
            "retention_score": self.retention_score,
            "friction_notes": list(self.friction_notes),
        }


class BlindPlaytester:
    """Autonomous playtester driven solely by observable affordances and a behavioral persona."""

    def __init__(self, persona: str = "explorer", seed: int = 42):
        self.persona = persona
        self.seed = seed
        self.rng = DeterministicRNG.from_seed(seed)

    def select_action(self, obs: StepResult) -> Optional[str]:
        if not obs.legal_actions:
            return None

        actions = obs.legal_actions

        if self.persona == "brute":
            # Prefers combat, systemic force, high risk, high strength actions
            preferred = [a for a in actions if "force" in a["id"] or a["category"] in ("systemic", "combat")]
            if preferred:
                val, self.rng = self.rng.next_int(0, len(preferred) - 1)
                return str(preferred[val]["id"])

        elif self.persona == "infiltrator":
            # Prefers trait exploits, stealth, cunning, lockpicking
            preferred = [a for a in actions if a["category"] in ("trait_exploit", "item_affordance") or "slip" in a["id"] or "pick" in a["id"]]
            if preferred:
                val, self.rng = self.rng.next_int(0, len(preferred) - 1)
                return str(preferred[val]["id"])

        elif self.persona == "speedrunner":
            # Prefers movement actions that advance to new scenes quickly
            preferred = [a for a in actions if a["category"] == "movement"]
            if preferred:
                val, self.rng = self.rng.next_int(0, len(preferred) - 1)
                return str(preferred[val]["id"])

        elif self.persona == "saboteur":
            # Prefers high-risk, environmental burning/melting
            preferred = [a for a in actions if a["risk"] == "high" or "burn" in a["id"] or "melt" in a["id"]]
            if preferred:
                val, self.rng = self.rng.next_int(0, len(preferred) - 1)
                return str(preferred[val]["id"])

        # Default / Explorer: prefers variety and unvisited interaction verbs
        idx, self.rng = self.rng.next_int(0, len(actions) - 1)
        return str(actions[idx]["id"])

    def run_session(self, initial_char: CharacterSheet, start_scene: str, max_turns: int = 20) -> SessionTelemetry:
        registry = build_world_registry()
        engine = AdventureEngine(registry)

        state = GameState(
            build_id="af-build-001",
            session_id=f"blind-playtest-{self.persona}-{self.seed}",
            character=initial_char,
            current_region=engine.get_region_id_for_scene(start_scene) or "iron_crags",
            current_scene=start_scene,
            rng=DeterministicRNG.from_seed(self.seed)
        )

        obs = engine.observe(state)
        decisions: List[str] = []
        scenes_visited: List[str] = [obs.scene_id]
        fingerprints: List[str] = [obs.fingerprint]
        friction_notes: List[str] = []

        for turn in range(max_turns):
            if obs.is_terminal:
                break

            action_id = self.select_action(obs)
            if not action_id:
                friction_notes.append(f"Dead end: No legal actions at scene {obs.scene_id}")
                break

            decisions.append(action_id)
            state, obs = engine.step(state, action_id)

            if not obs.success:
                friction_notes.append(f"Rejected legal action: {action_id}")
                break

            scenes_visited.append(obs.scene_id)
            fingerprints.append(obs.fingerprint)

        # Calculate retention heuristic (variety of meaningful decisions + unique scenes explored)
        unique_scenes = len(set(scenes_visited))
        retention = min(1.0, (len(decisions) * 0.05) + (unique_scenes * 0.15))

        return SessionTelemetry(
            persona=self.persona,
            seed=self.seed,
            turn_count=len(decisions),
            decisions_made=decisions,
            scenes_visited=scenes_visited,
            fingerprints=fingerprints,
            terminal_outcome=obs.outcome,
            retention_score=round(retention, 2),
            friction_notes=friction_notes
        )
