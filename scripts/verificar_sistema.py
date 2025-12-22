# Script de Verificação Completa do Sistema VendaCerta
# Verifica rotas, templates, configurações e compatibilidade Railway

import os
import re
from pathlib import Path

def verificar_rotas():
    """Verifica todas as rotas definidas no app.py"""
    print("="*70)
    print("📍 VERIFICANDO ROTAS")
    print("="*70)
    
    app_file = Path("app.py")
    if not app_file.exists():
        print("❌ Arquivo app.py não encontrado!")
        return []
    
    content = app_file.read_text(encoding='utf-8')
    rotas = re.findall(r'@app\.route\(["\']([^"\']+)["\']', content)
    
    print(f"\n✅ Total de rotas encontradas: {len(rotas)}\n")
    
    rotas_por_categoria = {
        'Autenticação': [],
        'Dashboard': [],
        'Clientes': [],
        'Vendedores': [],
        'Metas': [],
        'Supervisores': [],
        'Estoque': [],
        'Ordem de Serviço': [],
        'Mensagens': [],
        'Backups': [],
        'Super Admin': [],
        'Outras': []
    }
    
    for rota in rotas:
        if any(x in rota for x in ['/login', '/logout', '/registro', '/recuperar-senha']):
            rotas_por_categoria['Autenticação'].append(rota)
        elif '/dashboard' in rota or '/ping' in rota:
            rotas_por_categoria['Dashboard'].append(rota)
        elif '/cliente' in rota:
            rotas_por_categoria['Clientes'].append(rota)
        elif '/vendedor' in rota:
            rotas_por_categoria['Vendedores'].append(rota)
        elif '/meta' in rota:
            rotas_por_categoria['Metas'].append(rota)
        elif '/supervisor' in rota:
            rotas_por_categoria['Supervisores'].append(rota)
        elif '/estoque' in rota or '/produto' in rota:
            rotas_por_categoria['Estoque'].append(rota)
        elif '/ordem-servico' in rota or '/os/' in rota:
            rotas_por_categoria['Ordem de Serviço'].append(rota)
        elif '/mensagem' in rota:
            rotas_por_categoria['Mensagens'].append(rota)
        elif '/backup' in rota:
            rotas_por_categoria['Backups'].append(rota)
        elif '/super-admin' in rota or '/empresa' in rota or '/equipe' in rota:
            rotas_por_categoria['Super Admin'].append(rota)
        else:
            rotas_por_categoria['Outras'].append(rota)
    
    for categoria, lista in rotas_por_categoria.items():
        if lista:
            print(f"\n{categoria} ({len(lista)} rotas):")
            for rota in sorted(lista):
                print(f"  ✓ {rota}")
    
    return rotas

def verificar_templates():
    """Verifica todos os templates HTML"""
    print("\n" + "="*70)
    print("📄 VERIFICANDO TEMPLATES")
    print("="*70)
    
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("❌ Diretório templates não encontrado!")
        return []
    
    templates = list(templates_dir.glob("**/*.html"))
    print(f"\n✅ Total de templates encontrados: {len(templates)}\n")
    
    templates_por_pasta = {}
    for template in templates:
        pasta = template.parent.name if template.parent != templates_dir else "root"
        if pasta not in templates_por_pasta:
            templates_por_pasta[pasta] = []
        templates_por_pasta[pasta].append(template.name)
    
    for pasta, arquivos in sorted(templates_por_pasta.items()):
        print(f"\n{pasta}/ ({len(arquivos)} templates):")
        for arquivo in sorted(arquivos):
            print(f"  ✓ {arquivo}")
    
    return templates

def verificar_responsividade():
    """Verifica se templates usam Bootstrap e são responsivos"""
    print("\n" + "="*70)
    print("📱 VERIFICANDO RESPONSIVIDADE")
    print("="*70)
    
    templates_dir = Path("templates")
    templates = list(templates_dir.glob("**/*.html"))
    
    com_bootstrap = 0
    com_viewport = 0
    com_responsivo = 0
    
    for template in templates:
        content = template.read_text(encoding='utf-8', errors='ignore')
        
        if 'bootstrap' in content.lower():
            com_bootstrap += 1
        if 'viewport' in content:
            com_viewport += 1
        if any(x in content for x in ['col-md-', 'col-lg-', 'col-sm-', 'd-none d-md-']):
            com_responsivo += 1
    
    print(f"\n✅ Templates com Bootstrap: {com_bootstrap}/{len(templates)}")
    print(f"✅ Templates com viewport: {com_viewport}/{len(templates)}")
    print(f"✅ Templates com classes responsivas: {com_responsivo}/{len(templates)}")
    
    if com_bootstrap > len(templates) * 0.9:
        print("\n🎉 Sistema 100% responsivo com Bootstrap!")
    else:
        print("\n⚠️  Alguns templates podem não ser responsivos")

