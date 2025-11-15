# Quick Start - Claude Memory System

Guia rápido de 5 minutos para começar a usar o sistema.

---

## 📦 Já Está Instalado?

Se você vê este arquivo, o sistema já está instalado! Pule para "Como Usar".

---

## 🚀 Instalando em Novo Projeto

```bash
# Copie o script de setup
cp .claude/setup-claude-memory.sh /seu/novo/projeto/

# Entre no diretório
cd /seu/novo/projeto

# Execute o setup
bash setup-claude-memory.sh

# Reinicie o Claude CLI
# Pronto!
```

---

## 💻 Como Usar

### Primeira Vez

1. **Reinicie o Claude CLI** (se acabou de instalar)
2. **Digite `/start`** para começar
3. **Trabalhe normalmente**
4. **Digite `/end`** ao finalizar

### Sessões Seguintes

```bash
# Inicia sessão mostrando resumo da anterior
/start

# Escolha: continuar de onde parou ou iniciar novo
> Continuar ou novo? [digite sua escolha]

# Trabalhe...

# Finaliza e registra tudo
/end
```

---

## 🎯 Comandos Principais

| Comando | Quando Usar | O Que Faz |
|---------|-------------|-----------|
| `/start` | Início da sessão | Carrega contexto + mostra última sessão |
| `/memory` | Durante trabalho | Lista ferramentas disponíveis |
| `/organize` | Organizar notas | Processa arquivo de notas |
| `/end` | Fim da sessão | Cria log estruturado |

---

## 📝 Exemplo Completo

```
# Dia 1 - Primeira sessão
Você: /start
Claude: Ferramentas carregadas. Nenhuma sessão anterior.
        Pronto para trabalhar!

Você: Preciso criar uma API REST
Claude: [trabalha na API...]

Você: /end
Claude: [cria log 2025.11.15.md com atividades e pendências]

---

# Dia 2 - Retomando
Você: /start
Claude: Última sessão: 2025-11-15
        Tópico: Desenvolvimento de API REST

        Pendências:
        - [ ] Adicionar autenticação
        - [ ] Escrever testes

        Continuar de onde paramos ou nova atividade?

Você: Continuar
Claude: Ótimo! Vamos trabalhar na autenticação da API...
```

---

## 📋 Organização de Notas

Quer organizar suas notas? Use este formato:

```markdown
[raw]

Minhas ideias e notas aqui...
- Tópico 1
- Tópico 2

---
[prompt]
Identifique os tópicos e sugira prioridades.

---
[organized]

[Resultado aparecerá aqui após /organize]
```

Então execute: `/organize nome-do-arquivo.md`

---

## ❓ Dúvidas?

- **Documentação completa**: `.claude/README.md`
- **Setup técnico**: `.claude/README-SETUP.md`
- **Ver ferramentas**: `/memory` no Claude CLI

---

## 🎓 Conceitos-Chave

1. **Memória**: Sistema "lembra" via logs em `YYYY.MM.DD.md`
2. **Workflows**: Processos documentados em `.workflow-*.md`
3. **Comandos**: Atalhos `/start`, `/end`, etc.
4. **Continuidade**: Cada sessão pode retomar a anterior

---

## ✅ Checklist Primeira Vez

- [ ] Sistema instalado (arquivos em `.claude/`)
- [ ] Claude CLI reiniciado
- [ ] Executei `/start` com sucesso
- [ ] Testei `/memory` para ver ferramentas
- [ ] Executei `/end` ao finalizar
- [ ] Vi o arquivo de log criado (YYYY.MM.DD.md)

---

**Pronto! Você está usando um Claude com memória persistente.**

**Próximo passo**: Use `/start` em todas as sessões e `/end` ao finalizar.

---

*Sistema versão 1.0*
