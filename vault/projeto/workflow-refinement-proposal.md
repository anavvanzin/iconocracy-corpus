---
tags: [meta, workflow, proposal]
date: 2026-06-19
status: draft
---

# Iconocracy Workflow and Infrastructure Modernization: A Unified Plan for High-Velocity Research and Writing

As the Iconocracy monorepo approaches its 2026 defense milestones, the technical overhead of running the corpus pipeline, managing metadata in `records.jsonl`, and organizing 314+ catalog cards presents both a bottleneck and an opportunity. To maximize research efficiency and reduce context fatigue, this proposal outlines a comprehensive roadmap to modernize our infrastructure and transform the writing pipeline. By implementing immediate, low-overhead solutions—such as session resurrection protocols, automated zettelkasten generation, local health dashboards, and dialectic agents—we can establish a bottom-up research environment where polished thesis chapters emerge directly and naturally from daily analysis.

## 1. Immediate Infrastructure Improvements

### 1.1 Session Resurrection Protocol

To solve the "cold-start" friction where every new AI session requires re-explaining active files and current research goals, we propose establishing a rolling `.session-state.md` file in the repo root. This file serves as a handoff artifact between sessions.

> [!TIP] **Session State Schema**
> Maintain this structure at the root of the workspace:
> ````markdown
> # Session State — [Current Date]
> - **Active Files**:
>   - `[file_path]` — [purpose]
> - **Current Thesis Focus**: [active chapter or concept]
> - **Last Verification Run**: `[command]` — [result]
> - **Next Planned Step**: [next task]
> - **Pending Decisions**:
>   - [ ] [question for next startup]
> ````
> On starting any new chat, the contents of this file are pasted as the first message to guarantee instant continuity.

### 1.2 Context & Disk Optimization

As the corpus expands, parsing raw data files like `records.jsonl` eats up the model's context window and slows down reasoning. To optimize memory footprint and local disk constraints, we propose:

* **The IconoContext Daemon**: A lightweight local background server that watches `data/processed/records.jsonl` and exposes a summary of corpus health. Instead of reading megabytes of JSONL, the agent curls a quick summary.
* **Skill Compiler**: A sync script (`tools/scripts/compile_skills.py`) that aggregates project-specific instructions from custom skills and keeps `AGENTS.md` updated automatically.
* **Shadow Corpus Symlinking**: Moving heavy image binaries in `data/raw/` to a dedicated external mount (`/Volumes/ICONOCRACIA/`), replacing them with local metadata references to prevent system disk exhaustion.

#### Proposed IconoContext Endpoint Response Sample (`GET /status`)
```json
{
  "total_records": 265,
  "recent_ingests": ["FR-048", "PT-004"],
  "purification_means": {
    "desincorporacao": 1.8,
    "rigidez_postural": 2.1,
    "uniformizacao_facial": 1.5
  },
  "schema_errors": 0
}
```

---

## 2. Data Pipeline, Provenance, and Rigor

### 2.1 Autonomous Gallica Harvester (ARGOS v2)
To close the gap between discovering allegorical items and ingesting them into our dataset, we propose a cron-backed MCP loop. ARGOS v2 will run scheduled queries against the Gallica API (filtering by keywords like `allegorie`, `justice`, `droit`, `femme`), download metadata and IIIF manifests, run initial analyses, and format items for the review queue.

### 2.2 The "Purification" Diff Tool & Anti-Hallucination Ledger
Auditability and accuracy are paramount to our methodology. Two mechanisms ensure data integrity:

1. **The CLI Diff Tool (`scripts/purify-diff.py`)**: Provides a visual split-pane comparison of indicator changes during the *endurecimento* coding process.
2. **The Anti-Hallucination Ledger**: An MCP tool that checks claims about an image against its official database profile before outputting text.

#### Sample output of `purify-diff.py --id gallica-btv1b12345678`:
```markdown
+------------------------------------+------------------------------------+
| BEFORE (2026-06-01)                | AFTER (2026-06-18)                 |
+------------------------------------+------------------------------------+
| desincorporacao: 1                 | desincorporacao: 3                 |
| rigidez_postural: 2                | rigidez_postural: 2                |
| uniformizacao_facial: 0            | uniformizacao_facial: 1            |
| comment: Initial categorization.   | comment: Downgraded based on rule  |
|                                    | 4B (Uniformization of facial features)|
+------------------------------------+------------------------------------+
* Triggered by: rule_validation.py (line 124)
```

