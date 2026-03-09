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
    #    (Opcional) Se PREFER_DATABASE_PUBLIC_URL=1 e DATABASE_PUBLIC_URL existir,
    #    usa a URL pública primeiro (útil para executar scripts via `railway run` local).
    # 2. Construção via variáveis PG* individuais (PGHOST, PGPORT, etc)
    # 3. SQLite local (fallback para desenvolvimento)
    
    prefer_public = os.environ.get('PREFER_DATABASE_PUBLIC_URL', '0') == '1'
    database_url = None

    if prefer_public and os.environ.get('DATABASE_PUBLIC_URL'):
        database_url = os.environ.get('DATABASE_PUBLIC_URL')
    else:
        database_url = os.environ.get('DATABASE_URL') or os.environ.get('URL_DO_BANCO_DE_DADOS')
    
    # IMPORTANTE: Remove strings vazias (Railway pode retornar "" ao invés de None)
    if database_url:
        database_url = database_url.strip()
        if not database_url:  # String vazia após strip
            database_url = None
            print("[CONFIG] ⚠️  DATABASE_URL vazia detectada - sera construida via PG*")
    
    # Log para debug (sem emojis para evitar problemas de encoding em alguns ambientes)
    if database_url:
        # Mascara senha para segurança nos logs
        safe_url = database_url.split('@')[1] if '@' in database_url else 'local'
        print(f"[CONFIG] DATABASE_URL encontrada - Host: {safe_url.split('/')[0]}")
    else:
        print("[CONFIG] DATABASE_URL nao encontrada, construindo via variaveis PG*...")
    
    # Constrói a partir das variáveis individuais do PostgreSQL (Railway sempre fornece)
    if not database_url:
        pgdatabase = os.environ.get('PGDATABASE')
        pghost = os.environ.get('PGHOST')
        pguser = os.environ.get('PGUSER')
        pgpassword = os.environ.get('PGPASSWORD')
        pgport = os.environ.get('PGPORT', '5432')
        
        if all([pgdatabase, pghost, pguser, pgpassword]):
            database_url = f'postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}'
            print("[CONFIG] URL construida via PG* variables")
            print(f"[CONFIG]    Host: {pghost}:{pgport}")
            print(f"[CONFIG]    Database: {pgdatabase}")
            print(f"[CONFIG]    User: {pguser}")
        else:
            print("[CONFIG] Variaveis PG* incompletas - PostgreSQL obrigatório")
            print(f"[CONFIG]    PGDATABASE: {'OK' if pgdatabase else 'FALTA'}")
            print(f"[CONFIG]    PGHOST: {'OK' if pghost else 'FALTA'}")
            print(f"[CONFIG]    PGUSER: {'OK' if pguser else 'FALTA'}")
            print(f"[CONFIG]    PGPASSWORD: {'OK' if pgpassword else 'FALTA'}")
            # Não interrompa o import aqui: o fallback SQLite pode estar habilitado
            # via ALLOW_SQLITE_DEV=1 ou FLASK_ENV=testing.
            database_url = None

    # ==========================================
    # 🔧 NORMALIZAÇÃO E VALIDAÇÃO DA DATABASE_URL
    # ==========================================
    if database_url:
        # Fix para Heroku/Render/Railway: postgres:// -> postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
            print("[CONFIG] Corrigido: postgres:// -> postgresql://")
        
        # Valida formato básico
        if database_url.startswith('postgresql://'):
            print("[CONFIG] DATABASE_URL válida - PostgreSQL configurado")
        else:
            print(f"[CONFIG] DATABASE_URL com formato inesperado: {database_url[:20]}...")

    # Define URI final do SQLAlchemy
    allow_sqlite_dev = os.environ.get('ALLOW_SQLITE_DEV', '0') == '1' or os.environ.get('FLASK_ENV') == 'testing'
    if not database_url:
        if allow_sqlite_dev:
            # Fallback seguro para desenvolvimento/testes locais
            SQLALCHEMY_DATABASE_URI = 'sqlite:///vendacerta_dev.db'
            print("[CONFIG] Fallback SQLite habilitado para desenvolvimento/testes")
        else:
            raise RuntimeError("CONFIG: DATABASE_URL não definida e não foi possível construir via PG*. Configure o PostgreSQL.")
    else:
        SQLALCHEMY_DATABASE_URI = database_url
        print("[CONFIG] Sistema configurado para PostgreSQL (PRODUÇÃO)")

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

    # Configurações do engine conforme o tipo de banco
    if SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
        # Opções seguras para SQLite (evita connect_args inválido)
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,
        }
    else:
        # Otimizações para PostgreSQL (Railway/produção)
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,
            'pool_recycle': 280,
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 30,
            'connect_args': {
                'connect_timeout': 10,
                'options': '-c statement_timeout=30000'
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
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB max
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
