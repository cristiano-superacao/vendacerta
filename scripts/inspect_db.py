
import sys
import os
import sqlite3

# Adicionar diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def inspect_db():
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance', 'vendacerta.db')
    print(f"Inspecionando: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Listar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tabelas:", [t[0] for t in tables])
    
    # Contar clientes
    try:
        cursor.execute("SELECT count(*) FROM clientes")
        count = cursor.fetchone()[0]
        print(f"Total de clientes: {count}")
        
        if count > 0:
            cursor.execute("SELECT id, nome, cidade, empresa_id, codigo_cliente FROM clientes LIMIT 5")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
    except Exception as e:
        print(f"Erro ao ler clientes: {e}")
        
    conn.close()

if __name__ == "__main__":
    inspect_db()
