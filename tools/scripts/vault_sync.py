#!/usr/bin/env python3
"""
vault_sync.py — Sincroniza data/processed/records.jsonl ↔ vault/candidatos/ (Obsidian)

Substitui notion_sync.py: o vault Obsidian é o espelho catalográfico canônico.

Uso:
    python tools/scripts/vault_sync.py status          # contagem em ambos os lados
    python tools/scripts/vault_sync.py diff            # diferenças sem escrever
    python tools/scripts/vault_sync.py pull            # vault → records.jsonl (novos itens)
    python tools/scripts/vault_sync.py push            # records.jsonl → vault (novas notas)
    python tools/scripts/vault_sync.py sync            # pull + push (bidirecional)

Formato de frontmatter suportado (vault/candidatos/):
    - BR-001 <título>.md  — notas com id: BR-001 (corpus IDs)
    - SCOUT-NNN <título>.md — notas de busca automática
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS = REPO / "data" / "processed" / "records.jsonl"
VAULT = REPO / "vault" / "candidatos"

# Namespace for deterministic UUIDs (same as csv_to_records.py)
_NS = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
VAULT_BATCH_ID = "00000000-1c0c-4842-8a1a-vaultsync0001"

VALID_REGIMES = {"fundacional", "normativo", "militar", "contra-alegoria"}

# Country code → full name mapping
COUNTRY_NAMES: dict[str, str] = {
    "FR": "France", "BR": "Brazil", "US": "United States",
    "DE": "Germany", "UK": "United Kingdom", "BE": "Belgium",
    "NL": "Netherlands", "PT": "Portugal", "IT": "Italy",
    "AT": "Austria", "ES": "Spain", "CH": "Switzerland",
    "UY": "Uruguay", "MX": "Mexico", "AR": "Argentina",
}

# Corpus ID pattern: XX-NNN or XX-TEXT
CORPUS_ID_RE = re.compile(r"^[A-Z]{2,4}-[A-Z0-9]+$")
# SCOUT ID pattern
SCOUT_ID_RE = re.compile(r"^SCOUT-(\d+)$")
# Characters invalid in filenames (Windows + POSIX common subset)
_INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\[\]]')
# Confidence label → float mapping
_CONFIDENCE_LEVELS = {"alto": 0.85, "medio": 0.65, "baixo": 0.45, "muito-baixo": 0.25}


# ---------------------------------------------------------------------------
# YAML frontmatter parser (minimal, no deps)
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> dict:
    """
    Parse YAML frontmatter between --- delimiters.
    Returns a dict with string/list values (best-effort, no full YAML parser needed).
    """
    fm: dict = {}
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end == -1:
        return fm
    block = text[3:end].strip()

    current_key = None
    current_list: list | None = None

    for line in block.splitlines():
        # List item
        if line.startswith("  - ") or line.startswith("- "):
            item = line.lstrip(" -").strip().strip('"').strip("'")
            if current_list is not None:
                current_list.append(item)
            continue

        # Key: value
        if ":" in line and not line.startswith(" "):
            # Flush previous list
            if current_key and current_list is not None:
                fm[current_key] = current_list

            parts = line.split(":", 1)
            current_key = parts[0].strip()
            val = parts[1].strip().strip('"').strip("'") if len(parts) > 1 else ""

            if val == "":
                # Might be followed by list items
                current_list = []
                fm[current_key] = current_list
            else:
                current_list = None
                fm[current_key] = val

    return fm


# ---------------------------------------------------------------------------
# records.jsonl I/O
# ---------------------------------------------------------------------------

def _load_records() -> list[dict]:
    if not RECORDS.exists():
        return []
    recs = []
    with RECORDS.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    recs.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return recs


def _save_records(recs: list[dict]) -> None:
    RECORDS.parent.mkdir(parents=True, exist_ok=True)
    with RECORDS.open("w", encoding="utf-8") as f:
        for rec in recs:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _records_url_index(recs: list[dict]) -> dict[str, int]:
    """Return {url: index_in_list} for quick lookup."""
    idx: dict[str, int] = {}
    for i, rec in enumerate(recs):
        sr = (rec.get("webscout") or {}).get("search_results") or []
        url = sr[0].get("url", "") if sr else ""
        if url:
            idx[url] = i
    return idx


def _records_title_index(recs: list[dict]) -> dict[str, int]:
    idx: dict[str, int] = {}
    for i, rec in enumerate(recs):
        title = (rec.get("input") or {}).get("title_hint", "").lower()
        if title:
            idx[title] = i
    return idx


# ---------------------------------------------------------------------------
# Vault note scanning
# ---------------------------------------------------------------------------

def _scan_vault_notes() -> list[dict]:
    """Scan vault/candidatos/ and return list of parsed frontmatter dicts."""
    notes = []
    if not VAULT.exists():
        return notes
    for path in sorted(VAULT.iterdir()):
        if path.suffix != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
            fm = _parse_frontmatter(text)
            fm["_file"] = path.name
            fm["_path"] = path
            notes.append(fm)
        except Exception:
            pass
    return notes


def _note_url(fm: dict) -> str:
    return str(fm.get("url") or fm.get("URL") or "").strip()


def _note_title(fm: dict) -> str:
    return str(fm.get("titulo") or fm.get("title") or fm.get("_file", "")).strip()


def _note_id(fm: dict) -> str:
    return str(fm.get("id") or "").strip()


def _note_regime(fm: dict) -> str:
    raw = str(fm.get("regime") or "").lower().strip()
    return raw if raw in VALID_REGIMES else ""


def _note_country(fm: dict) -> str:
    pais = str(fm.get("pais") or "").strip()
    # May be a code like "BR" or a full name
    return COUNTRY_NAMES.get(pais.upper(), pais)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Build master record from vault note
# ---------------------------------------------------------------------------

def _vault_note_to_record(fm: dict) -> dict:
    title = _note_title(fm)
    url = _note_url(fm)
    item_id_str = _note_id(fm) or title

    item_uuid = str(uuid.uuid5(_NS, f"iconocracy-vault-{item_id_str}"))
    hash_src = url if url.startswith("http") else title
    item_hash = hashlib.sha256(hash_src.encode()).hexdigest()

    safe_url = url if url.startswith("http") else f"https://iconocracy.corpus/vault/{item_uuid}"

    # Motifs from tags
    motifs = [
        t.replace("motivo/", "").replace("-", " ").title()
        for t in (fm.get("tags") or [])
        if str(t).startswith("motivo/")
    ]
    if not motifs:
        motifs = [str(fm.get("motivo_alegorico") or "Figura feminina alegórica")]

    # Country / place
    country = _note_country(fm)
    date_str = str(fm.get("data_estimada") or fm.get("periodo") or fm.get("date") or "")

    # Purification
    regime = _note_regime(fm)
    confianca_str = str(fm.get("confianca") or "").lower()
    confidence = _CONFIDENCE_LEVELS.get(confianca_str, 0.5)

    # ABNT citation if present
    abnt = str(fm.get("citation_abnt") or "")

    # Tags
    tags = fm.get("tags") or []
    audit_flags = ["vault-import", "#verificar"] if "#verificar" in str(tags) else ["vault-import"]

    now = _now_iso()

    record: dict = {
        "master_record_version": "1.0",
        "batch_id": VAULT_BATCH_ID,
        "item_id": item_uuid,
        "item_hash": item_hash[:16],
        "input": {
            "input_url": safe_url,
            "title_hint": title,
            "date_hint": date_str,
            "place_hint": country,
        },
        "webscout": {
            "search_results": [
                {
                    "evidence_id": "v1",
                    "source_type": "primary_image",
                    "title": title,
                    "url": safe_url,
                    "abnt_citation": abnt or title,
                    "iconclass_candidates": [],
                    "notes": f"Importado do vault Obsidian: {fm.get('_file', '')}",
                }
            ],
            "summary_evidence": title,
            "gaps": ["descrição detalhada pendente"],
        },
        "iconocode": {
            "pre_iconographic": [{"motif": m, "observed": True} for m in motifs],
            "codes": [],
            "interpretation": [
                {
                    "claim_text": f"Regime iconocrático: {regime.upper()}" if regime else "Regime pendente",
                    "claim_type": "iconographic",
                    "status": "tentative" if not regime else "supported",
                    "confidence": confidence,
                }
            ],
            "validation": {"claim_ledger": []},
            "confidence": confidence,
        },
        "exports": {
            "abnt_citations": [abnt] if abnt else [],
            "audit_flags": audit_flags,
        },
        "timestamps": {
            "created_at": now,
            "updated_at": now,
        },
    }

    if regime:
        record["purificacao"] = {
            "desincorporacao": 0, "rigidez_postural": 0, "dessexualizacao": 0,
            "uniformizacao_facial": 0, "heraldizacao": 0, "enquadramento_arquitetonico": 0,
            "apagamento_narrativo": 0, "monocromatizacao": 0, "serialidade": 0,
            "inscricao_estatal": 0,
            "purificacao_composto": 0.0,
            "regime_iconocratico": regime,
            "coded_by": "vault-import",
            "coded_at": now,
            "notes": "Codificação pendente — importado do vault",
        }

    return record


# ---------------------------------------------------------------------------
# Vault note generator (push direction)
# ---------------------------------------------------------------------------

def _sanitize_filename(title: str, max_len: int = 60) -> str:
    clean = _INVALID_FILENAME_CHARS.sub("", title)
    clean = clean.replace("\n", " ").strip()
    if len(clean) > max_len:
        clean = clean[:max_len].rsplit(" ", 1)[0]
    return clean.strip(". ")


def _next_scout_id() -> int:
    max_id = 0
    if VAULT.exists():
        for f in VAULT.iterdir():
            m = re.match(r"SCOUT-(\d+)", f.name)
            if m:
                n = int(m.group(1))
                if n > max_id:
                    max_id = n
    return max_id + 1


def _record_to_vault_note(record: dict, note_id: str) -> str:
    """Generate an Obsidian note from a master record."""
    inp = record.get("input", {})
    title = inp.get("title_hint") or "Sem título"
    url = inp.get("input_url", "")
    date_str = inp.get("date_hint", "")
    country = inp.get("place_hint", "")

    sr = (record.get("webscout") or {}).get("search_results") or [{}]
    abnt = (record.get("exports") or {}).get("abnt_citations") or []
    abnt_str = abnt[0] if abnt else title

    # Motifs
    motifs = [
        m.get("motif", "")
        for m in (record.get("iconocode") or {}).get("pre_iconographic", [])
        if m.get("observed", True)
    ]

    # Regime
    purif = record.get("purificacao") or {}
    regime = purif.get("regime_iconocratico", "").upper() or "INDETERMINADO"

    # Country code
    cc = next((k for k, v in COUNTRY_NAMES.items() if v == country), country[:2].upper())

    # Tags
    tags = ["corpus/candidato"]
    if cc:
        tags.append(f"pais/{cc}")
    if regime.lower() in VALID_REGIMES:
        tags.append(f"regime/{regime.lower()}")
    tags.append("#verificar")

    tags_yaml = "\n".join(f"  - {t}" for t in tags)
    today = date.today().isoformat()
    record_ts = record.get("timestamps", {}).get("created_at", today)

    frontmatter = f"""---
