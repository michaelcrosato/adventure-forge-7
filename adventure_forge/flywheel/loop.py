"""Autonomous Flywheel Loop Runner (zu-loop / af-flywheel).

Execution:
    zu-loop run --cycles 10
    python3 -m adventure_forge.flywheel.loop run --cycles 10

Implements Minimal Proof #1:
Runs unattended cycles and records improving retention heuristics and decision volume.
"""
import sys
import argparse
from typing import Optional, List
from adventure_forge.flywheel.orchestrator import OrchestratorManager
from adventure_forge.flywheel.playtester import PlaytesterPersona


def run_loop(
    cycles: int = 10,
    log_path: str = "flywheel_audit.jsonl",
    personas: Optional[List[str]] = None,
) -> bool:
    print("=" * 70)
    persona_desc = f" ({', '.join(personas)})" if personas else " (all 8 personas)"
    print(f"ADVENTUREFORGE AUTONOMOUS FLYWHEEL — RUNNING {cycles} CYCLES{persona_desc}")
    print("=" * 70)

    manager = OrchestratorManager(log_path=log_path, personas=personas)
    all_green = True

    for i in range(1, cycles + 1):
        summary = manager.run_cycle(cycle_num=i)
        if summary.gate_status != "ALL_GREEN":
            all_green = False

        status_icon = "✓" if summary.gate_status == "ALL_GREEN" else "✗"
        print(f"Cycle {i:2d}/{cycles} [{status_icon}] Gates: {summary.gate_status} | "
              f"Sessions: {summary.sessions_run} | "
              f"Decisions: {summary.total_decisions} | "
              f"Avg Retention: {summary.avg_retention:.3f}")

    print("=" * 70)
    retention_trend = [s.avg_retention for s in manager.history]
    print(f"Flywheel Complete. Retention Trend across cycles: {retention_trend}")
    print(f"Audit log persisted to: {log_path}")
    print("=" * 70)
    return all_green


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(description="AdventureForge Autonomous Flywheel Runner (zu-loop)")
    parser.add_argument("command", nargs="?", default="run", help="Command (run)")
    parser.add_argument("--cycles", type=int, default=10, help="Number of unattended cycles to execute")
    parser.add_argument("--log", type=str, default="flywheel_audit.jsonl", help="Log output path")
    parser.add_argument(
        "--persona",
        type=str,
        default=None,
        help=f"Single persona to run (choices: {', '.join(p.value for p in PlaytesterPersona)}, case-insensitive)",
    )
    parser.add_argument(
        "--personas",
        type=str,
        default=None,
        help="Comma-separated or whitespace-separated list of personas to run (case-insensitive)",
    )

    args = parser.parse_args(argv)

    selected_personas: Optional[List[str]] = None
    if args.persona:
        try:
            p_enum = PlaytesterPersona.from_str(args.persona)
            selected_personas = [p_enum.value]
        except ValueError as e:
            parser.error(str(e))
    elif args.personas:
        try:
            raw_list = [p.strip() for p in args.personas.replace(",", " ").split() if p.strip()]
            selected_personas = [PlaytesterPersona.from_str(p).value for p in raw_list]
        except ValueError as e:
            parser.error(str(e))

    success = run_loop(cycles=args.cycles, log_path=args.log, personas=selected_personas)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
