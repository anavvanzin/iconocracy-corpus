# Auditoria — Estratificação do Corpus por Instrumento de Codificação (`coded_by`)

**Gerado:** 2026-06-10 · **Fonte:** `corpus/corpus-data.json` (N=264) · **Método:** geração automática a partir dos dados (não-transcrito)

**Contexto:** material de decisão para `DIALETICA-N165-vs-265.md`. Produzido por auditoria de 3 agentes paralelos (estratificação, proveniência, protocolo inter-instrumento) — verificado contra os dados aqui.


---

## 0. Achados-chave (verificados nos dados)

1. **Conjunto não-codificado == conjunto sem regime:** CONFIRMADO (os 41 itens sem `coded_by` são exatamente os sem `regime`).
2. **`vault-import` é inerte:** 58/58 itens têm os 10 indicadores = 0 (variância zero). Não é codificação Panofsky — é preenchimento-padrão. Tratar como quase-não-codificado.
3. **`migration` sem score:** 19/19 itens têm `endurecimento_score = null` (só regime heurístico atribuído).
4. **Nenhum item IconoCode pontua 0:** 0/145 itens `iconocode-*` têm score 0. ⟹ **`endurecimento_score=0` NÃO é, nos dados atuais, um 'score válido de baixa purificação'** — todo 0 observado é placeholder (uncoded) ou preenchimento (vault-import). **Contradiz a nota de terminologia em CLAUDE.md** e deve ser corrigido antes de qualquer análise que trate zeros como dados.
5. **Decomposição dos 99 zeros:** vault-import=58, (ausente)=41.
6. **Decomposição dos 19 nulls:** migration=19.

## (a) Crosstab `coded_by` × `regime`

| coded_by | (ausente) | fundacional | normativo | militar | contra-alegoria | TOTAL |
|---|---|---|---|---|---|---|
| iconocode-opus | 0 | 58 | 29 | 13 | 0 | **100** |
| iconocode-opus-4.6-metadata-refined | 0 | 11 | 5 | 7 | 6 | **29** |
| iconocode-opus-4.6-image | 0 | 2 | 6 | 7 | 1 | **16** |
| vault-import | 0 | 28 | 26 | 3 | 1 | **58** |
| migration | 0 | 6 | 9 | 4 | 0 | **19** |
| manual-entry | 0 | 0 | 1 | 0 | 0 | **1** |
| (ausente) | 41 | 0 | 0 | 0 | 0 | **41** |

## (b) Indicadores completos & score por estrato

| estrato | N | 10 indicadores | score presente | score=0 | score=null | all-zero (inerte) |
|---|---|---|---|---|---|---|
| iconocode-opus | 100 | 100 | 100 | 0 | 0 | 0 |
| iconocode-opus-4.6-metadata-refined | 29 | 29 | 29 | 0 | 0 | 0 |
| iconocode-opus-4.6-image | 16 | 16 | 16 | 0 | 0 | 0 |
| vault-import | 58 | 58 | 58 | 58 | 0 | 58 |
| migration | 19 | 19 | 0 | 0 | 19 | 19 |
| manual-entry | 1 | 1 | 1 | 0 | 0 | 0 |
| (ausente) | 41 | 0 | 41 | 41 | 0 | 0 |

## (c) N analíticos reais (não 165 vs 265)

- **N=145** — IconoCode puro (opus + opus-4.6). **Mais defensável.** Pré-requisito: confiabilidade inter-instrumento (ver `IRR-INTER-INSTRUMENTO-2026-06-10.md`).
- **N=146** — IconoCode + manual-entry genuíno (FR-048, único não-IconoCode com codificação real de 10 indicadores).
- **N≈165** — + `migration` (19) SE re-codificados (hoje têm score null).
- **N≈223** ('estrato moderado') — **NÃO defensável como está**: inclui os 58 `vault-import` inertes (all-zero placeholder).
- **N=264** — **inválido** (inclui 41 não-codificados).

## (d) Estrato 0 — os não-codificados (quarentena)

41 itens — sem `coded_by`, sem `regime`, indicadores vazios, score=0 placeholder:

```
BR-021, BR-023, BR-027, BR-041, BR-044, BR-045, FR-049, FR-050, FR-054, FR-055, FR-056, FR-057, FR-058, FR-059, FR-060, FR-061, FR-062, FR-063, FR-064, FR-065, FR-066, FR-067, FR-072, FR-076, FR-078, FR-079, FR-080, FR-083, FR-086, FR-088, FR-096, UK-011, UK-012, UK-013, UK-014, UK-015, UK-016, UK-017, US-022, US-023, US-024
```

## (e) Listas para re-codificação

**vault-import (58)** — veredito: RE-CODIFICAR (notas de vault têm só rótulo qualitativo, nunca os 10 scores 0–3):

```
BE-003, BE-004, BR-017, BR-018, BR-019, BR-020, BR-022, BR-024, BR-025, BR-026, BR-028, BR-029, BR-030, BR-031, BR-032, BR-033, BR-034, BR-035, BR-036, BR-037, BR-038, BR-039, BR-040, BR-042, BR-043, BR-046, DE-016, DE-017, DE-018, DE-019, DE-020, DE-021, FR-051, FR-052, FR-053, FR-068, FR-069, FR-070, FR-071, FR-073, FR-074, FR-075, FR-077, FR-081, FR-082, FR-084, FR-085, FR-087, FR-089, FR-090, FR-091, FR-092, FR-093, FR-094, FR-095, UK-018, US-021, US-025
```

**migration (19)** — veredito: RE-CODIFICAR (score null, regime heurístico):

```
BE-5F-LEOPOLD-1832, BE-CONGO-100F-1912, BE-CONGO-MON-1921, BR-1000R-1906, BR-1CR-1970, BR-50CR-1965, DE-1000M-1910, DE-100M-1908, DE-50M-1919, FR-ASSIGNAT-1792, FR-CERES-5F-1849, UK-FLORIN-1902, UK-HALFPENNY-1695, UK-PENNY-1895, UK-PENNY-1912, US-BANNER-1861, US-EDUC-1896-01, US-NAST-1864, US-SEATED-1840
```

## (f) Auditoria dos notebooks (contaminação de zeros)

**Fonte dos notebooks:** `data/processed/corpus_dataset.csv` — **165 linhas** (snapshot congelado), NÃO os 264.

**Estado atual: NÃO contaminado.** O CSV de 165 tem **0 linhas all-zero** (verificado). `coded_by` no CSV: iconocode-opus 106, opus-4.6-metadata-refined 29, opus-4.6-image 10, vazio 20. Os notebooks usam `df.dropna(subset=INDICATORS)`, que remove os 41 uncoded (indicadores null) — porém **NÃO removeria** os 58 vault-import (indicadores = 0, não null) se eles estivessem no CSV.

**Risco latente (ação requerida):** o hook PostToolUse regenera `corpus_dataset.csv` via `code_purification.py --export-csv` a cada edição de `corpus-data.json`. Regenerar a partir dos 264 importaria os 58 zero-vectors de vault-import + os 19 migration (score null) → contaminaria todos os notebooks. **Correção:** `code_purification.py --export-csv` deve filtrar por `coded_by` válido (excluir uncoded + vault-import all-zero) antes de exportar. Nenhum notebook filtra por `coded_by` — eles dependem do CSV já vir limpo.
