#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script simples para criar usuário de teste"""

import os
os.environ['FLASK_ENV'] = 'development'

from app import app, db
from models import Usuario

def criar_usuario_teste():
    with app.app_context():
        email_teste = 'teste@exemplo.com'

        # Remover se já existir
        existe = Usuario.query.filter_by(email=email_teste).first()
        if existe:
            db.session.delete(existe)
            db.session.commit()
            print("Removido usuário existente")

        # Criar novo
        usuario = Usuario(
            nome='Teste Usuario',
            email=email_teste,
            cargo='usuario',
            ativo=True
        )
        usuario.set_senha('teste123')
        db.session.add(usuario)
        db.session.commit()

        print(f"✅ Usuário criado: {email_teste} / teste123")

        # Testar senha
        u = Usuario.query.filter_by(email=email_teste).first()
        if u.check_senha('teste123'):
            print("✅ Senha correta!")
        return True

if __name__ == '__main__':
    criar_usuario_teste()
