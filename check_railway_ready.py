"""
Script de Verificação Pré-Deploy para Railway
Valida se o projeto está pronto para deploy
"""
import os
import sys

def check_file_exists(filepath, description):
    """Verifica se arquivo existe"""
    exists = os.path.exists(filepath)
    status = "[OK]" if exists else "[ERRO]"
    print(f"{status} {description}: {filepath}")
    return exists

def check_file_content(filepath, search_text, description):
    """Verifica se arquivo contém texto específico"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            has_content = search_text in content
            status = "[OK]" if has_content else "[AVISO]"
            print(f"{status} {description}")
            return has_content
    except Exception as e:
        print(f"[ERRO] Erro ao ler {filepath}: {e}")
        return False

def main():
    print("="*70)
    print("VERIFICACAO PRE-DEPLOY - RAILWAY")
    print("="*70)
    
    all_ok = True
    
    # 1. Arquivos essenciais
    print("\n1. Verificando arquivos essenciais...")
    files = [
        ('app.py', 'Aplicacao principal'),
        ('wsgi.py', 'WSGI entry point'),
        ('config.py', 'Configuracoes'),
        ('models.py', 'Modelos do banco'),
        ('requirements.txt', 'Dependencias Python'),
        ('Procfile', 'Comando de start Railway'),
        ('railway.json', 'Configuracao Railway'),
        ('nixpacks.toml', 'Build config'),
        ('.gitignore', 'Git ignore'),
    ]
    
    for filepath, description in files:
        if not check_file_exists(filepath, description):
            all_ok = False
    
    # 2. Verificar requirements.txt
    print("\n2. Verificando dependencias...")
    required_packages = [
        ('Flask', 'Framework web'),
        ('gunicorn', 'WSGI server'),
        ('psycopg2-binary', 'PostgreSQL driver'),
        ('Flask-SQLAlchemy', 'ORM'),
        ('Flask-Login', 'Autenticacao'),
        ('Flask-WTF', 'Formularios'),
    ]
    
    for package, description in required_packages:
        check_file_content('requirements.txt', package, f'{description} ({package})')
    
    # 3. Verificar Procfile
    print("\n3. Verificando Procfile...")
    check_file_content('Procfile', 'gunicorn', 'Comando gunicorn configurado')
    check_file_content('Procfile', 'wsgi:app', 'Entry point correto (wsgi:app)')
    
    # 4. Verificar railway.json
    print("\n4. Verificando railway.json...")
    check_file_content('railway.json', 'healthcheckPath', 'Health check configurado')
    check_file_content('railway.json', '/ping', 'Endpoint /ping definido')
    
    # 5. Verificar config.py
    print("\n5. Verificando config.py...")
    check_file_content('config.py', 'DATABASE_URL', 'Suporte a DATABASE_URL')
    check_file_content('config.py', 'FLASK_SECRET_KEY', 'Suporte a FLASK_SECRET_KEY')
    check_file_content('config.py', 'postgresql', 'Configuracao PostgreSQL')
    
    # 6. Verificar app.py
    print("\n6. Verificando app.py...")
    check_file_content('app.py', '@app.route("/ping")', 'Endpoint /ping existe')
    check_file_content('app.py', '@app.route("/login")', 'Endpoint /login existe')
    
    # 7. Verificar estrutura de pastas
    print("\n7. Verificando estrutura de pastas...")
    folders = [
        ('templates', 'Templates HTML'),
        ('static', 'Arquivos estaticos'),
        ('static/css', 'CSS'),
        ('static/js', 'JavaScript'),
    ]
    
    for folder, description in folders:
        exists = os.path.isdir(folder)
        status = "[OK]" if exists else "[ERRO]"
        print(f"{status} {description}: {folder}/")
        if not exists:
            all_ok = False
    
    # 8. Verificar .gitignore
    print("\n8. Verificando .gitignore...")
    gitignore_items = [
        ('venv/', 'Virtual environment'),
        ('__pycache__/', 'Python cache'),
        ('*.pyc', 'Compiled Python'),
        ('.env', 'Variaveis locais'),
        ('instance/', 'Instance folder'),
    ]
    
    for item, description in gitignore_items:
        check_file_content('.gitignore', item, f'{description} ({item})')
    
    # 9. Verificar ausência de arquivos sensíveis
    print("\n9. Verificando seguranca...")
    sensitive_files = [
        '.env',
        'instance/vendacerta.db',
        '*.db',
        '.DS_Store',
    ]
    
    for pattern in sensitive_files:
        if '*' not in pattern:
            if os.path.exists(pattern):
                print(f"[AVISO] Arquivo sensivel encontrado (deve estar no .gitignore): {pattern}")
            else:
                print(f"[OK] Arquivo sensivel nao encontrado: {pattern}")
    
    # 10. Resumo final
    print("\n" + "="*70)
    if all_ok:
        print("RESULTADO: [OK] Projeto pronto para deploy no Railway!")
        print("\nProximos passos:")
        print("1. Fazer commit: git add . && git commit -m 'Preparado para Railway'")
        print("2. Fazer push: git push origin main")
        print("3. No Railway: New Project > Deploy from GitHub")
        print("4. Adicionar PostgreSQL no Railway")
        print("5. Configurar variaveis (ver .env.railway.example)")
        print("6. Aguardar deploy automatico")
        print("7. Acessar URL gerada e testar /ping e /login")
        return 0
    else:
        print("RESULTADO: [ERRO] Corrigir problemas antes do deploy")
        return 1

if __name__ == '__main__':
    sys.exit(main())
