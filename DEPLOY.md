# 🚀 Deploy Automático - VendaCerta

## 📋 Visão Geral

Sistema de gestão completa de vendas, clientes e metas com deploy automático via GitHub Actions + Railway.

## 🔄 Deploy Automático

### Como Funciona

1. **Push para `main`** → Aciona GitHub Actions
2. **GitHub Actions** → Executa workflow de deploy
3. **Railway** → Recebe deploy e executa
4. **WSGI** → Auto-corrige banco antes do Gunicorn
5. **Healthcheck** → Valida `/ping` endpoint

### Configuração de Secrets

Configure no GitHub: `Settings > Secrets and variables > Actions`

**Secrets Necessários:**
- `RAILWAY_TOKEN` - Token de autenticação Railway
- `RAILWAY_PROJECT_ID` - ID do projeto Railway

**Variables (opcional):**
- `HEALTHCHECK_URL` - URL customizada para healthcheck (padrão: metacerta.up.railway.app/ping)

### Obter Railway Token

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Obter token
railway whoami --token
```

### Obter Project ID

```bash
# No diretório do projeto
railway status
# ou
railway link
```

## 📁 Estrutura Essencial

```
vendacerta/
├── .github/workflows/
│   └── railway-deploy.yml      # CI/CD GitHub Actions
├── app.py                      # Aplicação Flask principal
├── wsgi.py                     # WSGI entry point com auto-fix
├── config.py                   # Configurações do sistema
├── models.py                   # Modelos SQLAlchemy
├── forms.py                    # Flask-WTForms
├── helpers.py                  # Funções auxiliares
├── requirements.txt            # Dependências Python
├── runtime.txt                 # Versão Python (3.11.x)
├── nixpacks.toml              # Config Railway build
├── Procfile                    # Comando de start (Gunicorn)
├── railway.json               # Config Railway (healthcheck)
├── templates/                  # Templates Jinja2
├── static/                     # Assets (CSS, JS, images)
├── modules/                    # Módulos do sistema
├── scripts/                    # Scripts utilitários
├── migrations_scripts/         # Migrações de banco
├── docs/                       # Documentação
└── fix_database_railway.py    # Auto-correção banco (WSGI)
```

## 🛠️ Arquivos de Configuração

### `Procfile`
```
web: gunicorn --config gunicorn_config.py wsgi:app
```

### `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "healthcheckPath": "/ping",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 5
  }
}
```

### `nixpacks.toml`
```toml
[phases.setup]
nixPkgs = ['python311']

[phases.install]
cmds = [
  'pip install --upgrade pip',
  'pip install -r requirements.txt'
]

[start]
cmd = 'gunicorn --config gunicorn_config.py wsgi:app'
```

## ⚙️ Variáveis de Ambiente (Railway)

Configurar no Railway Dashboard:

```env
# Database (Railway PostgreSQL interno)
DATABASE_URL=postgresql://...

# Flask
SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=production

# Timezone
TZ=America/Sao_Paulo

# Python
PYTHONUNBUFFERED=1
```

## 🔍 Healthcheck

Endpoint: `/ping`

**Resposta esperada:**
```json
{
  "status": "ok",
  "message": "VendaCerta API is running",
  "timestamp": "2026-01-03T12:00:00"
}
```

## 📊 Monitoramento

### Logs Railway
```bash
# Ver logs em tempo real
railway logs

# Filtrar por serviço
railway logs --service <service-name>
```

### Status do Deploy
- GitHub: `Actions` tab - ver workflow runs
- Railway: Dashboard - ver deploy status e logs

## 🚨 Troubleshooting

### Deploy falha com erro de import
- Verificar `requirements.txt` atualizado
- Confirmar versão Python em `runtime.txt`
- Checar logs de build no Railway

### Healthcheck falha
- Verificar se route `/ping` existe em `app.py`
- Confirmar timeout em `railway.json`
- Checar logs do Gunicorn

### Banco não atualiza
- Script `fix_database_railway.py` roda via `wsgi.py`
- Verificar `DATABASE_URL` configurado
- Checar logs WSGI no Railway

## 📝 Comandos Úteis

```bash
# Deploy manual (local)
railway up

# Link projeto
railway link <project-id>

# Ver variáveis
railway variables

# Executar comando no Railway
railway run <command>

# Abrir dashboard
railway open
```

## 🔒 Segurança

- ✅ `.env` no `.gitignore`
- ✅ Secrets via GitHub Secrets
- ✅ DATABASE_URL interna Railway
- ✅ HTTPS automático Railway
- ✅ WSGI com ProxyFix para headers seguros

## 📞 Suporte

Para problemas com deploy:
1. Verificar logs GitHub Actions
2. Verificar logs Railway
3. Confirmar secrets configurados
4. Validar `railway.json` e `Procfile`
