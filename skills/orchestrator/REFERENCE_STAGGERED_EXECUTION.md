# Quick Ref: Staggered Gemini Execution

> **Fast & Safe Parallelism**: Fixes CLI race conditions (Issue #3161) while retaining 4-8x speedup.

## 🚀 Quick Start
```bash
# Define independent tasks
TASKS=("audit_security" "check_style" "find_bugs" "review_docs")

# Launch workers with 1s stagger (CRITICAL)
for task in "${TASKS[@]}"; do
  gemini -p "Analyze: $task" < context.txt --yolo -o text > "$task.md" &
  sleep 1  # 🛑 Essential delay
done

# Wait for completion & verify
wait
ls -l *.md
```

## ⏱️ Delay Recommendations

| Environment | Delay | Reasoning |
| :--- | :--- | :--- |
| **Production** | `1.0s` | **Safest**. 100% reliability with 8+ workers. |
| **Development** | `0.5s` | Faster startup, minor risk of race condition. |
| **Heavy Load** | `2.0s` | Use if system/network is under high stress. |

## 📊 Performance Summary (6 Workers)

| Method | Total Time | Throughput | Success Rate |
| :--- | :--- | :--- | :--- |
| **Sequential** | ~360s | 1x | 100% |
| **Pure Parallel** | ~5s (Fail) | 0x | 0% (Race Cond.) |
| **Staggered** | **~66s** | **~5.5x** | **100%** |

## ⚠️ Common Pitfalls
*   **Missing `sleep`**: Causes 0% success rate (all fail at startup).
*   **Missing `&`**: Runs sequentially (slow).
*   **Shared Output File**: Workers overwriting each other (`>> out.txt` is risky, use unique files).
*   **No `wait`**: Script exits before workers finish.

## 📋 Strategy Selection

| Use **Staggered** When... | Use **Sequential** When... |
| :--- | :--- |
| Tasks are independent (Context A, B, C) | Task B depends on Task A result |
| Speed is critical (Batch processing) | Debugging complex logic |
| running > 2 heavy queries | Simple/Single quick query |
