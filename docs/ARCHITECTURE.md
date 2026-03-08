# 🏗️ Arquitetura do Sistema VendaCerta

> **Documentação técnica completa da arquitetura, componentes e integrações**

---

## 📊 Visão Geral da Arquitetura

### Modelo de Arquitetura: MVC (Model-View-Controller)

```mermaid
graph TB
    subgraph Cliente
        Browser[🌐 Navegador]
        PWA[📱 PWA App]
    end
    
    subgraph Servidor[Flask Application Server]
        Routes[📍 Routes/Controllers]
        Models[🗄️ Models/ORM]
        Templates[🎨 Templates/Views]
        Helpers[🔧 Helpers/Utils]
    end
    
    subgraph Database[💾 PostgreSQL 15]
        Tables[16 Tabelas]
        Indexes[Índices Performance]
        Constraints[Constraints/FKs]
    end
    
    subgraph External[🔌 Serviços Externos]
        Railway[Railway Platform]
        Excel[Excel Import/Export]
        PDF[ReportLab PDFs]
    end
    
    Browser --> Routes
    PWA --> Routes
    Routes --> Helpers
    Routes --> Models
    Routes --> Templates
    Models --> Tables
    Tables --> Indexes
    Tables --> Constraints
    Templates --> Browser
    Templates --> PWA
    Routes --> Excel
    Routes --> PDF
    Servidor --> Railway
```

---

## 🗂️ Estrutura de Diretórios

```
vendacerta/
│
├── app.py                      # 🚀 Aplicação principal Flask (119 rotas)
├── models.py                   # 🗄️ 16 Models SQLAlchemy
├── forms.py                    # 📋 Formulários WTForms com validação
├── helpers.py                  # 🔧 Funções auxiliares e permissões
├── config.py                   # ⚙️ Configurações (dev/prod)
├── wsgi.py                     # 🌐 Entry point WSGI (Gunicorn)
│
├── calculo_comissao.py         # 💰 Engine de cálculo de comissões
├── calculo_projecao.py         # 📈 Projeções de metas
├── calculo_balanceamento.py   # ⚖️ Balanceamento de equipes
├── pdf_generator.py            # 📄 Geração de relatórios PDF
│
├── migrations_scripts/         # 🔄 Scripts de migração de banco
│   ├── adicionar_supervisor_id.py
│   ├── criar_tabelas_estoque.py
│   └── migrar_permissoes_granulares.py
│
├── templates/                  # 🎨 64 templates HTML (Bootstrap 5.3.3)
│   ├── base.html              # Layout base responsivo
│   ├── dashboard.html         # Dashboard principal
│   ├── clientes/              # 8 templates
│   ├── vendedores/            # 7 templates
│   ├── metas/                 # 4 templates
│   ├── estoque/               # 7 templates
│   ├── os/                    # 6 templates
│   ├── equipes/               # 3 templates
│   ├── configuracoes/         # 2 templates
│   ├── supervisor/            # 4 templates
│   ├── vendedor/              # 2 templates
│   └── super_admin/           # 7 templates
│
├── static/                     # 📦 Arquivos estáticos
│   ├── css/
│   ├── js/
│   ├── images/
│   └── templates_excel/       # Modelos importação
│
├── instance/                   # 💾 Dados locais (SQLite dev)
│   └── vendacerta.db
│
└── docs/                       # 📚 Documentação completa
    ├── ARCHITECTURE.md        # Este arquivo
    ├── API.md                 # Documentação API REST
    └── GETTING_STARTED.md     # Guia rápido início
```

---

## 🗄️ Modelos de Dados (16 Models)

### Diagrama Entidade-Relacionamento (Principal)

