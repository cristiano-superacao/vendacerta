# 📚 MANUAL RESUMIDO DE MÓDULOS - VENDA CERTA

Este manual oferece uma visão rápida de **como usar cada módulo principal**
do sistema, com passos práticos. Para detalhes completos, consulte o
**MANUAL COMPLETO DE MÓDULOS** em:

- docs/archive/MANUAL_COMPLETO_MODULOS.md

---

## 1️⃣ Autenticação

**O que faz:** Login, criação de conta e controle de sessão.

**Como usar:**
- Acessar a URL do sistema → tela de login.
- Informar **email** e **senha** → **Entrar**.
- Link "Criar conta" para registrar nova empresa/usuário (quando habilitado).
- Link "Esqueci minha senha" para fluxo de recuperação.

**Perfis principais:** Super Admin, Admin, Gerente, Supervisor, Vendedor,
Técnico, Financeiro, RH, Auxiliar.

---

## 2️⃣ Dashboard

**O que faz:** Mostra indicadores e gráficos de desempenho por cargo.

**Como usar (Admin/Gerente):**
- Após login, visualizar cards com vendas, metas, comissões e ranking.
- Filtrar por período (mês/ano) no topo da tela.
- Clicar em links/atalhos para abrir relatórios detalhados.

**Como usar (Supervisor/Vendedor):**
- Supervisor: vê performance da equipe e metas por vendedor.
- Vendedor: vê suas próprias metas, vendas e comissão prevista.

---

## 3️⃣ Vendedores

**O que faz:** Cadastro e gestão de vendedores e seus acessos.

**Passo a passo:**
- Menu lateral → **Vendedores** → **Listar Vendedores**.
- Botão **Novo Vendedor** para cadastrar:
  - Nome, email, telefone, CPF, supervisor, status.
- Ações na lista:
  - **Editar** dados, **Ativar/Desativar**, **Criar Login**, **Resetar Senha**.

Uso típico:
- Criar vendedores, associar a supervisores/equipes e entregar acesso ao app.

---

## 4️⃣ Clientes (CRM)

**O que faz:** Cadastro, listagem, filtro e importação de clientes.

**Passo a passo principal:**
- Menu → **Clientes** → **Listar Clientes**:
  - Filtros por nome, vendedor, status, período.
  - Lista paginada com dados principais (nome, CPF/CNPJ, contato, endereço).
- **Novo Cliente**:
  - Preencher dados básicos, vincular vendedor responsável.
- **Importar Excel** (quando habilitado):
  - Baixar modelo de planilha.
  - Preencher dados conforme colunas.
  - Enviar arquivo e conferir relatório de validação.

---

## 5️⃣ Supervisores e Funcionários

**O que faz:** Gestão de supervisores e demais cargos (técnicos, auxiliares, etc.).

**Como usar:**
- Menu → **Supervisores** / **Funcionários**.
- Cadastrar supervisores com vínculo à empresa.
- Associar vendedores e equipes a supervisores.
- Definir cargos específicos (supervisor_manutencao, tecnico, auxiliar, etc.).

Uso típico:
- Estruturar hierarquia: Admin → Gerente → Supervisor → Vendedores/Técnicos.

---

## 6️⃣ Metas

**O que faz:** Define metas mensais por vendedor/equipe e acompanha desempenho.

**Passo a passo:**
- Menu → **Metas** → **Listar Metas**.
- Botão **Nova Meta**:
  - Escolher vendedor, mês/ano e valor da meta.
- Na lista, atualizar **Receita Alcançada** conforme vendas reais.
- Sistema recalcula automaticamente **% de alcance** e **comissão**.
- Acompanhar status de comissão: Pendente → Aprovado → Pago.

Uso típico:
- Configurar metas mensais e acompanhar quem está abaixo/na/meta/acima.

---

## 7️⃣ Comissões

**O que faz:** Calcula comissões a partir das metas e faixas configuradas.

**Como funciona:**
- O módulo de metas chama o cálculo de comissão com base em:
  - Valor da meta.
  - Receita alcançada.
  - Faixas de comissão configuradas por empresa/cargo.
- Resultados aparecem em:
  - Lista de metas.
  - Dashboards por cargo.
  - Relatórios específicos (quando habilitados).

