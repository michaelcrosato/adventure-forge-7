"""Evidence-Based Defect Triage and Replay Verifier.

Enforces SYS-07 / Minimal Proof #7:
- Replays reported bug traces before admitting them as verified defects.
- Unreplayable or fabricated reports are rejected with deterministic proof.
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
from adventure_forge.core.character import CharacterSheet
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry


@dataclass
class TriageReport:
    verified: bool
    status: str
    reproduction_trace: List[str]
    final_fingerprint: str
    details: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verified": self.verified,
            "status": self.status,
            "reproduction_trace": list(self.reproduction_trace),
            "final_fingerprint": self.final_fingerprint,
            "details": self.details,
        }


def triage_defect_report(
    initial_char: CharacterSheet,
    start_scene: str,
    action_trace: List[str],
    claimed_defect: str,
    seed: int = 42
) -> TriageReport:
    """Attempt to deterministically reproduce a reported defect."""
    registry = build_world_registry()
    engine = AdventureEngine(registry)

    state = GameState(
        build_id="af-build-001",
        session_id="triage-replay",
        character=initial_char,
        current_region=engine.get_region_id_for_scene(start_scene) or "iron_crags",
        current_scene=start_scene,
        rng=DeterministicRNG.from_seed(seed)
    )

    reproduced = False
    details = ""

    for idx, act in enumerate(action_trace):
        state, obs = engine.step(state, act)
        if not obs.success:
            reproduced = True
            details = f"Action '{act}' failed at step {idx}: {obs.message}"
            break

    if not reproduced:
        # Check if claimed defect matched any recorded events or deadlocks
        if "deadlock" in claimed_defect and len(obs.legal_actions) == 0 and not obs.is_terminal:
            reproduced = True
            details = f"Deadlock confirmed at scene {obs.scene_id}: zero legal actions in non-terminal scene."

    if reproduced:
        return TriageReport(
            verified=True,
            status="VERIFIED_DEFECT",
            reproduction_trace=action_trace,
            final_fingerprint=state.fingerprint(),
            details=f"Defect reproduced deterministically: {details}"
        )
    else:
        return TriageReport(
            verified=False,
            status="REJECTED_UNREPLAYABLE",
            reproduction_trace=action_trace,
            final_fingerprint=state.fingerprint(),
            details=f"Report rejected. Trace executed successfully without error or deadlock. Claims could not be reproduced."
        )
