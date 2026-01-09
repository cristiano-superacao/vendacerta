#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Duplica todos os clientes (incluindo inativos) para a empresa "Teste 001".

Características:
- Usa unicidade por empresa (cpf, cnpj, codigo_cliente) sem conflitar com outras empresas.
- Gera `codigo_cliente` usando `Cliente.gerar_codigo_cliente(cidade, empresa_id)` por cidade/empresa.
- Tenta mapear `vendedor` e `supervisor` por e-mail para a empresa alvo; se não encontrar, deixa `NULL`.
- Ignora (pula) clientes que já existam na empresa alvo por CPF ou CNPJ (idempotente).
- Suporta `--dry-run` para simular sem escrever no banco.

Uso:
    python scripts/duplicar_clientes_para_empresa.py [--dry-run]

Observações:
- O script exige que a empresa alvo com nome exatamente "Teste 001" já exista.
  Caso não exista, ele aborta com instrução para criar a empresa antes.
"""

import os
import sys
import argparse

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app, db
from models import Cliente, Empresa, Vendedor, Usuario
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError


def encontrar_empresa_alvo(nome_alvo: str) -> Empresa:
    empresa = Empresa.query.filter(Empresa.nome == nome_alvo).first()
    return empresa


def mapear_vendedor_para_empresa_alvo(orig_vendedor_id, empresa_alvo_id):
    """Tenta mapear vendedor pelo e-mail para a empresa alvo.
    Se não encontrar, retorna None (deixa sem vendedor).
    """
    if not orig_vendedor_id:
        return None
    origem = Vendedor.query.get(orig_vendedor_id)
    if not origem or not origem.email:
        return None
    # Busca vendedor com mesmo e-mail na empresa alvo
    alvo = Vendedor.query.filter(
        Vendedor.email == origem.email,
        Vendedor.empresa_id == empresa_alvo_id
    ).first()
    return alvo.id if alvo else None


def mapear_supervisor_para_empresa_alvo(orig_supervisor_id, empresa_alvo_id):
    """Tenta mapear supervisor (Usuario) pelo e-mail para a empresa alvo.
    Se não encontrar, retorna None (deixa sem supervisor).
    """
    if not orig_supervisor_id:
        return None
    origem = Usuario.query.get(orig_supervisor_id)
    if not origem or not origem.email:
        return None
    alvo = Usuario.query.filter(
        Usuario.email == origem.email,
        Usuario.empresa_id == empresa_alvo_id
    ).first()
    return alvo.id if alvo else None


def cliente_existe_na_empresa_alvo_por_documento(empresa_id, cpf, cnpj) -> bool:
    filtros = [Cliente.empresa_id == empresa_id]
    doc_filters = []
    if cpf:
        doc_filters.append(Cliente.cpf == cpf)
    if cnpj:
        doc_filters.append(Cliente.cnpj == cnpj)
    if not doc_filters:
        return False
    return db.session.query(Cliente.id).filter(and_(*filtros, or_(*doc_filters))).first() is not None


def copiar_campos_cliente(orig: Cliente, empresa_alvo_id: int, vendedor_id_mapeado, supervisor_id_mapeado) -> Cliente:
    # Determinar cidade de referência para geração de código
    cidade_ref = orig.cidade or orig.municipio or 'SEM_CIDADE'
    codigo_novo = Cliente.gerar_codigo_cliente(cidade_ref, empresa_alvo_id)

    novo = Cliente(
        nome=orig.nome,
        razao_social=orig.razao_social,
        sigla=orig.sigla,
        cpf=orig.cpf,
        cnpj=orig.cnpj,
        inscricao_estadual=orig.inscricao_estadual,
        codigo_bp=orig.codigo_bp,
        codigo_cliente=codigo_novo,
        # Endereço
        logradouro=orig.logradouro,
        municipio=orig.municipio,
        bairro=orig.bairro,
        estado=orig.estado,
        cep=orig.cep,
        cidade=orig.cidade,
        ponto_referencia=orig.ponto_referencia,
        coordenada_x=orig.coordenada_x,
        coordenada_y=orig.coordenada_y,
        longitude=orig.longitude,
        latitude=orig.latitude,
        # Contato
        telefone=orig.telefone,
        telefone2=orig.telefone2,
        celular=orig.celular,
        celular2=orig.celular2,
        email=orig.email,
        # Códigos especiais
        codigo_bw=orig.codigo_bw,
        # Formas de pagamento (texto JSON)
        formas_pagamento=orig.formas_pagamento,
        dia_visita=orig.dia_visita,
        # Relacionamentos
        vendedor_id=vendedor_id_mapeado,
        supervisor_id=supervisor_id_mapeado,
        empresa_id=empresa_alvo_id,
        # Status/Observações
        ativo=orig.ativo,
        observacoes=orig.observacoes,
        # Auditoria (preserva data de cadastro)
        data_cadastro=orig.data_cadastro,
    )
    return novo


def duplicar_clientes(empresa_nome_alvo: str = "Teste 001", dry_run: bool = False):
    empresa_alvo = encontrar_empresa_alvo(empresa_nome_alvo)
    if not empresa_alvo:
        print(f"❌ Empresa alvo '{empresa_nome_alvo}' não encontrada.")
        print("   Crie a empresa com este nome antes de rodar a duplicação.")
        return

    print("\n" + "="*70)
    print(f"📦 Duplicação de clientes para a empresa: {empresa_alvo.nome} (ID={empresa_alvo.id})")
    print("="*70 + "\n")

    # Seleciona todos os clientes que NÃO são da empresa alvo (inclui inativos)
    clientes_origem = Cliente.query.filter(
        or_(Cliente.empresa_id.is_(None), Cliente.empresa_id != empresa_alvo.id)
    ).all()

    total = len(clientes_origem)
    inseridos = 0
    pulados_documento = 0
    erros = 0

    print(f"Encontrados {total} clientes de origem para processar.\n")

    # Transação para operação atômica
    trans = db.session.begin_nested()
    try:
        for idx, orig in enumerate(clientes_origem, start=1):
            try:
                if cliente_existe_na_empresa_alvo_por_documento(empresa_alvo.id, orig.cpf, orig.cnpj):
                    pulados_documento += 1
                    if idx % 100 == 0:
                        print(f"- {idx}/{total} processados... (pulados por CPF/CNPJ: {pulados_documento})")
                    continue

                vend_map = mapear_vendedor_para_empresa_alvo(orig.vendedor_id, empresa_alvo.id)
                sup_map = mapear_supervisor_para_empresa_alvo(orig.supervisor_id, empresa_alvo.id)

                novo = copiar_campos_cliente(orig, empresa_alvo.id, vend_map, sup_map)
                db.session.add(novo)

                # Feedback pontual
                if idx % 200 == 0:
                    print(f"- {idx}/{total} processados... (tentando inserir)")

                if not dry_run:
                    db.session.flush()  # valida unicidade/códigos
                inseridos += 1

            except IntegrityError as ie:
                db.session.rollback()  # rollback parcial e segue
                erros += 1
                msg = str(ie).lower()
                if ('unique' in msg) or ('duplicate' in msg):
                    # Algum conflito inesperado (ex.: código gerado coincidir)
                    # Tenta gerar novo código e inserir novamente uma vez
                    try:
                        vend_map = mapear_vendedor_para_empresa_alvo(orig.vendedor_id, empresa_alvo.id)
                        sup_map = mapear_supervisor_para_empresa_alvo(orig.supervisor_id, empresa_alvo.id)
                        novo = copiar_campos_cliente(orig, empresa_alvo.id, vend_map, sup_map)
                        # Força novo código
                        cidade_ref = orig.cidade or orig.municipio or 'SEM_CIDADE'
                        novo.codigo_cliente = Cliente.gerar_codigo_cliente(cidade_ref, empresa_alvo.id)
                        db.session.add(novo)
                        if not dry_run:
                            db.session.flush()
                        inseridos += 1
                        erros -= 1  # compensar sucesso na segunda tentativa
                    except Exception as e2:
                        db.session.rollback()
                        erros += 1
                        print(f"⚠️  Conflito ao inserir cliente ID={orig.id} ({orig.nome}). Pulando. Motivo: {str(e2)[:120]}")
                else:
                    print(f"⚠️  Erro ao inserir cliente ID={orig.id} ({orig.nome}). Pulando. Motivo: {str(ie)[:120]}")
            except Exception as e:
                db.session.rollback()
                erros += 1
                print(f"⚠️  Erro inesperado com cliente ID={orig.id} ({orig.nome}). Pulando. Motivo: {str(e)[:120]}")

        if dry_run:
            trans.rollback()
            print("\n[DRY-RUN] Nenhuma alteração foi persistida.")
        else:
            trans.commit()
            print("\n✅ Dados persistidos com sucesso.")

    finally:
        pass

    print("\n" + "-"*70)
    print("Resumo da operação:")
    print(f"  • Processados: {total}")
    print(f"  • Inseridos:  {inseridos}")
    print(f"  • Pulados por documento (CPF/CNPJ): {pulados_documento}")
    print(f"  • Erros:      {erros}")
    print("-"*70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Duplicar clientes para a empresa 'Teste 001'")
    parser.add_argument('--dry-run', action='store_true', help='Simula a operação sem persistir no banco')
    args = parser.parse_args()

    with app.app_context():
        duplicar_clientes(empresa_nome_alvo="Teste 001", dry_run=args.dry_run)


if __name__ == '__main__':
    main()
