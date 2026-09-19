# Relatório de regeneração — corpus-data-enriched.json

**Data**: 2026-09-17
**Fonte autoritativa**: `corpus/corpus-data.json` (335 itens)
**Enriched anterior**: 95 itens (91 overlays legados preservados)
**Saída**: `corpus/corpus-data-enriched.json` (335 itens, ordenados por país + id)

## Órfãos do enriched anterior (revisão necessária)

Presentes no enriched antigo, **ausentes do ledger** — excluídos da regeneração:

- **FR-007** — République Française: 3e Emprunt de la Défense nationale
- **US-011** — Wake up America! Civilization calls every man, woman and child!
- **US-012** — Columbia calls—Enlist now for U.S. Army
- **DE-NOTG-1921** — Notgeld Bielefeld — Jungbrunnen (Fountain of Youth) silk note

## Distribuição por regime

| Regime | Itens |
|--------|-------|
| FUNDACIONAL | 163 |
| NORMATIVO | 103 |
| MILITAR | 54 |
| CONTRA-ALEGORIA | 15 |

## Distribuição por país

| País (ledger) | Itens |
|---------------|-------|
| France | 101 |
| Brazil | 72 |
| United States | 32 |
| Germany | 27 |
| United Kingdom | 23 |
| Italy | 20 |
| Belgium | 11 |
| Portugal | 11 |
| Netherlands | 10 |
| Spain | 10 |
| Austria | 4 |
| CL | 3 |
| Denmark | 3 |
| Mexico | 3 |
| Argentina | 1 |
| France (held in Austria) | 1 |
| Germany (Netherlands origin) | 1 |
| Switzerland | 1 |
| Uruguay | 1 |

## Qualidade e lacunas

- Itens com `regime_incerto` (classificador diverge do ledger): **180**
- Itens sem `date` no ledger (emitidos com `date: ""`): **22**
- Itens sem `support` útil (None/'?'): **83**
- Itens legados cujo regime mudou em relação ao enriched antigo (ledger vence, justificativa regenerada): **51**
- Valores de `support` em texto livre sem mapeamento canônico: **0**

### Cobertura de campos

| Campo | Itens preenchidos |
|-------|-------------------|
| creator | 91/335 |
| institution | 91/335 |
| source_archive | 91/335 |
| medium | 285/335 |
| medium_norm | 280/335 |
| period | 311/335 |
| rights | 86/335 |
| thumbnail_url | 38/335 |
| url_iiif | 42/335 |
| url_image_download | 81/335 |
| iiif_source | 91/335 |
| iiif_note | 74/335 |
| local_image_path | 78/335 |
| citation_chicago | 86/335 |
| citation_abnt | 335/335 |
| year | 294/335 |

## Anomalias do ledger

- **161 itens com `endurecimento_score` > 1.0** (máx. 3.0). A escala real parece ser 0–3 (média dos 10 indicadores, cada um 0–3), não 0–1. O schema externo exige máximo 1 — esses itens falham na validação de intervalo (classe conhecida). Recomendado: normalizar dividindo por 3 ou revisar o schema.
- 22 itens sem `date` (ano derivado null).
- `country` usa variantes com parênteses ('Germany (Netherlands origin)', 'France (held in Austria)') e o código 'CL' em vez de 'Chile' — `country_pt` foi derivado do país-base.

## Lacunas conhecidas dos 244 itens novos

Nulos até uma futura passada de rede/IIIF: `iiif_source`, `iiif_note`, `url_iiif`, `url_image_download`, `thumbnail_url`, `rights`, `creator`, `institution`, `source_archive`, `citation_chicago`. `period_norm` também é null para itens novos (ver docstring de `derive_period` no script). `local_image_path` é null para todos: `corpus/imagens/` não existe nesta máquina.

## Validação (2026-09-17)

