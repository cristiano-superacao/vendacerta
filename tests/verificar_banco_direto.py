"""
Script para verificar a estrutura REAL do banco de dados SQLite
"""
import sqlite3

def verificar_banco():
    print("\n" + "="*70)
    print("🔍 VERIFICAÇÃO DIRETA DO BANCO DE DADOS")
    print("="*70)
    
    conn = sqlite3.connect('instance/vendacerta.db')
    cursor = conn.cursor()
    
    # Verifica se a tabela existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clientes'")
    existe = cursor.fetchone()
    
    if not existe:
        print("\n❌ Tabela 'clientes' NÃO EXISTE!")
        conn.close()
        return
    
    print("\n✅ Tabela 'clientes' encontrada")
    
    # Pega a estrutura da tabela
    cursor.execute("PRAGMA table_info(clientes)")
    colunas = cursor.fetchall()
    
    print(f"\n📊 Total de colunas: {len(colunas)}")
    print("\nEstrutura da tabela:")
    print(f"{'ID':<5} {'Nome':<25} {'Tipo':<15} {'Not Null':<10} {'Default':<15}")
    print("-" * 70)
    
    for coluna in colunas:
        cid, nome, tipo, notnull, dflt_value, pk = coluna
        print(f"{cid:<5} {nome:<25} {tipo:<15} {notnull:<10} {str(dflt_value):<15}")
    
    # Verifica campos específicos
    print("\n🎯 Verificando campos críticos:")
    nomes_colunas = [col[1] for col in colunas]
    
    campos_criticos = ['logradouro', 'municipio', 'codigo_cliente']
    for campo in campos_criticos:
        existe = campo in nomes_colunas
        status = "✅" if existe else "❌"
        print(f"   {status} {campo}: {'EXISTE' if existe else 'NÃO EXISTE'}")
    
    # Lista índices
    print("\n🔑 Índices da tabela:")
    cursor.execute("PRAGMA index_list(clientes)")
    indices = cursor.fetchall()
    if indices:
        for idx in indices:
            print(f"   - {idx[1]} (unique: {idx[2]})")
    else:
        print("   Nenhum índice encontrado")
    
    conn.close()
    
    print("\n" + "="*70)

if __name__ == '__main__':
    verificar_banco()
