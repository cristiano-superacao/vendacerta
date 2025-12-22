"""
Teste final do login via HTTP
"""
import requests

try:
    print("="*70)
    print("TESTE FINAL - LOGIN VIA HTTP")
    print("="*70)
    
    # 1. Verificar se a página de login carrega
    print("\n1. Verificando pagina de login...")
    response = requests.get("http://127.0.0.1:5001/login")
    print(f"   Status: {response.status_code}")
    print(f"   OK: {response.status_code == 200}")
    
    # 2. Tentar fazer login
    print("\n2. Tentando fazer login...")
    session = requests.Session()
    
    # Primeiro, pegar a página de login para obter o token CSRF
    response = session.get("http://127.0.0.1:5001/login")
    
    # Extrair token CSRF do formulário
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    
    if csrf_token:
        csrf_value = csrf_token.get('value')
        print(f"   Token CSRF obtido: {csrf_value[:20]}...")
        
        # Fazer POST com as credenciais
        login_data = {
            'csrf_token': csrf_value,
            'email': 'admin@vendacerta.com',
            'senha': 'admin123',
            'submit': 'Entrar'
        }
        
        response = session.post(
            "http://127.0.0.1:5001/login",
            data=login_data,
            allow_redirects=False
        )
        
        print(f"   Status da resposta: {response.status_code}")
        
        if response.status_code == 302:
            print(f"   [OK] Redirecionamento: {response.headers.get('Location')}")
            print("\n   => LOGIN FUNCIONANDO PERFEITAMENTE!")
        elif response.status_code == 200:
            # Verificar se há mensagem de erro
            soup = BeautifulSoup(response.text, 'html.parser')
            alerts = soup.find_all('div', class_='alert')
            if alerts:
                print(f"   [AVISO] Resposta 200 com alertas:")
                for alert in alerts:
                    print(f"      - {alert.get_text(strip=True)}")
            else:
                print("   [AVISO] Resposta 200 mas sem redirecionamento")
        else:
            print(f"   [ERRO] Status inesperado: {response.status_code}")
    else:
        print("   [AVISO] Token CSRF nao encontrado no formulario")
    
    # 3. Verificar Bootstrap
    print("\n3. Verificando Bootstrap...")
    response = requests.get("http://127.0.0.1:5001/static/css/bootstrap.min.css")
    print(f"   Status: {response.status_code}")
    print(f"   Tamanho: {len(response.content)} bytes")
    
    print("\n" + "="*70)
    print("TESTE CONCLUIDO")
    print("="*70)
    
except Exception as e:
    print(f"\n[ERRO] {e}")
    import traceback
    traceback.print_exc()
