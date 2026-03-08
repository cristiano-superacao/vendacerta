# Guia de Implantação no Railway (Sistema Modular)

Este sistema foi reestruturado para suportar **Múltiplos Bancos de Dados (Micro-serviços lógicos)** e implantação nativa no Railway.

## 1. Configuração do Railway

O arquivo `nixpacks.toml` e `Dockerfile` foram removidos para permitir que o Railway use sua configuração automática (Railpack/Nixpacks) que é mais otimizada.

### Arquivos de Configuração Criados:
- **railway.json**: Configuração oficial do Railway.
- **Procfile**: Comando de inicialização do Gunicorn.

## 2. Bancos de Dados Modulares

O sistema agora suporta a separação dos dados em bancos diferentes. Você pode usar um único banco PostgreSQL (padrão) ou criar bancos separados para cada módulo.

### Variáveis de Ambiente (Opcionais)
Se você quiser separar os dados, defina estas variáveis no Railway. Se não definir, tudo será salvo no banco principal (`DATABASE_URL`).

- `DATABASE_URL_AUTH`: Tabelas de Usuários e Empresas.
- `DATABASE_URL_VENDAS`: Vendedores, Metas, Equipes, Comissões.
- `DATABASE_URL_CLIENTES`: Clientes e Compras.
- `DATABASE_URL_ESTOQUE`: Produtos e Movimentações.
- `DATABASE_URL_SERVICOS`: Técnicos e Ordens de Serviço.
- `DATABASE_URL_COMUNICACAO`: Mensagens.

**Recomendação:** Para iniciar, use apenas a variável `DATABASE_URL` padrão. O sistema criará todas as tabelas lá, mas manterá a estrutura lógica separada para facilitar a migração futura.

## 3. Deploy

1. Conecte seu repositório ao Railway.
2. O Railway detectará automaticamente o Python e o arquivo `requirements.txt`.
3. Defina as variáveis de ambiente básicas:
   - `FLASK_SECRET_KEY`: Uma chave aleatória segura.
   - `FLASK_APP`: `app.py`
4. O deploy deve ocorrer automaticamente.

## 4. Manutenção

Para criar as tabelas na primeira vez, o sistema usa `db.create_all()`. Se precisar rodar migrações, use o Flask-Migrate.
