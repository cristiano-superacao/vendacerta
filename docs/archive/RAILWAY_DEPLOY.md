# 🚀 Deploy no Railway - Guia Completo

## 📋 Pré-requisitos

- Conta no [Railway.app](https://railway.app)
- Repositório GitHub com o código
- PostgreSQL configurado no Railway

## 🎯 Passo a Passo

### 1️⃣ Criar Novo Projeto no Railway

1. Acesse [Railway.app](https://railway.app)
2. Clique em **"New Project"**
3. Selecione **"Deploy from GitHub repo"**
4. Escolha o repositório `cristiano-superacao/suameta`

### 2️⃣ Adicionar PostgreSQL

1. No projeto Railway, clique em **"+ New"**
2. Selecione **"Database"** → **"PostgreSQL"**
3. O Railway criará automaticamente a variável `DATABASE_URL`

### 3️⃣ Configurar Variáveis de Ambiente

No painel do Railway, vá em **Variables** e adicione:

```env
FLASK_ENV=production
SECRET_KEY=<gere-uma-chave-aleatoria-segura>
INIT_DB_ONLY=1
FLASK_DEBUG=0
```

**Gerar SECRET_KEY segura:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4️⃣ Configurações Automáticas

O Railway detecta automaticamente:

- ✅ **Nixpacks** como builder (via `nixpacks.toml`)
- ✅ **Python** como runtime
- ✅ **PORT** variável (Railway define automaticamente)
- ✅ **DATABASE_URL** do PostgreSQL

### 5️⃣ Deploy Automático

O Railway executa automaticamente:

1. **Build**: `pip install -r requirements.txt`
2. **Init DB**: `python init_db.py` (cria tabelas e usuários)
3. **Start**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

## 🔐 Credenciais Padrão

Após o primeiro deploy, acesse com:

### 👑 Super Administrador
- **Email**: `admin@suameta.com.br`
- **Senha**: `Admin@2025!`

### 🏢 Gerente da Empresa
- **Email**: `gerente@suameta.com.br`
- **Senha**: `Gerente@2025!`

⚠️ **IMPORTANTE**: Altere as senhas após o primeiro acesso!

## 📊 Monitoramento

### Health Check
O sistema possui endpoint de health check em:
```
https://seu-app.railway.app/ping
```

### Logs
Acesse os logs do Railway em tempo real:
1. Clique no serviço **web**
2. Vá na aba **"Deployments"**
3. Clique no deploy ativo
4. Visualize os logs

## 🔧 Arquivos de Configuração

### `railway.json`
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python init_db.py && gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120",
    "healthcheckPath": "/ping",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `nixpacks.toml`
```toml
[phases.setup]
providers = ["python"]

[phases.install]
cmd = "pip install -r requirements.txt"

[start]
cmd = "python init_db.py && gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120"
```

### `Procfile` (fallback)
```
web: python init_db.py && gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

## 🐛 Troubleshooting

### Erro: "Health check failed"
- Verifique se `/ping` está respondendo
- Aumente `healthcheckTimeout` se necessário
- Veja logs para identificar erro de inicialização

### Erro: "Database connection failed"
- Confirme que PostgreSQL está rodando
- Verifique variável `DATABASE_URL`
- Teste conexão com: `psql $DATABASE_URL`

### Erro: "Application timeout"
- Aumente `GUNICORN_TIMEOUT` (padrão: 120s)
- Verifique código que pode estar travando
- Analise logs de erro

### Banco não inicializa
- Veja logs do `init_db.py`
- Confirme que `INIT_DB_ONLY=1` está configurado
- Verifique permissões do banco de dados

## 🔄 Redeploy

Para fazer redeploy após alterações:

```bash
git add .
git commit -m "feat: suas alterações"
git push origin main
```

O Railway faz deploy automático ao detectar push na branch `main`.

## 📱 Domínio Personalizado

1. No Railway, vá em **Settings** → **Domains**
2. Clique em **"Generate Domain"** (domínio .railway.app)
3. Ou adicione domínio personalizado:
   - Clique em **"Custom Domain"**
   - Digite seu domínio
   - Configure DNS conforme instruções

## 🎨 PWA (Progressive Web App)

O sistema já está configurado como PWA:
- ✅ `manifest.json` configurado
- ✅ Service Worker (`sw.js`)
- ✅ Ícones para instalação
- ✅ Meta tags PWA

Os usuários podem instalar o app:
- **Android**: Chrome → Menu → "Adicionar à tela inicial"
- **iOS**: Safari → Compartilhar → "Adicionar à tela inicial"
- **Desktop**: Chrome → Ícone de instalação na barra de endereço

## 📞 Suporte

- 📧 Email: contato@suameta.com.br
- 📱 Telefone: (11) 99999-9999
- 🌐 Railway Docs: [docs.railway.app](https://docs.railway.app)

---

✨ **Sistema pronto para produção!** ✨
