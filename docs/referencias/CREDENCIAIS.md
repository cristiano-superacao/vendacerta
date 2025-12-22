# 🔐 Informações de Login - Sistema de Metas

## ✅ Sistema Funcionando Normalmente

O sistema está **100% operacional** tanto localmente quanto em produção (Railway).

---

## 👤 Credenciais de Acesso

### Local (SQLite)
Existem **4 usuários** cadastrados no banco de dados local:

1. **Admin Principal (antigo)**
   - 📧 Email: `admin@metas.com`
   - 🔑 Senha: `admin123`
   - 👔 Cargo: Administrador

2. **Admin Novo**
   - 📧 Email: `admin@suameta.com`
   - 🔑 Senha: `admin123`
   - 👔 Cargo: Administrador

3. **João Silva**
   - 📧 Email: `joao.silva@metas.com`
   - 🔑 Senha: _(definida anteriormente)_
   - 👔 Cargo: Usuário

4. **Maria Santos**
   - 📧 Email: `maria.santos@metas.com`
   - 🔑 Senha: _(definida anteriormente)_
   - 👔 Cargo: Usuário

---

## 🌐 Produção (Railway - PostgreSQL)

URL: https://web-production-90dab.up.railway.app

**Credenciais de Admin:**
- 📧 Email: `admin@suameta.com`
- 🔑 Senha: `admin123`
- 👔 Cargo: Administrador

---

## ✨ Funcionalidades Testadas e Confirmadas

### Login ✅
- ✅ Validação de email e senha
- ✅ Verificação de usuário ativo
- ✅ Hash de senha com Werkzeug
- ✅ Sessão com Flask-Login
- ✅ Redirecionamento após login

### Registro ✅
- ✅ Criação de novo usuário
- ✅ Hash automático de senha
- ✅ Validação de email duplicado
- ✅ Validação de senha (mínimo 6 caracteres)
- ✅ Confirmação de senha
- ✅ Seleção de cargo (usuário/supervisor/admin)

---

## 🧪 Como Testar

### Teste de Login (Local)
1. Acesse: http://127.0.0.1:5001/login
2. Use qualquer uma das credenciais acima
3. Clique em "Entrar"

### Teste de Registro (Local)
1. Acesse: http://127.0.0.1:5001/registro
2. Preencha o formulário:
   - Nome: Seu Nome
   - Email: seuemail@exemplo.com
   - Cargo: Usuário
   - Senha: mínimo 6 caracteres
   - Confirmar Senha: mesma senha
3. Clique em "Cadastrar"

### Teste em Produção (Railway)
1. Acesse: https://web-production-90dab.up.railway.app
2. Use: `admin@suameta.com` / `admin123`

---

## 🔧 Comandos Úteis

### Ver todos os usuários do banco local:
```powershell
python -c "from app import app; from models import Usuario; ctx = app.app_context(); ctx.push(); users = Usuario.query.all(); [print(f'{u.id} - {u.email} - {u.nome} - {u.cargo}') for u in users]"
```

### Criar usuário manualmente:
```powershell
python criar_teste.py
```

### Verificar senha de um usuário:
```powershell
python -c "from app import app; from models import Usuario; ctx = app.app_context(); ctx.push(); u = Usuario.query.filter_by(email='admin@suameta.com').first(); print('Senha correta:', u.check_senha('admin123'))"
```

---

## 📊 Status do Sistema

| Componente | Status | Observações |
|------------|--------|-------------|
| Banco de Dados | ✅ OK | SQLite (local), PostgreSQL (prod) |
| Autenticação | ✅ OK | Flask-Login + Werkzeug |
| Login | ✅ OK | Validação funcionando |
| Registro | ✅ OK | Criação de usuários OK |
| Hash de Senha | ✅ OK | Werkzeug generate_password_hash |
| Sessão | ✅ OK | Flask-Login session |
| Layout | ✅ OK | Responsivo e profissional |
| Deploy Railway | ✅ OK | https://web-production-90dab.up.railway.app |

---

## 🎨 Layout

✅ **Mantido 100% responsivo e profissional:**
- Gradiente animado (roxo → rosa)
- Ícone de alvo (bullseye) com animação flutuante
- Botão com efeito shine
- Design moderno com Bootstrap 5.3.3
- Favicon customizado
- Tipografia Inter (Google Fonts)

---

## 📝 Notas Importantes

1. **Dois admins**: Existem dois usuários admin por razões históricas:
   - `admin@metas.com` (criado primeiro)
   - `admin@suameta.com` (atual)

2. **Ambos funcionam** com a senha `admin123`

3. **Registro funcionando**: Novos usuários podem se cadastrar sem problemas

4. **Produção**: Use `admin@suameta.com` para acessar o sistema em produção

---

## 🚀 Próximos Passos (Opcional)

1. Remover usuário duplicado `admin@metas.com` do banco local
2. Atualizar emails dos usuários teste (João Silva, Maria Santos)
3. Implementar recuperação de senha
4. Adicionar autenticação de dois fatores (2FA)

---

✨ **Sistema 100% operacional e mantendo layout responsivo e profissional!**
