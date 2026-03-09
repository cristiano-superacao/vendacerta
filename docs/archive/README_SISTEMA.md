# 📊 Sistema de Gestão de Metas e Comissões - Documentação Completa

## 🎯 Visão Geral

Sistema profissional completo para gerenciamento de metas de vendas, cálculo automático de comissões e acompanhamento de desempenho em tempo real.

**Status**: ✅ Totalmente funcional e otimizado  
**Versão**: 1.0  
**Data**: Dezembro 2025

---

## 📁 Estrutura do Projeto

### Arquivos Principais

```
suameta/
├── app.py                      # Aplicação Flask principal (849 linhas)
├── models.py                   # Modelos de banco de dados (SQLAlchemy)
├── forms.py                    # Formulários WTForms
├── config.py                   # Configurações (Dev/Prod/Test)
├── pdf_generator.py            # Geração de relatórios PDF
├── calculo_comissao.py         # Lógica de cálculo de comissões
├── migrate.py                  # ✨ Script consolidado de migração
│
├── requirements.txt            # Dependências Python
├── Procfile                    # Configuração Render/Heroku
├── railway.json                # Configuração Railway
├── nixpacks.toml              # Build Railway
├── runtime.txt                 # Versão Python
│
├── static/
│   └── css/
│       └── theme.css          # ✨ Tema unificado e responsivo
│
└── templates/
    ├── base.html              # ✨ Template base responsivo
    ├── login.html
    ├── registro.html
    ├── dashboard.html
    ├── recuperar_senha.html
    ├── redefinir_senha.html
    ├── ajuda.html
    ├── vendedores/
    │   ├── lista.html
    │   └── form.html
    ├── metas/
    │   ├── lista.html
    │   └── form.html
    ├── equipes/
    │   ├── lista.html
    │   ├── form.html
    │   └── detalhes.html
    └── super_admin/
        ├── empresas.html
        ├── empresa_form.html
        └── empresa_detalhes.html
```

### Arquivos de Documentação

```
📄 README.md                    # Documentação principal
📄 DEPLOY.md                    # ✨ Guia consolidado de deploy
📄 MANUAL_USUARIO.md            # Manual para usuários finais
📄 DOCUMENTACAO_SUPORTE.md      # Documentação de suporte
📄 README_SISTEMA.md            # Este arquivo
```

### ❌ Arquivos Removidos (Duplicados)

Foram removidos **20 arquivos duplicados** para simplificar o projeto:

**Scripts Python (10)**:
- aplicar_migracao_auto.py
- aplicar_migracao_final.py
- aplicar_migracao_railway.py
- migrar_banco.py
- migrar_railway_simples.py
- configurar_railway.py
- configurar_railway_automatico.py
- configurar_railway_completo.py
- criar_banco_completo.py
- criar_banco_novo.py

**Arquivos Markdown (10)**:
- DEPLOY_AUTOMATICO.md
- DEPLOY_FINAL.md
- DEPLOY_RAILWAY_RAPIDO.md
- FINALIZE_DEPLOY.md
- GUIA_DEPLOY_RAILWAY.md
- GUIA_3_CLIQUES.md
- GUIA_RAILWAY_PASSO_A_PASSO.md
- GUIA_CORRECAO_RAILWAY.md
- deploy_railway.bat
- finalizar_railway.bat

**✅ Substituídos por**:
- `migrate.py` - Script único e inteligente de migração
- `DEPLOY.md` - Guia consolidado de deploy

---

## ✨ Funcionalidades Implementadas

### 🔐 Autenticação e Segurança

✅ **Sistema de Login Completo**
- Login com email e senha
- Registro de novos usuários
- Validação de formulários
- Proteção contra CSRF
- Senhas com hash bcrypt
- Sessões seguras com Flask-Login

✅ **Recuperação de Senha**
- Link "Esqueceu a senha?" no login
- Geração de token seguro com limite de tempo
- Página de redefinição de senha
- Validação de token e expiração

✅ **Controle de Acesso**
- 3 níveis: Super Admin, Admin, Usuário
- Proteção de rotas com decorators
- Isolamento de dados por empresa

