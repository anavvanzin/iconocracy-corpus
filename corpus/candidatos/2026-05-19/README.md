# ICONOCRACIA — Pacote da execução do pipeline (2026-05-19)

## Artefatos principais (prontos para uso)
- `candidatos-2026-05-19.json` — 43 candidatos validados, schema enriched, prontos para merge
- `research-2026-05-19.md` — runbook YAML por sub-questão com estatísticas

## Saídas por sub-questão
- `sq1_candidates.json` + `sq1_log.md` — SQ1 (8 itens, alegorias séc. XIX fora de Gallica)
- `sq2_candidates.json` + `sq2_log.md` — SQ2 (15 itens, iconografia jurídica latino-americana)
- `sq3_candidates.json` + `sq3_log.md` — SQ3 (10 itens, museus europeus com IIIF)
- `sq4_candidates.json` + `sq4_log.md` — SQ4 (10 itens, tratados de iconologia)

## Infraestrutura
- `SHARED_SPEC.md` — especificação compartilhada (schema-alvo, regras de filtragem, códigos ICONCLASS)
- `dedup_urls.txt` — 368 URLs canônicas do corpus existente, usadas para deduplicação
- `stats.json` — estatísticas agregadas da execução
- `validate.py` — script de validação + consolidação + dedup + normalização ICONCLASS
- `render_md.py` — script gerador do markdown runbook

## Como reproduzir
```bash
python3 validate.py    # consolida sqN_candidates.json em candidatos-YYYY-MM-DD.json
python3 render_md.py   # gera research-YYYY-MM-DD.md a partir do JSON consolidado
```
