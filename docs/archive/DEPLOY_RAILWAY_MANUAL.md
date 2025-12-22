# 🚀 Deploy Railway - Finalização Manual

**Status:** ⚠️ Aguardando PostgreSQL  
**Data:** 17/12/2025  
**Projeto:** mettacerta

---

## ✅ JÁ CONFIGURADO

### 1. Railway CLI Instalado ✅
```bash
railway --version
# v4.12.0
```

### 2. Projeto Vinculado ✅
```bash
Project: mettacerta
Environment: production
Service: mettacerta (aec2b62a-a9fa-43af-95b1-e1499967708d)
```

### 3. Variáveis Configuradas ✅
```bash
SECRET_KEY=513652f64505d922cea51ad3e692b593e8b309fe64a68e3c5b18a98e4b01d672
FLASK_ENV=production
PYTHONUNBUFFERED=1
```

### 4. Código Atualizado no GitHub ✅
```bash
Commit: ea3014a - fix: Simplify railway.json
Branch: main
```

---

## 🔴 PENDENTE - AÇÃO NECESSÁRIA

### 1. Adicionar PostgreSQL Database

**Via Railway Dashboard:**

1. **Acesse:** https://railway.com/project/e5727da0-17ad-4823-8fc0-25f73e012ae6

2. **Clique em:** `+ New Service`

3. **Selecione:** `Database` → `PostgreSQL`

4. **Aguarde provisionamento** (~30 segundos)

5. **Variáveis automáticas criadas:**
   ```
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   PGDATABASE=railway
   PGHOST=<host>.railway.app
   PGUSER=postgres
   PGPASSWORD=<password>
   PGPORT=5432
   ```

### 2. Conectar PostgreSQL ao Serviço

**Ainda no Dashboard:**

1. **No serviço `mettacerta`** → aba `Variables`

2. **Add Reference Variable:**
   ```
   DATABASE_URL = ${{Postgres.DATABASE_URL}}
   PGPASSWORD = ${{Postgres.PGPASSWORD}}
   ```

3. **Salvar** (deploy automático será disparado)

---

## 🚀 Deploy Automático

Após adicionar PostgreSQL, o Railway fará deploy automático:

```
1. Build inicia (~2-3 min)
   ├─ Setup: Python 3.11
   ├─ Install: 25 pacotes
   └─ Build: init_railway.py

2. Deploy (Gunicorn) (~1-2 min)
   ├─ Health check /ping
   ├─ Start Gunicorn (2 workers)
   └─ Logs em tempo real

3. ✅ Aplicação Online!
   └─ https://mettacerta.up.railway.app (domínio gerado)
```

---

## 📋 Alternativa - Railway CLI

Se preferir configurar PostgreSQL via CLI:

```bash
# Adicionar PostgreSQL ao projeto (via dashboard apenas)
# Depois, referenciar no serviço:

railway variables --set "DATABASE_URL=\${{Postgres.DATABASE_URL}}" --set "PGPASSWORD=\${{Postgres.PGPASSWORD}}"

# Fazer deploy manual
railway up
```

**Nota:** A criação do PostgreSQL deve ser feita pelo Dashboard, pois o CLI não suporta `railway add postgres` diretamente.

---

## ✅ Verificação Pós-Deploy

Após deploy concluído:

### 1. Health Check
```bash
curl https://mettacerta.up.railway.app/ping

# Resposta esperada:
{
  "status": "ok",
  "timestamp": "2025-12-17T...",
  "service": "vendacerta",
  "version": "2.0"
}
```

### 2. Logs
```bash
railway logs --tail 100

# Ou via dashboard:
# https://railway.com/project/.../deployments
```

### 3. Acesso
```
https://mettacerta.up.railway.app
```

---

## 📊 Status das Variáveis

### ✅ Configuradas (3/5)
- `SECRET_KEY` ✅
- `FLASK_ENV=production` ✅
- `PYTHONUNBUFFERED=1` ✅

### ⏳ Pendentes (2/5)
- `DATABASE_URL` - Aguardando PostgreSQL
- `PGPASSWORD` - Aguardando PostgreSQL

---

## 🎯 Próximos Passos

1. **Acesse Railway Dashboard:**
   ```
   https://railway.com/project/e5727da0-17ad-4823-8fc0-25f73e012ae6
   ```

2. **Adicione PostgreSQL:**
   - Click `+ New Service`
   - Selecione `Database` → `PostgreSQL`
   - Aguarde ~30 segundos

3. **Conecte ao Serviço:**
   - Vá em `mettacerta` → `Variables`
   - Add: `DATABASE_URL = ${{Postgres.DATABASE_URL}}`
   - Add: `PGPASSWORD = ${{Postgres.PGPASSWORD}}`
   - Salve

4. **Aguarde Deploy:**
   - Deploy automático (~3-5 min)
   - Monitore em `Deployments`

5. **Teste a Aplicação:**
   ```bash
   curl https://mettacerta.up.railway.app/ping
   ```

---

## 📞 Recursos

**Railway Dashboard:**  
https://railway.com/project/e5727da0-17ad-4823-8fc0-25f73e012ae6

**Documentação:**
- [Guia Completo Railway](docs/GUIA_COMPLETO_RAILWAY.md)
- [Resumo Railway](docs/RESUMO_RAILWAY.md)
- [Health Check Script](scripts/railway_healthcheck.py)

**Suporte Railway:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

---

## ✅ Resumo

**Status Atual:**
- ✅ Railway CLI configurado
- ✅ Projeto vinculado
- ✅ 3/5 variáveis configuradas
- ✅ Código no GitHub atualizado
- ⏳ PostgreSQL pendente (ação manual no dashboard)

**Próximo Passo:**  
**→ Adicionar PostgreSQL via Railway Dashboard**

**Tempo Estimado:** 5 minutos  
**Deploy Automático Após:** 3-5 minutos

---

**🚂 Sistema pronto para deploy final após adicionar PostgreSQL!**

**Data:** 17/12/2025  
**Projeto:** mettacerta  
**Commit:** ea3014a
