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
class SourceClass:
    domain: str
    protocol: str


def classify_source(url: str) -> SourceClass:
    domain = urlparse(url).netloc.lower()
    protocol = PROTOCOL_MAP.get(domain, "unknown")
    return SourceClass(domain=domain, protocol=protocol)
