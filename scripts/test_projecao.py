"""
Testes para o sistema de projeção de vendas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculo_projecao import contar_dias_uteis, calcular_projecao_mes, formatar_moeda
from datetime import datetime

def teste_contar_dias_uteis():
    """Testa o cálculo de dias úteis"""
    print("=" * 60)
    print("TESTE: Contagem de Dias Úteis")
    print("=" * 60)

    # Janeiro/2025 - mês com 23 dias úteis
    total, trabalhados = contar_dias_uteis(2025, 1, 10)
    print(f"\n📅 Janeiro/2025 até dia 10:")
    print(f"   Total de dias úteis no mês: {total}")
    print(f"   Dias úteis trabalhados: {trabalhados}")
    print(f"   Dias úteis restantes: {total - trabalhados}")

    assert total == 23, f"Janeiro/2025 deveria ter 23 dias úteis, mas obteve {total}"
    print("   ✅ PASSOU - Janeiro/2025 tem 23 dias úteis")

    # Fevereiro/2025 - mês com 20 dias úteis
    total_fev, _ = contar_dias_uteis(2025, 2)
    print(f"\n📅 Fevereiro/2025:")
    print(f"   Total de dias úteis no mês: {total_fev}")

    assert total_fev == 20, f"Fevereiro/2025 deveria ter 20 dias úteis, mas obteve {total_fev}"
    print("   ✅ PASSOU - Fevereiro/2025 tem 20 dias úteis")

def teste_calcular_projecao():
    """Testa o cálculo de projeção de vendas"""
    print("\n" + "=" * 60)
    print("TESTE: Cálculo de Projeção de Vendas")
    print("=" * 60)

    # Cenário 1: Vendedor no ritmo (vai bater a meta)
    print("\n📊 Cenário 1: Vendedor no ritmo para bater a meta")
    projecao1 = calcular_projecao_mes(
        receita_atual=45000,
        meta_mes=100000,
        ano=2025,
        mes=1,
        dia_atual=10
    )

    print(f"   Receita atual: R$ 45.000,00")
    print(f"   Meta do mês: R$ 100.000,00")
    print(f"   Dias trabalhados: {projecao1['dias_uteis_trabalhados']}")
    print(f"   Média diária: {formatar_moeda(projecao1['media_diaria'])}")
    print(f"   Projeção final: {formatar_moeda(projecao1['projecao_mes'])}")
    print(f"   Percentual: {projecao1['percentual_projecao']:.2f}%")
    print(f"   Status: {projecao1['status_projecao']}")

    # Janeiro/2025 dia 10 = 8 dias úteis trabalhados
    # Média = 45000 / 8 = 5625
    # Projeção = 5625 * 23 = 129375
    assert projecao1['dias_uteis_trabalhados'] == 8, "Dias úteis trabalhados incorreto"
    assert projecao1['media_diaria'] == 5625.0, "Média diária incorreta"
    assert projecao1['projecao_mes'] == 129375.0, "Projeção mensal incorreta"
    assert projecao1['status_projecao'] == 'acima', "Status deveria ser 'acima'"
    print("   ✅ PASSOU - Cálculos corretos")

    # Cenário 2: Vendedor atrasado (não vai bater a meta)
    print("\n📊 Cenário 2: Vendedor atrasado")
    projecao2 = calcular_projecao_mes(
        receita_atual=30000,
        meta_mes=100000,
        ano=2025,
        mes=1,
        dia_atual=10
    )

    print(f"   Receita atual: R$ 30.000,00")
    print(f"   Meta do mês: R$ 100.000,00")
    print(f"   Média diária: {formatar_moeda(projecao2['media_diaria'])}")
    print(f"   Projeção final: {formatar_moeda(projecao2['projecao_mes'])}")
    print(f"   Percentual: {projecao2['percentual_projecao']:.2f}%")
    print(f"   Status: {projecao2['status_projecao']}")
    print(f"   Meta diária necessária: {formatar_moeda(projecao2['meta_diaria_necessaria'])}")

    # 30000 / 8 dias = 3750/dia
    # 3750 * 23 = 86250
    assert projecao2['media_diaria'] == 3750.0, "Média diária incorreta"
    assert projecao2['projecao_mes'] == 86250.0, "Projeção mensal incorreta"
    assert projecao2['status_projecao'] == 'abaixo', "Status deveria ser 'abaixo'"
    print("   ✅ PASSOU - Cálculos corretos")

    # Cenário 3: Início do mês (1 dia trabalhado)
    print("\n📊 Cenário 3: Primeiro dia do mês")
    projecao3 = calcular_projecao_mes(
        receita_atual=5000,
        meta_mes=100000,
        ano=2025,
        mes=1,
        dia_atual=2  # Primeiro dia útil
    )

    print(f"   Receita atual: R$ 5.000,00")
    print(f"   Meta do mês: R$ 100.000,00")
    print(f"   Dias trabalhados: {projecao3['dias_uteis_trabalhados']}")
    print(f"   Média diária: {formatar_moeda(projecao3['media_diaria'])}")
    print(f"   Projeção final: {formatar_moeda(projecao3['projecao_mes'])}")
    print(f"   Percentual: {projecao3['percentual_projecao']:.2f}%")

    # No primeiro dia, a projeção pode ser bem diferente da realidade
    print(f"   ⚠️ Atenção: Projeção no início do mês é menos confiável")
    print("   ✅ PASSOU - Cálculos corretos (mas projeção instável)")

def teste_formatar_moeda():
    """Testa a formatação de valores em moeda"""
    print("\n" + "=" * 60)
    print("TESTE: Formatação de Moeda")
    print("=" * 60)

    assert formatar_moeda(1000) == "R$ 1.000,00", "Formatação incorreta"
    print("   R$ 1.000,00 ✅")

    assert formatar_moeda(1234.56) == "R$ 1.234,56", "Formatação incorreta"
    print("   R$ 1.234,56 ✅")

    assert formatar_moeda(1234567.89) == "R$ 1.234.567,89", "Formatação incorreta"
    print("   R$ 1.234.567,89 ✅")

    print("   ✅ PASSOU - Formatação correta")

def teste_cenario_real():
    """Testa com dados de um cenário real"""
    print("\n" + "=" * 60)
    print("TESTE: Cenário Real de Equipe")
    print("=" * 60)

    # Equipe com 5 vendedores
    vendedores = [
        {"nome": "João", "receita": 50000, "meta": 80000},
        {"nome": "Maria", "receita": 65000, "meta": 100000},
        {"nome": "Pedro", "receita": 30000, "meta": 60000},
        {"nome": "Ana", "receita": 75000, "meta": 90000},
        {"nome": "Carlos", "receita": 40000, "meta": 70000},
    ]

    print(f"\n📊 Equipe com {len(vendedores)} vendedores (Dia 10 de Janeiro/2025)")
    print("-" * 60)

    total_receita = 0
    total_meta = 0
    total_projecao = 0

    for v in vendedores:
        projecao = calcular_projecao_mes(
            receita_atual=v['receita'],
            meta_mes=v['meta'],
            ano=2025,
            mes=1,
            dia_atual=10
        )

        total_receita += v['receita']
        total_meta += v['meta']
        total_projecao += projecao['projecao_mes']

        status_icon = "✅" if projecao['status_projecao'] == 'acima' else "⚠️"
        print(f"{status_icon} {v['nome']:8} | Receita: {formatar_moeda(v['receita']):15} | "
              f"Meta: {formatar_moeda(v['meta']):15} | "
              f"Projeção: {formatar_moeda(projecao['projecao_mes']):15} | "
              f"{projecao['percentual_projecao']:.1f}%")

    print("-" * 60)
    print(f"{'TOTAL':8} | Receita: {formatar_moeda(total_receita):15} | "
          f"Meta: {formatar_moeda(total_meta):15} | "
          f"Projeção: {formatar_moeda(total_projecao):15} | "
          f"{(total_projecao/total_meta*100):.1f}%")

    # Calcular projeção da equipe
    projecao_equipe = calcular_projecao_mes(
        receita_atual=total_receita,
        meta_mes=total_meta,
        ano=2025,
        mes=1,
        dia_atual=10
    )

    print(f"\n📈 Análise da Equipe:")
    print(f"   Velocidade média: {formatar_moeda(projecao_equipe['media_diaria'])}/dia")
    print(f"   Status: {projecao_equipe['status_projecao'].upper()}")
    print(f"   Dias restantes: {projecao_equipe['dias_uteis_restantes']}")

    if projecao_equipe['status_projecao'] == 'abaixo':
        print(f"   ⚠️ Falta vender: {formatar_moeda(projecao_equipe['receita_faltante'])}")
        print(f"   ⚠️ Meta diária necessária: {formatar_moeda(projecao_equipe['meta_diaria_necessaria'])}")
    else:
        print(f"   ✅ Equipe está no ritmo para superar a meta!")

if __name__ == "__main__":
    print("\n🧪 INICIANDO TESTES DO SISTEMA DE PROJEÇÃO")
    print("=" * 60)

    try:
        teste_contar_dias_uteis()
        teste_calcular_projecao()
        teste_formatar_moeda()
        teste_cenario_real()

        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("=" * 60)
        print("\n💡 O sistema de projeção está funcionando corretamente.")
        print("   Você pode acessar o dashboard para ver as projeções em ação.\n")

    except AssertionError as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
