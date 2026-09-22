# iconocracy-corpus — v0.2 snapshot

Snapshot pos-recuperacao de thumbnails (2026-07-04; revisao de integridade 2026-07-08).

## Numeros

| Metrica | v0.1 | v0.2 |
|---|---:|---:|
| Verde — in-scope + thumbnail usavel + fonte | 16 | **97** |
| Ambar — fora da janela 1800-2000 | 29 | 35 |
| Ambar — sem thumbnail usavel | 93 | 6 |
| Vermelho — fora de escopo | 27 | 27 |

## Verdes por pais (v0.2)

France 30 · United States 20 · Brazil 12 · Germany 10 · United Kingdom 8 · Belgium 7 · Italy 4 · Spain 2 · Portugal 2 · Austria 1 · Mexico 1

## Verdes por suporte

cartaz 22 · moeda 21 · estampa 11 · papel-moeda 10 · fotografia 9 · pintura 7 · gravura/litografia 6 · monumento 4 · selo 4 · gravura 2 · texto 1

## Arquivos

| Arquivo | Descricao |
|---|---|
| `data/processed/v0.2/README.md` | Este arquivo |
| `CHANGELOG.md` | Historico de versoes com justificativa por mudanca |
| `corpus/corpus-data.json` | Export publico com campos `thumbnail_*` persistidos para o snapshot |
| `data/processed/corpus_dataset.csv` | Dataset achatado com 165 linhas e colunas de thumbnail/status |
| `data/processed/thumbnail_registry.jsonl` | Registro completo de 165 itens com `fetch_status`, licenca e custodia |
| `data/processed/v0.2/audit_v1.json` | Auditoria baseline |
| `data/processed/v0.2/audit_v2.json` | Auditoria v0.2 com verdes, ambares, vermelhos e distribuicoes |
| `data/processed/v0.2/amber_recoverable_full.json` | Entrada dos candidatos recuperaveis |
| `data/processed/v0.2/sourcing/` | Scripts de extracao e resultados intermediarios auditaveis |

## Como interpretar `thumbnail_fetch_status`

- `verified_direct` (38 itens verdes): URL abre em cliente HTTP comum.
- `hotlink_protected` (33 itens verdes): URL valida, mas requer `Referer` do dominio de origem; para exibicao, usar proxy.
- `existing_pre_v01` (26 itens verdes): thumbnail ja existia antes da recuperacao v0.2 e foi backfilled com status explicito.
- `broken_url` (1 item): URL extraida retornou erro; fica fora dos verdes ate substituicao.

## Pendencias para v0.3 (6 itens sem thumbnail usavel)

- `AR-001` — Allegory, Liberty Seated (Argentina, selo 1899). Colnect exige login.
- `BR-006` — Alegoria da Republica (Carlos Chambelland). URL direta do MHN retornou erro; precisa nova fonte.
- `BR-008` — Estatua da Justica (Luiz Rochet). Pagina e PDF sem imagem embutida recuperavel.
- `BR-016` — Alegoria da Republica (Estados Unidos do Brasil). Sem thumbnail recuperado.
- `DE-NOTG-1921` — Notgeld Bielefeld, Jungbrunnen silk note. Sem thumbnail recuperado.
- `DE-GERM-BELG-1914` — Germania "Belgien" overprint (WWI). Colnect exige login.

## Correcoes de integridade aplicadas na revisao

- `US-SLQ-1916` deixou de apontar para a pagina polonesa da Numista e agora usa o obverso de 1916 em Wikimedia Commons.
- `FR-SEM-SELO-1903` usa o selo Semeuse de 1903 em Wikimedia Commons.
- `UK-PENNY-1860` usa a imagem do reverso da Britannia.
- Metadados LOC foram normalizados para valores escalares, com `thumbnail_license` por extenso.
- `BR-006` permanece documentado como tentativa `broken_url`, mas nao conta como verde.

## Reproducao

Todos os scripts e outputs de extracao ficam em `data/processed/v0.2/sourcing/`:

- `extract_thumbnails.py` — round 1, extracao via APIs, com paths repo-relativos por padrao.
- `round1_candidates.json` — output cru.
- `round1_validated.json` — output com validacao de fetch.
- `round2_urls.txt` + `round2_schema.json` — inputs do round 2.
- `round2_candidates.json` — output cru do browser.
- `round2_validated.json` — output validado.
- `round2_lookup.json` — lookup de IDs e URLs do round 2.
- `recovery_v02.json` + `recovery_v02.csv` — merge final da recuperacao.

## Licenciamento

Metadados do corpus: CC0. Imagens de thumbnails: cada item carrega `thumbnail_license` e `thumbnail_custody`. Uso educacional/pesquisa academica cobre parte dos casos; publicacao requer verificacao individual por item.
