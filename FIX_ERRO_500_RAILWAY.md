# 🚨 CORREÇÃO URGENTE - ERRO 500 NO RAILWAY

## 🔍 Problema Identificado

**Erro:** `ERRO: a coluna usuarios.supervisor_id não existe no caractere 316`

**Causa:** A tabela `usuarios` no PostgreSQL do Railway está faltando colunas que foram adicionadas recentemente:
- `supervisor_id` (INTEGER) - Hierarquia vendedor→supervisor
- `pode_gerenciar_tecnicos` (BOOLEAN) - Permissão de gerenciamento
- `pode_atribuir_tecnicos` (BOOLEAN) - Permissão de atribuição

## ✅ Solução Implementada

Foram criados 3 arquivos para corrigir automaticamente:

### 1. `fix_database_railway.py`
Script que adiciona as colunas faltantes no PostgreSQL do Railway.

### 2. `startup.sh` (Modificado)
Agora executa o fix automaticamente antes de iniciar o Gunicorn.

### 3. `app.py` (Modificado)
Detecta ambiente Railway e executa verificação do banco.

## 🚀 Passos para Deploy

### Opção 1: Deploy Automático (Recomendado)

```bash
# 1. Commitar as mudanças
git add .
git commit -m "fix: adicionar colunas faltantes no PostgreSQL Railway"

# 2. Push para o repositório
git push origin main

# 3. Railway vai fazer o redeploy automaticamente
# O script fix_database_railway.py será executado no startup.sh
```

### Opção 2: Execução Manual via Railway CLI

```bash
# 1. Instalar Railway CLI (se ainda não tiver)
npm i -g @railway/cli
# ou
curl -fsSL https://railway.app/install.sh | sh

# 2. Fazer login
railway login

# 3. Linkar ao projeto
railway link

# 4. Executar o fix diretamente
railway run python fix_database_railway.py

# 5. Verificar variáveis de ambiente
railway run python check_railway_env.py

# 6. Fazer redeploy
railway up
```

### Opção 3: Executar SQL Direto no PostgreSQL

Se preferir executar SQL manualmente:

```sql
-- Conectar ao PostgreSQL do Railway (copie a DATABASE_URL do painel)

-- Adicionar coluna supervisor_id
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS supervisor_id INTEGER;

-- Adicionar foreign key
ALTER TABLE usuarios 
ADD CONSTRAINT fk_usuarios_supervisor 
FOREIGN KEY (supervisor_id) 
REFERENCES usuarios(id) 
ON DELETE SET NULL;

-- Criar índice para performance
CREATE INDEX IF NOT EXISTS idx_usuario_supervisor 
ON usuarios(supervisor_id);

-- Adicionar colunas de permissão
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS pode_gerenciar_tecnicos BOOLEAN DEFAULT FALSE;

ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS pode_atribuir_tecnicos BOOLEAN DEFAULT FALSE;
```

## 🔧 Verificação Pós-Deploy

### 1. Verificar Logs do Railway

```bash
railway logs
```

Procure por:
- ✅ `Estrutura do banco verificada/corrigida.`
- ✅ `Coluna supervisor_id adicionada com sucesso`
- ✅ `Servidor iniciado com sucesso`

### 2. Testar o Site

Acesse: https://metacerta.up.railway.app/login

Deve carregar sem erro 500.

### 3. Verificar Variáveis de Ambiente

```bash
railway run python check_railway_env.py
```

## 🛠️ Variáveis de Ambiente Necessárias

Verifique no painel do Railway (`Variables`):

| Variável | Valor | Origem |
|----------|-------|--------|
| `DATABASE_URL` | `postgres://...` | Automático (PostgreSQL service) |
| `PORT` | `8080` | Automático (Railway) |
| `RAILWAY_ENVIRONMENT` | `production` | Automático (Railway) |
| `FLASK_SECRET_KEY` | `(32+ chars)` | **VOCÊ PRECISA CONFIGURAR** |
| `FLASK_ENV` | `production` | Recomendado |
| `FLASK_DEBUG` | `False` | Recomendado |

### Gerar FLASK_SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie o resultado e adicione no Railway:
1. Dashboard do Railway → Seu projeto
2. `Variables` → `New Variable`
3. Nome: `FLASK_SECRET_KEY`
4. Valor: (cole o token gerado)
5. `Add` → Railway vai redeploy automaticamente

## 📊 Estrutura das Colunas Adicionadas

```sql
-- Hierarquia de supervisão
supervisor_id INTEGER 
  REFERENCES usuarios(id) ON DELETE SET NULL
  
-- Permissões de gestão
pode_gerenciar_tecnicos BOOLEAN DEFAULT FALSE
pode_atribuir_tecnicos BOOLEAN DEFAULT FALSE

-- Índice para performance
idx_usuario_supervisor ON usuarios(supervisor_id)
```

## 🎯 Fluxo de Inicialização no Railway

```
1. Railway Build (Nixpacks)
   ↓
2. Criar .venv e instalar dependências
   ↓
3. Executar startup.sh
   ↓
4. fix_database_railway.py (NOVO)
   - Conectar PostgreSQL
   - Verificar colunas existentes
   - Adicionar colunas faltantes
   - Criar FK e índices
   ↓
5. init_railway.py
   - Criar tabelas se não existirem
   - Criar usuário admin
   ↓
6. Gunicorn (wsgi:app)
   - Servidor rodando na porta $PORT
```

## 🚨 Se Ainda Tiver Erro 500

### 1. Verificar logs detalhados

```bash
railway logs --tail 100
```

### 2. Conectar ao PostgreSQL e verificar

```bash
# Copie DATABASE_URL do painel Railway
railway variables

# Conecte via psql
psql "DATABASE_URL_AQUI"

# Verifique a estrutura
\d usuarios
```

Deve mostrar as colunas:
- `supervisor_id`
- `pode_gerenciar_tecnicos`
- `pode_atribuir_tecnicos`

### 3. Forçar Redeploy

```bash
railway up --detach
```

## 📝 Checklist Final

- [ ] Arquivo `fix_database_railway.py` criado
- [ ] Arquivo `startup.sh` modificado
- [ ] Arquivo `app.py` modificado
- [ ] Variável `FLASK_SECRET_KEY` configurada no Railway
- [ ] Commit e push das mudanças
- [ ] Railway fez redeploy automaticamente
- [ ] Logs não mostram erro de coluna
- [ ] Site carrega sem erro 500
- [ ] Login funciona corretamente

## 🆘 Suporte

Se o erro persistir, verifique:

1. **Logs do Railway:** `railway logs`
2. **Variáveis de ambiente:** `railway variables`
3. **Estrutura do banco:** `railway run python -c "from models import db; print(db.engine.table_names())"`
4. **Versão PostgreSQL:** Deve ser 14+

## 📚 Arquivos Relacionados

- [`fix_database_railway.py`](fix_database_railway.py) - Script de correção
- [`startup.sh`](startup.sh) - Script de inicialização
- [`app.py`](app.py) - Aplicação principal
- [`models.py`](models.py) - Modelos do banco de dados
- [`check_railway_env.py`](check_railway_env.py) - Verificador de variáveis

---

**Última Atualização:** Correção do erro de coluna `supervisor_id` não existente
**Status:** ✅ Scripts criados e prontos para deploy
