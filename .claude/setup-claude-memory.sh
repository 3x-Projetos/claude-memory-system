#!/bin/bash

# Setup Claude Memory System
# Creates a complete memory/workflow/logging system for Claude CLI
# Version: 1.0
# Date: 2025-11-15

echo "=== Claude Memory System Setup ==="
echo "This will create a complete workflow system for Claude CLI"
echo ""

# Get target directory (default to current)
TARGET_DIR="${1:-.}"
cd "$TARGET_DIR" || exit 1

echo "Target directory: $(pwd)"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 1
fi

echo ""
echo "Creating directory structure..."

# Create .claude/commands directory
mkdir -p .claude/commands

echo "✓ Directory structure created"
echo ""
echo "Creating workflow files..."

# 1. Create .claude-memory.md
cat > .claude-memory.md << 'EOF'
# Claude Memory - Toolbox

Este arquivo serve como índice central da "caixa de ferramentas" - arquivos de memória persistente que definem workflows, processos e contextos para auxiliar nas interações com Claude neste diretório.

**Leia este arquivo no início de cada sessão para ter acesso às ferramentas e contextos disponíveis.**

---

## About

Este diretório contém arquivos de workflow e memória que permitem ao Claude manter consistência e eficiência nas interações. Cada arquivo de memória documenta um processo específico que pode ser invocado durante as sessões.

---

## Ferramentas Disponíveis

### 1. Workflow de Organização de Notas
**Arquivo**: `.workflow-claude-notes-organization.md`

**Propósito**: Define o processo padrão para organização de notas diárias com identificação de tópicos e sugestão de prioridades.

**Quando usar**: Sempre que houver um arquivo de notas com blocos `[raw]` e `[prompt]` que precise ser processado.

**Estrutura**:
- Blocos: `[raw]` → `[prompt]` → `[organized]`
- Separadores: `---` entre blocos
- Tags sempre em minúsculas

**Comando típico**:
```
leia o [arquivo].md e execute a ação contida no bloco [prompt].
Registre o retorno no local [organized], mantendo a tag.
```

**Output esperado**:
- Topics Identified & Organized
- Suggested Priorities com próximos passos

### 2. Workflow de Session Logging
**Arquivo**: `.workflow-session-logging.md`

**Propósito**: Registrar todas as interações e atividades realizadas em cada sessão para manter histórico e continuidade.

**Quando usar**:
- Início: `/start` carrega contexto e lembra de fazer log
- Fim: `/end` cria/atualiza log da sessão

**Estrutura**:
- Arquivo: `YYYY.MM.DD.md` (exemplo: `2025.11.15.md`)
- Bloco: `[session-log]`
- Seções: Atividades, Arquivos modificados, Próximos passos, Notas

**Obrigatório**: Toda sessão deve ter seu log registrado

### 3. Workflow de Session Continuity
**Arquivo**: `.workflow-session-continuity.md`

**Propósito**: Manter contexto entre sessões, permitindo retomar trabalho de onde parou ou iniciar nova atividade com awareness do histórico.

**Como funciona**:
- `/start` lê automaticamente o log mais recente
- Apresenta resumo da última sessão
- Lista pendências (tarefas não concluídas)
- Pergunta se deve continuar ou iniciar novo foco

**Benefícios**:
- Continuidade natural sem reexplicar contexto
- Retoma direto de onde parou
- Flexibilidade para mudar de foco mantendo histórico

---

## Convenções Gerais

### Nomenclatura de Arquivos de Memória
- Prefixo com `.` para arquivos ocultos de workflow
- Formato: `.workflow-[nome-descritivo].md`
- Memória central: `.claude-memory.md` (este arquivo)

### Tags e Marcadores
- Sempre minúsculas: `[raw]`, `[prompt]`, `[organized]`, etc.
- Separadores visuais: `---`
- Blocos claramente demarcados

---

## Slash Commands Disponíveis

### `/start`
Carrega a caixa de ferramentas no início da sessão. Lê este arquivo e confirma ferramentas disponíveis. Lembra de usar `/end` ao finalizar.

### `/memory`
Consulta a caixa de ferramentas durante a sessão. Útil para relembrar workflows disponíveis.

### `/organize`
Executa o workflow de organização de notas. Pode especificar o arquivo ou será perguntado.

### `/end`
Finaliza a sessão criando/atualizando o log de atividades do dia (YYYY.MM.DD.md). Pergunta sobre atividades realizadas e cria registro estruturado.

---

## Como Adicionar Novas Ferramentas

1. Crie arquivo `.workflow-[nome].md` documentando o processo
2. Adicione entrada nesta seção "Ferramentas Disponíveis"
3. Descreva: arquivo, propósito, quando usar, estrutura esperada
4. Opcionalmente, crie slash command em `.claude/commands/[nome].md`

---

## Contexto do Diretório

