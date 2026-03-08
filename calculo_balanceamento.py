"""
Módulo de cálculo de balanceamento de metas
- Média simples
- Média ponderada
- Análise de tendência
"""

from datetime import datetime, timedelta
from sqlalchemy import func, extract
from app import db
from models import CompraCliente, Vendedor

def calcular_meta_balanceada(vendedor_id, periodo_historico=6, tipo_balanceamento='simples'):
    """
    Calcula meta balanceada baseada no histórico de vendas
    
    Args:
        vendedor_id: ID do vendedor
        periodo_historico: Quantidade de meses para análise (3-12)
        tipo_balanceamento: 'simples', 'ponderado' ou 'tendencia'
    
    Returns:
        dict com dados calculados
    """
    
    # Validar período
    if periodo_historico < 3:
        periodo_historico = 3
    elif periodo_historico > 12:
        periodo_historico = 12
    
    # Data de referência
    hoje = datetime.now()
    data_inicio = hoje - timedelta(days=30 * periodo_historico)
    
    # Buscar vendas do período histórico
    vendas_historico = db.session.query(
        extract('year', CompraCliente.data_compra).label('ano'),
        extract('month', CompraCliente.data_compra).label('mes'),
        func.sum(CompraCliente.valor).label('total_valor'),
        func.count(CompraCliente.id).label('total_volume')
    ).filter(
        CompraCliente.vendedor_id == vendedor_id,
        CompraCliente.data_compra >= data_inicio
    ).group_by('ano', 'mes').order_by('ano', 'mes').all()
    
    if not vendas_historico:
        return {
            'meta_valor': 0,
            'meta_volume': 0,
            'media_mensal_valor': 0,
            'media_mensal_volume': 0,
            'tendencia': 0,
            'historico': [],
            'meses_analisados': 0
        }
    
    # Calcular baseado no tipo de balanceamento
    if tipo_balanceamento == 'ponderado':
        resultado = _calcular_media_ponderada(vendas_historico)
    elif tipo_balanceamento == 'tendencia':
        resultado = _calcular_com_tendencia(vendas_historico)
    else:  # simples
        resultado = _calcular_media_simples(vendas_historico)
    
    # Adicionar histórico detalhado
    resultado['historico'] = [
        {
            'ano': int(v.ano),
            'mes': int(v.mes),
            'mes_nome': _nome_mes(int(v.mes)),
            'total_valor': float(v.total_valor or 0),
            'total_volume': int(v.total_volume or 0)
        }
        for v in vendas_historico
    ]
    resultado['meses_analisados'] = len(vendas_historico)
    resultado['periodo_historico'] = periodo_historico
    resultado['tipo_balanceamento'] = tipo_balanceamento
    
    return resultado


def _calcular_media_simples(vendas_historico):
    """Calcula média simples do histórico"""
    
    total_valor = sum([v.total_valor or 0 for v in vendas_historico])
    total_volume = sum([v.total_volume or 0 for v in vendas_historico])
    meses_com_venda = len(vendas_historico)
    
    media_valor = total_valor / meses_com_venda if meses_com_venda > 0 else 0
    media_volume = total_volume / meses_com_venda if meses_com_venda > 0 else 0
    
    return {
        'meta_valor': round(media_valor, 2),
        'meta_volume': int(media_volume),
        'media_mensal_valor': round(media_valor, 2),
        'media_mensal_volume': int(media_volume),
        'tendencia': 0  # Média simples não calcula tendência
    }


def _calcular_media_ponderada(vendas_historico):
    """
    Calcula média ponderada dando mais peso aos meses recentes
    Pesos crescentes: mês mais recente tem peso maior
    """
    
    n = len(vendas_historico)
    
    # Gerar pesos crescentes (1, 1.2, 1.4, 1.6, 1.8, 2.0)
    pesos = [1 + (i * 0.2) for i in range(n)]
    
    soma_valor_ponderada = 0
    soma_volume_ponderada = 0
    soma_pesos = sum(pesos)
    
    for i, venda in enumerate(vendas_historico):
        peso = pesos[i]
        soma_valor_ponderada += (venda.total_valor or 0) * peso
        soma_volume_ponderada += (venda.total_volume or 0) * peso
    
    media_valor = soma_valor_ponderada / soma_pesos if soma_pesos > 0 else 0
    media_volume = soma_volume_ponderada / soma_pesos if soma_pesos > 0 else 0
    
    return {
        'meta_valor': round(media_valor, 2),
        'meta_volume': int(media_volume),
        'media_mensal_valor': round(media_valor, 2),
        'media_mensal_volume': int(media_volume),
        'tendencia': 0  # Pode ser calculado separadamente
    }


