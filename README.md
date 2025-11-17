# Claude Memory System

Sistema de memória hierárquica para Claude CLI com métricas holísticas de impacto humano.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude CLI](https://img.shields.io/badge/Claude-CLI-orange.svg)](https://github.com/anthropics/claude-code)
[![Version](https://img.shields.io/badge/version-2.1-blue.svg)](https://github.com/3x-Projetos/claude-memory-system/releases)

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

---

## ✨ Features

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
git clone https://github.com/YOUR_USERNAME/claude-memory-system.git
cd claude-memory-system

# Usar framework neste diretório
# (já configurado e pronto)
```

**Opção 2: Bootstrap em projeto existente**
```bash
# Clone repo temporário
git clone https://github.com/YOUR_USERNAME/claude-memory-system.git /tmp/cms

# Execute bootstrap no seu projeto
bash /tmp/cms/.claude/setup-claude-memory.sh /path/to/your/project

# Cleanup
rm -rf /tmp/cms
```

### Configuração

1. **Reinicie Claude CLI** (para registrar hooks e comandos)

2. **Primeiro uso**:
```bash
# Inicia sessão carregando framework
/start
```

3. **Ao final**:
```bash
# Finaliza e registra sessão
/end
```

### Workflow Típico

```bash
# Segunda-feira (retomar trabalho)
/continue
# ... trabalho ...
/end

# Meio da semana (nova feature)
/new
# ... trabalho ...
/reflect  # opcional: registrar well-being
/end

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

### Comandos Slash

| Comando | Descrição |
|---------|-----------|
| `/start` | Carrega framework, pergunta se continua ou inicia novo |
| `/continue` | Retoma trabalho com quick memories (84-88% economia) |
| `/new` | Nova atividade (awareness sem pressão) |
| `/memory` | Consulta ferramentas disponíveis |
| `/organize` | Organiza notas com workflow padrão |
| `/end` | Finaliza sessão (log + métricas + state) |
| `/update-profile` | Atualiza perfil global manualmente |
| `/reflect` | Registra métricas de well-being |
| `/aggregate week\|month` | Força agregação temporal |
| `/auto-approve on\|bash\|all\|off` | Toggle auto-aprovação |
| **🆕 `/projects`** | **Dashboard multi-projeto (categorizado)** |
| **🆕 `/switch [name]`** | **Muda contexto para projeto específico** |
| **🆕 `/project-status [name]`** | **Atualiza status/roadmap de projeto** |

---

## 🏗️ Arquitetura

### Estrutura de Diretórios

```
your-project/
├── .claude-memory.md              # Índice central
├── .session-state.md              # Working memory + Aggregation Status
├── .workflow-*.md                 # 7 workflows documentados
├── logs/
│   ├── daily/                     # Logs detalhados
│   ├── weekly/                    # Resumos semanais
│   └── monthly/                   # Resumos mensais
├── .projects/                     # 🆕 v2.1 - Project-Centric Memory
│   ├── README.md
│   └── [project-name]/
│       ├── .context.md            # Contexto completo do projeto
│       ├── .context.quick.md      # 🆕 Contexto resumido (~30 linhas)
│       └── .status.md             # Roadmap, decisões, métricas
└── .claude/
    ├── commands/                  # 12 slash commands (+3 novos)
    │   ├── projects.md            # 🆕 Dashboard multi-projeto
    │   ├── switch.md              # 🆕 Context switching
    │   └── project-status.md      # 🆕 Status update
    ├── performance/               # 🆕 v2.1 - Performance Tracking
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
    ├── AGENT-MODEL-DETECTION.md   # 🆕 Auto-detecção de modelo
    ├── MEMORY-IMPROVEMENTS.md     # 🆕 Tracking de melhorias
    ├── METRICS-FRAMEWORK.md       # Framework de métricas
    └── IMPLEMENTATION-PLAN.md     # Plano completo

# Memória Global (fora do projeto)
~/.claude-memory/
├── global-memory.md               # Perfil completo (com PII)
├── global-memory.safe.md          # Perfil redacted (auto-gerado)
├── global-memory.quick.md         # 🆕 v2.1 - Perfil resumido (~50 linhas)
├── profile-history/               # Snapshots versionados
├── profile-changelog.md           # Histórico de mudanças
└── projects/                      # Referências a projetos
```

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
- `global-memory.quick.md` - 🆕 Resumida, safe por padrão (~88% menor)

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

**Versão atual**: **2.1** (funcional, publicado)

**GitHub**: https://github.com/3x-Projetos/claude-memory-system

**Próximos passos**:
- M010.2: Project-specific history (logs bidimensionais)
- M010.3: Algoritmo inteligente de geração de quick memories
- Testes em ambiente de produção com usuários reais

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

- **Anthropic** por criar o Claude CLI
- **Pesquisa acadêmica**:
  - HAI Index (Stanford, 2025): Métricas de augmentation vs automation
  - MemTree (2024): Hierarquia temporal para LLMs
  - PersonaLLM (2025): Perfis adaptativos
  - Well-being research (Nature): Impacto holístico de GenAI

---

## 📞 Suporte

- **Documentação**: Veja `.claude/README.md` e `.claude/QUICKSTART.md`
- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/claude-memory-system/issues)
- **Discussões**: [GitHub Discussions](https://github.com/YOUR_USERNAME/claude-memory-system/discussions)

---

**Desenvolvido com Claude Code** 🤖

*Sistema de memória hierárquica que torna Claude seu verdadeiro parceiro de longo prazo*
