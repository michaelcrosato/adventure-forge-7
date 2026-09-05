#!/usr/bin/env python3
"""PostToolUse Syntax Verification Hook.

Runs quick syntax validation on python files modified by edit tools.
Contract: Always outputs empty JSON object `{}` to stdout.
"""
import sys
import json
import py_compile
import os

def main():
    try:
        raw_input = sys.stdin.read()
        if raw_input.strip():
            payload = json.loads(raw_input)
            tool_call = payload.get("toolCall", {})
            args = tool_call.get("args", {})
            target_file = args.get("TargetFile", "")

            if target_file and target_file.endswith(".py") and os.path.exists(target_file):
                try:
                    py_compile.compile(target_file, doraise=True)
                except py_compile.PyCompileError as exc:
                    sys.stderr.write(f"[post_edit_lint] Syntax check warning in {target_file}: {exc}\n")
    except Exception as exc:
        sys.stderr.write(f"[post_edit_lint] Hook error: {exc}\n")
    finally:
        # PostToolUse contract strictly expects `{}` on stdout
        sys.stdout.write("{}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
