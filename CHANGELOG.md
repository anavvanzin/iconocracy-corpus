# CHANGELOG — iconocracy-corpus

Rastreamento de versões do corpus. Cada versão é um snapshot rastreável do dataset. Nunca sobrepor versão anterior sem incremento e sem justificativa por item.

Formato: `[semver] — YYYY-MM-DD — descrição`. Snapshots correspondem a git tags no repositório `anavvanzin/iconocracy-corpus`.

---

## [v0.2] — 2026-07-04 — Recuperação de thumbnails (round 1 + round 2)

### Contexto
Auditoria v0.1 (2026-07-04, manhã) identificou 75 itens âmbar recuperáveis: dentro da janela 1800-2000, com `source_url` verificável, mas sem `thumbnail_url` populado. A recuperação v0.2 torna essas tentativas auditáveis antes de qualquer inferência estatística.

Correção de revisão aplicada em 2026-07-08: os artefatos foram alinhados ao conteúdo real do snapshot, `broken_url` deixou de contar como verde, metadados LOC foram normalizados e divergências visuais específicas foram corrigidas.

### Regras metodológicas aplicadas
- Nenhuma URL fabricada. Toda `thumbnail_url` vem de fonte primária, página institucional ou repositório de imagem verificável.
- Nenhum item adicionado. O universo do corpus permanece em 165 linhas no nível de análise.
- Campos `thumbnail_*` foram persistidos no export público (`corpus/corpus-data.json`), no dataset achatado (`data/processed/corpus_dataset.csv`) e no registro auditável (`data/processed/thumbnail_registry.jsonl`).
- Cada thumbnail recuperado carrega, quando disponível: `thumbnail_source`, `thumbnail_fetch_status`, `thumbnail_license`, `thumbnail_custody`, `thumbnail_creator` e `thumbnail_recovered_at`.
- Nenhuma inferência sobre `regime_iconocratico` ou indicadores de purificação foi refeita; a codificação existente foi preservada.

### Round 1 — extração programática via API
Foram atacados itens cujas fontes têm API estruturada ou padrão `og:image` confiável. O script `data/processed/v0.2/sourcing/extract_thumbnails.py` usa paths repo-relativos por padrão e aceita `--input`, `--output` e `--delay` para reprodução local.

| Fonte | Estratégia |
|---|---|
| Library of Congress | JSON API (`?fo=json`), com normalização escalar de `rights_advisory` e `dates` |
| Europeana | `og:image` + JSON-LD quando disponível |
| Met Museum | Collection API v1 (`primaryImage`) |
| Museums Victoria, IWM, DHM, INAH e outros | `og:image` com fallback documentado |
| Wikipedia/Wikimedia | REST summary API ou URL Commons validada manualmente |

### Round 2 — extração via browser em lote
Os itens sem endpoint estruturado foram processados via browser em lote, com captura de imagem principal, licença e custódia. O merge final está em `data/processed/v0.2/sourcing/recovery_v02.json` e `.csv`.

### `fetch_status` — classificação da URL recuperada
- `verified_direct` (38 verdes): URL abre em cliente HTTP comum.
- `hotlink_protected` (33 verdes): URL válida, mas requer `Referer` do domínio origem; Numista e Gallica são os principais casos.
- `existing_pre_v01` (26 verdes): thumbnail já existia antes da recuperação v0.2 e recebeu status explícito.
- `broken_url` (1): URL extraída retornou erro; documentada no registro, mas excluída dos verdes.

### Resultado global (semáforo v0.2 vs v0.1)

| Classificação | v0.1 | v0.2 | Δ |
|---|---:|---:|---:|
| 🟢 Verde (in-scope + thumbnail usável + fonte) | 16 | **97** | **+81** |
| 🟡 Âmbar — fora da janela 1800-2000 | 29 | 35 | +6 |
| 🟡 Âmbar — sem thumbnail usável | 93 | 6 | -87 |
| 🔴 Vermelho (fora de escopo, apêndice comparador) | 27 | 27 | 0 |
| **Total** | 165 | 165 | 0 |

### Itens que ficaram sem thumbnail usável (6) — pendentes para v0.3
- `AR-001` — Allegory, Liberty Seated (Argentina, selo 1899). Colnect exige login.
- `BR-006` — Alegoria da República (Carlos Chambelland). URL direta do MHN retornou erro; precisa nova fonte.
- `BR-008` — Estátua da Justiça (Luiz Rochet), referência no Almanak Laemmert. Página é PDF sem imagem embutida recuperável.
- `BR-016` — Alegoria da República (Estados Unidos do Brasil). Sem thumbnail recuperado.
- `DE-NOTG-1921` — Notgeld Bielefeld, Jungbrunnen silk note. Sem thumbnail recuperado.
- `DE-GERM-BELG-1914` — Germania "Belgien" overprint (WWI). Colnect exige login.

Ação sugerida para v0.3: buscar esses itens em Wikimedia Commons, acervos institucionais alternativos ou bases numismáticas/filatélicas de acesso aberto.

### Correções de integridade aplicadas na revisão
- `US-SLQ-1916`: substituída a página polonesa da Numista por imagem Commons do obverso do Standing Liberty quarter de 1916.
- `FR-SEM-SELO-1903`: substituído o placeholder por selo Semeuse de 1903 em Wikimedia Commons.
- `UK-PENNY-1860`: substituída a imagem para o reverso com Britannia.
- `BR-006`: tentativa `broken_url` preservada para auditoria, mas sem `thumbnail_url` canônica e fora do grupo verde.
- LOC: `thumbnail_license` usa o texto completo `No known restrictions on publication.`; `date_on_page` foi normalizado para escalar nos outputs de sourcing.

### Notas de licenciamento
- Itens LOC: `No known restrictions on publication.` conforme metadado `rights_advisory`.
- Gallica: `Domaine public` quando indicado.
- Numista: crédito varia por item; cada linha mantém atribuição própria em `thumbnail_license`.
- Europeana: `webResourceEdmRights` capturado quando presente.
- Publicação externa de imagens exige verificação individual por item.

### Regime de análise
Nenhuma inferência estatística ou análise de padrões deve ser refeita sobre v0.2 até que a distribuição de países e suportes seja reavaliada. O corpus verde saltou de 16 para 97, portanto proporções usadas antes do snapshot não devem ser reaproveitadas.

### Arquivos alterados
- `corpus/corpus-data.json` — persistência dos campos `thumbnail_*` do snapshot.
- `data/processed/corpus_dataset.csv` — dataset achatado de 165 linhas com colunas de thumbnail e status.
- `data/processed/thumbnail_registry.jsonl` — registro de 165 itens com proveniência, status, licença e custódia.
- `data/processed/v0.2/audit_v2.json` — auditoria v0.2 recalibrada.
- `data/processed/v0.2/README.md` — documentação do snapshot.
- `data/processed/v0.2/sourcing/` — script de extração e outputs intermediários.
- `tools/scripts/code_purification.py` — export CSV preserva as colunas canônicas de thumbnail.

### Arquivos preservados intactos
- `data/processed/records.jsonl` (328 registros mestres)
- `data/processed/purification.jsonl` (238 itens codificados)
- `data/processed/id_crosswalk.jsonl` (316 mapeamentos)
- `data/processed/pathosformel_index.jsonl` (SKOS de motivos)
- `data/docs/codebook.md` (10 indicadores de purificação)

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