```mermaid
erDiagram
    EMPRESA ||--o{ USUARIO : possui
    EMPRESA ||--o{ VENDEDOR : possui
    EMPRESA ||--o{ CLIENTE : possui
    EMPRESA ||--o{ META : possui
    EMPRESA ||--o{ PRODUTO : possui
    EMPRESA ||--o{ ORDEM_SERVICO : possui
    
    USUARIO ||--o{ VENDEDOR : gerencia
    USUARIO ||--o{ EQUIPE : supervisiona
    USUARIO ||--o{ ORDEM_SERVICO : cria
    
    VENDEDOR ||--o{ META : tem
    VENDEDOR ||--o{ EQUIPE : pertence
    VENDEDOR }o--|| USUARIO : vinculado_a
    
    CLIENTE ||--o{ COMPRA_CLIENTE : realiza
    CLIENTE ||--o{ ORDEM_SERVICO : solicita
    
    PRODUTO ||--o{ ESTOQUE_MOVIMENTO : registra
    
    EQUIPE ||--o{ VENDEDOR : contém
    
    META }o--|| VENDEDOR : atribuida_a
    META }o--|| FAIXA_COMISSAO : calcula_por
    
    ORDEM_SERVICO }o--|| CLIENTE : para
    ORDEM_SERVICO }o--|| TECNICO : executada_por
```

### Tabelas e Relacionamentos

| # | Model | Tabela | Chave Estrangeira | Relação |
|---|-------|--------|-------------------|---------|
| 1 | **Empresa** | empresas | - | Multi-tenant raiz |
| 2 | **Usuario** | usuarios | empresa_id → empresas | N:1 com Empresa |
| 3 | **Vendedor** | vendedores | empresa_id, usuario_id, gerente_id, equipe_id | N:1 com Empresa, Usuario, Equipe |
| 4 | **Meta** | metas | empresa_id, vendedor_id | N:1 com Empresa, Vendedor |
| 5 | **Equipe** | equipes | empresa_id, supervisor_id | N:1 com Empresa, Usuario |
| 6 | **Cliente** | clientes | empresa_id | N:1 com Empresa |
| 7 | **CompraCliente** | compras_clientes | empresa_id, cliente_id | N:1 com Cliente |
| 8 | **Produto** | produtos | empresa_id | N:1 com Empresa |
| 9 | **EstoqueMovimento** | estoque_movimentos | empresa_id, produto_id, usuario_id | N:1 com Produto, Usuario |
| 10 | **OrdemServico** | ordens_servico | empresa_id, cliente_id, tecnico_id, criado_por_id, aprovado_por_id | N:1 com Cliente, Tecnico, Usuario |
| 11 | **Tecnico** | tecnicos | empresa_id, usuario_id | N:1 com Empresa, Usuario |
| 12 | **FaixaComissao** | faixas_comissao | empresa_id | N:1 com Empresa |
| 13 | **FaixaComissaoVendedor** | faixas_comissao_vendedor | empresa_id, vendedor_id | N:1 com Vendedor |
| 14 | **FaixaComissaoSupervisor** | faixas_comissao_supervisor | empresa_id, supervisor_id | N:1 com Usuario |
| 15 | **Mensagem** | mensagens | empresa_id, remetente_id, destinatario_id | N:1 com Usuario |
| 16 | **Configuracao** | configuracoes | empresa_id | N:1 com Empresa |

---

## 🔐 Hierarquia de Permissões

### 10 Cargos Implementados

```mermaid
graph TD
    SA[👑 Super Admin] --> A[🏢 Admin]
    A --> G[👔 Gerente]
    G --> S[🎯 Supervisor]
    S --> V[💼 Vendedor]
    S --> T[🔧 Técnico]
    
    A --> ADM[📊 Administrativo]
    A --> FIN[💰 Financeiro]
    A --> RH[👥 RH]
    A --> U[👤 Usuário]
    
    style SA fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style A fill:#4c6ef5,stroke:#364fc7,color:#fff
    style G fill:#7950f2,stroke:#5f3dc4,color:#fff
    style S fill:#f59f00,stroke:#e67700,color:#fff
    style V fill:#51cf66,stroke:#37b24d,color:#fff
    style T fill:#22b8cf,stroke:#0b7285,color:#fff
    style ADM fill:#868e96,stroke:#495057,color:#fff
    style FIN fill:#ffa94d,stroke:#fd7e14,color:#fff
    style RH fill:#ff8787,stroke:#fa5252,color:#fff
    style U fill:#adb5bd,stroke:#868e96,color:#fff
```

### Matriz de Permissões (24 Flags)

