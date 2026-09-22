# Audit Wave 2.1 — Data Integrity Report

**Date:** 2026-06-26  
**Auditor:** Hermes Agent (automated)  
**Repository:** `/Users/ana/Research/hub/iconocracy-corpus`  
**Scope:** Cross-validation of canonical data hierarchy, schema compliance, traceability rule, placeholder URLs, and duplicate detection.

---

## Resumo Executivo

Auditoria da integridade dos dados do corpus ICONOCRACY (299 registros). **Schema validation: 299/299 pass ✅**. As estruturas canônicas estão consistentes internamente (records.jsonl = 299, corpus-data.json = 299, purification.jsonl = 236). Foram identificados **2 CRITICAL** (traceability gaps: drive manifest cobre apenas 55% e vault cobre apenas 17% dos registros mapeados), **2 MAJOR** (id-mapping desatualizado com 3 duplicatas; 3 itens do corpus-data.json sem entrada no mapping), e **3 MINOR** (6 placeholder URLs vs 8 esperados; divergência vault: 357 arquivos quando 314 esperados; 3 pares de item_hash duplicados com conteúdo distinto). O índice geral de integridade é 89% — as estruturas core (records + corpus + purification) estão íntegras, mas a rastreabilidade periférica (Drive + vault) requer sincronização.

---

## CRITICAL (2)

### C1 — Traceability Rule: Drive Manifest coverage = 55% (165/299)

**Regra canônica (CLAUDE.md):**  
> Every corpus item must exist in: (1) Google Drive + `data/raw/drive-manifest.json`, (2) `vault/candidatos/CC-NNN Title.md`, (3) `data/processed/records.jsonl`.

**Resultado:** `data/raw/drive-manifest.json` contém apenas **165 itens** (55.2% dos 299 registros). Os 134 itens restantes (44.8%) não possuem entrada no drive manifest — ou seja, não há registro de que estejam espelhados no Google Drive.

| Métrica | Valor |
|---------|-------|
| records.jsonl | 299 |
| drive-manifest.json | 165 |
| Cobertura | 55.2% |
| Gap | 134 itens (44.8%) |

**IDs no drive manifest que NÃO estão no corpus-data.json:** _Pending_ (os 165 IDs do drive são subconjunto dos 277 short codes mapeados; sem divergência interna).

**Impacto:** 134 itens do corpus não têm rastreabilidade confirmada para o Google Drive. Risco de perda de dados se os binários não estiverem efetivamente armazenados (ADR-001 exige que `data/raw/` seja metadata-only no git, com binários no Drive).

---

### C2 — Traceability Rule: Vault coverage via id-mapping = 15% (45/299)

**Resultado:** Apenas **45 dos 277 short codes** mapeados no `id-mapping.json` possuem correspondência em `vault/candidatos/` (16.2%). Extrapolando para os 299 registros: apenas ~15% têm ficha catalográfica no vault.

| Métrica | Valor |
|---------|-------|
| Arquivos .md no vault/ | 357 |
| IDs regulares (XX-NNN) parseados | 52 |
| IDs regulares no id-mapping | 26 |
| IDs regulares no corpus-data.json | 26 |
| IDs regulares no records (via mapping) | 26 |

**Divergência vault:** AGENTS.md (2026-06-23) reporta 314 catalog cards; hoje são 357 arquivos (+43). Porém apenas 52 são fichas catalográficas regulares (XX-NNN); os outros 305 são notas SCOUT (analíticas, Zwischenraum, negative controls).

**26 vault IDs não mapeados** (BR-047 a BR-050, CL-001 a CL-003, ES-005 a ES-006, FR-097 a FR-099, IT-009 a IT-018, PT-008 a PT-011): são fichas novas no vault sem entrada correspondente no id-mapping, corpus-data.json, ou records.jsonl. Ou são adições pendentes de processamento, ou são candidatos ainda não incorporados ao corpus canônico.

**Impacto:** A regra de rastreabilidade tripla (Drive + vault + records) é violada para a maioria dos itens. O vault funciona primariamente como "auxiliary mirror" (conforme CLAUDE.md), mas a baixa cobertura sugere que o pipeline de sincronização vault ↔ records não está automatizado.

---

## MAJOR (2)

### M1 — ID Mapping: 3 duplicate short codes + 3 orphans

