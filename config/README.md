# ⚙️ Configurações

Arquivos de configuração e variáveis de ambiente do sistema.

## 📁 Arquivos

### `.env.example`
Template de variáveis de ambiente para desenvolvimento local.

**Uso**:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

### `.env.production`
Configurações para ambiente de produção.

### `.env.railway`
Configurações específicas para deploy no Railway.

### `.railway_db_url.txt`
URL de conexão do banco de dados PostgreSQL do Railway.

---

## 🔒 Segurança

⚠️ **NUNCA** commite arquivos `.env` reais no git!

Os arquivos `.env` estão no `.gitignore` e são apenas para referência.

---

## 📝 Variáveis Principais

```bash
# Flask
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Railway (automático)
RAILWAY_ENVIRONMENT=production
```

---

**Atualizado**: Dezembro 12, 2025
