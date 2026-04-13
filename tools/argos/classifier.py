"""Domain → protocol classification.

Each corpus source URL belongs to a known archive domain. The
classifier maps the domain to the most appropriate acquisition
protocol. The subagent playbook escalates through fallback protocols
on failure, but the initial dispatch uses this mapping.
"""

from __future__ import annotations

from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Protocol taxonomy
# ---------------------------------------------------------------------------
#   iiif                  — presentation API or image API endpoint discoverable
#   rest-api              — structured REST endpoint returns image URL
#   direct                — single HTTP GET to image URL
#   playwright-required   — JS-heavy page; needs headless browser
#   blocked-prone         — historically returns 403/Cloudflare without headers
#   unknown               — no prior classification; HEAD-probe first

PROTOCOL_MAP: dict[str, str] = {
    # IIIF-first archives
    "gallica.bnf.fr": "iiif",
    "www.loc.gov": "iiif",
    "loc.gov": "iiif",
    "tile.loc.gov": "iiif",
    "www.rijksmuseum.nl": "iiif",
    "rijksmuseum.nl": "iiif",
    "bndigital.bnportugal.gov.pt": "iiif",
    "brasilianafotografica.bn.gov.br": "iiif",
    "www.europeana.eu": "iiif",
    "europeana.eu": "iiif",
    "api.europeana.eu": "iiif",
    "www.metmuseum.org": "iiif",
    "metmuseum.org": "iiif",
    "collectionapi.metmuseum.org": "rest-api",
    # REST-API archives
    "www.bildindex.de": "rest-api",
    "bildindex.de": "rest-api",
    "www.iwm.org.uk": "rest-api",
    "iwm.org.uk": "rest-api",
    "collections.vam.ac.uk": "rest-api",
    "api.vam.ac.uk": "rest-api",
    # Direct HTTP
    "en.wikipedia.org": "direct",
    "commons.wikimedia.org": "direct",
    "upload.wikimedia.org": "direct",
    "memoria.bn.br": "direct",
    # Playwright-required (JS catalogs, Cloudflare-fronted)
    "colnect.com": "playwright-required",
    "www.colnect.com": "playwright-required",
    "en.numista.com": "playwright-required",
    "numista.com": "playwright-required",
    # Blocked-prone (frequent 403 without careful headers)
    "www.britishmuseum.org": "blocked-prone",
    "britishmuseum.org": "blocked-prone",
    # German historical archive
    "germanhistorydocs.ghi-dc.org": "direct",
}

# Domains where Terms of Service discourage bulk scraping.
# Items on these domains are marked `tos_restricted` unless an
# explicit --allow-tos flag is passed.
TOS_RESTRICTED: set[str] = {
    "colnect.com",
    "www.colnect.com",
    "en.numista.com",
    "numista.com",
}


def domain_for(url: str) -> str:
    """Return the lower-case host component for ``url`` (empty on failure)."""

    if not url:
        return ""
    try:
        return (urlparse(url).hostname or "").lower()
    except (ValueError, AttributeError):
        return ""


def classify(url: str) -> str:
    """Return the protocol bucket for ``url``.

    Unknown domains default to ``unknown``; the acquisition worker will
    HEAD-probe and fall back through direct → IIIF discovery → Playwright.
    """

    host = domain_for(url)
    if not host:
        return "unknown"
    if host in PROTOCOL_MAP:
        return PROTOCOL_MAP[host]
    # Wildcard match for loc.gov subdomains
    for known, protocol in PROTOCOL_MAP.items():
        if host.endswith("." + known) or host == known:
            return protocol
    return "unknown"


def is_tos_restricted(url: str) -> bool:
    """True if the host is flagged for TOS concerns."""

    host = domain_for(url)
    return host in TOS_RESTRICTED or any(
        host == known or host.endswith("." + known) for known in TOS_RESTRICTED
    )
