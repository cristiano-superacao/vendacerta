from app import app, db
from models import FaixaComissaoManutencao

DEFAULT_FAIXAS = [
    # ordem, min, max, taxa%, cor
    (0, 0, 50, 0.015, 'danger'),
    (1, 51, 75, 0.025, 'warning'),
    (2, 76, 100, 0.035, 'info'),
    (3, 125, 10000, 0.05, 'success'),
]

if __name__ == '__main__':
    with app.app_context():
        created = 0
        for ordem, amin, amax, taxa, cor in DEFAULT_FAIXAS:
            exists = FaixaComissaoManutencao.query.filter_by(ordem=ordem).first()
            if exists:
                continue
            faixa = FaixaComissaoManutencao(
                empresa_id=None,
                alcance_min=float(amin),
                alcance_max=float(amax),
                taxa_comissao=float(taxa),
                cor=cor,
                ordem=ordem,
            )
            db.session.add(faixa)
            created += 1
        db.session.commit()
        print(f"Seed concluído. Faixas criadas: {created}")
