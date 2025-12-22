# 🚀 Guia Completo de Deploy - Sistema de Metas

## 📋 Índice Rápido

1. [Deploy no Railway (Recomendado)](#-railway-deploy-recomendado)
2. [Deploy no Render](#-render-deploy-alternativa)
3. [Migração do Banco de Dados](#-migração-do-banco-de-dados)
4. [Solução de Problemas](#-solução-de-problemas)

---

## 🎯 Railway Deploy (Recomendado)

### ✨ Passo a Passo Simplificado (5 minutos)

#### 1️⃣ Preparar o Projeto

```bash
# Clone ou navegue até o projeto
cd /caminho/para/o/projeto

# Certifique-se de que todos os arquivos estão commitados
git add .
git commit -m "Preparar para deploy"
git push
```

#### 2️⃣ Criar Projeto no Railway

1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em **"New Project"**
4. Selecione **"Deploy from GitHub repo"**
5. Escolha o repositório **suameta**

#### 3️⃣ Adicionar PostgreSQL

1. No projeto criado, clique em **"+ New"**
2. Selecione **"Database"** → **"PostgreSQL"**
3. Aguarde a criação (30 segundos)

#### 4️⃣ Configurar Variáveis de Ambiente

Na seção **"Variables"** do seu serviço web, adicione:

```bash
# Variáveis Essenciais
DATABASE_URL=${{Postgres.DATABASE_URL}}
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-super-segura-aqui
PYTHONUNBUFFERED=1
PYTHON_VERSION=3.11.9
```

> **💡 Dica**: O Railway sugere automaticamente algumas variáveis. Clique em **"Add"** para adicioná-las rapidamente.

#### 5️⃣ Aplicar Migração do Banco

Após o deploy inicial, execute:

```bash
# Use o script consolidado
python migrate.py
```

O script irá:
- ✅ Detectar automaticamente o ambiente (local ou produção)
- ✅ Criar todas as tabelas necessárias
- ✅ Criar empresa padrão
- ✅ Criar usuários admin e super admin

#### 6️⃣ Gerar Domínio Público

1. No Railway, vá em **"Settings"**
2. Clique em **"Generate Domain"**
3. Aguarde a geração (ex: `web-production-90dab.up.railway.app`)

#### 7️⃣ Acessar a Aplicação

```
🌐 URL: https://seu-dominio.up.railway.app
👤 Super Admin: superadmin@suameta.com / 18042016
🔑 Admin: admin@suameta.com / admin123
```

---

## � Render Deploy (Alternativa)

### Passo a Passo

#### 1️⃣ Criar Web Service

1. Acesse [render.com](https://render.com)
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: sistema-metas
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

#### 2️⃣ Adicionar PostgreSQL

1. Clique em **"New +"** → **"PostgreSQL"**
2. Escolha o plano **Free**
3. Copie a **Internal Database URL**

#### 3️⃣ Configurar Variáveis

No Web Service, adicione em **"Environment"**:

```bash
DATABASE_URL=<cole-a-url-do-postgres>
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-aqui
```

#### 4️⃣ Aplicar Migração

```bash
python migrate.py
# Cole a DATABASE_URL quando solicitado
```

---

## 💾 Migração do Banco de Dados

### Script Consolidado: `migrate.py`

O sistema agora possui um **único script de migração** que funciona em qualquer ambiente:

```bash
python migrate.py
```

#### Funcionalidades

✅ **Detecção Automática de Ambiente**
- Detecta automaticamente se é local (SQLite) ou produção (PostgreSQL)
- Lê DATABASE_URL de múltiplas fontes (variáveis, arquivo salvo, input manual)

✅ **Criação de Estrutura Completa**
- Cria todas as tabelas necessárias
- Cria empresa padrão
- Cria usuários administrativos

✅ **Suporte Multi-Plataforma**
- SQLite para desenvolvimento local
- PostgreSQL para Railway/Render

### Fluxos de Uso

#### Desenvolvimento Local
```bash
python migrate.py
# Detecta automaticamente SQLite
# Cria metas.db
# Pronto para usar!
```

#### Produção (Railway/Render)
```bash
# Opção 1: Com DATABASE_URL nas variáveis de ambiente
export DATABASE_URL="postgresql://..."
python migrate.py

# Opção 2: Colar quando solicitado
python migrate.py
# Digite 's' quando perguntado
# Cole a DATABASE_URL
```

---

## 🔧 Solução de Problemas

### ❌ Erro: "Could not determine join condition"

**Causa**: Modelo `Usuario` sem `ForeignKey` adequado.

**Solução**: O arquivo `models.py` já está corrigido. Execute:
```bash
python migrate.py
```

### ❌ Erro: "relation already exists"

**Causa**: Tentando criar tabela que já existe.

**Solução**: Normal! O script ignora tabelas existentes.

### ❌ Erro: "psycopg2 not installed"

**Solução**:
```bash
pip install psycopg2-binary
```

### ❌ Erro 500 no Railway após Deploy

**Causas Comuns**:
1. DATABASE_URL não configurada
2. Migração não executada
3. Variáveis de ambiente faltando

**Solução**:
```bash
# 1. Verifique as variáveis no Railway
# 2. Execute a migração
python migrate.py

# 3. Verifique os logs no Railway
railway logs
```

### 🔍 Como Ver Logs no Railway

1. Acesse seu projeto no Railway
2. Clique no serviço web
3. Aba **"Deployments"**
4. Clique no deploy ativo
5. Visualize os logs em tempo real

### 🔍 Como Ver Logs no Render

1. Acesse seu Web Service
2. Aba **"Logs"**
3. Logs em tempo real

---

## 📊 Arquivos de Configuração

### `Procfile` (Render/Heroku)
```
web: gunicorn app:app
```

### `railway.json` (Railway)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `nixpacks.toml` (Railway Build)
```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "gunicorn app:app --bind 0.0.0.0:$PORT"
```

---

## 🎯 Checklist de Deploy

### Antes do Deploy

- [ ] Código commitado no GitHub
- [ ] `requirements.txt` atualizado
- [ ] Arquivos de configuração presentes (`Procfile`, `railway.json`, etc)
- [ ] `.gitignore` configurado (não commitar `.env`, `metas.db`, etc)

### Durante o Deploy

- [ ] Projeto criado no Railway/Render
- [ ] PostgreSQL adicionado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy executado com sucesso

### Após o Deploy

- [ ] Migração do banco executada (`python migrate.py`)
- [ ] Domínio público gerado
- [ ] Acesso testado com usuários admin
- [ ] Funcionalidades principais testadas

---

## 🎨 Recursos do Sistema

### ✅ Implementado e Funcional

✨ **Autenticação Completa**
- Login/Registro
- Recuperação de senha
- Controle de acesso por perfil

👥 **Gestão de Vendedores**
- CRUD completo
- Vinculação com equipes
- Histórico de performance

📊 **Gestão de Metas**
- Criação de metas mensais
- Cálculo automático de comissões
- 5 faixas de comissão baseadas em performance

🏢 **Sistema Multi-Empresa**
- Super Admin global
- Isolamento de dados por empresa
- Gestão de empresas (criar, editar, bloquear)

📈 **Dashboard Interativo**
- Cards com gradientes modernos
- Ranking de vendedores
- Estatísticas em tempo real
- 100% responsivo

📄 **Exportação PDF**
- Dashboard completo
- Relatórios de metas por período

🎨 **Layout Profissional**
- Design responsivo mobile-first
- Sidebar moderna com gradientes
- Tema unificado (theme.css)
- Componentes reutilizáveis

---

## 📞 Suporte

**Desenvolvedor**: Cristiano Santos  
**WhatsApp**: (71) 99337-2960  
**Email**: cristiano.s.santos@ba.estudante.senai.br

---

## 📝 Notas Importantes

### Arquivos Consolidados

Este guia **substitui** os seguintes arquivos duplicados (removidos):

❌ **Removidos/Consolidados**:
- `DEPLOY_AUTOMATICO.md`
- `DEPLOY_FINAL.md`
- `DEPLOY_RAILWAY_RAPIDO.md`
- `FINALIZE_DEPLOY.md`
- `GUIA_DEPLOY_RAILWAY.md`
- `GUIA_3_CLIQUES.md`
- `GUIA_RAILWAY_PASSO_A_PASSO.md`
- `GUIA_CORRECAO_RAILWAY.md`

✅ **Mantidos**:
- `README.md` - Documentação principal do projeto
- `DEPLOY.md` - Este arquivo (guia consolidado)
- `MANUAL_USUARIO.md` - Manual para usuários finais
- `DOCUMENTACAO_SUPORTE.md` - Documentação de suporte

### Scripts Consolidados

❌ **Scripts Duplicados** (substituídos por `migrate.py`):
- `aplicar_migracao_auto.py`
- `aplicar_migracao_final.py`
- `aplicar_migracao_railway.py`
- `migrar_banco.py`
- `migrar_railway_simples.py`
- `configurar_railway.py`
- `configurar_railway_automatico.py`
- `configurar_railway_completo.py`
- `criar_banco_completo.py`
- `criar_banco_novo.py`

✅ **Script Único Consolidado**:
- `migrate.py` - Migração universal (local + produção)

---

## 🚀 Vamos Começar!

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/suameta.git

# 2. Execute localmente
python migrate.py
python app.py

# 3. Acesse
http://127.0.0.1:5000

# 4. Deploy no Railway
# Siga o passo a passo acima!
```

**Pronto para o sucesso! 🎉**

---

# Arquivos criados para deploy:

1. **Procfile** - Comando para iniciar o servidor
2. **runtime.txt** - Versão do Python
3. **requirements.txt** - Dependências (atualizado com gunicorn)
4. **render.yaml** - Configuração automática do Render
5. **.gitignore** - Ignora arquivos locais (.db, __pycache__, etc)

---

# Testar localmente antes do deploy:

```bash
# Instalar gunicorn
pip install gunicorn

# Testar servidor de produção
gunicorn app:app

# Acesse: http://127.0.0.1:8000
```

---

# Após o deploy:

1. Acesse a URL fornecida
2. Faça login: admin@metas.com / admin123
3. Cadastre vendedores, metas e equipes
4. Exporte relatórios em PDF
5. Compartilhe a URL com sua equipe!

🚀 **Bom deploy!**