| Permissão | Super Admin | Admin | Gerente | Supervisor | Vendedor | Técnico | Outros |
|-----------|:-----------:|:-----:|:-------:|:----------:|:--------:|:-------:|:------:|
| **pode_gerenciar_empresas** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **pode_gerenciar_usuarios** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **pode_gerenciar_vendedores** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **pode_gerenciar_metas** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **pode_ver_relatorios** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| **pode_gerenciar_clientes** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **pode_gerenciar_estoque** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **pode_criar_os** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **pode_aprovar_os** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **pode_executar_os** | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **pode_exportar_clientes** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **pode_importar_excel** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **pode_ver_comissoes** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **pode_configurar_comissoes** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **pode_gerenciar_equipes** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **pode_ver_dashboard** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **pode_editar_proprias_metas** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **pode_ver_apenas_proprios** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |

**Total de Permissões Implementadas**: 24 flags booleanas no modelo Usuario

---

## 📍 Mapeamento de Rotas (119 Endpoints)

### Distribuição por Módulo

| Módulo | Rotas | Templates | Models Principais |
|--------|:-----:|:---------:|-------------------|
| **Autenticação** | 7 | 5 | Usuario |
| **Dashboard** | 5 | 3 | Vendedor, Meta, Cliente |
| **Super Admin** | 17 | 7 | Empresa, Usuario, Backup |
| **Supervisores** | 7 | 4 | Usuario |
| **Vendedores** | 13 | 7 | Vendedor, Usuario |
| **Funcionários** | 5 | 2 | Usuario |
| **Clientes** | 11 | 8 | Cliente, CompraCliente |
| **Mensagens** | 8 | 5 | Mensagem |
| **Metas** | 7 | 4 | Meta, FaixaComissao |
| **Equipes** | 5 | 3 | Equipe |
| **Comissões** | 3 | 2 | FaixaComissao |
| **Estoque** | 11 | 7 | Produto, EstoqueMovimento |
| **Ordens de Serviço** | 9 | 6 | OrdemServico, Tecnico, Cliente |
| **Relatórios** | 2 | 1 | Meta, Vendedor, Usuario |
| **API/Utilities** | 10 | 0 | Variados |
| **TOTAL** | **119** | **64** | **16 models** |

### Exemplos de Rotas Principais

#### Dashboard e Autenticação
```
GET  /                          → dashboard.html (redirecionamento baseado em cargo)
GET  /dashboard                 → dashboard.html (admin/gerente)
GET  /supervisor/dashboard      → supervisor/dashboard.html
GET  /vendedor/dashboard        → vendedor/dashboard.html
GET  /login                     → login.html
POST /login                     → Autenticação + redirecionamento
GET  /logout                    → Logout + redirect
GET  /registro                  → registro.html
POST /registro                  → Criar novo usuário
```

#### Gestão de Vendedores
```
GET  /vendedores                → vendedores/lista.html
GET  /vendedores/novo           → vendedores/form.html
POST /vendedores/novo           → Criar vendedor
GET  /vendedores/<id>/editar    → vendedores/form.html (edição)
POST /vendedores/<id>/editar    → Atualizar vendedor
POST /vendedores/<id>/deletar   → Deletar vendedor
GET  /vendedores/importar       → vendedores/importar.html
POST /vendedores/importar       → Processar Excel
```

#### Gestão de Metas
```
GET  /metas                     → metas/lista.html
GET  /metas/nova                → metas/form.html
POST /metas/nova                → Criar meta
GET  /metas/<id>/editar         → metas/form.html
POST /metas/<id>/editar         → Atualizar meta (recalcula comissão)
POST /metas/<id>/deletar        → Deletar meta
GET  /metas/configurar          → metas/configurar.html (faixas)
```

#### Gestão de Clientes
```
GET  /clientes                  → clientes/lista.html
GET  /clientes/novo             → clientes/form.html
POST /clientes/novo             → Criar cliente
GET  /clientes/<id>             → clientes/ver.html (detalhes + compras)
GET  /clientes/<id>/editar      → clientes/form.html
POST /clientes/<id>/editar      → Atualizar cliente
POST /clientes/<id>/deletar     → Deletar cliente
GET  /clientes/exportar         → CSV download
GET  /clientes/modelo-importacao → XLSX template download
POST /clientes/importar         → Processar Excel (11/18/23 colunas)
```

