import sys
import os
from sqlalchemy import create_engine, text


def test_connection():
    # Tenta pegar a URL do ambiente ou usa a padrão do Docker local
    default_url = 'postgresql://vendacerta_user:vendacerta_password@localhost:5432/vendacerta_db'
    db_url = os.environ.get('DATABASE_URL', default_url)

    print("🔌 Tentando conectar ao PostgreSQL...")
    print(f"📝 URL (mascarada): {db_url.split('@')[0]}@***:{db_url.split(':')[-1]}")

    try:
        engine = create_engine(db_url)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print("\n✅ SUCESSO! Conexão estabelecida.")
            print(f"🐘 Versão do Banco: {version}")
            return True
    except Exception as e:
        print("\n❌ ERRO: Não foi possível conectar.")
        print(f"Detalhes: {str(e)}")
        print("\nDicas:")
        print("1. Verifique se o PostgreSQL está rodando (Docker ou Local).")
        print("2. Verifique usuário, senha e porta.")
        print("3. Se estiver usando Docker, rode: docker-compose up -d")
        return False


if __name__ == "__main__":
    success = test_connection()

    sys.exit(0 if success else 1)
