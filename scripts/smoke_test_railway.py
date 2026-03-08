#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Smoke test para ambiente Railway (produção).

Validações:
- HTTP: /ping, /login e uma rota /api (não deve retornar 5xx)
- Postgres (via DATABASE_PUBLIC_URL / PG*): tabelas essenciais e admin seed

Uso recomendado (puxa variáveis do Railway no seu terminal local):
  railway run python scripts/smoke_test_railway.py

Opcional:
  BASE_URL=https://metacerta.up.railway.app railway run python scripts/smoke_test_railway.py
  ADMIN_EMAIL=admin@sistema.com ADMIN_PASSWORD=admin123 railway run python scripts/smoke_test_railway.py

Observação: este script NÃO faz login via formulário/CSRF. Ele valida apenas que:
- o app está respondendo
- o banco está acessível
- o admin existe e está com flags corretas
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

# Garante que o diretório raiz do projeto esteja no PYTHONPATH,
# mesmo quando o script é executado fora do cwd do repo (ex.: `railway run`).
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sqlalchemy import create_engine, inspect, text


def _fail(msg: str) -> int:
    print(f"❌ {msg}")
    return 1


def _get_base_url() -> str:
    env_domain = (os.getenv("RAILWAY_PUBLIC_DOMAIN") or os.getenv("RAILWAY_STATIC_URL") or "").strip()
    if env_domain:
        return f"https://{env_domain}"

    base_url = (os.getenv("BASE_URL") or "https://metacerta.up.railway.app").strip()
    return base_url.rstrip("/")


def _http_status(url: str, timeout: int = 20) -> int:
    req = urllib.request.Request(url, headers={"User-Agent": "vendacerta-smoke/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return int(getattr(resp, "status", 200))
    except urllib.error.HTTPError as e:
        return int(e.code)


def _database_url() -> str:
    # Import local (evita efeitos colaterais de importar o app Flask)
    from db_utils import get_database_url

    url = get_database_url(prefer_public=True, allow_internal_host=False)
    if not url:
        raise RuntimeError("DATABASE_PUBLIC_URL/DATABASE_URL/PG* não encontrados no ambiente")
    return url


def _connect_args_for_url(url: str) -> dict:
    sslmode = (os.getenv("DB_SSLMODE") or os.getenv("PGSSLMODE") or "").strip()

    # Se não foi especificado e parece URL pública (proxy), exigir SSL.
    # Obs: mesmo em modo interno, 'prefer' costuma ser seguro.
    if not sslmode and ("proxy.rlwy.net" in url or "rlwy.net" in url):
        sslmode = "require"

    return {"sslmode": sslmode} if sslmode else {}


def main() -> int:
    base_url = _get_base_url()
    admin_email = os.getenv("ADMIN_EMAIL", "admin@sistema.com").strip().lower()

    # HTTP
    try:
        checks = {
            "/ping": {200},
            "/login": {200},
            "/api/ranking": {200, 302, 401, 403},
            "/pedidos": {200, 302, 401, 403},
            "/pedidos/visualizar/1": {200, 302, 401, 403},
        }
        for path, ok_status in checks.items():
            status = _http_status(f"{base_url}{path}")
            if status not in ok_status:
                return _fail(f"HTTP {path} retornou {status} (esperado: {sorted(ok_status)})")
        print(f"✅ HTTP OK ({base_url})")
    except Exception as e:
        return _fail(f"Falha HTTP: {e}")

    # DB
    try:
        url = _database_url()
        connect_args = _connect_args_for_url(url)
        engine = create_engine(url, connect_args=connect_args) if connect_args else create_engine(url)

        insp = inspect(engine)
        tables = set(insp.get_table_names())
        required = {
            "usuarios",
            "empresas",
            "clientes",
            "vendedores",
            "metas",
            "vendedor_dias_liberados",
            "pedidos",
        }
        missing = sorted(required - tables)
        if missing:
            return _fail(f"Tabelas faltando no Postgres: {missing}")

        # Validação mínima do schema de pedidos
        pedidos_cols = {c["name"] for c in insp.get_columns("pedidos")}
        pedidos_required_cols = {
            "id",
            "numero_pedido",
            "data_pedido",
            "status",
            "empresa_id",
            "produto",
            "quantidade",
            "preco_unitario",
            "valor_total",
        }
        pedidos_missing_cols = sorted(pedidos_required_cols - pedidos_cols)
        if pedidos_missing_cols:
            return _fail(f"Tabela 'pedidos' sem colunas esperadas: {pedidos_missing_cols}")

        with engine.connect() as conn:
            # Consulta simples (não deve falhar) para garantir que a tabela existe e é consultável
            conn.execute(text("SELECT COUNT(*) FROM pedidos")).scalar()

            row = conn.execute(
                text(
                    """
                    SELECT id, email, cargo, is_super_admin, ativo, bloqueado
                    FROM usuarios
                    WHERE lower(email) = :email
                    """
                ),
                {"email": admin_email},
            ).fetchone()

        if not row:
            return _fail(f"Admin não encontrado no Postgres: {admin_email}")

        _id, email, cargo, is_super_admin, ativo, bloqueado = row
        if cargo != "admin" or not is_super_admin or not ativo or bool(bloqueado):
            return _fail(
                "Admin encontrado, mas flags inválidas: "
                + json.dumps(
                    {
                        "email": email,
                        "cargo": cargo,
                        "is_super_admin": bool(is_super_admin),
                        "ativo": bool(ativo),
                        "bloqueado": bool(bloqueado),
                    },
                    ensure_ascii=False,
                )
            )

        print(f"✅ DB OK (tabelas: {len(tables)}; admin id={_id})")
    except Exception as e:
        return _fail(f"Falha DB: {e}")

    print("\n✅ SMOKE RAILWAY OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
