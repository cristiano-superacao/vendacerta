# 🚀 Guia Rápido - Testar Sistema Localmente

## ⚡ Início Rápido (3 minutos)

### 1. Verificar Requisitos
```powershell
# Verificar Python (deve ser 3.11+)
python --version

# Verificar pip
pip --version
```

### 2. Instalar Dependências
```powershell
# Navegar até a pasta do projeto
cd "c:\Users\Superação\Desktop\Sistema\suameta"

# Instalar dependências
pip install -r requirements.txt
```

### 3. Iniciar o Sistema
```powershell
# Executar o aplicativo
python app.py
```

### 4. Acessar o Sistema
Abra o navegador e acesse:
```
http://127.0.0.1:5001
```

---

## 🔑 Credenciais de Teste

### Admin Padrão
```
Email: admin@suameta.com
Senha: admin123
```

⚠️ **IMPORTANTE:** Altere esta senha após o primeiro acesso!

---

## ✅ Testar Funcionalidades

### 1. Cadastrar Vendedor
1. Login com admin
2. Menu **Vendedores** → **Novo Vendedor**
3. Preencher formulário:
   - Nome: João Silva
   - Email: joao@teste.com
   - Telefone: (71) 99999-9999
   - CPF: 123.456.789-00
4. Clicar em **Salvar**

### 2. Cadastrar Mais Vendedores
Repetir o processo acima com:
- Maria Santos (maria@teste.com)
- Carlos Oliveira (carlos@teste.com)
- Ana Costa (ana@teste.com)

✅ **Verificar:** Todos devem ser cadastrados com sucesso!

### 3. Criar Equipe
1. Menu **Equipes** → **Nova Equipe**
2. Preencher:
   - Nome: Equipe Vendas SP
   - Descrição: Equipe de vendas de São Paulo
   - Supervisor: Selecionar um usuário
3. Salvar

### 4. Criar Meta
1. Menu **Metas** → **Nova Meta**
2. Preencher:
   - Vendedor: Selecionar vendedor
   - Mês: Dezembro
   - Ano: 2025
   - Valor da Meta: R$ 50.000,00
   - Receita Alcançada: R$ 35.000,00
3. Salvar

✅ **Verificar:** Comissão calculada automaticamente!

### 5. Verificar Dashboard
1. Menu **Dashboard**
2. Verificar:
   - Total de vendedores
   - Receita total
   - Comissões
   - Ranking

### 6. Acessar Manual
1. Menu **Ajuda**
2. Clicar em **Baixar Manual**
3. Verificar que o arquivo é baixado

---

## 🐛 Solução de Problemas

### Erro: "Módulo não encontrado"
```powershell
pip install -r requirements.txt
```

### Erro: "Banco de dados não encontrado"
O sistema cria automaticamente ao iniciar. Se persistir:
```powershell
python init_db.py
```

### Erro: "Porta 5001 em uso"
Altere a porta no final de `app.py`:
```python
app.run(debug=True, port=5002)  # Mudar de 5001 para 5002
```

### Erro ao cadastrar vendedor
✅ **JÁ CORRIGIDO!** Se ainda ocorrer:
1. Verifique se o email é único
2. Verifique se o CPF é único
3. Campos supervisor e equipe são opcionais

---

## 🎯 Checklist de Testes

- [ ] Sistema inicia sem erros
- [ ] Login com admin funciona
- [ ] Cadastrar 1º vendedor ✅
- [ ] Cadastrar 2º vendedor ✅
- [ ] Cadastrar 3º vendedor ✅
- [ ] Criar equipe
- [ ] Criar meta
- [ ] Dashboard exibe dados
- [ ] Exportar PDF
- [ ] Acessar manual
- [ ] Editar vendedor
- [ ] Editar meta

---

## 📊 Estrutura do Banco de Dados

O sistema usa SQLite localmente (desenvolvimento):
```
📁 suameta/
  └── metas.db (criado automaticamente)
```

Para produção, o Railway usa PostgreSQL.

---

## 🔄 Resetar Banco de Dados

Se quiser começar do zero:
```powershell
# Parar o sistema (CTRL+C)

# Deletar banco de dados
Remove-Item metas.db

# Reiniciar sistema
python app.py
```

---

## 📝 Próximos Passos Após Testes

### Testar Deploy no Railway

1. **Criar conta no Railway:**
   - Acesse https://railway.app
   - Login com GitHub

2. **Criar projeto:**
   - New Project → Deploy from GitHub
   - Selecione `suameta`

3. **Adicionar PostgreSQL:**
   - + New → Database → PostgreSQL

4. **Gerar domínio:**
   - Settings → Networking → Generate Domain

5. **Aguardar deploy:**
   - ~3 minutos
   - Sistema disponível publicamente!

---

## 📞 Suporte

Problemas? Entre em contato:

**Cristiano Santos**  
📱 WhatsApp: (71) 99337-2960  
📧 Email: cristiano.s.santos@ba.estudante.senai.br

**Horário:**
- Segunda a Sexta: 8h às 18h
- Sábado: 8h às 12h

---

## ✅ Confirmação de Funcionamento

Após seguir este guia, você deve conseguir:
- ✅ Iniciar o sistema localmente
- ✅ Fazer login
- ✅ Cadastrar múltiplos vendedores
- ✅ Criar metas e equipes
- ✅ Visualizar dashboard
- ✅ Acessar manual do usuário

**Sistema 100% Funcional!** 🎉
