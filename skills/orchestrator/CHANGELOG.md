# Changelog - Orchestrator Skill

All notable changes to the orchestrator skill will be documented in this file.

## [1.1.0] - 2025-12-31

### Added
- Staggered parallel execution pattern for Gemini CLI workers
- Comprehensive `STAGGERED-EXECUTION.md` technical guide
- `PROVIDER-LIMITS.md` - API quota constraints documentation
- Quota awareness in orchestration planning workflow
- Performance metrics: 4-8x throughput vs sequential execution
- 100% reliability with up to 8 parallel workers tested

### Changed
- Updated `SKILL.md` with staggered pattern examples and quota checking in planning workflow
- Updated `PATTERNS.md` with staggered parallel execution template
- Updated `AGENTS.md` parallel Gemini instances pattern
- All parallel execution code examples now include 1s `sleep` delays

### Fixed
- Gemini CLI race condition (Issue #3161) via staggered launch
- Silent failure when launching workers simultaneously

### Performance
- 4 workers: 3.8x faster than sequential
- 6 workers: 5.5x faster than sequential
- 8 workers: 7.1x faster than sequential

---

## [1.0.0] - 2025-12-30

### Added
- Initial orchestrator skill implementation
- Shell-As-Bus pattern documentation
- Agent catalog (Claude, Gemini, Local Model)
- 5 orchestration patterns
- Decision matrix for agent selection
- Multi-agent coordination patterns

### Documentation
- SKILL.md - Core orchestration principles
- PATTERNS.md - Detailed workflows
- AGENTS.md - Agent capabilities and composition

---

**Versioning:** Follows Semantic Versioning (MAJOR.MINOR.PATCH)
