#!/usr/bin/env python3
"""Extract SCOUT candidates and Zwischenraume from vault notes into JSON for Cloudflare deploy.

This script scans both vault/candidatos and vault/corpus/scout-session-* directories,
normalizes individual and composite entries, checks their promotion status against the
canonical records.jsonl ledger, and exports a unified scout-data.json to both the deploy
root and the companion worker src directory.
"""
import json
import re
from pathlib import Path

# Reconstruct relative to script directory
REPO_ROOT = Path(__file__).resolve().parent.parent
CANDIDATOS_DIR = REPO_ROOT / "vault" / "candidatos"
CORPUS_DIR = REPO_ROOT / "vault" / "corpus"
RECORDS_PATH = REPO_ROOT / "data" / "processed" / "records.jsonl"
MAPPING_FILE = REPO_ROOT / "data" / "processed" / "id-mapping.json"

OUT_DEPLOY = REPO_ROOT / "deploy" / "scout-data.json"
OUT_COMPANION = REPO_ROOT / "deploy" / "iconocracia-companion" / "src" / "scout-data.json"

def parse_frontmatter(text):
    """Extract YAML-like frontmatter between --- markers."""
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('-') and not line.startswith('#'):
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val:
                fm[key] = val
    return fm

def extract_from_composite(text):
    """Extract multiple SCOUT entries from composite files (agent outputs with multiple notes)."""
    entries = []
    # Split by --- separators that mark new frontmatter blocks starting with id: SCOUT
    blocks = re.split(r'\n---\n(?=id:\s*(?:SCOUT|[A-Z]{2}-))', text)
    for block in blocks:
        if not block.strip():
            continue
        id_m = re.search(r'^id:\s*(.+)', block, re.MULTILINE)
        tipo_m = re.search(r'^tipo:\s*(.+)', block, re.MULTILINE)
        titulo_m = re.search(r'^titulo:\s*["\']?(.+?)["\']?\s*$', block, re.MULTILINE)
        if id_m and tipo_m:
            entry = {
                'id': id_m.group(1).strip(),
                'tipo': tipo_m.group(1).strip(),
                'titulo': titulo_m.group(1).strip() if titulo_m else '',
            }
            for field in ['pais', 'data_estimada', 'suporte', 'motivo_alegorico', 'regime', 'confianca', 'url', 'acervo', 'periodo']:
                m = re.search(rf'^{field}:\s*["\']?(.+?)["\']?\s*$', block, re.MULTILINE)
                if m:
                    entry[field] = m.group(1).strip()
            # Extract endurecimento
            end_m = re.search(r'endurecimento detectado:\s*(.+?)(?:\n|$)', block)
            if not end_m:
                end_m = re.search(r'endurecimento_detectado:\s*["\']?(.+?)["\']?(?:\n|$)', block)
            if end_m:
                entry['endurecimento'] = end_m.group(1).strip()
            # Extract justificativa
            just_m = re.search(r'\*\*Justificativa:\*\*\s*(.+?)(?:\n\n|\n\*\*)', block, re.DOTALL)
            if not just_m:
                just_m = re.search(r'"justificativa_relevancia":\s*"(.+?)"', block)
            if just_m:
                entry['justificativa'] = just_m.group(1).strip()[:300]
            entries.append(entry)
    return entries

