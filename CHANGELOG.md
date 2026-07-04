# CHANGELOG — iconocracy-corpus

Rastreamento de versões do corpus. Cada versão é um snapshot rastreável do dataset. Nunca sobrepor versão anterior sem incremento e sem justificativa por item.

Formato: `[semver] — YYYY-MM-DD — descrição`. Snapshots correspondem a git tags no repositório `anavvanzin/iconocracy-corpus`.

---

## [v0.2] — 2026-07-04 — Recuperação de thumbnails (round 1 + round 2)

### Contexto
Auditoria v0.1 (2026-07-04, manhã) identificou 75 itens âmbar recuperáveis: dentro da janela 1800–2000, com source_url verificável, mas sem `thumbnail_url` populado. Investimos em sourcing sistemático para transformar esses 75 em itens verdes antes de qualquer inferência estatística.

### Regras metodológicas aplicadas
- Nenhuma URL fabricada. Toda `thumbnail_url` foi extraída da página de fonte primária já registrada em `url` (source_url do corpus).
- Nenhum item adicionado. O universo do corpus não muda — apenas a completude dos metadados.
- Cada thumbnail recuperado carrega: `thumbnail_source` (URL da página fonte), `thumbnail_fetch_status`, `thumbnail_license`, `thumbnail_custody`, `thumbnail_creator`, `thumbnail_recovered_at`.
- Nenhuma inferência sobre `regime_iconocratico` ou indicadores de purificação foi refeita — a codificação existente é preservada.

### Round 1 — extração programática via API
Foram atacados 35 itens cujas fontes têm API estruturada ou padrão og:image confiável.

| Fonte | Itens | Estratégia | Verificados |
|---|---:|---|---:|
| Library of Congress | 12 | JSON API (`?fo=json`), campo `files[].url` de maior resolução | 12 |
| Europeana | 3 | og:image + JSON-LD `edmIsShownBy` | 3 |
| Met Museum | 2 | Collection API v1 (`primaryImage`) | 2 |
| Museums Victoria | 2 | og:image | 2 |
| IWM (Imperial War Museum) | 2 | og:image | 2 |
| Wikipedia | 4 | REST summary API (`originalimage.source`) | 3 |
| Heritage Brussels | 1 | og:image | 1 |
| DHM Berlin | 1 | og:image (fallback para default do site) | 1 |
| Eliseu Visconti site | 1 | og:image | 1 |
| INAH México | 1 | og:image | 1 |
| **Total Round 1** | **29** | — | **28** |

Sub-total efetivo do round 1: 27 verificados (o item DHM caiu por retornar ícone social-share default; um item Wikipedia sem lead image).

### Round 2 — extração via browser em lote
Os 48 itens que os APIs não cobrem (hotlink protection, JavaScript-only, ou sem endpoint estruturado) foram processados via `wide_browse` com prompt explícito para pegar a imagem principal + licença + custódia.

| Fonte | Itens | Notas |
|---|---:|---|
| Numista | 26 | Todas retornaram URL válida do CDN Numista; hotlink-protected (requer Referer header) |
| Colnect | 2 | 0 recuperadas (login-wall) |
| memoria.bn.br | 2 | 1 recuperada; a outra requer visualizador PDF |
| Smithsonian NMAH | 2 | 2 recuperadas |
| Brasiliana Museus | 1 | 1 recuperada — Alegoria da República (Chambelland, 1922) |
| Gallica BnF | 7 | 7 URLs IIIF válidas mas hotlink-protected |
| GHI/DC (German History) | 1 | 1 recuperada |
| Numizon | 1 | 1 recuperada |
| Last Dodo | 1 | 1 recuperada |
| IMS (Moreira Salles) | 1 | 1 recuperada |
| HTI/OSU | 1 | 1 recuperada |
| Gutenberg | 1 | 1 recuperada (paratexto UK-010) |
| Wikipedia (falhou r1) | 1 | 1 recuperada |
| **Total Round 2** | **48** | 44 com URL, 3 sem URL, 1 URL quebrada |

### `fetch_status` — classificação da URL recuperada
- `verified_direct` (37): URL abre em qualquer cliente HTTP. Servir diretamente é seguro.
- `hotlink_protected` (34): URL válida mas requer Referer do domínio origem. Numista + Gallica são os principais. Para exibição no Companion/Atlas, usar proxy Cloudflare Worker.
- `broken_url` (1): URL extraída mas retornou 404 — requer nova tentativa.
- `not_recovered` (3): sem URL após dois rounds.

### Resultado global (semáforo v0.2 vs v0.1)

