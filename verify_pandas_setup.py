import sys
import os
import importlib.util

def check_package(package_name):
    print(f"Verificando {package_name}...", end=" ")
    try:
        pkg = importlib.import_module(package_name)
        print(f"✅ Instalado (Versão: {getattr(pkg, '__version__', 'N/A')})")
        return True
    except ImportError as e:
        print(f"❌ Erro: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    print("="*50)
    print("VERIFICAÇÃO DE AMBIENTE PANDAS/EXCEL")
    print("="*50)
    
    print(f"Python Version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print("-" * 30)

    packages = ['pandas', 'numpy', 'openpyxl']
    all_ok = True

    for pkg in packages:
        if not check_package(pkg):
            all_ok = False

    print("-" * 30)
    
    # Verificar dependências de sistema (Linux)
    if sys.platform.startswith('linux'):
        print("Verificando bibliotecas de sistema (Linux)...")
        try:
            import ctypes.util
            libopenblas = ctypes.util.find_library('openblas')
            print(f"OpenBLAS: {'✅ Encontrado' if libopenblas else '⚠️ Não encontrado (pode causar erro no numpy)'}")
            
            # Verificar libstdc++
            libstdc = ctypes.util.find_library('stdc++')
            print(f"libstdc++: {'✅ Encontrado' if libstdc else '❌ Não encontrado (CRÍTICO)'}")
            
            if not libstdc:
                print("   Tentando localizar manualmente...")
                os.system("find /nix/store -name libstdc++.so.6 2>/dev/null | head -n 3")
                print("   LD_LIBRARY_PATH atual:", os.environ.get('LD_LIBRARY_PATH', 'N/A'))
        except:
            print("Não foi possível verificar bibliotecas de sistema.")

    print("-" * 30)
    if all_ok:
        print("✅ TUDO PRONTO! O ambiente suporta importação/exportação Excel.")
        
        # Teste rápido
        try:
            import pandas as pd
            from io import BytesIO
            print("Teste funcional: Criando DataFrame e exportando para Excel...", end=" ")
            df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer)
            print("✅ Sucesso!")
        except Exception as e:
            print(f"❌ Falha no teste funcional: {e}")
    else:
        print("❌ PROBLEMAS DETECTADOS. Verifique o requirements.txt e nixpacks.toml.")

if __name__ == "__main__":
    main()
