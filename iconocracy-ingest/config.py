"""
Pipeline configuration — all tuneable parameters in one place.
Adjust thresholds, naming conventions, and source mappings here.
"""

from pathlib import Path

# ── Source institution mappings ──────────────────────────────────────────────
# Maps folder-name fragments (case-insensitive) → canonical institution codes.
# Add new sources here; the pipeline picks them up automatically.
SOURCE_CODES = {
    "bnd": "BND",           # Biblioteca Nacional Digital
    "bndigital": "BND",
    "biblioteca nacional": "BND",
    "camara": "CAM",        # Câmara dos Deputados
    "deputados": "CAM",
    "senado": "SEN",        # Senado Federal
    "archive.org": "IA",    # Internet Archive
    "internet archive": "IA",
    "ia_": "IA",
}

# ── Supported languages ─────────────────────────────────────────────────────
# ISO 639-1 → Tesseract language code
LANG_MAP = {
    "pt": "por",
    "es": "spa",
    "fr": "fra",
    "it": "ita",
    "en": "eng",   # fallback
    "de": "deu",   # occasional German legal texts
    "la": "lat",   # Latin inscriptions
}

# Languages to attempt detection on (langdetect codes)
TARGET_LANGS = {"pt", "es", "fr", "it", "en", "de", "la"}

# ── OCR settings ────────────────────────────────────────────────────────────
# Tesseract Page Segmentation Mode:
#   6 = assume a single uniform block of text (good for scanned pages)
#   3 = fully automatic (default)
TESSERACT_PSM = 6

# Confidence threshold (0-100). Pages below this go into the quality report.
CONFIDENCE_THRESHOLD = 60

# Minimum text length (chars) to consider a page "has text"
MIN_TEXT_LENGTH = 30

# ── File handling ────────────────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = {".pdf", ".tif", ".tiff", ".png", ".jpg", ".jpeg", ".jp2"}

# DPI for PDF → image conversion
PDF_DPI = 300

# ── Naming convention ────────────────────────────────────────────────────────
# Pattern: {source}_{year}_{seq:04d}_{orig_stem}.{ext}
# Example: BND_1891_0001_constituicao-federal.pdf
RENAME_PATTERN = "{source}_{year}_{seq:04d}_{stem}.{ext}"

# ── CSV master file ──────────────────────────────────────────────────────────
MASTER_CSV_COLUMNS = [
    "file_id",              # unique identifier (sha256 of original file)
    "original_filename",    # as downloaded
    "renamed_filename",     # after pipeline renaming
    "source_institution",   # BND | CAM | SEN | IA | UNKNOWN
    "detected_language",    # ISO 639-1
    "ocr_language_used",    # Tesseract code actually passed
    "total_pages",
    "mean_confidence",      # average OCR confidence across pages (0-100)
    "min_confidence",       # worst page confidence
    "low_conf_pages",       # comma-separated list of page numbers below threshold
    "caption_count",        # number of captions/figure mentions extracted
    "has_figures",          # True / False
    "year_detected",        # year extracted from filename or metadata
    "ingestion_timestamp",  # ISO 8601
    "input_folder",         # relative path of the batch folder
    "notes",                # free-text field for manual annotation
]

# ── Output paths (relative to run directory) ─────────────────────────────────
DEFAULT_OUTPUT_DIR = Path("output")
MASTER_CSV_NAME = "iconocracy_master.csv"
QUALITY_REPORT_NAME = "quality_report.html"
OCR_TEXT_DIR = "ocr_texts"          # plain-text OCR output per file
CAPTIONS_DIR = "captions"           # extracted captions per file
RENAMED_DIR = "renamed"             # renamed copies (optional; can rename in-place)