def main():
    # Load promoted records to cross-reference
    promoted_uuids = set()
    if RECORDS_PATH.exists():
        with open(RECORDS_PATH, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    if rec and "item_id" in rec:
                        promoted_uuids.add(rec["item_id"])
                except Exception:
                    pass

    # Load ID mapping to resolve UUID from legacy id
    id_mapping = {}
    if MAPPING_FILE.exists():
        with open(MAPPING_FILE, encoding='utf-8') as f:
            try:
                mapping_data = json.load(f)
                for entry in mapping_data.get("mapping", []):
                    c_id = entry.get("corpus_id")
                    item_id = entry.get("item_id")
                    if c_id and item_id:
                        id_mapping[c_id] = item_id
            except Exception:
                pass

    candidates = []
    zwischenraume = []
    seen_ids = set()

    # Define directories to scan
    vault_dirs = [CANDIDATOS_DIR]
    if CORPUS_DIR.exists():
        for sd in CORPUS_DIR.glob("scout-session-*"):
            if sd.is_dir():
                vault_dirs.append(sd)

    for vault_dir in vault_dirs:
        if not vault_dir.exists():
            continue
        for f in sorted(vault_dir.glob("*.md"), key=lambda x: x.name.lower()):
            text = f.read_text(encoding='utf-8')
            fm = parse_frontmatter(text)
            cid = fm.get('id') or f.stem

            if not cid:
                continue

            # Process single-note candidate file
            if cid not in seen_ids:
                seen_ids.add(cid)
                entry = {k: v for k, v in fm.items() if k in [
                    'id', 'tipo', 'titulo', 'acervo', 'url', 'data_estimada',
                    'pais', 'suporte', 'motivo_alegorico', 'regime', 'confianca', 'periodo'
                ]}
                
                # Check title / period synonyms
                if not entry.get('titulo') and fm.get('title'):
                    entry['titulo'] = fm.get('title')
                if not entry.get('titulo'):
                    entry['titulo'] = f.stem
                if not entry.get('data_estimada') and fm.get('periodo'):
                    entry['data_estimada'] = fm.get('periodo')

                # Extract indicators
                end_m = re.search(r'endurecimento detectado:\*\*\s*(.+?)(?:\n|$)', text)
                if not end_m:
                    end_m = re.search(r'endurecimento detectado:\s*(.+?)(?:\n|$)', text)
                if end_m:
                    entry['endurecimento'] = end_m.group(1).strip()
                else:
                    entry['endurecimento'] = fm.get('endurecimento', '')

                just_m = re.search(r'\*\*Justificativa:\*\*\s*(.+?)(?:\n\n|\n\*\*)', text, re.DOTALL)
                if just_m:
                    entry['justificativa'] = just_m.group(1).strip()[:300]
                else:
                    entry['justificativa'] = fm.get('justificativa', '')

                # Determine promotion status
                rec_uuid = fm.get("records_item_id") or id_mapping.get(cid)
                entry["promoted"] = "YES" if rec_uuid and rec_uuid in promoted_uuids else ""

                tipo_lower = str(fm.get('tipo', '')).lower()
                if 'zwischenraum' in tipo_lower or 'painel' in tipo_lower:
                    zwischenraume.append(entry)
                else:
                    candidates.append(entry)

            # Composite files (if no id exists or ID is not in frontmatter, but has multiple SCOUTs)
            if not fm.get('id'):
                entries = extract_from_composite(text)
                for entry in entries:
                    if entry['id'] not in seen_ids:
                        seen_ids.add(entry['id'])
                        
                        rec_uuid = id_mapping.get(entry['id'])
                        entry["promoted"] = "YES" if rec_uuid and rec_uuid in promoted_uuids else ""
                        
                        if 'zwischenraum' in entry.get('tipo', ''):
                            zwischenraume.append(entry)
                        elif 'candidato' in entry.get('tipo', '') or 'controle' in entry.get('tipo', ''):
                            candidates.append(entry)

    data = {
        "session": "2026-03-28 — 2026-04-01",
        "title": "CORPUS SCOUT — Campanhas de Pesquisa Iconografica",
        "thesis": "ICONOCRACY: Alegoria Feminina na Historia da Cultura Juridica (Sec. XIX-XX)",
        "total_candidates": len(candidates),
        "total_zwischenraume": len(zwischenraume),
        "candidates": candidates,
        "zwischenraume": zwischenraume,
        "theoretical_contributions": [
            {"name": "Anti-endurecimento", "desc": "Regime collapse reverses purification. Three paths: phantom persistence, satirical reversal, weaponization."},
            {"name": "endurecimento negativo", "desc": "endurecimento by subtraction (post-1945 Marianne removes body, cap, movement)."},
            {"name": "endurecimento positivo", "desc": "endurecimento by addition (armor, fasces, trident)."},
            {"name": "Captura transnacional", "desc": "Enemy seizes and inverts your allegory (Goetz capturing Marianne)."},
            {"name": "Dissolucao heraldica", "desc": "endurecimento terminus where the female body disappears entirely into heraldic residue (Belgian coins)."},
            {"name": "Principio da redundancia", "desc": "Where the courthouse exists in stone, Justitia vanishes from money (Notgeld tribunal cities)."},
            {"name": "Indigenizacao", "desc": "Colonial alternative to endurecimento: replace European allegorical body with racialized indigenous body (French colonial stamps)."},
            {"name": "Gradiente de transparencia da violencia imperial", "desc": "Olive branch (US) -> fasces (FR) -> trident (UK). Three levels of honesty about what the female body sanctions."},
            {"name": "Ausencia pre-modelo vs. pos-modelo", "desc": "Two types of absent female allegory: Mexico (1824, pre-model — did not know the European pattern) vs. Japan (1875, post-model — knew and consciously rejected). Japan copied metal, weight, fineness and English inscriptions but rejected the female body. Strongest cultural delimitation argument."},
            {"name": "endurecimento sinconico e comparativo", "desc": "endurecimento is not only diachronic: UK militarizes by addition (Britannia armed, seahorse chariot), France pastoralaizes by subtraction (Semeuse removes political attributes) — two synchronic modes of neutralizing the female allegorical body (1903-1913)."},
            {"name": "Numen mixtum", "desc": "Deliberate iconographic fusion of two deities into a single normalized legal type (Themis + Minerva in Belgian court sculpture, documented by Huygebaert 2019). Maps onto purification indicators uniformizacao_facial and apagamento_narrativo."},
        ]
    }

    # Write deploy output
    OUT_DEPLOY.parent.mkdir(parents=True, exist_ok=True)
    OUT_DEPLOY.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding='utf-8')
    print(f"Compiled {len(candidates)} candidates + {len(zwischenraume)} zwischenraume -> {OUT_DEPLOY}")

    # Write companion src output
    OUT_COMPANION.parent.mkdir(parents=True, exist_ok=True)
    OUT_COMPANION.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding='utf-8')
    print(f"Compiled {len(candidates)} candidates + {len(zwischenraume)} zwischenraume -> {OUT_COMPANION}")

if __name__ == "__main__":
    main()
