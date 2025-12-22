# Corrigir emojis em todos os arquivos Python para compatibilidade Windows
# Este script remove emojis que causam UnicodeEncodeError no Windows

import re
import os
from pathlib import Path

def remover_emojis_linha(linha):
    """Remove ou substitui emojis por texto ASCII"""
    substituicoes = {
        '✅': '[OK]',
        '❌': '[ERRO]',
        '⚠️': '[AVISO]',
        '📊': '[INFO]',
        '🔐': '[SEC]',
        '💬': '[MSG]',
        '📞': '[TEL]',
        '🎨': '[UI]',
        '🎯': '[META]',
        '📁': '[DIR]',
        '📄': '[FILE]',
        '🔄': '[PROC]',
        '🛑': '[STOP]',
        '⏭️': '[NEXT]',
        '⏱️': '[TIME]',
        '1️⃣': '[1]',
        '2️⃣': '[2]',
        '3️⃣': '[3]',
        '4️⃣': '[4]',
        '5️⃣': '[5]',
        '6️⃣': '[6]',
        '0️⃣': '[0]',
        '⌨️': '[KEY]',
    }
    
    for emoji, texto in substituicoes.items():
        linha = linha.replace(emoji, texto)
    
    return linha

arquivos_corrigidos = []
arquivos_analisados = 0

# Arquivos que devem ser corrigidos (somente scripts auxiliares, não o app.py principal)
arquivos_para_corrigir = [
    'backup_helper.py',
    'test_postgresql.py',
    'setup_postgresql.py',
    'migrate_to_postgresql.py',
    'quick_start.py',
    'wsgi.py',
    'teste_login.py'
]

for arquivo in arquivos_para_corrigir:
    if os.path.exists(arquivo):
        arquivos_analisados += 1
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            linhas_originais = conteudo.split('\n')
            linhas_corrigidas = [remover_emojis_linha(linha) for linha in linhas_originais]
            conteudo_corrigido = '\n'.join(linhas_corrigidas)
            
            if conteudo != conteudo_corrigido:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(conteudo_corrigido)
                arquivos_corrigidos.append(arquivo)
                print(f"[OK] {arquivo} - Corrigido")
            else:
                print(f"[OK] {arquivo} - Sem alteracoes")
                
        except Exception as e:
            print(f"[ERRO] {arquivo} - {e}")

print(f"\n=== RESUMO ===")
print(f"Arquivos analisados: {arquivos_analisados}")
print(f"Arquivos corrigidos: {len(arquivos_corrigidos)}")
if arquivos_corrigidos:
    print(f"\nArquivos modificados:")
    for arq in arquivos_corrigidos:
        print(f"  - {arq}")
