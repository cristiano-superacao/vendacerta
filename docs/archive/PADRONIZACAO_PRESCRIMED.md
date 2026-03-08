# 🎨 Padronização de Design - Estilo Prescrimed

> **Versão:** 3.0.0  
> **Data:** 2024  
> **Status:** ✅ Concluído

## 📋 Sumário Executivo

Sistema completamente redesenhado com base na interface moderna do Prescrimed, apresentando:
- **Sidebar verde escuro** com gradiente profissional
- **Cards limpos** com bordas coloridas (verde, teal, vermelho, roxo)
- **Ícones grandes** (56px) com backgrounds suaves
- **Tipografia Inter** com hierarquia visual clara
- **Design system** consistente em todos templates

---

## 🎨 Design System

### Paleta de Cores

```css
/* Cores Primárias */
--primary-green: #22c55e;     /* Verde principal */
--sidebar-bg: #1a4d2e;        /* Verde escuro sidebar */
--sidebar-dark: #0d3a1f;      /* Verde mais escuro */

/* Cores Secundárias */
--teal: #14b8a6;              /* Teal/Ciano */
--red: #ef4444;               /* Vermelho */
--purple: #a855f7;            /* Roxo */

/* Escala de Cinza */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-900: #111827;
```

### Tipografia

```css
/* Fonte Principal */
font-family: 'Inter', system-ui, -apple-system, sans-serif;

/* Hierarquia de Tamanhos */
.stats-value-clean: 2rem (32px) - Peso 700
.stats-label-clean: 0.875rem (14px) - Peso 600
.header-title: 1.75rem (28px) - Peso 700
.header-subtitle: 0.75rem (12px) - Peso 600
```

---

## 🔧 Componentes Principais

### 1. Cards de Estatísticas

```html
<!-- Card Verde (padrão principal) -->
<div class="stats-card-clean stats-card-green">
    <div class="stats-icon-clean stats-icon-green">
        <i class="bi bi-people-fill"></i>
    </div>
    <p class="stats-label-clean">Total de Vendedores</p>
    <h3 class="stats-value-clean">245</h3>
    <p class="stats-subtitle-clean">Cadastrados no sistema</p>
</div>

<!-- Card Teal (informações) -->
<div class="stats-card-clean stats-card-teal">
    <div class="stats-icon-clean stats-icon-teal">
        <i class="bi bi-graph-up"></i>
    </div>
    <p class="stats-label-clean">Receita Total</p>
    <h3 class="stats-value-clean">R$ 1.248.000</h3>
    <p class="stats-subtitle-clean">Acumulado no mês</p>
</div>

<!-- Card Vermelho (metas/alertas) -->
<div class="stats-card-clean stats-card-red">
    <div class="stats-icon-clean stats-icon-red">
        <i class="bi bi-bullseye"></i>
    </div>
    <p class="stats-label-clean">Meta do Mês</p>
    <h3 class="stats-value-clean">R$ 1.500.000</h3>
    <p class="stats-subtitle-clean">Objetivo estabelecido</p>
</div>

<!-- Card Roxo (comissões/financeiro) -->
<div class="stats-card-clean stats-card-purple">
    <div class="stats-icon-clean stats-icon-purple">
        <i class="bi bi-wallet2"></i>
    </div>
    <p class="stats-label-clean">Comissão</p>
    <h3 class="stats-value-clean">R$ 62.400</h3>
    <p class="stats-subtitle-clean">Saldo acumulado</p>
</div>
```

