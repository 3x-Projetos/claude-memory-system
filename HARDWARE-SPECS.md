# Hardware Specifications - Machine Profile

**Última atualização**: 2025-11-16
**Máquina**: Desktop Principal (luisr)

---

## Summary

Esta máquina possui configuração **muito capaz** para rodar LLMs locais:
- CPU top-tier com cache massivo (ideal para inferência)
- 96GB RAM (permite modelos grandes na CPU)
- GPU NVIDIA RTX 3090 24GB (permite modelos até ~70B quantizados)

---

## Detailed Specifications

### CPU
```
Modelo: AMD Ryzen 7 9800X3D 8-Core Processor
Cores: 8 físicos / 8 lógicos
Clock: 4.7 GHz (max)
Arquitetura: Zen 5 (3D V-Cache)
```

**Características relevantes para LLMs**:
- **3D V-Cache**: 96MB cache L3 (excelente para inferência)
- **Single-thread performance**: Top 1% (importante para autoregressive generation)
- **8 cores**: Suficiente para batch processing e multi-tasking

### RAM
```
Capacidade: 96 GB (2x 48GB)
Tipo: DDR5
Velocidade: 5200 MHz
```

**Características relevantes para LLMs**:
- **96GB total**: Permite rodar modelos até ~70B na CPU (quantizados Q4)
- **DDR5 5200MHz**: Bandwidth excelente (~83 GB/s)
- **Dual-channel**: Otimizado para throughput

### GPU
```
Modelo: NVIDIA GeForce RTX 3090
VRAM: 24 GB GDDR6X
Driver: 581.80
Compute Capability: 8.6 (Ampere)
```

**Características relevantes para LLMs**:
- **24GB VRAM**: Permite modelos até ~70B (Q4_K_M) ou ~34B (FP16)
- **Compute 8.6**: Suporta CUDA, cuDNN, TensorRT
- **Memory bandwidth**: ~936 GB/s (excelente para inferência)
- **FP16 support**: Tensor cores para aceleração

**Limitações conhecidas**:
- Não suporta FP8 nativo (apenas Ada Lovelace/4000 series)
- PCIe 4.0 (vs 5.0 em GPUs mais novas, mas não crítico para LLMs)

---

## Performance Estimates (LLMs Locais)

### CPU Inference (usando llama.cpp)

| Model Size | Quantization | Estimated Speed | RAM Usage | Viável? |
|------------|--------------|-----------------|-----------|---------|
| 3B params  | Q4_K_M       | ~80-100 tok/s   | ~2-3 GB   | ✅ Excelente |
| 7B params  | Q4_K_M       | ~40-60 tok/s    | ~4-6 GB   | ✅ Excelente |
| 13B params | Q4_K_M       | ~20-30 tok/s    | ~8-10 GB  | ✅ Muito bom |
| 34B params | Q4_K_M       | ~8-12 tok/s     | ~20-25 GB | ✅ Bom |
| 70B params | Q4_K_M       | ~3-5 tok/s      | ~40-50 GB | ⚠️ Usável (lento) |

### GPU Inference (usando llama.cpp + CUDA)

| Model Size | Quantization | Estimated Speed | VRAM Usage | Viável? |
|------------|--------------|-----------------|------------|---------|
| 3B params  | Q4_K_M       | ~150-200 tok/s  | ~2-3 GB    | ✅ Excelente |
| 7B params  | Q4_K_M       | ~80-120 tok/s   | ~4-6 GB    | ✅ Excelente |
| 7B params  | FP16         | ~60-80 tok/s    | ~14 GB     | ✅ Excelente |
| 13B params | Q4_K_M       | ~50-70 tok/s    | ~8-10 GB   | ✅ Excelente |
| 34B params | Q4_K_M       | ~20-30 tok/s    | ~20-22 GB  | ✅ Muito bom |
| 70B params | Q4_K_M       | ~8-12 tok/s     | ~40-45 GB  | ❌ VRAM insuficiente |
| 70B params | Q2_K         | ~10-15 tok/s    | ~22-24 GB  | ⚠️ Usável (qualidade degradada) |

