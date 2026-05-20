# ARGOS next-iteration implementation plan: HTML landing-page extraction first

Date: 2026-04-14
Owner surface: `tools/argos/` + `tools/scripts/`
Status: planning only, no code changes yet

## Why this plan exists

Repo inspection shows that ARGOS already has a working first pass for:
- manifest building: `tools/argos/manifest.py`
- protocol classification: `tools/argos/classifier.py`
- direct fetches: `tools/argos/protocols/direct.py`
- pattern-only IIIF discovery: `tools/argos/protocols/iiif.py`
- controlled Playwright fallback: `tools/argos/protocols/playwright_fallback.py`
- item acquisition orchestration: `tools/scripts/argos_acquire_item.py`
- dispatch grouping: `tools/scripts/argos_prepare_dispatch.py`
- markdown reporting: `tools/argos/report.py`

The main functional gap is clear in the direct protocol: `fetch_direct()` currently rejects HTML/text responses as `unexpected_content_type` and stops. That is correct for raw binary download, but it means ARGOS cannot yet turn a landing page into a resolvable asset URL. The next iteration should therefore make HTML landing-page extraction the first-class fallback for `direct` and `unknown` sources that return HTML instead of an image.

## Current repo facts that shape the work

1. `tools/argos/protocols/direct.py`
   - accepts image-like content types
   - rejects HTML/text via `_reject_unexpected_content_type()`
   - does not preserve the HTML body or discover embedded asset links

2. `tools/argos/protocols/iiif.py`
   - only performs heuristic pattern discovery
   - does not fetch and parse manifest JSON from arbitrary IIIF Presentation endpoints

3. `tools/argos/protocols/playwright_fallback.py`
   - currently captures screenshots, not actual asset downloads
   - has a restricted-domain gate already worth preserving

4. `tools/argos/classifier.py`
   - maps domain -> protocol only
   - has no richer route policy for HTML-first domains, IIIF-capable domains, or restricted browser retrieval

5. `tools/scripts/argos_acquire_item.py`
   - current attempt chain is: protocol -> `iiif-discovery` on block -> Playwright fallback when allowed
   - there is no dedicated HTML extraction step in the chain

6. `tools/argos/report.py`
   - already surfaces `unexpected_content_type` as a meaningful failure class
   - can be extended to report landing-page extraction outcomes and unresolved HTML cases

## Implementation goals

Primary goal for this iteration:
- add HTML landing-page extraction for `direct` / `unknown` fetches that return HTML or redirect into HTML, then retry acquisition from extracted asset candidates

Secondary hooks to lay now, even if not fully exploited immediately:
- real IIIF/API manifest parsing
- controlled restricted-domain browser asset retrieval
- domain-aware routing instead of domain -> protocol only

Non-goals for this iteration:
- full authenticated scraping
- automatic OCR or metadata extraction from landing pages
- broad crawler behavior across arbitrary sites
- replacing existing manifest/report workflow

## Target design

### A. New routing model

Keep the existing public protocol labels in the manifest (`iiif`, `direct`, `playwright-required`, `blocked`, `unknown`) so current schema and reports stay stable, but add route metadata behind the scenes.

Add a richer route object in `tools/argos/classifier.py`:
- normalized domain
- manifest protocol label
- ordered fallback chain
- `html_extraction_allowed`
- `iiif_probe_allowed`
- `browser_asset_allowed`
- `restricted_domain`

This lets acquisition logic decide:
- whether to attempt HTML extraction before giving up
- whether to probe for IIIF manifest/API links from HTML
- whether a domain can escalate to browser asset retrieval or must remain manual

### B. New HTML extraction layer

Create a new module: `tools/argos/protocols/html.py`

Responsibilities:
1. Accept raw HTML bytes or HTML text plus the response URL.
2. Parse candidate asset URLs from deterministic sources only:
   - `<meta property="og:image">`
   - `<meta name="twitter:image">`
   - `<link rel="image_src">`
   - `<img src>` / `<img data-src>` / `<img data-original>` / `<source srcset>`
   - JSON blobs containing IIIF or image URLs
   - anchor tags pointing to obvious image/download targets
