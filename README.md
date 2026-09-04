# AdventureForge: The Unbounded Action Engine

[![Verify](https://github.com/michaelcrosato/adventure-forge-7/actions/workflows/ci.yml/badge.svg)](https://github.com/michaelcrosato/adventure-forge-7)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"Freedom in design. Honesty in verification. The model never is the world."**

AdventureForge is an action-first, deeply reactive open-world RPG engine built on a pure deterministic state transition kernel (`step(state, action, seed_cursor) -> state'`). It combines the geographical travel breadth of **Skyrim** with the systemic, choice-rich depth of **Baldur's Gate 3**.

---

## Key Pillars

1. **Pure Deterministic Authority:** State transitions are 100% pure code. No wall clock, network, or unseeded randomness. Replays reproduce state hashes bit-for-bit.
2. **Deep Multi-Axis Customization:** Characters are defined across at least 6 orthogonal axes (ancestry, background, attributes, traits, flaws, reputation). Content queries character facets dynamically.
3. **High-Velocity Action Prose:** Hemingway baseline (1–3 short sentences, active voice, grade 6-8 reading level, max 18 words/sentence). Action choices dominate the screen.
4. **Unbounded Scene Possibility Space:** Dynamic affordance synthesis supporting 2 to 200+ legal actions without artificial ceilings.
5. **Single Continuous World Graph:** Hierarchical topology (Provinces -> Hubs -> POIs) with region-defining unique mechanics.
6. **Mechanical Verification Bar:** Single non-LLM command `python -m adventure_forge.verify` guarantees determinism, crawler reachability, counterfactual witness proofs, and prose linter gates.
7. **Autonomous Multi-Agent Flywheel:** Unattended self-healing and expansion loop using cost-efficient subagent fleets (Gemini 3.8 Flash benchmark).

---

## Quickstart

### 1. Run the Mechanical Verification Bar
```bash
python3 -m adventure_forge.verification.verify
# or using the entry point:
af-verify
```

### 2. Run Pytest Suite
```bash
pytest -v
```

### 3. Play the Game (CLI)
```bash
python3 -m adventure_forge.player.cli
```

### 4. Run the Autonomous Flywheel
```bash
python3 -m adventure_forge.flywheel.loop --cycles 10
# or:
zu-loop run --cycles 10
```

## Deployment & Vercel Integration

AdventureForge deploys seamlessly to Vercel with zero configuration when imported directly from GitHub:
- **Entrypoints**: `app.py` and `api/index.py` provide stateless ASGI handling.
- **Root Landing Page (`/`)**: Displays live system status, architecture overview, and deployment links.
- **Health Check (`/health`)**: High-velocity machine-readable deployment health monitor returning JSON status.
- **MCP HTTP Surface (`/api/mcp`)**: Streamable Model Context Protocol JSON-RPC 2.0 endpoint over HTTP for AI coding agents.
- **Vercel Plugin & MCP**: Pre-configured in `.agents/plugins/vercel/` and `.agents/mcp_config.json` for agent tool calling and remote Vercel API access (`https://mcp.vercel.com`).

### Local Vercel Preview
```bash
npx vercel dev
```

### Automatic GitHub Sync
The repository includes an automatic post-commit hook in `.githooks/post-commit` configured via `core.hooksPath`. Whenever any commit is made, it is automatically pushed to the remote GitHub repository.
```bash
# Enable hooks if cloning fresh:
git config core.hooksPath .githooks
```

---

## Architecture & Roadmap
Detailed architecture, condition/effect DSL schemas, and execution milestones are documented in [`INITIAL_PLAN.md`](INITIAL_PLAN.md).
