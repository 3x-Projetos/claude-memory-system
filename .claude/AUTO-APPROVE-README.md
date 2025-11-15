# Auto-Aprovação com Múltiplos Níveis

Este diretório contém um sistema de hook toggleável que permite ao Claude executar operações automaticamente sem pedir aprovação manual, com controle granular por tipo de operação.

## Arquivos

- `auto-approve-edits.py` - PreToolUse hook com suporte a múltiplos níveis
- `auto-approve-state` - Arquivo de estado (criado/modificado via `/auto-approve`)
- `.claude/commands/auto-approve.md` - Slash command para controlar o comportamento

## Níveis de Aprovação

- **off** - Nada aprovado automaticamente (padrão seguro)
- **edits** - Apenas Edit e Write
- **bash** - Edit, Write e Bash
- **all** - Todos os tools (sem confirmações)

## Como Usar

### ✅ Toggle em Tempo Real (SEM reiniciar CLI)

Use o slash command para alternar níveis instantaneamente:

```
/auto-approve on      # Ativa modo "edits" (Edit/Write apenas)
/auto-approve bash    # Ativa modo "bash" (Edit/Write/Bash)
/auto-approve all     # Ativa modo "all" (todos os tools)
/auto-approve off     # Desativa tudo (comportamento padrão)
/auto-approve status  # Verifica nível atual
```

### Como Configurar (Primeira Vez)

O hook já está configurado através de `.claude/settings.json` (configuração LOCAL deste projeto).

**Arquivo de configuração:** `.claude/settings.json`
**Script do hook:** `.claude/auto-approve-edits.py`
**Arquivo de estado:** `.claude/auto-approve-state`

Claude Code procura `settings.json` em dois lugares (nesta ordem):
1. **`.claude/settings.json`** (configuração LOCAL do projeto) ← **ESTAMOS USANDO ESTE**
2. `~/.claude/settings.json` (configuração GLOBAL)

Vantagens da configuração local:
- ✅ Hook funciona APENAS neste diretório
- ✅ Não afeta outros projetos
- ✅ Portável (vai junto no bootstrap)
- ✅ Não causa erros em outros diretórios

### Para ativar pela primeira vez:

1. **Reinicie o Claude CLI** (registra o hook)
2. **Use `/auto-approve on`** (ativa o comportamento)

### Conteúdo do .claude/settings.json:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/auto-approve-edits.py"
          }
        ]
      }
    ]
  }
}
```

_Nota: Matcher ".*" captura todos os tools. A lógica de aprovação por nível está no script Python._

## Como Funciona

1. Hook está sempre ativo (registrado no startup do CLI)
2. Quando Claude tenta executar qualquer operação:
   - Hook intercepta antes da execução
   - Script lê `.claude/auto-approve-state` e identifica o tool sendo chamado
   - Verifica se o tool deve ser aprovado baseado no nível:
     - **off**: Não aprova nada
     - **edits**: Aprova apenas Edit e Write
     - **bash**: Aprova Edit, Write e Bash
     - **all**: Aprova tudo
   - Retorna `"permissionDecision": "allow"` ou vazio (comportamento padrão)
3. Nível pode ser alterado a qualquer momento via `/auto-approve [on|bash|all|off]`
4. Efeito é **imediato** - próxima operação já usa novo nível

## Escopo

O hook verifica **todos** os tools dentro deste diretório de trabalho.

A decisão de aprovar ou não depende:
1. Do **nível** configurado em `.claude/auto-approve-state`
2. Do **tool** sendo executado

## Exemplo de Uso por Nível

**Modo edits** (recomendado para trabalho normal):
```
/auto-approve on
# Edit/Write: ✅ automático
# Bash: ❌ pede aprovação
```

**Modo bash** (quando precisa rodar comandos sem interrupção):
```
/auto-approve bash
# Edit/Write/Bash: ✅ automático
# Outros: ❌ pede aprovação
```

**Modo all** (máxima automação, use com cautela):
```
/auto-approve all
# Tudo: ✅ automático
# ⚠️ Nenhuma confirmação será pedida!
```

**Desativar** (volta ao comportamento padrão):
```
/auto-approve off
# Tudo: ❌ pede aprovação
```

## Remover Completamente

Se quiser desabilitar o hook permanentemente:
- Remova a configuração do hook do `settings.json` e reinicie o CLI

## Documentação Oficial

Mais informações sobre hooks: https://code.claude.com/docs/en/hooks.md
