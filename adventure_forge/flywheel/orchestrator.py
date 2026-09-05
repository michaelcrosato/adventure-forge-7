"""Repository Orchestrator and Manager Agent.

Manages:
- Flywheel monitoring and subagent task scheduling.
- Retention curves and hotspot discovery.
- Workflow mutation and self-healing patches.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple
import json
from adventure_forge.core.character import CharacterSheet, get_preset
from adventure_forge.flywheel.playtester import BlindPlaytester, SessionTelemetry
from adventure_forge.flywheel.triage import triage_session_telemetry
from adventure_forge.verification.verify import run_all_verification


@dataclass
class FlywheelCycleSummary:
    cycle_index: int
    gate_status: str
    sessions_run: int
    avg_retention: float
    total_decisions: int
    hotspots: List[str] = field(default_factory=list)
    triage_results: List[Dict[str, Any]] = field(default_factory=list)


def get_canonical_persona_setup(persona: str) -> Tuple[CharacterSheet, str]:
    """Map persona to canonical preset character and regional start scene."""
    p = persona.lower().strip()
    if p == "explorer":
        # explorer -> Silas (cutpurse, crags_base)
        return get_preset("cutpurse").character, "crags_base"
    elif p == "brute":
        # brute -> Garron (warrior, crags_base)
        return get_preset("warrior").character, "crags_base"
    elif p == "infiltrator":
        # infiltrator -> Silas (cutpurse, warrens_gate)
        return get_preset("cutpurse").character, "warrens_gate"
    elif p == "speedrunner":
        # speedrunner -> Torin (scout, reach_hub)
        return get_preset("scout").character, "reach_hub"
    elif p == "saboteur":
        # saboteur -> Silas (cutpurse + pyromaniac, torch, acid_vial, warrens_gate)
        silas = get_preset("cutpurse").character
        traits = list(silas.traits)
        if "pyromaniac" not in traits:
            traits.append("pyromaniac")
        inventory = list(silas.inventory)
        for item in ("torch", "acid_vial"):
            if item not in inventory:
                inventory.append(item)
        return silas.modify(traits=traits, inventory=inventory), "warrens_gate"
    elif p == "nomad":
        # nomad -> Kael (nomad, scorch_oasis)
        return get_preset("nomad").character, "scorch_oasis"
    elif p == "diver":
        # diver -> Mara (diver, hollows_grotto)
        return get_preset("diver").character, "hollows_grotto"
    elif p == "scout":
        # scout -> Torin (scout, reach_hub)
        return get_preset("scout").character, "reach_hub"
    else:
        return get_preset("cutpurse").character, "crags_base"


class OrchestratorManager:
    """The central manager agent governing repository velocity and game quality."""

    def __init__(self, log_path: str = "flywheel_audit.jsonl"):
        self.log_path = log_path
        self.history: List[FlywheelCycleSummary] = []
        self.personas = [
            "explorer",
            "brute",
            "infiltrator",
            "speedrunner",
            "saboteur",
            "nomad",
            "diver",
            "scout",
        ]

    def run_cycle(self, cycle_num: int) -> FlywheelCycleSummary:
        # 1. Run Mechanical Verification Bar
        gates_green = run_all_verification(verbose=False)
        gate_status = "ALL_GREEN" if gates_green else "GATES_FAILED"

        # 2. Deploy Blind Playtester Fleet across personas
        telemetries: List[SessionTelemetry] = []
        total_decisions = 0
        total_retention = 0.0

        hotspots: List[str] = []
        triage_results: List[Dict[str, Any]] = []

        for p_idx, persona in enumerate(self.personas):
            char, start_scene = get_canonical_persona_setup(persona)
            tester = BlindPlaytester(persona=persona, seed=cycle_num * 100 + p_idx)
            tel = tester.run_session(char, start_scene=start_scene, max_turns=15)
            telemetries.append(tel)
            total_decisions += tel.turn_count
            total_retention += tel.retention_score

            if tel.friction_notes:
                hotspots.extend(tel.friction_notes)
                triage_rep = triage_session_telemetry(tel, char, start_scene=start_scene)
                if triage_rep:
                    triage_results.append(triage_rep.to_dict())

        avg_retention = round(total_retention / len(telemetries), 3)

        summary = FlywheelCycleSummary(
            cycle_index=cycle_num,
            gate_status=gate_status,
            sessions_run=len(telemetries),
            avg_retention=avg_retention,
            total_decisions=total_decisions,
            hotspots=hotspots,
            triage_results=triage_results
        )
        self.history.append(summary)
        self._record_audit(summary)
        return summary

    def _record_audit(self, summary: FlywheelCycleSummary):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "cycle": summary.cycle_index,
                "gate_status": summary.gate_status,
                "sessions_run": summary.sessions_run,
                "avg_retention": summary.avg_retention,
                "total_decisions": summary.total_decisions,
                "hotspots": summary.hotspots,
                "triage_results": summary.triage_results
            }) + "\n")


