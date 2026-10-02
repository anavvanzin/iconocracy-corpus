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
