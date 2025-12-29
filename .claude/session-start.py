#!/usr/bin/env python3
"""
SessionStart Hook - Lazy Logging Strategy
1. Verifica se sessão ANTERIOR foi logged (via .previous-session-id)
2. Se não foi, registra a sessão anterior agora
3. Marca início da NOVA sessão
"""

import os
from datetime import datetime
from pathlib import Path

def get_state_file(filename):
    """Retorna path de arquivo de estado"""
    return Path(__file__).parent / filename

def get_log_path(date_str=None):
    """Retorna path do log do dia"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y.%m.%d")
    vault_path = Path(__file__).parent.parent
    logs_dir = vault_path / "logs" / "daily"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir / f"{date_str}.md"

def create_auto_session_entry(session_id):
    """Cria entrada automática para sessão não logged"""
    timestamp = session_id.replace('_', ' ').replace('-', ':')

    entry = f"""
---

## Sessão {timestamp.split()[1]}
**Encerramento**: Automático (Lazy Logging)

### Atividades Realizadas

_(Sessão encerrada sem executar `/end` - log gerado automaticamente no próximo startup)_

**Session ID**: {session_id}

### Notas

Este registro foi criado automaticamente pela estratégia de Lazy Logging porque a sessão anterior foi encerrada sem executar `/end`.

Para logs detalhados, use `/end` antes de encerrar.

---
"""
    return entry

def log_previous_session_if_needed():
    """Verifica e registra sessão anterior se necessário"""
    prev_file = get_state_file(".previous-session-id")

    if not prev_file.exists():
        return  # Primeira execução ou sessão anterior foi logged

    # Sessão anterior não foi logged, precisa registrar
    prev_session_id = prev_file.read_text(encoding='utf-8').strip()

    # Extrai data da sessão anterior
    date_part = prev_session_id.split('_')[0]
    log_path = get_log_path(date_part)

    # Adiciona entrada ao log
    entry = create_auto_session_entry(prev_session_id)

    if log_path.exists():
        # Append ao log existente
        content = log_path.read_text(encoding='utf-8')
        updated = content.rstrip() + "\n" + entry
        log_path.write_text(updated, encoding='utf-8')
    else:
        # Cria novo log com entrada automática
        header = f"""[session-log]

## Sessão: {date_part}

---
"""
        log_path.write_text(header + entry, encoding='utf-8')

    # Remove arquivo de sessão anterior (já foi logged)
    prev_file.unlink()

def main():
    """Executa lógica do SessionStart hook"""
    try:
        # PASSO 1: Registra sessão anterior se necessário (Lazy Logging)
        log_previous_session_if_needed()

        # PASSO 2: Marca início da NOVA sessão
        session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Salva como "sessão anterior" (será verificada no PRÓXIMO startup)
        prev_file = get_state_file(".previous-session-id")
        prev_file.write_text(session_id, encoding='utf-8')

        # Também mantém .current-session-id para compatibilidade com /end
        curr_file = get_state_file(".current-session-id")
        curr_file.write_text(session_id, encoding='utf-8')

    except Exception as e:
        # Erros silenciosos para não quebrar startup
        pass

if __name__ == "__main__":
    main()
