"""Utilitarios de backup com comportamento seguro para producao.

Este modulo existe para evitar falhas de import em ambientes onde o
fluxo de backup local nao esta habilitado.
"""

from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path


def _backup_dir() -> Path:
    base = Path("instance") / "backups"
    base.mkdir(parents=True, exist_ok=True)
    return base


def _database_path() -> Path | None:
    db_url = (os.environ.get("DATABASE_URL") or "").strip()
    if not db_url.startswith("sqlite:///"):
        return None
    db_file = db_url.replace("sqlite:///", "", 1)
    return Path(db_file)


def criar_backup_db(*args, **kwargs) -> str | None:
    """Cria backup para SQLite local; para outros bancos retorna None."""
    db_file = _database_path()
    if not db_file or not db_file.exists():
        return None

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = _backup_dir() / f"backup_{stamp}.db"
    shutil.copy2(db_file, target)
    return str(target)


def listar_backups(*args, **kwargs) -> list[str]:
    """Lista backups locais disponiveis."""
    return [p.name for p in sorted(_backup_dir().glob("*.db"), reverse=True)]


def restaurar_backup(nome: str, *args, **kwargs) -> bool:
    """Restaura backup local em SQLite; fora disso retorna False."""
    db_file = _database_path()
    if not db_file:
        return False

    origem = _backup_dir() / nome
    if not origem.exists():
        return False

    shutil.copy2(origem, db_file)
    return True


def deletar_backup(nome: str, *args, **kwargs) -> bool:
    """Remove um arquivo de backup local."""
    arq = _backup_dir() / nome
    if not arq.exists():
        return False
    arq.unlink()
    return True
