# Plano de Implementação - Sistema de Memória Hierárquica

**Versão**: 1.0
**Data**: 2025-11-15
**Status**: Planejamento completo, aguardando execução

---

## 📋 Visão Geral

Implementar sistema completo de memória hierárquica com:
- Memória global multi-projeto (~/.claude-memory/)
- Logs hierárquicos (daily/weekly/monthly)
- Perfil de usuário versionado
- Métricas holísticas de impacto
- Redação automática de PII
- Versionamento Git do framework

---

## 🎯 Objetivos

1. **Reduzir tokens**: 50-90% de economia no carregamento de sessão
2. **Personalização**: AI adapta-se ao usuário ao longo do tempo
3. **Continuidade**: Retomar trabalho sem perder contexto
4. **Insights**: Métricas de impacto humano real
5. **Portabilidade**: Sistema replicável via Git
6. **Privacidade**: PII protegido em transmissões

---

## 📦 Fases de Implementação

---

### **FASE 0: Preparação Git** 🔧

**Objetivo**: Versionar framework antes de implementar

**Ações**:
1. Criar repositório Git local no Obsidian Vault
2. Criar `.gitignore` apropriado:
   ```
   # Logs pessoais (não versionar)
   logs/
   *.log
   .session-state.md

   # Memória global (não versionar - contém PII)
   ~/.claude-memory/

   # Arquivos temporários
   .test-*
   auto-approve-state

   # Versionar apenas framework
   .claude/
   .workflow-*.md
   .claude-memory.md
   ```
3. Commit inicial: "feat: sistema de memória v1.0 - planejamento"
4. (Opcional) Criar repo GitHub para compartilhar framework
5. Adicionar README.md do projeto

**Entregáveis**:
- `.git/` inicializado
- `.gitignore` configurado
- Commit inicial registrado
- (Opcional) Remote GitHub configurado

**Tempo estimado**: 15 minutos

---

### **FASE 1: Estrutura de Memória Global** 🌍

**Objetivo**: Criar memória global persistente entre projetos

**Ações**:

1. **Criar diretório global**:
   ```
   ~/.claude-memory/
   ├── global-memory.md
   ├── global-memory.safe.md (gerado automaticamente)
   ├── profile-history/
   │   └── 2025-11-15_initial.md
   ├── profile-changelog.md
   └── projects/
       └── obsidian-vault.link
   ```

2. **Preencher global-memory.md**:
   - User Profile (inferido das interações até agora)
   - Collaboration Patterns
   - Communication Style
   - Technical Preferences
   - Opportunities (seção vazia inicialmente)
   - Recurring Architecture Decisions

3. **Criar profile-history/2025-11-15_initial.md** (snapshot)

4. **Criar profile-changelog.md** (vazio, pronto para registros)

5. **Marcar PII** com tags `[PII:TYPE]...[/PII:TYPE]`

**Entregáveis**:
- `~/.claude-memory/global-memory.md` (completo, com PII marcado)
- `~/.claude-memory/profile-history/2025-11-15_initial.md`
- `~/.claude-memory/profile-changelog.md`
- `~/.claude-memory/projects/` (diretório)

**Tempo estimado**: 30 minutos

---

### **FASE 2: Sistema de Redação de PII** 🔒

**Objetivo**: Proteger informações pessoais em transmissões

**Ações**:

1. **Criar `.claude/redact-pii.py`**:
   ```python
   #!/usr/bin/env python3
   """
   Redact PII from global memory before transmission.
   Reads global-memory.md, replaces [PII:TYPE]value[/PII:TYPE] with [REDACTED:TYPE]
   """
   import re
   import sys
   from pathlib import Path

   def redact_pii(content):
       pattern = r'\[PII:(\w+)\](.*?)\[/PII:\1\]'
       return re.sub(pattern, r'[REDACTED:\1]', content)

   # Implementation...
   ```

2. **Testar redação**:
   - Input: `[PII:NAME]Luis[/PII:NAME]`
   - Output: `[REDACTED:NAME]`

3. **Gerar global-memory.safe.md** inicial

