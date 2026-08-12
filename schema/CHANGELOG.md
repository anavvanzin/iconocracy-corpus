# LPAI codebook CHANGELOG

## 2.2.0 — 2026-06-24

**Mudança.** Consolida o codebook em `schema/codebook-MASTER.md`, preserva `tools/schemas/master-record.schema.json` como contrato técnico canônico e adiciona campos v2.2.0 opcionais ao bloco `purificacao`.

**Re-pontua itens anteriores?** Não. Os registros em `data/processed/records.jsonl` continuam válidos contra `master-record`; a expansão é compatível e opcional.

**Evidência empírica.** Validação real nesta branch: `records.jsonl` passou 278/278 contra `master-record`; `purification.jsonl` passou 234/234 contra `purification-record`; o schema experimental `codebook-v2.1.0` é preservado como contrato paralelo/orphan, não como validador do ledger canônico.

**Problema teórico endereçado.** Havia múltiplos artefatos competindo como codebook: frame capta, documento-pai de indicadores, patch Elicit e schema experimental. A consolidação reduz drift e deixa claro que a quantificação é capta situada, não evidência neutra.

**Risco de reatividade.** Baixo para dados existentes, porque não altera indicadores, escala nem campos obrigatórios. Médio para codificações futuras, pois novos campos de finalidade/poder podem orientar leituras; por isso permanecem opcionais até freeze.

## 2.1.0 — 2026-06-23

**Mudança.** Schema experimental em `schemas/codebook-v2.1.0.schema.json` com campos avançados (`programa_id`, `finalidade_atribuida`, `dado_negativo`, `power_at_stake`, decomposição de atributos etc.).

**Re-pontua itens anteriores?** Não aplicado ao ledger. Preservado como contexto metodológico e origem de campos v2.2.0 opcionais.

## 2.0.0 — 2026-06-22

**Mudança.** Codebook independente piloto para alegorias de Virtudes, Continentes e Oceanos/Rios; formalização do frame capta e expansão de campos iconográficos.

**Re-pontua itens anteriores?** Não. Documento usado como etapa de desenho, não como contrato único do ledger canônico.
