"""
Script para adicionar novos campos à tabela de clientes
Executa migração para campos estendidos de importação
"""

from app import app, db
from sqlalchemy import text

def adicionar_campos():
    with app.app_context():
        try:
            print("🔄 Adicionando novos campos à tabela clientes...")
            
            # Campos a adicionar
            campos = [
                ("razao_social", "VARCHAR(200)"),
                ("sigla", "VARCHAR(50)"),
                ("inscricao_estadual", "VARCHAR(20)"),
                ("codigo_bp", "VARCHAR(50)"),
                ("cep", "VARCHAR(10)"),
                ("coordenada_x", "VARCHAR(50)"),
                ("coordenada_y", "VARCHAR(50)"),
                ("telefone2", "VARCHAR(20)"),
                ("celular", "VARCHAR(20)")
            ]
            
            for campo, tipo in campos:
                try:
                    sql = f"ALTER TABLE clientes ADD COLUMN {campo} {tipo}"
                    db.session.execute(text(sql))
                    db.session.commit()
                    print(f"  ✅ Campo '{campo}' adicionado")
                except Exception as e:
                    if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                        print(f"  ℹ️  Campo '{campo}' já existe")
                    else:
                        print(f"  ⚠️  Erro ao adicionar '{campo}': {e}")
                    db.session.rollback()
            
            print("\n✅ Migração concluída com sucesso!")
            print("📊 Novos campos disponíveis:")
            print("   - razao_social (Razão Social)")
            print("   - sigla (Sigla/Apelido)")
            print("   - inscricao_estadual (Inscrição Estadual)")
            print("   - codigo_bp (Código BP/ERP)")
            print("   - cep (CEP)")
            print("   - coordenada_x (Longitude)")
            print("   - coordenada_y (Latitude)")
            print("   - telefone2 (Telefone 2)")
            print("   - celular (Celular)")
            
        except Exception as e:
            print(f"\n❌ Erro na migração: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    adicionar_campos()
