#!/usr/bin/env python3
"""Deterministic guard for thesis terminology (populated 2026-09-22).

BLOCKED terms are always-wrong strings in the thesis pipeline (scanned
paths: tese/manuscrito, tese/artigos, vault/tese). A line containing the
marker `<!-- termos-ok -->` is exempt — use it ONLY on lines that state
or discuss the rule itself (e.g. the Glossário entry for endurecimento),
never on thesis prose. Files that are rule metadata, not prose, go in
ALLOWLIST.

Run before every commit: exit 1 = blocked term found.
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
PATHS = [
    REPO / "tese" / "manuscrito",
    REPO / "tese" / "artigos",
    REPO / "vault" / "tese",
]

BLOCKED: dict[str, str] = {
    "hardening": "use 'endurecimento' (o termo é sempre em português; "
                 "regra do METHOD_CONTRACT e do Glossário §Endurecimento)",
    "embrutecimento": "use 'endurecimento' (nunca 'embrutecimento')",
    "canone eloquente": "o título correto é 'Il canone eclettico' "
                        "(LACCHÈ, Quaderni fiorentini, v. 39, 2010, p. 459-486)",
}

ALLOWLIST = {
    REPO / "docs" / "METHOD_CONTRACT_2026-04-23.md",
    # rule-metadata file, not prose: states the terminology rule itself
    REPO / "vault" / "tese" / "rascunhos-artigos" / "genealogia-alegoria-feminina.json",
}

LINE_EXEMPT_MARKER = "<!-- termos-ok"


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
        if not any(term.lower() in lowered for term in BLOCKED):
            continue  # fast path: skip per-line scan when no term present
        for lineno, line in enumerate(text.splitlines(), start=1):
            if LINE_EXEMPT_MARKER in line:
                continue
            lowered_line = line.lower()
            for term, replacement in BLOCKED.items():
                needle = term.lower()
                if needle in lowered_line:
                    failures.append(
                        f"{path.relative_to(REPO)}:{lineno} contains {term!r}: {replacement}"
                    )

    if failures:
        print("Blocked thesis terms found:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("thesis terms ok")


if __name__ == "__main__":
    main()