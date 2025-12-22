#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para resetar senha de um usuário
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Usuario

def resetar_senha():
    """Reseta a senha de um usuário específico"""
    with app.app_context():
        try:
            print("=" * 70)
            print("RESETAR SENHA DE USUÁRIO")
            print("=" * 70)
            
            # Listar usuários
            usuarios = Usuario.query.all()
            
            if not usuarios:
                print("\n⚠️  Nenhum usuário encontrado.")
                return
            
            print("\nUsuários disponíveis:\n")
            for i, usuario in enumerate(usuarios, 1):
                print(f"{i}. {usuario.nome} ({usuario.email}) - {usuario.cargo}")
            
            print("\n" + "-" * 70)
            
            # Escolher usuário
            escolha = input("\nDigite o número do usuário (ou Enter para cancelar): ").strip()
            
            if not escolha:
                print("Operação cancelada.")
                return
            
            try:
                idx = int(escolha) - 1
                if idx < 0 or idx >= len(usuarios):
                    print("Opção inválida.")
                    return
                
                usuario = usuarios[idx]
            except ValueError:
                print("Opção inválida.")
                return
            
            # Nova senha
            nova_senha = input(f"\nDigite a NOVA SENHA para {usuario.nome}: ").strip()
            
            if not nova_senha:
                print("Senha não pode ser vazia.")
                return
            
            # Confirmar
            confirma = input(f"\nConfirma resetar senha de '{usuario.nome}'? (s/n): ").strip().lower()
            
            if confirma != 's':
                print("Operação cancelada.")
                return
            
            # Resetar senha
            usuario.set_senha(nova_senha)
            db.session.commit()
            
            print("\n" + "=" * 70)
            print("✅ SENHA RESETADA COM SUCESSO!")
            print("=" * 70)
            print(f"\nUsuário: {usuario.nome}")
            print(f"Email: {usuario.email}")
            print(f"Nova Senha: {nova_senha}")
            print("\n⚠️  IMPORTANTE: Anote essa senha em local seguro!")
            print("\n" + "=" * 70)
            
        except Exception as e:
            print(f"\n✗ Erro: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    resetar_senha()
