# ⚡ Deploy Railway - 3 Passos Rápidos

> **Sistema VendaCerta** | Layout Bootstrap 5.3.3 Responsivo

---

## 🚀 Deploy em 5 Minutos

### 1️⃣ Criar Projeto Railway

1. Acesse: **https://railway.app**
2. **New Project** → **Deploy from GitHub repo**
3. Selecione: `cristiano-superacao/vendacerta`
4. **+ New** → **Database** → **PostgreSQL**

### 2️⃣ Configurar 9 Variáveis

Clique no serviço vendacerta → **Variables** → Cole (uma por linha):

```bash
FLASK_SECRET_KEY=${{ secret() }}
FLASK_ENV=production
FLASK_DEBUG=False
PYTHONUNBUFFERED=1
VERSAO_DO_PYTHON=3.11
TEMPO_DE_TEMPO_DE_GUNICORNIO=120
CONCORRENCIA_WEB=2
URL_DO_BANCO_DE_DADOS=${DATABASE_URL}
SKIP_INIT=0
```

### 3️⃣ Aguardar e Testar

1. **Deployments** → Aguarde ✅ Success (~2-3 min)
2. **Settings** → **Generate Domain**
3. Teste: `seu-app.up.railway.app/ping`
4. Login: `admin@vendacerta.com` / `admin123`

---

## 📚 Precisa de Ajuda?

- **Guia Completo**: [RAILWAY_DEPLOY_GUIA.md](RAILWAY_DEPLOY_GUIA.md) (334 linhas detalhadas)
- **Template de Variáveis**: [.env.railway.example](.env.railway.example)
- **Verificação Pré-Deploy**: `python check_railway_ready.py`

---

**Sistema**: VendaCerta  
**Layout**: Bootstrap 5.3.3 Responsivo  
**Deploy**: Railway + PostgreSQL + Gunicorn
