# 🎨 Padrões de Interface (UI Patterns)

## Visão Geral

Este documento define os padrões de interface utilizados no sistema VendaCerta, garantindo consistência, responsividade e profissionalismo em todas as telas.

---

## 🎯 Princípios de Design

### 1. Responsividade First
- Mobile-first approach usando Bootstrap 5.3.3
- Breakpoints padrão: xs (<576px), sm (≥576px), md (≥768px), lg (≥992px), xl (≥1200px)
- Componentes adaptáveis para todas as resoluções

### 2. Acessibilidade (WCAG 2.1)
- Atributos `aria-label` e `role` em todos os elementos interativos
- Contraste de cores adequado (mínimo 4.5:1)
- Navegação por teclado funcional
- Leitores de tela compatíveis

### 3. Consistência Visual
- Paleta de cores semântica Bootstrap
- Ícones Bootstrap Icons v1.11.x
- Tipografia clara (fontes sistema padrão)
- Espaçamento harmonioso (grid 8px base)

---

## 📋 Padrões de Listagem

### Header Clean Pattern

```html
<div class="page-header-clean mb-4">
    <div class="header-content">
        <p class="header-subtitle">CATEGORIA</p>
        <h1 class="header-title">
            <i class="bi bi-icon"></i> Título da Página
        </h1>
    </div>
    <div class="header-actions">
        <a href="#" class="btn btn-primary-clean">
            <i class="bi bi-plus-circle"></i> Ação Principal
        </a>
        <a href="#" class="btn btn-secondary-clean">
            <i class="bi bi-icon"></i> Ação Secundária
        </a>
    </div>
</div>
```

**Características:**
- Subtítulo categórico em maiúsculas
- Título principal com ícone descritivo
- Botões de ação alinhados à direita
- Responsive: botões empilham em mobile

---

### Cards de Estatísticas

```html
<div class="row g-4 mb-4">
    <div class="col-lg-4 col-md-6">
        <div class="stats-card-clean stats-card-primary h-100">
            <div class="stats-icon-clean stats-icon-primary">
                <i class="bi bi-icon"></i>
            </div>
            <p class="stats-label-clean">Título da Métrica</p>
            <h3 class="stats-value-clean">100</h3>
            <p class="stats-subtitle-clean">Descrição adicional</p>
        </div>
    </div>
</div>
```

**Variações de cores:**
- `stats-card-primary` / `stats-icon-primary` (Azul)
- `stats-card-teal` / `stats-icon-teal` (Verde-azulado)
- `stats-card-purple` / `stats-icon-purple` (Roxo)
- `stats-card-green` / `stats-icon-green` (Verde)
- `stats-card-orange` / `stats-icon-orange` (Laranja)

---

### Tabelas Responsivas

```html
<div class="card shadow-sm border-0" style="border-radius: 12px;">
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                    <tr>
                        <th class="border-0 text-uppercase small fw-semibold text-muted ps-4">
                            Coluna
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="ps-4">Conteúdo</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
```

**Boas práticas:**
- Adicionar `caption` com `visually-hidden` para acessibilidade
- Usar `scope` em cabeçalhos (`<th scope="col">`)
- Padding horizontal: 1rem (16px) mínimo
- Hover suave: `rgba(0, 123, 255, 0.03)`

---

## 🎬 Padrões de Ação

### Botões de Ação (Button Groups)

```html
<div class="btn-group btn-group-sm" role="group">
    <a href="#" class="btn btn-outline-primary" 
       title="Ver Detalhes" 
       aria-label="Ver detalhes de [Nome]">
        <i class="bi bi-eye"></i>
    </a>
    <a href="#" class="btn btn-outline-warning" 
       title="Editar" 
       aria-label="Editar [Nome]">
        <i class="bi bi-pencil"></i>
    </a>
</div>
```

**Hierarquia de ações:**
1. **Ver/Detalhes**: `btn-outline-primary` + `bi-eye`
2. **Editar**: `btn-outline-warning` + `bi-pencil`
3. **Ações específicas**: `btn-outline-success` + ícone contextual
4. **Ações administrativas**: Dropdown danger

