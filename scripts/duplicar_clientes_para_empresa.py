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

# Evita imports pesados do app (ex.: PDF/reportlab) durante scripts de manutenção
os.environ.setdefault("INIT_DB_ONLY", "1")


def _auto_ajustar_sqlite_local():
    """Garante que scripts de manutenção usem o mesmo SQLite local do projeto.

    Problema comum:
    - `DATABASE_URL=sqlite:///vendacerta.db` aponta para um arquivo inexistente na raiz,
      enquanto o banco real usado no desenvolvimento está em `instance/vendacerta.db`.

    Este ajuste só ocorre quando:
    - DATABASE_URL aponta para SQLite
    - o arquivo alvo não existe
    - existe `instance/vendacerta.db`
    """
    db_url = os.environ.get("DATABASE_URL") or os.environ.get("URL_DO_BANCO_DE_DADOS")
    if not db_url:
        return
    if not db_url.startswith("sqlite:///"):
        return

    # Caminho relativo (sqlite:///arquivo.db) resolve no CWD do processo
    rel_path = db_url.replace("sqlite:///", "", 1)
    cwd_target = os.path.abspath(os.path.join(os.getcwd(), rel_path))
    instance_target = os.path.abspath(os.path.join(ROOT_DIR, "instance", "vendacerta.db"))

    if not os.path.exists(cwd_target) and os.path.exists(instance_target):
        # Força caminho absoluto para evitar dependência do CWD
        instance_uri = "sqlite:///" + instance_target.replace("\\", "/")
        os.environ["DATABASE_URL"] = instance_uri


_auto_ajustar_sqlite_local()

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Imports que dependem do contexto do app/banco serão carregados sob demanda
app = None
db = None
Cliente = None
Empresa = None
Vendedor = None
Usuario = None
and_ = None
or_ = None
IntegrityError = None


def _carregar_contexto_app():
    """Importa app/db/models após variáveis de ambiente estarem definidas."""
    global app, db, Cliente, Empresa, Vendedor, Usuario, and_, or_, IntegrityError

    # Evita que o import do app dispare init do banco (sync/background),
    # o que pode interferir com transações e causar efeitos colaterais
    # (ex.: reset de senha admin) durante scripts.
    os.environ.setdefault("SKIP_DB_INIT_ON_START", "1")

    from app import app as flask_app, db as flask_db
    from models import Cliente as MCliente, Empresa as MEmpresa, Vendedor as MVendedor, Usuario as MUsuario
    from sqlalchemy import and_ as sand_, or_ as sor_
    from sqlalchemy.exc import IntegrityError as SIntegrityError

    app = flask_app
    db = flask_db
    Cliente = MCliente
    Empresa = MEmpresa
    Vendedor = MVendedor
    Usuario = MUsuario
    and_ = sand_
    or_ = sor_
    IntegrityError = SIntegrityError


def encontrar_empresa_alvo(nome_alvo: str) -> Empresa:
    empresa = Empresa.query.filter(Empresa.nome == nome_alvo).first()
    return empresa


def mapear_vendedor_para_empresa_alvo(orig_vendedor_id, empresa_alvo_id):
    """Tenta mapear vendedor pelo e-mail para a empresa alvo.
    Se não encontrar, retorna None (deixa sem vendedor).
    """
    if not orig_vendedor_id:
        return None
    origem = db.session.get(Vendedor, orig_vendedor_id)
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
    origem = db.session.get(Usuario, orig_supervisor_id)
    if not origem or not origem.email:
        return None
    alvo = Usuario.query.filter(
        Usuario.email == origem.email,
        Usuario.empresa_id == empresa_alvo_id
    ).first()
    return alvo.id if alvo else None


