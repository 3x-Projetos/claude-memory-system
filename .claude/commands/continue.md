---
description: Continua de onde a última sessão parou
---

# /continue - Session Continuation (v3.1)

This command invokes the **session-continuity-assistant** skill to resume work.

## What it does

1. **Cloud Sync** (if configured): Pulls updates from other devices
2. **Quick Loading** (M010.1): Reads session-state + provider-activities (~720 tokens, 91% savings)
3. **Temporal Triggers**: Alerts for aggregation if needed (Friday/end-of-month)
4. **Project Selection**: Shows active projects, waits for your choice
5. **On-Demand Context**: Loads chosen project context only

## How to use

Simply run:

```
/continue
```

The skill will:
- Present a summary of where you left off
- Show your active projects
- Wait for you to choose which project to continue
- Load context progressively (only what you need)

## Token Efficiency

| Scenario | Tokens | Savings vs v2.0 |
|----------|--------|-----------------|
| Startup only | ~720 | 91% |
| + Specific project | ~2,120 | 73% |
| + Multi-project mode | ~1,820 | 77% |

## Multi-Device Workflow

**Device A** → Work → `/end` → Push to cloud  
**Device B** → `/continue` → **Auto pull** → See Device A work  

Zero manual git commands needed!

## Implementation

Execute the Skill tool with `skill="session-continuity-assistant"`

The skill contains the full implementation including:
- Step 0: Cloud sync (.claude/workflows/cloud-sync-on-continue.md)
- Steps 1-5: Context loading, presentation, on-demand loading

For detailed workflow, see: `.claude/skills/session-continuity-assistant/SKILL.md`

---

**Remember**: Use `/end` to save your session when done.
