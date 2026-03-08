#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para criar vendedor de teste para o módulo de clientes
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Usuario, Vendedor, Empresa

def criar_vendedor_teste():
    """Cria um vendedor de teste"""
    with app.app_context():
        try:
            print("=" * 70)
            print("CRIANDO VENDEDOR DE TESTE")
            print("=" * 70)
            
            # Buscar ou criar empresa
            empresa = Empresa.query.first()
            
            if not empresa:
                print("\n[1/3] Criando empresa de teste...")
                empresa = Empresa(
                    nome="Empresa Teste",
                    cnpj="12345678000190",
                    email="empresa@teste.com",
                    plano="basico",
                    ativo=True
                )
                db.session.add(empresa)
                db.session.commit()
                print(f"  ✓ Empresa '{empresa.nome}' criada")
            else:
                print(f"\n[1/3] Usando empresa existente: {empresa.nome}")
            
            # Criar vendedor
            print("\n[2/3] Criando vendedor...")
            
            # Verificar se já existe
            vendedor_existente = Vendedor.query.filter_by(email="vendedor.teste@suameta.com").first()
            
            if vendedor_existente:
                vendedor = vendedor_existente
                print(f"  ⚠ Vendedor já existe: {vendedor.nome}")
            else:
                vendedor = Vendedor(
                    nome="João Vendedor",
                    email="vendedor.teste@suameta.com",
                    telefone="(71) 98765-4321",
                    cpf="12345678900",
                    empresa_id=empresa.id,
                    ativo=True
                )
                db.session.add(vendedor)
                db.session.commit()
                print(f"  ✓ Vendedor '{vendedor.nome}' criado")
            
            # Criar usuário para login
            print("\n[3/3] Criando login para vendedor...")
            
            usuario_existente = Usuario.query.filter_by(email="vendedor.teste@suameta.com").first()
            
            if usuario_existente:
                print(f"  ⚠ Login já existe para: {usuario_existente.nome}")
                usuario = usuario_existente
                # Resetar senha
                usuario.set_senha("vendedor123")
                db.session.commit()
                print(f"  ✓ Senha resetada")
            else:
                usuario = Usuario(
                    nome="João Vendedor",
                    email="vendedor.teste@suameta.com",
                    cargo="vendedor",
                    empresa_id=empresa.id,
                    vendedor_id=vendedor.id,
                    ativo=True,
                    bloqueado=False,
                    pode_enviar_mensagens=True,
                    pode_ver_dashboard=True
                )
                usuario.set_senha("vendedor123")
                db.session.add(usuario)
                db.session.commit()
                print(f"  ✓ Login criado para '{usuario.nome}'")
            
            print("\n" + "=" * 70)
            print("✅ VENDEDOR DE TESTE CRIADO COM SUCESSO!")
            print("=" * 70)
            print("\n🔑 CREDENCIAIS PARA TESTAR MÓDULO DE CLIENTES:")
            print("-" * 70)
            print(f"Email (Login): vendedor.teste@suameta.com")
            print(f"Senha: vendedor123")
            print(f"Cargo: Vendedor")
            print(f"Empresa: {empresa.nome}")
            print("-" * 70)
            print("\n✨ Use estas credenciais para:")
            print("  1. Fazer login no sistema")
            print("  2. Acessar menu 'Clientes'")
            print("  3. Cadastrar e gerenciar clientes")
            print("  4. Registrar compras")
            print("  5. Ver relatórios")
            print("\n" + "=" * 70)
            
        except Exception as e:
            print(f"\n✗ Erro: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    criar_vendedor_teste()
