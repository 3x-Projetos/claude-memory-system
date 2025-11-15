#!/usr/bin/env python3
"""
SessionEnd Hook - Graceful Shutdown
Garante que toda sessão seja registrada mesmo se o usuário não executar /end
Rastreia sessão atual via .current-session-id criado pelo SessionStart hook
"""

import os
from datetime import datetime
from pathlib import Path

def get_session_state_file():
    """Retorna path do arquivo de estado da sessão atual"""
    return Path(__file__).parent / ".current-session-id"

def get_log_path():
    """Retorna path do log do dia atual"""
    today = datetime.now().strftime("%Y.%m.%d")
    vault_path = Path(__file__).parent.parent
    return vault_path / f"{today}.md"

def session_was_logged():
    """
    Verifica se a sessão atual foi registrada via /end
    Se .current-session-id NÃO existe → /end deletou → sessão foi logged
    Se .current-session-id EXISTE → /end não foi executado → precisa registrar
    """
    state_file = get_session_state_file()
    return not state_file.exists()

def get_session_id():
    """Lê o ID da sessão atual"""
    state_file = get_session_state_file()
    if state_file.exists():
        return state_file.read_text(encoding='utf-8').strip()
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def create_session_entry(session_id):
    """Cria entrada de sessão para append ao log"""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M")

    entry = f"""
---

## Sessão {session_id.split('_')[1].replace('-', ':')}
**Encerramento**: Automático (SessionEnd hook)

### Atividades Realizadas

_(Sessão encerrada sem executar `/end` - log gerado automaticamente)_

**Timestamp**: {timestamp}

### Notas

Este registro foi criado automaticamente pelo SessionEnd hook porque a sessão foi encerrada sem executar `/end`.

Para logs detalhados, use `/end` antes de encerrar.

---
"""
    return entry

def create_new_log(log_path, session_id):
    """Cria novo arquivo de log com primeira sessão"""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M")

    content = f"""[session-log]

## Sessão: {now.strftime("%Y-%m-%d")}

---

## Sessão {session_id.split('_')[1].replace('-', ':')}
**Encerramento**: Automático (SessionEnd hook)

### Atividades Realizadas

_(Sessão encerrada sem executar `/end` - log gerado automaticamente)_

**Timestamp**: {timestamp}

---

### Notas

Este log foi criado automaticamente pelo SessionEnd hook porque a sessão foi encerrada sem executar `/end`.

Para logs detalhados e estruturados, use `/end` antes de encerrar a sessão.

---

*Log automático gerado em {timestamp}*
"""

    log_path.write_text(content, encoding='utf-8')

def append_session_to_log(log_path, session_id):
    """Adiciona nova entrada de sessão ao log existente"""
    existing_content = log_path.read_text(encoding='utf-8')
    new_entry = create_session_entry(session_id)

    # Append no final do arquivo
    updated_content = existing_content.rstrip() + "\n" + new_entry
    log_path.write_text(updated_content, encoding='utf-8')

def cleanup_session_state():
    """Remove arquivo de estado da sessão"""
    state_file = get_session_state_file()
    if state_file.exists():
        state_file.unlink()

def main():
    """Executa lógica do SessionEnd hook"""
    try:
        # Verifica se sessão atual já foi logged
        if session_was_logged():
            # /end foi executado, não precisa fazer nada
            return

        # Sessão não foi logged via /end, precisa registrar
        session_id = get_session_id()
        log_path = get_log_path()

        if log_path.exists():
            # Log do dia existe (sessões anteriores), append nova sessão
            append_session_to_log(log_path, session_id)
        else:
            # Primeira sessão do dia, cria log novo
            create_new_log(log_path, session_id)

        # Limpa arquivo de estado
        cleanup_session_state()

        # Execução silenciosa (não imprime nada)

    except Exception as e:
        # Erros silenciosos para não quebrar shutdown
        # Para debug, descomente:
        # import sys
        # print(f"SessionEnd hook error: {e}", file=sys.stderr)
        pass

if __name__ == "__main__":
    main()
