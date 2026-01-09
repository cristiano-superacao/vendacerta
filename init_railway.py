#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script ultrarrápido de inicialização para Railway
Cria tabelas apenas se necessário - otimizado para evitar timeout
"""

import os
import sys

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Garantir que o diretório instance existe (para SQLite)
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

print("🚀 Init Railway DB...")

# Verificar dependências Excel
try:
    enabled = os.environ.get("ENABLE_EXCEL_CHECK", "0")
    if enabled == "1":
        print("\n🔍 Verificando bibliotecas Excel...")
        import pandas as pd
        import openpyxl
        import numpy as np
        print(f"✅ Pandas {pd.__version__}")
        print(f"✅ OpenPyXL {openpyxl.__version__}")
        print(f"✅ NumPy {np.__version__}")
    else:
        print("\nℹ️ Verificação de bibliotecas Excel desativada (ENABLE_EXCEL_CHECK=0)")
except Exception as e:
    print(f"⚠️  Aviso Excel: {e}")
    if "libstdc++" in str(e) or ".so" in str(e):
        print("🔧 Erro de biblioteca do sistema - veja nixpacks.toml")

print()

try:
    db_url = os.environ.get('DATABASE_URL') or os.environ.get('URL_DO_BANCO_DE_DADOS')
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    if db_url and 'postgres' in db_url:
        print(f"✅ DB: PostgreSQL")
    else:
        print("⚠️ DB: SQLite")
    
    from app import app, db
    from sqlalchemy import create_engine, text, inspect
    
    with app.app_context():
        # Criar tabelas rapidamente
        db.create_all()
        print("✅ Tabelas OK")
        
        # Migração: Adicionar colunas faltantes na tabela usuarios (supervisor_id, gerente_id, departamento, permissões)
        try:
            print("🔧 Verificando migração de colunas em 'usuarios'...")
            inspector = inspect(db.engine)
            
            if 'usuarios' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('usuarios')]

                cols_to_check = {
                    'supervisor_id': 'INTEGER',
                    'gerente_id': 'INTEGER',
                    'departamento': 'VARCHAR(50)',
                    'pode_gerenciar_tecnicos': 'BOOLEAN DEFAULT FALSE',
                    'pode_atribuir_tecnicos': 'BOOLEAN DEFAULT FALSE'
                }

                for col_name, col_type in cols_to_check.items():
                    if col_name not in columns:
                        print(f"➡️  Adicionando {col_name}...")
                        try:
                            db.session.execute(text(f"ALTER TABLE usuarios ADD COLUMN {col_name} {col_type}"))
                            db.session.commit()
                            print(f"✅ Coluna {col_name} adicionada")
                            
                            if col_name in ['supervisor_id', 'gerente_id']:
                                # Adicionar FK
                                try:
                                    fk_name = f"fk_usuarios_{col_name.replace('_id', '')}"
                                    db.session.execute(text(f"""
                                        ALTER TABLE usuarios 
                                        ADD CONSTRAINT {fk_name} 
                                        FOREIGN KEY ({col_name}) 
                                        REFERENCES usuarios(id)
                                    """))
                                    db.session.commit()
                                    print(f"✅ FK {fk_name} criada")
                                except Exception as e:
                                    print(f"⚠️  FK {col_name}: {e}")
                        except Exception as e:
                            print(f"❌ Erro ao adicionar {col_name}: {e}")
                    else:
                        print(f"✅ {col_name} já existe")
        except Exception as e:
            print(f"⚠️  Migração: {e}")
        
        # Quick check
        from sqlalchemy import text
        db.session.execute(text("SELECT 1"))
        db.session.commit()
        print("✅ Conexão OK")

        # Garantir unicidade por empresa em 'clientes' (corrige índices legados globais)
        try:
            if db_url and 'postgres' in db_url:
                print("\n🔧 Verificando unicidade por empresa em 'clientes'...")
                DROP_INDEXES = [
                    'ix_clientes_cpf',
                    'ix_clientes_cnpj',
                    'ix_clientes_codigo_cliente',
                    'clientes_cpf_key',
                    'clientes_cnpj_key',
                    'clientes_codigo_cliente_key',
                ]
                for idx in DROP_INDEXES:
                    try:
                        db.session.execute(text(f'DROP INDEX IF EXISTS {idx}'))
                    except Exception as e:
                        print(f"   ⚠️  Não foi possível remover {idx}: {e}")
                db.session.commit()

                CREATE_UNIQUE = [
                    "CREATE UNIQUE INDEX IF NOT EXISTS uq_cliente_empresa_cpf ON clientes (empresa_id, cpf)",
                    "CREATE UNIQUE INDEX IF NOT EXISTS uq_cliente_empresa_cnpj ON clientes (empresa_id, cnpj)",
                    "CREATE UNIQUE INDEX IF NOT EXISTS uq_cliente_empresa_codigo ON clientes (empresa_id, codigo_cliente)",
                ]
                for create_sql in CREATE_UNIQUE:
                    try:
                        db.session.execute(text(create_sql))
                    except Exception as e:
                        print(f"   ❌ Erro ao criar índice: {e}")
                db.session.commit()
                print("✅ Unicidade por empresa garantida")
            else:
                print("ℹ️  Unicidade por empresa: verificação automática focada em PostgreSQL. Pulando...")
        except Exception as e:
            print(f"⚠️  Verificação de unicidade por empresa falhou: {e}")
        
except Exception as e:
    print(f"⚠️ Aviso: {e}")
    # Não bloqueia deploy
    pass

print("✅ Init concluído")
    # NÃO fazer sys.exit(1) para não travar o deploy
    # O Gunicorn vai tentar iniciar o app de qualquer forma

print("=" * 70)
print("✅ Inicialização concluída - Gunicorn vai assumir agora")
print("=" * 70)
