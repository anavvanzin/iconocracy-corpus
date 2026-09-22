# Wave 2.2 — Schema Audit Report

**Date:** 2026-06-26  
**Auditor:** Hermes Agent (subagent)  
**Repository:** `/Users/ana/Research/hub/iconocracy-corpus`  
**Data snapshot:** 299 records in `records.jsonl`, 236 records in `purification.jsonl`

---

## 1. JSON Schema Draft Identification

| Schema File | `$schema` URI | Draft |
|---|---|---|
| `tools/schemas/master-record.schema.json` | `https://json-schema.org/draft/2020-12/schema` | **Draft 2020-12** |
| `tools/schemas/iconocode-output.schema.json` | `https://json-schema.org/draft/2020-12/schema` | **Draft 2020-12** |
| `tools/schemas/webscout-input.schema.json` | `https://json-schema.org/draft/2020-12/schema` | **Draft 2020-12** |
| `tools/schemas/webscout-output.schema.json` | `https://json-schema.org/draft/2020-12/schema` | **Draft 2020-12** |
| `tools/schemas/purification-record.schema.json` | `https://json-schema.org/draft/2020-12/schema` | **Draft 2020-12** |

**Finding:** All 5 schemas use Draft 2020-12. No version inconsistency. ✅

---

## 2. Validation Results — `validate_schemas.py`

### 2.1 Execution Output

```
$ python tools/scripts/validate_schemas.py --verbose
Validating data/processed/records.jsonl against master-record schema...
Results: 299/299 records valid
✓ All records valid
```

```
$ python tools/scripts/validate_schemas.py data/processed/purification.jsonl --schema purification-record --verbose
Validating data/processed/purification.jsonl against purification-record schema...
Results: 236/236 records valid
✓ All records valid
```

### 2.2 Deprecation Warning

```
DeprecationWarning: jsonschema.RefResolver is deprecated as of v4.18.0,
in favor of the https://github.com/python-jsonschema/referencing library
```

**Severity:** Low. The validator still works, but `RefResolver` should be migrated to `referencing` before the `jsonschema` library drops the deprecated API. No functional impact yet.

---

## 3. Cross-Reference: Schema Fields vs. Actual records.jsonl Fields

### 3.1 Top-Level Keys — PERFECT MATCH ✅

| Schema Required | In Records? | Notes |
|---|---|---|
| `master_record_version` | ✅ `str` | Always `"1.0"` |
| `batch_id` | ✅ `str` | UUID or pattern |
| `item_id` | ✅ `str` | UUID format |
| `item_hash` | ✅ `str` | SHA-256, minLength=16 |
| `input` | ✅ `dict` | url, title_hint, date_hint, place_hint |
| `webscout` | ✅ `dict` | `$ref: webscout-output` |
| `iconocode` | ✅ `dict` | `$ref: iconocode-output` |
| `exports` | ✅ `dict` | abnt_citations, audit_flags |
| `timestamps` | ✅ `dict` | created_at, updated_at |
| `purificacao` | ✅ `dict` | Additional fields (see §3.2) |

**No top-level drift.** All 299 records contain exactly the 10 keys required by the schema. `additionalProperties: false` enforced at this level.

### 3.2 `purificacao` Sub-keys — SIGNIFICANT DRIFT ⚠️

The `purificacao` object has `additionalProperties: true`, allowing undocumented fields to pass validation. This masks real schema drift.

#### 3.2.1 Fields in RECORDS but NOT in Schema (UNDOCUMENTED DRIFT)

| Field | Type | Records | Description |
|---|---|---|---|
| `analytic_eligible` | `bool` | 19 | Eligibility flag for analytic samples |
| `cohort` | `str` | 19 | Experiment cohort identifier (e.g., `e1-opus48-2026-06`) |
| `period_extended` | `bool` | 19 | Extended period classification |
| `record_metadata` | `dict` | 15 | Rich metadata block (title, date, creator, institution, country, medium, motif[], description, url, thumbnail_url, rights, citation_abnt, tags[], regime, endurecimento_score, coded_at, nota_metodologica) |
| `funcao_liturgica_vs_estatal` | `str` | 1 | Liturgical vs. state function classification |
| `hipotese_racial_interpretacao` | `str` | 1 | Racial hypothesis — interpretation layer |
| `hipotese_racial_observavel` | `str` | 1 | Racial hypothesis — observable layer |
| `n_figuras_no_item` | `int` | 1 | Number of figures in the item |
| `posicao_arquitetonica` | `str` | 1 | Architectural position |
| `programa_iconografico` | `bool` | 1 | Iconographic program flag |
| `status_evidencia` | `str` | 1 | Evidence status |
| `tipo_virtude` | `str` | 1 | Virtue type classification |

