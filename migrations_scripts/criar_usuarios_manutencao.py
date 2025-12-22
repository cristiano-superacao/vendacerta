"""
Script para criar usuários de teste para o sistema de manutenção
"""
import sys
from app import app, db
from models import Usuario, Empresa, Tecnico, Cliente
from werkzeug.security import generate_password_hash
from datetime import datetime

def criar_usuarios_manutencao():
    """Cria usuários de teste para manutenção"""
    with app.app_context():
        print("🔧 Criando usuários de teste para sistema de manutenção...\n")
        
        # Buscar empresa padrão
        empresa = Empresa.query.first()
        if not empresa:
            print("❌ Nenhuma empresa encontrada! Execute init_db.py primeiro.")
            return
        
        print(f"✅ Empresa encontrada: {empresa.nome}\n")
        
        # Lista de usuários para criar
        usuarios = [
            {
                'nome': 'Admin Sistema',
                'email': 'admin@vendacerta.com',
                'cargo': 'admin',
                'criar_tecnico': False
            },
            {
                'nome': 'Maria Silva - Administrativo',
                'email': 'administrativo@vendacerta.com',
                'cargo': 'administrativo',
                'criar_tecnico': False
            },
            {
                'nome': 'Carlos Souza - Supervisor Manutenção',
                'email': 'supervisor.manutencao@vendacerta.com',
                'cargo': 'supervisor_manutencao',
                'criar_tecnico': False
            },
            {
                'nome': 'João Santos - Técnico',
                'email': 'tecnico1@vendacerta.com',
                'cargo': 'tecnico',
                'criar_tecnico': True,
                'tecnico_info': {
                    'cpf': '12345678901',
                    'telefone': '(11) 98765-4321',
                    'especialidades': 'Impressoras\nComputadores\nRedes'
                }
            },
            {
                'nome': 'Ana Costa - Técnico',
                'email': 'tecnico2@vendacerta.com',
                'cargo': 'tecnico',
                'criar_tecnico': True,
                'tecnico_info': {
                    'cpf': '98765432100',
                    'telefone': '(11) 91234-5678',
                    'especialidades': 'Notebooks\nHardware\nSoftware'
                }
            }
        ]
        
        senha_padrao = '123456'
        usuarios_criados = 0
        tecnicos_criados = 0
        
        for user_data in usuarios:
            # Verificar se já existe
            usuario_existe = Usuario.query.filter_by(email=user_data['email']).first()
            if usuario_existe:
                print(f"⚠️  Usuário {user_data['nome']} já existe (pulando)")
                continue
            
            # Criar usuário
            usuario = Usuario(
                nome=user_data['nome'],
                email=user_data['email'],
                senha_hash=generate_password_hash(senha_padrao),
                cargo=user_data['cargo'],
                empresa_id=empresa.id,
                ativo=True,
                data_criacao=datetime.now()
            )
            
            db.session.add(usuario)
            db.session.flush()  # Para obter o ID
            
            print(f"✅ Usuário criado: {user_data['nome']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Cargo: {user_data['cargo']}")
            print(f"   Senha: {senha_padrao}")
            
            usuarios_criados += 1
            
            # Criar técnico se necessário
            if user_data.get('criar_tecnico'):
                tecnico_info = user_data['tecnico_info']
                tecnico = Tecnico(
                    nome=user_data['nome'],
                    cpf=tecnico_info['cpf'],
                    telefone=tecnico_info['telefone'],
                    especialidades=tecnico_info['especialidades'],
                    usuario_id=usuario.id,
                    empresa_id=empresa.id,
                    ativo=True,
                    disponivel=True,
                    total_os=0,
                    os_concluidas=0,
                    avaliacao_media=0.0,
                    data_cadastro=datetime.now()
                )
                
                db.session.add(tecnico)
                print(f"   🔧 Técnico vinculado: CPF {tecnico_info['cpf']}")
                tecnicos_criados += 1
            
            print()
        
        # Criar alguns clientes de teste se não existir
        if Cliente.query.count() == 0:
            print("📝 Criando clientes de teste...\n")
            clientes = [
                {
                    'nome': 'Empresa Alpha LTDA',
                    'cnpj': '12345678000190',
                    'telefone': '(11) 3333-4444',
                    'email': 'contato@alpha.com.br'
                },
                {
                    'nome': 'José Silva',
                    'cpf': '11122233344',
                    'celular': '(11) 99999-8888',
                    'email': 'jose@email.com'
                }
            ]
            
            for cliente_data in clientes:
                cliente = Cliente(
                    nome=cliente_data['nome'],
                    cpf=cliente_data.get('cpf'),
                    cnpj=cliente_data.get('cnpj'),
                    telefone=cliente_data.get('telefone'),
                    celular=cliente_data.get('celular'),
                    email=cliente_data.get('email'),
                    empresa_id=empresa.id,
                    data_cadastro=datetime.now()
                )
                db.session.add(cliente)
                print(f"✅ Cliente criado: {cliente_data['nome']}")
        
        # Salvar tudo
        try:
            db.session.commit()
            print("\n" + "="*60)
            print(f"✅ SUCESSO!")
            print(f"   {usuarios_criados} usuários criados")
            print(f"   {tecnicos_criados} técnicos vinculados")
            print("="*60)
            print("\n📋 CREDENCIAIS DE ACESSO:")
            print("-" * 60)
            for user_data in usuarios:
                print(f"   {user_data['cargo'].upper()}")
                print(f"   Email: {user_data['email']}")
                print(f"   Senha: {senha_padrao}")
                print()
            print("="*60)
            print("\n🚀 Acesse: http://127.0.0.1:5001/login")
            print("💡 Use as credenciais acima para testar o sistema\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Erro ao salvar no banco: {e}")
            sys.exit(1)

if __name__ == '__main__':
    criar_usuarios_manutencao()
