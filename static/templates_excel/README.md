# 📊 Templates Excel para Importação

Este diretório contém templates de planilhas Excel para importação em massa de dados.

## 📁 Templates Disponíveis:

### 1. **template_vendedores.xlsx**
Template para importar vendedores em massa.

**Colunas obrigatórias:**
- Nome (texto)
- Email (texto único)
- Telefone (texto)
- CPF (texto único, formato: 000.000.000-00)

**Colunas opcionais:**
- Supervisor Email (email do supervisor)
- Equipe Nome (nome da equipe)

### 2. **template_metas.xlsx**
Template para importar metas em massa.

**Colunas obrigatórias:**
- Vendedor Email (email do vendedor)
- Mês (número de 1 a 12)
- Ano (número, ex: 2025)
- Valor Meta (número decimal)
- Receita Alcançada (número decimal)

**Colunas opcionais:**
- Status Comissão (Pendente, Aprovado, Pago)
- Observações (texto)

### 3. **template_supervisores.xlsx**
Template para importar supervisores em massa.

**Colunas obrigatórias:**
- Nome (texto)
- Email (texto único)
- Cargo (supervisor, gerente, admin)

**Colunas opcionais:**
- Telefone (texto)

## 📝 Instruções de Uso:

1. **Baixe o template** correspondente
2. **Preencha os dados** seguindo o formato
3. **Salve como Excel** (.xlsx)
4. **Acesse a página de importação** no sistema
5. **Faça upload** do arquivo
6. **Aguarde o processamento**
7. **Verifique os resultados**

## ⚠️ Regras Importantes:

### Vendedores:
- Email e CPF devem ser únicos
- Se supervisor/equipe não existir, será ignorado
- Vendedor será criado como ativo por padrão
- Empresa será a do usuário logado

### Metas:
- Vendedor deve existir no sistema
- Não pode haver meta duplicada (mesmo vendedor, mês e ano)
- Status padrão é "Pendente"
- Comissão será calculada automaticamente

### Supervisores:
- Email deve ser único
- Senha padrão será: senha123
- Cargo padrão: supervisor
- Empresa será a do usuário logado

## 🎯 Exemplo de Dados:

### Vendedores:
```
Nome              | Email                  | Telefone         | CPF            | Supervisor Email      | Equipe Nome
João Silva        | joao@empresa.com       | (11) 98765-4321  | 123.456.789-00 | maria@empresa.com     | Equipe A
Maria Santos      | maria@empresa.com      | (11) 98765-4322  | 123.456.789-01 |                       | Equipe B
```

### Metas:
```
Vendedor Email    | Mês | Ano  | Valor Meta | Receita Alcançada | Status Comissão | Observações
joao@empresa.com  | 12  | 2025 | 50000.00   | 45000.00          | Pendente        | Bom desempenho
maria@empresa.com | 12  | 2025 | 60000.00   | 65000.00          | Aprovado        | Superou meta
```

### Supervisores:
```
Nome           | Email                | Cargo      | Telefone
Carlos Admin   | carlos@empresa.com   | admin      | (11) 98765-4323
Ana Supervisor | ana@empresa.com      | supervisor | (11) 98765-4324
```

## ✅ Validações Automáticas:

O sistema validará automaticamente:
- ✅ Formato de email
- ✅ Unicidade de email e CPF
- ✅ Existência de registros relacionados
- ✅ Valores numéricos corretos
- ✅ Datas válidas
- ✅ Status válidos

## 🚨 Tratamento de Erros:

Se houver erros:
1. Sistema mostrará lista de erros encontrados
2. Nenhum registro será importado (transação atômica)
3. Corrija os erros no arquivo
4. Tente novamente

Se tudo estiver correto:
1. Todos os registros serão importados
2. Mensagem de sucesso será exibida
3. Você será redirecionado para a lista

## 📞 Suporte:

Dúvidas sobre importação?
- 📧 Email: cristiano.s.santos@ba.estudante.senai.br
- 📱 WhatsApp: (71) 99337-2960
