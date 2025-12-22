# 🚀 Guia Rápido - Sistema de Clientes

## 📋 Passo a Passo para Começar

### 1️⃣ Atualizar o Banco de Dados

Primeiro, execute o script para criar as tabelas:

```bash
python atualizar_banco_clientes.py
```

**Ou manualmente no Python:**
```python
from app import app, db
with app.app_context():
    db.create_all()
```

### 2️⃣ Acessar o Módulo

1. Faça login no sistema como **Vendedor**
2. No menu lateral, clique em **"Clientes"** 👤
3. Você verá a lista de clientes (vazia no início)

### 3️⃣ Cadastrar Seu Primeiro Cliente

1. Clique no botão **"Novo Cliente"** (verde)
2. Preencha os campos:

**Obrigatórios:**
- ✅ Nome completo ou Razão Social
- ✅ CPF **OU** CNPJ (pelo menos um)

**Recomendados:**
- 📍 Cidade e Bairro
- 📞 Telefone (para WhatsApp)
- 📅 Dia da visita
- 💳 Formas de pagamento

3. Clique em **"Salvar Cliente"**

### 4️⃣ Registrar Compra

**Opção 1 - Da lista:**
1. Encontre o cliente
2. Clique no ícone do carrinho 🛒

**Opção 2 - Dos detalhes:**
1. Clique no nome do cliente
2. Clique em **"Nova Compra"**

**Preencha:**
- Valor da compra
- Forma de pagamento
- Observações (opcional)

### 5️⃣ Entender os Status

| Cor | Status | Significado |
|-----|--------|-------------|
| 🟢 Verde | Positivado | Comprou nos últimos 30 dias |
| 🟡 Amarelo | Atenção | 30-38 dias sem compra |
| 🔴 Vermelho | Sem Compras | Mais de 38 dias sem compra |

### 6️⃣ Usar Filtros

Na lista de clientes, filtre por:
- **Status**: Verde/Amarelo/Vermelho
- **Cidade**: Digite o nome da cidade
- **Bairro**: Digite o nome do bairro
- **Dia de Visita**: Selecione o dia

### 7️⃣ Gerar Relatórios

1. Clique em **"Relatório"**
2. Veja estatísticas:
   - Total de clientes
   - Clientes positivados (verde)
   - Clientes em atenção (amarelo)
   - Clientes sem compras (vermelho)
3. Clique em **"Imprimir"** para salvar/imprimir

## 💡 Dicas Importantes

### ✅ Para Vendedores

1. **Cadastre logo após a venda**
   - O cliente já entra como "verde"
   - Seus dados ficam salvos

2. **Use o dia de visita**
   - Organize sua rotina semanal
   - Filtre clientes por dia

3. **Atenção aos amarelos**
   - Revisite em 30-38 dias
   - Evite que fiquem vermelhos

4. **WhatsApp rápido**
   - Na tela do cliente, clique no 📱
   - Abre direto o WhatsApp

### 🎯 Metas de Compra

- **Mínimo**: 1 compra por mês
- **Máximo**: 4-5 compras por mês
- **Controle**: Sistema valida automaticamente

### 📊 Como Melhorar seu Desempenho

1. **Meta: 80%+ de clientes verdes**
   - Visite regularmente
   - Mantenha contato ativo

2. **Reduza os vermelhos**
   - Foque em reativar clientes inativos
   - Use filtros para identificá-los

3. **Organize visitas**
   - Use o campo "Dia de visita"
   - Planeje sua semana

## 🔧 Resolução de Problemas

### ❌ "CPF já cadastrado"
- Cliente já existe no sistema
- Use a busca para encontrá-lo

### ❌ "Limite de compras atingido"
- Cliente já comprou 4-5 vezes este mês
- Aguarde o próximo mês

### ❌ Não vejo meus clientes
- Verifique se está logado como vendedor
- Atualize a página

### ❌ Status não muda de cor
- Registre uma compra para atualizar
- Status é calculado automaticamente

## 📱 Recursos Mobile

O sistema é **100% responsivo**:
- ✅ Funciona em celular
- ✅ Funciona em tablet
- ✅ Funciona em desktop

## 🎓 Exemplo Prático

### Cadastro Completo

```
Nome: João Silva Comércio
CNPJ: 12.345.678/0001-90
Telefone: (71) 98888-7777
Cidade: Salvador
Bairro: Itapuã
Dia Visita: Terça-feira
Formas Pagamento: PIX, Dinheiro
```

### Primeira Compra

```
Valor: R$ 250,00
Forma: PIX
Obs: Primeira compra - pedido teste
```

**Resultado**: Cliente fica 🟢 VERDE (positivado)

### Acompanhamento

- Após 30 dias sem compra → 🟡 AMARELO
- Após 38 dias sem compra → 🔴 VERMELHO
- Nova compra → volta para 🟢 VERDE

## 🏆 Melhores Práticas

1. **Cadastre todos os clientes**
   - Mesmo os pequenos
   - Crie seu histórico

2. **Atualize dados regularmente**
   - Telefone mudou? Atualize
   - Novo endereço? Registre

3. **Use observações**
   - Preferências do cliente
   - Datas importantes
   - Histórico de problemas/soluções

4. **Monitore seu relatório**
   - Semanalmente
   - Ajuste sua rota
   - Foque nos amarelos/vermelhos

## 📞 Precisa de Ajuda?

1. Leia este guia completo
2. Consulte [IMPLEMENTACAO_CLIENTES.md](IMPLEMENTACAO_CLIENTES.md)
3. Entre em contato com seu supervisor

---

**Boas vendas! 🚀💰**
