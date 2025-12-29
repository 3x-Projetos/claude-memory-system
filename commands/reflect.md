---
description: Registro manual de métricas de well-being e estado
---

Coleta manual de métricas holísticas (baseado em `.workflow-metrics-collection.md`).

## Propósito
Capturar métricas que Claude NÃO pode inferir automaticamente:
- Well-being & Satisfaction
- Energy level
- Frustration points
- Life integration

## Uso
```
/reflect
```

## Processo

### 1. Prompt ao Usuário
Apresentar questionário breve:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Quick Reflection (opcional)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Satisfação com o progresso hoje? (1-10)
   [ Digite um número de 1-10 ]

2. Nível de energia agora?
   [ Energizado / Neutro / Drenado ]

3. Algo frustrante ou bloqueador?
   [ Texto livre ou "nada" ]

4. Notas pessoais (opcional):
   [ Texto livre ou deixe em branco ]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Importante**: Todas as respostas são opcionais. Usuário pode pular qualquer pergunta.

### 2. Validação de Respostas

- **Satisfação**: Se fornecido, validar que é número 1-10
- **Energia**: Se fornecido, validar que é uma das 3 opções
- **Frustração**: Qualquer texto livre aceito
- **Notas**: Qualquer texto livre aceito

### 3. Salvar em Arquivo Temporário

Criar `.metrics-reflection.tmp` com formato:

```markdown
# Metrics Reflection
**Timestamp**: YYYY-MM-DD HH:MM

## Métricas Relatadas

**Satisfação**: X/10
**Energia**: [Energizado/Neutro/Drenado]
**Frustração**: [texto ou "Nenhuma"]
**Notas**: [texto ou vazio]

---
*Este arquivo será incorporado no próximo /end e então deletado*
```

### 4. Confirmação

```
✓ Reflexão registrada em .metrics-reflection.tmp

Estas métricas serão automaticamente incorporadas ao log quando você executar `/end`.

Obrigado pelo feedback!
```

---

## Incorporação no /end

Quando usuário executar `/end`:

1. Claude detecta existência de `.metrics-reflection.tmp`
2. Pergunta: "Incorporar reflexão anterior ao log? (y/n)"
3. Se sim:
   - Merge com métricas inferidas
   - Incluir na seção `## Métricas da Sessão` do log diário
   - Deletar `.metrics-reflection.tmp`

**Formato no log**:
```markdown
## Métricas da Sessão

**Inferidas**:
- Duration: ~X min
- Files modified: Y
- Commits: Z
- Complexity: [Low/Medium/High]
- AI reliance: [Low/Medium/High]

**Relatadas** (via /reflect):
- Satisfação: X/10
- Energia: [estado]
- Frustração: [texto]
- Notas: [texto]
```

---

## Frequência Recomendada

- **Diária**: Ideal para tracking contínuo
- **Semanal**: Mínimo recomendado
- **Ad-hoc**: Quando sentir necessidade de registrar estado

**Não obrigatório**: Sistema funciona sem /reflect (apenas com inferências)

---

## Privacidade

- Arquivo `.metrics-reflection.tmp` é local (não versionado, em .gitignore)
- Métricas vão para `logs/daily/` (não versionado)
- Agregações semanais/mensais podem incluir tendências (não valores específicos)
- Perfil global pode incluir padrões (ex: "Productivity peak: manhãs") mas não dados sensíveis

---

## Benefícios

### Para Claude
- Entende seu estado emocional e energético
- Ajusta colaboração (ex: tarefas simples quando energia baixa)
- Detecta padrões (ex: frustração recorrente → sugerir melhorias)

### Para Você
- Autoconsciência sobre produtividade e bem-estar
- Tracking de evolução ao longo do tempo
- Identificação de triggers de frustração/satisfação
- Dados para otimizar workflow pessoal

---

## Exemplo de Uso

```
> /reflect

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Quick Reflection (opcional)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Satisfação com o progresso hoje? (1-10)
   > 8

2. Nível de energia agora?
   > Neutro

3. Algo frustrante ou bloqueador?
   > Configuração de Git demorou mais que esperado

4. Notas pessoais (opcional):
   > [em branco]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Reflexão registrada em .metrics-reflection.tmp

Estas métricas serão automaticamente incorporadas ao log quando você executar `/end`.

Obrigado pelo feedback!
```

---

**Lembre**: Reflexão é opcional mas valiosa. Torne um hábito se quiser maximizar insights do sistema de métricas holísticas.
