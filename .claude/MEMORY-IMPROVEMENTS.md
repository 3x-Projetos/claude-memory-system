# Memory System - Suggested Improvements

**Versão**: 1.0
**Data**: 2025-11-16
**Propósito**: Tracking de oportunidades de melhoria identificadas no sistema de memória e workflows

---

## Como Usar Este Documento

**Claude**: Sempre que notar oportunidade de melhoria durante sessões, adicione entrada aqui.

**Estrutura de cada entrada**:
```markdown
## [ID] - Nome da Melhoria
**Tipo**: Quick Win / Implementação Grande
**Impacto**: Alto / Médio / Baixo
**Esforço**: 1h / 1 dia / 1 semana / etc
**Status**: 🔵 Proposta / 🟡 Em Análise / 🟢 Implementada / ❌ Descartada
**Data proposta**: YYYY-MM-DD

**Descrição**: [O que fazer]
**Motivação**: [Por que fazer - dados, observações, padrões]
**Benefícios esperados**: [Lista]
**Riscos/Trade-offs**: [Lista]
**Notas de implementação**: [Dicas técnicas]
```

---

## Princípios do Sistema de Memória

**Estabelecidos durante planejamento (2025-11-16)**:

1. **Cross-Domain First**: Sistema deve FACILITAR trabalho cross-domain (ponto forte do usuário)
   - Memória isolada por agente MAS com shared learnings layer
   - Insights cross-domain capturados e acessíveis globalmente
   - Augmentation de capacidade cross-domain via agentes

2. **Distributed Storage**: Arquitetura client-server para multi-máquina
   - Memórias locais: cache, working memory, logs de device
   - Memórias remotas: global profile, shared learnings, agent contexts
   - Uma máquina atua como servidor central de memória

3. **Privacy & Control**: Dados sensíveis sempre sob controle do usuário
   - PII redaction para compartilhamento
   - Choice de o que fica local vs remoto
   - Encryption para dados remotos

---

## Melhorias Propostas

### [M008] - Project-Centric Memory Layer ⭐⭐⭐
**Tipo**: Implementação Média
**Impacto**: Alto (alinhado com working style do usuário)
**Esforço**: 2-3 horas
**Status**: 🟢 Implementada (2025-11-16)
**Data proposta**: 2025-11-16

**Descrição**:
Adicionar dimensão **project-centric** ao sistema de memória, além da dimensão temporal (time-centric) já existente.

**Problema identificado**:
- Sistema atual é unidimensional: time-centric (daily → weekly → monthly)
- Usuário trabalha em múltiplos projetos paralelamente (multi-project workflow natural)
- Dificulta organização project-centric, context switching, tracking de status por projeto
- Aumenta clutter mental (pendências misturadas entre projetos)

**Solução implementada**:
```
.projects/
├── [project-name]/
│   ├── .context.md       # Working memory do projeto
│   ├── .status.md        # Roadmap, decisões, métricas
│   └── history/          # Logs específicos (opcional)
```

**Categorias suportadas** (visão holística da vida):
- 💻 Code
- 🎨 Creative
- 🏗️ Physical
- 👤 Personal
- 🤝 Social/Community
- 💼 Business/Finance
- 🤖 AI/Research
- 🌐 Other

**Novos comandos**:
- `/projects` - Dashboard multi-projeto (agrupado por categoria)
- `/switch [name]` - Muda contexto para projeto específico
- `/project-status [name]` - Atualiza status/roadmap/decisões

**Comandos atualizados**:
- `/continue` - Agora pergunta qual projeto trabalhar
- `/new` - Agora permite escolher projeto ou criar novo
- `/end` - Agora registra "projects touched" e % tempo por projeto

**Benefícios alcançados**:
- ✅ Redução de clutter mental (tudo organizado por projeto)
- ✅ Context switching fluido (memória específica por projeto)
- ✅ Tracking de status claro (COMPLETE/IMPLEMENTING/PLANNING/PAUSED/BLOCKED)
- ✅ Visão holística (não apenas código - todos os aspectos da vida)
- ✅ Dashboard consolidado (ver todos os projetos de uma vez)
- ✅ Augmentation real (sistema se adapta ao workflow multi-projeto)

**Riscos/Trade-offs**:
- Adiciona complexidade ao sistema (mais comandos, mais estrutura)
- Requer disciplina para manter atualizado (mitigado com prompts em /end)
- Pode fragmentar logs (mitigado com logs temporais mantidos)

**Notas de implementação**:
- Flat structure (`.projects/[name]/`) vs hierárquica (`.projects/code/[name]/`)
  - Escolhido flat + categorização via campo "**Category**" em .context.md
  - Mais flexível (projetos podem ter múltiplas categorias)
- Templates em `.projects/README.md` para facilitar criação de novos projetos
- `.session-state.md` atualizado com seção "Active Projects"
- Campo "Last Touched" atualizado automaticamente pelo `/end`

**Filosofia - Simbiose**:
Sistema deve se adaptar ao modo natural do usuário trabalhar (multi-projeto, context switching orgânico), não forçar adaptação a estrutura rígida. Isso é **augmentation vs automation** (HAI Index).

---

### [M001] - Agent Memory + Cross-Domain Insights Layer
**Tipo**: Implementação Grande
**Impacto**: Alto
**Esforço**: 1-2 dias
**Status**: 🔵 Proposta
**Data proposta**: 2025-11-16

**Descrição**:
Criar estrutura de memória com **dupla camada**:

**Layer 1 - Agent-Specific Memory** (isolada):
```
~/.claude-memory/agents/
  ├── dev/
  │   ├── context.md          # Contexto persistente (stack, projetos)
  │   ├── learnings.md        # Padrões específicos DEV
  │   └── history.jsonl       # Histórico de interações
  ├── finance/
  │   ├── context.md
  │   ├── learnings.md
  │   └── history.jsonl
  └── ...
```

