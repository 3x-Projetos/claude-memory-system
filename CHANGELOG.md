# Changelog

All notable changes to Claude Memory System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.5.0] - 2025-12-31

### Added
- **Orchestrator Skill v1.1.0**: Multi-agent coordination system
  - Shell-As-Bus architecture for agent delegation
  - Staggered parallel execution pattern (4-8x throughput improvement)
  - 100% reliability with up to 8 parallel Gemini workers (tested)
  - Quota-aware planning workflow
  - 7 documentation files (SKILL.md, PATTERNS.md, AGENTS.md, PROVIDER-LIMITS.md, etc.)
- **PROVIDER-LIMITS.md**: API quota constraints documentation
  - Gemini free tier: ~20-25 workers/session (~10h reset)
  - Claude API constraints and usage strategies
  - LM Studio placeholder (pending multi-device sync)
  - Quota management patterns and fallback strategies

### Fixed
- **Gemini CLI Issue #3161 Workaround**: Parallel execution via staggered launch
  - Race condition occurs during startup initialization, not runtime
  - Solution: 500ms-1s delays between worker launches
  - Workers run simultaneously after staggered startup

### Performance
- **4 workers**: 3.8x faster than sequential execution
- **6 workers**: 5.5x faster than sequential execution
- **8 workers**: 7.1x faster than sequential execution
- **Context efficiency**: 44% token savings via worker delegation

### Research
- Comprehensive parallel execution research (~17.5KB documentation)
- Empirical testing: 6 scenarios validating staggered pattern
- Community best practices integration
- Direct API capabilities analysis

### Milestone
- **First commit produced via multi-agent workflow**: This release was researched, documented, and validated using the orchestrator pattern itself (self-referential implementation)

## [3.4.0] - 2025-12-29

### Added
- **Progressive Context Loading**: Complete strategy for efficient context management
  - Global CLAUDE.md with session best practices (~600 tokens)
  - Framework-specific CLAUDE.md (~400 tokens)
  - CLI-CONTEXT-LOADING.md documenting loading behavior
  - SESSION-TEMPLATES.md with 5 session type templates
  - Context budget guidelines (Quick Fix <25%, Feature <50%, Research <60%, Architecture <70%)
- **GitHub Labels System**: Complete issue organization
  - Priority labels (high, medium, low)
  - Type labels (bug, security, cleanup, documentation, enhancement, skill, review)
  - Status labels (monitoring, structure)
  - All issues #1-#13 properly labeled

### Changed
- Target context usage from ~90% to <50% for normal sessions
- 40-50% expected reduction in context usage per session

### Documentation
- PROGRESSIVE-LOADING-IMPLEMENTATION.md summarizing all improvements
- Comprehensive CLI loading sequence documentation
- Lazy-loading guidelines and anti-patterns

## [3.3.0] - 2025-12-29

### Changed
- **87-90% Context Reduction**: Skills compacted with SOTA pattern
- **scientist skill**: Reduced from 431 to 42 lines (90% reduction)
- **Config-driven cloud sync**: Path read from .config.json (not hardcoded)
- **Performance**: 10% startup improvement (~800 tokens saved per session)

### Added
- **skill-creator**: Meta-tool for automatic skill creation
- skills/scientist/GUIDE.md - Detailed documentation (on-demand loading)
- commands/archive/end-v2.3.md - Archived old version

## [3.0.0] - 2025-12-28

### Added
- **Skills System**: Auto-activation based on intent
- **Progressive Disclosure**: SKILL.md concise (<2,500 words) + detailed references
- **Multi-Device Awareness**: Skills understand cloud sync
- **3 Included Skills**:
  - 🔬 scientist: Universal scientific thinking framework
  - 🔄 session-continuity-assistant: Intelligent multi-device continuation
  - 📓 note-organizer: Systematic note processing
- .claude/skills/ directory for distributed skills
- Auto-discovery via description matching

### Changed
- Skills activate automatically when relevant (no explicit invocation needed)

## [2.3.1] - 2025-12-28

### Added
- **Auto Cloud Sync on /end**: Zero manual steps for multi-device sync
- Non-blocking sync (logs always saved locally first)
- Multi-device coordination with automatic pull --rebase
- User-configurable cloud path from .config.json
- Comprehensive error handling (conflicts, network, invalid paths)
- Informative automatic commit messages with device, provider, duration

### Changed
- /end command now automatically syncs to cloud (if configured)
- Sync workflow: copy → pull → commit → push → error handling

### Documentation
- .claude/workflows/cloud-sync-on-end.md

## [2.3.0] - 2025-12-26

### Added
- **Multi-Device Memory**: Access memories from any device
- **Optional Cloud Sync**: Framework works perfectly without cloud (local-only by default)
- No hardcoded URLs - user-configurable git repository
- Provider-agnostic cloud sync (GitHub, GitLab, Gitea, etc.)
- Bootstrap detection with interactive setup
- Web session integration for ephemeral VMs
- Seamless device handoff (work on Device A, continue on Device B)
- Conflict resolution with auto-merge by timestamp
- Device registry tracking all devices and last sync

