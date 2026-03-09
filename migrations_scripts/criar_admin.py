#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para criar usuário administrador
"""

import os
import sys

# Garante que o diretório raiz do projeto esteja no PYTHONPATH,
# mesmo quando o script é executado fora do cwd do repo (ex.: `railway run`).
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app, db
from models import Usuario, Empresa

def criar_admin():
    """Cria usuário administrador padrão"""
    
    with app.app_context():
        print("\n" + "="*70)
        print("🔐 CRIANDO USUÁRIO ADMINISTRADOR")
        print("="*70 + "\n")
        
        # Permite parametrizar credenciais via env (útil para seed e Railway)
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@metas.com').strip().lower()
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        admin_existe = Usuario.query.filter_by(email=admin_email).first()
        
        if admin_existe:
            print(f"⚠️  Admin já existe: {admin_email}")
            print(f"📧 Email: {admin_email}")
            print("🔑 Resetando senha do admin...")
            
            # Resetar senha
            admin_existe.set_senha(admin_password)
            admin_existe.ativo = True
            admin_existe.bloqueado = False
            admin_existe.cargo = 'admin'
            admin_existe.is_super_admin = True
            db.session.commit()
            
            print("\n✅ Senha resetada com sucesso!")
        else:
            print(f"➕ Criando novo administrador...")
            
            # Criar empresa padrão se não existir
            empresa = Empresa.query.filter_by(cnpj='00000000000000').first()
            if not empresa:
                empresa = Empresa(
                    nome='Empresa Padrão',
                    cnpj='00000000000000',
                    email='contato@empresa.com',
                    telefone='(00) 0000-0000',
                    plano='premium',
                    max_usuarios=100,
                    max_vendedores=500,
                    ativo=True,
                    bloqueado=False
                )
                db.session.add(empresa)
                db.session.commit()
                print(f"   ✅ Empresa criada: {empresa.nome}")
            
            # Criar admin
            admin = Usuario(
                nome='Administrador',
                email=admin_email,
                cargo='admin',
                empresa_id=empresa.id,
                is_super_admin=True,
                ativo=True,
                bloqueado=False
            )
            admin.set_senha(admin_password)
            db.session.add(admin)
            db.session.commit()
            
            print(f"\n✅ Administrador criado com sucesso!")
        
        print("\n" + "="*70)
        print("📋 CREDENCIAIS DE ACESSO")
        print("="*70)
        print(f"\n📧 Email:  {admin_email}")
        print("🔑 Senha:  (definida via ADMIN_PASSWORD)")
        print(f"\n🌐 Acesse: http://127.0.0.1:5001/login")
        print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    criar_admin()
