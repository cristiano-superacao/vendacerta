# 🧪 Guia de Testes Locais - Sistema VendaCerta

> ⚠️ **ARQUIVO LEGADO/ARQUIVADO**: pode conter exemplos antigos.
> Não use credenciais/senhas fixas; siga `docs/GETTING_STARTED.md`.

## 🚀 Status do Servidor

✅ **Servidor Flask rodando em:**
- URL Local: http://127.0.0.1:5000
- URL Rede: http://192.168.0.101:5000
- Modo: Debug (desenvolvimento)
- Backup automático: Agendado para 02:00

---

## 🔐 Credenciais de Acesso

### Super Admin (Acesso Total)
```
Email: admin@sistema.com
Senha: (defina no seu ambiente; sem senha padrão)
```

### Usuário de Teste (se criado)
```
Email: teste@vendacerta.com
Senha: (defina no seu ambiente)
```

---

## ✅ Checklist de Testes

### 1. **Login e Dashboard** ✅
- [ ] Acessar http://127.0.0.1:5000
- [ ] Fazer login com credenciais admin
- [ ] Verificar dashboard principal
- [ ] Confirmar menu lateral responsivo

### 2. **Importação/Exportação de Clientes (NOVO)** 🆕

#### Teste de Formato Simples
- [ ] Acessar **Clientes → Importar Clientes**
- [ ] Selecionar **Formato Simples** (deve estar selecionado por padrão)
- [ ] Clicar em **Baixar Modelo em Branco**
  - ✅ Arquivo deve baixar: `modelo_importacao_clientes_simples.xlsx`
  - ✅ Deve ter 11 colunas
  - ✅ Linha 2 deve conter exemplo preenchido
- [ ] Clicar em **Exportar Clientes Atuais**
  - ✅ Arquivo deve baixar: `clientes_simples_YYYYMMDD_HHMMSS.xlsx`
  - ✅ Deve ter 17 colunas

#### Teste de Formato Estendido
- [ ] Selecionar **Formato Estendido** (radio button)
- [ ] Verificar mudança visual do card selecionado
- [ ] Clicar em **Baixar Modelo em Branco**
  - ✅ Arquivo deve baixar: `modelo_importacao_clientes_estendido.xlsx`
  - ✅ Deve ter 20 colunas (incluindo Razão Social, Sigla, IE, CEP, etc)
  - ✅ Linha 2 com exemplo completo
- [ ] Clicar em **Exportar Clientes Atuais**
  - ✅ Arquivo deve baixar: `clientes_estendido_YYYYMMDD_HHMMSS.xlsx`
  - ✅ Deve ter 27 colunas

#### Teste de Importação
- [ ] Abrir modelo baixado no Excel
- [ ] Preencher dados de teste (2-3 clientes)
- [ ] Salvar arquivo
- [ ] Fazer upload via formulário
- [ ] Verificar mensagem de sucesso
- [ ] Confirmar clientes na listagem

### 3. **Relatório de Metas Avançado** ✅

- [ ] Acessar **Relatórios → Metas Avançado**
- [ ] Verificar cards de estatísticas:
  - ✅ Total de Metas
  - ✅ Metas Atingidas
  - ✅ Taxa de Sucesso
  - ✅ Total Comissões
- [ ] Testar filtros:
  - [ ] Filtrar por vendedor
  - [ ] Filtrar por tipo (valor/volume)
  - [ ] Filtrar por ano
  - [ ] Filtrar por mês
- [ ] Verificar tabela de metas:
  - ✅ Barra de progresso deve mostrar percentual
  - ✅ Badge de comissão deve estar visível
  - ✅ Formato de data: MM/YYYY (ex: 12/2025)
- [ ] Clicar no botão de gráfico (📊):
  - ✅ Modal deve abrir
  - ✅ Gráfico com 2 linhas (Valor e Volume)
  - ✅ Eixo Y esquerdo: Valores em R$
  - ✅ Eixo Y direito: Volume em vendas
  - ✅ Últimos 12 meses de dados

### 4. **CRUD de Clientes**

- [ ] Acessar **Clientes → Listar Clientes**
- [ ] Criar novo cliente
- [ ] Editar cliente existente
- [ ] Verificar campos novos:
  - [ ] Razão Social
  - [ ] Sigla
  - [ ] Inscrição Estadual
  - [ ] Código BP
  - [ ] CEP
  - [ ] Coordenada X
  - [ ] Coordenada Y
  - [ ] Telefone 2
  - [ ] Celular
- [ ] Exportar cliente criado (formato estendido)
- [ ] Confirmar todos os campos na planilha

### 5. **Gestão de Metas**