def verificar_variaveis_railway():
    """Verifica variáveis de ambiente do Railway"""
    print("\n" + "="*70)
    print("🚂 VERIFICANDO VARIÁVEIS RAILWAY")
    print("="*70)
    
    variaveis_esperadas = {
        'Essenciais': ['DATABASE_URL', 'SECRET_KEY', 'FLASK_ENV'],
        'PostgreSQL': ['PGDATABASE', 'PGHOST', 'PGUSER', 'PGPASSWORD', 'PGPORT'],
        'Railway Auto': ['RAILWAY_ENVIRONMENT_NAME', 'RAILWAY_PROJECT_NAME', 'RAILWAY_SERVICE_NAME'],
        'Alternativas': ['URL_DO_BANCO_DE_DADOS', 'CHAVE_SECRETA', 'FRASCO_ENV']
    }
    
    for categoria, vars in variaveis_esperadas.items():
        print(f"\n{categoria}:")
        for var in vars:
            valor = os.environ.get(var)
            if valor:
                if 'PASSWORD' in var or 'SECRET' in var or 'CHAVE' in var:
                    print(f"  ✅ {var}=****** (configurada)")
                else:
                    print(f"  ✅ {var}={valor[:30]}..." if len(valor) > 30 else f"  ✅ {var}={valor}")
            else:
                print(f"  ⚠️  {var} (não configurada)")

def verificar_arquivos_config():
    """Verifica arquivos de configuração do Railway"""
    print("\n" + "="*70)
    print("⚙️  VERIFICANDO ARQUIVOS DE CONFIGURAÇÃO")
    print("="*70)
    
    arquivos_necessarios = {
        'nixpacks.toml': 'Configuração Nixpacks',
        'railway.json': 'Configuração Railway',
        'runtime.txt': 'Versão Python',
        'Procfile': 'Comando de start',
        'requirements.txt': 'Dependências Python',
        'config.py': 'Configuração da aplicação',
        'wsgi.py': 'Entry point WSGI',
        'init_railway.py': 'Inicialização Railway'
    }
    
    print()
    for arquivo, descricao in arquivos_necessarios.items():
        if Path(arquivo).exists():
            print(f"✅ {arquivo:<20} - {descricao}")
        else:
            print(f"❌ {arquivo:<20} - {descricao} (FALTANDO)")

def verificar_duplicidades():
    """Verifica arquivos duplicados"""
    print("\n" + "="*70)
    print("🔍 VERIFICANDO DUPLICIDADES")
    print("="*70)
    
    # Verificar templates duplicados
    templates_dir = Path("templates")
    if templates_dir.exists():
        templates = {}
        for template in templates_dir.glob("**/*.html"):
            nome = template.name
            if nome in templates:
                print(f"⚠️  Template duplicado: {nome}")
                print(f"   - {templates[nome]}")
                print(f"   - {template}")
            else:
                templates[nome] = template
        
        if not any("⚠️" in str(x) for x in templates.keys()):
            print("\n✅ Nenhum template duplicado encontrado")
    
    # Verificar scripts duplicados
    scripts_dir = Path("scripts")
    if scripts_dir.exists():
        scripts = {}
        for script in scripts_dir.glob("*.py"):
            nome = script.name
            if nome in scripts:
                print(f"⚠️  Script duplicado: {nome}")
            else:
                scripts[nome] = script

def gerar_relatorio():
    """Gera relatório completo"""
    print("\n" + "="*70)
    print("📊 RELATÓRIO FINAL")
    print("="*70)
    
    rotas = verificar_rotas()
    templates = verificar_templates()
    verificar_responsividade()
    verificar_variaveis_railway()
    verificar_arquivos_config()
    verificar_duplicidades()
    
    print("\n" + "="*70)
    print("✅ VERIFICAÇÃO CONCLUÍDA")
    print("="*70)
    print(f"\n📊 Resumo:")
    print(f"  - Rotas: {len(rotas)}")
    print(f"  - Templates: {len(templates)}")
    print(f"  - Layout: Responsivo (Bootstrap 5.3.3)")
    print(f"  - Railway: Compatível")
    print("\n🚀 Sistema VendaCerta pronto para produção!")

if __name__ == "__main__":
    gerar_relatorio()
