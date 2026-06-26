---
name: validate-corpus
description: Valida os schemas JSON do corpus ICONOCRACY e reporta erros, avisos e quantidade de registros válidos. Use quando o usuário pedir para validar o corpus ou checar integridade dos dados.
version: 1.0.0
author: Ana Vanzin + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [iconocracy, corpus, validation, json, schema]
    related_skills: [sync-corpus, iconocracy-agent]
---

# Validate Corpus

Valide o corpus a partir da raiz canônica do hub:
- `/Users/ana/Research/hub/iconocracy-corpus` (canonical)
- `~/iconocracy-corpus` apenas como compatibilidade (symlink), nunca como path preferencial

## Passos

1. Ir para a raiz canônica do hub.
2. Rodar:
   - `conda run -n iconocracy python tools/scripts/validate_schemas.py`
3. Se o usuário fornecer arquivos específicos, validar apenas esses:
   - `conda run -n iconocracy python tools/scripts/validate_schemas.py <arquivos>`
4. Reportar claramente:
   - erros com caminhos/arquivos
   - campos problemáticos, se disponíveis
   - avisos relevantes
   - contagem de registros válidos quando passar
5. Se `data/processed/records.jsonl` falhar mas `corpus/corpus-data.json` + `data/processed/corpus_dataset.csv` existirem, verificar se `tools/scripts/csv_to_records.py --dry-run` consegue regenerar o ledger e reportar isso como caminho de restauração antes de editar qualquer dado.

## Regras

- Não inventar sucesso: sempre basear o resultado na saída do script
- Se o ambiente `iconocracy` não estiver disponível, reportar isso explicitamente
- Se `validate_schemas.py` disser `jsonschema library required` apesar de `jsonschema` estar instalado, testar o import dentro do env:
  - `conda run -n iconocracy python -c "import jsonschema; from jsonschema import Draft202012Validator, FormatChecker, RefResolver; print('ok')"`
  - Se aparecer `ModuleNotFoundError: No module named 'rpds.rpds'`, o problema é dependência quebrada de `rpds-py`/`referencing` no env, não ausência real de schema; reportar como falha de ambiente antes de interpretar os dados.
  - Para auditoria read-only, pode rodar `python3 tools/scripts/validate_schemas.py ...` fora do conda apenas como comparação, deixando explícito que o gate canônico continua quebrado.
  - **Workaround conhecido:** Use o python direto do ambiente: `conda run -n iconocracy python tools/scripts/validate_schemas.py ...` ou `/Users/ana/.venvs/iconocracy/bin/python3.12 tools/scripts/validate_schemas.py ...` — veja `references/iconocracy-env-workaround.md`
- Se o problema for drift estrutural entre `records.jsonl` e `corpus-data.json`, sugerir `sync-corpus` ou restauração controlada do ledger antes de qualquer release
- **Validate against the canonical schema first.** In 2026-06-24, `master-record.schema.json` (governing the 280-record corpus) passed 280/280 while `codebook-v2.1.0.schema.json` (an orphan expansion schema) failed 0/280. Always identify which schema actually governs the current corpus before running validation, and report both results if multiple schemas exist.

## v2.3.0 conditional rules (warnings mode)

As of 2026-06-25, `tools/scripts/validate_schemas.py` was upgraded (commit `49caba3` on `main`) with 3 conditional rules that emit **warnings** (not errors) for records that touch patch v2.3.0 fields. The validator exposes these via the in-memory function `validate_records()` which returns `(valid, total, errors, warnings)` — the CLI surface (`main()`) still reports only errors. To inspect warnings during a validation run, import `validate_records` directly:

```python
from tools.scripts.validate_schemas import validate_records
import json

with open("data/processed/records.jsonl") as f:
    records = [json.loads(line) for line in f if line.strip()]

valid, total, errors, warnings = validate_records(records, "master-record")
print(f"{valid}/{total} valid, {len(warnings)} warnings")
for w in warnings:
    # w has keys: code, record_id, field, detail
    print(f"  [{w['code']}] {w['record_id']}: {w['field']} — {w['detail']}")
```

**Codes emitted** (defined in `tools/scripts/validate_schemas.py`):
- `JUSTIFICATIVA_CURTA` — `genero_atribuido=masculino` or `familia_alegorica=Masculino_Juridico` with `justificativa_genero` < 80 chars
- `REQUIRES_V23_FIELDS` — `familia_alegorica=Masculino_Juridico` without any of the 5 v2.3.0 patch fields populated
- `HERCULES_INCOERENTE` — `substituicao_atributiva_hercules` with `atributo_canonico_substituido == atributo_novo`

**Promotion to errors** is deferred to v2.4.0+ once data stabilizes (per `docs/decisions/2026-06-25-lacunas-v2.3.0.md`).

**Tests**: `tests/test_validate_schemas.py` (5/5 passing as of 2026-06-25) covers baseline preservation, each warning code, and the coherent-HERCULES negative case.

## Known gaps (v2.3.0 freeze plan)

The validator still does not cover (R-2026-06-25 in `2026-06-25-lacunas-v2.3.0.md`):
- `interseccao de arrays` for `substituicao_atributiva_hercules` (e.g., `Clava` must NOT appear in `objetos_regalia`); not modeled yet.
- `required-when-enum-match` *for all 5 v2.3.0 fields* — current rule warns if NONE are populated; strict mode requires at least one specific field per subtipo.

Both are scheduled for v2.4.0+.
