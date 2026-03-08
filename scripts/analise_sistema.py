#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Análise Completa do Sistema
Verifica: rotas, templates, segurança, duplicidades
"""

import re
import os
from pathlib import Path

def analisar_rotas():
    """Analisa todas as rotas do app.py"""
    print("=" * 80)
    print("🔍 ANÁLISE DE ROTAS")
    print("=" * 80)

    # Ajusta caminho para rodar de qualquer diretório
    script_dir = Path(__file__).parent
    app_path = script_dir.parent / 'app.py'

    with open(app_path, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    rotas = []
    rotas_duplicadas = []
    rotas_sem_login = []
    rotas_sem_permissao = []

    for i, linha in enumerate(linhas):
        # Detecta rotas
        match = re.search(r"@app\.route\('([^']+)'", linha)
        if match:
            rota = match.group(1)
            linha_num = i + 1

            # Verifica decoradores acima
            tem_login = False
            tem_super_admin = False
            tem_permissao_check = False

            # Olha 5 linhas acima
            for j in range(max(0, i-5), i):
                if '@login_required' in linhas[j]:
                    tem_login = True
                if '@super_admin_required' in linhas[j]:
                    tem_super_admin = True

            # Olha 10 linhas abaixo para checks de permissão
            for j in range(i, min(len(linhas), i+15)):
                if 'current_user.cargo' in linhas[j] or 'super_admin' in linhas[j]:
                    tem_permissao_check = True

            rotas.append({
                'rota': rota,
                'linha': linha_num,
                'tem_login': tem_login,
                'tem_super_admin': tem_super_admin,
                'tem_permissao_check': tem_permissao_check
            })

    # Verifica duplicadas
    rotas_vistas = {}
    for r in rotas:
        if r['rota'] in rotas_vistas:
            rotas_duplicadas.append({
                'rota': r['rota'],
                'linhas': [rotas_vistas[r['rota']], r['linha']]
            })
        else:
            rotas_vistas[r['rota']] = r['linha']

    # Verifica segurança
    rotas_publicas = ['/login', '/registro', '/recuperar-senha', '/redefinir-senha/<token>', '/manifest.json', '/sw.js', '/offline.html']

    for r in rotas:
        # Pula rotas públicas e de API/estáticos
        if r['rota'] in rotas_publicas or r['rota'].startswith('/static') or r['rota'].startswith('/api/public'):
            continue

        # Verifica se tem @login_required
        if not r['tem_login'] and not r['tem_super_admin']:
            rotas_sem_login.append(r)

        # Rotas de admin que devem ter check de permissão
        if '/super-admin' in r['rota'] or '/admin' in r['rota'] or '/configuracoes' in r['rota']:
            if not r['tem_permissao_check'] and not r['tem_super_admin']:
                rotas_sem_permissao.append(r)

    # Relatório
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total de rotas: {len(rotas)}")
    print(f"   Rotas duplicadas: {len(rotas_duplicadas)}")
    print(f"   Rotas sem @login_required: {len(rotas_sem_login)}")
    print(f"   Rotas admin sem check de permissão: {len(rotas_sem_permissao)}")

    if rotas_duplicadas:
        print(f"\n⚠️  ROTAS DUPLICADAS:")
        for r in rotas_duplicadas:
            print(f"   ❌ {r['rota']} (linhas {r['linhas']})")
    else:
        print(f"\n✅ Nenhuma rota duplicada!")

    if rotas_sem_login:
        print(f"\n⚠️  ROTAS SEM @login_required:")
        for r in rotas_sem_login:
            print(f"   ⚠️  Linha {r['linha']}: {r['rota']}")
    else:
        print(f"\n✅ Todas as rotas protegidas estão com @login_required!")

    if rotas_sem_permissao:
        print(f"\n⚠️  ROTAS ADMIN SEM CHECK DE PERMISSÃO:")
        for r in rotas_sem_permissao:
            print(f"   ⚠️  Linha {r['linha']}: {r['rota']}")
    else:
        print(f"\n✅ Todas as rotas admin têm verificação de permissão!")

    return rotas

def analisar_templates():
    """Analisa todos os templates"""
    print("\n" + "=" * 80)
    print("📁 ANÁLISE DE TEMPLATES")
    print("=" * 80)

    # Ajusta caminho para rodar de qualquer diretório
    script_dir = Path(__file__).parent
    templates_dir = script_dir.parent / 'templates'

    templates = list(templates_dir.rglob('*.html'))

    print(f"\n📊 Total de templates: {len(templates)}")
    print(f"\n📂 Estrutura de templates:")

    estrutura = {}
    for t in templates:
        rel_path = t.relative_to(templates_dir)
        parent = str(rel_path.parent)
        if parent == '.':
            parent = 'raiz'
        if parent not in estrutura:
            estrutura[parent] = []
        estrutura[parent].append(rel_path.name)

    for pasta, arquivos in sorted(estrutura.items()):
        print(f"\n   📁 {pasta}/")
        for arq in sorted(arquivos):
            print(f"      📄 {arq}")

    return templates

def verificar_responsividade():
    """Verifica uso de Bootstrap e classes responsivas"""
    print("\n" + "=" * 80)
    print("📱 ANÁLISE DE RESPONSIVIDADE")
    print("=" * 80)

    # Ajusta caminho para rodar de qualquer diretório
    script_dir = Path(__file__).parent
    templates_dir = script_dir.parent / 'templates'

    templates = list(templates_dir.rglob('*.html'))

    templates_sem_bootstrap = []
    templates_sem_container = []

    for t in templates:
        with open(t, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        tem_bootstrap = 'bootstrap' in conteudo.lower() or 'extends "base.html"' in conteudo
        tem_container = 'container' in conteudo or 'container-fluid' in conteudo

        if not tem_bootstrap:
            templates_sem_bootstrap.append(t.name)

        if not tem_container and t.name != 'base.html':
            templates_sem_container.append(t.name)

    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Templates analisados: {len(templates)}")

    if templates_sem_bootstrap:
        print(f"\n⚠️  Templates sem Bootstrap:")
        for t in templates_sem_bootstrap:
            print(f"   ❌ {t}")
    else:
        print(f"\n✅ Todos os templates usam Bootstrap!")

    if templates_sem_container:
        print(f"\n⚠️  Templates sem container:")
        for t in templates_sem_container:
            print(f"   ⚠️  {t}")
    else:
        print(f"\n✅ Todos os templates têm estrutura container!")

def main():
    """Executa análise completa"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "ANÁLISE COMPLETA DO SISTEMA v2.9.0" + " " * 24 + "║")
    print("╚" + "═" * 78 + "╝")

    rotas = analisar_rotas()
    templates = analisar_templates()
    verificar_responsividade()

    print("\n" + "=" * 80)
    print("✅ RESUMO FINAL")
    print("=" * 80)
    print(f"\n📊 Sistema possui:")
    print(f"   • {len(rotas)} rotas")
    print(f"   • {len(templates)} templates")
    print(f"\n✅ Análise concluída!")
    print("\n")

if __name__ == '__main__':
    main()
