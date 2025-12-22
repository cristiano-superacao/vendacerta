#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Migração: FaixaComissao → FaixaComissaoVendedor e FaixaComissaoSupervisor

Este script migra os dados existentes da tabela FaixaComissao (modelo antigo)
para as novas tabelas separadas FaixaComissaoVendedor e FaixaComissaoSupervisor.

Uso:
    python scripts/migrar_faixas_comissao_separadas.py
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, FaixaComissao, FaixaComissaoVendedor, FaixaComissaoSupervisor

def migrar_faixas():
    """
    Migra as faixas de comissão antigas para os novos modelos separados
    """
    with app.app_context():
        print("=" * 70)
        print("MIGRAÇÃO DE FAIXAS DE COMISSÃO")
        print("=" * 70)
        print()

        try:
            # Cria as novas tabelas se não existirem
            db.create_all()
            print("✓ Tabelas criadas/verificadas")

            # Busca todas as faixas antigas
            faixas_antigas = FaixaComissao.query.all()

            if not faixas_antigas:
                print("\n⚠ Nenhuma faixa antiga encontrada para migrar")
                print("As tabelas novas estão prontas para uso!")
                return

            print(f"\n📦 Encontradas {len(faixas_antigas)} faixas para migrar")
            print()

            migradas_vendedor = 0
            migradas_supervisor = 0

            for faixa_antiga in faixas_antigas:
                print(f"Migrando: {faixa_antiga.alcance_min}%-{faixa_antiga.alcance_max}% = {faixa_antiga.taxa_comissao*100}%")

                # Verifica se já existe faixa vendedor com mesmos parâmetros
                faixa_vendedor_existente = FaixaComissaoVendedor.query.filter_by(
                    empresa_id=faixa_antiga.empresa_id,
                    ordem=faixa_antiga.ordem,
                    alcance_min=faixa_antiga.alcance_min,
                    alcance_max=faixa_antiga.alcance_max
                ).first()

                if not faixa_vendedor_existente:
                    # Cria faixa para vendedor
                    faixa_vendedor = FaixaComissaoVendedor(
                        empresa_id=faixa_antiga.empresa_id,
                        alcance_min=faixa_antiga.alcance_min,
                        alcance_max=faixa_antiga.alcance_max,
                        taxa_comissao=faixa_antiga.taxa_comissao,
                        cor=faixa_antiga.cor,
                        ordem=faixa_antiga.ordem,
                        ativa=faixa_antiga.ativa
                    )
                    db.session.add(faixa_vendedor)
                    migradas_vendedor += 1
                    print("  ✓ Criada faixa para VENDEDOR")
                else:
                    print("  ○ Faixa VENDEDOR já existe")

                # Verifica se já existe faixa supervisor com mesmos parâmetros
                faixa_supervisor_existente = FaixaComissaoSupervisor.query.filter_by(
                    empresa_id=faixa_antiga.empresa_id,
                    ordem=faixa_antiga.ordem,
                    alcance_min=faixa_antiga.alcance_min,
                    alcance_max=faixa_antiga.alcance_max
                ).first()

                if not faixa_supervisor_existente:
                    # Cria faixa para supervisor
                    faixa_supervisor = FaixaComissaoSupervisor(
                        empresa_id=faixa_antiga.empresa_id,
                        alcance_min=faixa_antiga.alcance_min,
                        alcance_max=faixa_antiga.alcance_max,
                        taxa_comissao=faixa_antiga.taxa_comissao,
                        cor=faixa_antiga.cor,
                        ordem=faixa_antiga.ordem,
                        ativa=faixa_antiga.ativa
                    )
                    db.session.add(faixa_supervisor)
                    migradas_supervisor += 1
                    print("  ✓ Criada faixa para SUPERVISOR")
                else:
                    print("  ○ Faixa SUPERVISOR já existe")

                print()

            # Commit das alterações
            db.session.commit()

            print("=" * 70)
            print("MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 70)
            print(f"\n📊 Resumo:")
            print(f"  • Faixas antigas encontradas: {len(faixas_antigas)}")
            print(f"  • Faixas VENDEDOR criadas: {migradas_vendedor}")
            print(f"  • Faixas SUPERVISOR criadas: {migradas_supervisor}")
            print()

            # Pergunta se deve manter ou remover faixas antigas
            print("⚠ IMPORTANTE:")
            print("As faixas antigas ainda estão no banco de dados.")
            print("Você pode:")
            print("  1. Mantê-las como backup (recomendado)")
            print("  2. Removê-las manualmente depois de testar")
            print()
            print("Para remover manualmente, use SQL:")
            print("  DELETE FROM faixas_comissao;")
            print()

        except Exception as e:
            db.session.rollback()
            print("\n❌ ERRO durante a migração!")
            print(f"Detalhes: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

        return True

def verificar_migracao():
    """
    Verifica o status da migração
    """
    with app.app_context():
        print("\n" + "=" * 70)
        print("VERIFICAÇÃO DA MIGRAÇÃO")
        print("=" * 70)

        faixas_antigas = FaixaComissao.query.count()
        faixas_vendedor = FaixaComissaoVendedor.query.count()
        faixas_supervisor = FaixaComissaoSupervisor.query.count()

        print(f"\n📊 Status das Tabelas:")
        print(f"  • FaixaComissao (antiga): {faixas_antigas} registros")
        print(f"  • FaixaComissaoVendedor: {faixas_vendedor} registros")
        print(f"  • FaixaComissaoSupervisor: {faixas_supervisor} registros")
        print()

        if faixas_vendedor > 0 or faixas_supervisor > 0:
            print("✓ Migração realizada com sucesso!")
            print()

            # Mostra algumas faixas de exemplo
            print("Exemplo de faixas migradas:")
            print("\n[VENDEDORES]")
            for faixa in FaixaComissaoVendedor.query.limit(3).all():
                print(f"  • {faixa.alcance_min}%-{faixa.alcance_max}% = {faixa.taxa_comissao*100}% ({faixa.cor})")

            print("\n[SUPERVISORES]")
            for faixa in FaixaComissaoSupervisor.query.limit(3).all():
                print(f"  • {faixa.alcance_min}%-{faixa.alcance_max}% = {faixa.taxa_comissao*100}% ({faixa.cor})")
        else:
            print("⚠ Nenhuma faixa migrada ainda")

        print()

if __name__ == '__main__':
    print("\n🚀 Iniciando migração de faixas de comissão...\n")

    # Executa migração
    sucesso = migrar_faixas()

    # Verifica resultado
    if sucesso is not False:
        verificar_migracao()

    print("\n" + "=" * 70)
    print("Script finalizado!")
    print("=" * 70 + "\n")
