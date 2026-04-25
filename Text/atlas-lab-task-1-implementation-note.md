# Atlas Lab v1 — Task 1 implementation note

Date: 2026-04-10
Scope audited:
- `tools/atlas_lab/AtlasLab_original.jsx`
- `corpus/atlas-iconometrico.html`
- `tools/scripts/atlas_mapping.py`

## Recommendation in one line
Use `corpus/atlas-iconometrico.html` as the v1 implementation surface, but reposition it as an Atlas Lab shell for the ICONOCRACY module and extract only the reusable view/data pieces from the legacy Atlas code.

## What can be reused

### Reusable UI pieces
- Atlas gallery pattern in `corpus/atlas-iconometrico.html`:
  - regime filter bar
  - image card grid
  - right-side detail panel / drawer
  - compact atlas statistics header
- Visual treatment already coherent with ICONOCRACY:
  - dark research-studio palette
  - regime color coding
  - panel badges / chips
  - image-first comparative browsing
- Detail-panel iconeometric profile:
  - radar chart pattern is useful for Research Mode and can later be simplified for Learning Mode
- Standalone embedding pattern:
  - the page already mounts a React app into `#atlas-root`, so it is the lowest-risk place to evolve the first slice without building a separate product shell first

### Reusable data/constants
- Shared seed corpus structure present in both Atlas files:
  - id, title, date, country, medium, archive, image, regime
  - this is a workable demo-level entry shape for v1
- ICONOCRACY indicator vocabulary:
  - FEI, CII, PRI, SMI, SMS, AMCP, MVI, WI, RI, AI
  - can be reused as Research Mode vocabulary, with a reduced subset later exposed in Learning Mode
- Regime taxonomy:
  - Fundacional-Sacrificial
  - Normativo-Jurídico
  - Militar-Imperial
  - the labels/colors are already usable as shared conceptual constants
- Existing panel labels in the public atlas page:
  - useful as demonstration copy for ICONOCRACY panel previews
- `tools/scripts/atlas_mapping.py` provides reusable research reference material:
  - panel naming candidates
  - keyword sets for panel association experiments
  - mapping output shape that could later support research-side panel suggestions

## What should be replaced or deprecated

### Replace
- Top-level product identity `Atlas Iconométrico`
  - for v1 the page should become `Atlas Lab` as umbrella platform, with `ICONOCRACY` clearly framed as the featured module
- Single-surface atlas browsing
  - v1 needs explicit Learning Mode and Research Mode entry points instead of one undifferentiated atlas screen
- Inline duplicated constants across files
  - `CORPUS` / `REFERENCE_CORPUS`, `REGIMES`, `PANELS`, and indicator labels should move into shared extracted constants for reuse

### Deprecate
- Firebase/Gemini Canvas bootstrapping in `AtlasLab_original.jsx`
  - depends on injected globals (`__firebase_config`, `__app_id`, `__initial_auth_token`)
  - not appropriate as the v1 foundation inside this repo
- Incomplete legacy app path in `AtlasLab_original.jsx`
  - the file itself states the app is adapted from Gemini Canvas and is incomplete
  - `exportToLabCSV` is referenced but missing
  - the component body is not actually present in the checked-in file, so it should be treated as archival reference, not active implementation base
- Audio helper code in `AtlasLab_original.jsx`
  - unrelated to the first implementation slice and should not be carried into v1
- Large inline Babel/React/Recharts app inside `corpus/atlas-iconometrico.html`
  - acceptable as the current target surface, but should be treated as transitional and gradually extracted into maintainable modules
- Heuristic panel-mapping logic as source of truth
  - `atlas_mapping.py` uses keyword matching over vault markdown and is useful for experiments only
  - it should not define the canonical panel model for v1 UI

## Important inconsistencies found
- Panel-model mismatch:
  - `AtlasLab_original.jsx` and `corpus/atlas-iconometrico.html` expose 5 panel labels
  - `atlas_mapping.py` defines 8 thesis panels
  - v1 must choose one explicit panel surface instead of silently mixing both
- Data duplication:
  - the same seed corpus and conceptual constants are duplicated across the legacy JSX and the public HTML
- Product-layer mismatch:
  - current public page is module-first (`Atlas Iconométrico`), while the new product direction is platform-first (`Atlas Lab` → `ICONOCRACY`)
