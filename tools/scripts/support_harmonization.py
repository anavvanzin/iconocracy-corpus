"""Canonical support harmonization gate used before image sampling."""

from __future__ import annotations

import unicodedata
from collections import Counter
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config" / "support_harmonization.yaml"


class SupportHarmonizationError(ValueError):
    """Raised when a candidate cannot pass the pre-selection support gate."""


def _normalize(value: object) -> str:
    return unicodedata.normalize("NFKC", str(value)).strip().casefold()


def _normalize_marker(marker: object) -> str:
    # Sem strip(): os marcadores " e " e " and " dependem dos espaços para casar só
    # entre palavras. Passados por _normalize() viravam "e" e "and", e o gate rejeitava
    # como composto todo suporte que contivesse a letra — moeda, selo, escultura.
    return unicodedata.normalize("NFKC", str(marker)).casefold()


def load_protocol(path: Path = DEFAULT_CONFIG) -> dict:
    with open(path, encoding="utf-8") as stream:
        document = yaml.safe_load(stream)
    protocol = document.get("support_harmonization", {})
    if protocol.get("apply_before") != "image_selection":
        raise SupportHarmonizationError(
            "support_harmonization.apply_before must be image_selection"
        )
    return protocol


def harmonize_support(support_raw: object, support_source: str, protocol: dict | None = None) -> dict:
    protocol = protocol or load_protocol()
    if not support_source:
        raise SupportHarmonizationError("support_source is required")

    normalized = _normalize(support_raw)
    adjudication = protocol["adjudication"]
    forbidden = {_normalize(value) for value in adjudication["forbidden_values"]}
    if normalized in forbidden:
        raise SupportHarmonizationError(f"forbidden support value: {support_raw!r}")
    # Espaço nas duas pontas para que " e " case também no início e no fim do valor.
    padded = f" {normalized} "
    for marker in adjudication["reject_composite_if_contains"]:
        if _normalize_marker(marker) in padded:
            raise SupportHarmonizationError(f"composite support requires adjudication: {support_raw!r}")

    mappings = {
        _normalize(raw): stratum
        for raw, stratum in protocol["raw_to_stratum"]["mappings"].items()
    }
    support_stratum = mappings.get(normalized)
    if support_stratum is None:
        raise SupportHarmonizationError(f"unmapped support requires adjudication: {support_raw!r}")
    support_family = protocol["stratum_to_family"]["mappings"].get(support_stratum)
    if support_family is None:
        raise SupportHarmonizationError(f"stratum without family: {support_stratum!r}")
    return {
        "support_raw": support_raw,
        "support_source": support_source,
        "support_stratum": support_stratum,
        "support_family": support_family,
        "support_harmonization_version": protocol["version"],
    }


def harmonize_candidates(candidates: list[dict], *, raw_key: str = "support", source_key: str = "support_source") -> list[dict]:
    """Enrich every candidate or fail the complete batch before sampling."""
    protocol = load_protocol()
    rejected = []
    enriched = []
    for candidate in candidates:
        try:
            support = harmonize_support(candidate.get(raw_key), candidate.get(source_key, ""), protocol)
        except SupportHarmonizationError as exc:
            rejected.append(f"{candidate.get('item_id') or candidate.get('id')}: {exc}")
            continue
        enriched.append({**candidate, **support})

    if rejected and protocol["frequency_reports"].get("fail_if_rejected_rows_exist", True):
        details = "\n  - ".join(rejected)
        raise SupportHarmonizationError(
            f"support harmonization rejected {len(rejected)} candidate(s) before selection:\n  - {details}"
        )
    return enriched


def frequency_counts(candidates: list[dict]) -> dict[str, dict[str, int]]:
    """Return the protocol's auditable pre-selection frequency views."""
    protocol = load_protocol()
    strata = protocol["stratum_to_family"]["mappings"]
    families = set(strata.values())
    raw = Counter(str(item["support_raw"]) for item in candidates)
    by_stratum = Counter(item["support_stratum"] for item in candidates)
    by_family = Counter(item["support_family"] for item in candidates)
    return {
        "support_raw": dict(sorted(raw.items())),
        "support_stratum": {key: by_stratum.get(key, 0) for key in strata},
        "support_family": {key: by_family.get(key, 0) for key in sorted(families)},
    }
