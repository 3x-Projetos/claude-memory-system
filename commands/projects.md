Lista todos os projetos com visão holística, agrupados por categoria.

## Passos

### 1. Ler todos os projetos
- Listar diretórios em `.projects/`
- Para cada projeto, ler `.context.md` (extrair Category, Status, Last Touched, Next Actions)

### 2. Agrupar por categoria
Identificar categorias:
- 💻 Code
- 🎨 Creative
- 🏗️ Physical
- 👤 Personal
- 🤝 Social/Community
- 💼 Business/Finance
- 🤖 AI/Research
- 🌐 Other

**Nota**: Projetos podem ter múltiplas categorias (ex: "💻 Code / 🎨 Creative")

### 3. Apresentar visão consolidada

Formato:

```
# Projects Dashboard 🎯

**Total**: X projetos ativos

---

## 💻 Code Projects

### Memory System - ✅ COMPLETE
- **Status**: v2.0 publicado no GitHub
- **Last**: 2025-11-16 (hoje)
- **Next**: M008 (em andamento), melhorias opcionais
- **Context**: `.projects/memory-system/.context.md`

### Hybrid Agent - 🔵 IMPLEMENTING
- **Status**: Fase 0 pendente
- **Last**: 2025-11-16 (hoje)
- **Next**: LM Studio API, benchmark, MCP server
- **Context**: `.projects/hybrid-agent/.context.md`

---

## 🎨 Creative Projects

### Creative Workflow - 📋 PLANNING
- **Status**: Prioridades identificadas
- **Last**: 2025-11-14
- **Next**: LM Studio setup, audio system
- **Context**: `.projects/creative-workflow/.context.md`

---

## 🏗️ Physical Projects
*(Nenhum projeto nesta categoria ainda)*

---

## 👤 Personal Projects
*(Nenhum projeto nesta categoria ainda)*

---

## Status Summary

- ✅ Complete: 1 projeto
- 🔵 Implementing: 1 projeto
- 📋 Planning: 1 projeto
- ⏸️ Paused: 0 projetos
- ❌ Blocked: 0 projetos

---

## Recent Activity (Last 3 Days)

1. **Memory System** - 2025-11-16 (hoje)
2. **Hybrid Agent** - 2025-11-16 (hoje)
3. **Creative Workflow** - 2025-11-14

---

## Commands

- `/switch [project-name]` → Mudar foco para projeto específico
- `/project-status [project-name]` → Atualizar status/roadmap
- `/projects` → Este dashboard (atualizar visão)

---

## Quick Actions

Sugerir baseado no contexto:
- Projetos BLOCKED ou PAUSED: "Retomar [project]?"
- Projetos não tocados há 7+ dias: "Atualizar status de [project]?"
- Projetos COMPLETE: "Arquivar ou adicionar melhorias?"
```

### 4. Highlighting de insights

Se detectar:
- **Projeto não tocado há 7+ dias**: Marcar com ⚠️
- **Projeto BLOCKED**: Destacar e perguntar como desbloquear
- **Múltiplos projetos IMPLEMENTING**: Avisar sobre context switching excessivo

### 5. Sugestões contextuais

Baseado em padrões:
- "3 projetos de Code ativos - considere focar em 1-2 por vez"
- "Projeto Physical sem atividade - ainda relevante?"
- "Creative Workflow conecta com Hybrid Agent (local LLM) - sinergia possível"

---

## Notas

- Dashboard **read-only** (não modifica arquivos)
- Atualizado dinamicamente ao executar comando
- Visão holística de **todos** os aspectos da vida (não só código)
- Útil para decidir prioridades e identificar sobrecarga

---

## Filosofia

Este comando implementa **augmentation**:
- Reduz clutter mental (tudo visível em um lugar)
- Identifica padrões (projetos esquecidos, sobrecarga)
- Sugere ações (priorização, sinergia entre projetos)
- Respeita multi-project workflow natural

---

*Parte do M008: Project-Centric Memory Layer*
