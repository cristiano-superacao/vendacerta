# helpers.py - Funções auxiliares reutilizáveis para evitar duplicação
import re
from flask import flash


_DIA_VISITA_ORDEM = {
    "segunda": 0,
    "terca": 1,
    "quarta": 2,
    "quinta": 3,
    "sexta": 4,
    "sabado": 5,
    "domingo": 6,
}


_DIA_VISITA_LABEL = {
    "segunda": "Segunda-feira",
    "terca": "Terça-feira",
    "quarta": "Quarta-feira",
    "quinta": "Quinta-feira",
    "sexta": "Sexta-feira",
    "sabado": "Sábado",
    "domingo": "Domingo",
}


def normalizar_dia_visita(dia):
    """Normaliza valores de dia_visita para o padrão usado no sistema."""
    if not dia:
        return None

    dia_norm = str(dia).strip().lower()

    aliases = {
        "segunda-feira": "segunda",
        "segunda feira": "segunda",
        "terca-feira": "terca",
        "terça-feira": "terca",
        "terca feira": "terca",
        "terça feira": "terca",
        "quarta-feira": "quarta",
        "quarta feira": "quarta",
        "quinta-feira": "quinta",
        "quinta feira": "quinta",
        "sexta-feira": "sexta",
        "sexta feira": "sexta",
        "sabado": "sabado",
        "sábado": "sabado",
        "domingo": "domingo",
    }

    dia_norm = aliases.get(dia_norm, dia_norm)
    return dia_norm


def listar_dias_visita_validos():
    return set(_DIA_VISITA_ORDEM.keys())


def dia_visita_label(dia):
    dia_norm = normalizar_dia_visita(dia)
    return _DIA_VISITA_LABEL.get(dia_norm, "-")


def dia_visita_sort_key(dia):
    dia_norm = normalizar_dia_visita(dia)
    return _DIA_VISITA_ORDEM.get(dia_norm, 99)


def get_dia_visita_hoje(ref_dt=None):
    """Retorna o dia_visita (segunda..domingo) para a data informada (ou hoje)."""
    from datetime import datetime

    dt = ref_dt or datetime.now()
    weekday = dt.weekday()  # 0=segunda .. 6=domingo
    inv = {v: k for k, v in _DIA_VISITA_ORDEM.items()}
    return inv.get(weekday)


def limpar_cpf(cpf):
    """Remove caracteres não numéricos de CPF"""
    return re.sub(r"\D", "", cpf) if cpf else None


def limpar_cnpj(cnpj):
    """Remove caracteres não numéricos de CNPJ"""
    return re.sub(r"\D", "", cnpj) if cnpj else None


def limpar_telefone(telefone):
    """Remove caracteres não numéricos de telefone"""
    return re.sub(r"\D", "", telefone) if telefone else None


def formatar_cpf(cpf):
    """Formata CPF: 123.456.789-00"""
    if not cpf:
        return ""
    cpf_limpo = limpar_cpf(cpf)
    if len(cpf_limpo) != 11:
        return cpf
    return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"


def formatar_cnpj(cnpj):
    """Formata CNPJ: 12.345.678/0001-00"""
    if not cnpj:
        return ""
    cnpj_limpo = limpar_cnpj(cnpj)
    if len(cnpj_limpo) != 14:
        return cnpj
    return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"


def formatar_telefone(telefone):
    """Formata telefone: (11) 98765-4321"""
    if not telefone:
        return ""
    tel_limpo = limpar_telefone(telefone)
    
    if len(tel_limpo) == 11:  # Celular com DDD
        return f"({tel_limpo[:2]}) {tel_limpo[2:7]}-{tel_limpo[7:]}"
    elif len(tel_limpo) == 10:  # Fixo com DDD
        return f"({tel_limpo[:2]}) {tel_limpo[2:6]}-{tel_limpo[6:]}"
    else:
        return telefone


def flash_sucesso(entidade, acao="criado"):
    """Exibe mensagem de sucesso padronizada"""
    mensagens = {
        "criado": f"{entidade} criado com sucesso!",
        "atualizado": f"{entidade} atualizado com sucesso!",
        "deletado": f"{entidade} deletado com sucesso!",
        "ativado": f"{entidade} ativado com sucesso!",
        "desativado": f"{entidade} desativado com sucesso!",
        "importado": f"{entidade} importado com sucesso!",
        "exportado": f"{entidade} exportado com sucesso!",
        "enviado": f"{entidade} enviado com sucesso!",
    }
    mensagem = mensagens.get(acao, f"{entidade} {acao} com sucesso!")
    flash(mensagem, "success")


def flash_erro(acao, erro):
    """Exibe mensagem de erro padronizada"""
    flash(f"Erro ao {acao}: {str(erro)}", "danger")


def flash_aviso(mensagem):
    """Exibe mensagem de aviso padronizada"""
    flash(mensagem, "warning")


def flash_info(mensagem):
    """Exibe mensagem informativa padronizada"""
    flash(mensagem, "info")


