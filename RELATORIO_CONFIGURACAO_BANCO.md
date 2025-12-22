# 📊 Relatório: Configuração do Banco de Dados e Conexões

**Data:** 19 de dezembro de 2025  
**Sistema:** VendaCerta  
**Ambiente:** Railway (PostgreSQL)

---

## 🧩 REQUISITOS OBRIGATÓRIOS (PostgreSQL)

### Variáveis de Ambiente (Railway / Produção)
```
✅ DATABASE_URL       = postgresql://postgres:***@postgres.railway.internal:5432/railway
✅ PGDATABASE         = railway
✅ PGHOST             = postgres.railway.internal
✅ PGUSER             = postgres
✅ PGPASSWORD         = ezvdYHRrPgvtFwyLBMzOZpHVbTpHiGwb
✅ PGPORT             = 5432
```

---

## ☁️ CONFIGURAÇÃO RAILWAY (Produção)

### Variáveis de Ambiente
```
✅ DATABASE_URL       = postgresql://postgres:***@postgres.railway.internal:5432/railway
✅ PGDATABASE         = railway
✅ PGHOST             = postgres.railway.internal
✅ PGUSER             = postgres
✅ PGPASSWORD         = ezvdYHRrPgvtFwyLBMzOZpHVbTpHiGwb
✅ PGPORT             = 5432
```

### Banco de Dados Ativo
```yaml
Tipo: PostgreSQL 17.7
Host: postgres.railway.internal:5432
Database: railway
Usuário: postgres
Status: ✅ Configurado e Operacional
Uso: Produção
```

### Configuração SQLAlchemy (PostgreSQL)
```python
SQLALCHEMY_DATABASE_URI: 'postgresql://postgres:***@postgres.railway.internal:5432/railway'

SQLALCHEMY_ENGINE_OPTIONS:
  pool_pre_ping: True              # Verifica conexão antes de usar
  pool_recycle: 280                # Recicla conexões a cada 4:40min
  pool_size: 5                     # 5 conexões simultâneas
  max_overflow: 10                 # Até 15 conexões total (5 + 10)
  pool_timeout: 30                 # 30s para obter conexão
  connect_args:
    connect_timeout: 10            # 10s timeout de conexão
    options: '-c statement_timeout=30000'  # 30s timeout para queries
```

---

## 🔗 ARQUITETURA DE CONEXÃO

### Fluxo de Detecção (3 Níveis)

```
┌─────────────────────────────────────────────────────────┐
│  NÍVEL 1: DATABASE_URL Direta                          │
│  ┌───────────────────────────────────────────────────┐ │
│  │ os.environ.get('DATABASE_URL')                    │ │
│  │ ↓                                                  │ │
│  │ ✅ Railway: postgresql://postgres:***@...         │ │
│  │ ❌ Local: None                                     │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                        ↓ (se vazia/None)
┌─────────────────────────────────────────────────────────┐
│  NÍVEL 2: Construção via PG* Variables                │
│  ┌───────────────────────────────────────────────────┐ │
│  │ PGHOST + PGPORT + PGUSER + PGPASSWORD + PGDATABASE│ │
│  │ ↓                                                  │ │
│  │ ✅ Railway: Constrói URL completa                 │ │
│  │ ❌ Local: Variáveis não definidas                 │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                        ↓ (se incompleto)
┌─────────────────────────────────────────────────────────┐
│  ERRO: PostgreSQL obrigatório                           │
│  ┌───────────────────────────────────────────────────┐ │
│  │ raise RuntimeError("CONFIG: Banco obrigatório     │ │
│  │ PostgreSQL não configurado...")                   │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Arquivo: config.py (Linhas 18-88)

```python
# 1️⃣ Busca DATABASE_URL
database_url = os.environ.get('DATABASE_URL')

# 2️⃣ Remove strings vazias (problema descoberto!)
if database_url:
    database_url = database_url.strip()
    if not database_url:
        database_url = None
        print("[CONFIG] ⚠️  DATABASE_URL vazia detectada")

# 3️⃣ Constrói via PG* se necessário
if not database_url:
    if all([PGDATABASE, PGHOST, PGUSER, PGPASSWORD]):
        database_url = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'
        print("[CONFIG] ✅ URL construida via PG* variables")

# 4️⃣ Normaliza postgres:// para postgresql://
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

# 5️⃣ Define URI final (PostgreSQL obrigatório)
if not database_url:
    raise RuntimeError("CONFIG: Banco obrigatório PostgreSQL não configurado.")
SQLALCHEMY_DATABASE_URI = database_url
```

---

## 📦 POOL DE CONEXÕES

### Railway (PostgreSQL)
```
┌─────────────────────────────────────────────┐
│  Connection Pool                           │
├─────────────────────────────────────────────┤
│  Base Pool: 5 conexões                     │
│  Max Overflow: 10 conexões                 │
│  Total Máximo: 15 conexões simultâneas     │
│                                            │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ │
│  │ C1  │ │ C2  │ │ C3  │ │ C4  │ │ C5  │ │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ │
│         Base Pool (sempre ativas)          │
│                                            │
│  + 10 conexões overflow (sob demanda)      │
│                                            │
│  Timeouts:                                 │
│  • Obter conexão: 30s                     │
│  • Conectar ao banco: 10s                 │
│  • Executar query: 30s                    │
│                                            │
│  Reciclagem:                               │
│  • A cada 280 segundos (4:40min)          │
│  • Antes do timeout de 5min do Railway    │
└─────────────────────────────────────────────┘
```

> Observação: O sistema não suporta SQLite. Todo ambiente deve usar PostgreSQL.

---

## 🗄️ ESTRUTURA DO BANCO DE DADOS

### Tabelas (16 no total)

```sql
-- Autenticação e Usuários
usuarios                  -- Usuários do sistema
vendedores               -- Equipe de vendas

