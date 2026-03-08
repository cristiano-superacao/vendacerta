#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WSGI Entry Point para Gunicorn em produção (Railway)
Este arquivo garante que o app seja inicializado corretamente no Railway
"""
import os
import sys

# Adiciona o diretório atual ao path
# Garante que o diretório do app esteja no PYTHONPATH (Linux case-sensitive)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("=" * 70)
print("🚀 Iniciando aplicação via WSGI/Gunicorn...")
print(f"[INFO] Python: {sys.version.split()[0]}")
print(f"🌍 Ambiente: {os.environ.get('FLASK_ENV', 'production')}")
print("=" * 70)

try:
    # Antes de importar o app, tentar corrigir o schema do banco (Railway)
    # Nota: a correção do banco é iniciada em background após app carregar

    # Importa o app do módulo principal
    from app import app as application
    
    app = application
    
    # Configurações específicas para produção
    if __name__ != "__main__":
        # Apenas quando executado via Gunicorn/WSGI
        # Desabilita o modo debug em produção
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        
        # Configura log level apropriado
        import logging
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        
        # Log de inicialização
        app.logger.info('='*70)
        app.logger.info('🚀 Aplicação iniciada via Gunicorn (Produção)')
        
        db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if 'postgresql' in db_uri:
            app.logger.info('🗄️  Database: PostgreSQL (Railway)')
        elif 'sqlite' in db_uri:
            app.logger.info('🗄️  Database: SQLite (Local)')
        
        app.logger.info(f'🔧 Debug: {app.config.get("DEBUG")}')
        app.logger.info(f'📦 Workers: Gunicorn gerenciado')
        app.logger.info('='*70)
        
        print("[OK] Aplicação Flask carregada com sucesso!")
        print("[OK] Health check disponível em: /ping")
        print("=" * 70)

        # Dispara correção do banco em background para não bloquear healthcheck
        try:
            import threading
            def _corrigir_banco_bg():
                try:
                    print("🔧 (BG) Iniciando correção de banco em background...")
                    fix_module = os.path.join(os.path.dirname(__file__), "fix_database_railway.py")
                    if not os.path.exists(fix_module):
                        print("ℹ️ (BG) fix_database_railway.py indisponível no container. Pulando correção automática.")
                        return

                    from fix_database_railway import fix_database
                    ok = fix_database()
                    if ok:
                        print("✅ (BG) Banco verificado/corrigido")
                    else:
                        print("ℹ️ (BG) Correção não aplicada (variáveis insuficientes ou já ok)")
                except Exception as e:
                    print(f"ℹ️ (BG) Correção automática indisponível: {e}")
            threading.Thread(target=_corrigir_banco_bg, daemon=True).start()
        except Exception as e:
            print(f"⚠️ Aviso: não foi possível iniciar correção em background: {e}")
    
    # Exporta a aplicação para o Gunicorn
    application = app

except Exception as e:
    print(f"[ERRO] ERRO FATAL ao importar aplicação: {e}")
    import traceback
    traceback.print_exc()
    raise  # Re-raise para Gunicorn detectar o erro

if __name__ == "__main__":
    # Se executado diretamente (não recomendado)
    print("[AVISO]  Aviso: Use 'python app.py' para desenvolvimento local")
    print("[AVISO]  Ou 'gunicorn wsgi:application' para produção")
