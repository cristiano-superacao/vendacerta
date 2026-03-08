"""
Script para adicionar campos logradouro e municipio à tabela clientes
"""
import sqlite3
import os
import sys

def migrar_campos_endereco():
    """Adiciona campos logradouro e municipio se não existirem"""
    db_path = os.path.join('instance', 'metas.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Verificando estrutura da tabela clientes...")
        
        # Verificar colunas existentes
        cursor.execute("PRAGMA table_info(clientes)")
        colunas_existentes = {col[1] for col in cursor.fetchall()}
        print(f"✅ Colunas existentes: {len(colunas_existentes)}")
        
        campos_adicionados = []
        
        # Adicionar logradouro se não existir
        if 'logradouro' not in colunas_existentes:
            print("➕ Adicionando coluna 'logradouro'...")
            cursor.execute("ALTER TABLE clientes ADD COLUMN logradouro VARCHAR(255)")
            campos_adicionados.append('logradouro')
            print("   ✅ Coluna 'logradouro' adicionada")
        else:
            print("   ℹ️  Coluna 'logradouro' já existe")
        
        # Adicionar municipio se não existir
        if 'municipio' not in colunas_existentes:
            print("➕ Adicionando coluna 'municipio'...")
            cursor.execute("ALTER TABLE clientes ADD COLUMN municipio VARCHAR(100)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_clientes_municipio ON clientes(municipio)")
            campos_adicionados.append('municipio')
            print("   ✅ Coluna 'municipio' adicionada com índice")
        else:
            print("   ℹ️  Coluna 'municipio' já existe")
        
        # Copiar dados de cidade para municipio se municipio estiver vazio
        if 'municipio' in campos_adicionados and 'cidade' in colunas_existentes:
            print("\n📋 Copiando dados de 'cidade' para 'municipio'...")
            cursor.execute("UPDATE clientes SET municipio = cidade WHERE municipio IS NULL AND cidade IS NOT NULL")
            rows_updated = cursor.rowcount
            print(f"   ✅ {rows_updated} registros atualizados")
        
        conn.commit()
        
        # Estatísticas finais
        print("\n" + "="*60)
        print("📊 ESTATÍSTICAS DA MIGRAÇÃO")
        print("="*60)
        
        cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = cursor.fetchone()[0]
        print(f"Total de clientes: {total_clientes}")
        
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE logradouro IS NOT NULL")
        com_logradouro = cursor.fetchone()[0]
        print(f"Com logradouro: {com_logradouro}")
        
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE municipio IS NOT NULL")
        com_municipio = cursor.fetchone()[0]
        print(f"Com município: {com_municipio}")
        
        if campos_adicionados:
            print(f"\n✅ Campos adicionados: {', '.join(campos_adicionados)}")
        else:
            print("\nℹ️  Nenhum campo novo foi adicionado (já existem)")
        
        print("\n✅ Migração concluída com sucesso!")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Erro durante a migração: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("="*60)
    print("MIGRAÇÃO: Adicionar campos logradouro e municipio")
    print("="*60)
    print()
    
    sucesso = migrar_campos_endereco()
    
    if sucesso:
        print("\n🎉 Migração executada com sucesso!")
        print("\n⚠️  PRÓXIMOS PASSOS:")
        print("   1. Verifique se o servidor está funcionando")
        print("   2. Teste o cadastro de novos clientes")
        print("   3. Teste a edição de clientes existentes")
        print("   4. Verifique a importação de planilhas")
    else:
        print("\n❌ Migração falhou!")
        sys.exit(1)
