---
description: Finaliza sessão e cria/atualiza log de atividades
---

Finalizando sessão com sistema de memória hierárquica.

## Passos

### 1. Detectar modelo automaticamente (NOVO)

**Auto-detecção por agente**:

**Claude**:
- Modelo sempre conhecido (aparece no início da conversa)
- Exemplos: "Sonnet 4.5", "Opus", "Haiku"
- Modelo ID exato disponível (ex: `claude-sonnet-4-5-20250929`)
- **Nunca perguntar** - sempre auto-detectar

**Gemini**:
- Se usando API: ler de variável de ambiente ou config
- Se via interface: tentar detectar do contexto
- **Fallback**: perguntar ao usuário

**Local LLMs** (LM Studio):
- Ler de config do LM Studio
- Detectar do model path
- **Fallback**: perguntar ao usuário

**GPT-4** (via API):
- Ler de config ou variável de ambiente
- **Fallback**: perguntar ao usuário

**Formato de registro**:
```
**Agente**: Claude
**Modelo**: Sonnet 4.5 (claude-sonnet-4-5-20250929)
```

### 2. Perguntar ao usuário (apenas se necessário)
- Qual foi o tópico/foco principal da sessão?
- Quais foram as principais atividades realizadas?
- Há próximos passos ou tarefas pendentes?
- (Opcional) Se `.metrics-reflection.tmp` existir, perguntar se deseja incluir
- **(Se modelo não detectado)**: Qual modelo você usou? [lista de opções]

### 3. Identificar projetos tocados (M008)

Ler `~/.claude-memory/providers/claude/session-state.md` → "Current Focus":
- Se houver projeto listado: "Você trabalhou em **[Project Name]**. Trabalhou em outros projetos também? [sim/não]"
- Se sim: listar projetos disponíveis e marcar quais foram tocados
- Se não havia projeto: "Trabalhou em algum projeto específico? [listar projetos]"

**Para cada projeto tocado**:
- Perguntar % de tempo aproximado (ex: 70% Memory System, 30% Hybrid Agent)
- Atualizar `.projects/[name]/.context.md`:
  - "**Last Touched**:" → timestamp atual
  - "## Recent Changes" → adicionar linha sobre esta sessão

**Registrar no log da sessão**:
```markdown
### Projects Touched

**[Project 1]** (X% do tempo):
- Atividades principais
- Status: [mudou de Y para Z] ou [mantém Z]

**[Project 2]** (Y% do tempo):
- Atividades principais
- Status: [mantém Z]

### Current Focus at End
[Projeto] (next session focus)
```

### 4. Inferir métricas da sessão
Análise automática (baseado em `.workflow-metrics-collection.md`):

**Métricas Tradicionais**:
- Duration: Inferir da sessão
- Files modified: Contar arquivos tocados
- Commits: Se houver git activity
- Complexity: Baixa/Média/Alta (baseado em linguagem dos logs)
- New tech: Tecnologias novas mencionadas
- AI reliance: Baixa/Média/Alta (baseado em autonomia)

**Token Metrics** (model-specific):

**Para Claude** (auto-detectado):
- Modelo: [Sonnet 4.5 | Opus | Haiku] (model ID completo)
- Budget: 200.000 tokens
- Tokens usados: [ver system warnings acumulados]
- Uso %: [calcular]
- Custo relativo: [$$$|$$|$]

**Para Gemini**:
- Modelo: [Gemini 1.5 Pro | Flash | 2.0 Flash]
- Budget: [2M | 1M | etc] tokens
- Tokens usados: [de API ou estimativa]
- Uso %: [calcular]
- Custo relativo: [$|$$]

**Para Local LLMs**:
- Modelo: [DeepSeek-Coder 33B | Qwen2.5 | etc]
- Context limit: [16k | 32k | 128k] tokens
- Tokens usados: [estimativa]
- Performance: [tok/s]
- Custo: $0 (local)

**Economia com framework** (universal):
- Sem framework: [estimar baseado em logs brutos]
- Com framework: [tokens reais usados]
- Economia: [% economizado]

### 4. Coletar Performance Metrics (M009 - NOVO)

**Auto-detectar**:
1. **Modelo usado**: [já implementado no Passo 1]
2. **Tokens**:
   - Budget: [conhecido por modelo - Claude: 200k, Gemini: 1-2M, etc]
   - Usados: [system warnings acumulados para Claude, API count para outros]
   - % utilizado: [calcular]
3. **Duration**: [inferir de session timestamps]
4. **Files**: [git diff --stat ou contar arquivos modificados]
5. **Technologies**: [inferir de file extensions + imports detectados]
6. **Task type**: [inferir de arquivos modificados + comandos executados]
7. **Project**: [já rastreado em M008 - Passo 3]

**Perguntar ao usuário** (opcional, pulável com Enter):
```
📊 Avaliação de Performance (opcional - Enter para pular todas):

1. Qualidade desta sessão: ⭐ [1-5, Enter=auto-inferir]
2. Tarefa completada? [yes/partial/no, Enter=yes]
3. Categoria: [architecture/code/refactor/debug/docs/research, Enter=auto]
```

**Registrar performance**:
- Se `.claude/performance/profiles/[model-name].md` não existir: criar com template
- Adicionar entrada de sessão ao profile
- Update stats agregados (contadores, médias)
- **Mensal** (via `/aggregate month`): Re-calcular comparative performance e context optimization insights

### 5. Criar/atualizar log diário
**Localização**: `~/.claude-memory/providers/claude/logs/daily/YYYY.MM.DD.md`

