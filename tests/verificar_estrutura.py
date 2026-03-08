import sqlite3

conn = sqlite3.connect('instance/metas.db')
cursor = conn.cursor()

print("="*60)
print("ESTRUTURA DA TABELA CLIENTES")
print("="*60)

cursor.execute('PRAGMA table_info(clientes)')
colunas = cursor.fetchall()

for col in colunas:
    print(f'{col[0]:2d}: {col[1]:25s} {col[2]:10s} {"NOT NULL" if col[3] else "NULL":8s}')

print(f"\nTotal de colunas: {len(colunas)}")

conn.close()