- [ ] Acessar **Metas → Configurar Meta**
- [ ] Criar meta de valor
- [ ] Criar meta de volume
- [ ] Verificar cálculo de comissão
- [ ] Confirmar atualização no relatório

### 6. **Responsividade**

- [ ] Redimensionar janela do navegador
- [ ] Verificar menu lateral (sidebar) responsivo
- [ ] Testar em larguras:
  - [ ] Desktop (> 1200px)
  - [ ] Tablet (768px - 1199px)
  - [ ] Mobile (< 768px)
- [ ] Confirmar cards empilham em telas pequenas
- [ ] Verificar tabelas com scroll horizontal em mobile

### 7. **Validações de Formulários**

#### Importação de Clientes
- [ ] Tentar importar sem arquivo → Erro esperado
- [ ] Importar arquivo .txt → Erro de formato
- [ ] Importar Excel sem coluna "Nome" → Erro
- [ ] Importar com CPF duplicado → Registro ignorado
- [ ] Importar com CNPJ duplicado → Registro ignorado
- [ ] Importar arquivo > 10MB → Erro de tamanho

### 8. **Permissões de Acesso**

- [ ] Como **Vendedor**:
  - [ ] Deve ver apenas seus clientes
  - [ ] Deve ver apenas suas metas
  - [ ] Pode importar clientes apenas para si
  
- [ ] Como **Supervisor**:
  - [ ] Deve ver clientes da equipe
  - [ ] Deve ver metas da equipe
  - [ ] Pode configurar metas para vendedores

- [ ] Como **Admin**:
  - [ ] Acesso total a todos os dados
  - [ ] Pode exportar todos os clientes
  - [ ] Pode criar usuários e equipes

---

## 🎨 Validações Visuais

