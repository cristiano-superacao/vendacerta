#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para atualizar o banco de dados com as novas tabelas de clientes
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Cliente, CompraCliente

def atualizar_banco():
    """Cria as novas tabelas no banco de dados"""
    with app.app_context():
        try:
            print("=" * 60)
            print("ATUALIZANDO BANCO DE DADOS - MÓDULO DE CLIENTES")
            print("=" * 60)
            
            # Criar todas as tabelas
            print("\n[1/3] Criando tabelas de clientes...")
            db.create_all()
            print("✓ Tabelas criadas com sucesso!")
            
            # Verificar se as tabelas foram criadas
            print("\n[2/3] Verificando tabelas...")
            inspector = db.inspect(db.engine)
            tabelas = inspector.get_table_names()
            
            if 'clientes' in tabelas:
                print("✓ Tabela 'clientes' criada")
            else:
                print("✗ ERRO: Tabela 'clientes' não foi criada")
            
            if 'compras_clientes' in tabelas:
                print("✓ Tabela 'compras_clientes' criada")
            else:
                print("✗ ERRO: Tabela 'compras_clientes' não foi criada")
            
            print("\n[3/3] Finalizando...")
            db.session.commit()
            
            print("\n" + "=" * 60)
            print("ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print("\nVocê já pode utilizar o módulo de clientes.")
            print("Acesse: /clientes")
            print("\nFuncionalidades disponíveis:")
            print("  • Cadastro de clientes com CPF/CNPJ")
            print("  • Registro de compras")
            print("  • Sistema de status (verde/amarelo/vermelho)")
            print("  • Relatórios por vendedor/supervisor")
            print("  • Filtros por cidade, bairro, dia de visita")
            print("\n")
            
            return True
            
        except Exception as e:
            print(f"\n✗ ERRO ao atualizar banco: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    atualizar_banco()
