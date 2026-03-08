# Script para limpar duplicidades e espaços vazios do sistema
import re
import os

def limpar_linhas_vazias_duplicadas(arquivo):
    """Remove linhas vazias consecutivas, mantendo apenas uma"""
    with open(arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    linhas_limpas = []
    linha_vazia_anterior = False

    for linha in linhas:
        linha_apenas_espacos = linha.strip() == ''

        if linha_apenas_espacos:
            if not linha_vazia_anterior:
                linhas_limpas.append('\n')
                linha_vazia_anterior = True
        else:
            linhas_limpas.append(linha)
            linha_vazia_anterior = False

    with open(arquivo, 'w', encoding='utf-8') as f:
        f.writelines(linhas_limpas)

    return len(linhas) - len(linhas_limpas)

def main():
    arquivos_python = []

    # Buscar todos os arquivos .py no diretório atual
    for root, dirs, files in os.walk('.'):
        # Ignorar diretórios específicos
        dirs[:] = [d for d in dirs if d not in ['.venv', 'venv', '__pycache__', '.git', 'instance']]

        for file in files:
            if file.endswith('.py'):
                arquivos_python.append(os.path.join(root, file))

    total_removidas = 0
    arquivos_processados = 0

    print("🧹 Limpando espaços vazios duplicados...\n")

    for arquivo in arquivos_python:
        try:
            removidas = limpar_linhas_vazias_duplicadas(arquivo)
            if removidas > 0:
                print(f"✅ {arquivo}: {removidas} linhas vazias removidas")
                total_removidas += removidas
                arquivos_processados += 1
        except Exception as e:
            print(f"❌ Erro em {arquivo}: {e}")

    print(f"\n📊 Resumo:")
    print(f"   Arquivos processados: {arquivos_processados}")
    print(f"   Total de linhas removidas: {total_removidas}")

if __name__ == '__main__':
    main()