def filtrar_vendedores_por_escopo(current_user, apenas_ativos=True):
    """
    Retorna vendedores de acordo com o escopo do usuário logado
    
    Args:
        current_user: Usuário logado
        apenas_ativos: Se True, retorna apenas vendedores ativos
    
    Returns:
        Query de vendedores filtrada
    """
    from models import Vendedor
    
    query = Vendedor.query
    
    if apenas_ativos:
        query = query.filter_by(ativo=True)
    
    if current_user.is_super_admin:
        # Super admin vê todos
        return query.all()
    elif current_user.cargo == "supervisor":
        # Supervisor vê apenas seus vendedores
        return query.filter_by(supervisor_id=current_user.id).all()
    else:
        # Admin da empresa vê vendedores da sua empresa
        return query.filter_by(empresa_id=current_user.empresa_id).all()


def filtrar_clientes_por_escopo(current_user, apenas_ativos=True):
    """
    Retorna clientes de acordo com o escopo do usuário logado
    
    Args:
        current_user: Usuário logado
        apenas_ativos: Se True, retorna apenas clientes ativos
    
    Returns:
        Query de clientes filtrada
    """
    from models import Cliente, Vendedor
    
    query = Cliente.query
    
    if apenas_ativos:
        query = query.filter_by(ativo=True)
    
    if current_user.is_super_admin:
        # Super admin vê todos
        return query.all()
    elif current_user.cargo == "vendedor" and current_user.vendedor_id:
        # Vendedor vê apenas seus clientes do dia atual + dias extras liberados
        dia_hoje = get_dia_visita_hoje()
        dias_permitidos = {dia_hoje} if dia_hoje else set()

        from models import VendedorDiaLiberado
        extras = VendedorDiaLiberado.query.filter_by(
            vendedor_id=current_user.vendedor_id,
            empresa_id=current_user.empresa_id,
        ).all()
        for r in extras:
            d_norm = normalizar_dia_visita(r.dia_visita)
            if d_norm:
                dias_permitidos.add(d_norm)

        q = query.filter_by(vendedor_id=current_user.vendedor_id)
        if dias_permitidos:
            q = q.filter(Cliente.dia_visita.in_(list(dias_permitidos)))
        return q.all()
    elif current_user.cargo == "supervisor":
        # Supervisor vê clientes dos seus vendedores
        vendedores_ids = [v.id for v in Vendedor.query.filter_by(
            supervisor_id=current_user.id
        ).all()]
        return query.filter(Cliente.vendedor_id.in_(vendedores_ids)).all()
    else:
        # Admin da empresa vê clientes da sua empresa
        return query.filter_by(empresa_id=current_user.empresa_id).all()


def paginar_query(query, page=1, per_page=20):
    """
    Pagina uma query do SQLAlchemy
    
    Args:
        query: Query do SQLAlchemy
        page: Página atual (começando em 1)
        per_page: Itens por página
    
    Returns:
        Objeto de paginação do Flask-SQLAlchemy
    """
    return query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )


def validar_email(email):
    """
    Valida formato de email
    
    Args:
        email: String com email
    
    Returns:
        True se válido, False caso contrário
    """
    if not email:
        return False
    
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))


def calcular_porcentagem(valor, total):
    """
    Calcula porcentagem com segurança contra divisão por zero
    
    Args:
        valor: Valor parcial
        total: Valor total
    
    Returns:
        Float com porcentagem (0-100)
    """
    if not total or total == 0:
        return 0.0
    return round((valor / total) * 100, 2)


def pode_importar(current_user, tipo_importacao="geral"):
    """
    Verifica se o usuário tem permissão para importar dados
    
    Args:
        current_user: Usuário logado
        tipo_importacao: Tipo de importação ('clientes', 'vendedores', 'supervisores', 'metas', 'produtos', 'geral')
    
    Returns:
        Boolean indicando se pode importar
    """
    # Admin, Supervisores (incluindo supervisor_manutencao) e Gerentes (incluindo gerente_manutencao), além de RH, podem importar
    # Conforme especificação: Vendedor, Técnico, Administrativo, Financeiro e Usuário NÃO podem importar
    if current_user.cargo in ["admin", "supervisor", "supervisor_manutencao", "rh", "gerente", "gerente_manutencao"]:
        return True
    
    # Verificar permissão específica de importação de clientes (campo granular)
    if tipo_importacao == "clientes" and hasattr(current_user, 'pode_importar_clientes'):
        return current_user.pode_importar_clientes
    
    return False


def pode_exportar(current_user, tipo_exportacao="geral"):
    """
    Verifica se o usuário tem permissão para exportar dados
    
    Args:
        current_user: Usuário logado
        tipo_exportacao: Tipo de exportação ('clientes', 'vendedores', 'metas', 'produtos', 'geral')
    
    Returns:
        Boolean indicando se pode exportar
    """
    # Admin, Supervisores (incluindo supervisor_manutencao) e Gerentes (incluindo gerente_manutencao), além de RH, podem exportar tudo
    if current_user.cargo in ["admin", "supervisor", "supervisor_manutencao", "rh", "gerente", "gerente_manutencao"]:
        return True
    
    # Vendedor NÃO pode exportar lista de clientes (conforme especificação)
    # Apenas Admin, Gerente, Supervisor e RH podem exportar
    
    return False


