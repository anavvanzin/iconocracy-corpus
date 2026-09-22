---
name: abnt-precommit
description: Use before committing thesis chapters (vault/tese/*.md, tese/manuscrito/*.md) to catch ABNT NBR 6023:2025 violations — missing page refs on direct quotes, malformed (AUTOR, ano) in-text citations, orphan [@key] without matching BibTeX entry, missing "Acesso em:" on URL references. Runs regex gate first, then delegates LLM-level review to abnt-checker agent.
---

# abnt-precommit

Fast gate before commit. Two-layer: regex script (deterministic, seconds) → `abnt-checker` agent (LLM, minutes).

## When to invoke

- User says "commit", "preparar commit", "antes de commit" on thesis chapters
- Before `/compilar-tese` for release builds
- After importing references from Zotero
- Symptoms: "check ABNT", "verificar citações", "validar referências"

## Workflow

1. **Identify target files.** Default: staged `.md` in `vault/tese/` + `tese/manuscrito/`. Override: user-supplied path.

   ```bash
   git diff --cached --name-only --diff-filter=ACM | grep -E '(vault/tese|tese/manuscrito)/.*\.md$'
   ```

2. **Run regex gate** (`check.sh`). Exits non-zero on hard violations. Three classes:
   - Direct quote >3 lines without page number
   - `[@citationkey]` not present in `references.bib`
   - URL reference missing `Acesso em:`

3. **If regex passes**, dispatch `abnt-checker` agent on each chapter for semantic review (author order, italics vs bold, punctuation).

4. **Report.** Aggregate errors by file:line. User decides commit/fix.

5. **Optional hook install.** If user says "instalar hook", symlink `check.sh` as `.git/hooks/pre-commit`.

## Quick reference — ABNT NBR 6023:2025

| Element | Rule | Example |
|---------|------|---------|
| In-text | `(SOBRENOME, ano)` or `Sobrenome (ano, p. X)` | `(FOUCAULT, 1975, p. 32)` |
| 4+ authors | `et al.` | `(SILVA et al., 2020)` |
| Direct quote >3 lines | indented, 10pt, **page required** | must have `, p. N` |
| Book ref | SOBRENOME, Nome. **Título**. Local: Editora, ano. | titles **bold**, not italic |
| Online | + `Disponível em: <url>. Acesso em: dd mmm. aaaa.` | `Acesso em: 14 abr. 2026.` |
| Date format | `dd mmm. aaaa` | `14 abr. 2026` (lowercase month abbr) |

## Hard errors (regex-catchable, block commit)

- Direct quote block `>` 3 linhas sem `p. \d+`
- `[@key]` sem entry `@type{key,` em `references.bib`
- URL em ref list sem `Acesso em:`
- `*Título*` (italic) em ref list — deve ser `**Título**` (bold, ABNT 2025)

## Soft errors (agent review, warn not block)

- Author order (alfabética)
- Punctuação inconsistente
- Capitalização de título
- `p.` vs `pp.` mix

## Red flags

- About to `--no-verify` to skip → **don't**. Fix cite or explicitly defer via commit message flag `[abnt-defer: reason]`.
- Script reports zero errors but chapter has Turabian-style refs → regex misses mixed styles; run agent pass.
- `references.bib` changed but no chapters changed → still run (bib keys may have been renamed).

## Usage

```
/abnt-precommit              # check staged thesis files
/abnt-precommit capitulo-3   # check specific chapter
/abnt-precommit --install    # install as git pre-commit hook
```

See `check.sh` for implementation.
