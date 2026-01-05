#!/usr/bin/env python3
"""
Command Validator Hook
======================
Validates bash commands before execution to prevent dangerous operations.

Usage in hooks.json:
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python3 .agent/hooks/command_validator.py",
        "timeout": 10
      }]
    }]
  }
}
"""

import json
import re
import sys

# Dangerous patterns to block
BLOCKED_PATTERNS = [
    (r"rm\s+-rf\s+/", "BLOCKED: 'rm -rf /' is extremely dangerous"),
    (r"rm\s+-rf\s+~", "BLOCKED: 'rm -rf ~' will delete home directory"),
    (r"rm\s+-rf\s+\*", "BLOCKED: 'rm -rf *' without explicit path"),
    (r":\(\)\{\s*:\|:\s*&\s*\}", "BLOCKED: Fork bomb detected"),
    (r"mkfs\.", "BLOCKED: Filesystem formatting command"),
    (r"dd\s+if=.*of=/dev/", "BLOCKED: Direct disk write"),
]

# Warnings (allow but notify)
WARNING_PATTERNS = [
    (r"pip\s+install\s+(?!-r)", "WARNING: Consider using 'pip install -r requirements.txt'"),
    (r"git\s+push\s+.*--force", "WARNING: Force push detected, be careful"),
    (r"chmod\s+777", "WARNING: chmod 777 is insecure"),
]

# Suggestions for better alternatives
SUGGESTIONS = [
    (r"^grep\s+", "TIP: Consider using 'rg' (ripgrep) for better performance"),
    (r"^find\s+.*-name", "TIP: Consider using 'fd' for faster file search"),
]


def validate_command(command: str) -> tuple[list[str], list[str], list[str]]:
    """Returns (blocked, warnings, suggestions)"""
    blocked = []
    warnings = []
    suggestions = []
    
    for pattern, message in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            blocked.append(message)
    
    for pattern, message in WARNING_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            warnings.append(message)
    
    for pattern, message in SUGGESTIONS:
        if re.search(pattern, command, re.IGNORECASE):
            suggestions.append(message)
    
    return blocked, warnings, suggestions


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command:
        sys.exit(0)

    blocked, warnings, suggestions = validate_command(command)
    
    for msg in suggestions:
        print(msg, file=sys.stderr)
    
    for msg in warnings:
        print(msg, file=sys.stderr)
    
    if blocked:
        for msg in blocked:
            print(msg, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
