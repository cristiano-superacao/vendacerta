"""
Adiciona os campos logradouro e municipio ao banco vendacerta.db
"""
import sqlite3

conn = sqlite3.connect('instance/vendacerta.db')
cursor = conn.cursor()

print("\n" + "="*70)
print("🔧 ADICIONANDO CAMPOS LOGRADOURO E MUNICÍPIO")
print("="*70)

# Verifica estrutura atual
cursor.execute("PRAGMA table_info(clientes)")
colunas = cursor.fetchall()
nomes_colunas = [col[1] for col in colunas]
print(f"\n📊 Total de colunas antes: {len(colunas)}")

# Adiciona logradouro se não existir
if 'logradouro' not in nomes_colunas:
    print("\n➕ Adicionando coluna 'logradouro'...")
    cursor.execute("ALTER TABLE clientes ADD COLUMN logradouro VARCHAR(255)")
    print("   ✅ Coluna 'logradouro' adicionada")
else:
    print("\n✅ Coluna 'logradouro' já existe")

# Adiciona municipio se não existir
if 'municipio' not in nomes_colunas:
    print("\n➕ Adicionando coluna 'municipio'...")
    cursor.execute("ALTER TABLE clientes ADD COLUMN municipio VARCHAR(100)")
    print("   ✅ Coluna 'municipio' adicionada")
    
    # Cria índice para municipio
    print("\n🔑 Criando índice para 'municipio'...")
    try:
        cursor.execute("CREATE INDEX ix_clientes_municipio ON clientes (municipio)")
        print("   ✅ Índice criado")
    except Exception as e:
        print(f"   ⚠️  Índice já existe ou erro: {e}")
else:
    print("\n✅ Coluna 'municipio' já existe")

conn.commit()

# Verifica estrutura final
cursor.execute("PRAGMA table_info(clientes)")
colunas = cursor.fetchall()
print(f"\n📊 Total de colunas depois: {len(colunas)}")

print("\n🎯 Verificando campos:")
for col in colunas:
    if col[1] in ['logradouro', 'municipio', 'codigo_cliente']:
        print(f"   ✅ {col[1]:<20} {col[2]:<15}")

conn.close()

print("\n" + "="*70)
print("✅ CAMPOS ADICIONADOS COM SUCESSO!")
print("="*70)
