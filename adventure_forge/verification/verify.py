"""Unified Mechanical Verification Bar.

Execution:
    python3 -m adventure_forge.verification.verify

Invariants Enforced (No LLM required):
- I1: Pure Determinism and Replay Fingerprint Matching
- I2/SYS-02: Link Validation and Closed DSL Schema Integrity
- G2: Plain-Speech and Hemingway Baseline Prose Linter
- I4/G1/G3: Counterfactual Character Sheet Witness Divergence
- G6: Choice Unboundedness (100+ actions in single scene)
- SYS-05: Non-LLM BFS/DFS Reachability Crawler
- R5/SYS-06: Macro-World Interactable Density Invariant (>= 260 scenes with >= 3 interactables)
"""
import sys
from adventure_forge.content.loader import build_world_registry, validate_world_links
from adventure_forge.linter.prose_linter import ProseLinter
from adventure_forge.verification.determinism import verify_replay_determinism
from adventure_forge.verification.counterfactual import verify_counterfactual_divergence
from adventure_forge.verification.stress import verify_large_action_set
from adventure_forge.verification.crawler import crawl_world_graph
from adventure_forge.verification.density import verify_interactable_density


def run_all_verification(verbose: bool = True) -> bool:
    print("=" * 70)
    print("ADVENTUREFORGE MECHANICAL VERIFICATION BAR")
    print("=" * 70)
    registry = build_world_registry()

    checks = []

    # 1. Determinism & Replay
    print("[1/7] Verifying I1 Determinism & Replay Fingerprint...")
    ok_det, msg_det = verify_replay_determinism()
    checks.append(("I1 Determinism", ok_det, msg_det))
    print(f"      {'✓ PASS' if ok_det else '✗ FAIL'}: {msg_det}")

    # 2. Link Resolution
    print("[2/7] Verifying World Graph Link Integrity...")
    ok_links, link_errs = validate_world_links(registry)
    msg_links = "All cross-scene and entity links resolved." if ok_links else f"Broken links: {link_errs}"
    checks.append(("Graph Link Integrity", ok_links, msg_links))
    print(f"      {'✓ PASS' if ok_links else '✗ FAIL'}: {msg_links}")

    # 3. Plain-Speech Prose Linter
    print("[3/7] Verifying G2 High-Velocity Hemingway Prose Linter...")
    linter = ProseLinter()
    ok_lint, lint_errs = linter.lint_registry(registry)
    msg_lint = "Prose strictly conforms to Hemingway baseline (<=18 words/sent)." if ok_lint else f"{len(lint_errs)} prose violations."
    checks.append(("G2 Prose Linter", ok_lint, msg_lint))
    print(f"      {'✓ PASS' if ok_lint else '✗ FAIL'}: {msg_lint}")
    if not ok_lint and verbose:
        for err in lint_errs[:5]:
            print(f"        - {err}")

    # 4. Counterfactual Witness Divergence
    print("[4/7] Verifying I4/G1/G3 Counterfactual Character Divergence...")
    ok_count, msg_count, _ = verify_counterfactual_divergence()
    checks.append(("I4 Counterfactual Divergence", ok_count, msg_count))
    print(f"      {'✓ PASS' if ok_count else '✗ FAIL'}: {msg_count}")

    # 5. Choice Unboundedness Stress
    print("[5/7] Verifying G6 Unbounded Choice Scaling (100+ Legal Actions)...")
    ok_stress, msg_stress, _ = verify_large_action_set()
    checks.append(("G6 Unbounded Choices", ok_stress, msg_stress))
    print(f"      {'✓ PASS' if ok_stress else '✗ FAIL'}: {msg_stress}")

    # 6. Non-LLM Reachability Crawler
    print("[6/7] Verifying SYS-05 Non-LLM Reachability Crawler...")
    ok_crawl, msg_crawl, _ = crawl_world_graph()
    checks.append(("SYS-05 Reachability Crawler", ok_crawl, msg_crawl))
    print(f"      {'✓ PASS' if ok_crawl else '✗ FAIL'}: {msg_crawl}")

    # 7. Macro-World Interactable Density Invariant
    print("[7/7] Verifying SYS-06 Macro-World Interactable Density Invariant (>= 260 scenes)...")
    ok_density, msg_density, _ = verify_interactable_density(registry)
    checks.append(("SYS-06 Interactable Density", ok_density, msg_density))
    print(f"      {'✓ PASS' if ok_density else '✗ FAIL'}: {msg_density}")

    print("=" * 70)
    all_passed = all(c[1] for c in checks)
    if all_passed:
        print("VERIFICATION RESULT: ALL GATES GREEN ✓")
        print("The repository satisfies all hard engine invariants.")
    else:
        print("VERIFICATION RESULT: VERIFICATION FAILED ✗")
        failed = [c[0] for c in checks if not c[1]]
        print(f"Failed gates: {', '.join(failed)}")
    print("=" * 70)
    return all_passed


def main():
    passed = run_all_verification(verbose=True)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
