---
titulo: "MASTER PLAN — Três exemplares trabalhados à mão (registro Martyn)"
projeto: ICONOCRACIA · catálogo iconológico
autor: A. Vanzin
data: 2026-07-13
estado: PLANEJAMENTO (não iniciar redação até aprovação dos exemplares)
escopo: apenas os 3 exemplares; sem fallback legado; sem novas features do browser
---

# Visão geral

Objetivo desta fase: transformar três registros do protótipo `catalogo-iconologico-prototipo.html`
de fichas com apparatus em **exemplares trabalhados à mão** — cada um lido, em prosa,
pelos três estratos de Panofsky, com a interpretação iconológica (Nível III) efetivamente
redigida em vez de deixada como slot vazio. A finalidade é a reunião de cotutela: demonstrar
(a) o método de Martyn absorvido e (b) a crítica de gênero/pós-colonial construída sobre ele.

Cada exemplar nasce como **nota Markdown no formato do vault** (YAML frontmatter + três níveis
em prosa + referências ABNT/Chicago + bloco legível por máquina), e essa nota alimenta os
registros "trabalhados" do HTML. Uma só fonte de verdade, dois destinos (vault + showcase).

Restrição inegociável (regra de integridade): toda afirmação substantiva rastreável a fonte
identificável. Separar explicitamente (a) citação direta, (b) tradução minha, (c) formulação
autoral. Nada fabricado. Onde a fonte não sustentar a frase com precisão, marcar `[VERIFICAR]`
e não afirmar. O Nível III é apparatus autoral (framework ICONOCRACIA) redigido em voz de Ana,
rotulado como formulação a revisar — não como citação.

# Os três exemplares (com fallback documentado)

