"""
Migração completa e unificada - Adiciona todos os campos necessários
"""
import sqlite3
import sys
import os

def migrar_completo():
    """Adiciona todas as colunas necessárias de uma vez"""
    
    db_path = 'instance/metas.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("="*70)
        print("🔄 MIGRAÇÃO COMPLETA - Adicionar campos faltantes")
        print("="*70)
        
        # Verificar colunas existentes
        cursor.execute('PRAGMA table_info(clientes)')
        colunas_existentes = {col[1] for col in cursor.fetchall()}
        print(f"\n📊 Colunas existentes: {len(colunas_existentes)}")
        
        campos_adicionar = []
        
        # Definir todos os campos que precisam existir
        campos_necessarios = {
            'logradouro': 'VARCHAR(255)',
            'municipio': 'VARCHAR(100)',
            'codigo_cliente': 'VARCHAR(9)'
        }
        
        # Verificar quais campos faltam
        for campo, tipo in campos_necessarios.items():
            if campo not in colunas_existentes:
                campos_adicionar.append((campo, tipo))
        
        if not campos_adicionar:
            print("\n✅ Todos os campos já existem!")
        else:
            print(f"\n➕ Adicionando {len(campos_adicionar)} campo(s)...")
            
            for campo, tipo in campos_adicionar:
                print(f"   - {campo} ({tipo})")
                cursor.execute(f'ALTER TABLE clientes ADD COLUMN {campo} {tipo}')
            
            print("\n✅ Colunas adicionadas com sucesso!")
        
        # Criar índices
        print("\n📑 Criando índices...")
        
        # Índice para municipio
        try:
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_clientes_municipio ON clientes(municipio)')
            print("   ✅ Índice idx_clientes_municipio criado")
        except:
            print("   ℹ️  Índice idx_clientes_municipio já existe")
        
        # Índice único para codigo_cliente
        try:
            cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_codigo_cliente ON clientes(codigo_cliente)')
            print("   ✅ Índice idx_codigo_cliente criado")
        except:
            print("   ℹ️  Índice idx_codigo_cliente já existe")
        
        conn.commit()
        
        # Verificar estrutura final
        cursor.execute('PRAGMA table_info(clientes)')
        colunas_final = cursor.fetchall()
        
        print("\n" + "="*70)
        print("📊 ESTRUTURA FINAL")
        print("="*70)
        print(f"Total de colunas: {len(colunas_final)}")
        
        # Mostrar apenas os campos novos/importantes
        campos_importantes = ['logradouro', 'municipio', 'codigo_cliente', 'cidade', 'bairro']
        print("\nCampos de endereço:")
        for col in colunas_final:
            if col[1] in campos_importantes:
                print(f"   {col[1]:20s} {col[2]}")
        
        conn.close()
        
        print("\n🎉 Migração concluída com sucesso!")
        print("\n⚠️  PRÓXIMOS PASSOS:")
        print("   1. Reinicie o servidor Flask (CTRL+C + python app.py)")
        print("   2. Teste o cadastro de clientes")
        print("   3. Teste a importação")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    sucesso = migrar_completo()
    sys.exit(0 if sucesso else 1)
