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
import re
import http.cookiejar
import urllib.error
import urllib.request
import urllib.parse

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


def _extract_csrf_token(html: str) -> str | None:
    # WTForms normalmente gera: <input id="csrf_token" name="csrf_token" type="hidden" value="...">
    m = re.search(r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if not m:
        return None
    return m.group(1)


def _login_and_validate(base_url: str, admin_email: str, admin_password: str) -> None:
    """Efetua login real (GET /login -> CSRF -> POST) e valida rota protegida."""

    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    # 1) GET /login para pegar CSRF
    login_url = f"{base_url}/login"
    req = urllib.request.Request(login_url, headers={"User-Agent": "vendacerta-smoke/1.0"})
    with opener.open(req, timeout=30) as resp:
        status = int(getattr(resp, "status", 200))
        html = resp.read().decode("utf-8", errors="replace")

    if status != 200:
        raise RuntimeError(f"GET /login retornou {status}")

    csrf = _extract_csrf_token(html)
    if not csrf:
        raise RuntimeError("Não foi possível extrair csrf_token do HTML de /login")

    # 2) POST credenciais
    payload = urllib.parse.urlencode(
        {
            "csrf_token": csrf,
            "email": admin_email,
            "senha": admin_password,
        }
    ).encode("utf-8")

    post_req = urllib.request.Request(
        login_url,
        data=payload,
        method="POST",
        headers={
            "User-Agent": "vendacerta-smoke/1.0",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    # opener segue redirects automaticamente
    with opener.open(post_req, timeout=30) as post_resp:
        post_status = int(getattr(post_resp, "status", 200))
        _ = post_resp.read()  # drenar

    if post_status not in {200}:
        # Em geral após redirect já vira 200
        raise RuntimeError(f"POST /login retornou {post_status}")

    # 3) Validar rota protegida com sessão
    protected_url = f"{base_url}/dashboard"
    dash_req = urllib.request.Request(protected_url, headers={"User-Agent": "vendacerta-smoke/1.0"})
    with opener.open(dash_req, timeout=30) as dash_resp:
        dash_status = int(getattr(dash_resp, "status", 200))
        dash_html = dash_resp.read().decode("utf-8", errors="replace")

    if dash_status != 200:
        raise RuntimeError(f"GET /dashboard pós-login retornou {dash_status}")
    if "Bem-vindo" in dash_html and "Email ou senha incorretos" in dash_html:
        raise RuntimeError("Login parece ter falhado (mensagem de erro detectada)")


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
    admin_password = (os.getenv("ADMIN_PASSWORD") or "").strip()

    # HTTP
    try:
        checks = {
            "/ping": {200},
            "/login": {200},
            "/api/ranking": {200, 302, 401, 403},
            "/pedidos": {200, 302, 401, 403},
            # Pode não existir pedido com id=1 em bases novas
            "/pedidos/visualizar/1": {200, 302, 401, 403, 404},
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

        # Schema do cancelamento (colunas adicionadas)
        pedidos_cancel_cols = {
            "status_pedido",
            "cancelado_por",
            "data_cancelamento",
            "motivo_cancelamento",
        }
        pedidos_cancel_missing = sorted(pedidos_cancel_cols - pedidos_cols)
        if pedidos_cancel_missing:
            return _fail(f"Tabela 'pedidos' sem colunas de cancelamento: {pedidos_cancel_missing}")

        # Auditoria
        if "pedidos_log" not in tables:
            return _fail("Tabela 'pedidos_log' não encontrada (auditoria de pedidos)")

        # CompraCliente (vendas) também deve suportar cancelamento sem apagar histórico
        if "compras_clientes" in tables:
            compras_cols = {c["name"] for c in insp.get_columns("compras_clientes")}
            compras_cancel_cols = {
                "status_compra",
                "cancelado_por",
                "data_cancelamento",
                "motivo_cancelamento",
            }
            compras_cancel_missing = sorted(compras_cancel_cols - compras_cols)
            if compras_cancel_missing:
                return _fail(
                    f"Tabela 'compras_clientes' sem colunas de cancelamento: {compras_cancel_missing}"
                )

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

    # Login E2E (opcional; depende de ADMIN_PASSWORD)
    if admin_password:
        try:
            _login_and_validate(base_url, admin_email, admin_password)
            print("✅ LOGIN OK (/login -> /dashboard)")
        except Exception as e:
            return _fail(f"Falha LOGIN: {e}")
    else:
        print("ℹ️  LOGIN SKIP (defina ADMIN_PASSWORD para validar ponta a ponta)")

    print("\n✅ SMOKE RAILWAY OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
