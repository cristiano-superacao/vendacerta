"""
Script SQL para atualizar o banco de dados Railway
Garante que a tabela faixas_comissao existe com a estrutura correta
"""

-- Criação da tabela faixas_comissao se não existir
CREATE TABLE IF NOT EXISTS faixas_comissao (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES empresas(id) ON DELETE CASCADE,
    alcance_min DOUBLE PRECISION NOT NULL DEFAULT 0,
    alcance_max DOUBLE PRECISION NOT NULL,
    taxa_comissao DOUBLE PRECISION NOT NULL,
    cor VARCHAR(20) DEFAULT 'primary',
    ordem INTEGER DEFAULT 0,
    ativa BOOLEAN DEFAULT true,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_faixas_comissao_empresa 
    ON faixas_comissao(empresa_id);

CREATE INDEX IF NOT EXISTS idx_faixas_comissao_ordem 
    ON faixas_comissao(ordem);

CREATE INDEX IF NOT EXISTS idx_faixas_comissao_ativa 
    ON faixas_comissao(ativa);

-- Inserir faixas padrão globais se não existirem
INSERT INTO faixas_comissao (empresa_id, alcance_min, alcance_max, taxa_comissao, cor, ordem, ativa)
SELECT NULL, 0, 50, 0.01, 'danger', 0, true
WHERE NOT EXISTS (
    SELECT 1 FROM faixas_comissao 
    WHERE empresa_id IS NULL AND alcance_min = 0 AND alcance_max = 50
);

INSERT INTO faixas_comissao (empresa_id, alcance_min, alcance_max, taxa_comissao, cor, ordem, ativa)
SELECT NULL, 51, 75, 0.015, 'warning', 1, true
WHERE NOT EXISTS (
    SELECT 1 FROM faixas_comissao 
    WHERE empresa_id IS NULL AND alcance_min = 51 AND alcance_max = 75
);

INSERT INTO faixas_comissao (empresa_id, alcance_min, alcance_max, taxa_comissao, cor, ordem, ativa)
SELECT NULL, 76, 99, 0.02, 'info', 2, true
WHERE NOT EXISTS (
    SELECT 1 FROM faixas_comissao 
    WHERE empresa_id IS NULL AND alcance_min = 76 AND alcance_max = 99
);

INSERT INTO faixas_comissao (empresa_id, alcance_min, alcance_max, taxa_comissao, cor, ordem, ativa)
SELECT NULL, 100, 10000, 0.025, 'success', 3, true
WHERE NOT EXISTS (
    SELECT 1 FROM faixas_comissao 
    WHERE empresa_id IS NULL AND alcance_min = 100 AND alcance_max = 10000
);

-- Verificar resultado
SELECT 
    'Faixas de comissão criadas com sucesso!' as mensagem,
    COUNT(*) as total_faixas
FROM faixas_comissao;

SELECT 
    id,
    CASE WHEN empresa_id IS NULL THEN 'Global' ELSE 'Empresa #' || empresa_id END as escopo,
    alcance_min || '% - ' || alcance_max || '%' as faixa,
    (taxa_comissao * 100) || '%' as comissao,
    cor,
    ordem,
    CASE WHEN ativa THEN 'Ativa' ELSE 'Inativa' END as status
FROM faixas_comissao
ORDER BY empresa_id NULLS FIRST, ordem;
