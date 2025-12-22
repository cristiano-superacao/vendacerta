"""
Script para corrigir automaticamente problemas de formatação do código Python.
Usa autopep8 para corrigir warnings do Flake8 mantendo layout profissional.
"""
import subprocess
import sys

def instalar_autopep8():
    """Instala autopep8 se não estiver disponível"""
    try:
        import autopep8
        print("✅ autopep8 já instalado")
        return True
    except ImportError:
        print("📦 Instalando autopep8...")
        subprocess.run([sys.executable, "-m", "pip", "install", "autopep8"], 
                      check=True, capture_output=True)
        print("✅ autopep8 instalado com sucesso")
        return True

def corrigir_arquivo(arquivo):
    """Corrige formatação de um arquivo Python"""
    try:
        import autopep8
        
        print(f"\n🔧 Corrigindo {arquivo}...")
        
        # Ler arquivo original
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo_original = f.read()
        
        # Corrigir formatação (ignora E501 - linha longa, pois pode quebrar strings)
        codigo_corrigido = autopep8.fix_code(
            codigo_original,
            options={
                'max_line_length': 79,
                'ignore': ['E501'],  # Ignora linha longa por enquanto
                'aggressive': 1
            }
        )
        
        # Salvar arquivo corrigido
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(codigo_corrigido)
        
        print(f"   ✅ {arquivo} corrigido")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao corrigir {arquivo}: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 70)
    print("CORREÇÃO AUTOMÁTICA DE FORMATAÇÃO PYTHON")
    print("=" * 70)
    
    # Instalar autopep8
    if not instalar_autopep8():
        print("❌ Não foi possível instalar autopep8")
        return
    
    # Arquivos para corrigir (somente os principais)
    arquivos = [
        'forms.py',
        'config.py',
    ]
    
    # Corrigir cada arquivo
    sucesso = 0
    falhas = 0
    
    for arquivo in arquivos:
        if corrigir_arquivo(arquivo):
            sucesso += 1
        else:
            falhas += 1
    
    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO DA CORREÇÃO")
    print("=" * 70)
    print(f"✅ Arquivos corrigidos: {sucesso}")
    print(f"❌ Falhas: {falhas}")
    print("\n⚠️  AVISOS:")
    print("- Linhas longas (>79 chars) não foram alteradas automaticamente")
    print("- Revise manualmente se necessário")
    print("- Teste o sistema após as correções: python app.py")
    print("=" * 70)

if __name__ == '__main__':
    main()