**Tipos PII suportados**:
- NAME, EMAIL, LOCATION, COMPANY, PROJECT
- CREDENTIAL, API, DOCUMENT

**Entregáveis**:
- `.claude/redact-pii.py` (funcional)
- `~/.claude-memory/global-memory.safe.md` (gerado)
- Testes validados

**Tempo estimado**: 20 minutos

---

### **FASE 3: Reestruturação de Logs Locais** 📂

**Objetivo**: Hierarquizar logs do projeto (daily/weekly/monthly)

**Ações**:

1. **Criar estrutura de diretórios**:
   ```
   logs/
   ├── daily/
   │   ├── 2025.11.15.md (migrar arquivo atual)
   │   └── ...
   ├── weekly/
   │   └── (vazio, será preenchido automaticamente)
   └── monthly/
       └── (vazio, será preenchido automaticamente)
   ```

2. **Migrar log atual**:
   - Mover `2025.11.15.md` → `logs/daily/2025.11.15.md`

3. **Criar `.session-state.md`** (working memory):
   ```markdown
   # Session State (Working Memory)

   **Última sessão**: 2025-11-15
   **Resumo**: Sistema de memória hierárquica planejado

   ## Pendências Ativas
   - [ ] Implementar sistema de memória hierárquica

   ## Arquivos Principais
   - .claude/METRICS-FRAMEWORK.md
   - .claude/IMPLEMENTATION-PLAN.md

   ## Próximos Passos
   1. Executar FASE 0-7 deste plano
   2. Testar sistema completo
   3. Iterar conforme necessário
   ```

**Entregáveis**:
- `logs/daily/`, `logs/weekly/`, `logs/monthly/` (estrutura)
- `logs/daily/2025.11.15.md` (migrado)
- `.session-state.md` (criado)

**Tempo estimado**: 10 minutos

---

### **FASE 4: Workflows de Agregação** 📝

**Objetivo**: Documentar processos de agregação temporal

**Ações**:

1. **Criar `.workflow-weekly-aggregation.md`**:
   - Input: Todos os logs diários da semana
   - Output: Resumo semanal (~100 linhas)
   - Seções: Projetos, Arquivos, Aprendizados, Métricas

2. **Criar `.workflow-monthly-aggregation.md`**:
   - Input: Todos os resumos semanais do mês
   - Output: Resumo mensal (~30 linhas)
   - Seções: Realizações, Padrões, Tecnologias, Métricas

3. **Criar `.workflow-profile-update.md`**:
   - Detecta mudanças significativas
   - Threshold: 3+ menções em 1 semana
   - Processo de versionamento do perfil

4. **Criar `.workflow-metrics-collection.md`**:
   - Baseado em METRICS-FRAMEWORK.md
   - Inferência de métricas de logs
   - Atualização de dashboard

**Entregáveis**:
- `.workflow-weekly-aggregation.md`
- `.workflow-monthly-aggregation.md`
- `.workflow-profile-update.md`
- `.workflow-metrics-collection.md`

**Tempo estimado**: 40 minutos

---

### **FASE 5: Comandos Slash (Atualizados)** ⚙️

**Objetivo**: Adaptar comandos para novo sistema

**Ações**:

1. **Atualizar `/end`**:
   ```markdown
   Ao finalizar sessão:
   1. Perguntar sobre atividades realizadas
   2. Criar/atualizar logs/daily/YYYY.MM.DD.md
   3. Atualizar .session-state.md (working memory)
   4. Inferir métricas da sessão
   5. Detectar se precisa agregação semanal/mensal
   ```

2. **Atualizar `/continue`**:
   ```markdown
   Ao iniciar sessão:
   1. Executar redact-pii.py (gera .safe.md)
   2. Ler ~/.claude-memory/global-memory.safe.md
   3. Ler .session-state.md
   4. Detectar agregações pendentes:
      - Se passou 1 semana sem weekly: criar
      - Se passou 1 mês sem monthly: criar
   5. Informar: "Retomando [data], [resumo 1 linha]"
   6. Listar pendências ativas
   ```

