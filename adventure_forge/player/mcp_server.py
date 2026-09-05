"""Agent Model Context Protocol (MCP) Player Surface.

Enforces:
- R4: Dynamic affordance synthesis with unbounded legal actions (no artificial truncation).
- R6 / I6: Information Firewall — returns only player-visible StepResult fields
  (scene id, prose, legal actions, status), never internal source code or raw engine objects.
- Interface Contract:
  new_game(preset: str) -> Dict
  step_game(action_id: str) -> Dict
  get_state() -> Dict
"""
import sys
import json
from typing import Dict, Any, List, Optional
from adventure_forge.core.character import get_preset, list_presets
from adventure_forge.core.state import GameState
from adventure_forge.core.engine import AdventureEngine, StepResult
from adventure_forge.core.rng import DeterministicRNG
from adventure_forge.content.loader import build_world_registry


def sanitize_observation(obs: StepResult) -> Dict[str, Any]:
    """Sanitize StepResult to enforce the I6 Information Firewall.

    Guarantees:
    - Whitelists only player-visible primitive fields.
    - Zero internal engine references (no GameState, AdventureEngine, CharacterSheet).
    - Zero condition DSL rules or effect mutation payloads leaked.
    - Zero hidden world flags leaked.
    - Zero source code paths or raw stack traces.
    """
    safe_actions: List[Dict[str, Any]] = []
    for act in obs.legal_actions:
        safe_actions.append({
            "id": str(act["id"]),
            "label": str(act.get("label", act["id"])),
            "category": str(act.get("category", "general")),
            "risk": str(act.get("risk", "low")),
            "stamina_cost": int(act.get("stamina_cost", 0)),
        })

    if obs.is_terminal:
        status_str = "terminal"
    elif not obs.success:
        status_str = "error"
    else:
        status_str = "active"

    return {
        "success": bool(obs.success),
        "message": str(obs.message),
        "status": status_str,
        "scene_id": str(obs.scene_id),
        "region_id": str(obs.region_id),
        "title": str(obs.title),
        "description": str(obs.description),
        "events": [str(ev) for ev in obs.events],
        "legal_actions": safe_actions,
        "turn_count": int(obs.turn_count),
        "is_terminal": bool(obs.is_terminal),
        "outcome": str(obs.outcome) if obs.outcome is not None else None,
        "fingerprint": str(obs.fingerprint),
    }


def error_observation(message: str, status: str = "error") -> Dict[str, Any]:
    """Return a firewall-compliant error observation dictionary."""
    return {
        "success": False,
        "message": str(message),
        "status": status,
        "scene_id": "",
        "region_id": "",
        "title": "",
        "description": "",
        "events": [],
        "legal_actions": [],
        "turn_count": 0,
        "is_terminal": False,
        "outcome": None,
        "fingerprint": "",
    }


