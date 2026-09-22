# ADR-002: Notion como índice catalográfico

**Status:** Superado por ADR-004
**Data:** 2026-03-22

> Histórico: esta decisão foi substituída pelo uso do vault Obsidian como
> espelho catalográfico. O texto abaixo é mantido apenas para referência.

## Decisão

O Notion serve como interface de catalogação e índice do corpus.
Cada registro no Notion corresponde a um master record em `records.jsonl`.
A sincronização é feita via `notion_sync.py` (Notion → JSONL e JSONL → Notion).

## Motivação

- Interface amigável para catalogação manual e colaborativa
- Suporte a campos ricos (relações, selects, fórmulas)
- API robusta para automação bidirecional
- Permite que orientador e colaboradores acessem sem conhecer git

## Consequências

- `notion_sync.py` deve manter idempotência (sync sem duplicar registros)
- O Notion database ID deve ser configurável via variável de ambiente
- Conflitos de edição simultânea devem ser resolvidos com "last write wins" + log
- O JSONL no GitHub é a fonte canônica; Notion é espelho editável
