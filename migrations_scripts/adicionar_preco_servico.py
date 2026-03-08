"""
Script para adicionar o campo preco_servico na tabela produtos
"""
from app import app, db
from models import Produto
from sqlalchemy import text

def adicionar_campo_preco_servico():
    """Adiciona o campo preco_servico na tabela produtos"""
    with app.app_context():
        try:
            # Verifica se a coluna já existe
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('produtos')]
            
            if 'preco_servico' in columns:
                print('✅ Campo preco_servico já existe!')
                return
            
            # Adiciona a coluna preco_servico
            with db.engine.connect() as conn:
                conn.execute(text("""
                    ALTER TABLE produtos 
                    ADD COLUMN preco_servico FLOAT DEFAULT 0
                """))
                conn.commit()
            
            print('✅ Campo preco_servico adicionado com sucesso!')
            print('📊 Todos os produtos foram inicializados com preco_servico = 0')
            
            # Exibe estatísticas
            total_produtos = Produto.query.count()
            print(f'\n📈 Total de produtos no banco: {total_produtos}')
            
        except Exception as e:
            print(f'❌ Erro ao adicionar campo: {str(e)}')
            db.session.rollback()

if __name__ == '__main__':
    print('🔧 Adicionando campo preco_servico na tabela produtos...\n')
    adicionar_campo_preco_servico()
    print('\n✅ Migração concluída!')