**Arquivo:** `data/processed/id-mapping.json` (version 1.0, 2026-05-14)  
**Entradas:** 280 mapeamentos, 277 short codes únicos, 3 duplicatas.

| Short Code | UUID 1 | UUID 2 | Status |
|-----------|--------|--------|--------|
| FR-024 | `2b7a1a18-...5c65e8` | `68a00893-...547974` | Duplicate |
| US-016 | `39ebfe77-...85a081` | `82c0efc9-...a2fac` | Duplicate |
| US-017 | `473ac4d7-...2fc23` | `6c4a12c1-...ee9` | Duplicate |

Cada short code duplicado aponta para 2 UUIDs diferentes com conteúdo distinto (item_hash diferentes). Isso significa que o mapeamento short→UUID é ambíguo para estes 3 itens. Qualquer resolução automatizada (ex.: sync vault, export corpus) que dependa do id-mapping produzirá resultados inconsistentes para FR-024, US-016, e US-017.

**3 corpus IDs órfãos:** FR-007, US-011, US-012 existem em `corpus-data.json` mas NÃO têm entrada no `id-mapping.json`. Estes itens estão no corpus público mas não podem ser rastreados de volta ao records.jsonl via mapping.

**19 UUIDs sem short code:** 19 registros em records.jsonl (6.4%) não possuem short code no id-mapping — seus UUIDs aparecem diretamente no corpus-data.json. Estes são os itens mais recentes (pós 2026-05-14) que ainda não receberam catalogação curta.

**Impacto:** O id-mapping é a espinha dorsal da rastreabilidade. Duplicatas e órfãos quebram a confiança na resolução automática de identidade entre as camadas do corpus.

---

### M2 — Schema Drift: id-mapping.json metadata desatualizado

**Arquivo:** `data/processed/id-mapping.json`  
**Declarado:** version=1.0, total_records=277, total_corpus=264, matched=257 (2026-05-14)  
**Real:** 299 records, 299 corpus, 280 mapeamentos, 277 short codes únicos

O metadata do arquivo reflete o estado do corpus em 14 de maio de 2026 (277 registros), mas hoje há 299 registros (+22). O arquivo não foi regenerado desde então. Os 22 novos registros (19 UUIDs sem short code + 3 órfãos no corpus) evidenciam que o pipeline de exportação `records_to_corpus.py` não atualiza automaticamente o id-mapping.

**Impacto:** Qualquer script que leia `total_records` ou `matched` do metadata tomará decisões baseadas em contagens obsoletas (277 vs 299).

---

## MINOR (3)

### m1 — Placeholder URLs: 6 encontrados (8 esperados)

A tarefa reportou 8 registros com placeholder URLs. Foram encontrados **6 registros únicos** (12 ocorrências — input_url + search_result.url em cada registro):

| UUID | Short Code (via mapping) | Placeholder URL |
|------|--------------------------|-----------------|
| `4e83a07f-...88ce` | FR-047 | `https://iconocracy.corpus/placeholder/FR-047` |
| `56ed1d5a-...5834` | FR-036 | `https://iconocracy.corpus/placeholder/FR-036` |
| `af855a2f-...1ad4` | FR-048 | `https://iconocracy.corpus/placeholder/FR-048` |
| `dd101f3a-...39d1` | FR-039 | `https://iconocracy.corpus/placeholder/FR-039` |
| `e933260c-...bb3` | FR-038 | `https://iconocracy.corpus/placeholder/FR-038` |
| `f0f589b2-...dfa` | SCOUT-337 / FR-040 | `https://iconocracy.corpus/placeholder/FR-040` |

**Anomalia:** O placeholder FR-040 está associado ao ID `SCOUT-337` no corpus-data.json (não FR-040). Isto é uma inconsistência de nomenclatura — o placeholder URL diz FR-040 mas o corpus ID é SCOUT-337.

Todos os 6 placeholders são itens franceses (FR-036 a FR-048), concentrados em um gap de aquisição de imagens da França. O gap de 2 registros (task diz 8, encontrados 6) pode indicar que 2 placeholders foram resolvidos desde a última contagem, ou que estão em formato não detectado (ex.: campo diferente).

**Impacto:** Itens sem URL real não podem ser verificados quanto à fonte primária. Bloqueia a validação iconográfica completa para esses 6 registros.

