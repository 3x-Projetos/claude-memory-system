# Cloud Sync on /end - Auto-sync Workflow

**Contexto**: Este workflow é executado automaticamente ao final do comando `/end` se cloud sync estiver habilitado.

**Objetivo**: Sincronizar memória local (~/.claude-memory/) com repositório cloud (path configurável) automaticamente.

---

## Quando Executar

**Ler config first**:
```bash
# Ler ~/.claude-memory/.config.json
SYNC_ENABLED=$(jq -r '.sync_enabled' ~/.claude-memory/.config.json)
ON_SESSION_END=$(jq -r '.sync.on_session_end' ~/.claude-memory/.config.json)
CLOUD_PATH=$(jq -r '.cloud_path' ~/.claude-memory/.config.json)
```

**Condições**:
- `sync_enabled` == true, E
- `sync.on_session_end` == true, E
- `cloud_path` está definido (não null/vazio)

Se TODAS true: executar sync automático
Caso contrário: pular sync (silent)

---

## Processo de Sync

### 0. Setup - Resolver cloud path

```bash
# Ler cloud_path da config
CLOUD_PATH=$(jq -r '.cloud_path' ~/.claude-memory/.config.json)

# Expandir ~ para home directory
CLOUD_PATH="${CLOUD_PATH/#\~/$HOME}"

# Validar que existe
if [ ! -d "$CLOUD_PATH/.git" ]; then
  echo "⚠️ Cloud sync skipped: repo not found at $CLOUD_PATH"
  echo "Configure cloud sync: /setup-cloud"
  exit 0  # Non-blocking
fi
```

**Importante**: `cloud_path` é **user-provided** durante `/setup-cloud`, não hardcoded!

### 1. Copiar arquivos para cloud repo

**Comandos** (multi-plataforma):
```bash
cd ~/.claude-memory

# Copiar diretórios (usar $CLOUD_PATH variável)
cp -r providers integration profile-history projects "$CLOUD_PATH/"

# Copiar arquivos raiz
cp .config.json global-memory.md global-memory.safe.md global-memory.quick.md "$CLOUD_PATH/"
```

**Arquivos a EXCLUIR** (já existem no cloud repo, não sobrescrever):
- `.git/` (obviamente)
- `.gitignore` (configuração do cloud repo)
- `.sync-config.json` (config do cloud repo, se existir)
- `README.md` (documentação do cloud repo, se existir)

**Tratamento de erros**:
```bash
if [ $? -ne 0 ]; then
  echo "⚠️ Cloud sync failed: could not copy files to $CLOUD_PATH"
  exit 0  # Non-blocking
fi
```

### 2. Git Pull (rebase)

**Objetivo**: Integrar mudanças remotas antes de commitar
**Razão**: Pode haver commits de outros devices (multi-device setup)

```bash
cd "$CLOUD_PATH"
git pull --rebase 2>&1
```

**Tratamento de saída**:
- Exit code 0: Pull bem-sucedido, continuar
- "Already up to date": OK, continuar
- **"CONFLICT" na saída**: ABORTAR sync, avisar usuário

```bash
if echo "$OUTPUT" | grep -q "CONFLICT"; then
  echo "⚠️ Cloud sync skipped: merge conflicts detected"
  echo "Resolva manualmente: cd $CLOUD_PATH && git status"
  echo "Logs salvos localmente em ~/.claude-memory/"
  exit 0  # Non-blocking
fi
```

### 3. Git Add

```bash
cd "$CLOUD_PATH"
git add .
```

