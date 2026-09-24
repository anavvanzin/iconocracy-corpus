---
documento: auditoria e decisão
id: DEC-2026-09-22-REABERTURA-INFERENCIAL
data: 2026-09-22
autora: Ana Vitória Vanzin Mendes (auditoria executada por agente Kimi Code, a pedido)
tese: "Iconocracia: Alegoria Feminina na História da Cultura Jurídica (séculos XIX–XX)"
programa: PPGD/UFSC
status: vigente
reafirma:
  - DEC-2026-07-28-COMPOSTO (aposentadoria do índice composto)
  - DEC-2026-07-29-APARATO-MINIMO (aparato mínimo e suficiente)
  - DEC-2026-07-31-METODOLOGIA-2-0 (iconometria como ecologia plural)
substitui: (nenhuma — ver §Veredito)
escopo: "camada inferencial (notebooks 02–08), citações epistêmicas do Cap. 2 §2.5, deriva texto↔ledger"
licenca: CC-BY-4.0
---

# Reabertura auditada da camada inferencial: a dúvida de setembro

## Por que a questão foi reaberta

Em 2026-09-22, Ana formulou a dúvida "não sei se Python ainda é uma boa ideia",
escopada à stack de análise do corpus, com dois gatilhos declarados:
(a) adequação metodológica — a análise quantitativa/computacional pertence ao
desenho da tese?; (b) custo de tempo vs. retorno.

A regra do projeto (ler `docs/decisions/*` antes de re-decidir) localizou três
decisões vigentes de julho/2026 que já respondem à pergunta em tese. Em vez de
simplesmente aplicá-las, optou-se pela **reabertura com auditoria**: submeter as
decisões a verificação empírica antes de confirmá-las. Este documento registra
o método, as evidências e o veredito.

## Método

Três braços independentes, executados em paralelo:

1. **Mapa de afirmações** — toda afirmação quantitativa/estatística do manuscrito
   (`tese/manuscrito/`: Introdução `_rev` e `_original_v2`, Cap. 4, 5, 6, 7,
   Conclusão, sumário, notas e scaffolds), classificada por tipo e cotejada com
   o ledger canônico (`records.jsonl` = 336; `purification.jsonl` = 286;
   audit 2026-09-21).
2. **Reprodutibilidade** — notebooks `02`–`08` inspecionados e re-executados
   (computação de cabeçalho) contra o ledger atual, sem modificar o repo
   (scripts descartáveis em `/tmp/icon_audit/`; env conda `iconocracy`).
3. **Citações** — verificação externa (web) das três referências flagueadas
   `[VERIFICAR]` no Cap. 4 §2.5: Roele, Moran, Braman.

## Evidências

### 1. A camada inferencial não reproduz no ledger atual

Todos os notebooks leem `data/processed/corpus_dataset.csv` — projeção
descartável que está (a) **atrasada** (328 linhas, 238 codificadas, de
24/08/2026, contra 286 codificadas no ledger) e (b) **com schema quebrado**:
`year`, `medium_norm`, `period_norm` e `in_scope` estão 100% vazias, e
`--export-csv` não a regeneraria hoje (a projeção `corpus-data.json` perdeu
esses metadados e migrou para UUIDs). Os metadados só são recuperáveis via join
`purification.jsonl` ⇄ `id_crosswalk.jsonl` ⇄ `corpus-data.json`.

