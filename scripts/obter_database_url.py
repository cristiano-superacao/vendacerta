#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para obter DATABASE_URL do Railway e aplicar migração
"""

import subprocess
import sys
import os

print("\n" + "="*70)
print("🔍 OBTENDO DATABASE_URL DO RAILWAY")
print("="*70 + "\n")

# Verificar se Railway CLI está instalado
try:
    result = subprocess.run(['railway', '--version'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print("✅ Railway CLI encontrado!")
        print(f"   Versão: {result.stdout.strip()}\n")

        print("🔗 Obtendo DATABASE_URL do Railway...")

        # Tentar obter variáveis do Railway
        result = subprocess.run(['railway', 'variables'], 
                              capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            output = result.stdout

            # Procurar DATABASE_URL na saída
            for line in output.split('\n'):
                if 'DATABASE_URL' in line:
                    print("\n✅ DATABASE_URL encontrada!\n")
                    # Extrair a URL (formato pode variar)
                    if '=' in line:
                        url = line.split('=', 1)[1].strip()
                    else:
                        url = line.split(':', 1)[1].strip()

                    print(f"🔗 URL: {url[:50]}...\n")

                    # Salvar em arquivo temporário
                    with open('.railway_db_url.txt', 'w') as f:
                        f.write(url)

                    print("💾 URL salva em .railway_db_url.txt")
                    print("\n🚀 Agora execute:")
                    print("   python aplicar_migracao_railway.py")
                    sys.exit(0)

            print("\n⚠️  DATABASE_URL não encontrada nas variáveis.")
            print("\n📋 Variáveis disponíveis:")
            print(output)
        else:
            print(f"❌ Erro ao obter variáveis: {result.stderr}")

except FileNotFoundError:
    print("⚠️  Railway CLI não está instalado.\n")
    print("📦 Para instalar:")
    print("   npm i -g @railway/cli\n")
    print("   Depois execute:")
    print("   railway login")
    print("   railway link\n")

except Exception as e:
    print(f"❌ Erro: {e}\n")

# Se chegou aqui, não conseguiu via CLI
print("\n" + "="*70)
print("📋 OBTER DATABASE_URL MANUALMENTE")
print("="*70 + "\n")

print("Siga estes passos:\n")
print("1. Acesse: https://railway.app")
print("2. Faça login")
print("3. Clique no seu projeto")
print("4. Clique no card 'PostgreSQL'")
print("5. Clique na aba 'Variables' ou 'Connect'")
print("6. Copie a 'DATABASE_URL' ou 'Postgres Connection URL'\n")

database_url = input("🔗 Cole a DATABASE_URL aqui (ou pressione Enter para sair): ").strip()

if database_url:
    # Salvar em arquivo
    with open('.railway_db_url.txt', 'w') as f:
        f.write(database_url)

    print("\n✅ URL salva em .railway_db_url.txt")
    print("\n🚀 Executando migração automaticamente...\n")

    # Definir variável de ambiente e executar migração
    os.environ['DATABASE_URL'] = database_url

    # Executar script de migração
    try:
        subprocess.run([sys.executable, 'aplicar_migracao_railway.py'], check=True)
    except subprocess.CalledProcessError:
        print("\n❌ Erro ao executar migração.")
        print("💡 Tente executar manualmente:")
        print("   python aplicar_migracao_railway.py")
else:
    print("\n⏭️  Operação cancelada.")

print("\n" + "="*70 + "\n")
