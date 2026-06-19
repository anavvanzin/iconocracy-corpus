# T4 → T3 Merge Pipeline

**Created:** 2026-04-28 (session trancada — continuar próxima)
**Status:** STAGING PRONTO · MERGE PENDENTE

## Estado atual

- DOCX re-parsed com sucesso: 15/15 fichas validadas
- Dedup: 1 MATCHES · 6 PARTIAL · 8 NEW
- Adjudicação concluída (2026-04-22, Council & Santa) — log reconstituído
- Staging: `data/staging/fichas-lpai-v2-parsed.jsonl` + vault drafts
- Log: `data/staging/t4-adjudication-log.json`

## Decisões (já tomadas)

### ENRICH (5) — merge em registros existentes
| Staged | → | Canônico | Nota |
|--------|---|----------|------|
| FR-SCOUT-001 | → | FR-005 | MATCHES. URL + title_exact. Rops. Merge campos LPAI. |
| BR-SCOUT-005 | → | BR-009 | Mesmo objeto (Ceschiatti). Título LPAI omite atribuição. |
| FR-SCOUT-002 | → | FR-008 | Mesmo objeto, état avec remarque. Enriquecer, não duplicar. |
| FR-SCOUT-005 | → | FR-009 | Mesma família (Buste de la République). Série fotográfica. |
| FR-SCOUT-006 | → | FR-038 | Mesmo objeto. Suprir URL Gallica + atribuição Janinet. |

### NEW (10) — promover como novos registros
BR-SCOUT-001 · BR-SCOUT-002 · BR-SCOUT-003 · BR-SCOUT-004 · BR-SCOUT-006 · BR-SCOUT-007
FR-SCOUT-003 · FR-SCOUT-004 · FR-SCOUT-007 · FR-SCOUT-008

## Passo 1: Merge ENRICH — enriquecer registros canônicos

Para cada um dos 5 ENRICH:
- Carregar o staged record do JSONL
- Carregar o canonical record do `records.jsonl` (buscar por ID)
- Merge: adicionar campos LPAI (`lpai_v2_code`, `classe`, `atributos`, `nota_analitica`), atualizar citação ABNT se a LPAI for mais completa, preencher URL se ausente no canônico
- Manter: `item_id`, `purificacao`, `iconocode.codes`, `iconocode.interpretation` originais
- Atualizar `updated_at`

Script helper: criar `tools/scripts/enrich_from_staging.py` ou fazer manualmente via Python no execute_code.

## Passo 2: Promote NEW — anexar ao ledger

```bash
cd /Users/ana/Research/hub/iconocracy-corpus

# Gate check
grep -l "placeholder_url_BLOCK_PROMOTE\|intra_batch_duplicate" \
  data/staging/fichas-lpai-v2-parsed.jsonl \
  && echo "STOP" && exit 1

# Extrair apenas os 10 NEW do JSONL e anexar
# (filtrar por staged_id na lista NEW, remover ENRICH e MATCHES)
python -c "
import json
new_ids = {'BR-SCOUT-001','BR-SCOUT-002','BR-SCOUT-003','BR-SCOUT-004','BR-SCOUT-006','BR-SCOUT-007',
           'FR-SCOUT-003','FR-SCOUT-004','FR-SCOUT-007','FR-SCOUT-008'}
with open('data/staging/fichas-lpai-v2-parsed.jsonl') as f:
    for line in f:
        rec = json.loads(line)
        # Identify staged_id — check exports.audit_flags or input.title_hint
        # (need to confirm how staged_id is embedded in the records)
        # Append to records.jsonl
"

# Copiar vault drafts
cp data/staging/vault-drafts-lpai-v2/BR-SCOUT-001*.md vault/candidatos/
# ... repeat for all 10 NEW ...
```

## Passo 3: Validação

```bash
conda run -n iconocracy env -u PYTHONPATH python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
conda run -n iconocracy env -u PYTHONPATH python tools/scripts/records_to_corpus.py --diff
# Se diff limpo:
conda run -n iconocracy env -u PYTHONPATH python tools/scripts/records_to_corpus.py
```

## Passo 4: Recalcular T3 coding queue

```bash
conda run -n iconocracy env -u PYTHONPATH python tools/scripts/code_purification.py --status
```

Esperado: ~29 itens pendentes (19 anteriores + 10 novos).

## Passo 5: Verificar acesso a imagens

```bash
ls /Volumes/ICONOCRACIA/ 2>&1
```

Se não montado, montar SSD ou usar Google Drive.

## Passo 6: Iniciar T3 IconoCode

Para cada item na fila:
- Carregar imagem (local ou URL)
- Panofsky 3 níveis (pré-iconográfico · iconográfico · iconológico)
- 10 indicadores ENDURECIMENTO (0–3)
- Classificação de regime (fundacional · normativo · militar · contra-alegoria)
- Escrever via `code_purification.py --item <ID>`

Usar `iconocode-batch` skill para processamento em lote.

---

## Arquivos relevantes

| Path | Estado |
|------|--------|
| `data/staging/fichas-lpai-v2-parsed.jsonl` | ✅ Re-parsed, 15 records |
| `data/staging/vault-drafts-lpai-v2/` | ✅ 15 draft .md |
| `data/staging/t4-adjudication-log.json` | ✅ Reconstituído |
| `data/processed/records.jsonl` | ⏳ 165 itens (aguardando merge) |
| `corpus/corpus-data.json` | ⏳ Precisa rebuild após merge |
| `docs/T4-LPAI-INGEST-REPORT.md` | ✅ Decisões em §5.a |
| `docs/T3-coding-queue.md` | ⏳ 19 itens (crescerá p/ ~29) |
