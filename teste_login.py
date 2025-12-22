"""
Script de teste para identificar o erro 500 no login
"""
import sys
sys.path.insert(0, '.')

try:
    from app import app, db
    from models import Usuario
    from werkzeug.security import check_password_hash
    
    print("=" * 60)
    print("TESTE DE LOGIN - Diagnóstico de Erro 500")
    print("=" * 60)
    
    with app.app_context():
        # Buscar usuário admin
        usuario = Usuario.query.filter_by(email='admin@vendacerta.com').first()
        
        if usuario:
            print(f"\n[OK] Usuário encontrado: {usuario.nome}")
            print(f"   Email: {usuario.email}")
            print(f"   Cargo: {usuario.cargo}")
            print(f"   Ativo: {usuario.ativo}")
            print(f"   Senha Hash existe: {bool(usuario.senha_hash)}")
            print(f"   Tamanho hash: {len(usuario.senha_hash) if usuario.senha_hash else 0}")
            
            # Testar senha
            senha_teste = "admin123"
            print(f"\n[SEC] Testando senha: {senha_teste}")
            
            try:
                resultado = usuario.check_senha(senha_teste)
                print(f"   [OK] Método check_senha executou: {resultado}")
            except Exception as e:
                print(f"   [ERRO] ERRO no check_senha: {type(e).__name__}: {e}")
                
            # Testar diretamente
            try:
                resultado_direto = check_password_hash(usuario.senha_hash, senha_teste)
                print(f"   [OK] check_password_hash direto: {resultado_direto}")
            except Exception as e:
                print(f"   [ERRO] ERRO no check_password_hash direto: {type(e).__name__}: {e}")
                
        else:
            print("\n[ERRO] Usuário admin@vendacerta.com não encontrado!")
            print("\nUsuários no banco:")
            usuarios = Usuario.query.all()
            for u in usuarios:
                print(f"   - {u.email} ({u.nome})")
                
        # Testar form
        print("\n" + "=" * 60)
        print("TESTE DE FORMULÁRIO")
        print("=" * 60)
        
        from forms import LoginForm
        from flask import Flask
        
        test_app = Flask(__name__)
        test_app.config['SECRET_KEY'] = 'test'
        test_app.config['WTF_CSRF_ENABLED'] = False
        
        with test_app.test_request_context(method='POST', data={
            'email': 'admin@vendacerta.com',
            'senha': 'admin123'
        }):
            form = LoginForm()
            print(f"\n[OK] Form criado")
            print(f"   Email: {form.email.data}")
            print(f"   Senha: {'*' * len(form.senha.data) if form.senha.data else 'None'}")
            
            if form.validate():
                print(f"   [OK] Form validado com sucesso")
            else:
                print(f"   [ERRO] Erros de validação: {form.errors}")
                
except Exception as e:
    print(f"\n[ERRO] ERRO GERAL: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    
print("\n" + "=" * 60)
