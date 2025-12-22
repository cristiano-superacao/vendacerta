-- Migration: Adicionar campo gerente_id para hierarquia supervisor -> gerente/administrador
-- Data: 2024
-- Objetivo: Permitir vincular supervisores a gerentes ou administradores da empresa

-- Adicionar coluna gerente_id à tabela usuarios
-- Esta coluna permite criar uma hierarquia: supervisor → gerente → administrador
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS gerente_id INTEGER;

-- Adicionar foreign key constraint referenciando a própria tabela usuarios
-- Isso permite um relacionamento self-referential (auto-referência)
ALTER TABLE usuarios ADD CONSTRAINT fk_usuarios_gerente_id 
    FOREIGN KEY (gerente_id) REFERENCES usuarios(id)
    ON DELETE SET NULL;

-- Criar índice para melhorar performance de consultas que filtram por gerente_id
CREATE INDEX IF NOT EXISTS idx_usuarios_gerente_id ON usuarios(gerente_id);

-- Comentários explicativos
COMMENT ON COLUMN usuarios.gerente_id IS 'ID do gerente ou administrador responsável pelo supervisor';

-- Exemplo de uso:
-- UPDATE usuarios SET gerente_id = <id_do_gerente> WHERE id = <id_do_supervisor>;

-- Verificar estrutura após migração:
-- SELECT id, nome, cargo, gerente_id FROM usuarios WHERE cargo IN ('supervisor', 'gerente', 'admin');
