import re
from pathlib import Path

# Ler app.py
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar todas as rotas e seus templates
rotas_templates = []
current_route = None
in_function = False

for i, line in enumerate(lines):
    # Detectar decorator de rota
    route_match = re.match(r"@app\.route\(['\"]([^'\"]+)['\"]", line)
    if route_match:
        current_route = route_match.group(1)
        in_function = True
        continue

    # Detectar render_template dentro da função
    if in_function and current_route:
        template_match = re.search(r"render_template\(['\"]([^'\"]+)['\"]", line)
        if template_match:
            template_name = template_match.group(1)
            rotas_templates.append({
                'rota': current_route,
                'template': template_name,
                'linha': i + 1
            })

    # Detectar fim de função (nova definição de função ou decorator)
    if re.match(r"^@app\.|^def ", line):
        if not route_match:  # Se não for um novo decorator de rota
            in_function = False
            current_route = None

# Listar templates existentes
templates_dir = Path('templates')
templates_exist = set()

for html_file in templates_dir.rglob('*.html'):
    rel_path = html_file.relative_to(templates_dir).as_posix()
    templates_exist.add(rel_path)

# Agrupar por template
templates_dict = {}
for item in rotas_templates:
    template = item['template']
    if template not in templates_dict:
        templates_dict[template] = []
    templates_dict[template].append(item['rota'])

# Verificar quais templates estão faltando
print("="*80)
print(f"ANÁLISE DE {len(set([r['rota'] for r in rotas_templates]))} ROTAS DO APP.PY")
print("="*80)
print()

missing_templates = []

for template in sorted(templates_dict.keys()):
    exists = template in templates_exist
    status = "✅ OK" if exists else "❌ FALTANDO"

    if not exists:
        missing_templates.append({
            'template': template,
            'rotas': templates_dict[template]
        })
        print(f"{status} - Template: {template}")
        for rota in templates_dict[template]:
            print(f"           Rota: {rota}")
        print()

print("="*80)
print("RESUMO")
print("="*80)
print(f"Total de templates únicos usados: {len(templates_dict)}")
print(f"Templates existentes: {len([t for t in templates_dict.keys() if t in templates_exist])}")
print(f"Templates faltando: {len(missing_templates)}")
print()

if missing_templates:
    print("="*80)
    print("LISTA DE TEMPLATES FALTANDO:")
    print("="*80)
    for item in missing_templates:
        print(f"\n- Rota: {', '.join(item['rotas'])}")
        print(f"  Template esperado: {item['template']}")
        print(f"  Status: FALTANDO")
else:
    print("✅ Todos os templates necessários estão presentes!")
