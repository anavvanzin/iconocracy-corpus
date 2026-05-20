# ARGOS Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build ARGOS (“Archive Retrieval & Governance Orchestrator for Sources”), an autonomous corpus-acquisition orchestrator that inventories pending archive sources, classifies their acquisition protocol, dispatches one parallel subagent per source/domain, records auditable results in `manifest.json`, stores binaries on SSD or staging with provenance sidecars, and generates a committed report of successes, partial successes, and manual-intervention cases.

**Architecture:** Keep acquisition logic in Python under `tools/argos/` and expose it through thin CLI wrappers in `tools/scripts/`. The agent runtime is responsible for parallel Task/subagent dispatch, but repo code must make dispatch deterministic by producing a validated manifest, source-group worklists, atomic manifest updates, and a final markdown report. All binary outputs stay off-git on `/Volumes/ICONOCRACIA` or `data/raw/.staging/`; only metadata (`manifest.json`, `report.md`, provenance sidecars under staging if needed) and code are committed.

**Tech Stack:** Python stdlib, `jsonschema`, `requests`, optional `playwright`, existing repo helpers (`enrich_iiif.py`, `download_corpus_images.py`, `log_agent_run.py`, `validate_schemas.py`).

---

## What gets better vs. the old plan

1. Use current repo facts, not stale assumptions:
   - `corpus/corpus-data.json` currently has 165 items.
   - `data/processed/records.jsonl` currently has 139 records.
   - `data/raw/drive-manifest.json` exists but `items` is empty.
2. Define “pending acquisition” from the actual raw-binary contract:
   - an item is pending when it has a source URL but no entry in `drive-manifest.json.items` and no verified local acquisition recorded in ARGOS metadata.
   - missing `thumbnail_url` is a prioritization signal, not the sole pending criterion.
3. Keep the runtime boundary clean:
   - Python code should not try to invoke the Task tool directly.
   - Python prepares deterministic source groups; Hermes/Claude runtime reads those groups and spawns one Task/subagent per source.
4. Use stdlib `unittest` for repo-local tests instead of assuming pytest.
5. Extend existing validation tooling instead of inventing a second schema validator.

---

## Scope

In scope:
- build a validated ARGOS manifest
- classify each pending source by protocol: `iiif`, `direct`, `playwright-required`, `blocked`, `unknown`
- attempt acquisition via protocol chain
- on 403/block: try IIIF discovery, then Playwright fallback where allowed
- write success/failure back to manifest atomically
- write provenance sidecar per downloaded artifact
- generate `data/raw/argos/report.md`
- produce per-source worklists for parallel subagents
- commit code + committed metadata outputs (`manifest.json`, `report.md`)

Out of scope for this iteration:
- automatic migration from `.staging` to SSD after remount
- authenticated scraping flows
- browser-cookie/session persistence
- modifying `records.jsonl` or `corpus/corpus-data.json` directly
- committing binaries into git

---

## Implementation notes from repo inspection

Relevant existing files:
- `tools/scripts/hunt.py` — archive/domain patterns and query logic
- `tools/scripts/enrich_iiif.py` — IIIF URL construction heuristics
- `tools/scripts/download_corpus_images.py` — retry, SSL fallback, destination naming
- `tools/scripts/log_agent_run.py` — operational run log, but must be extended to accept `argos`
- `tools/scripts/validate_schemas.py` — existing schema validation path
- `.gitignore` — already excludes many local artifacts, but not ARGOS staging/lock paths
- `docs/scripts.md` and `CLAUDE.md` — need updated operational documentation

Planned new directories/files:
- `tools/argos/`
- `tools/argos/protocols/`
- `tests/argos/`
- `docs/plans/`
- `data/raw/argos/`

---

### Task 1: Create ARGOS module scaffold and test package

**Objective:** Create the minimum file structure so later tasks stay small and predictable.

**Files:**
- Create: `tools/argos/__init__.py`
- Create: `tools/argos/protocols/__init__.py`
- Create: `tests/argos/__init__.py`
- Create: `tests/argos/fixtures/__init__.py`

**Step 1: Write failing smoke test**

```python
from pathlib import Path


def test_argos_package_exists():
    assert Path("tools/argos/__init__.py").exists()
    assert Path("tools/argos/protocols/__init__.py").exists()
```

**Step 2: Run test to verify failure**

Run: `python -m unittest tests.argos.test_smoke -v`
Expected: FAIL — missing files/module.

