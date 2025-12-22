"""
Verificação Completa de Integração Sistema-Banco de Dados
"""
import sys
import sqlite3
from sqlalchemy import inspect, text
from app import app, db
from models import (
    Vendedor, Cliente, CompraCliente, Meta, 
    Mensagem, Produto, EstoqueMovimento, Tecnico, 
    OrdemServico, Empresa, Equipe, Configuracao,
    FaixaComissao, FaixaComissaoVendedor, FaixaComissaoSupervisor
)

def verificar_colunas_modelo_vs_banco():
    """Compara colunas dos modelos SQLAlchemy com o banco real"""
    print("\n" + "="*80)
    print("🔍 VERIFICAÇÃO DE INTEGRAÇÃO SISTEMA-BANCO DE DADOS")
    print("="*80)
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Lista de modelos para verificar
        modelos = [
            ('empresa', Empresa),
            ('vendedor', Vendedor),
            ('clientes', Cliente),
            ('compra_cliente', CompraCliente),
            ('metas', Meta),
            ('equipe', Equipe),
            ('configuracao', Configuracao),
            ('faixa_comissao', FaixaComissao),
            ('faixa_comissao_vendedor', FaixaComissaoVendedor),
            ('faixa_comissao_supervisor', FaixaComissaoSupervisor),
            ('mensagem', Mensagem),
            ('produtos', Produto),
            ('estoque_movimento', EstoqueMovimento),
            ('tecnico', Tecnico),
            ('ordem_servico', OrdemServico)
        ]
        
        problemas = []
        sucesso = []
        
        for nome_tabela, modelo in modelos:
            print(f"\n📊 Verificando tabela: {nome_tabela}")
            print("-" * 80)
            
            # Verificar se a tabela existe
            if not inspector.has_table(nome_tabela):
                print(f"❌ Tabela '{nome_tabela}' NÃO EXISTE no banco!")
                problemas.append(f"Tabela '{nome_tabela}' não existe")
                continue
            
            # Obter colunas do banco
            colunas_banco = {col['name'] for col in inspector.get_columns(nome_tabela)}
            
            # Obter colunas do modelo
            colunas_modelo = {col.name for col in inspect(modelo).columns}
            
            # Verificar diferenças
            faltam_no_banco = colunas_modelo - colunas_banco
            sobram_no_banco = colunas_banco - colunas_modelo
            
            if faltam_no_banco:
                print(f"⚠️  Colunas faltando no banco: {', '.join(faltam_no_banco)}")
                problemas.append(f"{nome_tabela}: faltam {faltam_no_banco}")
            
            if sobram_no_banco:
                print(f"ℹ️  Colunas extras no banco: {', '.join(sobram_no_banco)}")
            
            if not faltam_no_banco and not sobram_no_banco:
                print(f"✅ Tabela '{nome_tabela}' está sincronizada!")
                sucesso.append(nome_tabela)
            elif not faltam_no_banco:
                print(f"✅ Tabela '{nome_tabela}' tem todas as colunas necessárias")
                sucesso.append(nome_tabela)
            
            # Mostrar detalhes das colunas
            print(f"\n   Colunas no modelo ({len(colunas_modelo)}): {', '.join(sorted(colunas_modelo))}")
            print(f"   Colunas no banco ({len(colunas_banco)}): {', '.join(sorted(colunas_banco))}")
        
        # Resumo final
        print("\n" + "="*80)
        print("📋 RESUMO DA VERIFICAÇÃO")
        print("="*80)
        print(f"✅ Tabelas OK: {len(sucesso)}/{len(modelos)}")
        print(f"❌ Problemas encontrados: {len(problemas)}")
        
        if sucesso:
            print("\n✅ Tabelas sincronizadas:")
            for tabela in sucesso:
                print(f"   • {tabela}")
        
        if problemas:
            print("\n⚠️  Problemas detectados:")
            for problema in problemas:
                print(f"   • {problema}")
        
        return len(problemas) == 0

def verificar_comunicacao_banco():
    """Testa a comunicação com o banco de dados"""
    print("\n" + "="*80)
    print("🔗 TESTE DE COMUNICAÇÃO COM BANCO DE DADOS")
    print("="*80)
    
    with app.app_context():
        try:
            # Teste 1: Contar vendedores
            total_vendedores = Vendedor.query.count()
            print(f"✅ Query de vendedores OK - Total: {total_vendedores}")
            
            # Teste 2: Contar clientes
            total_clientes = Cliente.query.count()
            print(f"✅ Query de clientes OK - Total: {total_clientes}")
            
            # Teste 3: Contar compras
            total_compras = CompraCliente.query.count()
            print(f"✅ Query de compras OK - Total: {total_compras}")
            
            # Teste 4: Contar metas
            total_metas = Meta.query.count()
            print(f"✅ Query de metas OK - Total: {total_metas}")
            
            # Teste 5: Verificar relações
            print("\n🔗 Verificando relações entre tabelas...")
            
            # Buscar uma compra com cliente
            compra_com_cliente = CompraCliente.query.filter(CompraCliente.cliente_id.isnot(None)).first()
            if compra_com_cliente:
                print(f"✅ Relação CompraCliente->Cliente OK (ID: {compra_com_cliente.id})")
            else:
                print("ℹ️  Nenhuma compra com cliente associado")
            
            # Buscar uma meta com vendedor
            meta_com_vendedor = Meta.query.filter(Meta.vendedor_id.isnot(None)).first()
            if meta_com_vendedor:
                print(f"✅ Relação Meta->Vendedor OK (ID: {meta_com_vendedor.id})")
            else:
                print("ℹ️  Nenhuma meta com vendedor associado")
            
            print("\n✅ Comunicação com banco de dados: OK")
            return True
            
        except Exception as e:
            print(f"\n❌ Erro na comunicação com banco: {str(e)}")
            return False

