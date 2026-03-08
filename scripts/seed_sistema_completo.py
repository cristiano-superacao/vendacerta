"""Seed completo e idempotente para ambiente de testes/demonstracao.

Uso:
  python scripts/seed_sistema_completo.py
  python scripts/seed_sistema_completo.py --reset
"""

from __future__ import annotations

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Evita perda de dados entre processos quando o ambiente local usa DB em memoria.
if os.environ.get("DATABASE_URL", "").strip() == "sqlite:///:memory:":
    os.environ["DATABASE_URL"] = "sqlite:///vendacerta_seed.db"

from app import app, db
from models import (
    Empresa,
    Usuario,
    Equipe,
    Vendedor,
    Meta,
    Cliente,
    CompraCliente,
    Produto,
    EstoqueMovimento,
    Tecnico,
    OrdemServico,
    Mensagem,
)


TZ_BR = ZoneInfo("America/Sao_Paulo")


def now_br() -> datetime:
    return datetime.now(TZ_BR).replace(tzinfo=None)


def find_or_create_empresa() -> Empresa:
    empresa = Empresa.query.filter_by(cnpj="12345678000199").first()
    if empresa:
        return empresa

    empresa = Empresa(
        nome="VendaCerta Demo",
        cnpj="12345678000199",
        email="contato@vendacerta.demo",
        telefone="11999990000",
        cidade="Sao Paulo",
        estado="SP",
        ativo=True,
    )
    db.session.add(empresa)
    db.session.flush()
    return empresa


def upsert_usuario(email: str, defaults: dict, senha: str | None = None) -> Usuario:
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        usuario = Usuario(email=email, **defaults)
        usuario.set_senha(senha or "Temp@123")
        db.session.add(usuario)
        db.session.flush()
        return usuario

    for k, v in defaults.items():
        setattr(usuario, k, v)
    if senha:
        usuario.set_senha(senha)
    return usuario


def upsert_vendedor(email: str, defaults: dict) -> Vendedor:
    vendedor = Vendedor.query.filter_by(email=email).first()
    if not vendedor:
        vendedor = Vendedor(email=email, **defaults)
        db.session.add(vendedor)
        db.session.flush()
        return vendedor

    for k, v in defaults.items():
        setattr(vendedor, k, v)
    return vendedor


def upsert_cliente(nome: str, vendedor_id: int, empresa_id: int, codigo: str, dia_visita: str) -> Cliente:
    cliente = Cliente.query.filter_by(empresa_id=empresa_id, codigo_cliente=codigo).first()
    if not cliente:
        cliente = Cliente(
            nome=nome,
            codigo_cliente=codigo,
            cidade="Sao Paulo",
            bairro="Centro",
            telefone="11988887777",
            dia_visita=dia_visita,
            vendedor_id=vendedor_id,
            empresa_id=empresa_id,
            ativo=True,
            data_cadastro=now_br(),
        )
        db.session.add(cliente)
        db.session.flush()
        return cliente

    cliente.nome = nome
    cliente.vendedor_id = vendedor_id
    cliente.empresa_id = empresa_id
    cliente.dia_visita = dia_visita
    cliente.ativo = True
    return cliente