**Step 3: Create minimal files**

```python
# tools/argos/__init__.py
"""ARGOS acquisition orchestration package."""

# tools/argos/protocols/__init__.py
"""Protocol adapters for ARGOS."""
```

**Step 4: Add smoke test file**

Create `tests/argos/test_smoke.py` with the failing test above.

**Step 5: Run test to verify pass**

Run: `python -m unittest tests.argos.test_smoke -v`
Expected: PASS.

**Step 6: Commit**

```bash
git add tools/argos/__init__.py tools/argos/protocols/__init__.py tests/argos/__init__.py tests/argos/fixtures/__init__.py tests/argos/test_smoke.py
git commit -m "test: add ARGOS package scaffold"
```

---

### Task 2: Implement source-domain classifier and protocol taxonomy

**Objective:** Create one canonical place for domain → protocol mapping and policy flags.

**Files:**
- Create: `tools/argos/classifier.py`
- Test: `tests/argos/test_classifier.py`

**Step 1: Write failing tests**

```python
import unittest
from tools.argos.classifier import classify_source


class ClassifierTests(unittest.TestCase):
    def test_gallica_is_iiif(self):
        result = classify_source("https://gallica.bnf.fr/ark:/12148/btv1b...")
        self.assertEqual(result.protocol, "iiif")
        self.assertEqual(result.domain, "gallica.bnf.fr")

    def test_numista_requires_playwright(self):
        result = classify_source("https://en.numista.com/catalogue/exonumia123.html")
        self.assertEqual(result.protocol, "playwright-required")

    def test_british_museum_is_blocked_prone(self):
        result = classify_source("https://www.britishmuseum.org/collection/object/...")
        self.assertEqual(result.protocol, "blocked")
```

**Step 2: Run test to verify failure**

Run: `python -m unittest tests.argos.test_classifier -v`
Expected: FAIL — `tools.argos.classifier` missing.

**Step 3: Write minimal implementation**

```python
from dataclasses import dataclass
from urllib.parse import urlparse


PROTOCOL_MAP = {
    "gallica.bnf.fr": "iiif",
    "loc.gov": "iiif",
    "www.loc.gov": "iiif",
    "rijksmuseum.nl": "iiif",
    "www.europeana.eu": "iiif",
    "europeana.eu": "iiif",
    "commons.wikimedia.org": "direct",
    "en.wikipedia.org": "direct",
    "bildindex.de": "direct",
    "www.iwm.org.uk": "direct",
    "collections.vam.ac.uk": "direct",
    "numista.com": "playwright-required",
    "en.numista.com": "playwright-required",
    "colnect.com": "playwright-required",
    "www.britishmuseum.org": "blocked",
    "britishmuseum.org": "blocked",
}


@dataclass(frozen=True)
class SourceClass:
    domain: str
    protocol: str


def classify_source(url: str) -> SourceClass:
    domain = urlparse(url).netloc.lower()
    protocol = PROTOCOL_MAP.get(domain, "unknown")
    return SourceClass(domain=domain, protocol=protocol)
```

**Step 4: Run test to verify pass**

Run: `python -m unittest tests.argos.test_classifier -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add tools/argos/classifier.py tests/argos/test_classifier.py
git commit -m "feat: add ARGOS source classifier"
```

---

### Task 3: Implement storage-tier resolution and provenance sidecars

**Objective:** Resolve SSD vs staging safely and write sidecar metadata for every successful download.

**Files:**
- Create: `tools/argos/storage.py`
- Create: `tools/argos/provenance.py`
- Test: `tests/argos/test_storage.py`

**Step 1: Write failing tests**

```python
import tempfile
import unittest
from pathlib import Path
from tools.argos.storage import resolve_storage_root
from tools.argos.provenance import build_provenance_record


class StorageTests(unittest.TestCase):
    def test_falls_back_to_staging_when_ssd_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            root, tier = resolve_storage_root(repo_root, ssd_root=repo_root / "missing-ssd")
            self.assertEqual(tier, "staging")
            self.assertTrue(str(root).endswith("data/raw/.staging"))

    def test_provenance_contains_required_keys(self):
        record = build_provenance_record(
            item_id="FR-001",
            source_url="https://gallica.bnf.fr/...",
            fetched_by="argos/subagent-gallica",
            protocol="iiif",
            storage_tier="staging",
        )
        self.assertIn("fetched_at", record)
        self.assertEqual(record["protocol"], "iiif")
```

