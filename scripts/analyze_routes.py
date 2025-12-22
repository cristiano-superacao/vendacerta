import re
from pathlib import Path
from collections import defaultdict

# Ler app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Extrair todas as rotas e templates
# Padrão para encontrar @app.route e render_template na mesma função
pattern = r"@app\.route\(['\"]([^'\"]+)['\"].*?\ndef\s+\w+\(.*?\):.*?(?=@app\.route|def\s+\w+\(|$)"
functions = re.findall(pattern, content, re.DOTALL)

# Para cada rota, encontrar render_template
route_template_map = []

# Método mais simples: buscar render_template com contexto
lines = content.split('\n')
current_routes = []

for i, line in enumerate(lines):
    # Capturar rotas
    if '@app.route(' in line:
        route_match = re.search(r"@app\.route\(['\"]([^'\"]+)['\"]", line)
        if route_match:
            # Pode haver múltiplas rotas para a mesma função
            route = route_match.group(1)
            # Olhar as próximas linhas para outras rotas
            j = i + 1
            routes = [route]
            while j < len(lines) and '@app.route(' in lines[j]:
                r_match = re.search(r"@app\.route\(['\"]([^'\"]+)['\"]", lines[j])
                if r_match:
                    routes.append(r_match.group(1))
                j += 1
            current_routes = routes

    # Capturar render_template
    if 'render_template(' in line and current_routes:
        template_match = re.search(r"render_template\(['\"]([^'\"]+)['\"]", line)
        if template_match:
            template = template_match.group(1)
            for route in current_routes:
                route_template_map.append({
                    'rota': route,
                    'template': template,
                    'linha': i + 1
                })

    # Reset quando encontrar nova definição de função que não seja rota
    if line.strip().startswith('def ') and not any('@app.route' in lines[i-j] for j in range(1, 5) if i-j >= 0):
        current_routes = []

# Listar templates existentes
templates_dir = Path('templates')
templates_exist = set()

for html_file in templates_dir.rglob('*.html'):
    rel_path = html_file.relative_to(templates_dir).as_posix()
    templates_exist.add(rel_path)

# Criar mapa de templates para rotas
template_routes = defaultdict(list)
for item in route_template_map:
    template_routes[item['template']].append(item['rota'])

# Encontrar templates únicos
unique_templates = sorted(set([item['template'] for item in route_template_map]))

print("="*80)
print(f"ANÁLISE COMPLETA DE ROTAS E TEMPLATES DO APP.PY")
print("="*80)
print(f"\nTotal de chamadas render_template encontradas: {len(route_template_map)}")
print(f"Total de templates únicos: {len(unique_templates)}")
print(f"Total de arquivos .html na pasta templates/: {len(templates_exist)}")
print()

# Verificar templates faltando
missing_templates = []

for template in unique_templates:
    if template not in templates_exist:
        missing_templates.append({
            'template': template,
            'rotas': template_routes[template]
        })

print("="*80)
if missing_templates:
    print(f"❌ TEMPLATES FALTANDO ({len(missing_templates)}):")
    print("="*80)
    print()

    for item in missing_templates:
        for rota in item['rotas']:
            print(f"- Rota: {rota}")
            print(f"  Template esperado: {item['template']}")
            print(f"  Status: FALTANDO")
            print()
else:
    print("✅ RESULTADO:")
    print("="*80)
    print("\n✅ Todos os templates necessários estão presentes!\n")

# Mostrar estatísticas
print("="*80)
print("ESTATÍSTICAS:")
print("="*80)
print(f"Templates necessários: {len(unique_templates)}")
print(f"Templates existentes: {len(templates_exist)}")
print(f"Templates faltando: {len(missing_templates)}")
