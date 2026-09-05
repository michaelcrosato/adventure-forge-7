---
name: af-player-mcp
description: >-
  Use this skill when testing or interacting with the game as a player via the
  AdventureForge MCP server tools (new_game, step_game, get_state) under the
  I6 Information Firewall.
---

# AdventureForge Player MCP Server Runbook

This skill describes how an AI agent can interact with AdventureForge using the Model Context Protocol (MCP) server tools under the **I6 Information Firewall**.

---

## 1. Available MCP Player Tools

The AdventureForge MCP server exposes 3 core tools to agents:

### 1. `new_game`
Starts a fresh adventure with a chosen character preset and optional seed.
- **Arguments**:
  * `preset` (string, optional, default: `"cutpurse"`):
    - `"cutpurse"` (Silas: stealth, agility, lockpicking)
    - `"noble"` (Vivienne: court intrigue, high charisma, wealth)
    - `"warrior"` (Kael: physical strength, heavy weapons, intimidation)
    - `"pit_fighter"` (Torin: unarmed combat, endurance, streetwise)
    - `"scholar"` (Mara: history, arcana, languages)
    - `"ranger"` (Eamon: survival, tracking, archery)
  * `seed` (integer, optional): Deterministic PRNG seed.
- **Returns**: Sanitized initial `StepResult` dictionary.

### 2. `step_game`
Executes an action from the currently available legal actions.
- **Arguments**:
  * `action_id` (string, required): The unique identifier of the chosen legal action (from `legal_actions[].id`).
- **Returns**: Sanitized `StepResult` dictionary with updated scene, narrative event prose, and new legal actions.

### 3. `get_state`
Retrieves the current player-visible state observation.
- **Arguments**: None.
- **Returns**: Current sanitized `StepResult` dictionary.

---

## 2. Information Firewall Compliance (I6)

When acting as an agent player:
1. **Never read raw state objects**: Rely solely on the observation dictionary returned by MCP tools.
2. **Never inspect source code to solve scenes**: Treat puzzles, choices, and encounters as black-box narrative situations.
3. **Observation Fields Available**:
   - `title`: Current location name.
   - `description`: Hemingway-compliant scene description.
   - `events`: Recent action outcome narrative.
   - `legal_actions`: Array of action objects with `id`, `label`, `category`, `risk`, `stamina_cost`.
   - `status`: `"active"`, `"terminal"`, or `"error"`.
   - `fingerprint`: Current deterministic state hash.

---

## 3. Running MCP Server Manually
```bash
# Stdio server
python3 -m adventure_forge.player.mcp_server

# Test via python interactive prompt
python3 -c "
from adventure_forge.player.mcp_server import new_game, step_game
obs = new_game('cutpurse')
print('Scene:', obs['scene_id'])
print('Actions:', [a['label'] for a in obs['legal_actions'][:5]])
"
```
