---
description: Força agregação semanal ou mensal de logs
---

Executar workflows de agregação temporal para economia de tokens.

## Uso
```
/aggregate week [YYYY] [week_number]
/aggregate month [YYYY] [MM]
```

**Exemplos**:
- `/aggregate week` → Agrega última semana completa
- `/aggregate week 2025 46` → Agrega semana 46 de 2025
- `/aggregate month` → Agrega último mês completo
- `/aggregate month 2025 11` → Agrega novembro de 2025

---

## Agregação Semanal

### 1. Identificação da Semana
- Se argumentos fornecidos: usar YYYY e week_number
- Se não: calcular última semana completa (segunda a domingo)

**Cálculo de semana ISO**:
- Semana 1 = primeira semana com quinta-feira do ano
- Dias: Segunda a Domingo

### 2. Validação
- Verificar se já existe `logs/weekly/YYYY.MM.weekN.md`
- Se existir: perguntar se deseja sobrescrever
- Verificar se todos os 7 dias têm logs em `logs/daily/`
- Se faltar dias: avisar mas continuar

### 3. Execução do Workflow
Seguir exatamente `.workflow-weekly-aggregation.md`:

a) **Ler logs diários** da semana (7 arquivos)
b) **Agregar** em ~100 linhas:
   - Projetos Ativos (alto nível)
   - Arquivos Principais (top 10-15)
   - Atividades por Categoria (Dev/Docs/Infra/Learning/Decisões)
   - Métricas da Semana (quantitativas + holísticas)
   - Próximos Passos (pendências priorizadas)

### 4. Salvar Resumo
Criar `logs/weekly/YYYY.MM.weekN.md` com conteúdo agregado.

### 5. Atualizar Session State
Marcar em `.session-state.md` que semana foi agregada (para não sugerir novamente).

### 6. Confirmação
```
✓ Resumo semanal criado: logs/weekly/YYYY.MM.weekN.md
✓ Economia: ~85% (XX linhas vs YYY linhas de logs diários)
✓ Nenhuma informação crítica perdida

Próximo /continue carregará este resumo automaticamente.
```

---

## Agregação Mensal

### 1. Identificação do Mês
- Se argumentos fornecidos: usar YYYY e MM
- Se não: calcular último mês completo

### 2. Validação
- Verificar se já existe `logs/monthly/YYYY.MM.md`
- Se existir: perguntar se deseja sobrescrever
- Verificar quantos resumos semanais existem para o mês
- Avisar se incompleto mas continuar

### 3. Execução do Workflow
Seguir exatamente `.workflow-monthly-aggregation.md`:

a) **Ler resumos semanais** do mês (~4-5 arquivos)
b) **Agregar** em ~30 linhas:
   - Realizações do Mês (projetos completos, features principais)
   - Padrões e Tendências (tech stack, áreas de foco)
   - Tecnologias e Ferramentas (adotadas no mês)
   - Métricas Mensais (agregadas + tendências holísticas)
   - Decisões Arquiteturais Importantes (top 3-5)
   - Aprendizados Principais (top 5)
   - Próximos Passos (foco do mês seguinte)

### 4. Salvar Resumo
Criar `logs/monthly/YYYY.MM.md` com conteúdo agregado.

### 5. Atualizar Session State
Marcar em `.session-state.md` que mês foi agregado.

### 6. Confirmação
```
✓ Resumo mensal criado: logs/monthly/YYYY.MM.md
✓ Economia: ~93% vs diários, ~85% vs semanais
✓ Visão estratégica preservada

Este resumo fornece contexto de longo prazo para próximas sessões.
```

---

## Economia de Tokens

### Exemplo Real
**Logs diários brutos** (1 mês):
- ~30 dias × ~150 linhas/dia = ~4.500 linhas

**Com agregação hierárquica**:
- Resumo mensal: 30 linhas
- Último resumo semanal: 100 linhas
- Working memory: 50 linhas
- **Total carregado**: ~180 linhas

**Economia: ~96%** sem perda de contexto crítico

---

## Detecção Automática

Comandos `/continue` e `/new` detectam automaticamente se há agregações pendentes:

```
⚠️ Agregações Pendentes:
- Semana 46 de 2025: Execute `/aggregate week`
- Mês 2025.11: Execute `/aggregate month`
```

**Não obrigatório**: Sistema funciona sem agregações, mas carregará mais tokens.

---

## Validação Pós-Agregação

Claude deve auto-validar:
- [ ] Arquivo criado no diretório correto
- [ ] Tamanho dentro do alvo (100 linhas para weekly, 30 para monthly)
- [ ] Nenhuma informação crítica perdida (decisões, blockers, aprendizados)
- [ ] Métricas calculadas corretamente
- [ ] Próximos passos capturam pendências reais

---

## Notas Importantes

- **Não é sumário verbatim**: Agregação inteligente, não copy-paste
- **Foco em tendências**: O que persistiu, não eventos únicos
- **Contexto suficiente**: Cada item auto-explicativo
- **Top N**: Top 3-5 em vez de listar tudo
- **Reversível**: Logs diários preservados, sempre pode consultar detalhes

---

## Quando Executar

### Semanal
- **Recomendado**: Toda segunda-feira
- **Mínimo**: Ao final de cada semana completa

### Mensal
- **Recomendado**: Primeiro dia de cada mês
- **Mínimo**: Quando tiver 4+ resumos semanais

---

## Exemplo de Uso

```
> /aggregate week

Calculando última semana completa...

Semana 46 de 2025 (13/11 - 19/11)
- 7/7 dias com logs encontrados

Lendo logs diários...
✓ logs/daily/2025.11.13.md
✓ logs/daily/2025.11.14.md
✓ logs/daily/2025.11.15.md
✓ logs/daily/2025.11.16.md
✓ logs/daily/2025.11.17.md
✓ logs/daily/2025.11.18.md
✓ logs/daily/2025.11.19.md

Agregando atividades...
- 3 projetos identificados
- 47 arquivos modificados
- 12 commits
- 5 tecnologias mencionadas
- 2 decisões arquiteturais importantes

Gerando resumo semanal...

✓ Resumo semanal criado: logs/weekly/2025.11.week46.md
✓ Economia: ~85% (98 linhas vs 673 linhas de logs diários)
✓ Nenhuma informação crítica perdida

Próximo /continue carregará este resumo automaticamente.
```

---

**Lembre**: Agregações regulares mantêm sistema eficiente e contexto acessível.