def _calcular_com_tendencia(vendas_historico):
    """
    Calcula meta considerando tendência de crescimento/queda
    Usa regressão linear simples
    """
    
    n = len(vendas_historico)
    
    if n < 2:
        return _calcular_media_simples(vendas_historico)
    
    # Preparar dados para regressão linear
    valores = [float(v.total_valor or 0) for v in vendas_historico]
    volumes = [int(v.total_volume or 0) for v in vendas_historico]
    
    # Calcular regressão linear manualmente (y = ax + b)
    # x = índice do mês (0, 1, 2, ...)
    # y = valor/volume
    
    x_vals = list(range(n))
    
    # Para valores
    x_mean = sum(x_vals) / n
    y_mean_valor = sum(valores) / n
    
    numerador_valor = sum([(x_vals[i] - x_mean) * (valores[i] - y_mean_valor) for i in range(n)])
    denominador = sum([(x - x_mean) ** 2 for x in x_vals])
    
    if denominador != 0:
        coef_angular_valor = numerador_valor / denominador
        coef_linear_valor = y_mean_valor - (coef_angular_valor * x_mean)
        
        # Prever próximo mês
        proximo_mes = n
        meta_valor_prevista = coef_angular_valor * proximo_mes + coef_linear_valor
        
        # Tendência percentual
        tendencia_percentual = (coef_angular_valor / y_mean_valor * 100) if y_mean_valor > 0 else 0
    else:
        meta_valor_prevista = y_mean_valor
        tendencia_percentual = 0
    
    # Para volumes
    y_mean_volume = sum(volumes) / n
    numerador_volume = sum([(x_vals[i] - x_mean) * (volumes[i] - y_mean_volume) for i in range(n)])
    
    if denominador != 0:
        coef_angular_volume = numerador_volume / denominador
        coef_linear_volume = y_mean_volume - (coef_angular_volume * x_mean)
        meta_volume_prevista = coef_angular_volume * proximo_mes + coef_linear_volume
    else:
        meta_volume_prevista = y_mean_volume
    
    return {
        'meta_valor': round(max(0, meta_valor_prevista), 2),  # Não pode ser negativo
        'meta_volume': int(max(0, meta_volume_prevista)),
        'media_mensal_valor': round(y_mean_valor, 2),
        'media_mensal_volume': int(y_mean_volume),
        'tendencia': round(tendencia_percentual, 2)
    }


def obter_ranking_meses(vendedor_id, ano=None):
    """
    Retorna ranking dos melhores e piores meses de um vendedor
    
    Args:
        vendedor_id: ID do vendedor
        ano: Ano específico (None para todos os anos)
    
    Returns:
        dict com melhores e piores meses
    """
    
    if ano is None:
        ano = datetime.now().year
    
    # Buscar vendas por mês do ano
    vendas_mes = db.session.query(
        extract('month', CompraCliente.data_compra).label('mes'),
        func.sum(CompraCliente.valor).label('total_valor'),
        func.count(CompraCliente.id).label('total_volume')
    ).filter(
        CompraCliente.vendedor_id == vendedor_id,
        extract('year', CompraCliente.data_compra) == ano
    ).group_by('mes').all()
    
    if not vendas_mes:
        return {
            'melhores': [],
            'piores': [],
            'ano': ano
        }
    
    # Converter para lista de dicionários
    meses_dados = [
        {
            'mes': int(v.mes),
            'mes_nome': _nome_mes(int(v.mes)),
            'total_valor': float(v.total_valor or 0),
            'total_volume': int(v.total_volume or 0)
        }
        for v in vendas_mes
    ]
    
    # Ordenar por valor (decrescente para melhores, crescente para piores)
    melhores = sorted(meses_dados, key=lambda x: x['total_valor'], reverse=True)[:3]
    piores = sorted(meses_dados, key=lambda x: x['total_valor'])[:3]
    
    # Calcular percentuais em relação à média
    valores = [m['total_valor'] for m in meses_dados]
    media = sum(valores) / len(valores) if valores else 0
    
    for m in melhores + piores:
        m['percentual_media'] = round((m['total_valor'] / media * 100) if media > 0 else 0, 1)
    
    return {
        'melhores': melhores,
        'piores': piores,
        'ano': ano,
        'media_mensal': round(media, 2)
    }


def _nome_mes(numero_mes):
    """Converte número do mês para nome"""
    meses = [
        '', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    return meses[numero_mes] if 1 <= numero_mes <= 12 else ''


def obter_dados_grafico_evolucao(vendedor_id, periodo_meses=12):
    """
    Retorna dados para gráfico de evolução temporal
    
    Args:
        vendedor_id: ID do vendedor
        periodo_meses: Quantidade de meses para exibir
    
    Returns:
        dict com labels e dados para Chart.js
    """
    
    hoje = datetime.now()
    data_inicio = hoje - timedelta(days=30 * periodo_meses)
    
    vendas = db.session.query(
        extract('year', CompraCliente.data_compra).label('ano'),
        extract('month', CompraCliente.data_compra).label('mes'),
        func.sum(CompraCliente.valor).label('total_valor'),
        func.count(CompraCliente.id).label('total_volume')
    ).filter(
        CompraCliente.vendedor_id == vendedor_id,
        CompraCliente.data_compra >= data_inicio
    ).group_by('ano', 'mes').order_by('ano', 'mes').all()
    
    labels = []
    valores = []
    volumes = []
    
    for v in vendas:
        mes_nome = _nome_mes(int(v.mes))[:3]  # Abreviado
        ano_curto = str(int(v.ano))[2:]  # 25 para 2025
        labels.append(f"{mes_nome}/{ano_curto}")
        valores.append(float(v.total_valor or 0))
        volumes.append(int(v.total_volume or 0))
    
    return {
        'labels': labels,
        'valores': valores,
        'volumes': volumes
    }
