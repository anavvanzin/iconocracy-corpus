#!/usr/bin/env python3
"""
notion_sync.py — Sincroniza records.jsonl ↔ Notion database.

Uso:
    python tools/scripts/notion_sync.py pull   # Notion → JSONL
    python tools/scripts/notion_sync.py push   # JSONL → Notion
    python tools/scripts/notion_sync.py sync   # Bidirecional (last-write-wins)

Variáveis de ambiente requeridas:
    NOTION_API_KEY          Token de integração Notion
    NOTION_CORPUS_DB_ID     ID da database principal

Referência: docs/notion-schema.md, docs/adr/002-notion-as-index.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

RECORDS_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "records.jsonl"


def _require_env(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        print(f"ERRO: variável de ambiente {name} não definida.", file=sys.stderr)
        sys.exit(1)
    return val


def pull() -> None:
    """Baixa registros do Notion e atualiza records.jsonl."""
    _require_env("NOTION_API_KEY")
    _require_env("NOTION_CORPUS_DB_ID")
    # TODO: implementar chamada à Notion API
    print("notion_sync pull: não implementado ainda — stub criado para scaffolding.")


def push() -> None:
    """Envia registros de records.jsonl para Notion."""
    _require_env("NOTION_API_KEY")
    _require_env("NOTION_CORPUS_DB_ID")
    if not RECORDS_PATH.exists():
        print(f"ERRO: {RECORDS_PATH} não encontrado.", file=sys.stderr)
        sys.exit(1)
    # TODO: implementar upsert via Notion API (idempotente por item_id)
    print("notion_sync push: não implementado ainda — stub criado para scaffolding.")


def sync() -> None:
    """Sincronização bidirecional com resolução last-write-wins."""
    _require_env("NOTION_API_KEY")
    _require_env("NOTION_CORPUS_DB_ID")
    # TODO: implementar merge bidirecional
    print("notion_sync sync: não implementado ainda — stub criado para scaffolding.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sincroniza records.jsonl ↔ Notion")
    parser.add_argument("command", choices=["pull", "push", "sync"])
    args = parser.parse_args()

    commands = {"pull": pull, "push": push, "sync": sync}
    commands[args.command]()


if __name__ == "__main__":
    main()