- Estrutural: 335 itens, campos obrigatórios do schema presentes, sem ids duplicados, conjunto de ids idêntico ao do ledger.
- Overlay legado: nenhum campo de overlay (creator, institution, source_archive, thumbnail_url, url_iiif, citation_chicago, regime_justificativa) perdido nos 91 itens legados.
- JSON Schema (`imagens/schemas/corpus-data-enriched.schema.json`, draft-07): **221 violações, todas em duas classes conhecidas** — 161 × `endurecimento_score` acima do máximo 1 (escala real 0–3, ver Anomalias) e 60 × `id` fora do padrão `^[A-Z]{2,}(-[A-Z0-9]+)+$` (ids UUID das importações recentes do vault/IconoCode).
- Testes do repo: `pytest tests/test_corpus_export_idempotent.py tests/test_cross_file_consistency.py tests/test_id_crosswalk.py` — **21 passed**.

## Follow-up

- **Não sincronizado**: `/Users/ana/Research/imagens/site/data/corpus-data-enriched.json` (cópia do site) — atualizar em passo separado, fora deste repositório.
- Decidir o destino dos 4 órfãos (reimportar ao ledger ou aposentar).
- Revisar itens com `regime_incerto` listados abaixo.
- Resolver a tensão do schema: normalizar `endurecimento_score` (÷3) ou atualizar o schema para máximo 3; decidir se ids UUID entram no padrão ou se os 60 itens recebem ids canônicos.

### Itens com regime_incerto (ledger ≠ classificador)