- Pedagogical mismatch:
  - current atlas UI is a browse-and-inspect interface, but the planned product requires mode separation and AI framed as reflective scaffold

## Best target surface for v1

### Primary target
Evolve `corpus/atlas-iconometrico.html` into the first Atlas Lab shell.

Why:
- it already works as a standalone public-facing surface
- it already contains the strongest reusable UI pieces
- it avoids reviving the incomplete Firebase/Gemini implementation
- it is the fastest route to proving the first slice goals in a visible way

### Supporting extraction target
Use `tools/atlas_lab/` as the extraction area for:
- shared constants/config
- reusable React view components
- mode metadata and ICONOCRACY seed content

### Role of `atlas_mapping.py`
Keep it as an offline research-support script, not the main implementation surface.
It can inform later Research Mode features such as:
- candidate panel suggestions
- vault-to-panel experiments
- comparison prompts for researchers

## Explicit implementation decisions for v1

### Canonical data decision
For v1, separate canonical production data from demonstrative UI seed data.

- Canonical repository data remains:
  - `data/processed/records.jsonl` as source of truth
  - `corpus/corpus-data.json` as public export
- Front-end demonstrative seed data for the first slice should be extracted into shared JS constants under `tools/atlas_lab/`.
- The first Atlas Lab shell should not attempt a full corpus migration yet.
- Therefore Task 2 should create shared seed/config files for UI work, while leaving future integration with `corpus/corpus-data.json` as a later step.

### Canonical panel decision
For v1, the front-end should use a 5-panel demonstrative surface derived from the existing public atlas, not the 8-panel thesis mapping from `atlas_mapping.py`.

Reason:
- the 5-panel surface already exists in the current atlas-facing UI
- it is enough to prove Learning Mode vs Research Mode and the Atlas Lab shell
- the 8-panel thesis logic can later become a richer Research Mode extension

Implication:
- `atlas_mapping.py` should not drive front-end panel state in v1
- the 5-panel v1 surface must be treated explicitly as a demonstrative panel model, not as the final thesis-wide canonical panel system

## Proposed v1 surface shape
- Atlas Lab shell at top level
- Featured module: ICONOCRACY
- Explicit mode choices:
  - Learning Mode
  - Research Mode
- One demonstrative ICONOCRACY path in each mode
- Short visible AI philosophy block stating:
  - observe first
  - compare before concluding
  - AI responds after user input
  - AI supports reflection, not authority

## Task 2 implementation target
Task 2 should produce extracted shared front-end constants/config, likely under `tools/atlas_lab/`, with at minimum:
- platform metadata (`Atlas Lab`)
- module metadata (`ICONOCRACY`)
- mode metadata (`learning`, `research`)
- 5-panel demonstrative front-end panel definitions
- small seed entry set for UI proof-of-concept

Task 2 is done when:
- front-end constants are no longer duplicated inline across legacy atlas surfaces
- there is one explicit place to read v1 mode/panel/platform metadata
- the distinction between demo UI data and canonical corpus data is documented

## Task 3 implementation target
Task 3 should reshape `corpus/atlas-iconometrico.html` into an Atlas Lab shell that visibly provides:
- Atlas Lab umbrella identity
- ICONOCRACY as featured module
- Learn entry point
- Research entry point
- short AI philosophy block

Task 3 is done when:
- a first-time user can tell within seconds that this is not only an atlas browse screen
- Learning vs Research are visibly distinct entry paths
- the page still functions as the repo’s easiest public-facing implementation surface

## Practical reuse decision
- Reuse from `corpus/atlas-iconometrico.html`:
  - yes, as the visible base surface
- Reuse from `AtlasLab_original.jsx`:
  - partial only: constants, naming clues, and any view ideas worth extracting
  - no, as direct application base
- Reuse from `atlas_mapping.py`:
  - yes, as research logic reference only
  - no, as canonical panel model or front-end data source

## Bottom line
The safest and cleanest v1 path is not to resurrect the old Atlas app. It is to reframe the existing public atlas page as the first Atlas Lab shell, extract the duplicated ICONOCRACY constants into shared files, and build explicit Learning/Research mode entry points around that surface.