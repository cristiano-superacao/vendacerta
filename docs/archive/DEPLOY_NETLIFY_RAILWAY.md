# Guia de Deploy: Railway e Netlify

Este projeto foi configurado para ser compatível com **Railway** (Aplicação Completa) e **Netlify** (Documentação/Frontend Estático).

## 🚀 Opção 1: Railway (Recomendado para a Aplicação)

O Railway é a plataforma ideal para hospedar a aplicação Flask completa, pois suporta:

- Banco de Dados PostgreSQL (Persistência)
- Agendador de Tarefas (APScheduler)
- Processos de Longa Duração

### Arquivos de Configuração Criados

- `railway.json`: Configurações de deploy e healthcheck.
- `nixpacks.toml`: Instala dependências do sistema (Linux) necessárias para gerar PDFs e processar imagens.
- `Procfile`: Comando de inicialização do servidor Gunicorn.
- `runtime.txt`: Versão do Python (3.11).

### Como Fazer o Deploy no Railway

1. Crie uma conta em [railway.app](https://railway.app).
2. Clique em "New Project" > "Deploy from GitHub repo".
3. Selecione este repositório.
4. O Railway detectará automaticamente o `nixpacks.toml` e configurará o ambiente.
5. **Variáveis de Ambiente:** Adicione as variáveis do seu `.env` no painel do Railway.
    - `FLASK_SECRET_KEY`
    - `DATABASE_URL` (O Railway cria um Postgres automaticamente se você adicionar o plugin de Database).

---

## 🌐 Opção 2: Netlify (Documentação)

O Netlify é excelente para hospedagem estática. Como esta aplicação depende de um agendador em background e conexão constante com banco de dados, o Netlify foi configurado para hospedar a **Documentação de Regras de Negócio**.

### Arquivo de Configuração

- `netlify.toml`: Configura o Netlify para servir o arquivo `docs/MANUAL_DO_USUARIO.html` como página inicial.

### Como Fazer o Deploy no Netlify

1. Crie uma conta em [netlify.com](https://netlify.com).
2. Arraste a pasta do projeto para o painel ou conecte com GitHub.
3. O Netlify lerá o `netlify.toml` e publicará a documentação automaticamente.
4. Acesse a URL fornecida para ver o Manual do Usuário online.

---

## 🛠️ Resumo Técnico

| Recurso | Railway | Netlify |
|---------|---------|---------|
| **Tipo** | Backend / Full Stack | Frontend Estático |
| **Aplicação Flask** | ✅ Suportado (Gunicorn) | ❌ Limitado (Functions) |
| **Banco de Dados** | ✅ PostgreSQL Nativo | ❌ Requer conexão externa |
| **Agendador (Cron)** | ✅ Suportado (APScheduler) | ❌ Não suportado |
| **Uso Recomendado** | **Sistema VendaCerta Completo** | **Documentação / Landing Page** |
