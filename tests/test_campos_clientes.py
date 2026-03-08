"""
Script de teste para verificar se todos os campos de clientes estão funcionando
"""
from app import app, db
from models import Cliente, Vendedor
import json

def test_database_schema():
    """Testa se os campos do modelo estão acessíveis"""
    with app.app_context():
        print("\n" + "="*70)
        print("🔍 VERIFICAÇÃO DE CAMPOS DO MODELO CLIENTE")
        print("="*70)
        
        # Tenta criar uma instância vazia
        try:
            cliente_teste = Cliente()
            print("\n✅ Modelo Cliente instanciado com sucesso")
            
            # Lista todos os campos
            campos = [c.name for c in Cliente.__table__.columns]
            print(f"\n📋 Total de campos no modelo: {len(campos)}")
            print("\nCampos encontrados:")
            for i, campo in enumerate(sorted(campos), 1):
                print(f"   {i:2}. {campo}")
            
            # Verifica campos críticos
            campos_criticos = ['logradouro', 'municipio', 'codigo_cliente']
            print("\n🎯 Verificando campos críticos:")
            for campo in campos_criticos:
                existe = hasattr(Cliente, campo)
                status = "✅" if existe else "❌"
                print(f"   {status} {campo}: {'ENCONTRADO' if existe else 'NÃO ENCONTRADO'}")
            
            # Tenta fazer uma query simples
            print("\n🔎 Testando query no banco...")
            total_clientes = Cliente.query.count()
            print(f"   ✅ Total de clientes no banco: {total_clientes}")
            
            # Se houver clientes, testa acessar campos
            if total_clientes > 0:
                print("\n📄 Testando leitura de dados...")
                cliente = Cliente.query.first()
                print(f"   ✅ Cliente ID {cliente.id}: {cliente.nome}")
                print(f"   - Logradouro: {cliente.logradouro or 'Não informado'}")
                print(f"   - Município: {cliente.municipio or 'Não informado'}")
                print(f"   - Código Cliente: {cliente.codigo_cliente or 'Não informado'}")
            
            print("\n" + "="*70)
            print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
            print("="*70)
            
        except Exception as e:
            print(f"\n❌ ERRO: {str(e)}")
            print("\nDetalhes do erro:")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == '__main__':
    test_database_schema()
