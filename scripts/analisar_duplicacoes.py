#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Análise de Duplicações e Código Morto
Identifica código duplicado, funções não utilizadas e imports desnecessários
"""

import re
import ast
from pathlib import Path
from collections import defaultdict, Counter

class AnalisadorDuplicacoes:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.relatorio = {
            'imports_nao_usados': [],
            'funcoes_duplicadas': [],
            'rotas_duplicadas': [],
            'templates_duplicados': [],
            'css_duplicados': []
        }
    
    def analisar_rotas_duplicadas(self):
        """Analisa rotas duplicadas no app.py"""
        print("\n📍 Analisando rotas duplicadas...")
        
        try:
            app_path = self.base_path / 'app.py'
            with open(app_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Encontrar todas as rotas
            routes = re.findall(r"@app\.route\(['\"]([^'\"]+)['\"]", content)
            
            # Contar duplicadas
            route_counts = Counter(routes)
            duplicatas = {route: count for route, count in route_counts.items() if count > 1}
            
            if duplicatas:
                print(f"   ⚠️  Encontradas {len(duplicatas)} rotas duplicadas:")
                for route, count in duplicatas.items():
                    print(f"      - {route}: {count}x")
                    self.relatorio['rotas_duplicadas'].append({
                        'rota': route,
                        'ocorrencias': count
                    })
            else:
                print(f"   ✅ Nenhuma rota duplicada (total: {len(set(routes))} únicas)")
            
            return len(duplicatas)
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return 0
    
    def analisar_imports_nao_usados(self):
        """Analisa imports que não são utilizados"""
        print("\n📦 Analisando imports não utilizados...")
        
        try:
            app_path = self.base_path / 'app.py'
            with open(app_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrair imports
            import_pattern = r'^(?:from\s+\S+\s+)?import\s+(.+)$'
            imports = []
            
            for linha in content.split('\n'):
                if match := re.match(import_pattern, linha.strip()):
                    imports_linha = match.group(1).split(',')
                    for imp in imports_linha:
                        imp_limpo = imp.strip().split(' as ')[0].strip()
                        if imp_limpo:
                            imports.append(imp_limpo)
            
            # Verificar quais são usados (simplificado)
            nao_usados = []
            for imp in set(imports):
                # Contar ocorrências (além do próprio import)
                ocorrencias = len(re.findall(r'\b' + re.escape(imp) + r'\b', content))
                if ocorrencias <= 1:  # Aparece só no import
                    nao_usados.append(imp)
            
            if nao_usados:
                print(f"   ⚠️  Possíveis imports não utilizados: {len(nao_usados)}")
                for imp in sorted(nao_usados)[:10]:  # Mostrar só os primeiros 10
                    print(f"      - {imp}")
                self.relatorio['imports_nao_usados'] = nao_usados
            else:
                print(f"   ✅ Todos os imports parecem estar em uso")
            
            return len(nao_usados)
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return 0
    
    def analisar_css_duplicado(self):
        """Analisa regras CSS duplicadas"""
        print("\n🎨 Analisando CSS duplicado...")
        
        try:
            css_path = self.base_path / 'static' / 'css' / 'custom.css'
            with open(css_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrair seletores CSS
            seletores = re.findall(r'([^\{\}]+)\s*\{', content)
            seletores_limpos = [s.strip() for s in seletores if s.strip()]
            
            # Contar duplicados
            selector_counts = Counter(seletores_limpos)
            duplicados = {sel: count for sel, count in selector_counts.items() if count > 1}
            
            if duplicados:
                print(f"   ⚠️  Encontrados {len(duplicados)} seletores duplicados:")
                for sel, count in list(duplicados.items())[:10]:  # Primeiros 10
                    print(f"      - {sel}: {count}x")
                self.relatorio['css_duplicados'] = list(duplicados.keys())
            else:
                print(f"   ✅ Nenhum seletor CSS duplicado")
            
            return len(duplicados)
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return 0
    
    def analisar_templates_duplicados(self):
        """Analisa templates HTML com potencial colisão no deploy.

        Observação:
        - Nomes repetidos (ex.: form.html em pastas diferentes) são uma convenção comum
          em apps Flask/Jinja e NÃO representam duplicação problemática.
        - O risco real é colisão por caminho/case (Windows vs Linux):
          ex.: templates/Clientes/Form.html vs templates/clientes/form.html.
        """
        print("\n📝 Analisando templates duplicados...")

        try:
            templates_dir = self.base_path / 'templates'
            templates = list(templates_dir.rglob('*.html'))

            # Detectar colisões por caminho/case (case-insensitive)
            rel_paths = [
                str(t.relative_to(templates_dir)).replace('\\', '/').strip()
                for t in templates
            ]
            rel_paths_lower = [p.lower() for p in rel_paths]
            path_counts = Counter(rel_paths_lower)
            colisoes = {p: count for p, count in path_counts.items() if count > 1}

            if colisoes:
                print(f"   ⚠️  Encontradas {len(colisoes)} colisões de templates (caminho/case):")
                for p_lower, count in colisoes.items():
                    print(f"      - {p_lower}: {count}x")
                    for p_original in rel_paths:
                        if p_original.lower() == p_lower:
                            print(f"         * templates/{p_original}")
                self.relatorio['templates_duplicados'] = list(colisoes.keys())
            else:
                print(f"   ✅ Nenhuma colisão de template por caminho/case (total: {len(templates)})")

            return len(colisoes)

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return 0
    
    def analisar_arquivos_temporarios(self):
        """Procura arquivos temporários, backup, old, etc"""
        print("\n🗑️  Procurando arquivos temporários...")

        # Evita falsos positivos por substring (ex.: "templates" contém "temp").
        # Foque em extensões/sufixos típicos de arquivos temporários.
        padroes = [
            '*.bak', '*.old', '*.tmp', '*.orig', '*.rej',
            '*.bkp', '*.backup', '*.copy',
            '*~', '*.swp', '*.swo', '*.swn'
        ]
        arquivos_temp = []
        
        for padrao in padroes:
            arquivos_temp.extend(self.base_path.rglob(padrao))
        
        # Filtrar pastas específicas que são válidas e manter apenas arquivos
        arquivos_temp_reais = []
        for arq in arquivos_temp:
            if not arq.is_file():
                continue
            # Ignorar arquivos em node_modules, venv, __pycache__, .git
            if any(parte in str(arq) for parte in ['node_modules', '.venv', '__pycache__', '.git', 'instance/backups']):
                continue
            arquivos_temp_reais.append(arq)
        
        if arquivos_temp_reais:
            print(f"   ⚠️  Encontrados {len(arquivos_temp_reais)} arquivos temporários:")
            for arq in arquivos_temp_reais[:20]:  # Primeiros 20
                print(f"      - {arq.relative_to(self.base_path)}")
        else:
            print(f"   ✅ Nenhum arquivo temporário encontrado")
        
        return len(arquivos_temp_reais)
    
    def gerar_relatorio(self):
        """Gera relatório final"""
        print("\n" + "=" * 80)
        print("📊 RELATÓRIO FINAL DE DUPLICAÇÕES".center(80))
        print("=" * 80)
        
        print(f"\n✅ Rotas duplicadas: {len(self.relatorio['rotas_duplicadas'])}")
        print(f"✅ Imports possivelmente não usados: {len(self.relatorio['imports_nao_usados'])}")
        print(f"✅ Seletores CSS duplicados: {len(self.relatorio['css_duplicados'])}")
        print(f"✅ Templates com colisão de caminho/case: {len(self.relatorio['templates_duplicados'])}")
        
        # Salvar relatório
        relatorio_path = self.base_path / 'docs' / 'RELATORIO_DUPLICACOES.md'
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            f.write("# Relatório de Análise de Duplicações\n\n")
            f.write(f"**Data:** {Path(__file__).stat().st_mtime}\n\n")
            
            f.write("## Rotas Duplicadas\n\n")
            if self.relatorio['rotas_duplicadas']:
                for item in self.relatorio['rotas_duplicadas']:
                    f.write(f"- `{item['rota']}`: {item['ocorrencias']}x\n")
            else:
                f.write("✅ Nenhuma rota duplicada encontrada.\n")
            
            f.write("\n## Imports Possivelmente Não Usados\n\n")
            if self.relatorio['imports_nao_usados']:
                for imp in self.relatorio['imports_nao_usados'][:50]:
                    f.write(f"- `{imp}`\n")
            else:
                f.write("✅ Todos os imports parecem estar em uso.\n")
            
            f.write("\n## Seletores CSS Duplicados\n\n")
            if self.relatorio['css_duplicados']:
                for sel in self.relatorio['css_duplicados'][:50]:
                    f.write(f"- `{sel}`\n")
            else:
                f.write("✅ Nenhum seletor duplicado encontrado.\n")
            
            f.write("\n## Templates com Colisão de Caminho/Case\n\n")
            if self.relatorio['templates_duplicados']:
                for temp in self.relatorio['templates_duplicados']:
                    f.write(f"- `{temp}`\n")
            else:
                f.write("✅ Nenhuma colisão de caminho/case encontrada.\n")
        
        print(f"\n📄 Relatório detalhado salvo em: docs/RELATORIO_DUPLICACOES.md")
        print("\n" + "=" * 80 + "\n")
    
    def executar(self):
        """Executa análise completa"""
        print("\n" + "=" * 80)
        print("🔍 ANÁLISE DE DUPLICAÇÕES E CÓDIGO MORTO".center(80))
        print("=" * 80)
        
        self.analisar_rotas_duplicadas()
        self.analisar_imports_nao_usados()
        self.analisar_css_duplicado()
        self.analisar_templates_duplicados()
        self.analisar_arquivos_temporarios()
        
        self.gerar_relatorio()

if __name__ == '__main__':
    analisador = AnalisadorDuplicacoes()
    analisador.executar()