3. Normalize relative URLs with `urllib.parse.urljoin`.
4. Score candidates by confidence, preferring:
   - IIIF image endpoints
   - explicit download links
   - high-resolution JPG/PNG/TIFF/WebP URLs
   - same-domain or known CDN asset URLs tied to the page
5. Return a structured extraction payload, not just one URL.

Suggested return shape:
- `page_url`
- `content_type`
- `page_title`
- `candidates` list with `{url, kind, score, source_hint}`
- `iiif_manifest_candidates`
- `api_candidates`
- `notes`

Implementation constraint:
- use stdlib HTML parsing and regex only; do not add a heavy scraping dependency for this first step

### C. Direct protocol should preserve HTML instead of discarding it blindly

Extend `tools/argos/protocols/direct.py` so HTML/text responses can optionally be returned as an inspectable result instead of immediate terminal failure.

Concrete change:
- add a new helper such as `fetch_direct_or_page(url, dest_path, timeout=60, retries=3)` or extend `fetch_direct()` with `capture_html=True`
- when the response is HTML/text:
  - do not persist it as the image artifact
  - return a structured result like:
    - `failure_class: "html_landing_page"`
    - `html_text`
    - `response_url`
    - `content_type`
    - `notes`
- keep current `unexpected_content_type` handling for non-image, non-HTML responses

This is the minimum change that unlocks extraction without breaking the current direct-download contract.

### D. Acquisition chain should add HTML extraction before IIIF/block escalation stops

Modify `tools/scripts/argos_acquire_item.py`.

New desired chain for `direct` and `unknown` routes:
1. direct fetch
2. if image success -> finish
3. if `html_landing_page` -> run HTML extraction
4. if an extracted asset candidate exists -> retry direct fetch against best candidate
5. if IIIF manifest candidate exists -> run IIIF fetch path
6. if still blocked and route/policy allows -> browser asset retrieval
7. otherwise mark `failed` or `manual`

New desired chain for `iiif` routes:
1. current IIIF discovery/fetch
2. if IIIF fails but source URL returns HTML -> HTML extraction can still mine manifest or asset links
3. if still blocked and allowed -> browser asset retrieval

Record each step in `attempts` with distinct step names, e.g.:
- `direct`
- `html-extract`
- `html-asset-direct`
- `html-iiif`
- `iiif`
- `browser-asset`

### E. IIIF/API parsing hook should be real, not only pattern-based

Add or extend module work in `tools/argos/protocols/iiif.py`.

For this iteration, implement a small but concrete parser layer:
- `fetch_iiif_manifest(manifest_url)`
- `extract_first_canvas_image(manifest_json)`
- support common IIIF Presentation 2 and 3 shapes
- preserve existing pattern discovery helpers (`gallica_manifest_from_ark`, Europeana/Gallica, LOC heuristics)

Then let HTML extraction feed discovered manifest URLs into this parser.

Keep scope narrow:
- first image/canvas only
- no multi-page selection UI yet
- no harvesting of all canvases in this iteration

### F. Controlled browser asset retrieval should move beyond screenshots

Extend `tools/argos/protocols/playwright_fallback.py` in a strictly controlled way.

Do not remove screenshot fallback, but add a second path for browser-resolved asset retrieval:
- inspect DOM after page load for image candidates and download links
- allow response interception for image requests from the same domain or approved CDN domains only
- write the resolved asset if a real binary image is captured
- keep screenshot fallback only when asset capture fails

Policy guardrails:
- preserve `RESTRICTED_DOMAINS`
- add an allowlist for acceptable asset hostnames derived from route metadata
- record whether the output is a real asset or only a screenshot in result notes and provenance metadata

### G. Reporting and manifest metadata should expose landing-page behavior

Extend manifest metadata via `provenance.metadata` rather than breaking top-level schema immediately.