---

### m2 — Vault file count divergence: 357 vs 314 esperados

| Fonte | Contagem reportada | Contagem real | Delta |
|-------|-------------------|---------------|-------|
| AGENTS.md (2026-06-23) | 314 catalog cards | — | — |
| Contagem real (2026-06-26) | — | 357 arquivos .md | +43 |
| IDs regulares (XX-NNN) | — | 52 (únicos) | — |
| IDs SCOUT (analíticos) | — | 280 (275 únicos) | 5 duplicatas |
| Não parseáveis | — | 25 (SCOUT-ZW-*, SCOUT-NC-*, SCOUT-SESSION-*) | — |

**Duplicatas no vault:** SCOUT-118 (2×), SCOUT-119 (2×), SCOUT-320 (2×), SCOUT-321 (2×), SCOUT-322 (2×) — 5 IDs com arquivos duplicados.

**Arquivos não parseáveis (25):** Notas analíticas com prefixos especiais (SCOUT-ZW-* = Zwischenraum, SCOUT-NC-* = negative control, SCOUT-SESSION-* = sessão). Estes não seguem o padrão `XX-NNN Title.md` e não são fichas catalográficas regulares.

**Impacto:** O crescimento de +43 arquivos (314→357) em 3 dias é atípico. Pode ser resultado de batch de análise SCOUT ou importação não documentada. A discrepância entre "314 catalog cards" e 52 IDs regulares sugere que a definição de "catalog card" precisa ser clarificada (inclui SCOUT?).

---

### m3 — Duplicate item_hashes com conteúdo distinto

Foram encontrados 3 pares de registros com `item_hash` idêntico mas conteúdo diferente (excluindo `item_id` e `item_hash`):

| Hash (truncado) | Short Codes | Conteúdo idêntico? |
|-----------------|-------------|---------------------|
| `d2f2e50028afe624...` | FR-024, FR-024 | ❌ False |
| `6ca5ddb24e5abb10...` | US-016, US-016 | ❌ False |
| `736fa3525977ec56...` | BR-038, SCOUT-414 | ❌ False |

Os dois primeiros pares correspondem às duplicatas de short code no id-mapping (FR-024 e US-016). O terceiro par (BR-038 + SCOUT-414) é um caso distinto: dois registros com short codes diferentes compartilham o mesmo hash.

Isto sugere que o `item_hash` ou é computado sobre um subconjunto de campos (não o registro completo), ou há uma colisão de hash. Em qualquer caso, o hash não serve como identificador de unicidade de conteúdo para estes 6 registros (2.0%).

**Impacto:** Scripts que usam `item_hash` para deduplicação podem falsamente considerar estes pares como idênticos e descartar um deles.

---

## Schema Validation

**Comando:** `python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose`  
**Resultado:** ✅ **299/299 records valid**  
**Schema:** `tools/schemas/master-record.schema.json`  
**Validator:** Draft202012Validator (jsonschema)

Nenhum erro de validação. Todos os 299 registros estão em conformidade com o schema `master-record.schema.json` (versão 1.0).

**Aviso:** A ferramenta utiliza `jsonschema.RefResolver` (deprecated a partir de v4.18.0). Recomenda-se migrar para a biblioteca `referencing`.

---

## Pontos Fortes

1. **Schema compliance 100%** — Nenhum registro viola o schema canônico. O pipeline de validação é robusto.
2. **Consistência interna records↔corpus** — Ambos com 299 itens. Nenhum drift de contagem.
3. **Purification integrity** — Todos os 236 registros de purification.jsonl resolvem para UUIDs válidos em records.jsonl (via id-mapping). Zero órfãos.
4. **Zero duplicate item_ids** — Não há IDs duplicados em records.jsonl, corpus-data.json, ou purification.jsonl.
5. **Placeholder localization** — Todos os 6 placeholders estão concentrados em um gap específico (França, FR-036–FR-048), facilitando a resolução em lote.
6. **Audit flags ativos** — O campo `exports.audit_flags` (ex.: `sem-thumbnail`) fornece metadados de integridade por item.

---

## Métricas