def verificar_integridade_dados():
    """Verifica a integridade dos dados"""
    print("\n" + "="*80)
    print("🔒 VERIFICAÇÃO DE INTEGRIDADE DE DADOS")
    print("="*80)
    
    with app.app_context():
        problemas = []
        
        # Verificar vendedores sem email
        vendedores_sem_email = Vendedor.query.filter(
            (Vendedor.email == None) | (Vendedor.email == '')
        ).count()
        
        if vendedores_sem_email > 0:
            print(f"⚠️  {vendedores_sem_email} vendedor(es) sem email")
            problemas.append(f"{vendedores_sem_email} vendedores sem email")
        else:
            print("✅ Todos os vendedores têm email")
        
        # Verificar clientes sem nome
        clientes_sem_nome = Cliente.query.filter(
            (Cliente.nome == None) | (Cliente.nome == '')
        ).count()
        
        if clientes_sem_nome > 0:
            print(f"⚠️  {clientes_sem_nome} cliente(s) sem nome")
            problemas.append(f"{clientes_sem_nome} clientes sem nome")
        else:
            print("✅ Todos os clientes têm nome")
        
        # Verificar compras órfãs (sem vendedor)
        compras_sem_vendedor = CompraCliente.query.filter(CompraCliente.vendedor_id == None).count()
        
        if compras_sem_vendedor > 0:
            print(f"⚠️  {compras_sem_vendedor} compra(s) sem vendedor")
            problemas.append(f"{compras_sem_vendedor} compras sem vendedor")
        else:
            print("✅ Todas as compras têm vendedor")
        
        if problemas:
            print(f"\n⚠️  Encontrados {len(problemas)} problemas de integridade")
            return False
        else:
            print("\n✅ Integridade dos dados: OK")
            return True

def verificar_indices_performance():
    """Verifica se os índices estão criados"""
    print("\n" + "="*80)
    print("⚡ VERIFICAÇÃO DE ÍNDICES DE PERFORMANCE")
    print("="*80)
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Verificar índices importantes
        indices_importantes = {
            'vendedor': ['email', 'cpf'],
            'clientes': ['codigo_cliente', 'cpf_cnpj'],
            'compra_cliente': ['vendedor_id', 'cliente_id', 'data'],
            'metas': ['vendedor_id', 'mes', 'ano']
        }
        
        for tabela, colunas in indices_importantes.items():
            if inspector.has_table(tabela):
                indices = inspector.get_indexes(tabela)
                colunas_indexadas = set()
                for idx in indices:
                    colunas_indexadas.update(idx['column_names'])
                
                print(f"\n📊 Tabela: {tabela}")
                for coluna in colunas:
                    if coluna in colunas_indexadas:
                        print(f"   ✅ Índice em '{coluna}': OK")
                    else:
                        print(f"   ℹ️  Índice em '{coluna}': Não encontrado (pode impactar performance)")

def gerar_relatorio_final():
    """Gera relatório final da verificação"""
    print("\n" + "="*80)
    print("📊 RELATÓRIO FINAL DO SISTEMA")
    print("="*80)
    
    with app.app_context():
        print("\n📈 Estatísticas do sistema:")
        print(f"   • Vendedores cadastrados: {Vendedor.query.count()}")
        print(f"   • Clientes cadastrados: {Cliente.query.count()}")
        print(f"   • Compras registradas: {CompraCliente.query.count()}")
        print(f"   • Metas ativas: {Meta.query.count()}")
        print(f"   • Equipes: {Equipe.query.count()}")
        print(f"   • Produtos: {Produto.query.count()}")
        print(f"   • Técnicos: {Tecnico.query.count()}")
        print(f"   • Ordens de Serviço: {OrdemServico.query.count()}")
        
        # Verificar vendedor admin
        admin = Vendedor.query.filter_by(cargo='gerente').first()
        if admin:
            print(f"\n👤 Vendedor Gerente:")
            print(f"   • Nome: {admin.nome}")
            print(f"   • Email: {admin.email}")
            print(f"   • Cargo: {admin.cargo}")
        else:
            print("\n⚠️  Nenhum vendedor gerente encontrado!")

if __name__ == '__main__':
    print("\n🚀 Iniciando verificação completa do sistema...")
    
    # Executar todas as verificações
    resultado1 = verificar_colunas_modelo_vs_banco()
    resultado2 = verificar_comunicacao_banco()
    resultado3 = verificar_integridade_dados()
    verificar_indices_performance()
    gerar_relatorio_final()
    
    # Resultado final
    print("\n" + "="*80)
    if resultado1 and resultado2 and resultado3:
        print("✅ SISTEMA TOTALMENTE INTEGRADO E FUNCIONANDO!")
    else:
        print("⚠️  SISTEMA COM PROBLEMAS - Verificar logs acima")
    print("="*80 + "\n")
    
    sys.exit(0 if (resultado1 and resultado2 and resultado3) else 1)
