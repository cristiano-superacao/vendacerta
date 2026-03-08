#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema VendaCerta v2.0 - Railway Health Check
Verificação de saúde do sistema para Railway deployment
"""

import os
import sys
from datetime import datetime

def check_environment_variables():
    """Verifica se todas as variáveis de ambiente necessárias estão configuradas"""
    required_vars = {
        'DATABASE_URL': 'URL de conexão PostgreSQL',
        'SECRET_KEY': 'Chave secreta Flask',
    }
    
    optional_vars = {
        'FLASK_ENV': 'Ambiente Flask (production/development)',
        'PYTHONUNBUFFERED': 'Output unbuffered',
        'PORT': 'Porta do servidor',
    }
    
    print("🔍 Verificando Variáveis de Ambiente Railway\n")
    print("=" * 60)
    
    # Variáveis obrigatórias
    print("\n✅ VARIÁVEIS OBRIGATÓRIAS:")
    missing_required = []
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            # Mascarar valores sensíveis
            if 'SECRET' in var or 'PASSWORD' in var or 'DATABASE_URL' in var:
                display_value = f"{value[:10]}...{value[-4:]}" if len(value) > 14 else "***"
            else:
                display_value = value
            print(f"   ✓ {var}: {display_value}")
            print(f"      → {description}")
        else:
            print(f"   ✗ {var}: NÃO CONFIGURADA")
            print(f"      → {description}")
            missing_required.append(var)
    
    # Variáveis opcionais
    print("\n📋 VARIÁVEIS OPCIONAIS:")
    for var, description in optional_vars.items():
        value = os.environ.get(var)
        if value:
            print(f"   ✓ {var}: {value}")
        else:
            print(f"   ○ {var}: não configurada (opcional)")
        print(f"      → {description}")
    
    # Railway auto-provided
    print("\n🚂 VARIÁVEIS RAILWAY (Auto-provided):")
    railway_vars = [
        'RAILWAY_ENVIRONMENT_NAME',
        'RAILWAY_PROJECT_NAME',
        'RAILWAY_SERVICE_NAME',
        'RAILWAY_PUBLIC_DOMAIN',
    ]
    for var in railway_vars:
        value = os.environ.get(var)
        if value:
            print(f"   ✓ {var}: {value}")
    
    print("\n" + "=" * 60)
    
    if missing_required:
        print(f"\n❌ ERRO: {len(missing_required)} variável(is) obrigatória(s) faltando:")
        for var in missing_required:
            print(f"   - {var}")
        return False
    else:
        print("\n✅ Todas as variáveis obrigatórias configuradas!")
        return True

def check_database_connection():
    """Verifica conexão com o banco de dados"""
    print("\n🗄️  Verificando Conexão com Banco de Dados\n")
    print("=" * 60)
    
    try:
        from config import Config
        database_url = Config.SQLALCHEMY_DATABASE_URI
        
        if not database_url:
            print("❌ DATABASE_URL não configurada")
            return False
        
        if database_url.startswith('postgresql://'):
            print("✅ PostgreSQL detectado (Railway)")
            # Mascarar URL
            parts = database_url.split('@')
            if len(parts) == 2:
                masked_url = f"{parts[0].split('://')[0]}://***@{parts[1]}"
                print(f"   URL: {masked_url}")
        elif database_url.startswith('sqlite://'):
            print("⚠️  SQLite detectado (desenvolvimento local)")
            print(f"   Path: {database_url}")
        
        # Tentar importar SQLAlchemy
        try:
            from sqlalchemy import create_engine, text
            engine = create_engine(database_url)
            
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                if result:
                    print("✅ Conexão com banco de dados OK!")
                    print("=" * 60)
                    return True
        except Exception as db_error:
            print(f"❌ Erro ao conectar: {str(db_error)}")
            print("=" * 60)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar configuração: {str(e)}")
        print("=" * 60)
        return False

def check_flask_app():
    """Verifica se a aplicação Flask está configurada corretamente"""
    print("\n🌐 Verificando Aplicação Flask\n")
    print("=" * 60)
    
    try:
        from app import app
        
        print(f"✅ App Flask carregado: {app.name}")
        print(f"   Debug Mode: {app.debug}")
        print(f"   Testing Mode: {app.testing}")
        
        # Verificar rotas
        routes_count = len([rule for rule in app.url_map.iter_rules()])
        print(f"   Total de Rotas: {routes_count}")
        
        # Verificar blueprints
        blueprints_count = len(app.blueprints)
        print(f"   Blueprints: {blueprints_count}")
        
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar Flask app: {str(e)}")
        print("=" * 60)
        return False

def check_static_files():
    """Verifica se os arquivos estáticos essenciais existem"""
    print("\n📁 Verificando Arquivos Estáticos\n")
    print("=" * 60)
    
    essential_files = [
        'static/css/custom.css',
        'static/js/custom.js',
        'templates/base.html',
        'templates/login.html',
    ]
    
    all_exist = True
    for file_path in essential_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NÃO ENCONTRADO")
            all_exist = False
    
    print("=" * 60)
    return all_exist

def check_responsive_layout():
    """Verifica se o layout responsivo está mantido"""
    print("\n📱 Verificando Layout Responsivo (Bootstrap)\n")
    print("=" * 60)
    
    try:
        # Verificar base.html
        base_template = 'templates/base.html'
        if os.path.exists(base_template):
            with open(base_template, 'r', encoding='utf-8') as f:
                content = f.read()
                
                checks = {
                    'Bootstrap CSS': 'bootstrap' in content.lower(),
                    'Viewport Meta': 'viewport' in content.lower(),
                    'Responsive Classes': 'container' in content or 'row' in content,
                    'Bootstrap JS': 'bootstrap.bundle' in content.lower() or 'bootstrap.min.js' in content.lower(),
                }
                
                all_ok = True
                for check_name, check_result in checks.items():
                    if check_result:
                        print(f"✅ {check_name}")
                    else:
                        print(f"⚠️  {check_name} - NÃO DETECTADO")
                        all_ok = False
                
                print("\n" + "=" * 60)
                return all_ok
        else:
            print(f"❌ {base_template} não encontrado")
            print("=" * 60)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar templates: {str(e)}")
        print("=" * 60)
        return False

def generate_report(results):
    """Gera relatório final da verificação"""
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL - RAILWAY HEALTH CHECK")
    print("=" * 60)
    print(f"\nData/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Sistema: VendaCerta v2.0")
    print(f"Plataforma: Railway\n")
    
    total_checks = len(results)
    passed_checks = sum(1 for r in results.values() if r)
    failed_checks = total_checks - passed_checks
    
    print(f"Total de Verificações: {total_checks}")
    print(f"✅ Aprovadas: {passed_checks}")
    print(f"❌ Falhadas: {failed_checks}")
    
    health_percentage = (passed_checks / total_checks) * 100
    print(f"\n🎯 Health Score: {health_percentage:.1f}%")
    
    if health_percentage == 100:
        status = "🟢 EXCELENTE - Pronto para produção"
    elif health_percentage >= 80:
        status = "🟡 BOM - Pequenos ajustes necessários"
    elif health_percentage >= 60:
        status = "🟠 ATENÇÃO - Correções recomendadas"
    else:
        status = "🔴 CRÍTICO - Correções necessárias"
    
    print(f"Status: {status}")
    
    print("\n" + "=" * 60)
    
    # Detalhamento
    print("\nDetalhamento por Categoria:\n")
    for check_name, check_result in results.items():
        icon = "✅" if check_result else "❌"
        print(f"{icon} {check_name}")
    
    print("\n" + "=" * 60)
    
    return health_percentage >= 80

def main():
    """Função principal de verificação"""
    print("\n" + "=" * 60)
    print("🚂 RAILWAY HEALTH CHECK - VENDACERTA v2.0")
    print("=" * 60)
    print("Verificação de compatibilidade e saúde do sistema\n")
    
    results = {
        'Variáveis de Ambiente': check_environment_variables(),
        'Conexão com Banco de Dados': check_database_connection(),
        'Aplicação Flask': check_flask_app(),
        'Arquivos Estáticos': check_static_files(),
        'Layout Responsivo': check_responsive_layout(),
    }
    
    success = generate_report(results)
    
    if success:
        print("\n✅ Sistema compatível com Railway!")
        print("🚀 Deploy pode prosseguir com segurança.\n")
        sys.exit(0)
    else:
        print("\n⚠️  Sistema requer ajustes antes do deploy.")
        print("📋 Revise os itens marcados com ❌ acima.\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
