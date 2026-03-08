# Script de Verificação de Rotas e Templates
# Verifica quais templates estão faltando

import os
import re

def extract_routes_from_app():
    """Extrai todas as rotas do app.py"""
    routes_info = []

    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Padrão para rotas que renderizam templates
    template_pattern = r"render_template\('([^']+)'"
    templates_used = re.findall(template_pattern, content)

    return set(templates_used)

def check_existing_templates():
    """Verifica quais templates existem"""
    existing_templates = set()

    for root, dirs, files in os.walk('templates'):
        for file in files:
            if file.endswith('.html'):
                rel_path = os.path.relpath(os.path.join(root, file), 'templates')
                rel_path = rel_path.replace('\\', '/')
                existing_templates.add(rel_path)

    return existing_templates

def main():
    print("=" * 80)
    print("VERIFICAÇÃO DE ROTAS E TEMPLATES")
    print("=" * 80)

    templates_used = extract_routes_from_app()
    existing_templates = check_existing_templates()

    print(f"\n✓ Templates usados no app.py: {len(templates_used)}")
    print(f"✓ Templates existentes: {len(existing_templates)}")

    # Templates faltando
    missing = templates_used - existing_templates

    if missing:
        print(f"\n⚠️  TEMPLATES FALTANDO ({len(missing)}):")
        for template in sorted(missing):
            print(f"   - {template}")
    else:
        print("\n✓ Todos os templates necessários existem!")

    # Templates extras (não usados)
    extra = existing_templates - templates_used

    if extra:
        print(f"\n📋 Templates extras não referenciados ({len(extra)}):")
        for template in sorted(extra):
            print(f"   - {template}")

    print("\n" + "=" * 80)
    print("VERIFICAÇÃO CONCLUÍDA")
    print("=" * 80)

if __name__ == '__main__':
    main()
