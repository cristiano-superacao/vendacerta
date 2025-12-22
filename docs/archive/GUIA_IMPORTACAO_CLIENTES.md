# 📊 Guia de Importação e Exportação de Clientes

## 🎯 Visão Geral

O sistema agora permite importar e exportar dados de clientes via planilhas Excel, facilitando o cadastro em massa e a gestão de informações.

## 📤 Exportação de Clientes

### Como Exportar

1. Acesse o menu **Clientes**
2. Clique no botão **"Exportar Excel"** (ícone verde)
3. O arquivo será baixado automaticamente

### Conteúdo do Arquivo

O arquivo exportado contém:

| Coluna | Descrição |
|--------|-----------|
| ID | Identificador único do cliente |
| Nome | Nome completo do cliente |
| CPF | CPF do cliente |
| CNPJ | CNPJ do cliente (se aplicável) |
| Telefone | Número de contato |
| Email | Endereço de email |
| Cidade | Cidade do cliente |
| Bairro | Bairro do cliente |
| Ponto de Referência | Referência de localização |
| Dia de Visita | Dia da semana para visita |
| Formas de Pagamento | Métodos de pagamento aceitos |
| Observações | Notas adicionais |
| Status | Status atual (VERDE/AMARELO/VERMELHO) |
| Última Compra | Data da última compra |
| Total Compras | Total de compras no mês |
| Ativo | Se o cliente está ativo |
| Vendedor | Nome do vendedor responsável |

### Filtros Aplicados

- **Vendedor**: Vê apenas seus clientes
- **Supervisor**: Vê clientes de sua equipe
- **Admin**: Vê todos os clientes da empresa
- **Super Admin**: Vê todos os clientes do sistema

## 📥 Importação de Clientes

### Como Importar

1. Acesse o menu **Clientes**
2. Clique no botão **"Importar Excel"** (ícone azul)
3. Na página de importação:
   - Baixe um modelo em branco OU
   - Use uma planilha com clientes exportados
4. Preencha os dados na planilha
5. Clique em **"Escolher arquivo"**
6. Selecione a planilha (.xlsx ou .xls)
7. Clique em **"Importar Clientes"**

### Modelos Disponíveis

#### 1. Modelo em Branco
- Planilha vazia com estrutura correta
- Inclui uma linha de exemplo
- Ideal para cadastro de novos clientes

#### 2. Exportação de Clientes Atuais
- Contém todos os clientes já cadastrados
- Útil para edição em massa
- Mantém IDs originais (serão ignorados na importação)

### Estrutura da Planilha

#### Colunas Obrigatórias

| Coluna | Obrigatório | Exemplo |
|--------|-------------|---------|
| Nome | ✅ SIM | João Silva |
| CPF | ❌ Não | 123.456.789-00 |
| CNPJ | ❌ Não | 12.345.678/0001-90 |
| Telefone | ❌ Não | (11) 98765-4321 |
| Email | ❌ Não | joao@email.com |
| Cidade | ❌ Não | São Paulo |
| Bairro | ❌ Não | Centro |
| Ponto de Referência | ❌ Não | Próximo ao mercado |
| Dia de Visita | ❌ Não | segunda |
| Formas de Pagamento | ❌ Não | dinheiro, pix, cartao_credito |
| Observações | ❌ Não | Cliente preferencial |

#### Formas de Pagamento Válidas

- `dinheiro`
- `pix`
- `cartao_debito`
- `cartao_credito`
- `boleto`

**Formato**: Separar por vírgula ou ponto-e-vírgula
**Exemplo**: `dinheiro, pix, cartao_credito`

#### Dias de Visita Válidos

- `segunda`
- `terça`
- `quarta`
- `quinta`
- `sexta`
- `sabado`
- `domingo`

### Validações Aplicadas

1. **Nome Obrigatório**: Todo cliente deve ter nome
2. **CPF Único**: Não pode haver duplicatas de CPF na mesma empresa
3. **CNPJ Único**: Não pode haver duplicatas de CNPJ na mesma empresa
4. **Formatação Automática**: CPF e CNPJ são limpos automaticamente (remove pontos, traços, barras)
5. **Formas de Pagamento**: Apenas valores válidos são aceitos
6. **Vendedor**: Clientes são automaticamente associados ao vendedor logado

### Processo de Importação

```
┌─────────────────────────┐
│  1. Upload do Arquivo   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  2. Validação Inicial   │
│  - Formato do arquivo   │
│  - Colunas obrigatórias │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  3. Processamento       │
│  - Linha por linha      │
│  - Validações de dados  │
│  - Verificação duplic.  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  4. Resultado           │
│  - Clientes importados  │
│  - Lista de erros       │
└─────────────────────────┘
```

### Mensagens de Retorno

#### ✅ Sucesso
```
5 cliente(s) importado(s) com sucesso!
```

#### ⚠️ Avisos (Importação Parcial)
```
5 cliente(s) importado(s) com sucesso!

Erros encontrados:
Linha 3: CPF 12345678900 já cadastrado
Linha 7: Nome obrigatório
Linha 10: CNPJ 12345678000190 já cadastrado
```

#### ❌ Erro Total
```
Erro ao importar arquivo: [descrição do erro]
```

## 📝 Dicas e Boas Práticas

### Antes de Importar

