#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para migrar o schema do banco de dados no Railway
Adiciona as novas colunas à tabela clientes
"""

import os
import sys
from sqlalchemy import create_engine, text

print("=" * 80)
print("🔄 MIGRANDO SCHEMA DO BANCO DE DADOS NO RAILWAY")
print("=" * 80)

# Obter DATABASE_URL
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    # Construir a partir das variáveis PG*
    pghost = os.environ.get('PGHOST')
    pgport = os.environ.get('PGPORT', '5432')
    pguser = os.environ.get('PGUSER')
    pgpassword = os.environ.get('PGPASSWORD')
    pgdatabase = os.environ.get('PGDATABASE')
    
    if all([pghost, pguser, pgpassword, pgdatabase]):
        database_url = f"postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}"
    else:
        print("❌ ERRO: Variáveis de ambiente não encontradas!")
        sys.exit(1)

# Corrigir URL
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

print(f"✅ Conectando ao banco de dados...")

try:
    engine = create_engine(database_url)
    
    with engine.connect() as conn:
        print("\n📋 Verificando schema atual...")
        
        # Verificar se as colunas já existem
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'clientes'
            ORDER BY column_name
        """))
        
        existing_columns = [row[0] for row in result]
        print(f"   Colunas existentes: {len(existing_columns)}")
        
        # Colunas que precisam ser adicionadas
        new_columns = {
            'estado': "VARCHAR(2)",
            'celular2': "VARCHAR(20)",
            'longitude': "NUMERIC(11, 8)",
            'latitude': "NUMERIC(10, 8)",
            'codigo_bw': "VARCHAR(50)",
            'supervisor_id': "INTEGER"
        }
        
        print("\n🔧 Adicionando novas colunas...")
        
        for col_name, col_type in new_columns.items():
            if col_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE clientes ADD COLUMN {col_name} {col_type}"
                    if col_name == 'supervisor_id':
                        sql += " REFERENCES usuarios(id)"
                    
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"   ✅ Coluna '{col_name}' adicionada")
                except Exception as e:
                    if "already exists" in str(e):
                        print(f"   ℹ️  Coluna '{col_name}' já existe")
                    else:
                        print(f"   ⚠️  Erro ao adicionar '{col_name}': {e}")
            else:
                print(f"   ℹ️  Coluna '{col_name}' já existe")
        
        # Criar índice para supervisor_id se não existir
        print("\n🔧 Criando índices...")
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_clientes_supervisor 
                ON clientes(supervisor_id)
            """))
            conn.commit()
            print("   ✅ Índice 'idx_clientes_supervisor' criado")
        except Exception as e:
            print(f"   ℹ️  Índice já existe ou erro: {e}")
        
        # Verificar resultado final
        print("\n📊 Verificando resultado...")
        result = conn.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'clientes'
            AND column_name IN ('estado', 'celular2', 'longitude', 'latitude', 'codigo_bw', 'supervisor_id')
            ORDER BY column_name
        """))
        
        final_columns = list(result)
        print(f"   Novas colunas confirmadas: {len(final_columns)}")
        
        for col_name, col_type in final_columns:
            print(f"   - {col_name}: {col_type}")
    
    print("\n" + "=" * 80)
    print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    print("\n💡 Próximos passos:")
    print("   1. Reinicie a aplicação Railway se necessário")
    print("   2. Teste a importação de clientes com os novos campos")
    print("   3. Verifique o formulário de cadastro de clientes")
    
except Exception as e:
    print(f"\n❌ ERRO NA MIGRAÇÃO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