- 0754a19f-a859-99e5-932d-17f5181496b2: ledger=FUNDACIONAL, classificador=NORMATIVO
- 0970108c-1619-50f5-bc85-719eb5f80aee: ledger=CONTRA-ALEGORIA, classificador=NORMATIVO
- 14990163-f5e4-a143-0d6b-288477d89a2b: ledger=FUNDACIONAL, classificador=NORMATIVO
- 235c545a-f3b8-568a-f268-178806a4bf07: ledger=NORMATIVO, classificador=MILITAR
- 3bc72151-1996-f7ca-b282-512024e54acf: ledger=FUNDACIONAL, classificador=NORMATIVO
- 3cb602f7-56b5-5b48-871e-629b65b216c8: ledger=MILITAR, classificador=NORMATIVO
- 46131280-d556-5ccf-b78f-f90523da0334: ledger=MILITAR, classificador=NORMATIVO
- 49706189-9d27-da9e-59d5-3467a32a1f5e: ledger=FUNDACIONAL, classificador=NORMATIVO
- 4f51943f-625d-c265-60ed-73edc3d29986: ledger=FUNDACIONAL, classificador=MILITAR
- 5b14d6a4-7b6d-5111-9253-b20bb72af0a1: ledger=FUNDACIONAL, classificador=NORMATIVO
- 6932b9c2-9bb3-5b21-9040-36f6323401e3: ledger=CONTRA-ALEGORIA, classificador=NORMATIVO
- 7b5ea66e-0285-59ea-a652-264f8a5e90bd: ledger=CONTRA-ALEGORIA, classificador=MILITAR
- 80b1d4ad-1aa4-7f87-35b7-ba8cea46f0cf: ledger=FUNDACIONAL, classificador=MILITAR
- 8d6151b3-9928-e42e-5dbc-713c10fe1a82: ledger=FUNDACIONAL, classificador=MILITAR
- 93b53069-d4b7-6c55-df87-f85d0341bdbe: ledger=FUNDACIONAL, classificador=MILITAR
- BE-002: ledger=NORMATIVO, classificador=MILITAR
- BE-003: ledger=FUNDACIONAL, classificador=NORMATIVO
- BE-5F-LEOPOLD-1832: ledger=FUNDACIONAL, classificador=NORMATIVO
- BE-CONGO-100F-1912: ledger=MILITAR, classificador=NORMATIVO
- BE-CONGO-1912: ledger=NORMATIVO, classificador=MILITAR
- BE-CONGO-MON-1921: ledger=MILITAR, classificador=NORMATIVO
- BR-010: ledger=FUNDACIONAL, classificador=NORMATIVO
- BR-018: ledger=NORMATIVO, classificador=FUNDACIONAL
- BR-019: ledger=CONTRA-ALEGORIA, classificador=MILITAR
- BR-022: ledger=FUNDACIONAL, classificador=MILITAR
- BR-026: ledger=NORMATIVO, classificador=FUNDACIONAL
- BR-028: ledger=FUNDACIONAL, classificador=NORMATIVO
- BR-029: ledger=FUNDACIONAL, classificador=NORMATIVO
- BR-032: ledger=FUNDACIONAL, classificador=NORMATIVO
- BR-033: ledger=FUNDACIONAL, classificador=NORMATIVO
- BR-038: ledger=NORMATIVO, classificador=FUNDACIONAL
- BR-039: ledger=FUNDACIONAL, classificador=NORMATIVO
- BR-044: ledger=FUNDACIONAL, classificador=MILITAR
- BR-046: ledger=FUNDACIONAL, classificador=NORMATIVO
- BR-1CR-1970: ledger=NORMATIVO, classificador=MILITAR
- DE-001: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-002: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-003: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-004: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-005: ledger=FUNDACIONAL, classificador=MILITAR
- DE-006: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-007: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-008: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-009: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-010: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-011: ledger=FUNDACIONAL, classificador=MILITAR
- DE-012: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-013: ledger=NORMATIVO, classificador=MILITAR
- DE-015: ledger=CONTRA-ALEGORIA, classificador=FUNDACIONAL
- DE-017: ledger=NORMATIVO, classificador=MILITAR
- DE-018: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-019: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-020: ledger=FUNDACIONAL, classificador=NORMATIVO
- DE-50M-1919: ledger=FUNDACIONAL, classificador=MILITAR
- DE-GERM-1900: ledger=MILITAR, classificador=NORMATIVO
- ES-003: ledger=FUNDACIONAL, classificador=NORMATIVO
- ES-004: ledger=FUNDACIONAL, classificador=MILITAR
- EU-001: ledger=FUNDACIONAL, classificador=MILITAR
- EU-002: ledger=FUNDACIONAL, classificador=NORMATIVO
- EU-003: ledger=FUNDACIONAL, classificador=NORMATIVO
- EU-004: ledger=FUNDACIONAL, classificador=NORMATIVO
- EU-005: ledger=FUNDACIONAL, classificador=NORMATIVO
- EU-006: ledger=FUNDACIONAL, classificador=NORMATIVO
- EU-007: ledger=FUNDACIONAL, classificador=NORMATIVO
- EU-008: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-001: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-002: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-003: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-011: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-015: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-016: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-017: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-020: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-022: ledger=CONTRA-ALEGORIA, classificador=MILITAR
- FR-025: ledger=NORMATIVO, classificador=MILITAR
- FR-026: ledger=NORMATIVO, classificador=MILITAR
- FR-028: ledger=NORMATIVO, classificador=MILITAR
- FR-029: ledger=NORMATIVO, classificador=MILITAR
- FR-031: ledger=CONTRA-ALEGORIA, classificador=NORMATIVO
- FR-032: ledger=CONTRA-ALEGORIA, classificador=FUNDACIONAL
- FR-033: ledger=CONTRA-ALEGORIA, classificador=NORMATIVO
- FR-036: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-047: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-048: ledger=NORMATIVO, classificador=FUNDACIONAL
- FR-049: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-050: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-051: ledger=MILITAR, classificador=NORMATIVO
- FR-054: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-055: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-056: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-057: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-058: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-059: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-060: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-061: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-062: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-063: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-064: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-065: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-066: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-067: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-071: ledger=MILITAR, classificador=NORMATIVO
- FR-078: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-079: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-080: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-083: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-084: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-086: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-091: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-093: ledger=NORMATIVO, classificador=FUNDACIONAL
- FR-095: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-096: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-CERES-5F-1849: ledger=FUNDACIONAL, classificador=NORMATIVO
- FR-HERC-1870: ledger=NORMATIVO, classificador=FUNDACIONAL
- FR-PIAST-1885: ledger=MILITAR, classificador=NORMATIVO
- IT-007: ledger=NORMATIVO, classificador=MILITAR
- MX-001: ledger=NORMATIVO, classificador=FUNDACIONAL
- MX-002: ledger=FUNDACIONAL, classificador=MILITAR
- NL-001: ledger=FUNDACIONAL, classificador=NORMATIVO
- NL-004: ledger=FUNDACIONAL, classificador=NORMATIVO
- NL-005: ledger=FUNDACIONAL, classificador=NORMATIVO
- NL-006: ledger=FUNDACIONAL, classificador=NORMATIVO
- NL-007: ledger=FUNDACIONAL, classificador=NORMATIVO
- NL-008: ledger=FUNDACIONAL, classificador=NORMATIVO
- PT-001: ledger=MILITAR, classificador=FUNDACIONAL
- PT-002: ledger=FUNDACIONAL, classificador=NORMATIVO
- PT-003: ledger=FUNDACIONAL, classificador=NORMATIVO
- PT-004: ledger=FUNDACIONAL, classificador=NORMATIVO
- PT-005: ledger=NORMATIVO, classificador=MILITAR
- PT-006: ledger=FUNDACIONAL, classificador=MILITAR
- PT-007: ledger=FUNDACIONAL, classificador=NORMATIVO
- SCOUT-337: ledger=FUNDACIONAL, classificador=NORMATIVO
- SCOUT-414: ledger=NORMATIVO, classificador=FUNDACIONAL
- SCOUT-558: ledger=FUNDACIONAL, classificador=MILITAR
- SCOUT-559: ledger=FUNDACIONAL, classificador=NORMATIVO
- SCOUT-560: ledger=NORMATIVO, classificador=MILITAR
- SCOUT-567: ledger=NORMATIVO, classificador=MILITAR
- SCOUT-568: ledger=NORMATIVO, classificador=FUNDACIONAL
- SCOUT-569: ledger=NORMATIVO, classificador=MILITAR
- SCOUT-571: ledger=CONTRA-ALEGORIA, classificador=NORMATIVO
- SCOUT-572: ledger=NORMATIVO, classificador=MILITAR
- SCOUT-573: ledger=NORMATIVO, classificador=FUNDACIONAL
- SCOUT-574: ledger=NORMATIVO, classificador=MILITAR
- UK-005: ledger=FUNDACIONAL, classificador=NORMATIVO
- UK-010: ledger=NORMATIVO, classificador=MILITAR
- UK-011: ledger=FUNDACIONAL, classificador=MILITAR
- UK-012: ledger=FUNDACIONAL, classificador=MILITAR
- UK-013: ledger=FUNDACIONAL, classificador=NORMATIVO
- UK-014: ledger=FUNDACIONAL, classificador=NORMATIVO
- UK-015: ledger=FUNDACIONAL, classificador=NORMATIVO
- UK-016: ledger=FUNDACIONAL, classificador=NORMATIVO
- UK-017: ledger=FUNDACIONAL, classificador=MILITAR
- UK-FLORIN-1902: ledger=NORMATIVO, classificador=MILITAR
- UK-HALFPENNY-1695: ledger=FUNDACIONAL, classificador=NORMATIVO
- UK-PENNY-1860: ledger=NORMATIVO, classificador=MILITAR
- UK-TRADE-1895: ledger=NORMATIVO, classificador=MILITAR
- US-001: ledger=FUNDACIONAL, classificador=NORMATIVO
- US-005: ledger=FUNDACIONAL, classificador=NORMATIVO
- US-006: ledger=FUNDACIONAL, classificador=NORMATIVO
- US-010: ledger=FUNDACIONAL, classificador=NORMATIVO
- US-019: ledger=CONTRA-ALEGORIA, classificador=MILITAR
- US-020: ledger=CONTRA-ALEGORIA, classificador=NORMATIVO
- US-021: ledger=FUNDACIONAL, classificador=NORMATIVO
- US-022: ledger=FUNDACIONAL, classificador=MILITAR
- US-023: ledger=FUNDACIONAL, classificador=MILITAR
- US-024: ledger=FUNDACIONAL, classificador=MILITAR
- US-SEATED-1840: ledger=FUNDACIONAL, classificador=NORMATIVO
- US-SLQ-1916: ledger=NORMATIVO, classificador=MILITAR
- UY-001: ledger=FUNDACIONAL, classificador=NORMATIVO
- a7971ac5-e277-f70a-bb11-ba25db7e6ac0: ledger=FUNDACIONAL, classificador=MILITAR
- ac900ea3-9461-bae5-e797-f93d58d4845b: ledger=FUNDACIONAL, classificador=NORMATIVO
- b1966d16-8731-58e4-a898-8ef3c44f59cb: ledger=CONTRA-ALEGORIA, classificador=FUNDACIONAL
- c9966731-1c38-5d06-9bc6-6081b5a87d1a: ledger=MILITAR, classificador=NORMATIVO
- ce773ab1-3bfc-9f6e-754a-efe0c567916d: ledger=CONTRA-ALEGORIA, classificador=NORMATIVO
- d8a81f31-5b21-573f-912e-64bb29559c06: ledger=FUNDACIONAL, classificador=MILITAR
- da35cbd9-2e8c-24a6-7c44-d7f1741e0a2a: ledger=FUNDACIONAL, classificador=NORMATIVO
- e0399402-b59d-5050-9776-b67f2c69a6b2: ledger=CONTRA-ALEGORIA, classificador=MILITAR
- e1d2e177-0905-a3bc-2e17-f6dd4f040db0: ledger=FUNDACIONAL, classificador=NORMATIVO
- f988255c-abaa-fb73-74fb-fcbce9abdaa8: ledger=FUNDACIONAL, classificador=NORMATIVO
- ff43ad57-b420-3e54-24ec-9d15caef8d64: ledger=FUNDACIONAL, classificador=MILITAR

