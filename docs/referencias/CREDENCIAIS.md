# 🔐 Credenciais e Primeiro Acesso (VendaCerta)

Este projeto **não** utiliza “credenciais padrão” para o Admin.

## ✅ Criar/atualizar o Admin (seed)

Defina as variáveis e execute o script:

Windows (PowerShell):
```powershell
$env:ADMIN_EMAIL="admin@sistema.com"
$env:ADMIN_PASSWORD="SUA_SENHA_FORTE"
python scripts/create_admin.py
```

Railway:
```powershell
$env:ADMIN_EMAIL="admin@sistema.com"
$env:ADMIN_PASSWORD="SUA_SENHA_FORTE"
railway run python scripts/create_admin.py
```

## ℹ️ Sobre outros usuários

Dependendo do fluxo (criação/importação), usuários não-admin podem receber uma senha temporária (`senha123`). Recomenda-se orientar a troca no primeiro acesso.