✅ **Headers de Segurança HTTP**
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Strict-Transport-Security
- Content-Security-Policy

### 👥 Gestão de Vendedores

✅ **CRUD Completo**
- Listar todos os vendedores
- Criar novo vendedor (nome, email, telefone, CPF)
- Editar informações
- Deletar vendedor (com confirmação)
- Ativar/desativar vendedor

✅ **Vinculação com Equipes**
- Atribuir vendedor a uma equipe
- Listar vendedores por equipe
- Supervisor da equipe

✅ **Histórico de Performance**
- Metas atingidas
- Comissões recebidas
- Ranking no dashboard

### 🏢 Gestão de Equipes

✅ **Gerenciamento de Equipes**
- Criar equipe com nome e descrição
- Atribuir supervisor
- Adicionar/remover vendedores
- Visualizar performance da equipe

✅ **Estatísticas de Equipe**
- Total de vendedores
- Metas coletivas
- Receita total da equipe
- Ranking entre equipes

### 📊 Gestão de Metas

✅ **Criação de Metas**
- Meta mensal por vendedor
- Valor de receita esperado
- Período (mês/ano)
- Descrição opcional

✅ **Atualização de Receitas**
- Atualizar receita alcançada
- Cálculo automático de percentual
- Cálculo automático de comissão
- Status de pagamento

✅ **Filtros e Busca**
- Filtrar por vendedor
- Filtrar por período (mês/ano)
- Filtrar por status de pagamento
- Busca textual

✅ **Cálculo Automático de Comissões**

| Alcance da Meta | Taxa | Cor |
|-----------------|------|-----|
| Até 50% | 1% | 🔴 Vermelho |
| 51% - 75% | 2% | 🟠 Laranja |
| 76% - 100% | 3% | 🔵 Azul |
| 101% - 125% | 4% | 🟢 Verde Claro |
| Acima de 125% | 5% | 🟢 Verde Escuro |

**Fórmula**: `Comissão = Receita Alcançada × Taxa da Faixa`

### 🏢 Sistema Multi-Empresa

✅ **Super Administrador Global**
- Acesso a todas as empresas
- Criar/editar/bloquear empresas
- Visualizar estatísticas globais
- Menu exclusivo no sidebar

✅ **Gestão de Empresas**
- CRUD completo de empresas
- Informações: nome, CNPJ, email, telefone, endereço
- Configurações: plano, limites de usuários/vendedores
- Status: ativo/inativo, bloqueado/desbloqueado

✅ **Isolamento de Dados**
- Cada empresa vê apenas seus dados
- Super Admin vê tudo
- Segurança por empresa_id

### 📈 Dashboard Interativo

✅ **Cards de Estatísticas**
- Total de vendedores
- Receita total alcançada
- Meta total do mês
- Comissões a pagar
- Percentual de alcance geral

✅ **Ranking de Vendedores**
- Top performersem tempo real
- Percentual de alcance
- Comissão calculada
- Cores por faixa de performance

✅ **Visualizações**
- Barras de progresso coloridas
- Gradientes modernos
- Ícones Bootstrap Icons
- Animações suaves

### 📄 Exportação de Relatórios PDF

✅ **PDF do Dashboard**
- Estatísticas gerais
- Ranking de vendedores
- Logo e formatação profissional
- Gerado em tempo real

✅ **PDF de Metas por Período**
- Filtro por mês/ano
- Tabela completa de metas
- Totalizadores
- Status de pagamento

### 🎨 Layout e Responsividade

✅ **Design Profissional**
- Sidebar moderna com gradientes
- Cores vibrantes e modernas
- Tipografia Inter (Google Fonts)
- Bootstrap Icons

✅ **100% Responsivo**
- Mobile-first approach
- Breakpoints: 576px, 768px, 992px
- Sidebar retrátil em mobile
- Menu hambúrguer
- Cards adaptáveis

