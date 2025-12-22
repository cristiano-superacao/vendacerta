# pdf_generator.py - Geração de relatórios em PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import io

def gerar_pdf_metas(metas, mes, ano):
    """Gera PDF com relatório de metas"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm
    )
    elements = []
    styles = getSampleStyleSheet()

    # Estilo customizado para título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    # Estilo para subtítulo
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#4a5568'),
        spaceAfter=20,
        alignment=TA_CENTER
    )

    # Cabeçalho
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    titulo = Paragraph("Relatório de Metas e Comissões", title_style)
    subtitulo = Paragraph(f"Período: {meses[mes-1]}/{ano}", subtitle_style)
    data_emissao = Paragraph(
        f"Emitido em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
        styles['Normal']
    )

    elements.append(titulo)
    elements.append(subtitulo)
    elements.append(data_emissao)
    elements.append(Spacer(1, 0.5*cm))

    if not metas:
        sem_dados = Paragraph(
            "Nenhuma meta encontrada para este período.",
            styles['Normal']
        )
        elements.append(sem_dados)
    else:
        # Calcular totais
        total_meta = sum(m.valor_meta for m in metas)
        total_receita = sum(m.receita_alcancada for m in metas)
        total_comissao = sum(m.comissao_total for m in metas)

        # Calcular percentuais para o resumo
        percentual_alcance_geral = (
            (total_receita / total_meta * 100) if total_meta > 0 else 0
        )
        percentual_comissao = (
            (total_comissao / total_receita * 100)
            if total_receita > 0 else 0
        )

        # Resumo com percentuais
        resumo_data = [
            ['Resumo do Período', '', '', ''],
            [
                'Total de Vendedores', 'Meta Total',
                'Receita Total', 'Comissão Total'
            ],
            [
                str(len(metas)),
                f'R$ {total_meta:,.2f}',
                (
                    f'R$ {total_receita:,.2f}\n'
                    f'({percentual_alcance_geral:.1f}% da meta)'
                ),
                (
                    f'R$ {total_comissao:,.2f}\n'
                    f'({percentual_comissao:.2f}% da receita)'
                )
            ]
        ]

        resumo_table = Table(resumo_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e2e8f0')),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
            ('SPAN', (0, 0), (-1, 0)),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            (
                'ROWBACKGROUNDS', (0, 2), (-1, -1),
                [colors.white, colors.HexColor('#f7fafc')]
            ),
        ]))

        elements.append(resumo_table)
        elements.append(Spacer(1, 1*cm))

        # Tabela de detalhes
        detalhes_titulo = Paragraph("Detalhamento por Vendedor",
                                    ParagraphStyle(
                                        'DetailTitle',
                                        parent=styles['Heading2'],
                                        fontSize=14,
                                        spaceAfter=10
                                    ))
        elements.append(detalhes_titulo)

        # Ordenar metas por receita para ranking
        metas_ordenadas = sorted(
            metas, key=lambda m: m.receita_alcancada, reverse=True
        )

        # Cabeçalho da tabela com Ranking e Supervisor
        table_data = [
            [
                '#', 'Vendedor', 'Supervisor', 'Meta', 'Receita',
                'Alcance', 'Comissão', 'Status'
            ]
        ]

        # Dados com ranking e supervisor
        for i, meta in enumerate(metas_ordenadas, 1):
            emoji = get_emoji_alcance(meta.percentual_alcance)
            emoji_posicao = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else f'{i}°'

            # Tratar supervisor com segurança
            try:
                supervisor = (
                    meta.vendedor.supervisor.nome
                    if meta.vendedor.supervisor
                    else 'Sem supervisor'
                )
            except AttributeError:
                supervisor = 'Sem supervisor'

            table_data.append([
                emoji_posicao,
                meta.vendedor.nome,
                supervisor,
                f'R$ {meta.valor_meta:,.2f}',
                f'R$ {meta.receita_alcancada:,.2f}',
                f'{emoji} {meta.percentual_alcance:.1f}%',
                f'R$ {meta.comissao_total:,.2f}',
                meta.status_comissao
            ])

        detail_table = Table(
            table_data,
            colWidths=[
                1.5*cm, 3.5*cm, 3*cm, 2*cm,
                2*cm, 2*cm, 2*cm, 1.5*cm
            ]
        )
        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Ranking centralizado
            # Vendedor e Supervisor à esquerda
            ('ALIGN', (1, 1), (2, -1), 'LEFT'),
            ('ALIGN', (3, 1), (-1, -1), 'CENTER'),  # Valores centralizados
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
            ('FONTSIZE', (0, 1), (-1, -1), 8),  # Texto menor para caber tudo
        ]))

        # Destacar top 3 com fundo especial
        for i in range(1, min(4, len(metas_ordenadas) + 1)):
            detail_table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (0, i), colors.HexColor('#fff5f5'))
            ]))

        # Colorir linha baseado no status
        # (coluna 7 - após adicionar ranking e supervisor)
        for i, meta in enumerate(metas_ordenadas, start=1):
            if meta.status_comissao == 'Pago':
                detail_table.setStyle(TableStyle([
                    ('BACKGROUND', (7, i), (7, i), colors.HexColor('#e6fffa'))
                ]))
            elif meta.status_comissao == 'Aprovado':
                detail_table.setStyle(TableStyle([
                    ('BACKGROUND', (7, i), (7, i), colors.HexColor('#f0fff4'))
                ]))

        elements.append(detail_table)

        # Legenda
        elements.append(Spacer(1, 0.5*cm))
        legenda = Paragraph(
            (
                "<b>Legenda de Alcance:</b> 🔴 0-50% | 🟡 51-75% | "
                "🔵 76-100% | 🟢 101-125% | 🟢 >125% | "
                "<b>Ranking:</b> 🥇 1° | 🥈 2° | 🥉 3°"
            ),
            ParagraphStyle('Legend', parent=styles['Normal'], fontSize=9)
        )
        elements.append(legenda)

    # Rodapé
    elements.append(Spacer(1, 1*cm))
    rodape = Paragraph(
        "Sistema de Gestão de Metas e Comissões © 2025",
        ParagraphStyle(
            'Footer', parent=styles['Normal'], fontSize=8,
            textColor=colors.grey, alignment=TA_CENTER
        )
    )
    elements.append(rodape)

    # Gerar PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def get_emoji_alcance(percentual):
    """Retorna emoji baseado no percentual"""
    if percentual < 50:
        return '🔴'
    elif percentual < 75:
        return '🟡'
    elif percentual < 100:
        return '🔵'
    elif percentual < 125:
        return '🟢'
    else:
        return '🟢'  # Em PDF não funciona bem com múltiplos emojis

def formatar_moeda(valor):
    """Formata valor como moeda brasileira"""
    valor_formatado = f"R$ {valor:,.2f}"
    return (
        valor_formatado
        .replace(',', '_')
        .replace('.', ',')
        .replace('_', '.')
    )

def gerar_pdf_dashboard(resumo_global, vendedores, mes=None, ano=None, equipes=None, supervisores=None):
    """
    Gera PDF COMPLETO com relatório do dashboard
    incluindo TODAS as informações
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        leftMargin=1.5*cm, rightMargin=1.5*cm
    )
    elements = []
    styles = getSampleStyleSheet()

    # Título com período
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    # Formatar período no título
    if mes and ano:
        meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril',
            'Maio', 'Junho', 'Julho', 'Agosto',
            'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        periodo_texto = f" - {meses[mes-1]}/{ano}"
    else:
        periodo_texto = ""

    titulo = Paragraph(f"Dashboard Completo{periodo_texto}", title_style)
    data_emissao = Paragraph(
        f"Emitido em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
        ParagraphStyle(
            'Date', parent=styles['Normal'],
            fontSize=9, alignment=TA_CENTER
        )
    )

    elements.append(titulo)
    elements.append(data_emissao)
    elements.append(Spacer(1, 0.5*cm))

    # ===== SEÇÃO 1: RESUMO GERAL =====
    # Calcular alcance geral e percentuais
    receita = resumo_global.get('receita_total', 0)
    meta = resumo_global.get('meta_total', 0)
    comissao = resumo_global.get('comissao_total', 0)
    alcance_geral = resumo_global.get('alcance_geral', 0)
    emoji_alcance = get_emoji_alcance(alcance_geral)
    percentual_comissao = (comissao / receita * 100) if receita > 0 else 0

    # Projeção global
    proj_global = resumo_global.get('projecao_global', {})

    resumo_data = [
        ['📊 RESUMO GERAL', '', '', ''],
        ['Total Vendedores', 'Receita Total', 'Meta Total', 'Comissão Total'],
        [
            str(resumo_global.get('total_vendedores', 0)),
            f"R$ {receita:,.2f}\n{emoji_alcance} {alcance_geral:.1f}% da meta",
            f"R$ {meta:,.2f}",
            f"R$ {comissao:,.2f}\n({percentual_comissao:.2f}% da receita)"
        ]
    ]

    resumo_table = Table(resumo_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
    resumo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e2e8f0')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('SPAN', (0, 0), (-1, 0)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 2), (-1, 2), 7),
    ]))

    elements.append(resumo_table)
    elements.append(Spacer(1, 0.4*cm))

    # ===== SEÇÃO 2: PROJEÇÃO DE VENDAS DA EQUIPE =====
    projecao_titulo = Paragraph(
        "📈 PROJEÇÃO DE VENDAS DA EQUIPE",
        ParagraphStyle(
            'SectionTitle', parent=styles['Heading2'], fontSize=11,
            textColor=colors.HexColor('#667eea'), spaceAfter=10
        )
    )
    elements.append(projecao_titulo)

    projecao_data = [
        [
            'Dias Úteis', 'Trabalhados', 'Restantes',
            'Média/Dia', 'Projeção Final', '% Projetado'
        ],
        [
            str(proj_global.get('dias_uteis_total', 0)),
            str(proj_global.get('dias_uteis_trabalhados', 0)),
            str(proj_global.get('dias_uteis_restantes', 0)),
            formatar_moeda(proj_global.get('media_diaria', 0)),
            formatar_moeda(proj_global.get('projecao_mes', 0)),
            f"{proj_global.get('percentual_projecao', 0):.1f}%"
        ]
    ]

    projecao_table = Table(
        projecao_data,
        colWidths=[2.5*cm, 2.5*cm, 2.5*cm, 2.8*cm, 2.8*cm, 2.5*cm]
    )
    projecao_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 1), (-1, 1), 7),
    ]))

    elements.append(projecao_table)
    elements.append(Spacer(1, 0.5*cm))

    # ===== SEÇÃO 3: RANKING DE EQUIPES =====
    if equipes:
        equipes_titulo = Paragraph(
            "👥 RANKING DE EQUIPES/MESAS",
            ParagraphStyle('SectionTitle', parent=styles['Heading2'], fontSize=11,
                          textColor=colors.HexColor('#667eea'), spaceAfter=10)
        )
        elements.append(equipes_titulo)

        equipes_data = [[
            '#', 'Equipe', 'Vendedores', 'Receita',
            'Meta', 'Alcance', 'Projeção'
        ]]

        for i, eq in enumerate(equipes[:10], 1):
            emoji_posicao = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else f'{i}°'
            emoji_alc = get_emoji_alcance(eq['percentual_alcance'])

            equipes_data.append([
                emoji_posicao,
                eq['nome'][:20],
                str(eq['vendedores_count']),
                f"R$ {eq['receita_total']:,.0f}",
                f"R$ {eq['meta_total']:,.0f}",
                f"{emoji_alc} {eq['percentual_alcance']:.0f}%",
                formatar_moeda(eq['projecao'].get('projecao_mes', 0))
            ])

        equipes_table = Table(equipes_data, colWidths=[1.2*cm, 3.5*cm, 2*cm, 2.3*cm, 2.3*cm, 2.2*cm, 2.3*cm])
        equipes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0ea5e9')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
        ]))

        # Destacar top 3
        for i in range(1, min(4, len(equipes) + 1)):
            equipes_table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (0, i), colors.HexColor('#fef3c7'))
            ]))

        elements.append(equipes_table)
        elements.append(Spacer(1, 0.4*cm))

    # ===== SEÇÃO 4: RANKING DE SUPERVISORES =====
    if supervisores:
        supervisores_titulo = Paragraph(
            "🏆 RANKING DE SUPERVISORES",
            ParagraphStyle('SectionTitle', parent=styles['Heading2'], fontSize=11,
                          textColor=colors.HexColor('#667eea'), spaceAfter=10)
        )
        elements.append(supervisores_titulo)

        supervisores_data = [['#', 'Supervisor', 'Vendedores', 'Receita', 'Meta', 'Alcance', 'Média/Dia']]

        for i, sup in enumerate(supervisores[:10], 1):
            emoji_posicao = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else f'{i}°'
            emoji_alc = get_emoji_alcance(sup['percentual_alcance'])

            supervisores_data.append([
                emoji_posicao,
                sup['nome'][:20],
                str(sup['vendedores_count']),
                f"R$ {sup['receita_total']:,.0f}",
                f"R$ {sup['meta_total']:,.0f}",
                f"{emoji_alc} {sup['percentual_alcance']:.0f}%",
                formatar_moeda(sup['projecao'].get('media_diaria', 0))
            ])

        supervisores_table = Table(supervisores_data, colWidths=[1.2*cm, 3.5*cm, 2*cm, 2.3*cm, 2.3*cm, 2.2*cm, 2.3*cm])
        supervisores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
        ]))

        # Destacar top 3
        for i in range(1, min(4, len(supervisores) + 1)):
            supervisores_table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (0, i), colors.HexColor('#fef3c7'))
            ]))

        elements.append(supervisores_table)
        elements.append(Spacer(1, 0.4*cm))

    # ===== SEÇÃO 5: RANKING COMPLETO DE VENDEDORES =====
    if vendedores:
        vendedores_titulo = Paragraph(
            f"🎯 RANKING DE VENDEDORES ({len(vendedores)} vendedores)",
            ParagraphStyle('SectionTitle', parent=styles['Heading2'], fontSize=11,
                          textColor=colors.HexColor('#667eea'), spaceAfter=10)
        )
        elements.append(vendedores_titulo)

        vendedores_data = [['#', 'Vendedor', 'Equipe', 'Receita', 'Meta', 'Alcance', 'Projeção']]

        for i, v in enumerate(vendedores[:20], 1):  # Top 20 para o PDF
            emoji_posicao = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else f'{i}°'
            emoji_alc = get_emoji_alcance(v['percentual'])

            vendedores_data.append([
                emoji_posicao,
                v['nome'][:18],
                v['equipe'][:12],
                f"R$ {v['receita']:,.0f}",
                f"R$ {v['meta']:,.0f}",
                f"{emoji_alc} {v['percentual']:.0f}%",
                formatar_moeda(v['projecao'].get('projecao_mes', 0))
            ])

        vendedores_table = Table(vendedores_data, colWidths=[1.2*cm, 3*cm, 2.5*cm, 2.3*cm, 2.3*cm, 2*cm, 2.5*cm])
        vendedores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (2, -1), 'LEFT'),
            ('ALIGN', (3, 1), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
            ('FONTSIZE', (0, 1), (-1, -1), 6),
        ]))

        # Destacar top 3
        for i in range(1, min(4, len(vendedores) + 1)):
            vendedores_table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (0, i), colors.HexColor('#fef3c7'))
            ]))

        elements.append(vendedores_table)

    # Rodapé
    elements.append(Spacer(1, 0.5*cm))
    rodape = Paragraph(
        "Sistema de Gestão de Metas e Comissões © 2025 | Relatório Completo do Dashboard",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=7,
                      textColor=colors.grey, alignment=TA_CENTER)
    )
    elements.append(rodape)

    # Gerar PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

    doc.build(elements)
    buffer.seek(0)
    return buffer
