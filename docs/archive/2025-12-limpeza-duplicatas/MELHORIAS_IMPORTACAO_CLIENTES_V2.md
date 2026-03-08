# Melhorias na Importação de Clientes (Atualizado)

**Data**: 17 de dezembro de 2025
**Descrição**: Ajuste na lógica de importação de clientes via Excel para permitir atualização de cadastros existentes.

## 🔄 Mudanças Realizadas

### Antes
- O sistema verificava se o CPF ou CNPJ já existia no banco de dados.
- Se existisse, a linha era rejeitada e um erro era exibido ("CNPJ já cadastrado").
- Isso impedia a atualização em massa de dados de clientes.

### Depois (Atual)
- O sistema verifica se o CPF ou CNPJ já existe.
- **Se existir**: O cliente é **atualizado** com os novos dados da planilha (endereço, telefone, vendedor, etc.).
    - O `codigo_cliente` original é preservado.
    - O `codigo_bp` (código do ERP) é atualizado se fornecido.
- **Se não existir**: Um novo cliente é criado.
    - Um novo `codigo_cliente` é gerado automaticamente.

## ✅ Benefícios
1. **Eliminação de Erros de Duplicidade**: Não haverá mais erros de "CNPJ já cadastrado" ao reimportar uma lista.
2. **Atualização em Massa**: É possível atualizar dados de contato, endereço ou vendedor de centenas de clientes apenas subindo a planilha novamente.
3. **Integridade dos Dados**: O histórico de compras e o código interno do cliente são mantidos mesmo na atualização.

## 📝 Como Usar
1. Acesse o menu **Clientes > Importar**.
2. Selecione o arquivo Excel (`.xlsx` ou `.xls`).
3. O sistema irá processar o arquivo:
    - Novos clientes serão adicionados.
    - Clientes existentes (identificados por CPF/CNPJ) serão atualizados.
4. Ao final, um resumo será exibido: "✅ Processamento concluído! X novos clientes importados e Y atualizados."
