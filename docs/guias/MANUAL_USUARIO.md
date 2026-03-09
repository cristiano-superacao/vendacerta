# 📚 Manual do Usuário - Sistema de Gestão de Metas e Comissões

## 🎯 Bem-vindo ao Sistema de Metas!

Este manual foi criado para ajudá-lo a usar todas as funcionalidades do sistema de forma simples e eficiente.

---

## 📞 Suporte Técnico

**Cristiano Santos**  
📱 Telefone/WhatsApp: **(71) 99337-2960**  
📧 Email: cristiano.s.santos@ba.estudante.senai.br  

**Horário de Atendimento:**
- Segunda a Sexta: 8h às 18h
- Sábado: 8h às 12h

---

## 🚀 Índice

1. [Primeiro Acesso](#primeiro-acesso)
2. [Como Fazer Login](#como-fazer-login)
3. [Dashboard Principal](#dashboard-principal)
4. [Gerenciar Vendedores](#gerenciar-vendedores)
5. [Gerenciar Metas](#gerenciar-metas)
6. [Gerenciar Equipes](#gerenciar-equipes)
7. [Relatórios e PDFs](#relatórios-e-pdfs)
8. [Recuperar Senha](#recuperar-senha)
9. [Perguntas Frequentes](#perguntas-frequentes)

---

## 1️⃣ Primeiro Acesso {#primeiro-acesso}

### Como Criar uma Conta

1. Acesse o sistema pela URL fornecida
2. Na tela de login, clique em **"Criar conta"**
3. Preencha o formulário:
   - **Nome Completo**: Seu nome completo
   - **Email**: Use um email válido (será usado para login)
   - **Cargo**: Selecione seu nível de acesso
     - 👤 **Usuário**: Visualiza apenas suas próprias metas
     - 👥 **Supervisor**: Gerencia vendedores e metas da equipe
     - 👨‍💼 **Administrador**: Acesso total ao sistema
   - **Senha**: Mínimo 6 caracteres
   - **Confirmar Senha**: Digite a mesma senha
4. Clique em **"Cadastrar"**
5. Você será redirecionado para o login

### Credenciais Padrão do Administrador

Se você é o primeiro usuário do sistema, crie o Admin definindo `ADMIN_PASSWORD` e executando:

```powershell
$env:ADMIN_EMAIL="admin@sistema.com"
$env:ADMIN_PASSWORD="SUA_SENHA_FORTE"
python scripts/create_admin.py
```

Depois faça login com `ADMIN_EMAIL` / `ADMIN_PASSWORD`.

---

## 2️⃣ Como Fazer Login {#como-fazer-login}

### Passo a Passo

1. Acesse a página de login
2. Digite seu **email** cadastrado
3. Digite sua **senha**
4. Clique em **"Entrar no Sistema"**
5. Você será direcionado para o Dashboard

### Esqueceu sua senha?

1. Na tela de login, clique em **"Esqueceu a senha?"**
2. Digite seu **email cadastrado**
3. Clique em **"Enviar Instruções"**
4. Copie o link fornecido na mensagem
5. Acesse o link e crie uma **nova senha**
6. Faça login com a nova senha

---

## 3️⃣ Dashboard Principal {#dashboard-principal}

O Dashboard é a tela principal onde você visualiza todas as métricas importantes.

### 📊 Informações Exibidas

#### Resumo Global (Topo da Página)
- 📈 **Total de Vendedores**: Quantos vendedores estão cadastrados
- 💰 **Receita Total**: Soma de toda receita alcançada
- 🎯 **Meta Total**: Soma de todas as metas do período
- 💵 **Comissões Totais**: Valor total em comissões a pagar
- 📊 **% de Alcance da Equipe**: Percentual geral da equipe

#### Tabela de Ranking
Mostra todos os vendedores ordenados por desempenho:
- **Nome do Vendedor**
- **Supervisor** responsável
- **Meta** estabelecida (R$)
- **Receita Alcançada** (R$)
- **% de Alcance** - Barra visual colorida:
  - 🔴 Vermelho: < 50% da meta
  - 🟡 Amarelo: 50% - 99% da meta
  - 🟢 Verde: ≥ 100% da meta
- **Comissão Total** (R$)
- **Status da Comissão**:
  - ⏳ Pendente
  - ✅ Aprovado
  - 💰 Pago
- **Ações**: Visualizar, Editar, Excluir

#### Projeções por Supervisão (novo)
- **Supervisor**: nome do responsável pela equipe
- **Taxa (%)**: percentual de comissão do supervisor aplicado sobre a base elegível
- **Comissão (R$)**: valor estimado/real de comissão do supervisor no período
- **Base**: calculada conforme regras de metas do tipo "valor"; para outros tipos, segue as regras vigentes do sistema

### 🔄 Filtrar por Período

No topo do dashboard:
1. Selecione o **Mês** desejado
2. Selecione o **Ano** desejado
3. Clique em **"Filtrar"**

---

## 4️⃣ Gerenciar Vendedores {#gerenciar-vendedores}

### 📋 Ver Lista de Vendedores

1. No menu lateral, clique em **"Vendedores"**
2. Você verá a lista completa com:
   - Nome
   - Email
   - Telefone
   - CPF
   - Equipe
   - Status (Ativo/Inativo)

### ➕ Adicionar Novo Vendedor

1. Clique no botão **"+ Adicionar Vendedor"**
2. Preencha o formulário:
   - **Nome Completo** (obrigatório)
   - **Email** (obrigatório, único)
   - **Telefone** (opcional)
   - **CPF** (opcional, 11 dígitos)
   - **Supervisor** (selecione da lista)
   - **Equipe** (selecione da lista)
3. Clique em **"Salvar"**

### ✏️ Editar Vendedor

1. Na lista de vendedores, clique no botão **"Editar"** (ícone de lápis)
2. Altere as informações necessárias
3. Clique em **"Salvar Alterações"**

### 🗑️ Excluir Vendedor

1. Clique no botão **"Excluir"** (ícone de lixeira)
2. Confirme a exclusão

⚠️ **Atenção:** Ao excluir um vendedor, todas as suas metas também serão excluídas!

### 🔄 Ativar/Desativar Vendedor

- **Vendedor Ativo**: Aparece nas listagens e pode ter metas
- **Vendedor Inativo**: Fica oculto mas não perde o histórico

---

## 5️⃣ Gerenciar Metas {#gerenciar-metas}

### 📋 Ver Lista de Metas

1. No menu lateral, clique em **"Metas"**
2. Visualize todas as metas com:
   - Vendedor
   - Período (Mês/Ano)
   - Meta (R$)
   - Receita Alcançada (R$)
   - % de Alcance
   - Comissão
   - Status

### ➕ Criar Nova Meta

1. Clique em **"+ Adicionar Meta"**
2. Preencha:
   - **Vendedor** (selecione da lista)
   - **Mês** (1-12)
   - **Ano** (ex: 2025)
   - **Valor da Meta** (R$)
   - **Receita Alcançada** (R$) - opcional, pode atualizar depois
   - **Status da Comissão** (Pendente/Aprovado/Pago)
   - **Observações** (opcional)
3. Clique em **"Salvar"**

### 💰 Como Funciona o Cálculo de Comissão

O sistema calcula automaticamente baseado no percentual de alcance:

| % de Alcance | Comissão Base | Exemplo (Meta R$ 100.000) |
|--------------|---------------|---------------------------|
| 0% - 49%     | 0%            | R$ 0,00                   |
| 50% - 69%    | 3%            | R$ 3.000,00               |
| 70% - 89%    | 5%            | R$ 5.000,00               |
| 90% - 99%    | 7%            | R$ 7.000,00               |
| 100% - 119%  | 10%           | R$ 10.000,00              |
| ≥ 120%       | 12%           | R$ 12.000,00              |

**Bônus por Superação:**
- Se alcançar mais de 100%, ganha comissão extra sobre o excedente
- Exemplo: Alcançou 110% (R$ 110.000)
  - Comissão base: 10% de R$ 100.000 = R$ 10.000
  - Bônus: 50% de 10% sobre R$ 10.000 = R$ 500
  - **Total: R$ 10.500**

### ✏️ Atualizar Receita de uma Meta

1. Na lista de metas, clique em **"Editar"**
2. Atualize o campo **"Receita Alcançada"**
3. O sistema recalcula automaticamente:
   - % de Alcance
   - Comissão Total
4. Clique em **"Salvar"**

### 🔄 Alterar Status da Comissão

1. Edite a meta
2. Altere o **"Status da Comissão"**:
   - **Pendente**: Ainda não foi processada
   - **Aprovado**: Aprovada para pagamento
   - **Pago**: Já foi paga ao vendedor
3. Salve as alterações

---

## 6️⃣ Gerenciar Equipes {#gerenciar-equipes}

### 📋 Ver Lista de Equipes

1. No menu lateral, clique em **"Equipes"**
2. Visualize:
   - Nome da Equipe
   - Supervisor
   - Número de Membros
   - Ações

### ➕ Criar Nova Equipe

1. Clique em **"+ Adicionar Equipe"**
2. Preencha:
   - **Nome da Equipe** (obrigatório, único)
   - **Descrição** (opcional)
   - **Supervisor** (selecione da lista de usuários)
3. Clique em **"Salvar"**

### 👥 Ver Detalhes da Equipe

1. Clique no nome da equipe
2. Você verá:
   - Informações da equipe
   - Lista de todos os vendedores
   - Métricas da equipe

### ✏️ Editar Equipe

1. Clique em **"Editar"**
2. Altere as informações
3. Salve as alterações

---

## 7️⃣ Relatórios e PDFs {#relatórios-e-pdfs}

### 📄 Gerar PDF do Dashboard

1. No Dashboard, clique em **"Gerar PDF"**
2. O PDF será baixado automaticamente contendo:
   - Resumo global do período
   - Ranking completo de vendedores
   - Gráficos e métricas

### 📊 Gerar Relatório de Metas

1. Acesse **"Metas"**
2. Clique em **"Gerar PDF de Metas"**
3. Relatório detalhado será gerado com:
   - Todas as metas do período
   - Detalhamento de comissões
   - Status de pagamentos

### 📈 Relatório de Metas Avançado — Visões Vendedor e Supervisor

No módulo de relatórios, o "Relatório de Metas Avançado" permite alternar a análise por Vendedor ou por Supervisor mantendo layout responsivo e profissional.

1. Acesse: Menu → Relatórios → Metas Avançado
2. Seletor "Visão": escolha entre **Vendedor** ou **Supervisor**
3. Filtros dinâmicos:
   - Visão Vendedor: filtros por vendedor, mês, ano, tipo de meta
   - Visão Supervisor: filtros por supervisor, mês, ano, tipo de meta
4. Tabelas exibidas:
   - Visão Vendedor: ranking e detalhamento por vendedor
   - Visão Supervisor: detalhamento por supervisão com colunas
     - Supervisor, Tipo, Período, Meta (R$), Realizado (R$)
     - Progresso (% com barra), **Taxa (%)** e **Comissão (R$)**
5. Responsividade: tabelas colapsam colunas menos críticas em telas pequenas

Observações:
- A **Taxa (%) do Supervisor** é determinada pelas faixas de comissão configuradas e aplicada sobre a base elegível para metas do tipo valor
- O **Progresso** usa cores padrão (vermelho/amarelo/verde) conforme o percentual de alcance

### 💡 Dica

Os PDFs são gerados no formato profissional e podem ser usados para:
- Apresentações para diretoria
- Prestação de contas
- Arquivo histórico
- Envio para vendedores

---

## 8️⃣ Recuperar Senha {#recuperar-senha}

### Passo a Passo Completo

1. **Na tela de login**, clique em **"Esqueceu a senha?"**

2. **Digite seu email cadastrado**
   - Use o mesmo email da sua conta

3. **Clique em "Enviar Instruções"**
   - Aparecerá uma mensagem com um link

4. **Copie o link fornecido**
   - Exemplo: `/redefinir-senha/abc123...`

5. **Acesse o link**
   - Cole no navegador após a URL do sistema

6. **Crie sua nova senha**
   - Mínimo 6 caracteres
   - O sistema mostra a força da senha:
     - 🔴 Fraca
     - 🟡 Média
     - 🟢 Forte

7. **Confirme a nova senha**
   - Digite exatamente a mesma senha

8. **Clique em "Redefinir Senha"**

9. **Faça login com a nova senha**

---

## 9️⃣ Perguntas Frequentes {#perguntas-frequentes}

### ❓ Como sei qual meu nível de acesso?

No menu lateral, ao lado do seu nome, aparece seu cargo:
- 👨‍💼 Admin
- 👥 Supervisor
- 👤 Usuário

### ❓ Posso editar minhas próprias informações?

Sim! Clique no seu nome no menu e depois em "Meu Perfil" (funcionalidade em desenvolvimento).

### ❓ Como adiciono um vendedor a uma equipe?

1. Edite o vendedor
2. No campo "Equipe", selecione a equipe desejada
3. Salve

### ❓ Posso ter metas de meses anteriores?

Sim! O sistema permite cadastrar metas de qualquer período passado ou futuro.

### ❓ Como sei se uma comissão foi paga?

No Dashboard ou na lista de Metas, verifique a coluna "Status":
- ⏳ **Pendente**: Ainda não processada
- ✅ **Aprovado**: Aprovada mas ainda não paga
- 💰 **Pago**: Já foi paga

### ❓ Posso excluir uma meta por engano?

⚠️ Cuidado! Não há confirmação antes de excluir. Sempre verifique antes de clicar em "Excluir".

### ❓ O sistema funciona no celular?

✅ Sim! O sistema é 100% responsivo e funciona em:
- 📱 Celulares
- 📱 Tablets
- 💻 Desktops
- 🖥️ Notebooks

### ❓ Preciso de internet para usar?

✅ Sim, o sistema é online e requer conexão com a internet.

### ❓ Meus dados estão seguros?

✅ Sim! O sistema usa:
- 🔒 Criptografia de senhas (hash)
- 🔐 Proteção CSRF em formulários
- 🛡️ Autenticação segura
- 🔑 Tokens únicos para recuperação de senha

---

## 📱 Atalhos e Dicas Úteis

### ⌨️ Atalhos do Teclado

- **Tab**: Navegar entre campos
- **Enter**: Submeter formulário
- **Esc**: Fechar alertas/modais

### 💡 Dicas de Uso

1. **Use filtros no Dashboard**
   - Visualize diferentes períodos rapidamente

2. **Mantenha os dados atualizados**
   - Atualize as receitas regularmente

3. **Verifique o ranking**
   - Incentive os vendedores a melhorarem

4. **Use observações nas metas**
   - Documente informações importantes

5. **Gere PDFs regularmente**
   - Mantenha histórico das performances

6. **Mantenha equipes organizadas**
   - Facilita o gerenciamento

---

## 🆘 Problemas Comuns e Soluções

### 🔴 Não consigo fazer login

**Soluções:**
1. Verifique se o email está correto
2. Verifique se o Caps Lock está desligado
3. Tente recuperar a senha
4. Entre em contato com o suporte

### 🔴 Esqueci meu email de cadastro

**Solução:**
- Entre em contato com o suporte pelo telefone **(71) 99337-2960**

### 🔴 O cálculo de comissão está errado

**Verificações:**
1. Confira se a meta está correta
2. Confira se a receita está atualizada
3. Verifique a tabela de percentuais
4. Entre em contato com o suporte se persistir

### 🔴 Não consigo adicionar vendedor

**Verificações:**
1. Email já cadastrado? Tente outro email
2. CPF já cadastrado? Verifique duplicidades
3. Todos os campos obrigatórios preenchidos?

### 🔴 A página não carrega

**Soluções:**
1. Atualize a página (F5)
2. Limpe o cache do navegador
3. Tente outro navegador
4. Verifique sua conexão com internet
5. Entre em contato com o suporte

---

## 📞 Como Entrar em Contato com o Suporte

### Por Telefone/WhatsApp
📱 **(71) 99337-2960**

**Horários:**
- Segunda a Sexta: 8h às 18h
- Sábado: 8h às 12h

### Por Email
📧 **cristiano.s.santos@ba.estudante.senai.br**

### Ao solicitar suporte, informe:
1. ✅ Seu nome e empresa
2. ✅ Descrição detalhada do problema
3. ✅ Prints de tela (se possível)
4. ✅ O que você estava tentando fazer
5. ✅ Mensagens de erro que apareceram

---

## 🎓 Tutoriais em Vídeo

Em breve disponibilizaremos tutoriais em vídeo para facilitar ainda mais o uso do sistema!

---

## 📋 Checklist para Novos Usuários

- [ ] Criar minha conta
- [ ] Fazer primeiro login
- [ ] Alterar senha padrão (se admin)
- [ ] Conhecer o Dashboard
- [ ] Cadastrar equipes
- [ ] Cadastrar vendedores
- [ ] Criar primeiras metas
- [ ] Atualizar receitas
- [ ] Gerar primeiro relatório PDF
- [ ] Salvar contato do suporte

---

## 🎯 Conclusão

Este sistema foi desenvolvido para facilitar a gestão de metas e comissões da sua equipe de vendas. Use-o diariamente para:

✅ Acompanhar performance em tempo real  
✅ Motivar sua equipe com ranking transparente  
✅ Calcular comissões automaticamente  
✅ Gerar relatórios profissionais  
✅ Tomar decisões baseadas em dados  

**Qualquer dúvida, estamos à disposição!**

---

## 📌 Informações do Sistema

- **Versão:** 1.0
- **Última Atualização:** Dezembro 2025 (inclui visão por Supervisor no relatório avançado e exibição de Taxa/Comissão no dashboard)
- **Desenvolvedor:** Cristiano Santos
- **Suporte:** (71) 99337-2960

---

**© 2025 - Sistema de Gestão de Metas e Comissões**  
**Todos os direitos reservados**
