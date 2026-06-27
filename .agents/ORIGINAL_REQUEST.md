# Original User Request

## Initial Request — 2026-06-27T00:32:22Z

Integrate curated contra-allegory cases (specifically CONTRA-002, CONTRA-003, and CONTRA-004) into the research corpus and thesis drafts for the ICONOCRACIA project.

Working directory: /Users/ana/Research/hub/iconocracy-corpus
Integrity mode: development

## Requirements

### R1. Source Verification
Verify the institutional STF report for the 1975 internal sculpture (CONTRA-002) and locate high-quality visual/archival sources (e.g. AFP/Getty) for Deborah de Robertis' performance (CONTRA-004) to prevent weak journalistic citations.

### R2. Candidate Creation
Create candidate Markdown files for the three cases (CONTRA-002, CONTRA-003, and CONTRA-004) under the `vault/candidatos/` directory, following the project's standard metadata schema and naming convention.

### R3. Thesis Draft Update
Integrate the three selected cases into the existing §3.4 drafts located in `vault/tese/drafts/sumario-iconocracia.md` and `tese/manuscrito/sumario_iconocracia.md` as outlined in `docs/decisions/CONTRA-ALEGORIAS-INTEGRATION-2026-06-26.md`.

## Acceptance Criteria

### Schema Validation
- [ ] The command `python tools/scripts/validate_schemas.py` executes successfully and reports zero schema or syntax errors on the newly created candidate files in `vault/candidatos/`.

### Draft Integration
- [ ] The files `vault/tese/drafts/sumario-iconocracia.md` and `tese/manuscrito/sumario_iconocracia.md` contain corresponding references/text integrating CONTRA-002, CONTRA-003, and CONTRA-004 into the §3.4 section.
