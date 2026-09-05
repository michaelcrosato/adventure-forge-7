---
name: af-verify
description: >-
  Use this skill when running the AdventureForge mechanical verification bar,
  executing the pytest suite, running static lint/type checks (ruff, mypy), or
  diagnosing test and verification failures across the 7 gates.
---

# AdventureForge Verification & Quality Runbook

This skill provides step-by-step instructions for executing the mechanical verification bar, the pytest suite, and static analysis checks, as well as gate-by-gate troubleshooting.

---

## 1. Fast Health Check Command
Run this sequence to verify the entire repository:
```bash
./verify && pytest -v && ruff check . && mypy adventure_forge
```

---

## 2. The 7 Verification Gates (`./verify`)

The canonical verification command is `./verify` (or `python3 -m adventure_forge.verify`). It enforces 7 non-negotiable gates:

| Gate | Name | What it Verifies | Failure Diagnosis |
| :--- | :--- | :--- | :--- |
| **[1/7]** | `I1 Determinism & Replay` | Bit-for-bit replay hash consistency across seeds. | Check for unseeded PRNG, floating-point drift, or dict ordering issues in state fingerprint. |
| **[2/7]** | `World Graph Link Integrity` | All scene exit targets and entity IDs resolve. | Inspect `adventure_forge/content/loader.py` or province files for typos in scene IDs. |
| **[3/7]** | `G2 Hemingway Prose Linter` | Word count <=18, 1–3 sentences, FKGL Grade 6–8, UI labels <=3 words, zero purple words. | Run prose linter directly (see below) to locate violating sentence or label. |
| **[4/7]** | `I4/G1/G3 Counterfactual Divergence` | Silas (Cutpurse) vs. Vivienne (Noble) yield distinct legal actions/dialogue in opening scene. | Verify character traits/skills are queried by scene affordance conditions. |
| **[5/7]** | `G6 Unbounded Choice Scaling` | Scene `bazaar_center` generates 100+ legal actions without crash or truncation. | Check dynamic affordance generator in `adventure_forge/content/data/provinces/lowlands.py`. |
| **[6/7]** | `SYS-05 Reachability Crawler` | Non-LLM BFS crawler proves 100% reachability across all 520 scenes. | Run crawler standalone to see disconnected scene IDs: `python3 -m adventure_forge.verification.crawler`. |
| **[7/7]** | `SYS-06 Interactable Density` | At least 260 of 520 scenes offer >= 3 meaningful interactables/entities. | Check scene entity count and non-movement base actions in province files. |

---

## 3. Targeted Diagnostic Commands

### Diagnosing Prose Linter Failures
Run the prose linter directly on the world registry:
```bash
python3 -c "
from adventure_forge.linter.prose_linter import ProseLinter
from adventure_forge.content.loader import build_world_registry

linter = ProseLinter()
registry = build_world_registry()
violations = linter.lint_registry(registry)
for scene_id, errs in violations.items():
    print(f'=== Scene {scene_id} ===')
    for e in errs:
        print(f'  - {e}')
"
```

### Diagnosing Crawler / Reachability Issues
Run the BFS crawler standalone:
```bash
python3 -c "
from adventure_forge.verification.crawler import BFSReachabilityCrawler
from adventure_forge.content.loader import build_world_registry

registry = build_world_registry()
crawler = BFSReachabilityCrawler(registry)
reachable, total, unreachable = crawler.crawl_all()
print(f'Reachable: {reachable}/{total}')
if unreachable:
    print('Unreachable scenes:', unreachable[:10])
"
```

### Running Specific Pytest Tiers
```bash
# Tier 1 & 2: Unit tests
pytest tests/unit/ -v

# Tier 3: Integration tests
pytest tests/integration/ -v

# Tier 4: Scenario playtests
pytest tests/scenarios/ -v

# Tier 5: Adversarial verification proofs
pytest tests/verification/ -v
```

---

## 4. Verification Check Before Concluding Any Task
Always guarantee:
1. `./verify` exits with code 0.
2. `pytest` passes with 0 failures.
3. `ruff check .` returns clean.
4. `mypy adventure_forge` returns clean.