**Step 2: Run test to verify failure**

Run: `python -m unittest tests.argos.test_storage -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

```python
# tools/argos/storage.py
from pathlib import Path

SSD_ROOT = Path("/Volumes/ICONOCRACIA/corpus/imagens")
STAGING_ROOT = Path("data/raw/.staging")


def resolve_storage_root(repo_root: Path, ssd_root: Path = SSD_ROOT):
    if ssd_root.is_dir():
        return ssd_root, "ssd"
    staging = repo_root / STAGING_ROOT
    staging.mkdir(parents=True, exist_ok=True)
    return staging, "staging"
```

```python
# tools/argos/provenance.py
from datetime import datetime, timezone


def build_provenance_record(item_id, source_url, fetched_by, protocol, storage_tier, license_hint=None):
    return {
        "item_id": item_id,
        "source_url": source_url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "fetched_by": fetched_by,
        "protocol": protocol,
        "storage_tier": storage_tier,
        "license_hint": license_hint,
        "user_agent": "ARGOS/1.0 (+iconocracy-research; ana.vanzin@ufsc.br)",
    }
```

**Step 4: Run test to verify pass**

Run: `python -m unittest tests.argos.test_storage -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add tools/argos/storage.py tools/argos/provenance.py tests/argos/test_storage.py
git commit -m "feat: add ARGOS storage and provenance helpers"
```

---

### Task 4: Add ARGOS manifest schema and wire it into the validator

**Objective:** Make `manifest.json` a first-class validated artifact.

**Files:**
- Create: `tools/schemas/argos-manifest.schema.json`
- Modify: `tools/scripts/validate_schemas.py`
- Test: `tests/argos/test_manifest_schema.py`

**Step 1: Write failing test**

```python
import unittest
from tools.scripts.validate_schemas import load_schema


class ManifestSchemaTests(unittest.TestCase):
    def test_argos_manifest_schema_loads(self):
        schema = load_schema("argos-manifest")
        self.assertEqual(schema["title"], "ArgosManifest")
```

**Step 2: Run test to verify failure**

Run: `python -m unittest tests.argos.test_manifest_schema -v`
Expected: FAIL — schema/choice missing.

**Step 3: Create schema**

Required top-level keys:
- `manifest_version`
- `generated_at`
- `storage_root`
- `storage_tier`
- `summary`
- `items`

Required per-item keys:
- `item_id`
- `title`
- `source_url`
- `source_domain`
- `protocol`
- `status`
- `failure_class`
- `failure_reason`
- `attempts`
- `local_path`
- `sha256`
- `provenance`

Use enums for:
- protocol: `iiif`, `direct`, `playwright-required`, `blocked`, `unknown`
- status: `pending`, `success`, `partial`, `failed`, `manual`

**Step 4: Extend validator choices**

Add `argos-manifest` to `choices=[...]` in `validate_schemas.py`.

**Step 5: Run test to verify pass**

Run: `python -m unittest tests.argos.test_manifest_schema -v`
Expected: PASS.

**Step 6: Commit**

```bash
git add tools/schemas/argos-manifest.schema.json tools/scripts/validate_schemas.py tests/argos/test_manifest_schema.py
git commit -m "feat: add ARGOS manifest schema"
```

---

### Task 5: Build manifest generation from corpus + drive-manifest

**Objective:** Generate `data/raw/argos/manifest.json` from actual pending acquisition needs.

**Files:**
- Create: `tools/argos/manifest.py`
- Create: `tools/scripts/argos_build_manifest.py`
- Test: `tests/argos/test_manifest_builder.py`

**Step 1: Write failing test**

```python
import unittest
from tools.argos.manifest import build_manifest


class ManifestBuilderTests(unittest.TestCase):
    def test_marks_item_pending_when_missing_from_drive_manifest(self):
        corpus = [{"id": "FR-001", "title": "Test", "url": "https://gallica.bnf.fr/ark:/...", "thumbnail_url": None}]
        drive_manifest = {"items": []}
        manifest = build_manifest(corpus, drive_manifest, storage_root="data/raw/.staging", storage_tier="staging")
        self.assertEqual(manifest["items"][0]["status"], "pending")
        self.assertEqual(manifest["items"][0]["protocol"], "iiif")
