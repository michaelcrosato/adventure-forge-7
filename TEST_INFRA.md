# E2E Test Infra: AdventureForge

## Test Philosophy
- Opaque-box, requirement-driven. Derives strictly from `ORIGINAL_REQUEST.md`.
- Methodology: Category-Partition, Boundary Value Analysis (BVA), Pairwise Combinatorial Testing, and Real-World Workload Testing.
- Progressive testability: verification mechanisms do not depend on internal engine implementation details.

## Feature Inventory
| # | Feature | Source | Tier 1 (Coverage) | Tier 2 (Boundary) | Tier 3 (Pairwise) |
|---|---------|--------|:-----------------:|:-----------------:|:-----------------:|
| 1 | Pure Deterministic Kernel | ORIGINAL_REQUEST §R1 | ≥5 tests | ≥5 tests | ✓ |
| 2 | 7-Axis Character Reactivity | ORIGINAL_REQUEST §R2 | ≥5 tests | ≥5 tests | ✓ |
| 3 | Hemingway Prose & Linter | ORIGINAL_REQUEST §R3 | ≥5 tests | ≥5 tests | ✓ |
| 4 | Unbounded Choice Space (100+ actions) | ORIGINAL_REQUEST §R4 | ≥5 tests | ≥5 tests | ✓ |
| 5 | Macro-World Graph & 5 Regional Mechanics | ORIGINAL_REQUEST §R5 | ≥5 tests | ≥5 tests | ✓ |
| 6 | Mechanical Verification Bar & Firewall | ORIGINAL_REQUEST §R6 | ≥5 tests | ≥5 tests | ✓ |

## Test Architecture
- **Test Runner**: `pytest -v` and `./verify` (exit code 0 required).
- **Test Locations**:
  - `tests/unit/`: Module-level tests (state, engine, DSL, linter, triage).
  - `tests/integration/`: Cross-feature tests (character traits + regional mechanics, inventory affordances).
  - `tests/verification/`: Formal proofs (determinism fingerprints, 520-scene BFS crawler reachability, counterfactual witness pairs, 115-action stress scene).
  - `tests/scenarios/`: Multi-step playtester workloads and continental quest progression.
- **Pass/Fail Semantics**: All tests must execute headlessly, deterministically, and exit 0.

## Real-World Application Scenarios (Tier 4)
| # | Scenario | Features Exercised | Complexity |
|---|----------|--------------------|------------|
| 1 | Silas the Cutpurse Infiltration | R1, R2, R4, R5 (Social Stealth) | Medium |
| 2 | Vivienne the High Noble Intrigue | R1, R2, R4, R5 (Court Intrigue) | Medium |
| 3 | Continental Expedition Across 5 Provinces | R1, R4, R5 (520 nodes, all 5 mechanics) | High |
| 4 | Unbounded Bazaar Economic Trade | R1, R4 (115 legal actions, pagination) | High |
| 5 | Playtester Saboteur Stress Simulation | R1, R4, R6 (Flywheel triage, invalid traces) | High |

## Coverage Thresholds
- Tier 1: ≥5 per feature (≥30 tests)
- Tier 2: ≥5 boundary & corner tests per feature (≥30 tests)
- Tier 3: pairwise coverage of major feature interactions (≥10 tests)
- Tier 4: ≥5 realistic application scenarios
