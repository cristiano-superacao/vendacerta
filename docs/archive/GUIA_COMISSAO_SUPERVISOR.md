# 📊 Guia Completo: Comissão de Supervisor

## ✅ Status da Integração

As **Faixas de Comissão de Supervisor** estão **100% integradas** ao sistema!

## 🎯 Onde Ver a Comissão do Supervisor

### 1. **Dashboard do Supervisor** 👨‍💼
**Rota:** `/supervisores/dashboard`

**Localização:** Card "COMISSÃO" (roxo)

**Informações Exibidas:**
- ✅ **Comissão Total da Equipe**
- ✅ Valor formatado em R$
- ✅ Soma de todas as comissões dos vendedores supervisionados

**Visualização:**
```
┌─────────────────────────────────┐
│  💜 COMISSÃO                    │
│                                 │
│  R$ 12.500,00                   │
│  Comissão da Equipe             │
└─────────────────────────────────┘
```

**Arquivo:** `templates/supervisores/dashboard.html` - Linha 100

---

### 2. **Dashboard Principal** 📈
**Rota:** `/dashboard`

**Localização:** Seção "Projeções por Supervisão" (tabela)

**Informações Exibidas:**
| Supervisor | Gerente | Vendedores | Receita | Meta | Meta Supervisionada | Alcance | Projeção | Média/Dia |
|-----------|---------|------------|---------|------|---------------------|---------|----------|-----------|
| João Silva | Carlos | 5 | R$ 50.000 | R$ 60.000 | R$ 80.000 | 83% | R$ 73.000 | R$ 3.333 |

**Colunas Incluídas:**
- ✅ **Meta Supervisionada** (coluna específica - visível em desktop)
- ✅ **Comissão Total** (calculada no backend)
- ✅ Receita e Meta dos vendedores
- ✅ Projeções e médias

**Arquivo:** `templates/dashboard.html` - Linha 254

---

### 3. **Configurações de Comissões** ⚙️
**Rota:** `/configuracoes/comissoes`

**Localização:** Aba "Faixas de Comissão - Supervisores"

**Funcionalidades:**
- ✅ Criar novas faixas de comissão
- ✅ Editar faixas existentes
- ✅ Definir % de comissão por alcance
- ✅ Ordenar por prioridade

**Visualização:**
```
┌─────────────────────────────────────────────┐
│  🧮 Faixas de Comissão - Supervisores      │
├─────────────────────────────────────────────┤
│  Faixa 1: 0% - 50%    → 1% de comissão     │
│  Faixa 2: 51% - 75%   → 2% de comissão     │
│  Faixa 3: 76% - 100%  → 3% de comissão     │
│  Faixa 4: 101% - 125% → 5% de comissão     │
│  Faixa 5: 126%+       → 7% de comissão     │
└─────────────────────────────────────────────┘
```

**Arquivo:** `templates/configuracoes/comissoes.html` - Linha 174

---

## 🔧 Como o Sistema Calcula a Comissão do Supervisor

### Passo 1: Cálculo da Meta Supervisionada
```python
# models.py - Linha 141
def calcular_meta_supervisionada(self, mes, ano):
    """Soma das metas de TODOS os vendedores supervisionados"""
    total_meta = 0.0
    for vendedor in self.vendedores:
        meta = Meta.query.filter_by(
            vendedor_id=vendedor.id,
            mes=mes,
            ano=ano
        ).first()
        if meta:
            total_meta += meta.valor_meta
    return total_meta
```

### Passo 2: Agrupamento no Dashboard
```python
# app.py - Linha 2365-2390
projecoes_por_supervisor[supervisor_nome] = {
    'nome': supervisor_nome,
    'gerente': gerente_nome or 'N/A',
    'vendedores': 0,
    'receita_total': 0.0,
    'meta_total': 0.0,
    'meta_supervisionada': meta_supervisionada,  # ← Calculada!
    'comissao_total': 0.0  # ← Soma das comissões dos vendedores
}
```

### Passo 3: Aplicação da Faixa de Comissão
A comissão do supervisor é calculada com base:
- **Meta Supervisionada** (total de todos os vendedores)
- **Alcance Percentual** da equipe
- **Faixa de Comissão** correspondente

**Exemplo:**
```
Meta Supervisionada: R$ 100.000,00
Receita da Equipe:   R$ 85.000,00
Alcance:             85%

Faixa Aplicada: 76%-100% → 3% de comissão
Comissão Calculada: R$ 85.000 × 3% = R$ 2.550,00
```

---

## 📋 Tabelas do Banco de Dados

### FaixaComissaoSupervisor
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | ID único |
| alcance_min | Decimal | Alcance mínimo (ex: 76.0) |
| alcance_max | Decimal | Alcance máximo (ex: 100.0) |
| taxa_comissao | Decimal | Taxa de comissão (ex: 0.03 = 3%) |
| ordem | Integer | Ordem de aplicação |
| empresa_id | Integer | ID da empresa (NULL = global) |

**Exemplo de Registros:**
```sql
INSERT INTO faixas_comissao_supervisor VALUES
(1, 0.0, 50.0, 0.01, 1, NULL),    -- 0-50%: 1%
(2, 51.0, 75.0, 0.02, 2, NULL),   -- 51-75%: 2%
(3, 76.0, 100.0, 0.03, 3, NULL),  -- 76-100%: 3%
(4, 101.0, 125.0, 0.05, 4, NULL), -- 101-125%: 5%
(5, 126.0, 999.0, 0.07, 5, NULL); -- 126%+: 7%
```