```

**Step 2: Run test to verify failure**

Run: `python -m unittest tests.argos.test_manifest_builder -v`
Expected: FAIL.

**Step 3: Write minimal implementation**

Core rules:
- source URL field = `item["url"]`
- skip items with no source URL
- pending if item id not present in `drive-manifest.json.items[*].item_id`
- include `thumbnail_missing: true/false` as prioritization metadata
- compute `source_domain` and `protocol` via `classify_source()`
- include `dispatch_group` = source domain, except blocked/unknown low-volume domains may later be bundled by dispatcher

**Step 4: Create CLI**

`tools/scripts/argos_build_manifest.py` should support:
- `--dry-run`
- `--output data/raw/argos/manifest.json`
- `--limit N`

**Step 5: Verify with command**

Run:
```bash
python tools/scripts/argos_build_manifest.py --dry-run
python tools/scripts/argos_build_manifest.py
python tools/scripts/validate_schemas.py data/raw/argos/manifest.json --schema argos-manifest
```
Expected:
- dry-run prints pending count and protocol breakdown
- manifest file created
- schema validation passes

**Step 6: Commit**

```bash
git add tools/argos/manifest.py tools/scripts/argos_build_manifest.py tests/argos/test_manifest_builder.py data/raw/argos/manifest.json
git commit -m "feat: add ARGOS manifest builder"
```

---

### Task 6: Add atomic locked manifest updates

**Objective:** Ensure every subagent writeback is safe under parallel execution.

**Files:**
- Modify: `tools/argos/manifest.py`
- Create: `tools/scripts/argos_manifest_update.py`
- Test: `tests/argos/test_manifest_update.py`

**Step 1: Write failing test**

```python
import json
import tempfile
import unittest
from pathlib import Path
from tools.argos.manifest import locked_update_manifest


class ManifestUpdateTests(unittest.TestCase):
    def test_updates_single_item_without_dropping_others(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(json.dumps({"items": [{"item_id": "FR-001", "status": "pending"}, {"item_id": "FR-002", "status": "pending"}]}), encoding="utf-8")
            locked_update_manifest(path, "FR-001", {"status": "success"})
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["items"][0]["status"], "success")
            self.assertEqual(data["items"][1]["status"], "pending")
```

**Step 2: Run test to verify failure**

Run: `python -m unittest tests.argos.test_manifest_update -v`
Expected: FAIL.

**Step 3: Implement lock helper**

Requirements:
- lock file: `data/raw/argos/manifest.lock`
- write backup: `manifest.json.bak`
- fsync before replace
- reject empty/invalid JSON
- revalidate schema after merge, before final write

**Step 4: Create CLI wrapper**

Command shape:
```bash
python tools/scripts/argos_manifest_update.py --item-id FR-001 --patch '{"status":"success"}'
```

**Step 5: Run test to verify pass**

Run: `python -m unittest tests.argos.test_manifest_update -v`
Expected: PASS.

**Step 6: Commit**

```bash
git add tools/argos/manifest.py tools/scripts/argos_manifest_update.py tests/argos/test_manifest_update.py
git commit -m "feat: add ARGOS atomic manifest updates"
```

---

### Task 7: Implement direct + IIIF acquisition helpers reusing existing repo logic

**Objective:** Handle the two most common acquisition paths before adding browser fallback.

**Files:**
- Create: `tools/argos/protocols/direct.py`
- Create: `tools/argos/protocols/iiif.py`
- Test: `tests/argos/test_protocols_core.py`

**Step 1: Write failing tests**

```python
import unittest
from tools.argos.protocols.iiif import gallica_manifest_from_ark
from tools.argos.protocols.direct import classify_http_failure


class ProtocolCoreTests(unittest.TestCase):
    def test_gallica_manifest_from_ark(self):
        self.assertIn("manifest.json", gallica_manifest_from_ark("ark:/12148/btv1b12345"))

    def test_403_maps_to_blocked_failure(self):
        self.assertEqual(classify_http_failure(403), "403_block")
