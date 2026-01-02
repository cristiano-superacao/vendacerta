"""
Script para Atualizar Banco de Dados Railway - Producao
Executa correcoes diretamente no PostgreSQL
"""
import os
import sys
from sqlalchemy import create_engine, text, inspect

def obter_database_url():
    """Obtem a URL do banco de dados Railway"""
    # Priorizar DATABASE_PUBLIC_URL para acesso externo
    db_url = os.getenv('DATABASE_PUBLIC_URL')
    if db_url:
        print(f"[OK] DATABASE_PUBLIC_URL encontrada (acesso externo)")
        return db_url
    
    # Tentar DATABASE_URL (rede interna Railway)
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        print(f"[OK] DATABASE_URL encontrada (rede interna)")
        return db_url
    
    # Construir a partir de variaveis individuais PG*
    pghost = os.getenv('PGHOST')
    pgport = os.getenv('PGPORT', '5432')
    pguser = os.getenv('PGUSER')
    pgpassword = os.getenv('PGPASSWORD')
    pgdatabase = os.getenv('PGDATABASE')
    
    if all([pghost, pguser, pgpassword, pgdatabase]):
        # Verificar se é host interno do Railway
        if 'railway.internal' in pghost:
            print(f"[AVISO] Host interno detectado: {pghost}")
            print(f"[INFO] Tentando usar DATABASE_PUBLIC_URL...")
            # Nao usar host interno para conexao externa
            return None
        
        db_url = f"postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}"
        print(f"[OK] URL construida a partir de variaveis PG*")
        print(f"     Host: {pghost}:{pgport}")
        print(f"     Database: {pgdatabase}")
        print(f"     User: {pguser}")
        return db_url
    
    print("[ERRO] Nenhuma configuracao de banco encontrada!")
    return None

def verificar_tabelas_existem(engine):
    """Verifica quais tabelas existem no banco"""
    inspector = inspect(engine)
    tabelas = inspector.get_table_names()
    
    print(f"\n[INFO] Tabelas encontradas no banco: {len(tabelas)}")
    for tabela in sorted(tabelas):
        print(f"  - {tabela}")
    
    return tabelas

def verificar_colunas_tabela(engine, nome_tabela):
    """Verifica colunas de uma tabela"""
    inspector = inspect(engine)
    
    if not inspector.has_table(nome_tabela):
        print(f"[AVISO] Tabela '{nome_tabela}' nao existe!")
        return []
    
    colunas = inspector.get_columns(nome_tabela)
    nomes_colunas = [col['name'] for col in colunas]
    
    print(f"\n[INFO] Colunas da tabela '{nome_tabela}': {len(nomes_colunas)}")
    for col in nomes_colunas:
        print(f"  - {col}")
    
    return nomes_colunas