def cliente_existe_na_empresa_alvo(empresa_id, cliente_origem: Cliente) -> bool:
    """Tenta identificar se o cliente já existe na empresa alvo.

    Ordem de checagem:
    1) CPF/CNPJ (quando existir)
    2) codigo_bp (quando existir)
    3) email (quando existir)
    4) nome + (celular/telefone) (quando existir)

    Objetivo: tornar o script idempotente também para clientes sem CPF/CNPJ.
    """
    filtros_base = [Cliente.empresa_id == empresa_id]

    # 1) CPF/CNPJ
    doc_filters = []
    if getattr(cliente_origem, 'cpf', None):
        doc_filters.append(Cliente.cpf == cliente_origem.cpf)
    if getattr(cliente_origem, 'cnpj', None):
        doc_filters.append(Cliente.cnpj == cliente_origem.cnpj)
    if doc_filters:
        return db.session.query(Cliente.id).filter(and_(*filtros_base, or_(*doc_filters))).first() is not None

    # 2) código BP
    if getattr(cliente_origem, 'codigo_bp', None):
        return db.session.query(Cliente.id).filter(and_(*filtros_base, Cliente.codigo_bp == cliente_origem.codigo_bp)).first() is not None

    # 3) e-mail
    if getattr(cliente_origem, 'email', None):
        return db.session.query(Cliente.id).filter(and_(*filtros_base, Cliente.email == cliente_origem.email)).first() is not None

    # 4) nome + (celular/telefone)
    nome = getattr(cliente_origem, 'nome', None)
    celular = getattr(cliente_origem, 'celular', None)
    telefone = getattr(cliente_origem, 'telefone', None)
    if nome and (celular or telefone):
        contato_filters = []
        if celular:
            contato_filters.append(Cliente.celular == celular)
        if telefone:
            contato_filters.append(Cliente.telefone == telefone)
        return db.session.query(Cliente.id).filter(and_(*filtros_base, Cliente.nome == nome, or_(*contato_filters))).first() is not None

    # 5) fallback: apenas nome (último recurso para evitar duplicação em reruns)
    if nome:
        return db.session.query(Cliente.id).filter(and_(*filtros_base, Cliente.nome == nome)).first() is not None

    return False


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

    # Limpa qualquer transação já aberta por consultas anteriores (autobegin)
    # antes de abrir a transação que controlaremos manualmente.
    db.session.rollback()

    # Transação externa para agrupar a operação; por cliente usamos savepoint
    # para permitir erros pontuais sem invalidar toda a execução.
    trans = db.session.begin()
    try:
        for idx, orig in enumerate(clientes_origem, start=1):
            if cliente_existe_na_empresa_alvo(empresa_alvo.id, orig):
                pulados_documento += 1
                if idx % 100 == 0:
                    print(f"- {idx}/{total} processados... (pulados por chave: {pulados_documento})")
                continue

            vend_map = mapear_vendedor_para_empresa_alvo(orig.vendedor_id, empresa_alvo.id)
            sup_map = mapear_supervisor_para_empresa_alvo(orig.supervisor_id, empresa_alvo.id)

            # Feedback pontual
            if idx % 200 == 0:
                print(f"- {idx}/{total} processados... (tentando inserir)")

            if dry_run:
                # Em dry-run, não escreve no banco; só contabiliza o que seria inserido.
                copiar_campos_cliente(orig, empresa_alvo.id, vend_map, sup_map)
                inseridos += 1
                continue

            try:
                with db.session.begin_nested():
                    novo = copiar_campos_cliente(orig, empresa_alvo.id, vend_map, sup_map)
                    db.session.add(novo)
                    db.session.flush()  # valida unicidade/códigos
                inseridos += 1
            except IntegrityError as ie:
                erros += 1
                msg = str(ie).lower()
                if ('unique' in msg) or ('duplicate' in msg):
                    # Conflito inesperado (ex.: código gerado coincidir). Retry 1x com novo código.
                    try:
                        with db.session.begin_nested():
                            novo = copiar_campos_cliente(orig, empresa_alvo.id, vend_map, sup_map)
                            cidade_ref = orig.cidade or orig.municipio or 'SEM_CIDADE'
                            novo.codigo_cliente = Cliente.gerar_codigo_cliente(cidade_ref, empresa_alvo.id)
                            db.session.add(novo)
                            db.session.flush()
                        inseridos += 1
                        erros -= 1
                    except Exception as e2:
                        erros += 1
                        print(f"⚠️  Conflito ao inserir cliente ID={orig.id} ({orig.nome}). Pulando. Motivo: {str(e2)[:120]}")
                else:
                    print(f"⚠️  Erro ao inserir cliente ID={orig.id} ({orig.nome}). Pulando. Motivo: {str(ie)[:120]}")
            except Exception as e:
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
    print(f"  • Pulados por chave (doc/codigo_bp/email/contato): {pulados_documento}")
    print(f"  • Erros:      {erros}")
    print("-"*70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Duplicar clientes para a empresa 'Teste 001'")
    parser.add_argument('--dry-run', action='store_true', help='Simula a operação sem persistir no banco')
    parser.add_argument('--empresa-alvo', default='Teste 001', help='Nome exato da empresa alvo (padrão: Teste 001)')
    parser.add_argument('--database-url', default=None, help='Override do DATABASE_URL para esta execução')
    parser.add_argument('--listar-empresas', action='store_true', help='Lista empresas do banco-alvo e sai')
    args = parser.parse_args()

    # Permite override do banco por argumento (útil para Railway/PostgreSQL)
    if args.database_url:
        os.environ['DATABASE_URL'] = args.database_url

    # Ajuste automático de SQLite local quando aplicável
    _auto_ajustar_sqlite_local()

    # Carregar app e models somente após definir env
    _carregar_contexto_app()

    with app.app_context():
        if args.listar_empresas:
            empresas = Empresa.query.order_by(Empresa.id).all()
            print("\nEmpresas no banco alvo:")
            for e in empresas:
                print(f"- ID={e.id} | {e.nome} | CNPJ={e.cnpj}")
            return

        duplicar_clientes(empresa_nome_alvo=args.empresa_alvo, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