```

**Step 2: Run test to verify failure**

Run: `python -m unittest tests.argos.test_protocols_core -v`
Expected: FAIL.

**Step 3: Implement IIIF helper**

Reuse patterns from `tools/scripts/enrich_iiif.py`:
- Gallica ARK → manifest + image URL
- LoC resource/API heuristic
- Europeana manifest heuristic

Minimal public functions:
- `discover_iiif(item: dict) -> dict | None`
- `fetch_iiif_image(item: dict, dest_path: Path) -> AttemptResult`
- `gallica_manifest_from_ark(ark: str) -> str`

**Step 4: Implement direct helper**

Reuse patterns from `download_corpus_images.py`:
- requests with retry + backoff
- SSL fallback classification
- `Retry-After` support
- map status codes to failure classes

Minimal public functions:
- `fetch_direct(url: str, dest_path: Path) -> AttemptResult`
- `classify_http_failure(status_code: int) -> str`

**Step 5: Run tests to verify pass**

Run: `python -m unittest tests.argos.test_protocols_core -v`
Expected: PASS.

**Step 6: Commit**

```bash
git add tools/argos/protocols/direct.py tools/argos/protocols/iiif.py tests/argos/test_protocols_core.py
git commit -m "feat: add ARGOS direct and IIIF protocols"
```

---

### Task 8: Implement optional Playwright fallback and blocked-policy handling

**Objective:** Handle JS-heavy and blocked domains without making Playwright mandatory.

**Files:**
- Create: `tools/argos/protocols/playwright_fallback.py`
- Test: `tests/argos/test_playwright_fallback.py`

**Step 1: Write failing test**

```python
import unittest
from tools.argos.protocols.playwright_fallback import playwright_available


class PlaywrightFallbackTests(unittest.TestCase):
    def test_playwright_probe_returns_bool(self):
        self.assertIn(playwright_available(), [True, False])
```

**Step 2: Run test to verify failure**

Run: `python -m unittest tests.argos.test_playwright_fallback -v`
Expected: FAIL.

**Step 3: Implement minimal adapter**

Required behavior:
- `playwright_available()` soft-imports package
- `fetch_with_playwright(url, dest_path)` only runs when import succeeds
- on missing package: return `failure_class="playwright_unavailable"`, `status="manual"`
- on blocked domains with explicit TOS concerns (e.g. `numista`, `colnect`), default to manual unless the manifest item has `playwright_allowed: true`

**Step 4: Run test to verify pass**

Run: `python -m unittest tests.argos.test_playwright_fallback -v`
Expected: PASS.

**Step 5: Commit**

```bash
git add tools/argos/protocols/playwright_fallback.py tests/argos/test_playwright_fallback.py
git commit -m "feat: add ARGOS playwright fallback"
```

---

### Task 9: Implement per-item worker with fallback chain and provenance writes

**Objective:** Create the single deterministic worker each subagent will call.

**Files:**
- Create: `tools/scripts/argos_acquire_item.py`
- Modify: `tools/scripts/log_agent_run.py`
- Test: `tests/argos/test_acquire_item.py`

**Step 1: Write failing test**

```python
import unittest
from tools.scripts.argos_acquire_item import infer_next_step


class AcquireItemTests(unittest.TestCase):
    def test_403_moves_to_iiif_discovery(self):
        attempt = {"status_code": 403, "failure_class": "403_block"}
        self.assertEqual(infer_next_step(protocol="direct", last_attempt=attempt), "iiif-discovery")
```

**Step 2: Run test to verify failure**

Run: `python -m unittest tests.argos.test_acquire_item -v`
Expected: FAIL.

**Step 3: Implement worker state machine**

State chain:
1. load manifest item by `item_id`
2. resolve destination root + tier
3. attempt protocol-specific acquisition
4. on 401/403/429/block signatures:
   - try `discover_iiif()`
   - if IIIF discovery fails and domain allows browser escalation, try Playwright
5. write file + compute sha256
6. write provenance sidecar `{item_id}.meta.json`
7. update manifest through `argos_manifest_update.py`
8. log via `log_agent_run.py --agent argos ...`

**Step 4: Extend `log_agent_run.py`**

Add `argos` to:
```python
choices=['validate', 'scout', 'iconocode', 'sync', 'lacunas', 'download', 'refresh', 'purification', 'argos']
```

**Step 5: Smoke-test command**

Run:
```bash
python tools/scripts/argos_acquire_item.py --item-id FR-013 --dry-run
```
Expected:
- prints ordered attempt plan
- does not mutate manifest on dry-run

**Step 6: Commit**

```bash
git add tools/scripts/argos_acquire_item.py tools/scripts/log_agent_run.py tests/argos/test_acquire_item.py
git commit -m "feat: add ARGOS acquisition worker"
```

---

### Task 10: Implement source grouping for parallel Task/subagent dispatch

**Objective:** Prepare deterministic worklists so the runtime can spawn one subagent per source/domain.

**Files:**
- Create: `tools/scripts/argos_prepare_dispatch.py`
- Test: `tests/argos/test_dispatch.py`

**Step 1: Write failing test**

```python
import unittest
from tools.scripts.argos_prepare_dispatch import build_dispatch_groups