**Notas**:
- Speeds são estimativas baseadas em benchmarks de hardware similar
- tok/s = tokens por segundo (geração)
- CPU + GPU offloading pode combinar melhor dos dois mundos para modelos >24GB

---

## Recomendações de Modelos por Use Case

### Uso Geral (Assistente, Chat)
**GPU (Recomendado)**:
- **Qwen2.5-7B-Instruct** (Q4_K_M): ~80 tok/s, excelente reasoning
- **Llama-3.2-8B-Instruct** (Q4_K_M): ~70 tok/s, muito responsivo
- **Mistral-7B-v0.3** (FP16): ~60 tok/s, qualidade máxima

**CPU (Fallback)**:
- **Qwen2.5-7B-Instruct** (Q4_K_M): ~50 tok/s, ainda responsivo
- **Llama-3.2-3B** (Q4_K_M): ~90 tok/s, muito rápido

### DEV - Code Generation
**GPU (Recomendado)**:
- **DeepSeek-Coder-33B-Instruct** (Q4_K_M): ~25 tok/s, qualidade excelente
- **Qwen2.5-Coder-14B** (Q4_K_M): ~40 tok/s, 92 linguagens
- **CodeLlama-13B-Instruct** (Q4_K_M): ~55 tok/s, balanceado

**CPU (Tarefas simples)**:
- **DeepSeek-Coder-6.7B** (Q4_K_M): ~45 tok/s, bom para snippets
- **CodeLlama-7B-Python** (Q4_K_M): ~50 tok/s, especializado Python

### Sub-Agents Especializados (Bulk Processing)
**GPU (Preferencial)**:
- **Llama-3.2-3B** (Q4_K_M): ~150 tok/s, rápido para tasks simples
- **Qwen2.5-7B** (Q4_K_M): ~80 tok/s, quando precisa qualidade

**CPU (Multi-instância possível)**:
- **Llama-3.2-1B** (Q4_K_M): ~200+ tok/s, extremamente rápido
- **Phi-3.5-mini-3.8B** (Q4_K_M): ~80 tok/s, Microsoft, bom reasoning

### Especialização Futura (Fine-tuning)
**Base models recomendados**:
- **Finance**: Llama-3.2-8B (fine-tune com dados financeiros)
- **Health**: Llama-3.2-8B ou Meditron-7B (já fine-tuned para medicina)
- **Infra/DevOps**: Qwen2.5-7B (excelente em seguir instruções)

---

## LM Studio Configuration

### Recomendações Iniciais

**GPU Acceleration**:
```yaml
Modelo: CUDA (NVIDIA)
GPU Layers: auto (ou manual: 99 para carregar tudo na GPU)
Context Length: 4096-8192 (balanço qualidade/velocidade)
Batch Size: 512 (padrão)
Threads: 8 (= cores CPU para CPU fallback)
```

**Para modelos 7B-13B**:
- GPU Layers: 99 (tudo na GPU)
- Context: 8192
- Esperado: ~80-120 tok/s

**Para modelos 33B-34B**:
- GPU Layers: auto (LM Studio decide offloading)
- Context: 4096 (economizar VRAM)
- Esperado: ~20-30 tok/s

### Multi-Model Strategy
Com 24GB VRAM, possível rodar:
- **Cenário 1**: 1x 34B (ocupa ~22GB) - máxima qualidade
- **Cenário 2**: 1x 13B (~10GB) + 1x 7B (~6GB) - multi-agente simultâneo
- **Cenário 3**: 2x 7B (~12GB total) - redundância ou especialização

**Recomendação inicial**: Cenário 1 (1x 34B para DEV Agent) + CPU para sub-agents leves

---

