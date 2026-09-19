# ARGOS operator runbook

Practical walkthrough for rerunning ARGOS from scratch from the repository root.

Assume you are already inside `iconocracy-corpus/`.

## 0. Preconditions

Activate the project environment first.

```bash
conda activate iconocracy
```

ARGOS uses these repo entrypoints:

- `python tools/scripts/argos_build_manifest.py`
- `python tools/scripts/validate_schemas.py`
- `python tools/scripts/argos_prepare_dispatch.py`
- `python tools/scripts/argos_acquire_item.py`
- `python tools/scripts/argos_report.py`

Optional but relevant:

- Playwright fallback may be needed for `playwright-required` or restricted sources.
- Preferred binary destination is `/Volumes/ICONOCRACIA/corpus/imagens`.
- If that SSD is not mounted, ARGOS falls back to `data/raw/.staging/` inside the repo.

Quick safety check:

```bash
git status --short
```

Do not start a new ARGOS run if you already have unreviewed ARGOS metadata changes mixed with unrelated work.

## 1. Build the manifest from scratch

First inspect without writing:

```bash
python tools/scripts/argos_build_manifest.py --dry-run
```

Then write the operational manifest:

```bash
python tools/scripts/argos_build_manifest.py
```

This writes:

- `data/raw/argos/manifest.json`

Useful variant for a smaller test run:

```bash
python tools/scripts/argos_build_manifest.py --limit 25
```

## 2. Validate the manifest

Validate the generated file against the ARGOS schema:

```bash
python tools/scripts/validate_schemas.py data/raw/argos/manifest.json --schema argos-manifest
```

If validation fails, stop and fix the manifest inputs before dispatching workers.

Current repo note: the manifest presently fails validation on at least one `source_url` containing a non-normalized URI from `bndigital.bnportugal.gov.pt`. Do not treat that as a clean run until corrected.

## 3. Inspect dispatch groups

Generate the deterministic work groups:

```bash
python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json
```

If you want fewer top-level buckets:

```bash
python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json --max-groups 4
```

What this gives you:

- one group per dominant domain when large enough
- a `longtail` group for smaller, blocked, or mixed sources
- the item IDs to assign to operators or subagents

In the current repo state, the main groups are:

- `en.numista.com` (`playwright-required`)
- `www.europeana.eu` (`iiif`)
- `www.loc.gov` (`iiif`)
- `gallica.bnf.fr` (`iiif`)
- `en.wikipedia.org` (`direct`)
- `longtail` (`mixed`)

## 4. Run a worker for one item

Dry-run one item first to confirm the attempt chain and storage target:

```bash
python tools/scripts/argos_acquire_item.py --manifest data/raw/argos/manifest.json --item-id FR-001 --dry-run
```

Then run the real acquisition:

```bash
python tools/scripts/argos_acquire_item.py --manifest data/raw/argos/manifest.json --item-id FR-001
```

If the source is restricted and policy allows browser fallback:

```bash
python tools/scripts/argos_acquire_item.py --manifest data/raw/argos/manifest.json --item-id DE-004 --playwright-allowed
```

Worker behavior:

- updates `data/raw/argos/manifest.json` atomically
- writes the binary to SSD or repo staging
- computes SHA256
- writes a provenance sidecar next to the binary as `*.meta.json`

## 5. Run workers for all items in one dispatch group

There is no dedicated batch runner in the repo right now. The practical pattern is: inspect the group JSON, then loop over the listed item IDs.

Example: run the Gallica group sequentially.

```bash
for item in FR-001 FR-002 FR-003 FR-004 FR-005 FR-006 FR-011 FR-013 FR-014 FR-015 FR-016 FR-017 FR-018 FR-019 FR-020 FR-031 FR-ASSIGNAT-1792; do
  python tools/scripts/argos_acquire_item.py --manifest data/raw/argos/manifest.json --item-id "$item"
done
```

Example: run a browser-dependent group with Playwright allowed.