**Tipo**: [Descrever tipo de projeto]
**Uso**: [Descrever uso principal]
**Tópicos principais**: [Listar tópicos]

---

*Sistema instalado em: $(date +%Y-%m-%d)*
EOF

echo "✓ .claude-memory.md"

# 2. Create workflow files
cat > .workflow-claude-notes-organization.md << 'EOF'
# Workflow: Organização de Notas

Define o processo padrão para organização de notas diárias com identificação de tópicos e sugestão de prioridades.

## Estrutura de Arquivo de Notas

### Blocos Principais
Os arquivos de notas devem conter os seguintes blocos, separados por `---`:

1. **[raw]** - Notas brutas/originais
2. **[prompt]** - Instrução para processamento
3. **[organized]** - Resultado do processamento

## Exemplo

```markdown
[raw]

Minhas notas aqui...

---
[prompt]
Identifique os tópicos e organize-os.
Sugira prioridades com próximos passos.

---
[organized]

[Resultado será inserido aqui]
```

## Convenções

- Tags sempre em minúsculas
- Separadores: `---` entre blocos
- Output inclui: Topics Identified & Organized, Suggested Priorities

---

*Versão: 1.0*
EOF

echo "✓ .workflow-claude-notes-organization.md"

cat > .workflow-session-logging.md << 'EOF'
# Workflow: Session Logging

Documenta o processo de registro de interações com Claude.

## Propósito

Manter histórico detalhado de todas as sessões, decisões tomadas, arquivos modificados e workflows executados.

## Processo

### Ao Finalizar Sessão
Use `/end` que irá:
1. Criar arquivo `YYYY.MM.DD.md`
2. Usar bloco `[session-log]`
3. Documentar: Atividades, Arquivos modificados, Próximos passos, Notas

## Estrutura do Log

```markdown
[session-log]

## Sessão: YYYY-MM-DD
**Tópico**: [Descrição breve]

---

### Atividades Realizadas

#### 1. [Nome da Atividade]
- Descrição
- Resultados

---

### Arquivos Criados/Modificados

**Criados**:
- `arquivo.ext` - Descrição

**Modificados**:
- `arquivo.ext` - O que mudou

---

### Próximos Passos

- [ ] Tarefa pendente 1
- [ ] Tarefa pendente 2

---

### Notas

Observações, insights, decisões importantes.
```

---

*Versão: 1.0*
EOF

echo "✓ .workflow-session-logging.md"

cat > .workflow-session-continuity.md << 'EOF'
# Workflow: Continuidade de Sessões

Documenta como manter contexto e continuidade entre diferentes sessões.

## Propósito

Permitir que cada nova sessão tenha acesso ao contexto da sessão anterior.

## Como Funciona

### Ao Iniciar Nova Sessão

Use `/start` que irá:
1. Carregar `.claude-memory.md`
2. Buscar log mais recente (YYYY.MM.DD.md)
3. Ler "Próximos Passos" e "Notas"
4. Apresentar resumo + pendências
5. Perguntar se deve continuar ou iniciar novo

## Benefícios

1. Continuidade natural sem reexplicar contexto
2. Retoma direto de onde parou
3. Histórico completo do trabalho
4. Flexibilidade para continuar ou mudar de foco

---

*Versão: 1.0*
EOF

echo "✓ .workflow-session-continuity.md"

echo ""
echo "Creating slash commands..."

# 3. Create slash commands
cat > .claude/commands/start.md << 'EOF'
---
description: Carrega a caixa de ferramentas e contexto da sessão
---

Leia o arquivo `.claude-memory.md` para carregar a caixa de ferramentas e contexto disponível neste diretório.

Em seguida, busque o arquivo de log mais recente (formato YYYY.MM.DD.md) no diretório:
1. Liste arquivos que seguem o padrão de data (2025.*.md, 2024.*.md, etc)
2. Identifique o mais recente
3. Se encontrado, leia a seção "Próximos Passos" e "Notas"

Apresente:
- Quantas ferramentas estão disponíveis e seus nomes
- **Última sessão**: Data e resumo rápido (1-2 linhas)
- **Pendências**: Liste tarefas não concluídas [ ] se houver
- Pergunte: "Deseja continuar de onde paramos ou iniciar nova atividade?"

Se não houver log anterior, apenas:
- Liste ferramentas disponíveis
- Informe que está pronto para trabalhar

Ao final, lembre: use `/end` para registrar a sessão.

Seja conciso e direto.
EOF

echo "✓ /start"

cat > .claude/commands/memory.md << 'EOF'
---
description: Consulta a caixa de ferramentas disponível
---

Leia o arquivo `.claude-memory.md` e apresente as ferramentas disponíveis de forma estruturada e concisa.
EOF

echo "✓ /memory"

cat > .claude/commands/organize.md << 'EOF'
---
description: Organiza as notas do arquivo especificado usando o workflow padrão
---

