"""Evidence-Based Defect Triage and Replay Verifier.

Enforces SYS-07 / Minimal Proof #7:
- Replays reported bug traces before admitting them as verified defects.
- Unreplayable or fabricated reports are rejected with deterministic proof.
- Automatically ingests playtester telemetry and friction notes.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from adventure_forge.core.character import CharacterSheet, get_preset
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry


@dataclass
class PlaytesterDefectReport:
    """A defect claim submitted by a blind playtester or test agent."""
    claimed_defect: str
    action_trace: List[str]
    start_scene: str
    initial_char: CharacterSheet
    seed: int = 42
    persona: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claimed_defect": self.claimed_defect,
            "action_trace": list(self.action_trace),
            "start_scene": self.start_scene,
            "seed": self.seed,
            "persona": self.persona,
            "metadata": dict(self.metadata),
        }


@dataclass
class TriageReport:
    """Deterministic verification result of a reported defect trace."""
    verified: bool
    status: str  # VERIFIED_DEFECT, VERIFIED_REPLAY, REJECTED_UNREPLAYABLE, CRASH_DEFECT, or FINGERPRINT_MISMATCH
    reproduction_trace: List[str]
    final_fingerprint: str
    details: str
    error_step: Optional[int] = None
    failing_scene: Optional[str] = None
    expected_fingerprint: Optional[str] = None

    @property
    def actual_fingerprint(self) -> str:
        """The final state SHA-256 fingerprint after trace execution."""
        return self.final_fingerprint

    @property
    def matches_expected(self) -> bool:
        """Whether the reproduction matched the expected defect verification."""
        if self.expected_fingerprint is not None:
            return (self.actual_fingerprint == self.expected_fingerprint) and self.verified
        return self.verified

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verified": self.verified,
            "status": self.status,
            "reproduction_trace": list(self.reproduction_trace),
            "final_fingerprint": self.final_fingerprint,
            "actual_fingerprint": self.actual_fingerprint,
            "expected_fingerprint": self.expected_fingerprint,
            "matches_expected": self.matches_expected,
            "details": self.details,
            "error_step": self.error_step,
            "failing_scene": self.failing_scene,
        }


def extract_defect_reports_from_telemetry(
    telemetry: Any,
    initial_char: CharacterSheet,
    start_scene: Optional[str] = None
) -> List[PlaytesterDefectReport]:
    """Extract structured defect reports from a BlindPlaytester SessionTelemetry."""
    reports: List[PlaytesterDefectReport] = []
    scenes = getattr(telemetry, "scenes_visited", [])
    resolved_start = start_scene or (scenes[0] if scenes else "crags_base")
    decisions = getattr(telemetry, "decisions_made", [])
    seed = getattr(telemetry, "seed", 42)
    persona = getattr(telemetry, "persona", "unknown")
    friction_notes = getattr(telemetry, "friction_notes", [])

    for note in friction_notes:
        reports.append(PlaytesterDefectReport(
            claimed_defect=note,
            action_trace=list(decisions),
            start_scene=resolved_start,
            initial_char=initial_char,
            seed=seed,
            persona=persona,
            metadata={"turn_count": getattr(telemetry, "turn_count", len(decisions))}
        ))
    return reports


def triage_defect_report(
    initial_char: CharacterSheet,
    start_scene: str,
    action_trace: List[str],
    claimed_defect: str,
    seed: int = 42,
    engine: Optional[AdventureEngine] = None,
) -> TriageReport:
    """Attempt to deterministically reproduce a reported defect."""
    if engine is None:
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

    # Always initialize observation so obs is never unbound
    obs = engine.observe(state)
    if not obs.success:
        return TriageReport(
            verified=True,
            status="VERIFIED_DEFECT",
            reproduction_trace=[],
            final_fingerprint=state.fingerprint(),
            details=f"Initial scene observation failed: {obs.message}",
            error_step=0,
            failing_scene=start_scene
        )

    reproduced = False
    details = ""
    error_step: Optional[int] = None
    executed_trace: List[str] = []

    for idx, act in enumerate(action_trace):
        executed_trace.append(act)
        try:
            state, obs = engine.step(state, act)
        except Exception as exc:
            reproduced = True
            error_step = idx
            details = f"Engine exception at step {idx} on action '{act}': {type(exc).__name__}: {exc}"
            return TriageReport(
                verified=True,
                status="CRASH_DEFECT",
                reproduction_trace=executed_trace,
                final_fingerprint=state.fingerprint(),
                details=f"Defect reproduced with crash: {details}",
                error_step=error_step,
                failing_scene=state.current_scene
            )

        if not obs.success:
            reproduced = True
            error_step = idx
            details = f"Action '{act}' failed at step {idx}: {obs.message}"
            break

    if not reproduced:
        # Check for deadlock / softlock in final scene
        defect_lower = claimed_defect.lower()
        is_deadlock_claim = any(
            term in defect_lower for term in ("deadlock", "softlock", "dead end", "no legal actions", "stuck")
        )
        if (is_deadlock_claim or len(obs.legal_actions) == 0) and len(obs.legal_actions) == 0 and not obs.is_terminal:
            reproduced = True
            error_step = len(executed_trace)
            details = f"Deadlock confirmed at scene {obs.scene_id}: zero legal actions in non-terminal scene."

    if reproduced:
        return TriageReport(
            verified=True,
            status="VERIFIED_DEFECT",
            reproduction_trace=executed_trace,
            final_fingerprint=state.fingerprint(),
            details=f"Defect reproduced deterministically: {details}",
            error_step=error_step,
            failing_scene=obs.scene_id
        )
    else:
        return TriageReport(
            verified=False,
            status="REJECTED_UNREPLAYABLE",
            reproduction_trace=executed_trace,
            final_fingerprint=state.fingerprint(),
            details="Report rejected. Trace executed successfully without error or deadlock. Claims could not be reproduced.",
            error_step=None,
            failing_scene=None
        )


def triage_playtester_report(report: PlaytesterDefectReport) -> TriageReport:
    """Triage a structured PlaytesterDefectReport."""
    return triage_defect_report(
        initial_char=report.initial_char,
        start_scene=report.start_scene,
        action_trace=report.action_trace,
        claimed_defect=report.claimed_defect,
        seed=report.seed
    )


def triage_session_telemetry(
    telemetry: Any,
    initial_char: CharacterSheet,
    start_scene: Optional[str] = None,
    engine: Optional[AdventureEngine] = None,
) -> Optional[TriageReport]:
    """Triage friction notes or rejected actions from playtester session telemetry."""
    friction_notes = getattr(telemetry, "friction_notes", [])
    if not friction_notes:
        return None
    scenes = getattr(telemetry, "scenes_visited", [])
    resolved_start = start_scene or (scenes[0] if scenes else "crags_base")
    claimed = "; ".join(friction_notes)
    return triage_defect_report(
        initial_char=initial_char,
        start_scene=resolved_start,
        action_trace=list(getattr(telemetry, "decisions_made", [])),
        claimed_defect=claimed,
        seed=getattr(telemetry, "seed", 42),
        engine=engine,
    )


def reproduce_trace(
    seed: int,
    preset: str,
    action_sequence: List[str],
    start_scene: Optional[str] = None,
    engine: Optional[AdventureEngine] = None,
    claimed_defect: Optional[str] = None,
    expected_fingerprint: Optional[str] = None,
) -> TriageReport:
    """Deterministically replay an action sequence from a character preset and verify outcome.

    Satisfies af-playtest/SKILL.md defect triage harness.
    """
    try:
        preset_data = get_preset(preset)
        initial_char = preset_data.character
        resolved_start = start_scene or preset_data.start_scene
    except KeyError:
        from adventure_forge.flywheel.orchestrator import get_canonical_persona_setup
        initial_char, default_start = get_canonical_persona_setup(preset)
        resolved_start = start_scene or default_start

    if claimed_defect is not None:
        report = triage_defect_report(
            initial_char=initial_char,
            start_scene=resolved_start,
            action_trace=action_sequence,
            claimed_defect=claimed_defect,
            seed=seed,
            engine=engine,
        )
    else:
        if engine is None:
            registry = build_world_registry()
            engine = AdventureEngine(registry)

        state = GameState(
            build_id="af-build-001",
            session_id="triage-replay",
            character=initial_char,
            current_region=engine.get_region_id_for_scene(resolved_start) or "iron_crags",
            current_scene=resolved_start,
            rng=DeterministicRNG.from_seed(seed)
        )

        try:
            obs = engine.observe(state)
        except Exception as exc:
            report = TriageReport(
                verified=True,
                status="CRASH_DEFECT",
                reproduction_trace=[],
                final_fingerprint=state.fingerprint(),
                details=f"Engine exception during initial observation: {type(exc).__name__}: {exc}",
                error_step=0,
                failing_scene=resolved_start,
            )
            obs = None  # type: ignore[assignment]

        if obs is not None:
            if not obs.success:
                report = TriageReport(
                    verified=True,
                    status="VERIFIED_DEFECT",
                    reproduction_trace=[],
                    final_fingerprint=state.fingerprint(),
                    details=f"Initial scene observation failed: {obs.message}",
                    error_step=0,
                    failing_scene=resolved_start,
                )
            else:
                executed_trace: List[str] = []
                failed = False
                for idx, act in enumerate(action_sequence):
                    executed_trace.append(act)
                    try:
                        state, obs = engine.step(state, act)
                    except Exception as exc:
                        failed = True
                        report = TriageReport(
                            verified=True,
                            status="CRASH_DEFECT",
                            reproduction_trace=executed_trace,
                            final_fingerprint=state.fingerprint(),
                            details=f"Engine exception at step {idx} on action '{act}': {type(exc).__name__}: {exc}",
                            error_step=idx,
                            failing_scene=state.current_scene,
                        )
                        break

                    if not obs.success:
                        failed = True
                        report = TriageReport(
                            verified=True,
                            status="VERIFIED_DEFECT",
                            reproduction_trace=executed_trace,
                            final_fingerprint=state.fingerprint(),
                            details=f"Defect reproduced deterministically: Action '{act}' failed at step {idx}: {obs.message}",
                            error_step=idx,
                            failing_scene=obs.scene_id,
                        )
                        break

                if not failed:
                    # Check for deadlock in non-terminal scene with 0 legal actions
                    if len(obs.legal_actions) == 0 and not obs.is_terminal:
                        report = TriageReport(
                            verified=True,
                            status="VERIFIED_DEFECT",
                            reproduction_trace=executed_trace,
                            final_fingerprint=state.fingerprint(),
                            details=f"Deadlock detected at scene {obs.scene_id}: zero legal actions in non-terminal scene.",
                            error_step=len(executed_trace),
                            failing_scene=obs.scene_id,
                        )
                    else:
                        report = TriageReport(
                            verified=True,
                            status="VERIFIED_REPLAY",
                            reproduction_trace=executed_trace,
                            final_fingerprint=state.fingerprint(),
                            details=f"Trace executed successfully ({len(executed_trace)} steps). Clean deterministic replay verified.",
                            error_step=None,
                            failing_scene=None,
                        )

    if expected_fingerprint is not None:
        report.expected_fingerprint = expected_fingerprint
        if report.actual_fingerprint != expected_fingerprint:
            report.verified = False
            report.status = "FINGERPRINT_MISMATCH"
            report.details = f"Fingerprint mismatch: expected {expected_fingerprint}, got {report.actual_fingerprint}"
        else:
            if report.status == "VERIFIED_REPLAY":
                report.verified = True

    return report

