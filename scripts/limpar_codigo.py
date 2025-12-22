"""
Script para limpar código removendo espaços vazios excessivos
Mantém apenas uma linha vazia entre blocos de código
"""
import re
import os
from pathlib import Path

def limpar_arquivo(caminho):
    """Remove linhas vazias consecutivas, mantendo apenas uma"""
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # Salvar conteúdo original para comparação
        original = conteudo

        # Remover múltiplas linhas vazias consecutivas, mantendo apenas uma
        # Substitui 3+ linhas vazias por 2 (uma linha vazia visual)
        conteudo = re.sub(r'\n\s*\n\s*\n+', '\n\n', conteudo)

        # Remover espaços em branco no final das linhas
        linhas = conteudo.split('\n')
        linhas = [linha.rstrip() for linha in linhas]
        conteudo = '\n'.join(linhas)

        # Garantir que o arquivo termina com uma única quebra de linha
        if conteudo and not conteudo.endswith('\n'):
            conteudo += '\n'

        # Remover múltiplas linhas vazias no final do arquivo
        conteudo = conteudo.rstrip('\n') + '\n'

        # Salvar apenas se houver mudanças
        if conteudo != original:
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(conteudo)

            linhas_removidas = original.count('\n') - conteudo.count('\n')
            return True, linhas_removidas

        return False, 0

    except Exception as e:
        print(f"Erro ao processar {caminho}: {e}")
        return False, 0

def main():
    """Limpa arquivos Python do projeto"""
    arquivos_para_limpar = [
        'app.py',
        'models.py',
        'forms.py',
        'config.py',
        'calculo_comissao.py',
        'calculo_projecao.py',
        'init_db.py',
        'init_data.py',
        'pdf_generator.py',
    ]

    base_path = Path(__file__).parent.parent
    total_arquivos = 0
    total_linhas_removidas = 0

    print("=" * 60)
    print("Limpando arquivos Python - Removendo espaços excessivos")
    print("=" * 60)

    for arquivo in arquivos_para_limpar:
        caminho = base_path / arquivo

        if not caminho.exists():
            print(f"❌ Arquivo não encontrado: {arquivo}")
            continue

        modificado, linhas_removidas = limpar_arquivo(caminho)

        if modificado:
            print(f"✅ {arquivo:<30} | {linhas_removidas:>4} linhas removidas")
            total_arquivos += 1
            total_linhas_removidas += linhas_removidas
        else:
            print(f"⏭️  {arquivo:<30} | Sem alterações")

    print("=" * 60)
    print(f"Total: {total_arquivos} arquivos modificados")
    print(f"Total: {total_linhas_removidas} linhas removidas")
    print("=" * 60)

if __name__ == '__main__':
    main()
