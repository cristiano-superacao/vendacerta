# ============================================================================
# INSTRUÇÕES DE INTEGRAÇÃO - SISTEMA DE ESTOQUE E PERMISSÕES GRANULARES
# ============================================================================

## RESUMO DO QUE FOI CRIADO

### 1. BANCO DE DADOS - ✅ CONCLUÍDO
- ✅ 21 colunas de permissões adicionadas à tabela usuarios
- ✅ 4 campos novos em produtos: codigo_barra, referencia, ncm, fornecedor
- ✅ Índices criados para busca otimizada
- ✅ Permissões padrão configuradas por cargo

### 2. FORMULÁRIOS - ✅ CONCLUÍDO
- ✅ ProdutoForm: Atualizado com 19 campos (código, nome, código de barras, referência, NCM, fornecedor, etc)
- ✅ UsuarioPermissoesForm: 26 checkboxes organizados por módulo
- ✅ EstoqueMovimentoForm: Para entrada/saída de produtos
- ✅ OrdemServicoForm: Para criar OS
- ✅ AprovarOSForm: Para supervisor aprovar OS
- ✅ AtualizarOSForm: Para técnico atualizar status

### 3. ROTAS DE ESTOQUE - ⚠️ CRIADO (precisa integrar ao app.py)
Arquivo criado: rotas_estoque.txt

ROTAS PRONTAS PARA INTEGRAR:
- /estoque - Dashboard com estatísticas
- /estoque/produtos - Lista de produtos com filtros
- /estoque/produto/novo - Cadastrar produto
- /estoque/produto/<id> - Visualizar produto
- /estoque/produto/<id>/editar - Editar produto
- /estoque/movimentacao/nova - Registrar entrada/saída
- /estoque/movimentacoes - Histórico de movimentações

### 4. TEMPLATES CRIADOS - ✅ CONCLUÍDO
- ✅ templates/estoque/dashboard.html - Dashboard com cards de estatísticas
- ✅ templates/estoque/produtos.html - Lista com todos os campos da imagem
- ✅ templates/estoque/produto_form.html - Formulário completo de produto

### 5. PENDENTE - ❌ NÃO CRIADO AINDA
- ❌ templates/estoque/produto_visualizar.html
- ❌ templates/estoque/movimentacao_form.html
- ❌ templates/estoque/movimentacoes.html
- ❌ Rotas de Ordens de Serviço (já criadas na FASE 1, precisa revisar)
- ❌ Sistema de permissões granulares nas rotas
- ❌ Menu atualizado no base.html para mostrar "ESTOQUE"

## ============================================================================
## PRÓXIMOS PASSOS PARA VOCÊ
## ============================================================================

### PASSO 1: Integrar as rotas ao app.py
1. Abra o arquivo `rotas_estoque.txt`
2. Copie todo o conteúdo
3. Cole no `app.py` após as rotas existentes (antes do final do arquivo)

### PASSO 2: Atualizar o base.html com menu de Estoque
Adicionar no menu principal:
```html
<!-- ESTOQUE -->
{% if current_user.pode_acessar_estoque or current_user.cargo == 'admin' %}
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" id="estoqueDropdown" role="button" 
       data-bs-toggle="dropdown">
        <i class="fas fa-boxes"></i> ESTOQUE
    </a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="{{ url_for('lista_estoque') }}">
            <i class="fas fa-chart-line"></i> Dashboard
        </a></li>
        <li><a class="dropdown-item" href="{{ url_for('lista_produtos') }}">
            <i class="fas fa-list"></i> Produtos
        </a></li>
        {% if current_user.pode_movimentar_estoque or current_user.cargo == 'admin' %}
        <li><a class="dropdown-item" href="{{ url_for('lista_movimentacoes') }}">
            <i class="fas fa-exchange-alt"></i> Movimentações
        </a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="{{ url_for('nova_movimentacao') }}">
            <i class="fas fa-plus"></i> Nova Movimentação
        </a></li>
        {% endif %}
        {% if current_user.pode_gerenciar_produtos or current_user.cargo == 'admin' %}
        <li><a class="dropdown-item" href="{{ url_for('novo_produto') }}">
            <i class="fas fa-box"></i> Novo Produto
        </a></li>
        {% endif %}
    </ul>
</li>
{% endif %}
```

### PASSO 3: Importar os forms no app.py
Adicione no início do app.py:
```python
from forms import (
    # ... imports existentes ...
    EstoqueMovimentoForm,
    OrdemServicoForm,
    AprovarOSForm,
    AtualizarOSForm
)
```

