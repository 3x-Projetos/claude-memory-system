#!/usr/bin/env python3
"""
PreToolUse Hook: Auto-approve operations with multiple levels
Toggleable via /auto-approve command - checks state file each execution.

Levels:
- off: Nothing auto-approved
- edits: Edit and Write only
- bash: Edit, Write, and Bash
- all: Everything
"""
import json
import sys
import os

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

# Get the tool being called
tool_name = input_data.get("toolName", "")

# Read auto-approve level from state file
script_dir = os.path.dirname(os.path.abspath(__file__))
state_file = os.path.join(script_dir, 'auto-approve-state')

level = "off"
if os.path.exists(state_file):
    try:
        with open(state_file, 'r') as f:
            state = f.read().strip()
            if state in ["off", "edits", "bash", "all"]:
                level = state
    except:
        pass

# Determine if this tool should be auto-approved
should_approve = False
reason = ""

if level == "off":
    should_approve = False
elif level == "edits":
    if tool_name in ["Edit", "Write"]:
        should_approve = True
        reason = "Auto-approved: edits mode (Edit/Write only)"
elif level == "bash":
    if tool_name in ["Edit", "Write", "Bash"]:
        should_approve = True
        reason = "Auto-approved: bash mode (Edit/Write/Bash)"
elif level == "all":
    should_approve = True
    reason = "Auto-approved: all mode (everything)"

# Return appropriate response
if should_approve:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": reason
        }
    }
else:
    output = {}

print(json.dumps(output))
sys.exit(0)
