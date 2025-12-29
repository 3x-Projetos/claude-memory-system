# Claude Memory System

Sistema completo de memória persistente, workflows e logging para Claude CLI.

> **Versão**: 1.0
> **Data**: 2025-11-15
> **Autor**: Desenvolvido colaborativamente com Claude

---

## 🎯 O que é isso?

Um sistema que permite ao Claude:
- **Lembrar** de sessões anteriores
- **Retomar** trabalho de onde parou
- **Organizar** notas automaticamente
- **Registrar** todas as atividades

Basicamente, transforma o Claude CLI em um assistente com memória persistente.

---

## ⚡ Quick Start

```bash
# 1. Instalar em um novo diretório
bash .claude/setup-claude-memory.sh /caminho/do/projeto

# 2. Reiniciar Claude CLI

# 3. Começar a usar
/start
```

---

## 🛠️ Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/start` | Inicia sessão, mostra resumo da anterior, pergunta se continua ou inicia novo |
| `/memory` | Lista todas as ferramentas/workflows disponíveis |
| `/organize` | Organiza notas seguindo estrutura [raw] → [prompt] → [organized] |
| `/end` | Finaliza sessão e cria log estruturado do dia |

---

## 📋 Workflows Incluídos

### 1. Organização de Notas
Processa notas brutas e gera análise estruturada com tópicos e prioridades.

**Arquivo**: `.workflow-claude-notes-organization.md`

### 2. Session Logging
Registra todas as atividades de cada sessão em formato estruturado.

**Arquivo**: `.workflow-session-logging.md`

### 3. Session Continuity
Mantém contexto entre sessões - você pode retomar de onde parou.

**Arquivo**: `.workflow-session-continuity.md`

---

## 💡 Exemplo de Uso

```
Você: /start

Claude:
Ferramentas carregadas: 3 workflows disponíveis

Última sessão: 2025-11-14
Tópico: Desenvolvimento de features X e Y

Pendências:
- [ ] Implementar testes para feature X
- [ ] Revisar PR #123

Deseja continuar de onde paramos ou iniciar nova atividade?

---

Você: Continuar

Claude: Ótimo! Vejo que você precisa implementar testes para
feature X. Quer que eu ajude com isso?
```

---

## 📁 Estrutura de Arquivos

```
./
├── .claude-memory.md                      # Índice central de ferramentas
├── .workflow-claude-notes-organization.md # Workflow: organizar notas
├── .workflow-session-logging.md           # Workflow: logging
├── .workflow-session-continuity.md        # Workflow: continuidade
├── .claude/
│   ├── README.md                          # Este arquivo
│   ├── README-SETUP.md                    # Docs técnicas
│   ├── setup-claude-memory.sh             # Script de instalação
│   └── commands/
│       ├── start.md
│       ├── memory.md
│       ├── organize.md
│       └── end.md
└── 2025.11.15.md                          # Logs de sessões (criados por /end)
```

---

## 🔧 Personalização

### Adicionar Novo Workflow

1. Criar arquivo `.workflow-meu-workflow.md`
2. Documentar o processo
3. Adicionar entrada em `.claude-memory.md`
4. Opcionalmente criar comando em `.claude/commands/meu-comando.md`

### Atualizar Contexto

Edite `.claude-memory.md` → seção "Contexto do Diretório" para descrever seu projeto.

---

## 📜 Convenções

- **Tags**: sempre minúsculas (`[raw]`, `[prompt]`, `[organized]`, `[session-log]`)
- **Separadores**: use `---` entre blocos
- **Logs**: formato `YYYY.MM.DD.md` (ex: `2025.11.15.md`)
- **Workflows**: prefixo `.workflow-[nome].md`

---

## 🚀 Instalação em Novo Projeto

```bash
# Copiar o script de setup
cp .claude/setup-claude-memory.sh /novo/projeto/.claude/

# Executar
cd /novo/projeto
bash .claude/setup-claude-memory.sh

# Reiniciar Claude CLI e usar /start
```

---

## 📚 Documentação Completa

- **Setup técnico**: `.claude/README-SETUP.md`
- **Workflows individuais**: Arquivos `.workflow-*.md`
- **Memória central**: `.claude-memory.md`

---

## 🎓 Como Funciona

1. **Memória Central**: `.claude-memory.md` indexa todas as ferramentas
2. **Workflows**: Arquivos `.workflow-*.md` documentam processos
3. **Slash Commands**: Automatizam workflows via comandos `/`
4. **Logs**: Arquivos `YYYY.MM.DD.md` registram cada sessão
5. **Continuidade**: `/start` lê logs anteriores e oferece retomar

---

## 🤝 Contribuindo

Este é um sistema vivo. Para melhorá-lo:

1. Crie novos workflows conforme necessário
2. Adicione comandos úteis em `.claude/commands/`
3. Documente em `.claude-memory.md`
4. Mantenha convenções de nomenclatura

---

## 📝 Changelog

### v1.0 (2025-11-15)
- ✨ Sistema inicial completo
- ✨ 3 workflows: organização, logging, continuidade
- ✨ 4 comandos: /start, /memory, /organize, /end
- ✨ Script de instalação automatizado
- ✨ Documentação completa

---

## 📄 Licença

Livre para usar, modificar e distribuir. Sistema desenvolvido colaborativamente com Claude.

---

**Pronto para começar? Execute `/start` no Claude CLI!**