### 2.3 The ENDURECIMENTO Dashboard
A static HTML dashboard, built directly from `records.jsonl` and served on a local port, will provide real-time visualizations of:
* Histograms of the 10 purification indicators.
* Temporal lines showing the distribution of allegorical regimes (FUNDACIONAL → NORMATIVO → MILITAR → CONTRA-ALEGORIA).
* Missing-data heatmaps and verification warnings.

---

## 3. Research-to-Writing Workflows

### 3.1 Luhmann-Style Zettelkasten & Voice Memo Processing
To capture fleeting insights and build a robust, bottom-up argumentative base:
* **Zettelkasten Memos**: Every research session automatically outputs an atomic card in `vault/zettel/` containing a single idea, a unique index, and wikilinks back to existing nodes.
* **Voice-to-Text Transcription**: An automated watcher on `inbox/audio/` runs Whisper transcription when voice memos are dropped in, allowing the agent to parse them directly into drafts, todo lists, or catalog card candidates.

### 3.2 Semantic Scholar & PDF Ingestion
To eliminate the manual drag of literature management, the `make ingest-pdf FILE=~/Downloads/article.pdf` command will:
1. Extract text and run OCR if necessary.
2. Generate a Zotero-ready metadata profile.
3. Automatically summarize and file a Markdown memo under `vault/literature/`.

### 3.3 Hegelian Dialectic & Iconclass Auto-Completion
* **Dialectic Writing Agents**: For critical thesis chapters, we use three agents (Thesis, Antithesis, Synthesis) to write the affirmative argument, challenge it with counterarguments, and reconcile them.
* **Iconclass Auto-Completion MCP**: Fuzzy-search Iconclass codes directly in the editor (e.g., searching "woman with sword" returns `44G124`) to speed up bibliographic annotation.

---

## 4. Pedagogy, Rendering, and Publication

### 4.1 Multimodal Thesis Chapters
A custom compiler will output chapters as interactive HTML pages with embedded IIIF viewers (like OpenSeadragon). Reviewers will be able to zoom into high-resolution allegorical details inline with the text.

### 4.2 Student Sandboxing & Containers
To train students in the Atlas Lab safely:
* **Reproducible Containers**: The `iconocracy` environment is frozen via `pixi` or a Docker container.
* **Git Worktrees**: Students work on sandboxed branches (`student/name`) with read-only symlinks to the canonical vault, submitting their diffs for review.

### 4.3 Publish-Ready Pipeline
A single command (`make article TARGET=seer`) compiles markdown drafts to ABNT-compliant DOCX, renders PDFs, generates SEER/OJS submission XMLs, and packages them into a zip file.

### 4.4 Git Archaeology
A script that parses git logs for keywords like `purification` or `ENDURECIMENTO` to auto-generate a chronological research diary, recording key methodology decisions for the defense.

---

## 5. Implementation Priority Matrix

| Priority | Items | Rationale |
| :--- | :--- | :--- |
| **Critical / Now** | 6 (Shadow Corpus), 10 (Purify Diff), 15 (Anti-Hallucination) | Essential for data reliability, verification, and disk survival. |
| **High / This Month** | 1 (Session State), 4 (ARGOS v2), 5 (Dashboard), 8 (Zettelkasten) | Delivers compounding value and immediate velocity. |
| **Medium / Next Quarter** | 2 (IconoContext), 3 (Skill Compiler), 9 (Voice), 12 (Scholar), 13 (PDF Ingest) | Improves quality of life, ingestion efficiency, and searchability. |
| **Low / Nice to Have** | 7 (Dialectic), 11 (Student Sandbox), 16 (HTML Thesis), 20 (Publish Command) | Enhances collaboration, pedagogy, and final thesis polish. |

---

## 6. Open Questions for Review

> [!WARNING] **Methodological and Infrastructure Decisions**
> 1. **ARGOS v2 Threshold**: What threshold of confidence should trigger automatic insertion vs. redirecting to the human review queue?
> 2. **Zettelkasten Storage**: Should the Zettelkasten note graph reside as standard Markdown in Obsidian, or should we query it via a local graph database (e.g., Neo4j)?
> 3. **Mount Reliability**: Is the `/Volumes/ICONOCRACIA` drive mounted consistently enough to handle automated background symlinking, or should we run it on-demand?
