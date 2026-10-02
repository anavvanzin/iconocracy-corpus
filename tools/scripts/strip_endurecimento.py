#!/usr/bin/env python3
"""Migração única: remove o escore composto aposentado dos dados canônicos.

Decisão da autora (2026-09-24), completando a aposentadoria metodológica de
2026-07-28 (`docs/decisions/2026-07-28-aposentadoria-do-indice-composto.md`):
o índice composto de endurecimento vira passado completo. A codificação vigente
é o inventário verbal de atributos (qualitativo) sobre os 10 indicadores
ordinais — que permanecem intactos.

Este script limpa os artefatos numéricos dos três artefatos de dados:

1. ``corpus/corpus-data.json`` — projeção pública:
   ``endurecimento_score`` e ``indicadores`` de nível superior;
2. ``data/processed/records.jsonl`` — ledger canônico (uma linha por item):
   ``endurecimento_score``/``indicadores``/``purificacao_composto`` de nível
   superior, ``iconographic_metadata.endurecimento_score``,
   ``purificacao.purificacao_composto`` e
   ``purificacao.record_metadata.endurecimento_score`` (os 10 indicadores
   ordinais e o ``regime_iconocratico`` NÃO são tocados);
3. ``data/processed/purification.jsonl`` — ledger de codificação:
   ``purificacao_composto`` (os 10 indicadores ordinais NÃO são tocados);
4. o parêntese mecânico ``(endurecimento N.N)`` embutido em
   ``panofsky.interpretation[].claim_text`` (top-level ou aninhado em
   ``iconographic_metadata``) e em ``iconocode.interpretation[].claim_text``.

O que NÃO é tocado: as ocorrências da palavra "endurecimento" como conceito na
prosa interpretativa (ex.: "Justiça antes do endurecimento alegórico"). Essas são
editoriais — rever caso a caso, não por script.

Uso:
    python tools/scripts/strip_endurecimento.py
    git add corpus/corpus-data.json data/processed && git commit -m "data: strip retired endurecimento score"
"""
import json
import os
import tempfile
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

JSON_ARRAYS = [
    REPO / "corpus" / "corpus-data.json",
]
JSONL_LEDGERS = [
    REPO / "data" / "processed" / "records.jsonl",
    REPO / "data" / "processed" / "purification.jsonl",
]
PAREN_SCORE = re.compile(r"\s*\(endurecimento\s+\d+(?:\.\d+)?\)")

DROP_TOP_LEVEL = ("endurecimento_score", "indicadores", "purificacao_composto")


def atomic_write(path: Path, payload: str) -> None:
    """Replace only after a complete, flushed sibling file exists."""
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(payload)
            tmp.flush()
            os.fsync(tmp.fileno())
        tmp_path.replace(path)
    finally:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()


def strip_assignments(value):
    """Remove literal retired assignments, preserving conceptual prose."""
    if isinstance(value, dict):
        return {k: strip_assignments(v) for k, v in value.items()}
    if isinstance(value, list):
        return [strip_assignments(v) for v in value]
    if isinstance(value, str):
        return re.sub(r"endurecimento_score\s*=\s*\d+(?:[.,]\d+)?", "[valor composto aposentado removido]", value)
    return value


def strip_item(item: dict) -> int:
    """Remove os artefatos do escore de um item. Retorna quantas remoções fez."""
    removed = 0
    for key in DROP_TOP_LEVEL:
        if key in item:
            del item[key]
            removed += 1
    meta = item.get("iconographic_metadata")
    if isinstance(meta, dict) and "endurecimento_score" in meta:
        del meta["endurecimento_score"]
        removed += 1
    pur = item.get("purificacao")
    if isinstance(pur, dict):
        if "purificacao_composto" in pur:
            del pur["purificacao_composto"]
            removed += 1
        rec_meta = pur.get("record_metadata")
        if isinstance(rec_meta, dict) and "endurecimento_score" in rec_meta:
            del rec_meta["endurecimento_score"]
            removed += 1
    # Parêntese mecânico em claim_text (panofsky top-level, aninhado em
    # iconographic_metadata, ou iconocode do ledger master-record).
    fontes = [item.get("panofsky"), (meta or {}).get("panofsky"), item.get("iconocode")]
    for fonte in fontes:
        if not isinstance(fonte, dict):
            continue
        for interp in fonte.get("interpretation") or []:
            text = interp.get("claim_text", "")
            text, n = PAREN_SCORE.subn("", text)
            if n:
                interp["claim_text"] = text
                removed += n
    cleaned = strip_assignments(item)
    if cleaned != item:
        item.clear()
        item.update(cleaned)
        removed += 1
    return removed


def strip_json_array(path: Path) -> None:
    items = json.loads(path.read_text(encoding="utf-8"))
    removed = sum(strip_item(item) for item in items)
    if removed:
        atomic_write(path, json.dumps(items, ensure_ascii=False, indent=2) + "\n")
    print(f"{path}: {removed} artefatos de escore removidos ({len(items)} itens)")


def strip_jsonl(path: Path) -> None:
    lines = []
    removed = 0
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        removed += strip_item(row)
        lines.append(json.dumps(row, ensure_ascii=False))
        n += 1
    if removed:
        atomic_write(path, "\n".join(lines) + "\n")
    print(f"{path}: {removed} artefatos de escore removidos ({n} linhas)")


if __name__ == "__main__":
    for p in JSON_ARRAYS:
        strip_json_array(p)
    for p in JSONL_LEDGERS:
        strip_jsonl(p)
