"""
Script de instalação local - Instala apenas dependências essenciais
Pula gevent e psycopg2 que requerem compilação e são apenas para produção
"""
import subprocess
import sys

# Dependências essenciais para desenvolvimento local (sem gevent e psycopg2)
packages = [
    "Flask==3.0.0",
    "Werkzeug==3.0.1",
    "Flask-SQLAlchemy==3.1.1",
    "Flask-Login==0.6.3",
    "Flask-WTF==1.2.1",
    "Flask-Compress==1.15",
    "Flask-Caching==2.1.0",
    "Flask-Migrate==4.0.5",
    "WTForms==3.1.2",
    "email-validator==2.1.0",
    "SQLAlchemy==2.0.23",
    "alembic==1.13.1",
    "python-dotenv==1.0.1",
    "reportlab==4.2.5",
    "Pillow==10.4.0",
    "openpyxl==3.1.2",
    "pandas==2.2.0",
    "APScheduler==3.10.4",
    "pytz==2024.1",
    "python-dateutil==2.8.2",
    "click==8.1.7",
]

print("🚀 Instalando dependências para desenvolvimento local...")
print("⏩ Pulando gevent e psycopg2 (apenas para produção)\n")

for package in packages:
    print(f"📦 Instalando {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
        print(f"✅ {package} instalado com sucesso!")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar {package}")

print("\n✨ Instalação concluída!")
print("\n📝 Para iniciar o servidor:")
print("   python app.py")
