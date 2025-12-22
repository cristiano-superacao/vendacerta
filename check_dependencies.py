#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Verificação de Dependências - Sistema VendaCerta
Verifica bibliotecas Excel e dependências nativas
"""

import sys
import os

def verificar_excel():
    """Verifica se as bibliotecas Excel estão funcionando"""
    print("=" * 70)
    print("🔍 VERIFICAÇÃO DE DEPENDÊNCIAS EXCEL")
    print("=" * 70)
    print()
    
    # Verificar pandas
    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__} - OK")
    except ImportError as e:
        print(f"❌ Pandas - NÃO INSTALADO")
        print(f"   Erro: {e}")
        return False
    except Exception as e:
        print(f"❌ Pandas - ERRO AO CARREGAR")
        print(f"   Erro: {e}")
        
        # Verificar se é erro de biblioteca compartilhada
        error_str = str(e)
        if "libstdc++" in error_str or ".so" in error_str:
            print()
            print("🔧 SOLUÇÃO DETECTADA:")
            print("   Erro de biblioteca compartilhada do sistema (libstdc++.so)")
            print()
            print("   Para Railway/Nixpacks, adicione ao nixpacks.toml:")
            print("   ─" * 35)
            print('   [phases.setup]')
            print('   nixPkgs = [')
            print('       "python311",')
            print('       "stdenv.cc.cc.lib",  # ← Biblioteca C++ necessária')
            print('       "openblas",')
            print('       "libgfortran"')
            print('   ]')
            print("   ─" * 35)
            print()
            print("   No comando [start], adicione:")
            print('   export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${NIXPACKS_PATH}/lib')
            print()
        
        return False
    
    # Verificar openpyxl
    try:
        import openpyxl
        print(f"✅ OpenPyXL {openpyxl.__version__} - OK")
    except ImportError as e:
        print(f"❌ OpenPyXL - NÃO INSTALADO")
        print(f"   Erro: {e}")
        return False
    except Exception as e:
        print(f"❌ OpenPyXL - ERRO AO CARREGAR")
        print(f"   Erro: {e}")
        return False
    
    # Verificar numpy
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__} - OK")
    except ImportError as e:
        print(f"❌ NumPy - NÃO INSTALADO")
        print(f"   Erro: {e}")
        return False
    except Exception as e:
        print(f"❌ NumPy - ERRO AO CARREGAR")
        print(f"   Erro: {e}")
        return False
    
    print()
    print("=" * 70)
    print("✅ TODAS AS DEPENDÊNCIAS EXCEL ESTÃO OK!")
    print("=" * 70)
    print()
    
    return True

def verificar_ambiente():
    """Verifica informações do ambiente"""
    print("📋 INFORMAÇÕES DO AMBIENTE")
    print("─" * 70)
    print(f"Python: {sys.version}")
    print(f"Plataforma: {sys.platform}")
    print(f"Executável: {sys.executable}")
    
    # Verificar LD_LIBRARY_PATH
    ld_path = os.environ.get("LD_LIBRARY_PATH", "não definido")
    print(f"LD_LIBRARY_PATH: {ld_path}")
    
    # Verificar NIXPACKS_PATH
    nixpacks_path = os.environ.get("NIXPACKS_PATH", "não definido")
    print(f"NIXPACKS_PATH: {nixpacks_path}")
    
    print("─" * 70)
    print()

def main():
    verificar_ambiente()
    
    if verificar_excel():
        print("🎉 Sistema pronto para importar/exportar Excel!")
        return 0
    else:
        print("⚠️  Algumas dependências não estão funcionando.")
        print("📖 Consulte a documentação acima para resolver.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