#### Gestão de Estoque
```
GET  /estoque                   → estoque/dashboard.html
GET  /estoque/produtos          → estoque/produtos.html
GET  /estoque/produtos/novo     → estoque/produto_form.html
GET  /estoque/produtos/<id>     → estoque/produto_visualizar.html
GET  /estoque/movimentacoes     → estoque/movimentacoes.html
POST /estoque/movimentacao/nova → Criar movimento
GET  /estoque/importar-produtos → estoque/importar_produtos.html
```

#### Ordens de Serviço
```
GET  /os                        → os/lista.html
GET  /os/nova                   → os/nova.html
POST /os/nova                   → Criar OS
GET  /os/<id>                   → os/visualizar.html
GET  /os/<id>/atualizar         → os/atualizar.html (técnico)
POST /os/<id>/aprovar           → Aprovar OS (supervisor)
GET  /os/<id>/avaliar           → os/avaliar.html (cliente)
GET  /os/<id>/pdf               → Gerar PDF da OS
POST /os/<id>/cancelar          → Cancelar OS
```

#### API REST
```
GET  /api/ranking               → JSON ranking vendedores
GET  /api/comissoes/faixas      → JSON faixas de comissão
GET  /api/metas/dados-grafico/<vendedor_id> → JSON dados gráficos
GET  /api/vendedor/<id>/supervisor → JSON info supervisor
GET  /health                    → Health check (Railway)
GET  /ping                      → Ping endpoint
```

---

## 📈 Relatório de Metas Avançado (Vendedor/Supervisor)

### Rota e Template
- Página: `/relatorios/metas-avancado`
- Template: `templates/relatorios/metas_avancado.html`

### Parâmetros de Query
- `visao`: `vendedor` (padrão) | `supervisor`
- `supervisor_id`: filtra por supervisor (apenas quando `visao=supervisor`)
- `vendedor_id`: filtra por vendedor (apenas quando `visao=vendedor`)
- `tipo_meta`: `valor` | `volume`
- `ano`: número (ex.: 2025)
- `mes`: 1-12

### Dados e Agregação
- Visão `vendedor`: exibe metas individuais com progresso, faixa e **comissão**.
- Visão `supervisor`: agrega metas dos vendedores do supervisor selecionado e calcula:
    - `meta_total`, `realizado_total`, `percentual_alcance` (consolidado)
    - `taxa_supervisor` e `comissao_supervisor` para metas de `valor` usando faixas configuradas
    - Para metas de `volume`, a comissão do supervisor reflete a soma de comissões dos vendedores (conforme regra atual)

### Lógica de Comissão (Supervisor)
- Função utilitária: `_obter_taxa_por_alcance(tipo, empresa_id, percentual)`
    - Busca a faixa aplicável (empresa ou global) com base no percentual de alcance
    - Retorna `taxa_supervisor` usada no cálculo de `comissao_supervisor = realizado_total × taxa`

### UI e Responsividade
- Filtros com **toggle de visão** (Vendedor/Supervisor) via Bootstrap.
- Tabela "Detalhamento por Supervisão" com colunas: Supervisor, Tipo, Período, Meta, Realizado, Progresso, Comissão.
- Exibição de **Taxa (%)** junto à comissão quando `tipo_meta = valor`.

---

## 🔄 Fluxos de Trabalho Principais

### 1. Fluxo de Autenticação

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Flask App
    participant DB as PostgreSQL
    participant S as Session
    
    U->>F: GET /login
    F->>U: Renderiza login.html
    U->>F: POST /login (email, senha)
    F->>DB: SELECT * FROM usuarios WHERE email=?
    DB->>F: Retorna usuario
    F->>F: Verificar senha (bcrypt)
    alt Senha correta
        F->>S: Criar sessão (Flask-Login)
        F->>F: Verificar cargo
        alt Super Admin / Admin / Gerente
            F->>U: Redirect → /dashboard
        else Supervisor
            F->>U: Redirect → /supervisor/dashboard
        else Vendedor / Técnico
            F->>U: Redirect → /vendedor/dashboard
        end
    else Senha incorreta
        F->>U: Flash error + Redirect /login
    end