**O que será adicionado**:
- Logs diários novos/atualizados (providers/*/logs/daily/*.md)
- Provider activities (integration/provider-activities.md + .quick.md)
- Session state (providers/*/session-state.md + .quick.md)
- Global memory (global-memory.md + .safe.md + .quick.md)
- Config (.config.json)
- Project contexts (projects/*/.)

### 4. Git Commit

**Mensagem descritiva** (template):
```bash
# Ler device_name da config
DEVICE_NAME=$(jq -r '.device_name' ~/.claude-memory/.config.json)

git commit -m "[auto] Session YYYY-MM-DD HH:MM - <topic>

Atividades:
- <atividade 1>
- <atividade 2>
- <atividade 3>

Projects: <project names, ou "N/A">
Device: $DEVICE_NAME
Provider: <provider name (claude/gemini/lmstudio/etc)>
Duration: ~<duration inferido>
Quality: <⭐⭐⭐⭐⭐ rating se disponível>

🤖 Auto-sync via /end command
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**Variáveis para substituir**:
- `<topic>`: Do input do usuário no /end (ex: "Skills System Implementation")
- `<atividade N>`: Resumo das atividades (max 3-5, concisas)
- `<project names>`: Projetos tocados (ex: "Claude Memory System, Golfleet")
- `$DEVICE_NAME`: De `.config.json` → `device_name` (dynamic)
- `<provider name>`: "claude" para Claude CLI, "gemini" para Gemini, etc
- `<duration>`: Calculado (ex: "~3.5 hours")
- `<quality>`: Se coletado (ex: "⭐⭐⭐⭐⭐ (5/5)")

**Se nada para commitar** (`nothing to commit, working tree clean`):
- Silent skip (não avisar usuário)
- Sync considerado "bem-sucedido" (já estava sincronizado)
- Exit code 0

```bash
git commit -m "..." 2>&1
if echo "$OUTPUT" | grep -q "nothing to commit"; then
  # Já sincronizado, silent success
  exit 0
fi
```

### 5. Git Push

```bash
cd "$CLOUD_PATH"
git push 2>&1
```

**Tratamento de saída**:
- Exit code 0: Push bem-sucedido! ✅
- Exit code != 0: Ver "Tratamento de Erros"

**Capturar commit hash**:
```bash
COMMIT_HASH=$(git -C "$CLOUD_PATH" rev-parse --short HEAD)
echo "✅ Cloud sync completo (commit $COMMIT_HASH)"
```

---

## Tratamento de Erros

### Erro 1: Pull com conflitos
**Sintoma**: `git pull --rebase` retorna "CONFLICT" na saída

**Ação**:
```
⚠️ Cloud sync skipped: merge conflicts detected

Outro device modificou os mesmos arquivos. Resolva manualmente:
  cd $CLOUD_PATH
  git status
  # Resolver conflitos, depois:
  git add .
  git rebase --continue
  git push

Logs salvos localmente em ~/.claude-memory/
```

**NÃO bloquear** finalização do /end

### Erro 2: Push falhou (network/auth)
**Sintomas**:
- "fatal: Could not read from remote repository"
- "error: failed to push some refs"
- Network timeout

**Ação**:
```
⚠️ Cloud sync failed: <error message>

Logs salvos localmente. Tente sincronizar manualmente:
  cd $CLOUD_PATH
  git push

Ou rode /end novamente depois (auto-sync tentará novamente)
```

**NÃO bloquear** finalização do /end

### Erro 3: Repo cloud não existe
**Sintoma**: `$CLOUD_PATH/.git/` não existe

**Ação**:
```
⚠️ Cloud sync skipped: cloud repo not found at $CLOUD_PATH

Configure cloud sync primeiro:
  /setup-cloud   # Interactive setup
```

**NÃO bloquear** finalização do /end

### Erro 4: Copy falhou
**Sintoma**: `cp` retorna erro (permissões, disco cheio, etc)

**Ação**:
```
⚠️ Cloud sync failed: could not copy files to $CLOUD_PATH

Error: <error message>
Logs salvos localmente em ~/.claude-memory/
```

**NÃO bloquear** finalização do /end

### Erro 5: Config inválida
**Sintoma**: `cloud_path` está vazio, null, ou inválido em .config.json

**Ação**:
```
⚠️ Cloud sync skipped: invalid cloud_path in config

Configure cloud sync primeiro:
  /setup-cloud   # Interactive setup
```

**NÃO bloquear** finalização do /end

---

## Princípios de Design

### 1. Non-blocking
**CRÍTICO**: Sync NUNCA deve bloquear finalização do /end
- Logs sempre salvos localmente PRIMEIRO
- Cloud sync é "best effort" (tentativa)
- Se falhar: usuário pode sync manual depois

### 2. Silent quando possível
- Se sync bem-sucedido: apenas ✅ na confirmação
- Se já sincronizado (nothing to commit): silent skip
- Se falhou: avisar com ⚠️ mas não alarmar

### 3. Multi-device aware
- Pull --rebase antes de commitar (evitar conflicts)
- Conflict detection e graceful abort
- Commit messages com device info para tracking

### 4. User-configurable
**IMPORTANTE**: Não hardcode paths!
- `cloud_path` vem de `.config.json` (user-provided)
- `device_name` vem de `.config.json` (user-provided)
- `cloud_repo` URL vem de `.config.json` (user-provided)
- Suporta qualquer git provider (GitHub, GitLab, Gitea, etc)

### 5. Informativo
- Commit messages descritivas (permitem reconstruir sessão)
- Include metadata (device, provider, duration, quality)
- Hash do commit na confirmação (usuário pode verificar)

### 6. Fail-safe
- Nunca perder dados (logs locais são source of truth)
- Tratamento de TODOS os erros possíveis
- Fallback para sync manual sempre disponível

---

## Config Structure (reference)

```json
{
  "version": "2.3",
  "sync_enabled": true,                     // Master switch
  "cloud_repo": "<user-provided-git-url>",  // Git remote URL
  "cloud_path": "<user-provided-path>",     // Local path to cloud repo (NOT hardcoded!)
  "device_name": "<user-provided-name>",    // Device identifier
  "providers": ["claude"],
  "sync": {
    "on_session_start": true,               // Pull on /continue
    "on_session_end": true,                 // Push on /end (THIS WORKFLOW!)
    "auto_commit": true,                    // Auto-commit enabled
    "conflict_resolution": "latest-timestamp"
  },
  "privacy": {
    "redact_pii": true,
    "auto_redact": ["email", "phone", "address"],
    "cloud_safe_only": false
  }
}
```

---

## Testing Checklist

Para validar implementação:

- [ ] Sync bem-sucedido (happy path)
- [ ] Já sincronizado (nothing to commit)
- [ ] Pull com conflitos (outro device modificou)
- [ ] Push falhou (network offline)
- [ ] Cloud repo não existe
- [ ] Cloud path inválido/vazio na config
- [ ] Sync disabled na config (silent skip)
- [ ] Copy falhou (permissões)
- [ ] Commit message correta (todas variáveis substituídas)
- [ ] Não bloqueia /end em NENHUM cenário de erro
- [ ] **Path dinâmico** (não hardcoded, lê de config)
- [ ] **Device name dinâmico** (lê de config)

---

## Integração com /end

**Posição no workflow**: Após passo 8 (Cleanup), antes de Confirmação

```markdown
### 8. Cleanup
[...]

### 9. Cloud Sync (se habilitado)
**Referência**: Ver `.claude/workflows/cloud-sync-on-end.md`

1. Ler config (~/.claude-memory/.config.json):
   - sync_enabled && sync.on_session_end ?
   - cloud_path definido e válido?

2. Se habilitado: executar sync automático
   - Copiar arquivos para $CLOUD_PATH
   - Git pull --rebase (multi-device)
   - Git add .
   - Git commit (mensagem descritiva)
   - Git push

3. Tratamento de erros (non-blocking):
   - Conflicts → skip com aviso
   - Network error → skip com aviso
   - Path inválido → skip com aviso
   - **NUNCA** bloquear finalização

4. Capturar resultado para confirmação:
   - Success: ✅ Cloud sync completo (commit hash)
   - Skip: silent (não mencionar)
   - Fail: ⚠️ com instrução de fallback

### 10. Confirmação
[...]
- (Se cloud sync tentado) ✅/⚠️ resultado do sync
[...]
```

---

## Exemplo de Output

**Sync bem-sucedido**:
```
✓ Log criado em ~/.claude-memory/providers/claude/logs/daily/2025.12.28.md
✓ session-state.md atualizado
✓ provider-activities.md atualizado
✅ Cloud sync completo (commit a1b2c3d)
Sessão finalizada com sucesso. Até a próxima!
```

**Sync falhou (network)**:
```
✓ Log criado em ~/.claude-memory/providers/claude/logs/daily/2025.12.28.md
✓ session-state.md atualizado
✓ provider-activities.md atualizado
⚠️ Cloud sync failed: Network error
   Tente manualmente: cd ~/.cloud-repo-custom && git push
Sessão finalizada com sucesso. Até a próxima!
```

**Sync disabled**:
```
✓ Log criado em ~/.claude-memory/providers/claude/logs/daily/2025.12.28.md
✓ session-state.md atualizado
✓ provider-activities.md atualizado
Sessão finalizada com sucesso. Até a próxima!
```

**Cloud path customizado** (exemplo):
```
# User configured cloud_path: ~/Dropbox/claude-memory-backup
✅ Cloud sync completo (commit a1b2c3d)
   Synced to: ~/Dropbox/claude-memory-backup
```
