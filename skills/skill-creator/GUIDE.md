# Skill Creation Guide - SOTA Patterns (v3.2)

## Context Optimization Learnings

### The Problem We Solved

**Before (v2.3)**:
- session-continuity-assistant: 1,252 words
- /end command: 284 lines
- Context usage: ~8,000 tokens on startup
- Verbose documentation loaded every time

**After (v3.2)**:
- session-continuity-assistant: 164 words (87% reduction)
- /end command: 58 lines (79.6% reduction)
- Context usage: ~7,200 tokens on startup (10% improvement)
- Details deferred to optional files

## SOTA Skill Design Pattern

### 1. Ultra-Compact SKILL.md (<200 words)

**Structure**:
```yaml
---
name: skill-name
description: One-line description (when to use)
version: 1.0.0
---

# Skill Title

## Workflow

1. **Step 1**: Clear action
2. **Step 2**: Clear action
3. **Step N**: Clear action

## Key Principle

**One sentence principle statement.**

---

Optional: GUIDE.md, EXAMPLES.md (load when needed)
```

### 2. Try-First Pattern (Don't Check, Just Try)

**Bad** (bloats context):
```markdown
1. Check if config exists
2. If exists, read cloud_path
3. If cloud_path set, try git pull
4. Handle various error cases
```

**Good** (compact):
```markdown
1. Read cloud_path from config and try git pull. On error, fall back to local.
```

**Why**: Error handling happens naturally. No need to pre-check conditions.

### 3. Lazy Loading Pattern

**Bad**:
```markdown
1. Load all project contexts
2. Load all session histories
3. Present options to user
```

**Good**:
```markdown
1. Load minimal state (session-state.md, 720 tokens)
2. Present options to user
3. **After user chooses**, load specific project context
```

**Why**: Don't load what might not be needed.

### 4. Config Reading Strategy

**Bad**:
```markdown
1. Read ~/.config.json to check if cloud sync is enabled
2. If enabled, read cloud_path
3. Proceed with operation
```

**Good**:
```markdown
1. Try operation using path from config. On error, skip gracefully.
```

**Exception**: Only read config when you MUST have the value before proceeding (e.g., need cloud_path for git operation).

### 5. Documentation Separation

**SKILL.md** (always loaded):
- Workflow steps only
- Key principle
- Reference to detailed docs

**GUIDE.md** (load on demand):
- Detailed examples
- Troubleshooting
- Edge cases
- Advanced patterns
- Design rationale

**EXAMPLES.md** (load on demand):
- Usage examples
- Common scenarios
- Before/after comparisons

### 6. Frontmatter Essentials

**Required**:
```yaml
name: skill-name           # Unique identifier
description: When to use   # Trigger conditions
version: 1.0.0            # Semantic versioning
```

**Optional**:
```yaml
license: See LICENSE.txt   # If needed
author: Name               # If sharing
```

## Skill Creation Checklist

- [ ] Skill solves recurring problem (not one-off)
- [ ] SKILL.md is <200 words
- [ ] Workflow uses numbered steps
- [ ] Try-first pattern applied (no unnecessary checks)
- [ ] Lazy loading implemented (defer details)
- [ ] Config reading minimized or eliminated
- [ ] Key principle stated clearly
- [ ] Optional docs in separate files (GUIDE.md, EXAMPLES.md)
- [ ] No auto-loading of detailed documentation

## Anti-Patterns to Avoid

### ❌ Verbose Instructions

Don't explain every detail in SKILL.md. Trust the agent to execute steps.

### ❌ Pre-Emptive Error Checking

Don't check if files exist, configs are set, etc. Just try the operation.

### ❌ Inline Examples

Don't put examples in SKILL.md. Move to EXAMPLES.md.

### ❌ Troubleshooting in Main Skill

Don't put troubleshooting guides in SKILL.md. Move to GUIDE.md.

### ❌ Reading Configs "Just In Case"

Don't read configs to check settings. Only read when you need the value.

### ❌ Loading All Context Upfront

Don't load everything. Load minimal state, wait for user decision, then load details.

## Versioning Strategy

**1.0.0**: Initial release
**1.1.0**: New features, backward compatible
**1.2.0**: More features
**2.0.0**: Breaking changes

## Testing Your Skill

1. **Context budget**: Does SKILL.md stay <200 words?
2. **Lazy loading**: Are optional docs in separate files?
3. **Try-first**: No unnecessary config checks?
4. **Clarity**: Can agent execute without confusion?
5. **Reusability**: Will this be used multiple times?

## Examples of Well-Designed Skills (v3.2)

### session-continuity-assistant (164 words)
- 6-step workflow
- Try-first cloud sync
- Lazy loading (project context loaded after user choice)
- Details in separate reference files

### end (156 words)
- 5-step workflow
- Non-blocking cloud sync
- Minimal state updates
- Archived verbose v2.3 command

### skill-creator (this skill!)
- ~150 words in SKILL.md
- SOTA patterns documented in GUIDE.md (this file)
- Context optimization focus

## Impact Metrics

**Session-continuity v1.0 → v2.0**:
- Word count: 1,252 → 164 (87% reduction)
- Context savings: ~4,000 tokens per invocation

**/end command v2.3 → v3.2**:
- Line count: 284 → 58 (79.6% reduction)
- Context savings: ~800 tokens per session

**Framework startup v3.1 → v3.2**:
- Startup context: ~8,000 → ~7,200 tokens (10% improvement)
- Cumulative savings: Significant over many sessions

## Future Optimizations

1. **Skill registry**: Central registry to avoid skill discovery overhead
2. **Compressed workflows**: Test even more compact patterns
3. **Context profiling**: Measure actual token usage per skill
4. **Skill dependencies**: Reference other skills without loading them

---

**Last Updated**: 2025-12-29 (v3.2 framework)
**Validated By**: Real-world testing, measurable context savings
