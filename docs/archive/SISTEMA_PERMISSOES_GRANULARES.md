# Sistema de Permissões Granulares

## 📋 Visão Geral

O sistema possui um **completo controle de permissões granulares** que permite ao Super Administrador definir exatamente o que cada usuário pode ver e fazer no sistema, independentemente do seu cargo.

## 🎯 Funcionalidades Implementadas

### ✅ 1. Gerenciamento de Usuários (Super Admin)

**Localização:** `/super-admin/usuarios`

O Super Administrador possui acesso total para:

- ✅ **Criar Usuários** - Cadastrar novos usuários no sistema
- ✅ **Editar Usuários** - Modificar dados e permissões de usuários existentes
- ✅ **Visualizar Permissões** - Ver todas as permissões de cada usuário via modal
- ✅ **Bloquear/Desbloquear** - Impedir/permitir acesso de usuários com motivo
- ✅ **Deletar Usuários** - Remover permanentemente usuários do sistema
- ✅ **Filtrar por Empresa** - Visualizar usuários de empresas específicas

### ✅ 2. Sistema de Permissões Granulares

O sistema possui **9 permissões configuráveis** que podem ser ativadas/desativadas individualmente para cada usuário:

#### 📊 Permissão: Visualizar Dashboard
- **Campo:** `pode_ver_dashboard`
- **Padrão:** ✅ Ativado
- **Descrição:** Permite acessar o dashboard com suas métricas e indicadores

#### ✉️ Permissão: Enviar Mensagens
- **Campo:** `pode_enviar_mensagens`
- **Padrão:** ✅ Ativado
- **Descrição:** Permite enviar mensagens para a equipe

#### 👥 Permissão: Gerenciar Vendedores
- **Campo:** `pode_gerenciar_vendedores`
- **Padrão:** ❌ Desativado
- **Descrição:** Permite criar, editar e excluir vendedores

#### 🎯 Permissão: Gerenciar Metas
- **Campo:** `pode_gerenciar_metas`
- **Padrão:** ❌ Desativado
- **Descrição:** Permite criar, editar e excluir metas
- **Observação:** Gerentes e Supervisores já possuem acesso por validação de cargo

#### 👁️ Permissão: Ver Todas as Metas
- **Campo:** `pode_ver_todas_metas`
- **Padrão:** ❌ Desativado
- **Descrição:** Permite visualizar metas de todos os vendedores da empresa

#### 👨‍👩‍👧‍👦 Permissão: Gerenciar Equipes
- **Campo:** `pode_gerenciar_equipes`
- **Padrão:** ❌ Desativado
- **Descrição:** Permite criar e organizar equipes de vendedores

#### 💰 Permissão: Gerenciar Comissões
- **Campo:** `pode_gerenciar_comissoes`
- **Padrão:** ❌ Desativado
- **Descrição:** Permite configurar faixas e regras de comissão

#### ✔️ Permissão: Aprovar Comissões
- **Campo:** `pode_aprovar_comissoes`
- **Padrão:** ❌ Desativado
- **Descrição:** Permite aprovar pagamento de comissões dos vendedores

#### 📥 Permissão: Exportar Dados
- **Campo:** `pode_exportar_dados`
- **Padrão:** ❌ Desativado
- **Descrição:** Permite exportar relatórios e dados em Excel/PDF

## 🎨 Interface de Usuário

### 1. Listagem de Usuários

**Recursos:**
- Cards de estatísticas (Total, Ativos, Bloqueados, Empresas)
- Tabela responsiva com informações dos usuários
- Badges coloridos para status e cargos
- 4 ações principais por usuário:
  - ✏️ **Editar** - Modificar dados e permissões
  - 🛡️ **Ver Permissões** - Modal com todas as permissões
  - 🔒 **Bloquear/Desbloquear** - Controlar acesso
  - 🗑️ **Deletar** - Remover permanentemente

### 2. Formulário de Edição

**Campos Principais:**
- Nome Completo
- Email (validado, único)
- Empresa
- Cargo (Usuário, Supervisor, Gerente, Admin)
- Status (Ativo/Inativo)
- Bloqueado (Sim/Não)
- Motivo do Bloqueio (quando aplicável)

