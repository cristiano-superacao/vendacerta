#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Verificar Instalação das Bibliotecas Excel
Sistema VendaCerta
"""

import sys
import importlib

def verificar_biblioteca(nome_modulo, nome_exibicao=None):
    """Verifica se uma biblioteca está instalada e retorna sua versão"""
    if nome_exibicao is None:
        nome_exibicao = nome_modulo
    
    try:
        modulo = importlib.import_module(nome_modulo)
        versao = getattr(modulo, '__version__', 'Versão desconhecida')
        print(f"✅ {nome_exibicao}: Instalado (v{versao})")
        return True
    except ImportError as e:
        print(f"❌ {nome_exibicao}: NÃO instalado")
        print(f"   Erro: {str(e)}")
        return False
    except Exception as e:
        print(f"⚠️  {nome_exibicao}: Erro ao verificar")
        print(f"   Erro: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("VERIFICAÇÃO DE BIBLIOTECAS EXCEL - Sistema VendaCerta")
    print("=" * 60)
    print()
    
    # Lista de bibliotecas necessárias
    bibliotecas = [
        ('pandas', 'Pandas'),
        ('openpyxl', 'OpenPyXL'),
        ('numpy', 'NumPy'),
    ]
    
    resultados = []
    
    for modulo, nome in bibliotecas:
        resultado = verificar_biblioteca(modulo, nome)
        resultados.append((nome, resultado))
    
    print()
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)
    
    todas_ok = all(resultado for _, resultado in resultados)
    
    if todas_ok:
        print("✅ Todas as bibliotecas Excel estão instaladas corretamente!")
        print()
        print("🎉 O sistema está pronto para importar/exportar clientes.")
    else:
        print("❌ Algumas bibliotecas não estão instaladas.")
        print()
        print("📦 Para instalar, execute:")
        print("   pip install pandas openpyxl numpy")
        print()
        print("   ou")
        print()
        print("   pip install -r requirements.txt")
    
    print("=" * 60)
    
    # Teste de funcionalidade básica
    if todas_ok:
        print()
        print("TESTE DE FUNCIONALIDADE")
        print("=" * 60)
        
        try:
            import pandas as pd
            from openpyxl import Workbook
            from io import BytesIO
            
            # Teste 1: Criar DataFrame
            print("📝 Teste 1: Criar DataFrame... ", end="")
            df = pd.DataFrame({'Nome': ['João', 'Maria'], 'CPF': ['111.111.111-11', '222.222.222-22']})
            print("✅ OK")
            
            # Teste 2: Criar Workbook
            print("📝 Teste 2: Criar Workbook... ", end="")
            wb = Workbook()
            ws = wb.active
            ws['A1'] = 'Teste'
            print("✅ OK")
            
            # Teste 3: Exportar para Excel em memória
            print("📝 Teste 3: Exportar para Excel... ", end="")
            output = BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            print("✅ OK")
            
            print()
            print("✅ Todos os testes passaram com sucesso!")
            
        except Exception as e:
            print(f"\n❌ Erro durante os testes: {str(e)}")
    
    print("=" * 60)
    print()
    
    return 0 if todas_ok else 1

if __name__ == "__main__":
    sys.exit(main())
