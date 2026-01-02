"""
Fix rápido: adiciona schema de manutenção/técnicos no Railway
Usa DATABASE_PUBLIC_URL ou variáveis PG* para conexão externa
"""
import os
import psycopg2

def get_public_db_url():
    """Obtém URL pública do banco"""
    # Priorizar DATABASE_PUBLIC_URL
    url = os.getenv('DATABASE_PUBLIC_URL')
    if url:
        print(f"[OK] Usando DATABASE_PUBLIC_URL")
        return url
    
    # Construir de PG* vars
    host = os.getenv('PGHOST')
    port = os.getenv('PGPORT', '5432')
    user = os.getenv('PGUSER')
    pwd = os.getenv('PGPASSWORD')
    db = os.getenv('PGDATABASE')
    
    if all([host, user, pwd, db]) and 'railway.internal' not in host:
        url = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"
        print(f"[OK] URL construída de PG* vars (host público)")
        return url
    
    print("[ERRO] Sem URL pública disponível")
    return None

def fix_schema():
    url = get_public_db_url()
    if not url:
        return False
    
    try:
        # Conectar
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        print("[OK] Conectado ao PostgreSQL")
        
        # 1. Criar tabela faixas_comissao_manutencao
        print("\n[1/4] Criando tabela faixas_comissao_manutencao...")
        cur.execute("""
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
        """)
        print("[OK] Tabela criada/verificada")
        
        # 2. Adicionar coluna faixa_manutencao_id
        print("\n[2/4] Adicionando coluna tecnicos.faixa_manutencao_id...")
        cur.execute("""
            DO $$
            BEGIN
              IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'tecnicos' AND column_name = 'faixa_manutencao_id'
              ) THEN
                ALTER TABLE tecnicos ADD COLUMN faixa_manutencao_id INTEGER;
              END IF;
            END $$;
        """)
        print("[OK] Coluna adicionada/verificada")
        
        # 3. Criar índice
        print("\n[3/4] Criando índice idx_tecnicos_faixa_manutencao...")
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_tecnicos_faixa_manutencao 
            ON tecnicos(faixa_manutencao_id)
        """)
        print("[OK] Índice criado/verificado")
        
        # 4. Criar FK
        print("\n[4/4] Criando FK fk_tecnicos_faixa_manutencao...")
        cur.execute("""
            DO $$
            BEGIN
              IF NOT EXISTS (
                SELECT 1 FROM pg_constraint c
                JOIN pg_class t ON t.oid = c.conrelid
                WHERE t.relname = 'tecnicos' AND c.conname = 'fk_tecnicos_faixa_manutencao'
              ) THEN
                ALTER TABLE tecnicos
                ADD CONSTRAINT fk_tecnicos_faixa_manutencao
                FOREIGN KEY (faixa_manutencao_id)
                REFERENCES faixas_comissao_manutencao (id)
                ON DELETE SET NULL;
              END IF;
            END $$;
        """)
        print("[OK] FK criada/verificada")
        
        cur.close()
        conn.close()
        print("\n✅ Schema de manutenção/técnicos atualizado com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return False

if __name__ == '__main__':
    import sys
    sys.exit(0 if fix_schema() else 1)