### Added - Commands
- /setup-cloud: Interactive cloud sync configuration
- /disable-cloud: Disable cloud sync (return to local-only)

### Documentation
- .claude/MEMORY-ORGANIZATION.md: Local vs cloud architecture (17 KB)
- .claude/commands/setup-cloud.md: Complete setup guide
- .claude/handInput/: Web session integration guide
- .claude/workflows/: Organized workflows (7 files)

### Security
- Automatic PII redaction before cloud sync
- Privacy-first design

## [2.2.0] - 2025-12-XX

### Added
- **Multi-Provider Architecture**: Support for multiple AI providers (Claude, LMStudio, etc.)
- providers/ directory structure for modular provider integration
- Provider-specific workflows with command routing
- LMStudio session manager with auto-checkpoint
- Rich summary handoff for seamless continuity
- Context window tracking with automatic detection
- Cross-provider integration via unified timeline
- Granular permissions (RO/RW/APPEND) per provider and resource

### Documentation
- integration/provider-activities.md: Unified cross-provider timeline

## [2.1.0] - 2025-12-XX

### Added - Multi-Resolution Memory (M010.1)
- **Quick Memories**: Summarized versions (~50 lines) for fast startup
- Lazy loading: Context loaded on-demand after user choice
- Aggregation status visible without reading logs
- Temporal triggers (Friday/end-of-month)
- 84-88% token savings on /continue (~6,500 tokens saved)
- 6x more session time available (70k → 85k tokens)

### Added - Project-Centric Memory (M008)
- **Bidimensional Memory**: Time × Project organization
- Support for multiple active projects
- Project categories: Code, Creative, Physical, Personal, Social, Business, AI, Other
- .projects/ directory structure with .context.md, .status.md, .context.quick.md
- Commands: /projects, /switch [name], /project-status
- Efficient context switching with isolated memories

### Added - Performance Tracking (M009)
- Multi-model support (Claude Sonnet/Opus/Haiku, Gemini, local LLMs)
- Context window metrics and utilization tracking
- Comparative model analysis
- Automatic model detection
- Performance sweet spots identification

## [2.0.0] - 2025-12-XX

### Added
- **Hierarchical Memory System**:
  - Working Memory: Current session context (~50 lines)
  - Quick Memories: Fast startup (~50 lines safe)
  - Daily Logs: Detailed session records
  - Weekly Summaries: Aggregated logs ~100 lines (85% savings)
  - Monthly Summaries: High-level overview ~30 lines (93% savings)

- **Global Profile**:
  - Versioned user profile shared across projects
  - Multi-resolution (Full ~165 lines + Quick ~50 lines)
  - Automatic updates (monthly + threshold-based)
  - Versioned snapshots with complete changelog

- **Holistic Metrics** (7 Dimensions):
  1. Performance & Productivity
  2. Cognitive Load & Mental Energy
  3. Well-Being & Satisfaction
  4. Learning & Growth
  5. Human Connection & Relationships
  6. Physical Health & Sustainability
  7. Alignment & Purpose

### Changed
- Session continuity with zero context loss between sessions
- Privacy-first design with automatic PII redaction

---

## Version History Summary

| Version | Date | Key Feature | Impact |
|---------|------|-------------|--------|
| 3.4.0 | 2025-12-29 | Progressive Context Loading | -40-50% context usage |
| 3.3.0 | 2025-12-29 | SOTA Skills Optimization | -90% skill size |
| 3.0.0 | 2025-12-28 | Skills System | Auto-activation |
| 2.3.1 | 2025-12-28 | Auto Cloud Sync | Zero manual sync |
| 2.3.0 | 2025-12-26 | Optional Cloud Sync | Multi-device |
| 2.2.0 | - | Multi-Provider | Claude + LMStudio |
| 2.1.0 | - | Multi-Resolution | -88% tokens |
| 2.0.0 | - | Hierarchical Memory | Zero context loss |

---

**Latest version**: 3.4.0
**License**: MIT
**Repository**: https://github.com/3x-Projetos/claude-memory-framework

[Unreleased]: https://github.com/3x-Projetos/claude-memory-framework/compare/v3.4.0...HEAD
[3.4.0]: https://github.com/3x-Projetos/claude-memory-framework/compare/v3.3.0...v3.4.0
[3.3.0]: https://github.com/3x-Projetos/claude-memory-framework/compare/v3.0.0...v3.3.0
[3.0.0]: https://github.com/3x-Projetos/claude-memory-framework/compare/v2.3.1...v3.0.0
[2.3.1]: https://github.com/3x-Projetos/claude-memory-framework/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/3x-Projetos/claude-memory-framework/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/3x-Projetos/claude-memory-framework/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/3x-Projetos/claude-memory-framework/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/3x-Projetos/claude-memory-framework/releases/tag/v2.0.0
