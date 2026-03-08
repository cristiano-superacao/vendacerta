# 🗺️ Mapa de Navegação do Sistema de Clientes

## 📋 Estrutura Completa de Navegação

```
┌─────────────────────────────────────────────────────────────────┐
│                    🏠 MENU LATERAL (Sidebar)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📊 DASHBOARD                                                    │
│  ├─ Dashboard (dashboard)                                       │
│  └─ Dashboard Supervisor (dashboard_supervisor)                 │
│                                                                  │
│  🎯 METAS                                                        │
│  ├─ 📋 Clientes (lista_clientes) ◄── MÓDULO DE CLIENTES        │
│  ├─ 📊 Relatório de Vendas (relatorio_vendas)                  │
│  ├─ 👤 Vendedores (lista_vendedores)                            │
│  ├─ 👔 Supervisores (lista_supervisores)                        │
│  ├─ 👥 Equipes (lista_equipes)                                  │
│  └─ 🎯 Gerenciar Metas (lista_metas)                            │
│                                                                  │
│  ⚙️ CONFIGURAÇÕES (Admin)                                       │
│  └─ 💰 Faixas de Comissão (configuracoes_comissoes)            │
│                                                                  │
│  ❓ AJUDA E SAIR                                                │
│  ├─ ❓ Central de Ajuda (ajuda)                                │
│  └─ 🚪 Sair (logout)                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxograma de Navegação - Módulo Clientes

```
                    📋 LISTA DE CLIENTES
                    /clientes
                    ┌─────────────────┐
                    │  Botões Topo:   │
                    │  ✓ Exportar     │
                    │  ✓ Importar     │
                    │  ✓ Novo Cliente │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌──────────────┐    ┌─────────────────┐
│ NOVO CLIENTE  │    │ VER CLIENTE  │    │ IMPORTAR EXCEL  │
│ /clientes/novo│    │ /clientes/id │    │/clientes/importar│
└───────┬───────┘    └──────┬───────┘    └────────┬────────┘
        │                   │                      │
        │            ┌──────┴──────┐              │
        │            ▼             ▼              │
        │    ┌──────────────┐  ┌──────────────┐  │
        │    │   EDITAR     │  │   COMPRA     │  │
        │    │/clientes/id/ │  │/clientes/id/ │  │
        │    │   editar     │  │   compra     │  │
        │    └──────────────┘  └──────────────┘  │
        │                                         │
        └─────────────────┬───────────────────────┘
                          ▼
                  ✅ VOLTA PARA LISTA
