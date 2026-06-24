# Revisão Sistemática da Trajetória Metodológica ICONOCRACIA

**Objeto da revisão:** Conjunto de artefatos produzidos na conversa entre 25 de março e 19 de junho de 2026, atendendo ao projeto de tese **"ICONOCRACIA — Alegoria Feminina na História da Cultura Jurídica (Séc. XIX–XX)"**, PPGD/UFSC.

**Metodologia:** Aplicação adaptada do protocolo PRISMA — critérios de inclusão definidos antes da revisão, classificação por tipo de artefato, extração estruturada de método/dado/saída, síntese de lacunas e oportunidades. Limites: este é um corpus de produção própria, não de literatura publicada; a revisão substitui "papers" por "deliverables" e "citation count" por "uso projetado na tese".

**Data da revisão:** 19 de junho de 2026
**Revisora:** auto-revisão assistida (Perplexity Computer agent)

---

## 1. Critérios de inclusão e exclusão

### Incluído
- Todo artefato produzido nesta thread (sites, scripts Python, SVG/PDF, documentos markdown, prompts para outras ferramentas, configurações de dados)
- Toda análise empírica sobre o corpus `iconocracy-corpus` (auditorias, heatmaps, gap analyses)
- Toda proposta teórica desenvolvida em diálogo (taxonomia, classificação de fios, indicadores)

### Excluído
- Decisões puramente conversacionais sem produto durável
- Sugestões mencionadas mas não construídas (por exemplo, opções 1, 3, 5, 6, 7, 8, 9 do brainstorm "be creative" — apenas a 2 foi executada)

---

## 2. Identificação dos artefatos (PRISMA fase 1: identification)

A trajetória produziu **22 artefatos identificáveis**, organizados em sete famílias funcionais:

| Família | Artefatos | Contagem |
|---|---|---:|
| Sites interativos publicados | ICONOCRACIA Atlas (geocoded), ICONOCRACIA Warburg Atlas | 2 |
| Tabelas de fontes / datasets | CSV 34 itens, CSV 116 itens (corpus snapshot), JSON estruturado, atlas data.json, flags JSON | 5 |
| Auditorias do corpus | French Panofsky audit (markdown + JSON), Heatmap completeness (XLSX), Audit on 309 entries | 3 |
| Documentos teóricos / metodológicos | Taxonomia das relações iconocráticas v0.1 (markdown), Capítulo 3 — caso francês (markdown, ~1.070 palavras) | 2 |
| Diagramas visuais | Taxonomia paisagem (SVG+PDF), Taxonomia retrato (SVG+PDF), Pôster banca 16:9 (SVG+PDF+PNG hi-res) | 6 |
| Ferramentas Python | `analyze_threads.py` toolkit (script + corpus + README + demo outputs em ZIP) | 1 |
| Prompts para Claude Code | Mapa-tab para iconocracia-companion, Warburg-tab para iconocracia-companion | 2 |
| Atualizações de memória | Companion app structure, repo structure | 1 |

**Total: 22 artefatos durável-recuperáveis.**

---

## 3. Triagem por escopo de pesquisa (PRISMA fase 2: screening)

Cada artefato classificado quanto à sua **função na tese**:

| Função | Artefatos | Uso projetado |
|---|---|---|
| **Capítulo 3** (caso francês) | Caso francês markdown, French Panofsky audit | Texto e revisão pré-submissão |
| **Capítulo 4** (metodologia) | Taxonomia v0.1, diagramas paisagem/retrato, pôster banca | Seção 4.X completa |
| **Capítulo 8/9** (Atlas) | Warburg Atlas, analyze_threads.py | Painéis Mnemosyne e análise relacional |
| **Anexos metodológicos** | Heatmap XLSX, flags JSON, demo report | Anexo A (transparência metodológica) |
| **Qualificação visual** | Pôster banca + SVG editável | Defesa de qualificação |
| **Companion integrações** | Mapa-tab prompt, Warburg-tab prompt | Extensões do app de pesquisa |
| **Site público / atlas** | Iconocracia Atlas (geocoded) | Output cidadão da tese |

Critério de exclusão aplicado: nenhum artefato foi descartado, pois todos têm função identificável.

---

## 4. Avaliação de qualidade (PRISMA fase 3: eligibility)

