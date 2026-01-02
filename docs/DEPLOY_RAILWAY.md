# Deploy automático no Railway (GitHub Actions)

Este guia descreve como configurar deploy automático para o Railway usando GitHub Actions com o workflow `.github/workflows/railway-deploy.yml`.

## Pré-requisitos
- Projeto conectado ao Railway (ID do projeto disponível em Settings → Project ID).
- Acesso ao repositório GitHub `cristiano-superacao/vendacerta`.

## Secrets necessários (GitHub)
Adicione dois secrets no repositório:

- `RAILWAY_TOKEN`: Token gerado em railway.app → Account → API Tokens → Generate.
- `RAILWAY_PROJECT_ID`: ID do projeto Railway.

Passos:
1. Acesse GitHub → Repository → Settings → Secrets and variables → Actions.
2. Clique em “New repository secret” e adicione:
   - `RAILWAY_TOKEN` com o token gerado.
   - `RAILWAY_PROJECT_ID` com o ID do projeto.

Alternativa via GitHub CLI:
```powershell
winget install GitHub.cli
gh auth login
gh secret set RAILWAY_TOKEN -b "SEU_TOKEN_AQUI"
gh secret set RAILWAY_PROJECT_ID -b "SEU_PROJECT_ID_AQUI"
```

## Como o workflow funciona
- Evento: `push` na branch `main` (ou acionamento manual via `workflow_dispatch`).
- Etapas:
  - Instala `@railway/cli`.
  - Executa `railway link $RAILWAY_PROJECT_ID`.
  - Executa `railway up`.
  - Healthcheck configurado em `/ping` (ver `railway.json`).

## Acionar o deploy
- Faça merge da branch `feature/comissoes-manutencao-acessibilidade` na `main`.
- Ou acione manualmente:
```powershell
gh workflow run railway-deploy.yml
```

## Verificação pós-deploy
- Healthcheck: `GET /ping` deve retornar `pong`.
- Login: `/login` acessível.
- Logs:
```powershell
railway logs
```

## CLI sem navegador (opcional)
Se preferir não usar Actions, é possível usar `RAILWAY_TOKEN` localmente:
```powershell
$env:RAILWAY_TOKEN="SEU_TOKEN_AQUI"
$env:RAILWAY_PROJECT_ID="SEU_PROJECT_ID_AQUI"
cd C:\Users\Superação\Desktop\Sistema\vendacerta
# Script PowerShell com suporte a token/ProjectId
./scripts/deploy_railway.ps1

# Ou manualmente
railway link $env:RAILWAY_PROJECT_ID
railway up
railway logs
```

## Observações
- O arquivo `railway.json` usa Nixpacks e define `healthcheckPath: "/ping"`.
- O app já possui a rota `/ping` (healthcheck) em `app.py`.
- Caso use variáveis sensíveis (ex.: `FLASK_SECRET_KEY`), configure no Railway → Variables.
- O script `scripts/deploy_railway.ps1` aceita token via variável `RAILWAY_TOKEN` e `RAILWAY_PROJECT_ID`, ou modo interativo se não definidos.