✅ **Tema Unificado** ([theme.css](cci:1://file:///workspaces/suameta/static/css/theme.css:0:0-0:0))
- CSS Variables para cores
- Componentes reutilizáveis
- Gradientes consistentes
- Animações suaves

### 📞 Central de Ajuda

✅ **Página de Ajuda** (`/ajuda`)
- 6 categorias de ajuda
- Perguntas frequentes
- Card de suporte com contato
- Busca em tempo real

✅ **Informações de Suporte**
- Nome: Cristiano Santos
- WhatsApp: (71) 99337-2960
- Email: cristiano.s.santos@ba.estudante.senai.br
- Horário: Seg-Sex 8h-18h, Sáb 8h-12h

### 💾 Banco de Dados

✅ **Suporte Múltiplo**
- SQLite para desenvolvimento
- PostgreSQL para produção
- Migrations automáticas

✅ **Modelos** ([models.py](cci:1://file:///workspaces/suameta/models.py:0:0-0:0))
- Empresa
- Usuario
- Vendedor
- Equipe
- Meta

✅ **Relacionamentos**
- ForeignKeys configurados
- Backref para navegação
- Cascade para deletions

---

## 🚀 Como Usar

### 1️⃣ Desenvolvimento Local

```bash
# 1. Clonar repositório
git clone https://github.com/cristiano-superacao/suameta.git
cd suameta

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar migração
python migrate.py
# Detecta automaticamente SQLite
# Cria metas.db
# Cria usuários padrão

# 5. Rodar aplicação
python app.py

# 6. Acessar
# http://127.0.0.1:5000
```

**Credenciais Padrão**:
**Primeiro acesso (sem senha padrão)**:
- 👑 Super Admin: `superadmin@suameta.com` (senha definida no seu ambiente)
- 🔑 Admin: defina `ADMIN_EMAIL`/`ADMIN_PASSWORD` e execute `python scripts/create_admin.py`

### 2️⃣ Deploy em Produção

Consulte [DEPLOY.md](cci:1://file:///workspaces/suameta/DEPLOY.md:0:0-0:0) para instruções detalhadas.

**Opções de Deploy**:
- ✅ Railway (Recomendado)
- ✅ Render (Alternativa gratuita)

**Passos Básicos**:
1. Criar projeto na plataforma
2. Adicionar PostgreSQL
3. Configurar variáveis de ambiente
4. Executar `python migrate.py` com DATABASE_URL
5. Acessar aplicação

---

## 🔧 Arquivos Consolidados

### `migrate.py` - Script Universal de Migração

**Recursos**:
- ✅ Detecção automática de ambiente (local/produção)
- ✅ Suporte SQLite e PostgreSQL
- ✅ Leitura de DATABASE_URL de múltiplas fontes
- ✅ Criação de estrutura completa
- ✅ Criação de empresa padrão
- ✅ Criação de usuários admin

**Uso**:
```bash
# Ambiente local (SQLite)
python migrate.py

# Ambiente produção (PostgreSQL)
export DATABASE_URL="postgresql://..."
python migrate.py

# Ou colar quando solicitado
python migrate.py
# Digite 's' quando perguntado
# Cole DATABASE_URL
```

### [theme.css](cci:1://file:///workspaces/suameta/static/css/theme.css:0:0-0:0) - Tema Unificado

**Características**:
- CSS Variables para cores
- Gradientes: `--gradient-start`, `--gradient-end`
- Componentes: cards, tables, progress bars, buttons
- Responsividade: breakpoints 576px, 768px, 992px
- Animações: fade-in, hover effects

**Exemplo de Uso**:
```html
<div class="stats-card hover-lift">
    <h3 class="stats-value-lg">R$ 150.000</h3>
    <p class="stats-title">Receita Total</p>
</div>
```

### [base.html](cci:1://file:///workspaces/suameta/templates/base.html:0:0-0:0) - Template Responsivo

**Estrutura**:
- Sidebar com menu dinâmico
- Toggle para mobile
- Footer com informações de suporte
- Blocos extensíveis: `content`, `extra_css`, `extra_js`

**JavaScript Integrado**:
- Toggle sidebar mobile
- Fechar ao clicar fora
- Animação de progress bars
- Auto-close em navegação

---

## 📊 Tecnologias Utilizadas

### Backend
- **Python 3.11**
- **Flask 3.0** - Framework web
- **SQLAlchemy** - ORM
- **Flask-Login** - Autenticação
- **WTForms** - Formulários
- **Werkzeug** - Hash de senhas
- **ReportLab** - Geração de PDFs
- **psycopg2-binary** - Driver PostgreSQL
- **Gunicorn** - Servidor WSGI

### Frontend
- **Bootstrap 5.3.3** - Framework CSS
- **Bootstrap Icons 1.11.3** - Ícones
- **Google Fonts Inter** - Tipografia
- **CSS3** - Gradientes e animações
- **JavaScript ES6** - Interatividade

### Banco de Dados
- **SQLite** - Desenvolvimento
- **PostgreSQL** - Produção

### Deploy
- **Railway** - PaaS recomendado
- **Render** - Alternativa gratuita
- **Nixpacks** - Build system

---

## 🎯 Melhorias Implementadas

### ✅ Consolidação
- ❌ 20 arquivos duplicados removidos
- ✅ 1 script de migração (`migrate.py`)
- ✅ 1 guia de deploy ([DEPLOY.md](cci:1://file:///workspaces/suameta/DEPLOY.md:0:0-0:0))
- ✅ 1 tema CSS ([theme.css](cci:1://file:///workspaces/suameta/static/css/theme.css:0:0-0:0))

### ✅ Responsividade
- Mobile-first design
- Sidebar retrátil
- Cards adaptáveis
- Tabelas responsivas
- Formulários otimizados

### ✅ Segurança
- Headers HTTP seguros
- CSRF protection
- Hash bcrypt de senhas
- Validação de entrada
- Sanitização de dados

### ✅ Performance
- CSS minificado
- Lazy loading
- Queries otimizadas
- Pool de conexões

### ✅ UX/UI
- Gradientes modernos
- Animações suaves
- Feedback visual
- Mensagens flash
- Confirmações de ação

---

## 📞 Suporte e Contato

**Desenvolvedor**: Cristiano Santos  
**WhatsApp**: [(71) 99337-2960](https://wa.me/5571993372960)  
**Email**: cristiano.s.santos@ba.estudante.senai.br  
**Horário**: Seg-Sex 8h-18h, Sáb 8h-12h

**Links Úteis**:
- [Central de Ajuda](/ajuda)
- [Manual do Usuário](cci:1://file:///workspaces/suameta/MANUAL_USUARIO.md:0:0-0:0)
- [Guia de Deploy](cci:1://file:///workspaces/suameta/DEPLOY.md:0:0-0:0)

---

## 📝 Changelog

### Versão 1.0 - Dezembro 2025

**Adicionado**:
- ✅ Sistema multi-empresa
- ✅ Super administrador
- ✅ Recuperação de senha
- ✅ Central de ajuda
- ✅ Exportação PDF
- ✅ Layout responsivo
- ✅ Script consolidado de migração
- ✅ Documentação consolidada

**Removido**:
- ❌ 10 scripts Python duplicados
- ❌ 10 arquivos markdown duplicados

**Otimizado**:
- ⚡ Tema CSS unificado
- ⚡ Template base responsivo
- ⚡ Queries de banco
- ⚡ Estrutura de arquivos

---

## 🚀 Próximos Passos

### Sugestões de Melhorias Futuras

- [ ] Dashboard com gráficos (Chart.js)
- [ ] Exportação Excel (openpyxl)
- [ ] Notificações por email (Flask-Mail)
- [ ] API REST (Flask-RESTful)
- [ ] Testes automatizados (pytest)
- [ ] CI/CD (GitHub Actions)
- [ ] Docker containerization
- [ ] Backup automático

---

## 📄 Licença

© 2025 Sistema de Gestão de Metas e Comissões  
Desenvolvido por Cristiano Santos  
Todos os direitos reservados

---

**🎉 Sistema 100% Funcional e Otimizado!**
