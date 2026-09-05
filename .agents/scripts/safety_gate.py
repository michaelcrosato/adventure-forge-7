#!/usr/bin/env python3
"""PreToolUse Safety Gate Hook.

Inspects commands before execution to prompt the user before running destructive commands.
Always outputs a valid JSON object with 'decision'.
"""
import sys
import json
import re

DESTRUCTIVE_PATTERNS = [
    r"\bgit\s+push\b.*(--force|-f)\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\s+(-[a-zA-Z]*f[a-zA-Z]*)\b",
    r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f\s+([/~]|\.git)\b",
    r"\bdrop\s+database\b",
]

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}))
            return

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})

        if tool_name == "run_command":
            cmd = args.get("CommandLine", "")
            for pat in DESTRUCTIVE_PATTERNS:
                if re.search(pat, cmd, re.IGNORECASE):
                    print(json.dumps({
                        "decision": "ask",
                        "reason": f"Potentially destructive command detected: '{cmd}'. User confirmation required."
                    }))
                    return

        print(json.dumps({"decision": "allow"}))
    except Exception:
        # Fallback safely to allow on any hook processing error
        print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
