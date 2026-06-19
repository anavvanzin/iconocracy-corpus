#!/usr/bin/env python3
"""Carrega o corpus ANALÍTICO = corpus-data.json menos a quarentena.

Fonte única de "o N analítico" para notebooks/análise. NÃO muta o canônico:
o export `corpus/corpus-data.json` permanece o ledger completo; aqui aplicamos
o manifesto de exclusão (`corpus/quarantine/manifest.json`) em memória.

Decisão Ana 2026-06-19 (dois filtros disjuntos) — ver
`data/reports/nframe-audit-2026-06-19.md` e `docs/decisions/DIALETICA-N165-vs-265.md`.

Uso:
    from tools.scripts.analytic_corpus import load_analytic_corpus
    records = load_analytic_corpus()          # subset analítico (exclui quarentena)

    python tools/scripts/analytic_corpus.py             # imprime contagens + estratos
    python tools/scripts/analytic_corpus.py --include-quarantined   # ledger completo
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
CORPUS = REPO / "corpus" / "corpus-data.json"
MANIFEST = REPO / "corpus" / "quarantine" / "manifest.json"

ICONOCODE_PREFIX = "iconocode"
IMPORT_INSTRUMENTS = {"vault-import", "migration", "manual-entry"}


def _load_json(path: Path) -> object:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo ausente: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_excluded_ids() -> set[str]:
    """Conjunto de ids semânticos excluídos da análise (união dos filtros)."""
    manifest = _load_json(MANIFEST)
    excluded: set[str] = set()
    for spec in manifest.get("filters", {}).values():
        excluded.update(spec.get("ids", []))
    return excluded


def load_analytic_corpus(include_quarantined: bool = False) -> list[dict]:
    """Retorna os registros do corpus, excluindo a quarentena por padrão."""
    records = _load_json(CORPUS)
    if not isinstance(records, list):
        raise ValueError(f"Esperava lista em {CORPUS}, obtive {type(records).__name__}")
    if include_quarantined:
        return records
    excluded = load_excluded_ids()
    return [r for r in records if r.get("id") not in excluded]


def _stratum(coded_by: str) -> str:
    if coded_by.startswith(ICONOCODE_PREFIX):
        return "estrato1_iconocode"
    if coded_by in IMPORT_INSTRUMENTS:
        return "estrato2_import_migration"
    return "estrato0_nao_codificado"


def _summary(records: list[dict]) -> None:
    strata = Counter(_stratum(r.get("coded_by") or "") for r in records)
    print(f"N analítico = {len(records)}")
    for name in ("estrato1_iconocode", "estrato2_import_migration", "estrato0_nao_codificado"):
        if strata.get(name):
            print(f"  {name}: {strata[name]}")
    by_country = Counter(r.get("country", "?") for r in records)
    print("países:", dict(by_country.most_common()))


def main() -> None:
    parser = argparse.ArgumentParser(description="Corpus analítico (exclui quarentena).")
    parser.add_argument(
        "--include-quarantined", action="store_true",
        help="Retorna o ledger completo (sem aplicar o manifesto de quarentena).",
    )
    args = parser.parse_args()
    records = load_analytic_corpus(include_quarantined=args.include_quarantined)
    _summary(records)


if __name__ == "__main__":
    main()
