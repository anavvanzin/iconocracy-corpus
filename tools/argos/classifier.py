from dataclasses import dataclass
from urllib.parse import urlparse


PROTOCOL_MAP = {
    "gallica.bnf.fr": "iiif",
    "loc.gov": "iiif",
    "www.loc.gov": "iiif",
    "rijksmuseum.nl": "iiif",
    "www.europeana.eu": "iiif",
    "europeana.eu": "iiif",
    "commons.wikimedia.org": "direct",
    "en.wikipedia.org": "direct",
    "bildindex.de": "direct",
    "www.iwm.org.uk": "direct",
    "collections.vam.ac.uk": "direct",
    "numista.com": "playwright-required",
    "en.numista.com": "playwright-required",
    "colnect.com": "playwright-required",
    "www.britishmuseum.org": "blocked",
    "britishmuseum.org": "blocked",
}


@dataclass(frozen=True)
class SourceClassification:
    """Normalized domain and protocol selected for a source URL.

    Contract:
    - `domain` is lowercased and has any explicit port removed.
    - `protocol` is one of the known protocol labels in `PROTOCOL_MAP`, or
      `"unknown"` when the domain is not mapped yet.
    - Unknown results are intentional and let callers decide whether to add a
      new mapping, fall back to generic handling, or skip the source.
    """

    domain: str
    protocol: str


def _normalize_domain(url: str) -> str:
    """Extract a normalized host from URL-like input.

    Bare host/path inputs such as `LOC.GOV/photos/item` are treated as URL-like
    by reparsing them with a leading `//`, which allows `urlparse` to populate
    the network location consistently.
    """

    parsed = urlparse(url)
    if not parsed.netloc and parsed.path:
        parsed = urlparse(f"//{url}")

    return parsed.netloc.lower().split(":", 1)[0]


def classify_source(url: str) -> SourceClassification:
    """Classify a source by normalized domain.

    Unmapped domains are returned with the `unknown` protocol instead of
    raising, keeping classification total for all inputs.
    """

    domain = _normalize_domain(url)
    protocol = PROTOCOL_MAP.get(domain, "unknown")
    return SourceClassification(domain=domain, protocol=protocol)
