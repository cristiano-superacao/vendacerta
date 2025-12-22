import os
import sys
from werkzeug.security import generate_password_hash

# Adicionar diretório atual ao path
sys.path.append(os.getcwd())

from app import app, db
from models import Usuario, Empresa

def reset_admin():
    print("="*60)
    print("SCRIPT DE RECUPERAÇÃO DE ACESSO - SUPER ADMIN")
    print("="*60)

    with app.app_context():
        # 1. Verificar se existe empresa padrão
        empresa = Empresa.query.filter_by(cnpj='00000000000000').first()
        if not empresa:
            print("⚠️ Empresa padrão não encontrada. Criando...")
            empresa = Empresa(
                nome='Empresa Padrão',
                cnpj='00000000000000',
                email='contato@empresa.com',
                plano='enterprise',
                ativo=True
            )
            db.session.add(empresa)
            db.session.commit()
            print("✅ Empresa padrão criada.")
        else:
            print(f"✅ Empresa padrão encontrada: {empresa.nome}")

        # 2. Lista de emails para verificar/resetar
        emails_admin = ['admin@metas.com', 'admin@vendacerta.com']
        admin_encontrado = False

        for email in emails_admin:
            usuario = Usuario.query.filter_by(email=email).first()
            
            if usuario:
                print(f"\n🔄 Usuário encontrado: {email}")
                print("   Resetando senha para: admin123")
                
                usuario.senha_hash = generate_password_hash('admin123')
                usuario.is_super_admin = True
                usuario.ativo = True
                usuario.bloqueado = False
                usuario.cargo = 'admin'
                usuario.empresa_id = empresa.id
                
                # Garantir todas as permissões
                usuario.pode_ver_dashboard = True
                usuario.pode_enviar_mensagens = True
                usuario.pode_exportar_dados = True
                usuario.pode_gerenciar_vendedores = True
                usuario.pode_gerenciar_metas = True
                usuario.pode_gerenciar_equipes = True
                usuario.pode_gerenciar_comissoes = True
                usuario.pode_ver_todas_metas = True
                usuario.pode_aprovar_comissoes = True
                usuario.pode_acessar_clientes = True
                usuario.pode_criar_clientes = True
                usuario.pode_editar_clientes = True
                usuario.pode_excluir_clientes = True
                usuario.pode_importar_clientes = True
                
                db.session.commit()
                print("✅ Senha e permissões atualizadas com sucesso!")
                admin_encontrado = True
        
        # 3. Se nenhum admin foi encontrado, criar um novo
        if not admin_encontrado:
            print("\n⚠️ Nenhum usuário admin encontrado. Criando novo...")
            novo_admin = Usuario(
                nome='Super Administrador',
                email='admin@metas.com',
                senha_hash=generate_password_hash('admin123'),
                cargo='admin',
                is_super_admin=True,
                ativo=True,
                empresa_id=empresa.id,
                # Permissões
                pode_ver_dashboard=True,
                pode_enviar_mensagens=True,
                pode_exportar_dados=True,
                pode_gerenciar_vendedores=True,
                pode_gerenciar_metas=True,
                pode_gerenciar_equipes=True,
                pode_gerenciar_comissoes=True,
                pode_ver_todas_metas=True,
                pode_aprovar_comissoes=True,
                pode_acessar_clientes=True,
                pode_criar_clientes=True,
                pode_editar_clientes=True,
                pode_excluir_clientes=True,
                pode_importar_clientes=True
            )
            db.session.add(novo_admin)
            db.session.commit()
            print("✅ Usuário 'admin@metas.com' criado com sucesso!")

    print("\n" + "="*60)
    print("DADOS DE ACESSO ATUALIZADOS:")
    print("📧 Email: admin@metas.com")
    print("🔑 Senha: admin123")
    print("="*60)

if __name__ == "__main__":
    try:
        reset_admin()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
