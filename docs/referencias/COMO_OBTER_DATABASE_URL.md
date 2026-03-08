# 🎯 PASSOS PARA OBTER A DATABASE_URL DO RAILWAY

## 📍 Você está aqui → Precisa da URL do PostgreSQL

### Passo a Passo Visual:

1. **No Railway (que acabei de abrir para você):**
   - Faça login se necessário
   - Você verá seus projetos

2. **Clique no projeto "mettacerta"** (ou nome similar)
   - Você verá cards: um para a aplicação web e um para PostgreSQL

3. **Clique no card "PostgreSQL"** (ícone de banco de dados)
   - Uma página lateral vai abrir

4. **Clique na aba "Connect"** (no topo)
   - Você verá várias informações de conexão

5. **Procure por "Postgres Connection URL"**
   - Será algo assim:
   ```
   postgresql://postgres:AbC123XyZ@containers-us-west-12.railway.app:7432/railway
   ```

6. **Clique no ícone de copiar** ao lado da URL

7. **Execute este comando** e cole a URL quando pedir:

```powershell
C:/Users/Superação/Desktop/Sistema/Metas/.venv/Scripts/python.exe obter_database_url.py
```

---

## ⚡ OU Atalho Rápido:

Se preferir fazer direto sem o script:

```powershell
# 1. Defina a variável (COLE A URL REAL)
$env:DATABASE_URL = "cole_aqui_a_url_do_railway"

# 2. Execute a migração
C:/Users/Superação/Desktop/Sistema/Metas/.venv/Scripts/python.exe aplicar_migracao_railway.py
```

---

## 🔍 Como Identificar a URL Correta:

✅ **URL CORRETA** começa com:
- `postgresql://postgres:...@containers...railway.app`
- `postgres://...@railway.app`

❌ **URL ERRADA** (exemplos que NÃO funcionam):
- `SQLALCHEMY_DATABASE_URI` ← Nome da variável, não a URL
- `sqlite:///metas.db` ← Banco local, não Railway
- `${{Postgres.DATABASE_URL}}` ← Sintaxe Railway, não URL real

---

## 💡 Dica:

A URL tem **senha sensível**. Não compartilhe em screenshots ou mensagens públicas!

