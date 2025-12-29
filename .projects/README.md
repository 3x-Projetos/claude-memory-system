# Projects - Visão Holística

Este diretório contém **todos os projetos** que você está trabalhando ou planejando, independente da categoria.

---

## Categorias Suportadas

### 💻 Code
Projetos de desenvolvimento de software, frameworks, ferramentas.
- Exemplos: memory-system, hybrid-agent

### 🎨 Creative
Projetos criativos (arte, música, escrita, design).
- Exemplos: creative-workflow, image generation

### 🏗️ Physical
Projetos físicos (construção, reformas, fabricação, DIY).
- Exemplos futuros: reforma da casa, construir móvel, horta

### 👤 Personal
Desenvolvimento pessoal, saúde, fitness, hábitos.
- Exemplos futuros: rotina de exercícios, aprender idioma, meditação

### 🤝 Social/Community
Projetos comunitários, colaborativos, sociais.
- Exemplos futuros: comunidade autossustentável, eventos

### 💼 Business/Finance
Negócios, finanças, empreendedorismo.
- Exemplos futuros: startup, investimentos, budget tracking

### 🤖 AI/Research
Pesquisa, experimentos, prototipagem em AI/ML.
- Exemplos: hybrid-agent

### 🌐 Infrastructure/Network
Infraestrutura, redes, servidores, sistemas.
- Exemplos: remote-access-system

### 🌍 Other
Qualquer outra categoria não coberta acima.

---

## Estrutura de Cada Projeto

```
.projects/
└── [project-name]/
    ├── .context.md       # Working memory (ativo)
    ├── .status.md        # Roadmap, milestones, decisões
    └── history/          # Logs específicos (opcional)
```

### Template `.context.md`

```markdown
# [Project Name] - Working Context

**Category**: [Icon + Category] (ex: 💻 Code, 🏗️ Physical)
**Status**: [Icon + Status]
**Last Touched**: [Data]
**Related**: [Projetos conectados]

---

## Current State
[Descrição do estado atual - 2-3 parágrafos]

---

## Working Memory (Active Items)

### Completed This Session
- [x] Item

### Next Actions (Priority 1)
- [ ] Ação prioritária 1
- [ ] Ação prioritária 2

### Backlog
- [ ] Ação futura

---

## Key Files / Resources
[Arquivos principais, links, referências]

---

## Recent Changes
[Últimas mudanças - últimos 3 dias/sessões]

---

## Notes
[Observações importantes]
```

### Template `.status.md`

```markdown
# [Project Name] - Status & Roadmap

**Project Status**: [Icon + Status]
**Started**: [Data]
**Current Phase**: [Fase atual]

---

## Milestones

### ✅ Phase X: [Name] (Data)
- [x] Item completo

### 🔵 Phase Y: [Name] (Em Andamento)
- [ ] Item pendente

### 📋 Phase Z: [Name] (Planejado)
- [ ] Item futuro

---

## Decisões Importantes

1. **[Decisão]**
   - Decisão: [O que foi decidido]
   - Motivo: [Por quê]
   - Data: [Quando]

---

## Metrics
[Métricas relevantes - tempo, custo, progresso, etc]

---

## Known Issues & Limitations
[Problemas conhecidos, blockers]

---

## Future Improvements
[Melhorias planejadas]

---

## References
[Links, docs, recursos]
```

---

## Como Adicionar Novo Projeto

1. **Criar diretório**:
   ```bash
   mkdir -p .projects/[project-name]/history
   ```

2. **Copiar templates**:
   - Usar templates acima para criar `.context.md` e `.status.md`
   - Preencher com informações do projeto

3. **Escolher categoria(s)**:
   - Um projeto pode ter múltiplas categorias (ex: "💻 Code / 🎨 Creative")
   - Use ícones + texto para clareza visual

4. **Atualizar `.session-state.md`**:
   - Adicionar projeto à seção "Active Projects"

---

## Comandos Disponíveis

- `/projects` - Lista todos os projetos (agrupados por categoria)
- `/switch [project-name]` - Muda contexto para projeto específico
- `/project-status [project-name]` - Atualiza status/roadmap

---

## Filosofia: Visão Holística

Este sistema suporta **todos os aspectos da sua vida**, não apenas código:
- Projetos digitais e físicos
- Trabalho e pessoal
- Individual e comunitário
- Técnico e criativo

**Objetivo**: Reduzir clutter mental organizando tudo em um único sistema coerente, mantendo visibilidade clara de:
- O que está ativo vs pausado
- Prioridades por projeto
- Conexões entre projetos
- Progresso ao longo do tempo

---

*Parte do M008: Project-Centric Memory Layer*
*Sistema de Memória Hierárquica v2.1+*
