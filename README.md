# Claude Memory System

Sistema de memória hierárquica para Claude CLI com métricas holísticas de impacto humano.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude CLI](https://img.shields.io/badge/Claude-CLI-orange.svg)](https://github.com/anthropics/claude-code)
[![Version](https://img.shields.io/badge/version-3.0-blue.svg)](https://github.com/3x-Projetos/claude-memory-system/releases)

---

## 🎯 O Que É?

Sistema completo de memória persistente e hierárquica para Claude CLI que:

- **Economiza até 88% de tokens** no startup (~6.500 tokens) com multi-resolution memory
- **Memória bidimensional** (tempo × projeto) para organização eficiente
- **Personaliza colaboração** através de perfil adaptativo do usuário
- **Tracking holístico** de impacto humano (não apenas produtividade)
- **Multi-agent support** com performance tracking por modelo
- **Zero perda de contexto** entre sessões
- **Privacidade first** com redação automática de PII
- **Skills System** com auto-activation baseada em intent
- **Cloud sync automático** multi-device sem configuração manual

---

## ✨ Features

### 🆕 v3.0 - Skills System (2025-12-28)
- **Auto-Activation Skills**: Skills que ativam automaticamente baseado em descrição (intent-based)
- **Progressive Disclosure**: SKILL.md conciso (<2,500 palavras) + references/ detalhados
- **Multi-Device Aware**: Skills entendem cloud sync e coordenação entre devices
- **3 Skills Incluídas**:
  - 🔬 **scientist**: Framework científico universal para investigação rigorosa
  - 🔄 **session-continuity-assistant**: Continuação inteligente multi-device aware
  - 📓 **note-organizer**: Processamento e organização sistemática de notas

**Skills Architecture**:
- `.claude/skills/`: Skills distribuídas com framework
- `~/.claude/skills/`: Skills pessoais instaladas pelo usuário
- Auto-discovery via description matching (sem invocação explícita)
- Integração seamless com comandos/workflows existentes

**Uso**:
- Skills ativam automaticamente quando relevantes
- Nenhum comando especial necessário
- Framework detecta intent e carrega skill apropriada

### 🆕 v2.3.1 - Auto Cloud Sync on /end (2025-12-28)
- **Automatic Sync**: `/end` agora faz git sync automático para cloud repo
- **Non-Blocking**: Sync nunca bloqueia finalização (logs sempre salvos localmente primeiro)
- **Multi-Device Coordination**: Pull --rebase automático antes de commit (evita conflicts)
- **User-Configurable**: Cloud path lido de `.config.json` (não hardcoded!)
- **Comprehensive Error Handling**: Conflicts, network errors, invalid paths tratados gracefully
- **Informative Commits**: Mensagens descritivas com device, provider, duration, metrics

**Processo automático**:
1. Copia `~/.claude-memory/` → `$CLOUD_PATH` (user-configured)
2. `git pull --rebase` (integra mudanças de outros devices)
3. `git commit` com mensagem descritiva automática
4. `git push` para repositório remoto
5. Tratamento graceful de todos os erros (non-blocking)

**Resultado**: Zero passos manuais para sync multi-device! 🚀

### 🆕 v2.3 - Optional Cloud Sync (2025-12-26)
- **Multi-Device Memory**: Acesse memórias de qualquer dispositivo (laptop, desktop, mobile, VM)
- **Optional Cloud Sync**: Framework funciona perfeitamente SEM cloud (local-only por padrão)
- **No Hardcoded URLs**: Usuários configuram seu próprio repositório cloud
- **Provider Agnostic**: Suporta qualquer git provider (GitHub, GitLab, Gitea, etc.)
- **Bootstrap Detection**: Setup interativo detecta e configura cloud automaticamente
- **Web Session Integration**: Integração de sessões web (ephemeral VMs) via export manual
- **Privacy First**: PII redação automática antes de sync para cloud
- **Seamless Handoff**: Trabalhe em Device A, continue em Device B sem perder contexto
- **Conflict Resolution**: Auto-merge por timestamp, preserva ambas versões em conflito
- **Device Registry**: Rastreamento de todos dispositivos e último sync

**Comandos novos**:
- `/setup-cloud`: Configuração interativa de cloud sync (clone existente OU initialize novo)
- `/disable-cloud`: Desabilita cloud sync (volta para local-only)

**Documentação**:
- `.claude/MEMORY-ORGANIZATION.md`: Arquitetura local vs cloud (17 KB)
- `.claude/commands/setup-cloud.md`: Guia completo de setup
- `.claude/workflows/cloud-sync-on-end.md`: 🆕 Auto-sync workflow
- `.claude/handInput/`: Web session integration guide
- `.claude/workflows/`: Workflows organizados (7 arquivos)

### 🆕 v2.2 - Multi-Provider Support (M011)
- **Multi-Provider Architecture**: Suporte para múltiplos providers (Claude, LMStudio, etc.)
- **Estrutura `providers/`**: Integração modular por provider (claude, lmstudio)
- **Provider-Specific Workflows**: Roteamento de comandos por provider
- **LMStudio Session Manager**: Auto-checkpoint e persistência de sessão
- **Rich Summary Handoff**: Resumos estruturados para continuidade seamless
- **Context Window Tracking**: Monitoramento automático (detecta configuração real)
- **Cross-Provider Integration**: Timeline unificada via `integration/provider-activities.md`
- **Permissões Granulares**: RO/RW/APPEND por provider e recurso

### 🆕 v2.1 - Multi-Resolution Memory (M010.1)
- **Quick Memories**: Versões resumidas (~50 linhas) para startup rápido
- **Lazy Loading**: Contexto carregado sob demanda após escolha do usuário
- **Aggregation Status**: Visível sem ler logs (gatilhos sexta/último dia)
- **84-88% economia** no `/continue` (~6.500 tokens economizados)
- **6x mais tempo de sessão** disponível (70k → 85k tokens)

### 🆕 v2.1 - Project-Centric Memory (M008)
- **Memória bidimensional**: Tempo × Projeto
- **4 projetos ativos**: Memory System, Hybrid Agent, Creative Workflow, Remote Access
- **Categorias**: Code, Creative, Physical, Personal, Social, Business, AI, Other
- **Comandos**: `/projects`, `/switch [name]`, `/project-status`
- **Context switching** eficiente com memórias isoladas

### 🆕 v2.1 - Performance Tracking (M009)
- **Multi-model support**: Claude Sonnet/Opus/Haiku, Gemini, local LLMs
- **Context window metrics**: Utilização, otimização, sweet spots
- **Comparative analysis**: Qual modelo usar para cada tarefa
- **Auto-detection**: Identifica modelo automaticamente

### Memória Hierárquica
- **Working Memory**: Contexto da sessão atual (~50 linhas)
- **Quick Memories**: Startup rápido (~50 linhas safe)
- **Logs Diários**: Sessões detalhadas
- **Resumos Semanais**: Agregação ~100 linhas (85% economia)
- **Resumos Mensais**: Alto nível ~30 linhas (93% economia)

### Perfil Global Versionado
- Compartilhado entre projetos
- **Multi-resolution**: Full (~165 linhas) + Quick (~50 linhas)
- Atualização automática (mensal + threshold)
- Snapshots versionados
- Changelog completo

### Métricas Holísticas (7 Dimensões)
1. Performance & Productivity
2. Cognitive Load & Mental Energy
3. Well-Being & Satisfaction
4. Learning & Growth
5. Autonomy & Empowerment
6. Collaboration Quality
7. Life Integration

### Sistema de Privacidade
- PII marcado e redacted automaticamente
- Dados completos localmente
- Transmissão apenas de dados safe

### Graceful Shutdown
- SessionStart/SessionEnd hooks
- Zero perda de sessões (mesmo sem `/end`)
- Rastreamento individual por sessão

### Auto-Aprovação Multi-Nível
- 4 níveis: off / edits / bash / all
- Toggle em tempo real
- Controle granular por projeto

---

## 🚀 Quick Start

### Instalação

**Opção 1: Clone este repo**
```bash
git clone https://github.com/3x-Projetos/claude-memory-system.git
cd claude-memory-system

# Usar framework neste diretório
# (já configurado e pronto)
```

**Opção 2: Bootstrap em projeto existente**
```bash
# Clone repo temporário
git clone https://github.com/3x-Projetos/claude-memory-system.git /tmp/cms

# Execute bootstrap no seu projeto
bash /tmp/cms/.claude/setup-claude-memory.sh /path/to/your/project

# Cleanup
rm -rf /tmp/cms
```

### Configuração

1. **Reinicie Claude CLI** (para registrar hooks, comandos e skills)

2. **Primeiro uso**:
```bash
# Inicia sessão carregando framework
/start
```

3. **Ao final**:
```bash
# Finaliza e registra sessão
# 🆕 Agora faz cloud sync automático!
/end
```

### Workflow Típico

```bash
# Segunda-feira (retomar trabalho)
/continue
# ... trabalho ...
/end      # 🆕 Auto-sync para cloud!

# Meio da semana (nova feature)
/new
# ... trabalho ...
/reflect  # opcional: registrar well-being
/end      # 🆕 Auto-sync para cloud!

# Fim da semana
/aggregate week

# Início do mês
/aggregate month
```

---

## 📚 Documentação

### Arquivos Principais

- **`.claude-memory.md`**: Índice central de ferramentas e workflows
- **`.claude/IMPLEMENTATION-PLAN.md`**: Plano completo de implementação
- **`.claude/METRICS-FRAMEWORK.md`**: Framework de métricas holísticas
- **`.claude/README.md`**: Documentação técnica detalhada
- **`.claude/QUICKSTART.md`**: Guia rápido de 5 minutos

### Workflows Documentados

1. **`.workflow-claude-notes-organization.md`**: Organização de notas
2. **`.workflow-session-logging.md`**: Logging de sessões
3. **`.workflow-session-continuity.md`**: Continuidade entre sessões
4. **`.workflow-weekly-aggregation.md`**: Agregação semanal
5. **`.workflow-monthly-aggregation.md`**: Agregação mensal
6. **`.workflow-profile-update.md`**: Atualização de perfil
7. **`.workflow-metrics-collection.md`**: Coleta de métricas
8. **`.workflow-cloud-sync-on-end.md`**: 🆕 Auto-sync workflow

### Comandos Slash

| Comando | Descrição |
|---------|-----------|
| `/start` | Carrega framework, pergunta se continua ou inicia novo |
| `/continue` | Retoma trabalho com quick memories (84-88% economia) |
| `/new` | Nova atividade (awareness sem pressão) |
| `/memory` | Consulta ferramentas disponíveis |
| `/organize` | Organiza notas com workflow padrão |
| `/end` | 🆕 **Finaliza sessão + auto cloud sync!** |
| `/update-profile` | Atualiza perfil global manualmente |
| `/reflect` | Registra métricas de well-being |
| `/aggregate week\|month` | Força agregação temporal |
| `/auto-approve on\|bash\|all\|off` | Toggle auto-aprovação |
| `/projects` | Dashboard multi-projeto (categorizado) |
| `/switch [name]` | Muda contexto para projeto específico |
| `/project-status [name]` | Atualiza status/roadmap de projeto |
| `/setup-cloud` | Configuração interativa de cloud sync |
| `/disable-cloud` | Desabilita cloud sync (local-only) |

### Skills (v3.0)

Skills ativam **automaticamente** quando relevantes (intent-based):

| Skill | Trigger Examples | Descrição |
|-------|------------------|-----------|
| 🔬 **scientist** | "investigate", "analyze systematically", "evidence-based" | Framework científico universal |
| 🔄 **session-continuity-assistant** | "continue session", "resume work", "what was I doing" | Continuação inteligente multi-device |
| 📓 **note-organizer** | "organize notes", "[raw]", "[organized]" | Processamento sistemático de notas |

**Sem comandos especiais**: Skills ativam automaticamente baseado no seu input!

---

## 🏗️ Arquitetura

### Estrutura de Diretórios

**Diretório de Trabalho** (seu projeto):
```
your-project/  (ou qualquer diretório onde você trabalha)
├── .projects/                     # v2.1 - Project-Centric Memory
│   ├── README.md
│   └── [project-name]/
│       ├── .context.md            # Contexto completo do projeto
│       ├── .context.quick.md      # Contexto resumido (~30 linhas)
│       └── .status.md             # Roadmap, decisões, métricas
└── .claude/                       # Framework (pode ser instalado globalmente)
    ├── commands/                  # 14 slash commands
    │   ├── end.md                 # 🆕 v2.3.1 - Atualizado com auto-sync
    │   ├── projects.md            # Dashboard multi-projeto
    │   ├── switch.md              # Context switching
    │   ├── project-status.md      # Status update
    │   ├── setup-cloud.md         # v2.3 - Cloud sync setup
    │   └── disable-cloud.md       # v2.3 - Disable cloud sync
    ├── skills/                    # 🆕 v3.0 - Skills System
    │   ├── scientist/             # Scientific thinking framework
    │   ├── session-continuity-assistant/  # Smart continuation
    │   └── note-organizer/        # Note processing
    ├── handInput/                 # v2.3 - Manual input directory
    ├── workflows/                 # v2.3 - Organized workflows
    │   ├── cloud-sync-on-end.md   # 🆕 v2.3.1 - Auto-sync docs
    │   └── .workflow-*.md         # 7 workflow docs
    ├── performance/               # v2.1 - Performance Tracking
    │   ├── README.md
    │   ├── TEMPLATE-performance-profile.md
    │   └── profiles/
    │       └── claude-sonnet-4.5.md
    ├── redact-pii.py              # Sistema de privacidade + quick gen
    ├── auto-approve-edits.py      # Auto-aprovação multi-nível
    ├── session-start.py           # Graceful shutdown (parte 1)
    ├── session-auto-end.py        # Graceful shutdown (parte 2)
    ├── settings.json              # Hooks configurados
    ├── setup-claude-memory.sh     # Bootstrap script
    ├── AGENT-MODEL-DETECTION.md   # Auto-detecção de modelo
    ├── MEMORY-IMPROVEMENTS.md     # Tracking de melhorias
    ├── MEMORY-ORGANIZATION.md     # v2.3 - Local vs Cloud architecture
    ├── METRICS-FRAMEWORK.md       # Framework de métricas
    └── IMPLEMENTATION-PLAN.md     # Plano completo
```

**Nota**: O framework evoluiu de memória local por projeto para memória global compartilhada. A estrutura acima mostra apenas os arquivos específicos do projeto. A maior parte da memória (session state, logs, perfil) agora reside em `~/.claude-memory/` (ver abaixo).

---

### Memória Global (centralizada, compartilhada)

**Principal estrutura de memória** (fora do projeto, `~/.claude-memory/`):
```
~/.claude-memory/                  # Memória central do framework
├── .config.json                   # v2.3 - Sync configuration
│                                  #   - sync_enabled: true/false
│                                  #   - cloud_repo: user's git URL
│                                  #   - cloud_path: user's local path
│                                  #   - device_name, providers, etc.
│
├── global-memory.md               # Perfil do usuário (completo com PII)
├── global-memory.safe.md          # Auto-gerado (PII redacted)
├── global-memory.quick.md         # v2.1 - Resumido (~50 linhas)
│
├── profile-history/               # Snapshots versionados do perfil
├── profile-changelog.md           # Histórico de mudanças
│
├── projects/                      # Referências a projetos ativos
│
├── providers/                     # v2.2 - Multi-Provider Support
│   ├── README.md                  # Documentação completa
│   │
│   ├── claude/                    # Provider Claude CLI
│   │   ├── session-state.md       # Working memory da sessão atual
│   │   ├── session-state.quick.md # Versão resumida
│   │   ├── logs/
│   │   │   ├── daily/             # Logs detalhados por dia
│   │   │   ├── weekly/            # Resumos semanais (~85% economia)
│   │   │   └── monthly/           # Resumos mensais (~93% economia)
│   │   └── web-sessions/          # v2.3 - Exported web sessions
│   │
│   └── lmstudio/                  # Provider LMStudio (mesma estrutura)
│       ├── session-state.md
│       ├── session-state.quick.md
│       └── logs/daily/
│
└── integration/                   # v2.2 - Cross-Provider Integration
    ├── provider-activities.md     # Timeline unificada (todos providers)
    └── provider-activities.quick.md
```

**Por que memória global?**
- ✅ Compartilhada entre todos os projetos (perfil único)
- ✅ Evita duplicação de logs e configuração
- ✅ Facilita multi-provider (Claude + LMStudio)
- ✅ Simplifica cloud sync (um repo, todos os devices)
- ✅ Mantém projetos limpos (apenas contexto específico)

---

### Cloud Memory (opcional, v2.3+)

**Estrutura de sincronização multi-device** (opcional, user-configured path):
```
$CLOUD_PATH/                       # v2.3 - Multi-device sync (user-configured!)
├── .gitignore                     # Privacy-first rules
├── .sync-config.json              # Sync preferences
├── README.md                      # Git guide for users
├── global-memory.md               # 🆕 v2.3.1 - Auto-synced by /end
├── global-memory.safe.md          # 🆕 v2.3.1 - Auto-synced by /end
├── global-memory.quick.md         # 🆕 v2.3.1 - Auto-synced by /end
├── .config.json                   # 🆕 v2.3.1 - Auto-synced by /end
├── devices/                       # Device registry
│   ├── laptop-work/
│   ├── desktop-big/
│   └── ...
├── projects/                      # 🆕 v2.3.1 - Auto-synced by /end
├── providers/                     # 🆕 v2.3.1 - Auto-synced by /end
│   ├── claude/daily|weekly|monthly/
│   └── lmstudio/...
├── integration/                   # 🆕 v2.3.1 - Auto-synced by /end
│   ├── provider-activities.md
│   └── provider-activities.quick.md
└── sync/                          # Sync metadata
    ├── device-registry.json
    └── conflicts/
```

**🆕 v2.3.1 - Auto-Sync**: Todos os arquivos marcados com 🆕 são sincronizados automaticamente quando você roda `/end`!

### Economia de Tokens (Exemplo Real)

**v2.0 - /continue (antes de M010.1)**:
- Session state: 245 linhas
- Global memory (safe): 165 linhas
- Weekly summary: 228 linhas
- Daily log: 66 linhas
- **Total: ~704 linhas (~8.000 tokens)**

**v2.1 - /continue com Quick Memories (M010.1)**:

| Cenário | Linhas | Tokens | Economia |
|---------|--------|--------|----------|
| Projeto específico | ~120 | ~1.400 | **84%** ✨ |
| Exploração livre | ~90 | ~1.000 | **88%** ✨ |

**Resultado**: ~6.500 tokens economizados no startup = **6x mais tempo de sessão**! 🚀

---

**Hierarquia temporal (logs completos)**:

**Sem hierarquia** (logs brutos 1 mês):
- ~30 dias × ~150 linhas/dia = ~4.500 linhas

**Com hierarquia**:
- Working memory: 50 linhas
- Global memory (quick): 50 linhas
- Resumo mensal: 30 linhas
- Último resumo semanal: 100 linhas
- **Total: ~230 linhas**

**Economia: ~95%** 🚀

---

## 🔐 Privacidade

Sistema híbrido de proteção de PII com multi-resolution:

**Local**: Dados completos em `~/.claude-memory/global-memory.md`

**Transmissão**:
- `global-memory.safe.md` - Completa, PII redacted
- `global-memory.quick.md` - Resumida, safe por padrão (~88% menor)

**Cloud** (v2.3+):
- Auto-redaction antes de sync
- User-configurable (qualquer git provider)
- Privacy-first .gitignore rules

**Marcação**:
```markdown
Nome: [PII:NAME]Roman[/PII:NAME]
Email: [PII:EMAIL]user@domain.com[/PII:EMAIL]
```

**Redaction** (auto via `/continue` e `/new`):
```markdown
Nome: [REDACTED:NAME]
Email: [REDACTED:EMAIL]
```

**Quick memories** (v2.1):
- Geradas automaticamente sem PII
- Usadas por padrão no `/continue`
- Economia de tokens + privacidade

**Tipos suportados**: NAME, EMAIL, LOCATION, COMPANY, PROJECT, CREDENTIAL, API, DOCUMENT

---

## 🧪 Status do Projeto

**Fases Originais (v2.0)**:
- ✅ **FASE 0-7**: Implementação completa do framework base
- ✅ **FASE 8**: Testes e validação

**Melhorias v2.1** (2025-11-17):
- ✅ **M008**: Project-Centric Memory Layer
  - Memória bidimensional (tempo × projeto)
  - 12 comandos slash (+ `/projects`, `/switch`, `/project-status`)
  - 4 projetos organizados por categoria

- ✅ **M009**: Agent Performance Tracking
  - Estrutura `.claude/performance/`
  - Templates para tracking multi-modelo
  - Auto-detecção de modelo

- ✅ **M010.1**: Multi-Resolution Memory
  - Quick memories (~50 linhas, safe)
  - Lazy loading + aggregation status
  - Gatilhos temporais (sexta/último dia)
  - **84-88% economia** no startup

**Melhorias v2.2** (2025-12-15):
- ✅ **M011**: Multi-Provider Support
  - Estrutura providers/ modular
  - Claude + LMStudio support
  - Cross-provider timeline unificada

**Melhorias v2.3** (2025-12-26):
- ✅ **Optional Cloud Sync**: Multi-device memory infrastructure
  - Framework funciona SEM cloud (local-only padrão)
  - Suporta qualquer git provider (user-configurable)
  - Web session integration (manual export)
  - Device-agnostic (laptop, desktop, mobile, VM, web VM)

**Melhorias v2.3.1** (2025-12-28):
- ✅ **M012**: Automatic Cloud Sync on /end
  - Auto-sync para cloud repo (zero passos manuais!)
  - Non-blocking error handling
  - Multi-device coordination (pull --rebase)
  - User-configurable cloud path

**Melhorias v3.0** (2025-12-28):
- ✅ **M013**: Skills System (Phase 1-3)
  - 3 skills implementadas (scientist, session-continuity, note-organizer)
  - Auto-activation baseada em intent
  - Progressive disclosure architecture
  - Multi-device aware skills

**Versão atual**: **3.0** (funcional, testado, publicado)

**GitHub**: https://github.com/3x-Projetos/claude-memory-system

**Próximos passos**:
- M013.1: skill-creator (Phase 4 - meta-tool para criar skills)
- M013.2: Skills documentation & testing (Phase 5)
- M011.1: Dashboard UI para acompanhar multi-provider em tempo real
- M011.2: Task routing automático (data-driven model selection)
- M010.2: Project-specific history (logs bidimensionais)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o repositório
2. Crie um branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para o branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.

---

## 🙏 Agradecimentos

- **Anthropic** por criar o Claude CLI e o Claude Code
- **Pesquisa acadêmica**:
  - HAI Index (Stanford, 2025): Métricas de augmentation vs automation
  - MemTree (2024): Hierarquia temporal para LLMs
  - PersonaLLM (2025): Perfis adaptativos
  - Well-being research (Nature): Impacto holístico de GenAI

---

## 📞 Suporte

- **Documentação**: Veja `.claude/README.md` e `.claude/QUICKSTART.md`
- **Issues**: [GitHub Issues](https://github.com/3x-Projetos/claude-memory-system/issues)
- **Discussões**: [GitHub Discussions](https://github.com/3x-Projetos/claude-memory-system/discussions)

---

**Desenvolvido com Claude Code** 🤖

*Sistema de memória hierárquica que torna Claude seu verdadeiro parceiro de longo prazo*
