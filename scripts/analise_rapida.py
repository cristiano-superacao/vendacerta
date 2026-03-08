import re

print("ANÁLISE DO SISTEMA")
print("=" * 60)

# 1. Rotas
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

routes = re.findall(r'@app\.route\([\"\'](.*?)[\"\']', content)
print(f"\n1. ROTAS: {len(routes)} encontradas")
from collections import Counter
dups = {r: c for r, c in Counter(routes).items() if c > 1}
if dups:
    print(f"   DUPLICADAS: {dups}")
else:
    print("   ✅ Sem duplicatas")

# 2. Templates
temps = re.findall(r'render_template\([\"\'](.*?)[\"\"]', content)
print(f"\n2. TEMPLATES: {len(set(temps))} únicos referenciados")

# 3. Queries
queries = {
    'Usuario': len(re.findall(r'Usuario\.query', content)),
    'Vendedor': len(re.findall(r'Vendedor\.query', content)),
    'Meta': len(re.findall(r'Meta\.query', content)),
    'db.session': len(re.findall(r'db\.session', content)),
}
print(f"\n3. QUERIES:")
for k, v in queries.items():
    print(f"   {k}: {v}x")

print("\n" + "=" * 60)
print("ANÁLISE CONCLUÍDA")