```

---

## 📊 Rotas e Seus Elementos de Navegação

### 1. 📋 Lista de Clientes (`/clientes`)

**Breadcrumb:**
```
Clientes
```

**Botões de Ação:**
- [Exportar Excel] → `/clientes/exportar` (download)
- [Importar Excel] → `/clientes/importar`
- [Novo Cliente] → `/clientes/novo`

**Ações na Tabela:**
- [Ver] → `/clientes/<id>`
- [Editar] → `/clientes/<id>/editar`
- [Compra] → `/clientes/<id>/compra`
- [Deletar] → POST `/clientes/<id>/deletar`

**Navegação:**
- Menu Lateral: "Clientes" (sempre visível)

---

### 2. ➕ Novo Cliente (`/clientes/novo`)

**Breadcrumb:**
```
Clientes > Novo Cliente
```

**Botões de Ação:**
- [Salvar] → POST → Redireciona para `/clientes/<id>` (ver cliente)
- [Cancelar] → Volta para `/clientes`

**Navegação:**
- Botão Cancelar retorna à lista
- Após salvar, vai para visualização do cliente criado

---

### 3. 👁️ Ver Cliente (`/clientes/<id>`)

**Breadcrumb:**
```
Clientes > [Nome do Cliente]
```

**Botões de Ação:**
- [Editar Cliente] → `/clientes/<id>/editar`
- [Registrar Compra] → `/clientes/<id>/compra`
- [Deletar Cliente] → POST `/clientes/<id>/deletar` → Redireciona para `/clientes`
- [Voltar] → `/clientes`

**Navegação:**
- Todas as compras listadas com data, valor e forma de pagamento
- Link "Voltar para Lista" no rodapé

---

### 4. ✏️ Editar Cliente (`/clientes/<id>/editar`)

**Breadcrumb:**
```
Clientes > [Nome do Cliente] > Editar
```

**Botões de Ação:**
- [Salvar Alterações] → POST → Redireciona para `/clientes/<id>`
- [Cancelar] → Volta para `/clientes/<id>`

**Navegação:**
- Formulário idêntico ao de criação
- Botão Cancelar retorna à visualização do cliente

---

### 5. 🛒 Registrar Compra (`/clientes/<id>/compra`)

**Breadcrumb:**
```
Clientes > [Nome do Cliente] > Registrar Compra
```

**Botões de Ação:**
- [Registrar Compra] → POST → Redireciona para `/clientes/<id>`
- [Cancelar] → Volta para `/clientes/<id>`

**Navegação:**
- Após registrar, volta para visualização do cliente
- Cliente atualizado com nova compra e data

---

### 6. 📊 Relatório de Vendas (`/clientes/relatorio-vendas`)

**Breadcrumb:**
```
Relatório de Vendas
```

**Botões de Ação:**
- [Imprimir] → `window.print()`
- [Exportar Excel] → `/clientes/exportar`

**Filtros Disponíveis:**
- Ano (select)
- Status (Verde/Amarelo/Vermelho)
- Vendedor (select)
- Supervisor (select)
- Cidade (input com datalist)
- Bairro (input com datalist)
- Forma de Pagamento (select)
- Buscar (submit)
- Limpar Filtros (link)

**Navegação:**
- Menu Lateral: "Relatório de Vendas"
- Filtros aplicados via GET

---

### 7. 📥 Importar Excel (`/clientes/importar`)

**Breadcrumb:**
```
Clientes > Importar Excel
```

**Botões de Ação:**
- [Baixar Modelo] → `/clientes/modelo-importacao` (download)
- [Enviar Arquivo] → POST → Validação → Sucesso/Erro
- [Cancelar] → Volta para `/clientes`

**Navegação:**
- Após importação bem-sucedida: volta para lista com mensagem
- Em caso de erro: permanece na página com mensagens de erro

---

### 8. 📤 Exportar Excel (`/clientes/exportar`)

**Tipo:** Download direto

**Navegação:**
- Chamado de 2 lugares:
  1. Lista de Clientes (botão "Exportar Excel")
  2. Relatório de Vendas (botão "Exportar Excel")
- Gera arquivo: `clientes_export_YYYYMMDD_HHMMSS.xlsx`
- Retorna automaticamente para a página de origem

---

## 🎨 Elementos de Interface Consistentes

### Cores de Status (em todas as páginas):

```css
🟢 Verde (Positivado):
   - Badge: bg-success
   - Card: bg-success bg-opacity-10 text-success
   - Indicação: Última compra < 30 dias

🟡 Amarelo (Atenção):
   - Badge: bg-warning
   - Card: bg-warning bg-opacity-10 text-warning
   - Indicação: Última compra 30-38 dias

🔴 Vermelho (Sem Compras):
   - Badge: bg-danger
   - Card: bg-danger bg-opacity-10 text-danger
   - Indicação: Última compra > 38 dias ou nenhuma compra
```

### Botões Padrão:

```html
✅ Primários (Ação Principal):
   - btn btn-success: Salvar, Registrar, Novo

⚪ Secundários (Ação Alternativa):
   - btn btn-outline-secondary: Cancelar, Voltar
   - btn btn-outline-success: Exportar
   - btn btn-outline-primary: Importar

🔴 Destrutivos (Deletar):
   - btn btn-danger: Deletar
