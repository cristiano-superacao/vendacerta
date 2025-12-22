# 📋 ATUALIZAÇÃO FORMULÁRIO DE CLIENTES

## ✅ Campos Adicionados

### 📌 Identificação
1. **Vendedor** (obrigatório) - SelectField com lista de vendedores ativos
2. **Supervisor** (readonly) - Preenchido automaticamente ao selecionar vendedor
3. **Razão Social** - Nome empresarial completo
4. **Sigla** - Apelido/sigla da empresa
5. **Inscrição Estadual** - IE do cliente

### 📍 Endereço
6. **CEP** - Código postal com máscara 00000-000
7. **Coordenada X** - Longitude GPS
8. **Coordenada Y** - Latitude GPS

### 📞 Contato
9. **Telefone 2 (Fone 2)** - Segundo telefone fixo
10. **Celular (Cel 1)** - Número do celular

### 🔧 Outros
11. **Código BP** - Código do sistema ERP/BP

---

## 🎨 Melhorias de Layout

### ✨ Design Responsivo
- **Grid Adaptativo**: 1 card principal ao invés de múltiplos cards
- **Seções Organizadas**: Divisores visuais entre seções (Endereço, Contato, GPS)
- **Ícones Bootstrap**: Cada campo tem ícone específico
- **Animações**: Hover effects nos checkboxes e botões
- **Máscaras**: CPF, CNPJ, CEP, telefones formatados automaticamente

### 📱 Breakpoints
- **Mobile** (< 768px): Campos em coluna única
- **Tablet** (768-992px): Campos em 2 colunas
- **Desktop** (> 992px): Campos em até 4 colunas

### 🎯 Hierarquia Visual
```
1. Vendedor e Supervisor (linha 1)
2. CPF e CNPJ (linha 2)
3. Sigla e Razão Social (linha 3)
4. IE e Nome (linha 4)
--- Endereço ---
5. Município e Bairro (linha 5)
6. CEP e Ponto de Referência (linha 6)
--- Contato ---
7. Fone(1), Fone(2), Cel(1) (linha 7)
8. Email (linha 8)
--- GPS ---
9. Coordenada X e Y (linha 9)
--- Adicionais ---
10. Código BP e Dia da Visita (linha 10)
11. Formas de Pagamento (grid 3 colunas)
12. Observações (textarea)
13. Status Ativo (switch)
```

---

## 🔄 Funcionalidades JavaScript

### 🎭 Máscaras Aplicadas
```javascript
CPF: 000.000.000-00
CNPJ: 00.000.000/0000-00
CEP: 00000-000
Telefone: (00) 0000-0000 ou (00) 00000-0000
```

### 🔍 AJAX - Busca de Supervisor
Ao selecionar um vendedor:
1. Faz requisição GET para `/api/vendedor/{id}/supervisor`
2. Recebe JSON: `{"supervisor": "Nome do Supervisor"}`
3. Preenche automaticamente o campo "Supervisor" (readonly)

### ✅ Validação Frontend
- Verifica se CPF **OU** CNPJ foi preenchido
- Exibe alerta se nenhum dos dois foi informado
- Animação de loading no botão ao enviar

---

## 📂 Arquivos Modificados

### 1. `forms.py`
**Mudanças:**
- Adicionados 11 novos campos no `ClienteForm`
- Adicionado `vendedor_id` (SelectField)
- Adicionado `supervisor_nome` (readonly)
- Modificado `__init__` para receber `empresa_id` e popular vendedores

**Linhas afetadas:** 293-380

### 2. `templates/clientes/form.html`
**Mudanças:**
- Formulário completamente refeito
- Layout em card único com seções organizadas
- JavaScript para máscaras e busca de supervisor
- CSS customizado para animações

**Arquivo:** Totalmente substituído (backup em `form_old.html`)

### 3. `app.py`
**Mudanças:**
- Rota `novo_cliente()` - Adicionados todos os novos campos
- Rota `editar_cliente()` - Atualização de todos os campos
- Nova rota API: `/api/vendedor/<id>/supervisor`

**Linhas afetadas:** 
- 3825-3875 (novo_cliente)
- 3920-4020 (editar_cliente)
- 5710-5735 (nova API)

---

## 🧪 Como Testar

### 1. Iniciar Servidor
```bash
python app.py
```

### 2. Acessar Formulário
```
http://127.0.0.1:5001/clientes/novo
```

### 3. Testar Campos
1. **Vendedor**: Selecionar da lista
2. **Supervisor**: Deve preencher automaticamente
3. **CPF/CNPJ**: Digitar números (máscara aplica automaticamente)
4. **Telefones**: Digitar números (máscara aplica)
5. **CEP**: Digitar números (máscara aplica)
6. **Coordenadas**: Valores decimais (ex: -38.5014)
7. **Formas de Pagamento**: Selecionar múltiplas opções

### 4. Validar
- ✅ Campos obrigatórios com asterisco vermelho
- ✅ Validação: CPF **OU** CNPJ deve ser preenchido
- ✅ Máscaras aplicadas corretamente
- ✅ Supervisor preenchido automaticamente
- ✅ Layout responsivo em mobile/tablet/desktop

---

## 📊 Comparação Antes vs Depois

### ANTES
- ❌ 9 campos apenas
- ❌ Vendedor não selecionável
- ❌ Sem supervisor
- ❌ Sem razão social
- ❌ Sem coordenadas GPS
- ❌ Apenas 1 telefone
- ❌ Layout básico em cards separados

### DEPOIS
- ✅ 20 campos completos
- ✅ Vendedor selecionável
- ✅ Supervisor automático
- ✅ Razão social + sigla
- ✅ Coordenadas GPS (X/Y)
- ✅ 3 telefones (Fone1, Fone2, Cel1)
- ✅ Layout profissional em card único

---

## 🚀 Próximos Passos

1. ✅ **Testado Localmente** - Verificar máscaras e validações
2. ⏳ **Testar Criação de Cliente** - Inserir dados reais
3. ⏳ **Testar Edição de Cliente** - Carregar cliente existente
4. ⏳ **Verificar Responsividade** - Mobile/Tablet/Desktop
5. ⏳ **Deploy Railway** - Após testes locais OK

---

## 📝 Notas Importantes

### ⚠️ Banco de Dados
Os campos já existem no modelo `Cliente`:
- `razao_social`
- `sigla`
- `inscricao_estadual`
- `codigo_bp`
- `cep`
- `telefone2`
- `celular`
- `coordenada_x`
- `coordenada_y`

**Não é necessária migração!** ✅

### 🔐 Permissões
- Super Admin: Acessa todos os vendedores de todas as empresas
- Admin: Acessa vendedores da sua empresa
- Vendedor: Vê apenas sua própria lista

### 📡 API Endpoint
```
GET /api/vendedor/{vendedor_id}/supervisor
Response: {"vendedor_id": 1, "vendedor_nome": "João", "supervisor": "Maria"}
```

---

**Data:** 17 de dezembro de 2025
**Status:** ✅ IMPLEMENTADO
**Testado:** ⏳ AGUARDANDO TESTES LOCAIS