3. **Atualizar `/new`**:
   ```markdown
   Ao iniciar nova atividade:
   1. Executar redact-pii.py
   2. Ler ~/.claude-memory/global-memory.safe.md
   3. Ler .session-state.md (awareness, mas sem listar pendências)
   4. Informar: "Pronto para nova atividade"
   ```

4. **Criar `/update-profile`** (manual):
   ```markdown
   Força atualização de perfil:
   1. Analisar últimos 30 dias de logs
   2. Identificar mudanças vs perfil atual
   3. Propor atualizações
   4. Se aprovado: criar snapshot em profile-history/
   5. Registrar em profile-changelog.md
   ```

5. **Criar `/reflect`** (coleta de métricas):
   ```markdown
   Registro manual de estado:
   1. Prompt: "Como se sente? (1-10)"
   2. Prompt: "Nível de energia? (Energizado/Neutro/Drenado)"
   3. Opcional: Notas livres
   4. Salvar em metrics-log temporário
   5. Incorporar em próximo /end
   ```

6. **Criar `/aggregate`** (forçar agregação):
   ```markdown
   Argumento: week | month
   - week: Agrega logs diários → weekly
   - month: Agrega logs semanais → monthly
   ```

**Entregáveis**:
- `.claude/commands/end.md` (atualizado)
- `.claude/commands/continue.md` (atualizado)
- `.claude/commands/new.md` (atualizado)
- `.claude/commands/update-profile.md` (novo)
- `.claude/commands/reflect.md` (novo)
- `.claude/commands/aggregate.md` (novo)

**Tempo estimado**: 60 minutos

---

### **FASE 6: Atualização da Memória Central** 📚

**Objetivo**: Documentar novo sistema no índice

**Ações**:

1. **Atualizar `.claude-memory.md`**:
   - Adicionar seção "Sistema de Memória Hierárquica"
   - Documentar estrutura de logs (daily/weekly/monthly)
   - Documentar memória global (~/.claude-memory/)
   - Documentar comandos novos/atualizados
   - Adicionar seção "Métricas e Impacto Humano"
   - Referência a METRICS-FRAMEWORK.md

2. **Adicionar quick reference**:
   ```markdown
   ## Quick Reference

   ### Memória de Projeto
   - Working: .session-state.md (~50 linhas)
   - Daily: logs/daily/YYYY.MM.DD.md (detalhado)
   - Weekly: logs/weekly/YYYY.MM.weekN.md (resumo)
   - Monthly: logs/monthly/YYYY.MM.md (alto nível)

   ### Memória Global
   - Perfil: ~/.claude-memory/global-memory.md
   - Métricas: Baseado em METRICS-FRAMEWORK.md
   - Privacidade: PII redacted automaticamente
   ```

**Entregáveis**:
- `.claude-memory.md` (atualizado)
- Documentação completa e clara

**Tempo estimado**: 30 minutos

---

### **FASE 7: Versionamento Git do Framework** 🔀

**Objetivo**: Versionar framework e preparar para compartilhamento

**Ações**:

1. **Criar README.md do repositório**:
   ```markdown
   # Claude Memory System

   Sistema de memória hierárquica para Claude CLI com métricas holísticas de impacto humano.

   ## Features
   - Memória global multi-projeto
   - Logs hierárquicos (daily/weekly/monthly)
   - Perfil de usuário versionado
   - Métricas de impacto em 7 dimensões
   - Redação automática de PII
   - Portável via bootstrap script

   ## Quick Start
   [Instruções de instalação]
   ```

2. **Atualizar `.claude/setup-claude-memory.sh`** (bootstrap):
   - Incluir criação de ~/.claude-memory/
   - Incluir redact-pii.py
   - Incluir estrutura logs/
   - Incluir novos comandos

3. **Organizar commits Git**:
   ```bash
   git add .claude/ .workflow-*.md .claude-memory.md
   git commit -m "feat: sistema de memória hierárquica v1.0"

   git add .claude/METRICS-FRAMEWORK.md
   git commit -m "docs: framework de métricas holísticas"

   git add .claude/IMPLEMENTATION-PLAN.md
   git commit -m "docs: plano de implementação completo"
   ```

