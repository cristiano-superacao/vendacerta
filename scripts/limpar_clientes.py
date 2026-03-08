#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para limpar todos os clientes cadastrados
Mantém todos os outros dados do sistema
"""

import os
import sys

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Cliente, CompraCliente

def limpar_clientes():
    """Remove todos os clientes e suas compras do banco de dados"""
    
    with app.app_context():
        try:
            print("\n" + "="*70)
            print("🗑️  LIMPANDO DADOS DE CLIENTES")
            print("="*70 + "\n")
            
            # Contar registros antes
            total_compras = CompraCliente.query.count()
            total_clientes = Cliente.query.count()
            
            print(f"📊 Registros encontrados:")
            print(f"   • Clientes: {total_clientes}")
            print(f"   • Compras: {total_compras}")
            print()
            
            # Deletar compras primeiro (relacionamento)
            if total_compras > 0:
                CompraCliente.query.delete()
                print(f"✅ {total_compras} compras removidas")
            
            # Deletar clientes
            if total_clientes > 0:
                Cliente.query.delete()
                print(f"✅ {total_clientes} clientes removidos")
            
            # Commit das alterações
            db.session.commit()
            
            print("\n" + "="*70)
            print("✅ LIMPEZA CONCLUÍDA COM SUCESSO!")
            print("="*70)
            print("\n📌 Informações:")
            print("   • Layout: 100% preservado")
            print("   • Usuários: mantidos")
            print("   • Vendedores: mantidos")
            print("   • Metas: mantidas")
            print("   • Configurações: mantidas")
            print()
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erro ao limpar clientes: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    limpar_clientes()
