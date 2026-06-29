# vault/prompts/

Biblioteca de prompts versionados para a tese ICONOCRACIA.

## Estrutura

```
prompts/
├── _TEMPLATE.md          schema YAML + skeleton (não vai pro INDEX)
├── INDEX.md              gerado por /prompt-index (não editar à mão)
├── _lint.md              gerado por /prompt-index se houver não-conformidade
├── corpus/               prompts de scout, coding, IconoCode
├── bibliografia/         elicit, perplexity, notebooklm
├── escrita/              redação de capítulos, revisão, ABNT
├── metodologia/          desenho de estudo, codebook, validação
├── catalogacao/          ficha catalográfica, Iconclass
└── meta/                 prompts sobre prompts, planejamento de pesquisa
```

## Workflow

1. Copiar `_TEMPLATE.md` para `<dominio>/<slug>.md`.
2. Preencher YAML (id sequencial `P-YYYY-NNN`).
3. Rodar `/prompt-index` para regenerar `INDEX.md`.
4. Se não-conforme, ver `_lint.md` e corrigir.

## Skills relacionadas

- `/prompt-extract` — triagem de notas soltas (read-only, gera `_triagem.md`).
- `/prompt-dedupe` — resolve drafts duplicados detectados na triagem.
- `/prompt-index` — gera catálogo idempotente.

## Convenções

- IDs `P-2026-NNN` sequenciais por ano.
- Datas ISO `YYYY-MM-DD`.
- `dominio` é fechado (lista acima); novos = decisão arquitetural.
- `_*.md` e `INDEX.md` ignorados pelo indexador.
