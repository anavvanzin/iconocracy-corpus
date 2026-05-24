from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin, urlparse


URL_PATTERN = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
IMAGE_EXT_PATTERN = re.compile(r"\.(?:jpe?g|png|tif{1,2}|webp)(?:$|[?#])", re.IGNORECASE)
MANIFEST_PATTERN = re.compile(r"/(?:presentation/)?[^\s\"']*manifest(?:\.json)?(?:$|[?#])", re.IGNORECASE)
IIIF_IMAGE_PATTERN = re.compile(r"/iiif(?:/\d+)?/.+/full/.+/\d+/(?:default|native)\.(?:jpe?g|png|webp|tif{1,2})", re.IGNORECASE)
INFO_JSON_PATTERN = re.compile(r"/iiif(?:/\d+)?/.+/info\.json(?:$|[?#])", re.IGNORECASE)
RESOLUTION_PATTERN = re.compile(r"(?:(\d{3,5})\s*[xX]\s*(\d{3,5})|(\d{3,5})w)")
DOWNLOAD_WORDS = ("download", "full", "original", "hires", "highres", "master")
IMAGE_WORDS = ("image", "jpg", "jpeg", "png", "tif", "tiff", "webp")
CDN_WORDS = ("cdn", "media", "images", "img", "static", "downloads")


class _LandingPageParser(HTMLParser):
    def __init__(self, page_url: str):
        super().__init__(convert_charrefs=True)
        self.page_url = page_url
        self.page_host = (urlparse(page_url).hostname or "").lower()
        self.page_domain = _base_domain(self.page_host)
        self.page_title = ""
        self._in_title = False
        self._title_parts: list[str] = []
        self.candidates: list[dict[str, Any]] = []
        self.iiif_manifest_candidates: list[str] = []
        self.api_candidates: list[str] = []
        self.notes: list[str] = []
        self._seen_candidate_urls: dict[str, dict[str, Any]] = {}
        self._seen_manifest_urls: set[str] = set()
        self._seen_api_urls: set[str] = set()
        self._capture_script = False
        self._script_parts: list[str] = []
        self._anchor_stack: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key.lower(): value for key, value in attrs if value is not None}
        tag = tag.lower()

        if tag == "title":
            self._in_title = True
            return

        if tag == "meta":
            key = (attrs_dict.get("property") or attrs_dict.get("name") or "").strip().lower()
            content = attrs_dict.get("content")
            if key == "og:image" and content:
                self._add_candidate(content, "image", "meta:og:image")
            elif key == "twitter:image" and content:
                self._add_candidate(content, "image", "meta:twitter:image")
            return

        if tag == "link":
            rel = (attrs_dict.get("rel") or "").lower()
            href = attrs_dict.get("href")
            if href and "image_src" in rel:
                self._add_candidate(href, "image", "link:image_src")
            return

        if tag == "img":
            for attr_name in ("src", "data-src", "data-original"):
                value = attrs_dict.get(attr_name)
                if value:
                    self._add_candidate(value, "image", f"img:{attr_name}")
            return

        if tag == "source":
            srcset = attrs_dict.get("srcset")
            if srcset:
                for candidate_url, descriptor in _parse_srcset(srcset):
                    self._add_candidate(candidate_url, "image", "source:srcset", descriptor=descriptor)
            return

        if tag == "a":
            href = attrs_dict.get("href")
            if not href:
                return
            self._anchor_stack.append(
                {
                    "href": href,
                    "attr_text": " ".join(
                        part for part in (attrs_dict.get("download"), attrs_dict.get("title"), attrs_dict.get("aria-label")) if part
                    ),
                    "text_parts": [],
                }
            )
            return

        if tag == "script":
            script_type = (attrs_dict.get("type") or "").lower()
            if script_type in {"application/ld+json", "application/json", "text/json", ""}:
                self._capture_script = True
                self._script_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
            self.page_title = " ".join(part.strip() for part in self._title_parts if part.strip())
            self._title_parts = []
            return
        if tag == "a" and self._anchor_stack:
            anchor = self._anchor_stack.pop()
            anchor_text = " ".join(part.strip() for part in anchor["text_parts"] if part.strip())
            context = " ".join(part for part in (anchor_text, anchor["attr_text"]) if part)
            lowered = f"{anchor['href']} {context}".lower()
            if any(word in lowered for word in DOWNLOAD_WORDS):
                self._add_candidate(anchor["href"], "download", "a:download", context=context)
            elif IMAGE_EXT_PATTERN.search(anchor["href"]) and any(word in lowered for word in IMAGE_WORDS):
                self._add_candidate(anchor["href"], "image", "a:image", context=context)
            return
        if tag == "script" and self._capture_script:
            self._capture_script = False
            script_text = "".join(self._script_parts)
            self._extract_urls_from_text(script_text, "json")
            self._script_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)
        if self._capture_script:
            self._script_parts.append(data)
        if self._anchor_stack:
            self._anchor_stack[-1]["text_parts"].append(data)

    def close(self) -> None:
        super().close()
        self.candidates.sort(key=lambda item: (-item["score"], item["url"], item["source_hint"]))
        self.iiif_manifest_candidates.sort()
        self.api_candidates.sort()

    def _add_candidate(
        self,
        raw_url: str,
        kind: str,
        source_hint: str,
        descriptor: str | None = None,
        context: str | None = None,
    ) -> None:
        normalized_url = _normalize_url(raw_url, self.page_url)
        if not normalized_url:
            return

        classified_kind = _classify_candidate_kind(normalized_url, default_kind=kind)
        if classified_kind == "iiif_manifest":
            if normalized_url not in self._seen_manifest_urls:
                self._seen_manifest_urls.add(normalized_url)
                self.iiif_manifest_candidates.append(normalized_url)
            return
        if classified_kind == "api":
            if normalized_url not in self._seen_api_urls:
                self._seen_api_urls.add(normalized_url)
                self.api_candidates.append(normalized_url)
            return

        score = _score_candidate(
            normalized_url,
            classified_kind,
            source_hint,
            self.page_host,
            self.page_domain,
            descriptor=descriptor,
            context=context,
        )
        candidate = {
            "url": normalized_url,
            "kind": classified_kind,
            "score": score,
            "source_hint": source_hint,
        }
        existing = self._seen_candidate_urls.get(normalized_url)
        if existing is None or candidate["score"] > existing["score"]:
            self._seen_candidate_urls[normalized_url] = candidate
            if existing is None:
                self.candidates.append(candidate)
            else:
                existing.update(candidate)

    def _extract_urls_from_text(self, text: str, source_hint: str) -> None:
        for matched in URL_PATTERN.findall(text or ""):
            cleaned = matched.rstrip(".,;)]}\"")
            kind = _classify_candidate_kind(cleaned, default_kind="image")
            if kind == "iiif_manifest":
                self._add_candidate(cleaned, kind, f"{source_hint}:manifest")
            elif kind == "api":
                self._add_candidate(cleaned, kind, f"{source_hint}:api")
            elif kind in {"iiif_image", "image"}:
                self._add_candidate(cleaned, kind, f"{source_hint}:url")


