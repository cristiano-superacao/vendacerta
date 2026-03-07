#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Análise de Duplicações e Código Morto
Identifica código duplicado, funções não utilizadas e imports desnecessários
"""

import re
import ast
import hashlib
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

            tree = ast.parse(content)

            # Apenas imports de nível de módulo (evita falsos positivos de imports locais)
            imports_top_level = set()
            for node in tree.body:
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports_top_level.add(alias.asname or alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        if alias.name != '*':
                            imports_top_level.add(alias.asname or alias.name)

            usados = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    usados.add(node.id)

            nao_usados = sorted(name for name in imports_top_level if name not in usados)
            
            if nao_usados:
                print(f"   ⚠️  Possíveis imports não utilizados: {len(nao_usados)}")
                for imp in sorted(nao_usados)[:10]:  # Mostrar só os primeiros 10
                    print(f"      - {imp}")
                self.relatorio['imports_nao_usados'] = nao_usados
            else:
                print("   ✅ Todos os imports parecem estar em uso")
            
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
            
            # Extrair seletores de primeiro nível (fora de @media)
            lines = content.splitlines()
            seletores_limpos = []
            depth = 0
            media_depth = 0

            for raw_line in lines:
                line = raw_line.strip()
                if not line or line.startswith('/*'):
                    depth += raw_line.count('{') - raw_line.count('}')
                    continue

                if depth == 0 and line.startswith('@media') and line.endswith('{'):
                    media_depth += 1

                if media_depth == 0 and '{' in line and not line.startswith('@'):
                    selector = line.split('{', 1)[0].strip()
                    if selector:
                        seletores_limpos.append(selector)

                opens = raw_line.count('{')
                closes = raw_line.count('}')
                depth += opens - closes

                if media_depth > 0 and closes > 0 and depth == 0:
                    media_depth = 0

            # Contar duplicados apenas no mesmo escopo (top-level)
            selector_counts = Counter(seletores_limpos)
            duplicados = {sel: count for sel, count in selector_counts.items() if count > 1}
            
            if duplicados:
                print(f"   ⚠️  Encontrados {len(duplicados)} seletores duplicados:")
                for sel, count in list(duplicados.items())[:10]:  # Primeiros 10
                    print(f"      - {sel}: {count}x")
                self.relatorio['css_duplicados'] = list(duplicados.keys())
            else:
                print("   ✅ Nenhum seletor CSS duplicado")
            
            return len(duplicados)
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return 0
    
    def analisar_templates_duplicados(self):
        """Analisa templates com conteúdo idêntico"""
        print("\n📝 Analisando templates duplicados...")
        
        try:
            templates_dir = self.base_path / 'templates'
            templates = list(templates_dir.rglob('*.html'))
            
            hashes = defaultdict(list)
            for template in templates:
                try:
                    data = template.read_bytes()
                    digest = hashlib.md5(data).hexdigest()
                    hashes[digest].append(template)
                except Exception:
                    continue

            duplicados = [paths for paths in hashes.values() if len(paths) > 1]

            if duplicados:
                print(f"   ⚠️  Encontrados {len(duplicados)} grupos de templates com conteúdo idêntico:")
                for grupo in duplicados:
                    print("      - Grupo:")
                    for t in grupo:
                        print(f"         * {t.relative_to(self.base_path)}")
                self.relatorio['templates_duplicados'] = [
                    [str(t.relative_to(self.base_path)) for t in grupo]
                    for grupo in duplicados
                ]
            else:
                print(f"   ✅ Nenhum template com conteúdo duplicado (total: {len(templates)})")
            
            return len(duplicados)
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return 0
    
    def analisar_arquivos_temporarios(self):
        """Procura arquivos temporários, backup, old, etc"""
        print("\n🗑️  Procurando arquivos temporários...")
        
        padroes = ['*.bak', '*~', '*.old', '*.tmp', '*.temp', '*.copy']
        arquivos_temp = []
        
        for padrao in padroes:
            arquivos_temp.extend(self.base_path.rglob(padrao))
        
        # Filtrar pastas específicas que são válidas
        arquivos_temp_reais = []
        for arq in arquivos_temp:
            if arq.is_dir():
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
            print("   ✅ Nenhum arquivo temporário encontrado")
        
        return len(arquivos_temp_reais)
    
    def gerar_relatorio(self):
        """Gera relatório final"""
        print("\n" + "=" * 80)
        print("📊 RELATÓRIO FINAL DE DUPLICAÇÕES".center(80))
        print("=" * 80)
        
        print(f"\n✅ Rotas duplicadas: {len(self.relatorio['rotas_duplicadas'])}")
        print(f"✅ Imports possivelmente não usados: {len(self.relatorio['imports_nao_usados'])}")
        print(f"✅ Seletores CSS duplicados: {len(self.relatorio['css_duplicados'])}")
        print(f"✅ Templates com conteúdo duplicado: {len(self.relatorio['templates_duplicados'])}")
        
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
            
            f.write("\n## Templates Duplicados\n\n")
            if self.relatorio['templates_duplicados']:
                for grupo in self.relatorio['templates_duplicados']:
                    f.write("- Grupo:\n")
                    for temp in grupo:
                        f.write(f"  - `{temp}`\n")
            else:
                f.write("✅ Nenhum template duplicado encontrado.\n")
        
        print("\n📄 Relatório detalhado salvo em: docs/RELATORIO_DUPLICACOES.md")
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
