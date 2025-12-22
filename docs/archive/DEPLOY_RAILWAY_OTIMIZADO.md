# 🚀 Guia de Deploy Railway - Sistema SuaMeta

> **Atualizado**: 16/12/2025  
> **Versão**: 2.9.1  
> **Tempo Estimado**: 15-20 minutos

---

## 📋 Pré-requisitos

✅ Conta GitHub (gratuita)  
✅ Conta Railway (gratuita - $5 crédito inicial)  
✅ Código do sistema no GitHub  
✅ 15 minutos de tempo

---

## 🎯 Passo a Passo Completo

### **1. Preparar Repositório GitHub**

```bash
# Se ainda não tem o repositório
cd "c:\Users\Superação\Desktop\Sistema\vendacerta"

# Inicializar git (se necessário)
git init
git add .
git commit -m "Deploy inicial Railway - v2.9.1"

# Criar repositório no GitHub
# Acesse github.com → New repository → "suameta"

# Conectar e enviar
git remote add origin https://github.com/SEU_USUARIO/suameta.git
git branch -M main
git push -u origin main
```

---

### **2. Criar Projeto no Railway**

1. **Acessar Railway**
   - URL: https://railway.app
   - Clique em "Start a New Project"
   - Login com GitHub

2. **Deploy from GitHub**
   - Clique "Deploy from GitHub repo"
   - Autorize Railway a acessar seus repositórios
   - Selecione `suameta`
   - Railway detecta automaticamente Python/Flask

3. **Aguardar Build Inicial**
   - Primeiro build leva ~3-5 minutos
   - Acompanhe logs em tempo real
   - Status: Building → Deploying → Running

---

### **3. Adicionar PostgreSQL**

1. **Criar Database**
   - No projeto Railway, clique "New"
   - Selecione "Database" → "Add PostgreSQL"
   - Aguarde provisionamento (~30 segundos)

2. **Variáveis Automáticas**
   Railway cria automaticamente:
   ```
   DATABASE_URL
   PGDATABASE
   PGHOST
   PGPASSWORD
   PGPORT
   PGUSER
   ```

3. **Conectar ao Serviço**
   - Vá em "Variables" do serviço web
   - Adicione referência:
   ```
   DATABASE_URL = ${{Postgres.DATABASE_URL}}
   ```

---

### **4. Configurar Variáveis de Ambiente**

Na aba "Variables" do serviço web, adicione:

#### **Obrigatórias**

```bash
# Chave secreta (gerar nova)
SECRET_KEY=cole-aqui-chave-gerada-abaixo

# Ambiente
FLASK_ENV=production

# Banco de dados (referência ao PostgreSQL)
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

#### **Gerar SECRET_KEY**

No terminal local:
```bash
python -c "import secrets; print(secrets.token_urlsafe(96))"
```

Copie o resultado e cole em `SECRET_KEY`.

#### **Opcionais**

```bash
# Desabilitar backup local em produção
BACKUP_ENABLED=false

# Google Drive (se configurado)
GOOGLE_DRIVE_ENABLED=false

# Timezone
TZ=America/Sao_Paulo
```

---

### **5. Configurar Domínio**

1. **Gerar Domínio Railway**
   - Settings → "Generate Domain"
   - URL: `https://suameta-production.up.railway.app`

2. **Domínio Customizado (Opcional)**
   - Settings → "Custom Domain"
   - Adicione: `suameta.seudominio.com.br`
   - Configure DNS conforme instruções

---

### **6. Validar Deploy**

#### **Health Check**

```bash
# Ping básico
curl https://sua-url.up.railway.app/ping

# Resposta esperada:
{"status": "ok", "timestamp": "2025-12-16T10:30:00"}

# Health detalhado
curl https://sua-url.up.railway.app/health

# Resposta esperada:
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-16T10:30:00"
}
```

#### **Acessar Interface**

1. Abra: `https://sua-url.up.railway.app`
2. Deve aparecer página de login
3. Se erro 500: Verifique logs

---

### **7. Setup Inicial do Sistema**

#### **Criar Super Admin**

1. Acesse: `https://sua-url.up.railway.app/setup-inicial-sistema`
2. Preencha formulário:
   ```
   Username: admin
   Email: seu@email.com
   Nome: Seu Nome
   Senha: SenhaForte123!
   Confirmar Senha: SenhaForte123!
   Nome da Empresa: Sua Empresa
   ```
