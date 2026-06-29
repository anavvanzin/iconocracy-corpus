#!/usr/bin/env python3
"""
scout_notes.py — Generate SCOUT Obsidian notes from hunt candidates.

Reads hunt.py output (JSON array from stdin or file) and generates
atomic SCOUT notes in vault/candidatos/ for candidates above a
score threshold.

Usage:
    python hunt.py --country FR --limit 20 | python scout_notes.py
    python scout_notes.py --input candidates.json --min-score 0.7
    python scout_notes.py --input candidates.json --dry-run
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

VAULT_PATH = Path(__file__).resolve().parents[2] / "vault" / "candidatos"

# Country code mapping
COUNTRY_CODE = {
    "France": "FR", "United Kingdom": "UK", "Germany": "DE",
    "United States": "US", "Belgium": "BE", "Brazil": "BR",
}

# Motif → tag mapping
MOTIF_TAGS = {
    "Marianne": "motivo/marianne",
    "Semeuse": "motivo/marianne",
    "Britannia": "motivo/britannia",
    "Columbia": "motivo/columbia",
    "Seated Liberty": "motivo/columbia",
    "Standing Liberty": "motivo/columbia",
    "Walking Liberty": "motivo/columbia",
    "Liberty": "motivo/columbia",
    "Germania": "motivo/germania",
    "Belgique": "motivo/belgique",
    "Belgica": "motivo/belgique",
    "Justitia": "motivo/justitia",
    "Justice": "motivo/justitia",
    "Republic": "motivo/republica",
    "Republic": "motivo/republica",
    "République": "motivo/republica",
    "República": "motivo/republica",
    "Minerva": "motivo/justitia",
    "Athena": "motivo/justitia",
    "Ceres": "motivo/republica",
    "Fortuna": "motivo/republica",
}

# Support → tag mapping
SUPPORT_TAGS = {
    "moeda": "suporte/moeda",
    "selo": "suporte/selo",
    "monumento": "suporte/monumento",
    "estampa": "suporte/estampa",
    "frontispicio": "suporte/frontispicio",
    "papel-moeda": "suporte/papel-moeda",
    "cartaz": "suporte/cartaz",
    "medalha": "suporte/moeda",
}

# Regime → tag mapping
REGIME_TAGS = {
    "fundacional": "regime/fundacional",
    "normativo": "regime/normativo",
    "militar": "regime/militar",
}


def find_next_scout_id(vault_path):
    """Scan vault/candidatos/ for highest SCOUT-NNN and return next."""
    max_id = 322  # known baseline
    if vault_path.exists():
        for f in vault_path.iterdir():
            m = re.match(r"SCOUT-(\d+)", f.name)
            if m:
                n = int(m.group(1))
                if n > max_id:
                    max_id = n
    return max_id + 1


def sanitize_filename(title, max_len=60):
    """Clean title for use as filename."""
    # Remove problematic chars
    clean = re.sub(r'[<>:"/\\|?*\[\]]', '', title)
    clean = clean.replace('\n', ' ').strip()
    if len(clean) > max_len:
        clean = clean[:max_len].rsplit(' ', 1)[0]
    return clean.strip('. ')


def build_tags(candidate):
    """Build YAML tag list from candidate data."""
    tags = ["corpus/candidato"]

    # Country tag
    country = candidate.get("country", "")
    cc = COUNTRY_CODE.get(country, "")
    if cc:
        tags.append(f"pais/{cc}")

    # Support tag
    support = candidate.get("support")
    if support and support in SUPPORT_TAGS:
        tags.append(SUPPORT_TAGS[support])

    # Regime tag
    regime = candidate.get("regime")
    if regime and regime in REGIME_TAGS:
        tags.append(REGIME_TAGS[regime])

    # Motif tags (dedup)
    seen_motif_tags = set()
    for motif in candidate.get("motif", []):
        tag = MOTIF_TAGS.get(motif)
        if tag and tag not in seen_motif_tags:
            tags.append(tag)
            seen_motif_tags.add(tag)

    # Verification tag
    tags.append("#verificar")

    # Hunt-specific
    tags.append("hunt-candidate")

    return tags


def format_regime_analysis(candidate):
    """Generate a preliminary endurecimento assessment."""
    regime = candidate.get("regime")
    support = candidate.get("support")
    motifs = candidate.get("motif", [])
    score = candidate.get("hunt_score", 0)

    if not regime:
        return "**Regime**: indeterminado — requer análise visual.\n**endurecimento**: pendente — sem acesso à imagem."

    regime_upper = regime.upper()
    lines = [f"**Regime preliminar**: {regime_upper}"]

    if regime == "fundacional":
        lines.append("Indicadores esperados: corpo dinâmico, seminudez, atributos revolucionários.")
        lines.append("endurecimento esperado: BAIXO (corpo ainda vivo, narrativo).")
    elif regime == "normativo":
        lines.append("Indicadores esperados: pose estática/frontal, drapeado pesado, serialidade.")
        lines.append("endurecimento esperado: MÉDIO a ALTO (corpo institucionalizado).")
    elif regime == "militar":
        lines.append("Indicadores esperados: armadura, capacete, escudo, rigidez extrema.")
        lines.append("endurecimento esperado: ALTO (corpo blindado/petrificado).")

    lines.append("")
    lines.append("*Classificação preliminar baseada em metadados textuais. Requer confirmação visual.*")

    return "\n".join(lines)


def generate_note(candidate, scout_id):
    """Generate a full SCOUT Obsidian note as a string."""
    title = candidate.get("title", "Sem título")
    country = candidate.get("country", "")
    cc = COUNTRY_CODE.get(country, "")
    date_str = candidate.get("date", "")
    creator = candidate.get("creator", "")
    institution = candidate.get("institution", "")
    url = candidate.get("url", "")
    support = candidate.get("support", "")
    regime = candidate.get("regime", "")
    motifs = candidate.get("motif", [])
    description = candidate.get("description", "")
    rights = candidate.get("rights", "")
    hunt_score = candidate.get("hunt_score", 0)
    hunt_source = candidate.get("hunt_source", "")
    citation = candidate.get("citation_abnt", "")
    thumbnail = candidate.get("thumbnail_url", "")

    tags = build_tags(candidate)

    # Primary motif for frontmatter
    primary_motif = motifs[0] if motifs else "Alegoria feminina"

    # Confidence based on score
    if hunt_score >= 0.8:
        confianca = "medio"
    elif hunt_score >= 0.5:
        confianca = "baixo"
    else:
        confianca = "muito-baixo"

    # Build YAML frontmatter
    tags_yaml = "\n".join(f'  - {t}' for t in tags)
    related_yaml = '  - "[[endurecimento]]"\n  - "[[Feminilidade de Estado]]"'

    frontmatter = f"""---
