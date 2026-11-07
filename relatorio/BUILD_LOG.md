# BUILD_LOG — A gramática alegórica da iconocracia · edição interativa

## Objetivo
Converter o dossiê "A gramática alegórica da iconocracia" em relatório interativo editorial (versão essencial): capa estado A + sumário executivo + 4 gráficos-assinatura + rail persistente + registro K1–K28.

## Decisões-chave
- **Design authority**: design-precedent-gate → Mnemosyne Viva / Iuris Memoria (tokens do repo `imagens`: paper #EFE5CF, lacre #A8281F, ametista = voz feminina/seleção, azul-tinta = masculino, terracota = fissura). Sobrepõe as invariantes do plugin (skill de usuário prevalece).
- **Átomo-tema**: a figura alegórica (Iustitia com balança de ouro, espada, venda de lacre + 8 variantes de atributo). Capa A = recursão da própria figura: zoom-out até virar célula do atlas do corpus; variantes fixas por posição do anel → loop 3× sem costura.
- **Gráficos**: P3 linha do tempo mural (20 marcos, 405–1896), P5 matriz de distribuição (8 categorias × regra), P2 fluxo de descendência (10 matrizes/mediações → 4 desfechos), P18 balança-veredito (o instrumento de Iustitia pesando as duas leituras), P14 rail de contexto.
- **Disciplina de dados**: nenhum número sem âncora K; leituras estruturais declaradas como síntese qualitativa; fontes s.d. graduadas com data de acesso.

## Arquivos
- `index.html` — estrutura e prosa (pt-BR), 6 seções + capa + rodapé de fontes
- `css/style.css` — tema Mnemosyne Viva adaptado aos componentes do relatório (sem restilizar o kit)
- `css/fonts.css` + `fonts/` — 5 woff2 locais (Instrument Serif, Crimson Pro, JetBrains Mono)
- `js/data.js` — window.RPT (stats, timeline, eras, matrix, flow, verdict)
- `js/sources.js` — window.SRCS K1–K28 + renderizador do registro
- `js/cover.js` — motor de recursão da figura (estado A)
- `js/chart-timeline.js`, `chart-matrix.js`, `chart-flow.js`, `chart-scale.js`, `rail.js`, `main.js`, `utils.js`
- `tools/bundle.py`, `tools/qa_scan.py`; `dist-single.html` (versão arquivo único)

## Validação
- `node --check` em todos os módulos JS: OK
- QA dual-width 1680/1280 (slow-scroll): 0 pageerrors, 0 console errors, 0 overflow horizontal, fontes locais carregadas
- `dist-single.html` sobre file://: 0 erros, fontes OK, overflow 0
- Spot-check de 5 drill-downs (stat 145, placa Tiepolo 1753, célula matriz Virtudes, peso da balança, faixa de falseabilidade): todos rastreiam a sources.js
- Rodadas de correção: rail × capa (margin-right), stat-band 3+1 → grid 4 colunas, hint dos cards, clamp de placas/eras da timeline, nome dos pratos e gatilhos da balança, truncação por palavra inteira, véu de leitura da capa em 1280

## Riscos residuais
- O texto dos pesos da balança é truncado por orçamento de pixel (texto completo no drill-down, por desenho P18)
- Em viewports ≤1180px o rail some (por desenho); o contexto fica nas seções
- A montagem FUSE do diretório de saída reverteu arquivos intermitentemente durante o build; o estado final foi verificado arquivo a arquivo antes do versionamento

## Atualização 2026-09-28 — corpus
- Ana sinalizou divergência ("145?"): os números do relatório vinham de um snapshot antigo (145 itens · 1239–1975 · 15 países).
- Verificado contra `site/data/corpus-data-enriched.json` (repo anavvanzin/imagens): **336 itens · 17 países · 1239–2021 (782 anos)**, codificação até 2026-09-15; inclui contra-alegorias contemporâneas (2018–2021).
- Atualizados: data.js (stats + gatilhos da balança), cover.js (legenda do atlas), chart-scale.js, index.html (âncora da capa, lede, §1, §4), "sete séculos"→"oito séculos".
- Nova âncora **K29** (corpus codificado, fonte primária dos números); registro passa a K1–K29; drill-downs dos stats rastreiam K29.
- Re-validado: QA dual-width 0 erros; bundle único sobre file:// 0 erros; spot-check drill 336→K29 OK.

<a id="reconciliacao-2026-10-13"></a>
## Reconciliação 2026-10-13 — 336 itens do relatório × 337 registros

### Fontes e versões verificadas

| Fonte | Versão | Entradas | Escopo |
|---|---|---:|---|
| `imagens/site/data/corpus-data-enriched.json` | [`6b6c409`](https://github.com/anavvanzin/imagens/commit/6b6c409320e3b59dd911cb871a185d6ea8701fc7), 22/09/2026 | 336 | Projeção enriquecida para consulta editorial |
| Mesmo arquivo, após retirada de campo aposentado | [`eae4c3a`](https://github.com/anavvanzin/imagens/blob/eae4c3a0a524eca6f1c4863c2d6fc21959f9435b/site/data/corpus-data-enriched.json), 27/09/2026, 20:18 −03 | 336 | Mesmas identidades; versão histórica agora vinculada em K29 |
| Mesmo arquivo, após sincronização Villares | [`ba0d25f`](https://github.com/anavvanzin/imagens/commit/ba0d25f91d4733a64c4d0f417c59e87ea9c0b52a), 27/09/2026, 20:46 −03 | 337 | Uma identidade adicionada; nenhuma removida |
| `records.jsonl` e `corpus-data.json` | [`33132b3`](https://github.com/anavvanzin/iconocracy-corpus/commit/33132b3485629183d7378c674c67cd8136d53ce1), contado no README em 04/10/2026 | 337 | Ledger de itens e sua projeção pública; não são 337 observações de codificação |

O commit `33132b3` é de 02/10; **04/10 é a data da contagem documentada**, não a data do commit. O ledger e as projeções consultadas nesta revisão também contêm 337 entradas. O corpus é aberto: esses números identificam versões, não um N definitivo.

### Diferença identificada e limite da inferência

A [PR #218](https://github.com/anavvanzin/iconocracy-corpus/pull/218), commit [`bd6fc53`](https://github.com/anavvanzin/iconocracy-corpus/commit/bd6fc534553b460a923728aca32666e0de2d2d00), de 22/09, acrescentou ao ledger o registro `dfe19295-505c-5df1-866e-e8bb695dbc5f`, **Décio Villares, Alegoria à Lei de 13 de Maio de 1888 (estudo)**. A comparação de `item_id` com o ledger anterior (`d5f8ad1`) mostra exatamente essa adição e nenhuma remoção. A comparação de `id` entre `eae4c3a` e `ba0d25f` no repo imagens mostra a mesma adição. A diferença de uma entrada é explicada por essa sincronização; não foi encontrado um filtro de inclusão que justificasse substituir automaticamente a amostra do relatório pelo ledger.

**Ressalva da data:** a atualização acima registra consulta em 28/09 e codificação até 15/09, mas a projeção em `main` já tinha 337 entradas na noite de 27/09. Não se recuperou evidência da versão exata efetivamente lida durante o build. `eae4c3a` comprova a existência da projeção de 336, mas **não é apresentado como o commit comprovadamente consultado**. Preservamos o registro original da consulta e tornamos explícita essa limitação, em vez de retroativamente inventar uma correspondência entre data e versão.

SHA-256 dos bytes de `site/data/corpus-data-enriched.json` recuperados por `git show`:

- `6b6c409`: `4a643a3fe78baec91ef4cd2cc8e70f832aa685ef4c6c5303aa01e4062cdc4c25`
- `eae4c3a`: `3ba8c273ef52c7a7ad4c3cef9e501503c248e4c8e66bde29d5f3176acc5048ef`
- `ba0d25f`: `06536855aed6fea8c002f898a46d207f147627a993af22b5c3501174317df58f`

A projeção de 336 já continha `BR-041`, com o mesmo título de Villares e URL institucional distinta. A adição do UUID conta como **mais um registro**, não comprova mais um objeto único. É uma possível sobreposição de identidade a revisar com proveniência; nenhum registro foi removido ou deduplicado nesta correção. A projeção enriquecida inclui campos e IDs editoriais, enquanto o ledger é autoridade por família de campos (ADR-006). Contagens de linhas, itens únicos e observações de codificação não são intercambiáveis.

### Decisão e correções

Preservar **336 como a contagem histórica usada pelo relatório**, junto das estatísticas e interpretações já compiladas, sem apresentá-la como o total atual. Atualizar essa amostra exigiria reconstrução e revisão do conjunto de estatísticas, não apenas trocar um numeral.

- Data e status histórico explícitos na descrição Open Graph, âncora da capa, legenda do canvas, cartão estatístico e teste proposto da balança.
- Nota visível junto às estatísticas distingue o ledger de 337, vincula sua versão e explica a ressalva de 28/09.
- K29 vinculado ao arquivo histórico em `eae4c3a`, preservando as datas documentadas de consulta e codificação.
- Regressões de conteúdo, legenda, navegação da fonte e leitura em mobile; incorporadas ao workflow do relatório.
- Dados canônicos, projeções do corpus e o relato original do build preservados.
