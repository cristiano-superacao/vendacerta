# 🛡️ Proteção de Dados no Deploy - Sistema de Metas

## 📋 Visão Geral

Este documento garante que **NENHUM DADO seja apagado** durante atualizações do sistema em produção.

---

## ✅ Configurações de Proteção

### 1️⃣ **Banco de Dados PostgreSQL (Railway/Render)**

#### Como Funciona:
- ✅ **Banco de dados separado**: PostgreSQL em instância independente
- ✅ **Dados persistem**: Mesmo com redeploy do app
- ✅ **DATABASE_URL**: Variável de ambiente aponta para banco externo
- ✅ **Migrations**: Apenas adiciona colunas, nunca remove dados

#### Garantias:
```python
# models.py - Migrations sempre aditivas
# ✅ CORRETO: Adicionar colunas
def upgrade():
    op.add_column('vendedores', sa.Column('novo_campo', sa.String(100)))

# ❌ ERRADO: Remover colunas (nunca fazer!)
# def upgrade():
#     op.drop_column('vendedores', 'campo_importante')
```

---

### 2️⃣ **Backups Automáticos**

#### Sistema de Backup Integrado:
1. **Backup Manual**: Super admin pode fazer backup a qualquer momento
2. **Backup Pré-Restauração**: Automático antes de restaurar outro backup
3. **Download**: Todos backups podem ser baixados localmente

#### Como Usar:
```bash
# Acesso: Super Administrador
1. Login: admin@suameta.com.br / Admin@2025!
2. Menu: Super Admin → Backups
3. Ações disponíveis:
   - ✅ Criar Backup
   - ✅ Download de Backup
   - ✅ Restaurar Backup
   - ✅ Upload de Backup Externo
```

---

### 3️⃣ **Deploy sem Perda de Dados**

#### Railway (Produção):
```yaml
# railway.json - Configuração segura
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**O que acontece no deploy:**
1. ✅ Nova versão do código é deployed
2. ✅ Banco de dados PostgreSQL NÃO é tocado
3. ✅ Migrations rodam (apenas adicionam, nunca removem)
4. ✅ Aplicação reinicia com novo código
5. ✅ **Todos os dados permanecem intactos**

---

### 4️⃣ **Variáveis de Ambiente Protegidas**

#### Nunca Modificar em Produção:
```bash
# ❌ NÃO ALTERAR:
DATABASE_URL=postgresql://...  # Mantém conexão com banco existente
SECRET_KEY=...                 # Mantém sessões ativas
FLASK_ENV=production          # Mantém modo produção

# ✅ PODE ALTERAR (se necessário):
SMTP_SERVER=...               # Configurações de email
LOG_LEVEL=...                 # Nível de logs
```

---

## 🔄 Processo de Atualização Segura

### Passo a Passo:

#### **ANTES** de atualizar:
```bash
# 1. Fazer backup manual
Acesse: /super-admin/backups
Clique: "Criar Backup"
Aguarde: Download do arquivo .db

# 2. Verificar variáveis de ambiente
Railway Dashboard → Variables
Confirmar: DATABASE_URL está configurada
```

#### **DURANTE** a atualização:
```bash
# 1. Push para GitHub
git add .
git commit -m "feat: Nova funcionalidade"
git push origin main

# 2. Railway auto-deploy
- Detecta push no GitHub
- Baixa novo código
- Instala dependências
- Roda migrations
- Reinicia aplicação
- ✅ Dados preservados!
```

#### **DEPOIS** da atualização:
```bash
# 1. Testar sistema
Acesse: https://suameta.up.railway.app
Login: Credenciais super admin
Verificar: Dados estão intactos

# 2. Verificar logs
Railway Dashboard → Logs
Checar: Sem erros de migration
```

---

## 🚨 Cenários de Emergência

### Se algo der errado:

#### Opção 1: Restaurar Backup
```bash
1. Acesse: /super-admin/backups
2. Selecione: Backup anterior
3. Clique: "Restaurar"
4. Sistema: Cria backup pré-restauração automático
5. Confirme: Restauração
```

#### Opção 2: Rollback no Railway
```bash
1. Railway Dashboard
2. Deployments → Selecionar versão anterior
3. Clique: "Redeploy"
4. Aguarde: Sistema volta à versão anterior
```

#### Opção 3: Backup Local
```bash
# Se você baixou backup localmente:
1. Acesse: /super-admin/backups
2. Upload: Arquivo .db salvo localmente
3. Restaure: Backup enviado
```

---

## 📊 Monitoramento de Dados

### Verificações Regulares:

```python
# Script de verificação (rodar mensalmente)
from models import db, Empresa, Usuario, Vendedor, Meta

# Contar registros
print(f"Empresas: {Empresa.query.count()}")
print(f"Usuários: {Usuario.query.count()}")
print(f"Vendedores: {Vendedor.query.count()}")
print(f"Metas: {Meta.query.count()}")
```

---

## ✅ Checklist de Proteção

Antes de cada deploy, confirme:

- [ ] Backup manual criado
- [ ] Backup baixado localmente
- [ ] DATABASE_URL configurada
- [ ] Migrations testadas em dev
- [ ] Nenhuma migration remove colunas
- [ ] Sistema de backup funcionando
- [ ] Logs sem erros críticos

---

## 📞 Suporte

**Se encontrar problemas:**

📧 **Email**: cristiano.s.santos@ba.estudante.senai.br  
📱 **WhatsApp**: (71) 99337-2960  
🕐 **Horário**: Segunda a Sexta, 8h às 18h

---

## 🔐 Boas Práticas

### DO's ✅
- ✅ Fazer backup antes de mudanças grandes
- ✅ Testar migrations em desenvolvimento primeiro
- ✅ Manter backups locais semanais
- ✅ Verificar logs após deploy
- ✅ Documentar mudanças no CHANGELOG

### DON'Ts ❌
- ❌ Nunca deletar DATABASE_URL
- ❌ Nunca rodar migrations que removem dados
- ❌ Nunca fazer deploy sem backup
- ❌ Nunca modificar dados diretamente no PostgreSQL
- ❌ Nunca ignorar erros de migration

---

## 📈 Crescimento Sustentável

### Escalabilidade de Dados:
- ✅ **PostgreSQL**: Suporta milhões de registros
- ✅ **Indexes**: Otimizam queries grandes
- ✅ **Soft Delete**: Dados nunca são removidos fisicamente
- ✅ **Archive**: Mover dados antigos para tabelas de arquivo

### Exemplo de Soft Delete:
```python
# ✅ CORRETO: Soft delete
vendedor.ativo = False
db.session.commit()

# ❌ ERRADO: Hard delete
# db.session.delete(vendedor)  # NUNCA FAZER!
```

---

## 🎯 Conclusão

Com estas configurações:
- ✅ **Dados nunca são apagados** em deploys
- ✅ **Backups protegem** contra acidentes
- ✅ **Rollback fácil** se necessário
- ✅ **Crescimento seguro** e escalável

**Seu sistema está PROTEGIDO! 🛡️**
