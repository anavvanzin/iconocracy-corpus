#!/usr/bin/env python3
"""
enrich_iiif.py — Enriquece corpus-data.json com url_iiif e url_image_download.

Estratégias por acervo:
  1. Gallica (url contém gallica.bnf.fr) → extrai ARK → constrói IIIF
  2. Europeana via Gallica (url contém ark__12148_) → decodifica ARK → IIIF Gallica
  3. Europeana nativa → IIIF Europeana via item ID
  4. Library of Congress → IIIF tile.loc.gov via resource URL
  5. Rijksmuseum → marcar para verificação manual (nova URL permalink)
  6. Brasiliana Fotográfica → thumbnail_url como proxy (sem IIIF nativo)
  7. Outros → preservar thumbnail_url se disponível

Uso:
  python3 enrich_iiif.py corpus-data.json [--out corpus-data-enriched.json] [--report]
"""

import json, re, sys, argparse
from urllib.parse import urlparse
from pathlib import Path
from collections import defaultdict

# ── Padrões ──────────────────────────────────────────────────────────────────

def iiif_gallica_from_ark(ark: str, size: str = "1000,") -> dict:
    """Constrói URL IIIF Gallica a partir de um ARK."""
    clean = re.sub(r'^https?://gallica\.bnf\.fr/', '', ark)
    clean = re.sub(r'^/?ark:/', 'ark:/', clean)
    if not clean.startswith('ark:'):
        clean = f'ark:/12148/{clean}'
    url = f"https://gallica.bnf.fr/iiif/{clean}/f1/full/{size}/0/native.jpg"
    manifest = f"https://gallica.bnf.fr/iiif/{clean}/manifest.json"
    return {"url_iiif": manifest, "url_image_download": url, "iiif_source": "gallica"}


def ark_from_europeana_url(url: str) -> str | None:
    """Extrai ARK Gallica de URL Europeana (padrão ark__12148_XXXX)."""
    m = re.search(r'ark__(\d+)_(\w+)', url)
    if m:
        return f"ark:/{m.group(1)}/{m.group(2)}"
    return None


def iiif_europeana_native(url: str) -> dict | None:
    """Constrói IIIF Europeana para itens não-Gallica."""
    # padrão: https://www.europeana.eu/en/item/PROVIDER/LOCAL_ID
    m = re.search(r'/item/(\d+)/(.+?)(?:\?|$)', url)
    if m:
        provider, local = m.group(1), m.group(2)
        manifest = f"https://iiif.europeana.eu/presentation/{provider}/{local}/manifest"
        return {"url_iiif": manifest, "url_image_download": None, "iiif_source": "europeana"}
    return None


def iiif_loc_from_resource(item: dict) -> dict | None:
    """
    Constrói IIIF LoC a partir da thumbnail_url (resource URL).
    Padrão: https://www.loc.gov/resource/cph.3a45724/
    → IIIF: https://tile.loc.gov/image-services/iiif/service:pnp:cph:3a45000:cph3a45724
    """
    thumb = item.get("thumbnail_url", "") or ""
    m = re.search(r'/resource/([a-z]+)\.(\w+)/?', thumb)
    if m:
        prefix, num = m.group(1), m.group(2)
        # LoC IIIF service path: prefix:NNNNN00:prefixNNNNNN
        # Heurística: primeiros 7 dígitos → subfolder com 00 no fim
        digits = re.sub(r'\D', '', num)
        if len(digits) >= 5:
            folder = digits[:5] + "000"  # aproximação — verificar
            service_id = f"service:pnp:{prefix}:{folder}:{prefix}{num}"
            manifest = f"https://tile.loc.gov/image-services/iiif/{service_id}/info.json"
            download = f"https://tile.loc.gov/image-services/iiif/{service_id}/full/pct:100/0/default.jpg"
            return {"url_iiif": manifest, "url_image_download": download,
                    "iiif_source": "loc", "iiif_note": "#verificar-iiif-loc"}
    # Fallback: item API JSON
    url = item.get("url", "")
    m2 = re.search(r'/item/(\d+)/?', url)
    if m2:
        item_id = m2.group(1)
        return {"url_iiif": f"https://www.loc.gov/item/{item_id}/?fo=json",
                "url_image_download": None,
                "iiif_source": "loc_api", "iiif_note": "#verificar-iiif-loc"}
    return None


