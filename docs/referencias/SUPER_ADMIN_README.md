# 🌟 Sistema de Super Administrador - Gerenciamento de Empresas

## ✅ Funcionalidades Implementadas

### 1. Modelo de Dados Multi-Empresa

#### Tabela `empresas`
- **Nome da empresa**
- **CNPJ** (validado e único)
- **Email e Telefone** para contato
- **Endereço completo** (cidade, estado)
- **Plano** (Básico, Premium, Enterprise)
- **Limites configuráveis**:
  - Máximo de usuários
  - Máximo de vendedores
- **Status**:
  - Ativo/Inativo
  - Bloqueado/Desbloqueado
  - Motivo do bloqueio

#### Tabela `usuarios` (atualizada)
- **empresa_id**: Relacionamento com empresa
- **is_super_admin**: Flag para super administrador (acesso total)

### 2. Sistema de Permissões

- **Super Administrador**: 
  - Não pertence a nenhuma empresa específica
  - Acesso a todas as funcionalidades de gestão de empresas
  - Pode criar, editar, bloquear e excluir empresas
  - Visualiza todas as empresas do sistema

- **Administrador de Empresa**:
  - Pertence a uma empresa específica
  - Gerencia apenas sua empresa
  - Acesso aos módulos normais (vendedores, metas, equipes)

### 3. Interface de Gerenciamento

#### 📊 Dashboard de Empresas (`/super-admin/empresas`)
- Lista todas as empresas cadastradas
- Informações exibidas:
  - Nome, CNPJ, Email/Telefone
  - Plano contratado
  - Número de usuários (atual/máximo)
  - Status (Ativo, Bloqueado, Inativo)
  - Data de criação
- Estatísticas:
  - Total de empresas
  - Empresas ativas
  - Empresas bloqueadas
  - Empresas inativas
- Ações rápidas:
  - Visualizar detalhes
  - Editar empresa
  - Bloquear/Desbloquear
  - Excluir (soft delete)

#### ➕ Criar Nova Empresa (`/super-admin/empresas/criar`)
- Formulário completo com validações:
  - Nome da empresa (obrigatório, 3-200 caracteres)
  - CNPJ (obrigatório, formato validado, único)
  - Email (obrigatório, formato validado)
  - Telefone (opcional, com máscara automática)
  - Endereço completo
  - Seleção de plano
  - Configuração de limites
- Máscaras automáticas:
  - CNPJ: `00.000.000/0000-00`
  - Telefone: `(00) 00000-0000`
- Validação em tempo real

#### ✏️ Editar Empresa (`/super-admin/empresas/<id>/editar`)
- Mesmo formulário de criação
- Pré-preenchido com dados existentes
- Validação de CNPJ excluindo próprio registro
- Exibe status atual da empresa

#### 👁️ Visualizar Detalhes (`/super-admin/empresas/<id>/visualizar`)
- Informações completas da empresa
- Estatísticas de uso:
  - Usuários cadastrados
  - Usuários ativos/inativos
  - Barra de progresso de uso
- Lista de todos os usuários da empresa:
  - Nome, email, cargo
  - Status (ativo/inativo)
  - Data de cadastro
  - Identificação de super admins
- Ações rápidas:
  - Editar empresa
  - Bloquear/Desbloquear

#### 🔒 Bloquear/Desbloquear Empresa (`/super-admin/empresas/<id>/bloquear`)
- Modal de confirmação
- Campo para motivo do bloqueio (opcional)
- Ao bloquear:
  - Empresa marcada como bloqueada
  - Motivo registrado no banco
  - Usuários mantidos, mas acesso bloqueado
- Ao desbloquear:
  - Empresa volta ao status ativo
  - Motivo removido

#### ❌ Excluir Empresa (`/super-admin/empresas/<id>/excluir`)
- Modal de confirmação com alerta
- Soft delete (não remove do banco):
  - Marca empresa como inativa
  - Bloqueia empresa automaticamente
  - Desativa todos os usuários da empresa
  - Mantém histórico no banco de dados

### 4. Menu de Navegação

- **Para Super Admins**:
  - Item especial no topo do menu lateral
  - Destaque visual (gradiente dourado)
  - Ícone de estrela
  - Separador visual

- **Para usuários normais**:
  - Menu padrão sem opção de gerenciar empresas

### 5. Layout Responsivo e Profissional

#### Design System
- **Cores**:
  - Gradiente principal: `#667eea` → `#764ba2`
  - Badges contextuais: success, danger, warning, info
  - Destaque dourado para super admin
  
- **Componentes**:
  - Cards com sombras suaves
  - Tabelas responsivas com hover
  - Modais Bootstrap 5
  - Badges e status visuais
  - Botões com ícones

#### Responsividade
- **Desktop**: Tabela completa com todas as colunas
- **Tablet**: Layout adaptado com grid
- **Mobile**: Cards empilhados verticalmente

### 6. Scripts de Migração

