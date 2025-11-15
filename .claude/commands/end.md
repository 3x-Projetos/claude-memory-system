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

**IMPORTANTE**: Após criar/atualizar o log, SEMPRE delete o arquivo `.claude/.current-session-id` usando Bash:
```bash
rm -f .claude/.current-session-id
```

Isso marca a sessão como registrada e evita que o SessionEnd hook crie log duplicado.

Ao finalizar, confirme que o log foi criado e deseje um bom trabalho.