**Seção de Permissões:** (visível apenas ao editar)
- 9 cards com switches toggle
- Ícones coloridos indicando permissão
- Descrição de cada permissão
- Layout em grid 2 colunas (responsivo)

### 3. Modal de Visualização de Permissões

**Características:**
- Modal grande (`modal-lg`) para melhor visualização
- 9 cards organizados em grid responsivo
- Indicadores visuais:
  - ✅ Check verde para permissões ativas
  - ❌ X vermelho para permissões negadas
  - Ícones coloridos conforme status
- Botão direto para editar permissões

## 💻 Implementação Técnica

### Backend (app.py)

#### Rota de Criação
```python
@app.route('/super-admin/usuarios/criar', methods=['GET', 'POST'])
@super_admin_required
def super_admin_criar_usuario():
    # Cria usuário com formulário
    # Define senha padrão: 'senha123'
    # Permissões recebem valores padrão do modelo
```

#### Rota de Edição (com permissões)
```python
@app.route('/super-admin/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@super_admin_required
def super_admin_editar_usuario(id):
    # Atualiza dados básicos do usuário
    # Processa 9 checkboxes de permissões via request.form
    # Atualiza campos pode_* no banco de dados
```

#### Rota de Listagem
```python
@app.route('/super-admin/usuarios')
@super_admin_required
def super_admin_usuarios():
    # Lista todos usuários (exceto super_admin)
    # Permite filtro por empresa
    # Envia dados para template
```

### Modelo de Dados (models.py)

```python
class Usuario(UserMixin, db.Model):
    # Campos básicos
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cargo = db.Column(db.String(20), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    bloqueado = db.Column(db.Boolean, default=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    
    # 9 Permissões Granulares
    pode_ver_dashboard = db.Column(db.Boolean, default=True)
    pode_gerenciar_vendedores = db.Column(db.Boolean, default=False)
    pode_gerenciar_metas = db.Column(db.Boolean, default=False)
    pode_gerenciar_equipes = db.Column(db.Boolean, default=False)
    pode_gerenciar_comissoes = db.Column(db.Boolean, default=False)
    pode_enviar_mensagens = db.Column(db.Boolean, default=True)
    pode_exportar_dados = db.Column(db.Boolean, default=False)
    pode_ver_todas_metas = db.Column(db.Boolean, default=False)
    pode_aprovar_comissoes = db.Column(db.Boolean, default=False)
```

### Formulários (forms.py)

```python
class UsuarioForm(FlaskForm):
    """Formulário de gerenciamento de usuários"""
    nome = StringField('Nome Completo', validators=[...])
    email = StringField('Email', validators=[...])
    cargo = SelectField('Cargo', choices=[...])
    empresa_id = SelectField('Empresa', coerce=int)
    ativo = SelectField('Status', choices=[...])
    bloqueado = SelectField('Bloqueado', choices=[...])
    motivo_bloqueio = TextAreaField('Motivo do Bloqueio')
```

**Observação:** As permissões são processadas diretamente via `request.form` na rota, não no formulário WTForms.

## 🔐 Segurança e Controle de Acesso

### Níveis de Acesso

1. **Super Admin**
   - Acesso total ao sistema
   - Gerencia todas as empresas
   - Configura permissões de todos os usuários
   - Não pode ser bloqueado ou editado

2. **Admin (por empresa)**
   - Acesso total à sua empresa
   - Gerencia vendedores, metas, equipes
   - Configurações de comissão
   - Pode ter permissões customizadas

3. **Gerente**
   - Gerencia equipes e metas
   - Visualiza dados da sua equipe
   - Permissões customizáveis

4. **Supervisor**
   - Supervisiona vendedores
   - Gerencia metas
   - Permissões customizáveis

5. **Vendedor/Usuário**
   - Acesso básico (dashboard, metas próprias)
   - Permissões podem ser expandidas

### Decorators de Proteção

```python
@super_admin_required  # Apenas Super Admin
@admin_required        # Admin ou superior
@login_required        # Qualquer usuário autenticado
```

