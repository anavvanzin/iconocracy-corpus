# Cinco lacunas de imagem do catálogo público — auditoria de 24/10/2026

**Resultado: nenhuma das cinco reproduções foi confirmada para publicação.**
Os cinco PNGs homônimos encontrados no armazenamento privado são a mesma imagem
cinza, de 256 × 256 pixels. O JPEG com o ID da performance é uma fotografia de
basquete. Não há cinco reproduções corretas prontas para copiar para o site.

Esta proposta corrige a documentação de evidência no ledger e o suporte da
performance. Preserva os 337 registros, todas as identidades, a seleção editorial,
os artefatos publicados e os dados de codificação. Não autoriza publicação nem
resolve por fusão a possível duplicata de Sèvres.

## Escopo e referências fixadas

- Ledger: `anavvanzin/iconocracy-corpus`, commit
  `4f5ff3f968743b6ecd7e112bbdcd9f59a643c2fb`, 337 registros nesta consulta.
- Catálogo: `anavvanzin/iconocracia`, referência `main`
  `29438d693a032e5321b768c4364bbf15b95b0f26`; 337 registros, 332 marcados com imagem.
- Investigação editorial anterior: [PR #79](https://github.com/anavvanzin/iconocracia/pull/79),
  separada da [PR visual #77](https://github.com/anavvanzin/iconocracia/pull/77).
  As quatro verificações de CI da PR #79 passaram no commit
  `97b5a03ebfaaad79b34a4f81af2ebb2864938356`.
- Manifestos de binários e thumbnails consultados, além de buscas no Drive por
  IDs e nomes; a busca não demonstra ausência absoluta de outros arquivos.
- Contrato: `AGENTS.md`, `CLAUDE.md`, `docs/adr/006-canonical-field-ownership-and-projections.md`
  e `docs/METHOD_CONTRACT_2026-07-31.md`. Nenhum dado privado foi promovido ao site.

## Identidades: não procurar imagens apenas pelo ID curto

| ID público | UUID canônico | Nota de origem | Resultado |
|---|---|---|---|
| BR-017 | `c02356de-a24e-52bc-9ee8-15d6cec55a4b` | SCOUT-205 | Frontispício; URL indisponível |
| BR-018 | `7c8866f2-49eb-591b-83ed-bee28abed5e7` | SCOUT-416 | Charge; página indicada contradiz a edição citada |
| FR-048 | `af855a2f-e19d-5a10-9ed6-915aa67c1ad4` | FR-048 | Sèvres; objeto sem inventário confirmado |
| FR-093 | `a155af76-1c78-502b-b024-b1f0b2ae3f03` | Importação da nota FR-048 | Possível duplicação de identidade, sem adjudicação |
| `6932b9c2-9bb3-5b21-9040-36f6323401e3` | mesmo UUID | FR-101 | Performance; Getty aponta para basquete |

As notas BR-017 e BR-018 no vault identificam, respectivamente, uma moeda de
2000 réis e um selo. Não são as duas entradas públicas sem imagem. A ligação
acima foi feita por título, URL e proveniência de importação do ledger; não foi
feita por igualdade do rótulo curto.

## Evidência examinada

### BR-017 — frontispício do Decreto n.º 1

A [URL registrada no DocVirt](http://docvirt.com/docreader/DocReader.aspx?bib=ACDigital&pagfis=11894)
retornou HTTP 404 nesta sessão, tanto por HTTP quanto por HTTPS. Isso é uma
observação de acesso, não prova de inexistência histórica do objeto. A descrição
minuciosa da nota SCOUT-205 não foi corroborada por reprodução. Uma cópia do texto
do decreto não comprovaria, por si, a existência do frontispício alegórico descrito.

### BR-018 — A República em Leilão

A [página física 4346, coleção 116300](https://memoria.bn.gov.br/docreader/116300/4346)
foi acessada diretamente. O DocReader informa **Ano 1905, Edição 0130, página 19**.
A nota SCOUT-416 cita **O Malho, n. 105, 17/09/1904**. A diferença é verificável
no HTML, mesmo sem uma reprodução utilizável da página. O endereço também aparece
no ledger para `4c2e84a1-6683-5e56-82a1-dc94c8b96afe`, atribuído a outro título e
a 1917; esse sexto registro não foi alterado nesta proposta.

A busca localizou a [edição 105 na Casa de Rui Barbosa](https://rubi.casaruibarbosa.gov.br/bitstream/20.500.11997/7439/1/O%20Malho%20n.105.pdf).
O índice de busca confirma a data da edição; o download do PDF não foi concluído
(HTTP 503/timeout). **Não foi feita inspeção integral da edição nem confirmado
que a charge nela exista.** A página 3321 na BN foi localizada como referência
àquela edição, não como substituta comprovada da imagem procurada.

### FR-048 e FR-093 — La Justice, Sèvres, 1889

Ambas as entradas carecem de fonte primária e inventário. Uma utiliza URL
`/placeholder/FR-048`, a outra um endereço interno `/vault/…`. A primeira já
registrava, em 19/06/2026, que a busca não confirmara a data de 1889. O manifesto
Drive traz FR-048 com `url: null` e um identificador de pasta placeholder; isso
não comprova aquisição. FR-093 foi importada da própria nota FR-048.

O registro institucional [Assiette à l'allégorie de la Justice, C739](https://www.parismuseescollections.paris.fr/ru/node/81549)
foi acessado: autoria anônima, cerca de **1793**, Musée Carnavalet, com
[manifesto IIIF](https://apicollections.parismusees.paris.fr/iiif/320061416/manifest).
É um resultado de busca distinto, não evidência de uma porcelana de Sèvres de 1889.
Não foi usado como imagem substituta. A provável duplicação dos dois registros
permanece uma questão de identidade a adjudicar; nenhum deles foi excluído.

### FR-101 / UUID público — Déborah de Robertis

A URL registrada contém um slug sobre a artista, mas o identificador numérico
Getty **1083427848** resolve para
[Iowa State v Texas Tech](https://www.gettyimages.com/detail/news-photo/kyler-edwards-of-the-texas-tech-red-raiders-shoots-the-ball-news-photo/1083427848),
fotografia de John Weast, de 16/01/2019. A página, os metadados e a imagem JPEG
foram examinados. A imagem mostra basquete; o nome do slug não determina a
identidade da fotografia.

O JPEG privado com o UUID da performance é byte a byte a mesma imagem do preview
Getty. A [busca da própria Getty pela artista](https://www.gettyimages.com/photos/deborah-de-robertis)
retorna fotografias de Marianne nos Champs-Élysées, de 15/12/2018; elas não
confirmam o título, os museus ou o evento descritos na nota. Não houve troca
silenciosa de evento. A identificação exata da performance ainda está aberta.

## Binários rejeitados para estas cinco entradas

| SHA-256 | Verificação | Resultado |
|---|---|---|
| `0450a3ca2ac200aa8eb5161791e275e2dc6ca74b237492067ebb0f141a1ac712` | Cinco PNGs, 758 bytes cada, 256 × 256, todos os pixels RGB (128, 128, 128) | Preenchimento cinza; não reprodução |
| `5145a14e6199d9aba0178c40a9959abab2ba44fb48237e8978dec9f43b08bd06` | JPEG privado e preview Getty, 58.678 bytes, 594 × 526 | Mesma foto de basquete; identidade incompatível com a performance |

Hashes calculados sobre bytes efetivamente obtidos, não preenchidos para satisfazer
um teste. São evidência de rejeição de candidatos, não recibos de publicação.
Não foram adicionados binários, URLs privadas do Drive, credenciais ou novos
vínculos ao manifesto de aquisições. Os arquivos privados não foram alterados.

## Correções propostas

1. Anotar as cinco lacunas em `webscout.gaps`, notas de fonte e `exports.audit_flags`.
2. Marcar as sete interpretações dessas entradas como `gap`, com lacunas explícitas
   no `claim_ledger`, pois as fontes disponíveis não sustentam o estatuto anterior.
3. Identificar os motivos visuais legados como não revalidados. Os valores
   `observed` e as confianças numéricas anteriores foram preservados como legado;
   não representam observações ou estimativas novas desta auditoria. A codificação
   de atributos exige imagem confirmada e adjudicação própria.
4. Corrigir somente `purificacao.record_metadata.medium` de `moeda` para
   `performance` no UUID da FR-101, conforme o campo `suporte` da nota de origem.
   Isso corrige a categoria documental; não confirma o evento, a data ou direitos.
5. Registrar o mapa de identidades, as próximas diligências e os hashes rejeitados
   em `data/staging/missing-public-images-2026-10-24.json`.

Os `input_url`, `item_id` e `item_hash` históricos foram preservados para não
reescrever a identidade de importação. O schema só dispõe de tipos positivos
para fontes; os `source_type` históricos também foram preservados e explicitamente
desautorizados como evidência validada nas notas. Não foi inventada URL substituta.
Os dez indicadores, seus autores e datas, o ledger `purification.jsonl`, o manifesto
editorial, os snapshots e todos os dados publicados permanecem intactos.

## Validação

| Verificação | Resultado |
|---|---|
| `python tools/scripts/validate_schemas.py` | 337/337 válidos, antes e depois |
| Schema de `purification.jsonl` | 286/286 válidos; ledger de codificação inalterado |
| `python -m pytest tests/test_validate_schemas.py tests/test_records_to_corpus.py tests/test_corpus_export_idempotent.py -q` | 15 testes passaram |
| `python tools/scripts/check_corpus_export_idempotent.py` | Base passa; proposta falha apenas no suporte da performance: canônico `performance`, projeção existente `moeda` |
| Comparação com o ledger base | Exatamente cinco registros anotados; os outros 332 sem alteração |
| Identidades e seleção | 337 UUIDs na mesma ordem; nenhum `input`, `item_hash` ou `batch_id` alterado |
| Codificação | Indicadores, autores e datas intactos; única mudança em `purificacao` é o metadado de suporte da performance |
| Rastreabilidade (`EvidenceTracer`, base/proposta) | 0 problemas altos, 641 médios e 40 baixos em ambas; sete interpretações agora têm `gap` documentado |
| Artefatos do site e fixtures | `acervo.json`, `stats.json`, `corpus-data-enriched.json` e fixtures de acervo/stats iguais à referência pública |
| `git diff --check` e leitura JSON do registro de auditoria | Passaram |

**Pendência de integração:** a diferença de suporte é introduzida por esta
correção comprovada e não pela PR visual. A projeção existente não foi regenerada
para eliminar a falha. A PR permanece rascunho; a propagação desse metadado para
uma futura projeção/release exige revisão própria. Isso não muda a contagem de
registros nem fornece uma reprodução para a performance.

Os 641 problemas médios e 40 baixos de rastreabilidade já existem na base e não
foram dispensados. Os 15 testes verificam contratos e funções; não certificam
novas reproduções nem equivalem a um release gate completo. Não foram executados
exportação pública, sincronização de publicação ou construção de release.

## O que falta para recuperar as imagens

Cada caso precisa de identidade confirmada, reprodução correspondente, proveniência
e direitos documentados. Para os brasileiros: cota do frontispício e localização
da charge na edição correta. Para Sèvres: inventário e decisão sobre duplicação.
Para a performance: confirmação do evento pretendido e da fotografia correspondente.
Essas diligências não podem ser substituídas por uma imagem parecida ou pela
declaração de que um arquivo homônimo está correto. O catálogo continua com 337
registros e 332 marcados com imagem; esta PR não produz release ou publicação.

## Integração autorizada em 25/10/2026

Após autorização para corrigir e publicar, a branch foi conciliada com a main
`b1333ea`, preservando as alterações posteriores da tese e de DE-100M-1908.
O exportador vigente foi executado para arquivo temporário. Seu diff contém a
correção comprovada de suporte desta performance e 15 preenchimentos de creator
preexistentes, fora do escopo. Apenas a entrada da performance produzida pelo
exportador foi aplicada à projeção, via escrita JSON atômica: `support` passa
de `moeda` a `performance`. Os outros 336 itens permanecem byte/semanticamente
inalterados e a seleção continua com 337 registros. Não há reconstrução global
para obter CI verde, nem exportação para o site ou para Hugging Face.

A conferência de idempotência dos campos autoritativos passa após essa mudança.
Os 15 preenchimentos de creator são dívida prévia do exportador e não foram
publicados por esta auditoria. O teste de idempotência existente não cobre esse
campo; portanto o resultado verde não significa igualdade integral do export.
As cinco reproduções continuam pendentes, sem imagem substituta nem alteração
nos indicadores de codificação. A tabela de 24/10 acima registra o estado antes
desta integração, não o resultado final do CI.
