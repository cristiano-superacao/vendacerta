# 📘 Manual Completo do Sistema de Gestão de Metas e Comissões

## 🎯 Visão Geral do Sistema

**Sistema SuaMeta** é uma plataforma completa de gestão de metas comerciais, comissões e equipes de vendas, desenvolvida com tecnologia moderna e layout responsivo profissional.

### ✨ Principais Funcionalidades

- 📊 **Dashboard Interativo** - Acompanhamento em tempo real
- 👥 **Gestão de Vendedores** - Cadastro e controle completo
- 🎯 **Gestão de Metas** - Definição e acompanhamento
- 👨‍👩‍👧‍👦 **Gestão de Equipes** - Organização por supervisores
- 💰 **Cálculo de Comissões** - Automático e configurável
- 📈 **Ranking de Performance** - Visualização de desempenho
- 📄 **Relatórios em PDF** - Exportação profissional
- 🔐 **Multi-Empresa** - Suporte a múltiplas organizações
- 📱 **Layout Responsivo** - Funciona em desktop, tablet e mobile

### 🎨 Design e Interface

- ✅ **Bootstrap 5.3.2** - Framework CSS moderno
- ✅ **Bootstrap Icons** - Ícones profissionais
- ✅ **Gradientes Modernos** - Visual atraente
- ✅ **Cards e Sombras** - Profundidade visual
- ✅ **Animações Suaves** - Transições fluidas
- ✅ **Cores Intuitivas** - Feedback visual claro

---

## 📚 Índice