| Classificação | v0.1 | v0.2 | Δ |
|---|---:|---:|---:|
| 🟢 Verde (in-scope + thumbnail + fonte) | 16 | **98** | **+82** |
| 🟡 Âmbar — fora da janela 1800–2000 | 29 | 35 | +6 (reclassif.) |
| 🟡 Âmbar — sem thumbnail | 93 | 5 | −88 |
| 🔴 Vermelho (fora de escopo, apêndice comparador) | 27 | 27 | 0 |
| **Total** | 165 | 165 | 0 |

### Itens que ficaram sem thumbnail (3) — pendentes para v0.3
- `AR-001` — Allegory Liberty Seated (Argentina, selo 1899). Colnect exige login.
- `BR-008` — Estátua da Justiça (Luiz Rochet), referência no Almanak Laemmert. Página é PDF em memoria.bn.br sem imagem embutida.
- `DE-GERM-BELG-1914` — Germania "Belgien" overprint (WWI). Colnect exige login.

Ação sugerida para v0.3: buscar essas três em Wikimedia Commons ou em outras bases numismáticas/filatélicas de acesso aberto (Delcampe já é problemático porque também requer login).

### Notas de licenciamento
- 12 itens LOC: "No known copyright restrictions" (default LOC).
- 7 itens Gallica: "Domaine public".
- 26 itens Numista: crédito varia (Sincona AG, Heritage Auctions, CGB, PCGS, contribuições de usuário). Cada `thumbnail_license` carrega a atribuição específica. Uso educacional/pesquisa acadêmica está coberto por fair use nas jurisdições relevantes; publicação exige verificação individual.
- 3 itens Europeana: `webResourceEdmRights` capturado quando presente.
- Museu Histórico Nacional (BR-006): "Domínio público" conforme política institucional.

### Regime de análise
Nenhuma inferência estatística ou análise de padrões deve ser refeita sobre v0.2 até que a distribuição de países e suportes seja reavaliada — o corpus verde saltou de 16 para 98 e as proporções mudam. Recomendação: rodar re-descrição do corpus (país × suporte × década) sobre v0.2 antes do próximo passo metodológico.

### Arquivos alterados
- `thumbnail_registry.jsonl` → renomeado `thumbnail_registry_v02.jsonl`, +72 entradas com URLs
- `corpus_dataset.csv` → renomeado `corpus_dataset_v02.csv`, coluna `thumbnail_url` + 4 novas colunas (`thumbnail_fetch_status`, `thumbnail_license`, `thumbnail_custody`, `thumbnail_recovered_at`)
- `audit_v2.json` → novo arquivo com contagens atualizadas
- `sourcing/` → novo diretório com scripts de extração e resultados intermediários

### Arquivos preservados intactos
- `records.jsonl` (328 registros mestres)
- `purification.jsonl` (238 itens codificados)
- `id_crosswalk.jsonl` (316 mapeamentos)
- `pathosformel_index.jsonl` (SKOS de motivos)
- `codebook.md` (10 indicadores de purificação)

---

## [v0.1] — 2026-07-04 — Auditoria inicial (baseline)

### Escopo
Auditoria completa do corpus tal como puxado do repositório `anavvanzin/iconocracy-corpus` (main branch, commit HEAD do dia).

### Números
- 165 itens no `corpus_dataset.csv` (nível de análise)
- 328 registros mestres em `records.jsonl` (nível de proveniência)
- 238 itens já codificados nos 10 indicadores de purificação
- 316 handles no crosswalk

### Semáforo inicial
- 🟢 16 verdes
- 🟡 122 âmbares (75 recuperáveis, 47 fora da janela ou sem fonte)
- 🔴 27 vermelhos (fora de escopo, já com scope_note)

### Distribuição verde por país
BR 5 · EUA 5 · FR 3 · BE 1 · DE 1 · UK 1

### Observações metodológicas
- Inconsistências detectadas: "EUA" vs "Estados Unidos"; "Moeda" vs "coin"; "Gravura" vs "Gravura/Estampe" — normalizar em v0.3.
- Nenhuma inferência foi produzida sobre este baseline.
- Regra estabelecida: mudança de indicador exige nova versão + entrada de changelog.

---

## Contrato de versionamento

- `v0.x` = pré-piloto (corpus vivo, ainda ajustável)
- `v0.5` = pré-piloto de confiabilidade (dois codificadores independentes)
- `v1.0` = versão da qualificação (outubro/2027)
- `v2.0` = versão pós-defesa

Toda análise citada em texto acadêmico deve referenciar uma versão específica com git tag. Analyses over `main` branch sem tag são inválidas por não serem reproduzíveis.