1. ✅ Verifique se os dados estão completos
2. ✅ Remova linhas vazias
3. ✅ Certifique-se que CPF/CNPJ não estão duplicados
4. ✅ Use o modelo fornecido como referência
5. ✅ Teste com poucos registros primeiro

### Durante a Importação

1. 📊 Aguarde o processamento (não feche a página)
2. 📊 Para muitos registros, pode demorar alguns segundos
3. 📊 O sistema mostrará o progresso ao final

### Após a Importação

1. ✔️ Verifique a lista de clientes importados
2. ✔️ Confira os dados de alguns clientes
3. ✔️ Leia a lista de erros (se houver)
4. ✔️ Corrija os erros e reimporte se necessário

### Variações de Nomes de Colunas

O sistema aceita diferentes variações de nomes de colunas:

| Coluna Padrão | Variações Aceitas |
|---------------|-------------------|
| Nome | nome completo, cliente |
| CPF | documento |
| CNPJ | cnpj/cpf |
| Telefone | fone, celular, contato |
| Email | e-mail, e mail |
| Cidade | município, municipio |
| Bairro | região |
| Ponto de Referência | ponto de referencia, referência, referencia |
| Dia de Visita | dia visita, dia |
| Formas de Pagamento | pagamento, formas pagamento |
| Observações | observacoes, obs |

## 🔒 Segurança e Permissões

### Quem Pode Importar

- ✅ **Vendedores**: Podem importar clientes que serão associados a eles
- ❌ **Supervisores**: Não podem importar diretamente
- ❌ **Admins**: Não podem importar diretamente
- ❌ **Super Admins**: Não podem importar diretamente

> **Nota**: Atualmente, apenas vendedores podem realizar importações. Isso garante que cada cliente tenha um vendedor responsável definido.

### Quem Pode Exportar

- ✅ **Vendedores**: Exportam apenas seus clientes
- ✅ **Supervisores**: Exportam clientes de sua equipe
- ✅ **Admins**: Exportam todos os clientes da empresa
- ✅ **Super Admins**: Exportam todos os clientes do sistema

## 📋 Exemplos Práticos

### Exemplo 1: Importação Simples

```excel
Nome            | CPF            | Telefone        | Cidade      | Formas de Pagamento
João Silva      | 123.456.789-00 | (11) 98765-4321| São Paulo   | dinheiro, pix
Maria Santos    | 987.654.321-00 | (11) 91234-5678| São Paulo   | pix, cartao_credito
```

### Exemplo 2: Importação Completa

```excel
Nome         | CPF            | CNPJ              | Telefone        | Email          | Cidade    | Bairro | Ponto de Referência | Dia de Visita | Formas de Pagamento       | Observações
João Silva   | 123.456.789-00 |                   | (11) 98765-4321| joao@email.com | São Paulo | Centro | Próximo ao mercado  | segunda       | dinheiro, pix             | Cliente VIP
ABC Ltda     |                | 12.345.678/0001-90| (11) 91234-5678| abc@empresa.com| Campinas  | Cambui | Av. Principal 1000  | terça         | pix, cartao_credito       | Empresa parceira
```

## 🐛 Solução de Problemas

### Erro: "Formato inválido"
**Solução**: Certifique-se que o arquivo é .xlsx ou .xls

### Erro: "Colunas obrigatórias faltando"
**Solução**: Verifique se a coluna "Nome" existe na planilha

### Erro: "CPF/CNPJ já cadastrado"
**Solução**: O cliente já existe no sistema. Edite-o diretamente ou use um CPF/CNPJ diferente

### Erro: "Nome obrigatório"
**Solução**: Alguma linha está sem nome. Preencha ou remova a linha

### Erro: "Arquivo muito grande"
**Solução**: O arquivo excede 10 MB. Divida em arquivos menores

## 📊 Limites e Restrições

| Limite | Valor |
|--------|-------|
| Tamanho máximo do arquivo | 10 MB |
| Formatos aceitos | .xlsx, .xls |
| Registros recomendados por importação | 500-1000 |
| Tempo máximo de processamento | 60 segundos |

## 🎨 Interface

### Lista de Clientes

```
┌────────────────────────────────────────────────────────┐
│  Meus Clientes                                         │
│  ┌──────────┐ ┌─────────────┐ ┌──────────────┐       │
│  │ Exportar │ │  Importar   │ │ Novo Cliente │       │
│  │  Excel   │ │   Excel     │ │              │       │
│  └──────────┘ └─────────────┘ └──────────────┘       │
└────────────────────────────────────────────────────────┘
```

### Página de Importação

```
┌─────────────────────────────────────────────────┐
│  Upload de Arquivo    │  Estrutura da Planilha  │
│  [Escolher arquivo]   │  Colunas obrigatórias   │
│  [Importar]           │  Exemplos               │
│                       │  [Baixar Modelo]        │
└─────────────────────────────────────────────────┘
│  Como Funciona a Importação                     │
│  1. Prepare  2. Upload  3. Processo  4. Confirma│
└─────────────────────────────────────────────────┘
```

## 🔄 Atualizações Futuras

Funcionalidades planejadas:
- [ ] Importação por supervisores e admins
- [ ] Atualização de clientes existentes via importação
- [ ] Exportação com filtros personalizados
- [ ] Importação de histórico de compras
- [ ] Validação de endereços (CEP)
- [ ] Importação via CSV
- [ ] Download de logs de importação

---

**Última atualização**: Dezembro 2024  
**Versão**: 1.0
