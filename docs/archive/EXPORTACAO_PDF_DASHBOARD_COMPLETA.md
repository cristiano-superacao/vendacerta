# Exportação PDF Dashboard Completa

## 📄 Descrição Geral

Implementada a exportação COMPLETA de TODAS as informações do Dashboard em PDF profissional, mantendo layout responsivo e organizado.

## ✅ Seções Implementadas no PDF

### 1. **Resumo Geral** 📊
- Total de Vendedores
- Receita Total com percentual de alcance e emoji
- Meta Total
- Comissão Total com percentual sobre a receita

### 2. **Projeção de Vendas da Equipe** 📈
- Dias Úteis (Total, Trabalhados, Restantes)
- Média Diária em R$
- Projeção Final do Mês em R$
- Percentual Projetado

### 3. **Ranking de Equipes/Mesas** 👥
Tabela ordenada por alcance (TOP 10):
- Posição com emojis (🥇🥈🥉)
- Nome da Equipe
- Quantidade de Vendedores
- Receita Total
- Meta Total
- Alcance % com emoji de status
- Projeção Final

**Destaques:**
- TOP 3 com fundo dourado (#fef3c7)
- Cabeçalho azul (#0ea5e9)

### 4. **Ranking de Supervisores** 🏆
Tabela ordenada por alcance (TOP 10):
- Posição com emojis
- Nome do Supervisor
- Quantidade de Vendedores Supervisionados
- Receita Total Supervisionada
- Meta Total Supervisionada
- Alcance % com emoji de status
- Média Diária

**Destaques:**
- TOP 3 com fundo dourado (#fef3c7)
- Cabeçalho roxo (#8b5cf6)

### 5. **Ranking de Vendedores** 🎯
Tabela com TOP 20 vendedores:
- Posição com emojis
- Nome do Vendedor
- Equipe
- Receita
- Meta
- Alcance % com emoji
- Projeção Final

**Destaques:**
- TOP 3 com fundo dourado (#fef3c7)
- Cabeçalho verde (#10b981)

## 🎨 Recursos Visuais

### Emojis de Status de Alcance
- 🔴 0-50% (Crítico)
- 🟡 51-75% (Atenção)
- 🔵 76-100% (Próximo da meta)
- 🟢 101%+ (Meta atingida)

### Emojis de Posição
- 🥇 1º Lugar
- 🥈 2º Lugar
- 🥉 3º Lugar
- 4° em diante

### Paleta de Cores
- **Primária**: #667eea (Títulos principais)
- **Azul**: #0ea5e9 (Equipes)
- **Roxo**: #8b5cf6 (Supervisores)
- **Verde**: #10b981 (Vendedores e Projeções)
- **Dourado**: #fef3c7 (Destaques TOP 3)
- **Cinza Claro**: #f7fafc (Linhas alternadas)

## 🔧 Mudanças Técnicas

### Arquivo: `pdf_generator.py`

#### Nova Função `formatar_moeda()`
```python
def formatar_moeda(valor):
    """Formata valor como moeda brasileira"""
    return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
```

#### Função Atualizada `gerar_pdf_dashboard()`
**Assinatura Nova:**
```python
def gerar_pdf_dashboard(resumo_global, vendedores, mes=None, ano=None, equipes=None, supervisores=None):
```

**Parâmetros Adicionados:**
- `equipes`: Lista de equipes ordenadas por alcance com projeções
- `supervisores`: Lista de supervisores ordenados por alcance com projeções

**Dados Utilizados:**
- `resumo_global['projecao_global']`: Contém dias úteis, média diária, projeção mensal
- `equipes[i]['projecao']`: Projeção de cada equipe
- `supervisores[i]['projecao']`: Projeção de cada supervisor
- `vendedores[i]['projecao']`: Projeção de cada vendedor

### Arquivo: `app.py`

#### Rota Atualizada `/exportar-pdf-dashboard`
**Linha 4064-4230**

**Melhorias:**
1. Agregação completa de equipes com vendedores
2. Agregação completa de supervisores
3. Cálculo de projeções para cada equipe usando `calcular_projecao_mes()`
4. Cálculo de projeções para cada supervisor
5. Ordenação por `percentual_alcance` descendente

**Chamada da Função:**
```python
pdf_buffer = gerar_pdf_dashboard(
    resumo, 
    vendedores, 
    mes_atual, 
    ano_atual, 
    equipes, 
    supervisores
)
```

**Nome do Arquivo:**
```python
f"Dashboard_Completo_{meses[mes_atual-1]}_{ano_atual}.pdf"
```

## 📊 Estrutura de Dados

### Estrutura `equipes` (lista):
```python
{
    'nome': 'Nome da Equipe',
    'vendedores_count': 10,
    'receita_total': 50000.00,
    'meta_total': 60000.00,
    'percentual_alcance': 83.33,
    'projecao': {
        'dias_uteis_total': 22,
        'dias_uteis_trabalhados': 15,
        'dias_uteis_restantes': 7,
        'media_diaria': 3333.33,
        'projecao_mes': 73333.06,
        'percentual_projecao': 122.22,
        'status_projecao': 'Projeção acima da meta! 🟢'
    }
}
```

### Estrutura `supervisores` (lista):
```python
{
    'nome': 'Nome do Supervisor',
    'vendedores_count': 15,
    'receita_total': 75000.00,
    'meta_total': 90000.00,
    'percentual_alcance': 83.33,
    'projecao': {
        # mesma estrutura de equipes
    }
}
```

### Estrutura `resumo_global` (dict):
```python
{
    'total_vendedores': 50,
    'receita_total': 250000.00,
    'meta_total': 300000.00,
    'comissao_total': 12500.00,
    'alcance_geral': 83.33,
    'projecao_global': {
        'dias_uteis_total': 22,
        'dias_uteis_trabalhados': 15,
        'dias_uteis_restantes': 7,
        'media_diaria': 16666.67,
        'projecao_mes': 366666.74,
        'percentual_projecao': 122.22,
        'status_projecao': 'Projeção acima da meta! 🟢'
    }
}
```

## 📏 Layout do PDF

### Margens
- **Top**: 1.5 cm
- **Bottom**: 1.5 cm
- **Left**: 1.5 cm
- **Right**: 1.5 cm

### Tamanho da Página
- **Formato**: A4 (21cm x 29.7cm)

### Espaçamentos
- Entre seções: 0.4 - 0.5 cm
- Após título principal: 0.5 cm

### Tamanhos de Fonte
- **Título Principal**: 16pt
- **Títulos de Seção**: 11pt
- **Cabeçalhos de Tabela**: 7-8pt
- **Conteúdo de Tabela**: 6-7pt
- **Rodapé**: 7pt

## 🚀 Como Usar

1. Acesse o **Dashboard** do sistema
2. Clique no botão **"Exportar PDF"** (ícone 📄)
3. O PDF será gerado automaticamente com TODAS as 5 seções
4. Arquivo salvo como: `Dashboard_Completo_<Mês>_<Ano>.pdf`

## ✅ Validações

### Dados Obrigatórios
- ✅ Resumo geral sempre presente
- ✅ Lista de vendedores sempre presente
- ✅ Equipes (se houver) - exibe TOP 10
- ✅ Supervisores (se houver) - exibe TOP 10
- ✅ Vendedores - exibe TOP 20

### Tratamento de Dados Ausentes
- Se `equipes` for None ou vazia, a seção é omitida
- Se `supervisores` for None ou vazio, a seção é omitida
- Se `vendedores` for vazio, a seção é omitida
- Projeções zeradas são exibidas como R$ 0,00

### Formatação Automática
- Valores monetários com 2 casas decimais
- Percentuais com 1 casa decimal (0 para rankings)
- Nomes de vendedores/equipes truncados para caber nas colunas
- Data/hora de emissão no formato brasileiro

## 🎯 Resultados Esperados

### Comparação Visual
O PDF agora reflete EXATAMENTE o que o usuário vê no Dashboard:
- ✅ Cards de estatísticas
- ✅ Projeção de vendas com dias úteis
- ✅ Ranking de equipes ordenado
- ✅ Ranking de supervisores ordenado
- ✅ Ranking de vendedores detalhado

### Vantagens
1. **Completude**: 100% das informações do Dashboard
2. **Profissionalismo**: Layout limpo e organizado
3. **Responsividade**: Colunas ajustadas para caber em A4
4. **Rastreabilidade**: Data/hora de emissão
5. **Hierarquia Visual**: Cores e emojis facilitam leitura
6. **TOP 3 Destacados**: Fácil identificação de destaques

## 📝 Observações Importantes

### Limitações Conhecidas
1. **TOP 20 Vendedores**: Para evitar PDF muito grande
2. **TOP 10 Equipes/Supervisores**: Foco nos principais
3. **Fonte Pequena**: Necessária para caber todas as colunas
4. **Sem Gráficos**: Apenas tabelas e dados textuais

### Dependências
- **ReportLab 4.2.5**: Biblioteca de geração de PDF
- **Pillow 12.0.0**: Processamento de imagens
- **Python datetime**: Cálculo de dias úteis
- **calculo_projecao.py**: Função `calcular_projecao_mes()`

## 🔍 Troubleshooting

### PDF não gera
- Verifique se `reportlab` está instalado: `pip install reportlab`
- Confirme permissões de escrita no diretório

### Dados incompletos
- Verifique se a rota está passando `equipes` e `supervisores`
- Confirme que `calcular_projecao_mes()` está funcionando
- Verifique logs do Flask para erros

### Layout quebrado
- Confirme que nomes não têm caracteres especiais demais
- Verifique se valores numéricos são válidos
- Teste com dados de exemplo menores

## 📅 Histórico de Versões

### v2.0.0 - EXPORTAÇÃO COMPLETA (Atual)
- ✅ Adicionada Seção "Projeção de Vendas da Equipe"
- ✅ Adicionada Seção "Ranking de Equipes/Mesas"
- ✅ Adicionada Seção "Ranking de Supervisores"
- ✅ Melhorado layout com cores distintivas
- ✅ TOP 3 destacados em todas as tabelas
- ✅ Função `formatar_moeda()` criada
- ✅ Assinatura da função atualizada com `equipes` e `supervisores`
- ✅ Rota atualizada para coletar dados completos

### v1.0.0 - Versão Anterior
- Resumo Geral básico
- Ranking de Vendedores (todos)
- Sem projeções detalhadas
- Sem rankings de equipes/supervisores

## 👤 Autor
Sistema de Gestão de Metas e Comissões © 2025

---

**Status**: ✅ IMPLEMENTADO E FUNCIONAL
**Data**: Janeiro 2025
**Versão**: 2.0.0
