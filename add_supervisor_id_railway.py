#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script super simplificado para adicionar colunas - SEM dependencia do app.py
Executa SQL direto usando psycopg2
"""

import os
import sys

print("=" * 80)
print("ADD COLUMNS TO CLIENTES TABLE")
print("=" * 80)

# Obter DATABASE_URL
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    print("[SKIP] DATABASE_URL not found - running locally")
    sys.exit(0)

try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    
    print("[INFO] Connecting to database...")
    
    # Conectar
    conn = psycopg2.connect(database_url)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    print("[INFO] Adding columns...")
    
    # Executar ALTER TABLE para cada coluna
    sqls = [
        ("estado", "ALTER TABLE clientes ADD COLUMN IF NOT EXISTS estado VARCHAR(2)"),
        ("celular2", "ALTER TABLE clientes ADD COLUMN IF NOT EXISTS celular2 VARCHAR(20)"),
        ("longitude", "ALTER TABLE clientes ADD COLUMN IF NOT EXISTS longitude NUMERIC(11, 8)"),
        ("latitude", "ALTER TABLE clientes ADD COLUMN IF NOT EXISTS latitude NUMERIC(10, 8)"),
        ("codigo_bw", "ALTER TABLE clientes ADD COLUMN IF NOT EXISTS codigo_bw VARCHAR(50)"),
        ("supervisor_id", "ALTER TABLE clientes ADD COLUMN IF NOT EXISTS supervisor_id INTEGER REFERENCES usuarios(id)"),
        ("index", "CREATE INDEX IF NOT EXISTS idx_clientes_supervisor ON clientes(supervisor_id)")
    ]
    
    for name, sql in sqls:
        try:
            cur.execute(sql)
            print(f"[OK] {name}")
        except Exception as e:
            print(f"[INFO] {name}: {str(e)[:60]}")
    
    cur.close()
    conn.close()
    
    print("\n[SUCCESS] Migration completed!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 
                ON usuarios(supervisor_id)
            """))
            
            conn.commit()
            
            print("✅ Coluna supervisor_id adicionada com sucesso!")
            print("✅ Foreign key criada: fk_usuarios_supervisor")
            print("✅ Índice criado: idx_usuario_supervisor")
            
    except Exception as e:
        print(f"❌ Erro ao executar migração: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    print("=" * 60)
    print("MIGRAÇÃO: Adicionar supervisor_id à tabela usuarios")
    print("=" * 60)
    add_supervisor_id()
    print("=" * 60)
    print("🎉 Migração concluída!")
