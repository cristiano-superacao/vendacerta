import os
import sys

# Garante import do app mesmo se o script rodar fora do cwd do repo.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

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
