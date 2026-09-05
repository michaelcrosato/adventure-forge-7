"""Pure Deterministic Adventure Kernel.

Implements:
step(state, action, world_registry) -> (new_state, step_result)

Hard Invariants:
- Pure transition: no wall clock, network, or unseeded random state.
- Stale or illegal actions strictly rejected without state mutation.
- Canonical fingerprint hash updated deterministically.
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
from adventure_forge.core.state import GameState
from adventure_forge.core.actions import Action, synthesize_affordances
from adventure_forge.core.effects import apply_effects
from adventure_forge.content.schema import RegionManifest, SceneNode
from adventure_forge.content.quests import get_continental_main_quest, evaluate_all_subquests


@dataclass
class StepResult:
    """The observable outcome of a transition step (player-safe)."""
    success: bool
    message: str
    scene_id: str
    region_id: str
    title: str
    description: str
    events: List[str]
    legal_actions: List[Dict[str, Any]]
    turn_count: int
    is_terminal: bool = False
    outcome: Optional[str] = None
    fingerprint: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "scene_id": self.scene_id,
            "region_id": self.region_id,
            "title": self.title,
            "description": self.description,
            "events": list(self.events),
            "legal_actions": list(self.legal_actions),
            "turn_count": self.turn_count,
            "is_terminal": self.is_terminal,
            "outcome": self.outcome,
            "fingerprint": self.fingerprint,
        }


class AdventureEngine:
    """Authoritative game engine executing transitions over declarative world manifests."""

    def __init__(self, world_registry: Dict[str, RegionManifest], build_id: str = "build-001"):
        self.world_registry = world_registry
        self.build_id = build_id
        # Map scene_id -> (region_id, SceneNode)
        self._scene_map: Dict[str, Tuple[str, SceneNode]] = {}
        for reg_id, region in world_registry.items():
            for sc_id, scene in region.scenes.items():
                self._scene_map[sc_id] = (reg_id, scene)

    def get_scene(self, scene_id: str) -> Optional[SceneNode]:
        found = self._scene_map.get(scene_id)
        return found[1] if found else None

    def get_region_id_for_scene(self, scene_id: str) -> Optional[str]:
        found = self._scene_map.get(scene_id)
        return found[0] if found else None

    def get_legal_actions(self, state: GameState) -> List[Action]:
        cached = getattr(state, "_cached_legal_actions", None)
        if isinstance(cached, list):
            return cached
        scene = self.get_scene(state.current_scene)
        if not scene:
            return []
        actions = synthesize_affordances(
            base_actions=scene.base_actions,
            scene_entities=scene.entities,
            character=state.character,
            world_flags=state.world_flags,
            region_id=scene.region or state.current_region,
        )
        object.__setattr__(state, "_cached_legal_actions", actions)
        return actions

    def get_quest_progress(self, state: GameState) -> Dict[str, Any]:
        """Compute current continental main quest progress and subquests for active state."""
        quest = get_continental_main_quest()
        progress = quest.evaluate_progress(state.character, state.world_flags)
        progress["subquests"] = evaluate_all_subquests(state.character, state.world_flags)
        return progress

    def observe(self, state: GameState, last_events: Optional[List[str]] = None) -> StepResult:
        """Produce the player observation for the current state."""
        scene = self.get_scene(state.current_scene)
        if not scene:
            return StepResult(
                success=False,
                message=f"Missing scene: {state.current_scene}",
                scene_id=state.current_scene,
                region_id=state.current_region,
                title="Unknown Void",
                description="The path ends in empty air.",
                events=last_events or [],
                legal_actions=[],
                turn_count=state.turn_count,
                is_terminal=True,
                fingerprint=state.fingerprint()
            )

        desc = scene.render_description(state.character, state.world_flags)
        legal_acts = self.get_legal_actions(state)
        act_dicts = [
            {
                "id": a.id,
                "label": a.label,
                "category": a.category,
                "risk": a.risk,
                "stamina_cost": a.stamina_cost,
            }
            for a in legal_acts
        ]

        return StepResult(
            success=True,
            message="Observation updated.",
            scene_id=scene.id,
            region_id=scene.region,
            title=scene.title,
            description=desc,
            events=last_events if last_events is not None else list(state.event_log[-3:]),
            legal_actions=act_dicts,
            turn_count=state.turn_count,
            is_terminal=scene.is_terminal,
            outcome=scene.outcome_type,
            fingerprint=state.fingerprint()
        )

    def step(self, state: GameState, action_id: str) -> Tuple[GameState, StepResult]:
        """Execute a canonical action against the authoritative state.
        
        Pure transition:
        - If action is illegal/stale: returns (state, failure StepResult).
        - If action is legal: returns (new_state, success StepResult).
        """
        scene = self.get_scene(state.current_scene)
        if not scene:
            obs = self.observe(state, [f"Error: Current scene {state.current_scene} not found"])
            return state, obs

        legal_actions = self.get_legal_actions(state)
        action_map = {a.id: a for a in legal_actions}

        if action_id not in action_map:
            # SYS-03: Stale or invalid actions strictly rejected
            obs = self.observe(state, [f"Illegal action '{action_id}' rejected for current state."])
            obs.success = False
            obs.message = f"Action '{action_id}' is not currently legal."
            return state, obs

        chosen = action_map[action_id]

        # 1. Deduct costs
        current_char = state.character
        if chosen.stamina_cost > 0:
            new_stamina = max(0, current_char.stamina - chosen.stamina_cost)
            current_char = current_char.modify(stamina=new_stamina)

        # 2. Advance RNG for transition
        rng_cursor = state.rng
        rng_val, rng_cursor = rng_cursor.next_u64()

        # 3. Apply action effects
        new_char, new_flags, emitted_events, scene_override = apply_effects(
            chosen.effects,
            current_char,
            state.world_flags
        )

        # 4. Add result text if any
        if chosen.result_text:
            emitted_events.insert(0, chosen.result_text)

        # 5. Resolve target scene
        next_scene_id = scene_override or chosen.target_scene or state.current_scene
        next_region_id = self.get_region_id_for_scene(next_scene_id) or state.current_region

        # 6. Construct new immutable state
        new_history = list(state.history) + [action_id]
        new_event_log = list(state.event_log) + emitted_events
        new_turn = state.turn_count + 1

        new_state = state.evolve(
            character=new_char,
            current_region=next_region_id,
            current_scene=next_scene_id,
            world_flags=new_flags,
            history=new_history,
            event_log=new_event_log,
            turn_count=new_turn,
            rng=rng_cursor
        )

        obs = self.observe(new_state, emitted_events)
        return new_state, obs
