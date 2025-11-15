Controla a auto-aprovação de operações com múltiplos níveis em tempo real.

**Uso**:
- `/auto-approve on` - Ativa modo "edits" (Edit/Write apenas)
- `/auto-approve bash` - Ativa modo "bash" (Edit/Write/Bash)
- `/auto-approve all` - Ativa modo "all" (todos os tools)
- `/auto-approve off` - Desativa tudo (comportamento padrão)
- `/auto-approve status` - Verifica nível atual

**Níveis de aprovação**:
- `off` - Nada aprovado automaticamente
- `edits` - Apenas Edit e Write
- `bash` - Edit, Write e Bash (padrão recomendado para fluxo fluido)
- `all` - Todos os tools (sem confirmações)

**Como funciona**:
O comando cria/modifica o arquivo `.claude/auto-approve-state` com o nível escolhido.
O hook lê este arquivo a cada operação, permitindo mudança instantânea sem reiniciar CLI.

---

**Instruções para Claude**:

Leia o argumento passado após `/auto-approve`:

1. **Se argumento for "on"**:
   - Escreva "edits" no arquivo `.claude/auto-approve-state`
   - Responda: "✅ Auto-aprovação ATIVADA (modo edits)\n- Edit/Write: aprovado automaticamente\n- Bash: requer aprovação\n- Outros: requer aprovação"

2. **Se argumento for "bash"**:
   - Escreva "bash" no arquivo `.claude/auto-approve-state`
   - Responda: "✅ Auto-aprovação ATIVADA (modo bash)\n- Edit/Write/Bash: aprovado automaticamente\n- Outros: requer aprovação"

3. **Se argumento for "all"**:
   - Escreva "all" no arquivo `.claude/auto-approve-state`
   - Responda: "✅ Auto-aprovação ATIVADA (modo all)\n- Todos os tools: aprovados automaticamente\n⚠️ ATENÇÃO: Nenhuma operação pedirá confirmação!"

4. **Se argumento for "off"**:
   - Escreva "off" no arquivo `.claude/auto-approve-state`
   - Responda: "❌ Auto-aprovação DESATIVADA\n- Todos os tools voltam a pedir confirmação"

5. **Se argumento for "status"**:
   - Leia o arquivo `.claude/auto-approve-state`
   - Se não existe ou contém "off": Responda "❌ Auto-aprovação: OFF (tudo requer aprovação)"
   - Se contém "edits": Responda "✅ Auto-aprovação: EDITS\n- Edit/Write: ✅ aprovado\n- Bash: ❌ requer aprovação\n- Outros: ❌ requer aprovação"
   - Se contém "bash": Responda "✅ Auto-aprovação: BASH\n- Edit/Write/Bash: ✅ aprovado\n- Outros: ❌ requer aprovação"
   - Se contém "all": Responda "✅ Auto-aprovação: ALL\n- Todos os tools: ✅ aprovado"

6. **Se nenhum argumento ou argumento inválido**:
   - Mostre uso: `/auto-approve [on|bash|all|off|status]`

**Importante**: Use a ferramenta Write (não Bash/echo) para criar/modificar o arquivo de estado.
