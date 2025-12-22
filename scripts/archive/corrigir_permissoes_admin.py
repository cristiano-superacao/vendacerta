"""
Script para corrigir permissões de admins no Railway
Execute no Railway: railway run python corrigir_permissoes_admin.py
"""

import os
from sqlalchemy import create_engine, text
from datetime import datetime

# URL do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("⚠️  DATABASE_URL não encontrada!")
    print("💡 Execute localmente com: python corrigir_permissoes_admin.py")
    print("   Ou no Railway: railway run python corrigir_permissoes_admin.py")

    # Tentar usar banco local
    DATABASE_URL = 'sqlite:///instance/suameta.db'
    print(f"\n🔄 Usando banco local: {DATABASE_URL}\n")

# Substituir postgres:// por postgresql://
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

print("=" * 70)
print("🔧 CORREÇÃO DE PERMISSÕES - ADMINISTRADORES")
print("=" * 70)
print(f"\n📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

try:
    # Criar engine
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        # 1. Verificar se colunas de permissão existem
        print("🔍 Verificando estrutura do banco...")

        # Verificar tipo de banco
        is_sqlite = 'sqlite' in DATABASE_URL.lower()

        if is_sqlite:
            # SQLite usa PRAGMA
            result = conn.execute(text("PRAGMA table_info(usuarios)"))
            colunas = [row[1] for row in result.fetchall()]
            colunas_permissao = [c for c in colunas if c.startswith('pode_')]
        else:
            # PostgreSQL usa information_schema
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'usuarios' AND column_name LIKE 'pode_%'
            """))
            colunas_permissao = [row[0] for row in result.fetchall()]

        if not colunas_permissao:
            print("❌ Colunas de permissão não encontradas!")
            print("💡 Execute migration_railway.py primeiro\n")
            exit(1)

        print(f"✅ {len(colunas_permissao)} colunas de permissão encontradas\n")

        # 2. Buscar admins e super_admins
        print("👥 Buscando administradores...")
        result = conn.execute(text("""
            SELECT id, nome, email, cargo, is_super_admin
            FROM usuarios 
            WHERE cargo IN ('admin', 'gerente') OR is_super_admin = TRUE
        """))
        admins = result.fetchall()

        print(f"✅ {len(admins)} administradores encontrados\n")

        if not admins:
            print("⚠️  Nenhum administrador encontrado!")
            print("💡 Verifique os usuários cadastrados no sistema\n")
            exit(0)

        # 3. Atualizar permissões
        print("🔐 Atualizando permissões...")
        for admin in admins:
            admin_id, nome, email, cargo, is_super = admin

            # Atualizar TODAS as permissões para TRUE
            conn.execute(text("""
                UPDATE usuarios 
                SET pode_ver_dashboard = TRUE,
                    pode_gerenciar_vendedores = TRUE,
                    pode_gerenciar_metas = TRUE,
                    pode_gerenciar_equipes = TRUE,
                    pode_gerenciar_comissoes = TRUE,
                    pode_enviar_mensagens = TRUE,
                    pode_exportar_dados = TRUE,
                    pode_ver_todas_metas = TRUE,
                    pode_aprovar_comissoes = TRUE
                WHERE id = :id
            """), {'id': admin_id})

            emoji = "👑" if is_super else "⭐"
            print(f"   {emoji} {nome} ({cargo}) - Permissões atualizadas")

        conn.commit()

        # 4. Verificar resultado
        print("\n📊 Verificando resultado...")
        result = conn.execute(text("""
            SELECT nome, cargo,
                   pode_ver_dashboard,
                   pode_gerenciar_vendedores,
                   pode_gerenciar_metas,
                   pode_enviar_mensagens
            FROM usuarios 
            WHERE cargo IN ('admin', 'gerente') OR is_super_admin = TRUE
        """))

        verificacao = result.fetchall()

        print("\n✅ Permissões atualizadas:")
        for row in verificacao:
            nome, cargo, dash, vend, metas, msg = row
            status = "✅" if all([dash, vend, metas, msg]) else "❌"
            print(f"   {status} {nome} ({cargo})")

        print("\n" + "=" * 70)
        print("✅ CORREÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        print("\n💡 Todos os administradores agora têm permissões completas")
        print("🚀 Faça login novamente para aplicar as mudanças\n")

except Exception as e:
    print(f"\n❌ ERRO na correção:")
    print(f"   {str(e)}\n")

    import traceback
    print("📋 Detalhes do erro:")
    print(traceback.format_exc())
    exit(1)
