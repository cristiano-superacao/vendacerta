#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Configuração PostgreSQL - Sistema VendaCerta
Cria banco de dados, usuário e estrutura inicial para o PostgreSQL
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configurações do PostgreSQL
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'admin_user': 'postgres',  # Usuário admin padrão do PostgreSQL
    'admin_password': '',  # Será solicitado
    'db_name': 'vendacerta_db',
    'db_user': 'vendacerta_user',
    'db_password': 'vendacerta_pass'
}

def print_header(texto):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {texto}")
    print("=" * 70)

def print_step(numero, texto):
    """Imprime passo numerado"""
    print(f"\n[{numero}] {texto}")

def conectar_postgres_admin():
    """Conecta ao PostgreSQL como administrador"""
    try:
        print("[PROC] Conectando ao PostgreSQL como administrador...")
        
        # Solicita senha do admin se não fornecida
        if not POSTGRES_CONFIG['admin_password']:
            import getpass
            POSTGRES_CONFIG['admin_password'] = getpass.getpass(
                f"Digite a senha do usuário '{POSTGRES_CONFIG['admin_user']}': "
            )
        
        conn = psycopg2.connect(
            host=POSTGRES_CONFIG['host'],
            port=POSTGRES_CONFIG['port'],
            user=POSTGRES_CONFIG['admin_user'],
            password=POSTGRES_CONFIG['admin_password'],
            database='postgres'  # Conecta ao DB padrão
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print("[OK] Conectado ao PostgreSQL com sucesso!")
        return conn
    except psycopg2.Error as e:
        print(f"[ERRO] Erro ao conectar ao PostgreSQL: {e}")
        sys.exit(1)

def verificar_usuario_existe(cursor, usuario):
    """Verifica se usuário já existe"""
    cursor.execute(
        "SELECT 1 FROM pg_roles WHERE rolname = %s",
        (usuario,)
    )
    return cursor.fetchone() is not None

def verificar_banco_existe(cursor, banco):
    """Verifica se banco de dados já existe"""
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (banco,)
    )
    return cursor.fetchone() is not None

def criar_usuario(cursor):
    """Cria usuário do banco de dados"""
    print_step(1, "Criando usuário do banco de dados")
    
    usuario = POSTGRES_CONFIG['db_user']
    senha = POSTGRES_CONFIG['db_password']
    
    if verificar_usuario_existe(cursor, usuario):
        print(f"[AVISO]  Usuário '{usuario}' já existe. Atualizando senha...")
        cursor.execute(
            sql.SQL("ALTER USER {} WITH PASSWORD %s").format(
                sql.Identifier(usuario)
            ),
            (senha,)
        )
    else:
        print(f"[PROC] Criando usuário '{usuario}'...")
        cursor.execute(
            sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
                sql.Identifier(usuario)
            ),
            (senha,)
        )
    
    print(f"[OK] Usuário '{usuario}' configurado com sucesso!")

def criar_banco(cursor):
    """Cria banco de dados"""
    print_step(2, "Criando banco de dados")
    
    banco = POSTGRES_CONFIG['db_name']
    usuario = POSTGRES_CONFIG['db_user']
    
    if verificar_banco_existe(cursor, banco):
        print(f"[AVISO]  Banco '{banco}' já existe.")
        resposta = input("Deseja recriar o banco? (isso apagará todos os dados) [s/N]: ")
        if resposta.lower() == 's':
            print(f"[PROC] Removendo banco '{banco}'...")
            # Encerra conexões ativas
            cursor.execute(
                sql.SQL("""
                    SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = %s
                    AND pid <> pg_backend_pid()
                """),
                (banco,)
            )
            cursor.execute(
                sql.SQL("DROP DATABASE {}").format(sql.Identifier(banco))
            )
            print(f"[OK] Banco '{banco}' removido!")
        else:
            print("[NEXT]  Mantendo banco existente.")
            return
    
    print(f"[PROC] Criando banco '{banco}'...")
    cursor.execute(
        sql.SQL("CREATE DATABASE {} OWNER {}").format(
            sql.Identifier(banco),
            sql.Identifier(usuario)
        )
    )
    print(f"[OK] Banco '{banco}' criado com sucesso!")

