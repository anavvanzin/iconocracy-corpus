---
tags: [meta, workflow, infrastructure, brainstorm, atlas-lab]
date: 2025-04-22
author: hermes
---

# Brainstorm: 20 Workflow & Infrastructure Improvements for ICONOCRACY

> Generated during an open brainstorming session on extending session horizons, reducing context friction, and tightening the research-to-writing pipeline.

---

## 1. Session Resurrection Protocol

**Problem:** Every new chat starts cold. You pay a context tax re-explaining corpus structure, active files, and current goals.

**Solution:** Maintain a rolling `.session-state.md` inside the repo root. Auto-update it every turn (or every major milestone) with:
- Active files and their purposes
- Open questions / decisions pending
- Last command run and its result
- Next planned step

**On cold start:** Paste the file contents as the first message. Instant continuity.

**Path:** `~/iconocracy-corpus/.session-state.md`

---

## 2. The "IconoContext" Window

**Problem:** `records.jsonl` is large. Parsing it in-context wastes tokens and slows reasoning.

**Solution:** A tiny local Python daemon that watches `data/processed/records.jsonl` and maintains a rolling summary:
- Last N records ingested
- Top Iconclass codes this session
- Missing-field histogram
- Confidence-score distribution

Expose via `localhost:8080/status`. I curl it in one shot instead of reading megabytes of JSONL.

**Stack:** `watchdog` + `fastapi` (or just `http.server`) + background process.

---

## 3. Skill Compiler

**Problem:** Skills live in three places: `~/.claude/skills/`, `~/.hermes/skills/`, and agency imports. Drift and duplication are inevitable.

**Solution:** A one-way sync script (`scripts/compile-skills.py`) that:
1. Scans all skill directories for ICONOCRACY-related entries
2. Concatenates them into a single canonical appendix
3. Writes to `~/iconocracy-corpus/AGENTS.md` (or `SKILLS.md`)

Codex and Hermes read the same source of truth. One file to rule them all.

**Trigger:** Run manually after any skill edit, or via pre-commit hook.

---

## 4. Autonomous Gallica Harvester (ARGOS v2)

**Problem:** ARGOS triggers manually. The gap between "discover" and "ingest" creates backlog.

**Solution:** A cron-backed MCP loop:
1. Gallica MCP queries: `allegorie`, `justice`, `droit`, `femme`, `19e siecle`
2. Downloads metadata + IIIF manifest for new items
3. Runs `iconocode` analysis automatically
4. Appends to `records.jsonl` only if confidence > threshold
5. Generates a weekly digest markdown file for human review

You review the digest, not every item.

**Tech:** `cronjob` skill + Gallica MCP + `iconocode-batch` skill.

---

## 5. The ENDURECIMENTO Dashboard

**Problem:** Indicator distributions and corpus health are invisible until you run a script.

**Solution:** A static HTML dashboard (zero backend) served by `artifact-preview` on port 8765:
- ENDURECIMENTO / DULCIFICACAO / etc. histograms
- PCA cluster scatter plot (Plotly or D3)
- Temporal trend line (records by year)
- Missing-data heatmap
- "Last ingest" timestamp

Open it in an Obsidian iframe or a browser pane. Live corpus health at a glance.

**Generator:** A Python script that reads `records.jsonl` and emits `dashboard/index.html`.

---

## 6. Shadow Corpus on `/Volumes/ICONOCRACIA`

**Problem:** System disk is ~94% full. File ops timeout or fail.

**Solution:** Keep code and JSONL on SSD, move blobs to the external volume:
- `data/raw/images/` → symlink to `/Volumes/ICONOCRACIA/corpus-storage/images/`
- `data/archive/` → symlink to `/Volumes/ICONOCRACIA/corpus-storage/archive/`

Alternatively: configure Git LFS with a custom object store pointing at the volume.

**Caveat:** `/Volumes/ICONOCRACIA` is root-owned. You may need to adjust mount permissions or use `rsync` with a dedicated user-space mount.

---

## 7. Electric Monk Dialectic for Thesis Writing

**Problem:** Thesis chapters are top-down and monocultural. Counter-arguments surface too late (at the committee).

**Solution:** Use the existing `dialectic` / `hegelian-dialectic` skill:
- **Thesis Agent:** Writes the affirmative (e.g., "The feminization of Justice is a liberal emancipatory strategy")
- **Antithesis Agent:** Writes the opposition (e.g., "The feminization is a disciplinary mechanism masking state violence")
- **Synthesis Agent:** Reconciles the strongest claims from both into a rigorous third position

