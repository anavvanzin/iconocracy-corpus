---
name: archive-fallback
description: >
  Retry-and-fallback routine for Gallica/Europeana/LOC/BnF/Numista image fetches.
  Try IIIF manifest first, 2 retries with backoff, then Playwright bypass, then
  metadata-only record with #imagem-pendente. Use when the user says "arquivo
  falhou", "tentar fallback", "gallica 429", "europeana timeout", or when SCOUT
  or ARGOS reports repeated archive failures. Invoked as a sub-routine by SCOUT/ARGOS.
user-invocable: true
---

Codifies the CLAUDE.md retry policy: "If an API fails twice, switch to fallback
strategy immediately — don't keep retrying the same endpoint."

## Decision ladder

For each target URL, walk in order. Stop at first success.

### Level 1 — IIIF manifest

Probe canonical IIIF entry points. If the archive exposes a manifest, fetch
the highest-resolution derivative directly. No Playwright cost.

- Gallica: `https://gallica.bnf.fr/iiif/ark:/<ark>/manifest.json`
- Europeana: via API `record/<dataset>/<id>.json` → `edmIsShownBy`
- LOC: `https://www.loc.gov/item/<id>/?fo=json`

Use `$REPO/tools/scripts/gallica_discovery.py` when target is Gallica.

### Level 2 — Direct HTTP, 2 retries max

```python
backoff = [2, 8]  # seconds
for attempt, wait in enumerate(backoff, 1):
    resp = fetch(url)
    if resp.ok: return resp
    if resp.status in (429, 503):
        sleep(wait)
        continue
    break  # hard failure — do not retry
```

Never exceed 2 retries on the same endpoint.

### Level 3 — Playwright bypass

For archives behind JS/anti-bot (Colnect, some Numista pages):

```bash
conda run -n iconocracy python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url, wait_until='networkidle')
    # capture the <img> src or screenshot the target region
"
```

Timeout 30s per page. Do not retry at this level.

### Level 4 — Metadata-only fallback

If all fetch attempts fail:

1. Create `vault/candidatos/XX-NNN Title.md` using existing vault naming
   pattern with whatever metadata was gathered (title, date, holding
   institution, source URL).
2. Tag `#imagem-pendente` and `#verificar`.
3. Append to `$REPO/vault/sessoes/archive-failures-YYYY-MM-DD.md` (ISO date).
   Line format:
   ```
   - SCOUT-NNN | <url> | <last-error> | attempts: IIIF/HTTP/PW
   ```
4. Do NOT write a placeholder image file. Corpus entries without an image
   stay text-only until a future campaign resolves them.

## Report format

After a batch:

```
| SCOUT  | Level reached | Status              |
|--------|---------------|---------------------|
| FR-042 | 1 (IIIF)      | OK                  |
| FR-043 | 2 (HTTP)      | OK after 1 retry    |
| DE-019 | 3 (Playwright)| OK                  |
| BR-008 | 4 (metadata)  | pendente            |
```

## Integration points

- **SCOUT** (`/Users/ana/.claude/skills/corpus-scout/`) calls this sub-routine
  whenever `requests.get` raises, times out, or returns non-2xx.
- **ARGOS** (`tools/scripts/argos_build_manifest.py`) consumes the failure log
  from `vault/sessoes/archive-failures-*.md` to rebuild the acquisition manifest.

## Do NOT

- Keep retrying the same endpoint past Level 2 — violates CLAUDE.md policy.
- Synthesize or hallucinate missing image data.
- Save binary placeholders to `data/raw/` (ADR-001 + CI will reject).
