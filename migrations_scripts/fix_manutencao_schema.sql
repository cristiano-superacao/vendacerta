-- Criar tabela faixas_comissao_manutencao se não existir
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
);

-- Adicionar coluna faixa_manutencao_id na tabela tecnicos se não existir
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'tecnicos' AND column_name = 'faixa_manutencao_id'
  ) THEN
    ALTER TABLE tecnicos ADD COLUMN faixa_manutencao_id INTEGER;
  END IF;
END $$;

-- Criar índice se não existir
CREATE INDEX IF NOT EXISTS idx_tecnicos_faixa_manutencao ON tecnicos(faixa_manutencao_id);

-- Criar FK se não existir
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