id: SCOUT-{scout_id}
tipo: corpus-candidato
status: candidato
titulo: "{title}"
acervo: "{institution}"
url: "{url}"
data_estimada: "{date_str}"
pais: {cc}
suporte: {support or 'indeterminado'}
motivo_alegorico: "{primary_motif}"
regime: {regime.upper() if regime else 'INDETERMINADO'}
confianca: {confianca}
tags:
{tags_yaml}
related:
{related_yaml}
hunt_score: {hunt_score}
hunt_source: {hunt_source}
data_scout: {date.today()}
---"""

    # Build body
    body_parts = []

    # Title section
    body_parts.append(f"## {title}")
    body_parts.append("")

    # Identification
    body_parts.append("### Identificação")
    if creator:
        body_parts.append(f"**Criador/Gravador**: {creator}")
    body_parts.append(f"**Acervo**: {institution}")
    if url:
        body_parts.append(f"**URL**: [link]({url})")
    body_parts.append(f"**Data**: {date_str or 'indeterminada'} | **País**: {cc or country} | **Suporte**: {support or 'indeterminado'}")
    if thumbnail:
        body_parts.append(f"**Thumbnail**: [imagem]({thumbnail})")
    if rights:
        body_parts.append(f"**Direitos**: {rights}")
    body_parts.append("")

    # Description
    if description:
        body_parts.append("### Descrição")
        body_parts.append(description)
        body_parts.append("")

    # Motifs
    if motifs:
        body_parts.append(f"**Motivos identificados**: {', '.join(motifs)}")
        body_parts.append("")

    # Regime analysis
    body_parts.append("### Análise preliminar de endurecimento")
    body_parts.append(format_regime_analysis(candidate))
    body_parts.append("")

    # Citation
    if citation:
        body_parts.append("### Citação ABNT")
        body_parts.append(citation)
        body_parts.append("")

    # Provenance
    body_parts.append("### Proveniência")
    body_parts.append(f"Candidato gerado automaticamente por `hunt.py` via {hunt_source}.")
    body_parts.append(f"Score de relevância: **{hunt_score}** | Data: {date.today()}")
    body_parts.append("")
    body_parts.append("> **#verificar**: Esta nota requer validação visual e confirmação de escopo pela pesquisadora.")

    return frontmatter + "\n\n" + "\n".join(body_parts) + "\n"


def log(msg):
    print(msg, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Generate SCOUT Obsidian notes from hunt candidates"
    )
    parser.add_argument("--input", type=str, default=None,
                        help="Path to JSON file with candidates (default: stdin)")
    parser.add_argument("--min-score", type=float, default=0.5,
                        help="Minimum hunt_score to generate a note (default: 0.5)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be generated without writing files")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max notes to generate")

    args = parser.parse_args()

    # Load candidates
    if args.input:
        with open(args.input, encoding="utf-8") as f:
            candidates = json.load(f)
    else:
        candidates = json.load(sys.stdin)

    if not isinstance(candidates, list):
        log("ERROR: Expected JSON array of candidates")
        sys.exit(1)

    # Filter by score
    eligible = [c for c in candidates if c.get("hunt_score", 0) >= args.min_score]
    eligible.sort(key=lambda c: -c.get("hunt_score", 0))

    if args.limit:
        eligible = eligible[:args.limit]

    log(f"Candidates loaded: {len(candidates)}")
    log(f"Above score {args.min_score}: {len(eligible)}")

    if not eligible:
        log("No candidates above threshold.")
        return

    # Find next SCOUT ID
    next_id = find_next_scout_id(VAULT_PATH)
    log(f"Starting SCOUT ID: {next_id}")

    generated = 0
    for candidate in eligible:
        scout_id = next_id + generated
        title = candidate.get("title", "Sem titulo")
        safe_title = sanitize_filename(title)
        filename = f"SCOUT-{scout_id} {safe_title}.md"
        filepath = VAULT_PATH / filename

        note_content = generate_note(candidate, scout_id)

        if args.dry_run:
            log(f"  [DRY-RUN] Would write: {filename}")
            log(f"    Score: {candidate.get('hunt_score', 0)} | "
                f"Motifs: {candidate.get('motif', [])} | "
                f"Regime: {candidate.get('regime', '?')}")
        else:
            filepath.write_text(note_content, encoding="utf-8")
            log(f"  [OK] {filename}")

        generated += 1

    log(f"\n{'=' * 50}")
    log(f"  SCOUT NOTES {'(dry run)' if args.dry_run else 'GENERATED'}")
    log(f"{'=' * 50}")
    log(f"  Total generated: {generated}")
    log(f"  ID range: SCOUT-{next_id} → SCOUT-{next_id + generated - 1}")
    log(f"  Output: {VAULT_PATH}/")
    log(f"{'=' * 50}")


if __name__ == "__main__":
    main()
