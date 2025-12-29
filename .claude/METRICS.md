# Session Metrics

**Version**: 3.4
**Command**: `/reflect` (optional)

---

## How It Works

### Automatic (Every `/end`)
Claude logs performance metrics automatically:
- Session duration, files modified, commits
- Context usage (real + overhead)
- Task complexity, technologies used

### Manual (Optional `/reflect`)
Quick 4-question reflection (all optional):
1. **Satisfaction**: 1-10
2. **Energy**: Energizado / Neutro / Drenado
3. **Frustration**: Any blockers?
4. **Notes**: Personal observations

Saved to `.metrics-reflection.tmp` → auto-merged into session log on `/end`.

---

## When to Use `/reflect`

**You'll be reminded**:
- At `/end` - "Quick reflection before finishing?"
- Contextually - Claude suggests when detecting frustration/achievement

**Frequency**: Daily or weekly (whatever feels natural)

---

## Benefits

- Track productivity and well-being trends
- Identify energy patterns and frustrations
- Help Claude understand your state

**Privacy**: All local, never shared unless you configure cloud sync.

---

## Advanced Reference

Full holistic framework (7 dimensions): `archive/METRICS-FRAMEWORK.md`

Current implementation = essential metrics only, minimal overhead.