| Notebook | Snapshot gravado | Resultado gravado | Re-execução no ledger atual (N=286) | Veredito |
|---|---|---|---|---|
| 02 Kruskal-Wallis | N=145 (F71/N40/M27/C7) | 9/10 indicadores significativos; composto H=33,81, p≈0 | **3/10** significativos (heraldicização p=0,004; serialidade p=0,001; inscrição estatal p=0,0005); **composto H=5,76, p=0,056 (ns)** | RUNS-BUT-DIFFERENT (material) |
| 03 Regressão | N=145 | R²=0,282 (~regime); R²=0,493 (+suporte) | **R²=0,027** (~regime); modelo com suporte não reexecutável (`medium_norm` morto) | RUNS-BUT-DIFFERENT (material) |
| 04 Correspondência (MCA) | 139 itens | inércias 3,9/3,6/3,3% | **BREAKS**: `prince` falha no env (`altair` ausente); `period_norm` extinta | BREAKS |
| 05 Temporal | markdown cita 165/158 | **nunca executado** (zero outputs) | executável só via parse de `corpus-data.date` (244/286 com ano) | STALE-INPUT / NUNCA EXECUTADO |
| 06 Clustering | markdown cita 165 | **nunca executado**; síntese com placeholders | primeiro run real: melhor k=2; clusters × regimes χ² p=0,061, **V=0,160 (fraco)** — clusters NÃO replicam regimes | PRIMEIRO RUN (negativo) |
| 07 PCA | citado indireto no 08 | PC1 = 53,7% | **PC1 = 67,8%**; Kaiser: 1 componente; PC3 = monocromatização isolada | RUNS-BUT-DIFFERENT (a favor da unidimensionalidade) |
| 08 Sub-scores | — | **nunca executado** | primeiro run: Formalização Burocrática H=16,75, p=8×10⁻⁴; CORE(8) p=0,029; monocromatização ns | REPRODUZ (qualitativamente) |

Três fatos graves de proveniência: os notebooks 05–08 **nunca foram executados**
(sem outputs embutidos; as figuras em `data/processed/` vêm de execução não
registrada); o resultado do 07 existe apenas como citação indireta no 08; e o
CSV de entrada é um input fantasma em relação ao ledger.

### 2. Deriva manuscrito ↔ decisões/ledger

O mapa completo está no relatório do braço 1; o drift é moderado-grande mas
concentrado em três tipos:

- **Deriva de snapshot (~20 passagens)**: os ternos 145/165/154/265 convivem
  com o ledger 336/286. Cap. 4 e Cap. 5 já rotulam instantâneos; **Introdução
  (`:127`, `:193`), Cap. 6 (§6.1 inteira, N=265 de 17-05-2026) e Conclusão
  (`:19`)** ainda afirmam números como estado atual.
