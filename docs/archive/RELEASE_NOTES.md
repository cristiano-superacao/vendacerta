# Release Notes - Sistema VendaCerta v2.0.0

## 🎉 Versão 2.0.0 - Formato Dual de Importação/Exportação Excel

**Data:** 17 de dezembro de 2025  
**Autor:** Equipe VendaCerta  
**Repositório:** https://github.com/cristiano-superacao/vendacerta

---

## 📋 Resumo das Alterações

Esta versão introduz um sistema completo de importação/exportação de clientes em Excel com dois formatos distintos, além de renomear o banco de dados e otimizar a estrutura do projeto.

---

## ✨ Novos Recursos

### 1. **Formato Dual de Planilhas Excel**

#### 📊 Formato Estendido (18 colunas)
Ideal para importações completas com todos os detalhes:
- **CPF/CNPJ** (combinado - detecta automaticamente pelo tamanho)
- **Sigla**
- **Razão Social**
- **Inscr.Estadual**
- **Município**
- **Bairro**
- **CEP**
- **Fone(1)**
- **Fone(2)**
- **Cel(1)**
- **Email**
- **Ponto de Referência**
- **Coordenada-X**
- **Coordenada-Y**
- **Codigo-BP**
- **Dia de Visita**
- **Formas de Pagamento**
- **Observações**

**Exportação inclui 23 colunas** (adiciona Status, Última Compra, Total Compras, Ativo, Vendedor)

#### 📝 Formato Simples (11 colunas)
Ideal para importações rápidas com dados básicos:
- Nome
- CPF
- CNPJ
- Telefone
- Email
- Cidade
- Bairro
- Ponto de Referência
- Dia de Visita
- Formas de Pagamento
- Observações

---

### 2. **Novos Campos no Banco de Dados**

Adicionados 9 novos campos ao modelo `Cliente`:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `razao_social` | String(200) | Razão social da empresa |
| `sigla` | String(50) | Sigla/apelido do cliente |
| `inscricao_estadual` | String(20) | Inscrição estadual |
| `codigo_bp` | String(50) | Código BP/ERP |
| `cep` | String(10) | Código postal |
| `coordenada_x` | String(20) | Longitude (coordenada X) |
| `coordenada_y` | String(20) | Latitude (coordenada Y) |
| `telefone2` | String(20) | Segundo telefone |
| `celular` | String(20) | Número de celular |

---

### 3. **Interface Modernizada de Importação**

- **Cards interativos** para seleção de formato
- **Destaque visual** no formato selecionado (borda colorida)
- **Botões grandes e claros** para download
- **JavaScript inteligente** que atualiza URLs dinamicamente
- **Validação de arquivo** antes do upload
- **Feedback visual** durante processamento

---

### 4. **Lógica Inteligente de Importação**

#### CPF/CNPJ Combinado
```python
# Detecta automaticamente se é CPF (11 dígitos) ou CNPJ (14 dígitos)
doc = re.sub(r'\D', '', cpf_cnpj_value)
if len(doc) == 11:
    cpf = doc
elif len(doc) == 14:
    cnpj = doc
```

#### Mapeamento Flexível de Colunas
O sistema reconhece automaticamente variações nos nomes das colunas:
- "Inscr.Estadual" ← "Inscrição Estadual", "IE", "I.E."
- "Município" ← "Cidade", "Municipio"
- "Coordenada-X" ← "Longitude", "Long", "Coordenada X"
- "Codigo-BP" ← "Código BP", "BP", "Código ERP"

---

## 🔧 Alterações Técnicas

### Banco de Dados
- **Nome alterado:** `metas.db` → `vendacerta.db`
- **Migração automática:** Script `adicionar_campos_clientes.py` executa ALTER TABLE
- **Compatibilidade:** Mantém dados existentes

### Rotas Atualizadas

#### `/clientes/exportar`
- Parâmetro `?formato=simples` ou `?formato=estendido`
- Gera Excel com formatação profissional
- Larguras de coluna otimizadas
- Exemplos na linha 2

#### `/clientes/modelo-importacao`
- Parâmetro `?formato=simples` ou `?formato=estendido`
- Template em branco com estrutura correta
- Linha de exemplo preenchida

#### `/clientes/importar`
- Suporta ambos os formatos automaticamente
- Detecta colunas por variações de nome
- Validação de CPF/CNPJ únicos
- Mensagens de erro detalhadas

---

## 📦 Deploy Railway

### Configurações Otimizadas

