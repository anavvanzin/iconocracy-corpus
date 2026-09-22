# Common Pandoc Options

## Convert to DOCX

```bash
pandoc input.md -o output.docx
```

**Common options:**
- `--reference-doc=template.docx` - Use custom DOCX template
- `--toc` - Generate table of contents
- `--toc-depth=2` - Set TOC depth level
- `--highlight-style=pygments` - Code highlighting style
- `--metadata="title=My Document"` - Set document metadata
- `--fail-if-warnings` - Exit on warnings
- `--verbose` - Show detailed output

## Convert from DOCX

```bash
pandoc input.docx -o output.md
```

**Common options:**
- `--extract-media=media/` - Extract images to directory
- `-t markdown` - Force Markdown output
- `-t html` - Convert to HTML
- `--standalone` - Create standalone document

## Custom Reference Doc

To create a custom reference doc for DOCX output:

1. Start with a default template:
   ```bash
   pandoc --print-default-data-file reference.docx > reference.docx
   ```

2. Edit styles in Word as needed

3. Use with `--reference-doc=reference.docx`

## Examples

### Markdown to DOCX with TOC
```bash
pandoc report.md -o report.docx --toc --toc-depth=2
```

### DOCX to Markdown with media extraction
```bash
pandoc document.docx -o document.md --extract-media=images/
```

### HTML to DOCX with custom template
```bash
pandoc article.html -o article.docx --reference-doc=my-template.docx
```

### Batch convert Markdown files to DOCX
```bash
for file in *.md; do
  pandoc "$file" -o "${file%.md}.docx"
done
```
