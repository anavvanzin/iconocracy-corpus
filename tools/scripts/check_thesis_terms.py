#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
PATHS = [
    REPO / "tese" / "manuscrito",
    REPO / "tese" / "artigos",
    REPO / "vault" / "tese",
]
BLOCKED = {
    "hardening": "use endurecimento",
    "0–4": "use 0–3",
    "0-4": "use 0-3",
    "0.0–4.0": "use 0.0–3.0",
    "0,0–4,0": "use 0,0–3,0",
    "ciberfeminismo": "remove from thesis text",
}

ALLOWLIST = {
    REPO / "docs" / "METHOD_CONTRACT_2026-04-23.md",
}


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for root in PATHS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.suffix.lower() in {".md", ".txt", ".json", ".bib"} and path not in ALLOWLIST:
                files.append(path)
    return sorted(files)


def main() -> None:
    failures: list[str] = []
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        lowered = text.lower()
        for term, replacement in BLOCKED.items():
            needle = term.lower()
            if needle in lowered:
                failures.append(f"{path.relative_to(REPO)} contains {term!r}: {replacement}")

    if failures:
        print("Blocked thesis terms found:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("thesis terms ok")


if __name__ == "__main__":
    main()