id: {note_id}
tipo: corpus/candidato
status: candidato
titulo: "{title}"
url: "{url}"
data_estimada: "{date_str}"
pais: {cc}
regime: {regime}
confianca: baixo
tags:
{tags_yaml}
related:
  - "[[ENDURECIMENTO]]"
  - "[[Feminilidade de Estado]]"
data_scout: {today}
records_item_id: {record.get('item_id', '')}
---"""

    motifs_str = ", ".join(motifs) if motifs else "Alegoria feminina"
    body = f"""
## {title}

### Identificação
**Data**: {date_str} | **País**: {cc} | **Regime**: {regime}
**URL**: [link]({url})

**Motivos identificados**: {motifs_str}

### Análise preliminar de ENDURECIMENTO
**Regime preliminar**: {regime}

*Análise gerada automaticamente a partir de records.jsonl. Requer validação visual.*

### Citação ABNT
{abnt_str}

### Proveniência
Nota gerada por `vault_sync.py push` em {today}.
Registro canônico: `data/processed/records.jsonl` item_id `{record.get('item_id', '')}`.

> **#verificar**: Esta nota requer validação visual e confirmação de escopo.
"""

    return frontmatter + body


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status() -> None:
    records = _load_records()
    notes = _scan_vault_notes()

    # Classify vault notes
    with_corpus_id = [n for n in notes if CORPUS_ID_RE.match(_note_id(n))]
    scout_notes = [n for n in notes if SCOUT_ID_RE.match(_note_id(n))]

    print(f"records.jsonl:           {len(records)} registros")
    print(f"vault/candidatos/:       {len(notes)} notas (.md)")
    print(f"  com corpus ID (XX-NNN): {len(with_corpus_id)}")
    print(f"  SCOUT-NNN:              {len(scout_notes)}")
    print(f"  outros:                 {len(notes) - len(with_corpus_id) - len(scout_notes)}")


def cmd_diff() -> None:
    records = _load_records()
    notes = _scan_vault_notes()

    rec_urls = {
        (rec.get("webscout") or {}).get("search_results", [{}])[0].get("url", "")
        for rec in records
    }
    vault_urls = {_note_url(n) for n in notes if _note_url(n)}

    only_records = rec_urls - vault_urls - {""}
    only_vault = vault_urls - rec_urls

    rec_titles = {
        (rec.get("input") or {}).get("title_hint", "").lower()
        for rec in records
    }
    vault_titles = {_note_title(n).lower() for n in notes}

    only_records_title = {
        (rec.get("input") or {}).get("title_hint", "")
        for rec in records
        if (rec.get("input") or {}).get("title_hint", "").lower() not in vault_titles
    } - {""}

    print(f"records.jsonl: {len(records)} | vault: {len(notes)}")
    print()

    if only_records:
        print(f"Apenas em records.jsonl (por URL) — {len(only_records)}:")
        for url in sorted(only_records)[:10]:
            print(f"  + {url[:80]}")
        if len(only_records) > 10:
            print(f"  ... e mais {len(only_records) - 10}")
    else:
        print("Sem itens exclusivos em records.jsonl (por URL).")

    if only_vault:
        print(f"\nApenas no vault (por URL) — {len(only_vault)}:")
        for url in sorted(only_vault)[:10]:
            note = next((n for n in notes if _note_url(n) == url), {})
            print(f"  - [{note.get('_file', '?')}] {url[:60]}")
        if len(only_vault) > 10:
            print(f"  ... e mais {len(only_vault) - 10}")
    else:
        print("Sem itens exclusivos no vault (por URL).")

    print(f"\nItens em records.jsonl sem nota vault (por título): {len(only_records_title)}")


def cmd_pull(dry_run: bool = False) -> None:
    """Pull: vault notes → records.jsonl (add new items not already in records)."""
    records = _load_records()
    url_idx = _records_url_index(records)
    title_idx = _records_title_index(records)
    notes = _scan_vault_notes()

    added = 0
    for note in notes:
        url = _note_url(note)
        title = _note_title(note).lower()

        # Skip if already in records
        if url and url in url_idx:
            continue
        if title and title in title_idx:
            continue

        # Only import notes that have a verifiable anchor:
        # - a corpus-style ID (BR-001, FR-013, etc.) ensures traceability to corpus, OR
        # - a URL provides direct evidence linkage.
        # SCOUT-NNN notes without either are speculative candidates only — skip.
        note_id = _note_id(note)
        has_corpus_id = CORPUS_ID_RE.match(note_id)
        has_url = bool(url)

        if not has_corpus_id and not has_url:
            continue  # no anchor — skip speculative SCOUT note

        rec = _vault_note_to_record(note)
        if dry_run:
            print(f"  [DRY-RUN] Pull: {note.get('_file', '')} → records.jsonl")
        else:
            records.append(rec)
            added += 1
            print(f"  PULL: {note.get('_file', '')} → item_id={rec['item_id'][:8]}…")

    if not dry_run:
        if added:
            _save_records(records)
            print(f"\nAdicionados {added} registros de records.jsonl. Total: {len(records)}")
        else:
            print("Nenhum item novo no vault.")
    else:
        print(f"\n[DRY-RUN] Importaria {added} notas para records.jsonl.")


def cmd_push(dry_run: bool = False) -> None:
    """Push: records.jsonl → vault notes (create notes for items without one)."""
    records = _load_records()
    notes = _scan_vault_notes()

    vault_urls = {_note_url(n) for n in notes if _note_url(n)}
    vault_titles_lower = {_note_title(n).lower() for n in notes}

    next_id = _next_scout_id()
    pushed = 0

    for rec in records:
        inp = rec.get("input") or {}
        url = inp.get("input_url", "")
        title = inp.get("title_hint", "")

        # Skip placeholder URLs — no point creating notes for these
        if url.startswith("https://iconocracy.corpus/placeholder/"):
            continue
        if url in vault_urls:
            continue
        if title.lower() in vault_titles_lower:
            continue

        # Use corpus ID from records item_id hint if available (from migration batch)
        # For vault-imported records the note_id would be SCOUT-NNN
        note_id = f"SCOUT-{next_id + pushed}"
        safe_title = _sanitize_filename(title)
        filename = f"{note_id} {safe_title}.md"
        filepath = VAULT / filename

        note_content = _record_to_vault_note(rec, note_id)

        if dry_run:
            print(f"  [DRY-RUN] Push: records item → {filename}")
        else:
            VAULT.mkdir(parents=True, exist_ok=True)
            filepath.write_text(note_content, encoding="utf-8")
            print(f"  PUSH: {filename}")

        pushed += 1

    if not dry_run:
        if pushed:
            print(f"\nCriadas {pushed} notas no vault.")
        else:
            print("Nenhuma nota nova para criar no vault.")
    else:
        print(f"\n[DRY-RUN] Criaria {pushed} notas no vault.")


def cmd_sync(dry_run: bool = False) -> None:
    """Bidirectional sync: pull then push."""
    print("=== PULL (vault → records.jsonl) ===")
    cmd_pull(dry_run=dry_run)
    print("\n=== PUSH (records.jsonl → vault) ===")
    cmd_push(dry_run=dry_run)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sincroniza records.jsonl ↔ vault/candidatos/ (Obsidian)"
    )
    parser.add_argument(
        "command",
        choices=["status", "diff", "pull", "push", "sync"],
        help="Comando a executar",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview sem escrever arquivos",
    )
    args = parser.parse_args()

    cmds = {
        "status": lambda: cmd_status(),
        "diff": lambda: cmd_diff(),
        "pull": lambda: cmd_pull(dry_run=args.dry_run),
        "push": lambda: cmd_push(dry_run=args.dry_run),
        "sync": lambda: cmd_sync(dry_run=args.dry_run),
    }
    cmds[args.command]()


if __name__ == "__main__":
    main()