### PASSO 4: Testar o sistema
1. Rode o servidor: `python app.py`
2. Faça login como admin
3. Acesse /estoque para ver o dashboard
4. Teste cadastro de produto
5. Teste movimentação de estoque
6. Verifique se as permissões funcionam (logue como técnico/administrativo)

## ============================================================================
## VERIFICAÇÕES DE SEGURANÇA
## ============================================================================

### Permissões implementadas:
✅ pode_acessar_estoque - Controla acesso ao módulo
✅ pode_gerenciar_produtos - Controla criar/editar produtos
✅ pode_movimentar_estoque - Controla entrada/saída
✅ pode_ver_custos - Controla visualização de valores
✅ pode_ajustar_estoque - Controla ajustes manuais

### Validações nas rotas:
- Todas as rotas verificam current_user.pode_acessar_estoque
- Cadastro/edição verifica pode_gerenciar_produtos
- Movimentações verifica pode_movimentar_estoque
- Exibição de custos verifica pode_ver_custos
- Admin sempre tem acesso total (cargo == 'admin')

## ============================================================================
## CAMPOS DA IMAGEM IMPLEMENTADOS
## ============================================================================

✅ Código - Campo principal de identificação
✅ Nome - Nome do produto
✅ Referência - Referência do fabricante
✅ Código de Barra - EAN/UPC para scanner
✅ NCM - Código fiscal brasileiro
✅ Data Hora - Automático em movimentações
✅ qte entrada - Registrado via EstoqueMovimento tipo='entrada'
✅ qte saída - Registrado via EstoqueMovimento tipo='saida'
✅ O.S - Campo ordem_servico_id relaciona com OS
✅ Administrativo - Mostrado via movimentacao.usuario
✅ Tecnico - Mostrado via OS.tecnico
✅ Vendedor - Pode ser adicionado em movimentações
✅ Supervisor - Mostrado via OS.aprovado_por
✅ Gerente - Campo hierarquia_id no usuario
✅ Status - Campo ativo no produto
✅ Agendamento - Pode ser adicionado em OS

## ============================================================================
## SISTEMA DE PERMISSÕES - 26 PERMISSÕES GRANULARES
## ============================================================================

### GERAIS (3)
- pode_ver_dashboard
- pode_enviar_mensagens
- pode_exportar_dados

### VENDAS (6)
- pode_acessar_vendedores
- pode_gerenciar_metas
- pode_gerenciar_equipes
- pode_gerenciar_comissoes
- pode_ver_todas_metas
- pode_aprovar_comissoes

### CLIENTES (5)
- pode_acessar_clientes
- pode_criar_clientes
- pode_editar_clientes
- pode_excluir_clientes
- pode_importar_clientes

### ORDENS DE SERVIÇO (5)
- pode_acessar_os
- pode_criar_os
- pode_aprovar_os
- pode_atualizar_os
- pode_cancelar_os

### ESTOQUE (5)
- pode_acessar_estoque
- pode_gerenciar_produtos
- pode_movimentar_estoque
- pode_ver_custos
- pode_ajustar_estoque

### TÉCNICOS (2)
- pode_gerenciar_tecnicos
- pode_atribuir_tecnicos

## ============================================================================
## CONFIGURAÇÃO POR CARGO (AUTO-CONFIGURADO)
## ============================================================================

### ADMIN
- Todas as permissões = 1

### SUPERVISOR_MANUTENCAO
- Todas permissões de OS = 1
- Todas permissões de Estoque = 1
- Gerenciar e atribuir técnicos = 1

### ADMINISTRATIVO
- Acessar/criar/editar clientes = 1
- Criar OS = 1
- Acessar estoque (somente visualização)

### TECNICO
- Atualizar OS = 1
- Acessar estoque (somente visualização)

### VENDEDOR
- Todas permissões de Vendas = 1
- Ver dashboard = 1
- Acessar clientes = 1

## ============================================================================
## ARQUIVO DE MIGRAÇÃO
## ============================================================================

Arquivo: migrar_permissoes_granulares.py

JÁ EXECUTADO COM SUCESSO:
- 21 colunas adicionadas
- 3 índices criados (codigo_barra, ncm, referencia)
- Permissões padrão configuradas
- Todos os usuários existentes atualizados

## ============================================================================
## PRÓXIMA FASE - MELHORIAS FUTURAS
## ============================================================================

1. Relatórios de estoque
2. Gráficos de movimentação
3. Alertas de estoque baixo via email
4. Integração com código de barras (scanner)
5. Impressão de etiquetas
6. Inventário físico
7. Curva ABC de produtos
8. Dashboard de custos
9. Importação de produtos via Excel
10. API para integração com outros sistemas