def get_cargos_permitidos_importacao(tipo_importacao="geral"):
    """
    Retorna lista de cargos permitidos para cada tipo de importação
    
    Args:
        tipo_importacao: Tipo de importação
    
    Returns:
        Tupla com lista de cargos permitidos
    """
    # Conforme especificação: Apenas Admin, Gerente (inclui gerente_manutencao),
    # Supervisor (inclui supervisor_manutencao) e RH podem importar
    # Vendedor, Técnico, Administrativo, Financeiro e Usuário NÃO podem importar
    cargos_por_tipo = {
        "clientes": [
            "admin",
            "supervisor",
            "supervisor_manutencao",
            "rh",
            "gerente",
            "gerente_manutencao",
        ],
        "vendedores": [
            "admin",
            "supervisor",
            "supervisor_manutencao",
            "rh",
            "gerente",
            "gerente_manutencao",
        ],
        "supervisores": [
            "admin",
            "supervisor",
            "supervisor_manutencao",
            "rh",
            "gerente",
            "gerente_manutencao",
        ],
        "metas": [
            "admin",
            "supervisor",
            "supervisor_manutencao",
            "rh",
            "gerente",
            "gerente_manutencao",
        ],
        "produtos": [
            "admin",
            "supervisor",
            "supervisor_manutencao",
            "rh",
            "gerente",
            "gerente_manutencao",
        ],
        "geral": [
            "admin",
            "supervisor",
            "supervisor_manutencao",
            "rh",
            "gerente",
            "gerente_manutencao",
        ],
    }
    
    return tuple(cargos_por_tipo.get(tipo_importacao, ["admin"]))


def get_cargos_permitidos_exportacao(tipo_exportacao="geral"):
    """
    Retorna lista de cargos permitidos para cada tipo de exportação
    
    Args:
        tipo_exportacao: Tipo de exportação
    
    Returns:
        Tupla com lista de cargos permitidos
    """
    # Conforme especificação: Vendedor NÃO pode exportar lista de clientes
    # Apenas Admin, Gerente (inclui gerente_manutencao), Supervisor (inclui
    # supervisor_manutencao) e RH podem exportar dados
    cargos_por_tipo = {
        "clientes": [
            "admin",
            "supervisor",
            "supervisor_manutencao",
            "rh",
            "gerente",
            "gerente_manutencao",
        ],
        "vendedores": [
            "admin",
            "supervisor",
            "supervisor_manutencao",
            "rh",
            "gerente",
            "gerente_manutencao",
        ],
        "metas": [
            "admin",
            "supervisor",
            "supervisor_manutencao",
            "rh",
            "gerente",
            "gerente_manutencao",
        ],
        "produtos": [
            "admin",
            "supervisor",
            "supervisor_manutencao",
            "rh",
            "gerente",
            "gerente_manutencao",
        ],
        "geral": [
            "admin",
            "supervisor",
            "supervisor_manutencao",
            "rh",
            "gerente",
            "gerente_manutencao",
        ],
    }
    
    return tuple(cargos_por_tipo.get(tipo_exportacao, ["admin"]))


def validar_arquivo_excel(request, nome_campo='arquivo'):
    """
    Valida se o arquivo Excel enviado é válido
    
    Args:
        request: Objeto request do Flask
        nome_campo: Nome do campo do arquivo no form (padrão: 'arquivo')
    
    Returns:
        tuple: (arquivo, erro_msg) - arquivo ou None se inválido, mensagem de erro ou None se OK
    """
    # Verificar se arquivo foi enviado
    if nome_campo not in request.files:
        return None, "Nenhum arquivo selecionado!"
    
    arquivo = request.files[nome_campo]
    
    # Verificar se arquivo tem nome
    if arquivo.filename == "":
        return None, "Nenhum arquivo selecionado!"
    
    # Verificar extensão
    if not arquivo.filename.endswith((".xlsx", ".xls")):
        return None, "Formato inválido! Use apenas .xlsx ou .xls"
    
    return arquivo, None


def verificar_excel_disponivel(ensure_func=None):
    """
    Verifica se bibliotecas Excel estão disponíveis
    
    Args:
        ensure_func: Função opcional para tentar recarregar Excel (ensure_excel_available)
    
    Returns:
        tuple: (disponivel, erro_msg) - True se disponível, mensagem de erro se não
    """
    try:
        import pandas
        import openpyxl
        return True, None
    except ImportError as e:
        # Tentar recarregar se função fornecida
        if ensure_func and callable(ensure_func):
            if ensure_func():
                return True, None
        return False, f"Bibliotecas Excel não instaladas: {str(e)}"