- Se não existir: criar novo com estrutura de `.workflow-session-logging.md`
- Se existir: adicionar nova seção de sessão

**Template do log** (incluir Agente + Modelo + Performance):
```markdown
## Sessão XX:XX (horário)
**Agente**: [Claude | Gemini | Local | Outro]
**Modelo**: [Sonnet 4.5 | Gemini 1.5 Pro | DeepSeek-Coder | etc]
**Tópico**: [Descrição]

### Projects Touched
[Se aplicável - M008]

### Atividades Realizadas
[...]

### Performance Metrics

**Context Metrics**:
- Budget: X tokens
- Used: ~Y tokens (Z%)
- Prompt avg: ~A tokens/interaction
- Output avg: ~B tokens/response
- Framework economy: W% (vs ~K tokens sem framework)

**Task Metrics**:
- Type: [Architecture/Code/Refactor/Debug/Docs/Research] (auto-detected)
- Quality: ⭐⭐⭐⭐⭐ (N/5, [user-rated|auto-inferred])
- Success: [yes|partial|no]
- Duration: ~H hours M min
- Files: X created, Y modified
- Technologies: [Lista] (auto-detected)

**Efficiency**:
- Output/Input ratio: N.NN
- Context utilization: [Optimal|Good|Low|High] (X-Y% range)
- Cost tier: [$-$$$$] ([justified|overkill|underpowered] for complexity)

**Método de medição**:
- Claude: System warnings acumulados
- Gemini: [API token count / estimativa]
- Local: [Estimativa baseada em prompt length]
```

Incluir seção `## Performance Metrics` com métricas auto-detectadas e relatadas (se houver)

### 6. Registrar em provider-activities.md (NOVO - v2.2)

**APPEND** (não editar) em `~/.claude-memory/integration/provider-activities.md`:

```markdown
### HH:MM | claude | session-<timestamp>
**Project**: [project-name] (se aplicável)
**Activities**:
- Atividade 1 (resumida)
- Atividade 2 (resumida)
- Atividade 3 (resumida)

**Output**: providers/claude/logs/daily/YYYY.MM.DD.md
**Context Usage**: X / 200K (Y%)
```

Também atualizar versão `.quick.md` (manter apenas últimas 24h).

**Propósito**: Outros providers (LMStudio) podem ver o que Claude fez.

### 7. Atualizar session-state.md
Atualizar `~/.claude-memory/providers/claude/session-state.md` com:
- Última sessão: Data atual
- Resumo: 1 linha do que foi feito
- Pendências ativas: Lista de TODOs não completados
- Arquivos principais: Top 5-10 arquivos tocados
- Próximos passos: Do que usuário informou

### 7. Detectar necessidade de agregações
- **Weekly**: Se última semana completa não tem resumo em `~/.claude-memory/providers/claude/logs/weekly/`
  - Informar usuário: "Semana X de YYYY sem resumo. Execute `/aggregate week` para agregar."
- **Monthly**: Se último mês completo não tem resumo em `~/.claude-memory/providers/claude/logs/monthly/`
  - Informar usuário: "Mês YYYY.MM sem resumo. Execute `/aggregate month` para agregar."

### 8. Cleanup
**CRÍTICO**: Deletar arquivos de estado da sessão para marcar como registrada:
```bash
rm -f .claude/.current-session-id .claude/.previous-session-id
```

Se `.metrics-reflection.tmp` foi incorporado, deletar também:
```bash
rm -f .metrics-reflection.tmp
```

### 9. Cloud Sync (se habilitado)

**Referência completa**: Ver `.claude/workflows/cloud-sync-on-end.md`

**Resumo do processo**:

1. **Verificar se habilitado**:
   - Ler `~/.claude-memory/.config.json`
   - Verificar: `sync_enabled == true` && `sync.on_session_end == true`
   - Ler `cloud_path` (user-configured, não hardcoded!)
   - Validar que `$CLOUD_PATH/.git/` existe

2. **Se habilitado, executar sync**:
   ```bash
   # Copiar arquivos locais para cloud repo
   cp -r providers integration profile-history projects "$CLOUD_PATH/"
   cp .config.json global-memory*.md "$CLOUD_PATH/"
   
   # Git operations
   cd "$CLOUD_PATH"
   git pull --rebase           # Multi-device: integrar mudanças remotas
   git add .
   git commit -m "[auto] Session [timestamp] - [topic] ..."
   git push
   ```

3. **Tratamento de erros** (non-blocking):
   - **Conflicts** → Skip com aviso, não bloquear
   - **Network error** → Skip com aviso, não bloquear
   - **Path inválido** → Skip com aviso, não bloquear
   - **Already synced** → Silent skip (nothing to commit)

4. **Capturar resultado**:
   - ✅ Success: "Cloud sync completo (commit [hash])"
   - ⚠️ Failed: "Cloud sync failed: [error]" + instrução manual
   - Silent: Sync não habilitado ou já sincronizado

**IMPORTANTE**: Logs sempre salvos localmente PRIMEIRO. Cloud sync é "best effort".


### 10. Confirmação
Informar ao usuário:
- ✓ Log criado/atualizado em `~/.claude-memory/providers/claude/logs/daily/YYYY.MM.DD.md`
- ✓ session-state.md atualizado
- ✓ provider-activities.md atualizado
- (Se cloud sync habilitado) ✅ Cloud sync completo (commit [hash]) OU ⚠️ Cloud sync falhou: [motivo]
- (Se aplicável) ⚠️ Agregações pendentes detectadas
- "Sessão finalizada com sucesso. Até a próxima!"
