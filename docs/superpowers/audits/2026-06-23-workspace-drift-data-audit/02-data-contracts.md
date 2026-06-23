# Audit Report — contratos de dados / schemas / contagens — lente de auditoria Wave 1.2
Escopo examinado: `/Users/ana/Research/hub/iconocracy-corpus/data/processed/`; `/Users/ana/Research/hub/iconocracy-corpus/corpus/corpus-data.json`; `/Users/ana/Research/hub/iconocracy-corpus/schema/`; `/Users/ana/Research/hub/iconocracy-corpus/schemas/`; `/Users/ana/Research/hub/iconocracy-corpus/tools/schemas/`; `/Users/ana/Research/hub/iconocracy-corpus/tools/scripts/validate_schemas.py`; `/Users/ana/Research/hub/iconocracy-corpus/tools/scripts/records_to_corpus.py`; inspeção mínima de CI em `.github/workflows/validate.yml` para lacunas de validação.
Arquivos analisados: 22
Data: 2026-06-23

## Resumo executivo (≤5 linhas)

As contagens atuais são 280 `records`, 280 itens no export público, 236 linhas de `purification` e 265 linhas de `pathosformel`; `regimes_visuais.yaml` não existe no escopo auditado.
O contrato correto de join é: `pathosformel_index.item_id` ↔ `records.item_id`; `pathosformel_index.sigla_id` ↔ `corpus-data.id`; `pathosformel_index.url` ↔ `corpus-data.url` como apoio, não chave primária.
Há drift de contratos: `corpus-data.json`, `pathosformel_index.jsonl` e `id-mapping.json` são consumidos por múltiplos scripts sem schema explícito próprio.
O CI valida `records` e `purification`, mas não valida schema de corpus/pathos/id-map nem a presença/contrato de `regimes_visuais.yaml`.
A validação local não pôde rodar porque o ambiente atual não tem `jsonschema`, embora `requirements.txt` declare a dependência.

## Achados — CRITICAL (bloqueante)
- Nenhum achado bloqueante confirmado em modo read-only; os problemas abaixo são MAJOR porque afetam rastreabilidade/contrato, mas não impedem a leitura dos dados atuais.