## Benchmarking Checklist (Próxima Sessão)

Ao testar modelos pela primeira vez, registrar:

- [ ] **Modelo**: Nome + quantização
- [ ] **Device**: CPU ou GPU
- [ ] **Speed**: Tokens/segundo (geração)
- [ ] **Latency**: Tempo para primeiro token (ms)
- [ ] **Context**: Max context testado
- [ ] **Quality**: Avaliação subjetiva (1-5 estrelas)
- [ ] **Use case**: Para qual tarefa é adequado
- [ ] **Issues**: Problemas encontrados (alucinações, erros, etc)

### Template de Benchmark
```markdown
## [Modelo] - [Quantização]

**Hardware**: GPU / CPU
**Speed**: X tok/s
**First token latency**: Xms
**Context tested**: X tokens
**Quality**: ⭐⭐⭐⭐☆ (4/5)
**Best for**: [Use case]
**Issues**: [Nenhum / descrição]
**Notes**: [Observações adicionais]
```

---

## Multi-Machine Architecture (Futuro)

### Possibilidades
Com múltiplas máquinas disponíveis:

**Arquitetura distribuída**:
```
┌─────────────────┐
│ Machine 1 (esta)│  ← Orchestrator + DEV Agents
│ RTX 3090 24GB   │
└────────┬────────┘
         │
    ┌────┴─────┬──────────┐
    │          │          │
┌───▼───┐  ┌───▼───┐  ┌───▼───┐
│Machine│  │Machine│  │Machine│
│   2   │  │   3   │  │   4   │
└───────┘  └───────┘  └───────┘
Finance    Health     Infra
Agent      Agent      Agent
```

**Benefícios**:
- Isolamento de recursos (agents não competem)
- Especialização por máquina
- Redundância (fallback se uma máquina offline)

**Implementação**:
- LM Studio rodando em cada máquina (portas diferentes)
- MCP server aponta para IPs locais (ex: `192.168.1.x:1234`)
- Routing considera disponibilidade de máquina

**Fase**: 4-5 (após validar single-machine)

---

## Limitações & Trade-offs

### Dispersão de Precisão (Modelos Locais)
Conforme observado pelo usuário:
- **Qualidade varia**: Mesmo modelo pode ter respostas inconsistentes
- **Alucinações**: Mais frequentes que Claude/GPT (especialmente modelos <13B)
- **Veracidade**: Difícil validar sem ground truth

**Mitigações planejadas**:
1. **Routing conservador**: Dúvida → Claude (comercial)
2. **Validation layer**: Respostas críticas passam por validação Claude
3. **Benchmarking contínuo**: Registrar qualidade ao longo do tempo
4. **Fine-tuning**: Melhorar domínios específicos com dados curados
5. **Ensemble**: Múltiplos modelos respondem, Claude sintetiza

### Hardware-Specific
- **VRAM limitada**: Modelos >34B precisam quantização agressiva (Q2/Q3)
- **Latência CPU**: Modelos >13B ficam lentos na CPU
- **Power consumption**: GPU em uso contínuo (considerar custo energia)

---

## Próximos Passos (Benchmark Inicial)

### Fase 0 - Validação de Hardware
1. [ ] Testar LM Studio API está rodando (`curl localhost:1234/v1/models`)
2. [ ] Benchmark 1 modelo 7B (GPU): medir tok/s, latência, qualidade
3. [ ] Benchmark 1 modelo 7B (CPU): comparar com GPU
4. [ ] Benchmark 1 modelo 33B (GPU): validar viabilidade para DEV Agent
5. [ ] Documentar resultados neste arquivo

### Template de Registro
Adicionar seção "Benchmark Results" abaixo com resultados reais.

---

## Benchmark Results

*Será preenchido na próxima sessão com testes reais*

### [Modelo 1]
...

### [Modelo 2]
...

---

*Este documento é referência técnica para decisões de modelo selection e deployment.*
