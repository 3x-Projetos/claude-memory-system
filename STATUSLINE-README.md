# Claude Code Status Line - Real-Time Context & Usage Tracking

## Overview

Custom status line that displays **live context window %** and **token usage** during your entire Claude Code session - no more surprises at 80%!

## What It Shows

```
[Sonnet 4.5] CTX:[====------] 45% | TOK:106.2k(I:90.9k/O:15.2k) | COST:$0.023 | DIR:project-name | GIT:main
```

### Components

1. **Model Name**: Current Claude model (Sonnet 4.5, Opus 4.5, Haiku 4.0)
2. **Context Window**:
   - Visual bar: `[====------]` (10 chars, ASCII-safe)
   - Percentage: `45%` of context window used
   - Indicators:
     - ` ` (space) = 0-59% (OK)
     - `*` = 60-79% (Warning)
     - `!` = 80-100% (Critical)

3. **Token Usage**:
   - Total: `106.2k` tokens this session
   - Input: `90.9k` (I: prefix)
   - Output: `15.2k` (O: prefix)
   - Auto-formats: k for thousands (1000+ → 1.0k)

4. **Cost**: Session cost in USD (`$0.023`)

5. **Directory**: Current working directory name

6. **Git Branch** (if in git repo): `GIT:branch-name`

## Installation

Already installed! The configuration is in:
- Script: `~/.claude/statusline.py`
- Config: `~/.claude/settings.json`

## How It Works

### Updates
- Refreshes every ~300ms when conversation changes
- Shows **real-time context** from latest API call
- Tracks **cumulative tokens** across entire session

### Context Window Calculation
```python
current_tokens = input_tokens + cache_creation_tokens + cache_read_tokens
percent = (current_tokens / context_window_size) * 100
```

**Note**: Shows current context (what's in memory), not total tokens sent.

### Why This Matters

**Before**:
- ⚠️ Warning appears at ~80% (often too late!)
- ❌ Auto-compact surprise mid-task
- ❌ Lost conversation continuity

**After**:
- ✅ See context % from 0% onwards
- ✅ Plan ahead when approaching 60-70%
- ✅ Use `/end` proactively before hitting limits

## Planning Ahead

### Strategy

| Context % | Action |
|-----------|--------|
| 0-40% | Work freely |
| 40-60% | Be aware, plan to wrap up current task |
| 60-75% | Finish current task, prepare to `/end` |
| 75-85% | Use `/end` soon to save session cleanly |
| 85-95% | Use `/end` NOW (auto-compact imminent) |
| 95-100% | Auto-compact triggered (conversation reset) |

### Best Practices

1. **Monitor the bar**: Glance at status line periodically
2. **Plan exits**: When you see 60-70%, finish current task
3. **Use `/end` early**: Better to end at 75% than get auto-compacted at 85%
4. **Long sessions**: For complex work, break into multiple sessions with `/end` + `/continue`

## Customization

Edit `~/.claude/statusline.py` to customize:

### Change Bar Length
```python
bar_length = 10  # Change to 15, 20, etc.
```

### Add More Info
```python
# Add duration
duration_ms = data.get('cost', {}).get('total_duration_ms', 0)
duration_min = duration_ms / 60000
status += f" | TIME:{duration_min:.1f}m"
```

### Change Colors (Unix/Mac only)
```python
if percent >= 80:
    color = '\033[91m'  # Red
# ... etc
```

## Troubleshooting

**Status line doesn't appear**:
1. Check script is executable: `chmod +x ~/.claude/statusline.py`
2. Verify settings.json has statusLine config
3. Restart Claude Code session

**Shows "Error: ..."**:
- Check Python 3 is installed: `python3 --version`
- Test manually: `echo '{"model":{"display_name":"Test"},...}' | python ~/.claude/statusline.py`

**Context always shows 0%**:
- Normal at session start (no API calls yet)
- After first message, should update

**Git branch doesn't show**:
- Only shows if current directory is a git repo
- Check: `git branch --show-current`

## Technical Details

### JSON Input Schema
Claude Code sends this JSON via stdin:
```json
{
  "model": {"display_name": "Sonnet 4.5"},
  "context_window": {
    "context_window_size": 200000,
    "total_input_tokens": 90000,
    "total_output_tokens": 15000,
    "current_usage": {
      "input_tokens": 85000,
      "cache_creation_input_tokens": 3000,
      "cache_read_input_tokens": 2000
    }
  },
  "cost": {"total_cost_usd": 0.023},
  "workspace": {"current_dir": "/path/to/project"}
}
```

### Performance
- **Update frequency**: ~300ms
- **Execution time**: ~10-20ms (Python script)
- **Git check**: Cached, ~5ms
- **Total overhead**: Negligible

## Version History

**v1.0** (2025-12-28):
- Initial release
- Real-time context window tracking
- Token usage display
- Cost tracking
- Git branch support
- Windows UTF-8 compatibility

---

**References**:
- [Official Status Line Docs](https://code.claude.com/docs/en/statusline)
- [GitHub: ccstatusline](https://github.com/sirmalloc/ccstatusline)
- [Feature Request #15247](https://github.com/anthropics/claude-code/issues/15247)

**Note**: This feature was requested by many users and is now available through custom scripts. A built-in toggle may come in future Claude Code releases.