3. Clique "Criar Super Administrador"
4. Login automático

#### **Primeiros Passos**

1. **Criar Empresa** (se multi-tenant)
   - Menu: Empresas → Nova Empresa

2. **Criar Usuários**
   - Menu: Usuários → Novo Usuário
   - Defina cargo: Admin, Supervisor, Vendedor

3. **Criar Vendedores**
   - Menu: Vendedores → Novo Vendedor
   - Vincule a usuário (se necessário)

4. **Configurar Comissões**
   - Menu: Configurações → Faixas de Comissão
   - Ajuste percentuais conforme sua necessidade

5. **Criar Primeira Meta**
   - Menu: Configurar Metas Avançadas
   - Escolha vendedor, tipo, período
   - Calcule e salve

---

## ⚙️ Configurações Avançadas

### **Auto-Deploy do GitHub**

Railway já está configurado para auto-deploy:

```bash
# Qualquer push na branch main dispara deploy
git add .
git commit -m "Atualização do sistema"
git push origin main

# Railway automaticamente:
# 1. Detecta push
# 2. Inicia build
# 3. Roda testes
# 4. Faz deploy
# 5. Notifica resultado
```

### **Configurar Notificações**

1. Railway Dashboard → Projeto → Settings
2. Notificações → Webhook ou Email
3. Receba alertas de:
   - Deploy bem-sucedido
   - Falha no build
   - Erro em produção

### **Escalar Recursos**

#### **Plano Hobby** (Grátis - $5 crédito)
- 500 MB RAM
- 1 GB Disco
- $5/mês uso incluído
- Ideal para início

#### **Plano Pro** ($20/mês)
- 8 GB RAM
- 100 GB Disco
- Uso ilimitado
- Suporte prioritário

**Ajustar**:
1. Settings → Resources
2. Escolha: 512 MB, 1 GB, 2 GB, 4 GB, 8 GB
3. CPU ajustado automaticamente

---

## 🔍 Monitoramento e Logs

### **Ver Logs em Tempo Real**

#### **Via Interface Railway**
1. Projeto → Deployments
2. Clique no deployment ativo
3. Aba "Logs" - atualização automática

#### **Via Railway CLI**

```bash
# Instalar CLI
npm i -g @railway/cli

# Login
railway login

# Link ao projeto
railway link

# Ver logs
railway logs

# Seguir logs (tail)
railway logs --follow
```

### **Métricas**

1. Railway Dashboard → Projeto
2. Aba "Metrics"
3. Visualize:
   - CPU Usage
   - Memory Usage
   - Network I/O
   - Request Rate

---

## 🐛 Troubleshooting

### **Build Failed**

```bash
# Erro comum: Dependências faltando
# Solução: Verificar requirements.txt

# Ver erro exato
railway logs

# Build local para testar
pip install -r requirements.txt
```

### **500 Internal Server Error**

```bash
# 1. Ver logs
railway logs

# 2. Verificar variáveis de ambiente
railway variables

# 3. Confirmar DATABASE_URL
railway variables | grep DATABASE_URL

# 4. Testar health check
curl https://sua-url.up.railway.app/ping
```

### **Database Connection Error**

```bash
# 1. Verificar PostgreSQL está rodando
# Railway Dashboard → Database → Status: Running

# 2. Verificar variável DATABASE_URL
# Settings → Variables → DATABASE_URL

# 3. Testar conexão direta
railway run python -c "from app import db; print(db)"
```

### **Aplicação Lenta**

```bash
# 1. Verificar uso de recursos
# Metrics → CPU/Memory

# 2. Aumentar workers Gunicorn
# railway.json:
"workers": 4  # Padrão: 2

# 3. Adicionar cache (Redis)
# New → Database → Redis
```

---

## 🔒 Segurança em Produção

### **Checklist de Segurança**

- [x] `SECRET_KEY` única e forte (96+ caracteres)
- [x] `FLASK_ENV=production`
- [x] HTTPS ativo (Railway automático)
- [x] Variáveis sensíveis em Environment Variables
- [x] `.env` no `.gitignore`
- [x] Database password forte
- [x] CORS configurado (se API)
- [x] Rate limiting (opcional)

### **Backup PostgreSQL**

**Automático (Railway)**:
- Backups diários
- Retenção 7 dias
- Restauração 1-click

