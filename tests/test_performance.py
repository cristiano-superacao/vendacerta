# test_performance.py
"""
Script para testar melhorias de performance do sistema
Compara antes/depois das otimizações
"""

import os
import unittest


if os.getenv("RUN_INTEGRATION_TESTS") != "1":
    raise unittest.SkipTest(
        "Teste de performance (depende de app/banco com dados). "
        "Defina RUN_INTEGRATION_TESTS=1 para executar."
    )

from app import app, db
from models import Usuario, Vendedor, Meta, Equipe
from datetime import datetime
import time
from sqlalchemy import text

def medir_tempo(func):
    """Decorator para medir tempo de execução"""
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        tempo = (fim - inicio) * 1000  # Converter para ms
        return resultado, tempo
    return wrapper

@medir_tempo
def test_query_dashboard_simples():
    """Teste: Query simples do dashboard (SEM otimização)"""
    metas = Meta.query.filter_by(mes=12, ano=2025).all()
    
    # Simular acesso a relacionamentos (causa N+1)
    for meta in metas:
        if meta.vendedor:
            _ = meta.vendedor.nome
            if meta.vendedor.supervisor_id:
                supervisor = Usuario.query.get(meta.vendedor.supervisor_id)
            if meta.vendedor.equipe_id:
                equipe = Equipe.query.get(meta.vendedor.equipe_id)
    
    return len(metas)

@medir_tempo
def test_query_dashboard_otimizado():
    """Teste: Query otimizada do dashboard (COM eager loading)"""
    from sqlalchemy.orm import joinedload
    
    metas = Meta.query.options(
        joinedload(Meta.vendedor).joinedload(Vendedor.equipe_obj),
        joinedload(Meta.vendedor).joinedload(Vendedor.supervisor_obj)
    ).filter_by(mes=12, ano=2025).all()
    
    # Acessar relacionamentos (já carregados)
    for meta in metas:
        if meta.vendedor:
            _ = meta.vendedor.nome
            if meta.vendedor.supervisor_obj:
                _ = meta.vendedor.supervisor_obj.nome
            if meta.vendedor.equipe_obj:
                _ = meta.vendedor.equipe_obj.nome
    
    return len(metas)

@medir_tempo
def test_busca_vendedores():
    """Teste: Busca de vendedores ativos"""
    vendedores = Vendedor.query.filter_by(ativo=True).all()
    return len(vendedores)

@medir_tempo
def test_busca_vendedores_com_indice():
    """Teste: Busca otimizada com índice composto"""
    vendedores = Vendedor.query.filter_by(
        empresa_id=1,
        ativo=True
    ).all()
    return len(vendedores)

def verificar_indices():
    """Verifica se os índices foram criados"""
    database_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    is_postgres = 'postgresql' in database_url
    
    print("\n📊 VERIFICANDO ÍNDICES...")
    print("=" * 70)
    
    if is_postgres:
        query = text("""
            SELECT 
                tablename, 
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname = 'public'
            AND indexname LIKE 'idx_%'
            ORDER BY tablename, indexname;
        """)
    else:
        # SQLite
        query = text("""
            SELECT name, tbl_name, sql 
            FROM sqlite_master 
            WHERE type='index' 
            AND name LIKE 'idx_%'
            ORDER BY tbl_name, name;
        """)
    
    try:
        result = db.session.execute(query)
        indices = result.fetchall()
        
        if indices:
            print(f"✅ {len(indices)} índices de performance encontrados:\n")
            for idx in indices:
                if is_postgres:
                    print(f"   • {idx.indexname} ({idx.tablename})")
                else:
                    print(f"   • {idx.name} ({idx.tbl_name})")
        else:
            print("⚠️  Nenhum índice de performance encontrado!")
            print("   Execute: python migrar_indices_performance.py")
        
        return len(indices) > 0
    except Exception as e:
        print(f"❌ Erro ao verificar índices: {e}")
        return False

def contar_queries():
    """Conta número de queries executadas"""
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    
    query_count = {'count': 0}
    
    @event.listens_for(Engine, "before_cursor_execute")
    def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
        query_count['count'] += 1
    
    return query_count

def run_tests():
    """Executa todos os testes de performance"""
    print("\n" + "=" * 70)
    print("🚀 TESTE DE PERFORMANCE - SISTEMA VENDACERTA")
    print("=" * 70)
    print()
    
    with app.app_context():
        # Verificar índices
        indices_ok = verificar_indices()
        
        print("\n📈 EXECUTANDO TESTES DE PERFORMANCE...")
        print("=" * 70)
        
        # Teste 1: Dashboard simples vs otimizado
        print("\n1️⃣ Dashboard - Query Simples (SEM otimização)")
        try:
            count, tempo = test_query_dashboard_simples()
            print(f"   ⏱️  Tempo: {tempo:.2f}ms")
            print(f"   📊 Registros: {count}")
            tempo_simples = tempo
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            tempo_simples = 0
        
        print("\n2️⃣ Dashboard - Query Otimizada (COM eager loading)")
        try:
            count, tempo = test_query_dashboard_otimizado()
            print(f"   ⏱️  Tempo: {tempo:.2f}ms")
            print(f"   📊 Registros: {count}")
            tempo_otimizado = tempo
            
            if tempo_simples > 0 and tempo_otimizado > 0:
                melhoria = ((tempo_simples - tempo_otimizado) / tempo_simples) * 100
                print(f"   ✨ Melhoria: {melhoria:.1f}% mais rápido!")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        # Teste 2: Busca de vendedores
        print("\n3️⃣ Busca de Vendedores - Sem Filtro de Empresa")
        try:
            count, tempo = test_busca_vendedores()
            print(f"   ⏱️  Tempo: {tempo:.2f}ms")
            print(f"   📊 Registros: {count}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        print("\n4️⃣ Busca de Vendedores - Com Índice Composto")
        try:
            count, tempo = test_busca_vendedores_com_indice()
            print(f"   ⏱️  Tempo: {tempo:.2f}ms")
            print(f"   📊 Registros: {count}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        # Estatísticas do banco
        print("\n📊 ESTATÍSTICAS DO BANCO DE DADOS")
        print("=" * 70)
        
        try:
            total_usuarios = Usuario.query.count()
            total_vendedores = Vendedor.query.count()
            total_metas = Meta.query.count()
            total_equipes = Equipe.query.count()
            
            print(f"   • Usuários: {total_usuarios}")
            print(f"   • Vendedores: {total_vendedores}")
            print(f"   • Metas: {total_metas}")
            print(f"   • Equipes: {total_equipes}")
        except Exception as e:
            print(f"   ❌ Erro ao buscar estatísticas: {e}")
        
        # Recomendações
        print("\n💡 RECOMENDAÇÕES")
        print("=" * 70)
        
        if not indices_ok:
            print("   ⚠️  Execute: python migrar_indices_performance.py")
            print("      Para criar índices de performance")
        else:
            print("   ✅ Índices de performance estão configurados!")
        
        print("\n   📚 Dicas:")
        print("      • Use eager loading (joinedload) em queries complexas")
        print("      • Evite queries dentro de loops")
        print("      • Utilize cache para dados que mudam pouco")
        print("      • Monitore queries lentas no Railway")
        
        print("\n" + "=" * 70)
        print("✅ TESTES CONCLUÍDOS!")
        print("=" * 70 + "\n")

if __name__ == '__main__':
    run_tests()
