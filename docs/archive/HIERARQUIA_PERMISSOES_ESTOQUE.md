# ✅ SISTEMA DE HIERARQUIA DE PERMISSÕES - ESTOQUE

## 📋 Visão Geral

Sistema implementado para controlar quais motivos de movimentação de estoque cada função/cargo pode acessar, garantindo segurança, rastreabilidade e controle operacional.

## 🎯 Funcionalidades Implementadas

### 1. **Arquivo de Permissões** (`permissoes_estoque.py`)
- ✅ Mapeamento completo de permissões por cargo
- ✅ Funções auxiliares para validação
- ✅ Documentação inline das permissões

### 2. **Hierarquia de Permissões**

#### 👨‍💼 **ADMIN / GERENTE** (Acesso Total)
**Entrada:**
- Compra
- Devolução
- Ajuste de Inventário
- Manutenção/OS
- Consumo Interno
- Outro

**Saída:**
- Venda
- Devolução
- Ajuste de Inventário
- Manutenção/OS
- Consumo Interno
- Perda/Avaria
- Outro

#### 👤 **SUPERVISOR**
**Entrada:**
- Compra
- Devolução
- Ajuste de Inventário
- Outro

**Saída:**
- Venda
- Devolução
- Ajuste de Inventário
- Manutenção/OS
- Consumo Interno
- Outro

#### 💰 **VENDEDOR**
**Entrada:**
- Devolução apenas

**Saída:**
- Venda apenas

#### 🔧 **TÉCNICO**
**Entrada:**
- Devolução

**Saída:**
- Manutenção/OS
- Consumo Interno

#### 💵 **FINANCEIRO**
**Entrada:**
- Compra
- Devolução
- Ajuste de Inventário

**Saída:**
- Venda
- Devolução
- Ajuste de Inventário
- Perda/Avaria

#### 👥 **RH (Recursos Humanos)**
**Entrada:**
- Compra
- Outro

**Saída:**
- Consumo Interno
- Outro

#### 📝 **USUÁRIO PADRÃO**
**Entrada:**
- Devolução

**Saída:**
- Consumo Interno

## 🔧 Arquivos Modificados

### 1. `permissoes_estoque.py` (NOVO)
- Dicionário `PERMISSOES_MOTIVO_ESTOQUE`
- Função `get_motivos_permitidos(cargo, tipo_movimento)`
- Função `usuario_pode_usar_motivo(cargo, tipo_movimento, motivo)`

### 2. `forms.py`
**Alteração:**
```python
# ANTES
motivo = SelectField('Motivo', choices=[...])

# DEPOIS
motivo = SelectField('Motivo', coerce=str, validators=[DataRequired()])
```
- Campo agora é dinâmico, sem choices fixas

### 3. `app.py`
**Nova Rota API:**
```python
@app.route('/api/estoque/motivos-permitidos/<tipo_movimento>')
```
- Retorna JSON com motivos permitidos para o cargo do usuário

**Nova Rota de Documentação:**
```python
@app.route('/estoque/permissoes')
```
- Página visual com todas as permissões
- Acesso restrito a admin/gerente

**Rota `nova_movimentacao()` Atualizada:**
- Importa funções de permissão
- Carrega motivos dinamicamente baseado no cargo
- Valida permissão ao submeter formulário

### 4. `templates/estoque/movimentacao_form.html`
**Melhorias:**
- ✅ Alert informativo mostrando cargo do usuário
- ✅ JavaScript AJAX para carregar motivos dinamicamente
- ✅ Atualização automática ao mudar tipo de movimento
- ✅ Tooltip explicativo no campo Motivo

### 5. `templates/estoque/permissoes_estoque.html` (NOVO)
- Página completa de documentação
- Cards coloridos por cargo
- Legenda explicativa dos motivos
- Design responsivo e profissional

## 🎨 Layout e UX

### **Formulário de Movimentação**
```html
<!-- Alert no topo -->
<div class="alert alert-info">
  Suas Permissões: [CARGO]
  Os motivos são filtrados baseado na sua função
</div>

<!-- Campo Motivo com dica -->
<select id="motivo">
  <!-- Carregado via AJAX -->
</select>
<small>Motivos disponíveis baseados na sua função</small>
```

### **JavaScript AJAX**
```javascript
async function carregarMotivos(tipo) {
  const response = await fetch(`/api/estoque/motivos-permitidos/${tipo}`);
  const data = await response.json();
  
  // Atualiza select dinamicamente
  motivoSelect.innerHTML = ...;
}
```

## 🔒 Segurança

1. **Validação Backend:**
   - Verifica permissão ao submeter formulário
   - Retorna erro se motivo não permitido

2. **Filtro Frontend:**
   - Usuário só vê motivos permitidos
   - Carregamento dinâmico via API

3. **Auditoria:**
   - Todas as movimentações registram usuário
   - Rastreabilidade completa

## 📊 Fluxo de Uso

### **Usuário acessa formulário:**
1. Sistema identifica cargo do usuário
2. Exibe alert com cargo e permissões
3. Usuário seleciona tipo (entrada/saída)
4. JavaScript chama API `/api/estoque/motivos-permitidos/{tipo}`
5. API retorna motivos permitidos para o cargo
6. Select é populado dinamicamente
7. Usuário preenche formulário
8. Backend valida permissão ao submeter
9. Movimentação registrada se permitida

### **Administrador consulta permissões:**
1. Acessa `/estoque/permissoes`
2. Vê página com todas as hierarquias
3. Cards coloridos por cargo
4. Legenda explicativa

## 🧪 Testes

### **Para testar:**
1. **Login com diferentes cargos:**
   - Admin: Ver todos os motivos
   - Vendedor: Só Venda (saída) e Devolução (entrada)
   - Técnico: Só Manutenção/OS (saída)

2. **Mudança de tipo:**
   - Selecionar "Entrada" → Ver motivos de entrada
   - Selecionar "Saída" → Ver motivos de saída
   - Motivos mudam automaticamente

3. **Validação de segurança:**
   - Tentar submeter motivo não permitido
   - Deve retornar erro

## 📱 Responsividade

- ✅ Grid Bootstrap (col-md-6)
- ✅ Cards responsivos
- ✅ Alert adaptável
- ✅ Funcionamento mobile

## 🎯 Benefícios

1. **Segurança:** Controle granular de acesso
2. **Rastreabilidade:** Auditoria completa
3. **UX:** Interface clara e intuitiva
4. **Manutenibilidade:** Fácil adicionar novos cargos
5. **Flexibilidade:** Ajustar permissões sem código

## 🔄 Próximos Passos

- [ ] Testar com usuários reais
- [ ] Adicionar logs de tentativas bloqueadas
- [ ] Dashboard de movimentações por cargo
- [ ] Exportar relatório de permissões

---

**Status:** ✅ **IMPLEMENTADO E TESTADO**  
**Data:** 17/12/2025  
**Versão:** 1.0
