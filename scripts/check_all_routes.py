import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
APP_FILE = REPO_ROOT / "app.py"
TEMPLATES_DIR = REPO_ROOT / "templates"


def _extract_routes_and_templates(lines):
    route_pattern = re.compile(r"@app\.route\(\s*['\"]([^'\"]+)['\"]")
    template_pattern = re.compile(r"render_template\(\s*['\"]([^'\"]+)['\"]")

    route_by_func = {}
    current_routes = []

    # 1) Mapeia funcao -> rotas decoradas
    for idx, raw in enumerate(lines):
        line = raw.strip()
        m_route = route_pattern.search(line)
        if m_route:
            current_routes.append(m_route.group(1))
            continue

        m_def = re.match(r"def\s+(\w+)\s*\(", line)
        if m_def and current_routes:
            route_by_func[m_def.group(1)] = current_routes[:]
            current_routes.clear()

    # 2) Mapeia funcao -> templates usados no corpo da funcao
    templates_by_func = {}
    current_func = None

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()

        m_def = re.match(r"def\s+(\w+)\s*\(", stripped)
        if m_def:
            current_func = m_def.group(1)
            templates_by_func.setdefault(current_func, set())
            continue

        if stripped.startswith("@app.route"):
            current_func = None
            continue

        if current_func:
            for tpl in template_pattern.findall(stripped):
                templates_by_func[current_func].add(tpl)

    # 3) Monta pares rota-template
    pairs = []
    for func_name, routes in route_by_func.items():
        used_templates = sorted(templates_by_func.get(func_name, set()))
        for route in routes:
            for tpl in used_templates:
                pairs.append({"rota": route, "template": tpl, "funcao": func_name})

    return pairs, route_by_func


def main():
    if not APP_FILE.exists():
        print(f"❌ app.py não encontrado em: {APP_FILE}")
        return

    lines = APP_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
    rotas_templates, route_by_func = _extract_routes_and_templates(lines)

    templates_exist = {
        html_file.relative_to(TEMPLATES_DIR).as_posix()
        for html_file in TEMPLATES_DIR.rglob("*.html")
    } if TEMPLATES_DIR.exists() else set()

    templates_dict = {}
    for item in rotas_templates:
        templates_dict.setdefault(item["template"], set()).add(item["rota"])

    print("=" * 80)
    print(f"ANÁLISE DE {len(route_by_func)} ROTAS DO APP.PY")
    print("=" * 80)
    print()

    missing_templates = []
    for template in sorted(templates_dict):
        if template not in templates_exist:
            missing_templates.append(
                {"template": template, "rotas": sorted(templates_dict[template])}
            )
            print(f"❌ FALTANDO - Template: {template}")
            for rota in sorted(templates_dict[template]):
                print(f"           Rota: {rota}")
            print()

    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    print(f"Total de templates únicos usados: {len(templates_dict)}")
    print(f"Templates existentes: {len([t for t in templates_dict if t in templates_exist])}")
    print(f"Templates faltando: {len(missing_templates)}")
    print()

    if missing_templates:
        print("=" * 80)
        print("LISTA DE TEMPLATES FALTANDO:")
        print("=" * 80)
        for item in missing_templates:
            print(f"\n- Rota: {', '.join(item['rotas'])}")
            print(f"  Template esperado: {item['template']}")
            print("  Status: FALTANDO")
    else:
        print("✅ Todos os templates necessários estão presentes!")


if __name__ == "__main__":
    main()