---

### Dropdown Administrativo (Admin-Only Actions)

```html
{% if current_user.cargo in ['admin', 'super_admin'] %}
<div class="btn-group" role="group">
    <button type="button" class="btn btn-outline-danger dropdown-toggle" 
            data-bs-toggle="dropdown" aria-expanded="false" 
            title="Ações Administrativas" 
            aria-label="Menu de ações para [Nome]">
        <i class="bi bi-three-dots-vertical"></i>
    </button>
    <ul class="dropdown-menu dropdown-menu-end">
        <li><h6 class="dropdown-header">Ações Administrativas</h6></li>
        <li>
            <button type="button" class="dropdown-item text-warning" 
                    onclick="confirmarInativacao(id, 'nome')">
                <i class="bi bi-slash-circle me-2"></i>Inativar [Tipo]
            </button>
        </li>
        <li><hr class="dropdown-divider"></li>
        <li>
            <button type="button" class="dropdown-item text-danger" 
                    onclick="confirmarExclusao(id, 'nome')">
                <i class="bi bi-trash me-2"></i>Excluir Permanentemente
            </button>
        </li>
    </ul>
</div>
{% endif %}
```

**Requisitos:**
- Controle de acesso via `current_user.cargo`
- Ícone três pontos verticais (`bi-three-dots-vertical`)
- Menu alinhado à direita (`dropdown-menu-end`)
- Cabeçalho descritivo no dropdown
- Separador visual antes de ações destrutivas

---

## 🔔 Modais de Confirmação

### Modal de Inativação (Warning)

```html
<div class="modal fade" id="modalInativar[Tipo]" tabindex="-1" 
     aria-labelledby="modalInativar[Tipo]Label" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header bg-warning text-dark">
                <h5 class="modal-title" id="modalInativar[Tipo]Label">
                    <i class="bi bi-slash-circle me-2"></i>Inativar [Tipo]
                </h5>
                <button type="button" class="btn-close" 
                        data-bs-dismiss="modal" aria-label="Fechar"></button>
            </div>
            <div class="modal-body">
                <p class="mb-3">
                    <i class="bi bi-info-circle text-warning me-2"></i>
                    Você está prestes a inativar [tipo]:
                </p>
                <div class="alert alert-warning mb-3">
                    <strong id="nomeInativar"></strong>
                </div>
                <p class="text-muted small">
                    <i class="bi bi-shield-check me-1"></i>
                    Os dados serão preservados e a ação pode ser revertida.
                </p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" 
                        data-bs-dismiss="modal">
                    <i class="bi bi-x-circle me-1"></i>Cancelar
                </button>
                <form id="formInativar[Tipo]" method="POST" style="display: inline;">
                    <button type="submit" class="btn btn-warning">
                        <i class="bi bi-slash-circle me-1"></i>Confirmar Inativação
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>
```

**Características:**
- Cor amarela (warning) para ação reversível
- Ícone `bi-slash-circle`
- Mensagem tranquilizadora sobre preservação de dados
- Modal centralizado (`modal-dialog-centered`)

---

### Modal de Exclusão Permanente (Danger)

