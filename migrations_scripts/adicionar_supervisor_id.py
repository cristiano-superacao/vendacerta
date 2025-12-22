"""
Migration: Adicionar campo supervisor_id na tabela usuarios
Data: 19/12/2025
Autor: Sistema

Objetivo:
- Adicionar campo supervisor_id para completar hierarquia Vendedor/Técnico → Supervisor → Gerente → Admin
- Permitir que vendedores e técnicos sejam vinculados diretamente a um supervisor
"""

import sqlite3
import os

def adicionar_supervisor_id():
    """Adiciona campo supervisor_id na tabela usuarios"""
    
    # Caminho do banco de dados
    db_path = os.path.join('instance', 'vendacerta.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado em: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Iniciando migração: adicionar supervisor_id")
        
        # Verificar se a coluna já existe
        cursor.execute("PRAGMA table_info(usuarios)")
        colunas = [col[1] for col in cursor.fetchall()]
        
        if 'supervisor_id' in colunas:
            print("✅ Campo supervisor_id já existe!")
            return True
        
        # Adicionar coluna supervisor_id
        cursor.execute("""
            ALTER TABLE usuarios 
            ADD COLUMN supervisor_id INTEGER
        """)
        
        print("✅ Campo supervisor_id adicionado com sucesso!")
        
        # Criar índice para melhorar performance
        try:
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_usuario_supervisor 
                ON usuarios(supervisor_id, ativo)
            """)
            print("✅ Índice idx_usuario_supervisor criado!")
        except Exception as e:
            print(f"⚠️  Índice já existe: {e}")
        
        conn.commit()
        print("\n" + "="*70)
        print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*70)
        print("\n📋 Próximos passos:")
        print("   1. Vincular vendedores aos supervisores apropriados")
        print("   2. Vincular técnicos aos supervisores de manutenção")
        print("   3. Atualizar interfaces para exibir hierarquia completa")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao adicionar supervisor_id: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("="*70)
    print("MIGRAÇÃO: Adicionar supervisor_id")
    print("="*70)
    print()
    
    sucesso = adicionar_supervisor_id()
    
    if sucesso:
        print("\n✅ Migração executada com sucesso!")
    else:
        print("\n❌ Migração falhou!")
