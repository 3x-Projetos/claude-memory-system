# Claude Memory System

Sistema de memória hierárquica para Claude CLI com métricas holísticas de impacto humano.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude CLI](https://img.shields.io/badge/Claude-CLI-orange.svg)](https://github.com/anthropics/claude-code)

---

## 🎯 O Que É?

Sistema completo de memória persistente e hierárquica para Claude CLI que:

- **Economiza 50-96% de tokens** com agregação temporal inteligente
- **Personaliza colaboração** através de perfil adaptativo do usuário
- **Tracking holístico** de impacto humano (não apenas produtividade)
- **Zero perda de contexto** entre sessões
- **Privacidade first** com redação automática de PII

---

## ✨ Features

### Memória Hierárquica
- **Working Memory**: Contexto da sessão atual (~50 linhas)
- **Logs Diários**: Sessões detalhadas
- **Resumos Semanais**: Agregação ~100 linhas (85% economia)
- **Resumos Mensais**: Alto nível ~30 linhas (93% economia)

### Perfil Global Versionado
- Compartilhado entre projetos
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
| `/continue` | Retoma trabalho (lista pendências) |
| `/new` | Nova atividade (awareness sem pressão) |
| `/memory` | Consulta ferramentas disponíveis |
| `/organize` | Organiza notas com workflow padrão |
| `/end` | Finaliza sessão (log + métricas + state) |
| `/update-profile` | Atualiza perfil global manualmente |
| `/reflect` | Registra métricas de well-being |
| `/aggregate week\|month` | Força agregação temporal |
| `/auto-approve on\|bash\|all\|off` | Toggle auto-aprovação |

---

## 🏗️ Arquitetura

### Estrutura de Diretórios

```
your-project/
├── .claude-memory.md              # Índice central
├── .session-state.md              # Working memory
├── .workflow-*.md                 # 7 workflows documentados
├── logs/
│   ├── daily/                     # Logs detalhados
│   ├── weekly/                    # Resumos semanais
│   └── monthly/                   # Resumos mensais
└── .claude/
    ├── commands/                  # 9 slash commands
    ├── redact-pii.py              # Sistema de privacidade
    ├── auto-approve-edits.py      # Auto-aprovação multi-nível
    ├── session-start.py           # Graceful shutdown (parte 1)
    ├── session-auto-end.py        # Graceful shutdown (parte 2)
    ├── settings.json              # Hooks configurados
    ├── setup-claude-memory.sh     # Bootstrap script
    ├── METRICS-FRAMEWORK.md       # Framework de métricas
    └── IMPLEMENTATION-PLAN.md     # Plano completo

# Memória Global (fora do projeto)
~/.claude-memory/
├── global-memory.md               # Perfil completo (com PII)
├── global-memory.safe.md          # Perfil redacted (auto-gerado)
├── profile-history/               # Snapshots versionados
├── profile-changelog.md           # Histórico de mudanças
└── projects/                      # Referências a projetos
```

### Economia de Tokens (Exemplo Real)

**Sem hierarquia** (logs brutos 1 mês):
- ~30 dias × ~150 linhas/dia = ~4.500 linhas

**Com hierarquia**:
- Working memory: 50 linhas
- Global memory (safe): 150 linhas
- Resumo mensal: 30 linhas
- Último resumo semanal: 100 linhas
- **Total: ~330 linhas**

**Economia: ~93%** 🚀

---

## 🔐 Privacidade

Sistema híbrido de proteção de PII:

**Local**: Dados completos em `~/.claude-memory/global-memory.md`

**Transmissão**: PII redacted em `global-memory.safe.md`

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

**Tipos suportados**: NAME, EMAIL, LOCATION, COMPANY, PROJECT, CREDENTIAL, API, DOCUMENT

---

## 🧪 Status do Projeto

- ✅ **FASE 0**: Preparação Git
- ✅ **FASE 1**: Estrutura de Memória Global
- ✅ **FASE 2**: Sistema de Redação de PII
- ✅ **FASE 3**: Reestruturação de Logs Locais
- ✅ **FASE 4**: Workflows de Agregação
- ✅ **FASE 5**: Comandos Slash Atualizados
- ✅ **FASE 6**: Atualização da Memória Central
- 🚧 **FASE 7**: Versionamento Git do Framework
- ⏳ **FASE 8**: Testes e Validação

**Versão atual**: 2.0 (funcional, em validação)

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
