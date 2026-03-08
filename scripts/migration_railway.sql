-- Migração para adicionar suporte a empresas e super admin
-- Execute este SQL no banco de dados PostgreSQL do Railway

-- 1. Criar tabela de empresas
CREATE TABLE IF NOT EXISTS empresas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    email VARCHAR(120) NOT NULL,
    telefone VARCHAR(20),
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    plano VARCHAR(20) DEFAULT 'basico',
    ativo BOOLEAN DEFAULT TRUE,
    bloqueado BOOLEAN DEFAULT FALSE,
    motivo_bloqueio TEXT,
    max_usuarios INTEGER DEFAULT 10,
    max_vendedores INTEGER DEFAULT 50,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Adicionar colunas na tabela usuarios (se não existirem)
DO $$ 
BEGIN
    -- Adicionar empresa_id
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='usuarios' AND column_name='empresa_id'
    ) THEN
        ALTER TABLE usuarios ADD COLUMN empresa_id INTEGER REFERENCES empresas(id);
    END IF;

    -- Adicionar is_super_admin
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='usuarios' AND column_name='is_super_admin'
    ) THEN
        ALTER TABLE usuarios ADD COLUMN is_super_admin BOOLEAN DEFAULT FALSE;
    END IF;
END $$;

-- 3. Criar empresa padrão
INSERT INTO empresas (nome, cnpj, email, telefone, cidade, estado, plano, max_usuarios, max_vendedores)
VALUES ('Empresa Padrão', '00000000000000', 'contato@empresapadrao.com', '(71) 99999-9999', 'Salvador', 'BA', 'premium', 100, 500)
ON CONFLICT (cnpj) DO NOTHING;

-- 4. Associar usuários existentes à empresa padrão
UPDATE usuarios 
SET empresa_id = (SELECT id FROM empresas WHERE cnpj = '00000000000000')
WHERE empresa_id IS NULL AND is_super_admin = FALSE;

-- 5. Criar super administrador
INSERT INTO usuarios (nome, email, senha_hash, cargo, is_super_admin, ativo, data_criacao)
VALUES (
    'Super Administrador', 
    'superadmin@suameta.com',
    'scrypt:32768:8:1$changeme$hashedpassword', -- ALTERE ISTO: execute o script criar_banco_novo.py localmente para gerar o hash correto
    'admin',
    TRUE,
    TRUE,
    CURRENT_TIMESTAMP
)
ON CONFLICT (email) DO UPDATE SET is_super_admin = TRUE;

-- 6. Garantir que admin@suameta.com não é super admin
UPDATE usuarios 
SET is_super_admin = FALSE,
    empresa_id = (SELECT id FROM empresas WHERE cnpj = '00000000000000')
WHERE email = 'admin@suameta.com';

-- Verificar resultado
SELECT 
    u.id, 
    u.nome, 
    u.email, 
    u.cargo, 
    u.is_super_admin,
    e.nome as empresa
FROM usuarios u
LEFT JOIN empresas e ON u.empresa_id = e.id
ORDER BY u.is_super_admin DESC, u.id;
