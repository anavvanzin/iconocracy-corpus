# Plano de correção do audit da tese — iconocracy-audit-2026-06-19

## Problemas confirmados
1. 1 record órfão em records.jsonl sem correspondente em corpus-data.json
2. 41 itens com regime vazio em corpus-data.json
3. Divergência 265/264 entre records e corpus
4. Capítulos canônicos faltando (Cap.4 a Cap.9 + Conclusão)
5. Duplicata Text/Capitulo1_rev.md já removida

## Objetivo
Fechar as inconsistências estruturais mínimas antes de expandir o escopo.

## Passos
- Mapear e classificar o record órfão
- Normalizar regimes vazios para PENDENTE
- Reconciliar contagem 265/264 com idempotência
- Documentar o gap de capítulos em um arquivo de tracking

## Critérios de conclusão
- records.jsonl, purification.jsonl e corpus-data.json alinhados
- Nenhum regime vazio remanescente
- Documento de inventário de capítulos atualizado