- **Deriva epistêmica contra as decisões de julho (~10 passagens)**: o 3º
  objetivo (`Introducao_rev.md:129`) e `:183` ("análise estatística inferencial
  que sustenta as hipóteses centrais"); os p-values de KW no corpo do Cap. 4
  (`:68–70`, `:108`); `sumario_iconocracia.md:172` (alfa de Krippendorff),
  `:194–204` (Cap. 6.2–6.4 inferenciais), `:321–322` (Apêndices C-Kappa e
  D-Saídas Estatísticas); `notas/paradigma-indiciario:11` ("p<0,05 em oito dos
  dez indicadores" — valor que **não consta** de nenhum notebook salvo); Cap. 7
  (`:29–33`, `:274–278`) tratando o composto aposentado como "âncora empírica"
  e "lei empírica".
- **Deriva texto↔ledger em escores pontuais (~8 passagens)**: FR-001 (texto 0,6
  vs ledger 0,7), FR-008 (0,8 vs 1,2), FR-005 (já flagueado), 0970108c
  ("sem codificação" vs codificado), 2419621d (reclassificação não propagada).

**Bug de dados descoberto pela auditoria (independe de trilha):** 15 itens
SCOUT-560–574 divergem entre `purification.jsonl` e `corpus-data.json`. Caso
âncora: **SCOUT-562 = 1,7 no purification vs 3,0 no corpus-data** — e a Tabela 2
do Cap. 6 imprime 3,0 com coluna de indicadores somando 1,7 (inconsistência
interna no próprio capítulo); o texto ainda o chama de "fundacional" quando o
ledger registra "normativo". Corrigir antes de qualquer reimpressão da Tabela 2.

### 3. Citações: nenhuma inventada, todas mal citadas

| No manuscrito | Veredito | Correção |
|---|---|---|
| Roele (2021) | ano errado + claim amplificado | **ROELE, 2025** — "Encounters with Justice", Frontiers of Socio-Legal Studies, CSLS Oxford, 29 jan. 2025. A frase "eschews empiricism" existe verbatim (dirigida ao livro de Hayaert); a formulação "forma do empirismo sem seu conteúdo" **não** é dela. Usável: "methodological encounter between the empirical and the hermeneutic". |
| Moran (2022) | existe, mas não sustenta a distinção | **MORAN, 2022** ("'Just Looking'", CSLS Oxford, 9 fev. 2022) trata do olhar/mind's eye, **não** de evidência proposicional vs. demonstrativa. A distinção é de **MNOOKIN, 1998** ("The Image of Truth", *Yale Journal of Law & the Humanities*, v. 10) e reaparece em **MNOOKIN; RISTOVSKA, 2023** (*First Monday* 28(7), DOI 10.5210/fm.v28i7.13229). |
| Braman (em Mnookin e Ristovska, 2023) | autora/container errados + claim não sustentado | **BRAMAN, S., 2023** — Sandra Braman (não Donald), "Discernment: Blurring and visual evidence", *First Monday*, v. 28, n. 7, DOI 10.5210/fm.v28i7.13245 (dossiê editado por Ristovska sozinha). Sustenta "prova visual construída, não dada" e o blurring ilustração/prova; **"Daubert" não aparece no artigo** — a afirmação sobre admissibilidade/replicabilidade é atribuição falsa a remover ou re-fontar. |

## Veredito: reafirmação, não substituição

A auditoria foi desenhada para poder derrubar as decisões de julho. O resultado
foi o oposto: elas saem **mais fortes**.

1. O argumento de 2026-07-29 era conceptual — o aparato responde a uma pergunta
   que a tese não faz. A auditoria acrescenta o argumento empírico: **os
   resultados gravados não sobrevivem ao ledger atual**. O efeito
   regime→indicadores encolhe de 9/10 para 3/10 indicadores; o composto perde
   significância (p=0,056); a regressão cai de R²=0,282 para R²=0,027; os
   clusters não replicam os regimes (V=0,16). Reinstalar a inferência como
   prova exigiria reescrever as afirmações de 2026 contra seus próprios números
   reexecutados.
2. A infraestrutura da camada está degradada além do estatístico: input CSV
   fantasma, dois notebooks nunca executados, dependência quebrada. "Manter o
   pipeline vivo" custa ~1 dia só para restaurar reprodutibilidade — antes de
   qualquer redação.
3. As três citações que blindariam epistemologicamente o §2.5 estavam todas
   incorretas nos detalhes — e a auditoria as corrige com fontes reais e
   verificadas, gratuitamente reforçando o paradigma indiciário (Mnookin é
   referência melhor que Moran para a distinção que a tese precisa).

**Resposta à dúvida original:** Python permanece boa ideia onde já está —
*plumbing* do corpus (validação, sync, export) e iconometria **descritiva**. A
camada **inferencial como prova** já estava aposentada em julho; a auditoria
confirma que a aposentadoria foi correta e registra que ela nunca foi
executada no manuscrito e nos artefatos.

## Determinações

1. **Notebooks 02–08 congelados** como artefatos exploratórios de diagnóstico
   interno (estatuto de DEC-2026-07-29, 4ª determinação). Não re-executar sobre
   o CSV quebrado. Qualquer re-execução futura exige snapshot datado congelado
   (records + purification + crosswalk) e join corrigido — ~1 dia de trabalho.
   Notebook 01 (descritivo) permanece mantido, atualizado para o ledger vigente.
2. **Cap. 6 = panorama descritivo + apêndice de diagnóstico do instrumento.**
   As seções 6.2–6.4 e os Apêndices C/D do `sumario_iconocracia.md` (março/2026)
   estão **revogados** neste desenho; substituem-se por: distribuições
   descritivas rotuladas como instantâneo + apêndice declarando estatuto de
   diagnóstico interno. (A execução no manuscrito pertence à trilha de
   conformidade — este doc registra, não redige.)
3. **Correções de citação aprovadas** conforme tabela do §3: ROELE 2025;
   MORAN 2022 restrito ao tema do olhar; distinção proposicional/demonstrativa
   reatribuída a MNOOKIN 1998 e/ou MNOOKIN; RISTOVSKA 2023; BRAMAN, S. 2023 sem
   a afirmação sobre Daubert.
4. **O achado que sobrevive e deve pautar a redação descritiva:** o eixo de
   *formalização burocrática* (serialidade, inscrição estatal, heraldicização)
   discrimina regimes no ledger atual (KW p≤0,004 nos três; PC2 burocrático no
   07; sub-score H=16,75, p<0,001 no 08). Entra no Cap. 6 como **padrão
   observado** no catálogo — não como teste de hipótese.
5. **Bug SCOUT-560–574**: reconciliação purification↔corpus-data é obrigatória
   antes de qualquer reimpressão da Tabela 2 do Cap. 6; valor canônico de
   SCOUT-562 a decidir por recodificação documentada.
6. **Harmonização de N**: na trilha de conformidade, todas as âncoras de N
   passam a instantâneo rotulado (ledger 336/286 em 2026-09-21), incluindo
   Introdução e Conclusão.

## Custo por trilha (estimativa da auditoria)

| Trilha | Conteúdo | Custo estimado |
|---|---|---|
| Conformidade (recomendada) | Reescrita do 3º objetivo e das âncoras de N; reenquadramento dos p-values do Cap. 4 como diagnóstico; correção das 3 citações; refresh descritivo do Cap. 6; fix SCOUT-560–574; registro do congelamento dos notebooks | ~1–1,5 dia, quase todo redação |
| Reinstalação inferencial | Reconstruir pipeline de dados + pinar env (prince/altair); primeira execução real de 05–08; redigir 6.2–6.4 + Apêndice D; defender perante banca resultados fracos/nulos contra a tipologia | ~1–2 semanas + risco metodológico auto-infligido |
| Mínimo factual | Só Ns stale + citações + nota KW | ~2–3 h; deixa o drift estrutural vivo |

## Lacunas

- A afirmação sobre Daubert (atribuída a Braman) ficou **sem fonte**: localizar
  fonte real ou removê-la na conformidade.
- Figuras em `data/processed/` atribuídas aos notebooks 05–08 vêm de execução
  não registrada: rastrear origem ou descartar/regenerar do snapshot.
- A ordem de médias F < N < M (`notas/paradigma-indiciario:49`) não se confirma
  em nenhum snapshot (ledger atual: F 1,251 < M 1,681 < N 1,742): revisar essa
  afirmação na conformidade.
- `Introducao_rev.md:155` ("defasagem de 152 anos", 1792→1944) tem marco inicial
  contestado no próprio texto — verificação pendente, fora do escopo inferencial.

## Referências novas verificadas

BRAMAN, Sandra. Discernment: blurring and visual evidence. **First Monday**,
Chicago, v. 28, n. 7, 3 jul. 2023. DOI: 10.5210/fm.v28i7.13245.

MNOOKIN, Jennifer L. The image of truth: photographic evidence and the power of
analogy. **Yale Journal of Law & the Humanities**, v. 10, n. 1, 1998.

MNOOKIN, Jennifer L.; RISTOVSKA, Sandra. [Entrevista sobre prova visual].
**First Monday**, Chicago, v. 28, n. 7, 2023. DOI: 10.5210/fm.v28i7.13229.

MORAN, Leslie J. 'Just looking': methodological challenges researching the
visual culture of law. **Frontiers of Socio-Legal Studies**, Centre for
Socio-Legal Studies, University of Oxford, 9 fev. 2022. Disponível em:
https://frontiers.csls.ox.ac.uk/just-looking/

ROELE, Isobel. Encounters with justice. **Frontiers of Socio-Legal Studies**,
Centre for Socio-Legal Studies, University of Oxford, 29 jan. 2025. Disponível
em: https://frontiers.csls.ox.ac.uk/encounters-with-justice/
