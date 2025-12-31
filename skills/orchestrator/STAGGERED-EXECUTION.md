# Staggered Execution - Gemini CLI Parallel Workers

**Version:** 1.1.0
**Date:** 2025-12-31
**Status:** Production-ready (100% success rate, 8 workers tested)

---

## Overview

Staggered execution enables **true parallel processing** with Gemini CLI by adding small delays (500ms-1s) between worker launches.

**Key benefit:** 4-8x throughput improvement with 100% reliability.

---

## The Problem

Gemini CLI v0.21.1 has race condition during startup when workers launch simultaneously:

```bash
# Pure parallel (FAILS)
gemini -p "task1" & gemini -p "task2" & wait
# Result: 0-byte files (silent failure)
```

**Root cause:** Race condition reading `~/.gemini/settings.json`

---

## The Solution

Add 1s delays between launches:

```bash
# Staggered (WORKS - 100% success)
gemini -p "task1" > out1.md &
sleep 1
gemini -p "task2" > out2.md &
wait
```

Workers run **simultaneously** after staggered startup!

---

## Quick Start

```bash
TASKS=("task1" "task2" "task3" "task4")

for i in "${!TASKS[@]}"; do
  gemini -p "${TASKS[$i]}" --yolo -o text > worker$i.md &
  sleep 1  # CRITICAL
done

wait
```

---

## Configuration

| Environment | Delay | Workers |
|-------------|-------|---------|
| Production | 1s | 4-6 |
| Development | 500ms | 4 |
| Conservative | 2s | 8 |

---

## Performance

| Workers | Time | vs Sequential |
|---------|------|---------------|
| 4 | ~63s | 3.8x faster |
| 6 | ~66s | 5.5x faster |
| 8 | ~68s | 7.1x faster |

---

## Best Practices

✅ Use 1s delay (proven reliable)
✅ Validate outputs (check file size)
✅ Limit to 6-8 workers
❌ Never use 0s delay (guaranteed fail)

---

## Tested Configurations (100% success)

- 4 workers × 1s delay ✅
- 6 workers × 1s delay ✅
- 8 workers × 1s delay ✅
- 4 workers × 500ms delay ✅

**Reference:** `~/.claude-memory/global/discoveries/gemini-research/2025-12-31/`