Add fields such as:
- `landing_page_url`
- `landing_page_content_type`
- `html_candidate_count`
- `selected_asset_url`
- `selected_asset_kind`
- `selected_asset_score`
- `iiif_manifest_url`
- `browser_capture_mode` (`asset` or `screenshot`)

Update `tools/argos/report.py` to add visibility for:
- how many items succeeded through HTML extraction
- how many remain unresolved after landing-page parsing
- which domains most often require landing-page extraction

## Bite-sized execution plan

### Task 1: Add route metadata without breaking current classifier callers

Files:
- modify `tools/argos/classifier.py`
- modify `tests/argos/test_classifier.py`
- add `tests/argos/test_routing.py`

Implementation:
- keep `classify_source()` working for existing tests
- add `build_route(url: str)` returning route policy metadata
- define per-domain route presets for current major sources:
  - `gallica.bnf.fr`
  - `www.europeana.eu` / `europeana.eu`
  - `loc.gov` / `www.loc.gov`
  - `en.numista.com` / `numista.com`
  - `colnect.com`
  - `www.britishmuseum.org`
  - generic direct/unknown fallback

Tests to add:
- route for Numista is HTML/browser-heavy and restricted
- route for Gallica allows IIIF probe first
- generic unknown route allows HTML extraction but not unrestricted browser capture

Verification commands:
- `python -m unittest tests.argos.test_classifier -v`
- `python -m unittest tests.argos.test_routing -v`

### Task 2: Introduce HTML extraction module

Files:
- add `tools/argos/protocols/html.py`
- add `tests/argos/test_html_extraction.py`

Implementation:
- implement `extract_landing_page_candidates(html_text: str, page_url: str) -> dict`
- support deterministic extraction from meta tags, img tags, srcset, manifest-like JSON, and obvious download anchors
- implement a small candidate scoring function
- detect IIIF manifest and image endpoints distinctly from generic image URLs

Fixtures to include inside tests:
- inline HTML with `og:image`
- inline HTML with relative `<img src>`
- inline HTML containing a IIIF manifest URL in JSON
- inline HTML with multiple candidates where the higher-resolution explicit download should win

Verification commands:
- `python -m unittest tests.argos.test_html_extraction -v`

### Task 3: Teach direct fetch to surface HTML landing pages cleanly

Files:
- modify `tools/argos/protocols/direct.py`
- modify `tests/argos/test_protocols_core.py`

Implementation:
- add a mode that returns `html_landing_page` instead of collapsing HTML into `unexpected_content_type`
- preserve old behavior for clearly non-HTML, non-image mismatches
- include returned page body and final URL only in memory; do not save HTML to the asset destination path
- keep retry behavior and SSL fallback behavior unchanged for actual image fetches

Tests to add:
- HTML response returns `failure_class == "html_landing_page"`
- returned payload includes `content_type`, `response_url`, and HTML text snippet/body
- non-HTML text or JSON still maps to `unexpected_content_type`

Verification commands:
- `python -m unittest tests.argos.test_protocols_core -v`

### Task 4: Insert HTML extraction into item acquisition orchestration

Files:
- modify `tools/scripts/argos_acquire_item.py`
- modify `tests/argos/test_acquire_item.py`

Implementation:
- when direct/unknown fetch returns `html_landing_page`, call HTML extraction
- retry the best extracted image candidate via direct fetch
- if extraction yields IIIF manifest candidates, call new IIIF parser path before browser fallback
- persist extracted selection details into `provenance.metadata`
- add attempt step names: `html-extract`, `html-asset-direct`, `html-iiif`

Tests to add:
- HTML page with `og:image` resolves to successful direct asset download
- HTML page with IIIF manifest candidate resolves through IIIF fetch
- HTML page with only low-confidence candidates ends as `failed` with metadata showing candidate count
- restricted route escalates to Playwright only when policy says allowed

Verification commands:
- `python -m unittest tests.argos.test_acquire_item -v`