1. [Arquitetura do Sistema](#arquitetura)
2. [Módulos do Sistema](#modulos)
3. [Níveis de Acesso](#niveis-acesso)
4. [Guia de Uso por Perfil](#guia-uso)
5. [Passo a Passo por Módulo](#passo-passo)
6. [Layout Responsivo](#layout-responsivo)
7. [Integrações e APIs](#integracoes)
8. [Manutenção e Suporte](#manutencao)

---

## 🏗️ 1. Arquitetura do Sistema {#arquitetura}

### Stack Tecnológico

**Backend:**
- Python 3.11+
- Flask (Framework Web)
- SQLAlchemy (ORM)
- PostgreSQL (Banco de Dados)
- Flask-Login (Autenticação)

**Frontend:**
- HTML5 + Jinja2 Templates
- CSS3 + Bootstrap 5.3.2
- JavaScript (Vanilla)
- Bootstrap Icons
- Chart.js (Gráficos)

**Infraestrutura:**
- Railway (Hospedagem)
- PostgreSQL Cloud
- Git + GitHub (Versionamento)

### Modelos de Dados

#### 1. **Empresa**
```python
- id: Identificador único
- nome: Nome da empresa
- cnpj: CNPJ único
- email: Email de contato
- plano: basico/premium/enterprise
- max_usuarios: Limite de usuários
- max_vendedores: Limite de vendedores
- ativo: Status ativo/inativo
- bloqueado: Bloqueio temporário
```

#### 2. **Usuário**
```python
- id: Identificador único
- nome: Nome completo
- email: Email único (login)
- senha_hash: Senha criptografada
- cargo: admin/supervisor/gerente/usuario/vendedor
- empresa_id: Referência à empresa
- vendedor_id: Referência ao vendedor (se cargo=vendedor)
- is_super_admin: Acesso global
- ativo: Status ativo/inativo
```

#### 3. **Vendedor**
```python
- id: Identificador único
- nome: Nome completo
- email: Email único
- telefone: Telefone de contato
- cpf: CPF único
- supervisor_id: Referência ao supervisor
- equipe_id: Referência à equipe
- empresa_id: Referência à empresa
- ativo: Status ativo/inativo
```

#### 4. **Meta**
```python
- id: Identificador único
- vendedor_id: Referência ao vendedor
- mes: Mês da meta (1-12)
- ano: Ano da meta
- valor_meta: Valor da meta em R$
- receita_alcancada: Receita conquistada
- percentual_alcance: % de alcance calculado
- comissao_total: Comissão calculada
- status_comissao: Pendente/Aprovado/Pago
- observacoes: Notas adicionais
```

#### 5. **Equipe**
```python
- id: Identificador único
- nome: Nome da equipe
- descricao: Descrição da equipe
- supervisor_id: Referência ao supervisor
- empresa_id: Referência à empresa
- ativa: Status ativa/inativa
- vendedores: Lista de vendedores
```

#### 6. **FaixaComissao**
```python
- id: Identificador único
- empresa_id: Referência à empresa (NULL = global)
- alcance_min: % mínimo de alcance
- alcance_max: % máximo de alcance
- taxa_comissao: Taxa em decimal (0.01 = 1%)
- cor: Cor para visualização
- ordem: Ordem de exibição
- ativa: Status ativa/inativa
```

### Cálculo de Comissões

**Faixas Padrão:**

| Alcance da Meta | Taxa de Comissão | Cor |
|-----------------|------------------|-----|
| 0% - 50% | 1.0% | 🔴 Vermelho |
| 51% - 75% | 1.5% | 🟡 Amarelo |
| 76% - 99% | 2.0% | 🔵 Azul |
| 100%+ | 2.5% | 🟢 Verde |

**Fórmula:**
```
Percentual de Alcance = (Receita Alcançada / Meta) × 100
Comissão = Receita Alcançada × Taxa da Faixa
```

---

## 🧩 2. Módulos do Sistema {#modulos}

### 📊 Dashboard
**Rota:** `/dashboard`  
**Acesso:** Todos os usuários autenticados

**Funcionalidades:**
- Visualização de métricas globais
- Ranking de vendedores por desempenho
- Gráficos de evolução
- Filtros por período
- Exportação para PDF

**Indicadores Exibidos:**
- Total de Vendedores
- Receita Total Alcançada
- Meta Total Definida
- Comissões Totais
- % de Alcance da Equipe
- Top 5 Vendedores

### 👥 Gestão de Vendedores
**Rota:** `/vendedores`  
**Acesso:** Admin, Supervisor

**Funcionalidades:**
- ➕ Cadastrar novo vendedor
- ✏️ Editar dados do vendedor
- 🗑️ Excluir vendedor
- 📊 Visualizar metas e performance
- 👤 Atribuir supervisor
- 👨‍👩‍👧‍👦 Associar a equipe
- 📥 Importar vendedores (Excel/CSV)
- 🔍 Buscar e filtrar vendedores

**Campos do Cadastro:**
- Nome completo
- Email
- Telefone
- CPF
- Supervisor responsável
- Equipe vinculada
- Status (Ativo/Inativo)

### 🎯 Gestão de Metas
**Rota:** `/metas`  
**Acesso:** Admin, Supervisor

**Funcionalidades:**
- ➕ Criar nova meta
- ✏️ Editar meta existente
- 🗑️ Excluir meta
- 💰 Atualizar receita alcançada
- 📊 Visualizar progresso
- 💵 Calcular comissões
- 📈 Acompanhar evolução mensal
- 📥 Importar metas (Excel)
- 📄 Exportar relatório PDF

**Campos da Meta:**
- Vendedor
- Mês/Ano
- Valor da Meta (R$)
- Receita Alcançada (R$)
- Status da Comissão
- Observações

**Cálculos Automáticos:**
- % de Alcance
- Faixa de Comissão
- Valor da Comissão
- Projeção de Comissão

### 👨‍👩‍👧‍👦 Gestão de Equipes
**Rota:** `/equipes`  
**Acesso:** Admin, Supervisor

**Funcionalidades:**
- ➕ Criar nova equipe
- ✏️ Editar equipe existente
- 🗑️ Excluir equipe
- 👥 Adicionar vendedores
- 🔍 Visualizar detalhes
- 📊 Métricas da equipe
- 👤 Definir supervisor

**Campos da Equipe:**
- Nome da equipe
- Descrição
- Supervisor responsável
- Vendedores membros
- Status (Ativa/Inativa)

### ⚙️ Configurações de Comissões
**Rota:** `/configuracoes/comissoes`  
**Acesso:** Admin

**Funcionalidades:**
- ➕ Criar faixa de comissão
- ✏️ Editar faixa existente
- 🗑️ Excluir faixa
- 🎨 Personalizar cores
- 📊 Ordenar faixas
- 👁️ Preview em tempo real

**Campos da Faixa:**
- Alcance Mínimo (%)
- Alcance Máximo (%)
- Taxa de Comissão (%)
- Cor de Visualização
- Ordem de Exibição

### 👨‍💼 Gestão de Supervisores
**Rota:** `/supervisores`  
**Acesso:** Admin

**Funcionalidades:**
- ➕ Cadastrar supervisor
- ✏️ Editar supervisor
- 🗑️ Excluir supervisor
- 📥 Importar supervisores
- 👥 Visualizar equipes supervisionadas

**Campos do Supervisor:**
- Nome completo
- Email
- Cargo
- Equipes supervisionadas
- Status (Ativo/Inativo)

### 🏢 Super Admin (Multi-Empresa)
**Rota:** `/super-admin`  
**Acesso:** Super Admin

**Funcionalidades:**
- 🏢 Gerenciar empresas
- 👥 Gerenciar usuários globais
- 📊 Dashboard consolidado
- 🔒 Bloquear/desbloquear empresas
- 💾 Backups do sistema
- ⚙️ Configurações globais

---

## 🔐 3. Níveis de Acesso {#niveis-acesso}

### 1. Super Admin 👑
**Acesso Total ao Sistema**

✅ Pode fazer:
- Gerenciar todas as empresas
- Criar/editar/excluir empresas
- Acessar dados de qualquer empresa
- Gerenciar usuários de todas as empresas
- Configurar faixas de comissão globais
- Fazer backups e restaurações
- Visualizar logs do sistema

❌ Não pode fazer:
- Nenhuma restrição

### 2. Administrador (Admin) 👨‍💼
**Controle Total da Empresa**

✅ Pode fazer:
- Gerenciar vendedores da empresa
- Criar/editar/excluir metas
- Gerenciar equipes
- Configurar faixas de comissão da empresa
- Adicionar supervisores
- Visualizar todos os relatórios
- Exportar dados
- Importar dados em lote

❌ Não pode fazer:
- Acessar dados de outras empresas
- Gerenciar empresas
- Acessar funções de super admin

### 3. Supervisor 👥
**Gerenciar Equipe de Vendas**

✅ Pode fazer:
- Visualizar vendedores da sua equipe
- Criar/editar metas dos seus vendedores
- Visualizar dashboard da equipe
- Exportar relatórios da equipe
- Atualizar receitas alcançadas
- Importar metas da equipe

❌ Não pode fazer:
- Criar/excluir vendedores
- Gerenciar outras equipes
- Configurar comissões
- Acessar dados de outras equipes

### 4. Vendedor 💼
**Visualizar Próprio Desempenho**

✅ Pode fazer:
- Visualizar suas próprias metas
- Ver seu progresso e comissões
- Ver seu ranking na equipe
- Acompanhar evolução mensal
- Exportar suas próprias metas (PDF)

❌ Não pode fazer:
- Ver dados de outros vendedores
- Editar metas
- Gerenciar qualquer recurso
- Acessar configurações

### 5. Usuário 👤
**Visualização Básica**

✅ Pode fazer:
- Visualizar dashboard geral
- Ver relatórios públicos
- Acompanhar métricas gerais

❌ Não pode fazer:
- Editar qualquer informação
- Acessar dados detalhados
- Gerenciar recursos

---

## 📖 4. Guia de Uso por Perfil {#guia-uso}

### 🎯 Para Administradores

#### Fluxo Inicial de Configuração

**1. Primeiro Acesso**
```
Login → Dashboard → Verificar dados iniciais
```

**2. Configurar Faixas de Comissão**
```
Menu → Configurações → Comissões → Criar Faixas
```

**3. Cadastrar Supervisores**
```
Menu → Supervisores → Novo Supervisor → Preencher dados
```

**4. Criar Equipes**
```
Menu → Equipes → Nova Equipe → Definir supervisor
```

**5. Cadastrar Vendedores**
```
Menu → Vendedores → Novo Vendedor → Atribuir equipe
```

**6. Definir Metas**
```
Menu → Metas → Nova Meta → Selecionar vendedor e período
```

#### Rotina Mensal

**Início do Mês:**
1. Criar metas para todos os vendedores
2. Revisar faixas de comissão (se necessário)
3. Enviar comunicado às equipes

**Durante o Mês:**
1. Atualizar receitas alcançadas
2. Acompanhar dashboard
3. Monitorar ranking
4. Exportar relatórios parciais

**Fim do Mês:**
1. Atualizar todas as receitas finais
2. Gerar relatório PDF completo
3. Aprovar comissões
4. Preparar próximo mês

### 👥 Para Supervisores

#### Fluxo de Trabalho Diário

**1. Acessar Dashboard**
```
Login → Dashboard → Filtrar por "Minha Equipe"
```

**2. Verificar Performance**
```
Dashboard → Ver Ranking → Identificar destaques e alertas
```

**3. Atualizar Receitas**
```
Menu → Metas → Editar Meta → Atualizar Receita Alcançada
```

**4. Acompanhar Equipe**
```
Menu → Equipes → Minha Equipe → Ver Detalhes
```

#### Rotina Semanal

**Segunda-feira:**
- Revisar metas da semana
- Comunicar objetivos

**Durante a Semana:**
- Atualizar receitas diariamente
- Motivar equipe
- Identificar oportunidades

**Sexta-feira:**
- Consolidar semana
- Exportar relatório semanal
- Planejar próxima semana

### 💼 Para Vendedores

#### Como Acompanhar Seu Desempenho

**1. Acessar Seu Dashboard**
```
Login → Vendedor Dashboard
```

**2. Visualizar Suas Metas**
```
Ver cards com:
- Meta do mês
- Receita alcançada
- % de progresso
- Comissão projetada
```

**3. Ver Seu Ranking**
```
Dashboard → Ranking → Localizar sua posição
```

**4. Exportar Seus Dados**
```
Metas → Exportar PDF → Salvar comprovante
```

---

## 📝 5. Passo a Passo por Módulo {#passo-passo}

### 📊 Módulo: Dashboard

#### Como Usar o Dashboard

**1. Acessar Dashboard**
- Após login, você é redirecionado automaticamente
- Ou clique em "Dashboard" no menu

**2. Entender os Cards de Resumo**
```
┌─────────────────────────────────────────────────┐
│ 👥 Total de Vendedores          📈 45           │
│ 💰 Receita Total                💵 R$ 2.5M     │
│ 🎯 Meta Total                   🎯 R$ 3.0M     │
│ 💵 Comissões Totais            💸 R$ 50K       │
│ 📊 % Alcance da Equipe          📈 83.3%       │
└─────────────────────────────────────────────────┘
```

**3. Usar Filtros**
- **Por Período:** Selecione mês e ano
- **Por Equipe:** Filtre equipe específica
- **Por Supervisor:** Veja apenas sua equipe

**4. Analisar Ranking**
```
Ranking exibe:
- 🥇 Posição do vendedor
- 👤 Nome e supervisor
- 🎯 Meta vs Receita
- 📊 % de Alcance
- 💵 Comissão calculada
- 📈 Barra de progresso visual
- 🎨 Cor por faixa de desempenho
```

**5. Exportar Relatório**
- Clique em "📄 Exportar PDF"
- PDF gerado com todos os dados
- Salve ou imprima

### 👥 Módulo: Vendedores

#### Como Cadastrar Vendedor

**Passo 1: Acessar Lista**
```
Menu → Vendedores → Lista de Vendedores
```

**Passo 2: Iniciar Cadastro**
```
Botão "➕ Novo Vendedor" (canto superior direito)
```

**Passo 3: Preencher Formulário**
```
┌─────────────────────────────────────────────┐
│ 📝 Dados do Vendedor                        │
├─────────────────────────────────────────────┤
│ Nome Completo: [________________]           │
│ Email:         [________________]           │
│ Telefone:      [________________]           │
│ CPF:           [___.___.___-__]            │
│                                             │
│ 👤 Atribuições                              │
│ Supervisor:    [Selecione ▼]               │
│ Equipe:        [Selecione ▼]               │
│                                             │
│ Status:        ☑ Ativo                     │
│                                             │
│ [Cancelar]  [💾 Salvar Vendedor]          │
└─────────────────────────────────────────────┘
```

**Passo 4: Validações Automáticas**
- ✅ Email único
- ✅ CPF válido
- ✅ Telefone formatado
- ✅ Campos obrigatórios preenchidos

**Passo 5: Confirmar**
- Clique em "Salvar"
- Vendedor aparece na lista
- Mensagem de sucesso exibida

#### Como Importar Vendedores em Lote

**Passo 1: Baixar Template**
```
Vendedores → Importar → Baixar Template Excel
```

**Passo 2: Preencher Planilha**
```excel
| Nome          | Email              | Telefone      | CPF            | Supervisor | Equipe    |
|---------------|--------------------|---------------|----------------|------------|-----------|
| João Silva    | joao@email.com     | 71999887766   | 123.456.789-00 | Maria      | Vendas 1  |
| Ana Santos    | ana@email.com      | 71988776655   | 987.654.321-00 | Maria      | Vendas 1  |
```

**Passo 3: Upload**
```
Vendedores → Importar → Escolher Arquivo → Upload
```

**Passo 4: Validação**
- Sistema valida cada linha
- Exibe erros se houver
- Confirma importação

**Passo 5: Confirmar**
- Vendedores importados aparecem na lista
- Recebem email de boas-vindas (se configurado)

#### Como Editar Vendedor

**Passo 1: Localizar**
```
Vendedores → 🔍 Buscar → Digite nome ou email
```

**Passo 2: Abrir Edição**
```
Clique no botão "✏️ Editar" na linha do vendedor
```

**Passo 3: Modificar Dados**
- Altere os campos desejados
- Sistema valida automaticamente

**Passo 4: Salvar**
```
Botão "💾 Salvar Alterações"
```

#### Como Desativar Vendedor

**Passo 1: Localizar Vendedor**
```
Vendedores → Encontre na lista
```

**Passo 2: Editar**
```
Clique em "✏️ Editar"
```

**Passo 3: Desmarcar Ativo**
```
☐ Ativo (desmarque o checkbox)
```

**Passo 4: Salvar**
- Vendedor fica inativo
- Não aparece em seleções
- Mantém histórico de metas

### 🎯 Módulo: Metas

#### Como Criar Meta

**Passo 1: Acessar Metas**
```
Menu → Metas → Lista de Metas
```

**Passo 2: Nova Meta**
```
Botão "➕ Nova Meta"
```

**Passo 3: Preencher Formulário**
```
┌─────────────────────────────────────────────┐
│ 🎯 Nova Meta                                │
├─────────────────────────────────────────────┤
│ Vendedor:      [Selecione ▼]               │
│ Mês:           [Janeiro ▼]                 │
│ Ano:           [2025 ▼]                    │
│ Valor da Meta: [R$ ________]               │
│                                             │
│ 📊 Projeção de Comissão                    │
│ Meta 100%:     R$ 2.500,00                 │
│ Comissão:      R$ 62,50 (2.5%)            │
│                                             │
│ [Cancelar]  [💾 Criar Meta]                │
└─────────────────────────────────────────────┘
```

**Passo 4: Validações**
- ✅ Vendedor ativo
- ✅ Período único (1 meta por vendedor/mês)
- ✅ Valor da meta > 0

**Passo 5: Confirmar**
- Meta criada
- Aparece na lista
- Vendedor pode visualizar

#### Como Atualizar Receita Alcançada

**Passo 1: Encontrar Meta**
```
Metas → Filtrar por vendedor/período
```

**Passo 2: Editar Meta**
```
Clique em "✏️ Editar" na meta desejada
```

**Passo 3: Atualizar Receita**
```
┌─────────────────────────────────────────────┐
│ 💰 Receita Alcançada                        │
│ Valor: [R$ ________]                       │
│                                             │
│ 📊 Cálculo Automático                      │
│ Meta:      R$ 50.000,00                    │
│ Receita:   R$ 42.500,00                    │
│ Alcance:   85% 🟡                          │
│ Comissão:  R$ 850,00 (2.0%)               │
└─────────────────────────────────────────────┘
```

**Passo 4: Salvar**
- Sistema recalcula automaticamente:
  - % de Alcance
  - Faixa de Comissão
  - Valor da Comissão

#### Como Importar Metas em Lote

**Passo 1: Preparar Planilha**
```excel
| Vendedor      | Mês | Ano  | Meta (R$) | Receita (R$) |
|---------------|-----|------|-----------|--------------|
| João Silva    | 12  | 2025 | 50000     | 42500        |
| Ana Santos    | 12  | 2025 | 45000     | 48000        |
```

**Passo 2: Importar**
```
Metas → Importar → Escolher Arquivo → Upload
```

**Passo 3: Validar**
- Sistema valida vendedores
- Verifica duplicatas
- Calcula comissões

**Passo 4: Confirmar**
- Metas importadas
- Comissões calculadas
- Relatório de importação exibido

### 👨‍👩‍👧‍👦 Módulo: Equipes

#### Como Criar Equipe

**Passo 1: Acessar Equipes**
```
Menu → Equipes → Lista de Equipes
```

**Passo 2: Nova Equipe**
```
Botão "➕ Nova Equipe"
```

**Passo 3: Preencher Dados**
```
┌─────────────────────────────────────────────┐
│ 👨‍👩‍👧‍👦 Nova Equipe                              │
├─────────────────────────────────────────────┤
│ Nome:         [________________]            │
│ Descrição:    [________________]            │
│               [________________]            │
│ Supervisor:   [Selecione ▼]                │
│ Status:       ☑ Ativa                      │
│                                             │
│ [Cancelar]  [💾 Criar Equipe]              │
└─────────────────────────────────────────────┘
```

**Passo 4: Salvar**
- Equipe criada
- Supervisor pode adicionar vendedores
- Aparece em seleções

#### Como Adicionar Vendedores à Equipe

**Opção 1: Ao Cadastrar Vendedor**
```
Vendedores → Novo → Selecionar Equipe no formulário
```

**Opção 2: Editar Vendedor Existente**
```
Vendedores → Editar → Alterar Equipe
```

**Opção 3: Importar em Lote**
```
Vendedores → Importar → Coluna "Equipe" na planilha
```

#### Como Ver Detalhes da Equipe

**Passo 1: Acessar Detalhes**
```
Equipes → Clique em "👁️ Ver Detalhes"
```

**Passo 2: Visualizar Informações**
```
┌─────────────────────────────────────────────┐
│ 📊 Equipe Vendas 1                          │
├─────────────────────────────────────────────┤
│ 👤 Supervisor: Maria Silva                  │
│ 👥 Total de Vendedores: 8                   │
│ 📈 Meta Total: R$ 400.000,00               │
│ 💰 Receita Total: R$ 350.000,00            │
│ 📊 % Alcance: 87.5%                        │
│ 💵 Comissões: R$ 7.000,00                  │
├─────────────────────────────────────────────┤
│ 👥 Membros da Equipe                        │
│ 1. João Silva    - 95% 🟢                  │
│ 2. Ana Santos    - 106% 🟢                 │
│ 3. Pedro Costa   - 80% 🟡                  │
│ ...                                         │
└─────────────────────────────────────────────┘
```

### ⚙️ Módulo: Configurações de Comissões

#### Como Criar Faixa de Comissão

**Passo 1: Acessar Configurações**
```
Menu → Configurações → Comissões
```

**Passo 2: Nova Faixa**
```
Botão "➕ Nova Faixa"
```

**Passo 3: Preencher Formulário**
```
┌─────────────────────────────────────────────┐
│ ⚙️ Nova Faixa de Comissão                   │
├─────────────────────────────────────────────┤
│ 📊 Faixa de Alcance                         │
│ Mínimo: [___]% até Máximo: [___]%          │
│                                             │
│ 💰 Taxa de Comissão                         │
│ Taxa:   [___]%                             │
│                                             │
│ 🎨 Cor de Visualização                      │
│ ● Vermelho  ● Amarelo  ● Azul  ● Verde     │
│                                             │
│ 📋 Ordem de Exibição                        │
│ Ordem:  [___]                              │
│                                             │
│ 👁️ Preview                                  │
│ ┌─────────────────┐                        │
│ │  76% - 99%     │                        │
│ │     2.0%       │                        │
│ └─────────────────┘                        │
│                                             │
│ [Cancelar]  [💾 Criar Faixa]               │
└─────────────────────────────────────────────┘
```

**Passo 4: Preview em Tempo Real**
- Ao digitar, preview atualiza
- Visualize como ficará no sistema

**Passo 5: Salvar**
- Faixa criada
- Passa a valer para novos cálculos
- Metas existentes podem ser recalculadas

#### Como Ordenar Faixas

**Passo 1: Definir Ordem**
- Ordem 0 = primeira faixa
- Ordem 1 = segunda faixa
- E assim por diante

**Passo 2: Editar Faixas**
```
Para cada faixa, defina:
- Ordem: 0 (0-50%)
- Ordem: 1 (51-75%)
- Ordem: 2 (76-99%)
- Ordem: 3 (100%+)
```

**Passo 3: Sistema Ordena Automaticamente**
- Lista exibe por ordem crescente
- Cards no dashboard seguem a ordem

---

## 📱 6. Layout Responsivo {#layout-responsivo}

### Conceito de Design Responsivo

O sistema se adapta automaticamente a diferentes tamanhos de tela:

#### 🖥️ Desktop (> 1200px)
```
┌────────────────────────────────────────────────────────────┐
│  🎯 SuaMeta        Dashboard  Vendedores  Metas  Equipes  │
├────────────────────────────────────────────────────────────┤
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐           │
│  │ 👥45 │ │💰2.5M│ │🎯3.0M│ │💵50K │ │📊83%│           │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘           │
│  ┌────────────────────────────────────────────┐           │
│  │ 📊 Ranking de Vendedores                   │           │
│  │ 🥇 João Silva  - 106% 🟢 - R$ 2.650,00    │           │
│  │ 🥈 Ana Santos  - 95%  🟡 - R$ 1.900,00    │           │
│  └────────────────────────────────────────────┘           │
└────────────────────────────────────────────────────────────┘
```

#### 💻 Tablet (768px - 1199px)
```
┌──────────────────────────────────────┐
│  🎯 SuaMeta         ☰               │
├──────────────────────────────────────┤
│  ┌──────┐ ┌──────┐ ┌──────┐        │
│  │ 👥45 │ │💰2.5M│ │🎯3.0M│        │
│  └──────┘ └──────┘ └──────┘        │
│  ┌──────┐ ┌──────┐                 │
│  │💵50K │ │📊83%│                 │
│  └──────┘ └──────┘                 │
│  ┌────────────────────────┐        │
│  │ 📊 Ranking             │        │
│  │ 🥇 João - 106% 🟢      │        │
│  └────────────────────────┘        │
└──────────────────────────────────────┘
```

#### 📱 Mobile (< 768px)
```
┌─────────────────────┐
│  🎯 SuaMeta    ☰   │
├─────────────────────┤
│  ┌───────────────┐  │
│  │   👥 45       │  │
│  │  Vendedores   │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │  💰 R$ 2.5M   │  │
│  │  Receita      │  │
│  └───────────────┘  │
│  ┌───────────────┐  │
│  │  🎯 R$ 3.0M   │  │
│  │  Meta         │  │
│  └───────────────┘  │
│  📊 Ranking         │
│  🥇 João - 106% 🟢  │
│  🥈 Ana - 95% 🟡    │
└─────────────────────┘
```

### Elementos Responsivos

#### ✅ Menu de Navegação
- **Desktop:** Barra horizontal completa
- **Tablet:** Menu condensado
- **Mobile:** Menu hamburguer (☰)

#### ✅ Cards de Métricas
- **Desktop:** 5 cards em linha
- **Tablet:** 2-3 cards por linha
- **Mobile:** 1 card por linha (stacked)

#### ✅ Tabelas
- **Desktop:** Todas as colunas visíveis
- **Tablet:** Colunas importantes + scroll horizontal
- **Mobile:** Cards verticais ao invés de tabela

#### ✅ Formulários
- **Desktop:** 2-3 colunas
- **Tablet:** 2 colunas
- **Mobile:** 1 coluna (full width)

#### ✅ Botões
- **Desktop:** Tamanho normal com ícone + texto
- **Tablet:** Tamanho médio
- **Mobile:** Tamanho grande (touch-friendly)

### Breakpoints do Sistema

```css
/* Mobile First */
/* Mobile: 0px - 767px (padrão) */

/* Tablet */
@media (min-width: 768px) {
  /* Estilos para tablet */
}

/* Desktop */
@media (min-width: 992px) {
  /* Estilos para desktop */
}

/* Large Desktop */
@media (min-width: 1200px) {
  /* Estilos para telas grandes */
}
```

### Componentes Adaptáveis

#### 1. Cards Responsivos
```html
<!-- Adapta de 1 coluna (mobile) a 5 colunas (desktop) -->
<div class="row">
  <div class="col-12 col-md-6 col-lg-4 col-xl-2">
    <div class="card"><!-- Card --></div>
  </div>
</div>
```

#### 2. Tabelas Responsivas
```html
<!-- Scroll horizontal em mobile -->
<div class="table-responsive">
  <table class="table"><!-- Tabela --></table>
</div>
```

#### 3. Modais Responsivos
```html
<!-- Se adapta ao tamanho da tela -->
<div class="modal-dialog modal-lg modal-dialog-centered">
  <!-- Conteúdo -->
</div>
```

---

## 🔌 7. Integrações e APIs {#integracoes}

### APIs Disponíveis

#### 1. API de Ranking
**Endpoint:** `/api/ranking`  
**Método:** GET  
**Autenticação:** Necessária

**Parâmetros:**
```json
{
  "mes": 12,
  "ano": 2025,
  "equipe_id": 1  // Opcional
}
```

**Resposta:**
```json
{
  "success": true,
  "data": [
    {
      "vendedor_id": 1,
      "nome": "João Silva",
      "meta": 50000.00,
      "receita": 53000.00,
      "percentual": 106.0,
      "comissao": 1325.00,
      "faixa": "success"
    }
  ]
}
```

#### 2. API de Faixas de Comissão
**Endpoint:** `/api/comissoes/faixas`  
**Método:** GET  
**Autenticação:** Necessária

**Resposta:**
```json
{
  "success": true,
  "faixas": [
    {
      "id": 1,
      "alcance_min": 0,
      "alcance_max": 50,
      "taxa_comissao": 0.01,
      "taxa_percentual": 1.0,
      "cor": "danger",
      "ordem": 0
    }
  ]
}
```

### Exportação de Dados

#### PDF
- **Formato:** Adobe PDF
- **Geração:** Servidor (reportlab)
- **Conteúdo:** Tabelas, gráficos, métricas
- **Personalização:** Logo, cabeçalho, rodapé

#### Excel (Importação)
- **Formato:** .xlsx, .csv
- **Biblioteca:** openpyxl, pandas
- **Validação:** Automática no upload
- **Feedback:** Relatório de erros/sucessos

---

## 🔧 8. Manutenção e Suporte {#manutencao}

### Backup do Sistema

#### Backup Automático (Super Admin)
```
Super Admin → Backups → Criar Backup
```

**O que é incluído:**
- ✅ Todos os dados do banco
- ✅ Configurações do sistema
- ✅ Faixas de comissão
- ✅ Histórico completo

**Frequência Recomendada:**
- 📅 Diário: Produção ativa
- 📅 Semanal: Uso moderado
- 📅 Mensal: Uso esporádico

#### Restauração de Backup
```
Super Admin → Backups → Restaurar → Selecionar Arquivo
```

### Logs e Auditoria

#### Informações Registradas
- 📝 Login/Logout de usuários
- ✏️ Criação/edição/exclusão de registros
- 💰 Cálculos de comissões
- 📊 Exportações de relatórios
- ❌ Erros do sistema

#### Como Acessar Logs
```
Super Admin → Logs → Filtrar por período/tipo
```

### Suporte Técnico

#### Canais de Atendimento

**📞 WhatsApp:** (71) 99337-2960  
**📧 Email:** cristiano.s.santos@ba.estudante.senai.br

**⏰ Horário:**
- Segunda a Sexta: 8h às 18h
- Sábado: 8h às 12h

#### Níveis de Suporte

**🟢 Nível 1 - Dúvidas de Uso**
- Como usar funcionalidades
- Navegação no sistema
- Interpretação de relatórios
- **SLA:** 2 horas úteis

**🟡 Nível 2 - Problemas Técnicos**
- Erros ao salvar dados
- Problemas de acesso
- Importações com erro
- **SLA:** 4 horas úteis

**🔴 Nível 3 - Crítico**
- Sistema fora do ar
- Perda de dados
- Falhas graves
- **SLA:** 1 hora (imediato)

### Atualizações do Sistema

#### Versionamento
```
Versão Atual: 2.9.1
- 2: Major (mudanças grandes)
- 9: Minor (novas funcionalidades)
- 1: Patch (correções)
```

#### Changelog
- Todas as atualizações documentadas
- Arquivo: `CHANGELOG.md`
- Histórico completo de versões

#### Como Atualizar
```bash
# Railway faz deploy automático ao push
git pull origin main
# Sistema atualiza automaticamente
```

---

## 📚 Apêndices

### A. Glossário

| Termo | Significado |
|-------|-------------|
| **Alcance** | Percentual da meta atingido |
| **Comissão** | Valor pago ao vendedor por desempenho |
| **Dashboard** | Painel de controle com métricas |
| **Faixa** | Intervalo de alcance com taxa específica |
| **Meta** | Objetivo de vendas em valor (R$) |
| **Ranking** | Classificação por desempenho |
| **Receita** | Valor em vendas alcançado |
| **Supervisor** | Responsável por equipe de vendedores |

### B. Atalhos do Teclado

| Atalho | Ação |
|--------|------|
| `Ctrl + K` | Abrir busca global |
| `Ctrl + N` | Novo registro |
| `Ctrl + S` | Salvar formulário |
| `Esc` | Fechar modal/cancelar |
| `Ctrl + P` | Exportar PDF |

### C. Cores e Significados

| Cor | Significado | Uso |
|-----|-------------|-----|
| 🔴 Vermelho | Baixo desempenho | 0-50% |
| 🟡 Amarelo | Desempenho médio | 51-75% |
| 🔵 Azul | Bom desempenho | 76-99% |
| 🟢 Verde | Excelente desempenho | 100%+ |
| ⚫ Cinza | Inativo/Desabilitado | - |

### D. Fórmulas e Cálculos

**Percentual de Alcance:**
```
% Alcance = (Receita Alcançada ÷ Meta) × 100
```

**Comissão:**
```
Comissão = Receita Alcançada × Taxa da Faixa
```

**Exemplo:**
```
Meta: R$ 50.000,00
Receita: R$ 42.500,00
% Alcance: (42.500 ÷ 50.000) × 100 = 85%
Faixa: 76-99% = 2.0%
Comissão: R$ 42.500 × 0.02 = R$ 850,00
```

### E. Perguntas Frequentes

**1. Posso ter várias metas para o mesmo vendedor no mesmo mês?**
Não. O sistema permite apenas 1 meta por vendedor por mês/ano.

**2. As comissões são calculadas automaticamente?**
Sim. Sempre que a receita é atualizada, o sistema recalcula.

**3. Posso customizar as faixas de comissão?**
Sim. Admins podem criar faixas personalizadas por empresa.

**4. Como funciona o acesso multi-empresa?**
Cada empresa tem seus dados isolados. Super Admin vê tudo.

**5. O sistema funciona offline?**
Não. Requer conexão com internet para acessar o banco de dados.

**6. Posso exportar todos os dados?**
Sim. Admins podem exportar relatórios completos em PDF.

**7. Como recupero minha senha?**
Use "Esqueceu a senha?" na tela de login.

**8. Vendedores podem editar suas metas?**
Não. Apenas visualizam. Supervisores e Admins editam.

---

## 🎓 Treinamento Recomendado

### Para Novos Usuários (2 horas)

**Módulo 1: Introdução (30 min)**
- Visão geral do sistema
- Login e navegação
- Dashboard e métricas

**Módulo 2: Cadastros Básicos (45 min)**
- Cadastrar vendedores
- Criar metas
- Atualizar receitas

**Módulo 3: Relatórios (30 min)**
- Interpretar ranking
- Exportar PDF
- Filtros e buscas

**Módulo 4: Prática (15 min)**
- Exercícios práticos
- Dúvidas e suporte

### Para Administradores (4 horas)

**Módulo 1: Configuração Inicial (1h)**
- Criar empresa
- Configurar comissões
- Cadastrar supervisores
- Criar equipes

**Módulo 2: Gestão de Dados (1h30)**
- Importação em lote
- Edição de registros
- Validações e regras

**Módulo 3: Relatórios Avançados (1h)**
- Análise de performance
- Exportações personalizadas
- Dashboards por equipe

**Módulo 4: Administração (30 min)**
- Backups
- Logs
- Manutenção

---

## 📞 Contato e Recursos

### Desenvolvedor

**Cristiano Santos**  
💼 Desenvolvedor Full Stack  
📱 (71) 99337-2960  
📧 cristiano.s.santos@ba.estudante.senai.br  

### Links Úteis

- 🌐 **Sistema:** https://vendacerta.up.railway.app
- 📚 **Documentação:** `/docs`
- 🐛 **Reportar Bugs:** GitHub Issues
- 💡 **Sugestões:** Email ou WhatsApp

### Recursos Online

- ✅ Manual do Usuário (este documento)
- ✅ Vídeos tutoriais (em breve)
- ✅ Base de conhecimento
- ✅ FAQ completo

---

**© 2025 Sistema SuaMeta - Todos os direitos reservados**

*Este manual foi atualizado em: 14/12/2025*  
*Versão do Sistema: 2.9.1*  
*Versão do Manual: 1.0.0*
