"""
Script para atualizar a estrutura do banco de dados na nuvem
Conecta no Railway e aplica as migrações necessárias
"""

from flask import Flask
from config import config
from models import db
import os
import sys

def atualizar_banco_dados():
    """Atualiza a estrutura do banco de dados"""

    print("=" * 80)
    print("ATUALIZAÇÃO DO BANCO DE DADOS")
    print("=" * 80)

    # Criar app Flask temporário
    app = Flask(__name__)

    # Carregar configuração
    env = os.environ.get('FLASK_ENV', 'production')
    app.config.from_object(config[env])

    # Verificar se temos DATABASE_URL
    database_url = app.config.get('SQLALCHEMY_DATABASE_URI')

    if not database_url or database_url == 'sqlite:///instance/suameta.db':
        print("\n⚠️  AVISO: Não foi detectada DATABASE_URL de produção!")
        print("Configure a variável de ambiente DATABASE_URL para atualizar o banco na nuvem")
        print("\nExemplo:")
        print('$env:DATABASE_URL="postgresql://usuario:senha@host:porta/database"')
        print('python atualizar_banco.py')
        return False

    print(f"\n✓ Conectando ao banco: {database_url[:30]}...")

    # Inicializar banco
    db.init_app(app)

    with app.app_context():
        try:
            print("\n📋 Verificando estrutura atual...")

            # Importar todos os modelos
            from models import (
                Usuario, Vendedor, Meta, Equipe, 
                Empresa, FaixaComissao
            )

            # Verificar conexão
            db.session.execute(db.text('SELECT 1'))
            print("✓ Conexão estabelecida com sucesso!")

            # Criar todas as tabelas
            print("\n🔨 Atualizando estrutura das tabelas...")
            db.create_all()
            print("✓ Estrutura atualizada com sucesso!")

            # Verificar tabelas existentes
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()

            print(f"\n✓ Tabelas no banco ({len(tables)}):")
            for table in sorted(tables):
                print(f"   - {table}")

            # Verificar se a tabela faixas_comissao existe
            if 'faixas_comissao' in tables:
                print("\n✓ Tabela 'faixas_comissao' existe!")

                # Contar registros
                from models import FaixaComissao
                count = FaixaComissao.query.count()
                print(f"   Registros encontrados: {count}")

                if count == 0:
                    print("\n⚠️  Nenhuma faixa de comissão cadastrada!")
                    print("   Você pode criar faixas pelo painel de administração.")
                else:
                    print("\n✓ Faixas de comissão cadastradas:")
                    faixas = FaixaComissao.query.order_by(FaixaComissao.ordem).all()
                    for faixa in faixas:
                        print(f"   - {faixa.alcance_min}% - {faixa.alcance_max}%: "
                              f"{faixa.taxa_comissao*100}% (cor: {faixa.cor})")
            else:
                print("\n⚠️  Tabela 'faixas_comissao' não encontrada!")
                print("   Recriando tabela...")
                db.create_all()
                print("   ✓ Tabela criada!")

            print("\n" + "=" * 80)
            print("✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 80)

            return True

        except Exception as e:
            print(f"\n❌ ERRO ao atualizar banco:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    sucesso = atualizar_banco_dados()
    sys.exit(0 if sucesso else 1)