**railway.json:**
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install --no-cache-dir -r requirements.txt"
  },
  "deploy": {
    "startCommand": "python init_db.py && gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --worker-class gthread --timeout 120 --graceful-timeout 30 --keep-alive 5 --max-requests 1000 --max-requests-jitter 50 --log-level info --access-logfile - --error-logfile - --preload",
    "healthcheckPath": "/ping",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Variáveis de Ambiente:**
- `DATABASE_URL` - PostgreSQL fornecido pelo Railway
- `SECRET_KEY` - Chave secreta para sessões
- `FLASK_ENV` - production

---

## 🎨 Layout e Design

### Bootstrap 5.3.3
- Layout totalmente responsivo
- Cards com sombras suaves
- Ícones Bootstrap Icons
- Tema verde profissional (#198754)

### JavaScript Moderno
- Eventos DOM com `addEventListener`
- Validação de arquivo antes do upload
- Atualização dinâmica de URLs
- Feedback visual de processamento

---

## 📊 Melhorias de Performance

1. **Importação em lote** - Processa múltiplos registros de uma vez
2. **Validação antecipada** - Verifica duplicatas antes de inserir
3. **Transações atômicas** - Rollback automático em caso de erro
4. **Cache de queries** - Pool de conexões otimizado

---

## 🔒 Segurança

- **Validação de tipos de arquivo** - Apenas .xlsx e .xls
- **Limite de tamanho** - Máximo 10 MB por arquivo
- **Sanitização de dados** - Remove caracteres especiais de CPF/CNPJ
- **CSRF Protection** - Token em todos os formulários
- **Permissões granulares** - Apenas vendedores podem importar seus clientes

---

## 📝 Documentação

### Arquivos Criados/Atualizados

- ✅ `DUAL_EXCEL_FORMATS_IMPLEMENTADO.md` - Documentação completa dos formatos
- ✅ `adicionar_campos_clientes.py` - Script de migração do banco
- ✅ `TESTE_LOCAL.md` - Guia de testes locais
- ✅ `docs/referencias/VALIDACAO_FORMULAS.md` - Validação de fórmulas
- ✅ `docs/archive/*` - Documentos históricos arquivados

---

## 🚀 Como Usar

### 1. Exportar Clientes

```bash
1. Acesse: /clientes/importar
2. Selecione o formato desejado (Simples ou Estendido)
3. Clique em "Exportar Clientes Atuais"
4. Edite a planilha conforme necessário
```

### 2. Baixar Modelo

```bash
1. Acesse: /clientes/importar
2. Selecione o formato desejado
3. Clique em "Baixar Modelo em Branco"
4. Preencha com os dados dos clientes
```

### 3. Importar Clientes

```bash
1. Prepare a planilha (modelo ou exportação editada)
2. Acesse: /clientes/importar
3. Selecione o arquivo .xlsx ou .xls
4. Clique em "Importar Clientes"
5. Aguarde o processamento
6. Verifique os resultados (importados e erros)
```

---

## 🐛 Correções de Bugs

- ✅ Corrigido erro de duplicação de colunas na exportação
- ✅ Corrigido mapeamento incorreto de "Cidade" vs "Município"
- ✅ Corrigido problema com CPF/CNPJ separados vs combinados
- ✅ Corrigido larguras de coluna desproporcionais
- ✅ Removido campo "Data Cadastro" desnecessário da exportação

---

## ⚠️ Breaking Changes

### Banco de Dados
- **Nome do arquivo:** `metas.db` → `vendacerta.db`
- **Ação necessária:** Execute `adicionar_campos_clientes.py` para migrar

### Formatos de Exportação
- **Antes:** 1 formato único com 20 colunas
- **Agora:** 2 formatos (Simples: 11 colunas | Estendido: 18/23 colunas)
- **Compatibilidade:** Planilhas antigas ainda funcionam (mapeamento flexível)

---

## 📈 Métricas

- **Arquivos alterados:** 19
- **Linhas adicionadas:** 5.343
- **Linhas removidas:** 203
- **Novos campos:** 9
- **Novos formatos:** 2
- **Tempo de implementação:** ~4 horas

---

## 🔮 Próximos Passos

1. **Validação de coordenadas** - Verificar formato de latitude/longitude
2. **Importação de imagens** - Logotipos de clientes
3. **Exportação PDF** - Relatórios formatados
4. **API REST** - Endpoints para integração externa
5. **Testes automatizados** - Coverage > 80%

---

## 🙏 Agradecimentos

Equipe de desenvolvimento VendaCerta pela implementação cuidadosa e teste extensivo.

---

## 📞 Suporte

- **Email:** suporte@vendacerta.com
- **GitHub:** https://github.com/cristiano-superacao/vendacerta
- **Documentação:** https://vendacerta.up.railway.app/docs

---

**Versão:** 2.0.0  
**Build:** 4044c14  
**Data de Release:** 17/12/2025