Cada artefato foi avaliado em três dimensões: **completude** (o artefato faz o que promete?), **defensibilidade acadêmica** (sustenta-se na qualificação?), **traceabilidade** (lastreia-se em fontes citáveis?).

| Artefato | Completude | Defensibilidade | Traceabilidade | Avaliação |
|---|---:|---:|---:|---|
| ICONOCRACIA Atlas (geocoded) | ✅ alta | ⚠ média | ✅ alta | Pronto para uso público |
| ICONOCRACIA Warburg Atlas | ✅ alta | ⚠ média (depende do uso) | ✅ alta | Pronto; persistência em localStorage limitante |
| Caso francês Cap. 3 | ✅ alta (1.070 palavras) | ⚠ depende de Panofsky | ✅ alta | Precisa codificação Panofsky para defender |
| Taxonomia v0.1 | ✅ alta | ✅ alta | ✅ alta | Pronto como ponto de partida; precisa v1.0 |
| Diagrama paisagem | ✅ alta | ✅ alta | ✅ alta | Pronto para inserção em tese |
| Diagrama retrato | ✅ alta | ✅ alta | ✅ alta | Pronto para A4 |
| Pôster banca | ✅ alta | ✅ alta | ✅ alta | Pronto para projeção |
| French Panofsky audit | ✅ alta | ✅ alta | ✅ alta | Documenta gaps reais |
| Heatmap XLSX (309 entries) | ✅ alta | ✅ alta | ✅ alta | Tier 1–5 de ações priorizadas |
| analyze_threads.py | ✅ alta | ⚠ ainda não testado com dados reais | ✅ alta | Pronto, aguarda fios reais |
| Demo report do analisador | ⚠ sintético | ⚠ ilustrativo apenas | — | Exemplifica saída, não evidência |
| Mapa-tab prompt | ✅ alta | — (prompt para terceiro) | ✅ alta | Pronto para Claude Code |
| Warburg-tab prompt | ✅ alta | — (prompt para terceiro) | ✅ alta | Pronto para Claude Code |

---

## 5. Síntese das contribuições (PRISMA fase 4: included)

### 5.1 Camada empírica — corpus e auditorias

- **Confirmado**: o corpus contém **309 itens** (snapshot de 19 jun.) distribuídos por 11 países, com cobertura panofskyana muito desigual (apenas 49,5% têm objeto `panofsky`; apenas 2,6% têm o nível 3 iconológico completo).
- **Identificado**: a lacuna é **estrutural, não pontual** — a hipótese inicial de que 6 entradas francesas precisavam de codificação revelou um problema de 24+ entradas só na França e 141 entradas em todo o corpus com tag de uma palavra no campo iconológico.
- **Documentado**: a metodologia Panofsky foi aplicada de modo inconsistente em três coortes de codificação (`iconocode-opus`, `iconocode-opus-4.6-image`, `None`), criando heterogeneidade que precisa ser corrigida antes da submissão.

### 5.2 Camada teórica — taxonomia das relações

- **Produzido**: taxonomia v0.1 com **5 famílias × 15 tipos** organizados em eixos não-mutuamente-exclusivos (tempo, função, crítica, regimes, constelação).
- **Articulado**: cada tipo tem definição operacional, indicadores empíricos, e expectativa de distribuição por regime (predictions falsificáveis).
- **Limitação reconhecida**: a taxonomia é dedutiva; a v1.0 só pode emergir do confronto com os fios efetivamente desenhados pela pesquisadora no Atlas Warburg.

### 5.3 Camada instrumental — sites e scripts

- **Construído**: três instrumentos digitais operacionais:
  1. **ICONOCRACIA Atlas** (geocoded, com IIIF thumbnails, gap matrix, regime coloring)
  2. **ICONOCRACIA Warburg Atlas** (drag-and-drop canvas Warburg-style com 8 painéis Mnemosyne)
  3. **analyze_threads.py** (toolkit Python que consome exports do Warburg)
- **Lacuna instrumental**: o Warburg ainda persiste em localStorage do browser, não em Cloudflare D1 (proposta no prompt para Claude Code, mas não executada).
- **Lacuna de integração**: a aba "Mapa" e a aba "Warburg" estão prontas como prompts mas não implementadas no companion.

### 5.4 Camada apresentacional — diagramas

