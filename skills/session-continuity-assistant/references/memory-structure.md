# Framework Memory Structure Reference

Complete guide to the claude-memory-system hierarchical memory organization.

## Overview

The framework uses a **multi-resolution memory system** designed for token efficiency through progressive disclosure. Instead of loading everything upfront, memory is organized in layers from quick summaries to full detail.

**Key Innovation**: 84-88% token savings on startup compared to v2.0

---

## Memory Hierarchy

### Layer 1: Working Memory (Always Loaded)

**File**: `~/.claude-memory/providers/claude/session-state.md`
**Size**: ~50 lines
**When**: Every session

**Contains**:
- Last session timestamp and topic
- Active projects (top 3-4)
- Current focus
- Pending tasks (top 5-7)
- Aggregation status (weekly/monthly)

**Purpose**: Minimal context for quick startup and routing decisions

### Layer 2: Quick Memories (Startup Only)

**Files**:
- `~/.claude-memory/global-memory.quick.md` (~50 lines)
- `.projects/[name]/.context.quick.md` (~30 lines)
- `~/.claude-memory/integration/provider-activities.quick.md` (~10 lines)

**Total**: ~90-130 lines depending on project selection

**Contains**:
- User profile essentials (not full details)
- Project summary (not full context)
- Cross-provider activity overview

**Purpose**: Enough context to start work without overwhelming token budget

### Layer 3: Full Memories (On-Demand)

**Files**:
- `~/.claude-memory/global-memory.safe.md` (~165 lines, PII redacted)
- `.projects/[name]/.context.md` (full project memory)
- Daily/weekly/monthly logs

**When**: Loaded only when needed for deep context

**Purpose**: Complete information when shallow context insufficient

### Layer 4: Temporal Logs

Progressive summarization with 93% token reduction across hierarchy:

| Level | File | Size | Coverage |
|-------|------|------|----------|
| Daily | `logs/daily/YYYY.MM.DD.md` | ~150 lines | One day |
| Weekly | `logs/weekly/YYYY.MM.weekN.md` | ~100 lines | 7 days |
| Monthly | `logs/monthly/YYYY.MM.md` | ~30 lines | 30 days |

**Aggregation workflow**:
- Daily logs accumulate during week
- `/aggregate week` creates weekly summary (deletes daily logs older than 7 days)
- `/aggregate month` creates monthly summary (deletes weekly logs older than 30 days)

---

## Directory Structure

### Local Memory (Per Device)

```
~/.claude-memory/
├── global-memory.md              # Full profile (with PII)
├── global-memory.safe.md         # PII redacted version
├── global-memory.quick.md        # Condensed (~50 lines)
│
├── profile-history/              # Versioned snapshots
│   └── YYYY-MM-DD_*.md
│
├── profile-changelog.md          # Version history
│
├── projects/                     # Project references (pointers)
│   └── [project-name]/
│       ├── .context.md           # Full memory
│       ├── .context.quick.md     # Condensed
│       └── .status.md            # Roadmap/decisions
│
├── providers/                    # Multi-provider support
│   ├── claude/
│   │   ├── session-state.md
│   │   ├── session-state.quick.md
│   │   ├── logs/
│   │   │   ├── daily/YYYY.MM.DD.md
│   │   │   ├── weekly/YYYY.MM.weekN.md
│   │   │   └── monthly/YYYY.MM.md
│   │   └── web-sessions/         # Manually exported web sessions
│   │
│   └── lmstudio/                 # Local LLM sessions
│       └── logs/...
│
└── integration/
    ├── provider-activities.md     # Full cross-provider timeline
    └── provider-activities.quick.md  # Recent only (~10 lines)
```

### Cloud Memory (GitHub Repo - Optional)

