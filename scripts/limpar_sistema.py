"""
Script de Limpeza e Inicialização do Sistema
Cria usuários corretos e remove usuários antigos
"""

from app import app, db
from models import Usuario, Empresa
from werkzeug.security import generate_password_hash

def limpar_e_inicializar():
    """Limpa usuários antigos e cria usuários corretos"""

    with app.app_context():
        print("\n" + "="*70)
        print("🔧 LIMPANDO E INICIALIZANDO SISTEMA")
        print("="*70 + "\n")

        # Criar tabelas se não existirem
        db.create_all()
        print("✅ Tabelas verificadas\n")

        # ==== CRIAR EMPRESA PADRÃO ====
        print("🏢 Verificando empresa padrão...")
        empresa_principal = Empresa.query.filter_by(
            cnpj='00.000.000/0001-00'
        ).first()

        if not empresa_principal:
            empresa_principal = Empresa(
                nome='SuaMeta Sistemas',
                cnpj='00.000.000/0001-00',
                email='contato@suameta.com.br',
                telefone='(11) 99999-9999',
                cidade='São Paulo',
                estado='SP',
                ativo=True,
                bloqueado=False,
                plano='enterprise',
                max_usuarios=999,
                max_vendedores=999
            )
            db.session.add(empresa_principal)
            db.session.commit()
            print("✅ Empresa SuaMeta criada!")
        else:
            print("✅ Empresa já existe")

        # ==== REMOVER USUÁRIOS ANTIGOS ====
        print("\n🗑️  Removendo usuários antigos...")

        emails_antigos = [
            'admin@metas.com',
            'joao.silva@metas.com',
            'maria.santos@metas.com',
            'admin@suameta.com'  # Admin antigo sem .br
        ]

        removidos = 0
        for email in emails_antigos:
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario:
                print(f"   ❌ Removendo: {email}")
                db.session.delete(usuario)
                removidos += 1

        if removidos > 0:
            db.session.commit()
            print(f"✅ {removidos} usuário(s) antigo(s) removido(s)\n")
        else:
            print("✅ Nenhum usuário antigo encontrado\n")

        # ==== CRIAR SUPER ADMINISTRADOR ====
        print("👑 Criando Super Administrador...")

        super_admin = Usuario.query.filter_by(
            email='admin@suameta.com.br'
        ).first()

        if not super_admin:
            super_admin = Usuario(
                nome='Super Administrador',
                email='admin@suameta.com.br',
                cargo='admin',
                is_super_admin=True,
                empresa_id=None,  # Super admin não pertence a empresa
                ativo=True,
                bloqueado=False
            )
            super_admin.senha_hash = generate_password_hash('Admin@2025!')
            db.session.add(super_admin)
            db.session.commit()

            print("✅ Super Administrador criado!")
            print("   📧 Email: admin@suameta.com.br")
            print("   🔑 Senha: Admin@2025!")
            print("   🎯 Tipo: Super Admin (acesso total)")
        else:
            # Atualizar se já existe
            super_admin.is_super_admin = True
            super_admin.cargo = 'admin'
            super_admin.empresa_id = None
            super_admin.ativo = True
            super_admin.bloqueado = False
            super_admin.senha_hash = generate_password_hash('Admin@2025!')
            db.session.commit()
            print("✅ Super Administrador atualizado!")
            print("   📧 Email: admin@suameta.com.br")
            print("   🔑 Senha: Admin@2025!")

        # ==== CRIAR GERENTE DA EMPRESA ====
        print("\n🏢 Criando Gerente da Empresa...")

        gerente = Usuario.query.filter_by(
            email='gerente@suameta.com.br'
        ).first()

        if not gerente:
            gerente = Usuario(
                nome='Gerente Principal',
                email='gerente@suameta.com.br',
                cargo='gerente',
                is_super_admin=False,
                empresa_id=empresa_principal.id,
                ativo=True,
                bloqueado=False
            )
            gerente.senha_hash = generate_password_hash('Gerente@2025!')
            db.session.add(gerente)
            db.session.commit()

            print("✅ Gerente criado!")
            print("   📧 Email: gerente@suameta.com.br")
            print("   🔑 Senha: Gerente@2025!")
            print("   🏢 Empresa: SuaMeta Sistemas")
        else:
            # Atualizar se já existe
            gerente.cargo = 'gerente'
            gerente.is_super_admin = False
            gerente.empresa_id = empresa_principal.id
            gerente.ativo = True
            gerente.bloqueado = False
            gerente.senha_hash = generate_password_hash('Gerente@2025!')
            db.session.commit()
            print("✅ Gerente atualizado!")
            print("   📧 Email: gerente@suameta.com.br")
            print("   🔑 Senha: Gerente@2025!")

        print("\n" + "="*70)
        print("✅ SISTEMA LIMPO E INICIALIZADO COM SUCESSO!")
        print("="*70)

        print("\n📊 RESUMO:")
        print(f"   • Usuários antigos removidos: {removidos}")
        print(f"   • Super Admin: admin@suameta.com.br")
        print(f"   • Gerente: gerente@suameta.com.br")
        print(f"   • Empresa: {empresa_principal.nome}")

        print("\n🔐 CREDENCIAIS DE ACESSO:")
        print("\n   👑 SUPER ADMINISTRADOR")
        print("      Email: admin@suameta.com.br")
        print("      Senha: Admin@2025!")
        print("      Acesso: Total (todas as empresas)")

        print("\n   🏢 GERENTE DA EMPRESA")
        print("      Email: gerente@suameta.com.br")
        print("      Senha: Gerente@2025!")
        print("      Acesso: SuaMeta Sistemas")

        print("\n⚠️  IMPORTANTE: Altere as senhas após o primeiro acesso!")
        print("\n")

if __name__ == '__main__':
    limpar_e_inicializar()
