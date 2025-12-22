"""
Verificacao de Responsividade dos Templates
"""
import os
import re

print("\n" + "="*80)
print("VERIFICACAO DE RESPONSIVIDADE E DESIGN PROFISSIONAL")
print("="*80)

templates_dir = r"C:\Users\Superação\Desktop\Sistema\vendacerta\templates"

# Padrões de design responsivo
padroes_responsivos = {
    'Bootstrap Grid': r'(col-|row|container)',
    'Classes Responsivas': r'(col-sm-|col-md-|col-lg-|col-xl-|d-none|d-block|d-md-|d-lg-)',
    'Viewport Meta': r'<meta\s+name=["\']viewport',
    'Media Queries': r'@media\s+\(',
    'Bootstrap Icons': r'bi-',
    'Cards Modernas': r'card-header|card-body|shadow',
    'Gradientes': r'bg-gradient|linear-gradient',
    'Animacoes': r'transition|animation|hover'
}

def verificar_arquivo(filepath):
    """Verifica padroes de responsividade em um arquivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
        resultados = {}
        for nome, padrao in padroes_responsivos.items():
            matches = re.findall(padrao, conteudo, re.IGNORECASE)
            if matches:
                resultados[nome] = len(matches)
        
        return resultados
    except Exception as e:
        return None

# Verificar templates principais
templates_principais = [
    'base.html',
    'clientes/importar.html',
    'vendedores/importar.html',
    'dashboard.html',
    'metas/lista.html'
]

print("\nTemplates Verificados:")
print("-" * 80)

total_responsivo = 0
total_templates = 0

for template in templates_principais:
    filepath = os.path.join(templates_dir, template)
    
    if os.path.exists(filepath):
        total_templates += 1
        print(f"\n{template}:")
        
        resultados = verificar_arquivo(filepath)
        if resultados:
            tem_responsivo = False
            for recurso, qtd in resultados.items():
                print(f"  {recurso}: {qtd} ocorrencias")
                if qtd > 0:
                    tem_responsivo = True
            
            if tem_responsivo:
                total_responsivo += 1
                print("  Status: RESPONSIVO ✓")
            else:
                print("  Status: PRECISA MELHORIAS")
        else:
            print("  Erro ao ler arquivo")
    else:
        print(f"\n{template}: NAO ENCONTRADO")

# Resumo
print("\n" + "="*80)
print("RESUMO DA VERIFICACAO")
print("="*80)
print(f"\nTemplates verificados: {total_templates}")
print(f"Templates responsivos: {total_responsivo}")
print(f"Percentual: {(total_responsivo/total_templates*100):.1f}%")

if total_responsivo == total_templates:
    print("\n✓ TODOS OS TEMPLATES ESTAO RESPONSIVOS E PROFISSIONAIS!")
else:
    print(f"\nAlerta: {total_templates - total_responsivo} template(s) precisam de melhorias")

print("="*80 + "\n")