class DispatchTests(unittest.TestCase):
    def test_one_group_per_source_domain_with_longtail_bundle(self):
        items = [
            {"item_id": "FR-001", "source_domain": "gallica.bnf.fr", "status": "pending"},
            {"item_id": "FR-002", "source_domain": "gallica.bnf.fr", "status": "pending"},
            {"item_id": "UK-001", "source_domain": "britishmuseum.org", "status": "pending"},
        ]
        groups = build_dispatch_groups(items, max_groups=6)
        self.assertTrue(any(group["group_name"] == "gallica.bnf.fr" for group in groups))
```

**Step 2: Run test to verify failure**

Run: `python -m unittest tests.argos.test_dispatch -v`
Expected: FAIL.

**Step 3: Implement grouping logic**

Rules:
- one group per top-volume source domain
- cap at 6 groups
- merge very small/blocked/unknown domains into `longtail`
- emit JSON array with:
  - `group_name`
  - `protocol`
  - `item_ids`
  - `prompt_hint`

**Step 4: Add CLI**

Run:
```bash
python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json
```
Expected: JSON printed to stdout for agent runtime consumption.

**Step 5: Commit**

```bash
git add tools/scripts/argos_prepare_dispatch.py tests/argos/test_dispatch.py
git commit -m "feat: add ARGOS dispatch grouping"
```

---

### Task 11: Implement markdown report generation

**Objective:** Generate a committed report that summarizes successes, partials, failures, and manual intervention.

**Files:**
- Create: `tools/argos/report.py`
- Create: `tools/scripts/argos_report.py`
- Test: `tests/argos/test_report.py`

**Step 1: Write failing test**

```python
import unittest
from tools.argos.report import build_report_markdown


class ReportTests(unittest.TestCase):
    def test_report_includes_manual_intervention_section(self):
        manifest = {
            "summary": {"success": 1, "manual": 1},
            "items": [
                {"item_id": "FR-001", "status": "success", "source_domain": "gallica.bnf.fr"},
                {"item_id": "UK-001", "status": "manual", "failure_class": "403_block", "source_url": "https://example.org", "source_domain": "britishmuseum.org"},
            ],
        }
        text = build_report_markdown(manifest)
        self.assertIn("Manual-intervention cases", text)
        self.assertIn("UK-001", text)
