#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Validação - Correções de Deploy Railway
Verifica se todas as otimizações foram aplicadas corretamente
"""

import os
import sys

def check(name, condition):
    """Helper para validação"""
    status = "✅" if condition else "❌"
    print(f"{status} {name}")
    return condition

def main():
    print("=" * 70)
    print("🔍 VALIDANDO CORREÇÕES DE DEPLOY RAILWAY")
    print("=" * 70)
    print()
    
    all_ok = True
    
    # 1. Verificar nixpacks.toml
    print("📦 1. Verificando nixpacks.toml...")
    try:
        with open('nixpacks.toml', 'r', encoding='utf-8') as f:
            nixpacks = f.read()
        
        all_ok &= check("  - Contém --no-cache-dir", "--no-cache-dir" in nixpacks)
        all_ok &= check("  - Contém init_railway.py no build", "python init_railway.py" in nixpacks)
        all_ok &= check("  - Start com gunicorn direto", "gunicorn wsgi:app" in nixpacks)
        all_ok &= check("  - Flag --preload presente", "--preload" in nixpacks)
        all_ok &= check("  - Bind na porta $PORT", "0.0.0.0:$PORT" in nixpacks)
    except FileNotFoundError:
        all_ok = False
        print("  ❌ Arquivo nixpacks.toml não encontrado!")
    
    print()
    
    # 2. Verificar railway.json
    print("🚂 2. Verificando railway.json...")
    try:
        import json
        with open('railway.json', 'r', encoding='utf-8') as f:
            railway = json.load(f)
        
        all_ok &= check("  - Builder NIXPACKS", railway.get('build', {}).get('builder') == 'NIXPACKS')
        all_ok &= check("  - Healthcheck /ping", railway.get('deploy', {}).get('healthcheckPath') == '/ping')
        
        timeout = railway.get('deploy', {}).get('healthcheckTimeout', 0)
        all_ok &= check(f"  - Timeout ajustado ({timeout}s)", timeout <= 100)
        
        retries = railway.get('deploy', {}).get('restartPolicyMaxRetries', 0)
        all_ok &= check(f"  - Max retries reduzido ({retries})", retries <= 3)
    except FileNotFoundError:
        all_ok = False
        print("  ❌ Arquivo railway.json não encontrado!")
    except json.JSONDecodeError:
        all_ok = False
        print("  ❌ Erro ao ler railway.json - JSON inválido!")
    
    print()
    
    # 3. Verificar init_railway.py
    print("🔧 3. Verificando init_railway.py...")
    try:
        with open('init_railway.py', 'r', encoding='utf-8') as f:
            init_code = f.read()
        
        all_ok &= check("  - Script simplificado", len(init_code) < 1500)
        all_ok &= check("  - Sem traceback.print_exc()", "traceback.print_exc()" not in init_code)
        all_ok &= check("  - Não falha em exceção", "pass" in init_code and "except" in init_code)
        all_ok &= check("  - Mensagens curtas", "Init Railway DB" in init_code or "Init concluído" in init_code)
    except FileNotFoundError:
        all_ok = False
        print("  ❌ Arquivo init_railway.py não encontrado!")
    
    print()
    
    # 4. Verificar Procfile
    print("📋 4. Verificando Procfile...")
    try:
        with open('Procfile', 'r', encoding='utf-8') as f:
            procfile = f.read()
        
        all_ok &= check("  - Comando web presente", "web:" in procfile)
        all_ok &= check("  - Ativa venv", ".venv/bin/activate" in procfile)
        all_ok &= check("  - Usa gunicorn", "gunicorn" in procfile)
        all_ok &= check("  - Bind na porta $PORT", "$PORT" in procfile)
        all_ok &= check("  - Flag --preload", "--preload" in procfile)
        all_ok &= check("  - Sem startup.sh", "startup.sh" not in procfile)
    except FileNotFoundError:
        all_ok = False
        print("  ❌ Arquivo Procfile não encontrado!")
    
    print()
    
    # 5. Verificar endpoint /ping em app.py
    print("🏥 5. Verificando endpoint /ping...")
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            app_code = f.read()
        
        all_ok &= check("  - Route /ping existe", '@app.route("/ping")' in app_code)
        all_ok &= check("  - Route /health existe", '@app.route("/health")' in app_code)
        all_ok &= check("  - Retorna status 200", 'return jsonify' in app_code and '200' in app_code)
        all_ok &= check("  - Query rápida SELECT 1", 'SELECT 1' in app_code)
    except FileNotFoundError:
        all_ok = False
        print("  ❌ Arquivo app.py não encontrado!")
    
    print()
    
    # 6. Verificar requirements.txt
    print("📦 6. Verificando requirements.txt...")
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            reqs = f.read()
        
        all_ok &= check("  - Flask instalado", "Flask==" in reqs)
        all_ok &= check("  - Gunicorn instalado", "gunicorn==" in reqs)
        all_ok &= check("  - psycopg2-binary instalado", "psycopg2-binary==" in reqs)
        all_ok &= check("  - Flask-SQLAlchemy instalado", "Flask-SQLAlchemy==" in reqs)
    except FileNotFoundError:
        all_ok = False
        print("  ❌ Arquivo requirements.txt não encontrado!")
    
    print()
    
    # 7. Verificar estrutura de pastas
    print("📁 7. Verificando estrutura...")
    all_ok &= check("  - Pasta templates existe", os.path.exists('templates'))
    all_ok &= check("  - Pasta static existe", os.path.exists('static'))
    all_ok &= check("  - wsgi.py existe", os.path.exists('wsgi.py'))
    all_ok &= check("  - config.py existe", os.path.exists('config.py'))
    all_ok &= check("  - models.py existe", os.path.exists('models.py'))
    
    print()
    print("=" * 70)
    
    if all_ok:
        print("✅ TODAS AS VALIDAÇÕES PASSARAM!")
        print()
        print("🚀 Sistema pronto para deploy no Railway")
        print()
        print("Próximos passos:")
        print("1. git add .")
        print('2. git commit -m "fix: Otimizar deploy Railway - corrigir timeout"')
        print("3. git push origin main")
        print("4. Aguardar deploy automático no Railway")
        print()
        return 0
    else:
        print("❌ ALGUMAS VALIDAÇÕES FALHARAM!")
        print()
        print("Por favor, corrija os problemas acima antes de fazer deploy.")
        print()
        return 1

if __name__ == '__main__':
    sys.exit(main())