**Total: 12 undocumented fields** ranging from widely used (`record_metadata`: 15 records) to singleton experimental fields.

#### 3.2.2 Fields in SCHEMA but ABSENT from All Records (UNPOPULATED)

These schema fields exist in `master-record.schema.json` under `purificacao.properties` but are NOT present (or only present as null/empty) in any of the 299 records:

| Field | Schema Type | Description |
|---|---|---|
| `prompt_version` | `str` | Coding prompt/codebook version — **0 records** have this key |
| `programa_id` | `str\|null` | v2.2.0 grouping identifier — **0 populated** |
| `ordem_no_programa` | `int\|null` | v2.2.0 ordinal position — **0 populated** |
| `dado_negativo` | `bool` | v2.2.0 absence marker — **0 populated** |
| `finalidade_atribuida` | `str` (enum) | v2.2.0 attributed purpose — **0 populated** |
| `disjuncao_representa_governa` | `bool` | v2.2.0 representation/governance disjunction — **0 populated** |
| `objetos_regalia` | `array[str]` | v2.2.0 objects/regalia — **0 populated** |
| `marcas_corporais` | `array[str]` | v2.2.0 body markers — **0 populated** |
| `marcadores_cena_arquitetura` | `array[str]` | v2.2.0 scene/architecture markers — **0 populated** |
| `relacao_com_repertorio_indigena` | `str` (enum) | v2.2.0 Indigenous repertoire relation — **0 populated** |
| `funcao_da_figura_masculina` | `str` (enum) | v2.3.0 optional patch — **0 populated** |
| `tipo_agencia_masculina` | `str` (enum) | v2.3.0 optional patch — **0 populated** |
| `funcao_atlanteana` | `bool` | v2.3.0 optional patch — **0 populated** |
| `tipo_efluencia_hidrica` | `str` (enum) | v2.3.0 optional patch — **0 populated** |
| `substituicao_atributiva_hercules` | `object` | v2.3.0 optional patch — **0 populated** |

**Total: 15 schema-defined fields with zero population.** These are forward-declared for v2.2.0/v2.3.0 but no data has been backfilled.

#### 3.2.3 The `justificativa_genero` Phantom Field 🔴

The validation script `validate_schemas.py` (`_check_v23_warnings`) references `purificacao.justificativa_genero` as part of the JUSTIFICATIVA_CURTA warning rule (line 188), requiring ≥80 characters when `genero=masculino` or `familia=Masculino_Juridico`.

However:
- **`justificativa_genero` is NOT defined** in `master-record.schema.json`
- **`justificativa_genero` does NOT exist** in any of the 299 records (0 records have this key)
- The validation code checks `purificacao.get("justificativa_genero") or ""`, which silently returns `""` for all records, making the warning **always fire** for every masculine-coded record

**Impact:** The JUSTIFICATIVA_CURTA rule is a dead letter — it produces warnings for every masculine record but cannot be satisfied because the field it checks doesn't exist in the schema or data.

---

## 4. Sub-schema Consistency Analysis

### 4.1 `webscout-output.schema.json` ↔ Records

| Schema Field | In Records? | Match? |
|---|---|---|
| `search_results` (array) | ✅ | Each item has evidence_id, source_type, title, url, abnt_citation |
| `summary_evidence` (str) | ✅ | |
| `gaps` (array) | ✅ | |
| `iconclass_candidates` (optional) | ✅ | Sometimes populated |
| `notes` (optional) | ✅ | |
| `score` (optional) | ✅ | |

**No drift.** All 299 records have `webscout` objects that conform. ✅

### 4.2 `iconocode-output.schema.json` ↔ Records

| Schema Field | In Records? | Match? |
|---|---|---|
| `pre_iconographic` (array) | ✅ | motif, observed[, notes] |
| `codes` (array) | ✅ | scheme, notation, label, code_role, confidence[, evidence_source_id] |
| `interpretation` (array) | ✅ | claim_text, claim_type, status, confidence |
| `validation` (object) | ✅ | claim_ledger array |
| `confidence` (number) | ✅ | |

**No drift.** All 299 records have `iconocode` objects that conform. ✅

