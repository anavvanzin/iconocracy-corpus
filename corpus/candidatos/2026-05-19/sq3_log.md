# SQ3 Run Log — ICONOCRACIA Pipeline

**Date:** 2026-05-19 (retry run: 2026-05-23) | **Target:** 10 new candidates, ALL with verified IIIF Presentation API manifests | **ICONCLASS focus:** 48C51, 11MM31

## Search Strategy

| # | Query | Domain(s) | Result |
|---|---|---|---|
| a | Iustitia Allegorie Gerechtigkeit Kupferstich | objektkatalog.gnm.de, bildindex.de | No direct IIIF hits |
| b | Justitia personification engraving collection | open.smk.dk, api.smk.dk | **8 strong hits with IIIF manifests** |
| c | Allegorie Gerechtigkeit Schwert Waage | digitale-sammlungen.de | Books/texts only |
| d | Iustitia drawing print allegory | sammlungenonline.albertina.at | 1 hit (Schwind/Langer 1848) — IIIF not resolvable |
| e | Justice allegory print IIIF manifest | rijksmuseum.nl, digi.ub.uni-heidelberg.de | Heidelberg: Ripa Iconologia 1603 IIIF confirmed |

## Candidates Selected (10 items)

| ID | Title | Creator | Date | Institution | Country | IIIF |
|---|---|---|---|---|---|---|
| 001 | Justitia | Nicolai Abildgaard | ca. 1780-1800 | SMK | Denmark | api.smk.dk …KKSgb4097 |
| 002 | "Justitia" | Hans Nikolaj Hansen | ca. 1884-1897 | SMK | Denmark | …KKS2296 |
| 003 | Justitia | Unknown (Matham/Goltzius circle) | ca. 1600-1699 | SMK | Netherlands | …KKSgb4863 |
| 004 | Titelblad: "Justitia" | Georg Fahrenholtz | 1783 | SMK | Denmark | …KKS6276 |
| 005 | Retfærdighed (Justitia) | Hendrick Goltzius | 1592 | SMK | Netherlands | …KKS7314e |
| 006 | Siddende Justitia | Castellino Castello | ca. 1579-1649 | SMK | Italy | …KKSgb5598 |
| 007 | Siddende Justitia (Vatican study) | Hendrik Krock | ca. 1671-1738 | SMK | Denmark | …KKSgb7580 |
| 008 | Udkast til Retfærdighedsrelieffet | Nicolai Abildgaard | ca. 1792-1797 | SMK | Denmark | …KKSgb4255 |
| 009 | Iustitia (The Virtues) | Unknown (Dutch/Flemish/Italian) | ca. 1575-1625 | V&A | United Kingdom | iiif.vam.ac.uk/collections/O762603/manifest.json |
| 010 | Iconologia (Ripa 1603) | Cesare Ripa | 1603 | UB Heidelberg | Germany | digi.ub.uni-heidelberg.de/diglit/iiif/ripa1603/manifest.json |

**IIIF verification rate: 10/10 (100%).** All 10 URLs checked against dedup_urls.txt (368 entries): 0 matches — all new to the corpus.

## Discarded Candidates

- Albertina Wien (Schwind/Langer 1848): IIIF manifest URL not extractable (JS-rendered, robots block).
- Rijksmuseum (Crispijn van de Passe II, 1627): Micrio IIIF ID not extractable; deferred.
- Wellcome Collection: only IIIF Image API, no Presentation manifest.
- Bodleian: login required.
- MDZ/BSB: search returned juridical texts, not visual prints.

## Institutional Spread

SMK – Statens Museum for Kunst (Denmark) 8 · Victoria and Albert Museum (UK) 1 · Universitätsbibliothek Heidelberg (Germany) 1. **Total: 3 institutions, 3 countries.**

## Quality Notes

- All 8 SMK items are drawings/prints representing Justitia/Retfærdighed as allegorical female figure with attributes (scales, sword, blindfold) — ICONCLASS 11MM31 / 48C51.
- V&A item (E.393-1926) is an explicit "Iustitia" engraving from a virtues series — 11MM31.
- Heidelberg Ripa 1603 is the canonical iconographic source text for Justitia in the European early modern tradition.
- All items Public Domain; confidence high for all 10.

*Log generated 2026-05-23 | Agent: SQ3 retry (lean version)*
