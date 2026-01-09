#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para duplicar produtos entre empresas no sistema multi-empresa.

Funcionalidades:
- Duplica todos os produtos (ativos/inativos) de outras empresas para a empresa alvo
- Gera códigos únicos automaticamente para cada produto na empresa alvo
- Detecta duplicatas por múltiplas chaves (código_barra, referencia, nome)
- Idempotente: execuções múltiplas não duplicam produtos
- Transações seguras com savepoint individual por produto
- Suporta dry-run para simulação sem persistir dados

Uso:
    # Simulação (não persiste)
    python scripts/duplicar_produtos_para_empresa.py --dry-run

    # Execução real (empresa padrão: "Teste 001")
    python scripts/duplicar_produtos_para_empresa.py

    # Especificar empresa alvo diferente
    python scripts/duplicar_produtos_para_empresa.py --empresa-alvo "Outra Empresa"

    # Listar empresas disponíveis
    python scripts/duplicar_produtos_para_empresa.py --listar-empresas

    # Executar contra banco específico (Railway/Postgres)
    python scripts/duplicar_produtos_para_empresa.py \
        --database-url "postgresql://user:pass@host:port/db"
"""

import os
import sys
import argparse

# Evitar que o import do app dispare inicialização/seed/reset durante scripts
os.environ.setdefault("SKIP_DB_INIT_ON_START", "1")
os.environ.setdefault("INIT_DB_ONLY", "1")

# Garantir que o diretório raiz do projeto está no PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Variáveis globais carregadas tardiamente
app = None
db = None
Produto = None
Empresa = None
and_ = None
or_ = None
IntegrityError = None


def _auto_ajustar_sqlite_local():
    """
    Se DATABASE_URL aponta para SQLite relativo inexistente,
    tenta construir caminho absoluto baseado no workspace.
    """
    db_url = os.environ.get("DATABASE_URL", "")
    if db_url.startswith("sqlite:///") and not db_url.startswith("sqlite:////"):
        # Remove prefixo para obter o path relativo
        rel_path = db_url.replace("sqlite:///", "")
        abs_path = os.path.join(ROOT_DIR, rel_path)
        # Se o arquivo não existe no caminho relativo, tenta usar instance/vendacerta.db
        if not os.path.exists(abs_path):
            instance_path = os.path.join(ROOT_DIR, "instance", "vendacerta.db")
            if os.path.exists(instance_path):
                # Constrói URI absoluto para SQLite
                os.environ["DATABASE_URL"] = f"sqlite:///{instance_path}"
                print(f"[AUTO-AJUSTE] DATABASE_URL ajustada para: sqlite:///{instance_path}")


def _carregar_contexto_app():
    """Importa app/db/models após variáveis de ambiente estarem definidas."""
    global app, db, Produto, Empresa, and_, or_, IntegrityError

    # Evita que o import do app dispare init do banco (sync/background),
    # o que pode interferir com transações e causar efeitos colaterais
    # (ex.: reset de senha admin) durante scripts.
    os.environ.setdefault("SKIP_DB_INIT_ON_START", "1")

    from app import app as flask_app, db as flask_db
    from models import Produto as MProduto, Empresa as MEmpresa
    from sqlalchemy import and_ as sand_, or_ as sor_
    from sqlalchemy.exc import IntegrityError as SIntegrityError

    app = flask_app
    db = flask_db
    Produto = MProduto
    Empresa = MEmpresa
    and_ = sand_
    or_ = sor_
    IntegrityError = SIntegrityError


def encontrar_empresa_alvo(nome_alvo: str):
    """Busca empresa por nome exato."""
    empresa = Empresa.query.filter(Empresa.nome == nome_alvo).first()
    return empresa


def produto_existe_na_empresa_alvo(empresa_id, produto_origem) -> bool:
    """Tenta identificar se o produto já existe na empresa alvo.

    Ordem de checagem:
    1) codigo_barra (quando existir e não for vazio)
    2) referencia (quando existir e não for vazia)
    3) nome (fallback final)

    Objetivo: tornar o script idempotente.
    """
    filtros_base = [Produto.empresa_id == empresa_id]

    # 1) Código de barras
    codigo_barra = getattr(produto_origem, 'codigo_barra', None)
    if codigo_barra and codigo_barra.strip():
        return db.session.query(Produto.id).filter(
            and_(*filtros_base, Produto.codigo_barra == codigo_barra)
        ).first() is not None

    # 2) Referência
    referencia = getattr(produto_origem, 'referencia', None)
    if referencia and referencia.strip():
        return db.session.query(Produto.id).filter(
            and_(*filtros_base, Produto.referencia == referencia)
        ).first() is not None

    # 3) Nome (fallback)
    nome = getattr(produto_origem, 'nome', None)
    if nome:
        return db.session.query(Produto.id).filter(
            and_(*filtros_base, Produto.nome == nome)
        ).first() is not None

    return False


def gerar_codigo_produto_unico(empresa_id: int, codigo_base: str) -> str:
    """Gera código único para produto na empresa alvo.
    
    Estratégia:
    - Tenta usar o código original com sufixo da empresa
    - Se houver colisão, incrementa sufixo numérico
    """
    # Remove prefixos comuns e normaliza
    codigo_limpo = codigo_base.strip().upper()
    
    # Tenta primeiro com sufixo da empresa
    codigo_tentativa = f"{codigo_limpo}-E{empresa_id}"
    
    # Verifica se já existe
    if not db.session.query(Produto.id).filter(
        Produto.codigo == codigo_tentativa,
        Produto.empresa_id == empresa_id
    ).first():
        return codigo_tentativa
    
    # Se existe, incrementa sufixo numérico
    contador = 1
    while True:
        codigo_tentativa = f"{codigo_limpo}-E{empresa_id}-{contador:03d}"
        if not db.session.query(Produto.id).filter(
            Produto.codigo == codigo_tentativa,
            Produto.empresa_id == empresa_id
        ).first():
            return codigo_tentativa
        contador += 1
        if contador > 9999:  # Limite de segurança
            raise ValueError(f"Não foi possível gerar código único para {codigo_base}")


def copiar_campos_produto(orig, empresa_alvo_id: int):
    """Copia todos os campos relevantes do produto origem para novo produto."""
    
    # Gera código único para a empresa alvo
    codigo_novo = gerar_codigo_produto_unico(empresa_alvo_id, orig.codigo)

    novo = Produto(
        # Identificação
        codigo=codigo_novo,
        codigo_barra=orig.codigo_barra,
        referencia=orig.referencia,
        ncm=orig.ncm,
        nome=orig.nome,
        descricao=orig.descricao,
        categoria=orig.categoria,
        fornecedor=orig.fornecedor,
        # Controle de estoque
        unidade=orig.unidade,
        estoque_minimo=orig.estoque_minimo,
        estoque_atual=orig.estoque_atual,
        # Valores
        custo_medio=orig.custo_medio,
        preco_venda=orig.preco_venda,
        preco_servico=orig.preco_servico,
        # Localização
        localizacao=orig.localizacao,
        # Status
        ativo=orig.ativo,
        # Empresa
        empresa_id=empresa_alvo_id,
        # Auditoria (preserva data de cadastro)
        data_cadastro=orig.data_cadastro,
    )
    return novo


def duplicar_produtos(empresa_nome_alvo: str = "Teste 001", dry_run: bool = False):
    """Duplica produtos de outras empresas para a empresa alvo."""
    empresa_alvo = encontrar_empresa_alvo(empresa_nome_alvo)
    if not empresa_alvo:
        print(f"❌ Empresa alvo '{empresa_nome_alvo}' não encontrada.")
        print("   Crie a empresa com este nome antes de rodar a duplicação.")
        return

    print("\n" + "="*70)
    print(f"📦 Duplicação de produtos para a empresa: {empresa_alvo.nome} (ID={empresa_alvo.id})")
    print("="*70 + "\n")

    # Seleciona todos os produtos que NÃO são da empresa alvo (inclui inativos)
    produtos_origem = Produto.query.filter(
        or_(Produto.empresa_id.is_(None), Produto.empresa_id != empresa_alvo.id)
    ).all()

    total = len(produtos_origem)
    inseridos = 0
    pulados_chave = 0
    erros = 0

    print(f"Encontrados {total} produtos de origem para processar.\n")

    # Limpa qualquer transação já aberta por consultas anteriores (autobegin)
    # antes de abrir a transação que controlaremos manualmente.
    db.session.rollback()

    # Transação externa para agrupar a operação; por produto usamos savepoint
    # para permitir erros pontuais sem invalidar toda a execução.
    trans = db.session.begin()
    try:
        for idx, orig in enumerate(produtos_origem, start=1):
            if produto_existe_na_empresa_alvo(empresa_alvo.id, orig):
                pulados_chave += 1
                if idx % 100 == 0:
                    print(f"- {idx}/{total} processados... (pulados por chave: {pulados_chave})")
                continue

            # Feedback pontual
            if idx % 200 == 0:
                print(f"- {idx}/{total} processados... (tentando inserir)")

            if dry_run:
                # Em dry-run, não escreve no banco; só contabiliza o que seria inserido.
                copiar_campos_produto(orig, empresa_alvo.id)
                inseridos += 1
                continue

            try:
                with db.session.begin_nested():
                    novo = copiar_campos_produto(orig, empresa_alvo.id)
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
                            novo = copiar_campos_produto(orig, empresa_alvo.id)
                            # Força novo código com sufixo incremental
                            novo.codigo = gerar_codigo_produto_unico(empresa_alvo.id, f"{orig.codigo}-R")
                            db.session.add(novo)
                            db.session.flush()
                        inseridos += 1
                        erros -= 1
                    except Exception as e2:
                        erros += 1
                        print(f"⚠️  Conflito ao inserir produto ID={orig.id} ({orig.nome}). Pulando. Motivo: {str(e2)[:120]}")
                else:
                    print(f"⚠️  Erro ao inserir produto ID={orig.id} ({orig.nome}). Pulando. Motivo: {str(ie)[:120]}")
            except Exception as e:
                erros += 1
                print(f"⚠️  Erro inesperado com produto ID={orig.id} ({orig.nome}). Pulando. Motivo: {str(e)[:120]}")

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
    print(f"  • Pulados por chave (codigo_barra/referencia/nome): {pulados_chave}")
    print(f"  • Erros:      {erros}")
    print("-"*70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Duplicar produtos para a empresa 'Teste 001'")
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

        duplicar_produtos(empresa_nome_alvo=args.empresa_alvo, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
