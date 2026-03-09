# 🧾 Guia de Importação de Pedidos Faturados (NF) — VendaCerta

Este guia descreve como importar pedidos **faturados** (via XLSX/CSV), atualizar o status do pedido para **FATURADO** ou **DIVERGENTE**, e gerar relatório de inconsistências.

---

## ✅ Quem pode usar

- Usuários com acesso administrativo ao módulo de **Pedidos**.

---

## 📍 Onde fica

- Tela: `/pedidos/importar-faturados`
- Modelos:
  - XLSX: `/pedidos/importar-faturados/modelo.xlsx`
  - CSV: `/pedidos/importar-faturados/modelo.csv`

---

## 📦 Formatos aceitos

- `.xlsx` (Excel)
- `.csv`

Limites e regras:
- Upload até **20MB**
- Até **20.000 linhas** por arquivo
- Linhas vazias são ignoradas
- Linhas duplicadas (mesmo Pedido/Romaneio) são ignoradas após a primeira ocorrência

---

## 🧱 Colunas obrigatórias

O importador é flexível com o nome das colunas (aceita variações), mas espera estes campos:

| Campo | Exemplo | Observação |
|------|---------|------------|
| **Romaneio** | `ROM-001` | Pode ser usado como chave se o Pedido vier vazio |
| **Pedido** | `12345` | Preferencialmente o `numero_pedido` do sistema |
| **Cliente** | `000123` | Usado para validação (quando possível) |
| **Data Faturamento** | `31/01/2026` | Aceita `dd/mm/aaaa` e `yyyy-mm-dd` |
| **Nota Fiscal** | `NF-123456` | Gravado em `numero_nota` |
| **Valor** | `1000,50` | Valor faturado (aceita `1.234,56` e `1234.56`) |

> Dica: use o modelo XLSX/CSV gerado pelo sistema para evitar erro de cabeçalho.

---

## 🔎 Validação (modo “Validar”)

Ao clicar em **Validar**, o sistema:

- Lê e valida o arquivo
- Confere se existe um pedido no banco com `numero_pedido` igual ao campo **Pedido** (ou **Romaneio** como fallback)
- Ignora pedidos **cancelados**
- Calcula divergência percentual entre:
  - **Valor (planilha)** vs
  - **Total do sistema** (soma de `valor_total` do pedido)

### Regra de divergência

- Se a diferença percentual for **maior que 2%**, o pedido será classificado como **DIVERGENTE**.
- Caso contrário, será classificado como **FATURADO**.

Fórmula (base do sistema):

$$\text{diferença\%} = \frac{|\text{valor\_excel} - \text{valor\_sistema}|}{\text{valor\_sistema}} \times 100$$

> No modo **Validar**, nenhuma alteração é aplicada.

---

## 🧾 Importação (modo “Importar”)

Ao clicar em **Importar**, além de validar, o sistema:

- Atualiza o pedido com:
  - `numero_nota`
  - `data_faturamento`
  - `valor_faturado`
  - `data_importacao_nf`
  - `status_pedido` = `FATURADO` ou `DIVERGENTE`
- Se o pedido ficar **FATURADO**, também ajusta `status` para `Exportado`
- Registra auditoria na tabela `importacoes_nf`
- Registra um log resumido (auditoria) em `pedidos_log`

---

## 📊 Relatório e auditoria

Após importar, o sistema mantém:

- Contadores: importados, atualizados, divergentes, não encontrados
- Detalhes (até 200 itens por tipo) para:
  - divergentes
  - não encontrados
  - issues/alertas (ex.: cliente não confere, duplicados, linhas inválidas)

---

## 🆘 Erros comuns

- **Colunas obrigatórias ausentes**: baixe e use o modelo do sistema.
- **Data inválida**: use `dd/mm/aaaa` ou `yyyy-mm-dd`.
- **Valor inválido**: evite texto; use `1000,50` ou `1000.50`.
- **Pedido não encontrado**: verifique se o número do pedido na planilha bate com o `numero_pedido` do sistema.

---

## ✅ Boas práticas

- Faça uma primeira execução com **Validar**.
- Em arquivos grandes, divida por períodos (ex.: por mês) para facilitar conferência.
- Para divergências recorrentes, revise cadastro de itens/preços do pedido no sistema.