You edit the synthesis. Forces epistemic friction before the draft is "done."

---

## 8. Zettelkasten-Style Memo Generation

**Problem:** Insights from analysis sessions evaporate. They are not linked to prior work.

**Solution:** After every significant session, auto-generate a Luhmann-style note card:
- Single atomic idea
- Unique ID (timestamp or Luhmann format)
- Backlinks to previous related cards
- Source URL / file path
- Optional: one-sentence "so what?"

Append to `vault/zettel/`. Over months, the thesis emerges bottom-up from linked cards rather than top-down from chapter outlines.

**Template:** Stored as a skill or Obsidian template.

---

## 9. Voice Memos → Structured Notes

**Problem:** Thoughts that occur while walking, cooking, or showering die unrecorded.

**Solution:** Reverse the existing TTS pipeline:
1. Dictate into Voice Memos (or any recorder)
2. Drop MP3s into `~/iconocracy-corpus/inbox/audio/`
3. A folder watcher runs Whisper transcription
4. I (Hermes) convert the transcript into:
   - ABNT-style footnote draft
   - Zettelkasten card
   - Todo item
   - Or a paragraph insertion for an active chapter

**Stack:** `fswatch` + `whisper.cpp` (or the `whisper` skill) + a small classification prompt.

---

## 10. The "Purification" Diff Tool

**Problem:** `purification.jsonl` tracks record mutations, but auditing why a specific image was downgraded is manual and painful.

**Solution:** A small CLI:
```bash
python scripts/purify-diff.py --id gallica-btv1b12345678
```

Output: a split-pane markdown diff showing the before/after of every indicator field, the rule that triggered the change, and the timestamp.

**Bonus:** Wrap it as a custom MCP tool so both Codex and Hermes can query record provenance conversationally.

---

## 11. Student Sandboxing via Git Worktrees

**Problem:** Atlas Lab needs to teach students AI-as-thinking-tool without risking the canonical corpus.

**Solution:** A template repository containing:
- Pre-configured skills (read-only symlink to canonical skills)
- Minimal corpus subset (10 sanitized records)
- Protected `main` branch
- A `student/` branch per learner

Each student works in a git worktree or fork. They run the same pipeline you do. You review their `records.jsonl` diffs instead of PDF essays.

**Learning outcome:** Students learn to treat AI as an instrument of critical inquiry, not a replacement for it.

---

## 12. LLM-as-Librarian

**Problem:** Your Zotero library and vault chapters are vast but unsearchable by semantic intent.

**Solution:** Index everything into a local vector database (Chroma, LanceDB, or the existing Deep Memory plugin):
- Zotero PDFs (chunked)
- Thesis chapters (chunked with paragraph boundaries)
- `vault/zettel/` notes

Then query in natural language:
> "Find every source linking Cesare Beccaria to visual allegory before 1850."

The system retrieves excerpts, cites page numbers, and drafts a paragraph with inline citations.

**Stack:** `sentence-transformers` + Chroma + a thin retrieval skill.

---

## 13. PDF Ingestion Pipeline

**Problem:** Scholars send PDFs. The path from download to cited literature is manual and error-prone.

**Solution:** One-command ingest:
```bash
make ingest-pdf FILE=~/Downloads/article.pdf
```

Steps:
1. Extract text (pdftotext / marker / nougat)
2. OCR if needed (pdf2image + pytesseract)
3. Generate Zotero-ready citation via `zotero-cite` skill
4. I summarize and tag it
5. File it under `vault/literature/YYYY/` with standardized naming

**Output:** A markdown memo + a Zotero import-ready CSL-JSON file.

---

## 14. Reproducible Analysis Containers

**Problem:** "It works on my machine" kills collaboration.

**Solution:** Freeze the `iconocracy` conda env and all pipeline scripts into a reproducible container:
- Option A: Dockerfile + `docker compose up`
- Option B: `pixi` lockfile (faster, no root daemon)
- Option C: `conda-lock` + explicit platform spec

Students and collaborators run the exact same stack. Debugging disappears.

**Priority:** Medium. Only critical if external collaboration scales up.

---

## 15. The Anti-Hallucination Ledger

**Problem:** LLMs hallucinate image descriptions. In legal iconography, a false claim about a sword, a scale, or a blindfold is a methodological catastrophe.