def configurar_permissoes(cursor):
    """Configura permissões do usuário"""
    print_step(3, "Configurando permissões")
    
    usuario = POSTGRES_CONFIG['db_user']
    banco = POSTGRES_CONFIG['db_name']
    
    print(f"[PROC] Concedendo permissões para '{usuario}' em '{banco}'...")
    
    # Concede privilégios no banco
    cursor.execute(
        sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
            sql.Identifier(banco),
            sql.Identifier(usuario)
        )
    )
    
    print(f"[OK] Permissões configuradas com sucesso!")

def gerar_env_file():
    """Gera arquivo .env com configurações"""
    print_step(4, "Gerando configuração .env")
    
    host = POSTGRES_CONFIG['host']
    port = POSTGRES_CONFIG['port']
    banco = POSTGRES_CONFIG['db_name']
    usuario = POSTGRES_CONFIG['db_user']
    senha = POSTGRES_CONFIG['db_password']
    
    database_url = f"postgresql://{usuario}:{senha}@{host}:{port}/{banco}"
    
    env_content = f"""# Configuração PostgreSQL - Sistema VendaCerta
# Gerado automaticamente por setup_postgresql.py

# Chave Secreta (altere em produção)
FLASK_SECRET_KEY=dev-key-local-testing-2025

# Ambiente de desenvolvimento
FLASK_ENV=development
FLASK_DEBUG=True

# Banco de dados PostgreSQL
DATABASE_URL={database_url}

# Ou configure usando variáveis individuais:
PGDATABASE={banco}
PGHOST={host}
PGPORT={port}
PGUSER={usuario}
PGPASSWORD={senha}

# Configurações opcionais
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
"""
    
    # Backup do .env existente
    if os.path.exists('.env'):
        print("[PROC] Fazendo backup do .env existente...")
        os.rename('.env', '.env.backup')
        print("[OK] Backup salvo como .env.backup")
    
    # Cria novo .env
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("[OK] Arquivo .env atualizado com configurações PostgreSQL!")
    print(f"\n📋 String de conexão: {database_url}")

def testar_conexao():
    """Testa conexão com o banco criado"""
    print_step(5, "Testando conexão com o banco de dados")
    
    try:
        print("[PROC] Conectando ao banco de dados...")
        conn = psycopg2.connect(
            host=POSTGRES_CONFIG['host'],
            port=POSTGRES_CONFIG['port'],
            user=POSTGRES_CONFIG['db_user'],
            password=POSTGRES_CONFIG['db_password'],
            database=POSTGRES_CONFIG['db_name']
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        versao = cursor.fetchone()[0]
        
        print("[OK] Conexão bem-sucedida!")
        print(f"[INFO] Versão do PostgreSQL: {versao}")
        
        cursor.close()
        conn.close()
        
        return True
    except psycopg2.Error as e:
        print(f"[ERRO] Erro ao conectar ao banco: {e}")
        return False

def main():
    """Função principal"""
    print_header("CONFIGURAÇÃO POSTGRESQL - SISTEMA VENDACERTA")
    
    print("\n📋 Configurações:")
    print(f"   • Host: {POSTGRES_CONFIG['host']}")
    print(f"   • Port: {POSTGRES_CONFIG['port']}")
    print(f"   • Banco de dados: {POSTGRES_CONFIG['db_name']}")
    print(f"   • Usuário: {POSTGRES_CONFIG['db_user']}")
    
    resposta = input("\n🤔 Deseja continuar com estas configurações? [S/n]: ")
    if resposta.lower() == 'n':
        print("[ERRO] Configuração cancelada pelo usuário.")
        sys.exit(0)
    
    # Conecta como administrador
    conn = conectar_postgres_admin()
    cursor = conn.cursor()
    
    try:
        # Executa passos de configuração
        criar_usuario(cursor)
        criar_banco(cursor)
        configurar_permissoes(cursor)
        
        cursor.close()
        conn.close()
        
        # Gera arquivo .env
        gerar_env_file()
        
        # Testa conexão
        if testar_conexao():
            print_header("CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
            print("\n[OK] Próximos passos:")
            print("   1. Revise o arquivo .env gerado")
            print("   2. Execute: python migrate_to_postgresql.py (para migrar dados do SQLite)")
            print("   3. Execute: python app.py (para iniciar o sistema)")
            print("\n" + "=" * 70)
        else:
            print("\n[AVISO]  Configuração criada, mas houve erro na conexão.")
            print("   Verifique as configurações e tente novamente.")
    
    except Exception as e:
        print(f"\n[ERRO] Erro durante a configuração: {e}")
        cursor.close()
        conn.close()
        sys.exit(1)

if __name__ == '__main__':
    main()
