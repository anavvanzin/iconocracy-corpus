# iconocracy-corpus — v0.2 snapshot

Snapshot pós-recuperação de thumbnails (2026-07-04).

## Números

| Métrica | v0.1 | v0.2 |
|---|---:|---:|
| 🟢 Verdes (in-scope + thumbnail + fonte) | 16 | **98** |
| 🟡 Âmbar — fora da janela 1800–2000 | 29 | 35 |
| 🟡 Âmbar — sem thumbnail | 93 | 5 |
| 🔴 Vermelho (fora de escopo) | 27 | 27 |

## Verdes por país (v0.2)
France 30 · United States 20 · Brazil 13 · Germany 10 · United Kingdom 8 · Belgium 7 · Italy 4 · Spain 2 · Portugal 2 · Austria 1 · Mexico 1

## Verdes por suporte
cartaz 22 · moeda 21 · estampa 11 · papel-moeda 10 · fotografia 9 · pintura 8 · gravura/litografia 6 · monumento 4 · selo 4 · gravura 2 · texto 1

## Arquivos

| Arquivo | Descrição |
|---|---|
| `CHANGELOG.md` | Histórico de versões com justificativa por mudança |
| `README_v02.md` | Este arquivo |
| `corpus_dataset_v02.csv` | Dataset achatado com thumbnails recuperados (165 linhas) |
| `thumbnail_registry_v02.jsonl` | Registro completo por item, com fetch_status/license/custody |
| `audit_v2.json` | Auditoria completa: verdes, âmbares, vermelhos com distribuições |
| `records.jsonl` | 328 registros mestres (inalterado) |
| `purification.jsonl` | 238 itens codificados (inalterado) |
| `id_crosswalk.jsonl` | 316 mapeamentos handle↔uuid (inalterado) |
| `pathosformel_index.jsonl` | SKOS de motivos (inalterado) |
| `codebook.md` | 10 indicadores de purificação (inalterado) |
| `sourcing/` | Scripts de extração e resultados intermediários (auditoria) |

## Como interpretar `thumbnail_fetch_status`

- `verified_direct` (37 itens): URL abre em qualquer cliente HTTP. Servir livremente.
- `hotlink_protected` (34 itens): URL válida mas requer Referer header do domínio origem (Numista, Gallica). Para exibição, usar proxy Cloudflare Worker.
- `existing_pre_v01` (27 itens): já tinha thumbnail antes desta recuperação.

## Pendências para v0.3 (3 itens sem thumbnail após rounds 1+2)

- `AR-001` — Allegory Liberty Seated (Argentina, selo 1899). Colnect exige login.
- `BR-008` — Estátua da Justiça (Luiz Rochet). Página é PDF sem imagem embutida.
- `DE-GERM-BELG-1914` — Germania "Belgien" overprint (WWI). Colnect exige login.

## Contrato de versionamento

- Nenhuma análise citável antes de tag git.
- Mudança de indicador = nova versão + entrada de changelog.
- Freeze v1.0 previsto para pré-qualificação (outubro/2027).

## Reprodução

Todos os scripts de extração estão em `sourcing/`:
- `extract_thumbnails.py` — round 1, extração via APIs
- `round1_candidates.json` — output cru
- `round1_validated.json` — output com validação de fetch
- `round2_urls.txt` + `round2_schema.json` — inputs do wide_browse
- `round2_candidates.json` — output cru do browser
- `round2_validated.json` — output validado
- `recovery_v02.json` + `recovery_v02.csv` — merge final

## Licenciamento

Metadados do corpus: CC0. Imagens de thumbnails: cada item carrega `thumbnail_license` e `thumbnail_custody`. Uso educacional/pesquisa acadêmica cobre a maioria dos casos; publicação requer verificação individual.
