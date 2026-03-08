"""
Script para criar tabelas de estoque e manutenção
"""
from app import app, db
from models import Produto, EstoqueMovimento, Tecnico, OrdemServico

print("\n" + "="*70)
print("🔧 CRIANDO TABELAS DE ESTOQUE E MANUTENÇÃO")
print("="*70)

with app.app_context():
    print("\n📊 Criando tabelas...")
    
    # Criar tabelas
    db.create_all()
    
    print("   ✅ produtos")
    print("   ✅ estoque_movimentos")
    print("   ✅ tecnicos")
    print("   ✅ ordens_servico")
    
    # Verificar
    import sqlite3
    conn = sqlite3.connect('instance/vendacerta.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('produtos', 'estoque_movimentos', 'tecnicos', 'ordens_servico')")
    tabelas = cursor.fetchall()
    
    print(f"\n📋 Tabelas criadas: {len(tabelas)}")
    for tab in tabelas:
        cursor.execute(f"PRAGMA table_info({tab[0]})")
        colunas = cursor.fetchall()
        print(f"   {tab[0]}: {len(colunas)} colunas")
    
    conn.close()
    
    print("\n" + "="*70)
    print("✅ TABELAS CRIADAS COM SUCESSO!")
    print("="*70)
