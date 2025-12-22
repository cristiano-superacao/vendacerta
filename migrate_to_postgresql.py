#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Migração SQLite -> PostgreSQL - Sistema VendaCerta
Migra todos os dados do banco SQLite para PostgreSQL preservando integridade
"""

import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

def print_header(texto):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {texto}")
    print("=" * 70)

def print_step(numero, texto):
    """Imprime passo numerado"""
    print(f"\n[{numero}] {texto}")

def get_sqlite_uri():
    """Retorna URI do banco SQLite"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    sqlite_path = os.path.join(basedir, 'instance', 'vendacerta.db')
    
    if not os.path.exists(sqlite_path):
        print(f"[ERRO] Banco SQLite não encontrado em: {sqlite_path}")
        return None
    
    return f'sqlite:///{sqlite_path}'

def get_postgresql_uri():
    """Retorna URI do banco PostgreSQL do .env"""
    from dotenv import load_dotenv
    load_dotenv()
    
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("[ERRO] DATABASE_URL não configurada no arquivo .env")
        print("   Execute primeiro: python setup_postgresql.py")
        return None
    
    # Fix postgres:// -> postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url

def criar_backup_sqlite():
    """Cria backup do banco SQLite"""
    import shutil
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    sqlite_path = os.path.join(basedir, 'instance', 'vendacerta.db')
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(basedir, 'instance', f'vendacerta_backup_{timestamp}.db')
    
    print("[PROC] Criando backup do SQLite...")
    shutil.copy2(sqlite_path, backup_path)
    print(f"[OK] Backup criado: {backup_path}")
    
    return backup_path

def listar_tabelas(engine):
    """Lista todas as tabelas do banco"""
    inspector = inspect(engine)
    return inspector.get_table_names()

def migrar_tabela(nome_tabela, engine_origem, engine_destino, session_origem, session_destino):
    """Migra dados de uma tabela específica"""
    try:
        # Reflete a estrutura da tabela
        metadata_origem = MetaData()
        metadata_destino = MetaData()
        
        tabela_origem = Table(nome_tabela, metadata_origem, autoload_with=engine_origem)
        tabela_destino = Table(nome_tabela, metadata_destino, autoload_with=engine_destino)
        
        # Busca todos os dados da origem
        with engine_origem.connect() as conn:
            resultado = conn.execute(tabela_origem.select())
            dados = resultado.fetchall()
        
        if not dados:
            print(f"   [AVISO]  Tabela '{nome_tabela}' vazia, pulando...")
            return 0, 0
        
        # Insere dados no destino
        registros_inseridos = 0
        registros_erro = 0
        
        with engine_destino.connect() as conn:
            for linha in dados:
                try:
                    # Converte Row para dict
                    dados_dict = dict(linha._mapping)
                    conn.execute(tabela_destino.insert().values(**dados_dict))
                    registros_inseridos += 1
                except Exception as e:
                    registros_erro += 1
                    if registros_erro <= 3:  # Mostra apenas os 3 primeiros erros
                        print(f"      [AVISO]  Erro ao inserir registro: {str(e)[:100]}")
            
            conn.commit()
        
        return registros_inseridos, registros_erro
    
    except Exception as e:
        print(f"   [ERRO] Erro ao migrar tabela '{nome_tabela}': {e}")
        return 0, 0

