#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para migrar/atualizar todas as tabelas do banco de dados
Adiciona colunas faltantes sem perder dados
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text, inspect

def migrar_banco():
    """Migra o banco de dados adicionando colunas faltantes"""
    with app.app_context():
        try:
            print("=" * 70)
            print("MIGRANDO BANCO DE DADOS - TODAS AS TABELAS")
            print("=" * 70)
            
            inspector = inspect(db.engine)
            
            # Verificar se é SQLite ou PostgreSQL
            db_uri = str(db.engine.url)
            is_sqlite = 'sqlite' in db_uri
            
            print(f"\n[INFO] Banco de dados: {'SQLite' if is_sqlite else 'PostgreSQL'}")
            
            # Lista de migrações para a tabela usuarios
            migrations_usuarios = [
                ("gerente_id", "INTEGER", "ALTER TABLE usuarios ADD COLUMN gerente_id INTEGER"),
                ("is_super_admin", "BOOLEAN", "ALTER TABLE usuarios ADD COLUMN is_super_admin BOOLEAN DEFAULT 0"),
                ("pode_ver_dashboard", "BOOLEAN", "ALTER TABLE usuarios ADD COLUMN pode_ver_dashboard BOOLEAN DEFAULT 1"),
                ("pode_gerenciar_vendedores", "BOOLEAN", "ALTER TABLE usuarios ADD COLUMN pode_gerenciar_vendedores BOOLEAN DEFAULT 0"),
                ("pode_gerenciar_metas", "BOOLEAN", "ALTER TABLE usuarios ADD COLUMN pode_gerenciar_metas BOOLEAN DEFAULT 0"),
                ("pode_gerenciar_equipes", "BOOLEAN", "ALTER TABLE usuarios ADD COLUMN pode_gerenciar_equipes BOOLEAN DEFAULT 0"),
                ("pode_gerenciar_comissoes", "BOOLEAN", "ALTER TABLE usuarios ADD COLUMN pode_gerenciar_comissoes BOOLEAN DEFAULT 0"),
                ("pode_enviar_mensagens", "BOOLEAN", "ALTER TABLE usuarios ADD COLUMN pode_enviar_mensagens BOOLEAN DEFAULT 1"),
                ("pode_exportar_dados", "BOOLEAN", "ALTER TABLE usuarios ADD COLUMN pode_exportar_dados BOOLEAN DEFAULT 0"),
                ("pode_ver_todas_metas", "BOOLEAN", "ALTER TABLE usuarios ADD COLUMN pode_ver_todas_metas BOOLEAN DEFAULT 0"),
                ("pode_aprovar_comissoes", "BOOLEAN", "ALTER TABLE usuarios ADD COLUMN pode_aprovar_comissoes BOOLEAN DEFAULT 0"),
            ]
            
            # Verificar e adicionar colunas na tabela usuarios
            if 'usuarios' in inspector.get_table_names():
                print("\n[1/2] Migrando tabela 'usuarios'...")
                colunas_existentes = [col['name'] for col in inspector.get_columns('usuarios')]
                
                for coluna, tipo, sql in migrations_usuarios:
                    if coluna not in colunas_existentes:
                        try:
                            db.session.execute(text(sql))
                            db.session.commit()
                            print(f"  ✓ Coluna '{coluna}' adicionada")
                        except Exception as e:
                            print(f"  ⚠ Erro ao adicionar '{coluna}': {str(e)}")
                            db.session.rollback()
                    else:
                        print(f"  ✓ Coluna '{coluna}' já existe")
            
            # Criar todas as tabelas (incluindo clientes)
            print("\n[2/2] Criando/atualizando todas as tabelas...")
            db.create_all()
            print("  ✓ Todas as tabelas criadas/atualizadas")
            
            # Verificar tabelas criadas
            print("\n[INFO] Verificando tabelas criadas:")
            tabelas = inspector.get_table_names()
            
            tabelas_esperadas = ['usuarios', 'empresas', 'vendedores', 'metas', 
                                'equipes', 'mensagens', 'clientes', 'compras_clientes']
            
            for tabela in tabelas_esperadas:
                if tabela in tabelas:
                    print(f"  ✓ {tabela}")
                else:
                    print(f"  ✗ {tabela} (FALTANDO)")
            
            print("\n" + "=" * 70)
            print("MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 70)
            print("\nO sistema está pronto para uso.")
            print("Reinicie o servidor Flask se estiver em execução.")
            print("\n")
            
            return True
            
        except Exception as e:
            print(f"\n✗ ERRO ao migrar banco: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    migrar_banco()
