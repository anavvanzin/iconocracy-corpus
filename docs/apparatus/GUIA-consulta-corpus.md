---
tags: [meta, data, guide, duckdb, apparatus]
date: 2026-06-19
status: guide
see_also: docs/decisions/2026-06-19-ssot-apparatus-critico-design.md
---

# Guia — Consultar o corpus Iconocracia (DuckDB sobre releases congelados)

> Engine: **DuckDB** (recomendado) · SQLite (alternativa embarcada) · **NÃO Postgres** (servidor multiusuário, overkill p/ corpus solo de ~300 itens; só valeria p/ backend web multiusuário). DuckDB lê JSON/CSV/Parquet **no lugar**, sem etapa de carga — encaixa no aparato crítico: os arquivos do release são a verdade, o DuckDB é só a camada de consulta.

## 0. Por que DuckDB aqui
- Zero-ETL: `SELECT ... FROM 'corpus-data.json'` direto. Nenhum mestre vivo a manter.
- Descartável: o índice é reconstruível do release a qualquer momento (Phase 4 do plano).
- SQL analítico forte (window functions, agregações) sem servidor.

## 1. Setup (uma vez)
```bash
# via skill: use a skill `install-duckdb`, ou:
brew install duckdb        # CLI
# Python (no env iconocracy):
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12 -m pip install duckdb
```
CLI: `duckdb` · Python: `import duckdb`.

## 2. Ler o corpus direto do arquivo (sem carregar)
```sql
-- corpus-data.json é uma lista de objetos (flat export, id semântico)
SELECT count(*) AS n FROM read_json_auto('corpus/corpus-data.json');

-- master ledger (records.jsonl, 1 objeto/linha, UUID item_id, estrutura rica)
SELECT count(*) FROM read_json_auto('data/processed/records.jsonl', format='newline_delimited');
```
> Consultar SEMPRE um **release congelado citado** (ex.: tag `corpus-v1.0`), não o working copy, quando o número for pra um capítulo. `git show corpus-v1.0:corpus/corpus-data.json > /tmp/v1.json` e leia de lá.

## 3. Consultas analíticas-chave (colunas reais do corpus)
Colunas do flat export: `id, url, title, description, motif, regime, endurecimento_score, coded_by, coded_at, citation_abnt, country, support, audit_flags`.

```sql
-- N por estrato de instrumento (o eixo da DIALETICA-N165): valida o N analítico
SELECT coalesce(coded_by,'(uncoded)') AS instrumento, count(*) AS n
FROM read_json_auto('corpus/corpus-data.json')
GROUP BY 1 ORDER BY n DESC;

-- N analítico = só codificados (exclui Estrato 0)
SELECT count(*) FROM read_json_auto('corpus/corpus-data.json')
WHERE coded_by IS NOT NULL AND trim(coded_by) <> '';

-- Distribuição de endurecimento por regime (o coração quantitativo)
SELECT regime,
       count(*) AS n,
       round(avg(endurecimento_score),2) AS media,
       round(median(endurecimento_score),2) AS mediana
FROM read_json_auto('corpus/corpus-data.json')
WHERE regime IS NOT NULL AND regime <> '' AND regime <> 'PENDENTE'
GROUP BY regime ORDER BY media;

-- Filtro de quarentena: excluir fora-do-escopo (audit_flags é lista)
SELECT count(*) FROM read_json_auto('corpus/corpus-data.json')
WHERE NOT list_contains(audit_flags, 'fora-do-escopo');

-- Por país e suporte (cobertura do corpus)
SELECT country, support, count(*) AS n
FROM read_json_auto('corpus/corpus-data.json')
GROUP BY ALL ORDER BY n DESC;
```

## 4. Padrões do cheat-sheet (Postgres) → traduzidos ao seu caso
| Padrão Postgres | No seu caso (DuckDB) |
|---|---|
| Índices B-tree/GIN manuais | **Desnecessário** — DuckDB é colunar/vetorizado; varre 300 linhas instantaneamente. Índice só importa em escala grande. |
| `timestamptz` p/ timestamps | `coded_at` já é ISO-8601 string; `CAST(coded_at AS TIMESTAMP)` quando precisar. |
| `numeric(10,2)` p/ dinheiro | `endurecimento_score` é float ordinal 0–3; ok como DOUBLE. NÃO tratar 0 como ausência (é score válido). |
| UPSERT `ON CONFLICT` | N/A — você **não escreve no DB**; a verdade é o release git. O DB é read-only derivado. |
| Cursor pagination | N/A nessa escala. |
| RLS / pooling / `max_connections` | N/A — sem servidor, sem multiusuário. |

## 5. Montar o índice derivado (Phase 4 do plano) — opcional
```sql
-- materializa um .duckdb a partir do release (reconstruível, descartável)
ATTACH 'corpus-v1.0.duckdb' AS idx;
CREATE TABLE idx.corpus AS SELECT * FROM read_json_auto('corpus/corpus-data.json');
-- consulte idx.corpus; delete o arquivo quando quiser, é só cache.
```

## 6. Se um dia precisar de SQLite em vez de DuckDB
Mesmo SQL essencial. Diferenças: SQLite não lê JSON nativo tão bem (precisa carregar via script Python `json`→`INSERT`), e é row-store (melhor p/ lookups pontuais que p/ agregação analítica). Para a análise da tese, DuckDB é superior. A skill `sqlite-database-expert` (instalada) cobre o caso SQLite.

## 7. Quando o Postgres faria sentido (e por que não agora)
Só se você for expor o corpus num **backend web multiusuário com escrita concorrente** (login, edição colaborativa, API pública). Hoje: não há isso (webiconocracy aposentada; companion é estático). Postgres adicionaria um servidor a manter, contra o princípio de menor-custo-de-atenção até 2027. Reabrir só se surgir o caso de uso.
