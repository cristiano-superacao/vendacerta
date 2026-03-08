import subprocess
import sys
import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


CHECKS = [
    {
        "name": "Compilacao Python",
        "cmd": [
            sys.executable,
            "-m",
            "py_compile",
            "app.py",
            "scripts/check_all_routes.py",
            "scripts/check_templates.py",
            "scripts/analisar_duplicacoes.py",
            "scripts/verificar_sistema.py",
        ],
        "required_tokens": [],
    },
    {
        "name": "Duplicidades Reais",
        "cmd": [sys.executable, "scripts/analisar_duplicacoes.py"],
        "required_tokens": [
            "Rotas duplicadas: 0",
            "Imports possivelmente não usados: 0",
            "Seletores CSS duplicados: 0",
            "Templates com conteúdo duplicado: 0",
        ],
    },
    {
        "name": "Rotas x Templates",
        "cmd": [sys.executable, "scripts/check_all_routes.py"],
        "required_tokens": ["Templates faltando: 0"],
    },
]


def run_check(check):
    print("\n" + "=" * 72)
    print(f"[CHECK] {check['name']}")
    print("=" * 72)
    print("$ " + " ".join(check["cmd"]))

    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        check["cmd"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    print(output.strip() if output.strip() else "(sem output)")

    if result.returncode != 0:
        print(f"\n[ERRO] Comando falhou com codigo {result.returncode}")
        return False

    for token in check["required_tokens"]:
        if token not in output:
            print(f"\n[ERRO] Resultado inesperado. Nao encontrei: {token}")
            return False

    print("\n[OK] Check concluido com sucesso.")
    return True


def main():
    print("\nIniciando pre-release check do VendaCerta...")
    print(f"Repositorio: {REPO_ROOT}")

    for check in CHECKS:
        if not run_check(check):
            print("\nRESULTADO FINAL: FALHA")
            sys.exit(1)

    print("\nRESULTADO FINAL: SUCESSO")
    sys.exit(0)


if __name__ == "__main__":
    main()