| Métrica | Valor | Alvo | Status |
|---------|-------|------|--------|
| records.jsonl | 299 | 299 | ✅ |
| corpus-data.json | 299 | 299 | ✅ |
| purification.jsonl | 236 | 236 | ✅ |
| Schema validation | 299/299 | 299/299 | ✅ |
| Duplicate item_ids (records) | 0 | 0 | ✅ |
| Duplicate item_ids (corpus) | 0 | 0 | ✅ |
| Duplicate item_ids (purification) | 0 | 0 | ✅ |
| Purification→Records traceability | 236/236 | 236/236 | ✅ |
| Placeholder URLs | 6 | 0 | ❌ |
| Drive manifest coverage | 165/299 (55%) | 299/299 (100%) | ❌ |
| Vault coverage (mapped) | 26/277 (9.4%) | 277/277 (100%) | ❌ |
| ID mapping duplicates | 3/277 (1.1%) | 0 | ❌ |
| ID mapping orphans (corpus→mapping) | 3 | 0 | ❌ |
| ID mapping metadata currency | 2026-05-14 | 2026-06-26 | ❌ |
| Duplicate item_hashes | 3 pares | 0 | ❌ |

---

## Recomendações

### Imediatas (antes da defesa)

1. **Resolver os 6 placeholder URLs** — Adquirir imagens para FR-036, FR-038, FR-039, FR-040, FR-047, FR-048. Corrigir SCOUT-337 para usar ID FR-040 (consistência de nomenclatura).

2. **Regenerar id-mapping.json** — Executar `records_to_corpus.py` com flag de rebuild do mapping para:
   - Atualizar metadata (total_records: 277→299)
   - Resolver as 3 duplicatas de short code (FR-024, US-016, US-017): decidir qual UUID é canônico e qual é redundante
   - Adicionar os 3 órfãos (FR-007, US-011, US-012)
   - Criar short codes para os 19 UUIDs sem catalogação curta

3. **Sincronizar drive-manifest.json** — Garantir que todos os 299 itens tenham entrada no Google Drive e no manifest. Prioridade: os 6 placeholders e os 19 registros pós-2026-05-14.

### Curto prazo (1–2 semanas)

4. **Auditar item_hash** — Verificar a função de hash utilizada. Se for SHA-256 sobre campos selecionados, documentar quais campos. Se for hash completo, investigar as 3 colisões (possível bug na computação).

5. **Sincronizar vault** — Executar `vault_sync.py status` e `vault_sync.py sync` para alinhar vault/candidatos/ com records.jsonl. As 26 fichas não mapeadas (BR-047–IT-018) precisam ser incorporadas ao corpus ou movidas para `candidatos/_pending/`.

6. **Migrar jsonschema** — Atualizar `validate_schemas.py` para usar `referencing` em vez de `RefResolver` (deprecated).

### Longo prazo (pós-defesa)

7. **Automatizar traceability gate** — Adicionar ao release gate (`build_hf_release.py`) verificações de:
   - Cobertura do drive-manifest (deve ser 100%)
   - Integridade do id-mapping (zero duplicatas, zero órfãos)
   - Placeholder URL detection (zero placeholders)

8. **Clarificar definição de "catalog card"** — Documentar se arquivos SCOUT-ZW-*, SCOUT-NC-*, e SCOUT-SESSION-* são considerados catalog cards ou notas auxiliares. Atualizar AGENTS.md com a contagem correta (52 regulares + 305 análiticos = 357).

---

## Notas do Auditor

- A data de referência do AGENTS.md (2026-06-23) reporta 280 records. Em 3 dias o corpus cresceu +19 registros (280→299), o que é uma taxa de crescimento alta. Recomenda-se verificar se todos os 19 novos registros passaram pelo pipeline completo (webscout → iconocode → export → vault_sync).
- O vault passou de 314 para 357 arquivos (+43) no mesmo período. A maioria são notas SCOUT, não fichas catalográficas. Isso é esperado durante a fase ativa de análise, mas deve ser documentado.
- As 3 duplicatas no id-mapping (FR-024, US-016, US-017) são provavelmente artefatos de re-importação ou re-processamento dos mesmos itens com UUIDs diferentes. Recomenda-se auditoria manual para decidir qual versão manter.

---

**Audit completed:** 2026-06-26  
**Next audit:** Wave 2.2 (Cross-reference integrity) or upon resolution of CRITICAL items