### Layout Bootstrap 5.3.3
- [ ] Tema verde principal (#1a4d2e) aplicado
- [ ] Cards com sombra sutil (`shadow-sm`)
- [ ] Ícones Bootstrap Icons carregados
- [ ] Badges coloridos conforme status
- [ ] Progress bars animadas

### Radio Buttons (Formato de Planilha)
- [ ] Cards dos radio buttons com hover effect
- [ ] Ícone verde para formato Simples
- [ ] Ícone azul para formato Estendido
- [ ] Texto explicativo visível
- [ ] Seleção visualmente destacada

### Gráfico Chart.js
- [ ] Carrega sem erros de console
- [ ] Tooltip aparece ao passar mouse
- [ ] Legend clicável para ocultar séries
- [ ] Eixos Y com formatação correta
- [ ] Responsivo ao redimensionar janela

---

## 🐛 Problemas Conhecidos e Soluções

### Problema 1: "Nenhum filtro chamado 'string.zfill'"
**Status:** ✅ CORRIGIDO
**Solução:** Alterado para `"%02d"|format(meta.mes)` no template

### Problema 2: "'estatisticas' é indefinido"
**Status:** ✅ CORRIGIDO
**Solução:** app.py agora passa dicionário `estatisticas` completo

### Problema 3: Campo `comissao_calculada` não existe
**Status:** ✅ CORRIGIDO
**Solução:** Alterado para `meta.comissao_total` (campo correto)

### Problema 4: Gráfico não carrega dados
**Status:** ✅ CORRIGIDO
**Solução:** API retorna estrutura `{evolucao: {labels, valores, volumes}, ranking}`

---

## 📊 Dados de Teste Sugeridos

### Planilha de Clientes (Formato Estendido)

| Nome | CPF | CNPJ | Razão Social | Sigla | IE | Código BP | Telefone | Telefone 2 | Celular | Email | Cidade | Bairro | CEP | Coordenada X | Coordenada Y | Dia Visita | Formas Pagamento | Obs |
|------|-----|------|--------------|-------|-------|-----------|----------|------------|---------|-------|--------|--------|-----|--------------|--------------|------------|------------------|-----|
| João Silva | 123.456.789-00 | | | JoãoBar | | BP-001 | (11) 3456-7890 | (11) 3456-7891 | (11) 98765-4321 | joao@test.com | São Paulo | Centro | 01310-100 | -46.633308 | -23.550520 | segunda | dinheiro, pix | Cliente VIP |
| Maria Santos | 987.654.321-00 | 12.345.678/0001-90 | Santos Comércio Ltda | SantosLtda | 123.456.789.012 | BP-002 | (11) 2222-3333 | | (11) 99999-8888 | maria@test.com | Campinas | Jardim | 13010-100 | -47.061960 | -22.907104 | terça | pix, cartao_credito | Pagamento em dia |
| Pedro Costa | 111.222.333-44 | | | PedroBar | | BP-003 | (11) 4444-5555 | (11) 4444-6666 | (11) 97777-6666 | pedro@test.com | Santos | Ponta da Praia | 11030-400 | -46.316667 | -23.966667 | quinta | dinheiro | Novo cliente |

### Comandos SQL para Verificar Dados

```sql
-- Ver todos os clientes
SELECT nome, cpf, cnpj, razao_social, sigla, cep FROM clientes;

-- Ver clientes com coordenadas
SELECT nome, coordenada_x, coordenada_y FROM clientes WHERE coordenada_x IS NOT NULL;

-- Ver total de clientes por vendedor
SELECT v.nome, COUNT(c.id) as total_clientes 
FROM vendedores v 
LEFT JOIN clientes c ON c.vendedor_id = v.id 
GROUP BY v.id;

-- Ver metas e comissões
SELECT v.nome, m.mes, m.ano, m.tipo_meta, m.valor_meta, m.receita_alcancada, m.comissao_total
FROM metas m
JOIN vendedores v ON m.vendedor_id = v.id
ORDER BY m.ano DESC, m.mes DESC;
```

---

## 🔍 Console do Navegador - Verificações

Abra DevTools (F12) e verifique:

### Console (sem erros críticos)
```
✅ Não deve haver erros vermelhos
✅ Chart.js deve carregar: "Chart.js v4.4.0"
✅ Bootstrap deve carregar: sem erros 404
```

### Network (recursos carregados)
```
✅ custom.css - 200 OK
✅ bootstrap.min.css - 200 OK
✅ bootstrap-icons.css - 200 OK
✅ chart.umd.min.js - 200 OK
```

### Application (service worker)
```
⚠️ service-worker.js pode dar 404 (normal em dev)
```

---

## 📈 Métricas de Performance (Esperadas)

- **Tempo de carregamento página:** < 2s
- **Tamanho planilha exportada:**
  - Simples: ~10-50 KB (dependendo do nº de clientes)
  - Estendida: ~15-70 KB
- **Tempo de importação:** < 5s para 100 clientes
- **Tempo de resposta API gráfico:** < 1s

---

## 🎯 Casos de Uso Reais

### Cenário 1: Vendedor Importa Planilha de Visitas
1. Vendedor recebe lista de clientes em Excel
2. Acessa sistema → Clientes → Importar
3. Seleciona formato (simples se só tem básico, estendido se tem todos os dados)
4. Baixa modelo em branco
5. Copia dados da planilha original para o modelo
6. Faz upload
7. Sistema importa e valida
8. Vendedor confirma clientes na listagem

### Cenário 2: Supervisor Exporta Base Completa
1. Supervisor precisa atualizar dados em massa
2. Acessa Clientes → Importar
3. Seleciona **Formato Estendido**
4. Clica em **Exportar Clientes Atuais**
5. Recebe planilha com 27 colunas completas
6. Edita campos no Excel (razão social, IE, coordenadas, etc)
7. Importa planilha editada
8. Sistema atualiza registros existentes

### Cenário 3: Admin Analisa Metas da Equipe
1. Admin acessa Relatórios → Metas Avançado
2. Vê cards com estatísticas gerais
3. Filtra por mês específico
4. Analisa tabela de metas
5. Clica no gráfico de um vendedor
6. Vê evolução dos últimos 12 meses
7. Identifica tendências e toma decisões

---

## 🆘 Troubleshooting

### Servidor não inicia
```bash
# Verificar se porta 5000 está em uso
netstat -ano | findstr :5000

# Matar processo se necessário
taskkill /PID <PID> /F

# Reiniciar servidor
python app.py
```

### Erro de importação de módulos
```bash
# Ativar ambiente virtual
.venv\Scripts\Activate.ps1

# Reinstalar dependências
pip install -r requirements.txt
```

### Banco de dados com erro
```bash
# Resetar banco de dados
python init_db.py
```

### Planilha não baixa
- Verificar popup blocker do navegador
- Testar com Ctrl+Shift+Click no botão
- Verificar console para erros JavaScript

---

## ✅ Checklist Final

- [ ] Servidor Flask rodando sem erros
- [ ] Login funcionando
- [ ] Dashboard carregando
- [ ] Importação/exportação simples OK
- [ ] Importação/exportação estendida OK
- [ ] Gráfico de metas carregando
- [ ] Filtros funcionando
- [ ] Layout responsivo
- [ ] Sem erros no console
- [ ] Performance aceitável

---

## 📞 Suporte

Se encontrar problemas:
1. Verificar console do navegador (F12)
2. Verificar terminal do Flask (erros em vermelho)
3. Consultar documentação: `DOCUMENTACAO_CONSOLIDADA.md`
4. Revisar este guia de testes

---

**Última atualização:** 16 de dezembro de 2025, 23:47  
**Versão do sistema:** 2.9.0  
**Status:** ✅ Pronto para testes completos
