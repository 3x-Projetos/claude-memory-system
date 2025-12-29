# Agent Model Detection - Guia Técnico

**Propósito**: Documentar como cada agente detecta automaticamente o modelo sendo usado.

---

## Princípio Fundamental

**Auto-detecção primeiro, pergunta apenas se falhar.**

Cada agente deve:
1. **Tentar** detectar automaticamente o modelo usado
2. **Registrar** no log sem perguntar ao usuário (se conseguir)
3. **Perguntar** ao usuário apenas como último recurso

---

## Claude (Claude CLI)

### Auto-Detecção: ✅ Sempre Possível

**Como funciona**:
- Modelo aparece no início de toda conversa
- Exemplo: "You are powered by the model named Sonnet 4.5. The exact model ID is claude-sonnet-4-5-20250929."
- Claude sempre sabe qual modelo está usando

**Modelos disponíveis** (Claude CLI):
- **Sonnet 4.5** (`claude-sonnet-4-5-20250929`) - Padrão, melhor custo/benefício
- **Opus** (`claude-opus-...`) - Máxima qualidade, mais caro
- **Haiku** (`claude-haiku-...`) - Rápido e barato, tarefas simples

**Token Budget**: 200.000 tokens (todos os modelos)

**Custo relativo**:
- Haiku: $ (mais barato, ~20x mais rápido que Sonnet)
- Sonnet: $$$ (balanceado)
- Opus: $$$$ (mais caro, máxima qualidade)

**Registro no log**:
```markdown
**Agente**: Claude
**Modelo**: Sonnet 4.5 (claude-sonnet-4-5-20250929)
```

**Nunca perguntar ao usuário** - sempre auto-detectar.

---

## Gemini (Google AI Studio / API)

### Auto-Detecção: ⚠️ Depende

**Cenário 1: Via API**:
- Ler variável de ambiente `GEMINI_MODEL`
- Ou ler de config file
- Auto-detecção possível ✅

**Cenário 2: Via Interface Web**:
- Tentar detectar do contexto (se disponível)
- **Fallback**: perguntar ao usuário

**Modelos disponíveis**:
- **Gemini 2.0 Flash** - Mais rápido, 1M tokens context
- **Gemini 1.5 Pro** - Balanceado, 2M tokens context
- **Gemini 1.5 Flash** - Rápido, 1M tokens context

**Token Budget**: 1M-2M tokens (muito maior que Claude)

**Custo relativo**:
- Flash: $ (mais barato, muito rápido)
- Pro: $$ (balanceado, contexto máximo)

**Registro no log**:
```markdown
**Agente**: Gemini
**Modelo**: Gemini 1.5 Pro
```

---

## Local LLMs (LM Studio)

### Auto-Detecção: ✅ Geralmente Possível

**Como funciona**:
- Ler arquivo de config do LM Studio
- Path: `~/.lmstudio/settings.json` ou similar
- Campo: `activeModel` ou equivalente

**Fallback**:
- Se config não acessível, perguntar ao usuário

**Modelos comuns**:
- **DeepSeek-Coder 33B Q4** - Code-specific, 16k context
- **Qwen2.5 7B/14B/32B** - General purpose, multilingual
- **Llama 3.2 3B/8B** - Rápido, menor contexto
- **Mistral/Mixtral** - Balanceado

**Context Limit**: 4k-128k tokens (varia por modelo)

**Custo**: $0 (rodando localmente)

**Performance**: Medida em tok/s (depende de GPU/CPU)
- GPU (RTX 3090): 25-150 tok/s (dependendo do modelo)
- CPU (Ryzen 9800X3D): 5-30 tok/s

**Registro no log**:
```markdown
**Agente**: Local
**Modelo**: DeepSeek-Coder 33B Q4_K_M
```

---

## GPT-4 / ChatGPT (OpenAI API)

### Auto-Detecção: ⚠️ Depende

**Via API**:
- Ler variável de ambiente `OPENAI_MODEL`
- Ou ler request parameters
- Auto-detecção possível ✅

**Via Interface**:
- Tentar detectar (se disponível no prompt)
- **Fallback**: perguntar ao usuário

**Modelos disponíveis**:
- **GPT-4 Turbo** - 128k context
- **GPT-4** - 8k context
- **GPT-3.5 Turbo** - Rápido, barato

**Token Budget**: 8k-128k tokens

**Custo relativo**:
- GPT-3.5: $ (barato)
- GPT-4 Turbo: $$$ (caro)
- GPT-4: $$$$ (muito caro)

**Registro no log**:
```markdown
**Agente**: OpenAI
**Modelo**: GPT-4 Turbo
```

---

## Workflow no `/end`

### Passo 1: Tentar Auto-Detectar

```python
def detect_model():
    """Cada agente implementa sua própria detecção"""

    # Claude
    if agent == "Claude":
        # Sempre conhecido - ler do início da conversa
        return "Sonnet 4.5 (claude-sonnet-4-5-20250929)"

    # Gemini
    elif agent == "Gemini":
        model = os.getenv("GEMINI_MODEL")
        if model:
            return model
        else:
            return None  # Fallback para pergunta

    # Local LLM
    elif agent == "Local":
        config = read_lmstudio_config()
        if config and "activeModel" in config:
            return config["activeModel"]
        else:
            return None  # Fallback para pergunta

    # Outros
    else:
        return None  # Perguntar ao usuário
```

### Passo 2: Fallback (só se auto-detecção falhar)

```markdown
Não foi possível detectar o modelo automaticamente.

Qual modelo você usou nesta sessão?

Opções comuns:
1. Claude Sonnet 4.5
2. Claude Opus
3. Claude Haiku
4. Gemini 1.5 Pro
5. Gemini 2.0 Flash
6. Local LLM (especificar)
7. Outro (especificar)

[Escolha 1-7 ou digite o nome do modelo]
```

---

## Benefícios da Auto-Detecção

1. **Zero Friction**: Usuário não precisa lembrar qual modelo usou
2. **Precisão**: Elimina erro humano (esquecer ou confundir modelos)
3. **Automação**: Logs sempre completos e consistentes
4. **Comparabilidade**: Dados precisos para análise multi-modelo

---

## Métricas por Modelo

### Claude Sonnet 4.5 (esta sessão)
- Budget: 200k tokens
- Usados: ~115k tokens (57.5%)
- Custo: $$$ (médio-alto)
- Performance: Excelente para arquitetura/planejamento

### Exemplo Comparativo (futuro)

**Tarefa: Refactoring simples**
- Haiku: 10k tokens, 30s, $ → ⭐ Melhor escolha
- Sonnet: 15k tokens, 60s, $$$ → Overkill
- Opus: 20k tokens, 120s, $$$$ → Desperdício

**Tarefa: Arquitetura complexa**
- Haiku: 80k tokens, 5min, $ → Qualidade inferior
- Sonnet: 105k tokens, 10min, $$$ → ⭐ Melhor escolha
- Opus: 90k tokens, 20min, $$$$ → Melhor qualidade, custo alto

---

*Framework Model-Agnostic v2.1+*
*Multi-Agent Support - M009 (em desenvolvimento)*