def iiif_rijksmuseum(item: dict) -> dict | None:
    """
    Rijksmuseum: novo permalink format não expõe IIIF diretamente.
    Marca para verificação manual mas preserva URL de recurso.
    """
    url = item.get("url", "")
    # tenta extrair object ID do permalink: /object/SLUG--ID
    m = re.search(r'/object/[^/]+--([\w]+)$', url)
    if m:
        obj_id = m.group(1)
        return {"url_iiif": None, "url_image_download": None,
                "iiif_source": "rijksmuseum_pending",
                "iiif_note": f"#verificar-iiif-rijksmuseum permalink_id={obj_id}"}
    return None


# ── Dispatcher principal ──────────────────────────────────────────────────────

def enrich_item(item: dict) -> dict:
    """Adiciona url_iiif e url_image_download ao item, sem sobrescrever campos existentes."""
    url = item.get("url", "") or ""
    thumb = item.get("thumbnail_url", "") or ""
    result = {"url_iiif": None, "url_image_download": None,
              "iiif_source": "none", "iiif_note": None}

    # 1. Gallica direto
    if "gallica.bnf.fr" in url:
        ark = re.search(r'ark:/\d+/\w+', url)
        if ark:
            result.update(iiif_gallica_from_ark(ark.group()))
            return {**item, **result}

    # 2. Thumbnail já é Gallica IIIF (ex: itens Europeana/Gallica)
    if "gallica.bnf.fr/iiif" in thumb:
        # Extrai ARK do thumbnail
        ark = re.search(r'ark:/\d+/\w+', thumb)
        if ark:
            r = iiif_gallica_from_ark(ark.group())
            result.update(r)
            return {**item, **result}

    # 3. Europeana com ARK Gallica codificado
    if "europeana.eu" in url:
        ark = ark_from_europeana_url(url)
        if ark:
            result.update(iiif_gallica_from_ark(ark))
            result["iiif_source"] = "europeana_gallica"
            return {**item, **result}
        # Europeana nativa
        r = iiif_europeana_native(url)
        if r:
            result.update(r)
            return {**item, **result}

    # 4. Library of Congress
    if "loc.gov" in url:
        r = iiif_loc_from_resource(item)
        if r:
            result.update(r)
            return {**item, **result}

    # 5. Rijksmuseum
    if "rijksmuseum.nl" in url:
        r = iiif_rijksmuseum(item)
        if r:
            result.update(r)
            return {**item, **result}

    # 6. Thumbnail disponível (Brasiliana, Wikipedia, etc.) → usar como fallback
    if thumb and thumb not in ("", "null"):
        result["url_image_download"] = thumb
        result["iiif_source"] = "thumbnail_fallback"
        result["iiif_note"] = "#sem-iiif usar-thumbnail"
        return {**item, **result}

    # 7. Sem URL de imagem
    result["iiif_note"] = "#sem-iiif #verificar"
    return {**item, **result}


# ── Relatório ─────────────────────────────────────────────────────────────────

def generate_report(enriched: list) -> str:
    stats = defaultdict(int)
    no_image = []
    for item in enriched:
        src = item.get("iiif_source", "none")
        stats[src] += 1
        if not item.get("url_image_download") and not item.get("url_iiif"):
            no_image.append(item["id"])

    lines = ["# Relatório de Enriquecimento IIIF", "",
             f"Total de itens: {len(enriched)}", ""]

    lines.append("## Por fonte IIIF")
    for src, count in sorted(stats.items(), key=lambda x: -x[1]):
        icon = "✓" if src not in ("none", "thumbnail_fallback", "rijksmuseum_pending") else "⚠"
        lines.append(f"- {icon} `{src}`: {count} itens")

    with_download = sum(1 for i in enriched if i.get("url_image_download"))
    with_manifest = sum(1 for i in enriched if i.get("url_iiif") and
                       not str(i.get("url_iiif","")).endswith("?fo=json"))
    lines.extend(["",
        f"## Resumo",
        f"- Itens com `url_image_download`: {with_download}/{len(enriched)}",
        f"- Itens com manifesto IIIF real: {with_manifest}/{len(enriched)}",
        f"- Itens sem nenhuma URL de imagem: {len(no_image)}",
    ])

    if no_image:
        lines.extend(["", "## Itens sem URL de imagem (requerem busca manual)"])
        for id_ in no_image:
            lines.append(f"- {id_}")

    lines.extend(["", "## Próximos passos",
        "1. Verificar itens `#verificar-iiif-loc` com API real do LoC",
        "2. Resolver itens `rijksmuseum_pending` via API Rijksmuseum",
        "3. Rodar script de download: `python3 download_images.py`",
        "4. Popular `drive-manifest.json` com os caminhos locais",
        "5. Subir imagens ao HF Hub: `hf upload warholana/iconocracy-corpus data/raw/ --type dataset`",
    ])
    return "\n".join(lines)


