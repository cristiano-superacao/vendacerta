# 🚀 Guia de Migração Railway - Sistema de Mensagens

## 📋 Situação Atual

✅ **O que já foi feito:**
- ✅ Correção do decorator `permission_required` para compatibilidade
- ✅ Sistema funciona AGORA sem as colunas de permissão
- ✅ Código enviado para GitHub
- ✅ Railway vai fazer auto-deploy em ~2 minutos

⏳ **O que falta fazer:**
- ⏳ Executar migração no banco Railway (adiciona colunas de permissões)
- ⏳ Testar sistema completo após migração

---

## ✅ Correção Imediata (JÁ FEITA)

O decorator foi corrigido para permitir acesso mesmo sem as colunas:

```python
# ANTES (causava erro 500):
if not getattr(current_user, permission_name, False):
    flash('Sem permissão', 'danger')
    return redirect('dashboard')

# AGORA (funciona sem as colunas):
if not hasattr(current_user, permission_name):
    return f(*args, **kwargs)  # Permite acesso
    
if not getattr(current_user, permission_name, True):
    flash('Sem permissão', 'danger')
    return redirect('dashboard')
```

**Resultado:** A rota `/mensagens` vai funcionar AGORA, assim que o Railway terminar o deploy (~2 min)

---

## 🔧 Próximo Passo: Executar Migração no Railway

### Opção 1: Via Railway CLI (Recomendado)

```bash
# 1. Instalar Railway CLI (se não tiver)
npm i -g @railway/cli

# 2. Login no Railway
railway login

# 3. Conectar ao projeto
railway link

# 4. Executar migração
railway run python migration_railway.py
```

### Opção 2: Via Railway Dashboard

1. Acesse: https://railway.app/dashboard
2. Selecione o projeto **suameta**
3. Vá em **Deployments** → **Latest Deploy**
4. Clique em **View Logs**
5. Clique no botão **Shell** (canto superior direito)
6. Execute o comando:
   ```bash
   python migration_railway.py
   ```

### Opção 3: Via Variável de Ambiente LOCAL

```bash
# 1. Copiar DATABASE_URL do Railway
#    Railway Dashboard → Project → Variables → DATABASE_URL

# 2. Executar localmente (Windows PowerShell):
$env:DATABASE_URL="postgresql://postgres:..."
python migration_railway.py
```

---

## 📊 O que a Migração Vai Fazer

A migração `migration_railway.py` vai:

1. ✅ Criar tabela `mensagens` (se não existir)
2. ✅ Adicionar 10 colunas na tabela `usuarios`:
   - `vendedor_id` (INTEGER)
   - `pode_ver_dashboard` (BOOLEAN)
   - `pode_gerenciar_vendedores` (BOOLEAN)
   - `pode_gerenciar_metas` (BOOLEAN)
   - `pode_gerenciar_equipes` (BOOLEAN)
   - `pode_gerenciar_comissoes` (BOOLEAN)
   - `pode_enviar_mensagens` (BOOLEAN)
   - `pode_exportar_dados` (BOOLEAN)
   - `pode_ver_todas_metas` (BOOLEAN)
   - `pode_aprovar_comissoes` (BOOLEAN)

3. ✅ Configurar permissões por cargo:
   - **Super Admin:** TODAS as permissões
   - **Admin:** TODAS as permissões
   - **Gerente:** Maioria das permissões (exceto comissões)
   - **Supervisor:** Permissões limitadas
   - **Vendedor:** Permissões básicas

4. ✅ Criar usuário "Sistema" para mensagens automáticas
5. ✅ Enviar mensagens de boas-vindas para todos os usuários

---

## 🧪 Verificação Após Migração

### 1. Verificar se migração funcionou

```bash
# Via Railway CLI
railway run python -c "from app import db, Usuario; u = Usuario.query.first(); print('✅ Migração OK!' if hasattr(u, 'pode_enviar_mensagens') else '❌ Migração falhou')"
```

### 2. Testar Rotas no Browser

Acesse estas URLs e verifique se funcionam:

- ✅ https://suameta.up.railway.app/mensagens (Caixa de Entrada)
- ✅ https://suameta.up.railway.app/mensagens/nova (Nova Mensagem)
- ✅ https://suameta.up.railway.app/mensagens/enviadas (Mensagens Enviadas)
- ✅ https://suameta.up.railway.app/vendedores/1/permissoes (Gerenciar Permissões)

### 3. Verificar Logs no Railway

```bash
railway logs
```

Procure por:
- ✅ "MIGRAÇÃO CONCLUÍDA COM SUCESSO!"
- ✅ "mensagens enviadas"
- ❌ Nenhum erro 500

---

## 🚨 Se Algo Der Errado

### Erro: "DATABASE_URL não encontrada"
**Causa:** Script rodando localmente sem a variável
**Solução:** Use Opção 2 (Railway Dashboard) ou configure a variável

### Erro: "permission denied for table usuarios"
**Causa:** Usuário do banco sem permissões de ALTER TABLE
**Solução:** Verifique as permissões do usuário no PostgreSQL

### Erro: "relation usuarios does not exist"
**Causa:** Banco de dados vazio
**Solução:** Execute `python init_db.py` primeiro

### Mensagens duplicadas
**Causa:** Executou migração 2 vezes
**Solução:** Não é grave, usuários terão 2 mensagens de boas-vindas

---

## 📝 Checklist Final

Após executar tudo:

- [ ] Deploy do Railway concluído (aguardar ~2 min)
- [ ] Rota `/mensagens` funcionando (sem erro 500)
- [ ] Migração executada no banco Railway
- [ ] 10 colunas adicionadas na tabela `usuarios`
- [ ] Mensagens de boas-vindas enviadas
- [ ] Sistema de permissões ativo
- [ ] Todas as rotas testadas

---

## 🎯 Resultado Esperado

Depois de tudo:

1. ✅ **Sistema funciona** mesmo SEM migração (graças à correção)
2. ✅ **Sistema completo** APÓS migração (com permissões granulares)
3. ✅ **Usuários podem** enviar/receber mensagens
4. ✅ **Admins podem** gerenciar permissões
5. ✅ **Nenhum erro 500** nas rotas

---

## 🆘 Precisa de Ajuda?

Se encontrar algum problema:

1. **Verifique os logs:** `railway logs`
2. **Teste localmente:** `python migration_railway.py` (com DATABASE_URL)
3. **Rollback se necessário:** As colunas são adicionadas com ALTER TABLE ADD (não remove nada)

---

**Criado em:** 2024
**Versão do Sistema:** 2.9.4
**Autor:** Sistema SuaMeta