Leia o arquivo `.workflow-claude-notes-organization.md` para consultar o workflow.

Em seguida, pergunte ao usuário qual arquivo de notas deve ser processado (se não foi especificado).

Execute o workflow:
1. Ler o arquivo de notas
2. Executar a ação do bloco [prompt]
3. Registrar resultado no bloco [organized]
4. Manter tags em minúsculas e separadores ---
EOF

echo "✓ /organize"

cat > .claude/commands/end.md << 'EOF'
---
description: Finaliza sessão e cria/atualiza log de atividades
---

Leia o arquivo `.workflow-session-logging.md` para consultar o formato de log.

Agora vamos finalizar esta sessão:

1. Identifique a data de hoje no formato YYYY.MM.DD
2. Verifique se já existe arquivo com esse nome
3. Se não existir, crie novo log seguindo a estrutura documentada
4. Se existir, pergunte se devo atualizar ou criar nova seção

Para criar o log, você deve me perguntar:
- Qual foi o tópico/foco principal da sessão?
- Quais foram as principais atividades realizadas?
- Há próximos passos ou tarefas pendentes?

Com essas informações, crie/atualize o arquivo de log seguindo o formato padrão com bloco `[session-log]`.

Ao finalizar, confirme que o log foi criado e deseje um bom trabalho.
EOF

echo "✓ /end"

echo ""
echo "Creating setup documentation..."

cat > .claude/README-SETUP.md << 'EOF'
# Claude Memory System - Setup Documentation

Sistema de memória persistente, workflows e logging para Claude CLI.

## O que foi instalado

### Arquivos de Memória e Workflows
- `.claude-memory.md` - Índice central de todas as ferramentas
- `.workflow-claude-notes-organization.md` - Workflow de organização de notas
- `.workflow-session-logging.md` - Workflow de logging de sessões
- `.workflow-session-continuity.md` - Workflow de continuidade entre sessões

### Slash Commands
- `/start` - Inicia sessão com contexto da sessão anterior
- `/memory` - Consulta ferramentas disponíveis
- `/organize` - Organiza notas com estrutura [raw] → [prompt] → [organized]
- `/end` - Finaliza sessão criando log estruturado

## Como Usar

### Primeira vez
1. Reinicie o Claude CLI
2. Digite `/start` para começar
3. Os comandos customizados devem aparecer ao digitar `/`

### Fluxo de trabalho típico
```
1. Início: /start
   → Carrega ferramentas
   → Mostra resumo da última sessão
   → Pergunta se continua ou inicia novo

2. Durante a sessão:
   - /memory para consultar ferramentas
   - /organize para processar notas
   - Trabalhar normalmente

3. Fim: /end
   → Cria log estruturado (YYYY.MM.DD.md)
   → Registra atividades e próximos passos
```

## Personalização

### Atualizar contexto do diretório
Edite `.claude-memory.md` na seção "Contexto do Diretório" para descrever seu projeto.

### Adicionar novos workflows
1. Crie `.workflow-[nome].md`
2. Documente o processo
3. Adicione entrada em `.claude-memory.md`
4. Opcionalmente crie comando em `.claude/commands/[nome].md`

## Estrutura de Arquivos

```
./
├── .claude-memory.md                      # Índice central
├── .workflow-*.md                         # Workflows documentados
├── .claude/
│   ├── README-SETUP.md                    # Esta documentação
│   ├── setup-claude-memory.sh             # Script de instalação
│   └── commands/
│       ├── start.md                       # /start
│       ├── memory.md                      # /memory
│       ├── organize.md                    # /organize
│       └── end.md                         # /end
└── YYYY.MM.DD.md                          # Logs de sessões
```

## Convenções

- Tags sempre minúsculas: `[raw]`, `[prompt]`, `[organized]`, `[session-log]`
- Separadores visuais: `---`
- Logs diários: `YYYY.MM.DD.md`
- Workflows: `.workflow-[nome].md`

## Reinstalar/Atualizar

Para reinstalar em outro diretório:
```bash
bash setup-claude-memory.sh [diretório-destino]
```

---

*Sistema versão 1.0 - 2025-11-15*
EOF

echo "✓ README-SETUP.md"

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Arquivos criados:"
echo "  • .claude-memory.md"
echo "  • .workflow-claude-notes-organization.md"
echo "  • .workflow-session-logging.md"
echo "  • .workflow-session-continuity.md"
echo "  • .claude/commands/start.md"
echo "  • .claude/commands/memory.md"
echo "  • .claude/commands/organize.md"
echo "  • .claude/commands/end.md"
echo "  • .claude/README-SETUP.md"
echo ""
echo "Próximos passos:"
echo "  1. Reinicie o Claude CLI"
echo "  2. Digite /start para começar"
echo "  3. Leia .claude/README-SETUP.md para documentação completa"
echo ""
echo "✓ Sistema pronto para uso!"
