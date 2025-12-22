#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para testar registro de usuário"""

from app import app, db
from models import Usuario

with app.app_context():
    print("🧪 Testando criação de usuário...")

    # Tentar criar um novo usuário
    email_teste = 'teste@exemplo.com'

    # Verificar se já existe
    existe = Usuario.query.filter_by(email=email_teste).first()
    if existe:
        print(f"⚠️  Usuário {email_teste} já existe. Removendo...")
        db.session.delete(existe)
        db.session.commit()

    # Criar novo usuário
    novo_usuario = Usuario(
        nome='Usuário de Teste',
        email=email_teste,
        cargo='usuario',
        ativo=True
    )
    novo_usuario.set_senha('teste123')

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        print(f"✅ Usuário criado com sucesso!")
        print(f"   📧 Email: {email_teste}")
        print(f"   🔑 Senha: teste123")

        # Verificar se consegue logar
        usuario_verificado = Usuario.query.filter_by(email=email_teste).first()
        if usuario_verificado.check_senha('teste123'):
            print("✅ Senha verificada com sucesso!")
        else:
            print("❌ Erro na verificação de senha!")

    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")
        db.session.rollback()
