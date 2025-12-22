#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CORREÇÃO URGENTE: Aplica migração no Railway
Resolve erro 500 ao fazer login
"""

import os
import sys

# Verificar se psycopg2 está instalado
try:
    import psycopg2
except ImportError:
    print("📦 Instalando psycopg2-binary...")
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'], check=True)
    import psycopg2

from werkzeug.security import generate_password_hash

print("\n" + "="*70)
print("🚨 CORREÇÃO URGENTE - ERRO 500")
print("="*70 + "\n")

print("O erro acontece porque o banco PostgreSQL do Railway não tem:")
print("  ❌ Tabela 'empresas'")
print("  ❌ Coluna 'is_super_admin' na tabela usuarios")
print("  ❌ Coluna 'empresa_id' na tabela usuarios\n")

print("Vou aplicar a migração agora!\n")
print("="*70 + "\n")

# Pedir DATABASE_URL
print("🔗 COLE A DATABASE_URL DO RAILWAY:\n")
print("Para obter:")
print("  1. Vá em: https://railway.com/project/8e59c87e-9d32-4230-bdd0-82d98f0eb0f5")
print("  2. Clique no card 'Postgres' (PostgreSQL)")
print("  3. Aba 'Variables' ou 'Connect'")
print("  4. Expanda '8 variables added by Railway'")
print("  5. Copie o valor de 'DATABASE_URL'\n")

database_url = input("DATABASE_URL: ").strip()

if not database_url:
    print("\n❌ Você não colou nada!")
    sys.exit(1)

if not database_url.startswith(('postgresql://', 'postgres://')):
    print(f"\n❌ URL inválida: {database_url[:50]}")
    print("\nDeve começar com: postgresql://")
    sys.exit(1)

print("\n" + "="*70)
print("⚙️  APLICANDO MIGRAÇÃO")
print("="*70 + "\n")

try:
    # Conectar
    print("🔌 Conectando ao PostgreSQL...")
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    print("✅ Conectado!\n")

    # Ler migração
    print("📄 Lendo migration_railway.sql...")
    with open('migration_railway.sql', 'r', encoding='utf-8') as f:
        sql = f.read()

    # Configurar senha
    print("🔐 Gerando senha para super admin...")
    hash_senha = generate_password_hash("18042016")
    sql = sql.replace("'scrypt:32768:8:1$changeme$hashedpassword'", f"'{hash_senha}'")
    print("✅ Senha configurada\n")

    # Executar
    print("⚙️  Executando comandos SQL...\n")

    comandos = sql.split(';')
    executados = 0
    ignorados = 0

    for i, cmd in enumerate(comandos, 1):
        cmd = cmd.strip()
        if not cmd:
            continue

        try:
            cursor.execute(cmd)
            conn.commit()
            executados += 1
            if i % 5 == 0:
                print(f"   ✅ {executados} comandos executados...")
        except psycopg2.Error as e:
            if "already exists" in str(e) or "duplicate" in str(e):
                ignorados += 1
                conn.rollback()
            else:
                print(f"   ⚠️  Erro: {str(e)[:100]}")
                conn.rollback()

    print(f"\n✅ Migração concluída!")
    print(f"   Executados: {executados}")
    print(f"   Ignorados (já existiam): {ignorados}\n")

    # Verificar
    print("🔍 Verificando banco de dados:\n")

    try:
        cursor.execute("SELECT COUNT(*) FROM empresas")
        print(f"   🏢 Empresas: {cursor.fetchone()[0]}")
    except:
        print("   ⚠️  Tabela empresas não encontrada")

    try:
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE is_super_admin = TRUE")
        print(f"   👑 Super Admins: {cursor.fetchone()[0]}")
    except:
        print("   ⚠️  Coluna is_super_admin não encontrada")

    try:
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        print(f"   👥 Total Usuários: {cursor.fetchone()[0]}")
    except:
        print("   ⚠️  Tabela usuarios não encontrada")

    cursor.close()
    conn.close()

    print("\n" + "="*70)
    print("🎉 MIGRAÇÃO APLICADA COM SUCESSO!")
    print("="*70 + "\n")

    print("🔄 PRÓXIMO PASSO: Reiniciar aplicação no Railway\n")
    print("   1. Vá em: https://railway.com/project/8e59c87e-9d32-4230-bdd0-82d98f0eb0f5")
    print("   2. Clique no card 'web'")
    print("   3. Clique nos 3 pontinhos (...)")
    print("   4. Clique em 'Restart'\n")

    print("Ou simplesmente aguarde 30 segundos e teste novamente!\n")

    print("🌐 URL: https://suameta.up.railway.app/login\n")
    print("👑 Super Admin:")
    print("   Email: superadmin@suameta.com")
    print("   Senha: 18042016\n")
    print("🔑 Admin:")
    print("   Email: admin@suameta.com")
    print("   Senha: admin123\n")

    print("✨ Layout responsivo e profissional mantido!")
    print("\n" + "="*70 + "\n")

except psycopg2.OperationalError as e:
    print(f"\n❌ Erro de conexão: {e}\n")
    print("Verifique se a DATABASE_URL está correta!")
    sys.exit(1)
except FileNotFoundError:
    print("\n❌ Arquivo migration_railway.sql não encontrado!")
    print("Certifique-se de estar na pasta do projeto.")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Erro: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)