- **Produzido**: 3 versões do diagrama da taxonomia (paisagem A3, retrato A4, pôster banca 16:9), em SVG editável e PDF print-ready.
- **Quality**: paleta consistente com o companion (parchment + Cormorant Garamond + IBM Plex Mono); 15 ícones SVG custom; legibilidade validada em três escalas (inline, página inteira, projeção 3m).

---

## 6. Lacunas identificadas (síntese crítica)

### Lacunas de codificação (alta urgência, pré-submissão)
1. **141 entradas com `iconological.regime` como tag de uma palavra** — exige expansão para texto interpretativo de 2–3 frases.
2. **24 entradas francesas sem objeto `panofsky`** — incluem itens citados em Cap. 3 (FR-013, FR-014, FR-015–017, FR-018, FR-021).
3. **Cluster Emprunts de la Défense Nationale (10 itens) completamente sem codificação** — homogêneo, codificável em lote.
4. **Duplicata FR-012 ↔ FR-021** (Delacroix) precisa deduplicação.

### Lacunas teóricas (média urgência, qualificação)
1. **Taxonomia v0.1 não foi testada contra dados reais.** Sem 80 fios desenhados (10 por painel × 8 painéis), as 15 categorias permanecem dedutivas.
2. **Hipótese ENDURECIMENTO sub-evidenciada para o regime militar.** Apenas 3 itens classificados como militar no snapshot consultado (Atlas v1); 16 no snapshot v2 — ainda abaixo de qualquer limiar estatístico (Kruskal-Wallis exige ≥15 por grupo).
3. **Translatio inter-nacional sem itens militares fora do Brasil.** Vichy France, Nazi Germany, Fascist Italy, US/UK WWII completamente ausentes.

### Lacunas instrumentais (baixa urgência, mas desejável)
1. **analyze_threads.py ainda não rodou contra dados reais** — só demonstração sintética foi executada.
2. **Atlas Warburg sem persistência server-side** — risco de perda de trabalho em troca de navegador.
3. **Pôster banca tem placeholder "[a confirmar]" para orientador** — precisa ser preenchido antes da apresentação.

---

## 7. Recomendações priorizadas

### Tier A — bloqueadores para o Cap. 3
- [ ] Codificar Panofsky completo para FR-013, FR-014, FR-015, FR-016, FR-017, FR-018
- [ ] Deduplicar FR-012/FR-021 (manter FR-012)
- [ ] Atualizar campo `regime` e `endurecimento_score` em FR-021 caso seja a entrada canônica

### Tier B — bloqueadores para qualificação
- [ ] Desenhar ≥10 fios por painel Mnemosyne (≥80 fios totais) usando a taxonomia v0.1
- [ ] Rodar `analyze_threads.py` contra os 8 JSONs exportados
- [ ] Refinar v0.1 → v1.0 da taxonomia comparando classificação manual vs. automática
- [ ] Expandir os 141 tags-de-uma-palavra do `iconological.regime` no corpus
- [ ] Codificar o cluster Emprunts de la Défense Nationale (10 itens) em lote

### Tier C — fortalecimento estatístico (para a tese final, não a qualificação)
- [ ] Coletar 12–15 itens militares adicionais não-brasileiros (Vichy, Nazi, Fascist, US/UK WWII)
- [ ] Coletar 6+ itens numismáticos (moedas e papel-moeda) para os regimes fundacional e normativo
- [ ] Expandir cobertura UK (atualmente 8) e BE (atualmente 6) para ≥15 cada

### Tier D — integração instrumental (desejável)
- [ ] Implementar aba "Mapa" no iconocracia-companion (prompt pronto)
- [ ] Implementar aba "Warburg" no iconocracia-companion com persistência D1 (prompt pronto)
- [ ] Adicionar referência cruzada entre o Atlas público e a tese

---

## 8. Avaliação metodológica meta

### Pontos fortes da trajetória
1. **Coerência entre camadas**: cada artefato refere-se à mesma palette, mesma tipografia, mesma estrutura de dados, mesmo vocabulário (regimes, scores, painéis). Esta integração não é trivial em um projeto de tese de larga escala.
2. **Empiricismo recursivo**: a taxonomia foi construída sobre o corpus, e o corpus foi auditado contra a taxonomia. Isso permite que cada nova rodada de codificação alimente a teoria.
3. **Pluralidade de saídas**: o mesmo conteúdo intelectual existe em quatro modalidades (site interativo, diagrama estático, ferramenta Python, prosa acadêmica). A pesquisadora pode mobilizar a modalidade adequada ao contexto (banca, leitor de tese, colaborador técnico, público externo).

