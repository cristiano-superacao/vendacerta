# 🌐 Documentação da API REST - VendaCerta

> **Referência completa de todos os endpoints da API REST do sistema VendaCerta**

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Autenticação](#-autenticação)
- [Endpoints Públicos](#-endpoints-públicos)
- [API de Ranking](#-api-de-ranking)
- [API de Metas](#-api-de-metas)
- [API de Comissões](#-api-de-comissões)
- [API de Vendedores](#-api-de-vendedores)
- [Health Checks](#-health-checks)
- [Códigos de Status](#-códigos-de-status)
- [Exemplos de Uso](#-exemplos-de-uso)

---

## 🎯 Visão Geral

### Base URL

| Ambiente | URL Base |
|----------|----------|
| **Produção** | `https://vendacerta.up.railway.app` |
| **Desenvolvimento** | `http://127.0.0.1:5000` |

### Formato de Resposta

Todas as respostas da API são em **JSON** com o seguinte formato padrão:

**Sucesso**:
```json
{
  "success": true,
  "data": { ... },
  "message": "Operação realizada com sucesso"
}
```

**Erro**:
```json
{
  "success": false,
  "error": "Descrição do erro",
  "code": "ERROR_CODE"
}
```

### Content-Type

- **Request**: `application/json`
- **Response**: `application/json; charset=utf-8`

### Rate Limiting

| Endpoint | Limite |
|----------|--------|
| `/api/*` (geral) | 200 requisições/dia, 50/hora |
| `/api/ranking` | 100 requisições/hora |
| `/health`, `/ping` | Sem limite |

---

## 🔐 Autenticação

### Autenticação via Sessão (Cookie)

A API utiliza **sessões baseadas em cookies** (Flask-Login).

#### Login
```http
POST /login
Content-Type: application/x-www-form-urlencoded

email=usuario@empresa.com&senha=senha123
```

**Resposta de Sucesso**:
```http
HTTP/1.1 302 Found
Set-Cookie: session=eyJfaWQiOnsid...
Location: /dashboard
```

**Resposta de Erro**:
```http
HTTP/1.1 200 OK
Content-Type: text/html

<!-- Flash message: "E-mail ou senha inválidos" -->
```

#### Verificar Autenticação
```http
GET /api/me
Cookie: session=eyJfaWQiOnsid...
```

**Resposta**:
```json
{
  "success": true,
  "data": {
    "id": 5,
    "nome": "João Silva",
    "email": "joao@empresa.com",
    "cargo": "vendedor",
    "empresa_id": 1,
    "permissoes": {
      "pode_gerenciar_vendedores": false,
      "pode_ver_relatorios": true,
      "pode_gerenciar_clientes": true
    }
  }
}
```

### Autenticação em Requisições Subsequentes

Todas as requisições à API devem incluir o cookie de sessão:

```http
GET /api/ranking?mes=12&ano=2024
Cookie: session=eyJfaWQiOnsid...
```

**Sem autenticação**:
```json
{
  "success": false,
  "error": "Autenticação necessária",
  "code": "UNAUTHORIZED"
}
```

---

## 🌍 Endpoints Públicos

### GET /ping

**Descrição**: Endpoint de ping básico (health check simplificado)

**Autenticação**: ❌ Não requerida

**Requisição**:
```http
GET /ping
```

**Resposta**:
```json
{
  "status": "ok",
  "timestamp": "2024-12-18T14:30:00.000Z"
}
```

---

### GET /health

**Descrição**: Health check completo com verificação de banco de dados

**Autenticação**: ❌ Não requerida

**Requisição**:
```http
GET /health
```

**Resposta (Sistema Saudável)**:
```json
{
  "status": "healthy",
  "database": "ok",
  "version": "2.0.0",
  "excel_available": true,
  "timestamp": "2024-12-18T14:30:00.000Z",
  "uptime_seconds": 86400
}
```

**Resposta (Sistema com Problemas)**:
```json
{
  "status": "unhealthy",
  "database": "error",
  "version": "2.0.0",
  "excel_available": false,
  "timestamp": "2024-12-18T14:30:00.000Z",
  "error": "Database connection failed"
}
```

---

### GET /status/excel

**Descrição**: Verifica disponibilidade das bibliotecas Excel (pandas/openpyxl)

**Autenticação**: ❌ Não requerida

**Requisição**:
```http
GET /status/excel
```

**Resposta (Disponível)**:
```json
{
  "available": true,
  "pandas_version": "2.3.3",
  "openpyxl_version": "3.1.2"
}
```

**Resposta (Indisponível)**:
```json
{
  "available": false,
  "error": "pandas module not found",
  "solutions": [
    "pip install pandas",
    "pip install openpyxl",
    "Verifique requirements.txt"
  ]
}
```

---

## 🏆 API de Ranking

### GET /api/ranking

**Descrição**: Retorna o ranking de vendedores ordenado por percentual de alcance de meta

**Autenticação**: ✅ Requerida

**Permissões**: `pode_ver_relatorios`

**Parâmetros de Query**:

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `mes` | integer | ❌ | Mês (1-12). Padrão: mês atual | `mes=12` |
| `ano` | integer | ❌ | Ano. Padrão: ano atual | `ano=2024` |
| `equipe_id` | integer | ❌ | Filtrar por equipe | `equipe_id=3` |

**Requisição**:
```http
GET /api/ranking?mes=12&ano=2024&equipe_id=1
Cookie: session=eyJfaWQiOnsid...
```

**Resposta de Sucesso**:
```json
{
  "success": true,
  "data": [
    {
      "posicao": 1,
      "vendedor_id": 8,
      "nome": "Maria Santos",
      "email": "maria@empresa.com",
      "equipe": "Equipe Alpha",
      "supervisor": "Ana Costa",
      "meta": 60000.00,
      "receita": 75000.00,
      "percentual": 125.0,
      "faixa": "Excelente",
      "faixa_cor": "success",
      "comissao": 3750.00,
      "status_pagamento": "Pendente"
    },
    {
      "posicao": 2,
      "vendedor_id": 5,
      "nome": "João Silva",
      "email": "joao@empresa.com",
      "equipe": "Equipe Alpha",
      "supervisor": "Ana Costa",
      "meta": 50000.00,
      "receita": 53000.00,
      "percentual": 106.0,
      "faixa": "Boa",
      "faixa_cor": "primary",
      "comissao": 2120.00,
      "status_pagamento": "Pendente"
    }
  ],
  "meta": {
    "mes": 12,
    "ano": 2024,
    "equipe_id": 1,
    "total_vendedores": 2,
    "meta_total": 110000.00,
    "receita_total": 128000.00,
    "percentual_medio": 116.36,
    "comissao_total": 5870.00
  }
}
```

**Resposta de Erro (Sem Permissão)**:
```json
{
  "success": false,
  "error": "Você não tem permissão para acessar este recurso",
  "code": "FORBIDDEN"
}
```

**Resposta de Erro (Parâmetros Inválidos)**:
```json
{
  "success": false,
  "error": "Mês inválido. Use valores entre 1 e 12",
  "code": "INVALID_PARAMETERS"
}
```

---

## 📊 API de Metas

### GET /api/metas/dados-grafico/:vendedor_id

**Descrição**: Retorna dados para geração de gráfico de evolução de metas de um vendedor

**Autenticação**: ✅ Requerida

**Permissões**: 
- `pode_ver_relatorios` (para qualquer vendedor)
- Vendedor pode ver apenas seus próprios dados

**Parâmetros de URL**:

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `vendedor_id` | integer | ID do vendedor |

**Parâmetros de Query**:

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `meses` | integer | ❌ | Quantidade de meses passados. Padrão: 6 | `meses=12` |

**Requisição**:
```http
GET /api/metas/dados-grafico/5?meses=6
Cookie: session=eyJfaWQiOnsid...
```

**Resposta de Sucesso**:
```json
{
  "success": true,
  "data": {
    "vendedor": {
      "id": 5,
      "nome": "João Silva",
      "equipe": "Equipe Alpha"
    },
    "periodo": {
      "inicio": "2024-07-01",
      "fim": "2024-12-31",
      "meses": 6
    },
    "metas": [
      {
        "mes": 7,
        "ano": 2024,
        "mes_ano": "Jul/2024",
        "meta": 50000.00,
        "receita": 48000.00,
        "percentual": 96.0,
        "comissao": 1440.00,
        "faixa": "Meta"
      },
      {
        "mes": 8,
        "ano": 2024,
        "mes_ano": "Ago/2024",
        "meta": 50000.00,
        "receita": 52000.00,
        "percentual": 104.0,
        "comissao": 2080.00,
        "faixa": "Boa"
      },
      {
        "mes": 9,
        "ano": 2024,
        "mes_ano": "Set/2024",
        "meta": 55000.00,
        "receita": 58000.00,
        "percentual": 105.45,
        "comissao": 2320.00,
        "faixa": "Boa"
      },
      {
        "mes": 10,
        "ano": 2024,
        "mes_ano": "Out/2024",
        "meta": 55000.00,
        "receita": 70000.00,
        "percentual": 127.27,
        "comissao": 3500.00,
        "faixa": "Excelente"
      },
      {
        "mes": 11,
        "ano": 2024,
        "mes_ano": "Nov/2024",
        "meta": 60000.00,
        "receita": 55000.00,
        "percentual": 91.67,
        "comissao": 1650.00,
        "faixa": "Meta"
      },
      {
        "mes": 12,
        "ano": 2024,
        "mes_ano": "Dez/2024",
        "meta": 60000.00,
        "receita": 53000.00,
        "percentual": 88.33,
        "comissao": 1590.00,
        "faixa": "Meta"
      }
    ],
    "totalizadores": {
      "meta_total": 330000.00,
      "receita_total": 336000.00,
      "percentual_medio": 102.12,
      "comissao_total": 12580.00,
      "melhor_mes": {
        "mes_ano": "Out/2024",
        "percentual": 127.27
      },
      "pior_mes": {
        "mes_ano": "Dez/2024",
        "percentual": 88.33
      }
    }
  }
}
```

**Resposta de Erro (Vendedor não encontrado)**:
```json
{
  "success": false,
  "error": "Vendedor não encontrado",
  "code": "NOT_FOUND"
}
```

**Resposta de Erro (Acesso negado)**:
```json
{
  "success": false,
  "error": "Você só pode visualizar seus próprios dados",
  "code": "FORBIDDEN"
}
```

---

## 💰 API de Comissões

### GET /api/comissoes/faixas

**Descrição**: Retorna as faixas de comissão configuradas para a empresa

**Autenticação**: ✅ Requerida

**Permissões**: `pode_ver_comissoes`

**Parâmetros de Query**:

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `apenas_ativas` | boolean | ❌ | Retornar apenas faixas ativas. Padrão: true | `apenas_ativas=false` |

**Requisição**:
```http
GET /api/comissoes/faixas?apenas_ativas=true
Cookie: session=eyJfaWQiOnsid...
```

**Resposta de Sucesso**:
```json
{
  "success": true,
  "data": {
    "faixas": [
      {
        "id": 1,
        "nome": "Crítica",
        "alcance_min": 0,
        "alcance_max": 50,
        "taxa_comissao": 0.01,
        "taxa_percentual": 1.0,
        "cor": "danger",
        "ordem": 0,
        "ativa": true
      },
      {
        "id": 2,
        "nome": "Baixa",
        "alcance_min": 50,
        "alcance_max": 75,
        "taxa_comissao": 0.02,
        "taxa_percentual": 2.0,
        "cor": "warning",
        "ordem": 1,
        "ativa": true
      },
      {
        "id": 3,
        "nome": "Meta",
        "alcance_min": 75,
        "alcance_max": 100,
        "taxa_comissao": 0.03,
        "taxa_percentual": 3.0,
        "cor": "info",
        "ordem": 2,
        "ativa": true
      },
      {
        "id": 4,
        "nome": "Boa",
        "alcance_min": 100,
        "alcance_max": 125,
        "taxa_comissao": 0.04,
        "taxa_percentual": 4.0,
        "cor": "primary",
        "ordem": 3,
        "ativa": true
      },
      {
        "id": 5,
        "nome": "Excelente",
        "alcance_min": 125,
        "alcance_max": 1000,
        "taxa_comissao": 0.05,
        "taxa_percentual": 5.0,
        "cor": "success",
        "ordem": 4,
        "ativa": true
      }
    ],
    "total": 5
  }
}
```

**Exemplo de Cálculo**:
```javascript
// Dado um vendedor com:
const meta = 50000;
const receita = 53000;
const percentual = (receita / meta) * 100; // 106%

// Encontrar faixa:
const faixa = faixas.find(f => 
  percentual >= f.alcance_min && percentual <= f.alcance_max
);
// faixa = { nome: "Boa", taxa_comissao: 0.04 }

// Calcular comissão:
const comissao = receita * faixa.taxa_comissao;
// comissao = 53000 * 0.04 = 2120.00
```

---

## 📄 Parâmetros de Relatórios (Páginas HTML)

Embora não sejam endpoints JSON, algumas páginas aceitam parâmetros de query para compor relatórios.

### GET /relatorios/metas-avancado

**Descrição**: Página de relatório com visão alternável entre vendedores e supervisores.

**Parâmetros de Query**:

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `visao` | string | ❌ | `vendedor` (padrão) ou `supervisor` | `visao=supervisor` |
| `supervisor_id` | integer | ❌ | Filtra por supervisor (quando `visao=supervisor`) | `supervisor_id=12` |
| `vendedor_id` | integer | ❌ | Filtra por vendedor (quando `visao=vendedor`) | `vendedor_id=34` |
| `tipo_meta` | string | ❌ | `valor` ou `volume` | `tipo_meta=valor` |
| `ano` | integer | ❌ | Ano de referência | `ano=2025` |
| `mes` | integer | ❌ | Mês (1-12) | `mes=12` |

**Observações**:
- Na visão `supervisor`, são exibidos consolidadores e a **taxa/comissão do supervisor** quando o tipo de meta é `valor`.
- Na visão `vendedor`, permanecem os gráficos e o ranking mensal originais.

## 👥 API de Vendedores

### GET /api/vendedor/:id/supervisor

**Descrição**: Retorna informações do supervisor de um vendedor

**Autenticação**: ✅ Requerida

**Permissões**: 
- `pode_gerenciar_vendedores` (para qualquer vendedor)
- Vendedor pode ver apenas seu próprio supervisor

**Parâmetros de URL**:

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `id` | integer | ID do vendedor |

**Requisição**:
```http
GET /api/vendedor/5/supervisor
Cookie: session=eyJfaWQiOnsid...
```

**Resposta de Sucesso**:
```json
{
  "success": true,
  "data": {
    "vendedor": {
      "id": 5,
      "nome": "João Silva",
      "email": "joao@empresa.com"
    },
    "supervisor": {
      "id": 3,
      "nome": "Ana Costa",
      "email": "ana@empresa.com",
      "telefone": "(11) 99999-8888",
      "cargo": "supervisor"
    },
    "equipe": {
      "id": 1,
      "nome": "Equipe Alpha",
      "descricao": "Equipe de vendas da região Sul"
    }
  }
}
```

**Resposta (Vendedor sem supervisor)**:
```json
{
  "success": true,
  "data": {
    "vendedor": {
      "id": 12,
      "nome": "Pedro Lima",
      "email": "pedro@empresa.com"
    },
    "supervisor": null,
    "equipe": null
  }
}
```

**Resposta de Erro (Vendedor não encontrado)**:
```json
{
  "success": false,
  "error": "Vendedor não encontrado",
  "code": "NOT_FOUND"
}
```

---

## 🏥 Health Checks

### Railway Health Checks

O Railway verifica automaticamente a saúde da aplicação através dos endpoints:

**Endpoint Principal**: `/health`

**Configuração no Railway** (`railway.json`):
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

**Interpretação de Status**:

| Status HTTP | Significado | Ação Railway |
|-------------|-------------|--------------|
| 200 OK | Aplicação saudável | Continua operando |
| 500/503 | Aplicação com problemas | Tenta reiniciar (max 3x) |
| Timeout (>300s) | Aplicação travada | Força reinício |

**Monitoramento**:
```bash
# Via curl
curl https://vendacerta.up.railway.app/health

# Via Railway CLI
railway logs --follow

# Ver métricas
# Railway Dashboard → Metrics → Health Checks
```

---

## 📝 Códigos de Status HTTP

### Códigos de Sucesso

| Código | Descrição | Uso |
|--------|-----------|-----|
| **200 OK** | Requisição bem-sucedida | GET, POST com sucesso |
| **201 Created** | Recurso criado | POST criando novo registro |
| **204 No Content** | Sucesso sem conteúdo | DELETE bem-sucedido |

### Códigos de Redirecionamento

| Código | Descrição | Uso |
|--------|-----------|-----|
| **302 Found** | Redirecionamento temporário | Após login/logout |

### Códigos de Erro do Cliente

| Código | Descrição | Uso |
|--------|-----------|-----|
| **400 Bad Request** | Dados inválidos | Parâmetros incorretos |
| **401 Unauthorized** | Não autenticado | Sem sessão válida |
| **403 Forbidden** | Sem permissão | Permissão negada |
| **404 Not Found** | Recurso não encontrado | ID inexistente |
| **422 Unprocessable Entity** | Validação falhou | Campos obrigatórios ausentes |
| **429 Too Many Requests** | Rate limit excedido | Muitas requisições |

### Códigos de Erro do Servidor

| Código | Descrição | Uso |
|--------|-----------|-----|
| **500 Internal Server Error** | Erro no servidor | Exceção não tratada |
| **503 Service Unavailable** | Serviço indisponível | Banco offline |

---

## 💻 Exemplos de Uso

### JavaScript/Fetch API

#### Buscar Ranking
```javascript
// Com autenticação de sessão (cookie enviado automaticamente)
fetch('/api/ranking?mes=12&ano=2024', {
  method: 'GET',
  credentials: 'include', // Importante: incluir cookies
  headers: {
    'Accept': 'application/json'
  }
})
.then(response => {
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
})
.then(data => {
  if (data.success) {
    console.log('Ranking:', data.data);
    console.log('Total vendedores:', data.meta.total_vendedores);
  } else {
    console.error('Erro:', data.error);
  }
})
.catch(error => {
  console.error('Erro na requisição:', error);
});
```

#### Buscar Dados de Gráfico
```javascript
async function carregarGraficoVendedor(vendedorId, meses = 6) {
  try {
    const response = await fetch(
      `/api/metas/dados-grafico/${vendedorId}?meses=${meses}`,
      { credentials: 'include' }
    );
    
    const resultado = await response.json();
    
    if (resultado.success) {
      const { metas, totalizadores } = resultado.data;
      
      // Preparar dados para Chart.js
      const labels = metas.map(m => m.mes_ano);
      const datasetMetas = metas.map(m => m.meta);
      const datasetReceitas = metas.map(m => m.receita);
      
      // Renderizar gráfico
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Meta',
              data: datasetMetas,
              borderColor: '#ff6384'
            },
            {
              label: 'Receita',
              data: datasetReceitas,
              borderColor: '#36a2eb'
            }
          ]
        }
      });
    }
  } catch (error) {
    console.error('Erro ao carregar gráfico:', error);
  }
}

// Uso
carregarGraficoVendedor(5, 12);
```

---

### Python/Requests

#### Login e Buscar Ranking
```python
import requests
from datetime import datetime

# URL base
BASE_URL = 'https://vendacerta.up.railway.app'

# Criar sessão (mantém cookies)
session = requests.Session()

# 1. Fazer login
login_data = {
    'email': 'joao@empresa.com',
    'senha': 'senha123'
}

response = session.post(f'{BASE_URL}/login', data=login_data)

if response.status_code == 200:
    print('✅ Login realizado com sucesso')
    
    # 2. Buscar ranking
    params = {
        'mes': datetime.now().month,
        'ano': datetime.now().year
    }
    
    ranking_response = session.get(f'{BASE_URL}/api/ranking', params=params)
    ranking_data = ranking_response.json()
    
    if ranking_data['success']:
        print(f"\n🏆 Ranking de {ranking_data['meta']['total_vendedores']} vendedores:")
        
        for vendedor in ranking_data['data'][:5]:  # Top 5
            print(f"{vendedor['posicao']}º - {vendedor['nome']}: {vendedor['percentual']:.1f}% (R$ {vendedor['comissao']:.2f})")
    else:
        print(f"❌ Erro: {ranking_data['error']}")
else:
    print(f'❌ Erro no login: {response.status_code}')
```

#### Verificar Saúde do Sistema
```python
import requests
import time

def verificar_saude_sistema(url):
    """
    Verifica se o sistema está saudável
    """
    try:
        start = time.time()
        response = requests.get(f'{url}/health', timeout=10)
        latency = (time.time() - start) * 1000  # ms
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"Status: {data['status']}")
            print(f"Database: {data['database']}")
            print(f"Versão: {data['version']}")
            print(f"Excel disponível: {data['excel_available']}")
            print(f"Latência: {latency:.2f}ms")
            
            return data['status'] == 'healthy'
        else:
            print(f"❌ Status HTTP {response.status_code}")
            return False
            
    except requests.Timeout:
        print("❌ Timeout (>10s)")
        return False
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

# Uso
if verificar_saude_sistema('https://vendacerta.up.railway.app'):
    print("✅ Sistema operacional")
else:
    print("⚠️ Sistema com problemas")
```

---

### cURL

#### Buscar Ranking
```bash
# Login primeiro (salvar cookie)
curl -c cookies.txt \
  -X POST \
  -d "email=joao@empresa.com&senha=senha123" \
  https://vendacerta.up.railway.app/login

# Usar cookie para buscar ranking
curl -b cookies.txt \
  "https://vendacerta.up.railway.app/api/ranking?mes=12&ano=2024" \
  | jq '.data[] | {posicao, nome, percentual, comissao}'

# Saída esperada:
# {
#   "posicao": 1,
#   "nome": "Maria Santos",
#   "percentual": 125,
#   "comissao": 3750
# }
```

#### Health Check
```bash
# Verificação simples
curl https://vendacerta.up.railway.app/ping

# Verificação completa
curl https://vendacerta.up.railway.app/health | jq

# Monitorar continuamente (cada 5s)
watch -n 5 'curl -s https://vendacerta.up.railway.app/health | jq ".status, .database"'
```

#### Status Excel
```bash
curl https://vendacerta.up.railway.app/status/excel | jq

# Se disponível:
# {
#   "available": true,
#   "pandas_version": "2.3.3",
#   "openpyxl_version": "3.1.2"
# }

# Se indisponível:
# {
#   "available": false,
#   "error": "pandas module not found",
#   "solutions": [...]
# }
```

---

## 🔧 Tratamento de Erros

### Estrutura de Erro Padrão

```json
{
  "success": false,
  "error": "Descrição legível do erro",
  "code": "ERROR_CODE",
  "details": {
    "campo": "nome_do_campo",
    "mensagem": "Validação específica"
  }
}
```

### Códigos de Erro Comuns

| Código | Significado | Ação Recomendada |
|--------|-------------|------------------|
| `UNAUTHORIZED` | Não autenticado | Fazer login novamente |
| `FORBIDDEN` | Sem permissão | Verificar permissões do usuário |
| `NOT_FOUND` | Recurso não encontrado | Verificar ID do recurso |
| `INVALID_PARAMETERS` | Parâmetros inválidos | Corrigir parâmetros da requisição |
| `VALIDATION_ERROR` | Validação falhou | Verificar campos obrigatórios |
| `DATABASE_ERROR` | Erro no banco | Tentar novamente ou contatar suporte |
| `RATE_LIMIT_EXCEEDED` | Muitas requisições | Aguardar antes de tentar novamente |

### Exemplo de Tratamento

```javascript
async function buscarRankingComTratamento(mes, ano) {
  try {
    const response = await fetch(
      `/api/ranking?mes=${mes}&ano=${ano}`,
      { credentials: 'include' }
    );
    
    const data = await response.json();
    
    if (!data.success) {
      // Tratamento específico por código
      switch (data.code) {
        case 'UNAUTHORIZED':
          window.location.href = '/login';
          break;
        
        case 'FORBIDDEN':
          alert('Você não tem permissão para visualizar este conteúdo');
          break;
        
        case 'INVALID_PARAMETERS':
          console.error('Parâmetros inválidos:', data.details);
          break;
        
        case 'RATE_LIMIT_EXCEEDED':
          setTimeout(() => buscarRankingComTratamento(mes, ano), 60000);
          break;
        
        default:
          console.error('Erro desconhecido:', data.error);
      }
      
      return null;
    }
    
    return data.data;
    
  } catch (error) {
    console.error('Erro de rede:', error);
    return null;
  }
}
```

---

## 📚 Recursos Adicionais

### Documentação Relacionada
- 🏗️ [Arquitetura do Sistema](ARCHITECTURE.md)
- 🚀 [Guia de Início Rápido](GETTING_STARTED.md)
- 📖 [README Principal](../README.md)

### Links Úteis
- 🌐 **API Produção**: [vendacerta.up.railway.app](https://vendacerta.up.railway.app)
- 🐙 **Repositório GitHub**: [cristiano-superacao/vendacerta](https://github.com/cristiano-superacao/vendacerta)

---

<div align="center">

**VendaCerta v2.0.0 - API REST Documentation**  
Última atualização: Dezembro 2024

[⬅️ Voltar ao README](../README.md) | [📚 Documentação Completa](../INDICE_DOCUMENTACAO.md)

</div>
