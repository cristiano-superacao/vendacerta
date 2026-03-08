import re
import os
from pathlib import Path

# Ler app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar todos os templates
pattern = r"render_template\(['\"]([^'\"]+)['\"]"
matches = re.findall(pattern, content)
templates_needed = sorted(set(matches))

# Listar templates existentes
templates_dir = Path('templates')
templates_exist = set()

for html_file in templates_dir.rglob('*.html'):
    rel_path = html_file.relative_to(templates_dir).as_posix()
    templates_exist.add(rel_path)

# Comparar
print("="*70)
print("TEMPLATES NECESSÁRIOS (encontrados no código):")
print("="*70)
for t in templates_needed:
    print(f"  - {t}")

print(f"\nTotal: {len(templates_needed)}")

print("\n" + "="*70)
print("TEMPLATES EXISTENTES (na pasta templates/):")
print("="*70)
for t in sorted(templates_exist):
    print(f"  - {t}")

print(f"\nTotal: {len(templates_exist)}")

print("\n" + "="*70)
print("TEMPLATES FALTANDO:")
print("="*70)

missing = []
for template in templates_needed:
    if template not in templates_exist:
        missing.append(template)
        print(f"  ❌ {template}")

if not missing:
    print("  ✅ Todos os templates necessários estão presentes!")
else:
    print(f"\nTotal de templates faltando: {len(missing)}")
