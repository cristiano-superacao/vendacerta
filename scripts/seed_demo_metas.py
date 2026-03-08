"""
Seed de dados de demonstração para testar exportação de PDF
- Cria Empresa, Supervisor, Vendedor e uma Meta de Valor
- Gera dois PDFs em instance/: Vendedores e Supervisores
"""
import os
from datetime import datetime

from app import app, db
from models import Empresa, Usuario, Vendedor, Meta
from pdf_generator import gerar_pdf_metas, gerar_pdf_metas_supervisor


def ensure_demo_data():
    with app.app_context():
        # Empresa
        empresa = Empresa.query.filter_by(cnpj="00.000.000/0001-00").first()
        if not empresa:
            empresa = Empresa(
                nome="Empresa Demo",
                cnpj="00.000.000/0001-00",
                email="contato@demo.local",
                cidade="São Paulo",
                estado="SP",
            )
            db.session.add(empresa)
            db.session.commit()

        # Supervisor
        supervisor = Usuario.query.filter_by(email="supervisor@demo.local").first()
        if not supervisor:
            supervisor = Usuario(
                nome="Supervisor Demo",
                email="supervisor@demo.local",
                senha_hash="",
                cargo="supervisor",
                empresa_id=empresa.id,
                ativo=True,
            )
            db.session.add(supervisor)
            db.session.commit()

        # Vendedor
        vendedor = Vendedor.query.filter_by(email="vendedor@demo.local").first()
        if not vendedor:
            vendedor = Vendedor(
                nome="Jonathan Santos",
                email="vendedor@demo.local",
                empresa_id=empresa.id,
                supervisor_id=supervisor.id,
                supervisor_nome=supervisor.nome,
                ativo=True,
            )
            db.session.add(vendedor)
            db.session.commit()

        # Meta do mês atual
        hoje = datetime.now()
        meta = Meta.query.filter_by(vendedor_id=vendedor.id, mes=hoje.month, ano=hoje.year).first()
        if not meta:
            meta = Meta(
                vendedor_id=vendedor.id,
                mes=hoje.month,
                ano=hoje.year,
                tipo_meta="valor",
                valor_meta=60000.0,
                receita_alcancada=31000.0,
                status_comissao="Aprovado",
            )
            db.session.add(meta)
            db.session.commit()

        # Recalcular comissão
        meta.calcular_comissao()
        db.session.commit()

        return empresa.id, supervisor.id, vendedor.id, meta.id


def gerar_pdfs(empresa_id, supervisor_id, vendedor_id, meta_id):
    with app.app_context():
        hoje = datetime.now()
        # Vendedores
        metas = Meta.query.join(Vendedor).filter(
            Vendedor.empresa_id == empresa_id,
            Meta.mes == hoje.month,
            Meta.ano == hoje.year,
        ).all()
        buf_vend = gerar_pdf_metas(metas, hoje.month, hoje.year)

        # Supervisores (agregar)
        grupos = {}
        for m in metas:
            sup_id = m.vendedor.supervisor_id if m.vendedor else None
            sup_nome = m.vendedor.supervisor_nome if m.vendedor else "N/A"
            if sup_id is None:
                continue
            if sup_id not in grupos:
                grupos[sup_id] = {
                    "supervisor_id": sup_id,
                    "supervisor_nome": sup_nome,
                    "tipo_meta": m.tipo_meta,
                    "mes": hoje.month,
                    "ano": hoje.year,
                    "meta_total": 0.0,
                    "realizado_total": 0.0,
                    "volume_meta_total": 0,
                    "volume_realizado_total": 0,
                    "comissao_total_vendedores": 0.0,
                }
            if m.tipo_meta == "valor":
                grupos[sup_id]["meta_total"] += float(m.valor_meta or 0.0)
                grupos[sup_id]["realizado_total"] += float(m.receita_alcancada or 0.0)
            else:
                grupos[sup_id]["volume_meta_total"] += int(m.volume_meta or 0)
                grupos[sup_id]["volume_realizado_total"] += int(m.volume_alcancado or 0)
            grupos[sup_id]["comissao_total_vendedores"] += float(m.comissao_total or 0.0)

        supervisores_resumo = []
        for g in grupos.values():
            if (g["tipo_meta"] or "valor") == "valor":
                alcance = (g["realizado_total"] / g["meta_total"] * 100) if g["meta_total"] > 0 else 0
                taxa_sup = None  # simplificado para seed
                comissao_sup = float(g["realizado_total"]) * float(taxa_sup or 0)
            else:
                alcance = (g["volume_realizado_total"] / g["volume_meta_total"] * 100) if g["volume_meta_total"] > 0 else 0
                taxa_sup = None
                comissao_sup = g["comissao_total_vendedores"]

            supervisores_resumo.append({
                "id": g["supervisor_id"],
                "nome": g["supervisor_nome"],
                "tipo_meta": g["tipo_meta"],
                "periodo": f"{hoje.month:02d}/{hoje.year}",
                "meta_total": g["meta_total"] if (g["tipo_meta"] == "valor") else g["volume_meta_total"],
                "realizado_total": g["realizado_total"] if (g["tipo_meta"] == "valor") else g["volume_realizado_total"],
                "percentual_alcance": alcance,
                "taxa_supervisor": taxa_sup,
                "comissao_supervisor": comissao_sup,
            })

        buf_sup = gerar_pdf_metas_supervisor(supervisores_resumo, hoje.month, hoje.year)

        # Salvar em instance/
        out_dir = os.path.join(app.instance_path)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, f"Relatorio_Metas_Vendedores_{hoje.month:02d}_{hoje.year}.pdf"), "wb") as f:
            f.write(buf_vend.read())
        with open(os.path.join(out_dir, f"Relatorio_Metas_Supervisores_{hoje.month:02d}_{hoje.year}.pdf"), "wb") as f:
            f.write(buf_sup.read())

        print(f"[OK] PDFs gerados em: {out_dir}")


if __name__ == "__main__":
    empresa_id, supervisor_id, vendedor_id, meta_id = ensure_demo_data()
    gerar_pdfs(empresa_id, supervisor_id, vendedor_id, meta_id)
