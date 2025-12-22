"""
Migração automática para adicionar/atualizar tabela de faixas de comissão
Pode ser executado localmente ou no Railway
"""

from flask import Flask
from config import config
from models import db, FaixaComissao
import os
import sys

def executar_migracao():
    """Executa a migração das faixas de comissão"""

    print("=" * 80)
    print("MIGRAÇÃO: FAIXAS DE COMISSÃO")
    print("=" * 80)

    # Criar app Flask temporário
    app = Flask(__name__)

    # Carregar configuração (produção se DATABASE_URL estiver definida)
    env = os.environ.get('FLASK_ENV', 'production' if os.environ.get('DATABASE_URL') else 'development')
    app.config.from_object(config[env])

    database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
    print(f"\n📊 Ambiente: {env}")
    print(f"🔗 Banco: {database_url[:50]}...")

    # Inicializar banco
    db.init_app(app)

    with app.app_context():
        try:
            # Verificar conexão
            print("\n🔌 Testando conexão...")
            db.session.execute(db.text('SELECT 1'))
            print("✓ Conexão estabelecida!")

            # Criar tabela se não existir
            print("\n🔨 Criando/atualizando tabela faixas_comissao...")
            db.create_all()
            print("✓ Tabela criada/atualizada!")

            # Verificar se já existem faixas globais
            faixas_existentes = FaixaComissao.query.filter(
                FaixaComissao.empresa_id.is_(None)
            ).count()

            print(f"\n📋 Faixas globais existentes: {faixas_existentes}")

            if faixas_existentes == 0:
                print("\n➕ Criando faixas padrão...")

                faixas_padrao = [
                    {
                        'alcance_min': 0,
                        'alcance_max': 50,
                        'taxa_comissao': 0.01,  # 1%
                        'cor': 'danger',
                        'ordem': 0
                    },
                    {
                        'alcance_min': 51,
                        'alcance_max': 75,
                        'taxa_comissao': 0.015,  # 1.5%
                        'cor': 'warning',
                        'ordem': 1
                    },
                    {
                        'alcance_min': 76,
                        'alcance_max': 99,
                        'taxa_comissao': 0.02,  # 2%
                        'cor': 'info',
                        'ordem': 2
                    },
                    {
                        'alcance_min': 100,
                        'alcance_max': 10000,
                        'taxa_comissao': 0.025,  # 2.5%
                        'cor': 'success',
                        'ordem': 3
                    }
                ]

                for faixa_data in faixas_padrao:
                    faixa = FaixaComissao(
                        empresa_id=None,  # Global
                        **faixa_data
                    )
                    db.session.add(faixa)
                    print(f"   ✓ Criada: {faixa_data['alcance_min']}%-{faixa_data['alcance_max']}% = "
                          f"{faixa_data['taxa_comissao']*100}% (cor: {faixa_data['cor']})")

                db.session.commit()
                print("\n✅ Faixas padrão criadas com sucesso!")
            else:
                print("\n✓ Faixas globais já existem, nenhuma ação necessária.")

            # Listar todas as faixas
            print("\n📊 FAIXAS CADASTRADAS:")
            print("-" * 80)

            todas_faixas = FaixaComissao.query.order_by(
                FaixaComissao.empresa_id.is_(None).desc(),
                FaixaComissao.ordem
            ).all()

            if todas_faixas:
                for faixa in todas_faixas:
                    escopo = "Global" if faixa.empresa_id is None else f"Empresa #{faixa.empresa_id}"
                    status = "✓ Ativa" if faixa.ativa else "✗ Inativa"
                    print(f"  [{escopo:15}] {faixa.alcance_min:5.1f}% - {faixa.alcance_max:7.1f}% = "
                          f"{faixa.taxa_comissao*100:5.2f}% | Cor: {faixa.cor:10} | Ordem: {faixa.ordem} | {status}")
            else:
                print("  Nenhuma faixa cadastrada.")

            print("\n" + "=" * 80)
            print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 80)

            return True

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERRO na migração:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    sucesso = executar_migracao()
    sys.exit(0 if sucesso else 1)
