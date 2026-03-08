# 📋 Mapeamento Completo: Rotas ↔ Templates

**Versão**: 2.9.3  
**Data**: 14 de Dezembro de 2025  
**Status**: ✅ 100% Mapeado e Validado

---

## 🎯 Índice por Módulo

1. [Autenticação](#autenticação)
2. [Dashboards](#dashboards)
3. [Vendedores](#vendedores)
4. [Mensagens](#mensagens)
5. [Metas](#metas)
6. [Equipes](#equipes)
7. [Supervisores](#supervisores)
8. [Comissões](#comissões)
9. [Super Admin](#super-admin)
10. [Ajuda](#ajuda)

---

## 1. Autenticação

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/login` | GET, POST | `login.html` | `login()` |
| `/registro` | GET, POST | `registro.html` | `registro()` |
| `/logout` | GET | - (redirect) | `logout()` |
| `/recuperar-senha` | GET, POST | `recuperar_senha.html` | `recuperar_senha()` |
| `/redefinir-senha/<token>` | GET, POST | `redefinir_senha.html` | `redefinir_senha(token)` |

**Templates:**
- ✅ `templates/login.html`
- ✅ `templates/registro.html`
- ✅ `templates/recuperar_senha.html`
- ✅ `templates/redefinir_senha.html`

---

## 2. Dashboards

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/` | GET | `dashboard.html` | `dashboard()` |
| `/dashboard` | GET | `dashboard.html` | `dashboard()` |
| `/vendedor/dashboard` | GET | `vendedor/dashboard.html` | `vendedor_dashboard()` |
| `/dashboard/exportar-pdf` | GET | - (PDF) | `exportar_pdf_dashboard()` |

**Templates:**
- ✅ `templates/dashboard.html` - Dashboard principal (admin/supervisor/gerente)
- ✅ `templates/vendedor/dashboard.html` - Dashboard do vendedor (cargo='vendedor')

---

## 3. Vendedores

### CRUD Básico

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/vendedores` | GET | `vendedores/lista.html` | `lista_vendedores()` |
| `/vendedores/novo` | GET, POST | `vendedores/form.html` | `novo_vendedor()` |
| `/vendedores/<id>/editar` | GET, POST | `vendedores/form.html` | `editar_vendedor(id)` |
| `/vendedores/<id>/deletar` | POST | - (redirect) | `deletar_vendedor(id)` |
| `/vendedores/importar` | GET, POST | `vendedores/importar.html` | `importar_vendedores()` |

### Gestão de Login e Permissões

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/vendedores/<id>/criar-login` | GET, POST | `vendedores/criar_login.html` | `criar_login_vendedor(id)` |
| `/vendedores/<id>/resetar-senha` | GET, POST | `vendedores/resetar_senha.html` | `resetar_senha_vendedor(id)` |
| `/vendedores/<id>/permissoes` | GET, POST | `vendedores/permissoes.html` | `gerenciar_permissoes_vendedor(id)` |
| `/vendedores/<id>/ativar` | POST | - (redirect) | `ativar_vendedor(id)` |
| `/vendedores/<id>/desativar` | POST | - (redirect) | `desativar_vendedor(id)` |

**Templates:**
- ✅ `templates/vendedores/lista.html` - Listagem com dropdown de ações
- ✅ `templates/vendedores/form.html` - Formulário criar/editar
- ✅ `templates/vendedores/importar.html` - Importação Excel
- ✅ `templates/vendedores/criar_login.html` - Criar acesso vendedor
- ✅ `templates/vendedores/resetar_senha.html` - Resetar senha
- ✅ `templates/vendedores/permissoes.html` - Gerenciar permissões

---

## 4. Mensagens

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/mensagens` | GET | `mensagens/caixa_entrada.html` | `caixa_entrada()` |
| `/mensagens/enviadas` | GET | `mensagens/enviadas.html` | `mensagens_enviadas()` |
| `/mensagens/nova` | GET, POST | `mensagens/nova.html` | `nova_mensagem()` |
| `/mensagens/<id>` | GET | `mensagens/ver.html` | `ver_mensagem(id)` |
| `/mensagens/<id>/arquivar` | POST | - (redirect) | `arquivar_mensagem(id)` |
| `/mensagens/<id>/marcar-lida` | POST | - (JSON) | `marcar_como_lida(id)` |
| `/mensagens/<id>/deletar` | POST | - (redirect) | `deletar_mensagem(id)` |
| `/mensagens/enviar-equipe` | GET, POST | `mensagens/enviar_equipe.html` | `enviar_mensagem_equipe()` |

**Templates:**
- ✅ `templates/mensagens/caixa_entrada.html` - Inbox com tabs
- ✅ `templates/mensagens/enviadas.html` - Mensagens enviadas
- ✅ `templates/mensagens/nova.html` - Nova mensagem individual
- ✅ `templates/mensagens/ver.html` - Detalhes da mensagem
- ✅ `templates/mensagens/enviar_equipe.html` - Broadcast para equipe

---

## 5. Metas

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/metas` | GET | `metas/lista.html` | `lista_metas()` |
| `/metas/nova` | GET, POST | `metas/form.html` | `nova_meta()` |
| `/metas/<id>/editar` | GET, POST | `metas/form.html` | `editar_meta(id)` |
| `/metas/<id>/deletar` | POST | - (redirect) | `deletar_meta(id)` |
| `/metas/importar` | GET, POST | `metas/importar.html` | `importar_metas()` |
| `/metas/exportar-pdf` | GET | - (PDF) | `exportar_pdf_metas()` |

**Templates:**
- ✅ `templates/metas/lista.html` - Listagem de metas
- ✅ `templates/metas/form.html` - Formulário criar/editar
- ✅ `templates/metas/importar.html` - Importação Excel

---

## 6. Equipes

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/equipes` | GET | `equipes/lista.html` | `lista_equipes()` |
| `/equipes/nova` | GET, POST | `equipes/form.html` | `nova_equipe()` |
| `/equipes/<id>/editar` | GET, POST | `equipes/form.html` | `editar_equipe(id)` |
| `/equipes/<id>/deletar` | POST | - (redirect) | `deletar_equipe(id)` |
| `/equipes/<id>/detalhes` | GET | `equipes/detalhes.html` | `detalhes_equipe(id)` |

**Templates:**
- ✅ `templates/equipes/lista.html` - Listagem de equipes
- ✅ `templates/equipes/form.html` - Formulário criar/editar
- ✅ `templates/equipes/detalhes.html` - Detalhes e membros

---

## 7. Supervisores

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/supervisores` | GET | `supervisores/lista.html` | `lista_supervisores()` |
| `/supervisores/novo` | GET, POST | `supervisores/form.html` | `novo_supervisor()` |
| `/supervisores/<id>/editar` | GET, POST | `supervisores/form.html` | `editar_supervisor(id)` |
| `/supervisores/<id>/deletar` | POST | - (redirect) | `deletar_supervisor(id)` |
| `/supervisores/importar` | GET, POST | `supervisores/importar.html` | `importar_supervisores()` |

**Templates:**
- ✅ `templates/supervisores/lista.html` - Listagem de supervisores
- ✅ `templates/supervisores/form.html` - Formulário criar/editar
- ✅ `templates/supervisores/importar.html` - Importação Excel

---

## 8. Comissões

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/configuracoes/comissoes` | GET | `configuracoes/comissoes.html` | `configuracoes_comissoes()` |
| `/configuracoes/comissoes/criar` | GET, POST | `configuracoes/comissao_form.html` | `criar_faixa_comissao()` |
| `/configuracoes/comissoes/<id>/editar` | GET, POST | `configuracoes/comissao_form.html` | `editar_faixa_comissao(id)` |
| `/configuracoes/comissoes/<id>/deletar` | POST | - (redirect) | `deletar_faixa_comissao(id)` |
| `/api/comissoes/faixas` | GET | - (JSON) | `api_faixas_comissoes()` |

**Templates:**
- ✅ `templates/configuracoes/comissoes.html` - Listagem de faixas
- ✅ `templates/configuracoes/comissao_form.html` - Formulário criar/editar

---

## 9. Super Admin

### Empresas

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/super-admin/empresas` | GET | `super_admin/empresas.html` | `super_admin_empresas()` |
| `/super-admin/empresas/criar` | GET, POST | `super_admin/empresa_form.html` | `super_admin_criar_empresa()` |
| `/super-admin/empresas/<id>/editar` | GET, POST | `super_admin/empresa_form.html` | `super_admin_editar_empresa(id)` |
| `/super-admin/empresas/<id>/visualizar` | GET | `super_admin/empresa_detalhes.html` | `super_admin_visualizar_empresa(id)` |
| `/super-admin/empresas/<id>/bloquear` | POST | - (redirect) | `super_admin_bloquear_empresa(id)` |
| `/super-admin/empresas/<id>/excluir` | POST | - (redirect) | `super_admin_excluir_empresa(id)` |

### Usuários

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/super-admin/usuarios` | GET | `super_admin/usuarios.html` | `super_admin_usuarios()` |
| `/super-admin/usuarios/criar` | GET, POST | `super_admin/usuario_form.html` | `super_admin_criar_usuario()` |
| `/super-admin/usuarios/<id>/editar` | GET, POST | `super_admin/usuario_form.html` | `super_admin_editar_usuario(id)` |
| `/super-admin/usuarios/<id>/bloquear` | POST | - (redirect) | `super_admin_bloquear_usuario(id)` |
| `/super-admin/usuarios/<id>/deletar` | POST | - (redirect) | `super_admin_deletar_usuario(id)` |

### Backups

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/super-admin/backups` | GET | `super_admin/backups.html` | `super_admin_backups()` |
| `/super-admin/backups/criar` | POST | - (redirect) | `criar_backup()` |
| `/super-admin/backups/download/<nome>` | GET | - (File) | `download_backup(nome)` |
| `/super-admin/backups/restaurar/<nome>` | POST | - (redirect) | `restaurar_backup(nome)` |
| `/super-admin/backups/deletar/<nome>` | POST | - (redirect) | `deletar_backup(nome)` |
| `/super-admin/backups/upload` | POST | - (redirect) | `upload_backup()` |

**Templates:**
- ✅ `templates/super_admin/empresas.html` - Listagem de empresas
- ✅ `templates/super_admin/empresa_form.html` - Formulário empresa
- ✅ `templates/super_admin/empresa_detalhes.html` - Detalhes empresa
- ✅ `templates/super_admin/usuarios.html` - Listagem de usuários
- ✅ `templates/super_admin/usuario_form.html` - Formulário usuário
- ✅ `templates/super_admin/backups.html` - Gestão de backups

---

## 10. Ajuda

| Rota | Método | Template | Função |
|------|--------|----------|---------|
| `/ajuda` | GET | `ajuda.html` | `ajuda()` |
| `/manual` | GET | - (redirect) | `manual()` |

**Templates:**
- ✅ `templates/ajuda.html` - Central de ajuda

---

## 🔧 APIs e Rotas Especiais

| Rota | Método | Retorno | Função |
|------|--------|---------|---------|
| `/api/ranking` | GET | JSON | `api_ranking()` |
| `/api/comissoes/faixas` | GET | JSON | `api_faixas_comissoes()` |
| `/migrar-faixas-comissao-agora` | GET | - | `migrar_faixas_comissao_agora()` |
| `/setup-inicial-sistema` | GET | - | `setup_inicial_sistema()` |

---

## 📊 Template Base

**`templates/base.html`** - Template principal usado por herança

**Componentes:**
- ✅ Sidebar responsiva
- ✅ Menu navegação
- ✅ Área de mensagens flash
- ✅ Footer
- ✅ Scripts Bootstrap 5.3.3
- ✅ CSS personalizado
- ✅ PWA manifest

**Uso:**
```django
{% extends "base.html" %}
{% block title %}Título da Página{% endblock %}
{% block content %}
  <!-- Conteúdo -->
{% endblock %}
```

---

## 🎨 Estrutura de Pastas

```
templates/
├── base.html                    # Template base (herança)
├── login.html                   # Autenticação
├── registro.html                # Cadastro
├── recuperar_senha.html         # Recuperação
├── redefinir_senha.html         # Redefinição
├── dashboard.html               # Dashboard principal
├── ajuda.html                   # Central de ajuda
│
├── vendedor/
│   └── dashboard.html           # Dashboard do vendedor
│
├── vendedores/
│   ├── lista.html               # Listagem
│   ├── form.html                # Criar/Editar
│   ├── importar.html            # Importação
│   ├── criar_login.html         # Criar acesso
│   ├── resetar_senha.html       # Resetar senha
│   └── permissoes.html          # Permissões
│
├── mensagens/
│   ├── caixa_entrada.html       # Inbox
│   ├── enviadas.html            # Enviadas
│   ├── nova.html                # Nova mensagem
│   ├── ver.html                 # Detalhes
│   └── enviar_equipe.html       # Broadcast
│
├── metas/
│   ├── lista.html               # Listagem
│   ├── form.html                # Criar/Editar
│   └── importar.html            # Importação
│
├── equipes/
│   ├── lista.html               # Listagem
│   ├── form.html                # Criar/Editar
│   └── detalhes.html            # Detalhes
│
├── supervisores/
│   ├── lista.html               # Listagem
│   ├── form.html                # Criar/Editar
│   └── importar.html            # Importação
│
├── configuracoes/
│   ├── comissoes.html           # Listagem faixas
│   └── comissao_form.html       # Criar/Editar faixa
│
└── super_admin/
    ├── empresas.html            # Listagem empresas
    ├── empresa_form.html        # Criar/Editar empresa
    ├── empresa_detalhes.html    # Detalhes empresa
    ├── usuarios.html            # Listagem usuários
    ├── usuario_form.html        # Criar/Editar usuário
    └── backups.html             # Gestão backups
```

---

## 🔒 Decorators de Proteção

### Templates que Requerem Autenticação:
**Todos exceto:**
- `login.html`
- `registro.html`
- `recuperar_senha.html`
- `redefinir_senha.html`

### Templates Protegidos por Permissão:

**Super Admin apenas:**
- `super_admin/*` - Todos os templates

**Admin ou permissão específica:**
- `vendedores/criar_login.html` - `@permission_required('pode_gerenciar_vendedores')`
- `vendedores/permissoes.html` - `@admin_required`
- `configuracoes/comissoes.html` - `@admin_required`
- `mensagens/*` - `@permission_required('pode_enviar_mensagens')`

---

## 📈 Estatísticas

```
Total de Templates: 36
Total de Rotas: 70
Total de Módulos: 10

Distribuição:
• Autenticação: 4 templates, 5 rotas
• Dashboards: 2 templates, 4 rotas
• Vendedores: 6 templates, 9 rotas
• Mensagens: 5 templates, 8 rotas
• Metas: 3 templates, 6 rotas
• Equipes: 3 templates, 5 rotas
• Supervisores: 3 templates, 5 rotas
• Comissões: 2 templates, 5 rotas
• Super Admin: 6 templates, 17 rotas
• Ajuda: 1 template, 2 rotas
• Base: 1 template (herança)

Cobertura: 100% ✅
```

---

## ✅ Validação

**Todas as rotas GET que renderizam templates:**
- ✅ Têm template correspondente
- ✅ Template existe fisicamente
- ✅ Template está acessível

**Todos os templates:**
- ✅ São usados por pelo menos uma rota
- ✅ Herdam de base.html (exceto base.html)
- ✅ Têm responsividade Bootstrap 5.3.3

**Resultado:**
- ✅ **100% de cobertura**
- ✅ **Zero templates órfãos**
- ✅ **Zero rotas sem template**

---

**Documentação criada em**: 14 de Dezembro de 2025  
**Versão**: 2.9.3  
**Status**: ✅ Validado e Completo