```

### 2. Fluxo de Criação de Meta com Cálculo de Comissão

```mermaid
sequenceDiagram
    participant U as Usuário (Gerente)
    participant F as Flask App
    participant H as helpers.py
    participant C as calculo_comissao.py
    participant DB as PostgreSQL
    
    U->>F: GET /metas/nova
    F->>DB: SELECT vendedores WHERE empresa_id=?
    DB->>F: Lista vendedores
    F->>U: Renderiza metas/form.html
    
    U->>F: POST /metas/nova (vendedor, mes, ano, valor_meta, receita)
    F->>H: pode_gerenciar_metas(current_user)
    H->>F: True (Gerente tem permissão)
    
    F->>C: calcular_comissao(valor_meta, receita_alcancada)
    C->>C: percentual = (receita / meta) * 100
    C->>DB: SELECT * FROM faixas_comissao WHERE alcance_min <= % <= alcance_max
    DB->>C: Retorna faixa (taxa_comissao)
    C->>C: comissao = receita * taxa
    C->>F: Retorna {percentual, comissao, faixa_id}
    
    F->>DB: INSERT INTO metas (vendedor_id, mes, ano, meta, receita, comissao, percentual)
    DB->>F: Meta criada (ID)
    F->>U: Flash success + Redirect /metas
```

### 3. Fluxo de Importação Excel de Clientes

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Flask App
    participant E as ensure_excel_available()
    participant P as Pandas/OpenPyXL
    participant DB as PostgreSQL
    
    U->>F: GET /clientes/importar
    F->>E: Verifica EXCEL_AVAILABLE
    E->>F: True/False
    alt Excel disponível
        F->>U: Renderiza importar.html (form ativo)
    else Excel indisponível
        F->>U: Renderiza importar.html (status red + instruções)
    end
    
    U->>F: POST /clientes/importar (arquivo.xlsx)
    F->>E: ensure_excel_available()
    E->>P: Import pandas, openpyxl
    P->>E: Success
    E->>F: EXCEL_AVAILABLE = True
    
    F->>P: pd.read_excel(arquivo.xlsx)
    P->>F: DataFrame (11/18/23 colunas detectadas)
    
    loop Para cada linha
        F->>F: Validar campos obrigatórios
        F->>DB: SELECT * FROM clientes WHERE codigo_cliente=?
        alt Cliente existe
            F->>DB: UPDATE clientes SET ...
        else Cliente novo
            F->>DB: INSERT INTO clientes (...)
        end
    end
    
    F->>U: Flash "{created} criados, {updated} atualizados" + Redirect /clientes
```

### 4. Fluxo de Ordem de Serviço (Ciclo Completo)

```mermaid
stateDiagram-v2
    [*] --> Aberta: Cliente/Vendedor cria OS
    Aberta --> Andamento: Técnico aceita e inicia
    Andamento --> Concluída: Técnico finaliza
    Concluída --> Aprovada: Supervisor aprova
    Aprovada --> Avaliada: Cliente avalia (1-5 estrelas)
    Avaliada --> [*]
    
    Aberta --> Cancelada: Cancelamento
    Andamento --> Cancelada: Cancelamento
    Cancelada --> [*]
    
    note right of Aberta
        Campos: cliente, descrição
        prioridade, categoria
    end note
    
    note right of Andamento
        Técnico atualiza:
        diagnóstico, solução
        peças utilizadas
    end note
    
    note right of Aprovada
        Supervisor registra:
        custo total, observações
        aprovação final
    end note
```

---

## 🧮 Sistema de Cálculo de Comissões

### Engine de Cálculo (`calculo_comissao.py`)

#### Algoritmo de Cálculo

```python
# Pseudocódigo do algoritmo

def calcular_comissao(valor_meta, receita_alcancada, empresa_id):
    # 1. Calcular percentual de alcance
    percentual = (receita_alcancada / valor_meta) * 100
    
    # 2. Buscar faixa de comissão aplicável
    faixa = db.query(FaixaComissao).filter(
        FaixaComissao.empresa_id == empresa_id,
        FaixaComissao.alcance_min <= percentual,
        FaixaComissao.alcance_max >= percentual,
        FaixaComissao.ativa == True
    ).order_by(FaixaComissao.ordem).first()
    
    # 3. Calcular comissão com base na taxa da faixa
    if faixa:
        taxa_comissao = faixa.taxa_comissao
        comissao = receita_alcancada * taxa_comissao
    else:
        # Faixa padrão se não encontrar
        comissao = 0
        taxa_comissao = 0
    
    # 4. Retornar resultado
    return {
        'percentual': percentual,
        'comissao': comissao,
        'faixa_id': faixa.id if faixa else None,
        'taxa_aplicada': taxa_comissao
    }
```

