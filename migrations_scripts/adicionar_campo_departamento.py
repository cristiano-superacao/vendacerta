"""
Script de migração: Adicionar campo departamento na tabela usuarios
Execute: python adicionar_campo_departamento.py
"""

from app import app, db
from models import Usuario
from sqlalchemy import text

def migrar():
    with app.app_context():
        print("🔄 Iniciando migração: adicionar campo departamento...")
        
        try:
            # Verificar se a coluna já existe
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('usuarios')]
            
            if 'departamento' in columns:
                print("ℹ️  Campo 'departamento' já existe na tabela usuarios")
                return
            
            # Adicionar coluna departamento
            with db.engine.connect() as conn:
                # Para SQLite
                if 'sqlite' in str(db.engine.url):
                    conn.execute(text(
                        "ALTER TABLE usuarios ADD COLUMN departamento VARCHAR(50)"
                    ))
                    conn.commit()
                # Para PostgreSQL
                else:
                    conn.execute(text(
                        "ALTER TABLE usuarios ADD COLUMN departamento VARCHAR(50)"
                    ))
                    conn.commit()
            
            print("✅ Campo 'departamento' adicionado com sucesso!")
            print("📊 Tabela usuarios atualizada")
            
        except Exception as e:
            print(f"❌ Erro na migração: {str(e)}")
            raise

if __name__ == '__main__':
    migrar()
