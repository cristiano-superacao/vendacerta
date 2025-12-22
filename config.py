# config.py - Sistema VendaCerta
import os
from datetime import timedelta

# Obter o diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configurações base da aplicação VendaCerta"""

    # Chave secreta para sessões e CSRF (Railway: FLASK_SECRET_KEY)
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or os.environ.get('CHAVE_SECRETA') or 'dev-key-change-in-production-2025'

    # Força HTTPS em produção
    PREFERRED_URL_SCHEME = 'https'

    # ==========================================
    # 🔗 CONFIGURAÇÃO DATABASE_URL - INTERLIGAÇÃO COMPLETA DO SISTEMA
    # ==========================================
    # Prioridade:
    # 1. DATABASE_URL ou URL_DO_BANCO_DE_DADOS (se não vazia)
    # 2. Construção via variáveis PG* individuais (PGHOST, PGPORT, etc)
    # 3. SQLite local (fallback para desenvolvimento)
    
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('URL_DO_BANCO_DE_DADOS')
    
    # IMPORTANTE: Remove strings vazias (Railway pode retornar "" ao invés de None)
    if database_url:
        database_url = database_url.strip()
        if not database_url:  # String vazia após strip
            database_url = None
            print("[CONFIG] ⚠️  DATABASE_URL vazia detectada - sera construida via PG*")
    
    # Log para debug
    if database_url:
        # Mascara senha para segurança nos logs
        safe_url = database_url.split('@')[1] if '@' in database_url else 'local'
        print(f"[CONFIG] ✅ DATABASE_URL encontrada - Host: {safe_url.split('/')[0]}")
    else:
        print(f"[CONFIG] 🔧 DATABASE_URL nao encontrada, construindo via variaveis PG*...")
    
    # Constrói a partir das variáveis individuais do PostgreSQL (Railway sempre fornece)
    if not database_url:
        pgdatabase = os.environ.get('PGDATABASE')
        pghost = os.environ.get('PGHOST')
        pguser = os.environ.get('PGUSER')
        pgpassword = os.environ.get('PGPASSWORD')
        pgport = os.environ.get('PGPORT', '5432')
        
        if all([pgdatabase, pghost, pguser, pgpassword]):
            database_url = f'postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}'
            print(f"[CONFIG] ✅ URL construida via PG* variables")
            print(f"[CONFIG]    Host: {pghost}:{pgport}")
            print(f"[CONFIG]    Database: {pgdatabase}")
            print(f"[CONFIG]    User: {pguser}")
        else:
            print(f"[CONFIG] ❌ Variaveis PG* incompletas - PostgreSQL obrigatório")
            print(f"[CONFIG]    PGDATABASE: {'✅' if pgdatabase else '❌ FALTA'}")
            print(f"[CONFIG]    PGHOST: {'✅' if pghost else '❌ FALTA'}")
            print(f"[CONFIG]    PGUSER: {'✅' if pguser else '❌ FALTA'}")
            print(f"[CONFIG]    PGPASSWORD: {'✅' if pgpassword else '❌ FALTA'}")
            raise RuntimeError("CONFIG: Banco obrigatório PostgreSQL não configurado. Defina DATABASE_URL ou PG* (PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE).")

    # ==========================================
    # 🔧 NORMALIZAÇÃO E VALIDAÇÃO DA DATABASE_URL
    # ==========================================
    if database_url:
        # Fix para Heroku/Render/Railway: postgres:// -> postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
            print("[CONFIG] 🔧 Corrigido: postgres:// → postgresql://")
        
        # Valida formato básico
        if database_url.startswith('postgresql://'):
            print("[CONFIG] ✅ DATABASE_URL válida - PostgreSQL configurado")
        else:
            print(f"[CONFIG] ⚠️  DATABASE_URL com formato inesperado: {database_url[:20]}...")

    # Define URI final do SQLAlchemy (PostgreSQL obrigatório)
    if not database_url:
        raise RuntimeError("CONFIG: DATABASE_URL não definida e não foi possível construir via PG*. Configure o PostgreSQL.")
    SQLALCHEMY_DATABASE_URI = database_url
    print("[CONFIG] 🚀 Sistema configurado para PostgreSQL (PRODUÇÃO)")

    # Configuração de Múltiplos Bancos (Binds) para Modularização
    # Permite separar dados em bancos diferentes ou usar o mesmo banco (default)
    SQLALCHEMY_BINDS = {
        'auth': os.environ.get('DATABASE_URL_AUTH') or SQLALCHEMY_DATABASE_URI,
        'vendas': os.environ.get('DATABASE_URL_VENDAS') or SQLALCHEMY_DATABASE_URI,
        'clientes': os.environ.get('DATABASE_URL_CLIENTES') or SQLALCHEMY_DATABASE_URI,
        'estoque': os.environ.get('DATABASE_URL_ESTOQUE') or SQLALCHEMY_DATABASE_URI,
        'servicos': os.environ.get('DATABASE_URL_SERVICOS') or SQLALCHEMY_DATABASE_URI,
        'comunicacao': os.environ.get('DATABASE_URL_COMUNICACAO') or SQLALCHEMY_DATABASE_URI
    }

    # Desabilita rastreamento de modificações (economiza memória)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações otimizadas para Railway PostgreSQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,           # Verifica conexão antes de usar
        'pool_recycle': 280,             # Recicla conexões a cada 4:40min (antes do timeout de 5min)
        'pool_size': 5,                  # Pool menor para Railway (otimizado)
        'max_overflow': 10,              # Overflow reduzido
        'pool_timeout': 30,              # Timeout para obter conexão do pool
        'connect_args': {
            'connect_timeout': 10,       # Timeout de conexão PostgreSQL
            'options': '-c statement_timeout=30000'  # 30s timeout para queries
        }
    }

    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True  # HTTPS habilitado em produção
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Configurações do Flask-WTF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # Token CSRF não expira

    # Configurações de paginação
    ITEMS_PER_PAGE = 10

    # Configurações de upload (se necessário no futuro)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

    # Timezone
    TIMEZONE = 'America/Sao_Paulo'

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    TESTING = False
    PREFERRED_URL_SCHEME = 'http'  # HTTP em desenvolvimento
    SESSION_COOKIE_SECURE = False  # Permite HTTP em dev

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Requer HTTPS

    # Em produção, SECRET_KEY DEVE vir de variável de ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.environ.get('FLASK_SECRET_KEY') or 'prod-key-change-me'

    # DATABASE_URL já configurado na classe Config base
    # Não precisa reconfigurar aqui

class TestingConfig(Config):
    """Configurações para testes"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
