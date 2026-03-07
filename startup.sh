#!/bin/bash
# startup.sh - startup resiliente para Railway

set -eu

cd /app

if [ ! -d ".venv" ]; then
    echo "[ERRO] Ambiente virtual .venv nao encontrado"
    exit 1
fi

source .venv/bin/activate

# Evita inicializacoes pesadas/sincronas no import do app para liberar o healthcheck rapido.
export SKIP_INIT="${SKIP_INIT:-1}"
export SKIP_DB_INIT_ON_START="${SKIP_DB_INIT_ON_START:-1}"
export RUN_DB_INIT_ON_START="${RUN_DB_INIT_ON_START:-0}"

export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"

exec gunicorn wsgi:app \
    --bind 0.0.0.0:${PORT} \
    --workers ${GUNICORN_WORKERS:-2} \
    --threads ${GUNICORN_THREADS:-4} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --keep-alive ${GUNICORN_KEEP_ALIVE:-5} \
    --log-level ${GUNICORN_LOG_LEVEL:-info} \
    --access-logfile - \
    --error-logfile -
