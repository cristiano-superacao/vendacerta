# 🐘 Guia Completo de Migração para PostgreSQL

## Sistema VendaCerta - Migração SQLite → PostgreSQL

Este guia detalha o processo completo de migração do banco de dados SQLite para PostgreSQL, mantendo todas as funcionalidades, rotas, templates e o layout responsivo profissional.

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação do PostgreSQL](#instalação-do-postgresql)
3. [Configuração do Banco](#configuração-do-banco)
4. [Migração de Dados](#migração-de-dados)
5. [Execução do Sistema](#execução-do-sistema)
6. [Verificação](#verificação)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Pré-requisitos

### Software Necessário

- **Python 3.9+** (recomendado 3.13.9)
- **PostgreSQL 12+** (recomendado 16.x)
- **pip** atualizado
- **Virtual environment** configurado

### Pacotes Python Instalados

```bash
pip install psycopg2-binary==2.9.11
pip install SQLAlchemy==2.0.45
pip install Flask==3.0.0
pip install python-dotenv==1.0.1
```

Todos os pacotes já estão listados no `requirements.txt` atualizado.

---

## 🔧 Instalação do PostgreSQL

### Windows

1. **Download do PostgreSQL**
   - Acesse: https://www.postgresql.org/download/windows/
   - Baixe o instalador mais recente (PostgreSQL 16.x)

2. **Instalação**
   ```
   - Execute o instalador
   - Defina senha para o usuário 'postgres' (ANOTE ESTA SENHA!)
   - Porta padrão: 5432
   - Locale: Portuguese, Brazil (ou deixe padrão)
   - Instale Stack Builder (opcional)
   ```

3. **Verificar Instalação**
   ```powershell
   # Abra PowerShell e teste
   psql --version
   # Deve mostrar: psql (PostgreSQL) 16.x
   ```

4. **Configurar PATH (se necessário)**
   - Adicione `C:\Program Files\PostgreSQL\16\bin` ao PATH do Windows
   - Reinicie o terminal após adicionar

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS

```bash
brew install postgresql@16
brew services start postgresql@16
```

---

## ⚙️ Configuração do Banco

### Passo 1: Executar Script de Configuração

O script `setup_postgresql.py` automatiza a criação do banco de dados, usuário e permissões.

```powershell
# Ative o ambiente virtual
.\venv\Scripts\Activate.ps1

# Execute o script de configuração
python setup_postgresql.py
```

**O que o script faz:**

1. ✅ Conecta ao PostgreSQL como administrador
2. ✅ Cria usuário `vendacerta_user` com senha `vendacerta_pass`
3. ✅ Cria banco de dados `vendacerta_db`
4. ✅ Configura permissões adequadas
5. ✅ Gera arquivo `.env` com configurações
6. ✅ Testa a conexão

**Saída esperada:**

```
======================================================================
  CONFIGURAÇÃO POSTGRESQL - SISTEMA VENDACERTA
======================================================================

📋 Configurações:
   • Host: localhost
   • Port: 5432
   • Banco de dados: vendacerta_db
   • Usuário: vendacerta_user

Digite a senha do usuário 'postgres': ********

[1] Criando usuário do banco de dados
✅ Usuário 'vendacerta_user' configurado com sucesso!

[2] Criando banco de dados
✅ Banco 'vendacerta_db' criado com sucesso!

[3] Configurando permissões
✅ Permissões configuradas com sucesso!

[4] Gerando configuração .env
✅ Arquivo .env atualizado com configurações PostgreSQL!

[5] Testando conexão com o banco de dados
✅ Conexão bem-sucedida!
📊 Versão do PostgreSQL: PostgreSQL 16.x...

======================================================================
  CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!
======================================================================
```

### Passo 2: Verificar Arquivo .env

O script gera automaticamente o arquivo `.env` com as configurações:

```dotenv
# Configuração PostgreSQL - Sistema VendaCerta
FLASK_SECRET_KEY=dev-key-local-testing-2025
FLASK_ENV=development
FLASK_DEBUG=True

# Banco de dados PostgreSQL
DATABASE_URL=postgresql://vendacerta_user:vendacerta_pass@localhost:5432/vendacerta_db

# Variáveis individuais
PGDATABASE=vendacerta_db
PGHOST=localhost
PGPORT=5432
PGUSER=vendacerta_user
PGPASSWORD=vendacerta_pass
```

### Configuração Manual (Alternativa)

Se preferir configurar manualmente:

```sql
-- 1. Conecte ao PostgreSQL
psql -U postgres

-- 2. Crie o usuário
CREATE USER vendacerta_user WITH PASSWORD 'vendacerta_pass';

-- 3. Crie o banco de dados
CREATE DATABASE vendacerta_db OWNER vendacerta_user;

-- 4. Conceda permissões
GRANT ALL PRIVILEGES ON DATABASE vendacerta_db TO vendacerta_user;

-- 5. Conecte ao banco criado
\c vendacerta_db

-- 6. Conceda permissões no schema public
GRANT ALL ON SCHEMA public TO vendacerta_user;

-- 7. Saia
\q
```

---

## 📦 Migração de Dados

### Passo 1: Verificar Dados Existentes no SQLite

```powershell
# Verifique se o banco SQLite existe
dir instance\vendacerta.db
```

Se o arquivo existir e tiver dados que deseja migrar, prossiga com a migração.

### Passo 2: Executar Script de Migração

```powershell
python migrate_to_postgresql.py
```

**O que o script faz:**

1. ✅ Verifica configurações do SQLite e PostgreSQL
2. ✅ Cria backup automático do SQLite
3. ✅ Cria estrutura de tabelas no PostgreSQL
4. ✅ Migra dados respeitando foreign keys
5. ✅ Gera relatório de migração

**Saída esperada:**

```
======================================================================
  MIGRAÇÃO SQLITE → POSTGRESQL - SISTEMA VENDACERTA
======================================================================

[1] Verificando configurações
✅ SQLite: sqlite:///C:/Users/.../instance/vendacerta.db
✅ PostgreSQL: postgresql://vendacerta_user@***

[2] Criando backup do SQLite
✅ Backup criado: instance/vendacerta_backup_20251218_170000.db

[3] Conectando aos bancos de dados
✅ SQLite conectado!
✅ PostgreSQL conectado!

[4] Criando estrutura de tabelas no PostgreSQL
✅ Estrutura de tabelas criada!

[5] Migrando dados
📊 Total de tabelas a migrar: 27

[1/27] Migrando tabela 'empresas'...
   ✅ 1 registros migrados

[2/27] Migrando tabela 'usuarios'...
   ✅ 1 registros migrados

[3/27] Migrando tabela 'vendedores'...
   ✅ 5 registros migrados

...

======================================================================
  MIGRAÇÃO CONCLUÍDA
======================================================================

📊 Estatísticas da migração:
   • Tabelas processadas: 27
   • Tabelas migradas: 27
   • Total de registros: 234
   • Erros: 0 ✅

💾 Backup SQLite salvo em:
   instance/vendacerta_backup_20251218_170000.db
```

### Ordem de Migração de Tabelas

O script respeita automaticamente a ordem de dependências:

```
1. empresas
2. usuarios
3. vendedores
4. categorias_produto
5. produtos
6. equipes
7. metas
8. clientes
9. ordens_servico
10. vendas
11. comissoes
12. historico_comissoes
... (demais tabelas)
```

---

## 🚀 Execução do Sistema

### Passo 1: Iniciar o Sistema

```powershell
# Com PostgreSQL configurado
python app.py
```

**Saída esperada:**

```
✅ Usando PostgreSQL em produção
✅ Compressão Gzip ativada - Respostas serão 70-90% menores
✅ Cache ativado - Relatórios e dashboards 40-60% mais rápidos

[2025-12-18 17:00:00,000] INFO in app: 🔄 Verificando estrutura do banco de dados...
[2025-12-18 17:00:00,100] INFO in app: ✅ Banco de dados inicializado com sucesso!

======================================================================
🚀 SISTEMA DE GESTÃO DE METAS E COMISSÕES - VERSÃO COMPLETA
======================================================================

✨ Recursos Ativos:
   🔐 Sistema de autenticação
   🐘 Banco de dados PostgreSQL
   👥 Gerenciamento de vendedores
   📊 Gerenciamento de metas
   🎯 Cálculo automático de comissões
   ⏰ Backup automático agendado

📊 Servidor iniciado com sucesso!
🌐 Acesse: http://127.0.0.1:5001/login

======================================================================

 * Running on http://127.0.0.1:5001
```

### Passo 2: Acessar o Sistema

1. Abra o navegador: http://127.0.0.1:5001/login
2. Faça login com credenciais existentes
3. Verifique se todos os dados foram migrados corretamente

---

## ✔️ Verificação

### Verificar Conexão PostgreSQL

```powershell
# Teste direto no PostgreSQL
psql -U vendacerta_user -d vendacerta_db -h localhost

# Dentro do psql:
\dt                    # Lista todas as tabelas
\d+ usuarios          # Descreve tabela usuarios
SELECT COUNT(*) FROM empresas;  # Conta registros
\q                    # Sair
```

### Verificar Dados no Sistema

1. **Dashboard Principal**
   - Acesse: http://127.0.0.1:5001/
   - Verifique estatísticas e gráficos

2. **Vendedores**
   - Acesse: http://127.0.0.1:5001/vendedores
   - Verifique lista de vendedores migrados

3. **Metas**
   - Acesse: http://127.0.0.1:5001/metas
   - Verifique metas configuradas

4. **Clientes**
   - Acesse: http://127.0.0.1:5001/clientes
   - Verifique cadastros migrados

5. **Relatórios**
   - Acesse: http://127.0.0.1:5001/relatorios
   - Teste geração de relatórios

### Verificar Layout Responsivo

O layout Bootstrap 5.3 permanece intacto:

- ✅ **Desktop**: Layout completo com sidebar
- ✅ **Tablet**: Menu colapsável
- ✅ **Mobile**: Interface otimizada para mobile

---

## 🔍 Troubleshooting

### Erro: "FATAL: password authentication failed"

**Causa:** Senha incorreta para o usuário PostgreSQL

**Solução:**
```powershell
# Execute novamente o setup
python setup_postgresql.py

# Ou altere a senha manualmente:
psql -U postgres
ALTER USER vendacerta_user WITH PASSWORD 'nova_senha';
# Atualize .env com a nova senha
```

### Erro: "could not connect to server"

**Causa:** Serviço PostgreSQL não está rodando

**Solução (Windows):**
```powershell
# Verifique o serviço
Get-Service postgresql*

# Inicie o serviço
Start-Service postgresql-x64-16
```

**Solução (Linux):**
```bash
sudo systemctl start postgresql
sudo systemctl status postgresql
```

### Erro: "database does not exist"

**Causa:** Banco não foi criado

**Solução:**
```powershell
python setup_postgresql.py
```

### Erro: "relation 'tabela' does not exist"

**Causa:** Estrutura não foi criada

**Solução:**
```powershell
# Execute o app uma vez para criar tabelas
python app.py
# Ctrl+C para parar
# Execute a migração novamente
python migrate_to_postgresql.py
```

### Performance lenta

**Causa:** Configurações de pool não otimizadas

**Solução:** Já configurado em `config.py`:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 280,
    'pool_size': 5,
    'max_overflow': 10,
    'pool_timeout': 30
}
```

---

## 📚 Estrutura de Tabelas PostgreSQL

### Tabelas Criadas (27 total)

#### Autenticação e Usuários
- `empresas` - Cadastro de empresas
- `usuarios` - Usuários do sistema
- `vendedores` - Cadastro de vendedores

#### Metas e Comissões
- `metas` - Metas individuais
- `metas_equipe` - Metas de equipe
- `comissoes` - Comissões calculadas
- `historico_comissoes` - Histórico de alterações

#### Clientes e Vendas
- `clientes` - Cadastro de clientes
- `vendas` - Registros de vendas
- `produtos` - Catálogo de produtos
- `categorias_produto` - Categorias

#### Serviços
- `ordens_servico` - Ordens de serviço
- `servicos_prestados` - Serviços executados

#### Estoque
- `movimentacoes_estoque` - Movimentações
- `produtos_estoque` - Estoque atual

#### Comunicação
- `mensagens` - Sistema de mensagens
- `notificacoes` - Notificações do sistema

#### Outros
- `equipes` - Equipes de vendas
- `balanceamento` - Balanceamento de metas
- `campanhas` - Campanhas de vendas
- E mais...

---

## 🎯 Próximos Passos

### 1. Produção (Railway/Heroku)

Já está configurado! Basta definir `DATABASE_URL` no ambiente:

```bash
# Railway
railway variables set DATABASE_URL="postgresql://user:pass@host:5432/db"

# Heroku
heroku config:set DATABASE_URL="postgresql://user:pass@host:5432/db"
```

### 2. Backup Automatizado

O sistema já tem backup automático configurado (ver `backup_helper.py`).

Para PostgreSQL, adicione backup via `pg_dump`:

```bash
# Criar backup
pg_dump -U vendacerta_user -d vendacerta_db -F c -f backup_$(date +%Y%m%d).dump

# Restaurar backup
pg_restore -U vendacerta_user -d vendacerta_db backup_20251218.dump
```

### 3. Monitoramento

```sql
-- Verificar tamanho do banco
SELECT pg_size_pretty(pg_database_size('vendacerta_db'));

-- Verificar tabelas maiores
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;

-- Verificar conexões ativas
SELECT * FROM pg_stat_activity WHERE datname = 'vendacerta_db';
```

---

## 📝 Notas Importantes

### ✅ Mantido Após Migração

- ✅ Todos os dados migrados
- ✅ Todas as rotas funcionando
- ✅ Todos os templates preservados
- ✅ Layout responsivo Bootstrap 5.3
- ✅ Sistema de autenticação
- ✅ Permissões e roles
- ✅ Cálculos de comissão
- ✅ Geração de relatórios PDF/Excel
- ✅ Backup automático
- ✅ Cache e compressão

### 🔐 Segurança

- ✅ Conexão SSL/TLS habilitada (produção)
- ✅ Senhas criptografadas (Werkzeug)
- ✅ CSRF Protection ativado
- ✅ Session cookies seguros
- ✅ SQL Injection protegido (SQLAlchemy)

### ⚡ Performance

- ✅ Connection pooling otimizado
- ✅ Índices preservados
- ✅ Queries otimizadas
- ✅ Cache de relatórios
- ✅ Compressão Gzip

---

## 🆘 Suporte

### Recursos Criados

1. `setup_postgresql.py` - Configuração automática do PostgreSQL
2. `migrate_to_postgresql.py` - Migração automática de dados
3. `.env` - Configurações de ambiente
4. `config.py` - Configurações otimizadas
5. `requirements.txt` - Dependências atualizadas

### Logs do Sistema

```powershell
# Ver logs em tempo real
python app.py

# Logs do PostgreSQL (Windows)
C:\Program Files\PostgreSQL\16\data\pg_log\

# Logs do PostgreSQL (Linux)
/var/log/postgresql/
```

---

## ✨ Conclusão

A migração para PostgreSQL foi concluída com sucesso! O sistema está:

✅ **Configurado** com PostgreSQL local
✅ **Dados migrados** do SQLite
✅ **Rodando** com todas as funcionalidades
✅ **Layout** responsivo e profissional mantido
✅ **Pronto** para produção (Railway/Heroku/Render)

**Acesse:** http://127.0.0.1:5001/login

---

*Documentação gerada em: 18/12/2025*
*Sistema VendaCerta - Versão PostgreSQL*
