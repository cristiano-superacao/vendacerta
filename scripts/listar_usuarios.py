#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para listar usuários cadastrados no sistema
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Usuario, Empresa

def listar_usuarios():
    """Lista todos os usuários do sistema"""
    with app.app_context():
        try:
            print("=" * 70)
            print("USUÁRIOS CADASTRADOS NO SISTEMA")
            print("=" * 70)
            
            usuarios = Usuario.query.all()
            
            if not usuarios:
                print("\n⚠️  Nenhum usuário encontrado no banco de dados.")
                print("\nPara criar um usuário administrador, execute:")
                print("  python init_data.py")
                return
            
            print(f"\nTotal de usuários: {len(usuarios)}\n")
            
            for usuario in usuarios:
                print("-" * 70)
                print(f"Nome: {usuario.nome}")
                print(f"Email (login): {usuario.email}")
                print(f"Cargo: {usuario.cargo}")
                print(f"Ativo: {'Sim' if usuario.ativo else 'Não'}")
                print(f"Bloqueado: {'Sim' if usuario.bloqueado else 'Não'}")
                print(f"Super Admin: {'Sim' if usuario.is_super_admin else 'Não'}")
                
                if usuario.empresa_id:
                    empresa = Empresa.query.get(usuario.empresa_id)
                    if empresa:
                        print(f"Empresa: {empresa.nome}")
                
                print(f"Data criação: {usuario.data_criacao.strftime('%d/%m/%Y %H:%M')}")
                
            print("-" * 70)
            print("\n📝 NOTA: As senhas são criptografadas e não podem ser visualizadas.")
            print("\nSe esqueceu a senha, você pode:")
            print("  1. Usar a função 'Recuperar Senha' no sistema")
            print("  2. Criar um novo usuário com init_data.py")
            print("  3. Resetar senha de um usuário específico\n")
            
            print("=" * 70)
            print("CREDENCIAIS PADRÃO (se você executou init_data.py):")
            print("=" * 70)
            print("\nAdmin/Super Admin:")
            print("  Email: admin@metas.com")
            print("  Senha: admin123")
            print("\nSupervisor:")
            print("  Email: supervisor@metas.com")
            print("  Senha: super123")
            print("\nVendedor:")
            print("  Email: vendedor@metas.com")
            print("  Senha: vend123")
            print("\n" + "=" * 70)
            
        except Exception as e:
            print(f"\n✗ Erro ao listar usuários: {str(e)}")

if __name__ == '__main__':
    listar_usuarios()