### Regimes alterados em itens legados

- BE-002: MILITAR → NORMATIVO
- BR-001: NORMATIVO → FUNDACIONAL
- BR-004: NORMATIVO → FUNDACIONAL
- BR-010: NORMATIVO → FUNDACIONAL
- DE-001: NORMATIVO → FUNDACIONAL
- DE-002: NORMATIVO → FUNDACIONAL
- DE-003: NORMATIVO → FUNDACIONAL
- DE-004: NORMATIVO → FUNDACIONAL
- DE-005: MILITAR → FUNDACIONAL
- DE-006: NORMATIVO → FUNDACIONAL
- DE-007: NORMATIVO → FUNDACIONAL
- DE-008: NORMATIVO → FUNDACIONAL
- DE-009: NORMATIVO → FUNDACIONAL
- DE-010: NORMATIVO → FUNDACIONAL
- DE-011: MILITAR → FUNDACIONAL
- DE-012: NORMATIVO → FUNDACIONAL
- DE-013: MILITAR → NORMATIVO
- EU-001: MILITAR → FUNDACIONAL
- EU-002: NORMATIVO → FUNDACIONAL
- EU-003: NORMATIVO → FUNDACIONAL
- EU-004: NORMATIVO → FUNDACIONAL
- EU-005: NORMATIVO → FUNDACIONAL
- EU-006: NORMATIVO → FUNDACIONAL
- EU-007: NORMATIVO → FUNDACIONAL
- EU-008: NORMATIVO → FUNDACIONAL
- FR-001: NORMATIVO → FUNDACIONAL
- FR-002: NORMATIVO → FUNDACIONAL
- FR-003: NORMATIVO → FUNDACIONAL
- FR-011: NORMATIVO → FUNDACIONAL
- FR-015: NORMATIVO → FUNDACIONAL
- FR-016: NORMATIVO → FUNDACIONAL
- FR-017: NORMATIVO → FUNDACIONAL
- FR-020: NORMATIVO → FUNDACIONAL
- MX-001: FUNDACIONAL → NORMATIVO
- NL-001: NORMATIVO → FUNDACIONAL
- NL-004: NORMATIVO → FUNDACIONAL
- NL-005: NORMATIVO → FUNDACIONAL
- NL-006: NORMATIVO → FUNDACIONAL
- NL-007: NORMATIVO → FUNDACIONAL
- NL-008: NORMATIVO → FUNDACIONAL
- PT-001: FUNDACIONAL → MILITAR
- PT-002: NORMATIVO → FUNDACIONAL
- PT-003: NORMATIVO → FUNDACIONAL
- PT-004: NORMATIVO → FUNDACIONAL
- PT-005: MILITAR → NORMATIVO
- UK-005: NORMATIVO → FUNDACIONAL
- US-001: NORMATIVO → FUNDACIONAL
- US-005: NORMATIVO → FUNDACIONAL
- US-006: NORMATIVO → FUNDACIONAL
- US-010: NORMATIVO → FUNDACIONAL
- UY-001: NORMATIVO → FUNDACIONAL
