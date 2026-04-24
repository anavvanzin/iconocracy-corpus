---
name: scout-dedupe
description: >
  Run dedupe verification on a SCOUT candidate before saving to vault/candidatos/.
  Combines textual check (corpus-dedup agent) with visual CLIP check
  (iconocracy_clip.py) when an image path is available. Use when the user says
  "dedupe", "verificar duplicata", "checar duplicata", or BEFORE any "salvar"
  of a new SCOUT note.
user-invocable: true
---

Gate new SCOUT candidates against the existing corpus before `vault/candidatos/` write. Emits `CLEAR`, `SIMILAR`, or `DUPLICATE`.

## Inputs

Accept one of:

- **Path** to a draft SCOUT note (reads YAML frontmatter for `titulo`, `url`, `url_iiif`, `acervo`, `data_estimada`, `image_path`)
- **Inline fields**: `titulo=...`, `url=...`, `acervo=...`, `image=...` (at least one required)

## Pipeline

### Step 1 — Textual dedupe (always)

Dispatch the `corpus-dedup` subagent with the extracted fields via the Agent tool:

```
Agent(subagent_type="corpus-dedup", prompt="Check candidate — titulo: <T>, url: <U>, acervo: <A>, data: <D>")
```

Parse verdict: `DUPLICATE`, `SIMILAR`, or `CLEAR`.

### Step 2 — Visual dedupe (only if image path provided AND Hermes runtime available)

```bash
REPO="$CLAUDE_PROJECT_DIR"
IMG="<candidate image path>"

# If runtime present, rank candidate against the gallery; top-1 similarity > 0.90 = SIMILAR; > 0.95 = DUPLICATE
conda run -n iconocracy python "$REPO/tools/scripts/iconocracy_clip.py" \
  rank --limit 1 --top-k 5 "$IMG" \
  --output /tmp/scout-dedupe-$(date +%s).json
```

If `iconocracy_clip.py` exits with "ICONOCRACY CLIP runtime is incomplete", **skip visual step** and annotate report with `visual: skipped (runtime missing)`. Do not treat as error.

For pairwise deep-check against a specific suspect found in Step 1, use:

```bash
python tools/scripts/iconocracy_clip.py pair "$IMG" "<suspect_image>"
```

Cosine > 0.90 → SIMILAR; > 0.95 → DUPLICATE.

### Step 3 — Consolidate verdict

Take the **stricter** of (textual, visual):

| Textual | Visual | Final |
|---------|--------|-------|
| CLEAR | CLEAR/skipped | **CLEAR** |
| CLEAR | SIMILAR | **SIMILAR** |
| CLEAR | DUPLICATE | **DUPLICATE** |
| SIMILAR | any | **SIMILAR** (at least) |
| DUPLICATE | any | **DUPLICATE** |

## Output

```
SCOUT-DEDUPE [candidate: <titulo or path>]
  textual: CLEAR | SIMILAR → SCOUT-<ID> | DUPLICATE → SCOUT-<ID>
  visual:  CLEAR (top-1 sim=0.XX) | SIMILAR (sim=0.XX) | DUPLICATE (sim=0.XX) | skipped
  verdict: CLEAR | SIMILAR | DUPLICATE

Action:
  CLEAR     → Proceed to salvar.
  SIMILAR   → Add tag "#possivel-duplicata" to frontmatter AND propose Zwischenraum panel linking to existing SCOUT-<ID>. Ask user before saving.
  DUPLICATE → DO NOT save. Update existing SCOUT-<ID> with new suporte/variant info instead.
```

## Rules

- **Never write** to `vault/candidatos/` from this skill — it only verifies. The actual save is a separate step the user triggers after seeing the verdict.
- If `SIMILAR` or `DUPLICATE`, quote the matching fields (url, titulo, visual score) so the user can audit.
- Missing CLIP runtime is **not a blocker** — textual gate alone still applies.
- If no fields and no path provided, ask the user for at least `titulo` + `url` or `titulo` + `image`.

## When to run

- Before every `salvar` that creates a new `vault/candidatos/XX-NNN *.md`
- During a SCOUT campaign review, to batch-check a draft folder
- After an ingest run, to flag near-duplicates in `records.jsonl`
