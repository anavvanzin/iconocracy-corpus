#!/usr/bin/env python3
"""
hunt_firecrawl.py — Automated allegory scouting via Firecrawl Agent API.

Uses Firecrawl's agent endpoint to discover female national allegories
with legal-political function across the web, then generates vault notes
in the ICONOCRACY corpus format.

Usage:
    python tools/scripts/hunt_firecrawl.py --dry-run
    python tools/scripts/hunt_firecrawl.py --limit 10
    python tools/scripts/hunt_firecrawl.py --country FR --medium coin
    python tools/scripts/hunt_firecrawl.py --query "Marianne stamps 1800-1920"

Requires: FIRECRAWL_API_KEY env var (or --api-key flag).
"""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_PATH = REPO_ROOT / "corpus" / "corpus-data.json"
VAULT_DIR = REPO_ROOT / "vault" / "candidatos"

COUNTRY_MAP = {
    "FR": "France",
    "UK": "United Kingdom",
    "DE": "Germany",
    "US": "USA",
    "BE": "Belgium",
    "BR": "Brazil",
}

REGIME_KEYWORDS = {
    "FUNDACIONAL": [
        "phrygian cap", "liberty cap", "barrette", "semi-nude", "breast exposed",
        "dynamic", "moving", "aggressive", "broken chains", "torch raised",
        "barricade", "blood", "sacrifice",
    ],
    "NORMATIVO": [
        "seated", "static", "frontal", "scales", "blindfold", "book",
        "code", "architectural frame", "generic face", "monochrome",
        "serial", "fully clothed", "covered",
    ],
    "MILITAR": [
        "helmet", "armor", "breastplate", "shield", "sword", "trident",
        "eagle", "lion", "globe", "ship", "monumental", "rigid",
        "trophies", "colonial",
    ],
}

SUPORTE_KEYWORDS = {
    "moeda": ["coin", "centimes", "francs", "euros", "pence", "penny", "dollar", "reis", "cent"],
    "selo": ["stamp", "timbre", "poste", "marianne type"],
    "medalha": ["medal", "token", "spielmarke", "exhibition"],
    "papel-moeda": ["banknote", "bill", "note"],
    "monumento": ["monument", "statue", "sculpture", "relief"],
    "gravura": ["engraving", "print", "etching"],
}


def detect_regime(desc_body: str, desc_attrs: str) -> str:
    """Infer iconocratic regime from visual description text."""
    text = (desc_body + " " + desc_attrs).lower()
    scores: dict[str, int] = {}
    for regime, keywords in REGIME_KEYWORDS.items():
        scores[regime] = sum(1 for kw in keywords if kw in text)
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "NORMATIVO"


def detect_suporte(medium: str, title: str) -> str:
    """Map medium/title to corpus suporte category."""
    text = (medium + " " + title).lower()
    for suporte, keywords in SUPORTE_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return suporte
    return "outro"


def detect_endurecimento(desc_body: str, desc_attrs: str) -> str:
    """Generate natural-language endurecimento assessment from descriptions."""
    text = (desc_body + " " + desc_attrs).lower()
    parts = []

    # dessexualização
    if any(w in text for w in ["fully clothed", "covered", "draped", "robes", "armored"]):
        parts.append("dessexualização alta: corpo coberto")
    elif any(w in text for w in ["semi-nude", "breast exposed"]):
        parts.append("dessexualização baixa: corpo parcialmente exposto")
    else:
        parts.append("dessexualização média: descrição ambígua")

    # rigidez postural
    if any(w in text for w in ["seated", "sitting", "sentada", "static", "rigid"]):
        parts.append("rigidez postural alta: postura estática/sentada")
    elif any(w in text for w in ["standing", "de pé", "moving", "walking", "dynamic"]):
        parts.append("rigidez postural média: de pé ou em movimento")
    else:
        parts.append("rigidez postural: indeterminada")

    # inscrição estatal
    if any(w in text for w in ["constitution", "inscription", "lettering", "motto", "value"]):
        parts.append("inscrição estatal alta")

    # serialidade
    if any(w in text for w in ["coin", "stamp", "serial", "circulation"]):
        parts.append("serialidade alta: suporte massivo")

    return "; ".join(parts) if parts else "indeterminado — requer análise visual"


