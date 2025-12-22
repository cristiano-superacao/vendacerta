# 📊 Sistema de Projeção de Vendas

## Visão Geral

O Sistema de Projeção de Vendas foi implementado para fornecer insights preditivos baseados no desempenho atual de cada vendedor e da equipe como um todo. As projeções são calculadas com base nos **dias úteis** (segunda a sexta-feira) do mês.

## Funcionalidades Implementadas

### 1. Cálculo de Dias Úteis
- **Dias Úteis Totais**: Total de dias úteis no mês (segunda a sexta)
- **Dias Úteis Trabalhados**: Quantos dias úteis já se passaram até hoje
- **Dias Úteis Restantes**: Quantos dias úteis faltam até o fim do mês

### 2. Métricas de Projeção

#### Para Cada Vendedor:
- **Média Diária**: Receita alcançada ÷ Dias úteis trabalhados
- **Projeção Mensal**: Média diária × Total de dias úteis do mês
- **Percentual Projetado**: (Projeção mensal ÷ Meta) × 100
- **Status da Projeção**: 
  - ✅ **Acima** (verde): Projeção ≥ 100% da meta
  - ⚠️ **Abaixo** (amarelo): Projeção < 100% da meta
- **Meta Diária Necessária**: Quanto precisa vender por dia para bater a meta

#### Para a Equipe (Agregado):
- **Velocidade Média Global**: Média de vendas por dia útil de toda a equipe
- **Projeção Total**: Estimativa de receita total ao fim do mês
- **Status Geral**: Se a equipe está no ritmo para bater a meta coletiva

## Como Funciona

### Exemplo Prático:

**Cenário:**
- Mês: Janeiro/2025 (23 dias úteis)
- Data atual: 15/01/2025 (10 dias úteis trabalhados)
- Meta do vendedor: R$ 100.000,00
- Receita alcançada: R$ 45.000,00

**Cálculos:**

1. **Média Diária:**
   ```
   R$ 45.000,00 ÷ 10 dias = R$ 4.500,00/dia
   ```

2. **Projeção Mensal:**
   ```
   R$ 4.500,00/dia × 23 dias = R$ 103.500,00
   ```

3. **Percentual Projetado:**
   ```
   (R$ 103.500,00 ÷ R$ 100.000,00) × 100 = 103,5%
   ```

4. **Status:** ✅ **Acima** (vendedor está no ritmo para superar a meta)

5. **Meta Diária Necessária:**
   ```
   Faltam: R$ 100.000,00 - R$ 45.000,00 = R$ 55.000,00
   Dias restantes: 23 - 10 = 13 dias
   Meta/dia: R$ 55.000,00 ÷ 13 = R$ 4.230,77/dia
   ```

## Visualização no Dashboard

### Card de Projeção da Equipe
Localizado após o card de "Alcance Geral da Equipe", mostra:
- 📅 **Dias Úteis**: Trabalhados, Restantes e Total
- 🚀 **Velocidade Média**: Receita média por dia útil
- 🏆 **Projeção Final**: Estimativa de receita total do mês

### Tabela de Ranking
Nova coluna **"Projeção"** (visível em telas grandes) com:
- **Valor Projetado**: Em verde (acima) ou amarelo (abaixo)
- **Média Diária**: Velocidade de vendas do vendedor
- **Percentual Projetado**: % da meta que será alcançado

## Benefícios

### Para Vendedores:
- ✅ **Acompanhamento em Tempo Real**: Saber se está no ritmo certo
- 📊 **Meta Diária Clara**: Quanto precisa vender por dia para bater a meta
- 🎯 **Ajuste de Estratégia**: Identificar quando precisa acelerar

### Para Supervisores:
- 👥 **Visão da Equipe**: Projeção agregada de todos os vendedores
- 🚨 **Identificação Precoce**: Detectar vendedores que precisam de apoio
- 📈 **Planejamento**: Estimar receita final do mês com antecedência

### Para Gestores:
- 💼 **Previsibilidade**: Projeção financeira mais precisa
- 🎯 **Tomada de Decisão**: Dados para ajustar metas ou estratégias
- 📊 **Análise de Performance**: Comparar alcance atual vs. projeção

## Considerações Importantes

### Dias Úteis
- ✅ Considera apenas **segunda a sexta-feira**
- ❌ **Não considera** feriados nacionais/estaduais automaticamente
- 💡 Para maior precisão, pode-se adicionar calendário de feriados no futuro

### Limitações
- Projeção assume **ritmo constante** de vendas
- Não considera **sazonalidade** (ex: vendas maiores no fim do mês)
- Mais confiável com **mais dias trabalhados** (após 5-7 dias úteis)

### Quando Usar
- **✅ Ideal**: A partir do dia 10 do mês (quando há histórico suficiente)
- **⚠️ Cuidado**: Nos primeiros 3-5 dias (projeção pode ser instável)
- **🎯 Melhor uso**: Comparar projeção com alcance real semanalmente

## Arquivos Modificados

### 1. `calculo_projecao.py` (NOVO)
Módulo dedicado para cálculos de projeção:
- `contar_dias_uteis()`: Calcula dias úteis do mês
- `calcular_projecao_mes()`: Projeção mensal baseada no desempenho
- `calcular_projecao_semana()`: Análise de ritmo semanal (preparado para futuro)
- `formatar_moeda()`: Formatação em Real brasileiro

### 2. `app.py`
- Importação de `calcular_projecao_mes` e `formatar_moeda`
- Rota `/dashboard` atualizada para incluir cálculos de projeção
- Projeção individual para cada vendedor
- Projeção agregada da equipe

### 3. `templates/dashboard.html`
- Card de "Projeção da Equipe" após card de alcance
- Coluna "Projeção" na tabela de ranking
- Indicadores visuais (verde/amarelo) de status
- Design responsivo (projeções ocultas em telas pequenas)

## Próximas Melhorias Possíveis

### Curto Prazo:
- [ ] Adicionar calendário de feriados brasileiros
- [ ] Gráfico de evolução da projeção ao longo do mês
- [ ] Alertas automáticos para vendedores abaixo da meta

### Médio Prazo:
- [ ] Projeção semanal ativa (além de mensal)
- [ ] Comparação: mês atual vs. mês anterior
- [ ] Análise de tendência (acelerando/desacelerando)

### Longo Prazo:
- [ ] Machine Learning para projeções mais precisas
- [ ] Considerar sazonalidade histórica
- [ ] Projeção por categoria de produto

## Como Testar

1. **Acesse o Dashboard**: http://localhost:5000/dashboard
2. **Observe o Card de Projeção**: Logo após as estatísticas globais
3. **Verifique a Tabela**: Nova coluna "Projeção" no ranking
4. **Teste com Dados Reais**: Cadastre metas e receitas para ver projeções

## Suporte

Se tiver dúvidas sobre o sistema de projeções:
- Verifique os cálculos em `calculo_projecao.py`
- Consulte a documentação de `app.py` na rota `/dashboard`
- Entre em contato com o time de desenvolvimento

---

**Versão**: 2.6.0  
**Data**: Janeiro 2025  
**Desenvolvido para**: Sistema SuaMeta
