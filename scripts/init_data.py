# init_data.py - Script para inicializar dados de exemplo

from app import app, db
from models import Usuario, Vendedor, Meta, Equipe
from datetime import datetime

def init_data():
    """Inicializa o banco de dados com dados de exemplo"""

    with app.app_context():
        # Limpa o banco de dados
        db.drop_all()
        db.create_all()

        print("\n" + "="*70)
        print("🔄 INICIALIZANDO BANCO DE DADOS COM DADOS DE EXEMPLO")
        print("="*70 + "\n")

        # 1. Criar usuários (Admin e Supervisores)
        print("👤 Criando usuários...")

        admin = Usuario(
            nome='Administrador',
            email='admin@metas.com',
            cargo='admin',
            ativo=True
        )
        admin.set_senha('admin123')
        db.session.add(admin)

        supervisor1 = Usuario(
            nome='João Silva',
            email='joao.silva@metas.com',
            cargo='supervisor',
            ativo=True
        )
        supervisor1.set_senha('supervisor123')
        db.session.add(supervisor1)

        supervisor2 = Usuario(
            nome='Maria Santos',
            email='maria.santos@metas.com',
            cargo='supervisor',
            ativo=True
        )
        supervisor2.set_senha('supervisor123')
        db.session.add(supervisor2)

        db.session.commit()
        print(f"   ✅ Admin: {admin.email} (senha: admin123)")
        print(f"   ✅ Supervisor: {supervisor1.email} (senha: supervisor123)")
        print(f"   ✅ Supervisor: {supervisor2.email} (senha: supervisor123)")

        # 2. Criar equipes
        print("\n📋 Criando equipes...")

        equipe_norte = Equipe(
            nome='Equipe Norte',
            descricao='Equipe responsável pela região Norte',
            supervisor_id=supervisor1.id,
            ativa=True
        )
        db.session.add(equipe_norte)

        equipe_sul = Equipe(
            nome='Equipe Sul',
            descricao='Equipe responsável pela região Sul',
            supervisor_id=supervisor2.id,
            ativa=True
        )
        db.session.add(equipe_sul)

        equipe_leste = Equipe(
            nome='Equipe Leste',
            descricao='Equipe responsável pela região Leste',
            supervisor_id=supervisor1.id,
            ativa=True
        )
        db.session.add(equipe_leste)

        db.session.commit()
        print(f"   ✅ {equipe_norte.nome} - Supervisor: {supervisor1.nome}")
        print(f"   ✅ {equipe_sul.nome} - Supervisor: {supervisor2.nome}")
        print(f"   ✅ {equipe_leste.nome} - Supervisor: {supervisor1.nome}")

        # 3. Criar vendedores
        print("\n👥 Criando vendedores...")

        vendedores_data = [
            {
                'nome': 'Carlos Oliveira',
                'email': 'carlos.oliveira@empresa.com',
                'telefone': '(11) 98765-4321',
                'cpf': '123.456.789-01',
                'supervisor_id': supervisor1.id,
                'supervisor_nome': supervisor1.nome,
                'equipe_id': equipe_norte.id
            },
            {
                'nome': 'Ana Paula Costa',
                'email': 'ana.costa@empresa.com',
                'telefone': '(11) 97654-3210',
                'cpf': '234.567.890-12',
                'supervisor_id': supervisor1.id,
                'supervisor_nome': supervisor1.nome,
                'equipe_id': equipe_norte.id
            },
            {
                'nome': 'Roberto Lima',
                'email': 'roberto.lima@empresa.com',
                'telefone': '(21) 96543-2109',
                'cpf': '345.678.901-23',
                'supervisor_id': supervisor2.id,
                'supervisor_nome': supervisor2.nome,
                'equipe_id': equipe_sul.id
            },
            {
                'nome': 'Patricia Alves',
                'email': 'patricia.alves@empresa.com',
                'telefone': '(21) 95432-1098',
                'cpf': '456.789.012-34',
                'supervisor_id': supervisor2.id,
                'supervisor_nome': supervisor2.nome,
                'equipe_id': equipe_sul.id
            },
            {
                'nome': 'Fernando Souza',
                'email': 'fernando.souza@empresa.com',
                'telefone': '(31) 94321-0987',
                'cpf': '567.890.123-45',
                'supervisor_id': supervisor1.id,
                'supervisor_nome': supervisor1.nome,
                'equipe_id': equipe_leste.id
            },
            {
                'nome': 'Juliana Rodrigues',
                'email': 'juliana.rodrigues@empresa.com',
                'telefone': '(31) 93210-9876',
                'cpf': '678.901.234-56',
                'supervisor_id': supervisor1.id,
                'supervisor_nome': supervisor1.nome,
                'equipe_id': equipe_leste.id
            }
        ]

        vendedores = []
        equipes_dict = {equipe_norte.id: equipe_norte, equipe_sul.id: equipe_sul, equipe_leste.id: equipe_leste}

        for v_data in vendedores_data:
            vendedor = Vendedor(**v_data)
            db.session.add(vendedor)
            vendedores.append(vendedor)
            equipe_nome = equipes_dict[v_data['equipe_id']].nome if v_data['equipe_id'] else 'Sem equipe'
            print(f"   ✅ {vendedor.nome} - Equipe: {equipe_nome}")

        db.session.commit()

        # 4. Criar metas para o mês atual
        print("\n🎯 Criando metas do mês atual...")

        mes_atual = datetime.now().month
        ano_atual = datetime.now().year

        metas_data = [
            {'vendedor': vendedores[0], 'valor_meta': 50000.00, 'receita': 58000.00},
            {'vendedor': vendedores[1], 'valor_meta': 45000.00, 'receita': 52000.00},
            {'vendedor': vendedores[2], 'valor_meta': 60000.00, 'receita': 48000.00},
            {'vendedor': vendedores[3], 'valor_meta': 55000.00, 'receita': 70000.00},
            {'vendedor': vendedores[4], 'valor_meta': 40000.00, 'receita': 38000.00},
            {'vendedor': vendedores[5], 'valor_meta': 50000.00, 'receita': 55000.00}
        ]

        for m_data in metas_data:
            meta = Meta(
                vendedor_id=m_data['vendedor'].id,
                mes=mes_atual,
                ano=ano_atual,
                valor_meta=m_data['valor_meta'],
                receita_alcancada=m_data['receita'],
                status_comissao='Pendente'
            )
            meta.calcular_comissao()
            db.session.add(meta)
            print(f"   ✅ {m_data['vendedor'].nome}: R$ {m_data['valor_meta']:,.2f} (Alcance: {meta.percentual_alcance:.1f}%)")

        db.session.commit()

        print("\n" + "="*70)
        print("✅ DADOS INICIALIZADOS COM SUCESSO!")
        print("="*70)
        print("\n📊 Resumo:")
        print(f"   • {Usuario.query.count()} usuários cadastrados")
        print(f"   • {Equipe.query.count()} equipes criadas")
        print(f"   • {Vendedor.query.count()} vendedores cadastrados")
        print(f"   • {Meta.query.count()} metas cadastradas")

        print("\n🔑 Credenciais de Acesso:")
        print("   Admin:")
        print("      Email: admin@metas.com")
        print("      Senha: admin123")
        print("\n   Supervisor 1:")
        print("      Email: joao.silva@metas.com")
        print("      Senha: supervisor123")
        print("\n   Supervisor 2:")
        print("      Email: maria.santos@metas.com")
        print("      Senha: supervisor123")
        print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    init_data()
