---
name: orchestrator
description: Detailed orchestration patterns and workflows
version: 1.1.0
---

# Orchestration Patterns - Detailed Workflows

Based on community research (Gemini analysis, 2025-12-30).

---

## Pattern 1: Orchestrator-Workers (The "Boss" Pattern)

**Use Case:** Complex task with distinct, parallelizable components

**Structure:**
- Claude (Orchestrator) breaks task into sub-tasks
- Specialized Workers execute in parallel
- Claude synthesizes results

**Example: Security Audit + Documentation Update**

```bash
# Task: Audit codebase security AND update docs with findings

# Step 1: Claude creates plan
echo "Plan:
1. Gemini: Security audit (massive context)
2. Gemini: Documentation gaps analysis
3. Claude: Synthesize findings
4. Claude: Update docs with recommendations"

# Step 2: Launch parallel workers with STAGGERED execution
find src/ -name "*.py" -exec cat {} \; > /tmp/codebase.txt
find docs/ -name "*.md" -exec cat {} \; > /tmp/all-docs.txt

# Worker 1: Security audit
gemini -p "Comprehensive security audit. Check: SQL injection, XSS, secrets, insecure dependencies. Output markdown with severity levels." < /tmp/codebase.txt --yolo -o text > /tmp/security-audit.md &
sleep 1  # CRITICAL: Stagger to avoid Gemini CLI race condition

# Worker 2: Docs gaps analysis
gemini -p "Identify documentation gaps. Compare codebase features vs documented features. Output missing sections." < /tmp/all-docs.txt --yolo -o text > /tmp/docs-gaps.md &

# Wait for workers (they run simultaneously after staggered start!)
wait

# Step 3: Claude synthesizes
cat /tmp/security-audit.md
cat /tmp/docs-gaps.md

# Step 4: Claude updates docs
# (Claude writes updated documentation incorporating both findings)
```

**Benefits:**
- 2x faster (parallel execution)
- Leverages Gemini's massive context (1M+ tokens)
- Claude focuses on synthesis (its strength)

---

## Pattern 2: Evaluator-Optimizer (The "Review" Pattern)

**Use Case:** Code generation, creative writing, critical decisions

**Structure:**
1. Generator creates initial solution
2. Evaluator critiques/tests it
3. Generator refines based on feedback
4. Loop until quality threshold met

**Example: Async/Await Refactoring**

```bash
# Task: Refactor auth.py to async/await with validation

# Round 1: Generate
cat auth.py
# Claude refactors
cat > auth-async.py << 'EOF'
# ... Claude's async version ...
EOF

# Round 1: Evaluate
gemini -p "Review this async refactoring. Check for:
- Proper await usage
- Error handling preserved
- Race conditions
- Performance issues
Output specific issues with line numbers." < auth-async.py --yolo -o text > review-round1.md

# Round 1: Optimize
cat review-round1.md
# Claude fixes issues identified by Gemini

# Round 2: Re-evaluate
gemini -p "Final security review. Any remaining issues?" < auth-async-v2.py --yolo -o text > review-round2.md

cat review-round2.md
# If clean, apply changes
```

**Benefits:**
- Cross-validation (two perspectives)
- Catches issues Claude might miss
- Iterative improvement
- Higher quality output

**Variation: Test-Driven**
```bash
# Generator: Claude writes code
# Evaluator: pytest runs tests
pytest test_auth.py
# If fail, Claude fixes and loops
```

---

## Pattern 3: Hierarchical Teams (The "Corp" Pattern)

**Use Case:** Very large systems, multi-phase projects

**Structure:**
- L1: Claude (Strategic Orchestrator)
- L2: Domain Agents (Tactical Executors)
- L3: Specialized Tools (Operational Workers)

**Example: Full-Stack Feature Implementation**

```bash
# Task: Implement user authentication feature

# L1: Claude - Strategic Planning
cat > architecture-plan.md << 'EOF'
Feature: User Authentication
Components:
1. Backend: JWT generation, validation
2. Frontend: Login form, session management
3. Database: User schema migration
4. Tests: Unit + integration tests
EOF

# L2: Gemini - Backend Architecture Deep Dive
gemini -p "Design backend auth architecture for FastAPI. Include: JWT strategy, refresh tokens, middleware, error handling. Output detailed implementation plan." --yolo -o text > backend-architecture.md

# L2: Local Model - Generate Boilerplate
# (Local model generates repetitive code)
python local-agent.py "Generate FastAPI user CRUD endpoints with JWT auth" > backend/routes/auth.py

# L3: Claude - Review and Refine
cat backend/routes/auth.py
# Claude reviews local model output, fixes issues

# L2: Gemini - Frontend Best Practices
gemini -p "Research 2025 React authentication best practices. Include: token storage, refresh flow, protected routes." --yolo -o text > frontend-patterns.md

# L1: Claude - Implementation
cat frontend-patterns.md
# Claude implements React components following best practices

# L3: pytest - Testing
pytest tests/
# If fail, L1 Claude debugs
```

**Benefits:**
- Scales to very large projects
- Each layer focuses on its strength
- Clear delegation boundaries
- Parallel execution at each layer

---

## Pattern 4: Research-Implement-Validate (Workflow Pattern)

**Use Case:** Building features requiring current best practices

**Structure:**
1. Research: Gemini searches latest info
2. Implement: Claude codes following research
3. Validate: Gemini reviews for best practices compliance

