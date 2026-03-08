"""
Migração: Adicionar permissões granulares e campos de estoque
"""
import sqlite3
from app import app

def migrar_permissoes_e_estoque():
    """Adiciona novas colunas de permissões e campos de estoque"""
    with app.app_context():
        db_path = 'instance/vendacerta.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Adicionando novas permissões granulares...")
        
        # Novas permissões de Clientes
        novas_permissoes_clientes = [
            "ALTER TABLE usuarios ADD COLUMN pode_acessar_clientes BOOLEAN DEFAULT 1",
            "ALTER TABLE usuarios ADD COLUMN pode_criar_clientes BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_editar_clientes BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_excluir_clientes BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_importar_clientes BOOLEAN DEFAULT 0",
        ]
        
        # Novas permissões de OS
        novas_permissoes_os = [
            "ALTER TABLE usuarios ADD COLUMN pode_acessar_os BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_criar_os BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_aprovar_os BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_atualizar_os BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_cancelar_os BOOLEAN DEFAULT 0",
        ]
        
        # Novas permissões de Estoque
        novas_permissoes_estoque = [
            "ALTER TABLE usuarios ADD COLUMN pode_acessar_estoque BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_gerenciar_produtos BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_movimentar_estoque BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_ver_custos BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_ajustar_estoque BOOLEAN DEFAULT 0",
        ]
        
        # Novas permissões de Técnicos
        novas_permissoes_tecnicos = [
            "ALTER TABLE usuarios ADD COLUMN pode_gerenciar_tecnicos BOOLEAN DEFAULT 0",
            "ALTER TABLE usuarios ADD COLUMN pode_atribuir_tecnicos BOOLEAN DEFAULT 0",
        ]
        
        # Novos campos de Produto
        novos_campos_produto = [
            "ALTER TABLE produtos ADD COLUMN codigo_barra VARCHAR(100)",
            "ALTER TABLE produtos ADD COLUMN referencia VARCHAR(100)",
            "ALTER TABLE produtos ADD COLUMN ncm VARCHAR(20)",
            "ALTER TABLE produtos ADD COLUMN fornecedor VARCHAR(200)",
        ]
        
        # Executar todas as migrações
        todas_migracoes = (
            novas_permissoes_clientes +
            novas_permissoes_os +
            novas_permissoes_estoque +
            novas_permissoes_tecnicos +
            novos_campos_produto
        )
        
        sucessos = 0
        erros = 0
        
        for sql in todas_migracoes:
            try:
                cursor.execute(sql)
                sucessos += 1
                # Extrair nome da coluna
                col_name = sql.split("ADD COLUMN ")[1].split(" ")[0]
                print(f"  ✅ Coluna '{col_name}' adicionada")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    col_name = sql.split("ADD COLUMN ")[1].split(" ")[0]
                    print(f"  ⚠️  Coluna '{col_name}' já existe (pulando)")
                else:
                    print(f"  ❌ Erro: {e}")
                    erros += 1
        
        # Atualizar permissões padrão para admins
        print("\n🔧 Configurando permissões padrão para administradores...")
        cursor.execute("""
            UPDATE usuarios 
            SET 
                pode_acessar_clientes = 1,
                pode_criar_clientes = 1,
                pode_editar_clientes = 1,
                pode_excluir_clientes = 1,
                pode_importar_clientes = 1,
                pode_acessar_os = 1,
                pode_criar_os = 1,
                pode_aprovar_os = 1,
                pode_atualizar_os = 1,
                pode_cancelar_os = 1,
                pode_acessar_estoque = 1,
                pode_gerenciar_produtos = 1,
                pode_movimentar_estoque = 1,
                pode_ver_custos = 1,
                pode_ajustar_estoque = 1,
                pode_gerenciar_tecnicos = 1,
                pode_atribuir_tecnicos = 1
            WHERE cargo = 'admin'
        """)
        
        # Configurar permissões para supervisor_manutencao
        cursor.execute("""
            UPDATE usuarios 
            SET 
                pode_acessar_os = 1,
                pode_aprovar_os = 1,
                pode_cancelar_os = 1,
                pode_acessar_estoque = 1,
                pode_movimentar_estoque = 1,
                pode_ver_custos = 1,
                pode_gerenciar_tecnicos = 1,
                pode_atribuir_tecnicos = 1
            WHERE cargo = 'supervisor_manutencao'
        """)
        
        # Configurar permissões para administrativo
        cursor.execute("""
            UPDATE usuarios 
            SET 
                pode_acessar_clientes = 1,
                pode_acessar_os = 1,
                pode_criar_os = 1,
                pode_acessar_estoque = 1
            WHERE cargo = 'administrativo'
        """)
        
        # Configurar permissões para tecnico
        cursor.execute("""
            UPDATE usuarios 
            SET 
                pode_acessar_os = 1,
                pode_atualizar_os = 1,
                pode_acessar_estoque = 1
            WHERE cargo = 'tecnico'
        """)
        
        # Criar índices para novos campos
        print("\n🔧 Criando índices...")
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_produto_codigo_barra ON produtos(codigo_barra)",
            "CREATE INDEX IF NOT EXISTS idx_produto_ncm ON produtos(ncm)",
            "CREATE INDEX IF NOT EXISTS idx_produto_referencia ON produtos(referencia)",
        ]
        
        for idx_sql in indices:
            try:
                cursor.execute(idx_sql)
                print(f"  ✅ Índice criado")
            except Exception as e:
                print(f"  ⚠️  {e}")
        
        # Commit e fechar
        conn.commit()
        conn.close()
        
        print("\n" + "="*60)
        print(f"✅ Migração concluída!")
        print(f"   {sucessos} colunas adicionadas com sucesso")
        if erros > 0:
            print(f"   {erros} erros encontrados")
        print("="*60)
        
        # Verificar estrutura
        print("\n🔍 Verificando estrutura da tabela usuarios...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(usuarios)")
        colunas = cursor.fetchall()
        
        permissoes_encontradas = [col[1] for col in colunas if col[1].startswith('pode_')]
        print(f"✅ {len(permissoes_encontradas)} permissões encontradas:")
        for perm in permissoes_encontradas:
            print(f"   - {perm}")
        
        print("\n🔍 Verificando estrutura da tabela produtos...")
        cursor.execute("PRAGMA table_info(produtos)")
        colunas_produto = cursor.fetchall()
        print(f"✅ {len(colunas_produto)} colunas na tabela produtos:")
        for col in colunas_produto:
            print(f"   - {col[1]} ({col[2]})")
        
        conn.close()

if __name__ == '__main__':
    migrar_permissoes_e_estoque()