def detect_atributos(desc_attrs: str) -> list[str]:
    """Extract attribute checklist from description text."""
    text = desc_attrs.lower()
    attrs = []
    mapping = {
        "balança": ["scales", "balance"],
        "espada": ["sword"],
        "barrete frígio": ["phrygian cap", "liberty cap", "barrette"],
        "tridente": ["trident"],
        "escudo": ["shield"],
        "leão": ["lion"],
        "capacete": ["helmet", "corinthian"],
        "cetro": ["scepter"],
        "bandeira": ["flag"],
        "tocha": ["torch"],
        "livro": ["book", "code"],
        "coroa de louros": ["laurel", "wreath"],
        "venda": ["blindfold"],
        "fasces": ["fasces"],
        "globo": ["globe"],
        "águia": ["eagle"],
        "toga": ["robe", "draped", "classical"],
    }
    for attr_pt, keywords in mapping.items():
        if any(kw in text for kw in keywords):
            attrs.append(attr_pt)
    return attrs


def build_vault_note(item: dict, item_id: str) -> str:
    """Build Obsidian vault note in ICONOCRACY frontmatter format."""
    desc_body = item.get("visual_description_body_posture", "")
    desc_attrs = item.get("visual_description_attributes", "")

    regime = detect_regime(desc_body, desc_attrs)
    suporte = detect_suporte(item.get("medium", ""), item.get("item_title", ""))
    endurecimento = detect_endurecimento(desc_body, desc_attrs)
    atributos = detect_atributos(desc_attrs)

    country_code = item.get("country", "").upper()
    # Normalize country codes
    country_norm = {
        "FRANCE": "FR", "UK": "UK", "UNITED KINGDOM": "UK",
        "GERMANY": "DE", "USA": "US", "UNITED STATES": "US",
        "BELGIUM": "BE", "BRAZIL": "BR",
    }.get(country_code, country_code)

    motivo = item.get("item_title", "Alegoria")
    # Try to extract allegory name from title
    for name in ["Marianne", "Britannia", "Germania", "Columbia", "Justitia",
                  "La Belgique", "A República", "Republica", "Liberty", "Republic"]:
        if name.lower() in motivo.lower():
            motivo = name
            break

    tags_list = "\n".join(f"  - {t}" for t in [
        "corpus/candidato",
        f"pais/{country_norm}",
        f"suporte/{suporte}",
        f"regime/{regime.lower()}",
        f"motivo/{motivo.lower().replace(' ', '-')}",
        "fonte/firecrawl-agent",
        "verificar",
    ])

    attrs_checklist = "\n".join(
        f"- [x] {a}" if a in atributos else f"- [ ] {a}"
        for a in ["balança", "espada", "barrete frígio", "tridente", "escudo/brasão",
                   "leão", "capacete/couraça", "bandeira", "tocha", "livro/constituição",
                   "coroa de louros", "venda nos olhos", "fasces", "toga/vestimenta clássica",
                   "postura frontal", "contexto arquitetônico"]
    )

    today = date.today().isoformat()
    year = item.get("year", "s.d.")
    image_url = item.get("image_url", "null")
    source_url = item.get("source_url", "null")
    full_desc = f"{desc_body} {desc_attrs}".strip()

    return f"""---
id: {item_id}
tipo: corpus-candidato
status: candidato
titulo: "{item.get('item_title', 'Sem título')}"
acervo: "Firecrawl Agent / Web"
url: {source_url}
url_iiif: null
data_estimada: "{year}"
pais: {country_norm}
suporte: {suporte}
motivo_alegorico: "{motivo}"
regime: {regime}
confianca: medio
tags:
{tags_list}
related:
  - "[[Regime {regime}]]"
  - "[[Nachleben]]"
  - "[[Contrato Sexual Visual]]"
hf_synced: false
data_scout: {today}
fonte_scout: firecrawl-agent
---

## Identificação

**Título:** {item.get('item_title', 'Sem título')}
**Acervo:** Firecrawl Agent / Web
**URL de acesso:** {source_url}
**URL da imagem:** {image_url}
**URL IIIF:** null
**Data estimada:** {year}
**País:** {country_norm}
**Suporte:** {suporte}

---

## Análise preliminar

**Motivo alegórico:** {motivo}
**Regime iconocrático:** {regime}
**Descrição:** {full_desc}

**Atributos identificados:**
{attrs_checklist}

**endurecimento detectado:** {endurecimento}

---

## Próximos passos

- [ ] Verificar imagem em alta resolução
- [ ] Confirmar data de emissão
- [ ] Verificar se item já existe no corpus (deduplicação)
- [ ] Análise visual profunda (iconocode-analyze)
- [ ] Código de purificação (code_purification.py)
"""