## 📱 Responsividade

O sistema é **100% responsivo** com breakpoints para:

- 📱 **Mobile** (< 768px)
  - Grid de permissões em 1 coluna
  - Botões empilhados
  - Tabelas com scroll horizontal

- 💻 **Tablet** (768px - 992px)
  - Grid de permissões em 2 colunas
  - Layout otimizado

- 🖥️ **Desktop** (> 992px)
  - Grid completo
  - Todas as funcionalidades visíveis

## 🎨 Design e UX

### Paleta de Cores (por funcionalidade)

- 🔵 **Primary (#3b82f6)** - Dashboard, geral
- 🟢 **Success (#10b981)** - Vendedores, aprovações
- 🟡 **Warning (#f59e0b)** - Metas, alertas
- 🔴 **Danger (#ef4444)** - Bloqueios, exclusões
- 🟣 **Info (#06b6d4)** - Informações, mensagens
- ⚫ **Secondary (#718096)** - Usuários, equipes

### Componentes Modernos

- **Cards elevados** com shadow-sm
- **Hover effects** em todos os botões
- **Badges coloridos** para status
- **Icons do Bootstrap** para todas as ações
- **Tooltips** informativos
- **Modals** para confirmações
- **Switches** animados para permissões

## 🚀 Casos de Uso

### Caso 1: Criar Supervisor com Acesso Limitado

1. Super Admin acessa `/super-admin/usuarios`
2. Clica em "Novo Usuário"
3. Preenche dados básicos
4. Seleciona cargo "Supervisor"
5. Usuário é criado com senha padrão `senha123`
6. Supervisor faz login e troca a senha
7. Super Admin edita o supervisor
8. Ativa apenas: `pode_ver_dashboard`, `pode_gerenciar_metas`, `pode_ver_todas_metas`
9. Supervisor agora tem acesso controlado conforme permissões

### Caso 2: Gerente com Permissões Especiais

1. Super Admin cria usuário cargo "Gerente"
2. Gerente possui acesso via cargo para metas
3. Super Admin adiciona permissões extras:
   - `pode_gerenciar_equipes` ✅
   - `pode_exportar_dados` ✅
   - `pode_aprovar_comissoes` ✅
4. Gerente agora tem poderes de admin sem ser admin

### Caso 3: Vendedor com Acesso Expandido

1. Super Admin cria vendedor
2. Por padrão tem apenas: `pode_ver_dashboard` e `pode_enviar_mensagens`
3. Super Admin concede: `pode_ver_todas_metas` ✅
4. Vendedor pode ver metas de colegas (motivação/competição)
5. Mas não pode editar ou criar metas

## 📊 Estatísticas do Sistema

### Dados Monitorados

- **Total de Usuários** - Contador geral
- **Usuários Ativos** - Com ativo=True e bloqueado=False
- **Usuários Bloqueados** - Com bloqueado=True
- **Empresas Cadastradas** - Total de empresas no sistema

### Filtros Disponíveis

- **Por Empresa** - Mostra usuários de empresa específica
- **Por Status** - Ativo/Inativo (implementação futura)
- **Por Cargo** - Admin/Gerente/Supervisor/Vendedor (implementação futura)

## 🔄 Fluxo de Permissões

```
┌─────────────────────┐
│   Super Admin       │
│  (Acesso Total)     │
└──────────┬──────────┘
           │
           ├─► Cria Usuário → Define Cargo
           │
           ├─► Edita Usuário → Configura 9 Permissões
           │
           └─► Visualiza Permissões → Modal Informativo
                      │
                      ▼
           ┌──────────────────────┐
           │ Sistema Valida       │
           │ - Cargo (route)      │
           │ - Permissões (model) │
           └──────────────────────┘
                      │
                      ▼
           ┌──────────────────────┐
           │ Usuário Acessa       │
           │ Funcionalidades      │
           │ Permitidas           │
           └──────────────────────┘
```

## ✅ Checklist de Funcionalidades

### Super Admin - Gerenciamento de Usuários
- ✅ Criar usuários com senha padrão
- ✅ Editar dados básicos (nome, email, cargo, empresa)
- ✅ Configurar 9 permissões granulares via checkboxes
- ✅ Visualizar permissões em modal detalhado
- ✅ Bloquear/desbloquear com motivo
- ✅ Deletar usuários permanentemente
- ✅ Filtrar por empresa
- ✅ Ver estatísticas (total, ativos, bloqueados)

### Interface e UX
- ✅ Layout responsivo (mobile, tablet, desktop)
- ✅ Cards de permissões com ícones coloridos
- ✅ Switches animados para toggle de permissões
- ✅ Modal de visualização rápida
- ✅ Badges de status e cargo
- ✅ Tooltips informativos
- ✅ Design moderno e profissional

### Backend e Segurança
- ✅ Decorator @super_admin_required
- ✅ Validação de email único
- ✅ Processamento de permissões via request.form
- ✅ Valores padrão no modelo Usuario
- ✅ Multi-tenant (empresa_id)
- ✅ Timestamps (created_at, updated_at)

## 🎓 Como Usar

### Para Super Administrador

1. **Acessar Gerenciamento**
   ```
   Login como Super Admin → Menu → Super Admin → Usuários
   ```

2. **Criar Novo Usuário**
   ```
   Botão "Novo Usuário" → Preencher Dados → Salvar
   Senha padrão: senha123
   ```

3. **Configurar Permissões**
   ```
   Lista de Usuários → Botão Editar (✏️) → Rolar até "Permissões de Acesso"
   Ativar/Desativar switches conforme necessário → Salvar
   ```

4. **Visualizar Permissões**
   ```
   Lista de Usuários → Botão Ver Permissões (🛡️) → Modal com detalhes
   ```

5. **Bloquear Usuário**
   ```
   Lista de Usuários → Botão Bloquear (🔒) → Informar Motivo → Confirmar
   ```

### Para Usuários

1. **Primeiro Acesso**
   ```
   Receber credenciais do Super Admin
   Login com senha123 → Sistema solicita troca de senha
   ```

2. **Verificar Permissões**
   ```
   Menu disponível conforme permissões concedidas
   Itens sem permissão não aparecem no menu
   ```

## 📝 Observações Importantes

### Permissões vs Cargo

- **Cargo** define o nível hierárquico do usuário
- **Permissões** definem funcionalidades específicas acessíveis
- Um Supervisor pode ter mais permissões que um Gerente
- Flexibilidade total para o Super Admin

### Senha Padrão

- Todos os usuários criados recebem `senha123`
- Recomenda-se implementar troca obrigatória no primeiro login
- Super Admin deve orientar usuários a trocar senha

### Bloqueio vs Inativo

- **Inativo**: Usuário desativado temporariamente (sem motivo aparente)
- **Bloqueado**: Usuário bloqueado por motivo específico (exibido na tela de login)

### Multi-Tenant

- Cada usuário pertence a uma empresa (`empresa_id`)
- Filtros e visualizações respeitam isolamento por empresa
- Super Admin visualiza todas as empresas

## 🔮 Melhorias Futuras

### Planejado

- [ ] Troca obrigatória de senha no primeiro login
- [ ] Reset de senha via email
- [ ] Log de alterações de permissões (auditoria)
- [ ] Permissões em massa (bulk edit)
- [ ] Templates de permissões por cargo
- [ ] Exportação de relatório de usuários
- [ ] Filtros avançados (múltiplos critérios)
- [ ] Histórico de bloqueios

### Sugestões

- [ ] Permissões temporárias (com data de expiração)
- [ ] Grupos de permissões personalizados
- [ ] Notificação por email ao criar/bloquear usuário
- [ ] Dashboard de atividades dos usuários
- [ ] Integração com Active Directory (LDAP)

## 📞 Suporte

Para dúvidas sobre o sistema de permissões:

1. Consulte este documento
2. Acesse a Central de Ajuda no sistema
3. Entre em contato com o administrador do sistema

---

**Versão:** 2.9.1  
**Última Atualização:** 2024  
**Desenvolvido por:** Sistema SuaMeta  
**Layout:** Responsivo e Profissional ✨
