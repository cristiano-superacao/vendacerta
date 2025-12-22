import sqlite3
import sys

def adicionar_codigo_cliente():
    """Adiciona coluna codigo_cliente diretamente via SQL"""
    try:
        conn = sqlite3.connect('instance/metas.db')
        cursor = conn.cursor()
        
        print("="*60)
        print("MIGRAÇÃO: Adicionar coluna codigo_cliente")
        print("="*60)
        
        # Verificar se coluna já existe
        cursor.execute('PRAGMA table_info(clientes)')
        colunas = [col[1] for col in cursor.fetchall()]
        
        if 'codigo_cliente' in colunas:
            print("✅ Coluna 'codigo_cliente' já existe!")
        else:
            print("➕ Adicionando coluna 'codigo_cliente'...")
            cursor.execute('ALTER TABLE clientes ADD COLUMN codigo_cliente VARCHAR(9)')
            print("✅ Coluna adicionada!")
            
            print("➕ Criando índice único...")
            cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_codigo_cliente ON clientes(codigo_cliente)')
            print("✅ Índice criado!")
        
        conn.commit()
        
        # Verificar resultado
        cursor.execute('PRAGMA table_info(clientes)')
        colunas_final = cursor.fetchall()
        print(f"\n✅ Total de colunas agora: {len(colunas_final)}")
        
        conn.close()
        print("\n🎉 Migração concluída com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        return False

if __name__ == '__main__':
    sucesso = adicionar_codigo_cliente()
    sys.exit(0 if sucesso else 1)
