Muda o contexto de trabalho para um projeto específico, carregando sua memória completa.

## Uso
```
/switch [project-name]
/switch memory-system
/switch hybrid-agent
```

---

## Passos

### 1. Validar projeto existe
- Verificar se `.projects/[project-name]/` existe
- Se NÃO: listar projetos disponíveis e sugerir

### 2. Carregar contexto completo do projeto

**Ler arquivos**:
- `.projects/[project-name]/.context.md` - Working memory
- `.projects/[project-name]/.status.md` - Roadmap e decisões

**Apresentar**:
```
🔄 Switching to: [Project Name]

**Category**: [Category]
**Status**: [Status]
**Last Touched**: [Data]

---

## Current State
[Resumo do estado atual do projeto]

---

## Next Actions (Top 3)
1. [ ] Ação prioritária 1
2. [ ] Ação prioritária 2
3. [ ] Ação prioritária 3

---

## Key Files
- [Arquivo 1]
- [Arquivo 2]

---

## Recent Changes (Last Session)
[O que mudou recentemente]

---

Contexto carregado. Pronto para trabalhar em **[Project Name]**.
```

### 3. Atualizar .session-state.md

Modificar seção "Current Focus":
```markdown
## Current Focus
**Projeto**: [Project Name]
**Atividade**: [Aguardando definição]
**Desde**: [Timestamp atual]
```

### 4. Perguntar próxima ação

"O que você quer fazer em **[Project Name]**?"

Sugestões baseadas em "Next Actions":
- Continuar [ação pendente]
- Atualizar status
- Adicionar novas tarefas
- Trabalhar em [feature específica]

---

## Benefícios

**Reduz friction de context switching**:
- Carrega memória completa do projeto
- Recorda decisões importantes
- Lista próximas ações claras
- Atualiza working memory automaticamente

**Augmentation real**:
- Sistema se adapta ao seu foco
- Memória específica por projeto (não poluída)
- Transições orgânicas entre projetos

---

## Exemplo Completo

```
> /switch hybrid-agent

🔄 Switching to: Hybrid Agent System

**Category**: 💻 Code / 🤖 AI
**Status**: 🔵 PLANNING → IMPLEMENTING (Fase 0 pendente)
**Last Touched**: 2025-11-16

---

## Current State

Sistema híbrido multi-agente (Claude + LM Studio) completamente planejado:
- Arquitetura documentada (~37 páginas)
- Hardware specs validadas
- Roadmap definido (Fase 0-5)

Princípios: Model-agnostic, cross-domain first, distributed-ready, robustez > economia.

---

## Next Actions (Top 3)
1. [ ] Verificar LM Studio API rodando
2. [ ] Benchmark 1-2 modelos (GPU + CPU)
3. [ ] Implementar MCP server mínimo (~50 linhas)

---

## Key Files
- .claude/HYBRID-AGENT-ARCHITECTURE.md
- .claude/HARDWARE-SPECS.md
- hybrid-agent-system/README.md

---

## Recent Changes (Last Session)
Sessão 00:02 (2025-11-16): Planejamento completo, arquitetura documentada.

---

Contexto carregado. Pronto para trabalhar em **Hybrid Agent System**.

O que você quer fazer?
```

---

## Notas

- Context switch é **explícito** (usuário controla)
- Carregamento de memória **sob demanda** (economia de tokens)
- Atualização automática de `.session-state.md` (rastreamento)
- Workflow natural: `/projects` (ver tudo) → `/switch [name]` (focar em um)

---

*Parte do M008: Project-Centric Memory Layer*
