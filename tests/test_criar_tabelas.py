"""
Script de teste para criar tabelas
"""

import os
import unittest


if os.getenv("RUN_INTEGRATION_TESTS") != "1":
    raise unittest.SkipTest(
        "Teste de integração (criação de tabelas). "
        "Defina RUN_INTEGRATION_TESTS=1 para executar."
    )


def main():
    from app import app, db

    with app.app_context():
        print("Criando tabelas...")
        db.create_all()
        print("Tabelas criadas!")

        # Verificar (SQLite local)
        import sqlite3

        conn = sqlite3.connect('instance/metas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = cursor.fetchall()
        print(f"\nTabelas encontradas: {len(tabelas)}")
        for tab in tabelas:
            print(f"  - {tab[0]}")
        conn.close()


if __name__ == '__main__':
    main()