### Pontos fracos da trajetória
1. **Ausência de validação empírica do Warburg**: o canvas foi construído mas a pesquisadora ainda não testou a operação de desenhar fios em sessão real. A taxonomia depende dessa testagem.
2. **Dependência de codificação automática**: 24 das 34 entradas francesas foram codificadas por `iconocode-opus-4.6-image` sem segunda passagem humana. Para sustentar a quantificação na tese, é preciso garantir inter-rater reliability via Cohen's Kappa em ≥10% do corpus.
3. **Não houve consulta a uma fonte secundária central**: nenhuma das ferramentas foi confrontada com a literatura específica sobre Atlas Mnemosyne (Gombrich, Didi-Huberman, Johnson, Michaud), nem sobre iconometria quantitativa (Hayaert 2025, citada no protocolo LPAI mas não cruzada com a taxonomia).

### Recomendação metodológica geral
**A próxima rodada precisa ser de fechamento, não de expansão.** A trajetória atual produziu um ecossistema rico mas com lacunas internas (codificação Panofsky incompleta, taxonomia ainda v0.1, instrumentos não testados). Mais do que adicionar novos artefatos, o próximo passo é:
1. Codificar (Tier A + parte de Tier B);
2. Desenhar fios (Tier B central);
3. Refinar taxonomia para v1.0;
4. Reapresentar o conjunto fechado na qualificação.

Esta recomendação é especialmente relevante porque, em termos de PRISMA, **a fase 5 (inclusão final) ainda não pode ser concluída** — vários artefatos estão na zona "elegível mas dependente de input pendente".

---

## 9. Diagrama de fluxo da trajetória (PRISMA flow)

```
                  Sessão 1 (25 mar.) — Pedido inicial: corpus + mapa
                                       ↓
                  Atlas v1 (geocoded, 22 entries provisional)
                                       ↓
                  Sessão 2 (3 abr.) — Conexão ao corpus real
                                       ↓
                  Atlas v2 (116 entries reais, com regime + score)
                                       ↓
                  Cap. 3 — caso francês (1.070 palavras)
                                       ↓
                  French Panofsky audit (descobre lacuna estrutural)
                                       ↓
                  Heatmap XLSX (309 entries, audita corpus completo)
                                       ↓
                  Brainstorm "be creative" — 9 opções
                                       ↓
                  Warburg Atlas construído (opção 2)
                                       ↓
                  Taxonomia das Relações v0.1 (5 famílias × 15 tipos)
                                       ↓
                  analyze_threads.py (toolkit consumidor de fios)
                                       ↓
                  Diagrama da taxonomia (paisagem + retrato + pôster)
                                       ↓
                  Esta revisão sistemática (19 jun.)
                                       ↓
                  [próximo] — codificação Tier A + sessão de fios
```

---

## 10. Conclusão

A trajetória de 25 de março a 19 de junho produziu **uma infraestrutura metodológica integrada** que cobre as camadas empírica (corpus + auditorias), teórica (taxonomia), instrumental (sites + scripts) e apresentacional (diagramas). Vinte e dois artefatos foram criados, todos com função identificável na tese.

A revisão identifica três níveis de débito técnico:
- **Codificação Panofsky** (141 entradas com tag de uma palavra; 24 entradas francesas sem Panofsky) — bloqueia a defesa do Cap. 3.
- **Validação empírica da taxonomia** (80 fios não desenhados) — bloqueia a passagem de v0.1 para v1.0.
- **Robustez estatística do regime militar** (3–16 itens; abaixo do limiar Kruskal-Wallis) — bloqueia a quantificação central da tese.

O recomendado é **interromper a expansão de novos artefatos e dedicar a próxima fase à conclusão dos três níveis acima.** A infraestrutura está pronta; falta usá-la.

---

*Revisão produzida segundo protocolo PRISMA adaptado a auto-avaliação de trajetória metodológica. Critérios de inclusão e classificação documentados nas seções 1–3; síntese e recomendações nas seções 5–10. Para revisão por par, recomenda-se cruzar este documento com o `cap3-fr-panofsky-audit.md` e o `iconocracy-panofsky-heatmap.xlsx` antes da qualificação.*
