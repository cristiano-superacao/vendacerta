#!/usr/bin/env python3
"""Script para corrigir warnings PEP8 no app.py"""

import re

def fix_pep8(filepath):
    """Corrige os principais warnings PEP8"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remover espaços em branco de linhas vazias
    content = re.sub(r'\n[ \t]+\n', '\n\n', content)
    
    # 2. Garantir 2 linhas em branco antes de decorators @app.route
    content = re.sub(
        r'\n(\n)?(@app\.route)',
        r'\n\n\n\2',
        content
    )
    
    # 3. Garantir 2 linhas em branco antes de def
    content = re.sub(
        r'\n(\n)?(\ndef [a-z_]+\()',
        r'\n\n\n\2',
        content
    )
    
    # 4. Garantir 2 espaços antes de comentários inline
    content = re.sub(
        r'([a-zA-Z0-9_\)\]"\'])\s?#\s',
        r'\1  # ',
        content
    )
    
    # 5. Substituir == True por is True
    content = re.sub(
        r'(\w+)\s*==\s*True\b',
        r'\1 is True',
        content
    )
    
    # 6. Remover linhas em branco duplicadas (mais de 3 seguidas)
    content = re.sub(r'\n\n\n\n+', '\n\n\n', content)
    
    # Salvar arquivo corrigido
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Arquivo {filepath} corrigido com sucesso!")

if __name__ == '__main__':
    fix_pep8('app.py')
