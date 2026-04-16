---
name: pandoc-fix
description: Use when Pandoc compile of the ICONOCRACIA thesis fails — undefined citation keys, LaTeX package errors, Markdown→LaTeX escape issues (underscores, ampersands, unicode), YAML frontmatter errors, missing .csl/.bib, or broken cross-references. Diagnoses the error, applies minimal fix, re-runs compile.
disable-model-invocation: true
---

# pandoc-fix

Diagnose and patch Pandoc compile errors for `vault/tese/`. Distinct from `compilar-tese` (which just runs `make`). Use AFTER a compile fails.

## When to invoke

- `pandoc: Error producing PDF`
- `LaTeX Error: File 'X.sty' not found`
- `Could not find reference '@citationkey'`
- `! Undefined control sequence`
- `YAML parse exception`
- `citeproc: reference X not found`
- Garbled output: unicode chars dropped, footnotes misplaced, tables breaking

## Workflow

1. **Capture error.** Re-run failing command with full log:
   ```bash
   cd vault/tese && make docx 2>&1 | tee /tmp/pandoc-err.log
   # PDF path: add -V debug, or retry with --verbose
   make pdf 2>&1 | tee /tmp/pandoc-err.log
   ```

2. **Classify** using the table below. Pick fix category BEFORE editing.

3. **Apply minimal fix.** One error class per edit — don't bundle.

4. **Re-run same target.** If new error → repeat. If same error → fix didn't land, inspect.

5. **Commit** fix with message naming the error class (e.g. `fix(tese): escape underscores in capitulo-3 code refs`).

## Error classes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `reference X not found` (citeproc) | `@chaveCitacao` missing in `references.bib` | Add BibTeX entry to `vault/tese/references.bib`. Export from Zotero → BibLaTeX format. Match key exactly. |
| `File 'abntex2.sty' not found` | LaTeX package missing | Install: `brew install --cask mactex-no-gui` OR switch to DOCX: `make docx`. |
| `! Package inputenc Error: Unicode character` | PDF engine lacks UTF-8 | Use XeLaTeX: add `--pdf-engine=xelatex` to `PANDOC_PDF` in Makefile. |
| `! Undefined control sequence \something` | Raw LaTeX in .md not loaded via preamble | Wrap in `\newcommand` in `header-includes`, or remove the macro and use Markdown syntax. |
| `YAML parse exception` | Bad frontmatter (unquoted colon, stray `---`) | Run `python -c "import yaml; yaml.safe_load(open('capitulo-N.md').read().split('---')[1])"` on indicated file. |
| Underscores render as subscript in PDF | Unescaped `_` in prose | Replace `word_with_underscore` → `word\_with\_underscore` OR use backticks for code. |
| `&` breaks LaTeX | Unescaped ampersand | Replace `&` → `\&` outside code fences. |
| Quoted text breaks | Fancy quotes `"..."` in LaTeX context | Use straight `"..."` or `--variable:smart` flag. |
| `toc` empty / wrong depth | `--toc-depth=3` but headings deeper | Either raise depth or reduce heading levels. |
| Images missing in output | Relative path broken when Pandoc runs from `vault/tese/` | Use paths relative to Makefile cwd, or `--resource-path=.:../.:../..` |
| `csl parse error` | Corrupted `abnt.csl` | Re-download from `citation-style-language/styles/blob/master/associacao-brasileira-de-normas-tecnicas.csl`. |
| Bibliography empty in DOCX | No `--citeproc` or `.bib` not loaded | Check Makefile: `PANDOC_COMMON` must contain `--citeproc` AND `--bibliography=$(BIB)`. |

## Citation key repair

Most common thesis failure. Pipeline:

```bash
# 1. List all [@key] in chapters
grep -rEho '\[@[a-zA-Z0-9_-]+\]' vault/tese/*.md | sort -u > /tmp/cited.txt

# 2. List all @key in bib
grep -E '^@' vault/tese/references.bib | sed -E 's/@[a-zA-Z]+\{([^,]+),.*/\1/' | sort -u > /tmp/defined.txt

# 3. Diff — keys cited but not defined
comm -23 <(sed 's/\[@\(.*\)\]/\1/' /tmp/cited.txt | sort -u) /tmp/defined.txt
```

Each missing key → either (a) add to `references.bib` via Zotero export, or (b) fix typo in chapter.

## LaTeX escape cheat

Characters needing `\` escape in Markdown prose destined for PDF:

`& % $ # _ { } ~ ^ \`

Regex to find unescaped underscores in a chapter (skip code fences):

```bash
awk '/^```/{f=!f;next} !f' vault/tese/capitulo-3.md | grep -nE '[^\\]_[a-zA-Z]'
```

## Red flags — stop before editing

- About to edit chapter but haven't read the error log verbatim → read log first.
- About to bulk `sed` escape all `_` → will break code blocks and `references.bib` keys. Use awk with code-fence state.
- About to install LaTeX packages → check DOCX target works first; DOCX rarely blocks on LaTeX.
- Error mentions line number in generated `.tex` not `.md` → map back via `pandoc --verbose` output.

## Common mistakes

- **Editing output file instead of source.** `output/tese_completa.tex` is generated; fix `.md` chapters.
- **Fixing symptom not cause.** If three chapters show same error, fix pattern once via script.
- **Skipping `make clean` between iterations.** Stale `.aux` files mask fixes.
- **Committing generated artifacts.** `output/` should be gitignored.
