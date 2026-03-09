# 🚀 DEPLOY RÁPIDO - Railway

> ⚠️ **ARQUIVO LEGADO/ARQUIVADO**: pode conter exemplos antigos.
> Não use credenciais/senhas fixas; siga `docs/DEPLOY_RAILWAY.md`.

## ⚡ 5 Minutos para Colocar no Ar

### 1️⃣ Login no Railway
```
👉 Abra: https://railway.app
👉 Clique: "Login with GitHub"
👉 Autorize: Railway
```

### 2️⃣ Criar Projeto
```
👉 Clique: "New Project"
👉 Selecione: "Deploy from GitHub repo"
👉 Escolha: cristiano-superacao/vendacerta
👉 Clique: "Deploy Now"
```

### 3️⃣ Adicionar Banco
```
👉 Clique: "+ New"
👉 Selecione: "Database"
👉 Escolha: "Add PostgreSQL"
👉 Aguarde: Criação automática
```

### 4️⃣ Configurar Variáveis
```
👉 Clique no serviço do app
👉 Vá em: "Variables"
👉 Adicione:
   SECRET_KEY = VendaCerta2025SecretKey!@#$%
   FLASK_ENV = production
```

### 5️⃣ Gerar Domínio
```
👉 Vá em: "Settings"
👉 Role até: "Domains"
👉 Clique: "Generate Domain"
👉 Será: vendacerta.up.railway.app
```

---

## ✅ Pronto!

Aguarde 3-5 minutos e acesse:

```
🌐 https://vendacerta.up.railway.app
```

Login inicial:
```
📧 Email: (defina em `ADMIN_EMAIL`)
🔑 Senha: (defina em `ADMIN_PASSWORD`)
```

Crie/atualize o admin via `python scripts/create_admin.py`.

---

## 📚 Precisa de Ajuda?

Leia o guia completo: **DEPLOY_RAILWAY_COMPLETO.md**

- ✅ 15 passos detalhados
- ✅ Troubleshooting
- ✅ Otimizações
- ✅ Segurança
- ✅ Monitoramento

---

**Boa sorte com o deploy! 🎉**
