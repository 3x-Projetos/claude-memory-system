---
name: orchestrator
description: Available agents catalog and capabilities matrix
version: 1.1.0
---

# Agent Catalog - Available Specialists

Current agents available for delegation.

---

## Agent 1: gemini-specialist

**Capabilities:**
- Massive context analysis (1M-2M tokens)
- Google Search grounding (real-time information)
- Large codebase security audits
- Documentation synthesis (100+ files)
- Cross-validation and second opinions
- Architecture planning with latest best practices

**When to Use:**
- Context exceeds Claude's 200k window
- Need real-time information/research
- Large-scale analysis tasks
- Second opinion for critical decisions

**Invocation:**
```bash
# Analysis
gemini -p "analyze this for security issues" < large-codebase.txt --yolo -o text > audit.md

# Research (with Search grounding)
gemini -p "research OAuth2 2025 best practices" --yolo -o text > research.md

# Cross-validation
gemini -p "review this architecture for issues" < design.md --yolo -o text > review.md
```

**Performance:**
- Speed: Fast (Gemini Flash)
- Context: 1M-2M tokens (5-10x Claude)
- Cost: Free tier (1000 requests/day)
- Quality: High for analysis, variable for generation

**Limitations:**
- Less precise than Claude for implementation
- May hallucinate on creative tasks
- Requires --yolo for non-interactive mode

---

## Agent 2: local-model (Future)

**Capabilities:**
- Bulk/repetitive code generation
- Privacy-sensitive data processing
- Boilerplate generation
- Offline operation

**When to Use:**
- Processing sensitive/private data
- High-volume repetitive tasks
- Need offline capability
- Cost optimization (free, unlimited)

**Invocation:**
```bash
# Via LM Studio API
curl -s http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"local-model","messages":[{"role":"user","content":"task"}]}' | \
  jq -r '.choices[0].message.content'

# Or via wrapper script
python scripts/local-agent.py "generate CRUD endpoints"
```

**Performance:**
- Speed: Varies (depends on model size and hardware)
- Context: Limited (typically 4k-32k tokens)
- Cost: Free (runs locally)
- Quality: Lower than Claude/Gemini

**Status:** 🔴 Not yet configured

---

## Agent 3: claude (Self - Orchestrator)

**Capabilities:**
- High-precision code implementation
- Complex reasoning and architecture
- File operations (edit, write, read)
- Git operations
- Tool orchestration (this role!)

**When to Use:**
- High creativity/reasoning required
- Precision code implementation
- File system operations
- When other agents fail (escalation)

**Invocation:**
- No invocation needed (you are Claude!)
- Execute directly when appropriate

**Performance:**
- Speed: Moderate
- Context: 200k tokens
- Cost: Highest (Sonnet 4.5)
- Quality: Highest for implementation

**Strengths:**
- Best for final implementation
- File operations
- Complex reasoning
- Orchestration/synthesis

---

## Capability Matrix

| Capability | Claude | Gemini | Local Model |
|------------|--------|--------|-------------|
| **Context Window** | 200k | 1M-2M | 4k-32k |
| **Code Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Speed** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Cost** | $$$ | $ | Free |
| **Analysis** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Generation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Real-time Info** | ❌ | ✅ | ❌ |
| **Privacy** | ⚠️ API | ⚠️ API | ✅ Local |
| **File Ops** | ✅ | ❌ | ❌ |

---

## Decision Framework

### When to use Claude (execute directly):
```yaml
Task requires:
  - High precision implementation
  - File system operations
  - Complex architecture decisions
  - Git operations
  - When context < 150k tokens
```

### When to delegate to Gemini:
```yaml
Task requires:
  - Massive context (>200k tokens)
  - Real-time information/research
  - Large-scale analysis
  - Second opinion/cross-validation
  - Latest best practices (Search grounding)
```

### When to delegate to Local Model:
```yaml
Task requires:
  - Privacy (sensitive data)
  - High volume/repetitive work
  - Offline operation
  - Cost optimization
  - When quality threshold is lower
```

---

## Agent Composition Patterns

### Pattern: Claude + Gemini (Most Common)

**Use Case:** Gemini analyzes/researches, Claude implements

```bash
# Gemini: Research
gemini -p "research microservices patterns for e-commerce" --yolo -o text > research.md

# Claude: Read and implement
cat research.md
# Claude implements based on research findings
```

### Pattern: Gemini + Local + Claude (Full Stack)

**Use Case:** Gemini plans, Local generates boilerplate, Claude refines

```bash
# Gemini: Architecture planning
gemini -p "design auth system architecture" --yolo -o text > architecture.md

# Local: Generate boilerplate
python local-agent.py "generate auth endpoints from $(cat architecture.md)" > boilerplate.py

# Claude: Review and refine
cat boilerplate.py
# Claude fixes issues, adds business logic
```

### Pattern: Staggered Parallel Gemini Instances (UPDATED v1.1.0)

**Use Case:** Multiple independent analyses

```bash
# CRITICAL: Use 1s stagger to avoid Gemini CLI race condition (Issue #3161)
# Result: 100% success rate, 3x faster than sequential!

# Analysis 1: Security
gemini -p "security audit" < codebase.txt --yolo -o text > security.md &
sleep 1  # Stagger prevents race condition

# Analysis 2: Performance
gemini -p "performance analysis" < codebase.txt --yolo -o text > performance.md &
sleep 1

# Analysis 3: Best practices
gemini -p "code quality review" < codebase.txt --yolo -o text > quality.md &

wait  # All 3 workers run simultaneously after staggered start!

# Claude: Synthesize all findings
cat security.md performance.md quality.md
# Create unified improvement plan
```

**Performance:** 3 workers staggered = ~62s (vs 180s sequential = 3x faster!)
**Reliability:** 100% success rate (tested with 8 workers)

---

## Adding New Agents

To add a new agent to the catalog:

1. **Create CLI wrapper** (if needed)
   ```bash
   # Example: agents/my-agent.sh
   #!/bin/bash
   # Standardized interface
   task="$1"
   # ... invoke actual agent ...
   echo "Task completed. Result: ..."
   ```

2. **Document in this file**:
   - Capabilities
   - When to use
   - Invocation examples
   - Performance characteristics

3. **Test integration**:
   - Verify stdout is clean
   - Check exit codes work
   - Validate file outputs

4. **Update Decision Matrix** above

---

## Future Agents (Roadmap)

### Agent: code-reviewer (Specialized Tool)
- **Purpose:** Automated code review with industry standards
- **Implementation:** Static analysis + AI review
- **Status:** Planned

### Agent: test-generator (Specialized Tool)
- **Purpose:** Comprehensive test suite generation
- **Implementation:** pytest + coverage analysis
- **Status:** Planned

### Agent: doc-generator (Specialized Tool)
- **Purpose:** API documentation from code
- **Implementation:** Parsing + template generation
- **Status:** Planned

---

## Agent Health Monitoring

### Check Agent Availability

```bash
# Check Gemini
gemini --version || echo "Gemini unavailable"

# Check Local Model (future)
curl -s http://localhost:1234/health || echo "Local model unavailable"
```

### Fallback Chain

```yaml
Primary: gemini-specialist
Fallback 1: local-model (if sensitive data)
Fallback 2: claude (always available)
```

---

*This catalog is maintained as agents are added/removed. Update this file when agent capabilities change.*

**Last updated:** 2025-12-30
**Active agents:** 2 (Claude, Gemini)
**Planned:** 1 (Local Model)
