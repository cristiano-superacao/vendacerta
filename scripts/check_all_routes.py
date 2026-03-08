import re
from pathlib import Path

# Ler app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar rotas e templates por bloco de função.
# - Suporta decorators adicionais entre @app.route e def
# - Suporta render_template com quebra de linha após "("
route_block_pattern = re.compile(
    r"^@app\.route\(\s*['\"](?P<route>[^'\"]+)['\"]"  # rota
    r"[^\n]*\)\s*\n"  # fim do decorator
    r"(?:^@[^\n]+\n)*"  # outros decorators
    r"^def\s+\w+\s*\([^\)]*\)\s*:\s*\n"  # assinatura da função
    r"(?P<body>(?:^(?!@app\.route\(|def\s).*(?:\n|$))*)",  # corpo até próxima def/route
    re.MULTILINE,
)

template_pattern = re.compile(r"render_template\(\s*['\"](?P<tpl>[^'\"]+)['\"]", re.MULTILINE)

rotas_templates = []

for m in route_block_pattern.finditer(content):
    route = m.group('route')
    body = m.group('body') or ''
    for tm in template_pattern.finditer(body):
        template_name = tm.group('tpl')
        # Melhor esforço: linha aproximada (início do bloco + offset do match)
        line_no = content[: (m.start('body') + tm.start())].count('\n') + 1
        rotas_templates.append({'rota': route, 'template': template_name, 'linha': line_no})

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
