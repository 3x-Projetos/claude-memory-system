# Claude Memory System - v3.3

Sistema completo de memória persistente, skills otimizados e logging para Claude CLI.

> **Versão**: 3.3
> **Data**: 2025-12-29
> **Autor**: Desenvolvido colaborativamente com Claude
> **Framework**: SOTA Compact Skills Pattern (87% context reduction)

---

## 🎯 O que é isso?

Um framework que permite ao Claude:
- **Lembrar** de sessões anteriores (multi-device com cloud sync)
- **Retomar** trabalho de onde parou (continuidade automática)
- **Skills System** para workflows reutilizáveis (<200 palavras, 87-90% redução)
- **Registrar** todas as atividades (logs estruturados)
- **Sincronizar** entre dispositivos (opcional, via git)

Transforma o Claude CLI em um assistente com memória persistente e context-optimized skills.

---

## 📊 Performance Highlights (v3.3)

| Component | Before | After | Reduction |
|-----------|--------|-------|-----------|
| session-continuity | 1,252 words | 164 words | **87%** ✅ |
| /end command | 284 lines | 58 lines | **79.6%** ✅ |
| scientist skill | 431 lines | 42 lines | **90%** ✅ |
| Startup context | ~8,000 tokens | ~7,200 tokens | **10%** ✅ |

**Novo**: skill-creator meta-tool (automates SOTA pattern creation)

---

## ⚡ Quick Start

```bash
/continue  # Retoma última sessão (auto cloud sync)
/end       # Finaliza e salva sessão (auto cloud sync)
```

---

## 🛠️ Skills Disponíveis (v3.3)

| Skill | Trigger | Descrição |
|-------|---------|-----------|
| **session-continuity-assistant** | `/continue` | Resume sessão anterior |
| **end** | `/end` | Finaliza sessão, logs, cloud sync |
| **scientist** | Systematic inquiry | Framework científico universal (compacto) |
| **note-organizer** | `/organize` | Organiza notas [raw] → [organized] |
| **skill-creator** | Create skill | Meta-tool para criar skills SOTA |

---

## 🎨 SOTA Skills Pattern

### Princípios de Design

1. **Ultra-compact SKILL.md** (<200 palavras, sempre carregado)
2. **Try-first pattern** (não checar configs, tentar + handle errors)
3. **Lazy loading** (carregar detalhes só quando necessário)
4. **Docs separados** (GUIDE.md carregado on-demand)

**Guia completo**: `.claude/skills/skill-creator/GUIDE.md`

---

## 🌐 Cloud Sync (Opcional)

Multi-device workflow com zero comandos manuais:

```bash
# Device A
/end  # Auto-commit + push para cloud

# Device B
/continue  # Auto-pull, vê trabalho do Device A
```

**Configurar**: Execute `/setup-cloud` e siga prompts

---

## 📋 Comandos

| Comando | Descrição |
|---------|-----------|
| `/continue` | Retoma última sessão (cloud sync + minimal load) |
| `/end` | Finaliza sessão (logs + state + timeline + cloud sync) |
| `/switch [project]` | Muda contexto de projeto |
| `/memory` | Lista ferramentas disponíveis |
| `/organize` | Processa workflow de notas |
| `/setup-cloud` | Configura cloud sync (one-time) |

---

## 📁 Estrutura

```
~/.claude/
├── README.md                           # Este arquivo
├── skills/                             # Skills system (v3.0+)
│   ├── session-continuity-assistant/
│   │   ├── SKILL.md                    # Compacto (<200 palavras)
│   │   └── references/                 # Docs detalhados (on-demand)
│   ├── scientist/
│   │   └── SKILL.md                    # Compacto (42 linhas)
│   ├── skill-creator/
│   │   ├── SKILL.md
│   │   └── GUIDE.md                    # Padrões SOTA documentados
│   ├── note-organizer/
│   └── end/
├── commands/                           # Slash commands compactos
│   ├── continue.md                     # Chama session-continuity skill
│   ├── end.md                          # Chama end skill
│   └── archive/                        # Versões antigas (referência)
└── workflows/                          # Workflows detalhados (archive)

~/.claude-memory/                       # Storage local
├── .config.json                        # Configuração
├── providers/claude/
│   ├── session-state.md                # Estado atual
│   └── logs/daily/YYYY.MM.DD.md        # Logs diários
├── projects/[name]/
│   ├── .context.md                     # Contexto completo
│   └── .status.md                      # Roadmap
└── integration/
    └── provider-activities.quick.md    # Apenas recentes

~/.claude-memory-cloud/                 # Cloud repo (opcional)
└── (mesma estrutura, synced via git)
```

---

## 🔧 Criando Skills

Use o skill-creator:

```bash
# Invoque o skill-creator
User: "Create a new skill for..."

# Skill-creator vai:
- Pedir requisitos
- Gerar SKILL.md (<200 palavras)
- Criar GUIDE.md opcional (docs on-demand)
- Seguir padrões SOTA automaticamente
```

**Abordagem manual**: Veja `.claude/skills/skill-creator/GUIDE.md`

---

## 📝 Changelog

### v3.3 (2025-12-29)
- ✨ skill-creator: Meta-tool para criar skills SOTA
- ✨ scientist skill: Compactado para 42 linhas (90% redução)
- ✨ Princípios SOTA documentados (skill-creator/GUIDE.md)
- ✨ /continue: Cloud path config-driven (não hardcoded)
- 🎯 3 major skills otimizados, criação automatizada

### v3.2 (2025-12-29)
- ✨ session-continuity v2.0: 164 palavras (87% redução)
- ✨ /end command: 58 linhas (79.6% redução)
- ✨ Command/skill precedence resolvido
- 🎯 10% startup context reduction validada

### v3.0-3.1 (2025-12-28)
- ✨ Skills System + auto cloud sync
- ✨ Padrões SOTA estabelecidos

### v2.3 (2025-12-26)
- ✨ Cloud sync opcional + multi-device

### v1.0 (2025-11-15)
- ✨ Sistema inicial

---

## 🎓 Filosofia

### Por que Skills Compactos?

**Problema**: Workflows tradicionais carregavam 1,000+ palavras sempre, desperdiçando context budget.

**Solução**: Padrão SOTA compacto
- SKILL.md: <200 palavras (sempre carregado)
- GUIDE.md: Detalhes (carregado apenas quando necessário)
- Resultado: 87-90% economia de contexto

### Por que Cloud Sync?

**Problema**: Comandos git manuais error-prone, interrompem fluxo.

**Solução**: Auto-sync no /end e /continue
- Non-blocking (logs salvos localmente primeiro)
- Multi-device aware (pull --rebase)
- Zero comandos manuais

---

## 🔗 Links

- **Framework**: https://github.com/3x-Projetos/claude-memory-framework
- **Cloud Example**: https://github.com/3x-Projetos/claude-memory-cloud
- **SOTA Design Guide**: `.claude/skills/skill-creator/GUIDE.md`

---

## 📄 Licença

Livre para usar, modificar e distribuir. Sistema desenvolvido colaborativamente com Claude.

---

**Pronto para começar? Execute `/continue` no Claude CLI!**

**v3.3 - SOTA Compact Skills - 87% Context Reduction - Multi-Device Sync**
