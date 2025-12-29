# Framework Tag Taxonomy

Complete reference for the claude-memory-system tag system used in notes, logs, and workflows.

## Document State Tags

**Workflow progression**:

- `[raw]` - Unprocessed input, needs organization
- `[prompt]` - Instructions for how to process
- `[organized]` - Structured output, processed
- `[session-log]` - Session activity recording

**Usage**: Track document transformation stages

## Content Classification Tags

### Decisions

- `[decision]` - Choice made, commitment established
- `[decision?]` - Tentative decision, needs confirmation

**Format**: `[decision] Description - Rationale`

**Example**: `[decision] Use git for cloud sync - Version control + familiar tooling`

### Actions

- `[action]` - Task to complete, deliverable
- `[action:done]` - Completed action (for tracking)

**Format**: `[action] Task - Owner - Deadline`

**Example**: `[action] Test on second device - Luis - Friday`

### Questions

- `[question]` - Open question, uncertainty
- `[question:answered]` - Question resolved

**Format**: `[question] What needs to be known - Why it matters`

**Example**: `[question] Which devices will sync? - Affects architecture`

### Insights

- `[insight]` - Key learning, realization
- `[pattern]` - Observed pattern, trend

**Format**: `[insight] What was learned - Implication`

**Example**: `[insight] Multi-resolution saves 84% tokens - Critical for scalability`

### References

- `[reference]` - External resource, citation
- `[link]` - URL reference

**Format**: `[reference] Resource name [URL if applicable]`

**Example**: `[reference] Claude Code Skills Docs [https://docs...]`

### Problems

- `[blocker]` - Impediment, prevents progress
- `[risk]` - Potential issue, not yet blocking
- `[issue]` - Problem identified, needs fix
- `[bug]` - Software defect

**Format**: `[blocker] What's blocking - Impact`

**Example**: `[blocker] Need decision on RACI ownership - Can't proceed with matrix`

## Priority Tags

Control urgency and scheduling:

- `[urgent]` - Immediate attention required (today)
- `[high]` - Important, should do soon (this week)
- `[medium]` - Normal priority (this month)
- `[low]` - Can defer (someday)

**Combine with content tags**:
- `[urgent] [action]` - Urgent task
- `[high] [question]` - Important question to resolve

## Project Tags

Associate content with projects:

- `[project:project-name]` - Links to specific project
- `[category:type]` - Project category (Code, Business, etc.)

**Example**: `[project:golfleet] [action] Complete RACI matrix`

## PII (Personally Identifiable Information) Tags

**Format**: `[PII:TYPE]value[/PII:TYPE]`

Protect sensitive information:

- `[PII:NAME]John Doe[/PII:NAME]`
- `[PII:EMAIL]user@example.com[/PII:EMAIL]`
- `[PII:PHONE]+1-555-0123[/PII:PHONE]`
- `[PII:ADDRESS]123 Main St, City[/PII:ADDRESS]`
- `[PII:COMPANY]Acme Corp[/PII:COMPANY]`
- `[PII:PROJECT]SecretProject[/PII:PROJECT]`

**Redaction**: Automatic via `.claude/redact-pii.py`
- `[PII:NAME]...[ /PII:NAME]` → `[REDACTED:NAME]`

## Temporal Tags (Implicit)

Time-based organization (not explicit tags, but log structure):

- `logs/daily/YYYY.MM.DD.md` - Day level
- `logs/weekly/YYYY.MM.weekN.md` - Week level
- `logs/monthly/YYYY.MM.md` - Month level

## Custom Tags

Framework supports custom tags. Guidelines:

**Naming**:
- Lowercase preferred: `[mytag]`
- Hyphens allowed: `[my-custom-tag]`
- No spaces: use hyphens instead

**Documentation**:
- Document custom tags in project `.context.md`
- Explain purpose and usage

**Examples**:
- `[experiment]` - Experimental feature
- `[deprecated]` - Old approach, being phased out
- `[spike]` - Time-boxed research

## Tag Combinations

Tags can be combined for rich semantics:

**Multiple priorities**:
- `[urgent] [high]` - Very high priority

**Complex items**:
- `[decision] [risk]` - Risky decision
- `[action] [blocker]` - Action that's blocked

**Project + content**:
- `[project:skills] [insight]` - Insight for skills project

**PII in actions**:
- `[action] Contact [PII:NAME]John[/PII:NAME] about...`

## Best Practices

### Use Consistently

Same tag for same concept:
- ✅ Always `[decision]`
- ❌ Mix `[decision]`, `[chose]`, `[selected]`

### Tag What Matters

Not everything needs tags:
- Tag: Decisions, actions, questions, insights
- Don't tag: Routine details, obvious facts

### Preserve Searchability

Tags enable `grep`:
```bash
grep -r "\[decision\]" ~/.claude-memory/
grep -r "\[action\].*urgent" ~/.claude-memory/
```

### Combine Wisely

Too many tags = noise:
- ✅ `[urgent] [action]`
- ❌ `[urgent] [high] [action] [important] [todo]`

## Tag Extraction

Use bundled script:

```bash
# Extract tags from file
cat notes.md | python extract_tags.py

# Extract tags from stdin
echo "[decision] Use git [action] Test it" | python extract_tags.py
```

## Version History

**v1.0.0** (2025-12-28)
- Initial taxonomy
- Framework standard tags
- PII protection tags
- Custom tag guidelines
