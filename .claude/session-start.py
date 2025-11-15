#!/usr/bin/env python3
"""
SessionStart Hook - Marca início de nova sessão
Cria identificador único para rastrear se a sessão foi registrada via /end
"""

import os
from datetime import datetime
from pathlib import Path

def main():
    """Marca início de nova sessão"""
    try:
        # Cria ID único baseado em timestamp
        session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Salva em arquivo de estado
        state_file = Path(__file__).parent / ".current-session-id"
        state_file.write_text(session_id, encoding='utf-8')

        # Execução silenciosa (não imprime nada)

    except Exception as e:
        # Erros silenciosos para não quebrar o startup
        pass

if __name__ == "__main__":
    main()
