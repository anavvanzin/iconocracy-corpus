"""
OCR engine: language detection, Tesseract OCR with confidence scoring.
Handles PDFs (multi-page) and single images.
"""

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pytesseract
from langdetect import detect_langs, LangDetectException
from pdf2image import convert_from_path
from PIL import Image

import config

logger = logging.getLogger(__name__)


@dataclass
class PageResult:
    """OCR result for a single page."""
    page_number: int
    text: str
    confidence: float          # mean word confidence 0-100
    detected_language: str     # ISO 639-1
    word_count: int
    is_low_confidence: bool


@dataclass
class FileOCRResult:
    """Aggregated OCR result for an entire file."""
    filepath: Path
    total_pages: int
    pages: list[PageResult] = field(default_factory=list)
    detected_language: str = ""
    ocr_language_used: str = ""
    mean_confidence: float = 0.0
    min_confidence: float = 0.0
    low_conf_pages: list[int] = field(default_factory=list)
    full_text: str = ""
    error: Optional[str] = None


def _detect_language(text: str) -> str:
    """
    Detect language from text sample.
    Returns ISO 639-1 code or 'und' (undetermined).
    Filters to only target languages.
    """
    if len(text.strip()) < config.MIN_TEXT_LENGTH:
        return "und"
    try:
        results = detect_langs(text[:5000])  # use first 5000 chars for speed
        for r in results:
            if r.lang in config.TARGET_LANGS:
                return r.lang
        # If no target language detected, return the top result anyway
        return results[0].lang if results else "und"
    except LangDetectException:
        return "und"


def _get_tesseract_lang(iso_code: str) -> str:
    """Map ISO 639-1 to Tesseract language code. Falls back to por+eng."""
    return config.LANG_MAP.get(iso_code, "por+eng")


def _preprocess_image(img: Image.Image) -> Image.Image:
    """
    Basic preprocessing for better OCR:
    - Convert to grayscale
    - Resize if very small
    """
    # Convert to grayscale
    if img.mode != "L":
        img = img.convert("L")

    # If image is very small, upscale 2x
    w, h = img.size
    if w < 800 or h < 800:
        img = img.resize((w * 2, h * 2), Image.LANCZOS)

    return img


def _ocr_single_image(
    img: Image.Image,
    page_number: int,
    lang_hint: Optional[str] = None,
) -> PageResult:
    """
    Run Tesseract on a single image. Returns PageResult with text + confidence.
    """
    processed = _preprocess_image(img)

    # First pass: quick OCR to detect language if no hint
    if lang_hint is None:
        quick_text = pytesseract.image_to_string(
            processed,
            lang="por+spa+fra+ita+eng",
            config=f"--psm {TESSERACT_PSM}",
        )
        detected_lang = _detect_language(quick_text)
        tess_lang = _get_tesseract_lang(detected_lang)
    else:
        detected_lang = lang_hint
        tess_lang = _get_tesseract_lang(lang_hint)

    # Main OCR pass with detected language
    data = pytesseract.image_to_data(
        processed,
        lang=tess_lang,
        config=f"--psm {TESSERACT_PSM}",
        output_type=pytesseract.Output.DICT,
    )

    # Extract text and compute mean confidence
    words = []
    confidences = []
    for i, conf_str in enumerate(data["conf"]):
        conf = float(conf_str)
        word = data["text"][i].strip()
        if conf > 0 and word:  # conf == -1 means no text detected
            words.append(word)
            confidences.append(conf)

    text = " ".join(words)
    mean_conf = sum(confidences) / len(confidences) if confidences else 0.0
    is_low = mean_conf < CONFIDENCE_THRESHOLD

    return PageResult(
        page_number=page_number,
        text=text,
        confidence=round(mean_conf, 1),
        detected_language=detected_lang,
        word_count=len(words),
        is_low_confidence=is_low,
    )


def ocr_file(filepath: Path) -> FileOCRResult:
    """
    Run OCR on a file (PDF or image). Returns FileOCRResult.
    For PDFs, processes each page individually.
    For images, treats as single page.
    """
    result = FileOCRResult(filepath=filepath, total_pages=0)

    try:
        ext = filepath.suffix.lower()

        if ext == ".pdf":
            images = convert_from_path(str(filepath), dpi=PDF_DPI)
        elif ext in {".tif", ".tiff", ".png", ".jpg", ".jpeg", ".jp2"}:
            images = [Image.open(filepath)]
        else:
            result.error = f"Unsupported format: {ext}"
            return result

        result.total_pages = len(images)
        lang_hint = None  # Will be set after first page

        for i, img in enumerate(images, start=1):
            page = _ocr_single_image(img, page_number=i, lang_hint=lang_hint)
            result.pages.append(page)

            # After first page, lock language for remaining pages
            if i == 1 and page.detected_language != "und":
                lang_hint = page.detected_language

        # Aggregate results
        if result.pages:
            confs = [p.confidence for p in result.pages]
            result.mean_confidence = round(sum(confs) / len(confs), 1)
            result.min_confidence = round(min(confs), 1)
            result.low_conf_pages = [
                p.page_number for p in result.pages if p.is_low_confidence
            ]
            # Use the most common detected language
            lang_counts: dict[str, int] = {}
            for p in result.pages:
                lang_counts[p.detected_language] = (
                    lang_counts.get(p.detected_language, 0) + 1
                )
            result.detected_language = max(lang_counts, key=lang_counts.get)
            result.ocr_language_used = _get_tesseract_lang(result.detected_language)
            result.full_text = "\n\n--- PAGE BREAK ---\n\n".join(
                p.text for p in result.pages
            )

    except Exception as e:
        logger.error("OCR failed for %s: %s", filepath, e)
        result.error = str(e)

    return result
