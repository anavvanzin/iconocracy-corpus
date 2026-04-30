# Corpus Inventory — Design Spec

## Goal
Extract neutral metadata from all 288 SCOUT candidate files (`vault/candidatos/SCOUT-*.md`) into a structured table for pattern analysis.

## Fields
- **SCOUT ID** (e.g. SCOUT-090, SCOUT-ZW-01)
- **Title**
- **Country** (`pais` from frontmatter)
- **Century** (derived from `data_estimada`)
- **Medium** (`suporte` from frontmatter)
- **Figure type** (`motivo_alegorico` from frontmatter)
- **Iconclass** (if present)
- **Promoted?** (cross-reference: `records_item_id` in frontmatter = already in ledger)

## Approach
Python script reads YAML frontmatter from all .md files, parses, outputs CSV. No interpretation in this phase — pure extraction. ZW (Zwischenraum) files included but flagged with a `type` column.

## Output
`docs/superpowers/inventory/2026-04-29-corpus-inventory.csv`

## Next steps after extraction
Pivot table by country, century, medium, figure type — let patterns surface.
