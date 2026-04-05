#!/usr/bin/env python3
"""
notion_sync.py — DESCONTINUADO

O Notion não é mais usado como espelho catalográfico.
O vault Obsidian é agora a fonte canônica auxiliar.

Use vault_sync.py em vez disso:

    python tools/scripts/vault_sync.py status
    python tools/scripts/vault_sync.py pull
    python tools/scripts/vault_sync.py push
    python tools/scripts/vault_sync.py sync
    python tools/scripts/vault_sync.py diff

Para documentação completa, consulte docs/scripts.md.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

VAULT_SYNC = Path(__file__).parent / "vault_sync.py"


def _deprecation_warning() -> None:
    print(
        "AVISO: notion_sync.py está descontinuado.\n"
        "O Notion não é mais utilizado como espelho catalográfico.\n"
        "Use vault_sync.py para sincronizar com o vault Obsidian:\n\n"
        f"    python tools/scripts/vault_sync.py <comando>\n\n"
        "Comandos disponíveis: status | diff | pull | push | sync\n",
        file=sys.stderr,
    )


def main() -> None:
    _deprecation_warning()

    args = sys.argv[1:]
    cmd_map = {"pull": "pull", "push": "push", "diff": "diff", "status": "status"}
    if args and args[0] in cmd_map:
        vault_cmd = cmd_map[args[0]]
        print(f"Redirecionando para vault_sync.py {vault_cmd}...\n", file=sys.stderr)
        result = subprocess.run(
            [sys.executable, str(VAULT_SYNC), vault_cmd] + args[1:],
            check=False,
        )
        sys.exit(result.returncode)
    else:
        print("Uso: python tools/scripts/vault_sync.py [status|diff|pull|push|sync]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
