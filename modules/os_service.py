"""
Módulo de serviços para Ordens de Serviço (OS)
Encapsula regras de negócio e operações de criação/consulta
para reduzir acoplamento com rotas em app.py.
"""
from datetime import datetime
from typing import List, Tuple

from flask import flash

from models import db, OrdemServico, Cliente, Tecnico


def listar_clientes_empresa(empresa_id: int) -> List[Cliente]:
    return (
        Cliente.query.filter_by(empresa_id=empresa_id)
        .order_by(Cliente.nome)
        .all()
    )


def listar_tecnicos_ativos(empresa_id: int) -> List[Tecnico]:
    return Tecnico.query.filter_by(empresa_id=empresa_id, ativo=True).all()


def gerar_numero_os(empresa_id: int) -> str:
    """Delegação para o método do modelo com proteção futura."""
    return OrdemServico.gerar_numero_os(empresa_id)


def criar_os(form, current_user) -> Tuple[bool, OrdemServico | None, str | None]:
    """
    Cria uma nova OS a partir do formulário.

    Returns:
        (ok, os_obj, erro)
    """
    try:
        numero_os = gerar_numero_os(current_user.empresa_id)
        os_obj = OrdemServico(
            numero_os=numero_os,
            cliente_id=form.cliente_id.data,
            titulo=form.titulo.data,
            descricao_problema=form.descricao_problema.data,
            prioridade=form.prioridade.data,
            status="aguardando_aprovacao",
            data_abertura=datetime.now(),
            criada_por_id=current_user.id,
            empresa_id=current_user.empresa_id,
        )
        db.session.add(os_obj)
        db.session.commit()
        flash(
            f"Ordem de Serviço {numero_os} criada com sucesso! Aguardando aprovação do supervisor.",
            "success",
        )
        return True, os_obj, None
    except Exception as e:
        db.session.rollback()
        return False, None, str(e)


def aprovar_ou_reprovar_os(form, os_obj: OrdemServico, current_user) -> Tuple[bool, str | None]:
    """
    Processa aprovação ou reprovação de uma OS com base no formulário.

    Retorna (ok, erro). Em caso de sucesso, mensagens são exibidas via flash.
    """
    try:
        if getattr(form, "aprovar", None) and form.aprovar.data:
            if not form.tecnico_id.data:
                return False, "Selecione um técnico para aprovar a ordem de serviço."

            os_obj.status = "aprovada"
            os_obj.tecnico_id = form.tecnico_id.data
            os_obj.data_aprovacao = datetime.now()
            os_obj.aprovada_por_id = current_user.id
            os_obj.motivo_reprovacao = None

            # Atualizar contador do técnico
            tecnico = Tecnico.query.get(form.tecnico_id.data)
            if tecnico:
                tecnico.total_os = (tecnico.total_os or 0) + 1

            flash(
                f"Ordem de Serviço {os_obj.numero_os} aprovada! Técnico {tecnico.nome if tecnico else ''} foi notificado.",
                "success",
            )
        else:
            if not form.motivo_reprovacao.data:
                return False, "Informe o motivo da reprovação."

            os_obj.status = "cancelada"
            os_obj.motivo_reprovacao = form.motivo_reprovacao.data
            os_obj.aprovada_por_id = current_user.id

            flash(
                f"⚠️ Ordem de Serviço {os_obj.numero_os} foi reprovada.",
                "warning",
            )

        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def atualizar_os(form, os_obj: OrdemServico, current_user) -> Tuple[bool, str | None]:
    """
    Atualiza campos de andamento da OS conforme o formulário enviado.

    Retorna (ok, erro). Em caso de sucesso, mensagens são exibidas via flash.
    """
    try:
        status_anterior = os_obj.status
        os_obj.status = form.status.data

        # Início de andamento
        if status_anterior != "em_andamento" and form.status.data == "em_andamento":
            os_obj.data_inicio = datetime.now()

        # Conclusão
        if form.status.data == "concluida":
            os_obj.data_conclusao = datetime.now()
            os_obj.descricao_solucao = form.descricao_solucao.data
            os_obj.valor_mao_obra = form.valor_mao_obra.data or 0
            os_obj.valor_pecas = form.valor_pecas.data or 0
            os_obj.valor_total = (os_obj.valor_mao_obra or 0) + (os_obj.valor_pecas or 0)

            if os_obj.tecnico:
                os_obj.tecnico.os_concluidas = (os_obj.tecnico.os_concluidas or 0) + 1

        # Previsão de conclusão
        if form.data_previsao.data:
            os_obj.data_previsao = form.data_previsao.data

        # Feedback do técnico
        if form.feedback_tecnico.data:
            os_obj.feedback_tecnico = form.feedback_tecnico.data

        db.session.commit()
        flash(
            f"Ordem de Serviço {os_obj.numero_os} atualizada com sucesso!",
            "success",
        )
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def avaliar_os(form, os_obj: OrdemServico, current_user) -> Tuple[bool, str | None]:
    """
    Registra avaliação do cliente para a OS e recalcula média do técnico.

    Retorna (ok, erro). Em caso de sucesso, mensagens são exibidas via flash.
    """
    try:
        os_obj.avaliacao_cliente = form.avaliacao_cliente.data

        # Atualizar média do técnico
        if os_obj.tecnico:
            avaliacoes = (
                OrdemServico.query.filter_by(tecnico_id=os_obj.tecnico_id)
                .filter(OrdemServico.avaliacao_cliente.isnot(None))
                .all()
            )
            if avaliacoes:
                soma = sum(av.avaliacao_cliente for av in avaliacoes)
                os_obj.tecnico.avaliacao_media = soma / len(avaliacoes)

        db.session.commit()
        flash(
            "Obrigado pela avaliação! Sua opinião é muito importante.",
            "success",
        )
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)
