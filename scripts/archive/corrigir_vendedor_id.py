"""
Corrige o campo vendedor_id para permitir NULL
"""
import sqlite3

conn = sqlite3.connect('instance/vendacerta.db')
cursor = conn.cursor()

print("\n" + "="*70)
print("🔧 CORRIGINDO CONSTRAINT vendedor_id")
print("="*70)

# SQLite não permite ALTER COLUMN diretamente, precisa recriar a tabela
print("\n📦 Fazendo backup dos dados...")
cursor.execute("SELECT * FROM clientes")
dados = cursor.fetchall()
print(f"   ✅ {len(dados)} clientes salvos")

# Pega estrutura atual
cursor.execute("PRAGMA table_info(clientes)")
colunas = cursor.fetchall()
print(f"\n📊 Total de colunas: {len(colunas)}")

# Criar tabela temporária
print("\n🏗️  Criando tabela temporária...")
cursor.execute("""
CREATE TABLE clientes_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(200) NOT NULL,
    razao_social VARCHAR(200),
    sigla VARCHAR(50),
    cpf VARCHAR(14),
    cnpj VARCHAR(18),
    inscricao_estadual VARCHAR(20),
    codigo_bp VARCHAR(50),
    codigo_cliente VARCHAR(9) UNIQUE,
    logradouro VARCHAR(255),
    municipio VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    cep VARCHAR(10),
    ponto_referencia VARCHAR(255),
    coordenada_x VARCHAR(50),
    coordenada_y VARCHAR(50),
    telefone VARCHAR(20),
    telefone2 VARCHAR(20),
    celular VARCHAR(20),
    email VARCHAR(120),
    formas_pagamento TEXT,
    dia_visita VARCHAR(50),
    vendedor_id INTEGER,
    empresa_id INTEGER,
    ativo BOOLEAN DEFAULT 1,
    observacoes TEXT,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vendedor_id) REFERENCES vendedores (id),
    FOREIGN KEY (empresa_id) REFERENCES empresas (id)
)
""")
print("   ✅ Tabela temporária criada")

# Copiar dados
if dados:
    print(f"\n♻️  Copiando {len(dados)} registros...")
    cursor.execute("""
        INSERT INTO clientes_new SELECT * FROM clientes
    """)
    print("   ✅ Dados copiados")

# Remover tabela antiga e renomear
print("\n🔄 Substituindo tabelas...")
cursor.execute("DROP TABLE clientes")
cursor.execute("ALTER TABLE clientes_new RENAME TO clientes")
print("   ✅ Tabela substituída")

# Recriar índices
print("\n🔑 Recriando índices...")
indices = [
    "CREATE INDEX ix_clientes_nome ON clientes (nome)",
    "CREATE UNIQUE INDEX ix_clientes_cpf ON clientes (cpf)",
    "CREATE UNIQUE INDEX ix_clientes_cnpj ON clientes (cnpj)",
    "CREATE INDEX ix_clientes_vendedor_id ON clientes (vendedor_id)",
    "CREATE INDEX ix_clientes_empresa_id ON clientes (empresa_id)",
    "CREATE INDEX ix_clientes_data_cadastro ON clientes (data_cadastro)",
    "CREATE INDEX ix_clientes_municipio ON clientes (municipio)",
    "CREATE UNIQUE INDEX idx_codigo_cliente ON clientes (codigo_cliente)"
]

for idx in indices:
    try:
        cursor.execute(idx)
        print(f"   ✅ {idx.split('INDEX')[1].split('ON')[0].strip()}")
    except Exception as e:
        print(f"   ⚠️  Erro: {e}")

conn.commit()

# Verificar
cursor.execute("PRAGMA table_info(clientes)")
colunas = cursor.fetchall()
for col in colunas:
    if col[1] == 'vendedor_id':
        print(f"\n✅ vendedor_id: NOT NULL = {col[3]} (0 = permite NULL)")

conn.close()

print("\n" + "="*70)
print("✅ CONSTRAINT CORRIGIDA COM SUCESSO!")
print("="*70)
