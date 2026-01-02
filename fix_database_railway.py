#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de correção do banco de dados PostgreSQL do Railway
Adiciona coluna supervisor_id e outros campos faltantes
"""
print("--- INICIANDO SCRIPT DE DIAGNÓSTICO E CORREÇÃO ---")

import os
import sys
import time
from sqlalchemy import create_engine, text, inspect

def fix_database():
    """Corrige o banco de dados adicionando colunas faltantes.

    Retorna True se tudo ocorreu bem, False caso contrário.
    Nunca faz sys.exit() para não derrubar o processo do servidor.
    """
    
    # Tenta obter a URL do banco de dados de múltiplas variáveis de ambiente
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('DATABASE_PUBLIC_URL')
    
    # Se não encontrou, tenta construir a partir das variáveis PG* individuais
    if not database_url:
        pghost = os.environ.get('PGHOST')
        pgport = os.environ.get('PGPORT')
        pguser = os.environ.get('PGUSER')
        pgpassword = os.environ.get('PGPASSWORD')
        pgdatabase = os.environ.get('PGDATABASE')
        
        if all([pghost, pgport, pguser, pgpassword, pgdatabase]):
            database_url = f"postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}"
            print("✅ URL do banco construída a partir de variáveis PG* individuais")
        else:
            print("❌ Nenhuma variável de ambiente de URL de banco de dados encontrada!")
            print("📝 Configure DATABASE_URL ou as variáveis PG* no Railway.")
            return False
    
    # Corrigir URL se necessário (Railway usa postgres:// mas SQLAlchemy precisa de postgresql://)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    print("🔗 Conectando ao banco de dados...")
    
    try:
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=280,
            connect_args={"connect_timeout": 10}
        )
        
        conn = None
        for attempt in range(1, 4):
            try:
                conn = engine.connect()
                break
            except Exception as e:
                print(f"⚠️ Tentativa {attempt}/3 de conexão falhou: {e}")
                time.sleep(5)
        
        if conn is None:
            print("❌ Não foi possível conectar ao banco após 3 tentativas.")
            return False
        
        with conn:
            print("✅ Conexão estabelecida com sucesso!")

            inspector = inspect(engine)

            # ==========================
            # 1) CORREÇÃO TABELA USUÁRIOS
            # ==========================
            if 'usuarios' not in inspector.get_table_names():
                print("❌ Tabela 'usuarios' não existe! Pulando correção automática.")
                return False

            # Obter colunas atuais de usuarios
            user_columns = [col['name'] for col in inspector.get_columns('usuarios')]
            print(f"📊 Colunas existentes em usuarios: {', '.join(user_columns)}")

            # Lista de colunas que devem existir em usuarios
            required_user_columns = {
                'supervisor_id': 'INTEGER',
                'gerente_id': 'INTEGER',
                'vendedor_id': 'INTEGER',
                'departamento': 'VARCHAR(50)',
                'pode_gerenciar_tecnicos': 'BOOLEAN DEFAULT FALSE',
                'pode_atribuir_tecnicos': 'BOOLEAN DEFAULT FALSE'
            }

            # Adicionar colunas faltantes em usuarios
            for column_name, column_type in required_user_columns.items():
                if column_name not in user_columns:
                    print(f"➕ Adicionando coluna em usuarios: {column_name}")

                    try:
                        # Adicionar coluna
                        sql = f"ALTER TABLE usuarios ADD COLUMN {column_name} {column_type}"
                        conn.execute(text(sql))
                        conn.commit()
                        print(f"   ✅ Coluna {column_name} adicionada com sucesso em usuarios!")

                        # Adicionar foreign keys e índices para colunas de relacionamento
                        if column_name in ['supervisor_id', 'gerente_id', 'vendedor_id']:
                            try:
                                # Adicionar constraint de foreign key
                                if column_name in ['supervisor_id', 'gerente_id']:
                                    ref_table = 'usuarios'
                                else:
                                    ref_table = 'vendedores'

                                fk_name = f"fk_usuarios_{column_name.replace('_id', '')}"
                                fk_sql = f"""
                                ALTER TABLE usuarios 
                                ADD CONSTRAINT {fk_name} 
                                FOREIGN KEY ({column_name}) 
                                REFERENCES {ref_table}(id) 
                                ON DELETE SET NULL
                                """
                                conn.execute(text(fk_sql))
                                conn.commit()
                                print(f"   ✅ Foreign key constraint {fk_name} adicionada!")
                            except Exception as e:
                                print(f"   ⚠️ Aviso ao adicionar FK {column_name}: {str(e)}")

                            try:
                                # Adicionar índice
                                idx_name = f"idx_usuario_{column_name.replace('_id', '')}"
                                idx_sql = f"CREATE INDEX {idx_name} ON usuarios({column_name})"
                                conn.execute(text(idx_sql))
                                conn.commit()
                                print(f"   ✅ Índice {idx_name} criado!")
                            except Exception as e:
                                print(f"   ⚠️ Aviso ao adicionar índice {column_name}: {str(e)}")

                    except Exception as e:
                        print(f"   ❌ Erro ao adicionar coluna {column_name} em usuarios: {str(e)}")
                        try:
                            conn.rollback()
                        except Exception:
                            pass
                else:
                    print(f"✓ Coluna {column_name} já existe em usuarios")

            # ==========================
            # 2) CORREÇÃO TABELA CLIENTES
            # ==========================
            if 'clientes' not in inspector.get_table_names():
                print("⚠️ Tabela 'clientes' não existe! Pulando correção de clientes.")
            else:
                cliente_columns = [col['name'] for col in inspector.get_columns('clientes')]
                print(f"\n📊 Colunas existentes em clientes: {', '.join(cliente_columns)}")

                required_cliente_columns = {
                    'estado': 'VARCHAR(2)',
                    'celular2': 'VARCHAR(20)',
                    'longitude': 'VARCHAR(50)',
                    'latitude': 'VARCHAR(50)',
                    'codigo_bw': 'VARCHAR(50)',
                    'supervisor_id': 'INTEGER'
                }

                for column_name, column_type in required_cliente_columns.items():
                    if column_name not in cliente_columns:
                        print(f"➕ Adicionando coluna em clientes: {column_name}")
                        try:
                            sql = f"ALTER TABLE clientes ADD COLUMN {column_name} {column_type}"
                            conn.execute(text(sql))
                            conn.commit()
                            print(f"   ✅ Coluna {column_name} adicionada com sucesso em clientes!")

                            if column_name == 'supervisor_id':
                                # Foreign key para usuarios.id e índice
                                try:
                                    fk_sql = """
                                    ALTER TABLE clientes 
                                    ADD CONSTRAINT fk_clientes_supervisor 
                                    FOREIGN KEY (supervisor_id) 
                                    REFERENCES usuarios(id) 
                                    ON DELETE SET NULL
                                    """
                                    conn.execute(text(fk_sql))
                                    conn.commit()
                                    print("   ✅ Foreign key fk_clientes_supervisor adicionada!")
                                except Exception as e:
                                    print(f"   ⚠️ Aviso ao adicionar FK supervisor_id em clientes: {str(e)}")

                                try:
                                    idx_sql = "CREATE INDEX IF NOT EXISTS idx_clientes_supervisor ON clientes(supervisor_id)"
                                    conn.execute(text(idx_sql))
                                    conn.commit()
                                    print("   ✅ Índice idx_clientes_supervisor criado!")
                                except Exception as e:
                                    print(f"   ⚠️ Aviso ao criar índice idx_clientes_supervisor: {str(e)}")

                        except Exception as e:
                            print(f"   ❌ Erro ao adicionar coluna {column_name} em clientes: {str(e)}")
                            try:
                                conn.rollback()
                            except Exception:
                                pass
                    else:
                        print(f"✓ Coluna {column_name} já existe em clientes")

            # ==========================
            # 3) CORREÇÃO MÓDULO MANUTENÇÃO/TÉCNICOS
            # ==========================
            print("\n📊 Corrigindo módulo Manutenção/Técnicos...")
            
            # 3.1) Criar tabela faixas_comissao_manutencao se não existir
            if 'faixas_comissao_manutencao' not in inspector.get_table_names():
                print("➕ Criando tabela faixas_comissao_manutencao...")
                try:
                    create_table_sql = """
                    CREATE TABLE faixas_comissao_manutencao (
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
                    conn.execute(text(create_table_sql))
                    conn.commit()
                    print("   ✅ Tabela faixas_comissao_manutencao criada!")
                except Exception as e:
                    print(f"   ❌ Erro ao criar tabela faixas_comissao_manutencao: {str(e)}")
                    try:
                        conn.rollback()
                    except Exception:
                        pass
            else:
                print("✓ Tabela faixas_comissao_manutencao já existe")
            
            # 3.2) Adicionar coluna faixa_manutencao_id em tecnicos
            if 'tecnicos' in inspector.get_table_names():
                tecnico_columns = [col['name'] for col in inspector.get_columns('tecnicos')]
                
                if 'faixa_manutencao_id' not in tecnico_columns:
                    print("➕ Adicionando coluna tecnicos.faixa_manutencao_id...")
                    try:
                        add_col_sql = "ALTER TABLE tecnicos ADD COLUMN faixa_manutencao_id INTEGER"
                        conn.execute(text(add_col_sql))
                        conn.commit()
                        print("   ✅ Coluna faixa_manutencao_id adicionada em tecnicos!")
                        
                        # Criar índice
                        try:
                            idx_sql = "CREATE INDEX IF NOT EXISTS idx_tecnicos_faixa_manutencao ON tecnicos(faixa_manutencao_id)"
                            conn.execute(text(idx_sql))
                            conn.commit()
                            print("   ✅ Índice idx_tecnicos_faixa_manutencao criado!")
                        except Exception as e:
                            print(f"   ⚠️ Aviso ao criar índice: {str(e)}")
                        
                        # Criar FK com ON DELETE SET NULL
                        try:
                            fk_sql = """
                            ALTER TABLE tecnicos
                            ADD CONSTRAINT fk_tecnicos_faixa_manutencao
                            FOREIGN KEY (faixa_manutencao_id)
                            REFERENCES faixas_comissao_manutencao (id)
                            ON DELETE SET NULL
                            """
                            conn.execute(text(fk_sql))
                            conn.commit()
                            print("   ✅ FK fk_tecnicos_faixa_manutencao criada com ON DELETE SET NULL!")
                        except Exception as e:
                            print(f"   ⚠️ Aviso ao criar FK: {str(e)}")
                        
                    except Exception as e:
                        print(f"   ❌ Erro ao adicionar coluna faixa_manutencao_id: {str(e)}")
                        try:
                            conn.rollback()
                        except Exception:
                            pass
                else:
                    print("✓ Coluna faixa_manutencao_id já existe em tecnicos")
            else:
                print("⚠️ Tabela tecnicos não existe ainda")

            # Verificar colunas finais
            inspector = inspect(engine)
            final_user_columns = [col['name'] for col in inspector.get_columns('usuarios')]
            print(f"\n📊 Colunas finais em usuarios: {', '.join(final_user_columns)}")

            if 'clientes' in inspector.get_table_names():
                final_cliente_columns = [col['name'] for col in inspector.get_columns('clientes')]
                print(f"📊 Colunas finais em clientes: {', '.join(final_cliente_columns)}")
            
            if 'tecnicos' in inspector.get_table_names():
                final_tecnico_columns = [col['name'] for col in inspector.get_columns('tecnicos')]
                print(f"📊 Colunas finais em tecnicos: {', '.join(final_tecnico_columns)}")

            print("\n✅ Migração concluída com sucesso!")
            print("🚀 O sistema pode ser reiniciado agora")
            return True
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🔧 CORREÇÃO DO BANCO DE DADOS - RAILWAY")
    print("=" * 60)
    ok = fix_database()
    sys.exit(0 if ok else 1)