**Layer 2 - Cross-Domain Insights** (compartilhada):
```
~/.claude-memory/
  ├── cross-domain-insights.md   # Insights que atravessam domínios
  ├── domain-connections.md      # Mapa de conexões entre domínios
  └── synthesis-patterns.md      # Padrões de síntese cross-domain
```

**Exemplo de cross-domain insight**:
```markdown
## Insight: Performance Optimization Pattern
**Domínios envolvidos**: DEV + FINANCE + AI
**Data identificada**: 2025-11-20

**Observação**:
Técnicas de otimização de performance em código (DEV) aplicam-se a:
- Portfolio backtesting (FINANCE): mesma lógica de vectorização
- Training loops ML (AI): mesma lógica de batching

**Aplicações**:
- DEV Agent: usa para code review de loops
- FINANCE Agent: sugere vectorizar cálculos financeiros
- AI Agent: sugere otimização de training pipelines

**Tags**: #performance #vectorization #cross-domain
```

**Motivação**:
- **Ponto forte do usuário**: trabalho cross-domain
- Sistema deve **augment** (não prejudicar) essa capacidade
- Agentes isolados podem perder conexões valiosas
- Insights cross-domain são os mais inovadores

**Benefícios esperados**:
- **Facilita cross-pollination** de ideias entre domínios
- Agentes podem sugerir aplicações cross-domain
- Usuário mantém visão holística (não fragmentada)
- Augmentation de capacidade cross-domain via AI

**Riscos/Trade-offs**:
- Complexidade de manutenção (duas camadas)
- Detectar automaticamente insights cross-domain (difícil)
- Pode crescer rápido (precisar compaction)

**Notas de implementação**:
- **Layer 1** (agent-specific): criada Fase 2 (primeiro domain agent)
- **Layer 2** (cross-domain): criada Fase 4 (quando >2 domínios ativos)
- Comando `/insight` para usuário marcar insight cross-domain manualmente
- Script semanal: analisa logs → sugere insights cross-domain (via Claude)
- Tags para facilitar busca cross-domain

---

### [M002] - Distributed Memory Architecture (Client-Server)
**Tipo**: Implementação Grande
**Impacto**: Alto
**Esforço**: 2-3 semanas
**Status**: 🔵 Proposta (Fase 5+)
**Data proposta**: 2025-11-16

**Descrição**:
Arquitetura de storage distribuído com uma máquina como servidor central:

```
┌─────────────────────────────────────────────────┐
│          Memory Server (Machine Central)        │
│                                                  │
│  Global Storage:                                 │
│  - Global user profile                          │
│  - Agent contexts (all domains)                 │
│  - Cross-domain insights                        │
│  - Shared learnings                             │
│  - Aggregated logs (weekly/monthly)             │
│                                                  │
│  API: REST (FastAPI) + Auth                     │
└────────────┬────────────────────────────────────┘
             │ LAN (HTTP/HTTPS)
    ┌────────┼──────────┬──────────┬──────────┐
    │        │          │          │          │
┌───▼────┐ ┌▼────┐  ┌───▼────┐ ┌───▼────┐ ┌───▼────┐
│Desktop │ │Laptop│ │Mobile  │ │Smart   │ │Machine │
│ (Main) │ │      │ │        │ │House   │ │  N     │
└────────┘ └──────┘ └────────┘ └────────┘ └────────┘
   Local      Local     Local      Local      Local
   Cache:     Cache:    Cache:     Cache:     Cache:
   - Session  - Session - Recent   - Voice    - Logs
   - Logs     - Logs    queries    contexts   - Temp
```

**Memória Local vs Remota**:

**Local (cada device)**:
- `.session-state.md` - working memory da sessão
- `logs/daily/` - logs detalhados do device
- Cache de contexto recente (últimas 3 sessões)
- Preferências de device (UI, shortcuts)

**Remota (servidor central)**:
- `~/.claude-memory/global-memory.md` - perfil global
- `~/.claude-memory/agents/` - todos os agent contexts
- `~/.claude-memory/cross-domain-insights.md`
- `logs/weekly/` e `logs/monthly/` - agregados
- Shared learnings entre devices

**Sincronização**:
- **Push**: Device → Server ao fim de cada sessão
- **Pull**: Server → Device ao iniciar sessão
- **Conflict resolution**: Server wins (versão canônica)
- **Offline mode**: Device usa cache local, sync quando reconectar

**Motivação**:
- Usuário tem múltiplas máquinas
- Assistente Pessoal deve funcionar cross-device
- Memória centralizada = única fonte de verdade
- Algumas máquinas podem especializar (ex: Machine 2 = Finance Server)

**Benefícios esperados**:
- Experiência contínua cross-device
- Backup automático (servidor central)
- Múltiplas máquinas podem rodar agentes especializados
- Compartilhamento de learnings entre devices

**Riscos/Trade-offs**:
- Complexidade técnica alta
- Requer servidor sempre disponível (ou fallback local)
- Latência de rede (LAN minimiza, mas existe)
- Security (autenticação, encryption)

**Notas de implementação**:
- **Fase 5+** (após sistema maduro single-machine)
- **Servidor**: FastAPI (Python) + SQLite ou PostgreSQL
- **Auth**: Token-based (JWT) apenas LAN
- **Encryption**: TLS para comunicação, dados at-rest opcional
- **API endpoints**:
  - `GET /memory/global` - pull global memory
  - `POST /memory/agent/{domain}` - push agent context
  - `GET /insights/cross-domain` - fetch cross-domain insights
  - `POST /session/sync` - sync session state
- **Fallback**: Se servidor offline, device usa cache local (read-only mode)
- **Escolha de servidor**: Machine mais potente ou always-on (desktop principal?)

