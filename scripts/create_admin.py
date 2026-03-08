import os

from app import app, db
from models import Usuario
from sqlalchemy import exc

if __name__ == '__main__':
    with app.app_context():
        try:
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@metas.com').strip().lower()
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
            u = Usuario(nome='Administrador', email=admin_email, cargo='admin', ativo=True)
            u.set_senha(admin_password)
            db.session.add(u)
            db.session.commit()
            print(f'Admin criado: {admin_email} / {admin_password}')
        except exc.IntegrityError:
            db.session.rollback()
            print(f'Admin já existe: {os.environ.get("ADMIN_EMAIL", "admin@metas.com")}')
