---
name: compilar-tese
description: Compile thesis chapters to DOCX or PDF via Pandoc. Use when the user says "compilar", "make tese", "gerar PDF", "gerar DOCX", or wants to build the thesis.
user-invocable: true
---

Compile the ICONOCRACIA thesis using the Makefile in `vault/tese/`.
Read `vault/tese/README.md` for canonical source paths and PDF prerequisites.
Compile `tese/manuscrito/` sources; treat Markdown chapters in `vault/tese/`
as Obsidian mirrors. Keep editorial numbering; do not add `--number-sections`.

## Usage

- `/compilar-tese` — full thesis as DOCX (default)
- `/compilar-tese pdf` — full thesis as PDF (requires LaTeX)
- `/compilar-tese capitulo-N` — single chapter as DOCX (e.g. `capitulo-3`)
- `/compilar-tese clean` — remove output artifacts

## Steps

1. Check prerequisites:
   ```bash
   command -v pandoc || echo "ERRO: pandoc não encontrado"
   make -C vault/tese bib-check  # required for complete and individual builds
   test -f vault/tese/abnt.csl || echo "AVISO: abnt.csl ausente — estilo ABNT não será aplicado"
   ```

2. Run the appropriate make target:
   ```bash
   # Full DOCX
   make -C vault/tese/ docx

   # Full PDF (LuaLaTeX + TeX Gyre Termes)
   make -C vault/tese/ pdf

   # Single chapter (replace N with chapter number)
   make -C vault/tese/ capitulo-N.docx

   # Clean
   make -C vault/tese/ clean
   ```

3. Report result:
   - On success: path to output file + file size; report the engine/font used for PDF
   - Distinguish missing local TeX/font dependencies from source failures; when
     using a documented engine/font override, report that limitation explicitly
   - On failure: show the Pandoc error, diagnose cause (missing .csl, .bib, bad YAML frontmatter), suggest fix

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `abnt.csl not found` | CSL file missing | Download from citation-style-language/styles |
| `references.bib not found` | BibTeX missing | Export from Zotero |
| `LaTeX Error` | Missing LaTeX package | Use DOCX target instead, or install texlive |
| `YAML parse error` | Bad frontmatter in chapter | Check the chapter file indicated in error |
