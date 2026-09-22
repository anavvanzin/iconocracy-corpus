# Atlas Lab v1 — first implementation slice

Date: 2026-04-10

## What this slice implements

This first Atlas Lab slice establishes a public-facing v1 shell for the ICONOCRACY module in `corpus/atlas-iconometrico.html`.

Implemented in this slice:
- Atlas Lab umbrella framing instead of a module-only atlas screen
- three visible entry routes:
  - Learning Mode
  - Research Mode
  - Explore Module / ICONOCRACY
- one guided Learning Mode exercise centered on `P2 · Calcificação da Justitia`
- one demonstrative Research Mode workspace with active comparative panels `P1–P3`
- one public module surface that still exposes the broader v1 atlas view with 5 demonstrative panels
- extracted shared demonstrative config and seed-data files under `tools/atlas_lab/data/`

This is a demonstrative front-end slice, not a full Atlas Lab product build.

## How Learning Mode and Research Mode differ

### Learning Mode
Learning Mode is the guided entry path.
It is designed for first-pass reading, teaching, and training visual attention before interpretation.

Current behavior:
- starts from a fixed exercise
- narrows the comparison to two entries
- asks the user to describe first, compare second, hypothesize third
- keeps explanation layers legible and scaffolded
- reserves AI for a later reflective challenge after user notes exist

### Research Mode
Research Mode is the comparative workspace entry path.
It is designed for panel-led inquiry and early hypothesis building.

Current behavior:
- starts from a panel workspace rather than a single guided exercise
- lets the user move across the currently implemented comparative panels
- foregrounds regime framing, indicator vocabulary, and coding prompts
- treats comparison as an analytical workflow: observe, code, interpret
- still remains demonstrative rather than fully data-driven

In short:
- Learning Mode teaches how to see and compare
- Research Mode structures how to work through a panel hypothesis

## Where future AI integration belongs

AI is intentionally not implemented as an authoritative answer layer in this slice.
Future AI integration belongs only after user observation and comparison are already present.

Planned insertion points:
- Learning Mode step 4 (`AI em breve`): return a reflective challenge, counter-reading, or follow-up question based on the user’s notes
- Research Mode panel workspace: generate comparison prompts, counter-hypotheses, or coding challenges from the selected entries and current panel
- shared explanation layers: optionally translate between public, learning, and research registers without replacing the user’s own reading

AI should remain:
- downstream of user input
- constrained by panel context and selected entries
- framed as reflective support, not as the source of truth

## What remains intentionally unfinished

The following are intentionally unfinished in this first slice:
- no live AI integration yet
- no canonical-data hydration from `data/processed/records.jsonl` or `corpus/corpus-data.json`
- no extraction of the full inline React app out of `corpus/atlas-iconometrico.html`
- no persistence layer for notes, coding state, or panel sessions
- no full Research Mode implementation for all 5 demonstrative panels
- no broader module system beyond the featured ICONOCRACY route
- no final thesis-wide panel model beyond the current demonstrative v1 surface

## File roles in this slice

- `corpus/atlas-iconometrico.html`
  - active public implementation surface for the first slice
- `tools/atlas_lab/data/atlasLabConfig.js`
  - shared Atlas Lab / ICONOCRACY v1 demonstrative metadata and panel definitions
- `tools/atlas_lab/data/iconocracySeedData.js`
  - shared demonstrative seed entries, comparison pairs, and panel-role helpers
- `docs/atlas-lab-task-1-implementation-note.md`
  - earlier review note that justified this implementation direction

## Slice status

The first Atlas Lab implementation slice is complete as a demonstrative shell.
It is documented, internally coherent, and intentionally partial.
Future work should extend from the extracted `tools/atlas_lab/data/` layer rather than adding more hidden scope into the HTML shell.