```
~/.claude-memory-cloud/           # Git repository (private)
├── .gitignore                    # Privacy rules (PII excluded)
├── .sync-config.json             # Sync settings
├── README.md                     # Git guide for newcomers
│
├── global/
│   ├── profile.md                # With PII markers
│   ├── profile.safe.md           # Auto-generated (redacted)
│   ├── profile.quick.md          # Auto-generated (condensed)
│   └── preferences.json          # Structured settings
│
├── devices/                      # Device-specific state
│   ├── laptop-work/
│   ├── laptop-personal/
│   ├── desktop-small/
│   ├── desktop-big/
│   └── android-phone/
│
├── projects/                     # Cross-device project contexts
│   └── [project-name]/
│       ├── .context.md
│       └── .status.md
│
├── providers/                    # Session logs (synced)
│   ├── claude/
│   │   └── logs/daily|weekly|monthly/
│   ├── lmstudio/
│   └── gemini/
│
├── sync/
│   ├── device-registry.json      # All known devices
│   ├── conflicts/                # Conflict resolution queue
│   └── logs/                     # Sync history
│
└── integration/
    └── timeline.md               # Unified cross-device timeline
```

**Sync Strategy**:
- SessionStart hook: `git pull` (get latest from other devices)
- SessionEnd hook: `git commit && git push` (share this session)
- Conflict resolution: Latest-timestamp wins

---

## Reading Strategies

### Strategy 1: Continuation (Default)

**Goal**: Resume work quickly

```
1. Read session-state.md (~50 lines)
2. Check time elapsed since last session
3. If same day → read daily log
4. If same week → read weekly summary
5. If older → read monthly summary
6. Load project context if focused work
```

**Token cost**: 50-200 lines (vs 700+ in v2.0)

### Strategy 2: Project Switch

**Goal**: Change context to different project

```
1. Read session-state.md (~50 lines)
2. Read .projects/[new-project]/.context.quick.md (~30 lines)
3. Optional: Load .status.md for roadmap
4. Update session-state.md (Current Focus)
```

**Token cost**: ~80-130 lines

### Strategy 3: Multi-Project Overview

**Goal**: Dashboard of all active work

```
1. Read session-state.md (~50 lines)
2. Read .projects/*/. context.quick.md for top 3-5 projects
3. Optional: Check provider-activities.quick.md
```

**Token cost**: ~100-200 lines

### Strategy 4: Deep Dive

**Goal**: Full context for complex task

```
1. Read session-state.md
2. Load global-memory.safe.md (~165 lines)
3. Load full project context (.context.md)
4. Load relevant logs (weekly or daily)
5. Optional: Load reference workflows
```

**Token cost**: 300-500 lines (still less than old v2.0 default)

---

## PII Protection

### PII Markers

**Format**: `[PII:TYPE]value[/PII:TYPE]`

**Types**:
- `[PII:NAME]John Doe[/PII:NAME]`
- `[PII:EMAIL]user@example.com[/PII:EMAIL]`
- `[PII:PHONE]+1-555-0123[/PII:PHONE]`
- `[PII:ADDRESS]123 Main St[/PII:ADDRESS]`
- `[PII:COMPANY]Acme Corp[/PII:COMPANY]`
- `[PII:PROJECT]SecretProject[/PII:PROJECT]`

### Redaction Process

**Script**: `.claude/redact-pii.py`

**Execution**: `/continue` command runs this automatically

**Output**:
- `global-memory.safe.md` - All PII → `[REDACTED:TYPE]`
- `global-memory.quick.md` - Condensed + redacted

**Cloud sync**: Only `.safe.md` and `.quick.md` files pushed to GitHub (never raw PII)

---

## Provider Abstraction

### Multi-Provider Design

**Principle**: Provider-agnostic memory structure

**Supported**:
- Claude CLI (primary)
- LMStudio (local LLM)
- Gemini (future)
- GPT (future)

**How it works**:
1. Each provider has own `providers/[name]/` directory
2. Session logs isolated per provider
3. Cross-provider timeline in `integration/`
4. Seamless handoff via `provider-activities.quick.md`

### Example: LMStudio Session

User works in LMStudio, then switches to Claude CLI:

```
1. LMStudio creates: providers/lmstudio/logs/daily/2025.12.28.md
2. LMStudio updates: integration/provider-activities.md
3. User switches to Claude CLI
4. Claude CLI reads: integration/provider-activities.quick.md
5. Claude sees: "Last LMStudio session worked on data analysis"
6. Claude offers: "Continue data analysis work or start new?"
```

**Benefit**: No duplicated work, smooth transitions

---

## Aggregation System

### Why Aggregate?

**Problem**: Daily logs accumulate → token budget grows → slower startup

**Solution**: Progressive summarization

