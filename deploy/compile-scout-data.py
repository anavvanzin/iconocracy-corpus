#!/usr/bin/env python3
"""Extract SCOUT candidates and Zwischenraume from vault notes into JSON for Cloudflare deploy."""
import json, re, sys
from pathlib import Path

vault_dirs = [
    Path("/Users/ana/iconocracy-corpus/vault/corpus/scout-session-2026-03-28"),
    Path("/Users/ana/iconocracy-corpus/vault/corpus/scout-session-2026-03-29"),
]

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
    # Split by --- separators that mark new frontmatter blocks
    blocks = re.split(r'\n---\n(?=id:\s*SCOUT)', text)
    for block in blocks:
        if not block.strip():
            continue
        # Try to find id and tipo
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
            # Extract ENDURECIMENTO
            end_m = re.search(r'ENDURECIMENTO detectado:\s*(.+?)(?:\n|$)', block)
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

candidates = []
zwischenraume = []
seen_ids = set()

for vault_dir in vault_dirs:
    if not vault_dir.exists():
        continue
    for f in sorted(vault_dir.glob("*.md")):
        text = f.read_text(encoding='utf-8')
        fm = parse_frontmatter(text)

        # Single-note files (from day 1 saved notes)
        if fm.get('id', '').startswith('SCOUT-') and fm.get('id') not in seen_ids:
            seen_ids.add(fm['id'])
            entry = {k: v for k, v in fm.items() if k in [
                'id', 'tipo', 'titulo', 'acervo', 'url', 'data_estimada',
                'pais', 'suporte', 'motivo_alegorico', 'regime', 'confianca', 'periodo'
            ]}
            # Extract ENDURECIMENTO from body
            end_m = re.search(r'ENDURECIMENTO detectado:\*\*\s*(.+?)(?:\n|$)', text)
            if not end_m:
                end_m = re.search(r'ENDURECIMENTO detectado:\s*(.+?)(?:\n|$)', text)
            if end_m:
                entry['endurecimento'] = end_m.group(1).strip()
            # Extract justificativa
            just_m = re.search(r'\*\*Justificativa:\*\*\s*(.+?)(?:\n\n|\n\*\*)', text, re.DOTALL)
            if just_m:
                entry['justificativa'] = just_m.group(1).strip()[:300]

            if fm.get('tipo') == 'corpus-zwischenraum':
                zwischenraume.append(entry)
            elif fm.get('tipo') == 'corpus-candidato':
                candidates.append(entry)

        # Composite files (agent outputs with multiple notes embedded)
        if not fm.get('id', '').startswith('SCOUT-'):
            entries = extract_from_composite(text)
            for entry in entries:
                if entry['id'] not in seen_ids:
                    seen_ids.add(entry['id'])
                    if 'zwischenraum' in entry.get('tipo', ''):
                        zwischenraume.append(entry)
                    elif 'candidato' in entry.get('tipo', '') or 'controle' in entry.get('tipo', ''):
                        candidates.append(entry)

data = {
    "session": "2026-03-28 / 2026-03-29",
    "title": "CORPUS SCOUT — Campanhas de Pesquisa Iconografica",
    "thesis": "ICONOCRACY: Alegoria Feminina na Historia da Cultura Juridica (Sec. XIX-XX)",
    "total_candidates": len(candidates),
    "total_zwischenraume": len(zwischenraume),
    "candidates": candidates,
    "zwischenraume": zwischenraume,
    "theoretical_contributions": [
        {"name": "Anti-ENDURECIMENTO", "desc": "Regime collapse reverses purification. Three paths: phantom persistence, satirical reversal, weaponization."},
        {"name": "ENDURECIMENTO negativo", "desc": "Hardening by subtraction (post-1945 Marianne removes body, cap, movement)."},
        {"name": "ENDURECIMENTO positivo", "desc": "Hardening by addition (armor, fasces, trident)."},
        {"name": "Captura transnacional", "desc": "Enemy seizes and inverts your allegory (Goetz capturing Marianne)."},
        {"name": "Dissolucao heraldica", "desc": "ENDURECIMENTO terminus where the female body disappears entirely into heraldic residue (Belgian coins)."},
        {"name": "Principio da redundancia", "desc": "Where the courthouse exists in stone, Justitia vanishes from money (Notgeld tribunal cities)."},
        {"name": "Indigenizacao", "desc": "Colonial alternative to ENDURECIMENTO: replace European allegorical body with racialized indigenous body (French colonial stamps)."},
        {"name": "Gradiente de transparencia da violencia imperial", "desc": "Olive branch (US) -> fasces (FR) -> trident (UK). Three levels of honesty about what the female body sanctions."},
        {"name": "Ausencia pre-modelo vs. pos-modelo", "desc": "Two types of absent female allegory: Mexico (1824, pre-model — did not know the European pattern) vs. Japan (1875, post-model — knew and consciously rejected). Japan copied metal, weight, fineness and English inscriptions but rejected the female body. Strongest cultural delimitation argument."},
        {"name": "ENDURECIMENTO sinconico e comparativo", "desc": "ENDURECIMENTO is not only diachronic: UK militarizes by addition (Britannia armed, seahorse chariot), France pastoralaizes by subtraction (Semeuse removes political attributes) — two synchronic modes of neutralizing the female allegorical body (1903-1913)."},
        {"name": "Numen mixtum", "desc": "Deliberate iconographic fusion of two deities into a single normalized legal type (Themis + Minerva in Belgian court sculpture, documented by Huygebaert 2019). Maps onto purification indicators uniformizacao_facial and apagamento_narrativo."},
    ]
}

out = Path("/Users/ana/iconocracy-corpus/deploy/scout-data.json")
out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
print(f"Compiled {len(candidates)} candidates + {len(zwischenraume)} zwischenraume -> {out}")
