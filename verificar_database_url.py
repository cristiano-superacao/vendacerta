#!/usr/bin/env python3
"""
🔗 Verificador de DATABASE_URL - Sistema VendaCerta
Verifica e valida a interligação completa do sistema com o banco de dados
"""

import os
import sys
from urllib.parse import urlparse

def verificar_variaveis_ambiente():
    """Verifica todas as variáveis de ambiente relacionadas ao banco"""
    print("\n" + "="*70)
    print("🔍 VERIFICAÇÃO DE VARIÁVEIS DE AMBIENTE")
    print("="*70)
    
    variaveis = {
        'DATABASE_URL': os.environ.get('DATABASE_URL'),
        'URL_DO_BANCO_DE_DADOS': os.environ.get('URL_DO_BANCO_DE_DADOS'),
        'PGDATABASE': os.environ.get('PGDATABASE'),
        'PGHOST': os.environ.get('PGHOST'),
        'PGPORT': os.environ.get('PGPORT'),
        'PGUSER': os.environ.get('PGUSER'),
        'PGPASSWORD': os.environ.get('PGPASSWORD'),
        'DATABASE_PUBLIC_URL': os.environ.get('DATABASE_PUBLIC_URL'),
    }
    
    for nome, valor in variaveis.items():
        if valor:
            # Mascara senha para segurança
            if 'PASSWORD' in nome or 'URL' in nome:
                if '@' in str(valor):
                    partes = valor.split('@')
                    valor_safe = f"***@{partes[1]}"
                else:
                    valor_safe = "***"
            else:
                valor_safe = valor
            print(f"✅ {nome:25} = {valor_safe}")
        else:
            print(f"❌ {nome:25} = (não configurada)")
    
    return variaveis

def construir_database_url(variaveis):
    """Constrói DATABASE_URL seguindo a mesma lógica do config.py"""
    print("\n" + "="*70)
    print("🔧 CONSTRUÇÃO DA DATABASE_URL")
    print("="*70)
    
    database_url = variaveis.get('DATABASE_URL') or variaveis.get('URL_DO_BANCO_DE_DADOS')
    
    # Remove strings vazias
    if database_url:
        database_url = database_url.strip()
        if not database_url:
            database_url = None
            print("⚠️  DATABASE_URL está vazia - será construída via PG*")
    
    if database_url:
        print(f"✅ DATABASE_URL encontrada diretamente")
        if '@' in database_url:
            host = database_url.split('@')[1].split('/')[0]
            print(f"   Host: {host}")
    else:
        print("🔧 Construindo DATABASE_URL a partir de variáveis PG*...")
        
        pgdatabase = variaveis.get('PGDATABASE')
        pghost = variaveis.get('PGHOST')
        pguser = variaveis.get('PGUSER')
        pgpassword = variaveis.get('PGPASSWORD')
        pgport = variaveis.get('PGPORT', '5432')
        
        if all([pgdatabase, pghost, pguser, pgpassword]):
            database_url = f'postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}'
            print(f"✅ URL construída com sucesso!")
            print(f"   Host: {pghost}:{pgport}")
            print(f"   Database: {pgdatabase}")
            print(f"   User: {pguser}")
        else:
            print("❌ Variáveis PG* incompletas!")
            print(f"   PGDATABASE: {'✅' if pgdatabase else '❌'}")
            print(f"   PGHOST: {'✅' if pghost else '❌'}")
            print(f"   PGUSER: {'✅' if pguser else '❌'}")
            print(f"   PGPASSWORD: {'✅' if pgpassword else '❌'}")
            return None
    
    # Normaliza postgres:// para postgresql://
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
        print("🔧 Normalizado: postgres:// → postgresql://")
    
    return database_url

def validar_database_url(database_url):
    """Valida o formato da DATABASE_URL"""
    print("\n" + "="*70)
    print("✅ VALIDAÇÃO DA DATABASE_URL")
    print("="*70)
    
    if not database_url:
        print("❌ DATABASE_URL não está configurada! (PostgreSQL é obrigatório)")
        print("\n💡 SOLUÇÃO:")
        print("   1. Configure DATABASE_URL diretamente no Railway:")
        print("      railway variables --set DATABASE_URL='postgresql://...'"
        )
        print("   2. OU garanta que todas as variáveis PG* estejam configuradas")
        return False
    
    try:
        parsed = urlparse(database_url)
        
        print(f"✅ Formato válido!")
        print(f"   Protocolo: {parsed.scheme}")
        print(f"   Host: {parsed.hostname}")
        print(f"   Porta: {parsed.port}")
        print(f"   Database: {parsed.path.lstrip('/')}")
        print(f"   Usuário: {parsed.username}")
        
        if parsed.scheme == 'postgresql':
            print("\n✅ PostgreSQL configurado - PRODUÇÃO")
        else:
            print(f"\n❌ Protocolo inválido para o sistema: {parsed.scheme} (esperado: postgresql)")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro ao validar URL: {e}")
        return False

