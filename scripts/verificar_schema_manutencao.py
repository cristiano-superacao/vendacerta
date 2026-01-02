"""
Verifica no PostgreSQL do Railway se o schema de manutenção/técnicos está correto:
- Tabela: faixas_comissao_manutencao
- Coluna: tecnicos.faixa_manutencao_id
"""
import os
import sys
from sqlalchemy import create_engine, inspect


def get_db_url():
    url = (
        os.getenv("DATABASE_PUBLIC_URL")
        or os.getenv("DATABASE_URL")
    )
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url:
        return url
    # Build from PG* vars if needed
    host = os.getenv("PGHOST")
    port = os.getenv("PGPORT", "5432")
    user = os.getenv("PGUSER")
    pwd = os.getenv("PGPASSWORD")
    db = os.getenv("PGDATABASE")
    if all([host, user, pwd, db]):
        return f"postgresql://{user}:{pwd}@{host}:{port}/{db}"
    return None


def main():
    print("\n=== Verificação de Schema: Manutenção/Técnicos ===")
    url = get_db_url()
    if not url:
        print("[ERRO] Variáveis de conexão não encontradas.")
        sys.exit(1)
    try:
        engine = create_engine(url, echo=False)
        insp = inspect(engine)
        tables = set(insp.get_table_names())
        ok = True

        # Tabela faixas_comissao_manutencao
        if "faixas_comissao_manutencao" in tables:
            print("[OK] Tabela 'faixas_comissao_manutencao' encontrada")
        else:
            print("[FALHA] Tabela 'faixas_comissao_manutencao' NÃO encontrada")
            ok = False

        # Coluna tecnicos.faixa_manutencao_id
        if "tecnicos" in tables:
            cols = [c["name"] for c in insp.get_columns("tecnicos")]
            if "faixa_manutencao_id" in cols:
                print("[OK] Coluna 'tecnicos.faixa_manutencao_id' encontrada")
            else:
                print("[FALHA] Coluna 'tecnicos.faixa_manutencao_id' NÃO encontrada")
                ok = False
        else:
            print("[FALHA] Tabela 'tecnicos' NÃO encontrada")
            ok = False

        print("\nResultado:")
        if ok:
            print("✅ Schema OK")
            sys.exit(0)
        else:
            print("❌ Schema incompleto")
            sys.exit(2)
    except Exception as e:
        print(f"[ERRO] Falha ao verificar schema: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
