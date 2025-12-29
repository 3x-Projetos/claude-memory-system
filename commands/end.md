---
description: Finalize session by creating detailed log and syncing to cloud
---

# /end - Session Finalization (v3.2)

This command invokes the **end** skill to finalize and log your session.

## What it does

1. **Collect Session Info**: Prompts for session summary (topic, projects, activities, decisions)
2. **Generate Daily Log**: Creates structured entry in `~/.claude-memory/providers/claude/logs/daily/YYYY.MM.DD.md`
3. **Update Session State**: Modifies session-state.md with current focus and pending tasks
4. **Update Integration Timeline**: Appends to provider-activities.md
5. **Cloud Sync** (if configured): Pushes logs to cloud (best-effort, non-blocking)
6. **Confirmation**: Shows what was logged and sync status

## How to use

Simply run:

```
/end
```

The skill will:
- Ask you about the session (topic, activities, next steps)
- Create a detailed log entry
- Update all state files
- Sync to cloud if configured
- Never lose local logs even if cloud sync fails

## Key Principle

**Logs saved locally first, cloud sync is best-effort.** Session finalization never blocks on cloud errors.

## Multi-Device Workflow

**Device A** → Work → `/end` → **Auto push** → Synced to cloud
**Device B** → `/continue` → Auto pull → See Device A work

Zero manual git commands needed!

## Implementation

Execute the Skill tool with `skill="end"`

The skill contains the full implementation including:
- Session info collection
- Log generation
- State updates
- Cloud sync workflow

For detailed workflow reference, see the old command in: `.claude/commands/archive/end-v2.3.md` (if needed)

---

**Next session**: Use `/continue` to resume where you left off.
