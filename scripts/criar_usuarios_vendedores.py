#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para criar usuários de login para vendedores existentes
Versão: v2.8.0
Data: 2024
Descrição: Cria contas de usuário (cargo='vendedor') para todos os vendedores cadastrados
"""

import sys
import os

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Vendedor, Usuario
import secrets
import string

def gerar_senha_temporaria(tamanho=8):
    """Gera uma senha temporária aleatória"""
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))

def criar_usuarios_vendedores():
    """Cria usuários para vendedores que ainda não têm"""
    with app.app_context():
        print("=" * 60)
        print("CRIAÇÃO DE USUÁRIOS PARA VENDEDORES")
        print("=" * 60)
        print()

        # Buscar todos os vendedores ativos
        vendedores = Vendedor.query.filter_by(ativo=True).all()
        print(f"✓ Total de vendedores ativos: {len(vendedores)}")
        print()

        # Verificar quais já têm usuário
        vendedores_sem_usuario = []
        for vendedor in vendedores:
            usuario_existente = Usuario.query.filter_by(vendedor_id=vendedor.id).first()
            if not usuario_existente:
                vendedores_sem_usuario.append(vendedor)

        print(f"✓ Vendedores sem usuário: {len(vendedores_sem_usuario)}")
        print(f"✓ Vendedores já com usuário: {len(vendedores) - len(vendedores_sem_usuario)}")
        print()

        if not vendedores_sem_usuario:
            print("✓ Todos os vendedores já possuem usuários!")
            return

        print("CRIANDO USUÁRIOS...")
        print("-" * 60)

        usuarios_criados = []

        for vendedor in vendedores_sem_usuario:
            # Verificar se já existe um usuário com este email
            usuario_email = Usuario.query.filter_by(email=vendedor.email).first()

            if usuario_email:
                print(f"⚠ Email {vendedor.email} já em uso. Pulando {vendedor.nome}...")
                continue

            # Gerar senha temporária
            senha_temp = gerar_senha_temporaria()

            # Criar novo usuário
            novo_usuario = Usuario(
                nome=vendedor.nome,
                email=vendedor.email,
                cargo='vendedor',
                empresa_id=vendedor.empresa_id,
                vendedor_id=vendedor.id,
                ativo=True
            )
            novo_usuario.set_senha(senha_temp)

            db.session.add(novo_usuario)

            usuarios_criados.append({
                'nome': vendedor.nome,
                'email': vendedor.email,
                'senha': senha_temp
            })

            print(f"✓ {vendedor.nome} - {vendedor.email}")

        # Salvar todas as alterações
        try:
            db.session.commit()
            print()
            print("=" * 60)
            print(f"✓ {len(usuarios_criados)} USUÁRIOS CRIADOS COM SUCESSO!")
            print("=" * 60)
            print()

            # Exibir credenciais
            if usuarios_criados:
                print("CREDENCIAIS DE ACESSO (SENHAS TEMPORÁRIAS):")
                print("-" * 60)
                for usuario in usuarios_criados:
                    print(f"Nome:  {usuario['nome']}")
                    print(f"Email: {usuario['email']}")
                    print(f"Senha: {usuario['senha']}")
                    print("-" * 60)

                print()
                print("⚠ IMPORTANTE:")
                print("1. Anote estas senhas temporárias")
                print("2. Informe cada vendedor de suas credenciais")
                print("3. Oriente-os a trocar a senha no primeiro acesso")
                print()

                # Salvar em arquivo
                with open('credenciais_vendedores.txt', 'w', encoding='utf-8') as f:
                    f.write("CREDENCIAIS DE ACESSO - VENDEDORES\n")
                    f.write("=" * 60 + "\n\n")
                    for usuario in usuarios_criados:
                        f.write(f"Nome:  {usuario['nome']}\n")
                        f.write(f"Email: {usuario['email']}\n")
                        f.write(f"Senha: {usuario['senha']}\n")
                        f.write("-" * 60 + "\n\n")

                print("✓ Credenciais salvas em: credenciais_vendedores.txt")
                print()

        except Exception as e:
            db.session.rollback()
            print()
            print("=" * 60)
            print("✗ ERRO AO CRIAR USUÁRIOS!")
            print("=" * 60)
            print(f"Erro: {str(e)}")
            print()
            return False

        return True

if __name__ == '__main__':
    print()
    print("Este script irá criar usuários para todos os vendedores")
    print("que ainda não possuem acesso ao sistema.")
    print()

    resposta = input("Deseja continuar? (s/n): ").strip().lower()

    if resposta == 's':
        criar_usuarios_vendedores()
    else:
        print("Operação cancelada.")
