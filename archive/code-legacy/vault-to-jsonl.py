#!/usr/bin/env python3
"""
vault-to-jsonl.py — Sync Obsidian vault corpus notes → records.jsonl

Reads all SCOUT-XXX markdown files from vault/01-corpus/candidatos/
(or vault/candidatos/ for backward compatibility), extracts YAML
frontmatter, and writes a master records.jsonl file.

Replaces the planned notion_sync.py in the ICONOCRACY knowledge architecture.

Usage:
    python3 vault-to-jsonl.py                          # default paths
    python3 vault-to-jsonl.py --vault path/to/vault    # custom vault
    python3 vault-to-jsonl.py --output path/to/out.jsonl
    python3 vault-to-jsonl.py --dry-run                # preview, no write
    python3 vault-to-jsonl.py --diff                   # show changes vs existing

Designed for: iconocracy-corpus repo
Author: Ana Vanzin · PPGD/UFSC (generated with Claude, April 2026)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# YAML frontmatter parser (no external dependencies)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter from markdown text.

    Handles the subset of YAML used in Obsidian notes:
    - scalar values (strings, numbers, booleans)
    - lists (both inline [...] and indented - item)
    - quoted and unquoted strings
    """
    match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return None

    raw = match.group(1)
    data = {}
    current_key = None
    current_list = None

    for line in raw.split('\n'):
        # Skip empty lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        # List continuation (indented "- item")
        list_match = re.match(r'^  +- (.+)$', line)
        if list_match and current_key and current_list is not None:
            val = _parse_value(list_match.group(1).strip())
            current_list.append(val)
            data[current_key] = current_list
            continue

        # Key-value pair
        kv_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*?)$', line)
        if kv_match:
            key = kv_match.group(1)
            raw_val = kv_match.group(2).strip()

            if raw_val == '' or raw_val is None:
                # Possibly a list that follows on next lines
                current_key = key
                current_list = []
                data[key] = current_list
            elif raw_val.startswith('[') and raw_val.endswith(']'):
                # Inline list
                items = raw_val[1:-1].split(',')
                data[key] = [_parse_value(i.strip()) for i in items if i.strip()]
                current_key = key
                current_list = None
            else:
                data[key] = _parse_value(raw_val)
                current_key = key
                current_list = None

    return data


def _parse_value(val: str):
    """Parse a single YAML value."""
    if not val:
        return None

    # Remove surrounding quotes
    if (val.startswith('"') and val.endswith('"')) or \
       (val.startswith("'") and val.endswith("'")):
        return val[1:-1]

    # Booleans
    if val.lower() in ('true', 'yes'):
        return True
    if val.lower() in ('false', 'no'):
        return False

    # null
    if val.lower() in ('null', 'none', '~'):
        return None

    # Numbers
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        pass

    # Strip wiki-link syntax from related items
    val = re.sub(r'\[\[([^\]]+)\]\]', r'\1', val)

    return val


# ---------------------------------------------------------------------------
# Corpus record builder
# ---------------------------------------------------------------------------

# Fields to extract from frontmatter → JSON record
RECORD_FIELDS = [
    'id', 'tipo', 'status', 'titulo', 'acervo', 'url', 'url_iiif',
    'data_estimada', 'pais', 'suporte', 'motivo_alegorico',
    'regime', 'endurecimento', 'confianca', 'tags', 'related',
    'data_scout',
]

# Additional fields extracted from note body
BODY_FIELDS = [
    'analise_pre_iconografica',
    'atributos',
    'justificativa_regime',
    'referencia_abnt',
]


def extract_body_fields(text: str) -> dict:
    """Extract structured data from the note body (below frontmatter)."""
    result = {}

    # Pre-iconographic analysis
    pre_ico = re.search(
        r'\*\*Nível pré-iconográfico:\*\*\s*\n(.+?)(?=\n\*\*|\n---)',
        text, re.DOTALL
    )
    if pre_ico:
        result['analise_pre_iconografica'] = pre_ico.group(1).strip()

    # Attributes checklist
    atributos = re.findall(r'- \[([xX ])\] (.+)', text)
    if atributos:
        result['atributos'] = {
            attr.strip(): (check.lower() == 'x')
            for check, attr in atributos
        }

    # Regime justification
    justif = re.search(
        r'\*\*Justificativa:\*\*\s*(.+)',
        text
    )
    if justif:
        result['justificativa_regime'] = justif.group(1).strip()

    # ABNT reference
    abnt = re.search(
        r'\*\*ABNT provisória:\*\*\s*\n(.+?)(?=\n\*\*|\n---|\n$)',
        text, re.DOTALL
    )
    if abnt:
        result['referencia_abnt'] = abnt.group(1).strip()

    return result


def note_to_record(filepath: Path) -> dict | None:
    """Convert a single Obsidian note to a corpus record dict."""
    text = filepath.read_text(encoding='utf-8')

    fm = parse_frontmatter(text)
    if not fm:
        return None

    # Only process corpus candidates
    if fm.get('tipo') not in ('corpus-candidato', 'corpus/candidato'):
        return None

    record = {}
    for field in RECORD_FIELDS:
        if field in fm:
            record[field] = fm[field]

    # Extract body fields
    body = extract_body_fields(text)
    record.update(body)

    # Add metadata
    record['_source_file'] = str(filepath.name)
    record['_synced_at'] = datetime.now().isoformat(timespec='seconds')

    return record


