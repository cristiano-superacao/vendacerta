# 📚 Guia Completo do Sistema SuaMeta v2.9.1

> ⚠️ **ARQUIVO LEGADO/ARQUIVADO**: pode conter exemplos antigos.
> Não use credenciais/senhas fixas; siga `docs/GETTING_STARTED.md` e `docs/DEPLOY_RAILWAY.md`.

> **Sistema Profissional de Gestão de Metas e Comissões**  
> Layout 100% Responsivo | Multi-Tenant | Cloud-Native | PWA

---

## 📑 Índice Rápido

1. [🎯 Visão Geral](#visao-geral)
2. [🚀 Acesso e Instalação](#acesso-instalacao)
3. [👥 Perfis e Permissões](#perfis-permissoes)
4. [⚙️ Funcionalidades Completas](#funcionalidades)
5. [💻 Arquitetura Técnica](#arquitetura)
6. [📊 Modelos de Dados](#modelos)
7. [🔐 Segurança](#seguranca)
8. [📱 PWA e Mobile](#pwa-mobile)
9. [🛠️ Deploy e Infraestrutura](#deploy)
10. [❓ FAQ e Suporte](#faq)

---

## 🎯 Visão Geral {#visao-geral}

### O que é o Sistema SuaMeta?

Sistema completo para gerenciar metas de vendas, calcular comissões automaticamente e acompanhar desempenho em tempo real. Desenvolvido em Python/Flask com PostgreSQL e hospedado no Railway.

### ✨ Principais Características

- 🏢 **Multi-Tenant:** Isolamento total de dados por empresa
- 📱 **Mobile-First:** Responsivo para todos os dispositivos
- ☁️ **Cloud-Native:** 100% na nuvem (Railway + PostgreSQL)
- 🔒 **Segurança:** Autenticação robusta + 9 permissões granulares
- 🎨 **Interface Moderna:** Bootstrap 5.3.3 com design profissional
- 📊 **Dashboards Dinâmicos:** KPIs e gráficos em tempo real
- 💰 **Comissões Automáticas:** Cálculo por faixas de desempenho
- 📥 **Importação Excel:** Carga em massa de vendedores e metas
- 📧 **Sistema de Mensagens:** Comunicação interna
- 📈 **Projeção de Ganhos:** Simulador de comissões

### 📊 Estatísticas do Sistema

| Métrica | Valor |
|---------|-------|
| Rotas HTTP | 72 |
| Templates HTML | 37 |
| Modelos de Dados | 8 |
| Perfis de Acesso | 5 |
| Permissões Granulares | 9 |
| APIs REST | 2 |
| Linhas de Código Python | ~4.000 |
| Empresas Ativas | Ilimitado |

---

## 🚀 Acesso e Instalação {#acesso-instalacao}

### 🌐 Acessar Sistema em Produção

**URL:** https://vendacerta.up.railway.app

#### Credenciais de Teste

**Super Administrador:**
- Email: `superadmin@suameta.com`
- Senha: (defina no seu ambiente; sem senha padrão)
- Acesso: Total (todas as empresas)

**Administrador Empresa 1:**
- Email: `admin@empresa.com`
- Senha: (defina no seu ambiente; sem senha padrão)
- Acesso: Gestão completa da empresa

**Vendedor:**
- Email: `vendedor@empresa.com`
- Senha: `vendedor123`
- Acesso: Dashboard e metas próprias

### 📱 Instalar como App (PWA)

#### No Celular (Android/iOS)

1. Acesse https://vendacerta.up.railway.app
2. No menu do navegador, toque em:
   - **Android:** "Adicionar à tela inicial"
   - **iOS:** "Adicionar à Tela de Início"
3. Ícone do app aparece na tela inicial
4. Use como app nativo!

#### No Desktop (Chrome/Edge)

1. Acesse o sistema
2. Clique no ícone ➕ na barra de endereço
3. Selecione "Instalar SuaMeta"
4. App abre em janela própria

### 💻 Instalação Local (Desenvolvimento)

#### Pré-requisitos

- Python 3.11+
- PostgreSQL 15+ OU SQLite
- Git

#### Passo a Passo

```bash
# 1. Clonar repositório
git clone https://github.com/cristiano-superacao/suameta.git
cd suameta

# 2. Criar ambiente virtual
python -m venv .venv

# 3. Ativar ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Configurar banco de dados
# Editar config.py com suas credenciais
# Ou usar SQLite (padrão para desenvolvimento)

# 6. Inicializar banco
python init_db.py

# 7. Carregar dados de teste
python init_data.py

# 8. Executar aplicação
python app.py

# 9. Acessar
# http://localhost:5000
```

---

## 👥 Perfis e Permissões {#perfis-permissoes}

### 1. 👑 Super Administrador

**Acesso Global ao Sistema**

✅ **Permissões:**
- Gerenciar todas as empresas
- Criar, editar, bloquear empresas
- Definir planos e limites por empresa
- Ver dados de qualquer empresa
- Sistema completo de backups
- Gerenciar usuários com permissões granulares
- Acessar logs e auditoria

🎯 **Casos de Uso:**
- Administração da plataforma
- Onboarding de novas empresas
- Suporte técnico avançado
- Gestão de limites e planos

### 2. 🔑 Administrador (Admin)

**Acesso Total da Empresa**

✅ **Permissões:**
- Gerenciar vendedores, metas, equipes
- Configurar faixas de comissão
- Criar logins para vendedores
- Enviar mensagens para equipe
- Exportar todos os relatórios
- Ver todos os dashboards
- Aprovar comissões

🎯 **Casos de Uso:**
- Gestão operacional completa
- Configuração de regras de negócio
- Acompanhamento de resultados
- Gestão de pessoas

### 3. 📋 Gerente

**Gestão Operacional e Metas**

✅ **Permissões:**
- ✨ **NOVO v2.9.1:** Criar, editar, deletar metas
- ✨ **NOVO v2.9.1:** Importar metas via Excel
- Gerenciar vendedores da equipe
- Criar logins de vendedores
- Gerenciar equipes
- Ver dashboards da equipe
- Exportar relatórios (se habilitado)

🎯 **Casos de Uso:**
- Lançamento de metas mensais
- Acompanhamento de equipes
- Gestão de vendedores
- Análise de desempenho

### 4. 👁️ Supervisor

**Supervisão e Metas**

✅ **Permissões:**
- ✨ **NOVO v2.9.1:** Criar, editar, deletar metas
- ✨ **NOVO v2.9.1:** Importar metas via Excel
- Visualizar vendedores supervisionados
- Acompanhar metas da equipe
- Enviar mensagens
- Ver dashboards filtrados

🎯 **Casos de Uso:**
- Supervisão de vendedores
- Lançamento de metas
- Acompanhamento diário
- Comunicação com equipe

### 5. 💼 Vendedor

**Acesso às Próprias Informações**

✅ **Permissões:**
- Ver próprio dashboard
- Acompanhar próprias metas
- Simular comissões (projeção)
- Visualizar histórico
- Receber mensagens
- Alterar própria senha

🎯 **Casos de Uso:**
- Acompanhar desempenho pessoal
- Simular ganhos futuros
- Verificar comissões
- Acessar informações de contato

### 🛡️ Sistema de Permissões Granulares

Além dos cargos, o Super Admin pode configurar **9 permissões individuais** para cada usuário:

| Permissão | Campo | Padrão | Descrição |
|-----------|-------|--------|-----------|
| 📊 Dashboard | `pode_ver_dashboard` | ✅ | Ver dashboard com métricas |
| ✉️ Mensagens | `pode_enviar_mensagens` | ✅ | Enviar mensagens |
| 👥 Vendedores | `pode_gerenciar_vendedores` | ❌ | CRUD vendedores |
| 🎯 Metas | `pode_gerenciar_metas` | ❌ | CRUD metas |
| 👁️ Ver Todas Metas | `pode_ver_todas_metas` | ❌ | Metas de todos |
| 👨‍👩‍👧‍👦 Equipes | `pode_gerenciar_equipes` | ❌ | CRUD equipes |
| 💰 Comissões | `pode_gerenciar_comissoes` | ❌ | Config comissões |
| ✔️ Aprovar | `pode_aprovar_comissoes` | ❌ | Aprovar pagamentos |
| 📥 Exportar | `pode_exportar_dados` | ❌ | Exportar relatórios |

**Como Configurar:**
1. Super Admin → Usuários
2. Clique em "Editar" no usuário
3. Role até "Permissões de Acesso"
4. Ative/Desative switches conforme necessário
5. Salvar

---

## ⚙️ Funcionalidades Completas {#funcionalidades}

### 📊 1. Dashboard Inteligente

**Visão Geral Dinâmica**

✨ **Cards de Estatísticas:**
- Total de vendedores ativos
- Metas cadastradas no mês
- Taxa de atingimento geral
- Comissões a pagar
- Ranking de desempenho

✨ **Gráficos Interativos:**
- Evolução mensal de metas
- Distribuição de atingimento
- Comissões por vendedor
- Projeção vs realizado

✨ **Filtros:**
- Por período (mês/ano)
- Por equipe
- Por vendedor
- Por status (atingida/pendente)

### 👥 2. Gestão de Vendedores

**CRUD Completo + Importação**

✨ **Funcionalidades:**
- ✅ Criar vendedor manualmente
- ✅ Editar dados (nome, email, telefone, meta padrão)
- ✅ Deletar vendedor
- ✅ Importar via Excel (carga em massa)
- ✅ Criar login de acesso ao sistema
- ✅ Editar permissões individuais
- ✅ Bloquear/desbloquear vendedor
- ✅ Ver histórico de metas
- ✅ Calcular comissões

✨ **Importação Excel:**
- Download de template (.xlsx)
- Upload de planilha preenchida
- Validação automática de dados
- Preview antes de salvar
- Tratamento de duplicatas
- Relatório de erros

**Colunas Obrigatórias:**
- Nome
- Email
- Telefone (opcional)
- Meta Padrão (opcional)

### 🎯 3. Gestão de Metas

**Lançamento e Acompanhamento**

✨ **Criar Meta Individual:**
- Selecionar vendedor
- Definir mês/ano
- Informar valor da meta
- Valor realizado (opcional)
- Status automático

✨ **Importar Metas Excel:**
- ✨ **NOVO v2.9.1:** Gerente e Supervisor podem importar
- Template padronizado (.xlsx)
- Múltiplas metas em uma planilha
- Validação de duplicatas
- Preview e confirmação
- Atualização automática de realizado

**Colunas Obrigatórias:**
- Email ou ID do vendedor
- Mês (1-12)
- Ano (ex: 2025)
- Valor da Meta
- Realizado (opcional)

✨ **Acompanhamento:**
- Lista de todas as metas
- Filtros por vendedor, mês, status
- Badges coloridos (verde/amarelo/vermelho)
- Percentual de atingimento
- Comissão calculada automática
- Botões: Editar, Deletar, Exportar PDF

✨ **Cálculo Automático:**
- Status baseado no atingimento:
  - 🟢 **Atingida:** >= 100%
  - 🟡 **Parcial:** 50% - 99%
  - 🔴 **Não Atingida:** < 50%

### 👨‍👩‍👧‍👦 4. Gestão de Equipes

**Organização de Vendedores**

✨ **Funcionalidades:**
- Criar equipes por região/produto
- Definir supervisor responsável
- Adicionar/remover vendedores
- Ver desempenho consolidado
- Dashboard específico da equipe
- Ranking interno

✨ **Benefícios:**
- Competições entre equipes
- Metas coletivas
- Comunicação direcionada
- Relatórios agrupados

### 💰 5. Sistema de Comissões

**Cálculo Automático por Faixas**

✨ **Configuração de Faixas:**

| Atingimento | Percentual Comissão | Exemplo (Meta R$ 10.000) |
|-------------|---------------------|--------------------------|
| 0% - 49% | 0% | R$ 0 |
| 50% - 79% | 1% | R$ 100 |
| 80% - 99% | 2% | R$ 200 |
| 100% - 119% | 5% | R$ 500 |
| 120%+ | 7% | R$ 700 |

✨ **Funcionalidades:**
- Admin configura faixas por empresa
- Cálculo automático ao lançar meta
- Histórico de comissões
- Exportação para folha de pagamento
- Aprovação de comissões
- Relatórios detalhados

✨ **Exemplo de Cálculo:**

```
Vendedor: João Silva
Meta: R$ 10.000
Realizado: R$ 11.500
Atingimento: 115%
Faixa: 100% - 119%
Comissão: R$ 10.000 × 5% = R$ 500
```

### 📈 6. Projeção de Ganhos

**Simulador de Comissões**

✨ **Funcionalidade:**
- Vendedor simula comissão futura
- Insere valor que pretende vender
- Sistema calcula:
  - Percentual de atingimento
  - Faixa de comissão aplicável
  - Valor da comissão estimada
- Motivação para bater metas

**Exemplo de Uso:**
1. Vendedor acessa "Projeção"
2. Informa: "Vou vender R$ 12.000"
3. Sistema mostra:
   - Meta: R$ 10.000
   - Atingimento: 120%
   - Faixa: 120%+
   - Comissão: R$ 840 (7%)

### 📧 7. Sistema de Mensagens

**Comunicação Interna**

✨ **Funcionalidades:**
- Admin/Gerente envia mensagens
- Destinatários: Vendedores/Equipes/Todos
- Mensagens individuais ou em grupo
- Histórico de mensagens
- Notificações visuais
- Marcar como lida

✨ **Casos de Uso:**
- Avisos importantes
- Parabenizações por metas
- Lembretes
- Motivação da equipe

### 📥 8. Importação e Exportação

**Integração com Excel**

✨ **Importar:**
- ✅ Vendedores (planilha Excel)
- ✅ Metas (planilha Excel)
- ✅ Supervisores (planilha Excel)
- Templates padronizados
- Validação automática
- Tratamento de erros

✨ **Exportar:**
- ✅ Lista de vendedores (Excel)
- ✅ Metas do mês (Excel/PDF)
- ✅ Comissões (Excel)
- ✅ Relatórios personalizados
- Filtros avançados
- Formatação profissional

### 🏢 9. Multi-Tenant (Super Admin)

**Gestão de Múltiplas Empresas**

✨ **Funcionalidades:**
- Criar empresas ilimitadas
- Configurar plano e limites
- Definir logo da empresa
- Isolamento total de dados
- Dashboard consolidado
- Backups automáticos
- Monitoramento de uso

✨ **Configurações por Empresa:**
- Nome e CNPJ
- Logo personalizada
- Limites de vendedores
- Limites de metas
- Plano (básico/premium)
- Ativo/Inativo

### 🔐 10. Autenticação e Segurança

**Sistema Robusto**

✅ **Recursos:**
- Login com email/senha
- Hash seguro de senhas (werkzeug)
- Sessões com Flask-Login
- Proteção CSRF
- Decorators de autorização:
  - `@login_required`
  - `@admin_required`
  - `@super_admin_required`
- Recuperação de senha
- Troca de senha
- Bloqueio de usuários
- Auditoria de ações

---

## 💻 Arquitetura Técnica {#arquitetura}

### 🏗️ Stack Tecnológico

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| **Backend** | Python | 3.11+ |
| **Framework** | Flask | 3.0+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Banco Produção** | PostgreSQL | 15+ |
| **Banco Dev** | SQLite | 3+ |
| **Autenticação** | Flask-Login | 0.6+ |
| **Formulários** | Flask-WTF | 1.2+ |
| **Frontend** | Bootstrap | 5.3.3 |
| **Icons** | Bootstrap Icons | 1.11+ |
| **PDF** | ReportLab | 4.0+ |
| **Excel** | OpenPyXL | 3.1+ |
| **Hospedagem** | Railway | Cloud |
| **Git** | GitHub | - |

### 📐 Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────┐
│                  PRESENTATION                        │
│   HTML/CSS/JS + Bootstrap + Jinja2 Templates        │
│   - 37 templates responsivos                         │
│   - Layout moderno com gradientes                    │
│   - PWA com service worker                           │
├─────────────────────────────────────────────────────┤
│                   APPLICATION                        │
│      Flask Routes + Business Logic + Forms           │
│   - 72 rotas HTTP (GET/POST)                         │
│   - Validações de formulários                        │
│   - Cálculo de comissões                             │
├─────────────────────────────────────────────────────┤
│                     DOMAIN                           │
│    Models (SQLAlchemy) + Regras de Negócio          │
│   - 8 modelos de dados                               │
│   - Relacionamentos (FK, Many-to-Many)               │
│   - Métodos de cálculo                               │
├─────────────────────────────────────────────────────┤
│                   PERSISTENCE                        │
│          PostgreSQL (Prod) / SQLite (Dev)            │
│   - Multi-tenant com empresa_id                      │
│   - Migrations automáticas                           │
│   - Backups programados                              │
└─────────────────────────────────────────────────────┘
```

### 🗂️ Estrutura de Diretórios

```
suameta/
├── app.py                    # Aplicação principal (72 rotas)
├── models.py                 # 8 modelos SQLAlchemy
├── forms.py                  # Formulários WTForms
├── config.py                 # Configurações (dev/prod)
├── requirements.txt          # Dependências Python
├── Procfile                  # Railway deploy
├── nixpacks.toml            # Build configuration
├── runtime.txt              # Python version
│
├── templates/               # 37 templates HTML
│   ├── base.html           # Template base responsivo
│   ├── dashboard.html      # Dashboard principal
│   ├── login.html          # Tela de login
│   ├── ajuda.html          # Central de ajuda
│   ├── metas/              # Templates de metas
│   ├── vendedores/         # Templates de vendedores
│   ├── equipes/            # Templates de equipes
│   ├── configuracoes/      # Templates de config
│   ├── super_admin/        # Templates super admin
│   └── vendedor/           # Dashboard vendedor
│
├── static/                  # Arquivos estáticos
│   ├── css/                # Estilos customizados
│   ├── img/                # Imagens e logos
│   ├── templates_excel/    # Templates Excel
│   ├── manifest.json       # PWA manifest
│   └── sw.js               # Service Worker
│
├── scripts/                 # Scripts utilitários
│   ├── init_db.py          # Inicializar banco
│   ├── init_data.py        # Dados de teste
│   └── migration_*.sql     # Migrações SQL
│
├── instance/                # Dados locais
│   └── suameta.db          # SQLite (dev)
│
└── docs/                    # Documentação
    ├── guias/              # Guias de uso
    └── referencias/        # Referências técnicas
```

---

## 📊 Modelos de Dados {#modelos}

### 1. 🏢 Empresa

**Multi-Tenancy Base**

```python
class Empresa(db.Model):
    id = PrimaryKey
    nome = String(100)
    cnpj = String(20), unique
    ativo = Boolean, default=True
    logo_url = String(200), optional
    
    # Limites
    limite_vendedores = Integer, default=50
    limite_metas = Integer, default=1000
    plano = String(20), default='basico'
    
    # Timestamps
    created_at = DateTime
    updated_at = DateTime
    
    # Relacionamentos
    usuarios = relationship(Usuario)
    vendedores = relationship(Vendedor)
    metas = relationship(Meta)
    equipes = relationship(Equipe)
    faixas_comissao = relationship(FaixaComissao)
```

### 2. 👤 Usuario

**Autenticação e Permissões**

```python
class Usuario(UserMixin, db.Model):
    id = PrimaryKey
    nome = String(100)
    email = String(100), unique
    senha_hash = String(200)
    cargo = String(20)  # super_admin, admin, gerente, supervisor, vendedor
    
    # Status
    ativo = Boolean, default=True
    bloqueado = Boolean, default=False
    motivo_bloqueio = Text, optional
    is_super_admin = Boolean, default=False
    
    # 9 Permissões Granulares
    pode_ver_dashboard = Boolean, default=True
    pode_gerenciar_vendedores = Boolean, default=False
    pode_gerenciar_metas = Boolean, default=False
    pode_gerenciar_equipes = Boolean, default=False
    pode_gerenciar_comissoes = Boolean, default=False
    pode_enviar_mensagens = Boolean, default=True
    pode_exportar_dados = Boolean, default=False
    pode_ver_todas_metas = Boolean, default=False
    pode_aprovar_comissoes = Boolean, default=False
    
    # Relacionamentos
    empresa_id = ForeignKey(Empresa)
    vendedor_id = ForeignKey(Vendedor), optional
    empresa = relationship(Empresa)
    vendedor = relationship(Vendedor)
```

### 3. 💼 Vendedor

**Força de Vendas**

```python
class Vendedor(db.Model):
    id = PrimaryKey
    nome = String(100)
    email = String(100)
    telefone = String(20), optional
    ativo = Boolean, default=True
    meta_padrao = Decimal(10,2), optional
    
    # Relacionamentos
    empresa_id = ForeignKey(Empresa)
    equipe_id = ForeignKey(Equipe), optional
    empresa = relationship(Empresa)
    equipe = relationship(Equipe)
    metas = relationship(Meta)
    usuario = relationship(Usuario)
```

### 4. 🎯 Meta

**Objetivos Mensais**

```python
class Meta(db.Model):
    id = PrimaryKey
    mes = Integer  # 1-12
    ano = Integer  # ex: 2025
    valor_meta = Decimal(10,2)
    valor_realizado = Decimal(10,2), default=0
    percentual_atingimento = Decimal(5,2), computed
    status = String(20), computed  # atingida, parcial, nao_atingida
    comissao_calculada = Decimal(10,2), computed
    
    # Relacionamentos
    vendedor_id = ForeignKey(Vendedor)
    empresa_id = ForeignKey(Empresa)
    vendedor = relationship(Vendedor)
    empresa = relationship(Empresa)
    
    # Timestamps
    created_at = DateTime
    updated_at = DateTime
```

### 5. 👨‍👩‍👧‍👦 Equipe

**Agrupamento de Vendedores**

```python
class Equipe(db.Model):
    id = PrimaryKey
    nome = String(100)
    descricao = Text, optional
    ativo = Boolean, default=True
    
    # Relacionamentos
    empresa_id = ForeignKey(Empresa)
    supervisor_id = ForeignKey(Vendedor), optional
    empresa = relationship(Empresa)
    supervisor = relationship(Vendedor)
    vendedores = relationship(Vendedor)
```

### 6. 💰 FaixaComissao

**Configuração de Comissões**

```python
class FaixaComissao(db.Model):
    id = PrimaryKey
    percentual_min = Decimal(5,2)  # ex: 0.00
    percentual_max = Decimal(5,2)  # ex: 49.99
    percentual_comissao = Decimal(5,2)  # ex: 0.00 (0%)
    
    # Relacionamento
    empresa_id = ForeignKey(Empresa)
    empresa = relationship(Empresa)
```

**Faixas Padrão:**
- 0% - 49.99%: 0% comissão
- 50% - 79.99%: 1% comissão
- 80% - 99.99%: 2% comissão
- 100% - 119.99%: 5% comissão
- 120%+: 7% comissão

### 7. 📧 Mensagem

**Comunicação Interna**

```python
class Mensagem(db.Model):
    id = PrimaryKey
    assunto = String(200)
    corpo = Text
    lida = Boolean, default=False
    data_leitura = DateTime, optional
    
    # Relacionamentos
    remetente_id = ForeignKey(Usuario)
    destinatario_id = ForeignKey(Usuario)
    empresa_id = ForeignKey(Empresa)
    remetente = relationship(Usuario, foreign_keys=[remetente_id])
    destinatario = relationship(Usuario, foreign_keys=[destinatario_id])
    
    # Timestamp
    created_at = DateTime
```

### 8. 📦 Backup

**Sistema de Backups**

```python
class Backup(db.Model):
    id = PrimaryKey
    nome_arquivo = String(200)
    tamanho_bytes = Integer
    status = String(20)  # sucesso, erro
    mensagem_erro = Text, optional
    
    # Relacionamento
    empresa_id = ForeignKey(Empresa)
    empresa = relationship(Empresa)
    
    # Timestamp
    created_at = DateTime
```

### 📊 Diagrama de Relacionamentos

```
┌─────────────┐
│   Empresa   │────┐
└─────────────┘    │
       │           │
       ├───────────┼──────────┐
       │           │          │
       ▼           ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Usuario  │ │ Vendedor │ │  Equipe  │
└──────────┘ └──────────┘ └──────────┘
       │           │          │
       │           ▼          │
       │      ┌──────────┐   │
       │      │   Meta   │◄──┘
       │      └──────────┘
       │
       ▼
┌──────────────┐
│  Mensagem    │
└──────────────┘

┌─────────────────┐
│ FaixaComissao   │◄── Empresa
└─────────────────┘

┌─────────────────┐
│     Backup      │◄── Empresa
└─────────────────┘
```

---

## 🔐 Segurança {#seguranca}

### 🛡️ Medidas Implementadas

#### 1. Autenticação
- ✅ Hash seguro de senhas (werkzeug.security)
- ✅ Sessões criptografadas (Flask-Login)
- ✅ Token CSRF em todos os formulários
- ✅ Logout automático em inatividade
- ✅ Recuperação de senha via email

#### 2. Autorização
- ✅ Decorators de proteção de rotas
- ✅ Validação de empresa_id em todas as queries
- ✅ Isolamento multi-tenant
- ✅ 9 permissões granulares
- ✅ Bloqueio de usuários

#### 3. Validação de Dados
- ✅ Validação server-side (WTForms)
- ✅ Validação client-side (HTML5)
- ✅ Sanitização de inputs
- ✅ Proteção contra SQL Injection (ORM)
- ✅ Proteção XSS (Jinja2 auto-escape)

#### 4. Infraestrutura
- ✅ HTTPS obrigatório (Railway)
- ✅ Variáveis de ambiente seguras
- ✅ Banco de dados isolado
- ✅ Backups automáticos
- ✅ Logs de auditoria

### 🔒 Boas Práticas

**Para Administradores:**
- Trocar senhas padrão imediatamente
- Usar senhas fortes (min 8 caracteres)
- Revisar permissões periodicamente
- Fazer backups regulares
- Monitorar logs de acesso

**Para Usuários:**
- Não compartilhar credenciais
- Fazer logout em computadores públicos
- Reportar atividades suspeitas
- Manter dados atualizados

---

## 📱 PWA e Mobile {#pwa-mobile}

### 📲 Progressive Web App

O sistema é um **PWA completo**, funcionando como app nativo.

#### Recursos PWA:

✅ **Instalável:**
- Adicionar à tela inicial
- Funciona offline (cache)
- Ícone personalizado
- Splash screen

✅ **Responsivo:**
- Adapta a qualquer tela
- Touch-friendly
- Gestos nativos
- Notificações push (futuro)

✅ **Performance:**
- Service Worker
- Cache estratégico
- Carregamento rápido
- Otimizado para mobile

#### Manifest.json

```json
{
  "name": "Sistema de Metas - SuaMeta",
  "short_name": "SuaMeta",
  "description": "Sistema de Gestão de Metas e Comissões",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#007bff",
  "icons": [
    {
      "src": "/static/img/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/img/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 📱 Design Responsivo

**Breakpoints Bootstrap:**

- **Mobile:** < 576px
- **Tablet:** 576px - 992px
- **Desktop:** > 992px

**Adaptações:**
- Menu colapsável em mobile
- Cards empilhados verticalmente
- Tabelas com scroll horizontal
- Botões full-width
- Espaçamentos ajustados

---

## 🛠️ Deploy e Infraestrutura {#deploy}

### ☁️ Railway Cloud

**Produção:** https://vendacerta.up.railway.app

#### Configuração:

1. **Repositório:** GitHub conectado
2. **Deploy:** Automático ao push na main
3. **Build:** Nixpacks (Python)
4. **Banco:** PostgreSQL Railway
5. **Variáveis:** Environment variables
6. **Domínio:** railway.app (gratuito)

#### Variáveis de Ambiente:

```bash
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=chave-secreta-flask
FLASK_ENV=production
FLASK_DEBUG=False
```

### 🔄 Processo de Deploy

```bash
# 1. Desenvolvimento local
git add .
git commit -m "feat: Nova funcionalidade"

# 2. Push para GitHub
git push origin main

# 3. Deploy automático Railway
# Build iniciado automaticamente
# ~2-3 minutos para conclusão

# 4. Verificação
# Acessar URL e testar funcionalidades
```

### 📦 Estrutura de Build

**nixpacks.toml:**
```toml
[phases.setup]
nixPkgs = ['python311', 'postgresql']

[phases.install]
cmds = ['pip install -r requirements.txt']

[start]
cmd = 'gunicorn app:app'
```

**Procfile:**
```
web: gunicorn app:app
```

**runtime.txt:**
```
python-3.11.5
```

### 🔧 Comandos Úteis

```bash
# Verificar logs Railway
railway logs

# Conectar ao banco
railway connect

# Executar comando
railway run python init_db.py

# Ver status
railway status
```

### 💾 Backup e Restore

#### Backup Automático (Super Admin):

1. Acesse "Super Admin → Backups"
2. Clique "Criar Novo Backup"
3. Aguarde processamento
4. Download do arquivo .sql

#### Restore Manual:

```bash
# Local
psql -U postgres -d suameta < backup.sql

# Railway
railway connect postgres < backup.sql
```

---

## ❓ FAQ e Suporte {#faq}

### 🤔 Perguntas Frequentes

#### 1. Como criar um novo vendedor?

**Passo a Passo:**
1. Login como Admin/Gerente
2. Menu "Vendedores" → "Novo Vendedor"
3. Preencher nome, email, telefone
4. Definir meta padrão (opcional)
5. Clicar "Salvar"
6. Opcional: Criar login de acesso

#### 2. Como importar metas via Excel?

**Passo a Passo:**
1. Menu "Metas" → "Importar Metas"
2. Baixar template Excel
3. Preencher com dados:
   - Email do vendedor
   - Mês (1-12)
   - Ano (2025)
   - Valor da meta
   - Realizado (opcional)
4. Upload do arquivo
5. Conferir preview
6. Confirmar importação

#### 3. Como são calculadas as comissões?

**Fórmula:**
```
Comissão = Valor da Meta × Percentual da Faixa

Exemplo:
Meta: R$ 10.000
Realizado: R$ 11.500
Atingimento: 115%
Faixa: 100%-119% → 5%
Comissão: R$ 10.000 × 5% = R$ 500
```

#### 4. Como dar permissões específicas a um usuário?

**Super Admin:**
1. Menu "Super Admin" → "Usuários"
2. Clicar "Editar" no usuário
3. Rolar até "Permissões de Acesso"
4. Ativar/desativar switches
5. Salvar

#### 5. Como bloquear um vendedor temporariamente?

**Admin:**
1. Lista de Vendedores
2. Botão "Editar" no vendedor
3. Desmarcar "Ativo"
4. Salvar

**Para bloquear acesso ao sistema:**
1. Super Admin → Usuários
2. Botão "Bloquear" no usuário
3. Informar motivo
4. Confirmar

#### 6. Como exportar relatórios?

**Opções:**
1. **Metas:** Botão "Exportar PDF" na listagem
2. **Vendedores:** Botão "Exportar Excel"
3. **Comissões:** Menu "Comissões" → "Exportar"

#### 7. Como resetar senha de um usuário?

**Admin:**
1. Pedir para usar "Esqueci minha senha" no login
2. OU: Super Admin deleta e recria usuário com senha padrão

#### 8. Posso ter múltiplas empresas?

**Sim!** (Super Admin)
- Crie quantas empresas precisar
- Cada uma com dados isolados
- Controle de planos e limites
- Logo personalizada

#### 9. Como funciona o sistema offline (PWA)?

**Recursos Offline:**
- ✅ Visualização de dados em cache
- ✅ Interface carregada
- ❌ Novas ações exigem conexão
- ✅ Sincronização automática ao reconectar

#### 10. Como atualizar o sistema?

**Railway (Auto):**
- Push no GitHub → Deploy automático
- Sem downtime
- Rollback fácil se necessário

### 📞 Suporte Técnico

#### Canais de Ajuda:

1. **Central de Ajuda:** Dentro do sistema
   - Menu → "Ajuda"
   - 9 módulos de documentação
   - FAQs expandidas
   - Vídeos tutoriais (futuro)

2. **GitHub Issues:**
   - https://github.com/cristiano-superacao/suameta/issues
   - Reportar bugs
   - Sugerir melhorias

3. **Email:**
   - suporte@suameta.com
   - Resposta em até 24h

4. **Documentação:**
   - README.md (técnico)
   - CHANGELOG.md (versões)
   - SISTEMA_PERMISSOES_GRANULARES.md (permissões)
   - Este guia completo

### 🐛 Reportar Problemas

**Ao reportar bug, informe:**
- Navegador e versão
- Ação que causou o erro
- Mensagem de erro (se houver)
- Prints de tela
- Cargo/perfil do usuário

### 💡 Sugestões de Melhorias

**Como sugerir:**
1. Abrir issue no GitHub
2. Descrever melhoria desejada
3. Explicar caso de uso
4. Prioridade (baixa/média/alta)

---

## 📝 Changelog Resumido

### v2.9.1 (14 Dez 2025)
- ✨ Gerente e Supervisor podem lançar metas
- ✨ Sistema completo de permissões granulares
- ✨ Modal de visualização de permissões
- 🎨 Modernização da Central de Ajuda
- 📚 Documentação consolidada

### v2.9.0 (13 Dez 2025)
- ✨ Sistema de permissões granulares (9 permissões)
- ✨ Gerenciamento completo de usuários (Super Admin)
- 🔒 Bloqueio de usuários com motivo
- 📊 Dashboard de usuários ativos/bloqueados

### v2.8.0 (Anterior)
- ✨ Importação de metas via Excel
- ✨ Importação de vendedores via Excel
- 📧 Sistema de mensagens
- 🎯 Projeção de comissões
- 📱 PWA completo

---

## 🎯 Conclusão

O **Sistema SuaMeta** é uma solução completa, moderna e profissional para gestão de metas e comissões. Com arquitetura multi-tenant, 9 permissões granulares, layout 100% responsivo e hospedagem na nuvem, atende desde pequenas empresas até operações complexas.

### ✨ Principais Diferenciais:

1. **Multi-Empresa:** Gerencie infinitas empresas em um só sistema
2. **Permissões Granulares:** Controle total sobre o que cada usuário pode fazer
3. **Cálculo Automático:** Comissões calculadas instantaneamente
4. **Importação Excel:** Carga em massa de vendedores e metas
5. **PWA:** Funciona como app nativo no celular
6. **Cloud-Native:** 100% na nuvem, sem manutenção de servidores
7. **Interface Moderna:** Design profissional e responsivo
8. **Documentação Completa:** Guias para todos os perfis

### 🚀 Próximos Passos:

- Notificações push (PWA)
- Gráficos avançados (Chart.js)
- Relatórios customizáveis
- Integração com WhatsApp
- App mobile nativo (React Native)
- Dashboard analytics avançado
- Gamificação de metas

---

**Desenvolvido com ❤️ por SuaMeta Team**  
**Versão:** 2.9.1  
**Última Atualização:** 14 de Dezembro de 2025