```

### Cards de Formulário:

```
┌────────────────────────────────────┐
│ Card Header (bg-gradient-primary) │
│ 📝 Dados Básicos                   │
├────────────────────────────────────┤
│ Card Body                          │
│ - Nome                             │
│ - Email                            │
│ - Telefone                         │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ Card Header (bg-gradient-success) │
│ 🆔 CPF / CNPJ                      │
├────────────────────────────────────┤
│ Card Body                          │
│ - CPF (com máscara)                │
│ - CNPJ (com máscara)               │
└────────────────────────────────────┘
```

---

## 🔐 Controle de Acesso por Rota

| Rota | Vendedor | Supervisor | Admin | Super Admin |
|------|----------|------------|-------|-------------|
| Lista Clientes | ✅ Seus | ✅ Equipe | ✅ Todos | ✅ Todos |
| Novo Cliente | ✅ | ✅ | ✅ | ✅ |
| Ver Cliente | ✅ Seus | ✅ Equipe | ✅ Todos | ✅ Todos |
| Editar Cliente | ✅ Seus | ✅ Equipe | ✅ Todos | ✅ Todos |
| Deletar Cliente | ✅ Seus | ✅ Equipe | ✅ Todos | ✅ Todos |
| Registrar Compra | ✅ Seus | ✅ Equipe | ✅ Todos | ✅ Todos |
| Relatório Resumido | ❌ | ✅ | ✅ | ✅ |
| Relatório Vendas | ✅ | ✅ | ✅ | ✅ |
| Exportar Excel | ✅ | ✅ | ✅ | ✅ |
| Importar Excel | ✅ | ✅ | ✅ | ✅ |

---

## 📱 Responsividade por Tela

### 📱 Mobile (< 768px):
```
- Menu lateral colapsado (hamburguer)
- Cards empilhados verticalmente (col-12)
- Tabela com scroll horizontal (table-responsive)
- Formulários em 1 coluna
- Botões full-width
```

### 📲 Tablet (768px - 991px):
```
- Menu lateral visível ou colapsável
- Cards em 2 colunas (col-md-6)
- Estatísticas em 2 colunas
- Formulários em 2 colunas
```

### 💻 Desktop (≥ 992px):
```
- Menu lateral fixo
- Cards em 3-4 colunas (col-md-3, col-lg-4)
- Estatísticas em 4 colunas
- Formulários em 2-3 colunas
- Tabela completa sem scroll
```

---

## 🔍 Filtros e Buscas

### Lista de Clientes:
```javascript
// Busca em tempo real
📝 Campo de busca (JavaScript)
   - Filtra por: Nome, CPF, CNPJ, Cidade, Bairro
   - Atualização instantânea na tabela
```

### Relatório de Vendas:
```html
<!-- Filtros via GET -->
🔍 Filtros avançados:
   - Ano (2020-2029)
   - Status (Verde/Amarelo/Vermelho)
   - Vendedor (select)
   - Supervisor (select)
   - Cidade (datalist)
   - Bairro (datalist)
   - Forma Pagamento (select)
```

---

## ✅ Checklist de Navegação

- [x] Menu lateral tem link "Clientes"
- [x] Breadcrumbs em todas as páginas
- [x] Botão "Voltar" em todas as páginas de ação
- [x] Botões de ação claros e visíveis
- [x] Cores consistentes (Verde/Amarelo/Vermelho)
- [x] Ícones Bootstrap Icons em todos os botões
- [x] Mensagens flash após ações (sucesso/erro)
- [x] Redirecionamentos corretos após salvar/deletar
- [x] Links funcionais entre páginas
- [x] Responsividade em todas as telas
- [x] Filtros preservados após ação
- [x] Tabelas com scroll horizontal em mobile

---

## 🎯 Principais Fluxos de Uso

### Fluxo 1: Cadastrar Cliente e Fazer Primeira Compra
```
1. Menu > Clientes
2. Clique em "Novo Cliente"
3. Preencha formulário (CPF, Nome, Endereço, etc.)
4. Clique em "Salvar"
5. Redirecionado para "Ver Cliente"
6. Clique em "Registrar Compra"
7. Preencha valor e forma de pagamento
8. Clique em "Registrar Compra"
9. Volta para "Ver Cliente" (compra aparece na lista)
```

### Fluxo 2: Importar Clientes via Excel
```
1. Menu > Clientes
2. Clique em "Importar Excel"
3. Clique em "Baixar Modelo" (primeira vez)
4. Preencha planilha com dados dos clientes
5. Volte para "Importar Excel"
6. Selecione arquivo preenchido
7. Clique em "Enviar Arquivo"
8. Sistema valida dados
9. Se OK: "X clientes importados!" → Volta para lista
10. Se erro: Mensagens de erro → Corrige e tenta novamente
```

### Fluxo 3: Gerar Relatório de Vendas Filtrado
```
1. Menu > Relatório de Vendas
2. Selecione filtros:
   - Ano: 2025
   - Status: Verde (Positivado)
   - Cidade: Salvador
3. Clique em "Buscar"
4. Visualiza tabela filtrada
5. Clique em "Exportar Excel" (opcional)
6. Clique em "Imprimir" (opcional)
```

---

## 🚀 Conclusão

O sistema possui uma navegação **intuitiva, consistente e totalmente integrada**. Todos os links funcionam corretamente, os fluxos de uso são claros, e a responsividade garante boa experiência em qualquer dispositivo.

**Status da Navegação: ✅ PERFEITO**

---

**Mapa criado por:** Copilot  
**Data:** Dezembro 2025
