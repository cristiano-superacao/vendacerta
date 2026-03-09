# 🚀 Guia de Início Rápido - VendaCerta

> **Comece a usar o sistema em 5 minutos! Guia completo passo-a-passo para cada perfil de usuário.**

---

## 📋 Índice

- [Primeiro Acesso](#-primeiro-acesso)
- [Guia por Perfil](#-guia-por-perfil)
  - [Super Administrador](#-super-administrador)
  - [Administrador/Gerente](#-administradorgerente)
  - [Supervisor](#-supervisor)
  - [Vendedor](#-vendedor)
  - [Técnico](#-técnico)
- [Módulos Principais](#-módulos-principais)
- [Dúvidas Frequentes](#-dúvidas-frequentes)

---

## 🔐 Primeiro Acesso

### 1. Acessar o Sistema

**URL Produção**: [https://vendacerta.up.railway.app](https://vendacerta.up.railway.app)  
**URL Local**: http://127.0.0.1:5000 (desenvolvimento)

### 2. Credenciais Padrão

Por segurança, o sistema **não possui senha padrão** para o usuário administrador.

#### ✅ Como criar o primeiro Admin

Local (Windows/PowerShell):
```powershell
$env:ADMIN_EMAIL="admin@sistema.com"
$env:ADMIN_PASSWORD="SUA_SENHA_FORTE"
python scripts/create_admin.py
```

Produção (Railway):
```powershell
$env:ADMIN_EMAIL="admin@sistema.com"
$env:ADMIN_PASSWORD="SUA_SENHA_FORTE"
railway run python scripts/create_admin.py
```

Depois, faça login com `ADMIN_EMAIL` / `ADMIN_PASSWORD`.

> ⚠️ Para usuários não-admin criados/importados pelo sistema, pode existir senha temporária (`senha123`). Oriente a troca no primeiro acesso.

### 3. Criar Nova Conta

Se não tiver credenciais, clique em **"Criar conta agora"** na tela de login:

1. Preencha seus dados pessoais
2. Escolha um **e-mail válido** (será usado para login)
3. Crie uma **senha forte** (mínimo 8 caracteres)
4. Aguarde aprovação do administrador
5. Receberá acesso conforme o cargo atribuído

---

## 👥 Guia por Perfil

### 👑 Super Administrador

**O que você pode fazer:**
- ✅ Gerenciar **múltiplas empresas** (criar, editar, bloquear)
- ✅ Gerenciar **todos os usuários** do sistema
- ✅ Acessar **backups** e restaurações
- ✅ Ver **métricas globais** de todas as empresas
- ✅ Configurar **permissões granulares**

#### Primeiros Passos

##### 1. Criar Empresa
```
Menu → Super Admin → Empresas → Nova Empresa

Preencha:
- Nome da empresa
- CNPJ
- Endereço completo
- Contato
- Status (Ativa/Bloqueada)
```

##### 2. Criar Primeiro Administrador da Empresa
```
Menu → Super Admin → Usuários → Novo Usuário

Configure:
- Nome e e-mail
- Cargo: "Admin"
- Empresa: Selecione a empresa criada
- Permissões: Marque todas as permissões administrativas
- Senha inicial: Será enviada ao usuário
```

##### 3. Configurar Backups Automáticos
```
Menu → Super Admin → Backups → Configurar

Defina:
- Frequência: Diário/Semanal
- Horário: Preferência fora do horário comercial
- Retenção: Quantos backups manter
- Destino: Local/Nuvem
```

##### 4. Monitorar Sistema
```
Dashboard Super Admin:
- Total de empresas ativas
- Total de usuários cadastrados
- Espaço em disco
- Último backup
- Alertas e notificações
```

---

### 🏢 Administrador/Gerente

**O que você pode fazer:**
- ✅ Gerenciar **vendedores** e **supervisores**
- ✅ Criar e acompanhar **metas**
- ✅ Configurar **faixas de comissão**
- ✅ Ver **relatórios completos**
- ✅ Gerenciar **equipes** e **clientes**
- ✅ Importar/Exportar dados via **Excel**

#### Primeiros Passos

##### 1. Criar Estrutura de Equipes
```
Menu → Equipes → Nova Equipe

Preencha:
- Nome da equipe (ex: "Equipe São Paulo")
- Descrição
- Supervisor responsável
```

##### 2. Cadastrar Vendedores
```
Menu → Vendedores → Novo Vendedor

📝 OPÇÃO 1: Cadastro Manual
- Nome completo
- E-mail
- Telefone
- CPF
- Cargo: Vendedor
- Equipe: Selecione a equipe
- Supervisor: Selecione o supervisor

📊 OPÇÃO 2: Importação Excel
Menu → Vendedores → Importar
1. Baixe o modelo Excel
2. Preencha com dados dos vendedores
3. Faça upload do arquivo
4. Revise os dados importados
5. Confirme importação
```

##### 3. Configurar Faixas de Comissão
```
Menu → Metas → Configurar Comissões

Exemplo de Configuração:
┌─────────────┬─────────┬─────────┬──────┐
│ Faixa       │ Mín (%) │ Máx (%) │ Taxa │
├─────────────┼─────────┼─────────┼──────┤
│ Crítica     │    0    │   50    │  1%  │
│ Baixa       │   50    │   75    │  2%  │
│ Meta        │   75    │  100    │  3%  │
│ Boa         │  100    │  125    │  4%  │
│ Excelente   │  125    │  999    │  5%  │
└─────────────┴─────────┴─────────┴──────┘

💡 Dica: Comece com estas faixas e ajuste conforme necessidade
```

##### 4. Criar Metas Mensais
```
Menu → Metas → Nova Meta

Para CADA vendedor:
- Selecione o vendedor
- Mês/Ano: Janeiro/2025
- Valor da Meta: R$ 50.000,00
- Receita Alcançada: R$ 0 (atualizar depois)
- Sistema calculará comissão automaticamente

💡 Dica: Use "Importar Metas" para cadastrar várias de uma vez via Excel
```

##### 5. Importar Base de Clientes
```
Menu → Clientes → Importar

Formatos suportados:
- Formato Simples: 11 colunas (dados básicos)
- Formato Estendido: 18 colunas (com endereço)
- Formato Completo: 23 colunas (todos os dados)

Passos:
1. Baixe modelo Excel compatível
2. Preencha com dados dos clientes
3. Valide CPF/CNPJ e códigos únicos
4. Faça upload
5. Sistema cria/atualiza automaticamente
```

##### 6. Acompanhar Performance
```
Dashboard Principal:
- Ranking de vendedores (tempo real)
- Total vendido no mês
- Meta da empresa vs. Alcançado
- Gráficos de evolução
- Top 5 vendedores

Filtros disponíveis:
- Por mês/ano
- Por equipe
- Por supervisor
```

---

### 🎯 Supervisor

**O que você pode fazer:**
- ✅ Gerenciar sua **equipe de vendedores**
- ✅ Criar e atualizar **metas** dos seus vendedores
- ✅ Ver **relatórios** da equipe
- ✅ Aprovar **ordens de serviço**
- ✅ Gerenciar **clientes** da equipe

#### Primeiros Passos

##### 1. Acessar Dashboard Supervisor
```
Após login → Redirecionado automaticamente

Você verá:
- Performance da sua equipe
- Ranking dos seus vendedores
- Metas individuais e status
- Ordens de serviço pendentes
- Alertas e notificações
```

##### 2. Acompanhar Vendedores
```
Menu → Vendedores

Visualize:
- Lista completa da sua equipe
- Status de cada vendedor (Ativo/Inativo)
- Metas atuais e histórico
- Performance individual

Ações disponíveis:
- Editar dados do vendedor
- Atualizar meta mensal
- Ver histórico de vendas
- Resetar senha (se necessário)
```

##### 3. Atualizar Receitas Alcançadas
```
Menu → Metas → [Selecione vendedor] → Editar

Atualize:
- Receita Alcançada: R$ 42.500,00
- Sistema recalcula automaticamente:
  * Percentual: (42.500 / 50.000) × 100 = 85%
  * Faixa: "Meta" (75-100%)
  * Comissão: R$ 42.500 × 3% = R$ 1.275,00

💡 Faça isso semanalmente para acompanhamento preciso
```

##### 4. Aprovar Ordens de Serviço
```
Menu → Ordens de Serviço → Pendentes de Aprovação

Para cada OS:
1. Revise diagnóstico do técnico
2. Verifique peças utilizadas
3. Confirme custo total
4. Aprove ou solicite correções

Status da OS:
- Aberta → Andamento → Concluída → Aprovada
```

##### 5. Gerenciar Clientes da Equipe
```
Menu → Clientes

Filtro automático: Apenas clientes da sua equipe

Você pode:
- Ver detalhes completos
- Editar informações
- Registrar nova compra
- Ver histórico de compras
- Exportar lista (CSV)
```

---

### 💼 Vendedor

**O que você pode fazer:**
- ✅ Ver suas **metas** e **comissões**
- ✅ Ver **ranking** de vendedores
- ✅ Gerenciar **seus clientes**
- ✅ Registrar **vendas/compras**
- ✅ Criar **ordens de serviço**

#### Primeiros Passos

##### 1. Acessar Dashboard Vendedor
```
Após login → Dashboard personalizado

Você verá:
- Sua meta do mês atual
- Receita alcançada até agora
- Percentual de alcance
- Comissão prevista
- Sua posição no ranking
- Gráfico de evolução mensal
```

##### 2. Ver Metas e Comissões
```
Menu → Minhas Metas

Detalhes:
- Meta Individual: R$ 50.000,00
- Receita Atual: R$ 38.000,00
- Falta para Meta: R$ 12.000,00
- Percentual: 76%
- Faixa Atual: "Meta" (3%)
- Comissão Prevista: R$ 1.140,00

📊 Histórico:
- Janeiro: 92% - R$ 1.380,00
- Dezembro: 108% - R$ 2.160,00
- Novembro: 85% - R$ 1.275,00
```

##### 3. Gerenciar Clientes
```
Menu → Clientes → Meus Clientes

Filtro automático: Apenas seus clientes

Ações:
- Cadastrar novo cliente
- Editar dados de cliente existente
- Ver histórico de compras
- Registrar nova venda

⚠️ Nota: Você NÃO pode exportar lista de clientes (restrição de segurança)
```

##### 4. Registrar Nova Venda
```
Opção 1: Via Cliente Existente
Menu → Clientes → [Selecione cliente] → Registrar Compra

Opção 2: Criar Cliente + Venda
Menu → Clientes → Novo Cliente
- Preencha dados do cliente
- Após salvar, clique em "Registrar Compra"

Dados da Compra:
- Produto/Serviço vendido
- Valor da venda
- Data da compra
- Forma de pagamento
- Observações

💡 Esta venda será contabilizada na sua meta automaticamente
```

##### 5. Criar Ordem de Serviço
```
Menu → Ordens de Serviço → Nova OS

Preencha:
- Cliente: Selecione da lista
- Descrição do problema
- Prioridade: Alta/Média/Baixa
- Categoria: Instalação/Manutenção/Reparo
- Observações

Após criação:
- Técnico será notificado
- Você pode acompanhar status
- Receberá notificação quando concluída
```

##### 6. Consultar Ranking
```
Dashboard → Seção "Ranking"

Visualize:
- Sua posição entre todos os vendedores
- Top 5 do mês
- Diferença de performance para o líder
- Evolução (subiu/desceu posições)

💪 Use para motivação e planejamento!
```

---

### 🔧 Técnico

**O que você pode fazer:**
- ✅ Ver **ordens de serviço** atribuídas a você
- ✅ Atualizar **status** das OS
- ✅ Registrar **diagnóstico** e **solução**
- ✅ Informar **peças utilizadas**
- ✅ Gerar **PDF** da OS concluída

#### Primeiros Passos

##### 1. Acessar Dashboard Técnico
```
Após login → Dashboard personalizado

Você verá:
- OS abertas aguardando você
- OS em andamento
- OS concluídas hoje
- Avaliação média (estrelas)
```

##### 2. Aceitar e Iniciar OS
```
Menu → Ordens de Serviço → Abertas

Para cada OS:
1. Revise descrição do problema
2. Verifique prioridade e cliente
3. Clique em "Aceitar e Iniciar"
4. Status muda: Aberta → Andamento
```

##### 3. Atualizar Andamento da OS
```
Menu → OS → [Selecione OS] → Atualizar

Preencha conforme avança:
- Diagnóstico: "Problema identificado na placa X"
- Solução aplicada: "Substituição da peça Y"
- Peças utilizadas: "Placa X - R$ 150,00"
- Tempo gasto: 2 horas
- Observações técnicas

💡 Atualize sempre que houver progresso
```

##### 4. Finalizar OS
```
Quando concluir o serviço:

Menu → OS → [Selecione OS] → Finalizar

Confirme:
- Diagnóstico final completo
- Todas as peças registradas
- Solução detalhada
- Custo total calculado

Após finalizar:
- Status: Andamento → Concluída
- Supervisor receberá notificação para aprovar
- Cliente poderá avaliar o serviço
```

##### 5. Gerar PDF da OS
```
Após aprovação do supervisor:

Menu → OS → [OS aprovada] → Gerar PDF

PDF conterá:
- Dados do cliente
- Descrição do problema
- Diagnóstico técnico
- Solução aplicada
- Peças e custos
- Assinatura técnico
- Avaliação do cliente (se já avaliada)

💡 Envie este PDF ao cliente por e-mail
```

---

## 📚 Módulos Principais

### 📊 Dashboard

**Acesso**: Tela inicial após login (varia por cargo)

**Dashboards Disponíveis**:

#### Dashboard Admin/Gerente
```
Métricas Gerais:
- Total de vendedores ativos
- Meta da empresa (soma todas as metas)
- Receita total alcançada
- Percentual geral de alcance

Ranking Completo:
- Top 10 vendedores do mês
- Ordenado por percentual de alcance
- Badges coloridos por faixa de comissão

Gráficos:
- Evolução mensal de vendas (12 meses)
- Distribuição de vendedores por faixa
- Comparativo meta vs. realizado
```

#### Dashboard Supervisor
```
Métricas da Equipe:
- Total de vendedores na equipe
- Meta da equipe (soma das metas)
- Receita da equipe
- Comissão prevista do supervisor

Ranking da Equipe:
- Todos os vendedores da equipe
- Performance individual
- Alertas de vendedores abaixo de 50%

OS da Equipe:
- Pendentes de aprovação
- Em andamento
- Concluídas no mês
```

#### Dashboard Vendedor
```
Métricas Individuais:
- Minha meta do mês
- Receita alcançada
- Falta para bater meta
- Comissão prevista

Meu Ranking:
- Minha posição geral
- Top 5 do mês
- Distância para o líder

Gráfico Pessoal:
- Evolução dos últimos 6 meses
- Comparativo com meta
```

---

### 💼 Vendedores

**Quem acessa**: Admin, Gerente, Supervisor

#### Listar Vendedores
```
Menu → Vendedores

Visualização:
- Cards responsivos (mobile) ou tabela (desktop)
- Foto, nome, e-mail, telefone
- Equipe e supervisor
- Status (Ativo/Inativo)
- Ações rápidas (Editar, Deletar, Permissões)

Filtros:
- Por equipe
- Por supervisor
- Por status
- Busca por nome/e-mail
```

#### Criar Vendedor
```
Menu → Vendedores → Novo

Dados Obrigatórios:
- Nome completo
- E-mail (único)
- Telefone
- CPF (único)

Dados Opcionais:
- Foto (upload)
- Data de nascimento
- Endereço completo
- Equipe
- Supervisor
- Comissão fixa (se houver)

Vínculo de Login:
- Criar usuário automaticamente
- Definir permissões do cargo "Vendedor"
- Senha inicial: será enviada por e-mail
```

#### Importar Vendedores (Excel)
```
Menu → Vendedores → Importar

Formato do Excel:
- Nome, E-mail, Telefone, CPF (obrigatórios)
- Equipe_ID, Supervisor_ID (opcionais)
- Endereço, Cidade, UF (opcionais)

Sistema:
- Valida duplicatas (e-mail/CPF)
- Cria usuários automaticamente
- Gera senhas aleatórias
- Envia e-mail de boas-vindas

Resultado:
- "15 vendedores criados, 3 atualizados, 2 erros"
- Lista de erros detalhada
```

---

### 🎯 Metas

**Quem acessa**: Admin, Gerente, Supervisor (própria equipe)

#### Listar Metas
```
Menu → Metas

Visualização:
- Tabela com vendedor, meta, receita, %, comissão
- Badges coloridos por faixa
- Status de pagamento (Pendente/Pago)

Filtros:
- Por mês/ano
- Por equipe
- Por vendedor
- Por faixa de comissão

Ações em Massa:
- Marcar como pagas
- Exportar PDF relatório
- Exportar Excel
```

#### Criar Meta Individual
```
Menu → Metas → Nova Meta

Configuração:
1. Selecione vendedor
2. Mês/Ano: Fevereiro/2025
3. Valor da Meta: R$ 60.000,00
4. Receita Alcançada: R$ 0 (pode deixar zero)

Sistema calcula automaticamente:
- Percentual: 0%
- Faixa: "Crítica" (0-50%)
- Comissão: R$ 0
- Status: "Pendente"

💡 Depois, edite para atualizar receita conforme vendas
```

#### Importar Metas em Massa
```
Menu → Metas → Importar

Formato Excel:
- Vendedor_ID ou Vendedor_Email
- Mes (1-12)
- Ano (2025)
- Valor_Meta (numérico)
- Receita_Alcancada (opcional, padrão 0)

Exemplo:
| Email | Mes | Ano | Meta |
|-------|-----|-----|------|
| joao@empresa.com | 1 | 2025 | 50000 |
| maria@empresa.com | 1 | 2025 | 60000 |

Sistema:
- Valida existência dos vendedores
- Calcula comissões automaticamente
- Cria ou atualiza metas existentes
```

#### Configurar Faixas de Comissão
```
Menu → Metas → Configurar Comissões

Cada Faixa tem:
- Nome (ex: "Excelente")
- Alcance Mínimo (%)
- Alcance Máximo (%)
- Taxa de Comissão (0.01 = 1%)
- Cor do Badge (success, warning, danger...)
- Ordem de exibição
- Ativa (Sim/Não)

Exemplo Prático:
Vendedor atingiu 112% da meta com R$ 56.000
- Faixa: "Boa" (100-125%)
- Taxa: 4%
- Comissão: R$ 56.000 × 0,04 = R$ 2.240,00
```

---

### 💰 Comissões

**Quem acessa**: Admin, Gerente

#### Visualizar Comissões
```
Menu → Relatórios → Comissões

Filtros:
- Por período (mês/ano)
- Por vendedor
- Por status (Pendente/Pago/Cancelado)

Totalizadores:
- Total de comissões do período
- Total pago
- Total pendente
- Média de comissão por vendedor

Ações:
- Marcar como "Pago"
- Gerar comprovante PDF
- Exportar relatório Excel
```

#### Configurar Comissões Especiais
```
Menu → Configurações → Comissões Especiais

Vendedor Individual:
- Sobrescrever faixas gerais
- Definir comissão fixa (%)
- Definir bônus adicional

Supervisor:
- Comissão sobre vendas da equipe (ex: 1%)
- Bônus por meta da equipe (ex: R$ 500 se equipe atingir 100%)
```

---

### 👥 Clientes

**Quem acessa**: Admin, Gerente, Supervisor, Vendedor

#### Listar Clientes
```
Menu → Clientes

Visualização por Cargo:
- Admin/Gerente: Todos os clientes da empresa
- Supervisor: Clientes da equipe
- Vendedor: Apenas seus clientes

Informações exibidas:
- Nome/Razão Social
- CPF/CNPJ
- Telefone
- E-mail
- Cidade/UF
- Última compra
- Total gasto

Filtros:
- Por cidade
- Por vendedor responsável
- Por período de cadastro
- Busca por nome/CPF/CNPJ
```

#### Cadastrar Cliente
```
Menu → Clientes → Novo

Dados Básicos (obrigatórios):
- Nome ou Razão Social
- CPF ou CNPJ (validação automática)
- Telefone
- E-mail

Dados Complementares:
- Inscrição Estadual
- Data de Nascimento
- Endereço completo (CEP, Logradouro, Número, Bairro, Cidade, UF)
- Coordenadas geográficas (latitude/longitude)
- Observações

Vínculo:
- Vendedor responsável (automático se você for vendedor)
```

#### Importar Clientes (3 Formatos)
```
Menu → Clientes → Importar

Formato 1: Simples (11 colunas)
- Código, Nome, CPF/CNPJ, Telefone, E-mail
- Cidade, UF, Endereço, Número, Bairro, CEP

Formato 2: Estendido (18 colunas)
- Simples + Razão Social, Inscrição Estadual
- Data Nascimento, Complemento, Observações

Formato 3: Completo (23 colunas)
- Estendido + Latitude, Longitude
- Vendedor_ID, Data_Cadastro, Ativo

Sistema:
- Detecta formato automaticamente
- Valida CPF/CNPJ (check digit)
- Valida códigos únicos
- Atualiza se cliente já existir (por código)
- Cria se não existir

Resultado:
"✅ 45 clientes criados, 12 atualizados, 3 erros (CPF inválido)"
```

#### Registrar Compra
```
Menu → Clientes → [Selecione cliente] → Registrar Compra

Dados:
- Data da compra
- Produto/Serviço
- Valor (R$)
- Quantidade
- Forma de pagamento
- Observações

Efeitos:
- Compra vinculada ao cliente
- Contabilizada na meta do vendedor responsável
- Atualiza "Última compra" do cliente
- Incrementa "Total gasto"
```

#### Exportar Clientes
```
Menu → Clientes → Exportar

Permissão:
✅ Admin, Gerente, Supervisor
❌ Vendedor (bloqueado por segurança)

Formato: CSV
Dados exportados:
- Todos os campos do cliente
- Vendedor responsável
- Total de compras
- Última compra

Filtros aplicados:
- Exporta apenas clientes visíveis com filtros ativos
```

---

### 📦 Estoque

**Quem acessa**: Admin, Gerente, Técnico, Administrativo

#### Dashboard Estoque
```
Menu → Estoque

Cards de Resumo:
- Total de produtos cadastrados
- Valor total do estoque
- Produtos em estoque baixo (alerta)
- Produtos zerados (crítico)

Últimas Movimentações:
- 10 movimentações mais recentes
- Tipo (Entrada/Saída/Ajuste)
- Produto, Quantidade, Responsável
```

#### Gerenciar Produtos
```
Menu → Estoque → Produtos

Lista de Produtos:
- Código, Nome, Categoria
- Quantidade em estoque
- Preço de custo
- Preço de venda
- Margem (%)
- Status (Ativo/Inativo)

Alertas visuais:
- 🔴 Estoque zerado
- 🟡 Estoque baixo (< 10 unidades)
- 🟢 Estoque ok
```

#### Cadastrar Produto
```
Menu → Estoque → Produtos → Novo

Dados:
- Código (único)
- Nome
- Descrição
- Categoria
- Unidade (UN, CX, PC, KG...)
- Preço de custo
- Preço de venda
- Estoque inicial
- Estoque mínimo (para alerta)
- Localização física (prateleira/depósito)
- Foto (opcional)

Sistema calcula:
- Margem: ((Venda - Custo) / Custo) × 100
```

#### Registrar Movimentação
```
Menu → Estoque → Movimentações → Nova

Tipos de Movimentação:

1. ENTRADA (Compra de fornecedor)
   - Produto
   - Quantidade
   - Custo unitário
   - Fornecedor
   - Nota fiscal

2. SAÍDA (Venda/Consumo)
   - Produto
   - Quantidade
   - Cliente/OS vinculada
   - Motivo

3. AJUSTE (Inventário/Correção)
   - Produto
   - Quantidade (positiva ou negativa)
   - Motivo do ajuste
   - Responsável

Sistema atualiza:
- Estoque atual
- Valor total do estoque
- Histórico de movimentações
```

#### Importar Produtos (Excel)
```
Menu → Estoque → Importar Produtos

Formato:
- Código, Nome, Categoria, Unidade
- Preco_Custo, Preco_Venda
- Estoque_Inicial, Estoque_Minimo
- Localizacao (opcional)

Sistema:
- Valida códigos únicos
- Calcula margem automaticamente
- Cria produtos novos
- Atualiza preços se produto existir
```

---

### 🔧 Ordens de Serviço (OS)

**Quem acessa**: Todos (permissões variadas)

#### Listar OS
```
Menu → Ordens de Serviço

Visualização por Cargo:
- Admin/Gerente: Todas as OS da empresa
- Supervisor: OS da equipe
- Vendedor: OS que ele criou
- Técnico: OS atribuídas a ele
- Cliente: Suas próprias OS (via portal)

Status das OS:
- 🟡 Aberta (criada, aguardando técnico)
- 🔵 Andamento (técnico trabalhando)
- 🟢 Concluída (técnico finalizou)
- ✅ Aprovada (supervisor aprovou)
- ⭐ Avaliada (cliente avaliou)
- ❌ Cancelada
```

#### Criar Nova OS
```
Menu → OS → Nova

Dados Iniciais:
- Cliente (busca por nome/CPF)
- Descrição do problema
- Categoria: Instalação/Manutenção/Reparo/Garantia
- Prioridade: Baixa/Média/Alta/Urgente
- Data desejada
- Observações

Sistema:
- Cria OS com status "Aberta"
- Notifica técnicos disponíveis
- Gera número único da OS
```

#### Atualizar OS (Técnico)
```
Menu → OS → [Selecione OS] → Atualizar

Durante execução:
- Diagnóstico técnico detalhado
- Solução aplicada
- Peças utilizadas (busca no estoque)
- Tempo gasto (horas)
- Fotos (antes/depois)
- Observações técnicas

Ao finalizar:
- Mudar status para "Concluída"
- Calcular custo total:
  * Peças (soma preços do estoque)
  * Mão de obra (horas × valor/hora)
  * Total = Peças + Mão de obra
```

#### Aprovar OS (Supervisor)
```
Menu → OS → Pendentes de Aprovação

Para cada OS:
1. Revise diagnóstico e solução
2. Confirme peças utilizadas (estoque)
3. Valide custo total
4. Adicione observações se necessário

Aprovar:
- Status: Concluída → Aprovada
- Cliente recebe notificação para avaliar

Reprovar:
- Retorna para técnico com comentários
- Status: Concluída → Andamento
```

#### Avaliar OS (Cliente)
```
Portal Cliente → Minhas OS → [OS aprovada] → Avaliar

Avaliação:
- Nota: 1 a 5 estrelas
- Comentário sobre o atendimento
- Rapidez: 1-5
- Qualidade: 1-5
- Atendimento: 1-5

Após avaliar:
- Status: Aprovada → Avaliada
- Técnico recebe feedback
- Média do técnico é atualizada
```

#### Gerar PDF da OS
```
Menu → OS → [Selecione OS] → Gerar PDF

PDF contém:
┌─────────────────────────────────────┐
│ ORDEM DE SERVIÇO #12345             │
├─────────────────────────────────────┤
│ Cliente: João Silva                 │
│ Telefone: (11) 99999-9999           │
│                                     │
│ Problema: Impressora não liga       │
│ Diagnóstico: Fonte queimada         │
│ Solução: Troca de fonte             │
│                                     │
│ Peças Utilizadas:                   │
│ - Fonte 12V/2A ....... R$ 45,00     │
│                                     │
│ Mão de Obra .......... R$ 80,00     │
│ ─────────────────────────────────── │
│ TOTAL ................ R$ 125,00    │
│                                     │
│ Técnico: Carlos Santos              │
│ Aprovado por: Ana Silva (Sup.)      │
│                                     │
│ Avaliação: ⭐⭐⭐⭐⭐ (5.0)            │
│ Comentário: "Ótimo atendimento!"    │
└─────────────────────────────────────┘

Assinatura Cliente: _______________
```

---

## ❓ Dúvidas Frequentes (FAQ)

### Autenticação e Acesso

**P: Esqueci minha senha. Como recuperar?**
```
R: Na tela de login:
1. Clique em "Esqueci minha senha"
2. Digite seu e-mail cadastrado
3. Você receberá um link de redefinição
4. Link válido por 24 horas
5. Crie uma nova senha forte
```

**P: Posso ter mais de um cargo?**
```
R: Não diretamente. Cada usuário tem 1 cargo principal.
   Mas você pode ter permissões granulares customizadas.
   
   Exemplo: Um "Vendedor" pode ter permissão adicional
   "pode_gerenciar_estoque" se necessário.
```

**P: Como alterar minha senha?**
```
R: Após login:
Menu → Meu Perfil → Alterar Senha

Requisitos da senha:
- Mínimo 8 caracteres
- Pelo menos 1 letra maiúscula
- Pelo menos 1 número
- Recomendado: símbolos (!@#$%...)
```

---

### Metas e Comissões

**P: Como o sistema calcula a comissão?**
```
R: Fórmula:
1. Percentual = (Receita Alcançada / Meta) × 100
2. Busca faixa onde Alcance_Min ≤ Percentual ≤ Alcance_Max
3. Comissão = Receita Alcançada × Taxa da Faixa

Exemplo:
- Meta: R$ 50.000
- Receita: R$ 53.000
- Percentual: 106%
- Faixa: "Boa" (100-125%, taxa 4%)
- Comissão: R$ 53.000 × 0,04 = R$ 2.120,00
```

**P: Posso ter metas diferentes para cada vendedor?**
```
R: Sim! Cada vendedor tem sua própria meta mensal.
   Você pode definir valores diferentes baseado em:
   - Experiência do vendedor
   - Região de atuação
   - Tipo de produto vendido
```

**P: Como funciona a comissão do supervisor?**
```
R: Sistema separado do vendedor:

Vendedor:
- Comissão sobre receita individual (ex: 3% de R$ 53.000)

Supervisor:
- Comissão sobre total da equipe (ex: 1% de R$ 250.000)
- Configurado em Menu → Metas → Configurar Comissões → Supervisor
```

---

### Importação de Dados

**P: Minha importação deu erro. O que fazer?**
```
R: Verifique:

1. Formato do arquivo: Deve ser .xlsx (não .xls ou .csv)
2. Colunas obrigatórias presentes
3. Dados válidos:
   - CPF/CNPJ com 11/14 dígitos válidos
   - E-mails no formato correto
   - Datas no formato DD/MM/YYYY
4. Sem linhas em branco no meio
5. Primeira linha deve ser o cabeçalho

Dica: Baixe o modelo e copie seus dados para ele.
```

**P: Posso atualizar dados importando o Excel novamente?**
```
R: Sim! Sistema detecta por chave única:

Clientes: Código do cliente
Vendedores: E-mail ou CPF
Produtos: Código do produto

Se encontrar, ATUALIZA.
Se não encontrar, CRIA NOVO.
```

**P: Excel não está disponível. Como habilitar?**
```
R: Verifique o status em /status/excel

Se indisponível:
1. Instalar pandas: pip install pandas
2. Instalar openpyxl: pip install openpyxl
3. Reiniciar aplicação

Em produção (Railway), dependências são instaladas automaticamente.
```

---

### Relatórios e Exportação

**P: Posso exportar relatórios em PDF?**
```
R: Sim! Disponível em:

- Dashboard: Exportar Dashboard (snapshot completo)
- Metas: Exportar Relatório de Metas (mês específico)
- OS: Gerar PDF individual de cada OS
- Comissões: Comprovante de pagamento

Formato: PDF profissional com logo e dados completos
```

**P: Como exportar lista de clientes?**
```
R: Menu → Clientes → Exportar

Permissão necessária:
✅ Admin, Gerente, Supervisor (podem exportar)
❌ Vendedor (bloqueado por segurança)

Formato: CSV (abrir no Excel)
Dados: Todos os campos + vendedor responsável
```

**P: Quais relatórios estão disponíveis?**
```
R: Principais relatórios:

1. Relatório de Metas (Excel/PDF)
   - Todos os vendedores
   - Meta, Receita, Comissão
   - Filtro por mês/equipe

2. Relatório de Vendas (Excel)
   - Histórico de compras
   - Por cliente/vendedor/período

3. Relatório de Estoque (Excel)
   - Produtos, quantidades, valores
   - Movimentações detalhadas

4. Relatório de OS (PDF)
   - Ordens concluídas
   - Por técnico/período/status
```

---

### Permissões e Segurança

**P: Um vendedor pode ver dados de outros vendedores?**
```
R: Não. Isolamento automático:

Vendedor vê apenas:
- Suas próprias metas
- Seus próprios clientes
- Ranking geral (mas sem detalhes alheios)
- Suas próprias OS

Exceção: Supervisor vê toda a equipe
```

**P: Como dar permissão especial a um usuário?**
```
R: Menu → Vendedores/Funcionários → [Usuário] → Permissões

Marque/desmarque as 24 permissões granulares:
- pode_gerenciar_vendedores
- pode_gerenciar_metas
- pode_ver_relatorios
- pode_exportar_clientes
- pode_gerenciar_estoque
- ... (e outras 19)

Sistema valida em tempo real.
```

**P: Posso ter múltiplas empresas no mesmo sistema?**
```
R: Sim! Sistema multi-tenant:

Super Admin:
- Cria múltiplas empresas
- Cada empresa tem seus próprios dados isolados
- Usuários pertencem a UMA empresa

Isolamento total:
- Empresa A não vê dados da Empresa B
- Banco de dados compartilhado, mas filtrado por empresa_id
```

---

### Performance e Otimização

**P: Sistema está lento. O que fazer?**
```
R: Diagnóstico rápido:

1. Verifique conexão com internet/banco
2. Limpe cache do navegador (Ctrl+Shift+Del)
3. Verifique filtros aplicados (muitos dados carregando)
4. Contate suporte se problema persistir

Administrador pode:
- Verificar logs em Railway
- Analisar queries lentas no banco
- Ativar cache de relatórios
```

**P: Posso usar o sistema offline?**
```
R: Parcialmente. Como PWA:

Offline:
- Dashboard (dados em cache)
- Visualizar metas/clientes (cache)

Requer conexão:
- Criar/editar dados
- Importar/exportar
- Ver relatórios atualizados

Dica: Instale o PWA no celular para melhor performance.
```

---

## 🆘 Precisa de Ajuda?

### 📚 Documentação Adicional
- 🏗️ [Arquitetura do Sistema](ARCHITECTURE.md)
- 🌐 [Documentação da API](API.md)
- 📖 [README Principal](../README.md)

### 🔗 Links Úteis
- 🌐 **Sistema**: [vendacerta.up.railway.app](https://vendacerta.up.railway.app)
- 🐙 **GitHub**: [cristiano-superacao/vendacerta](https://github.com/cristiano-superacao/vendacerta)

### 💬 Suporte
Entre em contato com seu administrador do sistema ou abra uma issue no GitHub.

---

<div align="center">

**VendaCerta v2.0.0 - Guia de Início Rápido**  
Última atualização: Dezembro 2024

[⬅️ Voltar ao README](../README.md) | [📚 Documentação Completa](../INDICE_DOCUMENTACAO.md)

</div>
