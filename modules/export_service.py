"""
Módulo de serviços de Importação/Exportação (Excel/PDF)
Abstrai integração com pandas/openpyxl e pdf_generator.
"""
from io import BytesIO
from typing import Tuple, List

from flask import current_app

# Excel libs são carregadas condicionalmente via app.ensure_excel_available
# e helpers.verificar_excel_disponivel. Aqui tentamos importar quando usados.

def gerar_planilha_clientes(clientes: List[dict]) -> Tuple[bool, BytesIO | None, str | None]:
    """Gera um arquivo XLSX em memória com a lista de clientes.
    Espera uma lista de dicts com chaves padrões.
    """
    try:
        import pandas as pd
        df = pd.DataFrame(clientes)
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Clientes")
        buffer.seek(0)
        return True, buffer, None
    except Exception as e:
        return False, None, str(e)


def gerar_pdf_metas_wrapper(metas, mes: int, ano: int) -> Tuple[bool, BytesIO | None, str | None]:
    """Wrapper que usa pdf_generator para retornar um BytesIO pronto para resposta."""
    try:
        from pdf_generator import gerar_pdf_metas
        buffer = gerar_pdf_metas(metas, mes, ano)
        # pdf_generator retorna BytesIO; garantir ponteiro no início
        buffer.seek(0)
        return True, buffer, None
    except Exception as e:
        return False, None, str(e)