---

### [M003] - Automatic Cross-Domain Pattern Detection
**Tipo**: Implementação Grande
**Impacto**: Alto (core feature para usuário)
**Esforço**: 1 semana
**Status**: 🔵 Proposta (Fase 4)
**Data proposta**: 2025-11-16

**Descrição**:
Sistema que automaticamente detecta padrões cross-domain:

**Funcionamento**:
1. Análise semanal de logs de todos os domínios
2. Claude/LLM identifica padrões, técnicas, insights repetidos
3. Detecta quando mesmo padrão aparece em domínios diferentes
4. Gera entrada em `cross-domain-insights.md`
5. Sugere aplicações em outros domínios

**Exemplo**:
```
Log DEV: "Implementado rate limiting para API"
Log HEALTH: "Criado rate limiting para exercícios (não sobrecarregar)"
Log FINANCE: "Limitado trades por dia (evitar overtrading)"

→ Pattern detectado: Rate Limiting
→ Domínios: DEV, HEALTH, FINANCE
→ Insight: "Rate limiting é pattern universal para evitar sobrecarga"
→ Sugestão: Aplicar em INFRA (network throttling)
```

**Motivação**:
- Usuário é forte em cross-domain, mas humanos têm limitações
- AI pode detectar padrões que passam despercebidos
- Augment capacidade cross-domain (não só replicar)
- Insights cross-domain são mais valiosos

**Benefícios esperados**:
- Descobrir conexões não-óbvias entre domínios
- Transferir learnings automaticamente
- Sugerir aplicações inovadoras
- Documentar pensamento cross-domain (meta-learning)

**Riscos/Trade-offs**:
- False positives (padrões que não são realmente cross-domain)
- Custo de LLM calls (análise semanal de logs)
- Pode gerar muitos insights (overflow)

**Notas de implementação**:
- Script semanal: `python .claude/detect-cross-domain-patterns.py`
- Usa Claude (ou modelo local grande) para análise
- Template de prompt estruturado (JSON output)
- Threshold de confiança (só adiciona se >80% confiança)
- Usuário pode revisar/aprovar antes de adicionar
- Tags automáticos para facilitar busca

---

### [M004] - Session Metrics Tracking
**Tipo**: Quick Win
**Impacto**: Médio
**Esforço**: 2-3 horas
**Status**: 🔵 Proposta
**Data proposta**: 2025-11-16

**Descrição**:
Adicionar seção de métricas quantitativas em logs diários:

```yaml
metrics:
  duration: 90min
  files_modified: 5
  lines_changed: +153/-40
  commits: 1
  tools_used: [Read, Edit, Write, Bash, WebSearch]
  domains_touched: [DEV, AI]  # Novo: tracking cross-domain
  ai_reliance: medium
  complexity: medium-high
  new_tech: ["Lazy Logging", "Windows SIGKILL"]
```

**Motivação**:
- Logs atuais são qualitativos (narrativa)
- Difícil agregar ou visualizar tendências
- Preparação para dashboard futuro
- **Tracking cross-domain work** (quantificar ponto forte)

**Benefícios esperados**:
- Dados para análise de produtividade
- Baseline para comparar melhorias
- Quantificar trabalho cross-domain (visibilidade)
- Input para auto-melhoria

**Riscos/Trade-offs**:
- Overhead manual (se não automatizado)
- Gamification (foco em quantidade vs qualidade)

**Notas de implementação**:
- Adicionar template YAML no comando `/end`
- Inferir métricas via git, file stats
- Campo `domains_touched` detecta cross-domain work
- Agregações incluem "% sessões cross-domain"

---

### [M005] - Hybrid System - Model Quality Benchmarking
**Tipo**: Implementação Grande
**Impacto**: Alto
**Esforço**: 1 semana (contínuo)
**Status**: 🟡 Em Análise (prioridade Fase 1-2)
**Data proposta**: 2025-11-16

**Descrição**:
Sistema de benchmark contínuo para avaliar qualidade de modelos locais:

**Estrutura**:
```
.claude/benchmarks/
  ├── test_queries.jsonl      # Query + expected output + domain
  ├── results/
  │   ├── 2025-11-16.json     # Resultados do dia
  │   └── ...
  └── analysis/
      └── quality_trends.md   # Análise temporal
```

**Categorias de teste**:
- Code generation (DEV)
- Reasoning (cross-domain)
- Factual recall (FINANCE, HEALTH)
- Creative (AI, design)
- **Cross-domain synthesis** (novo: principal foco)

**Motivação**:
- Modelos locais têm dispersão de precisão (confirmado)
- Decisões de routing dependem de conhecer qualidade real
- **Cross-domain tasks são críticos** (testar explicitamente)

**Benefícios esperados**:
- Dados objetivos para routing
- Detectar degradação de qualidade
- Comparar modelos (qual usar quando)
- Validar modelos para cross-domain work

**Riscos/Trade-offs**:
- Overhead de criação de ground truth
- Benchmarks podem não refletir uso real

**Notas de implementação**:
- Fase 1: Criar suite básica (30 queries, incluindo 10 cross-domain)
- Fase 2: Benchmark semanal automático
- Scoring: exact match, semantic similarity, Claude validation
- **Cross-domain scoring**: mede qualidade de síntese entre domínios

---

### [M006] - Memory Server - Smart Caching Strategy
**Tipo**: Quick Win (quando servidor implementado)
**Impacto**: Médio
**Esforço**: 1 dia
**Status**: 🔵 Proposta (Fase 5+)
**Data proposta**: 2025-11-16

**Descrição**:
Cache inteligente em cada device para minimizar latência:

