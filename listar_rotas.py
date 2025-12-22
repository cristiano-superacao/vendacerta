import sys
sys.path.insert(0, '.')
from app import app

routes = []
for rule in app.url_map.iter_rules():
    if rule.endpoint != 'static':
        routes.append({
            'rota': str(rule),
            'metodos': ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'})),
            'endpoint': rule.endpoint
        })

print(f'Total de rotas: {len(routes)}\n')
print('ROTAS MAPEADAS:\n')
for r in sorted(routes, key=lambda x: x['rota']):
    print(f"{r['rota']:60} [{r['metodos']:15}] -> {r['endpoint']}")
