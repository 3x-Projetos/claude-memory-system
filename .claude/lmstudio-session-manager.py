#!/usr/bin/env python3
"""
LMStudio Session Manager - Context Window Tracking

Gerencia sessões do LMStudio com monitoramento automático de tokens
e checkpoint quando atingir limite de contexto.

Integrado com memory-system (M008/M009/M010)
"""

import json
import requests
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class LMStudioSession:
    """Gerencia uma sessão do LMStudio com tracking de tokens"""

    # Configurações
    API_BASE = "http://127.0.0.1:1234/v1"
    LMS_CLI = str(Path.home() / ".lmstudio" / "bin" / "lms.exe")  # Windows default
    DEFAULT_MODEL = "qwen/qwen3-vl-30b"

    # Thresholds (percentual do limite configurado)
    WARNING_THRESHOLD = 0.70  # Alerta em 70%
    CHECKPOINT_THRESHOLD = 0.85  # Checkpoint em 85%

    # Paths
    MEMORY_BASE = Path.home() / ".claude-memory"
    PROVIDER_DIR = MEMORY_BASE / "providers" / "lmstudio"
    SESSION_STATE_FILE = PROVIDER_DIR / "session-state.md"
    LOGS_DIR = PROVIDER_DIR / "logs" / "daily"

    def __init__(self, model: str = None):
        """Inicializa sessão do LMStudio"""
        self.model = model or self.DEFAULT_MODEL

        # Consultar limite REAL configurado no LMStudio
        self.context_limit = self._get_configured_context_limit()

        # Estado da sessão
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.messages: List[Dict] = []
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.call_count = 0

        # Criar diretórios se não existirem
        self.PROVIDER_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)

        # Log inicial
        self._log(f"Session started: {self.session_id}")
        self._log(f"Model: {self.model} | Context limit: {self.context_limit} tokens")
        self._log(f"Thresholds: Warning={int(self.context_limit*self.WARNING_THRESHOLD)}, Checkpoint={int(self.context_limit*self.CHECKPOINT_THRESHOLD)}")

    def chat(self, prompt: str, system: str = None, max_tokens: int = 2048,
             temperature: float = 0.7) -> Tuple[str, Dict]:
        """
        Envia prompt ao LMStudio e retorna resposta + métricas

        Returns:
            (response_text, metrics_dict)
        """
        # Verificar se precisa checkpoint ANTES de enviar
        estimated_tokens = len(prompt.split()) * 1.3  # Estimativa grosseira
        if self.total_prompt_tokens + estimated_tokens > self.context_limit * self.CHECKPOINT_THRESHOLD:
            self._auto_checkpoint()

        # Preparar mensagens
        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        # Adicionar histórico (últimas N mensagens)
        messages.extend(self.messages[-10:])  # Manter últimas 10 trocas

        # Adicionar prompt atual
        messages.append({"role": "user", "content": prompt})

        # Fazer chamada à API
        try:
            response = requests.post(
                f"{self.API_BASE}/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=300  # 5 min timeout
            )
            response.raise_for_status()
            data = response.json()

            # Extrair resposta
            assistant_msg = data["choices"][0]["message"]["content"]

            # Extrair métricas
            usage = data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)

            # Atualizar estado
            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            self.call_count += 1

            # Adicionar ao histórico
            self.messages.append({"role": "user", "content": prompt})
            self.messages.append({"role": "assistant", "content": assistant_msg})

            # Preparar métricas
            metrics = {
                "call_tokens": {
                    "prompt": prompt_tokens,
                    "completion": completion_tokens,
                    "total": prompt_tokens + completion_tokens
                },
                "session_tokens": {
                    "prompt": self.total_prompt_tokens,
                    "completion": self.total_completion_tokens,
                    "total": self.total_prompt_tokens + self.total_completion_tokens
                },
                "context_usage": {
                    "used": self.total_prompt_tokens,
                    "limit": self.context_limit,
                    "percentage": round((self.total_prompt_tokens / self.context_limit) * 100, 1),
                    "remaining": self.context_limit - self.total_prompt_tokens
                },
                "call_count": self.call_count,
                "model": self.model
            }

            # Verificar thresholds
            usage_pct = metrics["context_usage"]["percentage"] / 100

            if usage_pct >= self.CHECKPOINT_THRESHOLD:
                self._log(f"[!] CHECKPOINT THRESHOLD ({usage_pct*100:.1f}%) - Auto-checkpoint triggered")
            elif usage_pct >= self.WARNING_THRESHOLD:
                self._log(f"[!] WARNING ({usage_pct*100:.1f}%) - Approaching context limit")

            # Log da chamada
            self._log(f"Call #{self.call_count} | Tokens: {prompt_tokens}->{completion_tokens} | Total: {self.total_prompt_tokens}/{self.context_limit} ({usage_pct*100:.1f}%)")

            return assistant_msg, metrics

        except Exception as e:
            self._log(f"[ERROR] {str(e)}")
            raise

    def _generate_rich_summary(self) -> str:
        """
        Gera resumo rico da sessão para handoff seamless

        Similar ao /continue do Claude - preserva contexto crítico
        """
        summary_prompt = """You are finishing a work session that reached the context limit.

**Your task**: Create a structured summary for seamless handoff to the next session.

**Format**:
## Session Context
[1-2 sentences: what you were doing]

## Key Decisions & Findings
- Decision/finding 1
- Decision/finding 2
- Decision/finding 3
(list all important ones)

## Current State
- Main task status
- Progress so far (%)

## Next Actions (Priority Order)
1. Immediate next step
2. Second step
3. Third step

## Important Context to Remember
- Critical constraint/limitation
- Critical technical detail
- Context that cannot be lost

Be concise but complete (~30-50 lines). Focus on what is CRITICAL to continue the work."""

        try:
            # Fazer chamada especial para gerar summary (não conta no histórico)
            response = requests.post(
                f"{self.API_BASE}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant that creates concise session summaries."},
                        {"role": "user", "content": summary_prompt}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.3
                },
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            summary = data["choices"][0]["message"]["content"]

            self._log(f"[SUMMARY] Generated rich summary ({len(summary)} chars)")
            return summary

        except Exception as e:
            self._log(f"[WARNING] Failed to generate summary: {e}")
            # Fallback: criar summary básico
            return f"""## Session Context
Working session interrupted at {self.total_prompt_tokens}/{self.context_limit} tokens.

## Current State
{self.call_count} interactions completed.

## Next Actions
1. Continue from last message
"""

    def _auto_checkpoint(self):
        """
        Salva estado atual e reinicia sessão (limpa histórico)

        Similar ao /end do Claude, mas automático
        Agora com rich summary para handoff de qualidade
        """
        self._log(f"[CHECKPOINT] Auto-checkpoint triggered at {self.total_prompt_tokens}/{self.context_limit} tokens")

        # Gerar rich summary ANTES de salvar
        rich_summary = self._generate_rich_summary()

        # Salvar checkpoint completo com rich summary
        checkpoint_content = f"""## Checkpoint: {self.session_id}
**Timestamp**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Reason**: Context limit approaching ({self.total_prompt_tokens}/{self.context_limit} tokens)

**Metrics**:
- Calls: {self.call_count}
- Prompt tokens: {self.total_prompt_tokens}
- Completion tokens: {self.total_completion_tokens}
- Total tokens: {self.total_prompt_tokens + self.total_completion_tokens}

### Session Summary (Rich)

{rich_summary}

### Last Messages (Raw)
{self._format_last_messages(3)}

---
"""

        # Append ao log diário
        today = datetime.datetime.now().strftime("%Y.%m.%d")
        log_file = self.LOGS_DIR / f"{today}.md"

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(checkpoint_content)

        # Resetar estado COMPLETAMENTE
        self.messages = []  # Limpar histórico
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.call_count = 0

        # Injetar rich summary como system message para próxima sessão
        self.session_summary = rich_summary
        self.messages = [
            {
                "role": "system",
                "content": f"""# Previous Session Context

{rich_summary}

---

You are continuing work from the previous session. The context above summarizes what was being done. Continue seamlessly from where you left off.
"""
            }
        ]

        # Novo ID de sessão
        old_id = self.session_id
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        self._log(f"[OK] Checkpoint saved | New session: {self.session_id} (previous: {old_id})")

    def _format_last_messages(self, n: int = 3) -> str:
        """Formata últimas N trocas de mensagens"""
        last = self.messages[-(n*2):]
        formatted = []
        for msg in last:
            role = msg["role"].upper()
            content = msg["content"][:200]  # Primeiros 200 chars
            if len(msg["content"]) > 200:
                content += "..."
            formatted.append(f"**{role}**: {content}")
        return "\n".join(formatted)

    def _get_configured_context_limit(self) -> int:
        """
        Consulta o limite de contexto configurado no LMStudio via CLI

        Usa `lms ps --json` para pegar o contextLength REAL configurado pelo usuário
        """
        import subprocess

        try:
            result = subprocess.run(
                [self.LMS_CLI, "ps", "--json"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                models = json.loads(result.stdout)

                # Procurar pelo modelo atual
                for model_info in models:
                    if model_info.get("modelKey") == self.model or model_info.get("identifier") == self.model:
                        context_limit = model_info.get("contextLength")

                        if context_limit:
                            print(f"[LMStudio] Detected context limit: {context_limit} tokens (configured in LMStudio)")
                            return context_limit

                # Se não encontrou o modelo específico, pegar o primeiro carregado
                if models:
                    context_limit = models[0].get("contextLength", 55000)
                    print(f"[LMStudio] Using context limit from first loaded model: {context_limit} tokens")
                    return context_limit

        except Exception as e:
            print(f"[LMStudio] Warning: Could not query context limit via CLI: {e}")

        # Fallback: usar limite conservador
        fallback = 55000
        print(f"[LMStudio] Using fallback context limit: {fallback} tokens")
        return fallback

    def _log(self, message: str):
        """Log interno (console + arquivo)"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [LMStudio] {message}")

    def get_metrics(self) -> Dict:
        """Retorna métricas da sessão atual"""
        usage_pct = (self.total_prompt_tokens / self.context_limit) * 100

        return {
            "session_id": self.session_id,
            "model": self.model,
            "calls": self.call_count,
            "tokens": {
                "prompt": self.total_prompt_tokens,
                "completion": self.total_completion_tokens,
                "total": self.total_prompt_tokens + self.total_completion_tokens
            },
            "context": {
                "limit": self.context_limit,
                "used": self.total_prompt_tokens,
                "remaining": self.context_limit - self.total_prompt_tokens,
                "percentage": round(usage_pct, 1)
            },
            "status": self._get_status(usage_pct)
        }

    def _get_status(self, usage_pct: float) -> str:
        """Retorna status baseado em uso de contexto"""
        if usage_pct >= 85:
            return "CRITICAL - checkpoint imminent"
        elif usage_pct >= 75:
            return "WARNING - approaching limit"
        elif usage_pct >= 50:
            return "MODERATE - half capacity"
        else:
            return "OK"

    def manual_checkpoint(self, reason: str = "Manual checkpoint"):
        """Checkpoint manual (pode ser chamado pelo usuário)"""
        self._log(f"[MANUAL] Manual checkpoint: {reason}")
        self._auto_checkpoint()


# Helper function para uso direto
def ask_lmstudio(prompt: str, system: str = None, max_tokens: int = 2048) -> Tuple[str, Dict]:
    """
    Helper simplificado para chamadas únicas

    Para sessões longas, use a classe LMStudioSession diretamente
    """
    session = LMStudioSession()
    response, metrics = session.chat(prompt, system=system, max_tokens=max_tokens)
    return response, metrics


if __name__ == "__main__":
    # Teste
    print("=== LMStudio Session Manager Test ===\n")

    session = LMStudioSession()

    response, metrics = session.chat(
        "Explique em 2 frases o que é Python.",
        system="Você é um assistente técnico conciso."
    )

    print(f"\n[Response]:\n{response}\n")
    print(f"[Metrics]:\n{json.dumps(metrics, indent=2)}\n")
    print(f"[Session Status]:\n{json.dumps(session.get_metrics(), indent=2)}")
