from app import app, db
from models import Usuario
from sqlalchemy import exc

if __name__ == '__main__':
    with app.app_context():
        try:
            u = Usuario(nome='Administrador', email='admin@metas.com', cargo='admin')
            u.set_senha('admin123')
            db.session.add(u)
            db.session.commit()
            print('Admin criado: admin@metas.com / admin123')
        except exc.IntegrityError:
            db.session.rollback()
            print('Admin já existe: admin@metas.com')