#### Faixas de Comissão Padrão

| Faixa | Alcance Mínimo | Alcance Máximo | Taxa | Cor Badge | Ordem |
|-------|:--------------:|:--------------:|:----:|-----------|:-----:|
| **Crítica** | 0% | 50% | 1% | `danger` | 0 |
| **Baixa** | 50% | 75% | 2% | `warning` | 1 |
| **Meta** | 75% | 100% | 3% | `info` | 2 |
| **Boa** | 100% | 125% | 4% | `primary` | 3 |
| **Excelente** | 125% | 1000% | 5% | `success` | 4 |

**Configuração**: Totalmente customizável via `/metas/configurar` (Gerentes e Admins)

---

## 🔒 Segurança Implementada

### Camadas de Segurança

#### 1. Autenticação e Sessão
- **Flask-Login**: Gerenciamento de sessão com `@login_required`
- **Werkzeug**: Hash de senhas com bcrypt (cost factor 12)
- **CSRF Protection**: Flask-WTF com tokens em todos os forms
- **Session Security**: Cookies HTTP-only, SameSite=Lax

#### 2. Permissões Granulares
```python
# Decorators implementados em helpers.py

@permission_required('pode_gerenciar_vendedores')
def criar_vendedor():
    # Apenas Super Admin, Admin, Gerente, Supervisor
    pass

@admin_required
def gerenciar_empresas():
    # Apenas Super Admin
    pass

@super_admin_required
def backup_database():
    # Apenas Super Admin
    pass
```

#### 3. Validação de Dados
- **Backend**: WTForms com validators (DataRequired, Email, Length, Regexp)
- **Frontend**: HTML5 validation + JavaScript
- **Sanitização**: Escape automático no Jinja2 (XSS prevention)
- **SQL Injection**: Proteção via SQLAlchemy ORM (parameterized queries)

#### 4. Headers HTTP de Segurança
```python
# Implementado em app.py

@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; ..."
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

#### 5. Rate Limiting
```python
# Implementado para rotas críticas

from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    # Máximo 10 tentativas por minuto (anti brute-force)
    pass
```

#### 6. Multi-Tenant Isolation
```python
# Todos os models têm empresa_id

class Cliente(db.Model):
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'))
    
# Todas as queries filtram por empresa
clientes = Cliente.query.filter_by(empresa_id=current_user.empresa_id).all()

# Super Admin pode ver todas as empresas
if current_user.cargo == 'super_admin':
    clientes = Cliente.query.all()  # Sem filtro empresa_id
```

---

## 📊 Performance e Otimização

### 1. Database Indexing
```python
# Índices criados em models.py

class Usuario(db.Model):
    __table_args__ = (
        db.Index('idx_usuario_email', 'email'),
        db.Index('idx_usuario_empresa', 'empresa_id'),
        db.Index('idx_usuario_gerente', 'gerente_id'),
        db.Index('idx_usuario_supervisor', 'supervisor_id'),
    )

class Cliente(db.Model):
    __table_args__ = (
        db.Index('idx_cliente_empresa', 'empresa_id'),
        db.Index('idx_cliente_codigo', 'codigo_cliente'),
        db.Index('idx_cliente_cpf_cnpj', 'cpf_cnpj'),
    )
```

### 2. Connection Pooling
```python
# config.py - PostgreSQL Production

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 5,          # 5 conexões permanentes
    'max_overflow': 10,       # +10 conexões sob demanda
    'pool_timeout': 30,       # Timeout 30s
    'pool_recycle': 1800,     # Reciclar conexões após 30min
    'pool_pre_ping': True     # Verificar conexão antes de usar
}
```

### 3. Caching
```python
# Flask-Caching para relatórios

from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutos
})

@app.route('/relatorios/metas-avancado')
@cache.cached(timeout=300, key_prefix=lambda: f'relatorio_{current_user.empresa_id}')
def relatorio_metas():
    # Cache por 5 minutos por empresa
    pass
```

### 4. Compressão Gzip
```python
# Flask-Compress

from flask_compress import Compress

Compress(app)  # Comprime respostas > 500 bytes (70-90% redução)
```

### 5. Lazy Loading de Excel
```python
# helpers.py - Importação sob demanda

