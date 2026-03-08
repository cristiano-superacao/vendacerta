#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Consolidado de Migração do Banco de Dados
Suporta ambientes local (SQLite) e produção (PostgreSQL/Railway)
"""

import os
import sys
import subprocess
from pathlib import Path

# Instalar dependências se necessário
try:
    import psycopg2
except ImportError:
    print("📦 Instalando psycopg2-binary...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'], 
                   capture_output=True)
    try:
        import psycopg2
    except ImportError:
        print("⚠️  psycopg2 será necessário apenas para PostgreSQL")

from werkzeug.security import generate_password_hash

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*70)
    print(f"🚀 {title}")
    print("="*70 + "\n")

def get_database_url():
    """Obtém DATABASE_URL de várias fontes"""
    # 1. Variável de ambiente
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        print("✅ DATABASE_URL encontrada nas variáveis de ambiente")
        return database_url

    # 2. Arquivo salvo
    if Path('.railway_db_url.txt').exists():
        with open('.railway_db_url.txt', 'r') as f:
            saved_url = f.read().strip()
            if saved_url.startswith(('postgresql://', 'postgres://')):
                print("✅ DATABASE_URL carregada do arquivo .railway_db_url.txt")
                return saved_url

    # 3. Construir de variáveis individuais (Railway)
    pg_vars = {
        'PGHOST': os.environ.get('PGHOST'),
        'PGPORT': os.environ.get('PGPORT'),
        'PGUSER': os.environ.get('PGUSER'),
        'PGPASSWORD': os.environ.get('PGPASSWORD'),
        'PGDATABASE': os.environ.get('PGDATABASE')
    }

    if all(pg_vars.values()):
        database_url = f"postgresql://{pg_vars['PGUSER']}:{pg_vars['PGPASSWORD']}@{pg_vars['PGHOST']}:{pg_vars['PGPORT']}/{pg_vars['PGDATABASE']}"
        print("✅ DATABASE_URL construída das variáveis PGHOST/PGPORT/etc")
        return database_url

    return None

def migrate_local():
    """Migração para banco SQLite local"""
    print_header("MIGRAÇÃO LOCAL (SQLite)")

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    # Criar app Flask temporária
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    # Importar modelos
    from models import Usuario, Empresa, Vendedor, Meta, Equipe

    with app.app_context():
        print("📊 Criando/atualizando tabelas...")
        db.create_all()
        print("✅ Tabelas criadas com sucesso!\n")

        # Criar empresa padrão se não existir
        empresa = Empresa.query.first()
        if not empresa:
            print("🏢 Criando empresa padrão...")
            empresa = Empresa(
                nome='Empresa Padrão',
                cnpj='00000000000000',
                email='contato@empresapadrao.com',
                telefone='(71) 99999-9999',
                endereco='Salvador, BA',
                cidade='Salvador',
                estado='BA',
                plano='premium',
                max_usuarios=100,
                max_vendedores=500,
                ativo=True,
                bloqueado=False
            )
            db.session.add(empresa)
            db.session.commit()
            print(f"✅ Empresa criada: {empresa.nome} (ID: {empresa.id})\n")

        # Criar super admin se não existir
        super_admin = Usuario.query.filter_by(email='superadmin@suameta.com').first()
        if not super_admin:
            print("👑 Criando Super Administrador...")
            super_admin = Usuario(
                nome='Super Admin',
                email='superadmin@suameta.com',
                cargo='admin',
                is_super_admin=True,
                empresa_id=None,
                ativo=True
            )
            super_admin.set_senha('18042016')
            db.session.add(super_admin)
            db.session.commit()
            print("✅ Super Admin criado!")
            print("   📧 Email: superadmin@suameta.com")
            print("   🔑 Senha: 18042016\n")

        # Criar admin da empresa se não existir
        admin = Usuario.query.filter_by(email='admin@suameta.com').first()
        if not admin:
            print("🔑 Criando Administrador da Empresa...")
            admin = Usuario(
                nome='Administrador',
                email='admin@suameta.com',
                cargo='admin',
                is_super_admin=False,
                empresa_id=empresa.id,
                ativo=True
            )
            admin.set_senha('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin criado!")
            print("   📧 Email: admin@suameta.com")
            print("   🔑 Senha: admin123\n")

        print("="*70)
        print("✅ MIGRAÇÃO LOCAL CONCLUÍDA COM SUCESSO!")
        print("="*70)
        print("\n🚀 Execute: python app.py")
        print("🌐 Acesse: http://127.0.0.1:5000\n")

def migrate_postgresql(database_url):
    """Migração para PostgreSQL (Railway/Render)"""
    print_header("MIGRAÇÃO POSTGRESQL (Produção)")

    try:
        import psycopg2
        from psycopg2 import sql
    except ImportError:
        print("❌ psycopg2-binary não instalado!")
        print("📦 Instale com: pip install psycopg2-binary")
        return False

    print(f"🔌 Conectando ao PostgreSQL...")

    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        print("✅ Conectado com sucesso!\n")

        # Ler arquivo de migração SQL
        sql_file = Path('migration_railway.sql')
        if not sql_file.exists():
            print("❌ Arquivo migration_railway.sql não encontrado!")
            return False

        print("📄 Aplicando migration_railway.sql...")
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        cursor.execute(sql_content)
        conn.commit()
        print("✅ Tabelas criadas com sucesso!\n")

        # Criar empresa padrão
        print("🏢 Criando empresa padrão...")
        cursor.execute("""
            INSERT INTO empresas (nome, cnpj, email, telefone, endereco, cidade, estado, 
                                plano, max_usuarios, max_vendedores, ativo, bloqueado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING
            RETURNING id;
        """, (
            'Empresa Padrão', '00000000000000', 'contato@empresapadrao.com',
            '(71) 99999-9999', 'Salvador, BA', 'Salvador', 'BA',
            'premium', 100, 500, True, False
        ))

        result = cursor.fetchone()
        if result:
            empresa_id = result[0]
            print(f"✅ Empresa criada (ID: {empresa_id})\n")
        else:
            cursor.execute("SELECT id FROM empresas WHERE email = %s", ('contato@empresapadrao.com',))
            empresa_id = cursor.fetchone()[0]
            print(f"ℹ️  Empresa já existe (ID: {empresa_id})\n")

        # Criar super admin
        print("👑 Criando Super Administrador...")
        senha_hash = generate_password_hash('18042016')
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha_hash, cargo, is_super_admin, 
                                empresa_id, ativo, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (email) DO UPDATE SET
                senha_hash = EXCLUDED.senha_hash,
                is_super_admin = EXCLUDED.is_super_admin
            RETURNING id;
        """, ('Super Admin', 'superadmin@suameta.com', senha_hash, 'admin', True, None, True))

        conn.commit()
        print("✅ Super Admin criado/atualizado!")
        print("   📧 Email: superadmin@suameta.com")
        print("   🔑 Senha: 18042016\n")

        # Criar admin da empresa
        print("🔑 Criando Administrador da Empresa...")
        senha_hash = generate_password_hash('admin123')
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha_hash, cargo, is_super_admin, 
                                empresa_id, ativo, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (email) DO UPDATE SET
                senha_hash = EXCLUDED.senha_hash,
                empresa_id = EXCLUDED.empresa_id
            RETURNING id;
        """, ('Administrador', 'admin@suameta.com', senha_hash, 'admin', False, empresa_id, True))

        conn.commit()
        print("✅ Admin criado/atualizado!")
        print("   📧 Email: admin@suameta.com")
        print("   🔑 Senha: admin123\n")

        cursor.close()
        conn.close()

        print("="*70)
        print("✅ MIGRAÇÃO POSTGRESQL CONCLUÍDA COM SUCESSO!")
        print("="*70)
        print("\n🌐 Sistema pronto para uso em produção!\n")
        return True

    except Exception as e:
        print(f"\n❌ Erro durante migração: {e}")
        return False

def main():
    """Função principal"""
    print_header("SISTEMA DE MIGRAÇÃO CONSOLIDADO")

    # Verificar se é ambiente de produção
    database_url = get_database_url()

    if database_url:
        # Ambiente de produção (PostgreSQL)
        print("🌐 Ambiente: PRODUÇÃO (PostgreSQL)")
        print(f"📍 Database: {database_url[:30]}...\n")

        # Salvar URL para uso futuro
        with open('.railway_db_url.txt', 'w') as f:
            f.write(database_url)
        print("💾 DATABASE_URL salva em .railway_db_url.txt\n")

        migrate_postgresql(database_url)
    else:
        # Ambiente local (SQLite)
        print("💻 Ambiente: LOCAL (SQLite)")
        print("📍 Database: metas.db\n")

        # Perguntar se quer migrar para produção
        print("💡 Dica: Para migrar para produção (Railway/Render):")
        print("   1. Configure DATABASE_URL nas variáveis de ambiente")
        print("   2. Ou cole a URL quando solicitado\n")

        resposta = input("Deseja fornecer DATABASE_URL para migração em produção? (s/N): ").strip().lower()

        if resposta == 's':
            print("\n📋 Cole a DATABASE_URL do Railway/Render:")
            print("   (Deve começar com postgresql:// ou postgres://)\n")
            database_url = input("DATABASE_URL: ").strip()

            if database_url.startswith(('postgresql://', 'postgres://')):
                # Salvar para uso futuro
                with open('.railway_db_url.txt', 'w') as f:
                    f.write(database_url)

                migrate_postgresql(database_url)
            else:
                print("\n⚠️  URL inválida. Executando migração local...")
                migrate_local()
        else:
            migrate_local()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Migração cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
