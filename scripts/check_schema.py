#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Valida o schema local do PostgreSQL para a tabela 'usuarios'.
- Verifica conexão via DATABASE_URL ou PG*.
- Lista colunas e confirma se campos críticos existem.

Uso:
  $env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/vendacerta"
  python scripts/check_schema.py
"""
import os
import sys
from sqlalchemy import create_engine, inspect

from db_utils import get_database_url

REQUIRED_COLS = [
    "supervisor_id",
    "gerente_id",
    "departamento",
    "pode_gerenciar_tecnicos",
    "pode_atribuir_tecnicos",
]


def _build_db_url():
    url = get_database_url(
        prefer_public=False,
        default_pg={
            "PGHOST": "localhost",
            "PGPORT": "5432",
            "PGUSER": "postgres",
            "PGPASSWORD": "postgres",
            "PGDATABASE": "vendacerta",
        },
    )
    if not url:
        raise RuntimeError("Não foi possível montar DATABASE_URL")
    return url


def main():
    try:
        url = _build_db_url()
        print(f"🔗 Conectando em: {url.split('@')[1] if '@' in url else url}")
        engine = create_engine(url)
        insp = inspect(engine)
        if "usuarios" not in insp.get_table_names():
            print("❌ Tabela 'usuarios' não encontrada.")
            sys.exit(2)
        cols = sorted([c["name"] for c in insp.get_columns("usuarios")])
        print("📊 Colunas:", ", ".join(cols))
        missing = [c for c in REQUIRED_COLS if c not in cols]
        if missing:
            print("❌ Faltando colunas:", ", ".join(missing))
            sys.exit(3)
        print("✅ Schema OK: todas as colunas obrigatórias existem.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