| # | ID | Item | Função retórica | Regime · score | Fallback |
|---|----|------|-----------------|----------------|----------|
| 1 | **EU-002** | *Time and Justice Reveal the Truth* — Bélgica, KIK-IRPA | Justitia no terreno próprio de Martyn (exempla iustitiae; Tempo revela a Verdade); eixo Bélgica da cotutela | normativo · 0.5 | EU-001 (Zick, *Thronende Justitia*, score 1.4) |
| 2 | **FR-008** | *La République nous appelle…* — Steinlen, 1915, BnF | République-mulher que convoca homens à guerra; máximo rendimento para a crítica de gênero; endurecimento militar | militar · 1.2 | FR-004 (*Marianne enseignant l'alphabet*) |
| 3 | **BR-005** | *Alegoria da República* — Décio Villares, c.1900, MHN | República-mulher positivista brasileira; conecta ao `Apostolado_Positivista_Programa_Iconografico.md` e à presidenta totêmica; laboratório de Ana | fundacional · 1.0 | BR-003 (Monumento à República, Belém, score 2.1 — polo de endurecimento alto) |

Racional do conjunto: o trio percorre três regimes (normativo → militar → fundacional),
três geografias (Bélgica, França, Brasil), e a escala de ENDURECIMENTO (0.5 → 1.2 → 1.0;
com o fallback BR-003 abrindo o polo 2.1). O exemplar 1 engaja Martyn diretamente; o 2 e o 3
mostram a torção feminista/pós-colonial que o §6.2 do skill identifica como a diferença da tese.

**[DECISÃO PENDENTE — Ana]** confirmar os três IDs primários (ou trocar por fallbacks) antes da redação.
Ponto sensível: EU-002 está com `date: Unknown` no dataset → data será marcada `[VERIFICAR]`
e confirmada no KIK-IRPA/BALaT antes de uso em texto submetido; se não confirmar rápido, promover EU-001.

# Estrutura de cada nota-exemplar (o "à mão")

Para cada exemplar, redigir os três estratos em prosa disciplinada:

- **Nível I — descrição pré-iconográfica.** O que o olho registra antes da convenção: suporte,
  formato, composição, gestos, atributos como formas. Sem nomear ainda a alegoria. Ancorado no
  esquema de Panofsky (nível pré-iconográfico) e na descrição formal do próprio registro.
- **Nível II — análise iconográfica.** Identificação do tipo alegórico e dos atributos
  (balança, espada, venda, barrete frígio, Tempo alado, etc.), autoria, data, instituição.
  Ancorado em Martyn (iconografia jurídica; genealogia de Justitia; exempla iustitiae) e nas
  referências ABNT/Chicago já no dataset.
- **Nível III — interpretação iconológica.** Sentido intrínseco: como a figura constrói (não
  apenas reflete) legitimidade jurídica, e — a torção da tese — como generiza e racializa o
  sujeito de direito. Aqui entra a leitura dos indicadores de ENDURECIMENTO já codificados,
  articulada com Warburg (Pathosformel), Rancière (partilha do sensível) e o aparato ICONOCRACIA.
  Formulação autoral, rotulada, a revisar por Ana.

Cada afirmação de Nível II/III recebe âncora inline; lacunas viram `[VERIFICAR]`.

# Arquivos a alterar / criar

- `corpus/exemplares/EU-002.md` — **novo.** Nota-exemplar (frontmatter + 3 níveis + refs + bloco JSON).
- `corpus/exemplares/FR-008.md` — **novo.** Idem.
- `corpus/exemplares/BR-005.md` — **novo.** Idem.
- `corpus/exemplares/worked.json` — **novo.** Agregado legível por máquina dos 3 níveis redigidos, extraído das notas.
- `corpus/build_site.py` — **alterar.** Ingerir `worked.json`; quando um registro tem análise trabalhada, o Nível III renderiza a prosa em vez do slot vazio, com um selo "exemplar trabalhado".
- `corpus/catalogo-iconologico-prototipo.html` — **regenerado** pelo build (não editar à mão).
- `corpus/MASTER_PLAN.md` — este arquivo.

Sem mudanças no browser (filtros, grid) além do necessário para exibir os 3 níveis redigidos.

# Funções (nome + o que faz)

- `load_worked_exemplars(dir) -> dict[id]->levels` — lê `corpus/exemplares/*.md`, extrai o bloco
  JSON de cada nota (níveis I/II/III em texto + âncoras), retorna dict indexado por ID do corpus.
- `parse_exemplar_note(md_text) -> record` — separa YAML frontmatter, as três seções de nível e o
  bloco `json` final; valida que os três níveis existem e não estão vazios.
- `merge_worked_into_corpus(corpus, worked)` — anexa `worked` ao registro correspondente por ID;
  marca `record.worked = true` para o front-end saber renderizar prosa em vez do slot.
- `render_worked_level3(record) -> html` — no template JS, se `record.worked`, monta o Nível III
  com a prosa redigida + âncoras + o apparatus ENDURECIMENTO; senão, mantém o slot atual.
- `extract_anchors(level_text) -> list[cite]` — coleta marcadores de âncora e `[VERIFICAR]` de cada
  nível para o gate de verificação e para exibir a lista de fontes no rodapé do registro.

# Testes / gates de verificação (nome + comportamento em 5-10 palavras)

- `test_three_levels_present` — cada exemplar tem I, II e III não-vazios.
- `test_every_substantive_claim_anchored` — afirmações de Nível II/III têm âncora ou [VERIFICAR].
- `test_no_fabricated_citations` — toda referência bate com o KB Martyn / dataset.
- `test_abnt_reference_valid` — ABNT NBR 6023:2025 presente e bem-formada por exemplar.
- `test_terminology_stable` — um termo por conceito; sem deriva de sinônimos entre níveis.
- `test_quote_translation_labeled` — citação/tradução/formulação autoral separadas e rotuladas.
- `test_image_resolves_or_flags` — miniatura carrega ou cai no quadro de acervo.
- `test_worked_flag_renders_prose` — registros trabalhados mostram prosa, não o slot vazio.
- `test_endurecimento_matches_dataset` — score e indicadores exibidos batem com o corpus base.
- `test_date_unknown_flagged` — EU-002 sem data confirmada aparece como [VERIFICAR].

# Sequência de execução (após aprovação)

1. Ana confirma/ajusta os 3 IDs (decisão pendente acima).
2. Consultar skill `georges-martyn-iconology` + dados do registro; para EU-002, verificar data no BALaT/KIK-IRPA.
3. Redigir `EU-002.md` (Justitia/Martyn) — o mais denso metodologicamente; serve de molde.
4. Redigir `FR-008.md` e `BR-005.md` reaproveitando a estrutura.
5. Passe de verificação (rodar os gates acima); marcar `[VERIFICAR]` onde couber.
6. Extrair `worked.json`; alterar `build_site.py`; regenerar o HTML.
7. Smoke test (Node/DOM shim, como no protótipo) + revisão de Ana.

# Fora de escopo (desta fase)

Imagens locais das miniaturas; visualizador IIIF OpenSeadragon; as outras duas direções do
"todos os 3" (site de três registros combinados; estética manifesto-gravura). Registrados
como trabalho futuro, não implementados agora.
