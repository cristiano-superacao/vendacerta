"""
Script de Verificação do Banco de Dados
Verifica se a migração de mensagens e permissões foi executada
"""

import os
import sys
from sqlalchemy import inspect, text

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models import Usuario, Mensagem

def verificar_banco():
    """Verifica se as tabelas e colunas necessárias existem"""
    print("🔍 Verificando estrutura do banco de dados...")
    print("=" * 70)

    with app.app_context():
        try:
            inspector = inspect(db.engine)

            # Verificar tabelas existentes
            tabelas_existentes = inspector.get_table_names()
            print(f"\n📊 Total de tabelas encontradas: {len(tabelas_existentes)}")
            print(f"   Tabelas: {', '.join(tabelas_existentes)}")

            # 1. Verificar tabela de mensagens
            print("\n" + "=" * 70)
            print("1️⃣  VERIFICANDO TABELA DE MENSAGENS")
            print("=" * 70)

            if 'mensagens' in tabelas_existentes:
                colunas = [col['name'] for col in inspector.get_columns('mensagens')]
                print("✅ Tabela 'mensagens' existe!")
                print(f"   Colunas ({len(colunas)}): {', '.join(colunas)}")

                # Contar mensagens
                result = db.session.execute(text('SELECT COUNT(*) FROM mensagens'))
                count = result.scalar()
                print(f"   Total de mensagens: {count}")
            else:
                print("❌ Tabela 'mensagens' NÃO EXISTE!")
                print("   ⚠️  É necessário executar: python migration_mensagens_permissoes.py")

            # 2. Verificar colunas de permissões na tabela usuarios
            print("\n" + "=" * 70)
            print("2️⃣  VERIFICANDO PERMISSÕES DOS USUÁRIOS")
            print("=" * 70)

            if 'usuarios' in tabelas_existentes:
                colunas = [col['name'] for col in inspector.get_columns('usuarios')]

                # Lista de colunas de permissões esperadas
                permissoes_esperadas = [
                    'pode_ver_dashboard',
                    'pode_gerenciar_vendedores',
                    'pode_gerenciar_metas',
                    'pode_gerenciar_equipes',
                    'pode_gerenciar_comissoes',
                    'pode_enviar_mensagens',
                    'pode_exportar_dados',
                    'pode_ver_todas_metas',
                    'pode_aprovar_comissoes'
                ]

                permissoes_faltando = []
                permissoes_encontradas = []

                for perm in permissoes_esperadas:
                    if perm in colunas:
                        permissoes_encontradas.append(perm)
                    else:
                        permissoes_faltando.append(perm)

                print(f"✅ Permissões encontradas ({len(permissoes_encontradas)}/9):")
                for perm in permissoes_encontradas:
                    print(f"   ✓ {perm}")

                if permissoes_faltando:
                    print(f"\n❌ Permissões faltando ({len(permissoes_faltando)}/9):")
                    for perm in permissoes_faltando:
                        print(f"   ✗ {perm}")
                    print("   ⚠️  É necessário executar: python migration_mensagens_permissoes.py")
                else:
                    print("\n✅ Todas as permissões estão configuradas!")

                # Contar usuários
                result = db.session.execute(text('SELECT COUNT(*) FROM usuarios'))
                count = result.scalar()
                print(f"\n   Total de usuários: {count}")
            else:
                print("❌ Tabela 'usuarios' NÃO EXISTE!")
                print("   ⚠️  Problema crítico! Verifique a configuração do banco.")

            # 3. Verificar outras tabelas importantes
            print("\n" + "=" * 70)
            print("3️⃣  VERIFICANDO OUTRAS TABELAS")
            print("=" * 70)

            tabelas_importantes = {
                'empresas': 'Sistema multi-tenant',
                'vendedores': 'Vendedores',
                'metas': 'Metas mensais',
                'equipes': 'Equipes de vendedores',
                'faixas_comissao': 'Configuração de comissões'
            }

            for tabela, descricao in tabelas_importantes.items():
                if tabela in tabelas_existentes:
                    result = db.session.execute(text(f'SELECT COUNT(*) FROM {tabela}'))
                    count = result.scalar()
                    print(f"✅ {tabela.ljust(20)} - {descricao.ljust(30)} ({count} registros)")
                else:
                    print(f"❌ {tabela.ljust(20)} - {descricao.ljust(30)} (NÃO EXISTE)")

            # 4. Resumo Final
            print("\n" + "=" * 70)
            print("📋 RESUMO FINAL")
            print("=" * 70)

            tabelas_esperadas = ['empresas', 'usuarios', 'vendedores', 'metas', 
                                'equipes', 'faixas_comissao', 'mensagens', 'configuracoes']
            tabelas_ok = sum(1 for t in tabelas_esperadas if t in tabelas_existentes)

            print(f"\nTabelas: {tabelas_ok}/{len(tabelas_esperadas)} OK")

            if 'mensagens' not in tabelas_existentes or permissoes_faltando:
                print("\n⚠️  AÇÃO NECESSÁRIA:")
                print("   Execute a migração do banco de dados:")
                print("   > python migration_mensagens_permissoes.py")
                return False
            else:
                print("\n✅ BANCO DE DADOS COMPLETO E ATUALIZADO!")
                print("   Todas as tabelas e colunas necessárias estão presentes.")
                return True

        except Exception as e:
            print(f"\n❌ ERRO ao verificar banco de dados:")
            print(f"   {str(e)}")
            print("\n💡 Dicas:")
            print("   1. Verifique se o banco de dados está acessível")
            print("   2. Verifique a variável DATABASE_URL no .env ou Railway")
            print("   3. Execute: flask shell e depois db.create_all()")
            return False

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🔍 VERIFICAÇÃO DO BANCO DE DADOS - SISTEMA SUAMETA")
    print("=" * 70)

    try:
        resultado = verificar_banco()
        print("\n" + "=" * 70)
        if resultado:
            print("✅ Verificação concluída com sucesso!")
            sys.exit(0)
        else:
            print("⚠️  Verificação concluída - ação necessária!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificação cancelada pelo usuário.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {str(e)}")
        sys.exit(1)