```html
<div class="modal fade" id="modalExcluir[Tipo]" tabindex="-1" 
     aria-labelledby="modalExcluir[Tipo]Label" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-danger">
            <div class="modal-header bg-danger text-white">
                <h5 class="modal-title" id="modalExcluir[Tipo]Label">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    Excluir [Tipo] Permanentemente
                </h5>
                <button type="button" class="btn-close btn-close-white" 
                        data-bs-dismiss="modal" aria-label="Fechar"></button>
            </div>
            <div class="modal-body">
                <div class="alert alert-danger mb-3">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i>
                    <strong>ATENÇÃO: Esta ação é IRREVERSÍVEL!</strong>
                </div>
                <p class="mb-3">Você está prestes a excluir permanentemente:</p>
                <div class="alert alert-danger mb-3">
                    <strong id="nomeExcluir"></strong>
                </div>
                <div class="card bg-light border-danger mb-3">
                    <div class="card-body">
                        <h6 class="card-title text-danger">
                            <i class="bi bi-trash me-2"></i>Dados que serão excluídos:
                        </h6>
                        <ul class="mb-0 small">
                            <li>Todas as informações cadastrais</li>
                            <li>Histórico completo de transações</li>
                            <li>Dados relacionados (especificar)</li>
                            <li>Esta operação NÃO pode ser desfeita</li>
                        </ul>
                    </div>
                </div>
                <p class="text-danger small mb-0">
                    <i class="bi bi-info-circle me-1"></i>
                    <strong>Recomendação:</strong> Considere usar "Inativar" ao invés.
                </p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" 
                        data-bs-dismiss="modal">
                    <i class="bi bi-x-circle me-1"></i>Cancelar
                </button>
                <form id="formExcluir[Tipo]" method="POST" style="display: inline;">
                    <button type="submit" class="btn btn-danger">
                        <i class="bi bi-trash me-1"></i>Confirmar Exclusão Permanente
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>
```

**Características:**
- Cor vermelha (danger) com borda vermelha
- Alerta destacado "IRREVERSÍVEL"
- Lista detalhada de dados que serão perdidos
- Recomendação explícita para usar inativação
- Ícone `bi-exclamation-triangle`

---

## 💻 JavaScript Pattern

### Funções de Confirmação

```javascript
/**
 * Exibe modal de confirmação de inativação
 * @param {number} id - ID do registro
 * @param {string} nome - Nome para exibição
 */
function confirmarInativacao(id, nome) {
    // Atualiza o nome no modal
    document.getElementById('nomeInativar').textContent = nome;
    
    // Define a ação do formulário
    const form = document.getElementById('formInativar[Tipo]');
    form.action = `/[rota]/${id}/inativar`;
    
    // Exibe o modal
    const modal = new bootstrap.Modal(
        document.getElementById('modalInativar[Tipo]')
    );
    modal.show();
}

/**
 * Exibe modal de confirmação de exclusão permanente
 * @param {number} id - ID do registro
 * @param {string} nome - Nome para exibição
 */
function confirmarExclusao(id, nome) {
    // Atualiza o nome no modal
    document.getElementById('nomeExcluir').textContent = nome;
    
    // Define a ação do formulário
    const form = document.getElementById('formExcluir[Tipo]');
    form.action = `/[rota]/${id}/deletar`;
    
    // Exibe o modal
    const modal = new bootstrap.Modal(
        document.getElementById('modalExcluir[Tipo]')
    );
    modal.show();
}
```

**Boas práticas:**
- JSDoc completo para documentação
- Uso de Bootstrap 5 Modal API
- Escape de caracteres no Jinja2: `{{ nome|e }}`
- IDs únicos para evitar conflitos

---

## 🎨 Badges e Status

### Status de Ativação

```html
<!-- Ativo -->
<span class="badge bg-success">
    <i class="bi bi-check-circle-fill"></i> Ativo
</span>

<!-- Inativo -->
<span class="badge bg-secondary">
    <i class="bi bi-x-circle"></i> Inativo
</span>

<!-- Bloqueado -->
<span class="badge bg-danger">
    <i class="bi bi-lock-fill"></i> Bloqueado
</span>
```

### Roles/Cargos

```html
<span class="badge bg-primary">
    <i class="bi bi-shield-fill"></i> Admin
</span>

<span class="badge bg-success">
    <i class="bi bi-person-badge"></i> Supervisor
</span>

<span class="badge bg-info">
    <i class="bi bi-person"></i> Vendedor
</span>

<span class="badge bg-warning text-dark">
    <i class="bi bi-tools"></i> Técnico
</span>
```

---

## 📱 Responsividade

### Classes de Visibilidade

```html
<!-- Ocultar em mobile -->
<td class="d-none d-md-table-cell">Conteúdo</td>

<!-- Ocultar em desktop -->
<div class="d-md-none">Conteúdo mobile</div>

<!-- Empilhar botões em mobile -->
<div class="d-flex flex-column flex-md-row gap-2">
    <button class="btn btn-primary">Ação 1</button>
    <button class="btn btn-secondary">Ação 2</button>
</div>
```