## Achados — MAJOR
- [M-01] `regimes_visuais.yaml` ausente no escopo auditado · `data/processed/regimes_visuais.yaml:0` · O arquivo esperado não existe em `/data/processed/`; busca direcionada por `regimes_visuais` encontrou apenas menção no plano de auditoria, e nenhum consumidor em `tools/scripts`. Portanto não foi possível inferir schema, contagem, nem decidir se seria derivado ou canônico. · Remediação: decidir explicitamente se `regimes_visuais.yaml` deve existir; se sim, recriá-lo via pipeline declarada, adicionar schema e teste de presença; se não, remover referências documentais que dizem que ele existe.
- [M-02] `pathosformel_index.jsonl` tem contrato implícito e sem schema explícito · `tools/scripts/e1_mark_no_image.py:84` · O schema implícito das entradas contém `item_id`, `sigla_id`, metadados bibliográficos, flags de codificação e 10 indicadores; ele é codificado diretamente em scripts, não em `tools/schemas`. `validate_schemas.py` só oferece `master-record`, `purification-record`, `argos-manifest`, `webscout-*` e `iconocode-output` (`tools/scripts/validate_schemas.py:195`) e inferiria `master-record` para qualquer JSONL não-`purification` (`tools/scripts/validate_schemas.py:213`). · Remediação: criar `tools/schemas/pathosformel-index.schema.json`, adicionar opção `--schema pathosformel-index` e validar no CI.
- [M-03] `pathosformel_index.jsonl` está incompleto frente ao corpus atual e tem três `sigla_id` órfãos · `data/processed/pathosformel_index.jsonl:22` · Contagem medida: 265 linhas contra 280 `records`; todos os 265 `item_id` existem em `records`, mas só 259 `sigla_id` batem com `corpus-data.id`. Órfãos: linha 22 `BR-016` (corresponde hoje a `SCOUT-559`), linha 84 `DE-NOTG-1921` (corresponde hoje a `SCOUT-558`) e linha 136 `FR-040` (corresponde hoje a `SCOUT-337`). · Remediação: normalizar `sigla_id` pelo contrato atual `corpus-data.id` ou registrar alias formal; acrescentar teste de integridade `pathos.sigla_id ⊆ corpus.id`.
- [M-04] `corpus-data.json` é superfície pública multi-consumida sem schema próprio · `tools/scripts/records_to_corpus.py:118` · O export é montado por função ad hoc e preserva campos ricos por merge; o contrato real observado tem 15 campos (`id`, `country`, `url`, `title`, `description`, `motif`, `regime`, `endurecimento_score`, `coded_by`, `coded_at`, `date`, `indicadores`, `citation_abnt`, `audit_flags`, `support`). Busca direcionada encontrou 25 scripts citando `corpus-data.json`, mas nenhum `corpus-data.schema.json`. · Remediação: criar schema para o export público, validar em CI e tornar `records_to_corpus.py --diff`/idempotência dependentes também de schema, não só de contagem.
- [M-05] `id-mapping.json` tem cabeçalho stale apesar de mapear 280 entradas · `data/processed/id-mapping.json:4` · O arquivo declara `total_records: 277`, `total_corpus: 264`, `matched: 257`, mas a contagem real é 280 `records`, 280 corpus e `mapping_len=280`. Como `records_to_corpus.py` prioriza este mapeamento (`tools/scripts/records_to_corpus.py:240`) antes de UUID5/URL, metadados stale podem induzir auditorias e scripts auxiliares a conclusões erradas. · Remediação: recomputar cabeçalho a partir do array `mapping` e validar `declared == actual` em CI.
- [M-06] Escalas de indicadores divergem entre codebook LPAI v2.1 e schemas operacionais · `schemas/codebook-v2.1.0.schema.json:94` · O schema LPAI v2.1 define `indicador_ordinal_0_4` com máximo 4, enquanto `master-record` e `purification-record` validam os 10 indicadores em escala 0–3 (`tools/schemas/master-record.schema.json:86`, `tools/schemas/purification-record.schema.json:30`). · Remediação: congelar uma escala canônica ou versionar conversão explícita; bloquear mistura silenciosa de 0–4 com 0–3.

## Achados — MINOR
- [m-01] Front matter do codebook v2.0.0 aponta para companheiros inexistentes no diretório `schema/` · `schema/codebook-v2.0.0.md:9` · O documento lista `schema/codebook-v2.0.0.yaml` e `schema/codebook-v2.0.0.schema.json`, mas no escopo há apenas `schema/*.md` e o schema de máquina atual está em `schemas/codebook-v2.1.0.schema.json`. · Remediação: atualizar referências ou arquivar explicitamente a versão 2.0.0 como documento histórico.
- [m-02] Validação local está dependente de ambiente, não hermética · `tools/scripts/validate_schemas.py:14` · As duas validações read-only executadas falharam com `Error: jsonschema library required. Install with: pip install jsonschema`; `requirements.txt:1` declara `jsonschema>=4.23,<5`, e o CI instala requirements, mas o workspace local atual não garante o comando. · Remediação: documentar execução via venv/uv e/ou usar `python -m pip install -r requirements.txt` em ambiente isolado antes de validar.
- [m-03] `validate_schemas.py` tem inferência perigosa para JSONL sem schema explícito · `tools/scripts/validate_schemas.py:213` · `purification.jsonl` infere `purification-record`, mas qualquer outro `.jsonl` infere `master-record`; isso torna `pathosformel_index.jsonl`, `irr_sample_metadata.jsonl` e outros JSONL vulneráveis a validação errada se alguém omitir `--schema`. · Remediação: inferir por nome somente para arquivos conhecidos e exigir `--schema` para JSONL sem contrato registrado.
- [m-04] `pathosformel_index.jsonl` mistura linhas codificadas e backlog no mesmo contrato sem discriminação de schema · `data/processed/pathosformel_index.jsonl:1` · Métrica medida: 44 linhas com `purificacao_composto` não nulo, 221 linhas com indicadores nulos, `coded_from` distribuído em `backlog=210`, `image=44`, `no_image=6`, `image_direct=5`. · Remediação: no schema proposto, modelar estados por `oneOf`/`if-then` para diferenciar codificado, fora de escopo, backlog e no-image.
- [m-05] O CI cobre contagem `records` ↔ `corpus`, mas não cobre joins inter-domínio · `.github/workflows/validate.yml:49` · O workflow testa apenas igualdade de contagem e idempotência; não há teste para `pathos.item_id ⊆ records.item_id`, `pathos.sigla_id ⊆ corpus.id`, cabeçalho de `id-mapping`, nem ausência/presença de `regimes_visuais.yaml`. · Remediação: adicionar etapa de integridade relacional read-only.

