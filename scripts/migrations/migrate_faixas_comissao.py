#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migração para criar tabela FaixaComissao no Railway
Executar: python migrate_faixas_comissao.py
"""

import os
import sys
from pathlib import Path

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*70)
    print(f"🚀 {title}")
    print("="*70 + "\n")

def get_database_url():
    """Obtém DATABASE_URL"""
    database_url = os.environ.get('DATABASE_URL')

    if not database_url and Path('.railway_db_url.txt').exists():
        with open('.railway_db_url.txt', 'r') as f:
            database_url = f.read().strip()

    if not database_url:
        print("❌ DATABASE_URL não encontrada!")
        print("\n📝 Configure a DATABASE_URL:")
        print("   1. Defina a variável de ambiente DATABASE_URL")
        print("   2. Ou crie o arquivo .railway_db_url.txt com a URL")
        sys.exit(1)

    # Corrige postgres:// para postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    return database_url

def migrar_faixas_comissao():
    """Cria tabela FaixaComissao e popula dados iniciais"""

    print_header("MIGRAÇÃO: Tabela FaixaComissao")

    database_url = get_database_url()
    print(f"📍 Banco de dados: {database_url[:50]}...")

    # Configura app Flask
    from app import app, db
    from models import FaixaComissao

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    with app.app_context():
        try:
            print("\n🔧 Criando tabela faixa_comissao...")

            # Cria apenas a tabela FaixaComissao
            from sqlalchemy import inspect, text

            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()

            if 'faixa_comissao' in existing_tables:
                print("⚠️  Tabela 'faixa_comissao' já existe!")

                # Verifica se há dados
                count = db.session.execute(text('SELECT COUNT(*) FROM faixa_comissao')).scalar()
                print(f"📊 Registros existentes: {count}")

                if count > 0:
                    print("\n✅ Tabela já está populada. Nada a fazer.")
                    return
            else:
                # Cria a tabela
                db.create_all()
                print("✅ Tabela 'faixa_comissao' criada!")

            # Popula com dados padrão
            print("\n📊 Criando faixas de comissão padrão...")

            faixas_padrao = [
                {
                    'ordem': 1,
                    'alcance_min': 0.0,
                    'alcance_max': 50.0,
                    'taxa_comissao': 0.01,  # 1%
                    'cor': 'danger',
                    'ativa': True
                },
                {
                    'ordem': 2,
                    'alcance_min': 51.0,
                    'alcance_max': 75.0,
                    'taxa_comissao': 0.02,  # 2%
                    'cor': 'warning',
                    'ativa': True
                },
                {
                    'ordem': 3,
                    'alcance_min': 76.0,
                    'alcance_max': 100.0,
                    'taxa_comissao': 0.03,  # 3%
                    'cor': 'info',
                    'ativa': True
                },
                {
                    'ordem': 4,
                    'alcance_min': 101.0,
                    'alcance_max': 125.0,
                    'taxa_comissao': 0.04,  # 4%
                    'cor': 'primary',
                    'ativa': True
                },
                {
                    'ordem': 5,
                    'alcance_min': 125.1,
                    'alcance_max': 10000.0,
                    'taxa_comissao': 0.05,  # 5%
                    'cor': 'success',
                    'ativa': True
                }
            ]

            for dados in faixas_padrao:
                faixa = FaixaComissao(
                    empresa_id=None,  # Globais
                    **dados
                )
                db.session.add(faixa)
                print(f"   ✅ {dados['alcance_min']}% - {dados['alcance_max']}% = {dados['taxa_comissao']*100}%")

            db.session.commit()

            print(f"\n✅ {len(faixas_padrao)} faixas de comissão criadas com sucesso!")
            print("\n📋 Faixas configuradas:")
            print("   1. 0% - 50%    = 1%  (🔴 Vermelho)")
            print("   2. 51% - 75%   = 2%  (🟡 Amarelo)")
            print("   3. 76% - 100%  = 3%  (🔵 Azul)")
            print("   4. 101% - 125% = 4%  (🔷 Azul Escuro)")
            print("   5. > 125%      = 5%  (🟢 Verde)")
            print("\n🎉 Migração concluída com sucesso!")

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erro na migração: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    migrar_faixas_comissao()
