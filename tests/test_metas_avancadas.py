"""
Script de teste para verificar as novas funcionalidades de metas avançadas
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("🧪 TESTE DE FUNCIONALIDADES - SISTEMA DE METAS AVANÇADAS")
print("=" * 70)

# Teste 1: Importar módulos
print("\n📦 Teste 1: Importando módulos...")
try:
    from calculo_balanceamento import (
        calcular_meta_balanceada,
        obter_ranking_meses,
        obter_dados_grafico_evolucao
    )
    print("   ✅ calculo_balanceamento.py importado com sucesso")
except ImportError as e:
    print(f"   ❌ Erro ao importar calculo_balanceamento: {e}")
    sys.exit(1)

try:
    from models import Meta, Vendedor, CompraCliente
    print("   ✅ Models importados com sucesso")
except ImportError as e:
    print(f"   ❌ Erro ao importar models: {e}")
    sys.exit(1)

# Teste 2: Verificar estrutura do modelo Meta
print("\n🗄️  Teste 2: Verificando campos do modelo Meta...")
campos_esperados = [
    'tipo_meta',
    'volume_meta',
    'volume_alcancado',
    'periodo_historico',
    'data_base_calculo',
    'meta_balanceada',
    'tendencia_calculada',
    'media_mensal_historico'
]

campos_meta = [col.name for col in Meta.__table__.columns]
print(f"   📋 Campos encontrados: {len(campos_meta)}")

for campo in campos_esperados:
    if campo in campos_meta:
        print(f"   ✅ {campo}")
    else:
        print(f"   ❌ {campo} - AUSENTE!")

# Teste 3: Verificar templates
print("\n📄 Teste 3: Verificando templates criados...")
import os

templates_esperados = [
    'templates/metas/configurar.html',
    'templates/relatorios/metas_avancado.html'
]

for template in templates_esperados:
    if os.path.exists(template):
        tamanho = os.path.getsize(template)
        print(f"   ✅ {template} ({tamanho} bytes)")
    else:
        print(f"   ❌ {template} - NÃO ENCONTRADO!")

# Teste 4: Verificar rotas no app.py
print("\n🛣️  Teste 4: Verificando rotas no app.py...")
rotas_esperadas = [
    'configurar_metas',
    'relatorio_metas_avancado',
    'api_dados_grafico_metas'
]

with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

for rota in rotas_esperadas:
    if f'def {rota}(' in app_content:
        print(f"   ✅ {rota}()")
    else:
        print(f"   ❌ {rota}() - NÃO ENCONTRADA!")

# Teste 5: Testar funções de balanceamento
print("\n🧮 Teste 5: Testando funções de balanceamento...")
try:
    # Criar um contexto de aplicação para acessar o banco
    from app import app
    from models import db
    
    with app.app_context():
        # Verificar se há vendedores no banco
        vendedores_count = Vendedor.query.count()
        print(f"   📊 Vendedores no banco: {vendedores_count}")
        
        # Verificar se há compras no banco
        compras_count = CompraCliente.query.count()
        print(f"   📊 Compras no banco: {compras_count}")
        
        # Verificar se há metas no banco
        metas_count = Meta.query.count()
        print(f"   📊 Metas no banco: {metas_count}")
        
        if vendedores_count > 0:
            vendedor = Vendedor.query.first()
            print(f"\n   🧪 Testando cálculo com vendedor: {vendedor.nome}")
            
            try:
                resultado = calcular_meta_balanceada(
                    vendedor_id=vendedor.id,
                    periodo_historico=6,
                    tipo_balanceamento='simples'
                )
                
                if resultado:
                    print(f"   ✅ Cálculo bem-sucedido!")
                    print(f"      Meta Valor: R$ {resultado.get('meta_valor', 0):.2f}")
                    print(f"      Meta Volume: {resultado.get('meta_volume', 0)} vendas")
                    print(f"      Meses Analisados: {resultado.get('meses_analisados', 0)}")
                else:
                    print("   ⚠️  Cálculo retornou None (vendedor sem histórico)")
            except Exception as e:
                print(f"   ❌ Erro ao calcular: {e}")
        else:
            print("   ⚠️  Sem vendedores para testar")
            
except Exception as e:
    print(f"   ❌ Erro no teste de funções: {e}")

# Resumo Final
print("\n" + "=" * 70)
print("✅ TESTES CONCLUÍDOS!")
print("=" * 70)
print("""
📝 Próximos Passos:
   1. Iniciar servidor: python app.py
   2. Acessar: http://127.0.0.1:5001/metas/configurar
   3. Acessar: http://127.0.0.1:5001/relatorios/metas-avancado
   4. Configurar primeira meta e testar interface
""")
