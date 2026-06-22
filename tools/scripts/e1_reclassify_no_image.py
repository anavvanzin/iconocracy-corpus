#!/usr/bin/env python3
"""
e1_reclassify_no_image.py — Reclassifica entradas #no-image do pathosformel_index.jsonl
em três estados honestos, povoando motivo_exclusao (audit trail Tier 2).

Resolve o achado da auditoria data/reports/e1-noimage-audit-2026-06-22.md:
o e1_mark_no_image.py fechou o DoD E1 marcando tudo o que não foi codificado
como e1-no-image, sem distinguir "backlog com URL viva" de "genuinamente sem
imagem", e sem registar motivo.

Classificação (por cruzamento sigla_id <-> corpus-data.json::id):
  - URL viva (http, host != iconocracy.corpus)  -> e1-uncoded, coded_from=backlog
  - iconocracy.corpus/vault/<uuid> (local)      -> e1-uncoded, coded_from=backlog
  - sem URL (url e thumbnail_url vazias)         -> e1-no-image (mantém), motivo irrecuperável

Idempotente: pode ser re-executada; entradas já e1-uncoded/e1-no-image com motivo
não são reescritas a menos que --force. Não toca entradas fable-5 (codificadas ou
fora_escopo).

Uso:
    python tools/scripts/e1_reclassify_no_image.py --dry-run    # lista apenas
    python tools/scripts/e1_reclassify_no_image.py              # grava
    python tools/scripts/e1_reclassify_no_image.py --force      # re-escreve motivo mesmo já classificado
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent.parent.parent
CORPUS_PATH = REPO / "corpus" / "corpus-data.json"
INDEX_PATH = REPO / "data" / "processed" / "pathosformel_index.jsonl"

BACKLOG_MOTIVO = "Backlog — URL viva/local esperado, não codificado nesta passagem (re-aquisição julho/2026)"
NOIMAGE_MOTIVO = "Sem URL/fonte de imagem — irrecuperável"

BACKLOG_NOTE_PREFIX = "#uncoded — backlog com fonte recuperável; não codificado nesta passagem"
NOIMAGE_NOTE = "#no-image — sem URL nem fonte de imagem acessível; irrecuperável"


def load_corpus_url_map() -> dict[str, dict]:
    """sigla_id -> corpus item (para url/thumbnail_url)."""
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)
    if isinstance(corpus, dict):
        corpus = corpus.get("items") or corpus.get("corpus") or []
    return {c.get("id"): c for c in corpus if c.get("id")}


def classify(corpus_item: dict | None) -> tuple[str, str, str, str]:
    """Retorna (coded_by, coded_from, motivo_exclusao, notes)."""
    if corpus_item is None:
        # sem correspondência no corpus — trata como sem imagem
        return ("e1-no-image", "no_image", NOIMAGE_MOTIVO, NOIMAGE_NOTE)
    url = corpus_item.get("url") or ""
    thumb = corpus_item.get("thumbnail_url") or ""
    if url.startswith("http"):
        host = urlparse(url).netloc.replace("www.", "")
        if host == "iconocracy.corpus":
            return ("e1-uncoded", "backlog", BACKLOG_MOTIVO,
                    f"{BACKLOG_NOTE_PREFIX} (local vault, UUID não resolve a ficheiro)")
        return ("e1-uncoded", "backlog", BACKLOG_MOTIVO,
                f"{BACKLOG_NOTE_PREFIX} (host={host})")
    if thumb.startswith("http"):
        host = urlparse(thumb).netloc.replace("www.", "")
        return ("e1-uncoded", "backlog", BACKLOG_MOTIVO,
                f"{BACKLOG_NOTE_PREFIX} (thumbnail host={host})")
    # nem url nem thumbnail — genuinamente sem imagem
    return ("e1-no-image", "no_image", NOIMAGE_MOTIVO, NOIMAGE_NOTE)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="lista apenas, não grava")
    ap.add_argument("--force", action="store_true",
                    help="re-escreve motivo mesmo em entradas já e1-uncoded/e1-no-image")
    args = ap.parse_args()

    if not INDEX_PATH.exists():
        print(f"Erro: {INDEX_PATH} não existe", file=sys.stderr)
        return 1

    corpus_map = load_corpus_url_map()

    out_lines: list[str] = []
    counts = {"fable-5": 0, "e1-uncoded": 0, "e1-no-image": 0, "other": 0}
    reclassified = 0
    kept = 0

    with open(INDEX_PATH) as f:
        for line in f:
            if not line.strip():
                out_lines.append(line)
                continue
            d = json.loads(line)
            cb = d.get("coded_by")
            fora = d.get("fora_escopo")

            if cb == "fable-5":
                # codificação real (in-scope ou fora_escopo) — intocável
                counts["fable-5"] += 1
                out_lines.append(json.dumps(d, ensure_ascii=False))
                continue

            if cb in ("e1-no-image", "e1-uncoded"):
                corpus_item = corpus_map.get(d.get("sigla_id"))
                new_cb, new_from, motivo, notes = classify(corpus_item)
                already = (cb == new_cb and d.get("motivo_exclusao") == motivo)
                if already and not args.force:
                    counts[new_cb] += 1
                    kept += 1
                    out_lines.append(json.dumps(d, ensure_ascii=False))
                    continue
                d["coded_by"] = new_cb
                d["coded_from"] = new_from
                d["motivo_exclusao"] = motivo
                d["notes"] = notes
                # fora_escopo permanece false para backlog; image_source mantém "none"
                counts[new_cb] += 1
                reclassified += 1
                out_lines.append(json.dumps(d, ensure_ascii=False))
                if args.dry_run:
                    print(f"  {d.get('sigla_id'):8} -> {new_cb:12} motivo={motivo[:70]}")
                continue

            counts["other"] += 1
            out_lines.append(json.dumps(d, ensure_ascii=False))

    print(f"\nContagens: fable-5={counts['fable-5']}  e1-uncoded={counts['e1-uncoded']}  "
          f"e1-no-image={counts['e1-no-image']}  other={counts['other']}")
    total = sum(counts.values())
    print(f"Total: {total}  (reclassificados={reclassified}, mantidos={kept})")
    if total != 265:
        print(f"AVISO: total {total} ≠ 265 esperado", file=sys.stderr)

    if args.dry_run:
        print("\n[dry-run] nada gravado.")
        return 0

    tmp = INDEX_PATH.with_suffix(".jsonl.tmp")
    with open(tmp, "w") as f:
        for line in out_lines:
            f.write(line.rstrip("\n") + "\n")
    tmp.replace(INDEX_PATH)
    print(f"\nGravado: {INDEX_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())