4. **(Opcional) Publicar no GitHub**:
   - Criar repositório público
   - Push do framework (SEM logs pessoais)
   - Adicionar LICENSE (MIT?)
   - Adicionar CONTRIBUTING.md

**Entregáveis**:
- README.md (repositório)
- `.claude/setup-claude-memory.sh` (atualizado)
- Commits organizados
- (Opcional) Repositório GitHub público

**Tempo estimado**: 45 minutos

---

### **FASE 8: Testes e Validação** ✅

**Objetivo**: Garantir que tudo funciona

**Checklist**:

1. **Teste de PII Redaction**:
   - [ ] global-memory.md contém [PII:NAME]Luis[/PII:NAME]
   - [ ] redact-pii.py gera .safe.md com [REDACTED:NAME]
   - [ ] Nenhum PII vaza em .safe.md

2. **Teste de Comandos**:
   - [ ] /continue carrega .session-state.md + global-memory.safe.md
   - [ ] /end cria logs/daily/YYYY.MM.DD.md + atualiza .session-state.md
   - [ ] /update-profile cria snapshot em profile-history/
   - [ ] /aggregate week cria logs/weekly/
   - [ ] /reflect registra métricas

3. **Teste de Agregação**:
   - [ ] Criar 7 logs diários simulados
   - [ ] Executar /aggregate week
   - [ ] Validar resumo semanal (~100 linhas, sem perda de info crítica)

4. **Teste de Continuidade**:
   - [ ] Encerrar sessão com /end
   - [ ] Reiniciar Claude CLI
   - [ ] Executar /continue
   - [ ] Validar que contexto foi preservado

5. **Teste de Métricas**:
   - [ ] Logs contêm dados para inferência
   - [ ] Métricas são calculadas corretamente
   - [ ] Dashboard reflete estado real

**Entregáveis**:
- Sistema validado e funcional
- Bugs documentados e corrigidos

**Tempo estimado**: 60 minutos

---

## 📊 Resumo Executivo

### Timeline Total
- FASE 0: 15 min (Git)
- FASE 1: 30 min (Memória global)
- FASE 2: 20 min (PII redaction)
- FASE 3: 10 min (Logs locais)
- FASE 4: 40 min (Workflows)
- FASE 5: 60 min (Comandos)
- FASE 6: 30 min (Documentação)
- FASE 7: 45 min (Git framework)
- FASE 8: 60 min (Testes)

**Total: ~5 horas de implementação**

### Ordem de Execução Recomendada
1. FASE 0 (Git setup - fundação)
2. FASE 1 (Memória global - core)
3. FASE 2 (PII - segurança)
4. FASE 3 (Logs - estrutura)
5. FASE 4 (Workflows - processos)
6. FASE 5 (Comandos - interface)
7. FASE 6 (Docs - conhecimento)
8. FASE 7 (Git - compartilhamento)
9. FASE 8 (Testes - validação)

### Dependências Críticas
- FASE 2 depende de FASE 1 (precisa ter global-memory.md para redactar)
- FASE 5 depende de FASE 2-4 (comandos usam estrutura + workflows)
- FASE 6 depende de tudo (documenta sistema completo)
- FASE 8 depende de tudo (testa sistema completo)

---

## 🎯 Próximos Passos Imediatos

**Hoje (2025-11-15)**:
1. Encerrar sessão com /end
2. Descansar 😴

**Próxima sessão**:
1. /continue para retomar
2. Executar FASE 0 (Git setup)
3. Decidir: implementar tudo de uma vez ou iterar por fases?

---

## 📝 Notas Importantes

- **Backup**: Antes de começar, backup de logs atuais
- **Iterativo**: OK pausar entre fases e testar incrementalmente
- **Flexível**: Plano pode adaptar conforme descobrimos issues
- **Privacidade**: NUNCA versionar logs pessoais ou global-memory.md no Git
- **Comunidade**: Framework pode ajudar outros usuários Claude CLI

---

*Última atualização: 2025-11-15 - Plano completo, aguardando execução*
