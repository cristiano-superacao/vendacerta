#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de inicialização do banco de dados para produção
Cria tabelas e usuários corretos
"""

import os
import sys

# Adicionar diretório pai ao path para importar app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Verificar se deve apenas inicializar DB (Railway)
INIT_DB_ONLY = os.environ.get('INIT_DB_ONLY', '0') == '1'

from app import app, db
from models import (
    Usuario, Empresa, Vendedor, Meta, Equipe, 
    FaixaComissao, FaixaComissaoVendedor, FaixaComissaoSupervisor, 
    Mensagem, Cliente, CompraCliente
)

def init_database():
    """Inicializa o banco de dados com tabelas e usuários corretos"""

    with app.app_context():
        print("\n" + "="*70)
        print("🔧 INICIALIZANDO BANCO DE DADOS")
        print("="*70 + "\n")

        # Criar todas as tabelas
        db.create_all()
        print("✅ Tabelas criadas com sucesso!\n")

        # Verificar ambiente
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if 'postgresql' in db_uri:
            print("🗄️  Banco: PostgreSQL (Produção)")
        else:
            print("🗄️  Banco: SQLite (Desenvolvimento)")

        # ==== CRIAR EMPRESA PADRÃO ====
        print("\n🏢 Verificando empresa padrão...")
        empresa = Empresa.query.filter_by(cnpj='00.000.000/0001-00').first()

        if not empresa:
            empresa = Empresa(
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
            db.session.add(empresa)
            db.session.commit()
            print("✅ Empresa SuaMeta criada!")
        else:
            print("✅ Empresa já existe")

        # ==== LIMPAR USUÁRIOS ANTIGOS ====
        print("\n🗑️  Limpando usuários antigos...")
        emails_antigos = [
            'admin@metas.com',
            'admin@suameta.com',  # Sem .br
            'joao.silva@metas.com',
            'maria.santos@metas.com'
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
            print(f"✅ {removidos} usuário(s) antigo(s) removido(s)")
        else:
            print("✅ Nenhum usuário antigo encontrado")

        # ==== CRIAR SUPER ADMINISTRADOR ====
        print("\n👑 Criando Super Administrador...")
        super_admin = Usuario.query.filter_by(
            email='admin@suameta.com.br'
        ).first()

        if not super_admin:
            super_admin = Usuario(
                nome='Super Administrador',
                email='admin@suameta.com.br',
                cargo='admin',
                is_super_admin=True,
                empresa_id=None,
                ativo=True,
                bloqueado=False
            )
            super_admin.set_senha('Admin@2025!')
            db.session.add(super_admin)
            db.session.commit()

            print("✅ Super Admin criado!")
            print("   📧 Email: admin@suameta.com.br")
            print("   🔑 Senha: Admin@2025!")
        else:
            # Atualizar se já existe
            super_admin.is_super_admin = True
            super_admin.cargo = 'admin'
            super_admin.empresa_id = None
            super_admin.ativo = True
            super_admin.bloqueado = False
            super_admin.set_senha('Admin@2025!')
            db.session.commit()
            print("✅ Super Admin atualizado!")
            print("   📧 Email: admin@suameta.com.br")
            print("   🔑 Senha: Admin@2025!")

        # ==== CRIAR GERENTE ====
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
                empresa_id=empresa.id,
                ativo=True,
                bloqueado=False
            )
            gerente.set_senha('Gerente@2025!')
            db.session.add(gerente)
            db.session.commit()

            print("✅ Gerente criado!")
            print("   📧 Email: gerente@suameta.com.br")
            print("   🔑 Senha: Gerente@2025!")
        else:
            # Atualizar se já existe
            gerente.cargo = 'gerente'
            gerente.is_super_admin = False
            gerente.empresa_id = empresa.id
            gerente.ativo = True
            gerente.bloqueado = False
            gerente.set_senha('Gerente@2025!')
            db.session.commit()
            print("✅ Gerente atualizado!")
            print("   📧 Email: gerente@suameta.com.br")
            print("   🔑 Senha: Gerente@2025!")

        print("\n" + "="*70)
        print("✅ BANCO DE DADOS INICIALIZADO COM SUCESSO!")
        print("="*70)

        print("\n🔐 CREDENCIAIS DE ACESSO:")
        print("\n   👑 SUPER ADMINISTRADOR")
        print("      Email: admin@suameta.com.br")
        print("      Senha: Admin@2025!")

        print("\n   🏢 GERENTE DA EMPRESA")
        print("      Email: gerente@suameta.com.br")
        print("      Senha: Gerente@2025!")

        print("\n⚠️  IMPORTANTE: Altere as senhas após o primeiro acesso!\n")

        # Se for apenas inicialização, encerrar com sucesso
        if INIT_DB_ONLY:
            print("\n✅ Inicialização concluída. O gunicorn será iniciado em seguida.\n")
            sys.exit(0)

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ ERRO NA INICIALIZAÇÃO: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
