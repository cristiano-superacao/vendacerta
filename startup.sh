#!/bin/bash
# startup.sh - Script de inicialização robusto para Railway

# Falhar em caso de erro
set -e

echo "======================================================================"
echo "🚀 INICIANDO SCRIPT DE STARTUP (VendaCerta)"
echo "======================================================================"

# 1. Ativar Virtual Environment
if [ -d ".venv" ]; then
    echo "📦 Ativando ambiente virtual (.venv)..."
    source .venv/bin/activate
else
    echo "❌ ERRO: Ambiente virtual .venv não encontrado!"
    echo "   Verifique se o build do Nixpacks completou corretamente."
    exit 1
fi

# 2. Verificar instalação do Gunicorn
if ! command -v gunicorn &> /dev/null; then
    echo "❌ ERRO: Gunicorn não encontrado no path!"
    echo "   Instalando dependências de emergência..."
    pip install gunicorn flask
fi

# 3. Corrigir estrutura do banco de dados
echo "🔧 Verificando/corrigindo estrutura do banco PostgreSQL..."
if [ -f "fix_database_railway.py" ]; then
    if python fix_database_railway.py; then
        echo "✅ Estrutura do banco verificada/corrigida."
    else
        echo "⚠️  AVISO: Falha na correção do banco. Continuando..."
    fi
else
    echo "⚠️  Script fix_database_railway.py não encontrado."
fi

# 4. Inicializar Banco de Dados (com tratamento de erro)
echo "🔧 Executando script de inicialização (init_railway.py)..."
if python init_railway.py; then
    echo "✅ Inicialização do banco concluída."
else
    echo "⚠️  AVISO: Falha na inicialização do banco. Continuando para permitir debug..."
fi

# 4.1. Migrar Schema (adicionar novas colunas) - VERSÃO SIMPLIFICADA
echo "🔧 Executando migração de schema (add_supervisor_id_railway.py)..."
if [ -f "add_supervisor_id_railway.py" ]; then
    if python add_supervisor_id_railway.py; then
        echo "✅ Migração de schema concluída."
    else
        echo "⚠️  AVISO: Falha na migração do schema. Continuando..."
    fi
else
    echo "⚠️  Script add_supervisor_id_railway.py não encontrado."
fi

# 5. Iniciar Gunicorn
echo "⚡ Iniciando servidor Gunicorn na porta $PORT..."
echo "======================================================================"

# Usar exec para que o Gunicorn assuma o PID 1
exec gunicorn wsgi:app \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --worker-class gthread \
    --threads 4 \
    --timeout 120 \
    --keep-alive 5 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