EXCEL_AVAILABLE = False

def ensure_excel_available():
    global EXCEL_AVAILABLE
    if not EXCEL_AVAILABLE:
        try:
            import pandas as pd
            import openpyxl
            EXCEL_AVAILABLE = True
        except ImportError:
            EXCEL_AVAILABLE = False
    return EXCEL_AVAILABLE
```

---

## 🌐 Deploy e Infraestrutura

### Railway Platform Architecture

```mermaid
graph LR
    subgraph Internet
        User[👤 Usuários]
        DNS[🌐 vendacerta.up.railway.app]
    end
    
    subgraph Railway[Railway Platform]
        LB[⚖️ Load Balancer]
        HTTPS[🔒 SSL/TLS Termination]
        
        subgraph App[Flask Application]
            G1[Gunicorn Worker 1]
            G2[Gunicorn Worker 2]
            G3[Gunicorn Worker 3]
        end
        
        subgraph Database[PostgreSQL 15]
            PG[(💾 Database)]
            PG_Backup[(💾 Daily Backups)]
        end
        
        Logs[📊 Railway Logs]
        Metrics[📈 Railway Metrics]
    end
    
    User --> DNS
    DNS --> HTTPS
    HTTPS --> LB
    LB --> G1
    LB --> G2
    LB --> G3
    
    G1 --> PG
    G2 --> PG
    G3 --> PG
    
    PG --> PG_Backup
    App --> Logs
    App --> Metrics
```

### Build Process (Nixpacks)

```toml
# nixpacks.toml

[phases.setup]
nixPkgs = ['python311', 'postgresql', 'openblas', 'gfortran']

[phases.install]
cmds = [
    'pip install --upgrade pip',
    'pip install -r requirements.txt'
]

[phases.build]
cmds = ['python -c "import pandas; import openpyxl; print(\"Excel libs OK\")"']

[start]
cmd = 'gunicorn --bind 0.0.0.0:$PORT --workers 3 --timeout 120 wsgi:app'
```

### Environment Variables

| Variável | Desenvolvimento | Produção |
|----------|----------------|----------|
| `FLASK_ENV` | `development` | `production` |
| `FLASK_DEBUG` | `True` | `False` |
| `FLASK_SECRET_KEY` | (gerado localmente) | **32+ chars forte** |
| `DATABASE_URL` | `sqlite:///instance/vendacerta.db` | `postgresql://user:pass@host:port/db` |
| `LOG_LEVEL` | `DEBUG` | `INFO` |
| `RATELIMIT_ENABLED` | `False` | `True` |
| `ENABLE_COMPRESSION` | `False` | `True` |
| `ENABLE_CACHE` | `False` | `True` |

---

## 📚 Tecnologias e Dependências

### Backend Stack

| Biblioteca | Versão | Propósito |
|------------|--------|-----------|
| **Flask** | 3.0.0 | Framework web principal |
| **Flask-SQLAlchemy** | 3.1.1 | ORM SQLAlchemy integrado |
| **Flask-Login** | 0.6.3 | Autenticação de usuários |
| **Flask-WTF** | 1.2.1 | Formulários e CSRF |
| **Flask-Limiter** | 3.5.0 | Rate limiting (anti DDoS) |
| **Flask-Compress** | 1.14 | Compressão Gzip |
| **Flask-Caching** | 2.1.0 | Sistema de cache |
| **Werkzeug** | 3.0.1 | WSGI utilities + segurança |
| **SQLAlchemy** | 2.0.23 | ORM e database toolkit |
| **psycopg2-binary** | 2.9.9 | Driver PostgreSQL |
| **pandas** | 2.3.3 | Análise e importação Excel |
| **openpyxl** | 3.1.2 | Leitura/escrita XLSX |
| **ReportLab** | 4.0.7 | Geração de PDFs |
| **Gunicorn** | 21.2.0 | WSGI HTTP Server (produção) |
| **python-dotenv** | 1.0.0 | Gerenciar variáveis ambiente |

### Frontend Stack

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Bootstrap** | 5.3.3 | Framework CSS responsivo |
| **Bootstrap Icons** | 1.11.3 | Ícones SVG |
| **Google Fonts (Inter)** | - | Tipografia moderna |
| **Chart.js** | 4.4.0 | Gráficos interativos |
| **JavaScript (Vanilla)** | ES6+ | Interatividade dinâmica |

