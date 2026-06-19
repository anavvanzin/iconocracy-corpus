# Dialectic — Single Source of Truth for the Iconocracia Corpus
## Round 1 · Context Briefing
_2026-06-19 · orchestrator: Claude (belief-free seat) · domain: mixed (empirical infra × normative scholarly method)_

## The decision under tension
Ana is designing a "serious, methodological data approach" — starting with **single source of truth (SSOT)**. Through brainstorming she chose, consistently, the most rigorous option each time:
- **Master store:** a SQLite database (not the git ledger, not the vault).
- **Provenance:** event-sourced / append-only — every change (ingest, code, recode, quarantine, metadata-fix) an immutable event; current state = projection.
- **Goal:** consolidate the many independent writers (Claude Code, Antigravity/Gemini, crons, manual edits) into one disciplined flow. Exports (records.jsonl, corpus-data.json, companion, vault notes) become deterministic projections.

## Why this is dialectic-worthy (not just lookup)
The choice is *internally coherent* but rests on an unexamined ontological commitment. The genuine, deep contradiction:

> **Is the Iconocracia corpus a DATASET or a HERMENEUTIC APPARATUS?**

- If a **dataset** (quantitative instrument), then event-sourced DB rigor is not optional — the thesis's empirical claims (endurecimento distributions, regime comparisons, Kruskal-Wallis) are unfalsifiable without reproducible coding provenance.
- If a **hermeneutic apparatus** (interpretive object in legal-iconographic history), then the single source of truth is Ana's *interpretive judgment* recorded in prose; an event-sourced DB imposes a positivist frame alien to the discipline, manufactures false precision from 0–3 ordinal codings, and — critically — consumes the one scarce resource (Ana's time/attention) that determines whether the thesis ships.

Degenerate framings to forbid: "DB vs files," "rigor vs speed," "structured vs unstructured." Both monks must argue at the ontological level.

## Concrete situation (ground both monks here)
- **Researcher:** Ana Vanzin, solo doctoral candidate, PPGD/UFSC. Field: criminal-law history / legal iconography (NOT data science). Defense/quali ~Nov 2027. Writes in Obsidian.
- **Corpus:** ~265–309 records (the exact number is itself contested — drift across stores is the precipitating wound). Female allegorical figures, coded on 10 ordinal "purification/endurecimento" indicators (0–3) across regimes (fundacional/normativo/militar/contra-alegoria).
- **The wound (this session, verbatim):** could not trust any corpus count (264/265/309/165); acted on a stale git fork (local 18-ahead/17-behind origin); rediscovered work already done on the remote (a quarantine-uncoded mechanism + tag script existed since 2026-05-30). Multiple AI tools writing to scattered JSON files = the divergence engine.
- **Existing pipeline:** records.jsonl (master ledger, UUID `item_id`) → records_to_corpus.py → corpus-data.json (export, semantic `id` BR-001) → companion-data.json; purification.jsonl (per-run coding ledger); vault_sync.py (BIDIRECTIONAL vault↔ledger — itself a divergence source); CI validates master↔export parity.
- **Prior vetted decision** (`docs/decisions/DIALETICA-N165-vs-265.md`, post-santa-loop): the corpus is a "versioned object," analytic validity = coding-instrument-provenance stratum, NOT date. 41 uncoded items excluded by definition. This already leans "dataset," but only for the *analytic* slice.
- **Tools in play:** Claude Code, Antigravity (Gemini-based IDE), crons/agents, manual edits. Multiple machines (Mac, an SSD that is a Linux mirror, GitHub remote). SQLite already present in her stack (iconclass-db, corpus-vault MCPs).

## Belief-burden calibration (Convergent-Visionary pattern)
Ana converged fast on "maximum rigor = right." She needs the two fully-believed futures held *outside* her so she can judge from the belief-free seat.
- **Monk A** validates the rigor vision at full conviction (so she can release it without it being "dismissed"): the corpus IS a dataset; event-sourced SQLite SSOT is the only defensible foundation.
- **Monk B** believes the strongest *alternative* at full conviction (NOT "rigor is bad"): the corpus is a hermeneutic apparatus; the true SSOT is the scholarly writing practice; the DB is a category error that will starve the thesis and worsen the real problem (tool proliferation) by adding another tool.

## Ontological question driving both prompts
**"What is the single source of truth for a doctoral corpus — the data store that holds it, or the scholarly practice that produces it? And does answering 'the store' silently convert a hermeneutic object into a positivist one?"**