## Pontos fortes (o que NÃO mexer)
- `records.jsonl` e `corpus-data.json` estão sincronizados em contagem: 280/280, e `python3 tools/scripts/records_to_corpus.py --diff` retornou `Em sincronização (por URL).`
- Não há IDs duplicados nos conjuntos principais medidos: `records.item_id`, `corpus.id`, `purification.id` e `pathos.item_id`.
- `records_to_corpus.py` explicita o contrato canônico de exportação: lê `data/processed/records.jsonl`, escreve `corpus/corpus-data.json`, e mantém `id-mapping.json`/UUID5/URL como mecanismos de reconciliação (`tools/scripts/records_to_corpus.py:27`, `tools/scripts/records_to_corpus.py:267`).
- O CI já instala dependências, valida `records.jsonl` contra `master-record`, valida `purification.jsonl` contra `purification-record`, verifica contagem `records`/`corpus` e roda teste de idempotência (`.github/workflows/validate.yml:33`, `.github/workflows/validate.yml:43`, `.github/workflows/validate.yml:46`, `.github/workflows/validate.yml:72`).
- Os schemas operacionais de `master-record` e `purification-record` existem e documentam claramente campos obrigatórios e enums de regime (`tools/schemas/master-record.schema.json:7`, `tools/schemas/purification-record.schema.json:8`).

