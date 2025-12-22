"""
Script de Migração do Banco de Dados
=====================================

Este script adiciona os novos campos necessários para o sistema multi-tenant:
- bloqueado e motivo_bloqueio na tabela usuarios
- empresa_id nas tabelas vendedores e equipes

Execute com: python migration_multi_tenant.py
"""

import os
import sys
from config import db, app
from models import Usuario, Vendedor, Equipe, Empresa

def verificar_coluna_existe(tabela, coluna):
    """Verifica se uma coluna já existe em uma tabela"""
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    colunas = [c['name'] for c in inspector.get_columns(tabela)]
    return coluna in colunas

def adicionar_coluna_bloqueado():
    """Adiciona colunas bloqueado e motivo_bloqueio na tabela usuarios"""
    print("🔧 Verificando tabela 'usuarios'...")

    if not verificar_coluna_existe('usuarios', 'bloqueado'):
        print("  ➕ Adicionando coluna 'bloqueado'...")
        db.engine.execute("""
            ALTER TABLE usuarios 
            ADD COLUMN bloqueado BOOLEAN DEFAULT FALSE
        """)
        print("  ✅ Coluna 'bloqueado' adicionada")
    else:
        print("  ✓ Coluna 'bloqueado' já existe")

    if not verificar_coluna_existe('usuarios', 'motivo_bloqueio'):
        print("  ➕ Adicionando coluna 'motivo_bloqueio'...")
        db.engine.execute("""
            ALTER TABLE usuarios 
            ADD COLUMN motivo_bloqueio TEXT
        """)
        print("  ✅ Coluna 'motivo_bloqueio' adicionada")
    else:
        print("  ✓ Coluna 'motivo_bloqueio' já existe")

def adicionar_empresa_id_vendedores():
    """Adiciona coluna empresa_id na tabela vendedores"""
    print("\n🔧 Verificando tabela 'vendedores'...")

    if not verificar_coluna_existe('vendedores', 'empresa_id'):
        print("  ➕ Adicionando coluna 'empresa_id'...")
        db.engine.execute("""
            ALTER TABLE vendedores 
            ADD COLUMN empresa_id INTEGER REFERENCES empresas(id)
        """)
        print("  ✅ Coluna 'empresa_id' adicionada")

        # Atualizar vendedores existentes com empresa_id da primeira empresa
        print("  🔄 Atualizando vendedores existentes...")
        primeira_empresa = Empresa.query.first()
        if primeira_empresa:
            db.engine.execute(f"""
                UPDATE vendedores 
                SET empresa_id = {primeira_empresa.id}
                WHERE empresa_id IS NULL
            """)
            print(f"  ✅ Vendedores atualizados com empresa: {primeira_empresa.nome}")
        else:
            print("  ⚠️  Nenhuma empresa encontrada. Crie uma empresa antes de prosseguir.")
    else:
        print("  ✓ Coluna 'empresa_id' já existe")

def adicionar_empresa_id_equipes():
    """Adiciona coluna empresa_id na tabela equipes"""
    print("\n🔧 Verificando tabela 'equipes'...")

    if not verificar_coluna_existe('equipes', 'empresa_id'):
        print("  ➕ Adicionando coluna 'empresa_id'...")
        db.engine.execute("""
            ALTER TABLE equipes 
            ADD COLUMN empresa_id INTEGER REFERENCES empresas(id)
        """)
        print("  ✅ Coluna 'empresa_id' adicionada")

        # Atualizar equipes existentes com empresa_id da primeira empresa
        print("  🔄 Atualizando equipes existentes...")
        primeira_empresa = Empresa.query.first()
        if primeira_empresa:
            db.engine.execute(f"""
                UPDATE equipes 
                SET empresa_id = {primeira_empresa.id}
                WHERE empresa_id IS NULL
            """)
            print(f"  ✅ Equipes atualizadas com empresa: {primeira_empresa.nome}")
        else:
            print("  ⚠️  Nenhuma empresa encontrada. Crie uma empresa antes de prosseguir.")
    else:
        print("  ✓ Coluna 'empresa_id' já existe")

def verificar_super_admin():
    """Verifica se existe pelo menos um super admin"""
    print("\n🔧 Verificando super administrador...")

    super_admin = Usuario.query.filter_by(is_super_admin=True).first()

    if not super_admin:
        print("  ⚠️  Nenhum super administrador encontrado!")
        print("  ℹ️  Você pode criar um super admin via console Python:")
        print("     from models import Usuario")
        print("     from config import db")
        print("     admin = Usuario.query.filter_by(email='seu@email.com').first()")
        print("     admin.is_super_admin = True")
        print("     db.session.commit()")
    else:
        print(f"  ✅ Super admin encontrado: {super_admin.nome} ({super_admin.email})")

def main():
    """Executa todas as migrações"""
    print("=" * 70)
    print("🚀 INICIANDO MIGRAÇÃO MULTI-TENANT")
    print("=" * 70)

    with app.app_context():
        try:
            # Executar migrações
            adicionar_coluna_bloqueado()
            adicionar_empresa_id_vendedores()
            adicionar_empresa_id_equipes()
            verificar_super_admin()

            print("\n" + "=" * 70)
            print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 70)
            print("\n📋 Próximos passos:")
            print("  1. Certifique-se de ter um super admin configurado")
            print("  2. Faça login como super admin")
            print("  3. Acesse 'Super Admin > Empresas' para gerenciar empresas")
            print("  4. Acesse 'Super Admin > Usuários' para gerenciar usuários")
            print("  5. Configure os cargos e empresas dos usuários existentes")
            print()

        except Exception as e:
            print("\n" + "=" * 70)
            print("❌ ERRO NA MIGRAÇÃO!")
            print("=" * 70)
            print(f"Erro: {str(e)}")
            print("\nDica: Verifique se o banco de dados está acessível")
            sys.exit(1)

if __name__ == '__main__':
    main()
