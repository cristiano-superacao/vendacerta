# ✅ MELHORIAS NA IMPORTAÇÃO DE CLIENTES

## 📋 Mudanças Implementadas

### 1. ⚙️ Vendedor Opcional na Importação

Agora há **3 modos de atribuição de vendedor**:

#### 🎯 Modo 1: Pegar da Planilha (Padrão)
- A planilha deve ter uma coluna "Vendedor"
- Aceita **nome** ou **ID** do vendedor
- Busca automática no banco de dados
- Se não encontrar, cliente fica sem vendedor

#### ⏱️ Modo 2: Atribuir Depois
- Clientes importados **sem vendedor**
- Pode atribuir manualmente depois
- Ideal para importação rápida

#### 👤 Modo 3: Vendedor Fixo
- Todos os clientes vão para um vendedor específico
- Seleção obrigatória no dropdown

---

### 2. 🔢 Código Único Automático

Cada cliente recebe um código no formato: **0001-0001**

#### Estrutura do Código:
- **4 primeiros dígitos**: Código do município (hash do nome)
- **4 últimos dígitos**: Sequência no município
- **Formato**: `XXXX-YYYY`

#### Exemplos:
```
Salvador:     3456-0001, 3456-0002, 3456-0003...
Feira:        7891-0001, 7891-0002, 7891-0003...
SEM_CIDADE:   1234-0001, 1234-0002, 1234-0003...
```

#### Características:
- ✅ **Único** - Não se repete
- ✅ **Automático** - Gerado no cadastro/importação
- ✅ **Indexado** - Busca rápida
- ✅ **Por Município** - Agrupa clientes da mesma cidade

---

## 📂 Arquivos Modificados

### 1. `models.py`
**Mudanças:**
- Adicionado campo `codigo_cliente VARCHAR(9) UNIQUE`
- Adicionado index em `codigo_cliente`
- `vendedor_id` agora permite NULL
- Adicionado método estático `gerar_codigo_cliente()`

### 2. `templates/clientes/importar.html`
**Mudanças:**
- 3 opções de radio buttons para modo de vendedor
- Select de vendedor aparece apenas se "Modo Fixo"
- JavaScript para controlar exibição do select
- Dicas atualizadas com informações sobre código único e vendedor

### 3. `app.py`
**Mudanças:**
- Rota `importar_clientes()`: Lógica para 3 modos de vendedor
- Suporte a coluna "Vendedor" na planilha (nome ou ID)
- Geração automática de `codigo_cliente`
- Rota `novo_cliente()`: Gera código único
- Busca de vendedor por nome na planilha (case-insensitive)

### 4. `migrar_codigo_cliente.py` (NOVO)
**Função:**
- Adiciona coluna `codigo_cliente` no banco
- Gera códigos para clientes existentes
- Estatísticas por município

---

## 🧪 Como Testar

### 1. Migrar Banco de Dados
```bash
python migrar_codigo_cliente.py
```

### 2. Acessar Importação
```
http://127.0.0.1:5001/clientes/importar
```

### 3. Testar os 3 Modos

#### **Modo 1: Planilha**
1. Criar Excel com coluna "Vendedor"
2. Colocar nomes: "João Silva", "Maria Santos"
3. Importar e verificar atribuição automática

#### **Modo 2: Depois**
1. Selecionar "Atribuir depois"
2. Importar planilha
3. Clientes ficam sem vendedor
4. Editar manualmente e atribuir

#### **Modo 3: Fixo**
1. Selecionar "Vendedor específico"
2. Escolher vendedor no dropdown
3. Todos os clientes vão para ele

### 4. Verificar Códigos Únicos
- Listar clientes
- Ver coluna "Código"
- Filtrar por município
- Sequência crescente: 0001, 0002, 0003...

---

## 📊 Estrutura da Planilha

### Formato Simples (com vendedor opcional):
```
| Nome            | CPF/CNPJ       | Telefone       | Email           | Cidade    | Vendedor     |
|-----------------|----------------|----------------|-----------------|-----------|--------------|
| João Silva      | 123.456.789-00 | (71) 99999-9999| joao@email.com  | Salvador  | Maria Santos |
| Empresa ABC     | 12.345.678/0001-99 | (71) 3333-4444 | abc@empresa.com | Feira     | 1            |
```

### Colunas Suportadas:
- **Nome** (obrigatório)
- **CPF/CNPJ** ou **CPF** e **CNPJ** separados
- **Vendedor** (opcional - nome ou ID)
- **Telefone**, **Fone(1)**, **Fone(2)**, **Cel(1)**
- **Email**, **Cidade**, **Bairro**, **CEP**
- **Razão Social**, **Sigla**, **Inscrição Estadual**
- **Coordenada X**, **Coordenada Y**, **Código BP**
- **Formas de Pagamento**, **Dia de Visita**, **Observações**

---

## 🎨 Layout Responsivo

### Mobile (< 768px):
- Radio buttons empilhados
- Select full-width
- Cards em coluna única

### Tablet (768-992px):
- Radio buttons 2 colunas
- Select 100% width
- Cards lado a lado

### Desktop (> 992px):
- Radio buttons 3 colunas
- Select 50% width
- Layout completo

---

## 🔒 Validações

### Importação:
✅ Nome obrigatório
✅ CPF/CNPJ único por empresa
✅ Vendedor existe e está ativo
✅ Município para gerar código
✅ Código único não duplicado

### Código Único:
✅ Formato XXXX-XXXX
✅ 4 primeiros = hash município
✅ 4 últimos = sequência
✅ Index para busca rápida
✅ Gerado automaticamente

---

## 📝 Mensagens ao Usuário

### Sucesso:
```
✅ 50 cliente(s) importado(s) com sucesso!
   Códigos gerados: 0001-0001 até 0001-0050
```

### Avisos:
```
⚠️ 5 clientes sem vendedor na planilha (atribua manualmente)
⚠️ 2 CPF/CNPJ duplicados (ignorados)
```

### Erros:
```
❌ Linha 15: Nome obrigatório
❌ Linha 23: CPF já cadastrado
❌ Vendedor "José Santos" não encontrado
```

---

## 🚀 Próximos Passos

1. ✅ Testar importação local
2. ⏳ Validar códigos gerados
3. ⏳ Testar edição de clientes
4. ⏳ Verificar listagem com códigos
5. ⏳ Deploy Railway

---

**Data:** 17 de dezembro de 2025
**Status:** ✅ IMPLEMENTADO
**Layout:** ✅ RESPONSIVO E PROFISSIONAL
