# AdventureForge Player Surfaces & MCP Server Rules

Any agent or contributor modifying `adventure_forge/player/` must strictly observe these rules:

---

## 1. Information Firewall (R6 / I6)
- The player surface (`cli.py`, `mcp_server.py`) is the boundary between the internal simulation engine and the player/agent.
- **Whitelist sanitization**: All observations returned to the player must pass through `sanitize_observation`.
- Only return player-visible primitive fields:
  * `success`: boolean
  * `message`: string
  * `status`: "active" | "terminal" | "error"
  * `scene_id`: string
  * `region_id`: string
  * `title`: string
  * `description`: string
  * `events`: list of strings
  * `legal_actions`: list of safe action dictionaries (`id`, `label`, `category`, `risk`, `stamina_cost`)
  * `turn_count`: integer
  * `is_terminal`: boolean
  * `outcome`: string or None
  * `fingerprint`: string
- **Zero leaks**: Never leak internal engine instances (`AdventureEngine`, `GameState`, `CharacterSheet`), raw condition DSL ASTs, hidden world flags, or source file traces.

---

## 2. Unbounded Action Presentation & Pagination
- The presentation layer must support 2 to 200+ actions without truncation.
- CLI must support paginated browsing (default 10 items per page) with category grouping.
- MCP server returns all sanitized legal actions in the `legal_actions` array without arbitrary dropping or trimming.