**Solution:** Before any LLM-generated claim about an image, force a grounded tool call:
1. Look up the image's `iconocode` in `records.jsonl`
2. Verify the `manifest_url` resolves
3. Cross-check the `endurecimento` / `dulcificacao` scores
4. Only then permit the descriptive claim

**Enforcement:** Implement as an MCP tool `verify_image_grounding(id, claim)` that returns `VALIDATED` or `MISMATCH: field X says Y, claim says Z`.

Makes the pipeline epistemically rigorous for peer review.

---

## 16. Multimodal Thesis Chapter Rendering

**Problem:** A text-only PDF thesis about visual allegory is an oxymoron. Reviewers cannot zoom into details while reading.

**Solution:** Generate chapters as `.html` with inline IIIF viewers:
```bash
make chapter-html CH=3
```

- Uses OpenSeadragon or simple Gallica tile URLs
- Side-by-side text and image
- Click-to-zoom on allegorical details
- Exportable to static site for committee review

**Host:** Drop the folder into `artifact-preview` or GitHub Pages.

---

## 17. LLM Commit Message Archaeology

**Problem:** Research decisions are buried in git history. You forget why you pivoted from facial-detection to posture-detection indicators.

**Solution:** A script that scans:
```bash
git log --all --grep="iconocode\|ENDURECIMENTO\|Gallica\|purification"
```

And generates a chronological narrative:
- Date of pivot
- Diff summary
- Inferred rationale from commit message body
- Link to relevant issue or note

**Output:** A markdown timeline under `vault/meta/research-archaeology.md`. Useful for methodology chapters and defense prep.

---

## 18. Smart Disk Janitor

**Problem:** Disk is at 94%. You are one Gallica bulk download away from system failure.

**Solution:** A rules-based janitor triggered when `df /` exceeds 96%:
- Delete `node_modules` in stale branches
- Compress raw TIFFs to JPEG2000
- Move Gallica bulk downloads older than 6 months to `/Volumes/ICONOCRACIA/`
- Vacuum SQLite / Chroma vector DBs
- Clear Python `__pycache__` recursively

**Safer:** Run in `--dry-run` mode first, require explicit `--execute` flag.

---

## 19. Iconclass Auto-Completion MCP

**Problem:** Looking up Iconclass codes (e.g., `48C51` = feminist iconography) breaks writing flow.

**Solution:** An MCP server wrapping the Iconclass SKOS dataset:
- Query `iconclass:48C51` → full hierarchy, related codes, Portuguese/English/French labels
- Fuzzy search: "woman with sword" → `48C51(+731)`, `44G124(+5)`
- Auto-insert formatted citation into current document

Never manually browse iconclass.org again.

**Data source:** Iconclass RDF dump, or scrape on first run.

---

## 20. Publish-Ready Pipeline

**Problem:** The gap from final markdown draft to submission-ready DOCX + metadata is tedious.

**Solution:** `make article TARGET=seer`

Steps:
1. Convert markdown chapter to ABNT-formatted DOCX via Pandoc
2. Generate PDF (print-ready and screen-ready variants)
3. Emit SEER/OJS metadata XML (title, abstract, keywords, author data)
4. Generate a cover letter template with editor name and submission date
5. Zip everything into `submissions/YYYY-MM-DD-seer.zip`

One command from draft to portal upload.

---

## Priority Matrix

| Priority | Items | Rationale |
|----------|-------|-----------|
| **Critical / Now** | 6 (disk), 10 (purify-diff), 15 (anti-hallucination) | Blockers for reliability and rigor |
| **High / This Month** | 1 (session state), 4 (ARGOS v2), 5 (dashboard), 8 (zettel) | Compound value over time |
| **Medium / Next Quarter** | 2 (IconoContext), 3 (skill compiler), 9 (voice), 12 (librarian), 13 (PDF ingest), 18 (janitor) | Quality of life and scale |
| **Low / Nice to Have** | 7 (dialectic), 11 (student sandbox), 14 (containers), 16 (HTML thesis), 17 (git archaeology), 19 (Iconclass MCP), 20 (publish pipeline) | Collaboration, pedagogy, and polish |

---

## Open Questions

- Should `.session-state.md` be human-editable, or auto-generated only?
- For ARGOS v2, what is the confidence threshold for auto-append vs. human-review queue?
- Should the Zettelkasten live in Obsidian (markdown) or a graph DB (Neo4j)?
- Is `/Volumes/ICONOCRACIA` reliably mounted, or should the shadow corpus sync be async (rsync cron)?

---

*Next step: Pick one item from the Critical or High tier and spec it into an implementation plan.*
