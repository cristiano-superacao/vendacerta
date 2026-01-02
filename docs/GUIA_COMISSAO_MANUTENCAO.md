# Guia de Comissão para Manutenção (Técnicos)

Este guia descreve como configurar e utilizar as faixas de comissão do módulo **Manutenção** aplicadas aos **Técnicos**.

## Onde fica
- Menu → Configurações → **Comissões**
- Abas: Vendedores | Supervisores | **Manutenção**

## Criar/Editar Faixas
1. Clique em **Nova Faixa**.
2. Defina:
   - Ordem (prioridade visual)
   - Alcance mínimo e máximo (%). Para "acima de", use máximo ≥ 1000.
   - Taxa de comissão (ex.: 0.02 para 2%).
   - Cor (danger, warning, info, success, primary) para visualização.
3. Salve e confirme.

## Visualização
- Cards mostram faixa (ordem, intervalo % e taxa %).
- Tabela lista todas as faixas com botões de **Editar** e **Excluir**.
- Layout responsivo, foco visível e ARIA melhoradas para acessibilidade.

## Vincular Faixa aos Técnicos
1. Na aba **Manutenção**, localize o card **Vincular Faixa aos Técnicos**.
2. Selecione a faixa desejada no **select**.
3. Clique em **Vincular a todos os Técnicos**.
4. O sistema aplica a faixa selecionada a todos os técnicos da empresa atual.

## Fórmula de Cálculo
```
Comissão Técnico = Receita Alcançada × Taxa da Faixa
```
- A faixa é determinada pelo **percentual de alcance** (Receita/Meta × 100).

## Boas Práticas
- Mantenha de 4 a 5 faixas com intervalos claros (ex.: 0–50, 51–75, 76–100, 101–125, Acima de 125).
- Use cores consistentes para interpretação rápida (danger=crítico, warning=atenção, success=excelente).
- Revise faixas trimestralmente conforme performance real.

## Acessibilidade e UX
- Abas com `aria-controls`, `aria-selected` e foco visível.
- Tabelas com `caption` oculto e cabeçalhos `scope="col"`.
- Botões de ação com `aria-label` descritivo.
- **Preferência de reduzir movimento** respeitada com `prefers-reduced-motion`.

## Pós-Configuração
- Valide cálculos em **Relatórios** e **Dashboard**.
- Ajuste metas dos técnicos para refletir a operação real.

## Troubleshooting
- Faixa não aparece? Verifique empresa atual e permissões.
- Vinculação não aplica? Confirme se há técnicos ativos na empresa.
- Healthcheck: `/ping` responde `pong` — útil para verificar se o app está online.
