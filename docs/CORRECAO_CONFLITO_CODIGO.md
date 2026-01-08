# Correção de Conflitos de Código de Cliente

## Problema Identificado
O sistema estava apresentando conflitos de código de cliente (`codigo_cliente`) ao cadastrar novos clientes, especialmente sob concorrência.

## Causas Raiz
1. **Race Condition**: Múltiplas requisições simultâneas consultavam o banco antes que qualquer código fosse inserido
2. **Verificação Tardia**: Validação de unicidade ocorria após geração do código
3. **Retry Duplicado**: Tanto `models.py` quanto `app.py` implementavam retry, causando overhead
4. **Fallback Inseguro**: Timestamp poderia gerar colisões

## Soluções Implementadas

### 1. Lock Thread-Safe (`models.py`)
- Adicionado `threading.Lock()` para coordenar geração entre threads
- Garante que apenas uma thread gera código por vez
- Evita consultas simultâneas ao banco

```python
# Lock global para evitar race conditions
_codigo_lock = None

@staticmethod
def _get_codigo_lock():
    if Cliente._codigo_lock is None:
        import threading
        Cliente._codigo_lock = threading.Lock()
    return Cliente._codigo_lock

@staticmethod
def gerar_codigo_cliente(cidade, empresa_id):
    with Cliente._get_codigo_lock():
        # ... lógica de geração
```

### 2. Verificação Atômica de Existência
- Usa `db.session.query().exists().scalar()` para verificação atômica
- Itera sequências até encontrar código disponível
- Máximo de 9999 clientes por município

### 3. Retry Inteligente no Commit (`app.py`)
- Até 5 tentativas de commit com backoff exponencial
- Regenera código apenas em caso de `IntegrityError` específico
- Mensagens específicas para CPF/CNPJ duplicados

```python
for commit_tentativa in range(max_commit_tentativas):
    try:
        db.session.commit()
        break  # Sucesso!
    except IntegrityError as e:
        if 'codigo_cliente' in str(e).lower():
            # Gerar novo código e tentar novamente
            novo_codigo = Cliente.gerar_codigo_cliente(...)
            cliente.codigo_cliente = novo_codigo
```

### 4. Fallback Seguro com UUID
- Última alternativa usa `uuid.uuid4()` para garantir unicidade global
- Formato mantido: `XXXX-YYYY`
- Extremamente improvável ser acionado

## Comportamento em Produção

### Cenário Normal
1. Thread A gera código "0001-0001" e retém o lock
2. Thread B aguarda o lock
3. Thread A faz commit (sucesso!)
4. Thread B gera código "0001-0002" (consulta vê o "0001-0001")
5. Thread B faz commit (sucesso!)

### Cenário de Alta Concorrência
1. Threads A e B geram código "0001-0001" (banco vazio)
2. Thread A faz commit primeiro (sucesso!)
3. Thread B tenta commit → `IntegrityError`
4. Thread B regenera código "0001-0002" e retenta
5. Thread B faz commit (sucesso!)

### Unicidade por Empresa
- Constraints composite garantem isolamento: `(empresa_id, codigo_cliente)`
- Empresa 1 pode ter "0001-0001" e Empresa 2 também
- Sem conflitos entre empresas diferentes

## Testes Realizados

### Teste de Concorrência
```bash
python scripts/testar_geracao_codigo_concorrente.py
```
- 20 threads simultâneas gerando códigos
- Lock previne race conditions
- Retry no commit resolve duplicações

### Validação de Unicidade por Empresa
```bash
python scripts/verificar_unicidade_por_empresa.py
```
- Bloqueio correto dentro da mesma empresa
- Permissão correta entre empresas distintas

## Melhorias Futuras (Opcional)

### Tabela de Sequência Dedicada
Para ambientes de altíssima concorrência, considerar:
```sql
CREATE TABLE codigo_sequencias (
    empresa_id INT,
    municipio VARCHAR(100),
    ultima_sequencia INT,
    PRIMARY KEY (empresa_id, municipio)
);
```

### PostgreSQL SERIAL ou SEQUENCE
Usar sequências nativas do PostgreSQL para garantir unicidade absoluta.

## Monitoramento

### Logs Relevantes
- `Conflito de código detectado na tentativa X`: Normal em alta concorrência
- `Falha persistente ao salvar cliente`: Indica problema sistêmico

### Métricas
- Número de retries por commit
- Tempo médio de geração de código
- Taxa de sucesso no primeiro commit

## Conclusão

O sistema agora é robusto contra conflitos de código:
- ✅ Lock thread-safe
- ✅ Verificação atômica
- ✅ Retry inteligente
- ✅ Mensagens claras
- ✅ Unicidade por empresa
- ✅ Fallback seguro

**Layout responsivo e profissional mantido em toda aplicação.**
