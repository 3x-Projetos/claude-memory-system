# Performance Tracking System (M009)

**Propósito**: Metrificar e comparar performance de diferentes agentes e modelos para decisões data-driven sobre qual usar em cada contexto.

---

## Estrutura

```
.claude/performance/
├── README.md                          # Este arquivo
├── TEMPLATE-performance-profile.md    # Template para novos profiles
├── profiles/
│   ├── claude-sonnet-4.5.md          # Profile por modelo
│   ├── claude-haiku.md
│   ├── gemini-1.5-pro.md
│   ├── deepseek-coder-33b.md
│   └── ...
├── comparisons/
│   └── 2025.11.md                    # Análises comparativas mensais
└── context-analysis/
    └── prompt-optimization.md         # Insights de otimização de prompts
```

---

## Métricas Coletadas

### Quantitativas (Automáticas)
- **Tokens/session**: Média, mediana, P95
- **Context window usage**: % utilizado da janela disponível
- **Prompt length distribution**: Histograma de tamanhos de prompt
- **Output/Input ratio**: Eficiência de geração
- **Latency**: Tempo médio de resposta (quando aplicável)
- **Cost**: Custo relativo ($ to $$$$)
- **Efficiency**: Tokens economizados com framework vs sem
- **Volume**: Linhas de código, arquivos modificados
- **Context limit hits**: Quantas vezes atingiu limite de contexto

### Qualitativas (Inferidas + Opcionalmente Perguntadas)
- **Task type**: Architecture, Code Gen, Refactoring, Debugging, Docs, Research
- **Specialization**: Tecnologias específicas (Python, JS, Rust, etc)
- **Quality rating**: 1-5 stars (usuário opcionalmente avalia)
- **Success rate**: Completou tarefa? (yes/partial/no)
- **Pattern detection**: Padrões de uso cross-domain
- **Context efficiency**: Qualidade vs tamanho de contexto usado

### Context Window Metrics (Foco Principal)
- **Window utilization**: % médio, peak, frequency of hitting limits
- **Prompt optimization**: Optimal prompt length range (correlação com qualidade)
- **Context quality correlation**: Sweet spot identification
- **Model-specific patterns**: Como cada modelo usa sua janela
- **Framework efficiency**: ROI da hierarquia de memória

---

## Workflow de Coleta

### Durante `/end`

**Passo 4: Coletar Performance Metrics**

1. **Auto-detectar** (zero friction):
   - Modelo usado (já implementado em Passo 1)
   - Tokens: budget, usados, % utilizado
   - Duration: inferir de session timestamps
   - Files: git diff --stat
   - Technologies: file extensions + imports
   - Task type: arquivos modificados + comandos
   - Project: rastreado em M008

2. **Perguntar (opcional - pulável)**:
   ```
   📊 Avaliação de Performance (Enter para pular):

   1. Qualidade: ⭐ [1-5, Enter=auto]
   2. Completou? [yes/partial/no, Enter=yes]
   3. Categoria: [architecture/code/etc, Enter=auto]
   ```

3. **Registrar**:
   - Se profile não existe: criar de template
   - Append session entry
   - Update stats agregados

4. **No log diário**: Incluir seção "Performance Metrics"

---

## Análise e Insights

### Mensal (via `/aggregate month`)
- Re-calcular stats agregados de cada profile
- Gerar análise comparativa (comparisons/YYYY.MM.md)
- Identificar sweet spots de contexto por task type
- Atualizar context optimization insights

### Insights Gerados

**Context Optimization** (exemplo):
```
📊 Descoberta: Tarefas de architecture têm qualidade 4.8/5
quando contexto usado é 50-70%, mas cai para 4.1/5 quando >85%.

Recomendação: Carregar contexto rico mas evitar overload.
Framework atual: Excelente (sweet spot 40-60%).
```

**Model Selection** (exemplo):
```
💡 Sugestão: Tarefa detectada como "refactor simples".
Sonnet pode ser overkill.

Considere Haiku:
- 20x mais rápido
- 75% mais barato
- Qualidade suficiente para refactors simples (4.2/5 histórico)
```

---

## Benefícios Esperados

1. **Economia de tokens**: Escolher modelo right-sized
2. **Melhor qualidade**: Usar modelo especializado quando importa
3. **Prompt optimization**: Identificar comprimento ótimo
4. **Context efficiency**: Saber quando mais contexto ajuda vs atrapalha
5. **Comparative analysis**: Data para decidir qual modelo usar
6. **Continuous improvement**: Tracking de tendências
7. **ROI do framework**: Quantificar benefício da hierarquia
8. **Multi-agent orchestration**: Dados para routing inteligente (futuro)

---

## Fases de Implementação

### ✅ Fase 1 (Imediato)
- Estrutura de diretórios criada
- Template de profile criado
- Coleta integrada no `/end`
- Auto-detection implementada
- Perguntas opcionais adicionadas

### 📋 Fase 2 (Após 2-3 semanas)
- Análise comparativa mensal
- Script de agregação
- Identificar sweet spots de contexto
- Gerar comparisons/YYYY.MM.md

### 📋 Fase 3 (Após 1-2 meses)
- Recomendações automáticas no `/end`
- Sugestões de modelo alternativo
- Alertas de context overload

### 📋 Fase 4 (Futuro)
- Multi-agent routing automático
- Sistema escolhe modelo baseado em task + histórico
- Hybrid approach: Claude (architecture) + DeepSeek (code) + Gemini (research)

---

## Princípios

1. **Auto-detection first**: Minimizar friction (perguntas opcionais)
2. **Continuous collection**: Dados coletados a cada sessão
3. **Model-agnostic**: Funciona com qualquer agente/modelo
4. **Data-driven**: Decisões baseadas em dados reais, não empíricos
5. **Context-aware**: Foco especial em otimização de janela de contexto
6. **Privacy**: Todos os dados ficam locais (não compartilhados)

---

## Como Usar

### Para o Usuário
1. Continue usando `/end` normalmente
2. (Opcional) Responda perguntas de qualidade se quiser
3. Sistema coleta dados automaticamente
4. Use `/aggregate month` mensalmente para análises

### Para Claude (Agente)
1. Ao executar `/end`, siga Passo 4 (Coletar Performance Metrics)
2. Auto-detecte tudo que puder
3. Pergunte qualidade/success apenas se usuário quiser dados precisos
4. Registre no profile do modelo
5. Inclua Performance Metrics no log diário
6. Ao executar `/aggregate month`, analise profiles e gere insights

---

## Notas

- **Context window metrics** foram adicionados por solicitação explícita do usuário
- Sistema combina métricas de contexto com qualidade/custo para insights poderosos
- Permite otimizar prompts baseado em dados reais de uso
- Framework de memória hierárquica já economiza tokens - agora medimos quanto

---

*Parte do M009: Agent Performance Tracking & Context Window Metrics*
*Sistema de Memória Hierárquica v2.1+*
*Estabelecido: 2025-11-16*