# ── Download script generator ─────────────────────────────────────────────────

def generate_download_script(enriched: list, output_dir: str = "data/raw") -> str:
    lines = [
        "#!/usr/bin/env python3",
        '"""download_images.py — Download em lote das imagens do corpus via IIIF/thumbnail."""',
        "import os, re, json, time, urllib.request, urllib.error",
        "from pathlib import Path",
        "",
        f'OUTPUT_DIR = Path("{output_dir}")',
        "",
        "ITEMS = [",
    ]
    for item in enriched:
        dl = item.get("url_image_download")
        if dl:
            country = item.get("country", "XX").split()[0][:2].upper()
            item_id = item.get("id", "UNKNOWN")
            lines.append(f'    {{"id": "{item_id}", "url": "{dl}", "country": "{country}"}},')
    lines.extend([
        "]",
        "",
        "def safe_filename(item_id: str, url: str) -> str:",
        '    ext = ".jpg" if "jpg" in url.lower() or "jpeg" in url.lower() else ".jpg"',
        "    return f\"{item_id}{ext}\"",
        "",
        "def download_item(item: dict) -> bool:",
        "    item_id, url = item['id'], item['url']",
        "    country = item['country']",
        "    dest_dir = OUTPUT_DIR / country.lower()",
        "    dest_dir.mkdir(parents=True, exist_ok=True)",
        "    dest = dest_dir / safe_filename(item_id, url)",
        "    if dest.exists():",
        "        print(f'  SKIP {item_id} (já existe)')",
        "        return True",
        "    try:",
        "        req = urllib.request.Request(url, headers={'User-Agent': 'ICONOCRACY-Corpus/1.0 (PPGD/UFSC; ana.vanzin@posgrad.ufsc.br)'})",
        "        with urllib.request.urlopen(req, timeout=30) as r:",
        "            data = r.read()",
        "        dest.write_bytes(data)",
        "        size_kb = len(data) // 1024",
        "        print(f'  OK {item_id} → {dest} ({size_kb} KB)')",
        "        return True",
        "    except Exception as e:",
        "        print(f'  ERRO {item_id}: {e}')",
        "        return False",
        "",
        "if __name__ == '__main__':",
        "    print(f'Baixando {len(ITEMS)} imagens para {OUTPUT_DIR}...')",
        "    ok, fail = 0, 0",
        "    for i, item in enumerate(ITEMS, 1):",
        "        print(f'[{i}/{len(ITEMS)}] {item[\"id\"]}')",
        "        if download_item(item):",
        "            ok += 1",
        "        else:",
        "            fail += 1",
        "        time.sleep(0.5)  # respeitar rate limit dos acervos",
        "    print(f'\\nConcluído: {ok} OK, {fail} falhas')",
    ])
    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Enriquece corpus-data.json com URLs IIIF")
    parser.add_argument("input", help="corpus-data.json de entrada")
    parser.add_argument("--out", default=None, help="arquivo de saída (padrão: sobrescreve input)")
    parser.add_argument("--report", action="store_true", help="gera relatório markdown")
    parser.add_argument("--download-script", action="store_true", help="gera download_images.py")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)
    items = data if isinstance(data, list) else data.get("items", data.get("corpus", []))

    print(f"Processando {len(items)} itens...")
    enriched = [enrich_item(item) for item in items]

    out_path = args.out or args.input
    if isinstance(data, list):
        out_data = enriched
    else:
        out_data = {**data}
        key = "items" if "items" in data else "corpus"
        out_data[key] = enriched

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print(f"Salvo: {out_path}")

    if args.report:
        report = generate_report(enriched)
        rpath = Path(out_path).parent / "iiif-enrichment-report.md"
        rpath.write_text(report)
        print(f"Relatório: {rpath}")
        print(report)

    if args.download_script:
        script = generate_download_script(enriched)
        spath = Path(out_path).parent / "download_images.py"
        spath.write_text(script)
        print(f"Script de download: {spath}")

    return enriched

if __name__ == "__main__":
    main()