# ---------------------------------------------------------------------------
# Main sync logic
# ---------------------------------------------------------------------------

def find_candidate_notes(vault_path: Path) -> list[Path]:
    """Find all SCOUT-XXX notes in the vault."""
    candidates = []

    # Check both old and new paths
    search_dirs = [
        vault_path / '01-corpus' / 'candidatos',  # new architecture
        vault_path / 'candidatos',                  # legacy path
    ]

    for search_dir in search_dirs:
        if search_dir.is_dir():
            for f in sorted(search_dir.glob('SCOUT-*.md')):
                candidates.append(f)

    # Deduplicate by filename (prefer new path)
    seen = set()
    unique = []
    for c in candidates:
        if c.name not in seen:
            seen.add(c.name)
            unique.append(c)

    return unique


def load_existing_records(output_path: Path) -> dict:
    """Load existing records.jsonl indexed by ID."""
    records = {}
    if output_path.exists():
        for line in output_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line:
                try:
                    rec = json.loads(line)
                    if 'id' in rec:
                        records[rec['id']] = rec
                except json.JSONDecodeError:
                    continue
    return records


def sync(vault_path: Path, output_path: Path, dry_run: bool = False,
         show_diff: bool = False) -> dict:
    """Main sync: vault notes → records.jsonl.

    Returns stats dict.
    """
    notes = find_candidate_notes(vault_path)
    existing = load_existing_records(output_path)

    new_records = {}
    errors = []

    for note_path in notes:
        try:
            record = note_to_record(note_path)
            if record and 'id' in record:
                new_records[record['id']] = record
        except Exception as e:
            errors.append((note_path.name, str(e)))

    # Calculate diff
    added = set(new_records.keys()) - set(existing.keys())
    updated = set()
    unchanged = set()

    for rid in set(new_records.keys()) & set(existing.keys()):
        # Compare without _synced_at
        old = {k: v for k, v in existing[rid].items() if k != '_synced_at'}
        new = {k: v for k, v in new_records[rid].items() if k != '_synced_at'}
        if old != new:
            updated.add(rid)
        else:
            unchanged.add(rid)

    removed = set(existing.keys()) - set(new_records.keys())

    stats = {
        'notes_found': len(notes),
        'records_generated': len(new_records),
        'added': len(added),
        'updated': len(updated),
        'unchanged': len(unchanged),
        'removed_from_jsonl': len(removed),
        'errors': len(errors),
    }

    # Print summary
    print(f"\n{'='*60}")
    print(f"  VAULT → JSONL SYNC")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print(f"  Notes found:       {stats['notes_found']}")
    print(f"  Records generated: {stats['records_generated']}")
    print(f"  Added:             {stats['added']}")
    print(f"  Updated:           {stats['updated']}")
    print(f"  Unchanged:         {stats['unchanged']}")
    print(f"  Removed:           {stats['removed_from_jsonl']}")
    if errors:
        print(f"  Errors:            {stats['errors']}")
        for name, err in errors:
            print(f"    - {name}: {err}")
    print(f"{'='*60}\n")

    if show_diff:
        if added:
            print("  + ADDED:")
            for rid in sorted(added):
                r = new_records[rid]
                print(f"    {rid}: {r.get('titulo', '?')} [{r.get('pais', '?')}]")
        if updated:
            print("  ~ UPDATED:")
            for rid in sorted(updated):
                r = new_records[rid]
                print(f"    {rid}: {r.get('titulo', '?')}")
        if removed:
            print("  - REMOVED from JSONL (note deleted from vault):")
            for rid in sorted(removed):
                print(f"    {rid}")
        print()

    if dry_run:
        print("  [DRY RUN — no files written]\n")
        return stats

    # Write output (only vault-sourced records; removed records stay removed)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        for rid in sorted(new_records.keys()):
            f.write(json.dumps(new_records[rid], ensure_ascii=False) + '\n')

    print(f"  Written to: {output_path}\n")
    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Sync Obsidian vault corpus notes → records.jsonl'
    )
    parser.add_argument(
        '--vault', type=Path, default=Path('vault'),
        help='Path to Obsidian vault directory (default: vault/)'
    )
    parser.add_argument(
        '--output', type=Path, default=Path('data/processed/records.jsonl'),
        help='Path to output JSONL file (default: data/processed/records.jsonl)'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Preview changes without writing'
    )
    parser.add_argument(
        '--diff', action='store_true',
        help='Show detailed diff of changes'
    )

    args = parser.parse_args()

    if not args.vault.is_dir():
        print(f"Error: vault directory not found: {args.vault}", file=sys.stderr)
        sys.exit(1)

    stats = sync(args.vault, args.output, dry_run=args.dry_run, show_diff=args.diff)

    if stats['errors'] > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