def dedup_against_corpus(items: list[dict]) -> list[dict]:
    """Remove items already present in corpus (by URL or title similarity)."""
    if not CORPUS_PATH.exists():
        return items

    with open(CORPUS_PATH, "r") as f:
        corpus = json.load(f)

    corpus_urls = set()
    corpus_titles = set()
    for c in corpus:
        for key in ["url", "source_url"]:
            val = c.get(key, "")
            if val:
                corpus_urls.add(val.lower().strip())
        title = c.get("title", "") or c.get("titulo", "")
        if title:
            corpus_titles.add(title.lower().strip())

    new_items = []
    for item in items:
        url = (item.get("source_url") or "").lower().strip()
        title = (item.get("item_title") or "").lower().strip()

        if url in corpus_urls:
            print(f"  [DEDUP] URL match: {item.get('item_title')}")
            continue
        if any(title in ct or ct in title for ct in corpus_titles if len(ct) > 5):
            print(f"  [DEDUP] Title match: {item.get('item_title')}")
            continue
        new_items.append(item)

    return new_items


def get_next_ids(country_code: str, count: int) -> list[str]:
    """Generate sequential vault note IDs for a country."""
    existing = list(VAULT_DIR.glob(f"{country_code}-*.md"))
    max_num = 0
    for p in existing:
        m = re.match(rf"^{country_code}-(\d+)", p.stem)
        if m:
            max_num = max(max_num, int(m.group(1)))

    return [f"{country_code}-{max_num + i + 1:03d}" for i in range(count)]


def run_firecrawl_agent(api_key: str, prompt: str, model: str = "spark-1-pro") -> list[dict]:
    """Call Firecrawl Agent API and return structured results."""
    try:
        from firecrawl import FirecrawlApp
    except ImportError:
        print("ERROR: firecrawl Python SDK not installed.")
        print("Run: pip install firecrawl")
        sys.exit(1)

    app = FirecrawlApp(api_key=api_key)

    # Define extraction schema (Python SDK uses dict-based schema)
    schema = {
        "type": "object",
        "properties": {
            "national_allegory_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "item_title": {"type": "string"},
                        "country": {"type": "string"},
                        "year": {"type": "number"},
                        "medium": {"type": "string"},
                        "source_url": {"type": "string"},
                        "image_url": {"type": "string"},
                        "visual_description_body_posture": {"type": "string"},
                        "visual_description_attributes": {"type": "string"},
                    },
                    "required": ["item_title", "country", "year", "source_url"],
                },
            }
        },
        "required": ["national_allegory_items"],
    }

    print(f"Running Firecrawl Agent (model: {model})...")
    print(f"Prompt: {prompt[:100]}...")

    result = app.agent(
        prompt=prompt,
        schema=schema,
        model=model,
    )

    if isinstance(result, dict):
        items = result.get("national_allegory_items", [])
    elif hasattr(result, "data"):
        data = result.data if isinstance(result.data, dict) else {}
        items = data.get("national_allegory_items", [])
    else:
        items = []

    return items


def build_prompt(countries: list[str] | None = None,
                 medium: str | None = None,
                 period: str = "1800-2000",
                 custom_query: str | None = None,
                 limit: int = 20) -> str:
    """Build the Firecrawl Agent prompt with filters."""
    if custom_query:
        return custom_query

    country_names = []
    if countries:
        country_names = [COUNTRY_MAP.get(c.upper(), c) for c in countries]
    else:
        country_names = list(COUNTRY_MAP.values())

    medium_filter = f"- Medium: {medium}." if medium else "- Medium: coins, banknotes, stamps, monuments, architectural reliefs, or historical engravings."

    return f"""Conduct a deep web research across auction sites, numismatic/philatelic catalogs, historical blogs, and open galleries to find at least {limit} distinct items featuring **female national allegories with a legal, political, or state function** (e.g., Marianne, Britannia, Germania, Columbia, Justitia, La Belgique, or A República).

Filter criteria:
- Countries: {', '.join(country_names)}.
- Date: {period}.
{medium_filter}

For each item found, extract exactly this data into a structured format:
1. **Title / Name** of the item
2. **Country & Year**
3. **Medium** (coin, statue, stamp, etc.)
4. **Source URL** (where you found it)
5. **Direct Image URL** (link to a high-res image)
6. **Visual Description (CRITICAL)**: Be extremely detailed about her body and posture. Is she fully clothed, armored, or semi-nude? Is she seated statically, standing rigidly, or moving? What attributes is she holding (scales, sword, shield, book, Phrygian cap)?"""


