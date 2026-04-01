#!/usr/bin/env python3
"""download_images.py — Download em lote das imagens do corpus via IIIF/thumbnail."""
import os, re, json, time, urllib.request, urllib.error
from pathlib import Path

OUTPUT_DIR = Path("data/raw")

ITEMS = [
    {"id": "BR-001", "url": "https://brasilianafotografica.bn.gov.br/brasiliana/bitstream/handle/20.500.12156.1/11778/0000001.JPG.jpg?sequence=3&isAllowed=y", "country": "BR"},
    {"id": "BR-002", "url": "https://brasilianafotografica.bn.gov.br/brasiliana/bitstream/handle/20.500.12156.1/13609/GV%20dvft%20004%20-%20Visita%20de%20Get%c3%balio%20a%20Bel%c3%a9m%20do%20Par%c3%a1%20Out19400000095.JPG.jpg?sequence=3&isAllowed=y", "country": "BR"},
    {"id": "BR-003", "url": "https://brasilianafotografica.bn.gov.br/brasiliana/bitstream/handle/20.500.12156.1/13611/GV%20dvft%20004%20-%20Visita%20de%20Get%c3%balio%20a%20Bel%c3%a9m%20do%20Par%c3%a1%20Out19400000097.JPG.jpg?sequence=3&isAllowed=y", "country": "BR"},
    {"id": "BR-004", "url": "https://brasilianafotografica.bn.gov.br/brasiliana/bitstream/handle/20.500.12156.1/11529/002080RJ0118.jpg.jpg?sequence=2&isAllowed=y", "country": "BR"},
    {"id": "BR-005", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/D%C3%A9cio_Villares_-_A_Rep%C3%BAblica.jpg/800px-D%C3%A9cio_Villares_-_A_Rep%C3%BAblica.jpg", "country": "BR"},
    {"id": "FR-001", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b531737635/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-002", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b531737529/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-003", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b53173732g/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-004", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b10574064v/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-005", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b531842166/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-006", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b8438243t/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-007", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b10051217v/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-008", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b10510623s/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-009", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b6952880n/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-010", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b8577646g/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "PT-001", "url": "https://bndigital.bnportugal.gov.pt/i/?IIIF=/c7/6e/8e/87/c76e8e87-15a8-464f-bc44-1c87dfdd8953/iiif/ct-117-g-cx_0000_000001.tif/full/!256,256/0/default.jpg", "country": "PO"},
    {"id": "PT-002", "url": "https://bndigital.bnportugal.gov.pt/i/?IIIF=/b3/e4/a7/5d/b3e4a75d-d38e-45ca-9c5b-2614e7f5b2bd/iiif/e-900-v_0000_000001.tif/full/!256,256/0/default.jpg", "country": "PO"},
    {"id": "PT-003", "url": "https://bndigital.bnportugal.gov.pt/i/?IIIF=/ae/8d/15/76/ae8d1576-002e-4678-af6f-cde5bdb3a602/iiif/e-4395-p_0000_1-2_p24-C-R0150_000001.tif/full/!256,256/0/default.jpg", "country": "PO"},
    {"id": "PT-004", "url": "https://bndigital.bnportugal.gov.pt/i/?IIIF=/96/87/56/c0/968756c0-6765-4371-bac9-b5efe8fa114e/iiif/e-4390-p_0000_1-2_p24-C-R0150_000001.tif/full/!256,256/0/default.jpg", "country": "PO"},
    {"id": "DE-001", "url": "https://www.bildindex.de/document/que20183316?part=0&medium=fmk45-ho-0136a", "country": "SW"},
    {"id": "DE-002", "url": "https://www.bildindex.de/document/obj08148970?part=0&medium=bh798728", "country": "IT"},
    {"id": "DE-003", "url": "https://www.bildindex.de/document/obj30110594?part=0&medium=mi10000g04", "country": "GE"},
    {"id": "DE-004", "url": "https://www.bildindex.de/document/obj20553978?part=0&medium=mi05228a07", "country": "GE"},
    {"id": "DE-005", "url": "https://www.bildindex.de/document/obj20672587?part=0&medium=mi07014d04", "country": "GE"},
    {"id": "DE-006", "url": "https://www.bildindex.de/document/obj08158050?part=0&medium=bh001222", "country": "IT"},
    {"id": "DE-007", "url": "https://www.bildindex.de/document/obj08108743?part=0&medium=bh_gern_024858_post", "country": "IT"},
    {"id": "DE-008", "url": "https://www.bildindex.de/document/obj20608421?part=0&medium=mi11300c09", "country": "GE"},
    {"id": "DE-009", "url": "https://www.bildindex.de/document/obj20459153?part=0&medium=mi04250a11", "country": "GE"},
    {"id": "DE-010", "url": "https://www.bildindex.de/document/obj20677105?part=0&medium=mi08920i01", "country": "GE"},
    {"id": "DE-011", "url": "https://www.bildindex.de/document/obj30143134?part=0&medium=mi12335e10", "country": "GE"},
    {"id": "US-001", "url": "https://tile.loc.gov/image-services/iiif/service:pnp:cph:34572000:cph3a45724/full/pct:100/0/default.jpg", "country": "UN"},
    {"id": "US-002", "url": "https://tile.loc.gov/image-services/iiif/service:pnp:ppmsca:87910000:ppmsca87910/full/pct:100/0/default.jpg", "country": "UN"},
    {"id": "US-003", "url": "https://tile.loc.gov/image-services/iiif/service:pnp:cph:30937000:cph3b09379/full/pct:100/0/default.jpg", "country": "UN"},
    {"id": "US-004", "url": "https://tile.loc.gov/image-services/iiif/service:pnp:cph:30402000:cph3f04023/full/pct:100/0/default.jpg", "country": "UN"},
    {"id": "US-007", "url": "https://tile.loc.gov/image-services/iiif/service:pnp:ppmsca:46404000:ppmsca46404/full/pct:100/0/default.jpg", "country": "UN"},
    {"id": "DE-012", "url": "https://commons.wikimedia.org/wiki/File:Gerechtigkeit-1537.jpg", "country": "GE"},
    {"id": "FR-012", "url": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Eug%C3%A8ne_Delacroix_-_Le_28_Juillet._La_Libert%C3%A9_guidant_le_peuple.jpg", "country": "FR"},
    {"id": "UK-004", "url": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Old_Bailey_Lady_Justice.jpg", "country": "UN"},
    {"id": "BE-002", "url": "https://upload.wikimedia.org/wikipedia/commons/1/10/Bruxelles_-_Palais_de_Justice.jpg", "country": "BE"},
    {"id": "FR-013", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b69480451/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-014", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b8410817c/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-015", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b8410270p/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-016", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b6942595s/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-017", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b8410268m/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-018", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b8412560z/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-019", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b9012753r/f1/full/1000,/0/native.jpg", "country": "FR"},
    {"id": "FR-020", "url": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b10544534k/f1/full/1000,/0/native.jpg", "country": "FR"},
]

def safe_filename(item_id: str, url: str) -> str:
    ext = ".jpg" if "jpg" in url.lower() or "jpeg" in url.lower() else ".jpg"
    return f"{item_id}{ext}"

def download_item(item: dict) -> bool:
    item_id, url = item['id'], item['url']
    country = item['country']
    dest_dir = OUTPUT_DIR / country.lower()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / safe_filename(item_id, url)
    if dest.exists():
        print(f'  SKIP {item_id} (já existe)')
        return True
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ICONOCRACY-Corpus/1.0 (PPGD/UFSC; ana.vanzin@posgrad.ufsc.br)'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        dest.write_bytes(data)
        size_kb = len(data) // 1024
        print(f'  OK {item_id} → {dest} ({size_kb} KB)')
        return True
    except Exception as e:
        print(f'  ERRO {item_id}: {e}')
        return False

if __name__ == '__main__':
    print(f'Baixando {len(ITEMS)} imagens para {OUTPUT_DIR}...')
    ok, fail = 0, 0
    for i, item in enumerate(ITEMS, 1):
        print(f'[{i}/{len(ITEMS)}] {item["id"]}')
        if download_item(item):
            ok += 1
        else:
            fail += 1
        time.sleep(0.5)  # respeitar rate limit dos acervos
    print(f'\nConcluído: {ok} OK, {fail} falhas')