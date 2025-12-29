# Session Continuation Patterns

Common scenarios and templates for seamlessly resuming work using the session-continuity-assistant skill, with full multi-device and cloud sync awareness.

---

## Multi-Device Context Awareness

**Critical Principle**: Different devices can work on same day. Always check cloud memory first.

**Device Detection Flow**:
1. Check local session-state.md → Last session on THIS device
2. Pull cloud memory → Get latest from ALL devices
3. Compare timestamps → Determine which device was most recent
4. Load appropriate context → May be from different device!

**Example Scenario**:
- Morning (9 AM): User works on `laptop-work`
- Afternoon (2 PM): User switches to `desktop-big` ← Need to know what laptop did!
- Evening (8 PM): User returns to `laptop-work` ← Need to know what desktop did!

---

## Pattern 1: Same-Day Resume (Single Device)

**Scenario**: User returns to SAME device within same day (< 8 hours)

**Device Check**: Local session-state matches cloud (no other device activity)

**Template**:

```
**Resuming from**: Today, [TIME] ([HOURS] hours ago)
**Device**: [THIS-DEVICE] (same as last session)

**Last Topic**: [One-line description]

**In Progress**:
- [Task 1] - [Status: in progress / needs review / blocked]
- [Task 2] - [Status]

**Recent Changes**:
- [File 1] - [What changed]
- [File 2] - [What changed]

**Next Immediate Steps**:
1. [Concrete next action]
2. [Follow-up action]
3. [Testing/validation step]

---

Ready to [verb] [specific task]?
```

---

## Pattern 1B: Same-Day Resume (Different Device)

**Scenario**: User worked on Device A today, now on Device B

**Device Check**: Local session-state is old, cloud has newer session from different device

**Critical**: Always pull cloud before presenting summary!

**Template**:

```
**Device Switch Detected** 🔄

**Current Device**: [THIS-DEVICE]
**Last Active Device**: [OTHER-DEVICE] (today, [TIME])

**Your Activity Today** (cross-device):
- Morning ([TIME]) on [DEVICE-1]: [Activity 1]
- Afternoon ([TIME]) on [DEVICE-2]: [Activity 2] ← Most recent
- Now: Resuming on [CURRENT-DEVICE]

**Latest Context** (from [OTHER-DEVICE]):
- Topic: [What other device was doing]
- Progress: [What was completed]
- In progress: [What's unfinished]

**Cloud Sync Status**:
✅ Synced [N] minutes ago from [OTHER-DEVICE]

**Next Steps** (continuing from [OTHER-DEVICE]):
1. [Action that makes sense based on other device's work]
2. [Follow-up]
3. [Validation]

**Files Changed Today** (all devices):
- On [DEVICE-1]: [Files]
- On [DEVICE-2]: [Files]

---

Continue where [OTHER-DEVICE] left off?
```

**Example**:

```
**Device Switch Detected** 🔄

**Current Device**: desktop-big
**Last Active Device**: laptop-work (today, 11:30 AM)

**Your Activity Today** (cross-device):
- Morning (9:15 AM) on laptop-work: Started skills system implementation
- Morning (11:30 AM) on laptop-work: Completed scientist skill installation ← Most recent
- Now (2:45 PM): Resuming on desktop-big

**Latest Context** (from laptop-work):
- Topic: Skills system implementation (Phase 1 complete)
- Progress: Scientist skill installed and tested
- In progress: Starting session-continuity-assistant skill (Phase 2)

**Cloud Sync Status**:
✅ Synced 3 hours ago from laptop-work
✅ Cloud memory pulled successfully

**Next Steps** (continuing from laptop-work):
1. Create session-continuity-assistant SKILL.md
2. Create reference files (memory-structure.md, continuation-patterns.md)
3. Test skill activation with trigger phrases

**Files Changed Today** (all devices):
- On laptop-work: ~/.claude/skills/scientist/SKILL.md (installed)
- On laptop-work: ~/.claude/skills/scientist/LICENSE.txt (installed)

---

Continue with session-continuity-assistant implementation?
```

---

## Pattern 2: Multi-Device Coordination

**Scenario**: User alternates between devices throughout day

**Critical**: Cloud is source of truth, local is cache

**Workflow**:

```
1. SessionStart Hook: git pull (get latest from cloud)
2. Check timestamps: local vs cloud
3. If cloud newer → different device was active
4. Load cloud context (not stale local)
5. Work locally
6. SessionEnd Hook: git commit + push (share with other devices)
```

**Template**:

```
**Multi-Device Activity Detected** 🔄

**Today's Device Timeline**:
[TIME] [DEVICE-1] → [Activity]
[TIME] [DEVICE-2] → [Activity]
[TIME] [DEVICE-3] → [Activity]
[TIME] [CURRENT] → Resuming

**Most Recent Work** (from [DEVICE-X]):
- [Summary of latest session]

**Cloud Sync Chain**:
[DEVICE-1] → Push → Cloud
Cloud → Pull → [DEVICE-2] → Push → Cloud
Cloud → Pull → [CURRENT]

**Continuity Preserved**:
✅ All work synced
✅ No sessions lost
✅ Context transferred seamlessly

**Current State**:
[Unified view of all today's work across devices]

---

Continue from where [DEVICE-X] stopped?
```

**Example**:

```
**Multi-Device Activity Detected** 🔄

**Today's Device Timeline**:
09:00 laptop-work → Framework exploration (2 hours)
11:30 laptop-work → Scientist skill install (30 min)
14:00 desktop-big → Session-continuity SKILL.md (1 hour)
15:30 laptop-work → Resuming now

**Most Recent Work** (from desktop-big):
- Created session-continuity-assistant/SKILL.md (complete)
- Created memory-structure.md reference (complete)
- Started continuation-patterns.md (in progress, 40% done)

**Cloud Sync Chain**:
laptop-work (11:30) → Push → Cloud
Cloud → Pull → desktop-big (14:00)
desktop-big (15:00) → Push → Cloud
Cloud → Pull → laptop-work (15:30 NOW)

**Continuity Preserved**:
✅ Morning work (laptop) synced to cloud
✅ Afternoon work (desktop) synced to cloud
✅ Now on laptop, all context available

**Current State** (unified view):
- Scientist skill: ✅ Installed (done on laptop)
- Session-continuity skill: 🔧 In progress (SKILL.md done on desktop, references 60% done)

---

Continue finishing continuation-patterns.md on laptop?
```

---

## Pattern 3: Cloud Sync Conflict Detection

**Scenario**: Two devices worked simultaneously (rare but possible)

**Conflict Resolution**: Latest-timestamp wins

**Template**:

```
⚠️ **Sync Conflict Detected**

**Situation**:
- [DEVICE-1] worked offline: [TIME-RANGE]
- [DEVICE-2] worked offline: [TIME-RANGE]
- Both pushed to cloud

**Conflict Resolution**:
✅ Latest-timestamp wins: [WINNING-DEVICE] ([TIME])

**Your Work** (from [THIS-DEVICE]):
- [Activity summary]
- Last sync: [TIME]

**Other Device Work** (from [OTHER-DEVICE]):
- [Activity summary]
- Last sync: [TIME] ← Newer

**Merged Result**:
- [OTHER-DEVICE] changes accepted (newer)
- [THIS-DEVICE] changes preserved in: cloud/sync/conflicts/[timestamp].md

**What You Need to Know**:
- [Summary of what other device did]
- [Any conflicts in your pending work]

**Next Steps**:
1. Review conflict file: cloud/sync/conflicts/[file].md
2. Manually merge if needed
3. Continue with latest cloud state

---

Proceed with merged state?
```

---

## Pattern 4: Device-Specific Work Tracking

**Scenario**: Need to see what each device contributed

**Use Case**: Debugging, auditing, understanding device usage patterns

**Template**:

```
**Device Activity Report**

**This Week** ([DATE-RANGE]):

| Device | Sessions | Hours | Projects | Key Contributions |
|--------|----------|-------|----------|-------------------|
| [DEVICE-1] | [N] | [H] | [List] | [Summary] |
| [DEVICE-2] | [N] | [H] | [List] | [Summary] |
| [DEVICE-3] | [N] | [H] | [List] | [Summary] |

**Device Specialization** (observed):
- [DEVICE-1]: [What it's typically used for]
- [DEVICE-2]: [What it's typically used for]

**Current Device** ([THIS-DEVICE]):
- Last used: [TIME]
- Typical work: [Pattern]
- Suggested for: [Type of work that fits this device]

**Cross-Device Workflows**:
- [Workflow 1]: [DEVICE-A] → [DEVICE-B] (e.g., plan on laptop, implement on desktop)
- [Workflow 2]: [DEVICE-B] → [DEVICE-C]

---

Using [THIS-DEVICE] for [current task] makes sense?
```

---

## Pattern 5: Cloud Sync Status Check

**Scenario**: User unsure if cloud is up-to-date

**Critical**: Before starting work, verify sync status

**Template**:

```
**Cloud Sync Status**

**Local Memory** ([THIS-DEVICE]):
- Last local session: [TIME]
- Last local commit: [COMMIT-ID] ([TIME])

**Cloud Memory** (GitHub):
- Last cloud commit: [COMMIT-ID] ([TIME])
- Last device pushed: [DEVICE-NAME]

**Sync Status**:
[✅ In sync / ⚠️ Out of sync / 🔄 Pulling now]

**If Out of Sync**:
- Local is [N minutes/hours] behind
- Cloud has [N] new commits from [DEVICE-LIST]
- Action: Pull latest before continuing

**Recent Cloud Activity** (from other devices):
- [TIME] [DEVICE]: [Activity]
- [TIME] [DEVICE]: [Activity]

**Ready to Work**:
[✅ Safe to start / ⏸️ Pull first / ⚠️ Conflicts detected]

---

[Action recommendation]
```

**Example**:

```
**Cloud Sync Status**

**Local Memory** (laptop-work):
- Last local session: Today 11:30 AM
- Last local commit: a7b3c9f (Today 11:30 AM)

**Cloud Memory** (GitHub):
- Last cloud commit: e4f8d2a (Today 3:15 PM) ← Newer!
- Last device pushed: desktop-big

**Sync Status**:
⚠️ Out of sync - Cloud is 3 hours 45 min ahead

**Cloud Activity Since Your Last Session**:
- 3:15 PM desktop-big: Completed session-continuity SKILL.md + references
- 3:15 PM desktop-big: 60% through continuation-patterns.md

**Pull Summary** (what you'll get):
- New files: session-continuity-assistant/SKILL.md
- New files: session-continuity-assistant/references/memory-structure.md
- Modified: continuation-patterns.md (60% done)

**Ready to Work**:
⏸️ Pull first - You'll get desktop's afternoon work

---

Running: git pull origin main...
✅ Pulled successfully! Now in sync. Continue?
```

---

## Pattern 6: Offline Work Recovery

**Scenario**: User worked offline (no internet), now syncing

**Challenge**: Local changes + cloud changes need reconciliation

**Template**:

```
**Offline Work Recovery**

**Your Offline Work** ([THIS-DEVICE]):
- Duration: [TIME-RANGE] (offline)
- Sessions: [N]
- Changes: [FILE-COUNT] files

**Cloud Work While You Were Offline** (other devices):
- [DEVICE]: [Activity summary]
- [DEVICE]: [Activity summary]

**Merge Strategy**:
- Your work: [SUMMARY]
- Cloud work: [SUMMARY]
- Conflicts: [YES/NO]

**If No Conflicts**:
✅ Auto-merge successful
- Your changes: Committed to cloud
- Cloud changes: Pulled to local
- Combined state: [DESCRIPTION]

**If Conflicts**:
⚠️ Manual resolution needed
- Conflicting files: [LIST]
- Resolution options:
  1. Keep yours (local wins)
  2. Keep theirs (cloud wins)
  3. Manual merge (best)

---

[Recommended action]
```

---

## Best Practices for Multi-Device

### Always Pull Before Work

```bash
# SessionStart hook should do this automatically
cd ~/.claude-memory-cloud
git pull origin main
```

**Why**: Get latest from all devices before starting

### Always Push After Work

```bash
# SessionEnd hook should do this automatically
cd ~/.claude-memory-cloud
git add .
git commit -m "Session from [DEVICE]"
git push origin main
```

**Why**: Share your work with other devices

### Check Sync Status Regularly

```
Ask: "Is my cloud memory in sync?"
```

**Skill will**:
1. Compare local vs cloud timestamps
2. Show recent activity from other devices
3. Recommend pull if needed

### Use Device Registry

**File**: `~/.claude-memory-cloud/sync/device-registry.json`

```json
{
  "devices": [
    {
      "id": "laptop-work",
      "name": "Work Laptop (Windows)",
      "last_seen": "2025-12-28T15:30:00Z",
      "typical_use": "Development, documentation"
    },
    {
      "id": "desktop-big",
      "name": "Desktop (Windows)",
      "last_seen": "2025-12-28T15:00:00Z",
      "typical_use": "Heavy computation, multiple monitors"
    }
  ]
}
```

**Benefits**:
- Track device activity
- Detect stale devices
- Understand device patterns

### Temporal Coherence Checks

**Always verify**:
1. What time is it now?
2. When was last session (any device)?
3. Which device had that session?
4. Has cloud been updated since?

**Decision tree**:
```
Is cloud newer than local?
├─ Yes → Pull first, then show context from other device
└─ No → Safe to use local context
```

---

## Version History

**v1.0.0** (2025-12-28)
- Initial pattern library
- Multi-device awareness
- Cloud sync integration
- Device coordination patterns

---

**Reference**: See `memory-structure.md` for complete framework architecture details, including cloud sync structure.
