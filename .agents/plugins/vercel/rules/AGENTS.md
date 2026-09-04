# Vercel Deployment & Runtime Rules

## Deployment Constraints & Standards

1. **Pure Stateless Architecture:**
   - Functions run in ephemeral environments. Never rely on in-memory mutable state across requests or local filesystem persistence across function invocations.
   - For AdventureForge, any persistent save state should be serialized via client tokens or database storage.

2. **Entrypoints & Detection:**
   - The primary ASGI entrypoint is `app.py` with top-level callable `app`.
   - Vercel function routing maps requests via `api/index.py` and `vercel.json` rewrites.
   - Any modifications to the entrypoint must preserve the health check endpoint `/health` returning JSON with keys `service`, `status`, and `version`.
   - Support both `GET` and `HEAD` requests gracefully.

3. **Dependency & Bundle Management:**
   - Keep runtime dependencies lean (prefer Python standard library where possible).
   - In `vercel.json`, maintain `excludeFiles` to keep bundle size minimal and omit test fixtures, caches, and agent logs.

4. **MCP Server Integration:**
   - The Vercel MCP server is accessible at `https://mcp.vercel.com`.
   - Local AdventureForge MCP server runs over stdio via `python3 -m adventure_forge.player.mcp_server`.