def extract_landing_page_candidates(html_text: str, page_url: str) -> dict[str, Any]:
    parser = _LandingPageParser(page_url)
    parser.feed(html_text or "")
    parser.close()
    return {
        "page_url": page_url,
        "content_type": "text/html",
        "page_title": html.unescape(parser.page_title.strip()),
        "candidates": parser.candidates,
        "iiif_manifest_candidates": parser.iiif_manifest_candidates,
        "api_candidates": parser.api_candidates,
        "notes": parser.notes,
    }


def _normalize_url(raw_url: str, page_url: str) -> str | None:
    value = (raw_url or "").strip()
    if not value or value.startswith(("data:", "javascript:", "mailto:")):
        return None
    return urljoin(page_url, html.unescape(value))


def _classify_candidate_kind(url: str, default_kind: str) -> str:
    lowered = url.lower()
    if MANIFEST_PATTERN.search(lowered):
        return "iiif_manifest"
    if INFO_JSON_PATTERN.search(lowered):
        return "api"
    if IIIF_IMAGE_PATTERN.search(lowered):
        return "iiif_image"
    return default_kind


def _score_candidate(
    url: str,
    kind: str,
    source_hint: str,
    page_host: str,
    page_domain: str,
    descriptor: str | None = None,
    context: str | None = None,
) -> int:
    lowered = url.lower()
    score = {
        "iiif_image": 160,
        "download": 120,
        "image": 80,
    }.get(kind, 50)

    if source_hint.startswith("meta:"):
        score += 24
    elif source_hint == "link:image_src":
        score += 18
    elif source_hint == "source:srcset":
        score += 16
    elif source_hint.startswith("json"):
        score += 18
    elif source_hint.startswith("img:"):
        score += 10
    elif source_hint.startswith("a:"):
        score += 12

    if any(word in lowered for word in DOWNLOAD_WORDS):
        score += 30

    if kind == "download" and IMAGE_EXT_PATTERN.search(lowered):
        score += 12

    if lowered.endswith((".tif", ".tiff")) or ".tif?" in lowered or ".tiff?" in lowered:
        score += 18
    elif lowered.endswith((".png", ".webp")) or ".png?" in lowered or ".webp?" in lowered:
        score += 12
    elif ".jpg" in lowered or ".jpeg" in lowered:
        score += 10

    score += _resolution_bonus(descriptor or url)

    host = (urlparse(url).hostname or "").lower()
    domain = _base_domain(host)
    if host and host == page_host:
        score += 20
    elif domain and page_domain and domain == page_domain:
        score += 12
    elif any(word in host for word in CDN_WORDS) and page_domain and page_domain.split(".")[0] in host:
        score += 8

    if context and any(word in context.lower() for word in DOWNLOAD_WORDS):
        score += 10

    return score


def _resolution_bonus(value: str) -> int:
    bonus = 0
    for match in RESOLUTION_PATTERN.finditer(value.lower()):
        width = height = span_width = 0
        if match.group(1) and match.group(2):
            width = int(match.group(1))
            height = int(match.group(2))
            span_width = min(width, height)
        elif match.group(3):
            width = int(match.group(3))
            span_width = width
        if span_width:
            bonus = max(bonus, min(span_width // 100, 40))
    return bonus


def _base_domain(host: str) -> str:
    parts = [part for part in (host or "").split(".") if part]
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return host or ""


def _parse_srcset(srcset: str) -> list[tuple[str, str | None]]:
    entries: list[tuple[str, str | None]] = []
    for part in srcset.split(","):
        chunk = part.strip()
        if not chunk:
            continue
        segments = chunk.split()
        url = segments[0]
        descriptor = segments[1] if len(segments) > 1 else None
        entries.append((url, descriptor))
    return entries
