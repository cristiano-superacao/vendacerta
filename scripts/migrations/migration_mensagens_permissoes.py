"""
Script de Migração - Sistema de Mensagens e Permissões
Adiciona a tabela de mensagens e campos de permissões aos usuários
"""

import os
import sys
from sqlalchemy import text

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models import Usuario, Mensagem

def migrar_banco():
    """Executa a migração do banco de dados"""
    print("🔄 Iniciando migração do banco de dados...")

    with app.app_context():
        try:
            # 1. Criar tabela de mensagens
            print("\n📧 Criando tabela de mensagens...")
            db.create_all()
            print("✅ Tabela de mensagens criada com sucesso!")

            # 2. Adicionar campos de permissões aos usuários existentes
            print("\n🔐 Adicionando campos de permissões aos usuários...")

            # Verificar se as colunas já existem
            inspector = db.inspect(db.engine)
            colunas_existentes = [col['name'] for col in inspector.get_columns('usuarios')]

            # Lista de novas colunas
            novas_colunas = {
                'vendedor_id': 'INTEGER NULL',  # Relacionamento com vendedor
                'pode_ver_dashboard': 'BOOLEAN DEFAULT TRUE',
                'pode_gerenciar_vendedores': 'BOOLEAN DEFAULT FALSE',
                'pode_gerenciar_metas': 'BOOLEAN DEFAULT FALSE',
                'pode_gerenciar_equipes': 'BOOLEAN DEFAULT FALSE',
                'pode_gerenciar_comissoes': 'BOOLEAN DEFAULT FALSE',
                'pode_enviar_mensagens': 'BOOLEAN DEFAULT TRUE',
                'pode_exportar_dados': 'BOOLEAN DEFAULT FALSE',
                'pode_ver_todas_metas': 'BOOLEAN DEFAULT FALSE',
                'pode_aprovar_comissoes': 'BOOLEAN DEFAULT FALSE'
            }

            # Adicionar colunas que não existem
            for coluna, tipo in novas_colunas.items():
                if coluna not in colunas_existentes:
                    try:
                        # PostgreSQL
                        sql = f'ALTER TABLE usuarios ADD COLUMN {coluna} {tipo}'
                        db.session.execute(text(sql))
                        db.session.commit()
                        print(f"  ✅ Coluna '{coluna}' adicionada")
                    except Exception as e:
                        print(f"  ℹ️  Coluna '{coluna}' já existe ou erro: {str(e)}")
                        db.session.rollback()
                else:
                    print(f"  ℹ️  Coluna '{coluna}' já existe")

            # 3. Configurar permissões padrão por cargo
            print("\n⚙️  Configurando permissões padrão por cargo...")

            usuarios = Usuario.query.all()
            for usuario in usuarios:
                if usuario.is_super_admin:
                    # Super Admin - todas as permissões
                    usuario.pode_ver_dashboard = True
                    usuario.pode_gerenciar_vendedores = True
                    usuario.pode_gerenciar_metas = True
                    usuario.pode_gerenciar_equipes = True
                    usuario.pode_gerenciar_comissoes = True
                    usuario.pode_enviar_mensagens = True
                    usuario.pode_exportar_dados = True
                    usuario.pode_ver_todas_metas = True
                    usuario.pode_aprovar_comissoes = True
                    print(f"  ✅ Super Admin: {usuario.nome} - Todas as permissões")

                elif usuario.cargo == 'admin':
                    # Administrador - quase todas as permissões
                    usuario.pode_ver_dashboard = True
                    usuario.pode_gerenciar_vendedores = True
                    usuario.pode_gerenciar_metas = True
                    usuario.pode_gerenciar_equipes = True
                    usuario.pode_gerenciar_comissoes = True
                    usuario.pode_enviar_mensagens = True
                    usuario.pode_exportar_dados = True
                    usuario.pode_ver_todas_metas = True
                    usuario.pode_aprovar_comissoes = True
                    print(f"  ✅ Admin: {usuario.nome} - Todas as permissões da empresa")

                elif usuario.cargo == 'gerente':
                    # Gerente - permissões de gestão
                    usuario.pode_ver_dashboard = True
                    usuario.pode_gerenciar_vendedores = True
                    usuario.pode_gerenciar_metas = True
                    usuario.pode_gerenciar_equipes = True
                    usuario.pode_gerenciar_comissoes = False
                    usuario.pode_enviar_mensagens = True
                    usuario.pode_exportar_dados = True
                    usuario.pode_ver_todas_metas = True
                    usuario.pode_aprovar_comissoes = True
                    print(f"  ✅ Gerente: {usuario.nome} - Permissões de gestão")

                elif usuario.cargo == 'supervisor':
                    # Supervisor - permissões da equipe
                    usuario.pode_ver_dashboard = True
                    usuario.pode_gerenciar_vendedores = False
                    usuario.pode_gerenciar_metas = True
                    usuario.pode_gerenciar_equipes = True
                    usuario.pode_gerenciar_comissoes = False
                    usuario.pode_enviar_mensagens = True
                    usuario.pode_exportar_dados = True
                    usuario.pode_ver_todas_metas = False
                    usuario.pode_aprovar_comissoes = False
                    print(f"  ✅ Supervisor: {usuario.nome} - Permissões de equipe")

                elif usuario.cargo == 'vendedor':
                    # Vendedor - apenas visualização
                    usuario.pode_ver_dashboard = True
                    usuario.pode_gerenciar_vendedores = False
                    usuario.pode_gerenciar_metas = False
                    usuario.pode_gerenciar_equipes = False
                    usuario.pode_gerenciar_comissoes = False
                    usuario.pode_enviar_mensagens = True
                    usuario.pode_exportar_dados = False
                    usuario.pode_ver_todas_metas = False
                    usuario.pode_aprovar_comissoes = False
                    print(f"  ✅ Vendedor: {usuario.nome} - Apenas visualização")

                else:
                    # Usuário padrão - permissões mínimas
                    usuario.pode_ver_dashboard = True
                    usuario.pode_gerenciar_vendedores = False
                    usuario.pode_gerenciar_metas = False
                    usuario.pode_gerenciar_equipes = False
                    usuario.pode_gerenciar_comissoes = False
                    usuario.pode_enviar_mensagens = True
                    usuario.pode_exportar_dados = False
                    usuario.pode_ver_todas_metas = False
                    usuario.pode_aprovar_comissoes = False
                    print(f"  ✅ Usuário: {usuario.nome} - Permissões mínimas")

            db.session.commit()

            # 4. Verificar criação
            print("\n📊 Verificando migração...")
            total_usuarios = Usuario.query.count()
            total_mensagens = Mensagem.query.count()

            print(f"  ✅ Total de usuários: {total_usuarios}")
            print(f"  ✅ Total de mensagens: {total_mensagens}")

            # 5. Criar mensagem de boas-vindas para todos os usuários
            print("\n📨 Criando mensagens de boas-vindas...")

            # Buscar ou criar usuário sistema
            sistema = Usuario.query.filter_by(email='sistema@suameta.com').first()
            if not sistema:
                sistema = Usuario(
                    nome='Sistema',
                    email='sistema@suameta.com',
                    cargo='admin',
                    is_super_admin=True,
                    ativo=True
                )
                sistema.set_senha('sistema123')
                db.session.add(sistema)
                db.session.commit()
                print("  ✅ Usuário 'Sistema' criado")

            # Enviar mensagem de boas-vindas para cada usuário
            usuarios_ativos = Usuario.query.filter_by(ativo=True).all()
            for usuario in usuarios_ativos:
                if usuario.id != sistema.id:
                    # Verificar se já recebeu mensagem de boas-vindas
                    mensagem_existe = Mensagem.query.filter_by(
                        remetente_id=sistema.id,
                        destinatario_id=usuario.id,
                        tipo='sistema'
                    ).first()

                    if not mensagem_existe:
                        mensagem_boasvindas = Mensagem(
                            remetente_id=sistema.id,
                            destinatario_id=usuario.id,
                            assunto='🎉 Bem-vindo ao Sistema de Mensagens!',
                            mensagem=f"""Olá {usuario.nome}!

Seja bem-vindo(a) ao novo sistema de mensagens do SuaMeta!

Agora você pode:
✅ Enviar mensagens para outros membros da equipe
✅ Receber notificações importantes
✅ Comunicar-se de forma rápida e eficiente

Suas permissões:
• Dashboard: {'✅' if usuario.pode_ver_dashboard else '❌'}
• Enviar Mensagens: {'✅' if usuario.pode_enviar_mensagens else '❌'}
• Gerenciar Vendedores: {'✅' if usuario.pode_gerenciar_vendedores else '❌'}
• Gerenciar Metas: {'✅' if usuario.pode_gerenciar_metas else '❌'}
• Exportar Dados: {'✅' if usuario.pode_exportar_dados else '❌'}

Para começar, clique em "Mensagens" no menu lateral.

Bom trabalho!
Equipe SuaMeta
""",
                            prioridade='normal',
                            tipo='sistema'
                        )
                        db.session.add(mensagem_boasvindas)
                        print(f"  ✅ Mensagem de boas-vindas enviada para {usuario.nome}")

            db.session.commit()

            print("\n" + "=" * 70)
            print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 70)
            print("\n📋 Resumo:")
            print(f"  • Tabela de mensagens criada")
            print(f"  • {len(novas_colunas)} colunas de permissões adicionadas")
            print(f"  • {total_usuarios} usuários configurados com permissões")
            print(f"  • Mensagens de boas-vindas enviadas")
            print("\n🚀 O sistema está pronto para uso!")

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERRO na migração: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    return True

if __name__ == '__main__':
    print("=" * 70)
    print("SISTEMA DE MENSAGENS E PERMISSÕES - MIGRAÇÃO")
    print("=" * 70)

    confirma = input("\n⚠️  Esta migração irá modificar o banco de dados. Continuar? (s/n): ")

    if confirma.lower() == 's':
        sucesso = migrar_banco()
        if sucesso:
            print("\n✅ Migração finalizada com sucesso!")
        else:
            print("\n❌ Migração falhou. Verifique os erros acima.")
    else:
        print("\n❌ Migração cancelada pelo usuário.")
