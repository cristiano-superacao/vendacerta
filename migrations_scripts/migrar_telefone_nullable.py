"""
Migração: Permitir NULL nos campos de contato (telefone, email, etc)
Data: 17/12/2024
"""
import os
import sqlite3
from sqlalchemy import create_engine, text

def migrar_banco():
    """Permite NULL nos campos de contato da tabela clientes"""
    
    # Detectar tipo de banco
    database_url = os.getenv('DATABASE_URL')
    
    if database_url and 'postgresql' in database_url:
        print("🔄 Migrando PostgreSQL...")
        # PostgreSQL
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # Alterar colunas para aceitar NULL
            conn.execute(text("ALTER TABLE clientes ALTER COLUMN telefone DROP NOT NULL;"))
            conn.execute(text("ALTER TABLE clientes ALTER COLUMN telefone2 DROP NOT NULL;"))
            conn.execute(text("ALTER TABLE clientes ALTER COLUMN celular DROP NOT NULL;"))
            conn.execute(text("ALTER TABLE clientes ALTER COLUMN email DROP NOT NULL;"))
            conn.commit()
        print("✅ PostgreSQL migrado com sucesso!")
    else:
        print("🔄 Migrando SQLite...")
        # SQLite - Precisa recriar a tabela
        db_path = 'instance/vendacerta.db'
        if not os.path.exists(db_path):
            print(f"❌ Banco de dados não encontrado: {db_path}")
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # SQLite não suporta ALTER COLUMN diretamente
            # Precisamos recriar a tabela
            
            # 1. Renomear tabela antiga
            cursor.execute("ALTER TABLE clientes RENAME TO clientes_old;")
            
            # 2. Criar nova tabela com estrutura correta
            cursor.execute("""
                CREATE TABLE clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(200) NOT NULL,
                    razao_social VARCHAR(200),
                    sigla VARCHAR(50),
                    cpf VARCHAR(14) UNIQUE,
                    cnpj VARCHAR(18) UNIQUE,
                    inscricao_estadual VARCHAR(20),
                    codigo_bp VARCHAR(50),
                    bairro VARCHAR(100),
                    cidade VARCHAR(100),
                    cep VARCHAR(10),
                    ponto_referencia VARCHAR(255),
                    coordenada_x VARCHAR(50),
                    coordenada_y VARCHAR(50),
                    telefone VARCHAR(20),
                    telefone2 VARCHAR(20),
                    celular VARCHAR(20),
                    email VARCHAR(120),
                    formas_pagamento TEXT,
                    dia_visita VARCHAR(50),
                    vendedor_id INTEGER NOT NULL,
                    empresa_id INTEGER,
                    ativo BOOLEAN DEFAULT 1,
                    observacoes TEXT,
                    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (vendedor_id) REFERENCES vendedores(id),
                    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
                );
            """)
            
            # 3. Copiar dados da tabela antiga
            cursor.execute("""
                INSERT INTO clientes 
                SELECT * FROM clientes_old;
            """)
            
            # 4. Remover tabela antiga
            cursor.execute("DROP TABLE clientes_old;")
            
            # 5. Recriar índices
            cursor.execute("CREATE INDEX ix_clientes_nome ON clientes (nome);")
            cursor.execute("CREATE INDEX ix_clientes_cpf ON clientes (cpf);")
            cursor.execute("CREATE INDEX ix_clientes_cnpj ON clientes (cnpj);")
            cursor.execute("CREATE INDEX ix_clientes_vendedor_id ON clientes (vendedor_id);")
            cursor.execute("CREATE INDEX ix_clientes_empresa_id ON clientes (empresa_id);")
            cursor.execute("CREATE INDEX ix_clientes_data_cadastro ON clientes (data_cadastro);")
            
            conn.commit()
            print("✅ SQLite migrado com sucesso!")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Erro na migração: {e}")
            raise
        finally:
            conn.close()
    
    print("\n✅ Migração concluída com sucesso!")
    print("📋 Campos de contato agora aceitam valores NULL")

if __name__ == '__main__':
    print("=" * 70)
    print("🔄 MIGRAÇÃO: Permitir NULL em campos de contato")
    print("=" * 70)
    migrar_banco()
