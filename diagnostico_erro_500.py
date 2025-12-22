"""
Diagnostico completo do erro 500 no Railway
"""
import os
import sys

print("\n" + "="*80)
print("DIAGNOSTICO DO ERRO 500 - RAILWAY")
print("="*80)

# 1. Verificar variaveis de ambiente
print("\n1. VARIAVEIS DE AMBIENTE:")
print("-" * 80)

variaveis_importantes = [
    'DATABASE_URL', 'DATABASE_PUBLIC_URL', 
    'PGHOST', 'PGPORT', 'PGUSER', 'PGDATABASE',
    'FLASK_SECRET_KEY', 'PORT', 'RAILWAY_ENVIRONMENT'
]

for var in variaveis_importantes:
    valor = os.getenv(var)
    if valor:
        if 'PASSWORD' in var or 'SECRET' in var:
            print(f"  {var}: ***oculto***")
        else:
            print(f"  {var}: {valor}")
    else:
        print(f"  {var}: NAO DEFINIDA")

# 2. Testar importacao do app
print("\n2. TESTE DE IMPORTACAO:")
print("-" * 80)

try:
    print("  Tentando importar app...")
    from app import app, db
    print("  ✓ App importado com sucesso!")
    
    # Verificar config
    print(f"\n  Config do app:")
    print(f"    DEBUG: {app.config.get('DEBUG')}")
    print(f"    TESTING: {app.config.get('TESTING')}")
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if 'postgresql' in db_uri:
        print(f"    DATABASE: PostgreSQL")
    elif 'sqlite' in db_uri:
        print(f"    DATABASE: SQLite")
    else:
        print(f"    DATABASE: Desconhecido")
        
except Exception as e:
    print(f"  X ERRO ao importar app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 3. Testar conexao com banco
print("\n3. TESTE DE CONEXAO COM BANCO:")
print("-" * 80)

try:
    with app.app_context():
        # Tentar uma query simples
        from sqlalchemy import text
        result = db.session.execute(text("SELECT 1"))
        print("  ✓ Conexao com banco OK!")
        
        # Verificar tabelas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tabelas = inspector.get_table_names()
        print(f"  ✓ Tabelas encontradas: {len(tabelas)}")
        print(f"    {', '.join(tabelas[:5])}{'...' if len(tabelas) > 5 else ''}")
        
except Exception as e:
    print(f"  X ERRO na conexao: {e}")
    import traceback
    traceback.print_exc()

# 4. Testar rotas principais
print("\n4. TESTE DE ROTAS:")
print("-" * 80)

try:
    with app.test_client() as client:
        # Testar rota raiz
        print("  Testando GET /...")
        response = client.get('/')
        print(f"    Status: {response.status_code}")
        if response.status_code != 200:
            print(f"    ERRO! Status esperado: 200")
            if response.status_code == 500:
                print(f"    Resposta: {response.data[:200]}")
        else:
            print(f"    ✓ Rota / OK!")
            
        # Testar login
        print("\n  Testando GET /login...")
        response = client.get('/login')
        print(f"    Status: {response.status_code}")
        if response.status_code == 200:
            print(f"    ✓ Rota /login OK!")
            
except Exception as e:
    print(f"  X ERRO ao testar rotas: {e}")
    import traceback
    traceback.print_exc()

# 5. Verificar modelos
print("\n5. VERIFICACAO DE MODELOS:")
print("-" * 80)

try:
    from models import Vendedor, Cliente, Meta
    print("  ✓ Modelos importados com sucesso")
    
    with app.app_context():
        # Contar registros
        print(f"  Vendedores: {Vendedor.query.count()}")
        print(f"  Clientes: {Cliente.query.count()}")
        print(f"  Metas: {Meta.query.count()}")
        
except Exception as e:
    print(f"  X ERRO com modelos: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("DIAGNOSTICO CONCLUIDO")
print("="*80 + "\n")
