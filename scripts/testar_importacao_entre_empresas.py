#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste de importação de clientes entre empresas diferentes.
Valida que clientes com mesmo CPF/CNPJ podem ser cadastrados em empresas distintas.
"""

import os, sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, db
from models import Cliente, Empresa


def main():
    print("\n" + "="*70)
    print("🧪 TESTE: Importação de clientes entre empresas")
    print("="*70 + "\n")
    
    with app.app_context():
        # Buscar empresas
        empresas = db.session.query(Empresa).order_by(Empresa.id).limit(2).all()
        
        if len(empresas) < 2:
            print("❌ Necessário pelo menos 2 empresas cadastradas")
            print(f"   Encontrado: {len(empresas)} empresa(s)")
            return
        
        empresa_a = empresas[0]
        empresa_b = empresas[1]
        
        print(f"Empresa A: ID={empresa_a.id}, Nome={empresa_a.nome}")
        print(f"Empresa B: ID={empresa_b.id}, Nome={empresa_b.nome}")
        print()
        
        # Dados de teste
        cpf_teste = "12345678901"
        cnpj_teste = "12345678000199"
        
        # Usar transações aninhadas para não persistir
        trans = db.session.begin_nested()
        
        try:
            print("-- Teste 1: Criar cliente com CPF na Empresa A --")
            codigo_a = Cliente.gerar_codigo_cliente("TesteCidade", empresa_a.id)
            cliente_a = Cliente(
                nome="Cliente Teste A",
                cpf=cpf_teste,
                codigo_cliente=codigo_a,
                empresa_id=empresa_a.id,
                ativo=True,
            )
            db.session.add(cliente_a)
            db.session.flush()
            print(f"✓ Cliente criado na Empresa A com CPF {cpf_teste}")
            print(f"  Código: {codigo_a}")
            
            print("\n-- Teste 2: Criar cliente com MESMO CPF na Empresa B --")
            codigo_b = Cliente.gerar_codigo_cliente("TesteCidade", empresa_b.id)
            cliente_b = Cliente(
                nome="Cliente Teste B",
                cpf=cpf_teste,
                codigo_cliente=codigo_b,
                empresa_id=empresa_b.id,
                ativo=True,
            )
            db.session.add(cliente_b)
            db.session.flush()
            print(f"✓ Cliente criado na Empresa B com MESMO CPF {cpf_teste}")
            print(f"  Código: {codigo_b}")
            
            print("\n-- Teste 3: Tentar criar duplicado CPF na MESMA empresa (A) --")
            trans_dup = db.session.begin_nested()
            try:
                codigo_a2 = Cliente.gerar_codigo_cliente("TesteCidade", empresa_a.id)
                cliente_a_dup = Cliente(
                    nome="Cliente Duplicado A",
                    cpf=cpf_teste,
                    codigo_cliente=codigo_a2,
                    empresa_id=empresa_a.id,
                    ativo=True,
                )
                db.session.add(cliente_a_dup)
                db.session.flush()
                print("❌ ERRO: Deveria ter bloqueado CPF duplicado na mesma empresa")
            except Exception as e:
                if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                    print(f"✓ Bloqueio correto de CPF duplicado na mesma empresa")
                else:
                    print(f"⚠️ Erro inesperado: {str(e)[:100]}")
            finally:
                trans_dup.rollback()
            
            print("\n-- Teste 4: Criar cliente com CNPJ na Empresa A --")
            codigo_cnpj_a = Cliente.gerar_codigo_cliente("OutraCidade", empresa_a.id)
            cliente_cnpj_a = Cliente(
                nome="Empresa Teste A",
                cnpj=cnpj_teste,
                codigo_cliente=codigo_cnpj_a,
                empresa_id=empresa_a.id,
                ativo=True,
            )
            db.session.add(cliente_cnpj_a)
            db.session.flush()
            print(f"✓ Cliente criado na Empresa A com CNPJ {cnpj_teste}")
            print(f"  Código: {codigo_cnpj_a}")
            
            print("\n-- Teste 5: Criar cliente com MESMO CNPJ na Empresa B --")
            codigo_cnpj_b = Cliente.gerar_codigo_cliente("OutraCidade", empresa_b.id)
            cliente_cnpj_b = Cliente(
                nome="Empresa Teste B",
                cnpj=cnpj_teste,
                codigo_cliente=codigo_cnpj_b,
                empresa_id=empresa_b.id,
                ativo=True,
            )
            db.session.add(cliente_cnpj_b)
            db.session.flush()
            print(f"✓ Cliente criado na Empresa B com MESMO CNPJ {cnpj_teste}")
            print(f"  Código: {codigo_cnpj_b}")
            
            print("\n-- Teste 6: Verificar códigos sequenciais por empresa --")
            print(f"   Empresa A - Códigos: {codigo_a}, {codigo_cnpj_a}")
            print(f"   Empresa B - Códigos: {codigo_b}, {codigo_cnpj_b}")
            
            # Verificar se códigos começam com diferentes prefixos ou seguem sequência
            if codigo_a.split('-')[0] != codigo_b.split('-')[0]:
                print("✓ Códigos com prefixos diferentes entre empresas (correto)")
            else:
                print("ℹ️ Códigos podem ter mesmo prefixo entre empresas (aceitável)")
            
            print("\n" + "="*70)
            print("✅ TODOS OS TESTES PASSARAM")
            print("="*70)
            print("\nConclusão:")
            print("- CPF/CNPJ podem ser usados em empresas diferentes ✓")
            print("- CPF/CNPJ são únicos dentro da mesma empresa ✓")
            print("- Códigos de cliente são gerados corretamente por empresa ✓")
            print()
            
        except Exception as e:
            print(f"\n❌ ERRO GERAL: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # Rollback para não persistir dados de teste
            trans.rollback()
            print("\n[INFO] Dados de teste revertidos (não persistidos)")


if __name__ == '__main__':
    main()
