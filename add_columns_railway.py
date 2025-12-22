#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script simples para adicionar colunas no Railway
Execute DENTRO do ambiente Railway: railway run python add_columns_railway.py
OU adicione ao startup.sh
"""

import os
import sys

print("=" * 80)
print("MIGRANDO SCHEMA - ADICIONANDO NOVAS COLUNAS")
print("=" * 80)

# Verificar se estamos no Railway
is_railway = os.environ.get('RAILWAY_ENVIRONMENT') is not None
if not is_railway:
    print("AVISO: Este script deve ser executado no Railway!")
    print("Use: railway run python add_columns_railway.py")

try:
    print("\nImportando aplicacao...")
    from app import app, db
    from sqlalchemy import text, inspect
    
    with app.app_context():
        print("Verificando schema atual...")
        
        # Obter inspector para verificar colunas existentes
        inspector = inspect(db.engine)
        existing_columns = [col['name'] for col in inspector.get_columns('clientes')]
        print(f"Colunas existentes: {len(existing_columns)}")
        
        # Definir colunas a adicionar
        new_columns = {
            'estado': "VARCHAR(2)",
            'celular2': "VARCHAR(20)",
            'longitude': "NUMERIC(11, 8)",
            'latitude': "NUMERIC(10, 8)",
            'codigo_bw': "VARCHAR(50)",
            'supervisor_id': "INTEGER REFERENCES usuarios(id)"
        }
        
        print(f"\nProcessando {len(new_columns)} novas colunas...")
        added = 0
        skipped = 0
        
        for col_name, col_type in new_columns.items():
            if col_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE clientes ADD COLUMN {col_name} {col_type}"
                    db.session.execute(text(sql))
                    db.session.commit()
                    print(f"[OK] Coluna '{col_name}' adicionada ({col_type})")
                    added += 1
                except Exception as e:
                    print(f"[ERRO] Falha ao adicionar '{col_name}': {str(e)[:80]}")
                    db.session.rollback()
            else:
                print(f"[INFO] Coluna '{col_name}' ja existe")
                skipped += 1
        
        # Criar índice
        print("\nCriando indice...")
        try:
            db.session.execute(text(
                "CREATE INDEX IF NOT EXISTS idx_clientes_supervisor ON clientes(supervisor_id)"
            ))
            db.session.commit()
            print("[OK] Indice 'idx_clientes_supervisor' criado")
        except Exception as e:
            print(f"[INFO] Indice: {str(e)[:80]}")
            db.session.rollback()
        
        # Relatório final
        print("\n" + "=" * 80)
        print("RELATORIO FINAL")
        print("=" * 80)
        print(f"Colunas adicionadas: {added}")
        print(f"Colunas ja existentes: {skipped}")
        print(f"Total de colunas processadas: {added + skipped}")
        
        if added > 0:
            print("\n[SUCCESS] MIGRACAO CONCLUIDA COM SUCESSO!")
            print("As novas colunas estao prontas para uso.")
        else:
            print("\n[INFO] NENHUMA ALTERACAO NECESSARIA")
            print("Todas as colunas ja existem no schema.")
        
        print("\nProximos passos:")
        print("1. Reinicie a aplicacao se necessario")
        print("2. Teste o formulario de cliente")
        print("3. Teste a importacao de Excel")
        print("=" * 80)
        
except Exception as e:
    print("\n" + "=" * 80)
    print("[ERROR] ERRO NA MIGRACAO")
    print("=" * 80)
    print(f"{str(e)}")
    print("\nStack trace:")
    import traceback
    traceback.print_exc()
    print("=" * 80)
    sys.exit(1)