### Task 5: Implement real IIIF manifest parsing hook

Files:
- modify `tools/argos/protocols/iiif.py`
- add `tests/argos/test_iiif_manifest_parser.py`
- optionally expand `tests/argos/test_protocols_core.py`

Implementation:
- add `fetch_iiif_manifest()` and `extract_first_canvas_image()`
- support common Presentation 2 and Presentation 3 shapes
- keep existing pattern discovery for Gallica/Europeana/LOC
- allow HTML extraction to pass discovered manifest URLs directly into the parser

Tests to add:
- parse Presentation 2 manifest fixture to image URL
- parse Presentation 3 manifest fixture to image URL
- fail cleanly when manifest is valid JSON but lacks extractable image service

Verification commands:
- `python -m unittest tests.argos.test_iiif_manifest_parser -v`
- `python -m unittest tests.argos.test_protocols_core -v`

### Task 6: Upgrade browser fallback from screenshot-only to controlled asset retrieval

Files:
- modify `tools/argos/protocols/playwright_fallback.py`
- add `tests/argos/test_playwright_fallback.py`

Implementation:
- add a DOM/response-inspection path to capture actual image assets
- restrict captured assets to same-domain or route-approved asset domains
- keep screenshot fallback as last resort, explicitly tagged in metadata

Tests to add:
- restricted domain without explicit allowance still returns `manual_required`
- allowed browser run can emit `browser_capture_mode == "asset"`
- screenshot fallback remains available when asset capture fails

Verification commands:
- `python -m unittest tests.argos.test_playwright_fallback -v`

### Task 7: Make dispatch domain-aware instead of only domain-bucketed

Files:
- modify `tools/scripts/argos_prepare_dispatch.py`
- modify `tests/argos/test_dispatch.py`

Implementation:
- keep existing domain grouping, but add route-aware priority metadata in each dispatch group:
  - `route_family`
  - `html_extraction_expected`
  - `browser_restricted`
  - `iiif_capable`
- group “HTML-first direct” domains distinctly from ordinary direct-image domains where useful
- preserve deterministic output ordering

Tests to add:
- unknown HTML-first routes stay separate from clean IIIF groups
- restricted browser domains remain grouped in a way that signals operator caution

Verification commands:
- `python -m unittest tests.argos.test_dispatch -v`
- `python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json --max-groups 6`

### Task 8: Extend report and runbook for the new behavior

Files:
- modify `tools/argos/report.py`
- modify `tests/argos/test_report.py`
- modify `docs/ARGOS_RUNBOOK.md`

Implementation:
- add report lines for HTML extraction successes/failures
- add next-action guidance for unresolved landing-page extraction cases
- document new operator checks and any new CLI flags or step names

Tests to add:
- report renders landing-page extraction follow-up text when such attempts exist
- report highlights browser screenshot vs asset capture distinction

Verification commands:
- `python -m unittest tests.argos.test_report -v`
- `python tools/scripts/argos_report.py --manifest data/raw/argos/manifest.json`

## Suggested implementation order

1. Task 2 first in practice if you want fastest TDD loop (`html.py` is self-contained)
2. Task 3 next to make direct fetch return structured HTML results
3. Task 4 to wire HTML extraction into acquisition
4. Task 5 for real IIIF manifest parsing
5. Task 1 and Task 7 to formalize domain-aware routing/dispatch
6. Task 6 for controlled browser asset retrieval
7. Task 8 for report/runbook polish

If strictly minimizing risk, do this sequence instead:
1. Task 1
2. Task 2
3. Task 3
4. Task 4
5. Task 5
6. Task 8
7. Task 7
8. Task 6

## Exact verification pass for the whole feature slice

From repo root:

