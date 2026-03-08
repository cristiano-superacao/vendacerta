# -*- coding: utf-8 -*-
"""Teste focado: validação de CPF/CNPJ por empresa no ClienteForm.

Objetivo:
- Mesmo CPF deve ser permitido em empresas diferentes.
- CPF duplicado dentro da mesma empresa deve ser bloqueado pelo formulário.

Este teste usa FLASK_ENV=testing (SQLite em memória + CSRF desabilitado).
"""

import os
import sys

# Precisa vir ANTES de importar o app
os.environ.setdefault("FLASK_ENV", "testing")

# Garantir import a partir da raiz do projeto
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, db  # noqa: E402
from forms import ClienteForm  # noqa: E402
from models import Cliente, Empresa, Vendedor  # noqa: E402


def _digits_only(value: str) -> str:
    return "".join(ch for ch in value if ch.isdigit())


def main() -> int:
    with app.app_context():
        db.drop_all()
        db.create_all()

        empresa_a = Empresa(
            nome="Empresa A",
            cnpj="11111111000111",
            email="a@empresa.teste",
            telefone="",
        )
        empresa_b = Empresa(
            nome="Empresa B",
            cnpj="22222222000122",
            email="b@empresa.teste",
            telefone="",
        )
        db.session.add_all([empresa_a, empresa_b])
        db.session.commit()

        vendedor_a = Vendedor(
            nome="Vendedor A",
            email="vend_a@empresa.teste",
            empresa_id=empresa_a.id,
            ativo=True,
        )
        vendedor_b = Vendedor(
            nome="Vendedor B",
            email="vend_b@empresa.teste",
            empresa_id=empresa_b.id,
            ativo=True,
        )
        db.session.add_all([vendedor_a, vendedor_b])
        db.session.commit()

        cpf_teste = "123.456.789-09"  # formato com máscara (form valida removendo não-numéricos)
        cpf_numbers = _digits_only(cpf_teste)

        # Cliente existente na Empresa A
        cliente_a = Cliente(
            nome="Cliente Existente A",
            cpf=cpf_numbers,
            codigo_cliente="0001-0001",
            empresa_id=empresa_a.id,
            vendedor_id=vendedor_a.id,
            ativo=True,
        )
        db.session.add(cliente_a)
        db.session.commit()

        # 1) Duplicado na mesma empresa deve falhar
        with app.test_request_context(
            "/clientes/novo",
            method="POST",
            data={
                "vendedor_id": str(vendedor_a.id),
                "nome": "Cliente Novo A",
                "cpf": cpf_teste,
                "cnpj": "",
            },
        ):
            form_a = ClienteForm(empresa_id=empresa_a.id)
            ok_a = form_a.validate()
            if ok_a:
                print("❌ ERA ESPERADO FALHAR: CPF duplicado na mesma empresa passou no formulário")
                return 1
            if not any("cpf" in k for k in form_a.errors.keys()):
                print(f"❌ Falhou, mas sem erro no campo CPF: {form_a.errors}")
                return 1
            print("✅ Form bloqueou CPF duplicado na mesma empresa (A)")

        # 2) Mesmo CPF em empresa diferente deve passar
        with app.test_request_context(
            "/clientes/novo",
            method="POST",
            data={
                "vendedor_id": str(vendedor_b.id),
                "nome": "Cliente Novo B",
                "cpf": cpf_teste,
                "cnpj": "",
            },
        ):
            form_b = ClienteForm(empresa_id=empresa_b.id)
            ok_b = form_b.validate()
            if not ok_b:
                print(f"❌ NÃO ERA PRA FALHAR: mesmo CPF em outra empresa foi bloqueado: {form_b.errors}")
                return 1
            print("✅ Form permitiu mesmo CPF em empresa diferente (B)")

        print("\n✅ TESTE OK: validação de documento é por empresa")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