#### `migrar_banco.py`
- Migra banco existente para nova estrutura
- Adiciona colunas `empresa_id` e `is_super_admin`
- Cria empresa padrão
- Cria super administrador
- Associa usuários existentes

#### `criar_banco_novo.py`
- Cria banco do zero com nova estrutura
- Popula dados iniciais:
  - 1 empresa padrão
  - 1 super administrador
  - 1 administrador
  - 1 supervisor

## 🔐 Credenciais (sem senha padrão)

⚠️ Este documento é uma referência técnica e pode refletir exemplos de e-mails usados em ambientes antigos.

- **Não existem credenciais/senhas padrão** no sistema.
- A senha deve ser **definida na criação** do usuário.

**Exemplos de e-mails** (podem variar por ambiente):
- Super Admin: `superadmin@suameta.com`
- Admin (empresa): `admin@suameta.com`

Para primeiro acesso/criação de admin, siga o fluxo seguro em `docs/referencias/CREDENCIAIS.md` (via `ADMIN_EMAIL`/`ADMIN_PASSWORD` e `python scripts/create_admin.py`).

## 📁 Arquivos Criados/Modificados

### Modelos
- ✅ `models.py` - Adicionado modelo `Empresa` e campos em `Usuario`

### Formulários
- ✅ `forms.py` - Adicionado `EmpresaForm` com validações

### Rotas
- ✅ `app.py`:
  - Decorator `@super_admin_required`
  - 6 novas rotas para gerenciar empresas
  - Importações atualizadas

### Templates
- ✅ `templates/base.html` - Menu de super admin
- ✅ `templates/super_admin/empresas.html` - Lista de empresas
- ✅ `templates/super_admin/empresa_form.html` - Criar/editar empresa
- ✅ `templates/super_admin/empresa_detalhes.html` - Visualizar detalhes

### Scripts
- ✅ `migrar_banco.py` - Migração de banco existente
- ✅ `criar_banco_novo.py` - Criação de banco novo

## 🚀 Como Usar

### 1. Acessar como Super Admin
1. Fazer login com `superadmin@suameta.com`
2. Menu lateral exibirá "Gerenciar Empresas" no topo (com estrela dourada)
3. Clicar para acessar dashboard de empresas

### 2. Criar Nova Empresa
1. No dashboard, clicar em "Nova Empresa"
2. Preencher formulário:
   - Dados da empresa (nome, CNPJ, contato)
   - Endereço
   - Selecionar plano
   - Definir limites de usuários e vendedores
3. Salvar

### 3. Gerenciar Empresa Existente
- **Visualizar**: Ícone de olho → Detalhes completos + lista de usuários
- **Editar**: Ícone de lápis → Modificar informações
- **Bloquear**: Ícone de cadeado → Bloquear acesso (com motivo opcional)
- **Excluir**: Ícone de lixeira → Desativar empresa (soft delete)

### 4. Estatísticas
Dashboard exibe cards com:
- Total de empresas
- Empresas ativas
- Empresas bloqueadas  
- Empresas inativas

## 🎨 Destaques do Layout

### Responsivo
- ✅ Grid adaptável (desktop/tablet/mobile)
- ✅ Tabelas com scroll horizontal em mobile
- ✅ Cards empilháveis
- ✅ Modais centralizados

### Profissional
- ✅ Gradientes modernos
- ✅ Ícones Bootstrap
- ✅ Animações suaves
- ✅ Feedback visual em ações
- ✅ Status coloridos contextuais

### Acessibilidade
- ✅ Contraste adequado
- ✅ Tooltips informativos
- ✅ Confirmações para ações destrutivas
- ✅ Mensagens de erro claras

## 📋 Checklist de Funcionalidades

- ✅ Modelo de dados multi-empresa
- ✅ Sistema de permissões (super admin vs admin)
- ✅ CRUD completo de empresas
- ✅ Bloquear/desbloquear empresas
- ✅ Excluir empresas (soft delete)
- ✅ Visualizar detalhes e estatísticas
- ✅ Validação de CNPJ (formato e unicidade)
- ✅ Máscaras automáticas (CNPJ, telefone)
- ✅ Menu destacado para super admin
- ✅ Layout responsivo e profissional
- ✅ Confirmações em modais
- ✅ Scripts de migração
- ✅ Commits no GitHub
- ✅ Deploy automático no Railway

## ⚠️ Observações Importantes

1. **Primeiro Acesso**: Altere as senhas padrão
2. **Produção**: Execute `migrar_banco.py` para atualizar banco existente
3. **PostgreSQL**: Scripts compatíveis com SQLite e PostgreSQL
4. **Soft Delete**: Empresas excluídas não são removidas do banco
5. **Super Admin**: Não pertence a nenhuma empresa específica
6. **Limites**: Configuráveis por plano (básico/premium/enterprise)

---

**Status**: ✅ Implementação completa e funcional
**Deploy**: 🚀 Código enviado para produção (Railway)
**Documentação**: 📝 README completo criado