**Manual**:
```bash
# Exportar banco
railway run pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Importar banco
railway run psql $DATABASE_URL < backup_20251216.sql
```

---

## 📊 Performance

### **Otimizações Aplicadas**

#### **Gunicorn** (Servidor WSGI)
```bash
# railway.json - startCommand
workers: 2                    # Processos paralelos
timeout: 120                  # Timeout requests
worker-class: sync            # Modo síncrono
max-requests: 1000            # Restart worker após N requests
max-requests-jitter: 50       # Variação aleatória
```

#### **Caching** (Futuro)
```python
# Adicionar Flask-Caching
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@cache.cached(timeout=300)
def dashboard():
    # Cache por 5 minutos
```

---

## 🔄 Rollback (Reverter Deploy)

### **Se algo der errado após deploy:**

1. **Via Interface**
   - Deployments → Histórico
   - Clique no deployment anterior (verde)
   - "Redeploy"

2. **Via Git**
   ```bash
   # Reverter último commit
   git revert HEAD
   git push origin main
   
   # Railway faz deploy automático
   ```

---

## 📱 PWA - Progressive Web App

### **Já Configurado**

O sistema já inclui:
- ✅ `manifest.json` - Metadados do app
- ✅ `service-worker.js` - Cache offline
- ✅ Ícones em múltiplos tamanhos
- ✅ Meta tags PWA no `base.html`

### **Instalar como App**

**Android**:
1. Abra no Chrome
2. Menu → "Adicionar à tela inicial"
3. Ícone aparece na tela

**iOS**:
1. Abra no Safari
2. Compartilhar → "Adicionar à Tela Inicial"
3. Ícone aparece

**Desktop (Chrome)**:
1. Ícone de instalação na barra de endereço
2. Clique → "Instalar"

---

## 📞 Suporte Railway

### **Recursos Oficiais**

- 📚 Docs: https://docs.railway.app
- 💬 Discord: https://discord.gg/railway
- 🐦 Twitter: @Railway
- 📧 Email: team@railway.app

### **Status do Serviço**

- 🟢 Status: https://railway.statuspage.io
- Verifique antes de reportar problema

---

## ✅ Checklist Final

Antes de considerar deploy completo:

### **Técnico**
- [ ] Build bem-sucedido sem erros
- [ ] PostgreSQL provisionado e conectado
- [ ] Todas variáveis de ambiente configuradas
- [ ] Health check `/ping` retorna 200 OK
- [ ] Domínio gerado e acessível
- [ ] HTTPS ativo (cadeado verde)
- [ ] Logs sem erros críticos

### **Funcional**
- [ ] Página de login carrega corretamente
- [ ] Setup inicial funcional (`/setup-inicial-sistema`)
- [ ] Super admin criado com sucesso
- [ ] Login com super admin funciona
- [ ] Dashboard carrega sem erro 500
- [ ] Cadastro de vendedor funciona
- [ ] Cadastro de meta funciona
- [ ] Gráficos Chart.js renderizam
- [ ] Exportação PDF funciona
- [ ] Mensagens internas funcionam

### **Performance**
- [ ] Tempo de carregamento < 3s
- [ ] Gráficos renderizam rápido
- [ ] Sem erros no console do navegador
- [ ] Mobile responsivo testado

### **Segurança**
- [ ] SECRET_KEY forte e única
- [ ] FLASK_ENV=production
- [ ] Senhas de banco fortes
- [ ] `.env` não commitado no Git

---

## 🎉 Deploy Concluído!

Parabéns! Seu sistema SuaMeta está rodando em produção no Railway! 🚀

### **Próximos Passos**

1. ✅ Compartilhe URL com equipe
2. ✅ Configure backup automático
3. ✅ Treine usuários no sistema
4. ✅ Monitore logs nos primeiros dias
5. ✅ Colete feedback e ajuste

### **URLs Importantes**

- 🌐 **Sistema**: `https://sua-url.up.railway.app`
- 📊 **Dashboard Railway**: `https://railway.app/project/SEU_PROJETO`
- 📈 **Métricas**: Dashboard → Metrics
- 📝 **Logs**: Dashboard → Deployments → Logs

---

**Desenvolvido por**: Cristiano Santos  
**WhatsApp**: (71) 99337-2960  
**Email**: cristiano@prescrimed.com.br

*Última atualização: 16/12/2025*