**Estratégia**:
```python
# Cache local em cada device
cache_strategy = {
    "session_state": "always_local",  # Never remote
    "global_profile": "cache_7_days",  # Sync semanal
    "agent_contexts": "cache_recent",  # Apenas agents usados recentemente
    "cross_domain_insights": "cache_all",  # Crítico para usuário
    "daily_logs": "local_only",  # Não sincronizar (muito grande)
    "weekly_logs": "sync_on_demand",  # Pull quando necessário
}
```

**Cache invalidation**:
- TTL (time-to-live) por tipo de memória
- Invalidação explícita via API (quando servidor atualiza)
- Fallback: se cache expirado e servidor offline, usar stale cache

**Motivação**:
- Reduzir latência de network calls
- Funcionar offline (degraded mode)
- Cross-domain insights são frequentes (cache agressivo)

**Benefícios esperados**:
- Latência baixa mesmo com servidor remoto
- Offline capability
- Reduz carga no servidor

**Notas de implementação**:
- SQLite local como cache
- Headers HTTP (ETag, Last-Modified) para validação
- Metrics: cache hit rate (objetivo >80%)

---

### [M007] - Domain Connection Map (Visual)
**Tipo**: Quick Win
**Impacto**: Baixo-Médio
**Esforço**: 4-6 horas
**Status**: 🔵 Proposta (Fase 4+)
**Data proposta**: 2025-11-16

**Descrição**:
Visualização de conexões entre domínios:

```
     DEV ←→ AI
      ↓  ×  ↑
   FINANCE → HEALTH
      ↑      ↓
   INFRA ←←←←
```

**Estrutura**:
```markdown
## Domain Connections

### DEV ←→ AI
**Conexões identificadas**: 15
**Tópicos comuns**: ML pipelines, performance optimization, data processing
**Último insight**: 2025-11-18 (vectorização)

### FINANCE ←→ HEALTH
**Conexões identificadas**: 8
**Tópicos comuns**: tracking, goal setting, optimization
**Último insight**: 2025-11-15 (rate limiting)
```

**Motivação**:
- Visualizar força de conexões cross-domain
- Identificar domínios que ainda não se conectaram
- Oportunidades de inovação (conexões fracas)

**Benefícios esperados**:
- Insight sobre padrões de trabalho cross-domain
- Sugerir conexões não-exploradas
- Dashboard visual (futuro)

**Notas de implementação**:
- Gerado automaticamente a partir de `cross-domain-insights.md`
- Update mensal
- Exportar como Mermaid diagram (visualização)

---

### [M009] - Agent Performance Tracking & Context Window Metrics ⭐⭐⭐
**Tipo**: Implementação Média
**Impacto**: Alto (otimização multi-modelo + prompt engineering)
**Esforço**: 1-2 dias (inicial) + contínuo
**Status**: 🔵 Proposta
**Data proposta**: 2025-11-16

**Descrição**:
Sistema abrangente para metrificar e comparar performance de diferentes agentes e modelos, incluindo métricas de janela de contexto para otimização de prompts.

**Problema identificado**:
- Sem dados sobre o que cada modelo/agente faz bem
- Escolha de modelo é empírica (não data-driven)
- Desperdício de tokens/custo usando modelo errado para tarefa
- Janela de contexto não é otimizada (prompts podem ser muito longos/curtos)
- Não há baseline para comparar modelos

**Estrutura de dados**:
```
.claude/performance/
├── profiles/
│   ├── claude-sonnet-4.5.md       # Performance profile por modelo
│   ├── claude-haiku.md
│   ├── gemini-1.5-pro.md
│   ├── deepseek-coder-33b.md
│   └── ...
├── comparisons/
│   └── 2025.11.md                 # Análises comparativas mensais
└── context-analysis/
    └── prompt-optimization.md     # Insights de otimização de prompts
```

**Métricas Coletadas**:

**1. Quantitativas (Auto)**:
- **Tokens/session**: Média, mediana, P95
- **Context window usage**: % utilizado da janela disponível
- **Prompt length distribution**: Histograma de tamanhos de prompt
- **Output/Input ratio**: Eficiência de geração
- **Latency**: Tempo médio de resposta (quando aplicável)
- **Cost**: Custo relativo ($ to $$$$)
- **Efficiency**: Tokens economizados com framework vs sem
- **Volume**: Linhas de código, arquivos modificados
- **Context limit hits**: Quantas vezes atingiu limite de contexto

**2. Qualitativas (Inferidas + Perguntadas)**:
- **Task type**: Architecture, Code Gen, Refactoring, Debugging, Docs, Research
- **Specialization**: Tecnologias específicas (Python, JS, Rust, etc)
- **Quality rating**: 1-5 stars (usuário opcionalmente avalia)
- **Success rate**: Completou tarefa? (yes/partial/no)
- **Pattern detection**: Padrões de uso cross-domain
- **Context efficiency**: Qualidade vs tamanho de contexto usado

**3. Context Window Metrics** (NOVO):
- **Window utilization**:
  - % médio usado por sessão
  - Peak usage (máximo atingido)
  - Frequency of hitting limits
- **Prompt optimization**:
  - Optimal prompt length range (correlação com qualidade)
  - Verbose vs concise effectiveness
  - Context compression ratio (framework vs raw)
- **Context quality correlation**:
  - Qualidade output vs % contexto usado
  - Sweet spot identification (ex: 40-60% uso = melhor qualidade)
  - Diminishing returns threshold (quando mais contexto não melhora)
- **Model-specific patterns**:
  - Claude: 200k budget, padrões de uso
  - Gemini: 1-2M budget, padrões diferentes
  - Local LLMs: 4k-128k, como lida com limite
- **Framework efficiency**:
  - Token economy por tipo de memória (working vs long-term)
  - Agregações: economia semanal/mensal
  - ROI de hierarquia de memória

