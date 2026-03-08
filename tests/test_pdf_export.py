#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste da Exportação de PDF do Dashboard
"""

import os

from pdf_generator import gerar_pdf_dashboard
from calculo_projecao import calcular_projecao_mes
from datetime import datetime

def test_pdf_completo():
    """Testa a geração de PDF com todas as seções"""
    print("🧪 Testando geração de PDF do Dashboard...")
    
    # Dados de teste
    resumo = {
        'total_vendedores': 25,
        'receita_total': 125000.00,
        'meta_total': 150000.00,
        'comissao_total': 6250.00,
        'alcance_geral': 83.33,
        'projecao_global': {
            'dias_uteis_total': 22,
            'dias_uteis_trabalhados': 15,
            'dias_uteis_restantes': 7,
            'media_diaria': 8333.33,
            'projecao_mes': 183333.26,
            'percentual_projecao': 122.22,
            'status_projecao': 'Projeção acima da meta! 🟢'
        }
    }
    
    vendedores = [
        {
            'nome': 'João Silva',
            'supervisor': 'Maria Santos',
            'equipe': 'Equipe A',
            'receita': 15000.00,
            'meta': 18000.00,
            'percentual': 83.33,
            'comissao': 750.00,
            'projecao': {
                'dias_uteis_total': 22,
                'dias_uteis_trabalhados': 15,
                'dias_uteis_restantes': 7,
                'media_diaria': 1000.00,
                'projecao_mes': 22000.00,
                'percentual_projecao': 122.22,
                'status_projecao': 'Projeção acima da meta! 🟢'
            }
        },
        {
            'nome': 'Pedro Oliveira',
            'supervisor': 'Maria Santos',
            'equipe': 'Equipe A',
            'receita': 12000.00,
            'meta': 15000.00,
            'percentual': 80.00,
            'comissao': 600.00,
            'projecao': {
                'dias_uteis_total': 22,
                'dias_uteis_trabalhados': 15,
                'dias_uteis_restantes': 7,
                'media_diaria': 800.00,
                'projecao_mes': 17600.00,
                'percentual_projecao': 117.33,
                'status_projecao': 'Projeção acima da meta! 🟢'
            }
        }
    ]
    
    equipes = [
        {
            'nome': 'Equipe A',
            'vendedores_count': 10,
            'receita_total': 50000.00,
            'meta_total': 60000.00,
            'percentual_alcance': 83.33,
            'projecao': {
                'dias_uteis_total': 22,
                'dias_uteis_trabalhados': 15,
                'dias_uteis_restantes': 7,
                'media_diaria': 3333.33,
                'projecao_mes': 73333.26,
                'percentual_projecao': 122.22,
                'status_projecao': 'Projeção acima da meta! 🟢'
            }
        },
        {
            'nome': 'Equipe B',
            'vendedores_count': 8,
            'receita_total': 40000.00,
            'meta_total': 48000.00,
            'percentual_alcance': 83.33,
            'projecao': {
                'dias_uteis_total': 22,
                'dias_uteis_trabalhados': 15,
                'dias_uteis_restantes': 7,
                'media_diaria': 2666.67,
                'projecao_mes': 58666.74,
                'percentual_projecao': 122.22,
                'status_projecao': 'Projeção acima da meta! 🟢'
            }
        }
    ]
    
    supervisores = [
        {
            'nome': 'Maria Santos',
            'vendedores_count': 10,
            'receita_total': 50000.00,
            'meta_total': 60000.00,
            'percentual_alcance': 83.33,
            'projecao': {
                'dias_uteis_total': 22,
                'dias_uteis_trabalhados': 15,
                'dias_uteis_restantes': 7,
                'media_diaria': 3333.33,
                'projecao_mes': 73333.26,
                'percentual_projecao': 122.22,
                'status_projecao': 'Projeção acima da meta! 🟢'
            }
        },
        {
            'nome': 'Carlos Mendes',
            'vendedores_count': 8,
            'receita_total': 40000.00,
            'meta_total': 48000.00,
            'percentual_alcance': 83.33,
            'projecao': {
                'dias_uteis_total': 22,
                'dias_uteis_trabalhados': 15,
                'dias_uteis_restantes': 7,
                'media_diaria': 2666.67,
                'projecao_mes': 58666.74,
                'percentual_projecao': 122.22,
                'status_projecao': 'Projeção acima da meta! 🟢'
            }
        }
    ]
    
    try:
        # Testar geração do PDF
        pdf_buffer = gerar_pdf_dashboard(
            resumo, 
            vendedores, 
            12,  # dezembro
            2025, 
            equipes, 
            supervisores
        )
        
        if pdf_buffer:
            pdf_buffer.seek(0)
            pdf_bytes = pdf_buffer.read()
            assert pdf_bytes.startswith(b"%PDF"), "Buffer gerado não parece ser um PDF válido"
            assert len(pdf_bytes) > 1000, "PDF gerado muito pequeno; pode indicar falha na geração"

            if os.getenv("WRITE_TEST_PDF") == "1":
                with open("test_dashboard.pdf", "wb") as f:
                    f.write(pdf_bytes)
            print("✅ PDF gerado com sucesso!")
            if os.getenv("WRITE_TEST_PDF") == "1":
                print("📄 Arquivo salvo: test_dashboard.pdf")
            print(f"📊 Resumo:")
            print(f"   - Total Vendedores: {resumo['total_vendedores']}")
            print(f"   - Receita: R$ {resumo['receita_total']:,.2f}")
            print(f"   - Meta: R$ {resumo['meta_total']:,.2f}")
            print(f"   - Alcance: {resumo['alcance_geral']:.1f}%")
            print(f"   - Vendedores no PDF: {len(vendedores)}")
            print(f"   - Equipes no PDF: {len(equipes)}")
            print(f"   - Supervisores no PDF: {len(supervisores)}")
            return True
        else:
            print("❌ PDF não foi gerado (buffer vazio)")
            return False
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    sucesso = test_pdf_completo()
    exit(0 if sucesso else 1)