## Métricas mensuradas
- `data/processed/records.jsonl`: 280 linhas/records JSON válidos para parse; 0 `item_id` ausentes; 0 duplicados.
- `corpus/corpus-data.json`: 280 itens; 0 `id` ausentes; 0 duplicados.
- `data/processed/purification.jsonl`: 236 linhas JSON válidas para parse; 0 `id` ausentes; 0 duplicados.
- `data/processed/pathosformel_index.jsonl`: 265 linhas JSON válidas para parse; 0 `item_id` ausentes; 0 duplicados.
- `data/processed/regimes_visuais.yaml`: ausente no escopo auditado; contagem não mensurável.
- `data/processed/id-mapping.json`: `mapping_len=280`; cabeçalho declara `total_records=277`, `total_corpus=264`, `matched=257`.
- Campos top-level de `records`: `batch_id`, `exports`, `iconocode`, `input`, `item_hash`, `item_id`, `master_record_version`, `purificacao`, `timestamps`, `webscout`.
- Campos top-level de `corpus-data`: `audit_flags`, `citation_abnt`, `coded_at`, `coded_by`, `country`, `date`, `description`, `endurecimento_score`, `id`, `indicadores`, `motif`, `regime`, `support`, `title`, `url`.
- Campos top-level de `pathosformel_index`: `apagamento_narrativo`, `coded_at`, `coded_by`, `coded_from`, `confidence`, `date`, `desincorporacao`, `dessexualizacao`, `enquadramento_arquitetonico`, `fora_escopo`, `heraldizacao`, `image_source`, `inscricao_estatal`, `item_id`, `monocromatizacao`, `motivo_exclusao`, `notes`, `place`, `purificacao_composto`, `regime_iconocratico`, `rigidez_postural`, `serialidade`, `sigla_id`, `title`, `uniformizacao_facial`, `url`.
- Join `pathos.item_id` ∩ `records.item_id`: 265/265.
- Join `pathos.sigla_id` ∩ `corpus.id`: 259/265; órfãos: `BR-016`, `DE-NOTG-1921`, `FR-040`.
- Join `pathos.url` ∩ `corpus.url`: 262 URLs não vazias em comum.
- Join ingênuo `pathos.item_id` ∩ `corpus.id`: 0, confirmando que `item_id` UUID não é a chave para o export público.
- Join `corpus` ↔ `records` pela precedência de `records_to_corpus.py`: 280/280 matches; 277 via `id-mapping`, 3 via UUID5, 0 via URL fallback.
- Distribuição `corpus.regime`: `fundacional=102`, `normativo=97`, `militar=31`, `contra-alegoria=9`, vazio=41.
- Distribuição `purification.regime_iconocratico`: `fundacional=102`, `normativo=97`, `militar=28`, `contra-alegoria=9`.
- Distribuição `pathos.regime_iconocratico`: `None=221`, `normativo=21`, `fundacional=13`, `militar=8`, `contra-alegoria=2`.
- `pathosformel_index` com score não nulo: 44/265; indicadores nulos: 221/265.
- Scripts em `tools/scripts` que citam arquivos sem schema próprio: `corpus-data.json` em 25 scripts; `id-mapping.json` em 7; `pathosformel_index.jsonl` em 2. `records.jsonl` aparece em 24 scripts, mas tem `master-record`; `purification.jsonl` aparece em 13, mas tem `purification-record`.
- Comandos de validação existentes: `python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose`; `python tools/scripts/validate_schemas.py data/processed/purification.jsonl --schema purification-record --verbose`; `python tools/scripts/records_to_corpus.py --diff`; `python tools/scripts/check_corpus_export_idempotent.py`; `python tools/scripts/trace_evidence.py data/processed/records.jsonl`; `python tools/scripts/code_purification.py --status`; `python tools/scripts/check_thesis_terms.py`.
- Execução local read-only de `python3 tools/scripts/records_to_corpus.py --diff`: sucesso, `records.jsonl items: 280`, `corpus-data.json items:280`, `Em sincronização (por URL).`
- Execução local read-only de `validate_schemas.py` para `records` e `purification`: falhou antes da validação por ausência de biblioteca `jsonschema` no ambiente atual.

## Dependências inter-domínio
- O contrato de `pathosformel_index.jsonl` depende simultaneamente do domínio canônico (`records.item_id`) e do domínio de export público (`corpus.id`/`url`); corrigir apenas um lado cria órfãos.
- O domínio de codebook/LPAI conflita com o domínio de schemas operacionais na escala dos indicadores (0–4 versus 0–3); estatísticas de endurecimento dependem dessa decisão.
- O domínio de CI depende de ambiente Python com `requirements.txt`; sem ambiente hermético, a validação local pode falhar antes de testar os dados.
- O domínio de release/export depende de `id-mapping.json`; metadados stale nesse arquivo conflitam com contagens atuais de `records` e `corpus`.
- A ausência de `regimes_visuais.yaml` conflita com documentação/plano que pressupõe sua existência, mas não conflita com scripts atuais porque nenhum consumidor foi encontrado em `tools/scripts`.

## Recomendações priorizadas (top 5)
1. Criar schemas explícitos para `corpus-data.json`, `pathosformel_index.jsonl` e `id-mapping.json`, e registrá-los em `validate_schemas.py`.
2. Adicionar ao CI uma etapa read-only de integridade relacional: `records ↔ corpus`, `pathos ↔ records`, `pathos ↔ corpus`, cabeçalho de `id-mapping`, e presença/ausência esperada de `regimes_visuais.yaml`.
3. Resolver a decisão sobre `regimes_visuais.yaml`: recriar com schema e provenance se for artefato necessário, ou remover a expectativa de existência.
4. Harmonizar a escala dos indicadores entre LPAI v2.1 (0–4) e schemas operacionais/purification (0–3), com migração/versionamento se necessário.
5. Atualizar `id-mapping.json` e os três `sigla_id` órfãos de `pathosformel_index.jsonl`, preservando aliases em changelog se os IDs antigos forem citáveis.