-- Clientes e Relacionamento
clientes                 -- Base de clientes
historico_clientes       -- Histórico de mudanças

-- Vendas e Comissões
vendas                   -- Registro de vendas
comissoes                -- Cálculo de comissões
metas                    -- Metas de vendedores

-- Estoque e Produtos
estoque                  -- Controle de estoque
movimentacoes_estoque    -- Movimentações
produtos                 -- Cadastro de produtos

-- Serviços
servicos                 -- Serviços prestados
servicos_clientes        -- Vínculo cliente-serviço

-- Organização
empresas                 -- Empresas/Filiais
departamentos            -- Estrutura organizacional
equipes                  -- Times de trabalho

-- Sistema
alembic_version          -- Controle de migrações
```

### Índices de Performance

```sql
-- Otimização de buscas
idx_vendedores_email     -- Busca por email
idx_vendedores_cpf       -- Busca por CPF
idx_clientes_codigo      -- Busca por código
idx_clientes_vendedor    -- Join clientes-vendedores
idx_metas_vendedor       -- Join metas-vendedores
```

---

## 🔧 BINDS (Múltiplos Bancos)

O sistema suporta separação de dados em bancos diferentes (mesmo banco por padrão):

```python
SQLALCHEMY_BINDS = {
    'auth': DATABASE_URL,           # Autenticação
    'vendas': DATABASE_URL,         # Vendas e comissões
    'clientes': DATABASE_URL,       # Clientes
    'estoque': DATABASE_URL,        # Estoque
    'servicos': DATABASE_URL,       # Serviços
    'comunicacao': DATABASE_URL     # Comunicação
}
```

**Status Atual:** Todos usando o mesmo banco (Railway PostgreSQL em produção)

---

## 📊 PADRÃO ÚNICO: PostgreSQL

O sistema é padronizado para PostgreSQL em todos os ambientes (dev, staging, prod).

---

## 🔍 LOGS DE INICIALIZAÇÃO

### Erro de configuração
```
[CONFIG] ❌ Variaveis PG* incompletas - PostgreSQL obrigatório
Traceback (most recent call last):
    RuntimeError: CONFIG: Banco obrigatório PostgreSQL não configurado...
```

### Railway (PostgreSQL)
```
[CONFIG] ✅ DATABASE_URL encontrada - Host: postgres.railway.internal:5432
[CONFIG] ✅ DATABASE_URL válida - PostgreSQL configurado
[CONFIG] 🚀 Sistema configurado para PostgreSQL (PRODUÇÃO)
```

---

## ✅ STATUS ATUAL

### Sistema Railway
```
✅ PostgreSQL configurado
✅ DATABASE_URL definida manualmente
✅ Variáveis PG* todas presentes
✅ Pool de conexões otimizado (5-15)
✅ Timeouts configurados
✅ Fix automático habilitado (wsgi.py)
✅ Deploy automático ativo
✅ Site funcionando: https://metacerta.up.railway.app
```

---

## 🛠️ COMANDOS ÚTEIS

### Verificar Configuração Local
```bash
python verificar_database_url.py
```

### Verificar Railway
```bash
railway variables | Select-String -Pattern "DATABASE|PG"
railway run python verificar_database_url.py
```

### Ver Logs Railway
```bash
railway logs --follow
railway logs | Select-String -Pattern "CONFIG"
```

### Testar Conexão Railway
```bash
railway shell
python
>>> from app import db
>>> db.engine.url
>>> db.session.execute('SELECT 1').fetchone()
```

---

## 📁 ARQUIVOS DE CONFIGURAÇÃO

| Arquivo | Responsabilidade |
|---------|------------------|
| [config.py](config.py) | Configuração principal do banco |
| [app.py](app.py) | Inicializa SQLAlchemy |
| [wsgi.py](wsgi.py) | Gunicorn + fix_database_railway.py |
| [models.py](models.py) | Define as 16 tabelas |
| [init_db.py](init_db.py) | Cria banco local |
| [fix_database_railway.py](fix_database_railway.py) | Corrige schema produção |

---

## 🎯 RESUMO EXECUTIVO

### ✅ Pontos Fortes
1. **Padrão Único**: PostgreSQL em todos os ambientes (dev/staging/prod)
2. **Detecção Robusta**: 3 níveis para obter a URL PostgreSQL
3. **Pool Otimizado**: 5-15 conexões Railway, reciclagem a cada 4:40min
4. **Timeouts Configurados**: Previne travamentos
5. **Fix Automático**: wsgi.py corrige schema no deploy
6. **Logs Detalhados**: Fácil debug

### 🔄 Fluxo Completo
```
Variáveis Railway → config.py → app.py → wsgi.py → PostgreSQL → Interface
```

### 🌐 URLs
- **Produção**: https://metacerta.up.railway.app
- **Local**: http://localhost:5000

---

**Sistema 100% configurado e operacional! 🚀**
