# calculo_comissao.py
# A tabela de faixas de comissão (usando R$ 30.000,00 como base, mas
# o percentual de comissão é aplicado sobre a Receita Alcançada,
# conforme o percentual de ALCANCE da META)
FAIXAS_COMISSAO = [
    # (Limite Superior do Alcance %, Taxa de Comissão)
    # Ex: Alcance até 50% => 1%
    {'alcance_max_perc': 50, 'taxa': 0.01},  # 1%
    # Ex: Alcance até 75% => 2%
    {'alcance_max_perc': 75, 'taxa': 0.02},  # 2%
    # Ex: Alcance até 100% => 3%
    {'alcance_max_perc': 100, 'taxa': 0.03}, # 3%
    # Ex: Alcance até 125% => 4%
    {'alcance_max_perc': 125, 'taxa': 0.04}, # 4%
    # Acima de 125% (usamos um valor grande para o max) => 5%
    {'alcance_max_perc': 1000, 'taxa': 0.05} # 5%
]

def calcular_percentual_alcance(receita_alcancada, meta_individual):
    """
    Calcula o percentual de alcance da meta.
    Fórmula: P = (Receita Alcançada / Meta Individual) * 100
    """
    if meta_individual <= 0:
        return 0.0
    return (receita_alcancada / meta_individual) * 100.0

def calcular_comissao(receita_alcancada, percentual_alcance):
    """
    Calcula a comissão total baseada no percentual de alcance.
    A comissão é a taxa da faixa atingida aplicada sobre a Receita Alcançada.
    Fórmula: C_total = Receita Alcançada * Taxa da Faixa
    """
    taxa_aplicada = 0.0

    # Itera sobre as faixas para encontrar a taxa correta
    for faixa in FAIXAS_COMISSAO:
        if percentual_alcance <= faixa['alcance_max_perc']:
            taxa_aplicada = faixa['taxa']
            break
        # Se o percentual de alcance for maior que todas as faixas (acima de 125%),
        # a última taxa (5%) será aplicada, garantida pela última entrada da lista.

    return receita_alcancada * taxa_aplicada

# Dados de exemplo (Mockup)
# Baseado nos seus exemplos, assumimos que a meta é individualizada (Opção B).
DADOS_VENDEDORES = [
    {
        'nome': 'Cristiano',
        'supervisor': 'Ana',
        'meta': 30300.00,
        'receita_alcancada': 22800.00,
        'status_comissao': 'Pendente'
    },
    {
        'nome': 'Cleo',
        'supervisor': 'Ana',
        'meta': 45000.00,
        'receita_alcancada': 30300.00,
        'status_comissao': 'Pendente'
    },
    {
        'nome': 'Novo Vendedor',
        'supervisor': 'Bruno',
        'meta': 30000.00,
        'receita_alcancada': 40000.00,
        'status_comissao': 'Pago'
    },
    {
        'nome': 'Maria Silva',
        'supervisor': 'Ana',
        'meta': 30000.00,
        'receita_alcancada': 33000.00,
        'status_comissao': 'Pendente'
    },
    {
        'nome': 'João Santos',
        'supervisor': 'Bruno',
        'meta': 35000.00,
        'receita_alcancada': 28000.00,
        'status_comissao': 'Pendente'
    },
]

def obter_dados_processados():
    """
    Processa os dados dos vendedores aplicando os cálculos de comissão.
    """
    vendedores_processados = []
    for vendedor in DADOS_VENDEDORES:
        v = vendedor.copy()

        # 1. Calcular Percentual de Alcance (P)
        p_alcance = calcular_percentual_alcance(v['receita_alcancada'], v['meta'])
        v['percentual_alcance'] = p_alcance

        # 2. Calcular Comissão Total (C_total)
        comissao = calcular_comissao(v['receita_alcancada'], p_alcance)
        v['comissao_total'] = comissao

        # Formatação para exibição (opcional, mas bom para o template)
        v['percentual_alcance_formatado'] = f"{p_alcance:.2f}%"
        v['comissao_total_formatada'] = f"R$ {comissao:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        vendedores_processados.append(v)

    # Ordena pelo percentual de alcance (ranking)
    return sorted(vendedores_processados, key=lambda x: x['percentual_alcance'], reverse=True)

if __name__ == '__main__':
    # Teste para verificar se os cálculos estão corretos
    dados = obter_dados_processados()
    print("\n" + "="*60)
    print("TESTE DE CÁLCULO DE COMISSÕES")
    print("="*60 + "\n")
    for d in dados:
        print(f"Vendedor: {d['nome']}")
        print(f"  Supervisor: {d['supervisor']}")
        print(f"  Receita: R$ {d['receita_alcancada']:,.2f} | Meta: R$ {d['meta']:,.2f}")
        print(f"  Alcance: {d['percentual_alcance']:.2f}%")
        print(f"  Comissão: R$ {d['comissao_total']:.2f}")
        print(f"  Status: {d['status_comissao']}")
        print("-" * 60)
