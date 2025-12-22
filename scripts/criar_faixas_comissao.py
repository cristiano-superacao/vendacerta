"""
Script de migração para criar tabela de faixas de comissão
e popular com valores padrão do sistema
"""

import sys
import os

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import FaixaComissao

def criar_faixas_padrao():
    """Cria as 5 faixas de comissão padrão do sistema"""

    print("🔧 Criando tabela de faixas de comissão...")

    # Cria todas as tabelas (incluindo a nova)
    with app.app_context():
        db.create_all()
        print("✅ Tabelas criadas/atualizadas!")

        # Verifica se já existem faixas
        count = FaixaComissao.query.count()
        if count > 0:
            print(f"⚠️  Já existem {count} faixas cadastradas.")
            resposta = input("Deseja sobrescrever? (s/N): ")
            if resposta.lower() != 's':
                print("❌ Operação cancelada.")
                return

            # Remove faixas existentes
            FaixaComissao.query.delete()
            db.session.commit()
            print("🗑️  Faixas antigas removidas.")

        # Faixas padrão do sistema
        faixas_padrao = [
            {
                'ordem': 1,
                'alcance_min': 0,
                'alcance_max': 50,
                'taxa_comissao': 0.01,  # 1%
                'cor': 'danger',
                'descricao': 'Faixa inicial - até 50% da meta'
            },
            {
                'ordem': 2,
                'alcance_min': 51,
                'alcance_max': 75,
                'taxa_comissao': 0.02,  # 2%
                'cor': 'warning',
                'descricao': 'Faixa intermediária - 51% a 75% da meta'
            },
            {
                'ordem': 3,
                'alcance_min': 76,
                'alcance_max': 100,
                'taxa_comissao': 0.03,  # 3%
                'cor': 'info',
                'descricao': 'Faixa de alcance - 76% a 100% da meta'
            },
            {
                'ordem': 4,
                'alcance_min': 101,
                'alcance_max': 125,
                'taxa_comissao': 0.04,  # 4%
                'cor': 'primary',
                'descricao': 'Faixa de superação - 101% a 125% da meta'
            },
            {
                'ordem': 5,
                'alcance_min': 126,
                'alcance_max': 10000,  # Valor alto para representar "acima de"
                'taxa_comissao': 0.05,  # 5%
                'cor': 'success',
                'descricao': 'Faixa de excelência - acima de 125% da meta'
            }
        ]

        print("\n📊 Criando faixas de comissão padrão...\n")

        for faixa_data in faixas_padrao:
            faixa = FaixaComissao(
                empresa_id=None,  # Faixas globais/padrão
                ordem=faixa_data['ordem'],
                alcance_min=faixa_data['alcance_min'],
                alcance_max=faixa_data['alcance_max'],
                taxa_comissao=faixa_data['taxa_comissao'],
                cor=faixa_data['cor'],
                ativa=True
            )

            db.session.add(faixa)

            # Exibe informações
            if faixa_data['alcance_max'] >= 10000:
                range_text = f"Acima de {faixa_data['alcance_min']}%"
            else:
                range_text = f"{faixa_data['alcance_min']}% - {faixa_data['alcance_max']}%"

            print(f"  {faixa_data['ordem']}. {range_text:<20} = {faixa_data['taxa_comissao']*100:.1f}% "
                  f"[{faixa_data['cor'].upper()}]")

        # Salva no banco
        db.session.commit()

        print("\n✅ 5 faixas de comissão criadas com sucesso!")
        print("\n📌 Para editar, acesse: /configuracoes/comissoes")
        print("🔐 Apenas Admin e Super Admin podem editar\n")

if __name__ == '__main__':
    criar_faixas_padrao()
