# 📘 Guia Rápido de Uso - Sistema de Clientes

## 🚀 Início Rápido

Este guia ensina como usar o sistema de clientes de forma prática e objetiva.

---

## 📋 Índice

1. [Acessando o Sistema](#1-acessando-o-sistema)
2. [Cadastrando um Novo Cliente](#2-cadastrando-um-novo-cliente)
3. [Visualizando Cliente](#3-visualizando-cliente)
4. [Registrando uma Compra](#4-registrando-uma-compra)
5. [Editando Cliente](#5-editando-cliente)
6. [Importando Clientes via Excel](#6-importando-clientes-via-excel)
7. [Exportando Clientes para Excel](#7-exportando-clientes-para-excel)
8. [Gerando Relatório de Vendas](#8-gerando-relatório-de-vendas)
9. [Entendendo os Status](#9-entendendo-os-status)
10. [Dicas e Atalhos](#10-dicas-e-atalhos)

---

## 1. Acessando o Sistema

### Como acessar a lista de clientes:

**Opção 1: Menu Lateral**
1. No menu lateral esquerdo, procure a seção **"METAS"**
2. Clique em **"📋 Clientes"**

**Opção 2: URL Direta**
- Digite na barra de endereço: `/clientes`

### O que você verá:

```
┌─────────────────────────────────────────────┐
│           📊 Cards de Estatísticas          │
│  Total | Positivados | Atenção | Sem Compras│
├─────────────────────────────────────────────┤
│          🔍 Campo de Busca                  │
├─────────────────────────────────────────────┤
│       📋 Tabela de Clientes                 │
│  Nome | CPF/CNPJ | Cidade | Status | Ações  │
└─────────────────────────────────────────────┘
```

---

## 2. Cadastrando um Novo Cliente

### Passo a Passo:

**1. Iniciar cadastro**
- Na tela de lista de clientes, clique no botão verde **"✚ Novo Cliente"**

**2. Preencher Dados Básicos**
- **Nome:** Nome completo do cliente
- **Email:** Email para contato (opcional)
- **Telefone:** Telefone com máscara automática `(XX) XXXXX-XXXX`

**3. Escolher CPF ou CNPJ**
- Selecione o tipo de documento:
  - ⚪ **CPF** (pessoa física)
  - ⚪ **CNPJ** (pessoa jurídica)
- Digite o número (máscara aplicada automaticamente)

**4. Endereço**
- **Bairro:** Bairro do cliente
- **Cidade:** Cidade do cliente
- **Estado:** Selecione o estado (UF)
- **CEP:** CEP com máscara `XXXXX-XXX` (opcional)

**5. Formas de Pagamento**
- Marque **pelo menos uma** opção:
  - ☐ Dinheiro
  - ☐ PIX
  - ☐ Cartão Débito
  - ☐ Cartão Crédito
  - ☐ Boleto
  - ☐ Transferência

**6. Salvar**
- Clique no botão verde **"💾 Salvar Cliente"**
- Você será redirecionado para a página de visualização do cliente

### ⚠️ Validações Automáticas:

- ❌ CPF/CNPJ já cadastrado → Erro
- ❌ Campos obrigatórios vazios → Erro
- ❌ Email inválido → Erro
- ✅ Tudo OK → Cliente cadastrado!

---

## 3. Visualizando Cliente

### Como acessar:

**Opção 1: Da lista**
- Na tabela de clientes, clique no nome do cliente OU
- Clique no botão **"👁️ Ver"**

### O que você verá:

```
┌─────────────────────────────────────────────┐
│  👤 [Nome do Cliente]                       │
│  Status: 🟢 Positivado                      │
│                                             │
│  ┌────────────────┐  ┌──────────────────┐  │
│  │ Dados          │  │ Histórico de     │  │
│  │ Cadastrais     │  │ Compras          │  │
│  └────────────────┘  └──────────────────┘  │
│                                             │
│  [✏️ Editar] [🛒 Nova Compra] [🗑️ Deletar] │
└─────────────────────────────────────────────┘
```

### Informações exibidas:

**Dados Cadastrais:**
- CPF ou CNPJ
- Telefone
- Email
- Endereço completo
- Formas de pagamento aceitas

**Estatísticas:**
- Total de compras
- Valor total comprado
- Última compra (data)
- Compras no mês atual

**Histórico de Compras:**
- Lista de todas as compras
- Data, valor, forma de pagamento
- Ordenadas da mais recente para a mais antiga

---

## 4. Registrando uma Compra

### Passo a Passo:

**1. Acessar registro de compra**
- Na visualização do cliente, clique em **"🛒 Nova Compra"** OU
- Na lista de clientes, clique em **"🛒 Compra"** na linha do cliente

**2. Preencher dados da compra**
- **Valor:** Digite o valor da compra (R$)
  - Exemplo: `150.00` ou `150,00`
  - Mínimo: R$ 0,01
- **Forma de Pagamento:** Selecione uma das formas aceitas pelo cliente
  - Opções são limitadas às formas cadastradas no cliente
- **Observações:** Informações adicionais (opcional)
  - Exemplo: "Primeira compra do mês", "Pedido especial"

**3. Verificar limite**
- O sistema mostra automaticamente:
  - ✅ **Compras no mês:** X compras
  - ✅ **Pode comprar?** Sim/Não
- ⚠️ Se o cliente atingiu o limite, você será avisado

**4. Salvar**
- Clique em **"✅ Registrar Compra"**
- Volta para a visualização do cliente
- Compra aparece no histórico
- Status atualizado automaticamente

### 📊 O que é atualizado:

- ✅ Data da última compra → Data atual
- ✅ Total de compras → +1
- ✅ Valor total → Soma o valor da nova compra
- ✅ Status → Recalculado (pode mudar para 🟢 Verde)

---

## 5. Editando Cliente

### Passo a Passo:

**1. Acessar edição**
- Na visualização do cliente, clique em **"✏️ Editar Dados"** OU
- Na lista de clientes, clique em **"✏️ Editar"**

**2. Modificar dados**
- O formulário é idêntico ao de cadastro
- Todos os campos já vêm preenchidos
- Altere apenas o que precisa

**3. Salvar alterações**
- Clique em **"💾 Salvar Alterações"**
- Volta para a visualização do cliente
- Mensagem de sucesso exibida

### ⚠️ Atenção:

- ❌ Não é possível alterar CPF/CNPJ se já houver compras
- ✅ Outros campos podem ser alterados livremente

---

## 6. Importando Clientes via Excel

### Passo a Passo:

**1. Baixar modelo**
- Na lista de clientes, clique em **"☁️ Importar Excel"**
- Clique em **"📥 Baixar Modelo de Importação"**
- Um arquivo Excel será baixado: `modelo_importacao_clientes.xlsx`

**2. Preencher planilha**
- Abra o arquivo no Excel ou LibreOffice
- Colunas disponíveis:
  1. **Nome** (obrigatório)
  2. **CPF** (obrigatório se não tiver CNPJ)
  3. **CNPJ** (obrigatório se não tiver CPF)
  4. **Email** (opcional)
  5. **Telefone** (opcional)
  6. **Bairro** (opcional)
  7. **Cidade** (opcional)
  8. **Estado** (opcional)
  9. **CEP** (opcional)
  10. **Formas de Pagamento** (opcional)
      - Formato: `dinheiro,pix,cartao_debito`

**Exemplo de linha:**
```
Nome: João da Silva
CPF: 123.456.789-00
Email: joao@email.com
Telefone: (71) 99999-9999
Bairro: Centro
Cidade: Salvador
Estado: BA
CEP: 40000-000
Formas Pagamento: dinheiro,pix
```

**3. Fazer upload**
- Volte para a página de importação
- Clique em **"Escolher arquivo"**
- Selecione seu arquivo preenchido
- Clique em **"📤 Enviar Arquivo"**

**4. Aguardar validação**
- O sistema valida automaticamente:
  - ✅ CPF/CNPJ únicos (não duplicados)
  - ✅ Campos obrigatórios preenchidos
  - ✅ Formatos corretos

**5. Resultado**
- ✅ **Sucesso:** "X clientes importados com sucesso!"
- ❌ **Erro:** Mensagens detalhadas do que precisa corrigir

### 💡 Dicas:

- 📝 Mantenha o cabeçalho da planilha (primeira linha)
- 📝 Não altere os nomes das colunas
- 📝 CPF com ou sem máscara (ambos aceitos)
- 📝 CNPJ com ou sem máscara (ambos aceitos)

---

## 7. Exportando Clientes para Excel

### Passo a Passo:

**1. Acessar exportação**
- Na lista de clientes, clique em **"📊 Exportar Excel"**

**2. Download automático**
- Um arquivo Excel será baixado automaticamente
- Nome do arquivo: `clientes_export_AAAAMMDD_HHMMSS.xlsx`
- Exemplo: `clientes_export_20251215_143022.xlsx`

### 📄 O que é exportado:

**Colunas do arquivo:**
1. ID
2. CPF
3. CNPJ
4. Nome
5. Email
6. Telefone
7. Bairro
8. Cidade
9. Estado
10. CEP
11. Formas de Pagamento
12. Data Última Compra
13. Total de Compras

### ✨ Formatação:

- ✅ Cabeçalho em **negrito**
- ✅ Bordas em todas as células
- ✅ Colunas ajustadas automaticamente
- ✅ Pronto para impressão ou análise

---

## 8. Gerando Relatório de Vendas

### Como acessar:

**Opção 1: Menu Lateral**
- Clique em **"📊 Relatório de Vendas"**

**Opção 2: Da lista de clientes**
- Clique em **"📊 Relatório"** (no rodapé)

### Filtros Disponíveis:

**1. Ano**
- Selecione o ano desejado (2020-2029)
- Padrão: Ano atual

**2. Status**
- Todos
- 🟢 Positivado
- 🟡 Atenção
- 🔴 Sem Compras

**3. Vendedor**
- Selecione um vendedor específico
- Padrão: Todos os vendedores

**4. Supervisor**
- Selecione um supervisor específico
- Padrão: Todos os supervisores

**5. Cidade**
- Digite o nome da cidade
- Autocomplete com cidades cadastradas

**6. Bairro**
- Digite o nome do bairro
- Autocomplete com bairros cadastrados

**7. Forma de Pagamento**
- Filtre por forma de pagamento específica

### Passo a Passo:

**1. Aplicar filtros**
- Selecione os filtros desejados
- Clique em **"🔍 Buscar"**

**2. Visualizar resultados**
- Tabela atualizada com os filtros aplicados
- Cards de resumo no topo:
  - Total de Clientes
  - Total de Compras
  - Valor Total

**3. Exportar (opcional)**
- Clique em **"📊 Exportar Excel"**
- Arquivo baixado com os dados filtrados

**4. Imprimir (opcional)**
- Clique em **"🖨️ Imprimir"**
- Janela de impressão do navegador aberta

**5. Limpar filtros**
- Clique em **"🔄 Limpar Filtros"**
- Volta para visualização sem filtros

---

## 9. Entendendo os Status

### 🟢 Verde - Positivado

**Significa:**
- Cliente comprou nos **últimos 30 dias**
- Está ativo e comprando regularmente

**Indicadores:**
- Badge verde
- Ícone: ✅ ou 🟢
- Texto: "Cliente Positivado"

**Ação sugerida:**
- ✅ Manter o bom relacionamento
- ✅ Oferecer novos produtos

---

### 🟡 Amarelo - Atenção

**Significa:**
- Cliente está entre **30 e 38 dias** sem comprar
- Pode estar perdendo o interesse

**Indicadores:**
- Badge amarelo
- Ícone: ⚠️ ou 🟡
- Texto: "Atenção Necessária"

**Ação sugerida:**
- 📞 Ligar para o cliente
- 💬 Enviar mensagem de contato
- 🎁 Oferecer promoção especial

---

### 🔴 Vermelho - Sem Compras

**Significa:**
- Cliente está **há mais de 38 dias** sem comprar OU
- Nunca fez nenhuma compra

**Indicadores:**
- Badge vermelho
- Ícone: ❌ ou 🔴
- Texto: "Sem Compras"

**Ação sugerida:**
- 🔔 Visitar o cliente pessoalmente
- 📧 Enviar email de reativação
- 🎯 Criar estratégia de reconquista

---

## 10. Dicas e Atalhos

### ⌨️ Atalhos de Teclado:

- **Buscar na lista:** Comece a digitar no campo de busca (foco automático)
- **Enter no formulário:** Salva o formulário
- **ESC no formulário:** Cancela e volta

### 💡 Dicas de Uso:

**1. Use a busca da lista**
- Filtra instantaneamente por:
  - Nome
  - CPF
  - CNPJ
  - Cidade
  - Bairro

**2. Máscaras automáticas**
- Não se preocupe com formatação
- CPF: `123.456.789-00`
- CNPJ: `12.345.678/0001-00`
- Telefone: `(71) 99999-9999`
- CEP: `40000-000`

**3. Validação em tempo real**
- Campos obrigatórios ficam vermelhos se vazios
- Email é validado automaticamente
- CPF/CNPJ verificam formato

**4. Importação em lote**
- Para cadastrar muitos clientes de uma vez
- Use a importação por Excel
- Muito mais rápido que cadastro manual

**5. Exportação para análise**
- Exporte para Excel
- Abra em ferramentas de análise (Excel, Google Sheets)
- Crie gráficos e dashboards personalizados

**6. Relatórios filtrados**
- Combine múltiplos filtros
- Exemplo: Clientes amarelos + Cidade Salvador
- Priorize ações de vendas

**7. Status como guia de ação**
- 🟢 Verde: Continue o bom trabalho
- 🟡 Amarelo: Atenção imediata
- 🔴 Vermelho: Ação urgente necessária

---

## ❓ Perguntas Frequentes

**P: Posso cadastrar cliente sem CPF e sem CNPJ?**  
R: ❌ Não. É obrigatório ter pelo menos um deles.

**P: O que acontece se eu importar um CPF já cadastrado?**  
R: ❌ O sistema rejeita e mostra erro. CPF e CNPJ devem ser únicos.

**P: Posso deletar um cliente?**  
R: ✅ Sim, mas é um "soft delete" (marcado como inativo, não apagado).

**P: Quantas compras um cliente pode fazer por mês?**  
R: Não há limite rígido. O sistema apenas avisa sobre o total de compras.

**P: Como faço para ver apenas meus clientes?**  
R: Se você é vendedor, vê automaticamente apenas seus clientes.

**P: Posso editar uma compra já registrada?**  
R: ❌ Não. Compras não podem ser editadas após registro (integridade de dados).

**P: O que significam as formas de pagamento no cliente?**  
R: São as formas que o cliente **aceita** receber. Ao registrar compra, escolhe uma delas.

---

## 🎯 Fluxo Ideal de Trabalho

### Para Vendedores:

**Manhã:**
1. Acesse a lista de clientes
2. Filtre por status 🟡 Amarelo
3. Entre em contato com esses clientes
4. Registre compras realizadas

**Durante o dia:**
1. Cadastre novos clientes no ponto de venda
2. Registre compras conforme ocorrem
3. Atualize dados de clientes se necessário

**Final do dia:**
1. Revise clientes 🔴 Vermelhos
2. Planeje ações para reconquista
3. Gere relatório de vendas do dia

---

## 📞 Suporte

**Precisa de ajuda?**

- 📧 Email: suporte@suameta.com
- 📱 WhatsApp: (71) 99337-2960
- 🕐 Horário: Seg-Sex 8h-18h | Sáb 8h-12h

**Encontrou um bug?**
- Relate para a equipe técnica
- Informe: O que você fez + O que esperava + O que aconteceu

---

**✅ Você está pronto para usar o sistema!**

Este guia cobre todos os recursos principais. Use-o como referência sempre que tiver dúvidas.

**Boas vendas! 🚀**
