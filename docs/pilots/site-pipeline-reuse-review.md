# Compatibilidade do pipeline existente no site

Inspeção: 2026-09-16. Commit examinado: `4416fda`, repositório `imagens`.
Nenhum merge/cherry-pick executado. Este parecer distingue reuso e adequação
ao plano aprovado; não substitui revisão integral da branch.

## Aproveitar

- Projeção com `legacy_ids`, `slug` e imagem acompanhada de crédito/alt.
- Versão canônica fixada por commit e data de geração recebida como entrada.
- Wrapper de geração e infraestrutura de testes existentes.
- Imagem `site/assets/acervo/BE-004.webp`, examinada nesta rodada; manter a
  origem no commit e conferir seu vínculo com o objeto digital da UNamur.

## Adaptar antes de integrar

- `index_records` reduz URL a um único registro por dicionário: colisões podem
  selecionar a última entrada. Resolver por UUID e aliases verificados.
- `resolve_entry` aceita fallback de URL e legado `grandfathered`. Isso não
  basta para confirmar identidade nem para a revisão exigida no novo contrato.
- `validate_publication` dispensa checagens para `grandfathered`; o plano exige
  revisão dos registros públicos e páginas de status para pendências.
- Manifesto usa `review`, `published`, `withheld`, enquanto o contrato aprovado
  preserva `draft`, `review`, `published`, `archived`. Documentar a migração.
- Aprovação por nome/data não se vincula ao conteúdo revisado por hash. Mudanças
  posteriores de fatos ou fontes precisam invalidar a revisão antiga.
- `overrides` e `public_analysis` vivem no site; fatos e análises revisados devem
  ser promovidos à fonte canônica com histórico antes de exportar.
- Há `approved_by: ana` para BE-004 no manifesto externo. Preservar essa
  informação como metadado recebido; a presente rodada não a reatribuiu nem
  importou automaticamente escores ou aprovação para o ledger.

## Resultado visual de BE-004

Examinada a reprodução extraída do commit: figura feminina coroada e sentada,
braços elevados com tábuas inscritas; leão, raios e cinco figuras masculinas
na zona inferior. A inscrição das tábuas contém 1831; a assinatura inferior
V. LAGYE DEL. acompanha 1852. A data do documento representado permanece
distinta da edição consultada. Proposta registrada em
`docs/pilots/publication-review-evidence.json`. Sem nova codificação.
