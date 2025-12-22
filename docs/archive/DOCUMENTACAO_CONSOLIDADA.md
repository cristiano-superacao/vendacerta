# 📚 Documentação Consolidada - Sistema SuaMeta

> **Versão**: 2.9.1  
> **Data**: 16 de Dezembro de 2025  
> **Status**: ✅ Produção

---

## 📋 Índice

1. [Visão Geral do Sistema](#-visão-geral-do-sistema)
2. [Arquitetura e Tecnologias](#-arquitetura-e-tecnologias)
3. [Funcionalidades Principais](#-funcionalidades-principais)
4. [Módulos do Sistema](#-módulos-do-sistema)
5. [Guia de Deploy Railway](#-guia-de-deploy-railway)
6. [Guia de Uso](#-guia-de-uso)
7. [Permissões e Controle de Acesso](#-permissões-e-controle-de-acesso)
8. [Backup e Segurança](#-backup-e-segurança)
9. [Suporte e Contato](#-suporte-e-contato)

---

## 🎯 Visão Geral do Sistema

O **SuaMeta** é um sistema completo de gestão de metas e comissões com:

### ✨ Destaques
- 🏢 **Multi-Empresa**: Suporte para múltiplas empresas isoladas
- 📊 **Dashboard Inteligente**: Análise em tempo real com gráficos interativos
- 💰 **Comissões Automáticas**: Cálculo com faixas configuráveis
- 👥 **Gestão de Equipes**: Hierarquia vendedores → supervisores → admins
- 📱 **100% Responsivo**: Mobile-first design com PWA
- ☁️ **Cloud Native**: Hospedado no Railway com PostgreSQL
- 🔐 **Segurança Avançada**: Autenticação, permissões granulares, auditoria

### 🎨 Interface
- **Design Profissional**: Verde escuro Prescrimed (#1a4d2e)
- **Bootstrap 5.3.3**: Framework responsivo moderno
- **Chart.js 4.4.0**: Gráficos interativos
- **Bootstrap Icons 1.11.3**: Iconografia consistente
- **Google Fonts Inter**: Tipografia profissional

---

## 🏗️ Arquitetura e Tecnologias

### Backend
```python
Flask 3.0.0              # Framework web Python
SQLAlchemy 2.0+          # ORM para banco de dados
PostgreSQL               # Banco de dados (Railway)
Gunicorn                 # Servidor WSGI produção
APScheduler              # Tarefas agendadas (backups)
```

### Frontend
```html
Bootstrap 5.3.3          # Framework CSS responsivo
Chart.js 4.4.0           # Gráficos interativos
Bootstrap Icons 1.11.3   # Ícones
Google Fonts Inter       # Tipografia
PWA Manifest             # Progressive Web App
```

### DevOps
```yaml
Railway                  # Plataforma de deploy
PostgreSQL Cloud         # Banco gerenciado
GitHub Actions           # CI/CD automático
Nixpacks                 # Build system
```

### Estrutura de Arquivos
```
vendacerta/
├── app.py                          # Aplicação Flask principal
├── models.py                       # Modelos SQLAlchemy
├── forms.py                        # Formulários WTForms
├── config.py                       # Configurações
├── calculo_comissao.py             # Lógica de comissões
├── calculo_projecao.py             # Projeções de vendas
├── calculo_balanceamento.py        # Metas balanceadas
├── pdf_generator.py                # Exportação PDF
├── backup_nuvem.py                 # Backup Google Drive
├── requirements.txt                # Dependências Python
├── railway.json                    # Config Railway
├── nixpacks.toml                   # Config build
├── Procfile                        # Comando de start
├── templates/                      # Templates HTML
│   ├── base.html                   # Layout base
│   ├── dashboard.html              # Dashboard principal
│   ├── clientes/                   # Módulo clientes
│   ├── metas/                      # Módulo metas
│   ├── relatorios/                 # Relatórios
│   └── ...
├── static/                         # Arquivos estáticos
│   ├── css/
│   │   └── custom.css              # Estilos customizados
│   ├── img/                        # Imagens e ícones
│   ├── manifest.json               # PWA manifest
│   └── service-worker.js           # Service worker
├── instance/                       # Dados locais (ignorado)
│   └── backups/                    # Backups SQLite local
└── scripts/                        # Scripts utilitários
    └── migrations/                 # Migrações de banco
```

---

## ⚡ Funcionalidades Principais

### 1. **Dashboard Inteligente** (`/dashboard`)
- 📊 Cards de estatísticas (vendas, metas, comissões)
- 📈 Gráficos de evolução mensal
- 🎯 Progresso de metas em tempo real
- 👥 Ranking de vendedores
- 📅 Filtros por período (mês/ano)

### 2. **Sistema de Metas Avançadas**

#### **Metas de Valor** (R$)
- Baseada em faturamento total
- Balanceamento automático (3-12 meses histórico)
- 3 algoritmos: Simples, Ponderado, Com Tendência

#### **Metas de Volume** (Quantidade)
- Baseada em número de vendas
- Mesmos algoritmos de balanceamento
- Ideal para medir produtividade

#### **Configuração** (`/metas/configurar`)
- Interface com abas (Valor/Volume)
- Seleção de período histórico
- Preview do cálculo com histórico
- Ajuste manual opcional

#### **Relatório Avançado** (`/relatorios/metas-avancado`)
- Filtros dinâmicos (vendedor, tipo, período)
- 4 cards de estatísticas
- Tabela com barras de progresso
- Gráficos Chart.js interativos
- Ranking melhores/piores meses

### 3. **Gestão de Clientes** (`/clientes`)
- ✅ Cadastro completo (11 campos)
- ✅ Histórico de compras
- ✅ Status visual (Ativo/Inativo/Prospecto/VIP)
- ✅ Filtros e busca avançada
- ✅ Importação via Excel
- ✅ Exportação de relatórios

### 4. **Comissões Configuráveis** (`/configuracoes/comissoes`)
- 💰 Faixas personalizadas por cargo
- 📊 Vendedor: 3 faixas (padrão 5%, 7%, 10%)
- 👨‍💼 Supervisor: 3 faixas (padrão 2%, 3%, 5%)
- 🔄 Edição em tempo real
- 📋 Preview visual das faixas

### 5. **Mensagens Internas** (`/mensagens`)
- 💬 Sistema de comunicação interno
- 📨 Caixa de entrada/enviados
- 🔔 Notificações em tempo real
- 👥 Mensagens individuais ou broadcast

### 6. **Backup Automático**
- ⏰ Agendamento flexível (diário, semanal, mensal)
- ☁️ Sincronização Google Drive (opcional)
- 📦 Backup local automático
- 🗂️ Limpeza de backups antigos (manter últimos 10)

### 7. **Controle de Acesso Granular**
- 🔐 4 níveis: Super Admin, Admin, Supervisor, Vendedor
- 🎯 Permissões específicas por módulo
- 🏢 Isolamento multi-empresa
- 📝 Log de auditoria

### 8. **Exportação PDF**
- 📄 Dashboard completo
- 📊 Relatórios de metas
- 👤 Dados de vendedores
- 🎨 Layout profissional com logo

### 9. **Progressive Web App (PWA)**
- 📱 Instalável como app nativo
- 🔄 Funciona offline (básico)
- 🎨 Ícone na tela inicial
- ⚡ Carregamento rápido

---

## 📦 Módulos do Sistema

### **1. Usuários e Autenticação**
**Modelos**: `Usuario`
**Rotas**: `/login`, `/logout`, `/registro`, `/perfil`

**Campos Principais**:
- Username, email, senha (hash bcrypt)
- Nome, cargo (super_admin, admin, supervisor, vendedor)
- Empresa_id (multi-tenant)
- Permissões granulares

### **2. Vendedores**
**Modelo**: `Vendedor`
**Rotas**: `/vendedores`, `/vendedores/novo`, `/vendedores/<id>/editar`

**Funcionalidades**:
- CRUD completo
- Vinculação com supervisor
- Vinculação com equipe
- Histórico de vendas
- Cálculo de comissões

### **3. Supervisores**
**Modelo**: `Usuario` (cargo='supervisor')
**Rota**: `/supervisor/dashboard`

**Funcionalidades**:
- Dashboard da equipe
- Metas consolidadas
- Projeções de vendas
- Relatórios de desempenho

### **4. Equipes**
**Modelo**: `Equipe`
**Rotas**: `/equipes`, `/equipes/nova`, `/equipes/<id>`

**Funcionalidades**:
- Criação e gestão
- Alocação de vendedores
- Metas coletivas
- Relatórios por equipe

### **5. Metas**
**Modelo**: `Meta`
**Rotas**: 
- `/metas` - Lista
- `/metas/nova` - Cadastro
- `/metas/configurar` - Configuração avançada
- `/relatorios/metas-avancado` - Relatório

**Campos Principais**:
- `tipo_meta`: 'valor' ou 'volume'
- `valor_meta`, `receita_alcancada`
- `volume_meta`, `volume_alcancado`
- `periodo_historico` (3-12 meses)
- `meta_balanceada`, `tendencia_calculada`

### **6. Clientes**
**Modelo**: `Cliente`, `CompraCliente`
**Rotas**: `/clientes`, `/clientes/<id>`, `/clientes/importar`

**Funcionalidades**:
- Cadastro com 11 campos
- Status (Ativo, Inativo, Prospecto, VIP)
- Histórico de compras
- Importação Excel
- Relatórios personalizados

### **7. Faixas de Comissão**
**Modelos**: `FaixaComissaoVendedor`, `FaixaComissaoSupervisor`
**Rota**: `/configuracoes/comissoes`

**Configuração**:
```python
# Vendedor
Faixa 1: 0-50% meta → 5% comissão
Faixa 2: 50-100% meta → 7% comissão
Faixa 3: >100% meta → 10% comissão

# Supervisor
Faixa 1: 0-50% meta → 2% comissão
Faixa 2: 50-100% meta → 3% comissão
Faixa 3: >100% meta → 5% comissão
```

### **8. Empresas (Multi-Tenant)**
**Modelo**: `Empresa`
**Rota**: `/super-admin/empresas` (apenas super_admin)

**Funcionalidades**:
- Cadastro de empresas
- Isolamento de dados
- Gestão de usuários por empresa
- Estatísticas consolidadas

### **9. Mensagens**
**Modelo**: `Mensagem`
**Rotas**: `/mensagens`, `/mensagens/nova`, `/mensagens/<id>`

**Funcionalidades**:
- Envio individual
- Broadcast para equipe
- Marcação de lidas
- Badge de não lidas

### **10. Backup**
**Módulo**: `backup_nuvem.py`
**Rota**: `/backups/configurar`

**Funcionalidades**:
- Backup automático agendado
- Sincronização Google Drive
- Download manual
- Limpeza automática

---

## 🚀 Guia de Deploy Railway

### **Passo 1: Preparar Repositório GitHub**

```bash
# Clone ou crie repositório
git init
git add .
git commit -m "Deploy inicial Railway"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/suameta.git
git push -u origin main
```

### **Passo 2: Criar Projeto no Railway**

1. Acesse [railway.app](https://railway.app)
2. Login com GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Selecione o repositório `suameta`
5. Railway detecta automaticamente Python/Flask

### **Passo 3: Adicionar Banco PostgreSQL**

1. No projeto Railway, clique "New" → "Database" → "Add PostgreSQL"
2. Aguarde provisionamento (~30s)
3. Vá em "Variables" → Railway cria automaticamente:
   - `DATABASE_URL`
   - `PGDATABASE`
   - `PGHOST`
   - `PGPASSWORD`
   - `PGPORT`
   - `PGUSER`

### **Passo 4: Configurar Variáveis de Ambiente**

Adicione em "Variables":

```bash
# Obrigatórias
SECRET_KEY=gerar-chave-secreta-aqui-128-caracteres
DATABASE_URL=${{Postgres.DATABASE_URL}}  # Referência automática
FLASK_ENV=production

# Opcionais
BACKUP_ENABLED=false  # Desabilitar backup local em produção
GOOGLE_DRIVE_ENABLED=false  # Habilitar se configurou Google Drive
```

**Gerar SECRET_KEY**:
```python
python -c "import secrets; print(secrets.token_urlsafe(96))"
```

### **Passo 5: Configurar Build (Automático)**

Railway usa `railway.json` e `nixpacks.toml`:

**railway.json** (já configurado):
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "python init_db.py && gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120",
    "healthcheckPath": "/ping",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### **Passo 6: Deploy Automático**

1. Railway inicia build automaticamente
2. Acompanhe logs em tempo real
3. Após ~3-5 minutos: ✅ Deploy concluído
4. Clique em "Settings" → "Generate Domain"
5. URL: `https://suameta-production.up.railway.app`

### **Passo 7: Setup Inicial do Sistema**

1. Acesse: `https://sua-url.up.railway.app/setup-inicial-sistema`
2. Crie super admin:
   ```
   Username: admin
   Email: seu@email.com
   Senha: senha-forte
   ```
3. Login: `https://sua-url.up.railway.app/login`
4. Configure empresa, vendedores e metas

### **Passo 8: Monitoramento**

**Logs em Tempo Real**:
```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Ver logs
railway logs
```

**Health Checks**:
- `/ping` - Status básico (200 OK)
- `/health` - Status detalhado (DB, disco, memória)

---

## 📖 Guia de Uso

### **Para Vendedores**

#### 1. **Acessar o Sistema**
- URL: `https://vendacerta.up.railway.app`
- Login com credenciais fornecidas pelo admin

#### 2. **Dashboard**
- Veja suas metas do mês
- Acompanhe progresso em tempo real
- Verifique comissão acumulada

#### 3. **Registrar Venda**
- Menu: Clientes → Novo Cliente (se necessário)
- Após criar cliente → Adicionar Compra
- Sistema atualiza meta automaticamente

#### 4. **Verificar Comissões**
- Dashboard mostra comissão calculada
- Relatórios detalhados disponíveis

### **Para Supervisores**

#### 1. **Dashboard da Equipe**
- Menu: Minha Equipe
- Veja todos os vendedores
- Metas consolidadas
- Projeções de fechamento

#### 2. **Gerenciar Vendedores**
- Menu: Vendedores → Lista
- Editar, ativar, desativar
- Vincular a equipes

#### 3. **Configurar Metas**
- Menu: Configurar Metas Avançadas
- Escolha vendedor
- Defina tipo (Valor/Volume)
- Configure período e balanceamento
- Calcule e salve

#### 4. **Relatórios**
- Menu: Relatório de Metas Avançado
- Filtros por vendedor, período
- Exportação PDF
- Gráficos interativos

### **Para Administradores**

#### 1. **Gestão Completa**
- Acesso total ao sistema
- Criar usuários, equipes, empresas
- Configurar faixas de comissão
- Backup e segurança

#### 2. **Configurar Comissões**
- Menu: Configurações → Faixas de Comissão
- Edite percentuais de vendedor e supervisor
- Salve e aplique

#### 3. **Backup**
- Menu: (via super admin) → Backups
- Configure agendamento
- Download manual
- Sincronização Google Drive (opcional)

#### 4. **Mensagens**
- Menu: Mensagens
- Envie comunicados para equipe
- Broadcast ou individual

---

## 🔐 Permissões e Controle de Acesso

### **Níveis de Acesso**

| Funcionalidade | Vendedor | Supervisor | Admin | Super Admin |
|---------------|----------|------------|-------|-------------|
| Ver próprio dashboard | ✅ | ✅ | ✅ | ✅ |
| Ver dashboard equipe | ❌ | ✅ | ✅ | ✅ |
| Cadastrar clientes | ✅ | ✅ | ✅ | ✅ |
| Gerenciar vendedores | ❌ | Só sua equipe | ✅ | ✅ |
| Configurar metas | ❌ | ✅ | ✅ | ✅ |
| Configurar comissões | ❌ | ❌ | ✅ | ✅ |
| Gerenciar empresas | ❌ | ❌ | ❌ | ✅ |
| Backup sistema | ❌ | ❌ | ✅ | ✅ |
| Ver relatórios | Próprios | Equipe | Todos | Todos |
| Mensagens | ✅ | ✅ | ✅ | ✅ |

### **Implementação**

```python
# Decorador de permissão
@login_required
@permission_required('ver_dashboard')
def dashboard():
    # Código da rota
    
# Verificação manual
if not current_user.has_permission('editar_comissoes'):
    flash('Sem permissão', 'danger')
    return redirect(url_for('dashboard'))
```

---

## 🛡️ Backup e Segurança

### **Backup Automático Local**

**Configuração**:
```python
# Em app.py, configurar APScheduler
backup_config = {
    'enabled': True,
    'frequency': 'daily',  # daily, weekly, monthly
    'time': '02:00',       # Horário (24h)
    'keep_last': 10        # Manter últimos 10 backups
}
```

**Localização**: `instance/backups/auto_backup_YYYYMMDD_HHMMSS.db`

### **Backup PostgreSQL (Railway)**

**Gerenciado Automaticamente**:
1. Railway Dashboard → Database → Backups
2. Backups diários automáticos
3. Retenção de 7 dias (plano Hobby)
4. Restauração com 1 clique

**Backup Manual**:
```bash
# Via Railway CLI
railway run pg_dump $DATABASE_URL > backup.sql
```

### **Sincronização Google Drive (Opcional)**

**Setup**:
1. Criar projeto Google Cloud
2. Habilitar Google Drive API
3. Criar credenciais OAuth 2.0
4. Baixar `credentials.json`
5. Colocar em `instance/`
6. Configurar em `/backups/configurar`

**Funcionamento**:
- Backup local criado
- Upload automático para Drive
- Pasta: `SuaMeta Backups/`

### **Segurança**

**Senhas**:
- Hash bcrypt (12 rounds)
- Salt único por senha
- Validação de força mínima

**Sessões**:
- Cookie seguro (HttpOnly, Secure em HTTPS)
- Timeout de 24h
- CSRF protection (Flask-WTF)

**Banco de Dados**:
- Conexão SSL/TLS (Railway)
- Credenciais em variáveis de ambiente
- Prepared statements (SQLAlchemy)

**Auditoria**:
- Log de ações sensíveis
- Rastreamento de alterações
- Timestamp automático

---

## 📞 Suporte e Contato

### **Desenvolvedor**
**Nome**: Cristiano Santos  
**WhatsApp**: (71) 99337-2960  
**Email**: cristiano@prescrimed.com.br  
**Horário**: Seg-Sex 8h-18h | Sáb 8h-12h

### **Suporte Técnico**

**Questões Comuns**:
1. **Esqueci minha senha**
   - Contate o administrador
   - Admin pode resetar via `/usuarios`

2. **Sistema lento**
   - Verifique conexão internet
   - Limpe cache do navegador
   - Contate suporte se persistir

3. **Erro ao salvar meta**
   - Verifique campos obrigatórios
   - Confirme que vendedor tem histórico
   - Tente ajuste manual se cálculo falhar

4. **Gráfico não carrega**
   - Verifique conexão (Chart.js via CDN)
   - Atualize página (Ctrl+F5)
   - Teste em outro navegador

**Reportar Bug**:
- Email com print do erro
- Informar usuário, data/hora, ação realizada
- Railway logs (se admin): `railway logs`

---

## 🎓 Recursos Adicionais

### **PWA - Instalar como App**
📱 [Guia de Instalação PWA](docs/guias/INSTALACAO_PWA.md)

### **Importação de Dados**
📊 [Guia de Importação Clientes](GUIA_IMPORTACAO_CLIENTES.md)

### **Referências Técnicas**
- [Sistema de Permissões](docs/SISTEMA_PERMISSOES_GRANULARES.md)
- [Backup Automático](docs/SISTEMA_BACKUP_AUTOMATICO.md)
- [Manual Completo](docs/MANUAL_COMPLETO_SISTEMA.md)

---

## 📊 Estatísticas do Sistema

- **Linhas de Código**: ~12.000 (Python + HTML + CSS + JS)
- **Templates**: 25+ arquivos HTML
- **Rotas**: 80+ endpoints
- **Modelos**: 10 tabelas principais
- **Tempo de Desenvolvimento**: ~200 horas
- **Versão**: 2.9.1
- **Última Atualização**: 16/12/2025

---

## ✅ Checklist de Validação

### **Desenvolvimento Local**
- [x] Sistema roda em `localhost:5001`
- [x] Todas as rotas funcionais
- [x] Testes de CRUD completos
- [x] Layout responsivo validado
- [x] PWA funcional

### **Deploy Railway**
- [x] Build bem-sucedido
- [x] PostgreSQL conectado
- [x] Variáveis de ambiente configuradas
- [x] Health check `/ping` OK
- [x] Domínio gerado e acessível
- [x] HTTPS ativo
- [x] Auto-deploy configurado

### **Funcional**
- [x] Login/Logout
- [x] Dashboard carrega
- [x] Cadastro de metas
- [x] Cálculo de comissões
- [x] Gráficos Chart.js
- [x] Exportação PDF
- [x] Mensagens internas
- [x] Backup automático
- [x] Multi-empresa

---

## 🚀 Próximas Versões (Roadmap)

### **v3.0 (Q1 2026)**
- [ ] App mobile nativo (React Native)
- [ ] API RESTful documentada
- [ ] Integração com WhatsApp Business
- [ ] Notificações push

### **v3.1 (Q2 2026)**
- [ ] BI avançado com PowerBI
- [ ] Machine Learning para previsão de vendas
- [ ] Gamificação (badges, rankings)

---

**🎉 Sistema 100% Funcional e Otimizado para Produção!**

*Documentação consolidada - Última atualização: 16/12/2025*
