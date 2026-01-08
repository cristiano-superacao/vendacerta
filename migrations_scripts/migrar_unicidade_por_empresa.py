#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migração: ajustar unicidade de clientes por empresa.
- Remove unicidade global de CPF/CNPJ/codigo_cliente
- Cria unicidade composta (empresa_id, cpf/cnpj/codigo_cliente)
Compatível com PostgreSQL.
"""

import os, sys
# Garantir que o diretório raiz do projeto está no PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, db
from sqlalchemy import text

DROP_INDEXES = [
    # Índices/constraints antigas (podem variar por nome)
    'ix_clientes_cpf',
    'ix_clientes_cnpj',
    'ix_clientes_codigo_cliente',
    'clientes_cpf_key',
    'clientes_cnpj_key',
    'clientes_codigo_cliente_key',
]

CREATE_UNIQUE = [
    "CREATE UNIQUE INDEX IF NOT EXISTS uq_cliente_empresa_cpf ON clientes (empresa_id, cpf)",
    "CREATE UNIQUE INDEX IF NOT EXISTS uq_cliente_empresa_cnpj ON clientes (empresa_id, cnpj)",
    "CREATE UNIQUE INDEX IF NOT EXISTS uq_cliente_empresa_codigo ON clientes (empresa_id, codigo_cliente)",
]

CHECK_DUPLICATES_SQL = {
    'cpf': text("""
        SELECT empresa_id, cpf, COUNT(*) AS total
        FROM clientes
        WHERE cpf IS NOT NULL AND cpf <> ''
        GROUP BY empresa_id, cpf
        HAVING COUNT(*) > 1
        ORDER BY total DESC
    """),
    'cnpj': text("""
        SELECT empresa_id, cnpj, COUNT(*) AS total
        FROM clientes
        WHERE cnpj IS NOT NULL AND cnpj <> ''
        GROUP BY empresa_id, cnpj
        HAVING COUNT(*) > 1
        ORDER BY total DESC
    """),
    'codigo_cliente': text("""
        SELECT empresa_id, codigo_cliente, COUNT(*) AS total
        FROM clientes
        WHERE codigo_cliente IS NOT NULL AND codigo_cliente <> ''
        GROUP BY empresa_id, codigo_cliente
        HAVING COUNT(*) > 1
        ORDER BY total DESC
    """),
}


def migrar():
    with app.app_context():
        print("\n" + "="*70)
        print("🔄 MIGRAÇÃO: Unicidade por empresa (clientes)")
        print("="*70 + "\n")
        
        with db.engine.connect() as conn:
            # 1) Remover constraints/índices antigos (se existirem)
            print("➖ Removendo índices/constraints antigos (se existirem)...")
            for idx in DROP_INDEXES:
                try:
                    conn.execute(text(f'DROP INDEX IF EXISTS {idx}'))
                    print(f"   - Removido: {idx}")
                except Exception as e:
                    print(f"   ⚠️  Não foi possível remover {idx}: {e}")
            conn.commit()

            # 2) Verificar duplicados por empresa (relatório)
            print("\n🔍 Verificando duplicados por empresa:")
            for campo, sql in CHECK_DUPLICATES_SQL.items():
                try:
                    res = conn.execute(sql).fetchall()
                    if res:
                        print(f"   ⚠️  Duplicados encontrados em '{campo}':")
                        for empresa_id, valor, total in res:
                            print(f"      - Empresa {empresa_id} | {campo}={valor} -> {total} registros")
                    else:
                        print(f"   ✅ Nenhum duplicado em '{campo}' por empresa")
                except Exception as e:
                    print(f"   ⚠️  Erro ao verificar '{campo}': {e}")

            # 3) Criar índices únicos compostos
            print("\n➕ Criando índices únicos compostos...")
            for create_sql in CREATE_UNIQUE:
                try:
                    conn.execute(text(create_sql))
                    print(f"   - Criado: {create_sql.split('ON')[0].strip()}")
                except Exception as e:
                    print(f"   ❌ Erro ao criar índice: {e}")
            conn.commit()

            print("\n" + "="*70)
            print("✅ MIGRAÇÃO CONCLUÍDA")
            print("="*70 + "\n")


if __name__ == '__main__':
    migrar()
