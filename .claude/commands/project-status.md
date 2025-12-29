Atualiza o status, roadmap ou decisões de um projeto específico.

## Uso
```
/project-status [project-name]
/project-status memory-system
```

---

## Passos

### 1. Validar projeto existe
- Verificar se `.projects/[project-name]/` existe
- Se NÃO: listar projetos disponíveis

### 2. Ler status atual
- Ler `.projects/[project-name]/.status.md`
- Apresentar resumo do status atual

### 3. Perguntar o que atualizar

```
Atualizando status de **[Project Name]**

Opções:
1. Mudar status do projeto (PLANNING → IMPLEMENTING, IMPLEMENTING → COMPLETE, etc)
2. Adicionar/atualizar milestone
3. Registrar decisão arquitetural importante
4. Atualizar métricas (tempo, custos, progresso)
5. Adicionar/resolver issue/blocker
6. Marcar como PAUSED ou COMPLETE

O que você quer atualizar? [1-6/outro]
```

### 4. Executar atualização

Baseado na escolha:

**Opção 1 - Mudar status**:
- Perguntar novo status (PLANNING/IMPLEMENTING/COMPLETE/PAUSED/BLOCKED)
- Atualizar campo "**Project Status**:" em `.status.md`
- Adicionar nota na seção relevante

**Opção 2 - Milestone**:
- Perguntar: adicionar novo ou marcar existente como completo?
- Atualizar seção "## Milestones"
- Se completar milestone: adicionar data de conclusão

**Opção 3 - Decisão arquitetural**:
- Perguntar: decisão, motivo, data
- Adicionar à seção "## Decisões Importantes"
- Formato padronizado

**Opção 4 - Métricas**:
- Perguntar quais métricas atualizar
- Atualizar seção "## Metrics"

**Opção 5 - Issue/Blocker**:
- Perguntar: adicionar novo ou resolver existente?
- Atualizar seção "## Known Issues & Limitations"

**Opção 6 - PAUSED ou COMPLETE**:
- Confirmar mudança de status
- Perguntar motivo (se PAUSED) ou conquistas (se COMPLETE)
- Atualizar `.status.md` e `.context.md`
- Se COMPLETE: perguntar se deve arquivar

### 5. Atualizar .context.md também

Se mudança de status:
- Atualizar campo "**Status**:" em `.context.md`
- Atualizar "**Last Touched**:" com timestamp atual

### 6. Confirmar atualização

```
✓ Status de **[Project Name]** atualizado.

Mudanças:
- [Lista de mudanças feitas]

Arquivos atualizados:
- .projects/[project-name]/.status.md
- .projects/[project-name]/.context.md (se aplicável)
```

---

## Exemplo Completo

```
> /project-status memory-system

Atualizando status de **Memory System**

Status atual: ✅ COMPLETE (v2.0)

Opções:
1. Mudar status
2. Adicionar milestone
3. Registrar decisão
4. Atualizar métricas
5. Adicionar issue
6. Marcar como PAUSED/COMPLETE

O que você quer atualizar? [1-6]

> 2

Adicionar novo milestone ou completar existente? [novo/completar]

> novo

Nome do milestone: v2.1 - Project-Centric Layer

Fase: Phase/Milestone number? (ex: Phase 1, Milestone 3)

> Milestone 3

Status: [🔵 Em Andamento / 📋 Planejado]

> 🔵 Em Andamento

Itens do milestone (um por linha, vazio para terminar):

> - [ ] M008: Estrutura .projects/ criada
> - [ ] Comandos /projects, /switch, /project-status
> - [ ] Atualização de /continue, /new, /end
> - [ ] Dashboard multi-projeto
>

✓ Milestone adicionado.

✓ Status de **Memory System** atualizado.

Mudanças:
- Adicionado: Milestone 3 "v2.1 - Project-Centric Layer" (Em Andamento)

Arquivos atualizados:
- .projects/memory-system/.status.md
- .projects/memory-system/.context.md (Last Touched atualizado)
```

---

## Notas

- Comando **write** (modifica arquivos)
- Mantém histórico de decisões e milestones
- Garante consistência entre `.context.md` e `.status.md`
- Útil para registrar progresso ao longo do tempo

---

## Filosofia

Tracking de projetos deve ser:
- **Fácil**: poucos comandos, fluxo claro
- **Flexível**: suporta qualquer tipo de projeto
- **Não-obstrutivo**: atualiza apenas quando relevante
- **Informativo**: histórico completo de decisões

---

*Parte do M008: Project-Centric Memory Layer*
