# test_local.py
"""
Script para testar o sistema localmente antes do deploy
Verifica todas as funcionalidades principais
"""

import os
import unittest


if os.getenv("RUN_INTEGRATION_TESTS") != "1":
    raise unittest.SkipTest(
        "Teste de integração local (depende de app/banco). "
        "Defina RUN_INTEGRATION_TESTS=1 para executar."
    )

from app import app, db
from models import Usuario, Vendedor, Cliente, Meta, Equipe
from datetime import datetime
import sys

def test_database_connection():
    """Testa conexão com o banco de dados"""
    print("\n📊 Testando conexão com banco de dados...")
    try:
        with app.app_context():
            # Tentar query simples
            count = Usuario.query.count()
            print(f"✅ Conexão OK - {count} usuários no banco")
            return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_models():
    """Testa os modelos do banco"""
    print("\n🔍 Testando modelos...")
    try:
        with app.app_context():
            # Testar cada modelo
            modelos = {
                'Usuario': Usuario.query.count(),
                'Vendedor': Vendedor.query.count(),
                'Cliente': Cliente.query.count(),
                'Meta': Meta.query.count(),
                'Equipe': Equipe.query.count(),
            }
            
            print("✅ Todos os modelos acessíveis:")
            for modelo, count in modelos.items():
                print(f"   • {modelo}: {count} registros")
            return True
    except Exception as e:
        print(f"❌ Erro nos modelos: {e}")
        return False

def test_routes():
    """Testa rotas principais"""
    print("\n🌐 Testando rotas principais...")
    
    rotas_teste = [
        ('/', 'Dashboard'),
        ('/login', 'Login'),
        ('/clientes', 'Lista de Clientes'),
        ('/vendedores', 'Lista de Vendedores'),
        ('/metas', 'Lista de Metas'),
    ]
    
    with app.test_client() as client:
        sucesso = 0
        erros = 0
        
        for rota, nome in rotas_teste:
            try:
                response = client.get(rota, follow_redirects=True)
                if response.status_code in [200, 302]:
                    print(f"✅ {nome}: OK ({response.status_code})")
                    sucesso += 1
                else:
                    print(f"⚠️  {nome}: {response.status_code}")
                    erros += 1
            except Exception as e:
                print(f"❌ {nome}: Erro - {e}")
                erros += 1
        
        print(f"\n📊 Resultado: {sucesso} OK, {erros} erros")
        return erros == 0

def test_cliente_form():
    """Testa formulário de clientes"""
    print("\n📝 Testando formulário de clientes...")
    
    with app.test_client() as client:
        # Fazer login primeiro (necessário para acessar rotas protegidas)
        # Nota: Esta é uma verificação básica, não testa login completo
        try:
            response = client.get('/clientes/novo', follow_redirects=True)
            if response.status_code == 200:
                print("✅ Formulário de novo cliente acessível")
                return True
            else:
                print(f"⚠️  Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

def test_backup_system():
    """Testa sistema de backup"""
    print("\n💾 Testando sistema de backup...")
    
    import os
    
    try:
        with app.app_context():
            backup_dir = os.path.join(app.instance_path, 'backups')
            
            if os.path.exists(backup_dir):
                backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
                print(f"✅ Pasta de backups existe: {len(backups)} backups encontrados")
                
                # Mostrar backups com data real
                for backup in backups[:5]:  # Mostrar apenas os 5 primeiros
                    filepath = os.path.join(backup_dir, backup)
                    stat = os.stat(filepath)
                    data = datetime.fromtimestamp(stat.st_mtime)
                    tamanho_kb = round(stat.st_size / 1024, 2)
                    print(f"   • {backup}")
                    print(f"     Data: {data.strftime('%d/%m/%Y às %H:%M:%S')}")
                    print(f"     Tamanho: {tamanho_kb} KB")
                
                return True
            else:
                print("⚠️  Pasta de backups não existe (será criada quando necessário)")
                return True
    except Exception as e:
        print(f"❌ Erro no sistema de backup: {e}")
        return False

def test_imports():
    """Testa imports necessários"""
    print("\n📦 Testando imports...")
    
    imports_ok = True
    
    # Testar Flask-Compress
    try:
        from flask_compress import Compress
        print("✅ Flask-Compress instalado")
    except ImportError:
        print("⚠️  Flask-Compress não instalado (opcional)")
        print("   Instale com: pip install flask-compress")
    
    # Testar outras dependências importantes
    dependencias = [
        ('sqlalchemy', 'SQLAlchemy'),
        ('flask_login', 'Flask-Login'),
        ('wtforms', 'WTForms'),
        ('reportlab', 'ReportLab'),
        ('pandas', 'Pandas'),
        ('openpyxl', 'OpenPyXL'),
    ]
    
    for modulo, nome in dependencias:
        try:
            __import__(modulo)
            print(f"✅ {nome} instalado")
        except ImportError:
            print(f"❌ {nome} NÃO instalado")
            imports_ok = False
    
    return imports_ok

def run_all_tests():
    """Executa todos os testes"""
    print("=" * 70)
    print("🧪 TESTE LOCAL DO SISTEMA VENDACERTA")
    print("=" * 70)
    print(f"\n🕐 Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
    
    resultados = {}
    
    # Executar testes
    resultados['Imports'] = test_imports()
    resultados['Banco de Dados'] = test_database_connection()
    resultados['Modelos'] = test_models()
    resultados['Rotas'] = test_routes()
    resultados['Formulário Clientes'] = test_cliente_form()
    resultados['Sistema Backup'] = test_backup_system()
    
    # Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO DOS TESTES")
    print("=" * 70)
    
    sucesso = sum(1 for v in resultados.values() if v)
    total = len(resultados)
    
    for teste, resultado in resultados.items():
        icone = "✅" if resultado else "❌"
        print(f"{icone} {teste}")
    
    print("\n" + "=" * 70)
    percentual = (sucesso / total) * 100
    print(f"🎯 Resultado Final: {sucesso}/{total} testes OK ({percentual:.0f}%)")
    
    if percentual == 100:
        print("✅ SISTEMA PRONTO PARA USO!")
    elif percentual >= 80:
        print("⚠️  Sistema funcional com algumas ressalvas")
    else:
        print("❌ Sistema precisa de correções")
    
    print("=" * 70 + "\n")
    
    return percentual >= 80

if __name__ == '__main__':
    sucesso = run_all_tests()
    
    if sucesso:
        print("\n🚀 Você pode iniciar o servidor com:")
        print("   python app.py")
        print("\n🌐 Acesse: http://127.0.0.1:5001")
        sys.exit(0)
    else:
        print("\n⚠️  Corrija os erros antes de iniciar o servidor")
        sys.exit(1)
