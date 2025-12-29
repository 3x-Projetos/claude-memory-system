---
description: Força atualização do perfil global do usuário
---

Executar workflow de atualização de perfil.

## Uso
```
/update-profile [scope]
```

**Scopes**:
- (nenhum) → Full review (padrão)
- `tech` → Apenas tecnologias/ferramentas
- `preferences` → Apenas preferências e working style
- `projects` → Apenas contexto de projetos

## Processo

Siga exatamente o workflow documentado em `.workflow-profile-update.md`:

### 1. Análise de Mudanças
- Ler últimos 30 dias de `logs/daily/` (ou último resumo mensal)
- Identificar:
  - Novas tecnologias/ferramentas (3+ menções)
  - Mudanças de preferências (3+ menções)
  - Novos padrões arquiteturais (3+ usos)
  - Evolução de projetos
  - Aprendizados e crescimento
  - Mudanças de contexto

### 2. Comparação com Perfil Atual
- Ler `~/.claude-memory/global-memory.md`
- Para cada mudança identificada:
  - Verificar se já existe
  - Determinar confidence (Alta/Média/Baixa)
  - **Regra**: Só propor se confidence >= Média

### 3. Proposta de Atualização
Apresentar ao usuário:

```markdown
## Proposta de Atualização do Perfil

**Data**: YYYY-MM-DD
**Trigger**: Manual (/update-profile [scope])
**Mudanças detectadas**: N

---

### Adições Propostas
1. **Seção**: [nome]
   **Item**: [novo item]
   **Confidence**: [Alta/Média]
   **Evidências**:
   - [exemplo 1 de log]
   - [exemplo 2 de log]
   - [exemplo 3 de log]

---

### Modificações Propostas
1. **Seção**: [nome]
   **Item atual**: [texto atual]
   **Item novo**: [texto proposto]
   **Confidence**: [Alta/Média]
   **Evidências**: [3 exemplos]

---

### Remoções Propostas (se aplicável)
1. **Seção**: [nome]
   **Item**: [item obsoleto]
   **Motivo**: Não observado em últimos 60 dias

---

**Aprovar estas mudanças?** (y/n)
```

### 4. Aplicação (Se Aprovado)

a) **Criar snapshot**:
```bash
cp ~/.claude-memory/global-memory.md ~/.claude-memory/profile-history/YYYY-MM-DD_[description].md
```
Description: `manual_update`, `tech_update`, `preferences_update`, etc

b) **Atualizar global-memory.md**:
- Aplicar adições, modificações, remoções
- Atualizar header (data, incrementar versão)
- **Marcar novos PIIs** com `[PII:TYPE]...[/PII:TYPE]`

c) **Atualizar profile-changelog.md**:
Adicionar entrada:
```markdown
## YYYY-MM-DD - Versão X.Y
**Snapshot**: `profile-history/YYYY-MM-DD_description.md`
**Trigger**: Manual (/update-profile [scope])

**Mudanças**:
- ✨ Adicionado: [item]
- ✏️ Modificado: [item]
- 🗑️ Removido: [item]

**Seções atualizadas**: [lista]
**Confidence**: [geral]
```

d) **Regenerar .safe.md**:
```bash
python .claude/redact-pii.py
```

### 5. Confirmação
```
✓ Snapshot criado: profile-history/YYYY-MM-DD_description.md
✓ Perfil atualizado: global-memory.md (versão X.Y)
✓ Changelog atualizado
✓ .safe.md regenerado

Perfil atualizado com sucesso!
```

---

## Versionamento

**Semântico**:
- **Major (X.0)**: Mudanças grandes (novo emprego, stack principal diferente)
- **Minor (X.Y)**: Adições e modificações normais

---

## Validação

Sempre validar:
- [ ] Evidências claras (2-3 exemplos de logs)
- [ ] Confidence >= Média
- [ ] Aprovação explícita do usuário
- [ ] Snapshot criado antes de modificar
- [ ] Novos PIIs marcados
- [ ] .safe.md regenerado

---

**Importante**: NUNCA atualizar perfil sem aprovação do usuário.