**Template de Performance Profile**:
```markdown
# Agent Performance: Claude Sonnet 4.5

**Model ID**: claude-sonnet-4-5-20250929
**Last Updated**: 2025-11-16

---

## Overall Stats
- **Sessions tracked**: 150
- **Success rate**: 94%
- **Avg quality**: 4.6/5 ⭐⭐⭐⭐⭐
- **Cost tier**: $$$ (médio-alto)

---

## Context Window Metrics

### Window Utilization
- **Budget**: 200,000 tokens
- **Avg usage**: 87,500 tokens (43.75%)
- **P95 usage**: 145,000 tokens (72.5%)
- **Peak usage**: 178,000 tokens (89%)
- **Limit hits**: 2/150 sessions (1.3%)

### Optimal Prompt Range
- **Sweet spot**: 40-65% context utilization
- **Quality by range**:
  - 0-25%: ⭐⭐⭐ (3.2/5) - Contexto insuficiente
  - 25-50%: ⭐⭐⭐⭐⭐ (4.8/5) - Optimal
  - 50-75%: ⭐⭐⭐⭐⭐ (4.7/5) - Muito bom
  - 75-90%: ⭐⭐⭐⭐ (4.1/5) - Começa degradar
  - 90-100%: ⭐⭐⭐ (3.5/5) - Context overload

### Framework Efficiency
- **Without framework**: ~180k avg tokens/session
- **With framework**: ~87k avg tokens/session
- **Economy**: 51.7% tokens saved
- **ROI**: Alta (framework paga custo de manutenção)

---

## Specializations (Auto-detected)

### Architecture & Planning ⭐⭐⭐⭐⭐
- **Sessions**: 45
- **Success rate**: 97%
- **Avg quality**: 4.8/5
- **Avg tokens**: 105k (52.5% usage)
- **Notes**: Excelente para design de sistemas complexos

### Code Generation ⭐⭐⭐⭐
- **Sessions**: 60
- **Success rate**: 92%
- **Avg quality**: 4.4/5
- **Avg tokens**: 75k (37.5% usage)
- **Notes**: Forte, mas não especializado (considerar DeepSeek-Coder)

### Documentation ⭐⭐⭐⭐⭐
- **Sessions**: 25
- **Success rate**: 98%
- **Avg quality**: 4.9/5
- **Avg tokens**: 65k (32.5% usage)
- **Notes**: Excelente clareza e estrutura

### Refactoring ⭐⭐⭐⭐
- **Sessions**: 15
- **Success rate**: 90%
- **Avg quality**: 4.3/5
- **Avg tokens**: 95k (47.5% usage)
- **Notes**: Bom, mas pode ser lento (considerar Haiku para simples)

### Research & Learning ⭐⭐⭐⭐⭐
- **Sessions**: 5
- **Success rate**: 100%
- **Avg quality**: 4.7/5
- **Avg tokens**: 120k (60% usage)
- **Notes**: Forte capacidade de síntese cross-domain

---

## By Technology

### Python ⭐⭐⭐⭐ (4.2/5)
- Sessions: 35
- Context avg: 80k tokens
- Best for: Architecture, APIs, data processing

### JavaScript/TypeScript ⭐⭐⭐⭐⭐ (4.7/5)
- Sessions: 40
- Context avg: 70k tokens
- Best for: Full-stack, React, Node.js

### Rust ⭐⭐⭐⭐ (4.0/5)
- Sessions: 10
- Context avg: 110k tokens
- Notes: Competente, mas pode precisar mais contexto

### Markdown/Docs ⭐⭐⭐⭐⭐ (4.9/5)
- Sessions: 25
- Context avg: 55k tokens
- Notes: Excelente clareza

---

## Comparative Performance

**vs Claude Haiku**:
- ✅ Better: Architecture (+35%), Complex reasoning (+50%)
- ❌ Worse: Speed (-60%), Cost (-75%)
- 📊 Context: Sonnet usa 2-3x mais tokens para mesma tarefa
- 🎯 Use Sonnet when: Complexidade alta, qualidade crítica
- 🎯 Use Haiku when: Tarefas simples, velocidade importa

**vs Claude Opus**:
- ✅ Better: Speed (+2x), Cost (+50%)
- ❌ Worse: Max quality (-10%), Edge cases (-15%)
- 📊 Context: Uso similar de tokens
- 🎯 Use Sonnet when: 90%+ dos casos (custo-benefício)
- 🎯 Use Opus when: Máxima qualidade crítica, budget ilimitado

**vs DeepSeek-Coder 33B**:
- ✅ Better: Generalization (+40%), Multi-language (+30%)
- ❌ Worse: Cost (API vs Local = ∞), Python specialization (-10%)
- 📊 Context: Sonnet 200k vs DeepSeek 16k (vantagem massiva)
- 🎯 Use Sonnet when: Multi-file refactoring, cross-domain
- 🎯 Use DeepSeek when: Python isolado, custo zero crítico

**vs Gemini 1.5 Pro**:
- ✅ Better: Code quality (+15%), Structured output (+20%)
- ❌ Worse: Context window (200k vs 2M), Multimodal (-100%)
- 📊 Context: Gemini permite prompts muito maiores
- 🎯 Use Sonnet when: Code-first, estrutura importa
- 🎯 Use Gemini when: Contexto massivo necessário, multimodal

---

## Context Optimization Insights

### Prompt Engineering Learnings
1. **Architectural tasks**: Beneficiam de 50-70% context usage (mais contexto = melhor)
2. **Code generation**: Sweet spot 30-50% (muito contexto atrapalha foco)
3. **Documentation**: Baixo contexto OK (25-40% suficiente)
4. **Debugging**: Médio-alto contexto (40-60% para entender problema)

### Framework Recommendations
- **Continue usando**: Hierarquia de memória (economia 51%)
- **Considere**: Comprimir logs semanais mais agressivamente (alguns chegam a 85% usage)
- **Evite**: Carregar todos os projetos simultaneamente (fragmenta contexto)

---

## Recommendations

### Best Use Cases
1. ⭐⭐⭐⭐⭐ Architecture & system design (sweet spot absoluto)
2. ⭐⭐⭐⭐⭐ Documentation & technical writing
3. ⭐⭐⭐⭐⭐ Cross-domain reasoning & research
4. ⭐⭐⭐⭐ Full-stack development (JS/TS/Python)
5. ⭐⭐⭐⭐ Multi-file refactoring

### Avoid For
- ❌ Tarefas simples repetitivas (use Haiku - 20x mais rápido, 75% mais barato)
- ❌ Code specialization extrema (use DeepSeek-Coder para Python puro)
- ❌ Contexto massivo >150k (use Gemini - 10x mais capacidade)

### Cost Optimization
- **Tarefa simples** (<5min esperado): Haiku ($)
- **Tarefa média** (5-30min): Sonnet ($$) ← Você está aqui
- **Tarefa complexa** (>30min, crítica): Opus ($$$$)

---

## Recent Sessions (Last 5)

1. **2025-11-16**: M008 Implementation + Multi-Agent Support
   - Type: Architecture + Documentation
   - Quality: ⭐⭐⭐⭐⭐ (5/5)
   - Tokens: 115,000 (57.5%)
   - Notes: Excelente design cross-domain

2. **2025-11-15**: Memory System v2.0
   - Type: Architecture + Implementation
   - Quality: ⭐⭐⭐⭐⭐ (5/5)
   - Tokens: 98,000 (49%)
   - Notes: Hierarquia bem pensada

3. **2025-11-14**: Lazy Logging + Windows SIGKILL
   - Type: Debugging + Implementation
   - Quality: ⭐⭐⭐⭐ (4/5)
   - Tokens: 85,000 (42.5%)
   - Notes: Solução criativa para limitação do Windows

[...]

---

## Data Collection

**Automatic**:
- Token usage (from system warnings)
- Duration (session timestamps)
- Files modified (git stats)
- Technologies (file extensions + imports)
- Task type (inferred from commands + file patterns)

**Manual** (optional prompt in `/end`):
- Quality rating (1-5 stars)
- Success (yes/partial/no)
- Task category (if auto-detection ambígua)

---

**Last analyzed**: 2025-11-16
**Next review**: 2025-11-30 (mensal)
```