def adicionar_coluna_se_nao_existe(conn, tabela, coluna, tipo, default=None):
    """Adiciona uma coluna se ela nao existir"""
    try:
        # Verificar se a coluna existe
        check_query = text(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = :tabela AND column_name = :coluna
        """)
        
        result = conn.execute(check_query, {"tabela": tabela, "coluna": coluna})
        existe = result.fetchone() is not None
        
        if existe:
            print(f"  [OK] Coluna '{coluna}' ja existe em '{tabela}'")
            return True
        
        # Adicionar coluna
        default_clause = f"DEFAULT {default}" if default is not None else ""
        alter_query = text(f"""
            ALTER TABLE {tabela} 
            ADD COLUMN {coluna} {tipo} {default_clause}
        """)
        
        conn.execute(alter_query)
        conn.commit()
        print(f"  [+] Coluna '{coluna}' adicionada em '{tabela}'")
        return True
        
    except Exception as e:
        print(f"  [ERRO] Falha ao adicionar '{coluna}' em '{tabela}': {e}")
        return False

def criar_tabela_se_nao_existe(conn, tabela, ddl_sql):
    """Cria uma tabela com o DDL informado se ela não existir."""
    try:
        check_query = text(
            """
            SELECT 1 FROM information_schema.tables
            WHERE table_name = :tabela
            """
        )
        existe = conn.execute(check_query, {"tabela": tabela}).fetchone() is not None
        if existe:
            print(f"  [OK] Tabela '{tabela}' já existe")
            return True

        conn.execute(text(ddl_sql))
        conn.commit()
        print(f"  [+] Tabela '{tabela}' criada")
        return True
    except Exception as e:
        print(f"  [ERRO] Falha ao criar tabela '{tabela}': {e}")
        return False

def criar_indice_se_nao_existe(conn, nome_idx, tabela, coluna):
    """Cria índice se não existir."""
    try:
        sql = text(
            f"""
            CREATE INDEX IF NOT EXISTS {nome_idx}
            ON {tabela} ({coluna})
            """
        )
        conn.execute(sql)
        conn.commit()
        print(f"  [OK] Índice '{nome_idx}' criado/verificado")
        return True
    except Exception as e:
        print(f"  [AVISO] Índice '{nome_idx}': {e}")
        return False

def criar_fk_se_nao_existe(conn, tabela, nome_fk, coluna, tabela_ref, coluna_ref, on_delete="SET NULL"):
    """Cria constraint de chave estrangeira se não existir."""
    try:
        # Verificar existência pelo pg_constraint
        check = text(
            """
            SELECT 1
            FROM pg_constraint c
            JOIN pg_class t ON t.oid = c.conrelid
            WHERE t.relname = :tabela
              AND c.conname = :nome_fk
            """
        )
        existe = conn.execute(check, {"tabela": tabela, "nome_fk": nome_fk}).fetchone() is not None
        if existe:
            print(f"  [OK] FK '{nome_fk}' já existe em '{tabela}'")
            return True

        alter = text(
            f"""
            ALTER TABLE {tabela}
            ADD CONSTRAINT {nome_fk}
            FOREIGN KEY ({coluna})
            REFERENCES {tabela_ref} ({coluna_ref})
            ON DELETE {on_delete}
            """
        )
        conn.execute(alter)
        conn.commit()
        print(f"  [+] FK '{nome_fk}' criada em '{tabela}' → '{tabela_ref}({coluna_ref})'")
        return True
    except Exception as e:
        print(f"  [AVISO] Falha ao criar FK '{nome_fk}': {e}")
        return False

def atualizar_banco_railway():
    """Executa atualizacoes no banco Railway"""
    print("\n" + "="*80)
    print("ATUALIZACAO DO BANCO DE DADOS RAILWAY")
    print("="*80)
    
    # Obter URL do banco
    db_url = obter_database_url()
    if not db_url:
        print("\n[ERRO] Impossivel continuar sem configuracao do banco!")
        return False
    
    try:
        # Conectar ao banco
        print(f"\n[PROC] Conectando ao banco PostgreSQL...")
        engine = create_engine(db_url, echo=False)
        
        with engine.connect() as conn:
            print("[OK] Conexao estabelecida!")
            
            # Verificar tabelas existentes
            tabelas = verificar_tabelas_existem(engine)
            
            # Atualizar tabela vendedores (se existir)
            if 'vendedores' in tabelas:
                print("\n" + "-"*80)
                print("ATUALIZANDO TABELA: vendedores")
                print("-"*80)
                
                colunas = verificar_colunas_tabela(engine, 'vendedores')
                
                # Adicionar colunas que podem estar faltando
                adicionar_coluna_se_nao_existe(conn, 'vendedores', 'supervisor_id', 'INTEGER')
                adicionar_coluna_se_nao_existe(conn, 'vendedores', 'pode_gerenciar_tecnicos', 'BOOLEAN', 'FALSE')
                adicionar_coluna_se_nao_existe(conn, 'vendedores', 'pode_atribuir_tecnicos', 'BOOLEAN', 'FALSE')
                adicionar_coluna_se_nao_existe(conn, 'vendedores', 'equipe_id', 'INTEGER')
                adicionar_coluna_se_nao_existe(conn, 'vendedores', 'ativo', 'BOOLEAN', 'TRUE')
            
            # Atualizar tabela usuarios (se existir)
            if 'usuarios' in tabelas:
                print("\n" + "-"*80)
                print("ATUALIZANDO TABELA: usuarios")
                print("-"*80)
                
                colunas = verificar_colunas_tabela(engine, 'usuarios')
                
                adicionar_coluna_se_nao_existe(conn, 'usuarios', 'supervisor_id', 'INTEGER')
                adicionar_coluna_se_nao_existe(conn, 'usuarios', 'pode_gerenciar_tecnicos', 'BOOLEAN', 'FALSE')
                adicionar_coluna_se_nao_existe(conn, 'usuarios', 'pode_atribuir_tecnicos', 'BOOLEAN', 'FALSE')
            
            # Atualizar tabela clientes (se existir)
            if 'clientes' in tabelas:
                print("\n" + "-"*80)
                print("ATUALIZANDO TABELA: clientes")
                print("-"*80)
                
                colunas = verificar_colunas_tabela(engine, 'clientes')
                
                adicionar_coluna_se_nao_existe(conn, 'clientes', 'vendedor_id', 'INTEGER')
                adicionar_coluna_se_nao_existe(conn, 'clientes', 'empresa_id', 'INTEGER')
                adicionar_coluna_se_nao_existe(conn, 'clientes', 'ativo', 'BOOLEAN', 'TRUE')
            
            # Criar indices para performance (se nao existirem)
            print("\n" + "-"*80)
            print("CRIANDO INDICES DE PERFORMANCE")
            print("-"*80)
            
            indices = [
                ("idx_vendedores_email", "vendedores", "email"),
                ("idx_vendedores_cpf", "vendedores", "cpf"),
                ("idx_clientes_codigo", "clientes", "codigo_cliente"),
                ("idx_clientes_vendedor", "clientes", "vendedor_id"),
                ("idx_metas_vendedor", "metas", "vendedor_id"),
            ]
            
            for nome_idx, tabela, coluna in indices:
                if tabela in tabelas:
                    try:
                        create_idx = text(f"""
                            CREATE INDEX IF NOT EXISTS {nome_idx} 
                            ON {tabela} ({coluna})
                        """)
                        conn.execute(create_idx)
                        conn.commit()
                        print(f"  [OK] Indice '{nome_idx}' criado/verificado")
                    except Exception as e:
                        print(f"  [AVISO] Indice '{nome_idx}': {e}")

            # ================================
            # MÓDULO MANUTENÇÃO / TÉCNICOS
            # ================================
            print("\n" + "-"*80)
            print("VERIFICAÇÃO DE TABELAS: manutenção/técnicos")
            print("-"*80)

            # 1) Tabela de faixas de comissão de manutenção
            ddl_faixas_manutencao = """
            CREATE TABLE IF NOT EXISTS faixas_comissao_manutencao (
              id SERIAL PRIMARY KEY,
              empresa_id INTEGER NULL,
              alcance_min DOUBLE PRECISION NOT NULL DEFAULT 0,
              alcance_max DOUBLE PRECISION NOT NULL,
              taxa_comissao DOUBLE PRECISION NOT NULL,
              cor VARCHAR(20) DEFAULT 'primary',
              ordem INTEGER DEFAULT 0,
              ativa BOOLEAN DEFAULT TRUE,
              data_criacao TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
              data_atualizacao TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
            )
            """
            criar_tabela_se_nao_existe(conn, 'faixas_comissao_manutencao', ddl_faixas_manutencao)

            # 2) Adicionar coluna de vínculo em 'tecnicos'
            if 'tecnicos' in tabelas:
                print("\n" + "-"*80)
                print("ATUALIZANDO TABELA: tecnicos")
                print("-"*80)
                adicionar_coluna_se_nao_existe(conn, 'tecnicos', 'faixa_manutencao_id', 'INTEGER')
                criar_indice_se_nao_existe(conn, 'idx_tecnicos_faixa_manutencao', 'tecnicos', 'faixa_manutencao_id')
                criar_fk_se_nao_existe(
                    conn,
                    tabela='tecnicos',
                    nome_fk='fk_tecnicos_faixa_manutencao',
                    coluna='faixa_manutencao_id',
                    tabela_ref='faixas_comissao_manutencao',
                    coluna_ref='id',
                    on_delete='SET NULL'
                )
            else:
                print("[AVISO] Tabela 'tecnicos' não encontrada; criação depende de 'create_tables_railway.py'.")
            
            print("\n" + "="*80)
            print("[SUCESSO] Banco de dados atualizado com sucesso!")
            print("="*80)
            return True
            
    except Exception as e:
        print(f"\n[ERRO CRITICO] Falha na atualizacao: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n[START] Iniciando atualizacao do banco Railway...")
    
    sucesso = atualizar_banco_railway()
    
    if sucesso:
        print("\n[OK] Processo concluido com sucesso!")
        sys.exit(0)
    else:
        print("\n[ERRO] Processo finalizado com erros!")
        sys.exit(1)