### Grid Adaptativo

```html
<div class="row g-4">
    <div class="col-12 col-md-6 col-lg-4">
        <!-- Coluna: 100% mobile, 50% tablet, 33% desktop -->
    </div>
</div>
```

---

## 🔒 Controle de Acesso

### Verificação no Template

```html
<!-- Admin e Super Admin -->
{% if current_user.cargo in ['admin', 'super_admin'] %}
    <!-- Conteúdo restrito -->
{% endif %}

<!-- Admin, Gerente e Supervisor -->
{% if current_user.cargo in ['admin', 'gerente', 'supervisor'] %}
    <!-- Conteúdo gerencial -->
{% endif %}

<!-- Super Admin apenas -->
{% if current_user.is_super_admin %}
    <!-- Funcionalidades globais -->
{% endif %}
```

### Verificação no Backend

```python
@app.route("/rota/<int:id>/deletar", methods=["POST"])
@login_required
def deletar_registro(id):
    """Deletar registro (admin-only)"""
    # Verificar permissão de cargo
    if current_user.cargo not in ["admin", "super_admin"]:
        flash("Acesso negado! Apenas administradores.", "danger")
        return redirect(url_for("lista"))
    
    # Verificar empresa (não-super_admin)
    registro = Modelo.query.get_or_404(id)
    if not current_user.is_super_admin:
        if registro.empresa_id != current_user.empresa_id:
            flash("Você não pode gerenciar este registro.", "danger")
            return redirect(url_for("lista"))
    
    # Executar ação...
```

---

## 📚 Exemplos Implementados

### Clientes
- **Arquivo**: `templates/clientes/lista.html`
- **Recursos**: Dropdown admin, modais de confirmação
- **Rotas**: `inativar_cliente`, `deletar_cliente`

### Vendedores
- **Arquivo**: `templates/vendedores/lista.html`
- **Recursos**: Dropdown com gerenciamento de login, ações de ativação
- **Rotas**: `desativar_vendedor`, `ativar_vendedor`, `deletar_vendedor`

### Supervisores
- **Arquivo**: `templates/supervisores/lista.html`
- **Recursos**: Botões de ação, modal de desativação
- **Rotas**: `deletar_supervisor`, `definir_senha_supervisor`

---

## ✅ Checklist de Implementação

Ao criar uma nova tela de listagem, verificar:

- [ ] Header Clean Pattern implementado
- [ ] Cards de estatísticas (se aplicável)
- [ ] Tabela responsiva com classes corretas
- [ ] Botões de ação com `aria-label`
- [ ] Dropdown administrativo (se admin-only)
- [ ] Modais de confirmação (inativação + exclusão)
- [ ] Funções JavaScript documentadas
- [ ] Controle de acesso no template e backend
- [ ] Badges de status padronizados
- [ ] Responsividade testada (mobile, tablet, desktop)
- [ ] Acessibilidade validada (teclado + leitor de tela)

---

## 🚀 Melhores Práticas

### Performance
- Usar `data-bs-toggle` para ativação lazy de modals
- Evitar modals múltiplos (1 modal reutilizável por tipo)
- Carregar scripts no final do `<body>`

### SEO e Semântica
- Tags `<caption>` em tabelas (pode usar `visually-hidden`)
- Hierarquia de headings correta (h1 → h2 → h3)
- Links descritivos (`aria-label` quando ícone sozinho)

### Manutenibilidade
- Prefixar classes customizadas (ex: `stats-card-clean`)
- Documentar padrões complexos inline
- Versionar mudanças em `CHANGELOG.md`

---

## 📖 Referências

- **Bootstrap 5.3.3**: https://getbootstrap.com/docs/5.3/
- **Bootstrap Icons**: https://icons.getbootstrap.com/
- **WCAG 2.1**: https://www.w3.org/WAI/WCAG21/quickref/
- **MDN Accessibility**: https://developer.mozilla.org/en-US/docs/Web/Accessibility

---

*Última atualização: 03/01/2026*
*Versão: 1.0.0*
