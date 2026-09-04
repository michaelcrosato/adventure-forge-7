---
name: vercel
description: Guidelines and runbooks for deploying, configuring, and verifying Vercel deployments and MCP integration.
---

# Vercel Deployment & MCP Skill

This skill guides deployment, testing, and operation of AdventureForge on Vercel.

## 1. Zero-Config GitHub Import
When importing this repository into Vercel from GitHub:
- **Framework Preset**: Automatically detected as Python (or select "Other" with zero config).
- **Root Directory**: `./`
- **Build Command**: None required (or `python3 -m adventure_forge.verification.verify`).
- **Output Directory**: Automatically handled by Vercel Functions.
- **Entrypoints**:
  - `app.py` (ASGI application exported as `app`)
  - `api/index.py` (Serverless Function bridge)

## 2. Local Preview with Vercel CLI
Test your deployment locally with the Vercel CLI:
```bash
# Start local dev server emulating Vercel runtime
npx vercel dev
```

## 3. Remote Vercel MCP Server
Vercel's official Model Context Protocol server:
- **Endpoint**: `https://mcp.vercel.com`
- **Capabilities**: Project management, deployment logs, build status, analytics queries.
- **CLI Connection**: `npx -y mcp-remote https://mcp.vercel.com`

## 4. Verification Check
Always test deployment endpoints before pushing:
```bash
pytest tests/test_vercel_app.py
```
Ensure `/health` returns `200 OK` with valid JSON metadata.