```

**Step 2: Run test to verify failure**

Run: `python -m unittest tests.argos.test_report -v`
Expected: FAIL.

**Step 3: Implement report builder**

Sections:
1. run metadata
2. summary counts
3. per-domain breakdown
4. failure taxonomy
5. manual-intervention checklist
6. next-action suggestions

**Step 4: Create CLI wrapper**

Run:
```bash
python tools/scripts/argos_report.py --manifest data/raw/argos/manifest.json --output data/raw/argos/report.md
```
Expected: markdown file written.

**Step 5: Run test to verify pass**

Run: `python -m unittest tests.argos.test_report -v`
Expected: PASS.

**Step 6: Commit**

```bash
git add tools/argos/report.py tools/scripts/argos_report.py tests/argos/test_report.py data/raw/argos/report.md
git commit -m "feat: add ARGOS acquisition report"
```

---

### Task 12: Wire docs, ignore rules, and operational commands

**Objective:** Make ARGOS discoverable and safe in the repo workflow.

**Files:**
- Modify: `.gitignore`
- Modify: `CLAUDE.md`
- Modify: `docs/scripts.md`

**Step 1: Write failing smoke test**

No code test here; use verification commands instead.

**Step 2: Update `.gitignore`**

Add:
```gitignore
data/raw/.staging/
data/raw/argos/manifest.lock
data/raw/argos/*.bak
```

**Step 3: Update `CLAUDE.md`**

Add quick commands:
```bash
python tools/scripts/argos_build_manifest.py
python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json
python tools/scripts/argos_report.py
```

Add routing trigger row:
- `argos`, `acquisition`, `orquestrar aquisicao` → ARGOS mode

**Step 4: Update `docs/scripts.md`**

Document:
- `argos_build_manifest.py`
- `argos_acquire_item.py`
- `argos_manifest_update.py`
- `argos_prepare_dispatch.py`
- `argos_report.py`

**Step 5: Verify docs changes**

Run:
```bash
git diff -- .gitignore CLAUDE.md docs/scripts.md
```
Expected: only ARGOS-related additions.

**Step 6: Commit**

```bash
git add .gitignore CLAUDE.md docs/scripts.md
git commit -m "docs: document ARGOS workflow"
```

---

### Task 13: End-to-end limited run and commit generated metadata artifacts

**Objective:** Prove the orchestrator works on a safe small slice before any full run.

**Files:**
- Generate: `data/raw/argos/manifest.json`
- Generate: `data/raw/argos/report.md`
- Modify: `corpus/agent-runs.json`

**Step 1: Build fresh manifest**

Run:
```bash
python tools/scripts/argos_build_manifest.py --limit 20
python tools/scripts/validate_schemas.py data/raw/argos/manifest.json --schema argos-manifest
```
Expected:
- manifest generated
- schema valid

**Step 2: Prepare dispatch groups**

Run:
```bash
python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json > /tmp/argos-dispatch.json
```
Expected:
- JSON worklist with <= 6 groups

**Step 3: Manual runtime handoff for parallel subagents**

The agent runtime should read `/tmp/argos-dispatch.json` and spawn one Task/subagent per group.
Each subagent prompt should be constrained to:
- iterate assigned `item_ids`
- call `python tools/scripts/argos_acquire_item.py --item-id <id>`
- never edit manifest directly; always use `argos_manifest_update.py`
- stop on unexpected destructive filesystem actions

**Step 4: Generate report**

Run:
```bash
python tools/scripts/argos_report.py --manifest data/raw/argos/manifest.json --output data/raw/argos/report.md
```
Expected:
- report includes summary, failure taxonomy, manual-intervention checklist

**Step 5: Review git safety**

Run:
```bash
git status --short
```
Expected:
- code files staged or visible
- `data/raw/argos/manifest.json` and `data/raw/argos/report.md` visible
- no binaries from SSD or `.staging/` tracked

**Step 6: Commit metadata artifacts**

```bash
git add tools/argos tools/scripts/argos_*.py tools/schemas/argos-manifest.schema.json tests/argos .gitignore CLAUDE.md docs/scripts.md data/raw/argos/manifest.json data/raw/argos/report.md corpus/agent-runs.json
git commit -m "feat(argos): add autonomous corpus acquisition orchestrator"
```

---

## Verification checklist

Run all of these from repo root after implementation:

```bash
conda activate iconocracy
python -m unittest discover -s tests/argos -v
python tools/scripts/argos_build_manifest.py --dry-run
python tools/scripts/argos_build_manifest.py --limit 20
python tools/scripts/validate_schemas.py data/raw/argos/manifest.json --schema argos-manifest
python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json
python tools/scripts/argos_acquire_item.py --item-id FR-013 --dry-run
python tools/scripts/argos_report.py --manifest data/raw/argos/manifest.json --output data/raw/argos/report.md
git status --short
```

Expected:
- ARGOS unit tests pass
- manifest validates
- dispatch groups are deterministic
- single-item dry-run shows protocol chain
- report is generated
- no binary files appear in git status

---

## Recommended Task/subagent prompt template

When the runtime dispatches a per-source subagent, use this shape:

```text
You are the ARGOS worker for source group <group_name>.
Assigned protocol: <protocol>.
Assigned item_ids: <comma-separated ids>.

For each item_id, run:
python tools/scripts/argos_acquire_item.py --item-id <id>

Rules:
1. Do not edit manifest.json directly.
2. Let the worker write back through argos_manifest_update.py.
3. If you hit 403/block behavior, allow the worker to try IIIF discovery, then Playwright fallback if permitted.
4. Do not commit.
5. Return a short JSON summary with counts by status and the list of manual-intervention item_ids.
```

---

## Final recommendation

Keep the name `ARGOS`.

Why this name wins:
- already fits the thesis’ juridical-surveillance vocabulary
- short and memorable
- distinct from SCOUT and ICONOCODE
- maps naturally to “many-eyed archive watcher” while still sounding like infrastructure

---

Plan complete and saved. Ready to execute using subagent-driven-development — I’ll dispatch a fresh subagent per task with two-stage review (spec compliance then code quality). Shall I proceed?
