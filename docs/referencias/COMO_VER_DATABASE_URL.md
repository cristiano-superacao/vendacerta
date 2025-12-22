# 🎯 COMO OBTER A DATABASE_URL - PASSO A PASSO

## Na imagem que você enviou, vejo a página Variables do Railway.

### ✨ Método 1: Expandir Variáveis Ocultas (MAIS RÁPIDO)

Na página que está aberta:

1. **Role a página para baixo** até ver:
   ```
   8 variables added by Railway
   ```

2. **Clique nessa linha** para expandir

3. Você verá várias variáveis, incluindo:
   - `DATABASE_URL`
   - `DATABASE_PRIVATE_URL`
   - `DATABASE_PUBLIC_URL`

4. **Copie o valor de `DATABASE_URL`**
   - Clique no ícone de copiar (📋) ao lado
   - Ou selecione e copie com Ctrl+C

---

### ✨ Método 2: Via Connect (ALTERNATIVO)

Se o Método 1 não funcionar:

1. Clique em **"Architecture"** (no topo da página)
2. Você verá 2 cards: **web** e **Postgres**
3. Clique no card **"Postgres"** (PostgreSQL)
4. Clique na aba **"Connect"**
5. Procure **"Postgres Connection URL"**
6. Clique no ícone de copiar

---

## 🚀 Depois de Copiar:

Execute este comando e cole a URL:

```powershell
C:/Users/Superação/Desktop/Sistema/Metas/.venv/Scripts/python.exe configurar_railway.py
```

**A URL deve começar com:** `postgresql://postgres:...`

---

## ⚠️ NÃO Cole:

- ❌ Números (1, 2, 3...)
- ❌ Nomes de variáveis (DATABASE_URL, PGHOST...)
- ❌ sqlite:///metas.db

## ✅ Cole a URL COMPLETA:

Exemplo do formato correto:
```
postgresql://postgres:AbC123XyZ@containers-us-west-45.railway.app:7432/railway
```

---

## 💡 Dica:

Se ainda não conseguir, tire um print expandindo as "8 variables added by Railway" que eu te ajudo!
