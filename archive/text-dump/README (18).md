# iconocracy-ingest

Repeatable ingestion pipeline for scanned archival material from Biblioteca Nacional Digital (BND), Câmara dos Deputados, Senado Federal, and Internet Archive. Designed for the Iconocracy doctoral research project (PPGD/UFSC).

## What it does

1. **Discovers** all supported files (PDF, TIFF, PNG, JPEG, JP2) in a given folder recursively
2. **Detects language** (Portuguese, Spanish, French, Italian, English, German, Latin) using `langdetect` on a quick OCR pass
3. **Runs Tesseract OCR** with the detected language, producing per-page confidence scores
4. **Extracts captions and figure mentions** — labels like `Figura 1`, `Fig. 2`, `Illustration 3`, `Fonte:`, `Source:`, technique/medium descriptions in parentheses, across PT/ES/FR/IT/EN
5. **Renames files** consistently: `{SOURCE}_{YEAR}_{SEQ:04d}_{sanitized-stem}.{ext}`
6. **Appends metadata** to a master CSV, using SHA-256 file hashes for deduplication
7. **Generates an HTML quality report** flagging low-confidence pages for manual review
8. **Logs each run** as a JSON audit trail

## Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Ensure Tesseract + language packs are installed
sudo apt install tesseract-ocr tesseract-ocr-por tesseract-ocr-spa \
    tesseract-ocr-fra tesseract-ocr-ita tesseract-ocr-deu tesseract-ocr-lat \
    poppler-utils

# Preview what would be processed (no OCR)
python ingest.py /path/to/new/batch --dry-run

# Run the pipeline
python ingest.py /path/to/new/batch

# Custom output directory
python ingest.py /path/to/batch --output /path/to/project/output

# Move files instead of copying
python ingest.py /path/to/batch --no-copy

# Custom confidence threshold (default: 60)
python ingest.py /path/to/batch --confidence 70

# Verbose logging
python ingest.py /path/to/batch -v
```

## Rerunning without duplicates

The pipeline identifies files by their SHA-256 content hash (`file_id` in the master CSV). Running it again on the same folder — or a folder containing already-processed files — skips them automatically:

```
$ python ingest.py same_folder --output output
[INFO] Master CSV has 42 existing records.
[INFO] 0 new files to process, 15 skipped (already in master CSV).
[INFO] Nothing new to process. Master CSV is up to date.
```

This means you can safely point the pipeline at a growing collection and only new files get processed.

## Output structure

```
output/
├── iconocracy_master.csv       # Master metadata (all runs accumulated)
├── quality_report.html         # Low-confidence page report
├── renamed/                    # Renamed file copies
│   ├── BND_1891_0001_constituicao-federal.pdf
│   ├── CAM_1934_0002_anais-assembleia.tiff
│   └── ...
├── ocr_texts/                  # Full OCR text per file
│   ├── BND_1891_0001_constituicao-federal.txt
│   └── ...
├── captions/                   # Extracted captions per file
│   ├── BND_1891_0001_constituicao-federal_captions.txt
│   └── ...
└── logs/                       # JSON run logs (audit trail)
    └── run_20260403_155454.json
```

## Master CSV columns

| Column | Description |
|---|---|
| `file_id` | SHA-256 hash (dedup key) |
| `original_filename` | Name as downloaded from source |
| `renamed_filename` | Standardized name after pipeline |
| `source_institution` | `BND`, `CAM`, `SEN`, `IA`, or `UNKNOWN` |
| `detected_language` | ISO 639-1 code (pt, es, fr, it, en, de, la) |
| `ocr_language_used` | Tesseract code passed to engine |
| `total_pages` | Number of pages (1 for images) |
| `mean_confidence` | Average OCR confidence 0–100 |
| `min_confidence` | Worst page confidence |
| `low_conf_pages` | Comma-separated page numbers below threshold |
| `caption_count` | Number of captions/figure refs extracted |
| `has_figures` | Whether any captions were found |
| `year_detected` | Year extracted from filename (1500–2030) |
| `ingestion_timestamp` | ISO 8601 UTC |
| `input_folder` | Path of the original batch folder |
| `notes` | Error messages or manual annotations |

## Source detection

The pipeline infers the source institution from folder names and file paths:

| Folder fragment | Source code |
|---|---|
| `bnd`, `bndigital`, `biblioteca nacional` | BND |
| `camara`, `deputados` | CAM |
| `senado` | SEN |
| `archive.org`, `internet archive`, `ia_` | IA |

To add a new source, edit `SOURCE_CODES` in `config.py`.

## Caption extraction

The pipeline detects multilingual figure labels and credits:

- **Figure labels**: `Figura`, `Fig.`, `Figure`, `Ilustração`, `Gravura`, `Estampa`, `Imagem`, `Fotografia`, `Prancha`, `Lâmina`, `Planche`, `Tavola`, `Lámina`, `Grabado`, `Illustration`
- **Credits**: `Fonte:`, `Source:`, `Fuente:`, `Acervo:`, `Crédito:`, `Collection:`, `Arquivo:`, `Archive:`
- **Media/technique**: parenthetical descriptions (óleo, gravura, litografia, fotografia, etc.)

## Quality report

The HTML report at `output/quality_report.html` shows:

- Run statistics (files, pages, issues, skipped)
- Summary table of files with low-confidence pages
- Per-file detail with page number, confidence badge, word count, and text preview
- Actionable guidance:
  - Below 40%: likely image-only or heavily degraded
  - 40–60%: partial success, consider re-scanning or manual correction
  - Systematic patterns point to source-level scan quality issues

## Configuration

All tuneable parameters are in `config.py`:

- `SOURCE_CODES` — folder-fragment → institution code mapping
- `LANG_MAP` — ISO 639-1 → Tesseract language code
- `CONFIDENCE_THRESHOLD` — below this goes into quality report (default 60)
- `MIN_TEXT_LENGTH` — minimum chars to consider a page "has text"
- `PDF_DPI` — resolution for PDF→image conversion (default 300)
- `TESSERACT_PSM` — page segmentation mode (default 6)
- `RENAME_PATTERN` — file naming template
- `MASTER_CSV_COLUMNS` — CSV schema (add columns here)

## Requirements

- Python 3.10+
- Tesseract 5.x with language packs: `por`, `spa`, `fra`, `ita`, `eng`, `deu`, `lat`
- poppler-utils (for PDF→image conversion via `pdftoppm`)
- See `requirements.txt` for Python packages

## Integration with iconocracy-corpus

This pipeline is designed to feed into the broader `iconocracy-corpus` monorepo:

- The master CSV can be imported into the PostgreSQL `image_objects` table
- OCR texts feed into full-text search / corpus analysis
- Captions map to the `motifs` and `interpretive_statements` tables
- Renamed files follow a convention compatible with the `image_id` field
- The quality report helps prioritize which scans need manual re-digitization
