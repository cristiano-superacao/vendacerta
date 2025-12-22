# 📚 MANUAL COMPLETO DE MÓDULOS - VENDA CERTA

**Sistema de Gestão de Vendas, Metas e Comissões**  
**Versão**: 3.0  
**Data**: 17 de dezembro de 2025

---

## 📖 ÍNDICE

1. [Módulo de Autenticação](#1-módulo-de-autenticação)
2. [Módulo de Dashboard](#2-módulo-de-dashboard)
3. [Módulo de Vendedores](#3-módulo-de-vendedores)
4. [Módulo de Clientes](#4-módulo-de-clientes)
5. [Módulo de Supervisores](#5-módulo-de-supervisores)
6. [Módulo de Funcionários](#6-módulo-de-funcionários)
7. [Módulo de Metas](#7-módulo-de-metas)
8. [Módulo de Comissões](#8-módulo-de-comissões)
9. [Módulo de Relatórios](#9-módulo-de-relatórios)
10. [Módulo de Super Admin](#10-módulo-de-super-admin)
11. [Módulo de Estoque](#11-módulo-de-estoque)
12. [Módulo de Backup](#12-módulo-de-backup)

---

## 1. 📝 MÓDULO DE AUTENTICAÇÃO

### O que faz?
Gerencia login, registro, recuperação de senha e controle de acesso ao sistema.

### Funcionalidades

#### 1.1 Login
**Como usar:**
1. Acesse a página inicial do sistema
2. Digite seu **email** e **senha**
3. Clique em **Entrar**

**Características:**
- ✅ Validação de credenciais
- ✅ Redirecionamento automático por perfil
- ✅ Mensagens de erro claras
- ✅ Sessão segura

**Perfis de acesso:**
- **Super Admin**: Controle total do sistema
- **Admin**: Gestão completa da empresa
- **Gerente**: Gestão de equipe e metas
- **Supervisor**: Acompanhamento de vendedores
- **Vendedor**: Acesso móvel para vendas
- **Financeiro**: Relatórios financeiros
- **RH**: Gestão de funcionários
- **Técnico**: Ordens de serviço

#### 1.2 Registro de Nova Empresa
**Como usar:**
1. Na tela de login, clique em **"Criar Conta"**
2. Preencha os dados da empresa:
   - Nome da empresa
   - Nome do responsável
   - Email (será seu login)
   - Senha (mínimo 6 caracteres)
3. Clique em **Registrar**

**O que acontece:**
- ✅ Empresa criada automaticamente
- ✅ Primeiro usuário vira Admin da empresa
- ✅ Banco de dados configurado
- ✅ Sistema pronto para usar

#### 1.3 Recuperação de Senha
**Como usar:**
1. Na tela de login, clique em **"Esqueci minha senha"**
2. Digite seu **email**
3. Receberá um token de recuperação
4. Use o token para redefinir a senha

**Dica:** Guarde o token em local seguro!

---

## 2. 📊 MÓDULO DE DASHBOARD

### O que faz?
Exibe indicadores de desempenho, gráficos e métricas importantes do negócio.

### Dashboards Disponíveis

#### 2.1 Dashboard Principal (Admin/Gerente)
**Indicadores:**
- 📈 **Vendas do Mês**: Total de vendas realizadas
- 🎯 **Meta do Mês**: Objetivo estabelecido
- 💰 **Receita Alcançada**: Valor já conquistado
- 📊 **% de Atingimento**: Progresso da meta
- 👥 **Vendedores Ativos**: Equipe em atividade
- 🏆 **Top Vendedores**: Melhores da equipe

**Gráficos:**
- 📉 Evolução de vendas (linha)
- 📊 Vendas por vendedor (barras)
- 🎯 Meta vs. Realizado (comparativo)
- 📅 Performance mensal

**Como usar:**
1. Faça login como Admin ou Gerente
2. Será redirecionado automaticamente
3. Navegue pelos cards e gráficos
4. Clique nos indicadores para detalhes

#### 2.2 Dashboard do Supervisor
**Indicadores:**
- 👥 **Minha Equipe**: Vendedores sob supervisão
- 🎯 **Meta da Equipe**: Objetivo coletivo
- 📊 **Desempenho Individual**: Cada vendedor
- 💰 **Comissões da Equipe**: Ganhos totais

**Como usar:**
1. Faça login como Supervisor
2. Veja resumo da sua equipe
3. Acompanhe performance individual
4. Identifique quem precisa de suporte

#### 2.3 Dashboard Mobile (Vendedor)
**Indicadores:**
- 🎯 **Minha Meta**: Objetivo pessoal
- 📊 **Minhas Vendas**: Total do mês
- 💰 **Minha Comissão**: Ganhos previstos
- 📅 **Faltam X dias**: Contador de prazo

**Funcionalidades:**
- ✅ Registro rápido de vendas
- ✅ Visualização de clientes
- ✅ Consulta de comissão
- ✅ Interface otimizada para celular

**Como usar:**
1. Acesse pelo celular
2. Faça login como Vendedor
3. Navegue pelo menu mobile
4. Registre vendas rapidamente

---

## 3. 👤 MÓDULO DE VENDEDORES

### O que faz?
Cadastro, gerenciamento e acompanhamento de vendedores.

### Funcionalidades

#### 3.1 Listar Vendedores
**Como usar:**
1. Menu lateral: **Vendedores** → **Listar Vendedores**
2. Visualize todos os vendedores cadastrados
3. Use os filtros para buscar:
   - Por nome
   - Por supervisor
   - Por status (ativo/inativo)

**Informações exibidas:**
- Nome completo
- Email
- Telefone
- Supervisor responsável
- Status (ativo/inativo)
- Ações disponíveis

#### 3.2 Cadastrar Novo Vendedor
**Como usar:**
1. Menu: **Vendedores** → **Novo Vendedor**
2. Preencha o formulário:
   - **Nome completo** (obrigatório)
   - **Email** (opcional)
   - **Telefone** (opcional)
   - **CPF** (opcional)
   - **Data de admissão**
   - **Supervisor** (selecione da lista)
   - **Status**: Ativo/Inativo
3. Clique em **Salvar**

**Dica:** Você pode criar o login depois!

#### 3.3 Criar Login para Vendedor
**Como usar:**
1. Na lista de vendedores, clique em **⚙️ Ações**
2. Selecione **Criar Login**
3. Preencha:
   - **Email** (será o login)
   - **Senha** (mínimo 6 caracteres)
   - **Confirmar senha**
4. Clique em **Criar Login**

**O vendedor poderá:**
- ✅ Acessar o app mobile
- ✅ Ver suas metas
- ✅ Consultar comissões
- ✅ Registrar vendas

#### 3.4 Editar Vendedor
**Como usar:**
1. Na lista, clique em **✏️ Editar**
2. Altere os dados necessários
3. Clique em **Atualizar**

#### 3.5 Ativar/Desativar Vendedor
**Como usar:**
1. Na lista, clique em **Ativar** ou **Desativar**
2. Confirme a ação

**Efeitos:**
- ❌ **Desativado**: Não aparece em relatórios ativos
- ✅ **Ativado**: Volta a aparecer normalmente

#### 3.6 Resetar Senha
**Como usar:**
1. Na lista, clique em **🔑 Resetar Senha**
2. Digite a nova senha
3. Confirme

#### 3.7 Importar Vendedores (Excel)
**Como usar:**
1. Menu: **Vendedores** → **Importar Excel**
2. Baixe o **modelo de planilha**
3. Preencha a planilha:
   ```
   Nome | Email | Telefone | CPF | Data Admissão
   ```
4. Faça upload do arquivo
5. Clique em **Importar**

**Validações automáticas:**
- ✅ Verifica duplicatas
- ✅ Valida formato de email
- ✅ Valida CPF
- ✅ Mostra erros encontrados

---

## 4. 🏢 MÓDULO DE CLIENTES

### O que faz?
Gestão completa de clientes, histórico de compras e relacionamento.

### Funcionalidades

#### 4.1 Listar Clientes
**Como usar:**
1. Menu: **Clientes** → **Listar Clientes**
2. Navegue pela lista paginada
3. Use os filtros:
   - **Nome**: Busca por nome
   - **Vendedor**: Filtra por responsável
   - **Status**: Ativo/Inativo
   - **Período**: Data de cadastro

**Informações exibidas:**
- Nome / Razão Social
- CPF / CNPJ
- Email e Telefone
- Endereço
- Vendedor responsável
- Total de compras
- Última compra

#### 4.2 Cadastrar Cliente
**Como usar:**
1. Menu: **Clientes** → **Novo Cliente**
2. Aba **Dados Básicos**:
   - Nome / Razão Social
   - CPF / CNPJ
   - Email
   - Telefone
   - Celular
3. Aba **Endereço**:
   - CEP (busca automática)
   - Logradouro
   - Número
   - Complemento
   - Bairro
   - Cidade
   - Estado
4. Aba **Comercial**:
   - Vendedor responsável
   - Observações
5. Clique em **Salvar**

**Recursos especiais:**
- 🔍 **Busca CEP automática**: Preenche endereço
- ✅ **Validação de CPF/CNPJ**: Evita duplicatas
- 📝 **Campo de observações**: Notas importantes

#### 4.3 Ver Detalhes do Cliente
**Como usar:**
1. Na lista, clique no **nome do cliente**
2. Visualize:
   - **Dados cadastrais completos**
   - **Histórico de compras**
   - **Total comprado**
   - **Última compra**
   - **Vendedor responsável**

#### 4.4 Registrar Compra
**Como usar:**
1. Nos detalhes do cliente, clique em **Nova Compra**
2. Ou menu: **Clientes** → **Registrar Compra**
3. Preencha:
   - **Cliente**: Selecione da lista
   - **Data da compra**
   - **Valor total**: R$ 0,00
   - **Produto/Serviço**: Descrição
   - **Observações**: Detalhes adicionais
4. Clique em **Registrar**

**Efeitos:**
- ✅ Compra adicionada ao histórico
- ✅ Total de compras atualizado
- ✅ Conta para metas e comissões

#### 4.5 Importar Clientes (Excel)
**Como usar:**
1. Menu: **Clientes** → **Importar**
2. Baixe o **modelo de planilha**
3. Preencha as colunas:
   ```
   Nome | CPF/CNPJ | Email | Telefone | CEP | Logradouro | Número | Bairro | Cidade | Estado | Vendedor
   ```
4. Faça upload
5. Sistema valida e importa

**Validações:**
- ✅ CPF/CNPJ únicos
- ✅ Email válido
- ✅ CEP válido
- ✅ Vendedor existe
- ❌ Mostra erros para corrigir

#### 4.6 Exportar Clientes
**Como usar:**
1. Menu: **Clientes** → **Exportar**
2. Selecione filtros (opcional):
   - Período
   - Vendedor
   - Status
3. Clique em **Exportar Excel**
4. Baixe o arquivo

**Arquivo contém:**
- Todos os dados cadastrais
- Histórico de compras
- Total por cliente
- Vendedor responsável

#### 4.7 Relatório de Clientes
**Como usar:**
1. Menu: **Clientes** → **Relatórios**
2. Selecione o tipo:
   - **Por Vendedor**: Clientes de cada vendedor
   - **Por Período**: Novos clientes no período
   - **Top Clientes**: Maiores compradores
3. Defina filtros
4. Clique em **Gerar Relatório**

---

## 5. 👔 MÓDULO DE SUPERVISORES

### O que faz?
Gestão de supervisores e suas equipes de vendedores.

### Funcionalidades

#### 5.1 Listar Supervisores
**Como usar:**
1. Menu: **Supervisores** → **Listar**
2. Veja todos os supervisores
3. Informações exibidas:
   - Nome
   - Email
   - Quantidade de vendedores
   - Status

#### 5.2 Cadastrar Supervisor
**Como usar:**
1. Menu: **Supervisores** → **Novo**
2. Preencha:
   - Nome completo
   - Email
   - Telefone
3. Clique em **Salvar**

**Próximo passo:**
- Defina a senha de acesso
- Associe vendedores à equipe

#### 5.3 Definir Senha
**Como usar:**
1. Na lista, clique em **🔑 Definir Senha**
2. Digite nova senha (mínimo 6 caracteres)
3. Confirme a senha
4. Clique em **Salvar**

**Supervisor poderá:**
- ✅ Acessar dashboard de supervisor
- ✅ Ver sua equipe
- ✅ Acompanhar metas da equipe
- ✅ Ver comissões da equipe

#### 5.4 Associar Vendedores
**Como usar:**
1. Vá em **Vendedores** → **Editar Vendedor**
2. No campo **Supervisor**, selecione o supervisor
3. Salve

**Ou em lote:**
1. Importe planilha de vendedores
2. Coluna "Supervisor" com nome do supervisor
3. Sistema associa automaticamente

#### 5.5 Importar Supervisores
**Como usar:**
1. Menu: **Supervisores** → **Importar**
2. Baixe modelo Excel
3. Preencha: Nome | Email | Telefone
4. Faça upload
5. Sistema importa e cria logins

---

## 6. 👨‍💼 MÓDULO DE FUNCIONÁRIOS

### O que faz?
Cadastro e gestão de funcionários de diferentes departamentos.

### Funcionalidades

#### 6.1 Listar Funcionários
**Como usar:**
1. Menu: **Funcionários** → **Listar**
2. Veja todos os funcionários
3. Filtre por:
   - Departamento
   - Cargo
   - Status

**Informações exibidas:**
- Nome
- Email
- Departamento
- Cargo
- Status (ativo/inativo)

#### 6.2 Cadastrar Funcionário
**Como usar:**
1. Menu: **Funcionários** → **Novo**
2. Preencha:
   - **Nome completo**
   - **Email** (será o login)
   - **Senha** (se criar agora)
   - **Departamento**:
     - RH
     - Financeiro
     - Comercial
     - TI
     - Administrativo
   - **Cargo**:
     - Admin
     - Gerente
     - Supervisor
     - Vendedor
     - Técnico
     - Financeiro
     - RH
     - Usuário
3. Clique em **Salvar**

**Permissões por cargo:**
- **Admin**: Acesso total
- **Gerente**: Gestão comercial
- **Financeiro**: Relatórios e finanças
- **RH**: Gestão de pessoas
- **Técnico**: Ordens de serviço

#### 6.3 Editar Funcionário
**Como usar:**
1. Na lista, clique em **✏️ Editar**
2. Altere dados necessários
3. Salve

#### 6.4 Ativar/Desativar
**Como usar:**
1. Clique no botão **Ativar/Desativar**
2. Confirme

**Efeito:**
- ❌ Desativado: Não pode fazer login
- ✅ Ativado: Volta a ter acesso

---

## 7. 🎯 MÓDULO DE METAS

### O que faz?
Definição, acompanhamento e gestão de metas de vendas.

### Funcionalidades

#### 7.1 Definir Meta Individual
**Como usar:**
1. Menu: **Metas** → **Nova Meta**
2. Selecione:
   - **Vendedor**
   - **Mês/Ano**
   - **Valor da meta**: R$ 0,00
3. Clique em **Salvar**

**Dica:** Defina metas realistas e desafiadoras!

#### 7.2 Definir Meta de Equipe
**Como usar:**
1. Menu: **Metas** → **Meta de Equipe**
2. Selecione:
   - **Supervisor**
   - **Mês/Ano**
   - **Meta total da equipe**
3. Sistema divide proporcionalmente entre vendedores

#### 7.3 Acompanhar Metas
**Como usar:**
1. Menu: **Metas** → **Acompanhamento**
2. Veja:
   - **Meta estabelecida**
   - **Realizado até agora**
   - **% de atingimento**
   - **Faltam X dias**
   - **Média diária necessária**

**Indicadores visuais:**
- 🔴 **< 50%**: Atenção
- 🟡 **50-80%**: Atenção
- 🟢 **> 80%**: Parabéns!

#### 7.4 Metas Avançadas
**Tipos de meta:**
- **Faturamento**: Valor total de vendas
- **Ticket Médio**: Valor médio por venda
- **Quantidade**: Número de vendas
- **Novos Clientes**: Clientes novos captados

**Como usar:**
1. Menu: **Metas** → **Avançadas**
2. Escolha o tipo
3. Defina valores
4. Sistema calcula automaticamente

---

## 8. 💰 MÓDULO DE COMISSÕES

### O que faz?
Cálculo automático e gestão de comissões de vendedores.

### Funcionalidades

#### 8.1 Configurar Faixas de Comissão
**Como usar:**
1. Menu: **Comissões** → **Configurar Faixas**
2. Defina faixas de atingimento:
   ```
   0-50%   = 2% de comissão
   51-80%  = 3% de comissão
   81-100% = 5% de comissão
   >100%   = 7% de comissão + bônus
   ```
3. Salve a configuração

**Exemplo prático:**
- Meta: R$ 10.000
- Vendeu: R$ 8.500 (85%)
- Comissão: R$ 8.500 × 5% = R$ 425

#### 8.2 Cálculo Automático
**Quando acontece:**
- ✅ Ao registrar uma venda
- ✅ Ao final do mês
- ✅ Ao consultar relatórios

**Como verificar:**
1. Menu: **Comissões** → **Calcular**
2. Selecione período
3. Sistema calcula automaticamente

#### 8.3 Relatório de Comissões
**Como usar:**
1. Menu: **Comissões** → **Relatório**
2. Filtre por:
   - Vendedor
   - Período (mês/ano)
   - Status (pago/pendente)
3. Veja:
   - Meta do vendedor
   - Total vendido
   - % de atingimento
   - Comissão calculada

**Exportar:**
- Clique em **Exportar Excel**
- Baixe planilha para pagamento

#### 8.4 Comissão de Supervisor
**Como funciona:**
- Supervisor ganha % sobre comissão da equipe
- Exemplo: 10% das comissões dos vendedores

**Como configurar:**
1. Menu: **Comissões** → **Supervisor**
2. Defina percentual
3. Sistema calcula automaticamente

---

## 9. 📈 MÓDULO DE RELATÓRIOS

### O que faz?
Geração de relatórios gerenciais e operacionais.

### Relatórios Disponíveis

#### 9.1 Relatório de Vendas
**Como usar:**
1. Menu: **Relatórios** → **Vendas**
2. Filtre por:
   - Período (data inicial e final)
   - Vendedor
   - Cliente
   - Produto/Serviço
3. Clique em **Gerar**

**Informações exibidas:**
- Total de vendas
- Quantidade de vendas
- Ticket médio
- Vendas por vendedor
- Vendas por período
- Gráficos de evolução

#### 9.2 Relatório de Clientes
**Como usar:**
1. Menu: **Relatórios** → **Clientes**
2. Escolha tipo:
   - **Novos clientes**: Cadastrados no período
   - **Top clientes**: Maiores compradores
   - **Clientes inativos**: Sem compras há X dias
3. Gere o relatório

#### 9.3 Relatório de Performance
**Como usar:**
1. Menu: **Relatórios** → **Performance**
2. Veja:
   - Performance individual
   - Performance por equipe
   - Ranking de vendedores
   - Evolução mensal

**Gráficos:**
- 📊 Vendas por vendedor (barras)
- 📈 Evolução mensal (linha)
- 🥇 Ranking (podium)

#### 9.4 Exportar Relatórios
**Formatos disponíveis:**
- 📄 **PDF**: Para impressão
- 📊 **Excel**: Para análise
- 📧 **Email**: Enviar por email

**Como usar:**
1. Gere o relatório
2. Clique em **Exportar**
3. Escolha o formato
4. Baixe ou envie

---

## 10. 👑 MÓDULO DE SUPER ADMIN

### O que faz?
Gerenciamento multi-empresa e controle total do sistema.

**Acesso:** Apenas Super Administradores

### Funcionalidades

#### 10.1 Gerenciar Empresas
**Como usar:**
1. Menu: **Super Admin** → **Empresas**
2. Veja todas as empresas cadastradas
3. Ações disponíveis:
   - **Visualizar**: Detalhes da empresa
   - **Editar**: Alterar dados
   - **Bloquear**: Desabilitar acesso
   - **Excluir**: Remover empresa

**Informações exibidas:**
- Nome da empresa
- CNPJ
- Email do admin
- Data de cadastro
- Quantidade de usuários
- Status (ativa/bloqueada)

#### 10.2 Criar Nova Empresa
**Como usar:**
1. Menu: **Super Admin** → **Empresas** → **Nova**
2. Preencha:
   - Nome da empresa
   - CNPJ
   - Email do administrador
   - Senha inicial
3. Clique em **Criar**

**Sistema cria:**
- ✅ Empresa no banco
- ✅ Usuário admin
- ✅ Configurações padrão

#### 10.3 Gerenciar Usuários
**Como usar:**
1. Menu: **Super Admin** → **Usuários**
2. Veja todos os usuários de todas as empresas
3. Filtre por:
   - Empresa
   - Tipo (admin, gerente, vendedor, etc.)
   - Status (ativo/bloqueado)

**Ações:**
- **Bloquear**: Usuário não pode mais acessar
- **Deletar**: Remove permanentemente
- **Resetar senha**: Define nova senha

#### 10.4 Backups
**Como usar:**
1. Menu: **Super Admin** → **Backups**
2. Veja lista de backups disponíveis
3. Ações:
   - **Criar backup**: Gera novo backup
   - **Download**: Baixa backup
   - **Restaurar**: Restaura backup
   - **Deletar**: Remove backup

**Backup automático:**
- ✅ Configurável: diário, semanal, mensal
- ✅ Mantém últimos N backups
- ✅ Sincroniza com nuvem (opcional)

**Dica:** Configure backup automático!

#### 10.5 Monitoramento
**Como usar:**
1. Menu: **Super Admin** → **Monitoramento**
2. Veja:
   - Empresas ativas
   - Total de usuários
   - Total de vendedores
   - Vendas totais do sistema
   - Performance geral

---

## 11. 📦 MÓDULO DE ESTOQUE

### O que faz?
Controle de estoque de produtos e movimentações.

### Funcionalidades

#### 11.1 Cadastrar Produto
**Como usar:**
1. Menu: **Estoque** → **Produtos** → **Novo**
2. Preencha:
   - **Código**: SKU/Código interno
   - **Nome**: Descrição do produto
   - **Categoria**: Selecione
   - **Unidade**: UN, KG, L, etc.
   - **Estoque mínimo**: Alerta
   - **Estoque máximo**: Limite
   - **Preço custo**: R$
   - **Preço venda**: R$
3. Clique em **Salvar**

#### 11.2 Movimentar Estoque
**Tipos de movimentação:**
- **Entrada**: Compra de fornecedor
- **Saída**: Venda para cliente
- **Ajuste**: Correção de estoque
- **Transferência**: Entre locais
- **Perda**: Avaria/Vencimento

**Como usar:**
1. Menu: **Estoque** → **Movimentações** → **Nova**
2. Selecione:
   - **Tipo**: Entrada, Saída, etc.
   - **Produto**: Da lista
   - **Quantidade**: Número
   - **Motivo**: Descrição
3. Confirme

**Sistema atualiza:**
- ✅ Saldo do estoque
- ✅ Valor total
- ✅ Histórico de movimentações

#### 11.3 Inventário
**Como fazer:**
1. Menu: **Estoque** → **Inventário**
2. Conte fisicamente os produtos
3. Digite quantidades reais
4. Sistema compara com sistema
5. Gera ajustes automaticamente

#### 11.4 Alertas de Estoque
**Alertas automáticos:**
- 🔴 **Estoque mínimo**: Produto acabando
- 🟡 **Estoque zerado**: Produto esgotado
- 🟢 **Estoque OK**: Tudo certo

**Como visualizar:**
1. Menu: **Estoque** → **Alertas**
2. Veja produtos com baixo estoque
3. Tome ações necessárias

---

## 12. 💾 MÓDULO DE BACKUP

### O que faz?
Proteção de dados com backups automáticos e manuais.

### Funcionalidades

#### 12.1 Backup Automático
**Configuração:**
1. Menu: **Configurações** → **Backup**
2. Configure:
   - **Frequência**: Diária, Semanal, Mensal
   - **Horário**: Ex: 02:00
   - **Manter últimos**: Ex: 7 backups
   - **Limpeza automática**: Sim/Não
3. Salve

**Sistema faz:**
- ✅ Backup no horário definido
- ✅ Mantém histórico
- ✅ Remove backups antigos automaticamente
- ✅ Notifica em caso de erro

#### 12.2 Backup Manual
**Como fazer:**
1. Menu: **Super Admin** → **Backups**
2. Clique em **Criar Backup**
3. Aguarde processamento
4. Backup aparece na lista

**Quando fazer:**
- Antes de atualizações
- Antes de mudanças grandes
- Antes de importações em massa

#### 12.3 Restaurar Backup
**Como fazer:**
1. Menu: **Super Admin** → **Backups**
2. Na lista, selecione o backup
3. Clique em **Restaurar**
4. **⚠️ ATENÇÃO**: Todos os dados atuais serão substituídos!
5. Confirme

**Sistema restaura:**
- ✅ Banco de dados completo
- ✅ Todas as tabelas
- ✅ Todos os registros

**Dica:** Faça backup antes de restaurar!

#### 12.4 Download de Backup
**Como fazer:**
1. Menu: **Super Admin** → **Backups**
2. Clique em **⬇️ Download**
3. Salve arquivo em local seguro

**Guarde em:**
- ☁️ Nuvem (Google Drive, Dropbox)
- 💾 HD externo
- 📧 Email para você mesmo

---

## 🎨 LAYOUT E DESIGN

### Características

#### Responsivo
- 📱 **Mobile**: Otimizado para celular
- 💻 **Tablet**: Adapta ao tamanho
- 🖥️ **Desktop**: Aproveita tela grande

#### Profissional
- 🎨 **Cores**: Azul, branco, cinza
- ✨ **Ícones**: Bootstrap Icons
- 📊 **Gráficos**: Chart.js
- 🎯 **Cards**: Informações organizadas

#### Navegação
- 📋 **Menu lateral**: Acesso rápido
- 🔝 **Barra superior**: Usuário e notificações
- 🏠 **Breadcrumbs**: Sabe onde está
- ⚡ **Atalhos**: Ações rápidas

---

## 🔐 PERMISSÕES E SEGURANÇA

### Níveis de Acesso

| Perfil | Dashboard | Vendedores | Clientes | Metas | Comissões | Relatórios | Super Admin |
|--------|-----------|------------|----------|-------|-----------|------------|-------------|
| **Super Admin** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Admin** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Gerente** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Supervisor** | 📊 Próprio | 👁️ Equipe | ✅ | 👁️ Equipe | 👁️ Equipe | 👁️ Equipe | ❌ |
| **Vendedor** | 📱 Mobile | ❌ | 👁️ Próprio | 👁️ Próprio | 👁️ Próprio | ❌ | ❌ |
| **Financeiro** | 📊 Finanças | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ |
| **RH** | 👥 Pessoas | ✅ | ❌ | ❌ | ❌ | 👥 RH | ❌ |

**Legenda:**
- ✅ Acesso total
- ❌ Sem acesso
- 👁️ Apenas visualização
- 📊 Dashboard específico

---

## 🚀 DICAS DE USO

### Para Administradores
1. ✅ Configure backups automáticos
2. ✅ Defina metas realistas
3. ✅ Acompanhe performance semanalmente
4. ✅ Revise comissões mensalmente
5. ✅ Mantenha cadastros atualizados

### Para Gerentes
1. 📊 Acompanhe dashboard diariamente
2. 🎯 Ajuste metas conforme necessário
3. 👥 Motive equipe com metas atingíveis
4. 📈 Use relatórios para decisões
5. 💰 Valide comissões antes de pagar

### Para Supervisores
1. 👁️ Monitore sua equipe
2. 🤝 Dê suporte aos vendedores
3. 📞 Comunique-se frequentemente
4. 🎯 Ajude a bater metas
5. 🏆 Reconheça bons resultados

### Para Vendedores
1. 📱 Use app mobile
2. 📊 Acompanhe sua meta
3. 🎯 Foco nos resultados
4. 💰 Maximize comissões
5. 🏃 Seja proativo

---

## ❓ PERGUNTAS FREQUENTES

### Como recuperar senha?
1. Tela de login → "Esqueci minha senha"
2. Digite seu email
3. Use o token recebido
4. Defina nova senha

### Como adicionar vendedor?
1. Menu: Vendedores → Novo
2. Preencha dados
3. Salve
4. Depois crie login se necessário

### Como importar clientes?
1. Baixe modelo Excel
2. Preencha planilha
3. Importe via menu Clientes
4. Sistema valida e importa

### Como ver minhas comissões?
1. Faça login
2. Dashboard mostra comissão atual
3. Ou: Menu Comissões → Minhas Comissões

### Como gerar relatório?
1. Menu: Relatórios
2. Escolha tipo
3. Defina filtros
4. Clique em Gerar

### Sistema trava, o que fazer?
1. Atualize a página (F5)
2. Limpe cache do navegador
3. Tente outro navegador
4. Contate o administrador

---

## 📞 SUPORTE

### Contato
- **Email**: suporte@vendacerta.com.br
- **WhatsApp**: (11) 99999-9999
- **Horário**: Segunda a Sexta, 9h às 18h

### Links Úteis
- 📚 [Documentação Técnica](DOCUMENTACAO.md)
- 🚀 [Guia Rápido](GUIA_RAPIDO.md)
- 📹 [Vídeos Tutoriais](https://youtube.com/vendacerta)

---

**Sistema desenvolvido com ❤️ para facilitar sua gestão de vendas!**

**Versão 3.0 - Dezembro 2025**
