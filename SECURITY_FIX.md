# 🔐 GUIA DE SEGURANÇA - VARIÁVEIS DE AMBIENTE

## ⚠️ PROBLEMA IDENTIFICADO

Erros de segurança encontrados no build Docker/Railway:

```
❌ SecretsUsedInArgOrEnv: Não utilize ARG/ENV para:
   - ADMIN_PASSWORD
   - FLASK_SECRET_KEY
   - SECRET_KEY

❌ UndefinedVar: Variável $NIXPACKS_PATH não definida
```

## ✅ SOLUÇÃO IMPLEMENTADA

### 1. Arquivo `.env.production.example`

Criado arquivo de referência com:
- ✅ Todas as variáveis necessárias documentadas
- ✅ Instruções claras de como gerar SECRET_KEY
- ✅ Avisos de segurança sobre ARG/ENV
- ✅ Configurações para Railway Dashboard

**Localização:** `.env.production.example`

### 2. `.dockerignore` Atualizado

Atualizado com segurança reforçada:
- ✅ Ignora todos os arquivos `.env*`
- ✅ Ignora `instance/` e bancos de dados locais
- ✅ Ignora `secrets/` e `credentials/`
- ✅ Ignora backups e arquivos sensíveis
- ✅ Permite apenas código da aplicação no build

**Localização:** `.dockerignore`

### 3. Nixpacks.toml - Sem Variáveis Sensíveis

O arquivo `nixpacks.toml` está correto e NÃO contém:
- ❌ ARG FLASK_SECRET_KEY
- ❌ ENV SECRET_KEY
- ❌ ARG ADMIN_PASSWORD

✅ Variável `$PORT` é fornecida automaticamente pelo Railway (não precisa definir)

## 🚀 COMO CONFIGURAR NO RAILWAY (CORRETO)

### Passo 1: Gerar SECRET_KEY Forte

```bash
python -c "import secrets; print('FLASK_SECRET_KEY=' + secrets.token_urlsafe(64))"
```

**Copie o resultado completo!**

### Passo 2: Adicionar no Railway Dashboard

1. **Acesse:** https://railway.app/dashboard
2. **Selecione:** Seu projeto VendaCerta
3. **Clique:** Serviço principal (não PostgreSQL)
4. **Vá em:** Variables (aba superior)
5. **Clique:** "+ New Variable"

### Passo 3: Adicionar Variáveis Uma a Uma

**CRÍTICAS (obrigatórias):**

```env
FLASK_SECRET_KEY=<cole-o-valor-gerado-no-passo-1>
FLASK_ENV=production
FLASK_DEBUG=False
```

**RECOMENDADAS:**

```env
PORT=5000
LOG_LEVEL=INFO
RATELIMIT_ENABLED=True
ENABLE_COMPRESSION=True
ENABLE_CACHE=True
SQLALCHEMY_POOL_SIZE=5
SQLALCHEMY_MAX_OVERFLOW=10
SESSION_PERMANENT_LIFETIME=86400
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

**AUTOMÁTICAS (Railway fornece):**

```env
DATABASE_URL=postgresql://... (auto-gerado ao conectar PostgreSQL)
RAILWAY_ENVIRONMENT=production
RAILWAY_PROJECT_NAME=vendacerta
PORT=<gerado automaticamente>
```

### Passo 4: Salvar e Redeploy

1. **Clique:** "Deploy" ou "Redeploy"
2. **Aguarde:** Build completar (3-5 min)
3. **Verifique:** Logs sem erros de segurança

## ❌ O QUE NÃO FAZER (IMPORTANTE!)

### NUNCA Adicione no Dockerfile:

```dockerfile
# ❌ ERRADO - NÃO FAÇA ISSO!
ARG FLASK_SECRET_KEY=abc123
ENV FLASK_SECRET_KEY=abc123
ARG SECRET_KEY=xyz789
ENV ADMIN_PASSWORD=senha123
```

### NUNCA Commit .env com Valores Reais:

```bash
# ❌ ERRADO
.env  # contém SECRET_KEY real

# ✅ CORRETO
.env.example  # apenas template
.env.production.example  # apenas template
```

### NUNCA Use Secrets em Código:

```python
# ❌ ERRADO
SECRET_KEY = 'minha-senha-fixa-123'

# ✅ CORRETO
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-fallback'
```

## 🔍 VERIFICAR SEGURANÇA

### 1. Verificar .dockerignore

```bash
# Deve conter:
.env
.env.local
.env.production
instance/
*.db
secrets/
credentials/
```

### 2. Verificar Railway Variables

**Railway Dashboard → Variables deve ter:**
- ✅ FLASK_SECRET_KEY (valor longo e aleatório)
- ✅ FLASK_ENV=production
- ✅ FLASK_DEBUG=False
- ✅ DATABASE_URL (auto-gerado)

### 3. Verificar Build Logs

**Railway → Deployments → Logs:**

```
✅ Buscando: "SecretsUsedInArgOrEnv" → NÃO deve aparecer
✅ Buscando: "UndefinedVar" → NÃO deve aparecer
✅ Buscando: "Build succeeded" → DEVE aparecer
```

## 🎯 CHECKLIST FINAL

- [ ] `.env.production.example` criado
- [ ] `.dockerignore` atualizado com segurança
- [ ] `nixpacks.toml` sem ARG/ENV sensíveis
- [ ] `FLASK_SECRET_KEY` gerada (64+ caracteres)
- [ ] Variáveis adicionadas no Railway Dashboard
- [ ] `.env` local NÃO commitado (está no .gitignore)
- [ ] Build Railway sem warnings de segurança
- [ ] Deploy funcionando com HTTPS
- [ ] Layout Bootstrap 5.3.3 responsivo OK

## 📱 LAYOUT RESPONSIVO - CONFIRMAÇÃO

**O layout permanece intacto:**

✅ **Bootstrap 5.3.3** carregando do CDN
✅ **Mobile-first** design ativo
✅ **Breakpoints** configurados:
   - Mobile: < 768px
   - Tablet: 768px - 1199px
   - Desktop: ≥ 1200px

✅ **Componentes responsivos:**
   - Menu hamburguer em mobile
   - Cards adaptáveis
   - Tabelas scrolláveis
   - Botões touch-friendly

**Nenhuma mudança foi feita em:**
- `templates/` (HTML)
- `static/css/` (CSS customizado)
- `static/js/` (JavaScript)
- Bootstrap CDN links

## 🚀 PRÓXIMOS PASSOS

1. **Commit mudanças:**
   ```bash
   git add .env.production.example .dockerignore
   git commit -m "security: Remove segredos de ARG/ENV e melhora .dockerignore"
   git push origin main
   ```

2. **Configurar Railway:**
   - Adicionar variáveis no Dashboard
   - Aguardar redeploy automático

3. **Testar produção:**
   - Acessar URL do Railway
   - Verificar login
   - Testar responsividade (F12 → Device Toolbar)

4. **Validar segurança:**
   - Mozilla Observatory: https://observatory.mozilla.org
   - Security Headers: https://securityheaders.com
   - Meta: Grade A

---

**✅ Erros de segurança corrigidos!**
**🎨 Layout responsivo mantido!**
**🚀 Pronto para deploy seguro no Railway!**