def main():
    """Função principal"""
    print_header("MIGRAÇÃO SQLITE → POSTGRESQL - SISTEMA VENDACERTA")
    
    # Verifica URIs
    print_step(1, "Verificando configurações")
    
    sqlite_uri = get_sqlite_uri()
    if not sqlite_uri:
        sys.exit(1)
    
    postgresql_uri = get_postgresql_uri()
    if not postgresql_uri:
        sys.exit(1)
    
    print(f"[OK] SQLite: {sqlite_uri}")
    print(f"[OK] PostgreSQL: {postgresql_uri.split('@')[0]}@***")  # Oculta credenciais
    
    # Confirma operação
    print("\n[AVISO]  ATENÇÃO: Esta operação irá:")
    print("   1. Criar backup do banco SQLite")
    print("   2. Criar todas as tabelas no PostgreSQL (se não existirem)")
    print("   3. Migrar todos os dados do SQLite para PostgreSQL")
    print("   4. Os dados existentes no PostgreSQL serão preservados")
    
    resposta = input("\n🤔 Deseja continuar? [s/N]: ")
    if resposta.lower() != 's':
        print("[ERRO] Migração cancelada pelo usuário.")
        sys.exit(0)
    
    # Cria backup
    print_step(2, "Criando backup do SQLite")
    backup_path = criar_backup_sqlite()
    
    # Conecta aos bancos
    print_step(3, "Conectando aos bancos de dados")
    
    try:
        print("[PROC] Conectando ao SQLite...")
        engine_sqlite = create_engine(sqlite_uri)
        Session_SQLite = sessionmaker(bind=engine_sqlite)
        session_sqlite = Session_SQLite()
        print("[OK] SQLite conectado!")
        
        print("[PROC] Conectando ao PostgreSQL...")
        engine_postgresql = create_engine(postgresql_uri)
        Session_PostgreSQL = sessionmaker(bind=engine_postgresql)
        session_postgresql = Session_PostgreSQL()
        print("[OK] PostgreSQL conectado!")
        
    except SQLAlchemyError as e:
        print(f"[ERRO] Erro ao conectar aos bancos: {e}")
        sys.exit(1)
    
    # Cria estrutura no PostgreSQL
    print_step(4, "Criando estrutura de tabelas no PostgreSQL")
    
    try:
        print("[PROC] Importando modelos e criando tabelas...")
        from app import app, db
        
        with app.app_context():
            db.create_all()
            print("[OK] Estrutura de tabelas criada!")
    
    except Exception as e:
        print(f"[ERRO] Erro ao criar estrutura: {e}")
        session_sqlite.close()
        session_postgresql.close()
        sys.exit(1)
    
    # Lista tabelas
    print_step(5, "Migrando dados")
    
    tabelas = listar_tabelas(engine_sqlite)
    print(f"[INFO] Total de tabelas a migrar: {len(tabelas)}")
    
    # Estatísticas
    total_tabelas = len(tabelas)
    total_registros = 0
    total_erros = 0
    tabelas_sucesso = 0
    
    # Ordem de migração (para respeitar foreign keys)
    # Primeiro tabelas sem dependências, depois as dependentes
    ordem_preferida = [
        'empresas',
        'usuarios',
        'vendedores',
        'categorias_produto',
        'produtos',
        'equipes',
        'metas',
        'clientes',
        'ordens_servico',
        'vendas',
        'comissoes',
        'historico_comissoes'
    ]
    
    # Organiza tabelas por ordem de prioridade
    tabelas_ordenadas = []
    for tabela in ordem_preferida:
        if tabela in tabelas:
            tabelas_ordenadas.append(tabela)
            tabelas.remove(tabela)
    
    # Adiciona tabelas restantes
    tabelas_ordenadas.extend(sorted(tabelas))
    
    # Migra cada tabela
    for i, tabela in enumerate(tabelas_ordenadas, 1):
        print(f"\n[{i}/{total_tabelas}] Migrando tabela '{tabela}'...")
        
        registros, erros = migrar_tabela(
            tabela,
            engine_sqlite,
            engine_postgresql,
            session_sqlite,
            session_postgresql
        )
        
        if registros > 0:
            print(f"   [OK] {registros} registros migrados", end='')
            if erros > 0:
                print(f" ({erros} erros)")
            else:
                print()
            tabelas_sucesso += 1
            total_registros += registros
            total_erros += erros
    
    # Fecha conexões
    session_sqlite.close()
    session_postgresql.close()
    
    # Resumo final
    print_header("MIGRAÇÃO CONCLUÍDA")
    
    print(f"\n[INFO] Estatísticas da migração:")
    print(f"   • Tabelas processadas: {total_tabelas}")
    print(f"   • Tabelas migradas: {tabelas_sucesso}")
    print(f"   • Total de registros: {total_registros}")
    
    if total_erros > 0:
        print(f"   • Erros encontrados: {total_erros}")
        print("\n[AVISO]  Alguns registros não foram migrados devido a erros.")
        print("   Verifique os logs acima para detalhes.")
    else:
        print(f"   • Erros: 0 [OK]")
    
    print(f"\n💾 Backup SQLite salvo em:")
    print(f"   {backup_path}")
    
    print("\n[OK] Próximos passos:")
    print("   1. Verifique os dados no PostgreSQL")
    print("   2. Execute: python app.py")
    print("   3. Teste o sistema com PostgreSQL")
    print("   4. Se tudo estiver OK, você pode remover o backup SQLite")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
