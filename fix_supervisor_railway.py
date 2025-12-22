"""
Script de correção: Adiciona coluna supervisor_id no PostgreSQL do Railway
"""

import os
import sys
from sqlalchemy import create_engine, text

def fix_supervisor_column():
    """Adiciona coluna supervisor_id na tabela usuarios"""
    
    # Pega a URL do banco de dados do ambiente
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print('❌ DATABASE_URL não encontrada')
        print('Configure: export DATABASE_URL="postgresql://..."')
        return False
    
    try:
        print('🔧 Conectando ao banco de dados...')
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Verifica se a coluna existe
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'usuarios' 
                AND column_name = 'supervisor_id'
            """))
            
            if result.fetchone():
                print('✅ Coluna supervisor_id já existe!')
                return True
            
            print('➡️  Adicionando coluna supervisor_id...')
            
            # Adiciona a coluna
            conn.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN supervisor_id INTEGER
            """))
            conn.commit()
            print('✅ Coluna adicionada')
            
            # Adiciona foreign key
            print('➡️  Criando foreign key...')
            conn.execute(text("""
                ALTER TABLE usuarios 
                ADD CONSTRAINT fk_usuarios_supervisor 
                FOREIGN KEY (supervisor_id) 
                REFERENCES usuarios(id)
            """))
            conn.commit()
            print('✅ Foreign key criada')
            
            # Adiciona índice
            print('➡️  Criando índice...')
            conn.execute(text("""
                CREATE INDEX idx_usuario_supervisor 
                ON usuarios(supervisor_id) 
                WHERE supervisor_id IS NOT NULL
            """))
            conn.commit()
            print('✅ Índice criado')
            
            print('\n' + '='*60)
            print('✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!')
            print('='*60)
            return True
            
    except Exception as e:
        print(f'❌ Erro: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print('='*60)
    print('CORREÇÃO: Adicionar supervisor_id no PostgreSQL')
    print('='*60)
    print()
    
    sucesso = fix_supervisor_column()
    sys.exit(0 if sucesso else 1)
