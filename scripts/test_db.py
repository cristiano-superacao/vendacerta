#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script de teste do banco de dados"""

from app import app, db
from models import Usuario

with app.app_context():
    print("🔍 Verificando usuários no banco...")
    usuarios = Usuario.query.all()
    print(f"Total de usuários: {len(usuarios)}")

    for u in usuarios:
        print(f"  - {u.nome} ({u.email}) - Cargo: {u.cargo}")

    print("\n🔍 Procurando admin@suameta.com...")
    admin = Usuario.query.filter_by(email='admin@suameta.com').first()

    if admin:
        print("✅ Admin encontrado!")
        print(f"  Nome: {admin.nome}")
        print(f"  Email: {admin.email}")
        print(f"  Cargo: {admin.cargo}")
        print(f"  Ativo: {admin.ativo}")

        # Testar senha
        if admin.check_senha('admin123'):
            print("✅ Senha 'admin123' está correta!")
        else:
            print("❌ Senha 'admin123' está incorreta!")
            print("🔧 Resetando senha...")
            admin.set_senha('admin123')
            db.session.commit()
            print("✅ Senha resetada para 'admin123'")
    else:
        print("❌ Admin não encontrado!")
        print("🔧 Criando usuário admin...")
        admin = Usuario(
            nome='Administrador',
            email='admin@suameta.com',
            cargo='admin',
            ativo=True
        )
        admin.set_senha('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuário admin criado!")
        print("  📧 Email: admin@suameta.com")
        print("  🔑 Senha: admin123")
