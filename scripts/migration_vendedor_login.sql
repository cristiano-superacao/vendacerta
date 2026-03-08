-- Migração para adicionar vendedor_id à tabela usuarios
-- Versão: v2.8.0
-- Data: 2024
-- Descrição: Permite que vendedores façam login no sistema

-- Adicionar coluna vendedor_id na tabela usuarios
ALTER TABLE usuarios ADD COLUMN vendedor_id INTEGER;

-- Adicionar foreign key constraint
ALTER TABLE usuarios ADD CONSTRAINT fk_usuarios_vendedor 
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(id) ON DELETE SET NULL;

-- Criar índice para performance
CREATE INDEX idx_usuarios_vendedor_id ON usuarios(vendedor_id);

-- Comentário na tabela
COMMENT ON COLUMN usuarios.vendedor_id IS 'ID do vendedor vinculado quando cargo=vendedor';
