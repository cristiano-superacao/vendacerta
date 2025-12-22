#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de migração: Adicionar campo gerente_id ao modelo Usuario
Objetivo: Permitir hierarquia supervisor → gerente → administrador

Este script adiciona o campo gerente_id à tabela usuarios de forma segura,
verificando se o campo já existe antes de tentar adicioná-lo.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, db
from models import Usuario
from sqlalchemy import text, inspect

def verificar_coluna_existe(table_name, column_name):
    """
    Verifica se uma coluna existe em uma tabela

    Args:
        table_name (str): Nome da tabela
        column_name (str): Nome da coluna

    Returns:
        bool: True se a coluna existe, False caso contrário
    """
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def adicionar_coluna_gerente_id():
    """
    Adiciona a coluna gerente_id à tabela usuarios
    """
    with app.app_context():
        try:
            # Verificar se a coluna já existe
            if verificar_coluna_existe('usuarios', 'gerente_id'):
                print("✓ A coluna 'gerente_id' já existe na tabela 'usuarios'")
                return True

            print("Adicionando coluna 'gerente_id' à tabela 'usuarios'...")

            # Adicionar coluna
            db.session.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN gerente_id INTEGER
            """))

            # Adicionar foreign key constraint
            db.session.execute(text("""
                ALTER TABLE usuarios 
                ADD CONSTRAINT fk_usuarios_gerente_id 
                FOREIGN KEY (gerente_id) REFERENCES usuarios(id)
                ON DELETE SET NULL
            """))

            # Criar índice
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_usuarios_gerente_id 
                ON usuarios(gerente_id)
            """))

            db.session.commit()
            print("✓ Coluna 'gerente_id' adicionada com sucesso!")
            print("✓ Foreign key constraint adicionada")
            print("✓ Índice criado para melhor performance")

            return True

        except Exception as e:
            db.session.rollback()
            print(f"✗ Erro ao adicionar coluna 'gerente_id': {e}")
            return False

def listar_usuarios_hierarquia():
    """
    Lista usuários mostrando a hierarquia supervisor → gerente
    """
    with app.app_context():
        try:
            usuarios = Usuario.query.filter(
                Usuario.cargo.in_(['supervisor', 'gerente', 'admin'])
            ).order_by(Usuario.cargo, Usuario.nome).all()

            if not usuarios:
                print("\nNenhum supervisor, gerente ou administrador encontrado.")
                return

            print("\n" + "="*80)
            print("HIERARQUIA DE USUÁRIOS")
            print("="*80)
            print(f"{'ID':<5} {'Nome':<25} {'Cargo':<15} {'Gerente':<25}")
            print("-"*80)

            for usuario in usuarios:
                gerente_nome = usuario.gerente.nome if usuario.gerente else 'N/A'
                print(f"{usuario.id:<5} {usuario.nome:<25} {usuario.cargo:<15} {gerente_nome:<25}")

            print("-"*80)
            print(f"Total: {len(usuarios)} usuário(s)\n")

        except Exception as e:
            print(f"✗ Erro ao listar usuários: {e}")

def main():
    """Função principal"""
    print("\n" + "="*80)
    print("MIGRAÇÃO: Adicionar campo gerente_id ao modelo Usuario")
    print("="*80 + "\n")

    # Adicionar coluna
    sucesso = adicionar_coluna_gerente_id()

    if sucesso:
        # Listar hierarquia atual
        listar_usuarios_hierarquia()

        print("\n" + "="*80)
        print("PRÓXIMOS PASSOS:")
        print("="*80)
        print("1. Atualize os supervisores com seus respectivos gerentes:")
        print("   - Acesse o painel administrativo")
        print("   - Ou execute SQL: UPDATE usuarios SET gerente_id = <id_gerente> WHERE id = <id_supervisor>")
        print("\n2. A meta do supervisor será calculada automaticamente como:")
        print("   - Soma das metas de todos os vendedores supervisionados")
        print("\n3. No Dashboard, você verá:")
        print("   - Nome do gerente responsável por cada supervisor")
        print("   - Meta supervisionada (soma das metas dos vendedores)")
        print("   - Receita total da equipe")
        print("="*80 + "\n")
    else:
        print("\n✗ Migração falhou. Verifique os erros acima.\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
