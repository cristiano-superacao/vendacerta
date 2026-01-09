# 🔧 Scripts Auxiliares

Esta pasta contém scripts de utilidade para desenvolvimento, testes e manutenção do sistema.

## 📁 Scripts Disponíveis

### 🐛 Correção e Diagnóstico

| Script | Descrição | Uso |
|--------|-----------|-----|
| `corrigir_erro_500.py` | Corrige erros 500 comuns | `python scripts/corrigir_erro_500.py` |
| `test_db.py` | Testa conexão com banco de dados | `python scripts/test_db.py` |

### 🧪 Testes e Desenvolvimento

| Script | Descrição | Uso |
|--------|-----------|-----|
| `criar_teste.py` | Cria dados de teste | `python scripts/criar_teste.py` |
| `test_registro.py` | Testa funcionalidade de registro | `python scripts/test_registro.py` |
| `duplicar_clientes_para_empresa.py` | Duplica clientes para empresa alvo (multi-empresa) | `python scripts/duplicar_clientes_para_empresa.py [--dry-run] [--empresa-alvo NOME]` |
| `duplicar_produtos_para_empresa.py` | Duplica produtos para empresa alvo (multi-empresa) | `python scripts/duplicar_produtos_para_empresa.py [--dry-run] [--empresa-alvo NOME]` |

### ⚙️ Utilitários

| Script | Descrição | Uso |
|--------|-----------|-----|
| `obter_database_url.py` | Obtém URL do banco Railway | `python scripts/obter_database_url.py` |
| `reconstruir_templates.py` | Reconstrói templates HTML | `python scripts/reconstruir_templates.py` |

---

## 🎯 Como Usar

### Duplicação de Clientes Entre Empresas

**Script**: `duplicar_clientes_para_empresa.py`

**Descrição**: Duplica todos os clientes (incluindo inativos) de outras empresas para a empresa alvo. Suporta operação multi-empresa com detecção avançada de duplicatas.

**Características**:
- ✅ **Multi-empresa**: Respeita unicidade por empresa (CPF/CNPJ/código)
- ✅ **Geração automática**: Códigos únicos por cidade/empresa
- ✅ **Mapeamento inteligente**: Vendedor/supervisor por e-mail
- ✅ **Idempotência total**: Detecta duplicatas por múltiplas chaves
  - CPF/CNPJ (prioridade 1)
  - codigo_bp (prioridade 2)
  - email (prioridade 3)
  - nome + telefone/celular (prioridade 4)
  - nome isolado (fallback)
- ✅ **Segurança**: Transação com savepoint por cliente
- ✅ **Dry-run**: Simulação sem persistir alterações

**Uso**:
```bash
# Simulação (não persiste alterações) - empresa padrão "Teste 001"
python scripts/duplicar_clientes_para_empresa.py --dry-run

# Execução real para empresa padrão
python scripts/duplicar_clientes_para_empresa.py

# Especificar empresa alvo diferente
python scripts/duplicar_clientes_para_empresa.py --empresa-alvo "Outra Empresa"

# Listar empresas disponíveis no banco
python scripts/duplicar_clientes_para_empresa.py --listar-empresas

# Executar contra banco específico (Railway/Postgres)
python scripts/duplicar_clientes_para_empresa.py \
  --database-url "postgresql://user:pass@host:port/db" \
  --empresa-alvo "Teste 001"
```

**Pré-requisitos**:
- Empresa alvo deve existir no banco
- Conexão ativa com banco de dados
- (Opcional) Migração de unicidade por empresa aplicada

**Saída esperada**:
```
📦 Duplicação de clientes para a empresa: Teste 001 (ID=2)

Encontrados 46 clientes de origem para processar.

✅ Dados persistidos com sucesso.

Resumo da operação:
  • Processados: 46
  • Inseridos:  46
  • Pulados por chave (doc/codigo_bp/email/contato): 0
  • Erros:      0
```

