---
description: Inicia nova atividade (carrega contexto mas começa do zero)
---

Iniciando nova atividade com awareness de contexto.

## Passos

### 1. Executar redação de PII
```bash
python .claude/redact-pii.py
```

### 2. Carregar memória global (redacted)
Ler `~/.claude-memory/global-memory.safe.md`:
- User Profile
- Collaboration Patterns
- Projects Context (awareness)
- Architecture Decisions

### 3. Carregar resumos de alto nível (awareness)
Ler apenas para contexto geral, **sem** detalhes de pendências:

a) **Último resumo mensal** (se existir):
   - Tendências de longo prazo
   - Tecnologias e padrões recentes

b) **Última sessão** (data apenas):
   - Ler `.session-state.md` apenas para saber quando foi a última vez

### 4. Detectar agregações pendentes (opcional)
Se houver semanas/meses sem agregação, informar brevemente (não insistir).

### 5. Apresentar contexto ao usuário
Formato conciso e otimista:

```
**Framework disponível**: X ferramentas, Y workflows
**Última sessão**: [Data]
(Se houver) **Contexto recente**: [1 linha sobre o que tem sido trabalhado]

Pronto para nova atividade. O que vamos fazer?
```

### 6. Lembrete final
"Use `/end` para registrar esta sessão ao finalizar."

---

## Diferença vs /continue
- **`/continue`**: Foco em retomar trabalho → lista pendências, próximos passos
- **`/new`**: Foco em começar novo → awareness de contexto, sem listar TODOs

Ambos carregam memória global e hierarquia, mas /new não pressiona para completar pendências.