### 4.3 Cross-Schema Reference Integrity

| Parent Schema | `$ref` Target | Resolves? |
|---|---|---|
| `master-record` → `webscout` | `webscout-output.schema.json` (by `$id`) | ✅ Resolved by `RefResolver` |
| `master-record` → `iconocode` | `iconocode-output.schema.json` (by `$id`) | ✅ Resolved by `RefResolver` |

`webscout-input.schema.json` is NOT referenced by any other schema — it's a standalone input specification for the webscout agent. This is correct; it should not be referenced by the output schemas.

### 4.4 `purification-record.schema.json` ↔ purification.jsonl

| Aspect | Finding |
|---|---|
| Schema draft | Draft 2020-12 ✅ |
| Validation | 236/236 valid ✅ |
| Required fields | All 15 required fields present |
| Field types | All match: 10 indicators (int 0-3), purificacao_composto (float 0-3), regime_iconocratico (enum), coded_by, coded_at |
| Optional fields | confidence_score, prompt_version, coding_round, adjudication_status, notes, country, medium_norm, period, title, year |

**No drift** between purification-record schema and purification.jsonl. ✅

---

## 5. Summary of Findings

### 5.1 Critical Issues 🔴

| # | Issue | Severity | Recommendation |
|---|---|---|---|
| 1 | `justificativa_genero` referenced by validator but undefined in any schema AND absent from all data | **High** | Either (a) add `justificativa_genero` to `master-record.schema.json` and populate it, or (b) remove the JUSTIFICATIVA_CURTA rule from validate_schemas.py until the field exists |
| 2 | 12 undocumented fields in `purificacao` (data has fields not in schema) | **Medium** | Add these fields to the schema or remove them from data; `additionalProperties: true` is masking the drift |

### 5.2 Warnings ⚠️

| # | Issue | Severity | Recommendation |
|---|---|---|---|
| 3 | 15 schema-defined fields with zero population (v2.2.0/v2.3.0 forward-declared) | **Low** | Acceptable for forward-compatible schemas, but schedule backfill or deprecation timeline |
| 4 | `prompt_version` field defined in schema but present in 0 records | **Low** | Either populate or remove from required/non-optional definitions |
| 5 | `RefResolver` deprecation warning | **Low** | Migrate to `referencing` library before `jsonschema` removes the API |

### 5.3 Clean Findings ✅

| # | Item | Status |
|---|---|---|
| 1 | All 5 schemas use Draft 2020-12 consistently | ✅ |
| 2 | Top-level keys: perfect match between schema and all 299 records | ✅ |
| 3 | `additionalProperties: false` enforced at top level — no unexpected keys leak | ✅ |
| 4 | `webscout-output` sub-schema: zero drift | ✅ |
| 5 | `iconocode-output` sub-schema: zero drift | ✅ |
| 6 | `webscout-input` schema: correctly standalone | ✅ |
| 7 | `purification-record` ↔ `purification.jsonl`: zero drift, 236/236 valid | ✅ |
| 8 | Cross-schema `$ref` references resolve correctly | ✅ |
| 9 | 299/299 master records pass validation | ✅ |

---

## 6. Remediation Plan

### Immediate (Pre-Release Gate)
1. **Resolve `justificativa_genero`**: Either add to schema + data or disable the JUSTIFICATIVA_CURTA rule.
2. **Document the 12 drift fields**: Add `analytic_eligible`, `cohort`, `period_extended`, `record_metadata`, `funcao_liturgica_vs_estatal`, `hipotese_racial_interpretacao`, `hipotese_racial_observavel`, `n_figuras_no_item`, `posicao_arquitetonica`, `programa_iconografico`, `status_evidencia`, `tipo_virtude` to `master-record.schema.json` with proper types and descriptions.

### Medium-Term (v2.4.0)
3. Populate or deprecate the 15 unused forward-declared fields.
4. Migrate `RefResolver` → `referencing` library.
5. Consider tightening `purificacao` to `additionalProperties: false` once all drift fields are captured in the schema.

---

## Appendix: Record Count by Data Layer

| Layer | Records | Validated | Schema |
|---|---|---|---|
| `records.jsonl` | 299 | 299/299 ✅ | `master-record` |
| `purification.jsonl` | 236 | 236/236 ✅ | `purification-record` |
| `corpus/corpus-data.json` | 280 | (export only) | N/A |
| `vault/candidatos/` | 314 | N/A (markdown) | N/A |
