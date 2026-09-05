"""Blind Playtester Fleet (Multi-Persona Autonomous Bots).

Enforces I6 Information Firewall:
- Agents interact STRICTLY through the player observation contract.
- Agents have zero access to source code, hidden flags, or solution maps.
- Supports divergent play personas: Explorer, Brute, Infiltrator, Speedrunner, Saboteur, Nomad, Diver, Scout.
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Set
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

    PERSONAS = [
        "explorer",
        "brute",
        "infiltrator",
        "speedrunner",
        "saboteur",
        "nomad",
        "diver",
        "scout",
    ]

    def __init__(self, persona: str = "explorer", seed: int = 42):
        self.persona = persona.lower().strip()
        self.seed = seed
        self.rng = DeterministicRNG.from_seed(seed)
        self.visited_verbs: Set[str] = set()
        self.visited_actions: Set[str] = set()

    def select_action(self, obs: StepResult) -> Optional[str]:
        if not obs.legal_actions:
            return None

        actions = obs.legal_actions
        p = self.persona

        preferred: List[Dict[str, Any]] = []

        if p == "explorer":
            # Prefers variety, unvisited interaction verbs, and world discovery
            discovery_kws = (
                "explore", "discover", "survey", "examine", "scout",
                "investigate", "inspect", "search", "venture", "uncover",
                "study", "observe", "read", "check", "navigate", "map",
                "climb", "descend", "ascend", "travel", "march", "enter", "head"
            )
            unvisited_verbs = [
                a for a in actions
                if a.get("id", "").lower().split("_")[0] not in self.visited_verbs
            ]
            if unvisited_verbs:
                pref_discovery = [
                    a for a in unvisited_verbs
                    if a.get("category") == "movement"
                    or any(kw in a.get("id", "").lower() or kw in a.get("label", "").lower() for kw in discovery_kws)
                ]
                pool = pref_discovery if pref_discovery else unvisited_verbs
            else:
                unvisited_actions = [a for a in actions if a.get("id") not in self.visited_actions]
                if unvisited_actions:
                    pref_discovery = [
                        a for a in unvisited_actions
                        if a.get("category") == "movement"
                        or any(kw in a.get("id", "").lower() or kw in a.get("label", "").lower() for kw in discovery_kws)
                    ]
                    pool = pref_discovery if pref_discovery else unvisited_actions
                else:
                    pool = actions

            val, self.rng = self.rng.next_int(0, len(pool) - 1)
            chosen_id = str(pool[val]["id"])
            self.visited_verbs.add(chosen_id.split("_")[0].lower())
            self.visited_actions.add(chosen_id)
            return chosen_id

        elif p == "brute":
            # Prefers force, brawling, breaking, combat, high-strength actions
            brute_kws = (
                "force", "brawl", "break", "smash", "bash", "strike",
                "fight", "crush", "punch", "tackle", "charge", "shatter",
                "kick", "cleave", "heave", "slam", "overpower", "assault", "combat"
            )
            direct_brute = [
                a for a in actions
                if any(kw in a.get("id", "").lower() or kw in a.get("label", "").lower() for kw in brute_kws)
                or a.get("category") == "combat"
            ]
            if direct_brute:
                preferred = direct_brute
            else:
                preferred = [
                    a for a in actions
                    if a.get("category") == "systemic"
                    or a.get("stamina_cost", 0) >= 2
                    or a.get("risk") == "high"
                ]

        elif p == "infiltrator":
            # Prefers stealth, cunning, lockpicking, slipping past guards
            infil_kws = (
                "stealth", "slip", "pick", "sneak", "lock", "cunning",
                "shadow", "hide", "bypass", "infiltrate", "guard",
                "sentry", "prowl", "creep", "evade", "distract",
                "unseen", "silent", "signet", "thief", "steal", "pickpocket"
            )
            direct_infil = [
                a for a in actions
                if any(kw in a.get("id", "").lower() or kw in a.get("label", "").lower() for kw in infil_kws)
            ]
            if direct_infil:
                preferred = direct_infil
            else:
                preferred = [
                    a for a in actions
                    if a.get("category") in ("trait_exploit", "item_affordance")
                ]

        elif p == "speedrunner":
            # Prefers movement actions that advance between scenes quickly
            move_kws = (
                "travel", "head", "go", "enter", "leave", "cross",
                "advance", "run", "sprint", "dash", "stride", "press",
                "move", "venture", "walk", "trek", "march", "climb_down",
                "climb_up", "return", "descend", "ascend", "swim_to",
                "retreat", "step"
            )
            preferred = [
                a for a in actions
                if a.get("category") == "movement"
                or any(kw in a.get("id", "").lower() or kw in a.get("label", "").lower() for kw in move_kws)
            ]

        elif p == "saboteur":
            # Prefers high-risk, environmental burning/melting, conflagration, sabotage
            sabo_kws = (
                "burn", "melt", "ignite", "corrode", "fire", "sabotage",
                "acid", "blast", "destroy", "conflagrat", "incinerat",
                "flame", "smoke", "bomb", "wreck", "ruin", "hazard", "torch"
            )
            direct_sabo = [
                a for a in actions
                if any(kw in a.get("id", "").lower() or kw in a.get("label", "").lower() for kw in sabo_kws)
            ]
            if direct_sabo:
                preferred = direct_sabo
            else:
                preferred = [
                    a for a in actions
                    if a.get("risk") == "high"
                    or (a.get("category") in ("systemic", "trait_exploit") and a.get("risk") in ("high", "medium"))
                ]

        elif p == "nomad":
            # Prefers survival, endurance, desert navigation, trade, oasis interaction
            nomad_kws = (
                "surviv", "endur", "desert", "dune", "trade", "oasis",
                "shade", "water", "drink", "sand", "well", "canteen",
                "salvage", "compass", "trek", "march", "bazaar", "rest",
                "nomad", "barter", "caravan", "brave", "scorch"
            )
            direct_nomad = [
                a for a in actions
                if any(kw in a.get("id", "").lower() or kw in a.get("label", "").lower() for kw in nomad_kws)
            ]
            if direct_nomad:
                preferred = direct_nomad
            else:
                preferred = [
                    a for a in actions
                    if a.get("category") in ("social", "interaction")
                ]

        elif p == "diver":
            # Prefers diving, submerging, water manipulation, deep trenches
            diver_kws = (
                "dive", "submerg", "water", "trench", "swim", "pool",
                "lake", "river", "grotto", "abyss", "depth", "deep",
                "wade", "conductive", "drown", "tide", "flood", "bell",
                "plunge", "sea", "ocean", "current", "channel", "aquatic",
                "salvage_diving", "coral", "reef", "sunken"
            )
            preferred = [
                a for a in actions
                if any(kw in a.get("id", "").lower() or kw in a.get("label", "").lower() for kw in diver_kws)
            ]

        elif p == "scout":
            # Prefers verticality, climbing, vantage points, scaling cliffs, scouting
            scout_kws = (
                "scout", "climb", "vantage", "scale", "cliff", "vertical",
                "ridge", "peak", "height", "lookout", "survey", "spire",
                "watch", "rope", "crag", "mountain", "ascent", "ascend",
                "tower", "overlook", "bluff", "high", "pass"
            )
            preferred = [
                a for a in actions
                if any(kw in a.get("id", "").lower() or kw in a.get("label", "").lower() for kw in scout_kws)
            ]

        if preferred:
            unvisited_pref = [a for a in preferred if a.get("id") not in self.visited_actions]
            pool = unvisited_pref if unvisited_pref else preferred
        else:
            unvisited_all = [a for a in actions if a.get("id") not in self.visited_actions]
            pool = unvisited_all if unvisited_all else actions

        val, self.rng = self.rng.next_int(0, len(pool) - 1)
        chosen_id = str(pool[val]["id"])
        self.visited_verbs.add(chosen_id.split("_")[0].lower())
        self.visited_actions.add(chosen_id)
        return chosen_id

    def run_session(
        self,
        initial_char: CharacterSheet,
        start_scene: str,
        max_turns: int = 20,
        engine: Optional[AdventureEngine] = None,
    ) -> SessionTelemetry:
        if engine is None:
            registry = build_world_registry()
            engine = AdventureEngine(registry)

        self.visited_verbs = set()
        self.visited_actions = set()

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

        for _turn in range(max_turns):
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
        if friction_notes:
            retention = max(0.0, retention - (len(friction_notes) * 0.25))

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