**Example: Implement OAuth2 Integration**

```bash
# Phase 1: Research (Gemini - Search grounding)
gemini -p "Research OAuth2 integration best practices 2025. Include: PKCE flow, token storage, security considerations. Provide code examples." --yolo -o text > oauth2-research.md

# Phase 2: Implement (Claude - Coding)
cat oauth2-research.md
# Claude implements based on research
cat > auth/oauth2.py << 'EOF'
# ... implementation following best practices ...
EOF

# Phase 3: Validate (Gemini - Review)
gemini -p "Review this OAuth2 implementation against 2025 best practices. Check: PKCE compliance, token security, error handling." < auth/oauth2.py --yolo -o text > oauth2-validation.md

cat oauth2-validation.md
# Claude addresses any issues found
```

---

## Pattern 5: Bulk-Refine (Processing Pattern)

**Use Case:** Large repetitive tasks requiring refinement

**Structure:**
1. Bulk: Local model or Gemini processes volume
2. Refine: Claude reviews and improves quality

**Example: Generate 50 Unit Tests**

```bash
# Phase 1: Bulk Generation (Local Model)
for file in src/*.py; do
  python local-agent.py "Generate pytest unit tests for $(basename $file)" > "tests/test_$(basename $file)"
done

# Phase 2: Selective Refinement (Claude)
# Claude reviews complex tests, fixes edge cases
cat tests/test_auth.py
# Refine critical tests manually
```

---

## Decision Matrix for Pattern Selection

| Scenario | Pattern | Why |
|----------|---------|-----|
| Multiple independent tasks | Orchestrator-Workers | Parallelization |
| Need validation/review | Evaluator-Optimizer | Quality assurance |
| Multi-phase project | Hierarchical Teams | Complexity management |
| Requires latest info | Research-Implement-Validate | Current best practices |
| High volume + quality | Bulk-Refine | Efficiency + precision |

---

## Error Handling Across Patterns

### Try-Catch-Escalate Standard

```bash
# Try: Delegate to specialist
gemini -p "task" --yolo -o text > output.txt

# Catch: Check for errors
if [ $? -ne 0 ] || [ ! -s output.txt ]; then
  echo "Agent failed - escalating to Claude"
  # Escalate: Claude handles directly
  # ... Claude's implementation ...
else
  # Success: Use agent output
  cat output.txt
fi
```

### Fallback Chain

```bash
# Tier 1: Try Gemini (fast, massive context)
gemini -p "task" --yolo -o text > result.txt 2>/dev/null

# Tier 2: If fail, try local model
if [ ! -s result.txt ]; then
  python local-agent.py "task" > result.txt
fi

# Tier 3: If still fail, Claude handles
if [ ! -s result.txt ]; then
  # Claude executes directly
  echo "All agents failed - Claude executing"
fi
```

---

## Coordination Mechanisms

### File-Based State Sharing

```bash
# Shared state directory
mkdir -p .context/

# Agent 1 writes state
gemini -p "analyze requirements" --yolo -o text > .context/requirements.md

# Agent 2 reads state
cat .context/requirements.md
# Agent 2 uses this context for next task
```

### Progress Ledger (Claude's Internal State)

```markdown
# .context/progress.md (Claude maintains this)

## Completed
- [x] Requirements analysis (Gemini)
- [x] Architecture design (Claude)

## In Progress
- [ ] Backend implementation (Local Model)

## Pending
- [ ] Frontend implementation
- [ ] Testing
```

---

## Performance Optimization

### Staggered Parallel Execution Template (RECOMMENDED)

```bash
# CRITICAL: Use staggered launch to avoid Gemini CLI race condition (Issue #3161)
# Tested: 8 workers, 1s delay, 100% success rate, 4-8x throughput improvement!

TASKS=("task1" "task2" "task3" "task4" "task5" "task6")

# Launch workers with staggered start
for i in "${!TASKS[@]}"; do
  gemini -p "${TASKS[$i]}" --yolo -o text > /tmp/task$i.txt &
  sleep 1  # Minimum 500ms, recommend 1s for production
done

# Wait for all (they run simultaneously after staggered startup!)
wait

# Check results
for i in "${!TASKS[@]}"; do
  if [ -s /tmp/task$i.txt ]; then
    echo "Task $i: ✅ ($(wc -c < /tmp/task$i.txt) bytes)"
  else
    echo "Task $i: ❌ Failed (0 bytes)"
  fi
done
```

**Performance:** 6 workers × 1s stagger = ~66s total (vs 360s sequential = 5.5x faster!)

**Why not pure parallel?** Gemini CLI has race condition during startup. Pure parallel (0s delay) = 0% success. Staggered (1s delay) = 100% success.

### Sequential with Early Exit

```bash
# Stop on first failure
task1 && task2 && task3 || echo "Pipeline failed"
```

---

## Key Insights from Community (Gemini Research)

1. **Shell-As-Bus is most robust** - Simpler than LangChain/CrewAI
2. **Standardized interfaces critical** - Clean stdout, exit codes
3. **Skills-based delegation** - Teach Claude when/how via .md files
4. **Explicit planning mode** - "Create a plan utilizing agents"
5. **File-based coordination** - Shared .context/ directory

---

*Based on research: `~/.claude-memory/global/discoveries/gemini-research/agent-orchestration-report.md`*