class MCPServer:
    """Model Context Protocol server and state container for AdventureForge."""

    def __init__(
        self,
        seed: int = 999,
        registry: Optional[Dict[str, Any]] = None,
        engine: Optional[AdventureEngine] = None,
    ):
        self.default_seed = seed
        if engine is not None:
            self.engine = engine
            self._registry = registry or engine.world_registry
        else:
            self._registry = registry or build_world_registry()
            self.engine = AdventureEngine(self._registry)
        self.state: Optional[GameState] = None
        self.last_obs: Optional[StepResult] = None

    def reset(self) -> None:
        """Reset active session state."""
        self.state = None
        self.last_obs = None

    def new_game(self, preset: str = "cutpurse", seed: Optional[int] = None) -> Dict[str, Any]:
        """Start a new game with the designated character preset."""
        if not isinstance(preset, str):
            preset = "cutpurse"
        try:
            char_preset = get_preset(preset)
        except KeyError:
            return error_observation(
                f"Unknown preset '{preset}'. Available presets: {list_presets()}"
            )

        effective_seed = seed if seed is not None else self.default_seed
        self.state = GameState(
            build_id="af-build-001",
            session_id=f"mcp-session-{char_preset.id}",
            character=char_preset.character,
            current_region=char_preset.start_region,
            current_scene=char_preset.start_scene,
            rng=DeterministicRNG.from_seed(effective_seed),
        )
        self.last_obs = self.engine.observe(self.state)
        return sanitize_observation(self.last_obs)

    def step_game(self, action_id: str) -> Dict[str, Any]:
        """Execute a canonical action against the active game session."""
        if self.state is None:
            return error_observation("No active game session. Call new_game() first.")

        if self.last_obs and self.last_obs.is_terminal:
            return error_observation(
                f"Game has concluded ({self.last_obs.outcome or 'terminal'}). Call new_game() to restart.",
                status="terminal",
            )

        new_state, obs = self.engine.step(self.state, action_id)
        if obs.success:
            self.state = new_state
        self.last_obs = obs
        return sanitize_observation(obs)

    def get_state(self) -> Dict[str, Any]:
        """Get the current player-visible state observation."""
        if self.state is None:
            return error_observation("No active game session. Call new_game() first.")

        obs = self.engine.observe(self.state)
        self.last_obs = obs
        return sanitize_observation(obs)

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """Return MCP tool declarations for agent discovery."""
        return [
            {
                "name": "new_game",
                "description": "Start a new adventure game with a character preset ('cutpurse', 'noble', 'warrior', 'nomad', 'diver', 'scout', 'pit_fighter').",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "preset": {
                            "type": "string",
                            "description": "Character preset identifier ('cutpurse', 'noble', 'warrior', 'nomad', 'diver', 'scout', 'pit_fighter').",
                            "default": "cutpurse",
                        },
                        "seed": {
                            "type": "integer",
                            "description": "Optional deterministic RNG seed.",
                        }
                    },
                    "required": ["preset"],
                },
            },
            {
                "name": "step_game",
                "description": "Execute a legal action in the current scene by its action ID.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "action_id": {
                            "type": "string",
                            "description": "The ID of the action to execute (from legal_actions list).",
                        }
                    },
                    "required": ["action_id"],
                },
            },
            {
                "name": "get_state",
                "description": "Retrieve current player observation, scene description, events, and legal actions.",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                },
            },
        ]

    def list_tools(self) -> List[Dict[str, Any]]:
        """Alias to get_tools_schema."""
        return self.get_tools_schema()

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch a tool call by name with arguments."""
        if not isinstance(arguments, dict):
            arguments = {}
        if name == "new_game":
            preset = arguments.get("preset", "cutpurse")
            seed = arguments.get("seed")
            return self.new_game(preset, seed=seed)
        elif name == "step_game":
            action_id = arguments.get("action_id", "")
            return self.step_game(action_id)
        elif name == "get_state":
            return self.get_state()
        else:
            return error_observation(f"Unknown tool '{name}'")


# Singleton instance for module-level contract functions
_DEFAULT_SERVER = MCPServer()


def new_game(preset: str = "cutpurse", seed: Optional[int] = None) -> Dict[str, Any]:
    """Module-level contract: new_game(preset: str) -> Dict."""
    if not isinstance(preset, str):
        preset = "cutpurse"
    return _DEFAULT_SERVER.new_game(preset, seed=seed)


def step_game(action_id: str) -> Dict[str, Any]:
    """Module-level contract: step_game(action_id: str) -> Dict."""
    return _DEFAULT_SERVER.step_game(action_id)


def get_state() -> Dict[str, Any]:
    """Module-level contract: get_state() -> Dict."""
    return _DEFAULT_SERVER.get_state()


def reset() -> None:
    """Reset default server session state."""
    _DEFAULT_SERVER.reset()


def list_tools() -> List[Dict[str, Any]]:
    """Return available tools schema."""
    return _DEFAULT_SERVER.list_tools()


def handle_jsonrpc_request(request: Dict[str, Any], server: Optional[MCPServer] = None) -> Optional[Dict[str, Any]]:
    """Handle a single JSON-RPC 2.0 request conforming to the MCP specification."""
    if not isinstance(request, dict):
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32600,
                "message": "Invalid Request: expected JSON object",
            },
        }

    srv = server or _DEFAULT_SERVER
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params")
    if not isinstance(params, dict):
        params = {}

    if req_id is None and method == "notifications/initialized":
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "adventure-forge-player",
                    "version": "0.1.0",
                }
            }
        }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": srv.get_tools_schema()
            }
        }

    if method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments")
        if not isinstance(arguments, dict):
            arguments = {}
        result = srv.call_tool(tool_name, arguments)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2)
                    }
                ],
                "isError": not result.get("success", True)
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": -32601,
            "message": f"Method '{method}' not found"
        }
    }


def handle_jsonrpc(request: Dict[str, Any]) -> Dict[str, Any]:
    """Module-level handler for a JSON-RPC request."""
    res = handle_jsonrpc_request(request, _DEFAULT_SERVER)
    return res if res is not None else {}


def run_stdio_server(server: Optional[MCPServer] = None) -> None:
    """Run MCP server over stdio reading line-delimited JSON-RPC requests."""
    srv = server or _DEFAULT_SERVER
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError as exc:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {exc}"},
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()
            continue

        try:
            resp = handle_jsonrpc_request(req, srv)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as exc:
            req_id = req.get("id") if isinstance(req, dict) else None
            err_resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": f"Internal error: {exc}"},
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


def main():
    """CLI entrypoint for running the MCP server."""
    run_stdio_server()


if __name__ == "__main__":
    main()