**Características:**
- Background branco (#ffffff)
- Borda esquerda colorida (4px)
- Sombra suave (0 1px 3px rgba(0,0,0,0.1))
- Border-radius 12px
- Padding 1.5rem (24px)
- Hover: elevação de sombra

### 2. Cabeçalhos de Página

```html
<div class="page-header-clean">
    <div class="header-content">
        <p class="header-subtitle">OPERACIONAL</p>
        <h1 class="header-title">
            <i class="bi bi-people-fill"></i> Gerenciamento de Vendedores
        </h1>
    </div>
    <div class="header-actions">
        <a href="#" class="btn btn-secondary-clean">
            <i class="bi bi-upload"></i> Importar
        </a>
        <a href="#" class="btn btn-primary-clean">
            <i class="bi bi-plus-circle"></i> Novo Vendedor
        </a>
    </div>
</div>
```

**Características:**
- Flex layout responsivo
- Subtítulo cinza uppercase (letter-spacing: 1.5px)
- Título grande com ícone
- Botões alinhados à direita
- Wrap em mobile

### 3. Botões

```html
<!-- Botão Primário Verde -->
<button class="btn btn-primary-clean">
    <i class="bi bi-check-circle"></i> Salvar
</button>

<!-- Botão Secundário Cinza -->
<button class="btn btn-secondary-clean">
    <i class="bi bi-x-circle"></i> Cancelar
</button>
```

**Características:**
- Border-radius: 10px
- Padding: 0.625rem 1.25rem
- Peso da fonte: 600
- Transição suave (0.2s)
- Hover: escurecimento

### 4. Sidebar

```html
<div class="sidebar" style="background: linear-gradient(180deg, #1a4d2e 0%, #0d3a1f 100%);">
    <!-- Logo/Marca -->
    <div class="sidebar-brand">
        <i class="bi bi-bullseye"></i> SUAMETA
    </div>
    
    <!-- Informações do Usuário -->
    <div class="sidebar-user">
        <p class="user-greeting">Bem-vindo</p>
        <p class="user-name">{{ current_user.nome }}</p>
        <p class="user-email">{{ current_user.email }}</p>
    </div>
    
    <!-- Navegação -->
    <nav class="sidebar-nav">
        <div class="nav-section">
            <p class="nav-section-title">Navegação</p>
            <a href="#" class="nav-link active">
                <i class="bi bi-speedometer2"></i> Dashboard
            </a>
        </div>
    </nav>
</div>
```

**Características:**
- Gradiente verde (#1a4d2e → #0d3a1f)
- Largura: 280px
- Info do usuário no topo
- Hover verde claro (#4ade80)
- Links com ícones alinhados

### 5. Barra de Busca e Filtros

```html
<div class="search-filter-bar">
    <div class="search-input-group">
        <i class="bi bi-search"></i>
        <input type="text" placeholder="Buscar...">
    </div>
    <select class="filter-select">
        <option>Todos</option>
    </select>
    <button class="btn btn-primary-clean">
        <i class="bi bi-funnel"></i> Filtrar
    </button>
</div>
```

### 6. Estado Vazio

```html
<div class="empty-state-clean">
    <i class="bi bi-inbox empty-state-icon"></i>
    <h3 class="empty-state-title">Nenhum item encontrado</h3>
    <p class="empty-state-text">Comece adicionando novos registros ao sistema.</p>
    <a href="#" class="btn btn-primary-clean">
        <i class="bi bi-plus-circle"></i> Adicionar Novo
    </a>
</div>
```

---

## 📁 Arquivos Modificados

### Templates Atualizados

```
✅ templates/base.html
   - Sidebar verde com gradiente
   - Seção de informações do usuário
   - Navegação com hover verde

✅ templates/dashboard.html
   - Header clean
   - 4 cards com bordas coloridas
   - Layout responsivo

✅ templates/vendedores/lista.html
   - Header padronizado
   - 3 cards (verde, teal, roxo)
   - Botões limpos

✅ templates/supervisores/lista.html
   - Header padronizado
   - 3 cards (verde, teal, verde)
   - Estilo consistente

✅ templates/metas/lista.html
   - Header atualizado
   - Preparado para novos cards
   - Botões modernos
```

### CSS Atualizado

```
📄 static/css/custom.css
   - Versão 3.0.0
   - 1061+ linhas
   - Variáveis CSS
   - Design system completo
```

---

## 🎯 Uso das Cores por Contexto

### Verde (#22c55e, #1a4d2e)
- **Uso:** Indicadores positivos, totais, ações principais
- **Contexto:** Vendedores ativos, botões de ação, sidebar
- **Exemplo:** Total de vendedores, Nova meta, Supervisor ativo

### Teal (#14b8a6)
- **Uso:** Informações, dados neutros, status
- **Contexto:** Receitas, valores financeiros, estatísticas
- **Exemplo:** Receita total, Vendas do mês, Dados gerais

### Vermelho (#ef4444)
- **Uso:** Metas, objetivos, alertas importantes
- **Contexto:** Metas estabelecidas, limites, avisos
- **Exemplo:** Meta do mês, Limite de vendas, Pendências

### Roxo (#a855f7)
- **Uso:** Comissões, valores financeiros especiais
- **Contexto:** Ganhos, pagamentos, bonificações
- **Exemplo:** Comissão acumulada, Bônus, Valores especiais

---

## 📱 Responsividade

### Breakpoints

```css
/* Mobile First */
Base: 12 colunas (col-12)

/* Small - Tablets */
@media (min-width: 576px)
  - Cards: 6 colunas (col-sm-6)
  - 2 cards por linha

/* Large - Desktop */
@media (min-width: 992px)
  - Cards: 3 ou 4 colunas (col-lg-3, col-lg-4)
  - 3-4 cards por linha
  - Sidebar fixa
```

### Adaptações Mobile

- **Sidebar:** Colapsável com menu hambúrguer
- **Cards:** Empilhados verticalmente
- **Header Actions:** Wrap em múltiplas linhas
- **Ícones:** Tamanho mantido (56px)
- **Espaçamentos:** Reduzidos proporcionalmente

---

## ✅ Checklist de Implementação

### Concluído
- [x] Criação de variáveis CSS
- [x] Design system no custom.css
- [x] Sidebar verde escura com gradiente
- [x] Seção de informações do usuário
- [x] Cards de estatísticas padrão Prescrimed
- [x] 4 variantes de cores (verde, teal, red, purple)
- [x] Ícones grandes (56px)
- [x] Cabeçalhos limpos (.page-header-clean)
- [x] Sistema de botões (.btn-primary-clean, .btn-secondary-clean)
- [x] Dashboard atualizado
- [x] Vendedores lista atualizada
- [x] Supervisores lista atualizada
- [x] Metas lista header atualizado
- [x] Layout 100% responsivo

### Pendente
- [ ] Aplicar filtros modernos em todas listas
- [ ] Implementar estados vazios
- [ ] Atualizar formulários
- [ ] Modernizar tabelas
- [ ] Adicionar loading states
- [ ] Implementar toasts/notificações

---

## 🚀 Como Usar

### 1. Criar Novo Card de Estatística

```html
<div class="stats-card-clean stats-card-[green|teal|red|purple]">
    <div class="stats-icon-clean stats-icon-[green|teal|red|purple]">
        <i class="bi bi-[icon-name]"></i>
    </div>
    <p class="stats-label-clean">Título do Card</p>
    <h3 class="stats-value-clean">Valor</h3>
    <p class="stats-subtitle-clean">Descrição adicional</p>
</div>
```

### 2. Criar Novo Header de Página

```html
<div class="page-header-clean">
    <div class="header-content">
        <p class="header-subtitle">CATEGORIA</p>
        <h1 class="header-title">
            <i class="bi bi-icon"></i> Título da Página
        </h1>
    </div>
    <div class="header-actions">
        <!-- Botões de ação -->
    </div>
</div>
```

### 3. Adicionar Botões

```html
<!-- Ação principal -->
<a href="#" class="btn btn-primary-clean">
    <i class="bi bi-plus-circle"></i> Adicionar
</a>

<!-- Ação secundária -->
<a href="#" class="btn btn-secondary-clean">
    <i class="bi bi-upload"></i> Importar
</a>
```

---

## 📊 Antes e Depois

### Antes (v2.9.x)
- ❌ Sidebar roxa com gradiente antigo
- ❌ Cards com estilos inline inconsistentes
- ❌ Múltiplas definições CSS duplicadas
- ❌ Badges coloridas em cada card
- ❌ Ícones pequenos (40px) com opacidade
- ❌ 560+ linhas de CSS duplicado

### Depois (v3.0.0)
- ✅ Sidebar verde profissional com gradiente
- ✅ Cards padronizados com classes reutilizáveis
- ✅ CSS centralizado em custom.css
- ✅ Design limpo sem badges desnecessárias
- ✅ Ícones grandes (56px) com cores vibrantes
- ✅ Sistema consistente e manutenível

---

## 🎓 Guia de Estilo

### DO's ✅
- Use classes `.stats-card-clean` para cards de estatísticas
- Mantenha hierarquia visual (ícone → label → valor → subtítulo)
- Use cores de acordo com o contexto (verde = positivo, vermelho = meta)
- Aplique `.page-header-clean` em todos cabeçalhos de página
- Utilize grid Bootstrap para responsividade
- Mantenha ícones grandes e visíveis (56px)

### DON'Ts ❌
- Não use estilos inline
- Não crie classes CSS específicas por página
- Não misture padrões antigos (.stats-card-modern) com novos
- Não use cores fora da paleta definida
- Não quebre a hierarquia visual dos cards
- Não ignore responsividade mobile

---

## 🔄 Histórico de Versões

### v3.0.0 - Redesign Prescrimed
- Nova paleta de cores (verde primário)
- Design system completo
- Sidebar verde escura
- Cards com bordas coloridas
- Tipografia Inter
- Componentes reutilizáveis

### v2.9.1 - Refatoração CSS
- Eliminação de 560 linhas duplicadas
- Consolidação em custom.css
- Preparação para novo design

### v2.9.0 - Estado Anterior
- Sidebar roxa
- Cards com estilos inline
- CSS fragmentado

---

## 📞 Suporte

Para dúvidas sobre implementação:
1. Consulte exemplos em `templates/dashboard.html`
2. Verifique classes em `static/css/custom.css`
3. Siga padrões dos templates já atualizados

---

**Última atualização:** 2024  
**Responsável:** Equipe de Desenvolvimento  
**Status:** ✅ Produção
