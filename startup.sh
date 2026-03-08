#!/bin/bash
# startup.sh - SCRIPT DE TESTE PARA ISOLAR O ERRO

# Falhar em caso de erro
set -e

echo "======================================================================"
echo "🚀 INICIANDO SCRIPT DE STARTUP (MODO DE DIAGNÓSTICO)"
echo "======================================================================"

# 1. Ativar Virtual Environment
if [ -d ".venv" ]; then
    echo "📦 Ativando ambiente virtual (.venv)..."
    source .venv/bin/activate
else
    echo "❌ ERRO: Ambiente virtual .venv não encontrado!"
    exit 1
fi

# 2. Configurar bibliotecas do sistema (essencial para Pandas)
echo "🔧 Configurando LD_LIBRARY_PATH para libstdc++..."
LIBSTDC=$(find /nix/store -name libstdc++.so.6 -printf '%h\n' 2>/dev/null | head -n 1)
if [ -n "$LIBSTDC" ]; then
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$LIBSTDC
    echo "✅ LD_LIBRARY_PATH atualizado para: $LD_LIBRARY_PATH"
else
    echo "⚠️  Aviso: libstdc++.so.6 não encontrada automaticamente."
fi

# 3. Adicionar diretório do projeto ao PYTHONPATH
echo "🐍 Adicionando diretório atual ao PYTHONPATH..."
export PYTHONPATH=$PYTHONPATH:$(pwd)
echo "✅ PYTHONPATH atualizado."

# 4. Iniciar Gunicorn diretamente para teste
echo "⚡ Iniciando servidor Gunicorn diretamente para diagnóstico..."
echo "   Os scripts de inicialização do banco foram ignorados temporariamente."
echo "======================================================================"

# Usar exec para que o Gunicorn assuma o PID 1
exec gunicorn wsgi:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --log-level debug \
    --access-logfile - \
    --error-logfile -