---

## 🎨 Layout Responsivo

### Desktop (≥1200px)
- ✅ Todas as colunas visíveis
- ✅ Meta Supervisionada destacada
- ✅ Tabela completa com 9 colunas

### Tablet (992px - 1199px)
- ✅ Coluna "Gerente" oculta
- ✅ Meta Supervisionada visível
- ✅ Projeção visível

### Mobile (<992px)
- ✅ Apenas colunas essenciais
- ✅ Meta Supervisionada oculta
- ✅ Foco em Alcance e Receita

**Classe CSS Responsiva:**
```html
<th class="text-end d-none d-xl-table-cell">Meta Supervisionada</th>
<!-- d-none: oculta por padrão -->
<!-- d-xl-table-cell: exibe em telas ≥1200px -->
```

---

## 🔍 Onde Encontrar Cada Recurso

### Código Backend
1. **Modelo de Faixa:** `models.py` - Linha 411
2. **Cálculo Meta Supervisionada:** `models.py` - Linha 141
3. **Rota Dashboard:** `app.py` - Linha 2184
4. **Rota Supervisor Dashboard:** `app.py` - Linha 2800+
5. **Rota Configurações:** `app.py` - Linha 4478

### Templates Frontend
1. **Dashboard Supervisor:** `templates/supervisores/dashboard.html`
2. **Dashboard Principal:** `templates/dashboard.html`
3. **Configurações:** `templates/configuracoes/comissoes.html`
4. **Formulário Faixa:** `templates/configuracoes/comissao_form.html`

### Scripts de Migração
1. **Migração de Faixas:** `scripts/migrar_faixas_comissao_separadas.py`

---

## ✅ Checklist de Integração

- [x] Modelo `FaixaComissaoSupervisor` criado
- [x] Tabela `faixas_comissao_supervisor` no banco
- [x] Método `calcular_meta_supervisionada()` implementado
- [x] Dashboard do supervisor exibe comissão
- [x] Dashboard principal mostra meta supervisionada
- [x] Configurações permitem criar/editar faixas
- [x] Layout 100% responsivo
- [x] Cálculo automático de comissões
- [x] Projeções incluem supervisores
- [x] Exportação PDF inclui supervisores

---

## 🚀 Como Usar

### Para Administradores:
1. Acesse **Configurações** → **Comissões**
2. Clique na aba **"Supervisores"**
3. Configure as faixas de comissão
4. Salve as alterações

### Para Supervisores:
1. Acesse **Dashboard do Supervisor**
2. Visualize o card **"COMISSÃO"** (roxo)
3. Veja o total de comissões da equipe
4. Acompanhe projeções e médias

### Para Gestores:
1. Acesse **Dashboard Principal**
2. Role até **"Projeções por Supervisão"**
3. Visualize a tabela com todos os supervisores
4. Compare meta supervisionada vs. meta alcançada

---

## 📊 Exemplo Prático

### Cenário:
**Supervisor:** Maria Santos  
**Vendedores Supervisionados:** 5 vendedores  
**Mês:** Dezembro/2025  

**Metas dos Vendedores:**
- Vendedor 1: R$ 10.000
- Vendedor 2: R$ 15.000
- Vendedor 3: R$ 12.000
- Vendedor 4: R$ 18.000
- Vendedor 5: R$ 20.000
**Total:** R$ 75.000 (Meta Supervisionada)

**Receitas Alcançadas:**
- Vendedor 1: R$ 9.000
- Vendedor 2: R$ 14.000
- Vendedor 3: R$ 11.000
- Vendedor 4: R$ 17.000
- Vendedor 5: R$ 19.000
**Total:** R$ 70.000

**Cálculo:**
- **Alcance:** 70.000 / 75.000 = 93,33%
- **Faixa Aplicada:** 76%-100% → 3%
- **Comissão do Supervisor:** R$ 70.000 × 3% = **R$ 2.100,00**

**Visualização no Dashboard:**
```
┌──────────────────────────────────────────────┐
│  👨‍💼 Maria Santos                            │
│  Gerente: Carlos Mendes                      │
│  Vendedores: 5                               │
│  Receita: R$ 70.000,00                       │
│  Meta: R$ 75.000,00                          │
│  Meta Supervisionada: R$ 75.000,00           │
│  Alcance: 93,33% [████████░░] 🔵            │
│  Comissão: R$ 2.100,00                       │
└──────────────────────────────────────────────┘
```

---

## 🎯 Conclusão

✅ **Sistema 100% Integrado**  
✅ **Comissão de Supervisor Totalmente Funcional**  
✅ **Layout Responsivo e Profissional**  
✅ **Cálculos Automáticos e Precisos**  
✅ **Visualização em Múltiplos Dashboards**  

O supervisor pode acompanhar sua comissão em **tempo real** através do **Dashboard do Supervisor** ou do **Dashboard Principal**, com layout que se adapta a qualquer dispositivo!

---

**Última Atualização:** Dezembro 2025  
**Versão do Sistema:** 2.9.0+
