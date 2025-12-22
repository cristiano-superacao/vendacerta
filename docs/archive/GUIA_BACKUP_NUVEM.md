# 🔐 Guia Completo: Backup Nuvem + Local - SuaMeta

## 📊 Status Atual do Sistema

### ✅ O que já está funcionando:
- ✅ Banco de dados local (SQLite) salvando todos os dados
- ✅ Sistema de backup automático configurado (diário às 02:00)
- ✅ Política de retenção (últimos 7 backups)
- ✅ Limpeza automática de backups antigos
- ✅ Layout responsivo e profissional mantido

### ⚠️ O que precisa ser configurado:
- ⚠️ Salvamento na nuvem (PostgreSQL Railway)
- ⚠️ Backup redundante na nuvem

---

## 🌐 OPÇÃO 1: Configurar Salvamento na Nuvem (Railway)

### Vantagens:
- 🔄 Backup automático do Railway
- 🌍 Acesso de qualquer lugar
- 📈 Escalabilidade automática
- 🔒 Alta disponibilidade
- 💾 Redundância nativa

### Passo a Passo:

#### 1️⃣ Criar Conta e Projeto no Railway

1. Acesse: https://railway.app
2. Clique em "Start a New Project"
3. Conecte com GitHub ou Google
4. Crie um novo projeto

#### 2️⃣ Adicionar PostgreSQL

```bash
# No painel do Railway:
1. Clique em "+ New"
2. Selecione "Database"
3. Escolha "PostgreSQL"
4. Aguarde provisionar (~1 minuto)
```

#### 3️⃣ Obter DATABASE_URL

```bash
# No PostgreSQL criado:
1. Clique na aba "Connect"
2. Copie a "Postgres Connection URL"
3. Formato: postgresql://user:password@host:port/database
```

#### 4️⃣ Configurar Variável de Ambiente

**Windows (PowerShell como Administrador):**
```powershell
# Definir variável permanente
setx DATABASE_URL "postgresql://usuario:senha@host:porta/banco"

# OU criar arquivo .env na raiz do projeto:
# Criar arquivo .env:
New-Item -Path .env -ItemType File -Force

# Adicionar ao .env:
Add-Content -Path .env -Value "DATABASE_URL=postgresql://usuario:senha@host:porta/banco"
Add-Content -Path .env -Value "FLASK_ENV=production"
```

**Linux/Mac:**
```bash
# Adicionar ao ~/.bashrc ou ~/.zshrc
echo 'export DATABASE_URL="postgresql://usuario:senha@host:porta/banco"' >> ~/.bashrc
source ~/.bashrc

# OU criar arquivo .env
echo "DATABASE_URL=postgresql://usuario:senha@host:porta/banco" > .env
echo "FLASK_ENV=production" >> .env
```

#### 5️⃣ Instalar Dependências PostgreSQL

```bash
# Instalar psycopg2 (driver PostgreSQL)
pip install psycopg2-binary

# Atualizar requirements.txt
pip freeze > requirements.txt
```

#### 6️⃣ Migrar Dados

```bash
# 1. Fazer backup do SQLite atual
python -c "import shutil; shutil.copy('instance/metas.db', 'backup_antes_migracao.db')"

# 2. Recriar tabelas no PostgreSQL
python init_db.py

# 3. Opcional: Migrar dados existentes
# (Criar script de migração se necessário)
```

#### 7️⃣ Deploy no Railway

```bash
# 1. Instalar Railway CLI
# Windows:
npm install -g @railway/cli

# 2. Login
railway login

# 3. Link ao projeto
railway link

# 4. Deploy
railway up
```

---

## 💾 OPÇÃO 2: Manter Local + Backup Duplo

### Configuração Atual (Já Implementada):

```python
# Sistema de backup automático configurado em app.py
backup_config = {
    'enabled': True,
    'frequency': 'daily',  # Diário
    'time': '02:00',       # 02:00 da manhã
    'keep_last': 7,        # Últimos 7 backups
    'auto_cleanup': True   # Limpa backups antigos
}
```

### Estrutura de Backups:

```
instance/
├── metas.db                          # Banco principal
└── backups/
    ├── auto_backup_20251215_020000.db  # Backup automático hoje
    ├── auto_backup_20251214_020000.db  # Ontem
    ├── auto_backup_20251213_020000.db  # 2 dias atrás
    ├── auto_backup_20251212_020000.db  # 3 dias atrás
    ├── auto_backup_20251211_020000.db  # 4 dias atrás
    ├── auto_backup_20251210_020000.db  # 5 dias atrás
    └── auto_backup_20251209_020000.db  # 6 dias atrás (último mantido)
```

### Adicionar Backup na Nuvem (Google Drive/OneDrive):

#### Método 1: Google Drive (Manual)

```bash
# 1. Instalar Google Drive Desktop
# Windows: Baixar de https://www.google.com/drive/download/

# 2. Configurar sincronização
# - Apontar para a pasta instance/backups/
# - Ativar sincronização automática
```

#### Método 2: Automação com Python (Recomendado)

Criar arquivo `backup_nuvem.py`:

```python
import os
import shutil
from datetime import datetime
from pathlib import Path

# Configurações
BACKUP_LOCAL = Path('instance/backups')
BACKUP_NUVEM = Path('C:/Users/Superação/OneDrive/SuaMeta_Backups')
# OU
# BACKUP_NUVEM = Path('C:/Users/Superação/Google Drive/SuaMeta_Backups')

def sincronizar_backup_nuvem():
    """Copia backups locais para nuvem"""
    try:
        # Criar pasta na nuvem se não existir
        BACKUP_NUVEM.mkdir(parents=True, exist_ok=True)
        
        # Copiar todos os backups
        if BACKUP_LOCAL.exists():
            for backup_file in BACKUP_LOCAL.glob('*.db'):
                destino = BACKUP_NUVEM / backup_file.name
                shutil.copy2(backup_file, destino)
                print(f'✅ Copiado: {backup_file.name}')
        
        print(f'🌐 Backup na nuvem concluído: {BACKUP_NUVEM}')
    except Exception as e:
        print(f'❌ Erro ao sincronizar: {e}')

if __name__ == '__main__':
    sincronizar_backup_nuvem()
```

Adicionar ao `app.py` para executar após cada backup:

```python
def criar_backup_automatico():
    """Cria backup automático do banco de dados"""
    with app.app_context():
        try:
            # ... código existente ...
            
            # NOVO: Sincronizar com nuvem
            try:
                from backup_nuvem import sincronizar_backup_nuvem
                sincronizar_backup_nuvem()
            except Exception as e:
                app.logger.error(f'Erro na sincronização com nuvem: {e}')
                
        except Exception as e:
            app.logger.error(f'❌ Erro ao criar backup automático: {str(e)}')
```

---

## 🎯 Recomendação Final

### Para Produção (Recomendado):
```
✅ Railway PostgreSQL (Nuvem)
  └─> Backup automático do Railway
  └─> Dados sempre disponíveis
  └─> Sem preocupação com backups manuais

OPCIONAL: Export manual mensal para segurança extra
```

### Para Desenvolvimento/Pequeno Porte:
```
✅ SQLite Local
  └─> Backup automático local (02:00 diariamente)
  └─> Sincronização com Google Drive/OneDrive
  └─> Backup duplo garantido
```

---

## 📋 Checklist de Implementação

### Opção Nuvem (Railway):
- [ ] Criar conta no Railway
- [ ] Provisionar PostgreSQL
- [ ] Copiar DATABASE_URL
- [ ] Configurar variável de ambiente
- [ ] Instalar psycopg2-binary
- [ ] Executar init_db.py
- [ ] Testar conexão
- [ ] Deploy da aplicação

### Opção Local + Nuvem:
- [x] Backup automático local configurado ✅
- [ ] Instalar Google Drive Desktop
- [ ] Configurar pasta de sincronização
- [ ] Testar sincronização
- [ ] Validar backups na nuvem
- [ ] (Opcional) Automatizar com backup_nuvem.py

---

## 🔍 Comandos Úteis

### Testar Backup Imediato:
```bash
# Executar backup manual
python -c "from app import criar_backup_automatico; criar_backup_automatico()"
```

### Verificar Status:
```bash
# Executar verificação
python verificar_backup.py
```

### Listar Backups:
```bash
# Windows
dir instance\backups

# Linux/Mac
ls -lh instance/backups/
```

### Restaurar Backup:
```bash
# 1. Parar aplicação
# 2. Fazer backup do atual
copy instance\metas.db instance\metas_antes_restaurar.db

# 3. Restaurar
copy instance\backups\auto_backup_YYYYMMDD_HHMMSS.db instance\metas.db

# 4. Reiniciar aplicação
```

---

## 🚨 Avisos Importantes

### ⚠️ Segurança:
- **NUNCA** commite DATABASE_URL no Git
- Use `.env` ou variáveis de ambiente
- Adicione `.env` ao `.gitignore`

### ⚠️ Migração:
- Sempre faça backup antes de migrar
- Teste em ambiente de desenvolvimento primeiro
- Valide dados após migração

### ⚠️ Custos:
- **Railway**: Plano gratuito inicial (500h/mês)
- **PostgreSQL Railway**: $5/mês após trial
- **Google Drive**: 15GB grátis
- **OneDrive**: 5GB grátis

---

## 📞 Próximos Passos Recomendados

1. **Decidir estratégia:**
   - Nuvem total (Railway)? → Seguir "OPÇÃO 1"
   - Local + sincronização? → Seguir "OPÇÃO 2"

2. **Testar backup atual:**
   ```bash
   python verificar_backup.py
   ```

3. **Configurar monitoramento:**
   - Verificar logs diários
   - Validar backups semanalmente
   - Testar restauração mensalmente

4. **Documentar:**
   - Manter registro de DATABASE_URL seguro
   - Documentar procedimento de restauração
   - Criar runbook para emergências

---

**Data:** 15/12/2025  
**Versão:** 1.0  
**Status:** 🟡 Backup Local Ativo, Nuvem Pendente  
**Layout:** ✅ Responsivo e Profissional Mantido
