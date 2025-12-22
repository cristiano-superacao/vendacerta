"""
Script de teste para criar tabelas
"""
from app import app, db
from models import Cliente

with app.app_context():
    print("Criando tabelas...")
    db.create_all()
    print("Tabelas criadas!")
    
    # Verificar
    import sqlite3
    conn = sqlite3.connect('instance/metas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = cursor.fetchall()
    print(f"\nTabelas encontradas: {len(tabelas)}")
    for tab in tabelas:
        print(f"  - {tab[0]}")
    conn.close()