Uso típico:
- Conferir valores de comissão antes de aprovação/pagamento.

---

## 8️⃣ Relatórios

**O que faz:** Gera relatórios de vendas, metas, comissões e clientes.

**Exemplos de uso:**
- Relatório de vendas por cliente/vendedor.
- Relatório de desempenho de metas no período.
- Exportação para Excel e/ou PDF (quando disponível).

Acesso:
- Menu **Relatórios** (ou seções específicas em cada módulo).

### 📈 Relatório de Metas Avançado (Vendedor/Supervisor)

**O que faz:** Permite alternar entre visão por **Vendedor** e por **Supervisor** mantendo layout responsivo e profissional.

**Como usar:**
- Abra: Relatórios → Metas Avançado.
- No topo, use o seletor **Visão** para alternar entre Vendedor/Supervisor.
- Quando em **Supervisor**:
  - Filtro adicional de **Supervisor** fica disponível.
  - Tabela "Detalhamento por Supervisão" mostra: Supervisor, Tipo (valor/volume), Período (mês/ano), Meta total, Realizado total, Progresso (%), **Comissão** e **Taxa (%)** (para metas de valor).
- Quando em **Vendedor**:
  - Mantém tabela original com progresso, comissão e gráficos.
  - Ranking de meses aparece apenas nesta visão.

**Interpretação de dados (Supervisor):**
- Metas de `valor`: comissão do supervisor = realizado_total × taxa_supervisor (definida por faixas configuradas conforme percentual de alcance).
- Metas de `volume`: comissão do supervisor reflete a soma das comissões dos vendedores.

**Dicas de uso:**
- Ajuste filtros de `tipo_meta`, `ano` e `mes` para análises específicas.
- Use a diferenciação visual das barras de progresso para identificar rapidamente desempenho crítico/meta/boa/excelente.

---

## 9️⃣ Equipes

**O que faz:** Agrupa vendedores em equipes com um supervisor responsável.

**Passo a passo:**
- Menu → **Equipes** → **Listar Equipes**.
- Botão **Nova Equipe**:
  - Nome, descrição, supervisor responsável.
- Adicionar/remover vendedores da equipe.
- Visualizar performance consolidada por equipe.

Uso típico:
- Organizar forças de vendas por região, produto ou linha de negócio.

---

## 🔟 Super Admin

**O que faz:** Camada de controle global do sistema.

Principais funções:
- Gerenciar empresas (multi-tenant).
- Gerenciar usuários e cargos de alto nível.
- Acessar painel de **Backups**.
- Ver métricas globais e relatórios macros.

Uso típico:
- Administração geral da plataforma e suporte avançado.

---

## 1️⃣1️⃣ Estoque

**O que faz:** Controle de produtos, níveis de estoque e movimentações.

**Passo a passo resumido:**
- Menu → **Estoque** → **Produtos**:
  - Cadastrar produtos (nome, código, preço, estoque mínimo etc.).
- Menu → **Movimentações**:
  - Registrar entradas (compra, ajuste) e saídas (venda, consumo, OS).
- Relatórios de giro e posição de estoque.

Uso típico:
- Garantir disponibilidade de produtos/peças e acompanhar consumo.

---

## 1️⃣2️⃣ Backup

**O que faz:** Cria, baixa, restaura e envia backups do banco.

**Acesso:**
- Menu **Super Admin** → **Backups**.

**Ações principais:**
- **Criar Backup**: gera arquivo .db local (SQLite) ou registra instruções (PostgreSQL).
- **Download**: baixa o arquivo para armazenamento externo.
- **Restaurar**: substitui o banco atual por um backup selecionado (com backup de segurança automático).
- **Enviar Backup**: sobe arquivo externo para a lista de backups.
- **Backup Automático** (SQLite): agendado conforme configuração interna.

Com o módulo `backup_nuvem`, os backups locais podem ser sincronizados
para uma **pasta de nuvem local** configurável.

---

## 📌 Referências Rápidas

- Guia visual e fluxo geral: docs/guias/GUIA_VISUAL.md
- Guia completo de uso (usuário): docs/guias/MANUAL_USUARIO.md
- Guia completo de uso (visão técnica): docs/guias/GUIA_USO.md
- Manual completo detalhado: docs/archive/MANUAL_COMPLETO_MODULOS.md
