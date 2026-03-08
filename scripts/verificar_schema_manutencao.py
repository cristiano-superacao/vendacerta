"""
Verifica no PostgreSQL do Railway se o schema de manutenção/técnicos está correto:
- Tabela: faixas_comissao_manutencao
- Coluna: tecnicos.faixa_manutencao_id
"""
import sys

from sqlalchemy import create_engine, inspect

from db_utils import get_database_url


def main():
    print("\n=== Verificação de Schema: Manutenção/Técnicos ===")
    url = get_database_url(prefer_public=True)
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
