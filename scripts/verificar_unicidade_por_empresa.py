#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste rápido das constraints de unicidade por empresa para clientes.
- Não persiste dados (usa transações e rollback)
- Verifica duplicidade dentro da mesma empresa e permissão entre empresas
"""

import os, sys, random
from datetime import datetime, timezone

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Permite sobrescrever o DATABASE_URL via CLI: --database-url=postgres://...
for arg in sys.argv[1:]:
    if arg.startswith('--database-url='):
        os.environ['DATABASE_URL'] = arg.split('=', 1)[1]
        break

from app import app, db
from models import Cliente, Empresa
from sqlalchemy.exc import IntegrityError


def gen_code():
    return f"{random.randint(1000, 9999)}-{random.randint(1, 9999):04d}"


def main():
    with app.app_context():
        print("\n" + "="*70)
        print("🔍 TESTE: Unicidade por empresa (clientes)")
        print("="*70 + "\n")
        
        empresas = db.session.query(Empresa.id).order_by(Empresa.id).all()
        if not empresas:
            print("❌ Nenhuma empresa encontrada no banco.")
            return
        
        emp_a = empresas[0][0]
        emp_b = empresas[1][0] if len(empresas) > 1 else None
        
        cpf_teste = f"9{random.randint(1000000000, 9999999999)}"[:11]
        codigo1 = gen_code()
        codigo2 = gen_code()
        
        print(f"Empresa A: {emp_a} | Empresa B: {emp_b if emp_b else 'N/A'}")
        print(f"CPF de teste: {cpf_teste}")
        print("\n-- Dentro da mesma empresa (A) --")
        
        trans = db.session.begin_nested()
        try:
            c1 = Cliente(
                nome="Teste A1",
                cpf=cpf_teste,
                codigo_cliente=codigo1,
                empresa_id=emp_a,
                ativo=True,
                data_cadastro=datetime.now(timezone.utc),
                data_atualizacao=datetime.now(timezone.utc),
            )
            db.session.add(c1)
            db.session.flush()
            print("✓ Primeiro insert (A) OK")
            
            c2 = Cliente(
                nome="Teste A2",
                cpf=cpf_teste,
                codigo_cliente=codigo2,
                empresa_id=emp_a,
                ativo=True,
                data_cadastro=datetime.now(timezone.utc),
                data_atualizacao=datetime.now(timezone.utc),
            )
            db.session.add(c2)
            db.session.flush()
            print("❌ ERA ESPERADO FALHAR DUPLICIDADE de CPF em A")
        except IntegrityError as e:
            print(f"✓ Bloqueio por unicidade dentro da mesma empresa funcionou: {str(e)[:120]}")
        finally:
            trans.rollback()
        
        print("\n-- Entre empresas distintas (A vs B) --")
        if emp_b:
            trans2 = db.session.begin_nested()
            try:
                c3 = Cliente(
                    nome="Teste B",
                    cpf=cpf_teste,
                    codigo_cliente=gen_code(),
                    empresa_id=emp_b,
                    ativo=True,
                    data_cadastro=datetime.now(timezone.utc),
                    data_atualizacao=datetime.now(timezone.utc),
                )
                db.session.add(c3)
                db.session.flush()
                print("✓ Mesmo CPF permitido em empresa distinta (B)")
            except IntegrityError as e:
                print(f"❌ Não deveria bloquear entre empresas distintas: {str(e)[:120]}")
            finally:
                trans2.rollback()
        else:
            print("⚠️ Apenas uma empresa encontrada; teste entre empresas não realizado.")
        
        print("\n" + "="*70)
        print("✅ TESTE CONCLUÍDO")
        print("="*70 + "\n")


if __name__ == '__main__':
    main()