**Workflow de coleta** (integrado no `/end`):

```markdown
### Passo X: Coletar Performance Metrics (NOVO)

**Auto-detectar**:
1. **Modelo usado**: [já implementado em M008]
2. **Tokens**:
   - Budget: [conhecido por modelo]
   - Usados: [system warnings acumulados]
   - % utilizado: [calcular]
3. **Duration**: [session start → end]
4. **Files**: [git diff --stat]
5. **Technologies**: [inferir de file extensions, imports]
6. **Task type**: [inferir de arquivos modificados + comandos]
7. **Project**: [já rastreado em M008]

**Perguntar ao usuário** (opcional, pulável):
```
Avalie esta sessão (opcional - Enter para pular):

1. Qualidade geral: ⭐⭐⭐⭐⭐ [1-5, Enter=auto]
2. Tarefa completada? [yes/partial/no, Enter=yes]
3. Tipo de tarefa: [architecture/code/refactor/debug/docs/research, Enter=auto-detect]
```

**Registrar no performance profile**:
- Adicionar entrada em `.claude/performance/profiles/[model-name].md`
- Update stats agregados (média, P95, etc)
- Re-calcular comparative performance (se >2 modelos têm dados)
- Atualizar context optimization insights (mensal)

**Formato no log da sessão**:
```markdown
### Performance Metrics

**Model**: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

**Context Metrics**:
- Budget: 200,000 tokens
- Used: ~115,000 tokens (57.5%)
- Prompt avg: ~12,000 tokens/interaction
- Output avg: ~3,500 tokens/response
- Framework economy: 52% (vs ~240k sem framework)

**Task Metrics**:
- Type: Architecture + Documentation (auto-detected)
- Quality: ⭐⭐⭐⭐⭐ (5/5, user-rated)
- Success: yes
- Duration: ~2h 30min
- Files: 12 created, 5 modified
- Technologies: Markdown, Python (auto-detected)

**Efficiency**:
- Output/Input ratio: 0.30 (alto)
- Context utilization: Optimal (50-60% range)
- Cost tier: $$$ (justified for complexity)
```
```

**Motivação**:
- Escolher modelo certo para tarefa (reduzir custo, melhorar qualidade)
- Data-driven decisions (não empírico)
- Otimizar prompts baseado em dados de contexto
- Identificar especializations de cada modelo
- Benchmark contínuo de performance
- **Context window optimization** (usuário pediu explicitamente)
- Combinar métricas de contexto com qualidade/custo = insights poderosos

**Benefícios esperados**:
- **Economia de tokens**: Escolher modelo right-sized para tarefa
- **Melhor qualidade**: Usar modelo especializado quando importa
- **Prompt optimization**: Identificar comprimento ótimo de prompt por tarefa/modelo
- **Context efficiency**: Saber quando mais contexto ajuda vs atrapalha
- **Comparative analysis**: Data para decidir qual modelo usar
- **Continuous improvement**: Tracking de tendências ao longo do tempo
- **ROI do framework**: Quantificar benefício da hierarquia de memória
- **Multi-agent orchestration**: Dados para routing inteligente (futuro)

**Riscos/Trade-offs**:
- Overhead de coleta (mitigado com auto-detection + perguntas opcionais)
- Pode gerar muito dado (agregações mensais mantêm gerenciável)
- Comparações podem ser unfair (contextos diferentes) - mitigar com categorização