```bash
for item in BE-5F-LEOPOLD-1832 BE-CONGO-100F-1912 BE-CONGO-1912 BE-IND-1880 BR-1000R-1906 BR-1CR-1970 BR-2000R-1907 BR-50CR-1965 DE-1000M-1910 DE-100M-1908 DE-50M-1919 DE-WR-1924-50PF ES-003 ES-004 FR-CERES-5F-1849 FR-HERC-1870 FR-PIAST-1885 FR-SEM-1898 IT-006 IT-007 PT-006 UK-HALFPENNY-1695 UK-PENNY-1860 UK-PENNY-1895 UK-TRADE-1895 US-EDUC-1896-01 US-SEATED-1840 US-SLQ-1916; do
  python tools/scripts/argos_acquire_item.py --manifest data/raw/argos/manifest.json --item-id "$item" --playwright-allowed
done
```

## 6. Run workers for all dispatch groups

Recommended order:

1. `iiif` groups first
2. `direct` groups second
3. `playwright-required` groups third
4. `longtail` last

Practical workflow:

1. print groups
2. copy the item IDs for one group
3. run one shell loop per group
4. rerun `argos_prepare_dispatch.py` between rounds if needed

Minimum full-pass command sequence:

```bash
python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json
# then run one for-loop per group using the emitted item_ids
```

If you need a controlled pilot before a full pass, rebuild with a limit:

```bash
python tools/scripts/argos_build_manifest.py --limit 25
python tools/scripts/validate_schemas.py data/raw/argos/manifest.json --schema argos-manifest
python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json
```

## 7. Generate the report

After the workers finish, render the report:

```bash
python tools/scripts/argos_report.py --manifest data/raw/argos/manifest.json
```

This writes:

- `data/raw/argos/report.md`

## 8. Inspect outputs

Inspect the top of the manifest:

```bash
python -m json.tool data/raw/argos/manifest.json | head -n 40
```

Inspect the report:

```bash
sed -n '1,120p' data/raw/argos/report.md
```

Check which items still need attention:

```bash
python - <<'PY'
import json
from pathlib import Path
manifest = json.loads(Path('data/raw/argos/manifest.json').read_text())
for item in manifest['items']:
    if item['status'] in {'failed', 'manual', 'pending'}:
        print(item['item_id'], item['status'], item.get('failure_class', ''))
PY
```

Check where binaries actually landed:

```bash
python - <<'PY'
import json
from pathlib import Path
manifest = json.loads(Path('data/raw/argos/manifest.json').read_text())
for item in manifest['items']:
    if item.get('local_path'):
        print(item['item_id'], item['local_path'])
PY
```

## 9. Safety notes

### SSD vs staging

ARGOS prefers:

- `/Volumes/ICONOCRACIA/corpus/imagens`

If the SSD is missing, it falls back automatically to:

- `data/raw/.staging/`

That fallback is operational only. Do not confuse repo staging with canonical raw storage. If you had to use `.staging`, reconcile those binaries manually after the SSD is mounted again.

### Restricted domains and Playwright

Use `--playwright-allowed` only when policy permits browser fallback.

Typical cases:

- `playwright-required`
- `blocked`
- sources that return 401, 403, or 429 and need controlled escalation

If a source requires manual retrieval, let ARGOS mark it as `manual` and preserve the provenance trail instead of forcing repeated blind retries.

### Commits

Commit only ARGOS metadata, not binaries.

Safe ARGOS metadata outputs to review and commit when appropriate:

- `data/raw/argos/manifest.json`
- `data/raw/argos/report.md`

Do not commit downloaded images into git. Raw binaries belong on SSD or Drive, not in repository history.

Before committing, review:

```bash
git status --short
```

If the run changed only ARGOS metadata and those changes are intentional, stage only the metadata files you want in history.

## 10. Canonical rerun checklist

```bash
conda activate iconocracy
python tools/scripts/argos_build_manifest.py --dry-run
python tools/scripts/argos_build_manifest.py
python tools/scripts/validate_schemas.py data/raw/argos/manifest.json --schema argos-manifest
python tools/scripts/argos_prepare_dispatch.py --manifest data/raw/argos/manifest.json
python tools/scripts/argos_acquire_item.py --manifest data/raw/argos/manifest.json --item-id FR-001 --dry-run
# run one real worker or one loop per dispatch group
python tools/scripts/argos_report.py --manifest data/raw/argos/manifest.json
git status --short
```
