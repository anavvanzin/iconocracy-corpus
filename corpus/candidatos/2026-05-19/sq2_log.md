# ICONOCRACIA SQ2 — Search Log

**Date:** 2026-05-19 | **Agent:** SQ2 | **Goal:** 12–15 new iconography candidates, legal/republican allegory, Latin America 1850–1950

## Dedup Check Summary

- Dedup file read: 368 URLs
- Notable exclusions: Google Arts coleção Lopes Rodrigues (indexed); Museu da República alegorias PDF (indexed); eliseuvisconti.com.br/obra/d702 (indexed). Other Visconti pages (a803, p332) are new.

## Searches Conducted

- **Search 1** — `pinacoteca.org.br, mnba.gov.br, ihgb.org.br` ("alegoria República Justiça Pedro Américo Victor Meirelles"): low yield; IHGB results were archival documents, not visual works.
- **Search 2** — `memoria.bn.br, senado.leg.br` ("frontispício código penal Brasil século XIX"): Código Criminal do Império 1830 (id 221763) and 1876 (id 227311) → candidates 007, 008.
- **Search 3** — BNA Argentina (`catalogo.bn.gov.ar, trapalanda.bn.gov.ar`): 0 hits.
- **Search 4** — UNAM/HNDM Mexico: HNDM downloads return binary/corrupt content; no clean image candidates.
- **Search 5** — Memoria Chilena: Código Penal chileno 1874 (article-10118) → candidate 011 (no associated visual imagery confirmed).
- **Search 6** — `portinari.org.br, acervos.ims.com.br`: A Justiça de Salomão (FCO-2742) → 006; Ciclos Econômicos → 010.
- **Search 7** — Pedro Américo: low yield for new canonical URLs.
- **Search 8** — broad: academic papers surfaced Manoel Lopes Rodrigues "A República" (1896) → 003; Pedro Bruno "Pátria" (1919) → 001; Aurélio de Figueiredo "Compromisso Constitucional" (1896) → 002.

### Supplemental

- A — Museu da República catalog PDF: "Caçada ao Jaguar" (Marianne with Phrygian cap) → 014.
- B — Décio Villares MHN acervo: "Alegoria da Exposição Internacional do Centenário 1922" (reg. 310906) → 005; "Alegoria à Lei de 13 de Maio de 1888" → 004.
- C — Eliseu Visconti: Ex-libris Biblioteca Nacional (A803, 1903) → 009; A Providência guia Cabral (P332) → 013.
- D — Manoel Lopes Rodrigues: MAB Bahia "A República" (1896) → 003.
- E — Portinari "A Justiça de Salomão": FCO-2742, têmpera s/ tela, 179 × 191 cm, MASP, ca. 1948 → 006.

## Candidates Summary

| # | ID | Title | Artist | Date | Country | Conf |
|---|---|---|---|---|---|---|
| 001 | sq2-2026-05-19-patria-pedro-bruno-001 | Pátria | Pedro Bruno | 1919 | Brazil | high |
| 002 | sq2-2026-05-19-compromisso-constitucional-002 | Compromisso Constitucional | Aurélio de Figueiredo | 1896 | Brazil | high |
| 003 | sq2-2026-05-19-republica-manoel-lopes-rodrigues-003 | A República | Manoel Lopes Rodrigues | 1896 | Brazil | high |
| 004 | sq2-2026-05-19-alegoria-lei-aurea-villares-004 | Alegoria à Lei de 13 de Maio de 1888 | Décio Villares | 1888 | Brazil | medium |
| 005 | sq2-2026-05-19-alegoria-centenario-mhn-villares-005 | Alegoria da Exposição Int. Centenário 1922 | Décio Villares | 1922 | Brazil | high |
| 006 | sq2-2026-05-19-justica-salomao-portinari-006 | A Justiça de Salomão | Candido Portinari | 1948 | Brazil | high |
| 007 | sq2-2026-05-19-codigo-criminal-imperio-1830-007 | Código Criminal do Império (1830) | [s. n.] | 1830 | Brazil | medium |
| 008 | sq2-2026-05-19-codigo-criminal-imperio-1876-008 | Codigo criminal do imperio do Brazil (1876) | Vicente Alves de Paula Pessoa | 1876 | Brazil | medium |
| 009 | sq2-2026-05-19-ex-libris-bn-visconti-009 | Ex-libris da Biblioteca Nacional | Eliseu Visconti | 1903 | Brazil | high |
| 010 | sq2-2026-05-19-portinari-ciclos-economicos-mnec-010 | Ciclos Econômicos (Palácio Capanema) | Candido Portinari | 1936-1944 | Brazil | high |
| 011 | sq2-2026-05-19-codigo-penal-chile-1874-memoriachilena-011 | Código Penal chileno (1874) | [s. n.] | 1874 | Chile | medium |
| 012 | sq2-2026-05-19-republica-brasil-decio-villares-012 | A República (conjunto positivista Villares) | Décio Villares | 1889 | Brazil | low |
| 013 | sq2-2026-05-19-providencia-guia-cabral-visconti-013 | A Providência guia Cabral | Eliseu Visconti | 1900 | Brazil | medium |
| 014 | sq2-2026-05-19-caçada-jaguar-museu-republica-014 | Die Kämpfende Amazone (Caçada ao Jaguar) | August Kiss / M. Geiß | 1843/1860 | Brazil | medium |
| 015 | sq2-2026-05-19-gloria-republica-decio-villares-pintura-015 | Alegoria à República (MNBA) | Décio Villares | 1890 | Brazil | low |

## Issues / Notes for Pipeline

1. **Argentina (BNA):** Zero results; domains require login / limited crawlable content.
2. **Mexico (HNDM):** Download URLs return binary/PDF; query periodical catalog interface directly.
3. **Chile (BNC):** Penal Code 1874 record found but no associated visual imagery; PDF needs direct inspection.
4. **Brazil (memoria.bn.br):** Suggest searching illustrated periodicals (*Revista Illustrada*, *O Mequetrefe*, *A Semana Illustrada*).
5. **IHGB:** Archival inventories rather than visual works; search RIHGB periodical archive.
6. **IIIF:** No IIIF manifests for Brazilian sources (consistent with spec); all url_iiif left empty.
7. **Low-confidence items (012, 015):** entry-level; verify and replace with specific works.
8. **Item 014 geographic note:** German sculpture (August Kiss, 1843) installed at Palácio do Catete since 1860s; documented by Museu da República as Brazilian republican iconography — included as Brazil-based object.

All 15 candidate URLs checked against dedup_urls.txt: none appear in the 368-URL list.