- Weekly aggregation: 85% reduction (7 daily logs → 1 weekly summary)
- Monthly aggregation: 93% reduction (4 weekly summaries → 1 monthly overview)

### When to Aggregate

**Automatic triggers** (suggested, not forced):
- Friday afternoon: "Aggregate week?"
- Last day of month: "Aggregate month?"

**Manual triggers**:
- `/aggregate week` - Aggregate past 7 days
- `/aggregate month` - Aggregate past 30 days

**Aggregation status** (in session-state.md):
```
## Aggregation Status

**Weekly Aggregation**:
- Status: ⏳ Pending (7 days to aggregate)
- Última semana agregada: 2025.12.weekN

**Monthly Aggregation**:
- Status: ✅ Up-to-date
- Último mês agregado: 2025.11
```

### What Gets Aggregated

**Weekly aggregation** extracts from daily logs:
- Key topics covered
- Projects touched (with % time)
- Decisions made
- Actions completed
- Blockers encountered
- Tools/technologies used

**Monthly aggregation** extracts from weekly summaries:
- High-level themes
- Major milestones
- Projects completed/started
- Key learnings
- Metrics (if tracked)

**What's preserved**:
- Critical decisions
- Project status changes
- Important insights
- Metrics data

**What's discarded**:
- Routine operations
- Redundant details
- Transient state

---

## Best Practices

### For Session Continuity

1. **Start minimal**: Always read session-state.md first
2. **Load progressively**: Only load detailed logs when needed
3. **Use quick versions**: Prefer `.quick.md` for routing decisions
4. **Aggregate regularly**: Prevent token budget bloat

### For Project Work

1. **Use `/switch`**: Explicitly change project context
2. **Update status**: Keep `.status.md` current
3. **Tag properly**: Use `[project:name]` in logs

### For Multi-Device

1. **Pull first**: SessionStart hook runs `git pull`
2. **Push after**: SessionEnd hook runs `git push`
3. **Check conflicts**: Rare, but handled by latest-timestamp wins
4. **Sync frequently**: Don't let devices diverge too much

### For Privacy

1. **Mark PII**: Use `[PII:TYPE]` markers consistently
2. **Never commit raw**: Only `.safe.md` goes to cloud
3. **Review `.gitignore`**: Ensure PII files excluded
4. **Audit periodically**: Check cloud repo for leaks

---

## Troubleshooting

**Issue**: Token budget still high
**Solution**: Check if aggregation pending; run `/aggregate week`

**Issue**: Missing recent logs
**Solution**: Check if `/end` was used last session; review lazy logging

**Issue**: Project context outdated
**Solution**: Use `/project-status` to update roadmap and decisions

**Issue**: Cloud sync conflicts
**Solution**: Check `.claude-memory-cloud/sync/conflicts/`; resolve manually

**Issue**: Can't find old sessions
**Solution**: Check if monthly aggregation ran; older than 30 days may be summarized

---

## Performance Metrics

### Token Savings

| Scenario | v2.0 (Old) | v2.3 (New) | Savings |
|----------|-----------|-----------|---------|
| Startup (continue) | ~700 lines | ~130 lines | 81% |
| Project switch | ~700 lines | ~80 lines | 88% |
| Multi-project view | ~700 lines | ~150 lines | 78% |
| Deep dive | ~700 lines | ~400 lines | 43% |

### Aggregation Impact

| Timeframe | Before Aggregation | After Aggregation | Reduction |
|-----------|-------------------|-------------------|-----------|
| 1 week (7 days) | 7 × 150 = 1,050 lines | 100 lines | 90% |
| 1 month (4 weeks) | 4 × 100 = 400 lines | 30 lines | 92.5% |

---

## Version History

**v2.3** (Current)
- Multi-resolution memory (quick/full versions)
- Cloud sync integration (optional GitHub repo)
- Multi-provider support (Claude, LMStudio)
- Progressive aggregation (daily → weekly → monthly)

**v2.2**
- Multi-provider abstraction
- Cross-provider timeline

**v2.1**
- Weekly aggregation workflow
- PII redaction system

**v2.0**
- Session continuity
- Daily logging
- Project-centric organization

**v1.0**
- Basic note organization
- Command system
- Workflow documentation

---

**Reference**: See `continuation-patterns.md` for common usage scenarios and templates.