### Database

| Sistema | Versão | Ambiente |
|---------|--------|----------|
| **SQLite** | 3.x | Desenvolvimento local |
| **PostgreSQL** | 15+ | Produção Railway |

---

## 🔗 Integrações Externas

### 1. Railway Platform
- **Deploy automático**: Conectado ao GitHub (push → deploy)
- **PostgreSQL gerenciado**: Backups diários automáticos
- **Domínio público**: `vendacerta.up.railway.app` (SSL incluído)
- **Logs centralizados**: Acesso via `railway logs --follow`
- **Métricas**: CPU, RAM, Network, Request count

### 2. Geração de Relatórios
- **ReportLab**: PDFs de metas, comissões e OS
- **Pandas/OpenPyXL**: Importação/exportação Excel multi-formato
- **Chart.js**: Gráficos de performance, metas e ranking

### 3. Health Checks
```python
@app.route('/health')
def health_check():
    try:
        # Verifica conexão com banco
        db.session.execute(text('SELECT 1'))
        db_status = 'ok'
    except:
        db_status = 'error'
    
    return {
        'status': 'healthy' if db_status == 'ok' else 'unhealthy',
        'database': db_status,
        'version': '2.0.0',
        'excel_available': EXCEL_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    }
```

---

## 📈 Monitoramento e Logs

### Estrutura de Logs

```python
import logging

# Configuração em app.py
logging.basicConfig(
    level=logging.INFO if app.config['FLASK_ENV'] == 'production' else logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console (Railway captura)
        logging.FileHandler('app.log') if app.debug else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)

# Exemplos de uso
logger.info(f'Usuário {current_user.email} criou meta ID {meta.id}')
logger.warning(f'Tentativa de acesso negada: {current_user.cargo} → /super-admin')
logger.error(f'Erro ao calcular comissão: {str(e)}')
```

### Métricas Chave

| Métrica | Descrição | Onde Ver |
|---------|-----------|----------|
| **Request Count** | Total requisições HTTP | Railway Dashboard |
| **Response Time** | Tempo médio resposta | Railway Metrics |
| **Database Queries** | Tempo queries SQL | SQLAlchemy logs |
| **Cache Hit Rate** | % requisições em cache | Flask-Caching stats |
| **Error Rate** | % requisições com erro 5xx | Railway Logs |
| **Active Users** | Usuários logados simultaneamente | Flask-Login sessions |

---

## 🚀 Próximas Evoluções (Roadmap)

### v2.1 - Curto Prazo
- [ ] API GraphQL para integração mobile
- [ ] Notificações push PWA
- [ ] Dashboard mobile nativo (React Native)
- [ ] Geolocalização de vendedores em tempo real

### v2.2 - Médio Prazo
- [ ] Integração com WhatsApp Business API
- [ ] Machine Learning para previsão de vendas
- [ ] Chat interno em tempo real (WebSockets)
- [ ] Calendário de visitas e agendamentos

### v3.0 - Longo Prazo
- [ ] Migração para microserviços (Flask → FastAPI)
- [ ] Kubernetes deployment (Railway → GKE/EKS)
- [ ] Event Sourcing + CQRS pattern
- [ ] GraphQL subscriptions (real-time)

---

## 📞 Suporte Técnico

### Recursos de Documentação
- 📖 [README Principal](../README.md)
- 🚀 [Guia Início Rápido](GETTING_STARTED.md)
- 🌐 [Documentação API REST](API.md)
- 🏗️ [Esta Arquitetura](ARCHITECTURE.md)

### Links Úteis
- 🌐 **Produção**: [vendacerta.up.railway.app](https://vendacerta.up.railway.app)
- 🐙 **GitHub**: [cristiano-superacao/vendacerta](https://github.com/cristiano-superacao/vendacerta)
- 🚂 **Railway Dashboard**: [railway.app/dashboard](https://railway.app/dashboard)

---

<div align="center">

**VendaCerta v2.0.0 - Arquitetura** | Última atualização: Dezembro 2024

[⬅️ Voltar ao README](../README.md) | [📚 Índice Documentação](../INDICE_DOCUMENTACAO.md)

</div>