def main():
    parser = argparse.ArgumentParser(description="Firecrawl-based allegory scout")
    parser.add_argument("--api-key", help="Firecrawl API key (or set FIRECRAWL_API_KEY)")
    parser.add_argument("--model", default="spark-1-pro", help="Firecrawl agent model")
    parser.add_argument("--country", nargs="+", help="Country codes (FR UK DE US BE BR)")
    parser.add_argument("--medium", help="Filter by medium (coin, stamp, medal, etc.)")
    parser.add_argument("--period", default="1800-2000", help="Date range (default: 1800-2000)")
    parser.add_argument("--query", help="Custom prompt (overrides other filters)")
    parser.add_argument("--limit", type=int, default=20, help="Target number of items")
    parser.add_argument("--dry-run", action="store_true", help="Show prompt without executing")
    parser.add_argument("--no-dedup", action="store_true", help="Skip deduplication against corpus")
    parser.add_argument("--output", help="Save raw JSON to file")
    args = parser.parse_args()

    prompt = build_prompt(
        countries=args.country,
        medium=args.medium,
        period=args.period,
        custom_query=args.query,
        limit=args.limit,
    )

    if args.dry_run:
        print("=== DRY RUN ===")
        print(f"Prompt:\n{prompt}")
        print(f"\nModel: {args.model}")
        return

    api_key = args.api_key or os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("ERROR: No API key. Set FIRECRAWL_API_KEY or use --api-key")
        sys.exit(1)

    # Run agent
    items = run_firecrawl_agent(api_key, prompt, model=args.model)
    print(f"\nAgent returned {len(items)} items")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
        print(f"Raw JSON saved to {args.output}")

    # Dedup
    if not args.no_dedup:
        print("\nDeduplicating against corpus...")
        items = dedup_against_corpus(items)
        print(f"{len(items)} new items after dedup")

    if not items:
        print("No new items found. Try different filters or a custom --query.")
        return

    # Generate vault notes
    print(f"\nGenerating vault notes...")
    VAULT_DIR.mkdir(parents=True, exist_ok=True)

    # Group by country for ID generation
    by_country = {}
    for item in items:
        cc = {
            "FRANCE": "FR", "UK": "UK", "UNITED KINGDOM": "UK",
            "GERMANY": "DE", "USA": "US", "UNITED STATES": "US",
            "BELGIUM": "BE", "BRAZIL": "BR",
        }.get(item.get("country", "").upper(), "XX")
        by_country.setdefault(cc, []).append(item)

    generated = []
    for cc, cc_items in by_country.items():
        ids = get_next_ids(cc, len(cc_items))
        for item, item_id in zip(cc_items, ids):
            note = build_vault_note(item, item_id)
            filepath = VAULT_DIR / f"{item_id} {item.get('item_title', 'Sem título')}.md"
            # Sanitize filename
            safe_name = re.sub(r'[<>:"/\\|?*]', '', filepath.name)
            filepath = filepath.parent / safe_name
            filepath.write_text(note, encoding="utf-8")
            generated.append(str(filepath))
            print(f"  ✓ {item_id}: {item.get('item_title', '?')}")

    print(f"\n{len(generated)} vault notes generated in {VAULT_DIR}/")
    print(f"\nNext steps:")
    print(f"  1. python tools/scripts/validate_schemas.py")
    print(f"  2. python tools/scripts/vault_sync.py status")
    print(f"  3. Review notes in Obsidian, then run iconocode-analyze for deep analysis")


if __name__ == "__main__":
    main()
