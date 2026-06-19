# Task: Classificar 41 itens PENDENTES

Criado em: 2026-06-19

## Contexto
Audit da tese identificou 41 itens em `corpus/corpus-data.json` marcados como `PENDENTE` após normalização de regimes vazios. Estes itens aguardam classificação IconoCode (regime + indicadores).

## Lista de IDs
FR-049, FR-050, FR-054, FR-055, FR-056, FR-057, FR-058, FR-059, FR-060, FR-061,
FR-062, FR-063, FR-064, FR-065, FR-066, FR-067,
BR-021, BR-023, BR-027, BR-041, BR-044, BR-045,
UK-011, UK-012, UK-013, UK-014, UK-015, UK-016, UK-017,
US-022, US-023, US-024

## Critério de entrada
- `regime` preenchido (FUNDACIONAL, NORMATIVO, MILITAR, CONTRA-ALEGORIA, CRÍTICO ou NÃO ALEGÓRICO)
- 10 indicadores de purificação preenchidos
- `coded_at` e `coded_by` atualizados
- `audit_flags` sem `#verificar`

## Owner
E3/IconoCode

## Prioridade
Média — não bloqueia publicação, mas deve ser fechado antes da defesa para evitar “?” no corpus público.