```bash
conda activate iconocracy
python -m unittest tests.argos.test_classifier -v
python -m unittest tests.argos.test_routing -v
python -m unittest tests.argos.test_html_extraction -v
python -m unittest tests.argos.test_protocols_core -v
python -m unittest tests.argos.test_iiif_manifest_parser -v
python -m unittest tests.argos.test_acquire_item -v
python -m unittest tests.argos.test_playwright_fallback -v
python -m unittest tests.argos.test_dispatch -v
python -m unittest tests.argos.test_report -v
python tools/scripts/validate_schemas.py data/raw/argos/manifest.json --schema argos-manifest
python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json --max-groups 6
python tools/scripts/argos_report.py --manifest data/raw/argos/manifest.json
```

## Focused integration smoke tests to run after implementation

### Smoke test 1: HTML landing page -> direct asset
- create a test manifest item whose source URL returns HTML with `og:image`
- expected result: `status == success`
- expected attempts include `direct`, `html-extract`, `html-asset-direct`
- expected `provenance.metadata.selected_asset_url` populated

### Smoke test 2: HTML landing page -> IIIF manifest
- create a test manifest item whose landing page exposes a IIIF manifest URL
- expected result: success through `html-iiif` or `iiif`
- expected `provenance.metadata.iiif_manifest_url` populated

### Smoke test 3: restricted domain -> controlled browser asset retrieval
- use mocked Playwright flow
- expected result: either real asset capture or explicit manual requirement
- screenshot-only outcomes must be clearly marked as such

### Smoke test 4: unresolved HTML page
- landing page yields only low-confidence or placeholder assets
- expected result: `failed` or `manual`
- expected report guidance points operator to inspect embedded media/download links

## Risks and guardrails

1. Over-eager extraction could download thumbnails instead of canonical assets.
   - Guardrail: candidate scoring + minimum byte thresholds + explicit metadata showing candidate kind/score.

2. Browser retrieval can drift into uncontrolled scraping.
   - Guardrail: preserve restricted-domain policy and asset-host allowlists.

3. Schema churn can break manifest validation mid-iteration.
   - Guardrail: add new details under `provenance.metadata` first; only widen schema if a new top-level field becomes unavoidable.

4. HTML extraction can become a mini crawler if left unconstrained.
   - Guardrail: single-page parsing only in this iteration; no follow-link crawling.

## Definition of done for this plan

The iteration is done when all of the following are true:
- ARGOS no longer treats HTML landing pages as terminal direct-download failures by default
- at least one deterministic HTML extraction path can convert a landing page into a real asset URL
- IIIF manifest URLs found in HTML can be parsed beyond hard-coded pattern heuristics
- browser fallback can distinguish real asset capture from screenshot fallback
- dispatch and reporting expose which domains/routes are HTML-first or browser-restricted
- the unittest suite above passes
- `docs/ARGOS_RUNBOOK.md` documents the new path clearly

## Expected file touch list

Likely new files:
- `tools/argos/protocols/html.py`
- `tests/argos/test_html_extraction.py`
- `tests/argos/test_routing.py`
- `tests/argos/test_iiif_manifest_parser.py`
- `docs/plans/2026-04-14-argos-html-landing-page-extraction-plan.md`

Likely modified files:
- `tools/argos/classifier.py`
- `tools/argos/protocols/direct.py`
- `tools/argos/protocols/iiif.py`
- `tools/argos/protocols/playwright_fallback.py`
- `tools/argos/report.py`
- `tools/scripts/argos_acquire_item.py`
- `tools/scripts/argos_prepare_dispatch.py`
- `tests/argos/test_classifier.py`
- `tests/argos/test_protocols_core.py`
- `tests/argos/test_acquire_item.py`
- `tests/argos/test_dispatch.py`
- `tests/argos/test_report.py`
- `docs/ARGOS_RUNBOOK.md`

## Short recommendation

Implement the first usable vertical slice as:
1. `html.py`
2. `direct.py` HTML-aware result
3. `argos_acquire_item.py` HTML extraction retry
4. tests proving `og:image` and IIIF manifest extraction

That slice will deliver the highest immediate improvement for ARGOS while setting up the IIIF, browser, and route-policy hooks needed for the next pass.
