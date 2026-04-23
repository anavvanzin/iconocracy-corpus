#!/usr/bin/env python3
"""
code_purification.py — CLI for coding purification indicators on corpus items.

Reads items from corpus/corpus-data.json, prompts the coder for each of 10
ordinal indicators (0–3) per the codebook, and writes results to
data/processed/purification.jsonl.

Usage:
    python tools/scripts/code_purification.py                  # code next uncoded item
    python tools/scripts/code_purification.py --resume         # skip already-coded items
    python tools/scripts/code_purification.py --item BR-001    # code specific item
    python tools/scripts/code_purification.py --batch FR       # code all FR-* items
    python tools/scripts/code_purification.py --status         # show coding progress
    python tools/scripts/code_purification.py --export-csv     # export to corpus_dataset.csv
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Paths (relative to repo root)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS_JSON = REPO_ROOT / "corpus" / "corpus-data.json"
OUTPUT_JSONL = REPO_ROOT / "data" / "processed" / "purification.jsonl"
OUTPUT_CSV = REPO_ROOT / "data" / "processed" / "corpus_dataset.csv"
CODEBOOK = REPO_ROOT / "data" / "docs" / "codebook.md"

INDICATORS = [
    ("desincorporacao", "Desincorporação do corpo feminino", [
        "0: Corpo naturalista, carnal, individualizado",
        "1: Corpo idealizado mas ainda orgânico",
        "2: Corpo estilizado, traços genéricos",
        "3: Forma puramente geométrica ou ausência de corpo",
    ]),
    ("rigidez_postural", "Rigidez postural e hierática", [
        "0: Movimento dinâmico, gesto espontâneo",
        "1: Pose contida mas com algum movimento",
        "2: Postura rígida, frontal, simétrica",
        "3: Hieratismo total, imobilidade estatuária",
    ]),
    ("dessexualizacao", "Dessexualização", [
        "0: Nudez ou erotismo explícito",
        "1: Decote ou formas corporais sugeridas",
        "2: Corpo coberto mas feminilidade visível",
        "3: Gênero indeterminado ou completamente encoberto",
    ]),
    ("uniformizacao_facial", "Uniformização facial", [
        "0: Retrato individualizado, expressão viva",
        "1: Rosto idealizado mas expressivo",
        "2: Rosto genérico, expressão neutra",
        "3: Sem rosto ou máscara pura",
    ]),
    ("heraldizacao", "Heraldização dos atributos", [
        "0: Atributos integrados à ação da figura",
        "1: Atributos portados mas estáticos",
        "2: Atributos destacados, quase autônomos",
        "3: Atributos isolados como emblemas (sem corpo)",
    ]),
    ("enquadramento_arquitetonico", "Enquadramento arquitetônico", [
        "0: Figura em espaço aberto/narrativo",
        "1: Fundo arquitetônico discreto",
        "2: Moldura arquitetônica define a composição",
        "3: Figura reduzida a elemento decorativo de edifício/selo",
    ]),
    ("apagamento_narrativo", "Apagamento da narrativa", [
        "0: Cena narrativa completa com interação",
        "1: Narrativa sugerida, poucos personagens",
        "2: Figura isolada com vestígio de contexto",
        "3: Figura completamente isolada, fundo neutro",
    ]),
    ("monocromatizacao", "Monocromatização / redução cromática", [
        "0: Policromia rica, cores naturalistas",
        "1: Paleta reduzida mas ainda colorida",
        "2: Bicromia ou tons muito restritos",
        "3: Monocromático / preto-e-branco / dourado-e-branco",
    ]),
    ("serialidade", "Serialidade e repetição", [
        "0: Obra única (pintura, escultura singular)",
        "1: Tiragem limitada (gravura, litografia)",
        "2: Reprodução em média escala (cartaz, livro)",
        "3: Reprodução massiva (selo, moeda, cédula, bandeira)",
    ]),
    ("inscricao_estatal", "Inscrição em dispositivo estatal", [
        "0: Obra autônoma sem vínculo estatal",
        "1: Encomenda oficial mas sem insígnia",
        "2: Contém insígnia estatal como elemento",
        "3: É o próprio dispositivo estatal (selo, brasão, moeda)",
    ]),
]

REGIMES = ["fundacional", "normativo", "militar", "contra-alegoria"]


def load_corpus():
    """Load corpus items from JSON."""
    with open(CORPUS_JSON, encoding="utf-8") as f:
        return json.load(f)


def load_coded(mode="latest"):
    """Load coded items from JSONL.

    Modes:
        latest   — dict[id -> record], last-write-wins (original behavior)
        all      — dict[id -> list[record]], all codings per item (for IRR)
        consensus — dict[id -> record], prefers adjudicated, falls back to latest
    """
    if mode not in ("latest", "all", "consensus"):
        raise ValueError(f"Unknown mode: {mode}")

    all_records = {}  # id -> list[record]
    if OUTPUT_JSONL.exists():
        with open(OUTPUT_JSONL, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rec = json.loads(line)
                    all_records.setdefault(rec["id"], []).append(rec)

    if mode == "all":
        return all_records

    if mode == "consensus":
        result = {}
        for item_id, records in all_records.items():
            adjudicated = [r for r in records if r.get("adjudication_status") == "adjudicated"]
            result[item_id] = adjudicated[-1] if adjudicated else records[-1]
        return result

    # mode == "latest"
    return {item_id: records[-1] for item_id, records in all_records.items()}


def save_record(record):
    """Append a single coded record to the JSONL file."""
    OUTPUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def display_item(item):
    """Display item metadata for the coder."""
    print("\n" + "=" * 70)
    print(f"  ID:       {item['id']}")
    print(f"  Title:    {item['title']}")
    print(f"  Date:     {item['date']}  |  Country: {item['country']}")
    print(f"  Medium:   {item['medium']}")
    print(f"  Period:   {item.get('period', 'N/A')}")
    print(f"  Creator:  {item.get('creator', 'N/A')}")
    print(f"  Motifs:   {item.get('motif_str', ', '.join(item.get('motif', [])))}")
    if item.get("thumbnail_url"):
        print(f"  Image:    {item['thumbnail_url']}")
    if item.get("url"):
        print(f"  Source:   {item['url']}")
    print("=" * 70)


def prompt_indicator(name, label, scale):
    """Prompt for a single indicator. Returns int 0-3 or None to skip."""
    print(f"\n  [{name}] {label}")
    for line in scale:
        print(f"    {line}")
    while True:
        val = input("  → Score (0-3), 's' to skip item, 'q' to quit: ").strip().lower()
        if val == "q":
            return "quit"
        if val == "s":
            return "skip"
        if val in ("0", "1", "2", "3"):
            return int(val)
        print("    ⚠ Enter 0, 1, 2, or 3 (or 's'/'q')")


def prompt_regime():
    """Prompt for regime iconocrático."""
    print(f"\n  [regime_iconocratico] Regime iconocrático")
    for i, r in enumerate(REGIMES):
        print(f"    {i + 1}: {r}")
    while True:
        val = input("  → Choice (1-3), 's' to skip, 'q' to quit: ").strip().lower()
        if val == "q":
            return "quit"
        if val == "s":
            return "skip"
        if val in ("1", "2", "3"):
            return REGIMES[int(val) - 1]
        print("    ⚠ Enter 1, 2, or 3")


def code_item(item, coder="ana"):
    """Interactive coding session for one item. Returns record dict or None."""
    display_item(item)

    scores = {}
    for name, label, scale in INDICATORS:
        result = prompt_indicator(name, label, scale)
        if result == "quit":
            return "quit"
        if result == "skip":
            return None
        scores[name] = result

    regime = prompt_regime()
    if regime == "quit":
        return "quit"
    if regime == "skip":
        return None

    # Compute composite
    composite = round(sum(scores.values()) / len(scores), 2)

    # Optional notes
    notes = input("\n  Notes (optional, Enter to skip): ").strip()

    record = {
        "id": item["id"],
        "title": item["title"],
        "country": item["country"],
        "year": item.get("year"),
        "period": item.get("period"),
        "medium_norm": item.get("medium_norm"),
        **scores,
        "purificacao_composto": composite,
        "regime_iconocratico": regime,
        "coded_by": coder,
        "coded_at": datetime.now(timezone.utc).isoformat(),
    }
    if notes:
        record["notes"] = notes

    # Show summary
    print(f"\n  ✅ {item['id']}: composite = {composite:.2f}, regime = {regime}")
    return record


def show_status(corpus, coded):
    """Display coding progress summary."""
    total = len(corpus)
    done = len(coded)
    pct = (done / total * 100) if total else 0

    print(f"\n{'=' * 50}")
    print(f"  Purification Coding Progress")
    print(f"{'=' * 50}")
    print(f"  Total items:   {total}")
    print(f"  Coded:         {done} ({pct:.0f}%)")
    print(f"  Remaining:     {total - done}")
    print(f"  Output file:   {OUTPUT_JSONL}")

    if coded:
        composites = [r["purificacao_composto"] for r in coded.values()]
        print(f"\n  Composite stats (coded items):")
        print(f"    Min:  {min(composites):.2f}")
        print(f"    Max:  {max(composites):.2f}")
        print(f"    Mean: {sum(composites) / len(composites):.2f}")

        # By country
        by_country = {}
        for r in coded.values():
            c = r.get("country", "?")
            by_country.setdefault(c, []).append(r["purificacao_composto"])
        print(f"\n  By country:")
        for c in sorted(by_country):
            vals = by_country[c]
            print(f"    {c:15s}  {len(vals):3d} coded  (mean={sum(vals)/len(vals):.2f})")

        # By regime
        by_regime = {}
        for r in coded.values():
            reg = r.get("regime_iconocratico", "?")
            by_regime.setdefault(reg, 0)
            by_regime[reg] += 1
        print(f"\n  By regime:")
        for reg in sorted(by_regime):
            print(f"    {reg:15s}  {by_regime[reg]:3d}")

    print()


def export_csv(corpus, coded):
    """Export merged corpus + purification data to CSV."""
    import csv

    indicator_names = [name for name, _, _ in INDICATORS]
    extra_cols = ["purificacao_composto", "regime_iconocratico", "coded_by", "coded_at", "notes"]

    # Base columns from corpus.
    # support: physical medium type (e.g. "selo", "moeda", "cartaz")
    # url: canonical source URL; thumbnail_url: preview image URL
    # description: detailed item description; citation_abnt: ABNT NBR 6023:2025 citation
    # in_scope: boolean inclusion status; scope_note: rationale for inclusion/exclusion
    base_cols = ["id", "title", "date", "year", "period", "period_norm",
                 "creator", "country", "country_pt", "medium", "medium_norm",
                 "support", "source_archive", "url", "thumbnail_url",
                 "description", "citation_abnt", "motif_str", "tags_str",
                 "in_scope", "scope_note"]

    all_cols = base_cols + indicator_names + extra_cols

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_cols, extrasaction="ignore")
        writer.writeheader()
        for item in corpus:
            row = {k: item.get(k, "") for k in base_cols}
            if item["id"] in coded:
                c = coded[item["id"]]
                for col in indicator_names + extra_cols:
                    row[col] = c.get(col, "")
            writer.writerow(row)

    print(f"  ✅ Exported {len(corpus)} items to {OUTPUT_CSV}")
    coded_count = sum(1 for item in corpus if item["id"] in coded)
    print(f"     ({coded_count} with purification codes, {len(corpus) - coded_count} uncoded)")


def select_sample(coded, n):
    """Generate a stratified random sample of N items for double-coding (IRR)."""
    import random

    if not coded:
        print("  ❌ No coded items found in purification.jsonl")
        sys.exit(1)

    # Group by regime
    by_regime = {}
    for item_id, rec in coded.items():
        regime = rec.get("regime_iconocratico", "unknown")
        by_regime.setdefault(regime, []).append(item_id)

    total = len(coded)
    n = min(n, total)

    print(f"\n  Stratified sample: {n} items from {total} coded")
    print(f"  {'─' * 50}")

    sample = []
    remainder = n
    regimes_sorted = sorted(by_regime.keys(), key=lambda r: len(by_regime[r]), reverse=True)

    for i, regime in enumerate(regimes_sorted):
        pool = by_regime[regime]
        if i == len(regimes_sorted) - 1:
            # last regime gets the remainder
            count = remainder
        else:
            count = max(1, round(n * len(pool) / total))
            count = min(count, len(pool), remainder)
        picked = random.sample(pool, min(count, len(pool)))
        sample.extend(picked)
        remainder -= len(picked)
        print(f"    {regime:20s}  {len(pool):3d} items → {len(picked):2d} sampled")

    random.shuffle(sample)

    print(f"\n  Sample IDs ({len(sample)} items):")
    for item_id in sorted(sample):
        rec = coded[item_id]
        print(f"    {item_id:15s}  regime={rec.get('regime_iconocratico','?'):15s}  "
              f"composto={rec.get('purificacao_composto', 0):.2f}")

    # Save sample list
    sample_path = REPO_ROOT / "data" / "processed" / "irr_sample.json"
    with open(sample_path, "w", encoding="utf-8") as f:
        json.dump({"sample_size": len(sample), "items": sorted(sample),
                    "generated_at": datetime.now(timezone.utc).isoformat()}, f, indent=2)
    print(f"\n  ✅ Sample saved to {sample_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Code purification indicators for Iconocracia corpus items"
    )
    parser.add_argument("--item", help="Code a specific item by ID (e.g. BR-001)")
    parser.add_argument("--batch", help="Code all items matching prefix (e.g. FR, DE)")
    parser.add_argument("--resume", action="store_true",
                        help="Skip already-coded items")
    parser.add_argument("--status", action="store_true",
                        help="Show coding progress and exit")
    parser.add_argument("--export-csv", action="store_true",
                        help="Export merged corpus + purification to CSV")
    parser.add_argument("--coder", default="ana",
                        help="Coder name for audit trail (default: ana)")
    parser.add_argument("--select-sample", type=int, metavar="N",
                        help="Generate stratified random sample of N items for double-coding")
    args = parser.parse_args()

    corpus = load_corpus()
    coded = load_coded()

    if args.status:
        show_status(corpus, coded)
        return

    if args.export_csv:
        export_csv(corpus, coded)
        return

    if args.select_sample:
        select_sample(coded, args.select_sample)
        return

    # Build work queue
    if args.item:
        queue = [item for item in corpus if item["id"] == args.item]
        if not queue:
            print(f"  ❌ Item '{args.item}' not found in corpus")
            sys.exit(1)
    elif args.batch:
        queue = [item for item in corpus if item["id"].startswith(args.batch)]
        if not queue:
            print(f"  ❌ No items matching prefix '{args.batch}'")
            sys.exit(1)
    else:
        queue = corpus

    if args.resume or (not args.item):
        queue = [item for item in queue if item["id"] not in coded]

    if not queue:
        print("  ✅ All items in selection already coded!")
        show_status(corpus, coded)
        return

    print(f"\n  📋 {len(queue)} items to code ({len(coded)} already done)")
    print("  Commands during coding: 0-3 = score, s = skip item, q = quit\n")

    coded_this_session = 0
    for i, item in enumerate(queue):
        print(f"\n  [{i + 1}/{len(queue)}]", end="")
        result = code_item(item, coder=args.coder)
        if result == "quit":
            print(f"\n  👋 Quitting. Coded {coded_this_session} items this session.")
            break
        if result is None:
            print(f"  ⏭  Skipped {item['id']}")
            continue
        save_record(result)
        coded[result["id"]] = result
        coded_this_session += 1

    print(f"\n  Session complete: {coded_this_session} items coded")
    show_status(corpus, coded)


if __name__ == "__main__":
    main()
