# Publicação progressiva e lente atlântica

## Objetivo

Publicar oito fichas constitucionais como primeira constelação curatorial de
iconocracia.com, mantendo o corpus como fonte canônica e o site como projeção
editorial rastreável.

## Fases

- [completed] 1. Preservar estado, auditar dados e fechar rastreabilidade.
- [in_progress] 2. Completar e validar oito análises IconoCode.
- [completed] 3. Promover SCOUT-625 e registrar adjudicações aprovadas.
- [completed] 4. Implementar manifesto, pipeline e schemas no site.
- [completed] 5. Implementar lente, fichas e compatibilidade de URLs.
- [in_progress] 6. Validar corpus, dados, frontend responsivo e acessibilidade.
- [pending] 7. Preparar PRs, publicar e verificar iconocracia.com.

## Gates

- As oito fichas formam lote indivisível para publicação.
- Nenhuma ficha nova é publicada sem imagem local, fonte, direitos, crédito,
  citação e adjudicação de Ana.
- `corpus/corpus-data.json` é sempre gerado a partir do ledger.
- O site não duplica nem permite edição de dados canônicos.
- Toda publicação fixa o SHA do corpus usado.

## Seleção e ordem

1. FR-087
2. FR-073
3. ce773ab1-3bfc-9f6e-754a-efe0c567916d
4. SCOUT-625, a receber ID canônico pelo fluxo existente
5. FR-075
6. BE-004
7. 235c545a-f3b8-568a-f268-178806a4bf07
8. BE-IND-1880

## Critério de conclusão

- Corpus validado com 336 registros e sem colisão de URL/hash.
- Site gerado com 103 itens e a constelação com oito membros.
- Testes de junção, gate editorial, aliases e idempotência aprovados.
- Verificação real em 1440, 390 e 320 px sem overflow.
- PR do corpus integrado antes do PR do site; produção validada sem cache.
