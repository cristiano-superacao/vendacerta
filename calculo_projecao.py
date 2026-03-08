# calculo_projecao.py
"""
Módulo para cálculo de projeções de vendas baseadas em dias úteis
"""

from datetime import datetime, timedelta
import calendar

def contar_dias_uteis(ano, mes, dia_atual=None):
    """
    Conta os dias úteis de um mês (segunda a sexta)

    Args:
        ano: Ano do mês
        mes: Mês (1-12)
        dia_atual: Dia atual para calcular dias úteis até hoje (opcional)

    Returns:
        tuple: (dias_uteis_total, dias_uteis_trabalhados)
    """
    # Obter primeiro e último dia do mês
    primeiro_dia = datetime(ano, mes, 1)
    ultimo_dia = datetime(ano, mes, calendar.monthrange(ano, mes)[1])

    # Se dia_atual não for fornecido, usar hoje
    if dia_atual is None:
        dia_atual = datetime.now().day

    # Limitar dia_atual ao último dia do mês
    dia_atual = min(dia_atual, ultimo_dia.day)

    # Contar dias úteis totais do mês
    dias_uteis_total = 0
    dia_corrente = primeiro_dia

    while dia_corrente <= ultimo_dia:
        # Segunda (0) a Sexta (4)
        if dia_corrente.weekday() < 5:
            dias_uteis_total += 1
        dia_corrente += timedelta(days=1)

    # Contar dias úteis trabalhados até o dia atual
    dias_uteis_trabalhados = 0
    dia_corrente = primeiro_dia
    data_limite = datetime(ano, mes, dia_atual)

    while dia_corrente <= data_limite:
        if dia_corrente.weekday() < 5:
            dias_uteis_trabalhados += 1
        dia_corrente += timedelta(days=1)

    return dias_uteis_total, dias_uteis_trabalhados

def calcular_projecao_mes(receita_atual, meta_mes, ano, mes, dia_atual=None):
    """
    Calcula a projeção de vendas para o mês baseada no desempenho atual

    Args:
        receita_atual: Receita alcançada até o momento
        meta_mes: Meta do mês
        ano: Ano atual
        mes: Mês atual (1-12)
        dia_atual: Dia atual (opcional, padrão é hoje)

    Returns:
        dict: Dicionário com informações de projeção
    """
    if dia_atual is None:
        dia_atual = datetime.now().day

    dias_uteis_total, dias_uteis_trabalhados = contar_dias_uteis(ano, mes, dia_atual)

    # Evitar divisão por zero
    if dias_uteis_trabalhados == 0:
        media_diaria = 0
        projecao_mes = 0
        percentual_projecao = 0
    else:
        # Média de vendas por dia útil
        media_diaria = receita_atual / dias_uteis_trabalhados

        # Projeção para o mês completo
        projecao_mes = media_diaria * dias_uteis_total

        # Percentual da projeção em relação à meta
        percentual_projecao = (projecao_mes / meta_mes * 100) if meta_mes > 0 else 0

    # Dias úteis restantes
    dias_uteis_restantes = dias_uteis_total - dias_uteis_trabalhados

    # Receita necessária por dia para bater a meta
    receita_faltante = max(0, meta_mes - receita_atual)

    if dias_uteis_restantes > 0:
        meta_diaria_necessaria = receita_faltante / dias_uteis_restantes
    else:
        meta_diaria_necessaria = 0

    return {
        'media_diaria': media_diaria,
        'projecao_mes': projecao_mes,
        'percentual_projecao': percentual_projecao,
        'dias_uteis_total': dias_uteis_total,
        'dias_uteis_trabalhados': dias_uteis_trabalhados,
        'dias_uteis_restantes': dias_uteis_restantes,
        'meta_diaria_necessaria': meta_diaria_necessaria,
        'receita_faltante': receita_faltante,
        'status_projecao': 'acima' if percentual_projecao >= 100 else 'abaixo'
    }

def calcular_projecao_semana(receita_semanal, dias_uteis_semana, meta_mes, ano, mes):
    """
    Calcula projeção semanal

    Args:
        receita_semanal: Receita da semana atual
        dias_uteis_semana: Dias úteis trabalhados nesta semana
        meta_mes: Meta do mês
        ano: Ano atual
        mes: Mês atual

    Returns:
        dict: Informações da projeção semanal
    """
    if dias_uteis_semana == 0:
        return {
            'media_diaria_semana': 0,
            'projecao_mes_por_semana': 0,
            'ritmo_semana': 'baixo'
        }

    # Média diária da semana
    media_diaria_semana = receita_semanal / dias_uteis_semana

    # Projetar para o mês baseado no ritmo da semana
    dias_uteis_total, _ = contar_dias_uteis(ano, mes)
    projecao_mes_por_semana = media_diaria_semana * dias_uteis_total

    # Avaliar ritmo
    percentual_semana = (projecao_mes_por_semana / meta_mes * 100) if meta_mes > 0 else 0

    if percentual_semana >= 100:
        ritmo_semana = 'alto'
    elif percentual_semana >= 75:
        ritmo_semana = 'médio'
    else:
        ritmo_semana = 'baixo'

    return {
        'media_diaria_semana': media_diaria_semana,
        'projecao_mes_por_semana': projecao_mes_por_semana,
        'percentual_semana': percentual_semana,
        'ritmo_semana': ritmo_semana
    }

def formatar_moeda(valor):
    """
    Formata valor para moeda brasileira

    Args:
        valor: Valor numérico

    Returns:
        str: Valor formatado (ex: R$ 1.234,56)
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
