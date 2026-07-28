# Relatório de gaps de migração — iconocracy-corpus → Mnemosyne Viva v0.2

**Data:** 2026-07-28  
**Fontes inspecionadas:**
- `data/processed/corpus_dataset.csv` (CSV mestre com campos descritivos + 10 indicadores)
- `corpus/corpus-data.json` (export JSON com 280 registros, scores crus)
- `corpus/corpus-data-enriched.json` (export público com 95 registros)
- `data/processed/records.jsonl` (ledger com 299 registros)

**Atenção:** o checkout local (`iconocracy-editorial-wt`) está atrás de `origin/main`. Antes de congelar o pipeline, executar `git pull` e reconciliar com a contagem canônica (308–309 registros).

## Gaps por campo canônico

| Campo Mnemosyne | Presente na fonte? | Onde encontrado | Onde falta | Ação |
|---|---|---|---|---|
| `id` (sigla) | Sim | `corpus_dataset.csv:id`, `corpus-data.json:id` | — | Usar diretamente |
| `uuid` | Não | — | Todos os exports | Adicionar do ledger de pesquisa |
| `slug` | Não | — | Todos | Gerar de `id`/`title` |
| `legacy_ids` | Parcial | `records.jsonl:item_id` | CSV/JSON principais | Coletar ids históricos |
| `title` | Sim | CSV/JSON | — | Usar diretamente |
| `creator` | Sim | CSV | `corpus-data.json` (faltando) | Promover do CSV |
| `date` | Sim | CSV/JSON | — | Usar diretamente |
| `year` | Sim | CSV | JSONs | Promover do CSV |
| `period` / `period_norm` | Sim | CSV | JSONs | Promover do CSV |
| `country` | Sim | CSV/JSON | — | Usar diretamente |
| `country_pt` | Sim | CSV | JSONs | Promover do CSV |
| `country_code` | Não | — | Todos | Derivar de `country` (ex.: UK → GB) |
| `region` | Não | — | Todos | Adicionar campo no Airtable/export |
| `medium` / `medium_norm` | Sim | CSV/JSON | — | Usar; mapear `support` para `medium_norm` |
| `motif` / `motif_str` | Sim | CSV/JSON | — | Usar diretamente |
| `tags` / `tags_str` | Sim | CSV | JSONs | Promover do CSV |
| `description` | Sim | CSV/JSON | — | Usar diretamente |
| `url` | Sim | CSV/JSON | — | Usar diretamente |
| `source_archive` | Sim | CSV/JSON | — | Usar diretamente |
| `institution` | Parcial | CSV `source_archive` contém instituição | Campo separado não existe | Separar/fontes e arquivos |
| `rights` | Não | — | Todos | Adicionar por item |
| `citation_abnt` | Sim | CSV/JSON | — | Usar diretamente |
| `citation_chicago` | Não | — | Todos | Gerar/adicional |
| `external_identifiers` | Não | — | Todos | Adicionar ARK/accession/DOI quando disponível |
| `thumbnail_url` | Sim | CSV/JSON | — | Usar diretamente |
| `url_image_download` | Não | — | Todos | Adicionar quando disponível |
| `url_iiif` | Não | — | Todos | Adicionar IIIF quando disponível |
| `iiif_source` / `iiif_note` | Não | — | Todos | Adicionar |
| `local_image_path` | Não | — | Todos | Adicionar path local quando relevante |
| `image_sha256` | Não | — | Todos | Calcular quando possível |
| `image_protocol` | Não | — | Todos | Derivar da análise de URLs |
| `regime` | Sim | JSON/CSV `regime_iconocratico` | — | Normalizar aliases |
| `regime_justificativa` | Não | — | Todos | Adicionar justificativa |
| `iconographic_metadata.allegorical_figure` | Não | — | Todos | Mapear de `motif` quando possível |
| `iconographic_metadata.attributes` | Não | — | Todos | Adicionar campo no Airtable/export |
| `iconographic_metadata.endurecimento_score` | Parcial | `corpus-data.json:endurecimento_score` (0–3 cru) | `corpus-data-enriched.json` | Normalizar para 0..1 |
| `iconographic_metadata.purification_indicators` | Não | — | Todos | Derivar de `coding_metadata.purification_scores` |
| `coding_metadata.purification_scores` | Sim | CSV (10 colunas), `corpus-data.json:indicadores` | — | Preservar crus |
| `coding_metadata.indicator_scale` | Não | — | Todos | Documentar escala mista (7×0–3, 3×0–4) |
| `coding_metadata.coded_by` / `coded_at` | Sim | CSV/JSON | — | Usar diretamente |
| `coding_metadata.codebook_version` | Não | — | Todos | Adicionar versão do codebook |
| `coding_metadata.coding_confidence` | Não | — | Todos | Adicionar se usado |
| `coding_metadata.uncertainty_note` | Parcial | CSV `scope_note`, `notes` | JSONs | Consolidar notas |
| `coding_metadata.adjudication_status` / `adjudication_log` | Não | — | Todos | Adicionar quando houver adjudicação |

## Decisões pendentes

1. **Normalização do `endurecimento_score`:** o export atual usa média crua dos dez indicadores (0–3.1). Como a escala é mista (máximo teórico 3.3), a regra do documento "dividir por 3 ou por 4" não se aplica diretamente. Opções:
   - (A) `score_public = raw / 3.3` (máximo teórico misto)
   - (B) `score_public = raw / observed_max` (máximo observado no dataset)
   - (C) Normalizar cada indicador individualmente para 0..1 e recalcular a média
   - Recomendação preliminar: (A) preserva a interpretação metodológica e é reprodutível.

2. **Atualização do checkout:** o repositório local está atrás de `origin/main`. Antes de produzir o export canônico, fazer `git pull` e validar a contagem (308–309 registros).

3. **`vault_note`:** não encontrado nos exports inspecionados. Se existir no corpus privado, mapear para `coding_metadata.uncertainty_note` ou criar `provenance_note`.

## Próximos passos

1. Reconciliar `iconocracy-editorial-wt` com `origin/main`.
2. Implementar script `scripts/export_to_mnemosyne.py` que leia `data/processed/corpus_dataset.csv` + `corpus/corpus-data.json` e produza `corpus-data-enriched.json` v0.2.
3. Validar o export de 280+ registros contra `schemas/corpus-data-enriched.schema.json` v0.2.
4. Produzir dataset card v0.1 documentando a escala mista e a regra de normalização escolhida.
