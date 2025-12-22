# migrar_indices_performance.py
"""
Script para adicionar índices de performance ao banco de dados
Melhora significativamente a velocidade das consultas
"""

from app import app, db
from sqlalchemy import text
import sys

def adicionar_indices():
    """Adiciona índices compostos para melhorar performance"""
    
    with app.app_context():
        try:
            print("=" * 70)
            print("🚀 ADICIONANDO ÍNDICES DE PERFORMANCE")
            print("=" * 70)
            print()
            
            # Verificar tipo de banco de dados
            database_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            is_postgres = 'postgresql' in database_url
            
            indices = []
            
            # Índices para tabela usuarios
            print("📊 Adicionando índices para tabela 'usuarios'...")
            indices.extend([
                # Índice composto para busca por empresa, cargo e status
                "CREATE INDEX IF NOT EXISTS idx_usuario_empresa_cargo ON usuarios(empresa_id, cargo, ativo)",
                # Índice para hierarquia de gerentes
                "CREATE INDEX IF NOT EXISTS idx_usuario_gerente ON usuarios(gerente_id, ativo)",
            ])
            
            # Índices para tabela vendedores
            print("📊 Adicionando índices para tabela 'vendedores'...")
            indices.extend([
                # Índice para nome (buscas frequentes)
                "CREATE INDEX IF NOT EXISTS idx_vendedor_nome ON vendedores(nome)",
                # Índice para email (buscas frequentes)
                "CREATE INDEX IF NOT EXISTS idx_vendedor_email ON vendedores(email)",
                # Índice para CPF (buscas frequentes)
                "CREATE INDEX IF NOT EXISTS idx_vendedor_cpf ON vendedores(cpf)",
                # Índice composto para supervisor e status
                "CREATE INDEX IF NOT EXISTS idx_vendedor_supervisor ON vendedores(supervisor_id, ativo)",
                # Índice composto para equipe e status
                "CREATE INDEX IF NOT EXISTS idx_vendedor_equipe ON vendedores(equipe_id, ativo)",
                # Índice composto para empresa e status
                "CREATE INDEX IF NOT EXISTS idx_vendedor_empresa ON vendedores(empresa_id, ativo)",
            ])
            
            # Índices para tabela metas
            print("📊 Adicionando índices para tabela 'metas'...")
            indices.extend([
                # Índice composto para busca por vendedor e período
                "CREATE INDEX IF NOT EXISTS idx_meta_vendedor_periodo ON metas(vendedor_id, ano, mes)",
                # Índice composto para busca por status e período
                "CREATE INDEX IF NOT EXISTS idx_meta_status ON metas(status_comissao, ano, mes)",
            ])
            
            # Índices para tabela clientes
            print("📊 Adicionando índices para tabela 'clientes'...")
            indices.extend([
                # Índice para bairro (relatórios geográficos)
                "CREATE INDEX IF NOT EXISTS idx_cliente_bairro ON clientes(bairro)",
                # Índice para cidade (relatórios geográficos)
                "CREATE INDEX IF NOT EXISTS idx_cliente_cidade ON clientes(cidade)",
                # Índice composto para vendedor e status
                "CREATE INDEX IF NOT EXISTS idx_cliente_vendedor_status ON clientes(vendedor_id, ativo)",
            ])
            
            # Índices para tabela compras_clientes
            print("📊 Adicionando índices para tabela 'compras_clientes'...")
            indices.extend([
                # Índice composto para relatórios de vendas por período
                "CREATE INDEX IF NOT EXISTS idx_compra_vendedor_data ON compras_clientes(vendedor_id, data_compra)",
                # Índice composto para análise de clientes
                "CREATE INDEX IF NOT EXISTS idx_compra_cliente_data ON compras_clientes(cliente_id, data_compra)",
            ])
            
            # Executar criação de índices
            print()
            print("⚙️  Executando comandos SQL...")
            print()
            
            sucesso = 0
            erros = 0
            
            for idx_sql in indices:
                try:
                    db.session.execute(text(idx_sql))
                    db.session.commit()
                    # Extrair nome do índice para log
                    idx_name = idx_sql.split("idx_")[1].split()[0] if "idx_" in idx_sql else "índice"
                    print(f"✅ Índice criado: idx_{idx_name}")
                    sucesso += 1
                except Exception as e:
                    # Ignorar erro se índice já existe
                    if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                        idx_name = idx_sql.split("idx_")[1].split()[0] if "idx_" in idx_sql else "índice"
                        print(f"⏭️  Índice já existe: idx_{idx_name}")
                        sucesso += 1
                    else:
                        print(f"❌ Erro ao criar índice: {e}")
                        erros += 1
                        db.session.rollback()
            
            print()
            print("=" * 70)
            print(f"✨ MIGRAÇÃO CONCLUÍDA!")
            print(f"   ✅ Índices criados/verificados: {sucesso}")
            if erros > 0:
                print(f"   ❌ Erros: {erros}")
            print("=" * 70)
            print()
            print("🎯 Benefícios esperados:")
            print("   • Queries até 10x mais rápidas")
            print("   • Dashboard carrega mais rápido")
            print("   • Relatórios mais ágeis")
            print("   • Melhor performance no Railway")
            print()
            
            return erros == 0
            
        except Exception as e:
            print(f"❌ Erro durante migração: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("\n⚠️  ATENÇÃO: Este script adicionará índices ao banco de dados")
    print("   Isso pode levar alguns minutos dependendo do tamanho do banco.")
    print()
    
    resposta = input("Deseja continuar? (s/n): ").lower().strip()
    
    if resposta == 's':
        sucesso = adicionar_indices()
        sys.exit(0 if sucesso else 1)
    else:
        print("\n❌ Operação cancelada pelo usuário.")
        sys.exit(1)
