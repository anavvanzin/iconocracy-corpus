# Housekeeping Pass Implementation Plan — iconocracy-corpus + Research

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve open issues (#21, #55, #56, #57) and triage open PRs across `anavvanzin/iconocracy-corpus` and `anavvanzin/Research` in one coherent pass.

**Architecture:** Six phases, each gated by verification.
- **A.** Sync the in-flight `.worktrees/export-contract` fix for #56, regenerate `corpus-data.json` with the legacy schema, get tests green, ship PR.
- **B.** Address #57 by generating a manifest of the 100 uncoded items, documenting the partial-coverage policy, and tagging the slim entries with `uncoded-purification` audit flag.
- **C.** Close #55 (empty `[writing]` template).
- **D.** Triage open PRs: subagent-reviewed disposition for the older corpus PRs (#52, #30, #23, #13) and a guided convert→review→decide cycle for Research drafts (#9, #4). Resolve #21 alongside #23.
- **E.** Update `MEMORY.md` (the stale "fix in branch" claim) and `CLAUDE.md` Known Data Issues section.
- **F.** Final report + cleanup of `.worktrees/` directories that are no longer in use.

**Tech Stack:** Python 3.11 (conda env `iconocracy`), pytest, `gh` CLI + GitHub MCP tools, git worktrees. Commits authored as `anavvanzin` with no co-author trailer.

**Decisions already locked in (from this session's brainstorming):**
- #56 schema: **legacy** — `id` is BR-007-style corpus_id, plus country/country_pt/support/medium_norm/year. Records without `corpus_id` in id-mapping.json fall back to the UUID `item_id` so the field still exists.
- #57 policy: **defer with documented queue** — 100 records get an `uncoded-purification` audit flag and an explicit manifest. Health reporting uses the 265 denominator with explicit "coded: 165 / queued: 100" split.
- #56 docs: live as an ADR in `docs/adr/006-corpus-export-schema.md` plus a short cross-reference from `CLAUDE.md`'s Known Data Issues block. We don't keep the schema in three places.
- Old PRs (#52, #30, #23, #13): subagent code review first, disposition (merge / close / convert) after.
- Research PRs (#9, #4): convert from DRAFT, subagent review, then merge-or-close.

---

## Phase A — Fix #56 (export contract regression)

The fix-in-flight at `.worktrees/export-contract` already restored `corpus/corpus-data.json` from commit `5d11823` and patched `tools/scripts/records_to_corpus.py` with id-mapping load + country derivation. **Nothing has been verified yet.** This phase verifies, completes, and ships.

### Task A1 — Confirm the worktree state vs main

**Files:** none modified

- [ ] **Step 1: Confirm worktree HEAD matches main**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus
git rev-parse main
cd .worktrees/export-contract
git rev-parse HEAD
```

Expected: both SHAs are `e7d3cda…` (the WIP-committed main from this session).

If different: in the worktree, run `git fetch && git reset --hard main` (local main, not origin/main, since we have unpushed work).

- [ ] **Step 2: Confirm records.jsonl line count matches between worktrees**

```bash
wc -l ~/Documents/projetos/research/hub/iconocracy-corpus/data/processed/records.jsonl
wc -l ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/export-contract/data/processed/records.jsonl
```

Expected: both 265.

If worktree is 165 while main is 265: investigate why `git reset --hard main` didn't propagate. Likely cause: the worktree was created from an older base and the reset did not run against the current branch tip. Re-run `git reset --hard main` and re-check.

- [ ] **Step 3: Confirm the in-flight edits are still present**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/export-contract
git diff --stat
```

Expected: `corpus/corpus-data.json` and `tools/scripts/records_to_corpus.py` modified. No staged changes.

If edits are missing: pop the stash created during the earlier resync: `git stash list && git stash pop` (only if a relevant stash exists).

### Task A2 — Verify the rich corpus-data.json restoration

**Files:** none modified (verification only)

- [ ] **Step 1: Confirm 165 rich items present**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/export-contract
python3 -c "
import json
d = json.load(open('corpus/corpus-data.json'))
print(f'count={len(d)}')
print(f'has_id={sum(1 for x in d if \"id\" in x)}')
print(f'has_country={sum(1 for x in d if \"country\" in x)}')
print(f'has_support={sum(1 for x in d if \"support\" in x)}')
print(f'has_year={sum(1 for x in d if \"year\" in x)}')
print(f'has_medium_norm={sum(1 for x in d if \"medium_norm\" in x)}')
"
```

Expected:
```
count=165
has_id=165
has_country=165
has_support=165
has_year=165
has_medium_norm=160
```

If counts are different: the restoration didn't take. Re-run `git show 5d11823:corpus/corpus-data.json > corpus/corpus-data.json` in the worktree and verify again.

### Task A3 — Inspect the records_to_corpus.py changes

**Files:** read-only check

- [ ] **Step 1: Inspect the script changes**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/export-contract
git diff tools/scripts/records_to_corpus.py | head -120
```

Expected: the diff shows three additions:
1. `COUNTRY_FROM_PREFIX` and `COUNTRY_PT_FROM_PREFIX` dicts replace the unused `COUNTRY_MAP_REVERSE`.
2. `_load_id_mapping()` and `_country_from_corpus_id()` helpers.
3. `_corpus_entry_from_record(record, existing, corpus_id="")` signature change and id/country derivation logic.
4. `export_corpus()` builds `id_mapping` and passes `corpus_id` through both the merge loop and the new-record loop.

If the diff is missing or partial: re-apply via the Edit commands documented in the prior session, or rewrite by hand (see Task A4 as the reference behavior).

### Task A4 — Write a regression test for the contract

This is the test that lives in `tests/test_corpus_export_idempotent.py` (already exists) plus the existing `tests/test_cross_file_consistency.py`. We need an *additional* test that locks in the schema contract: every corpus item must have `id`, `country`, `country_pt`, plus url-or-placeholder.

**Files:**
- Create: `tests/test_corpus_export_contract.py`

- [ ] **Step 1: Write the failing test**

```python
"""Test the public corpus-data.json schema contract.

Locks in the legacy schema after the #56 regression: every entry carries a stable
`id`, country/country_pt derived from the id prefix, and the rich fields are not
silently dropped on re-export. See docs/adr/006-corpus-export-schema.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
CORPUS = REPO / "corpus" / "corpus-data.json"
ID_MAPPING = REPO / "data" / "processed" / "id-mapping.json"

# Allow new IDs to be added by extending this map. Keep in sync with
# COUNTRY_FROM_PREFIX in tools/scripts/records_to_corpus.py.
KNOWN_PREFIXES = {
    "AR", "AT", "BE", "BR", "CH", "DE", "ES", "EU", "FR",
    "IT", "MX", "NL", "PT", "UK", "US", "UY",
}


@pytest.fixture(scope="module")
def corpus():
    return json.loads(CORPUS.read_text(encoding="utf-8"))


def test_every_entry_has_id(corpus):
    missing = [i for i, item in enumerate(corpus) if not item.get("id")]
    assert not missing, f"entries without id at indices: {missing[:10]}"


def test_id_uniqueness(corpus):
    ids = [item["id"] for item in corpus if item.get("id")]
    assert len(ids) == len(set(ids)), "duplicate ids in corpus-data.json"


def test_country_present_when_prefix_known(corpus):
    """Every entry whose id starts with a known country prefix must have country set."""
    failures = []
    for item in corpus:
        cid = item.get("id", "")
        if "-" not in cid:
            continue
        prefix = cid.split("-", 1)[0]
        if prefix in KNOWN_PREFIXES and not item.get("country"):
            failures.append(cid)
    assert not failures, f"missing country for: {failures[:10]}"


def test_mapping_corpus_ids_resolve(corpus):
    """Every corpus_id named in id-mapping.json appears in corpus-data.json `id`."""
    mapping = json.loads(ID_MAPPING.read_text(encoding="utf-8"))
    corpus_ids = {c["id"] for c in corpus if c.get("id")}
    missing = [
        e["corpus_id"]
        for e in mapping.get("mapping", [])
        if e.get("corpus_id") and e["corpus_id"] not in corpus_ids
    ]
    assert not missing, f"mapping has corpus_ids not in corpus: {missing[:10]}"
```

- [ ] **Step 2: Run the test (expect failure — fix not run yet)**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/export-contract
conda run -n iconocracy --no-capture-output pytest -q tests/test_corpus_export_contract.py 2>&1 | tail -20
```

Expected: `test_mapping_corpus_ids_resolve` fails because corpus-data.json has 165 items but id-mapping references items beyond those (e.g. the 100 new records). Other tests should pass.

This is the red light that the fix must turn green.

### Task A5 — Run the fixed script and regenerate corpus-data.json

- [ ] **Step 1: Run records_to_corpus.py --diff (sanity)**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/export-contract
conda run -n iconocracy --no-capture-output python tools/scripts/records_to_corpus.py --diff 2>&1
```

Expected: `records.jsonl items: 265`, `corpus-data.json items: 165`, `Only in records.jsonl (100): + …`. The 100 new records are listed.

If both sides show 165: records.jsonl in the worktree is stale; see Task A1 step 2.

- [ ] **Step 2: Regenerate corpus-data.json**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/export-contract
conda run -n iconocracy --no-capture-output python tools/scripts/records_to_corpus.py 2>&1
```

Expected: `OK: 265 itens escritos em /home/ana/.../corpus/corpus-data.json`.

- [ ] **Step 3: Verify the regenerated file**

```bash
python3 -c "
import json
d = json.load(open('corpus/corpus-data.json'))
print(f'count={len(d)}')
print(f'has_id={sum(1 for x in d if x.get(\"id\"))}')
print(f'has_country={sum(1 for x in d if x.get(\"country\"))}')
print(f'has_support={sum(1 for x in d if x.get(\"support\"))}')
# 100 new entries should have id (from mapping or UUID fallback) and country (derived from prefix)
print(f'has_indicadores={sum(1 for x in d if x.get(\"indicadores\"))}')
"
```

Expected:
```
count=265
has_id=265
has_country≥165   # 165 from rich preserve + as many of the 100 as id-mapping resolves
has_support=165   # 100 new ones don't have support yet (deferred to #57)
has_indicadores=165
```

If `has_country` is exactly 165: the mapping lookup is missing or the prefix derivation isn't firing. Inspect a few item ids:
```bash
python3 -c "import json; d=json.load(open('corpus/corpus-data.json')); print([x['id'] for x in d if not x.get('country')][:10])"
```

### Task A6 — Run all the acceptance checks

- [ ] **Step 1: Run --diff (should report synced)**

```bash
conda run -n iconocracy --no-capture-output python tools/scripts/records_to_corpus.py --diff
```

Expected: `records.jsonl items: 265 / corpus-data.json items: 265 / Em sincronização` (or only the 1 known PT-005 URL-encoding mismatch — pre-existing, document it).

- [ ] **Step 2: Run code_purification.py --status (country/support rollups must NOT be all '?')**

```bash
conda run -n iconocracy --no-capture-output python tools/scripts/code_purification.py --status
```

Expected:
```
Total items:   265
Coded:         165 (62%)
Remaining:     100

By country:
  Brazil       …
  France       …
  United Kingdom  …
  …

By support:
  moeda          …
  selo           …
  monumento      …
  …
```

If country rollups still show `?`: the script reads country from `corpus[].country`, so verify the regenerated corpus-data.json actually has that field on the 165 rich entries (Task A5 step 3).

- [ ] **Step 3: Run the cross-file consistency tests**

```bash
conda run -n iconocracy --no-capture-output pytest -q tests/test_cross_file_consistency.py
```

Expected: `9 passed` (was 8 passed 1 failed before the fix — `test_mapping_corpus_ids_exist`).

- [ ] **Step 4: Run the new schema contract test**

```bash
conda run -n iconocracy --no-capture-output pytest -q tests/test_corpus_export_contract.py
```

Expected: all 4 tests pass.

- [ ] **Step 5: Run the full test suite**

```bash
conda run -n iconocracy --no-capture-output pytest -q tests/
```

Expected: 0 failures. If anything fails that wasn't failing before the fix, fix it inline.

### Task A7 — Document the schema contract (ADR)

**Files:**
- Create: `docs/adr/006-corpus-export-schema.md`
- Modify: `CLAUDE.md` (Known Data Issues block — note the regression is fixed; cross-link the ADR)

- [ ] **Step 1: Write the ADR**

```markdown
# ADR 006 — Corpus Export Schema Contract

**Status:** Accepted
**Date:** 2026-05-19
**Related:** Issue #56, `tools/scripts/records_to_corpus.py`, `tests/test_corpus_export_contract.py`

## Context

The April–May 2026 corpus export regression dropped the public `corpus/corpus-data.json` from its legacy rich schema (33 keys including `id`, `country`, `support`, `medium_norm`, `year`, `panofsky`) to a slim 12-field form without stable `id`. Downstream code (`code_purification.py --status`, the cross-file consistency tests, notebooks, HF release builder) broke because they rely on those fields.

## Decision

The public corpus export uses the **legacy rich schema**. Specifically, every entry in `corpus/corpus-data.json` **must** include:

| Field | Type | Source |
|---|---|---|
| `id` | string | corpus_id from `data/processed/id-mapping.json` (e.g. `BR-007`); falls back to the UUID `item_id` if no mapping exists yet |
| `url` | string | `webscout.search_results[0].url` (placeholder URLs preserved as-is) |
| `title` | string | `input.title_hint` or `webscout.search_results[0].title` |
| `description` | string | `webscout.summary_evidence` |
| `motif` | string[] | `iconocode.pre_iconographic[*].motif` (observed=true) |
| `regime` | string | `purificacao.regime_iconocratico` |
| `endurecimento_score` | number | `purificacao.purificacao_composto` |
| `coded_by` | string | `purificacao.coded_by` |
| `coded_at` | string (ISO) | `purificacao.coded_at` |
| `citation_abnt` | string | `webscout.search_results[0].abnt_citation` |
| `country` | string | derived from `id` prefix via `COUNTRY_FROM_PREFIX` (BR→Brazil, etc.) OR preserved from prior export |
| `country_pt` | string | derived from `id` prefix via `COUNTRY_PT_FROM_PREFIX` OR preserved |

The following fields are **preserved on merge** if present on the existing entry (records.jsonl does not carry them; the rich versions must come from the vault / manual coding):

`support`, `medium`, `medium_norm`, `year`, `date`, `period`, `period_norm`, `creator`, `institution`, `source_archive`, `thumbnail_url`, `rights`, `tags`, `tags_str`, `motif_str`, `in_scope`, `scope_note`, `panofsky`, `indicadores`, `audit_flags`.

## How the contract is enforced

- `tools/scripts/records_to_corpus.py` reads `id-mapping.json` and writes `id`, `country`, `country_pt` for every entry.
- `tests/test_corpus_export_contract.py` asserts the contract on the committed file.
- `tests/test_cross_file_consistency.py::test_mapping_corpus_ids_exist` asserts every `corpus_id` in id-mapping appears as an `id` in corpus-data.json.

## Consequences

- Records lacking a `corpus_id` in id-mapping get a UUID as `id` (visible audit signal that they need mapping).
- The 100 records introduced after the last manual coding pass have `id` + `country` but no `support` / `year` until they go through the vault candidate workflow. They carry `audit_flags: ["uncoded-purification"]` (see ADR 007 / Issue #57).
- Downstream consumers (`code_purification.py`, notebooks, HF release builder) can depend on the `id` + `country` + `support` fields being present for the coded subset.

## Alternatives considered

- **Slim schema + consumer migration:** keep the broken slim shape and migrate `code_purification.py`, tests, notebooks. Rejected because the legacy schema is referenced widely (incl. external HF dataset card) and the cost of migration outweighs the cost of restoring the contract.
- **UUID-keyed schema:** use the record-level UUIDs as `id` instead of corpus_id. Rejected because id-mapping.json, vault notes, and citation strings already use BR-007-style codes.
```

- [ ] **Step 2: Update CLAUDE.md Known Data Issues block**

Find the "Known Data Issues (last audit: 2026-05-16)" section and update issue #1 to reflect the fix. Cross-link the ADR. Don't duplicate the schema spec.

Concrete change (rewrite the issue #1 bullet):

```diff
-1. **Major drift across exports** — current counts:
-   - `data/processed/records.jsonl` → **265 records, all schema-valid** (`validate_schemas.py` → 265/265 ✓)
-   - `corpus/corpus-data.json` → **165 items** (99 records in `records.jsonl` have not been propagated; `records_to_corpus.py --diff` lists them)
-   - `data/processed/purification.jsonl` → **165 records** (matches old corpus-data.json count; 100 records lack endurecimento coding)
-   - `companion-data.json` → **5 items** (drastically stale; `sync_companion.py` will rebuild)
+1. **Corpus export drift** — resolved 2026-05-19, see ADR 006 (`docs/adr/006-corpus-export-schema.md`).
+   - `corpus/corpus-data.json` is back to the legacy rich schema; `records_to_corpus.py` reconstructs `id` from `id-mapping.json` and derives `country` from the id prefix.
+   - **Purification coverage is partial** (165 of 265 coded; see Issue #57 + ADR 007 for the deferred-queue policy).
+   - `companion-data.json` may still be stale; run `sync_companion.py` before any release.
```

### Task A8 — Commit the fix on `fix/export-contract-regression`

- [ ] **Step 1: Stage the changes**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/export-contract
git add tools/scripts/records_to_corpus.py corpus/corpus-data.json tests/test_corpus_export_contract.py docs/adr/006-corpus-export-schema.md CLAUDE.md
git status --short
```

Expected: all 5 files staged, nothing else.

- [ ] **Step 2: Commit**

```bash
git commit -m "fix(corpus): restore export contract — id, country, country_pt on corpus-data.json (#56)

Issue #56: records_to_corpus.py dropped the legacy rich schema. corpus-data.json
items lost their stable id field, country/support rollups collapsed to '?', and
the cross-file consistency test broke.

Restores the legacy schema:
- records_to_corpus.py loads id-mapping.json and sets corpus[].id = corpus_id
  (BR-007 style), falling back to item_id (UUID) for records without a mapping
- country/country_pt are derived from the id prefix (BR→Brazil, FR→France, …)
- support/medium_norm/year/panofsky are preserved on merge from existing entries
  (records.jsonl does not carry them; new uncoded records get a slim row with
  audit_flag, see #57)

Adds tests/test_corpus_export_contract.py to lock the contract in.
Documents the contract in docs/adr/006-corpus-export-schema.md.

Closes #56."
```

- [ ] **Step 3: Verify the commit landed**

```bash
git log --oneline -3
```

Expected: top commit is the fix; second is the previous main HEAD.

### Task A9 — Push branch and open PR

- [ ] **Step 1: Push the branch**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/export-contract
git push -u origin fix/export-contract-regression
```

Expected: branch published, tracking set.

- [ ] **Step 2: Open the PR via gh (HEREDOC body to preserve formatting)**

```bash
gh pr create --repo anavvanzin/iconocracy-corpus \
  --title "fix(corpus): restore export contract — id, country, support fields (#56)" \
  --base main --head fix/export-contract-regression \
  --body "$(cat <<'EOF'
## Summary
Closes #56. Restores the legacy rich schema on `corpus/corpus-data.json` after a regression in `records_to_corpus.py` dropped `id`, `country`, and other fields downstream code depends on.

## Changes
- `tools/scripts/records_to_corpus.py` — load `id-mapping.json`; set `corpus[].id` = corpus_id (BR-007 style) with UUID fallback; derive `country`/`country_pt` from id prefix; preserve rich fields on merge.
- `corpus/corpus-data.json` — regenerated with the fixed script; 265 items (165 rich + 100 new with id/country only, slim until #57).
- `tests/test_corpus_export_contract.py` — new tests locking in the schema contract.
- `docs/adr/006-corpus-export-schema.md` — ADR documenting the contract.
- `CLAUDE.md` — Known Data Issues block updated to point at the ADR.

## Verification
- [x] `pytest tests/test_cross_file_consistency.py` — 9/9 pass (was 8/9)
- [x] `pytest tests/test_corpus_export_contract.py` — new, 4/4 pass
- [x] `pytest tests/` — full suite green
- [x] `records_to_corpus.py --diff` reports 265/265, "Em sincronização"
- [x] `code_purification.py --status` shows real country/support rollups

## Follow-up
- Issue #57 (the 100 uncoded records) is addressed in a separate PR on `fix/purification-reporting`.
EOF
)"
```

Expected: PR URL printed. Capture the number.

### Task A10 — Mark task complete

- [ ] **Step 1: Update task tracker**

```bash
# (in claude harness)
TaskUpdate id=8 status=completed
```

---

## Phase B — Address #57 (purification backlog)

### Task B1 — Switch to the purification-reporting worktree

- [ ] **Step 1: Sync the worktree**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/purification-reporting
git status --short
git fetch
git reset --hard main
```

Expected: clean working tree at main's HEAD.

### Task B2 — Generate the uncoded-records manifest

**Files:**
- Create: `tools/scripts/build_purification_manifest.py`
- Create: `data/processed/purification-manifest.json` (output)

- [ ] **Step 1: Write the manifest builder**

```python
#!/usr/bin/env python3
"""build_purification_manifest.py — Identify records lacking purification coding.

Produces a JSON manifest listing every record in records.jsonl that has no entry
in purification.jsonl, with item_id, corpus_id (if mapped), URL, title hint, and
the reason it's queued (e.g. "no purificacao block", "missing composito score").

Per ADR 007 / Issue #57, these records remain in the public corpus with an
`uncoded-purification` audit flag; this manifest is the authoritative work queue.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS = REPO / "data" / "processed" / "records.jsonl"
PURIF = REPO / "data" / "processed" / "purification.jsonl"
ID_MAPPING = REPO / "data" / "processed" / "id-mapping.json"
OUT = REPO / "data" / "processed" / "purification-manifest.json"


def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def _load_mapping() -> dict[str, str]:
    if not ID_MAPPING.exists():
        return {}
    m = json.loads(ID_MAPPING.read_text(encoding="utf-8"))
    return {
        e["item_id"]: e.get("corpus_id", "")
        for e in m.get("mapping", [])
        if e.get("item_id")
    }


def main() -> None:
    records = _load_jsonl(RECORDS)
    purif = _load_jsonl(PURIF)
    mapping = _load_mapping()

    coded_item_ids = {
        p.get("item_id") for p in purif if p.get("purificacao_composto") is not None
    }

    queued = []
    for rec in records:
        item_id = rec.get("item_id", "")
        if not item_id or item_id in coded_item_ids:
            continue
        sr = rec.get("webscout", {}).get("search_results", [{}])
        url = sr[0].get("url", "") if sr else ""
        title = (
            rec.get("input", {}).get("title_hint")
            or (sr[0].get("title", "") if sr else "")
        )
        queued.append({
            "item_id": item_id,
            "corpus_id": mapping.get(item_id, ""),
            "url": url,
            "title_hint": title,
            "reason": (
                "no purificacao block"
                if not rec.get("purificacao")
                else "missing purificacao_composto"
            ),
        })

    queued.sort(key=lambda x: (x["corpus_id"] or "ZZZ", x["item_id"]))

    payload = {
        "version": "1.0",
        "generated_at": "AUTOPOPULATE",  # replaced below
        "total_records": len(records),
        "total_coded": len(records) - len(queued),
        "total_queued": len(queued),
        "queued": queued,
    }

    from datetime import datetime, timezone
    payload["generated_at"] = datetime.now(timezone.utc).isoformat()

    OUT.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"OK: {len(queued)} queued records written to {OUT}")
    print(f"    coded: {payload['total_coded']} / {payload['total_records']}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/purification-reporting
conda run -n iconocracy --no-capture-output python tools/scripts/build_purification_manifest.py
```

Expected:
```
OK: 100 queued records written to /home/ana/.../data/processed/purification-manifest.json
    coded: 165 / 265
```

- [ ] **Step 3: Spot-check the manifest**

```bash
python3 -c "
import json
m = json.load(open('data/processed/purification-manifest.json'))
print(f'total_records={m[\"total_records\"]} total_coded={m[\"total_coded\"]} total_queued={m[\"total_queued\"]}')
print('first 3 queued:')
for q in m['queued'][:3]:
    print(f'  {q[\"corpus_id\"] or \"(no corpus_id)\"} {q[\"item_id\"][:8]}… — {q[\"title_hint\"][:60]}')
print('records without corpus_id:', sum(1 for q in m['queued'] if not q['corpus_id']))
"
```

Expected: 100 queued, mix of records with/without corpus_id, titles populated.

### Task B3 — Add the `uncoded-purification` audit flag to the slim corpus entries

After Phase A, the regenerated corpus-data.json has 100 slim entries (id + country only). We tag them so they're visible in the public export.

**Files:**
- Modify: `corpus/corpus-data.json` (via script)
- Create: `tools/scripts/tag_uncoded_purification.py`

- [ ] **Step 1: Write the tagging script**

```python
#!/usr/bin/env python3
"""tag_uncoded_purification.py — Add `uncoded-purification` audit flag to corpus
entries that are in the purification manifest's queued list.

Idempotent: running twice does not duplicate the flag.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
CORPUS = REPO / "corpus" / "corpus-data.json"
MANIFEST = REPO / "data" / "processed" / "purification-manifest.json"
FLAG = "uncoded-purification"


def main() -> None:
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    queued_corpus_ids = {q["corpus_id"] for q in manifest["queued"] if q["corpus_id"]}
    queued_item_ids = {q["item_id"] for q in manifest["queued"]}

    changed = 0
    for entry in corpus:
        eid = entry.get("id", "")
        if eid in queued_corpus_ids or eid in queued_item_ids:
            flags = entry.get("audit_flags", []) or []
            if FLAG not in flags:
                flags.append(FLAG)
                entry["audit_flags"] = flags
                changed += 1

    CORPUS.write_text(
        json.dumps(corpus, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"OK: tagged {changed} entries with `{FLAG}`")
    print(f"    expected: {len(queued_corpus_ids | queued_item_ids)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/purification-reporting
conda run -n iconocracy --no-capture-output python tools/scripts/tag_uncoded_purification.py
```

Expected: `OK: tagged 100 entries with uncoded-purification`.

Note: this depends on Phase A's PR being merged into main so the worktree's corpus-data.json has the 265 entries. If Phase A is still in flight, run Phase A first.

- [ ] **Step 3: Spot-check**

```bash
python3 -c "
import json
d = json.load(open('corpus/corpus-data.json'))
tagged = [x for x in d if 'uncoded-purification' in (x.get('audit_flags') or [])]
print(f'tagged: {len(tagged)}')
print('first 3:', [x['id'] for x in tagged[:3]])
"
```

Expected: `tagged: 100`.

### Task B4 — Update `code_purification.py --status` to surface the queue

**Files:**
- Modify: `tools/scripts/code_purification.py`

- [ ] **Step 1: Read the current --status output formatter**

```bash
grep -n "Total items\|Coded:\|Remaining:" tools/scripts/code_purification.py
```

- [ ] **Step 2: Add a manifest-aware footer**

After the existing `By regime:` block, append a "Backlog" section. Concrete edit:

```python
# After the existing By regime: block in code_purification.py --status path
manifest_path = REPO / "data" / "processed" / "purification-manifest.json"
if manifest_path.exists():
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    print(f"\n  Backlog (Issue #57 / ADR 007):")
    print(f"    queued: {m['total_queued']} (of {m['total_records']} canonical)")
    no_corpus_id = sum(1 for q in m['queued'] if not q['corpus_id'])
    if no_corpus_id:
        print(f"    no corpus_id mapped yet: {no_corpus_id}")
    print(f"    manifest: data/processed/purification-manifest.json")
```

Use the actual `REPO` variable name from the existing script — match what's already there. If `REPO` isn't defined, mirror the pattern from `records_to_corpus.py`.

- [ ] **Step 3: Verify the new output**

```bash
conda run -n iconocracy --no-capture-output python tools/scripts/code_purification.py --status 2>&1 | tail -20
```

Expected output now includes:
```
Backlog (Issue #57 / ADR 007):
  queued: 100 (of 265 canonical)
  no corpus_id mapped yet: N
  manifest: data/processed/purification-manifest.json
```

### Task B5 — Document the policy (ADR 007)

**Files:**
- Create: `docs/adr/007-purification-coverage-policy.md`

- [ ] **Step 1: Write the ADR**

```markdown
# ADR 007 — Partial Purification Coverage Policy

**Status:** Accepted
**Date:** 2026-05-19
**Related:** Issue #57, ADR 006, `tools/scripts/build_purification_manifest.py`, `data/processed/purification-manifest.json`

## Context

`data/processed/records.jsonl` contains 265 canonical records but only 165 of them have endurecimento coding in `data/processed/purification.jsonl`. The 100 uncoded records are valid corpus items — they passed schema validation — but they cannot participate in quantitative analysis until coded.

We need to ship Cap. 6 / the corpus export without blocking on coding the remaining 100. Coding requires manual iconographic judgment per item and is unrealistic on the current timeline.

## Decision

The 100 uncoded records remain in the public corpus (`corpus/corpus-data.json`) tagged with `audit_flags: ["uncoded-purification"]`. The authoritative work queue lives at `data/processed/purification-manifest.json`. Health reporting uses **265 as the canonical denominator** and reports the 165/100 coded/queued split explicitly.

This is the "defer with documented queue" option (Issue #57). The "batch-code all 100 now" and "exclude from release-facing views" alternatives were rejected.

## Consequences

- Analytical chapters (Cap. 6) MUST filter for `audit_flags ∌ "uncoded-purification"` and disclose the filter in the methodology section.
- HF dataset card lists 265 catalog / 165 coded explicitly.
- Notebook headers must check `len(df.query("audit_flags.str.contains('uncoded-purification') == False"))` before claiming coverage.
- New records added to records.jsonl get the flag by default until coded; the manifest regenerator (`build_purification_manifest.py`) is idempotent.

## How to clear an item from the queue

1. Code the record in `vault/candidatos/<corpus_id> <title>.md` per the standard SCOUT/ICONOCODE workflow.
2. Run `python tools/scripts/vault_sync.py sync` to propagate to records.jsonl.
3. Add the purificacao block via `python tools/scripts/code_purification.py --item <corpus_id>` (or batch).
4. Re-run `python tools/scripts/build_purification_manifest.py` to refresh the manifest.
5. Re-run `python tools/scripts/tag_uncoded_purification.py` to drop the audit flag from the corpus.

## Alternatives considered

- **Batch-code all 100 now:** blocks defense timeline; the IRR pilot (Cap. 4) is more urgent.
- **Exclude uncoded from `corpus-data.json`:** misrepresents the catalog state; downstream tools that count items would show 165 and obscure the backlog.
```

### Task B6 — Commit and PR

- [ ] **Step 1: Stage**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus/.worktrees/purification-reporting
git add tools/scripts/build_purification_manifest.py \
        tools/scripts/tag_uncoded_purification.py \
        tools/scripts/code_purification.py \
        data/processed/purification-manifest.json \
        corpus/corpus-data.json \
        docs/adr/007-purification-coverage-policy.md
git status --short
```

- [ ] **Step 2: Commit**

```bash
git commit -m "feat(corpus): purification backlog manifest + uncoded-purification audit flag (#57)

Issue #57: 100 of 265 canonical records lack endurecimento coding. This commit
documents the deferred-queue policy (ADR 007) and ships the tooling:

- build_purification_manifest.py emits data/processed/purification-manifest.json
  with the 100 queued records (item_id, corpus_id when mapped, URL, title, reason)
- tag_uncoded_purification.py marks the corresponding corpus-data.json entries
  with audit_flags: ['uncoded-purification']; idempotent
- code_purification.py --status now surfaces the backlog: 'queued: 100 (of 265
  canonical)' under a 'Backlog (Issue #57 / ADR 007)' header

ADR 007 documents the policy: 265 is the canonical denominator; analytical
chapters MUST filter on the uncoded-purification flag and disclose it.

Closes #57."
```

- [ ] **Step 3: Push and open PR**

```bash
git push -u origin fix/purification-reporting
gh pr create --repo anavvanzin/iconocracy-corpus \
  --title "feat(corpus): purification backlog manifest + audit flag (#57)" \
  --base main --head fix/purification-reporting \
  --body "$(cat <<'EOF'
## Summary
Closes #57. Documents the partial-coverage policy (ADR 007), generates an authoritative work queue (`purification-manifest.json`), and tags the 100 uncoded entries in `corpus-data.json` with `audit_flags: ["uncoded-purification"]`.

## Depends on
PR #N (Phase A — #56 fix). Must merge that first so the 265-entry corpus-data.json exists for tagging.

## Changes
- `tools/scripts/build_purification_manifest.py` — new; emits the queue.
- `tools/scripts/tag_uncoded_purification.py` — new; idempotent flagger.
- `tools/scripts/code_purification.py` — `--status` surfaces the backlog.
- `data/processed/purification-manifest.json` — new; 100 queued records.
- `corpus/corpus-data.json` — 100 entries tagged.
- `docs/adr/007-purification-coverage-policy.md` — ADR.

## Verification
- [x] `build_purification_manifest.py` reports `coded: 165 / 265`
- [x] `tag_uncoded_purification.py` reports `tagged: 100`
- [x] `code_purification.py --status` shows the Backlog section
- [x] Re-running both scripts is a no-op (idempotent)

## Follow-up
- Cap. 6 methodology disclosure: filter on `audit_flags ∌ "uncoded-purification"` and document it.
EOF
)"
```

---

## Phase C — Close issue #55

### Task C1 — Close the empty placeholder

- [ ] **Step 1: Verify it's the empty template**

```bash
gh issue view 55 --repo anavvanzin/iconocracy-corpus --json title,body
```

Expected: title `[writing]`, body is just the `## Goal`/`## Inputs`/`## Acceptance criteria` template with no content filled in.

- [ ] **Step 2: Close with a brief note**

```bash
gh issue close 55 --repo anavvanzin/iconocracy-corpus \
  --reason "not planned" \
  --comment "Closing — unfilled `[writing]` issue template. Writing tasks now tracked through the thesis manuscript folder (`tese/manuscrito/`) and per-chapter plan docs."
```

---

## Phase D — PR triage

### Task D1 — PR #52 (consolidação editorial + higiene de notebooks)

- [ ] **Step 1: Dispatch a subagent code review**

Use the `Agent` tool with `subagent_type: feature-dev:code-reviewer`. Prompt:

> Review PR #52 on `anavvanzin/iconocracy-corpus` ("consolidação editorial + higiene de notebooks/PENDING_REVIEW", DRAFT, +637/-55 in 8 files). It claims to map state against the "Known Data Issues" from April 2026.
>
> Context I've already established: today (2026-05-19) Issues #56 (export contract regression) and #57 (100 uncoded records) are being addressed in separate PRs that will land before this one is decided. So:
>
> 1. Identify any overlap with #56/#57 work. List specific files and line ranges where this PR touches the same surfaces as the #56/#57 PRs.
> 2. Flag any contradictions — places where this PR's approach disagrees with the legacy-schema decision (ADR 006) or the deferred-queue policy (ADR 007).
> 3. Identify any work that is independently useful — notebook hygiene, editorial fixes — that should be kept even if the overlap is dropped.
> 4. Recommend a disposition: (a) merge as-is after dependency PRs land, (b) close as superseded, (c) cherry-pick specific files. Be concrete: which files, which commits.
>
> Report findings as a short structured note (under 400 words) with specific file paths and a clear disposition recommendation.

- [ ] **Step 2: Act on the subagent's recommendation**

- If "merge as-is": wait for Phase A & B PRs to merge, then resolve conflicts and merge #52.
- If "close as superseded": `gh pr close 52 --repo anavvanzin/iconocracy-corpus --comment "Superseded by PRs for #56 + #57. Closing."`
- If "cherry-pick X, Y, Z": create a new branch `chore/from-52-X-Y-Z`, cherry-pick the listed files, open a new PR.

### Task D2 — PRs #30, #23, #13 (April, stale)

Dispatch three parallel subagent code reviews. One single message with three Agent calls.

- [ ] **Step 1: Dispatch reviews in parallel**

For each PR, the prompt template:

> Review PR #N on `anavvanzin/iconocracy-corpus`. Title, age, size: [as in plan summary table].
>
> Context I've already established: the repo has moved on substantially since April 25. The Research repo was extracted (so PR #30's workspace topology may be superseded). The corpus grew from 116→159→…→265 (so PR #13's "43 new items" may already be ingested via other means). PR #23 (Hono migration) has CodeQL failures and is tech-debt, not urgent.
>
> Tasks:
> 1. Verify whether the PR's work is still needed given the current state of main. For #30, check whether `~/Documents/projetos/research/` and the Research repo cover this. For #13, check whether the BR-011 through BR-025 items are already in `records.jsonl`. For #23, check whether the routing changes are still applicable to the current `deploy/iconocracia-companion/src/index.js`.
> 2. Recommend a disposition: (a) revive and merge (with conflict-resolution notes), (b) close as superseded, (c) extract specific commits and discard rest.
>
> Report findings as a short structured note (under 300 words) per PR.

Dispatch all three in a single message using the Agent tool with `subagent_type: feature-dev:code-reviewer` (parallel).

- [ ] **Step 2: Act on each recommendation**

For each PR: close, revive, or extract per the subagent's recommendation. Always include a clear comment when closing or reviving, referencing the review.

### Task D3 — Research PRs #9 and #4 (convert → review → decide)

Ana's instruction: "make the draft into ready for review and then review and close it."

- [ ] **Step 1: Convert both from DRAFT to ready-for-review**

```bash
gh pr ready 9 --repo anavvanzin/Research
gh pr ready 4 --repo anavvanzin/Research
```

- [ ] **Step 2: Dispatch two parallel subagent reviews**

For PR #9 (debian12 onboarding) — prompt:

> Review PR #9 on `anavvanzin/Research` ("docs(onboarding-debian12): manual operacional + prompt-mestre p/ setup Debian 12", recently DRAFT, +1979 lines in 8 files). It's onboarding documentation for the VAIO FE16 / Debian 12 setup for the ICONOCRACIA doctoral research.
>
> Tasks:
> 1. Verify the documentation is still accurate as of today (2026-05-19): check for stale paths (the migration from `/data/` to `~/Documents/` happened recently — `~/Documents/CLAUDE.md` reflects the new layout).
> 2. Check whether referenced commands still work (conda env name `iconocracy`, Python version, etc.).
> 3. Flag anything that contradicts the current setup or refers to retired tooling.
> 4. Recommend: merge as-is, merge with the listed fixes, or close.
>
> Report under 300 words.

For PR #4 (self-improving-agent) — prompt:

> Review PR #4 on `anavvanzin/Research` ("feat(self-improving-agent): wire hooks to Claude Code via settings.json", DRAFT since Apr 23, +171/-36 in 6 files). It wires the repo-local self-improving-agent hooks to Claude Code.
>
> Tasks:
> 1. Check whether the self-improving-agent project is still active. Look for `agency-agents/`, `agent-thesis/`, or similar in the meta-workspace.
> 2. Verify the `.claude/settings.json` hook contract is current (the format may have changed since April).
> 3. Recommend: merge, merge with fixes, or close as abandoned.
>
> Report under 300 words.

- [ ] **Step 3: Act on each recommendation**

Per Ana's instruction "review and close it": when a review concludes merge-then-close is sensible, merge first; when it concludes the work is no longer relevant, close with the review's reasoning in the comment.

### Task D4 — Issue #21 (Hono migration)

- [ ] **Step 1: Wait for Task D2 to decide #23's fate first**

#23 contains the actual Hono migration work; #21 is the request. If D2 closes #23 as superseded/stale, also close #21.

- [ ] **Step 2: Disposition**

If #23 closed: `gh issue close 21 --repo anavvanzin/iconocracy-corpus --reason "not planned" --comment "Closing alongside PR #23. The routing-order P0 bug it addressed was patched directly in the companion Worker; full Hono migration deferred indefinitely as tech-debt."`

If #23 revived & merged: keep #21 open until the merge lands, then close as completed.

---

## Phase E — Memory + index cleanup

### Task E1 — Update MEMORY.md

**Files:**
- Modify: `/home/ana/.claude/projects/-home-ana/memory/project_iconocracia.md`
- Modify: `/home/ana/.claude/projects/-home-ana/memory/MEMORY.md` (if the line there is also stale)

- [ ] **Step 1: Read current memory**

```bash
cat /home/ana/.claude/projects/-home-ana/memory/project_iconocracia.md
```

- [ ] **Step 2: Update**

The stale claim was "Fixed IDs/metadata in fix/export-contract-regression branch." Replace with the actual current state.

Concrete edit:

```diff
-Fixed IDs/metadata in fix/export-contract-regression branch.
+Issue #56 (export contract regression) resolved 2026-05-19; legacy schema (BR-007 IDs + country/support) restored — see ADR 006. Issue #57 (100 uncoded records) deferred with documented queue — see ADR 007 + purification-manifest.json.
```

Keep the rest of the memory intact unless additional claims are stale.

### Task E2 — Update the Obsidian vault index

**Files:**
- Modify: `/data/projetos/research/vaults/iconocracy-vault/hot.md`
- Modify: `/data/projetos/research/vaults/iconocracy-vault/log.md`

- [ ] **Step 1: Append a log entry**

In `log.md`, append:

```
- [2026-05-19TXX:XX:XX] HOUSEKEEPING repo=anavvanzin/iconocracy-corpus issues_closed=[55,56,57,21] prs_merged=[…] prs_closed=[…] adrs_added=[006,007] notes="ADR 006 schema contract; ADR 007 purification coverage policy; manifest at data/processed/purification-manifest.json"
```

Use the actual completion timestamp.

- [ ] **Step 2: Update `hot.md`'s recent activity**

Add an entry referencing the housekeeping pass with a one-line summary.

---

## Phase F — Cleanup

### Task F1 — Remove unused worktrees

After Phase A and B PRs are MERGED (not just opened), the worktrees can be torn down.

- [ ] **Step 1: Verify branches are merged**

```bash
gh pr view <A_PR> --repo anavvanzin/iconocracy-corpus --json mergedAt
gh pr view <B_PR> --repo anavvanzin/iconocracy-corpus --json mergedAt
```

Expected: `mergedAt` is non-null on both.

- [ ] **Step 2: Remove worktrees**

```bash
cd ~/Documents/projetos/research/hub/iconocracy-corpus
git worktree remove .worktrees/export-contract
git worktree remove .worktrees/purification-reporting
git worktree remove .worktrees/backlog-triage  # never had any commits
git worktree list
```

Expected: only `main` worktree remaining.

- [ ] **Step 3: Delete the local branches**

```bash
git branch -d fix/export-contract-regression fix/purification-reporting chore/backlog-triage
```

If any complains about unmerged commits, that's a signal something didn't actually land — investigate before forcing.

### Task F2 — Final report

- [ ] **Step 1: Confirm final state**

```bash
gh issue list --repo anavvanzin/iconocracy-corpus --state open
gh pr list --repo anavvanzin/iconocracy-corpus --state open
gh pr list --repo anavvanzin/Research --state open
```

- [ ] **Step 2: Mark all tasks complete in the task tracker**

```bash
TaskUpdate id=8 status=completed
TaskUpdate id=9 status=completed
TaskUpdate id=10 status=completed
TaskUpdate id=11 status=completed
TaskUpdate id=12 status=completed
TaskUpdate id=13 status=completed
```

- [ ] **Step 3: Summarize to the user**

One paragraph max. List: issues closed, PRs merged, PRs closed, ADRs added. Don't narrate the journey.

---

## Dependencies between phases

```
Phase A (#56)  ──► Phase B (#57 — needs A's 265-entry corpus)
              ──► Phase E (memory points at ADR 006)

Phase D (PR triage) — independent of A/B but blocked on subagent reviews

Phase C (#55) — fully independent

Phase F — blocked on A & B merged
```

Recommended execution order: **A → B → C → D → E → F** (with Phase C run in parallel whenever convenient).

## Open questions deferred to execution time

- **PR #52 disposition:** depends on the subagent review. May reveal we want to cherry-pick specific files rather than close-or-merge wholesale.
- **PR #13 (43 new items):** the corpus has since grown to 265. The subagent must verify whether those items are already in `records.jsonl` before recommending closure.
- **Notebook regeneration:** Phase A regenerates `corpus-data.json`, which means notebooks reading from it may need to be re-run. This is a documented post-merge step, not a plan step (notebooks aren't authoritative).