def testar_conexao(database_url):
    """Testa a conexão com o banco de dados"""
    print("\n" + "="*70)
    print("🔌 TESTE DE CONEXÃO")
    print("="*70)
    
    if not database_url:
        print("❌ Não é possível testar - DATABASE_URL não configurada")
        return False
    
    try:
        from sqlalchemy import create_engine, text
        
        # Configurações de teste
        engine_options = {
            'pool_pre_ping': True,
            'connect_args': {
                'connect_timeout': 10,
                'options': '-c statement_timeout=30000'
            }
        }
        
        print("🔄 Criando engine SQLAlchemy...")
        engine = create_engine(database_url, **engine_options)
        
        print("🔄 Testando conexão...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        
        print("✅ Conexão bem-sucedida!")
        
        # Testa listagem de tabelas
        print("\n🔄 Listando tabelas...")
        with engine.connect() as conn:
            query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            
            result = conn.execute(query)
            tabelas = [row[0] for row in result]
        
        if tabelas:
            print(f"✅ Encontradas {len(tabelas)} tabelas:")
            for tabela in tabelas[:10]:  # Mostra até 10 tabelas
                print(f"   • {tabela}")
            if len(tabelas) > 10:
                print(f"   ... e mais {len(tabelas) - 10} tabelas")
        else:
            print("⚠️  Nenhuma tabela encontrada (banco vazio)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        print(f"\n💡 Possíveis causas:")
        print("   • Host não acessível (postgres.railway.internal só funciona no Railway)")
        print("   • Credenciais incorretas")
        print("   • Banco de dados não existe")
        print("   • Firewall bloqueando conexão")
        return False

def verificar_config_py():
    """Verifica se o config.py está usando a DATABASE_URL corretamente"""
    print("\n" + "="*70)
    print("📄 VERIFICAÇÃO DO config.py")
    print("="*70)
    
    try:
        from config import Config
        
        print("✅ config.py importado com sucesso")
        
        uri = Config.SQLALCHEMY_DATABASE_URI
        if 'postgresql' in uri:
            print("✅ Config usando PostgreSQL")
        else:
            print(f"❌ Config inválida: esperado PostgreSQL. URI: {uri}")
            return False
        
        # Verifica engine options
        if hasattr(Config, 'SQLALCHEMY_ENGINE_OPTIONS'):
            options = Config.SQLALCHEMY_ENGINE_OPTIONS
            print(f"\n✅ Engine options configuradas:")
            print(f"   pool_size: {options.get('pool_size', 'padrão')}")
            print(f"   pool_recycle: {options.get('pool_recycle', 'padrão')}")
            print(f"   pool_pre_ping: {options.get('pool_pre_ping', 'padrão')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao importar config.py: {e}")
        return False

def main():
    """Executa verificação completa"""
    print("\n" + "="*70)
    print("🔗 VERIFICADOR DE DATABASE_URL - SISTEMA VENDACERTA")
    print("="*70)
    
    # 1. Verificar variáveis de ambiente
    variaveis = verificar_variaveis_ambiente()
    
    # 2. Construir DATABASE_URL
    database_url = construir_database_url(variaveis)
    
    # 3. Validar DATABASE_URL
    url_valida = validar_database_url(database_url)
    
    # 4. Testar conexão (se URL válida)
    if url_valida:
        conexao_ok = testar_conexao(database_url)
    else:
        conexao_ok = False
    
    # 5. Verificar config.py
    config_ok = verificar_config_py()
    
    # Resumo final
    print("\n" + "="*70)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("="*70)
    print(f"{'✅' if variaveis.get('DATABASE_URL') or all([variaveis.get('PGDATABASE'), variaveis.get('PGHOST'), variaveis.get('PGUSER'), variaveis.get('PGPASSWORD')]) else '❌'} Variáveis de ambiente (PostgreSQL)")
    print(f"{'✅' if url_valida else '❌'} DATABASE_URL válida (postgresql)")
    print(f"{'✅' if conexao_ok else '❌'} Conexão com banco (PostgreSQL)")
    print(f"{'✅' if config_ok else '❌'} Configuração do sistema (PostgreSQL)")
    
    if all([url_valida, config_ok]):
        print("\n🎉 SISTEMA TOTALMENTE INTERLIGADO E FUNCIONAL!")
        return 0
    else:
        print("\n⚠️  Sistema precisa de ajustes - veja os erros acima")
        return 1

if __name__ == '__main__':
    sys.exit(main())
