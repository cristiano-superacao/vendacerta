#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Smoke test do VendaCerta.

Objetivo: validar rapidamente banco/tabelas, seed do admin, rotas públicas e APIs.

Uso (local/SQLite):
  $env:ALLOW_SQLITE_DEV='1'
  $env:ADMIN_EMAIL='admin@sistema.com'
  $env:ADMIN_PASSWORD='admin123'
  python scripts/smoke_test_app.py

Uso (Railway/Postgres):
  $env:DATABASE_URL='...'
  $env:ADMIN_EMAIL='admin@sistema.com'
  $env:ADMIN_PASSWORD='admin123'
  python scripts/smoke_test_app.py
"""

import os
import sys


def _fail(msg: str) -> int:
    print(f"❌ {msg}")
    return 1


def main() -> int:
    # Evitar efeitos colaterais de init em import durante smoke
    os.environ.setdefault("SKIP_DB_INIT_ON_START", "1")

    admin_email = os.environ.get("ADMIN_EMAIL", "admin@sistema.com").strip().lower()
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")

    try:
        from app import app, db
        from models import Usuario
        from sqlalchemy import inspect
    except Exception as e:
        return _fail(f"Falha ao importar app/db/models: {e}")

    with app.app_context():
        # DB / tabelas
        try:
            db.create_all()
            insp = inspect(db.engine)
            tables = set(insp.get_table_names())
            required = {"usuarios", "empresas", "vendedores", "metas"}
            missing = sorted(required - tables)
            if missing:
                return _fail(f"Tabelas faltando: {missing}")
            print(f"✅ DB OK (tabelas: {len(tables)})")
        except Exception as e:
            return _fail(f"Falha DB/tabelas: {e}")

        # Validar admin
        try:
            admin = Usuario.query.filter_by(email=admin_email).first()
            if not admin:
                return _fail(f"Admin não encontrado no banco: {admin_email}. Rode a seed primeiro.")
            if not admin.check_senha(admin_password):
                return _fail("Senha do admin não confere com ADMIN_PASSWORD")
            if admin.cargo != "admin":
                return _fail(f"Cargo do admin inesperado: {admin.cargo}")
            if not admin.ativo:
                return _fail("Admin está inativo")
            print(f"✅ Admin OK ({admin.email})")
        except Exception as e:
            return _fail(f"Falha ao validar admin: {e}")

    # Rotas e APIs via test client
    try:
        client = app.test_client()

        # Públicas
        for path in ["/ping", "/login", "/registro", "/recuperar-senha"]:
            resp = client.get(path, follow_redirects=False)
            if resp.status_code not in (200, 302):
                return _fail(f"GET {path} retornou {resp.status_code}")
        print("✅ Rotas públicas OK")

        # Autenticar sem depender de CSRF/form: injetar sessão do Flask-Login
        with app.app_context():
            admin = Usuario.query.filter_by(email=admin_email).first()
            if not admin:
                return _fail(f"Admin não encontrado no banco: {admin_email}")

        with client.session_transaction() as sess:
            sess["_user_id"] = str(admin.id)
            sess["_fresh"] = True

        # Páginas principais (não devem retornar 500)
        main_pages = [
            "/dashboard",
            "/clientes",
            "/vendedores",
            "/metas",
            "/mensagens",
            "/estoque",
            "/os",
        ]
        for path in main_pages:
            resp = client.get(path, follow_redirects=False)
            if resp.status_code >= 500:
                return _fail(f"GET {path} retornou {resp.status_code}")
        print("✅ Páginas principais OK")

        # API (requer login)
        api_paths = [
            "/api/ranking",
            "/api/comissoes/faixas",
            "/api/estoque/motivos-permitidos/entrada",
        ]
        for path in api_paths:
            resp = client.get(path, follow_redirects=False)
            if resp.status_code in (401, 403):
                return _fail(f"GET {path} retornou {resp.status_code} (autorização falhou)")
            if resp.status_code >= 500:
                return _fail(f"GET {path} retornou {resp.status_code}")

        api_resp = client.get("/api/ranking", follow_redirects=False)
        if api_resp.status_code != 200:
            return _fail(f"GET /api/ranking retornou {api_resp.status_code}")
        if not api_resp.is_json:
            return _fail("/api/ranking não retornou JSON")
        print("✅ APIs OK")

    except Exception as e:
        return _fail(f"Falha no smoke de rotas/API: {e}")

    print("\n✅ SMOKE TEST OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
