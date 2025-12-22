"""
Migração para adicionar campos de metas avançadas
- Meta de Volume (quantidade de vendas)
- Meta de Valor com Balanceamento (histórico 3-12 meses)
"""

from app import app, db
from models import Meta
from sqlalchemy import inspect, text

def migrar_metas_avancadas():
    """Adiciona novos campos ao modelo Meta"""
    
    with app.app_context():
        inspector = inspect(db.engine)
        colunas_existentes = [col['name'] for col in inspector.get_columns('metas')]
        
        print("=" * 70)
        print("🔄 MIGRAÇÃO: Metas Avançadas")
        print("=" * 70)
        print(f"\n📋 Colunas existentes: {len(colunas_existentes)}")
        
        # Lista de novas colunas a adicionar
        novas_colunas = [
            ('tipo_meta', "VARCHAR(20) DEFAULT 'valor'"),
            ('volume_meta', "INTEGER"),
            ('volume_alcancado', "INTEGER DEFAULT 0"),
            ('periodo_historico', "INTEGER DEFAULT 6"),
            ('data_base_calculo', "DATETIME"),
            ('meta_balanceada', "BOOLEAN DEFAULT 0"),
            ('tendencia_calculada', "FLOAT"),
            ('media_mensal_historico', "FLOAT")
        ]
        
        colunas_adicionadas = 0
        
        for nome_coluna, tipo_coluna in novas_colunas:
            if nome_coluna not in colunas_existentes:
                try:
                    sql = f"ALTER TABLE metas ADD COLUMN {nome_coluna} {tipo_coluna}"
                    db.session.execute(text(sql))
                    db.session.commit()
                    print(f"  ✅ Coluna '{nome_coluna}' adicionada")
                    colunas_adicionadas += 1
                except Exception as e:
                    print(f"  ⚠️  Erro ao adicionar '{nome_coluna}': {e}")
                    db.session.rollback()
            else:
                print(f"  ℹ️  Coluna '{nome_coluna}' já existe")
        
        print("\n" + "=" * 70)
        print(f"✅ Migração concluída!")
        print(f"   Colunas adicionadas: {colunas_adicionadas}")
        print("=" * 70)

if __name__ == '__main__':
    migrar_metas_avancadas()
