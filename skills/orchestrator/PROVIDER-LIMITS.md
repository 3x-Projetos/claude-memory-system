---
name: orchestrator
description: API quotas and rate limits for orchestration planning
version: 1.1.0
---

# Provider Limits - API Quotas and Constraints

Critical resource constraints that MUST be considered during orchestration planning.

---

## Overview

Each AI provider has quota limits that become hard constraints in multi-agent workflows. Exceeding these limits causes task failures and requires fallback strategies.

**Key Principle**: **Quota awareness is mandatory for reliable orchestration.** Plan worker count and parallelism within provider limits.

---

## Gemini CLI (google-generativeai)

### Free Tier Quotas

**Tested on:** 2025-12-31, v0.21.1

| Resource | Limit | Reset Period | Notes |
|----------|-------|--------------|-------|
| **Requests/Session** | ~20-25 workers | ~10 hours | Empirical testing |
| **RPM (Rate)** | 2-15 RPM | Per minute | Varies by model |
| **Concurrent Workers** | 8+ tested | N/A | With staggered launch |

**Error Pattern:**
```
You have exhausted your capacity on this model.
Your quota will reset after 10h33m20s
```

### Paid Tier Quotas

**Documentation:** https://ai.google.dev/pricing

| Resource | Limit | Notes |
|----------|-------|-------|
| **RPM** | 1000+ | Model-dependent |
| **Requests/Day** | Higher | Check specific plan |

### Quota Management Strategies

**1. Worker Count Limits:**
```bash
# Conservative: Stay under free tier limit
MAX_WORKERS=15  # Leave margin

# Aggressive: Use full capacity
MAX_WORKERS=20  # Risk hitting quota
```

**2. Quota Tracking:**
```bash
# Track workers executed
WORKERS_USED=0

launch_worker() {
  if [ $WORKERS_USED -ge $MAX_WORKERS ]; then
    echo "⚠️ Quota limit reached. Aborting worker launch."
    return 1
  fi

  gemini -p "$1" --yolo -o text > "$2" &
  sleep 1
  WORKERS_USED=$((WORKERS_USED + 1))
}
```

**3. Fallback Strategy:**
```bash
# Try Gemini, fall back to Claude if quota exhausted
gemini -p "$TASK" --yolo -o text > result.md 2>&1

if grep -q "exhausted your capacity" result.md; then
  echo "⚠️ Gemini quota exhausted. Escalating to Claude."
  # Claude executes directly
fi
```

### Real-World Session Data

**Session:** 2025-12-31 (Parallel execution research)

| Phase | Workers | Result | Notes |
|-------|---------|--------|-------|
| Research (sequential) | 4 | ✅ Success | Within limits |
| Testing (staggered) | 18 | ✅ Success | 6 scenarios × 3 workers |
| Documentation (staggered) | 3 | ⚠️ Quota hit | 2/3 failed |
| **Total** | **~25** | **Quota exhausted** | Reset: 10h33m |

**Lesson:** Free tier supports **~20 workers/session** safely. Plan accordingly.

---

## Claude API (Anthropic)

### Resource Constraints

**Model:** Sonnet 4.5 (claude-sonnet-4-5-20250929)

| Resource | Limit | Notes |
|----------|-------|-------|
| **Context Window** | 200k tokens | Hard limit |
| **Rate Limits** | Tier-based | Check Anthropic console |
| **Cost** | $$$ (highest) | Use for synthesis, not bulk |

### Usage Strategy

**Optimal Use Cases:**
- Orchestration and coordination
- Synthesis of multi-agent outputs
- High-precision implementation
- Complex reasoning tasks

**Avoid:**
- High-volume parallel tasks (use Gemini)
- Massive context analysis (use Gemini 1M+ window)
- Repetitive generation (use local model when available)

**Context Management:**
- Target <70% usage during sessions
- Use `/compact` at 70%
- Delegate heavy lifting to cheaper providers

---

## Local Models (LM Studio)

**Status:** 🟡 Tested on other device, pending cloud sync

**Notes:**
- Installation and benchmarks available on other machine
- Will consolidate findings when multi-device memory syncs
- Expected advantages: Free, unlimited quota, privacy
- Expected constraints: Hardware-dependent latency, smaller context windows

**Documentation pending:** Multi-device cloud sync (next few days)

---

## Decision Matrix with Quota Constraints

| Scenario | Provider | Why | Quota Risk |
|----------|----------|-----|------------|
| **4-8 research tasks** | Gemini | Massive context + speed | ⚠️ Medium (within limits) |
| **15+ bulk tasks** | Gemini → Fallback | Quota risk | ⛔ High (need fallback ready) |
| **20+ workers** | ⛔ Split sessions | Exceeds free tier | ⛔ Critical (will fail) |
| **Synthesis/Implementation** | Claude | Quality + precision | ✅ Low (1 request) |
| **Real-time research** | Gemini | Search grounding | ⚠️ Medium |

---

## Orchestration Planning Template

### Before Launching Workers

**Quota Validation Checklist:**
```yaml
Task Analysis:
  - Total workers needed: [N]
  - Provider choice: [Gemini/Local/Claude]
  - Estimated quota usage: [X requests]

Risk Assessment:
  - Gemini workers planned: [N] / 20 max
  - Quota status: [Available/Low/Unknown]
  - Fallback ready: [Yes/No/N/A]

Execution Plan:
  - If N ≤ 15: ✅ Safe, execute as planned
  - If 15 < N ≤ 20: ⚠️ Risky, monitor closely
  - If N > 20: ⛔ Split into multiple sessions OR use local model
```

### During Execution

**Monitor:**
- Worker success rate (0 byte files = quota issue)
- Error messages (grep for "exhausted capacity")
- Execution time (timeout = possible rate limit)

**React:**
- If quota hit: Pause, switch to fallback, or reschedule
- Track workers used to avoid repeating mistake

---

## Testing New Providers

### Methodology

When adding new AI providers to orchestration:

**1. Small batch test** (2-4 workers)
- Validate basic functionality
- Check for quota warnings

**2. Medium batch test** (8-12 workers)
- Monitor for soft limits
- Track error patterns

**3. Stress test** (20+ workers)
- Find hard quota ceiling
- Document reset behavior

**4. Document findings** in this file

**Template:**
```markdown
## Provider: [Name]

**Tested:** [Date], [Version/Model]

| Resource | Limit | Evidence |
|----------|-------|----------|
| Requests/Session | [N] | [Test result] |
| RPM | [N] | [Documentation/Testing] |

**Error Pattern:** [Paste actual error message]
```

---

## Future Enhancements

**P1 (High Priority):**
1. Automated quota tracking during sessions
   - Count workers launched per provider
   - Warning at 80% quota (e.g., 16/20 Gemini workers)

**P2 (Medium Priority):**
2. Multi-provider load balancing
   - Distribute tasks across available providers
   - Automatic failover on quota exhaustion

3. Cost tracking and optimization
   - Monitor $ spent per provider
   - Choose cost-optimal provider per task type

**P3 (Low Priority):**
4. Quota reset scheduler
   - Wait for reset before large jobs
   - Queue-based task system

---

**Last Updated:** 2025-12-31
**Framework Version:** v3.5.0
**Status:** Active (Gemini + Claude documented)
**Pending:** LM Studio data from cloud sync