**Idempotência - Reexecução**:
```
# Executar novamente após clonagem bem-sucedida
python scripts/duplicar_clientes_para_empresa.py --dry-run

Resumo da operação:
  • Processados: 46
  • Inseridos:  0
  • Pulados por chave (doc/codigo_bp/email/contato): 46
  • Erros:      0
```

---

### Duplicação de Produtos Entre Empresas

**Script**: `duplicar_produtos_para_empresa.py`

**Descrição**: Duplica todos os produtos (ativos e inativos) de outras empresas para a empresa alvo. Suporta operação multi-empresa com detecção avançada de duplicatas.

**Características**:
- ✅ **Multi-empresa**: Respeita unicidade por empresa
- ✅ **Geração automática**: Códigos únicos por empresa (formato: CODIGO-E{ID})
- ✅ **Idempotência total**: Detecta duplicatas por múltiplas chaves
  - codigo_barra (prioridade 1)
  - referencia (prioridade 2)
  - nome (fallback)
- ✅ **Dados preservados**: Estoque, preços, categorias, localização, status
- ✅ **Segurança**: Transação com savepoint por produto
- ✅ **Dry-run**: Simulação sem persistir alterações

**Uso**:
```bash
# Simulação (não persiste alterações) - empresa padrão "Teste 001"
python scripts/duplicar_produtos_para_empresa.py --dry-run

# Execução real para empresa padrão
python scripts/duplicar_produtos_para_empresa.py

# Especificar empresa alvo diferente
python scripts/duplicar_produtos_para_empresa.py --empresa-alvo "Outra Empresa"

# Listar empresas disponíveis no banco
python scripts/duplicar_produtos_para_empresa.py --listar-empresas

# Executar contra banco específico (Railway/Postgres)
python scripts/duplicar_produtos_para_empresa.py \
  --database-url "postgresql://user:pass@host:port/db" \
  --empresa-alvo "Teste 001"
```

**Saída esperada**:
```
📦 Duplicação de produtos para a empresa: Teste 001 (ID=2)

Encontrados 94 produtos de origem para processar.

✅ Dados persistidos com sucesso.

Resumo da operação:
  • Processados: 94
  • Inseridos:  94
  • Pulados por chave (codigo_barra/referencia/nome): 0
  • Erros:      0
```

**Idempotência - Reexecução**:
```
# Executar novamente após clonagem bem-sucedida
python scripts/duplicar_produtos_para_empresa.py --dry-run

Resumo da operação:
  • Processados: 94
  • Inseridos:  0
  • Pulados por chave (codigo_barra/referencia/nome): 94
  • Erros:      0
```

---

### Ambiente de Desenvolvimento
```bash
# Criar dados de teste
python scripts/criar_teste.py

# Testar conexão do banco
python scripts/test_db.py

# Testar registro de usuário
python scripts/test_registro.py
```

### Troubleshooting
```bash
# Corrigir erro 500
python scripts/corrigir_erro_500.py

# Obter DATABASE_URL do Railway
python scripts/obter_database_url.py
```

### Manutenção
```bash
# Reconstruir templates
python scripts/reconstruir_templates.py
```

---

## ⚠️ Avisos Importantes

- **Não execute em produção**: Estes scripts são para desenvolvimento
- **Backup primeiro**: Sempre faça backup antes de executar scripts de correção
- **Dados de teste**: Scripts de teste criam dados fictícios

---

## 🔄 Alternativa: Script Consolidado

Para migrações e setup inicial, use o script consolidado na raiz:
```bash
# Na raiz do projeto
python migrate.py
```

Este script substitui vários dos scripts auxiliares e é a forma recomendada para setup.

---

## 📖 Mais Informações

- [README_SISTEMA.md](../README_SISTEMA.md) - Documentação técnica completa
- [DEPLOY.md](../DEPLOY.md) - Guia de deploy
- [INDEX.md](../INDEX.md) - Índice geral

---

**💡 Dica**: Para a maioria das tarefas comuns, use os scripts principais na raiz do projeto (`migrate.py`, `app.py`, `init_db.py`).

---

[← Voltar ao Índice Principal](../INDEX.md)