def seed(reset: bool = False) -> None:
    with app.app_context():
        if reset:
            db.drop_all()
            db.create_all()
        else:
            db.create_all()

        empresa = find_or_create_empresa()

        admin = upsert_usuario(
            "admin@vendacerta.demo",
            {
                "nome": "Admin Demo",
                "cargo": "admin",
                "empresa_id": empresa.id,
                "ativo": True,
                "pode_enviar_mensagens": True,
                "pode_acessar_clientes": True,
                "pode_acessar_estoque": True,
            },
            senha="Admin@123",
        )

        supervisor = upsert_usuario(
            "supervisor@vendacerta.demo",
            {
                "nome": "Supervisor Demo",
                "cargo": "supervisor",
                "empresa_id": empresa.id,
                "ativo": True,
                "pode_enviar_mensagens": True,
                "pode_acessar_clientes": True,
            },
            senha="Supervisor@123",
        )

        equipe = Equipe.query.filter_by(nome="Equipe Demo").first()
        if not equipe:
            equipe = Equipe(
                nome="Equipe Demo",
                descricao="Equipe criada por seed",
                empresa_id=empresa.id,
                supervisor_id=supervisor.id,
                ativa=True,
                data_criacao=now_br(),
            )
            db.session.add(equipe)
            db.session.flush()
        else:
            equipe.supervisor_id = supervisor.id
            equipe.empresa_id = empresa.id

        vendedor = upsert_vendedor(
            "vendedor@vendacerta.demo",
            {
                "nome": "Vendedor Demo",
                "telefone": "11977776666",
                "cpf": "12345678901",
                "supervisor_id": supervisor.id,
                "supervisor_nome": supervisor.nome,
                "equipe_id": equipe.id,
                "empresa_id": empresa.id,
                "ativo": True,
            },
        )

        usuario_vendedor = upsert_usuario(
            "vendedor.login@vendacerta.demo",
            {
                "nome": "Login Vendedor Demo",
                "cargo": "vendedor",
                "empresa_id": empresa.id,
                "vendedor_id": vendedor.id,
                "ativo": True,
                "pode_enviar_mensagens": True,
                "pode_acessar_clientes": True,
                "pode_acessar_estoque": True,
            },
            senha="Vendedor@123",
        )

        hoje = now_br()
        meta = Meta.query.filter_by(vendedor_id=vendedor.id, mes=hoje.month, ano=hoje.year).first()
        if not meta:
            meta = Meta(
                vendedor_id=vendedor.id,
                mes=hoje.month,
                ano=hoje.year,
                tipo_meta="valor",
                valor_meta=50000.0,
                receita_alcancada=15000.0,
                status_comissao="Pendente",
            )
            meta.calcular_comissao()
            db.session.add(meta)

        cliente_a = upsert_cliente("Cliente Alpha", vendedor.id, empresa.id, "0001-0001", "segunda")
        cliente_b = upsert_cliente("Cliente Beta", vendedor.id, empresa.id, "0001-0002", "terca")

        compra = CompraCliente.query.filter_by(cliente_id=cliente_a.id, vendedor_id=vendedor.id).first()
        if not compra:
            compra = CompraCliente(
                cliente_id=cliente_a.id,
                vendedor_id=vendedor.id,
                empresa_id=empresa.id,
                valor=850.0,
                forma_pagamento="pix",
                observacoes="Compra seed",
                data_compra=hoje,
                data_registro=hoje,
            )
            db.session.add(compra)
            db.session.flush()

        produto = Produto.query.filter_by(codigo="PROD-DEMO-001").first()
        if not produto:
            produto = Produto(
                codigo="PROD-DEMO-001",
                nome="Produto Demo",
                categoria="Pecas",
                unidade="UN",
                estoque_minimo=3,
                estoque_atual=20,
                preco_venda=120.0,
                preco_servico=150.0,
                empresa_id=empresa.id,
                ativo=True,
                data_cadastro=hoje,
                data_atualizacao=hoje,
            )
            db.session.add(produto)
            db.session.flush()

        movimento = EstoqueMovimento.query.filter_by(documento="SEED-ENTRADA-001").first()
        if not movimento:
            movimento = EstoqueMovimento(
                produto_id=produto.id,
                tipo="entrada",
                motivo="ajuste",
                quantidade=5,
                valor_unitario=100.0,
                valor_total=500.0,
                documento="SEED-ENTRADA-001",
                observacoes="Movimento seed",
                usuario_id=admin.id,
                empresa_id=empresa.id,
                data_movimento=hoje,
            )
            db.session.add(movimento)

        tecnico = Tecnico.query.filter_by(nome="Tecnico Demo", empresa_id=empresa.id).first()
        if not tecnico:
            tecnico = Tecnico(
                nome="Tecnico Demo",
                email="tecnico@vendacerta.demo",
                telefone="11966665555",
                empresa_id=empresa.id,
                supervisor_id=supervisor.id,
                ativo=True,
                disponivel=True,
                data_cadastro=hoje,
                data_atualizacao=hoje,
            )
            db.session.add(tecnico)
            db.session.flush()

        os_numero = OrdemServico.gerar_numero_os(empresa.id)
        ordem = OrdemServico.query.filter_by(numero_os=os_numero).first()
        if not ordem:
            ordem = OrdemServico(
                numero_os=os_numero,
                cliente_id=cliente_a.id,
                tecnico_id=tecnico.id,
                titulo="Manutencao Preventiva",
                descricao_problema="Equipamento com oscilacao",
                prioridade="normal",
                status="aprovada",
                data_abertura=hoje,
                data_aprovacao=hoje,
                criada_por_id=admin.id,
                aprovada_por_id=admin.id,
                empresa_id=empresa.id,
            )
            db.session.add(ordem)

        mensagem = Mensagem.query.filter_by(
            remetente_id=admin.id,
            destinatario_id=usuario_vendedor.id,
            assunto="Boas-vindas ao sistema",
        ).first()
        if not mensagem:
            mensagem = Mensagem(
                remetente_id=admin.id,
                destinatario_id=usuario_vendedor.id,
                assunto="Boas-vindas ao sistema",
                mensagem="Base de testes criada com sucesso.",
                prioridade="normal",
                data_envio=hoje,
                lida=False,
                arquivada_destinatario=False,
                arquivada_remetente=False,
            )
            db.session.add(mensagem)

        db.session.commit()

        print("\n=== SEED COMPLETO FINALIZADO ===")
        print(f"Empresa: {empresa.nome}")
        print("Credenciais:")
        print("- admin@vendacerta.demo / Admin@123")
        print("- supervisor@vendacerta.demo / Supervisor@123")
        print("- vendedor.login@vendacerta.demo / Vendedor@123")
        print(f"Data/Hora (Brasilia): {now_br().strftime('%d/%m/%Y %H:%M:%S')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed completo do sistema")
    parser.add_argument("--reset", action="store_true", help="Recria tabelas antes do seed")
    args = parser.parse_args()
    seed(reset=args.reset)


if __name__ == "__main__":
    main()
