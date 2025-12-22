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

### ⚙️ Utilitários

| Script | Descrição | Uso |
|--------|-----------|-----|
| `obter_database_url.py` | Obtém URL do banco Railway | `python scripts/obter_database_url.py` |
| `reconstruir_templates.py` | Reconstrói templates HTML | `python scripts/reconstruir_templates.py` |

---

## 🎯 Como Usar

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
