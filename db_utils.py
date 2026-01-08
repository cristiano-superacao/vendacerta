"""Utilitários de conexão/configuração de banco.

Este módulo centraliza regras repetidas em vários scripts:
- Preferir DATABASE_PUBLIC_URL quando aplicável (Railway acesso externo)
- Normalizar URL postgres:// -> postgresql:// (SQLAlchemy)
- Fallback para variáveis PG* (PGHOST/PGPORT/PGUSER/PGPASSWORD/PGDATABASE)

Não importa Flask nem instancia o app; é seguro para scripts e WSGI.
"""

from __future__ import annotations

import os
from typing import Mapping, Optional


def normalize_postgres_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def build_postgres_url_from_pg_env(
    *,
    default_pg: Optional[Mapping[str, str]] = None,
    allow_internal_host: bool = True,
) -> Optional[str]:
    default_pg = default_pg or {}

    host = os.getenv("PGHOST") or default_pg.get("PGHOST")
    port = os.getenv("PGPORT") or default_pg.get("PGPORT", "5432")
    user = os.getenv("PGUSER") or default_pg.get("PGUSER")
    password = os.getenv("PGPASSWORD") or default_pg.get("PGPASSWORD")
    database = os.getenv("PGDATABASE") or default_pg.get("PGDATABASE")

    if not all([host, user, password, database]):
        return None

    if not allow_internal_host and "railway.internal" in str(host):
        return None

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def get_database_url(
    *,
    prefer_public: bool = True,
    allow_internal_host: bool = True,
    default_pg: Optional[Mapping[str, str]] = None,
    allow_fallback_to_pg_env: bool = True,
) -> Optional[str]:
    """Retorna uma URL de banco baseada no ambiente.

    Ordem:
    1) DATABASE_PUBLIC_URL (se prefer_public)
    2) DATABASE_URL
    3) URL_DO_BANCO_DE_DADOS (compat)
    4) Construir a partir de PG* (se allow_fallback_to_pg_env)
    """

    candidates = []

    if prefer_public:
        candidates.append(os.getenv("DATABASE_PUBLIC_URL"))

    candidates.extend(
        [
            os.getenv("DATABASE_URL"),
            os.getenv("URL_DO_BANCO_DE_DADOS"),
        ]
    )

    for candidate in candidates:
        if candidate:
            return normalize_postgres_url(candidate)

    if not allow_fallback_to_pg_env:
        return None

    return build_postgres_url_from_pg_env(
        default_pg=default_pg,
        allow_internal_host=allow_internal_host,
    )
