#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de validação pré-deploy para Railway
Verifica se todos os componentes estão prontos
"""

import os
import sys
from pathlib import Path

print("=" * 70)
print("🔍 VALIDAÇÃO PRÉ-DEPLOY RAILWAY - VENDACERTA")
print("=" * 70)
print()

# Contadores
erros = 0
avisos = 0
sucessos = 0

def check(descricao, condicao, erro=True):
    """Verifica uma condição e reporta resultado"""
    global erros, avisos, sucessos
    
    if condicao:
        print(f"✅ {descricao}")
        sucessos += 1
        return True
    else:
        if erro:
            print(f"❌ {descricao}")
            erros += 1
        else:
            print(f"⚠️  {descricao}")
            avisos += 1
        return False

# 1. Verificar arquivos essenciais
print("📁 ARQUIVOS ESSENCIAIS")
print("-" * 70)

check("app.py existe", Path("app.py").exists())
check("config.py existe", Path("config.py").exists())
check("models.py existe", Path("models.py").exists())
check("requirements.txt existe", Path("requirements.txt").exists())
check("nixpacks.toml existe", Path("nixpacks.toml").exists())
check("Procfile existe", Path("Procfile").exists())
check("railway.json existe", Path("railway.json").exists())
check("wsgi.py existe", Path("wsgi.py").exists())
check("init_railway.py existe", Path("init_railway.py").exists())
check(".env.example existe", Path(".env.example").exists())
check(".gitignore existe", Path(".gitignore").exists())

print()

# 2. Verificar dependências no requirements.txt
print("📦 DEPENDÊNCIAS PYTHON")
print("-" * 70)

if Path("requirements.txt").exists():
    with open("requirements.txt") as f:
        deps = f.read()
    
    check("Flask instalado", "Flask==" in deps)
    check("Flask-SQLAlchemy instalado", "Flask-SQLAlchemy==" in deps)
    check("Flask-Login instalado", "Flask-Login==" in deps)
    check("Flask-Limiter instalado", "Flask-Limiter==" in deps)
    check("Flask-Compress instalado", "Flask-Compress==" in deps)
    check("gunicorn instalado", "gunicorn==" in deps)
    check("psycopg2-binary instalado", "psycopg2-binary==" in deps)
    check("python-dotenv instalado", "python-dotenv==" in deps)

print()

# 3. Verificar configurações do nixpacks.toml
print("🔧 NIXPACKS CONFIGURATION")
print("-" * 70)

if Path("nixpacks.toml").exists():
    with open("nixpacks.toml") as f:
        nixpacks = f.read()
    
    check("python311 configurado", "python311" in nixpacks)
    check("pip packages configurados", "python311Packages.pip" in nixpacks)
    check("PostgreSQL incluído", "postgresql" in nixpacks)
    check("pip install otimizado", "--no-cache-dir" in nixpacks)

print()

# 4. Verificar Procfile
print("🚀 PROCFILE")
print("-" * 70)

if Path("Procfile").exists():
    with open("Procfile") as f:
        procfile = f.read()
    
    check("gunicorn configurado", "gunicorn" in procfile)
    check("wsgi:app configurado", "wsgi:app" in procfile or "app:app" in procfile)
    check("init_railway.py presente", "init_railway.py" in procfile)
    check("PORT variável presente", "$PORT" in procfile)

print()

# 5. Verificar railway.json
print("🚂 RAILWAY.JSON")
print("-" * 70)

if Path("railway.json").exists():
    import json
    with open("railway.json") as f:
        railway_config = json.load(f)
    
    check("Builder NIXPACKS configurado", 
          railway_config.get("build", {}).get("builder") == "NIXPACKS")
    check("Health check configurado", 
          "healthcheckPath" in railway_config.get("deploy", {}))
    check("Health check é /ping", 
          railway_config.get("deploy", {}).get("healthcheckPath") == "/ping")

print()

# 6. Verificar .gitignore
print("🙈 GITIGNORE")
print("-" * 70)

if Path(".gitignore").exists():
    with open(".gitignore") as f:
        gitignore = f.read()
    
    check(".env ignorado", ".env" in gitignore)
    check("instance/ ignorado", "instance/" in gitignore)
    check("__pycache__ ignorado", "__pycache__" in gitignore)
    check("*.db ignorado", "*.db" in gitignore or "*.sqlite" in gitignore)

print()

# 7. Verificar app.py principais features
print("⚙️  APP.PY FEATURES")
print("-" * 70)

if Path("app.py").exists():
    with open("app.py", encoding='utf-8') as f:
        app_content = f.read()
    
    check("Flask-Limiter importado", "flask_limiter" in app_content.lower() or "Flask-Limiter" in app_content, erro=False)
    check("Health check /ping existe", '@app.route("/ping")' in app_content or '@app.route("/health")' in app_content)
    check("Security headers configurados", "Content-Security-Policy" in app_content or "set_security_headers" in app_content)
    check("ProxyFix configurado", "ProxyFix" in app_content)
    check("Database init existe", "init_database" in app_content or "db.create_all" in app_content)

print()

# 8. Verificar estrutura de diretórios
print("📂 ESTRUTURA DE DIRETÓRIOS")
print("-" * 70)

check("static/ existe", Path("static").exists())
check("templates/ existe", Path("templates").exists())
check("static/css/ existe", Path("static/css").exists(), erro=False)
check("static/js/ existe", Path("static/js").exists(), erro=False)
check("static/img/ existe", Path("static/img").exists(), erro=False)

print()

# 9. Verificar templates principais
print("🎨 TEMPLATES HTML")
print("-" * 70)

templates_dir = Path("templates")
if templates_dir.exists():
    check("login.html existe", (templates_dir / "login.html").exists())
    check("base.html existe", (templates_dir / "base.html").exists(), erro=False)
    
    # Verificar se templates usam Bootstrap
    if (templates_dir / "base.html").exists():
        with open(templates_dir / "base.html", encoding='utf-8') as f:
            base = f.read()
        check("Bootstrap 5.3 presente", "bootstrap@5.3" in base or "bootstrap/5.3" in base, erro=False)
        check("Viewport meta tag presente", 'name="viewport"' in base, erro=False)

print()

# 10. Verificar documentação
print("📚 DOCUMENTAÇÃO")
print("-" * 70)

check("README.md existe", Path("README.md").exists())
check("CHANGELOG.md existe", Path("CHANGELOG.md").exists(), erro=False)
check(".env.example existe", Path(".env.example").exists())

print()

# Resumo final
print("=" * 70)
print("📊 RESUMO DA VALIDAÇÃO")
print("=" * 70)
print(f"✅ Sucessos: {sucessos}")
print(f"⚠️  Avisos: {avisos}")
print(f"❌ Erros: {erros}")
print()

if erros == 0:
    print("🎉 SISTEMA PRONTO PARA DEPLOY NO RAILWAY!")
    print()
    print("Próximos passos:")
    print("1. Gerar SECRET_KEY: python -c \"import secrets; print(secrets.token_urlsafe(64))\"")
    print("2. Configurar variáveis no Railway Dashboard")
    print("3. git add . && git commit -m 'chore: Pronto para deploy'")
    print("4. git push origin main")
    print("5. Aguardar deploy automático no Railway")
    print()
    sys.exit(0)
elif erros <= 2:
    print("⚠️  SISTEMA QUASE PRONTO - Corrija os erros acima")
    print()
    sys.exit(1)
else:
    print("❌ SISTEMA NÃO ESTÁ PRONTO - Muitos erros críticos")
    print()
    print("Revise o CHECKLIST_RAILWAY.md para mais detalhes")
    print()
    sys.exit(1)
