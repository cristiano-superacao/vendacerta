"""
Inicialização do banco de dados para Railway
Executa antes do Gunicorn iniciar
"""
import os
import sys

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

def init_database():
    """Inicializa o banco de dados se necessário"""
    try:
        from app import app, db
        from models import Usuario
        
        with app.app_context():
            # Criar todas as tabelas
            db.create_all()
            print("[OK] Tabelas do banco de dados criadas/verificadas!")
            
            # Verificar se existe usuário admin
            admin = Usuario.query.filter_by(email='admin@vendacerta.com').first()
            if not admin:
                print("[PROC] Criando usuario admin padrao...")
                from werkzeug.security import generate_password_hash
                
                admin = Usuario(
                    nome='Administrador',
                    email='admin@vendacerta.com',
                    senha_hash=generate_password_hash('admin123'),
                    cargo='admin',
                    is_super_admin=True,
                    ativo=True
                )
                db.session.add(admin)
                db.session.commit()
                print("[OK] Usuario admin criado!")
                print("    Email: admin@vendacerta.com")
                print("    Senha: admin123")
            else:
                print("[OK] Usuario admin ja existe")
            
            return True
            
    except Exception as e:
        print(f"[ERRO] Erro ao inicializar banco: {e}")
        # Não falhar o deploy por causa disso
        # O app.py também tenta inicializar
        return False

if __name__ == '__main__':
    print("="*70)
    print("INICIALIZACAO DO BANCO DE DADOS - RAILWAY")
    print("="*70)
    init_database()
    print("="*70)
