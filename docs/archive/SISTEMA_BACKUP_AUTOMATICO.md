# 🔄 Sistema de Backup Automático

## 📋 Visão Geral

O **SuaMeta** agora possui um sistema completo de backup automático com agendamento inteligente, garantindo a segurança dos seus dados sem intervenção manual.

---

## ✨ Funcionalidades Principais

### ⏰ Agendamento Configurável
- **Frequência**: Escolha entre diário, semanal ou mensal
- **Horário Personalizável**: Defina o melhor momento para executar backups
- **Padrão Recomendado**: Diário às 02:00 (madrugada) para mínimo impacto

### 🗂️ Gestão Inteligente de Backups
- **Nomenclatura Automática**: `auto_backup_AAAAMMDD_HHMMSS.db`
- **Política de Retenção**: Mantenha os últimos N backups (configurável)
- **Limpeza Automática**: Remove backups antigos automaticamente
- **Backup Manual**: Botão "Backup Agora" para backups sob demanda

### 📊 Monitoramento em Tempo Real
- Status do agendador (Ativo/Inativo)
- Status do backup automático (Habilitado/Desabilitado)
- Data e hora da próxima execução
- Frequência atual configurada

---

## 🎯 Como Usar

### 1️⃣ Acessar Configurações
1. Faça login como **Super Administrador**
2. Acesse **Backups** no menu lateral
3. Clique em **⚙️ Configurar Agendamento**

### 2️⃣ Configurar Backup Automático
```
┌─────────────────────────────────────────┐
│  ⚙️ Configurações de Agendamento       │
├─────────────────────────────────────────┤
│  ☑ Habilitar Backup Automático         │
│                                         │
│  Frequência:      [📅 Diário]          │
│  Horário:         [02:00]              │
│  Manter Últimos:  [7] backups          │
│  ☑ Limpeza Automática                  │
│                                         │
│  [💾 Salvar Configurações]             │
└─────────────────────────────────────────┘
```

### 3️⃣ Opções de Frequência

| Frequência | Quando Executa | Recomendado Para |
|------------|----------------|------------------|
| 📅 **Diário** | Todos os dias no horário definido | Produção com dados críticos |
| 📆 **Semanal** | Domingos no horário definido | Ambientes de teste/staging |
| 🗓️ **Mensal** | Dia 1 de cada mês no horário definido | Arquivos históricos |

### 4️⃣ Política de Retenção

**Configuração Recomendada:**
- **Diário**: Manter 7 backups (1 semana)
- **Semanal**: Manter 4 backups (1 mês)
- **Mensal**: Manter 12 backups (1 ano)

---

## 🔧 Configurações Técnicas

### Configurações Padrão
```python
backup_config = {
    'enabled': True,
    'frequency': 'daily',
    'time': '02:00',
    'keep_last': 7,
    'auto_cleanup': True
}
```

### Estrutura de Arquivos
```
instance/
└── backups/
    ├── auto_backup_20251214_020000.db  ← Backup automático
    ├── auto_backup_20251213_020000.db
    ├── auto_backup_20251212_020000.db
    ├── backup_20251214_103045.db       ← Backup manual
    └── upload_20251210_154523.db       ← Backup enviado
```

### Logs de Execução
```
✅ Backup automático criado: auto_backup_20251214_020000.db
🗑️ Backup antigo removido: auto_backup_20251207_020000.db
🔄 Backup automático iniciado: daily às 02:00
```

---

## 🌐 Ambientes

### 🖥️ SQLite (Desenvolvimento Local)
- Backups salvos em `instance/backups/`
- Agendamento via APScheduler
- Download/upload manual disponível

### ☁️ PostgreSQL (Produção - Railway)
- Backups gerenciados automaticamente pelo Railway
- Acesse: Railway Dashboard → Database → Backups
- Point-in-time recovery disponível
- Snapshots diários automáticos

---

## 🚀 Comandos Úteis

### Backup Manual Via Interface
```
1. Acesse /super-admin/backups
2. Clique em "⚡ Backup Agora"
3. Backup criado instantaneamente
```

### Backup Manual Via Python
```python
from app import criar_backup_automatico, app

with app.app_context():
    criar_backup_automatico()
```

### Verificar Status do Scheduler
```python
from app import scheduler

# Verificar se está rodando
print(f"Scheduler ativo: {scheduler.running}")

# Listar jobs agendados
for job in scheduler.get_jobs():
    print(f"Job: {job.name}")
    print(f"Próxima execução: {job.next_run_time}")
```

---

## 📱 Interface Responsiva

### Desktop
```
┌────────────────────────────────────────────────────────┐
│ ⏰ Configuração de Backups Automáticos                 │
├───────────────────┬────────────────────────────────────┤
│ Status            │ Configurações                      │
│ ✅ Ativo          │ ☑ Habilitar Backup                │
│ ✅ Habilitado     │ Frequência: [📅 Diário]          │
│ 🗓️ Próxima: 02:00 │ Horário: [02:00]                  │
│                   │ Manter: [7] backups               │
└───────────────────┴────────────────────────────────────┘
```

### Mobile
```
┌──────────────────┐
│ Status           │
│ ✅ Ativo         │
│ ✅ Habilitado    │
│ 🗓️ Próxima:      │
│    02:00         │
├──────────────────┤
│ Configurações    │
│ ☑ Habilitar      │
│ Freq: Diário     │
│ Hora: 02:00      │
│ Manter: 7        │
│ [💾 Salvar]      │
└──────────────────┘
```

---

## 🔒 Segurança

### Controle de Acesso
- ✅ Apenas **Super Administradores** podem acessar
- ✅ Rotas protegidas com `@super_admin_required`
- ✅ Validação de dados no backend

### Segurança de Dados
- ✅ Backup de segurança antes de restaurar
- ✅ Logs de todas as operações
- ✅ Arquivos com nomenclatura única (timestamp)
- ✅ Validação de tipo de arquivo (.db apenas)

---

## ⚠️ Avisos Importantes

### 🔴 Nunca Deletar Todos os Backups
Mantenha sempre pelo menos 1 backup recente para recuperação de desastres.

### 🟡 Armazenamento Externo
Além dos backups automáticos, faça downloads periódicos e armazene em:
- ☁️ Google Drive / OneDrive
- 💾 HD Externo
- 🌐 Outro servidor

### 🟢 Teste de Restauração
Teste a restauração dos backups regularmente para garantir integridade.

---

## 📞 Suporte

**Em caso de problemas:**
1. Verifique os logs do sistema
2. Confira configurações do agendador
3. Teste backup manual primeiro
4. Entre em contato com suporte técnico

---

## 🎯 Checklist de Boas Práticas

- [ ] Backup automático habilitado
- [ ] Frequência configurada (mínimo semanal)
- [ ] Horário definido (preferência: madrugada)
- [ ] Política de retenção configurada (mínimo 3 backups)
- [ ] Limpeza automática ativada
- [ ] Download manual mensal realizado
- [ ] Backup testado e validado
- [ ] Armazenamento externo configurado

---

**✅ Sistema de Backup Automático - SuaMeta v2.9.2**  
*Proteção automática dos seus dados, 24/7* 🛡️