**Notas de implementação**:
- **Fase 1** (imediato): Adicionar coleta no `/end`
  - Auto-detect: modelo, tokens, duration, files, tech, project
  - Optional: quality rating, success, task type
  - Append to profile file (create if doesn't exist)
- **Fase 2** (após 2-3 semanas): Análise comparativa
  - Script mensal: agregar dados de todos os modelos
  - Gerar comparative performance section
  - Identificar sweet spots de contexto por task type
- **Fase 3** (após 1-2 meses): Recomendações automáticas
  - `/end` sugere modelo alternativo se atual não é optimal
  - Exemplo: "Tarefa simples (refactor), Sonnet pode ser overkill. Considere Haiku (75% mais barato)?"
- **Fase 4** (futuro): Multi-agent routing
  - Sistema escolhe modelo automaticamente baseado em task + histórico
  - Hybrid approach: Claude para architecture, DeepSeek para code, Gemini para research

**Context Window Insights** (específicos):
- Track correlation: % context used vs quality rating
- Identify diminishing returns threshold (quando mais contexto não melhora)
- Detect context overload patterns (>80% usage = degradação?)
- Measure framework ROI (economia de tokens com hierarquia)
- Prompt engineering data (optimal length por task type)
- Model comparison (como cada modelo usa sua janela)

**Exemplo de insight** (após coleta):
```
📊 Context Analysis: Claude Sonnet 4.5

Descoberta: Tarefas de architecture têm qualidade 4.8/5 quando contexto usado é 50-70%,
mas cai para 4.1/5 quando >85% (context overload).

Recomendação: Para architecture, carregar contexto rico (projetos + logs recentes),
mas evitar carregar TODOS os logs históricos (fragmenta atenção).

Framework atual: Excelente (working memory + hierarquia = sweet spot 40-60%).
```

---

### [M010] - Lazy Context Loading for /continue ⭐⭐⭐
**Tipo**: Quick Win
**Impacto**: Alto (3x mais tempo de sessão)
**Esforço**: 30-60 minutos
**Status**: ✅ IMPLEMENTADO → 🟢 M010.1 (Multi-Resolution Memory)
**Data proposta**: 2025-11-17
**Data implementada**: 2025-11-17

**Descrição**:
Refatorar comando `/continue` para carregar contexto sob demanda (lazy loading) ao invés de carregar tudo upfront.

**Problema identificado**:
- `/continue` atual consome ~8.000 tokens (4% do budget) apenas para "preparar ambiente"
- Carrega ~700 linhas de contexto ANTES do usuário escolher o que fazer:
  - Global memory safe (165 linhas)
  - Session state (245 linhas)
  - Weekly summary (228 linhas)
  - Daily log (66 linhas)
- Resultado: **3 estouros de token em sessões recentes** (usuário reportou)
- Contexto carregado pode ser irrelevante se usuário escolher projeto diferente
- Trade-off atual: contexto completo vs tempo de sessão → não é sustentável

**Solução proposta**:
```markdown
## /continue (NOVO - Lazy Loading)

### 1. Executar redação de PII
python .claude/redact-pii.py
(Necessário para segurança - mantém)

### 2. Ler APENAS working memory (mínimo)
Ler `.session-state.md`:
- Última sessão (data, resumo 1 linha)
- Projetos ativos (3-5 principais)
- Pendências ativas (top 5)
- Próximos passos sugeridos

### 3. Apresentar resumo AO USUÁRIO (não carregar arquivos)
Mostrar em texto plano (não Read tool):
```
**Retomando**: 2025-11-16 - M008 + M009 implementados

**Active Projects**:
1. Memory System - ✅ COMPLETE (v2.1)
2. Hybrid Agent - 🔵 PLANNING
3. Creative Workflow - 📋 PLANNING

**Top Pendências**:
- [ ] Testar comandos project-centric
- [ ] Git commit com M008+M009
- [ ] FASE 0: Verificar LM Studio

Qual projeto você quer trabalhar? [1-3/outro/nenhum]
```

### 4. AGUARDAR escolha do usuário

### 5. DEPOIS carregar contexto específico:

**Se escolher projeto específico (1, 2, 3)**:
- Read: `~/.claude-memory/global-memory.safe.md` (contexto do usuário)
- Read: `.projects/[project-name]/.context.md` (contexto do projeto)
- Executar `/switch [project-name]` (atualiza foco)
- Total: ~350 linhas (economia de 50%)

**Se escolher "outro"**:
- Listar projetos disponíveis (via `/projects`)
- Repetir fluxo após escolha

**Se escolher "nenhum" (exploração livre)**:
- Read: `~/.claude-memory/global-memory.safe.md`
- Read: Resumo semanal (contexto geral)
- Total: ~350 linhas (economia de 50%)

### 6. Lembrete final
"Use `/end` para registrar esta sessão ao finalizar."
```

**Comparação de consumo**:
| Cenário | Linhas carregadas | Tokens estimados | Economia |
|---------|-------------------|------------------|----------|
| **Atual** | ~700 linhas | ~8.000 tokens | 0% (baseline) |
| **Lazy (projeto específico)** | ~350 linhas | ~4.000 tokens | **50%** |
| **Lazy (multi-projeto)** | ~350 linhas | ~4.000 tokens | **50%** |
| **Lazy (exploração)** | ~300 linhas | ~3.500 tokens | **56%** |

**Motivação**:
- Usuário reportou 3 estouros recentes (problema urgente)
- 4% do budget só para iniciar é insustentável
- Contexto carregado pode ser irrelevante (desperdício)
- Princípio de lazy evaluation: carregar apenas o necessário, quando necessário
- User feedback direto: "Considerar redução mais agressiva de informações para inicio"

**Benefícios esperados**:
- **3x mais tempo de sessão** (de ~70k para ~85k tokens disponíveis para trabalho real)
- **Startup mais rápido** (menos leituras de arquivo = menos latência)
- **Contexto relevante** (apenas o que é necessário para tarefa escolhida)
- **Escalabilidade** (funciona mesmo com 10+ projetos ativos)
- **Melhor UX** (usuário escolhe primeiro, sistema carrega depois)

**Riscos/Trade-offs**:
- **Duas interações vs uma** (perguntar + carregar vs carregar tudo)
  - Mitigação: Escolha é rápida (1-3 segundos), economia compensa
- **Contexto fragmentado** (se usuário mudar de ideia após carregar)
  - Mitigação: Raro, e pode re-executar `/switch` se necessário
- **Complexidade de implementação** (lógica condicional no comando)
  - Mitigação: Comando slash suporta condicionais, já testado em `/new`

**Notas de implementação**:
1. Atualizar `.claude/commands/continue.md`:
   - Remover steps 2-4 (global memory, weekly, daily upfront)
   - Adicionar step "Apresentar resumo formatado" (sem Read)
   - Adicionar step "Aguardar escolha usuário"
   - Adicionar step "Carregar contexto sob demanda"
2. Criar helper no session-state.md:
   - Seção "Quick Summary" (formatted, ready to paste)
   - Manter seções completas para quando precisar
3. Testar com sessão real:
   - Medir tokens economizados
   - Validar que contexto carregado é suficiente
4. Documentar economia real em performance metrics

**Implementação realizada** (M010.1 - Multi-Resolution Memory):
1. ✅ Criado `global-memory.quick.md` (~88 linhas, safe por padrão)
2. ✅ Criados `.context.quick.md` para todos os 4 projetos (~30 linhas cada)
3. ✅ Refatorado `/continue` com lazy loading + gatilhos temporais
4. ✅ Adicionado "Aggregation Status" ao `.session-state.md`
5. ✅ Atualizado `redact-pii.py` para gerar `.quick` automaticamente
6. ✅ Gatilhos: Sexta-feira → `/aggregate week`, Último dia → `/aggregate month`

**Economia alcançada**:
- Projeto específico: ~1.400 tokens (84% vs v2.0)
- Exploração livre: ~1.000 tokens (88% vs v2.0)
- **6x mais tempo de sessão disponível** (de ~70k para ~85k tokens)

**Próximos passos**:
- [ ] Testar `/continue` em próxima sessão (validar economia real)
- [ ] M010.2: Project-specific history (logs bidimensionais)
- [ ] M010.3: Melhorar algoritmo de geração automática de `.quick`

---

## Melhorias Implementadas

### M010.1 - Multi-Resolution Memory ✅
**Implementada**: 2025-11-17
**Economia**: 84-88% tokens no startup (~6.500 tokens economizados)

**O que foi feito**:
- Sistema de memórias multi-resolução (full → quick)
- Quick memories para global profile e project contexts
- Aggregation status no session-state (visibilidade sem ler logs)
- Gatilhos temporais automáticos (sexta + último dia do mês)
- Lazy loading: carregar apenas após escolha do usuário
- redact-pii.py atualizado para gerar .quick automaticamente

**Arquivos criados/modificados**:
- `~/.claude-memory/global-memory.quick.md` (novo)
- `.projects/*/.context.quick.md` (4 arquivos novos)
- `.claude/commands/continue.md` (refatorado)
- `.session-state.md` (seção Aggregation Status)
- `.claude/redact-pii.py` (atualizado)

**Status**: ✅ Pronto para usar, teste pendente na próxima sessão

---

## Melhorias Descartadas

*Esta seção registra propostas descartadas e por quê (aprendizado)*

---

## Processo de Avaliação

**Frequência de revisão**: Mensal (ou quando >10 propostas acumuladas)

**Critérios de priorização**:
1. **Alinhamento com pontos fortes do usuário** (cross-domain = alta prioridade)
2. **Quick Wins** (alto impacto, baixo esforço) → prioridade máxima
3. **Impacto Alto** → priorizar sobre médio/baixo
4. **Alinhamento com roadmap** → se Fase N depende, prioriza
5. **Dados suportam?** → se logs/métricas indicam necessidade, prioriza

**Workflow**:
1. Claude identifica oportunidade durante sessão
2. Adiciona entrada neste documento
3. Revisão mensal: priorizar top 3-5
4. Implementar em próximas sessões
5. Atualizar status (implementada ou descartada)

---

## Templates

### Template de Nova Melhoria
```markdown
### [MXXX] - Nome da Melhoria
**Tipo**: Quick Win / Implementação Grande
**Impacto**: Alto / Médio / Baixo
**Esforço**: [estimativa]
**Status**: 🔵 Proposta
**Data proposta**: YYYY-MM-DD

**Descrição**: [O que fazer]
**Motivação**: [Por que - dados, observações]
**Benefícios esperados**: [Lista]
**Riscos/Trade-offs**: [Lista]
**Notas de implementação**: [Dicas]
```

---

## Notas

**Princípios orientadores**:
- **Cross-domain first**: Sistema augmenta trabalho cross-domain (ponto forte)
- **Distributed & resilient**: Arquitetura client-server para multi-device
- **Privacy & control**: Dados sensíveis sempre sob controle

**Este documento é colaborativo**:
- Claude adiciona propostas conforme identifica oportunidades
- Usuário pode adicionar propostas manualmente
- Revisão conjunta mensal (ou conforme necessário)

**Objetivo**: Capturar insights e evitar que boas ideias se percam
**Não-objetivo**: Implementar todas as propostas (priorizar é key)

---

*Documento vivo - atualizado continuamente conforme sistema evolui*
