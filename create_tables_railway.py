#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para criar todas as tabelas no PostgreSQL do Railway
Execute este script no Railway CLI: railway run python create_tables_railway.py
"""

import os
import sys
from datetime import datetime

print("=" * 70)
print("🚀 CRIANDO TABELAS NO POSTGRESQL DO RAILWAY")
print("=" * 70)

# Verificar variáveis de ambiente
print("\n📋 Verificando configuração...")
database_url = os.environ.get('DATABASE_URL') or os.environ.get('URL_DO_BANCO_DE_DADOS')

if not database_url:
    # Construir a partir das variáveis PG*
    pghost = os.environ.get('PGHOST')
    pgport = os.environ.get('PGPORT', '5432')
    pguser = os.environ.get('PGUSER')
    pgpassword = os.environ.get('PGPASSWORD')
    pgdatabase = os.environ.get('PGDATABASE')
    
    if all([pghost, pguser, pgpassword, pgdatabase]):
        database_url = f"postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}"
        print(f"✅ URL construída a partir de PG* vars")
        print(f"   Host: {pghost}:{pgport}")
        print(f"   Database: {pgdatabase}")
    else:
        print("❌ ERRO: Variáveis de ambiente PostgreSQL não encontradas!")
        print("   Configure DATABASE_URL ou as variáveis PG*")
        sys.exit(1)

# Corrigir URL se necessário
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
    print("🔧 URL corrigida: postgres:// → postgresql://")

print(f"✅ Banco configurado: PostgreSQL")

try:
    # Importar app e db
    print("\n📦 Importando aplicação...")
    from app import app, db
    from models import (
        Empresa, Usuario, Vendedor, Meta, Equipe,
        FaixaComissao, FaixaComissaoVendedor, FaixaComissaoSupervisor,
        Mensagem, Cliente, CompraCliente, Produto, EstoqueMovimento,
        Tecnico, OrdemServico
    )
    
    print("✅ Modelos importados com sucesso")
    
    # Criar todas as tabelas
    print("\n🔧 Criando tabelas...")
    with app.app_context():
        # Drop all (cuidado em produção!)
        # db.drop_all()
        # print("⚠️  Tabelas antigas removidas")
        
        # Criar todas as tabelas
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
        
        # Listar tabelas criadas
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n📊 Total de tabelas criadas: {len(tables)}")
        print("\n📋 Tabelas disponíveis:")
        for i, table in enumerate(sorted(tables), 1):
            print(f"   {i:2d}. {table}")
        
        # Testar conexão
        print("\n🔍 Testando conexão...")
        result = db.session.execute(text("SELECT version()"))
        version = result.scalar()
        print(f"✅ Conexão OK - {version.split(',')[0]}")
        
        # Verificar se há dados
        print("\n📈 Verificando dados existentes...")
        empresa_count = Empresa.query.count()
        usuario_count = Usuario.query.count()
        vendedor_count = Vendedor.query.count()
        
        print(f"   Empresas: {empresa_count}")
        print(f"   Usuários: {usuario_count}")
        print(f"   Vendedores: {vendedor_count}")
        
        if usuario_count == 0:
            print("\n💡 PRÓXIMO PASSO: Criar usuário administrador")
            print("   Execute: railway run python create_admin.py")
        
        db.session.commit()
        
    print("\n" + "=" * 70)
    print("✅ SUCESSO! Banco de dados inicializado")
    print("=" * 70)
    print("\n🌐 Acesse: https://metacerta.up.railway.app")
    print("📊 Status: https://metacerta.up.railway.app/status")
    print()

except Exception as e:
    print(f"\n❌ ERRO ao criar tabelas: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
