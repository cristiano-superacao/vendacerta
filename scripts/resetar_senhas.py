#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para resetar senhas dos usuários no banco de produção
Execute com: python resetar_senhas.py
"""

import os
import sys

# Adicionar diretório pai ao path para importar app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Usuario, Empresa

def resetar_senhas():
    """Reseta senhas dos usuários padrão"""

    with app.app_context():
        print("\n" + "="*70)
        print("🔐 RESETANDO SENHAS DOS USUÁRIOS")
        print("="*70 + "\n")

        # Buscar Super Admin
        print("👑 Processando Super Administrador...")
        super_admin = Usuario.query.filter_by(email='admin@suameta.com.br').first()

        if super_admin:
            super_admin.set_senha('Admin@2025!')
            super_admin.ativo = True
            super_admin.bloqueado = False
            super_admin.is_super_admin = True
            db.session.commit()
            print("   ✅ Senha resetada: admin@suameta.com.br / Admin@2025!")
        else:
            print("   ❌ Super Admin não encontrado no banco!")
            # Criar se não existir
            print("   📝 Criando Super Admin...")
            super_admin = Usuario(
                nome='Super Administrador',
                email='admin@suameta.com.br',
                cargo='admin',
                is_super_admin=True,
                empresa_id=None,
                ativo=True,
                bloqueado=False
            )
            super_admin.set_senha('Admin@2025!')
            db.session.add(super_admin)
            db.session.commit()
            print("   ✅ Super Admin criado: admin@suameta.com.br / Admin@2025!")

        # Buscar ou criar empresa
        print("\n🏢 Verificando empresa...")
        empresa = Empresa.query.filter_by(cnpj='00000000000100').first()

        if not empresa:
            print("   📝 Criando empresa padrão...")
            empresa = Empresa(
                nome='SuaMeta Sistemas',
                cnpj='00000000000100',
                email='contato@suameta.com.br',
                telefone='(11) 99999-9999',
                cidade='São Paulo',
                estado='SP',
                ativo=True,
                bloqueado=False,
                plano='enterprise',
                max_usuarios=999,
                max_vendedores=999
            )
            db.session.add(empresa)
            db.session.commit()
            print("   ✅ Empresa criada!")
        else:
            print("   ✅ Empresa encontrada!")

        # Buscar Gerente
        print("\n🏢 Processando Gerente...")
        gerente = Usuario.query.filter_by(email='gerente@suameta.com.br').first()

        if gerente:
            gerente.set_senha('Gerente@2025!')
            gerente.ativo = True
            gerente.bloqueado = False
            gerente.empresa_id = empresa.id
            db.session.commit()
            print("   ✅ Senha resetada: gerente@suameta.com.br / Gerente@2025!")
        else:
            print("   ❌ Gerente não encontrado no banco!")
            # Criar se não existir
            print("   📝 Criando Gerente...")
            gerente = Usuario(
                nome='Gerente Principal',
                email='gerente@suameta.com.br',
                cargo='gerente',
                is_super_admin=False,
                empresa_id=empresa.id,
                ativo=True,
                bloqueado=False
            )
            gerente.set_senha('Gerente@2025!')
            db.session.add(gerente)
            db.session.commit()
            print("   ✅ Gerente criado: gerente@suameta.com.br / Gerente@2025!")

        print("\n" + "="*70)
        print("✅ SENHAS RESETADAS COM SUCESSO!")
        print("="*70)

        print("\n🔐 CREDENCIAIS ATUALIZADAS:")
        print("\n   👑 SUPER ADMINISTRADOR")
        print("      Email: admin@suameta.com.br")
        print("      Senha: Admin@2025!")

        print("\n   🏢 GERENTE DA EMPRESA")
        print("      Email: gerente@suameta.com.br")
        print("      Senha: Gerente@2025!")

        print("\n✅ Tente fazer login agora!\n")

if __name__ == '__main__':
    resetar_senhas()
