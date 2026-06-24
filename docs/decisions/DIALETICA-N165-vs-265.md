# Dialética — Corpus N=165 vs 265

Material de apoio à decisão (skill `hegelian-dialectic`). NÃO é a decisão — é o mapa da
contradição. Decisão final é da Ana. Verificado adversarialmente via `santa-loop` (ver fim).

## A contradição de superfície
- **Congelar 165** (Monk A): corpus = objeto hermenêutico fechado; congelar com data de corte é *mais* rigoroso.
- **Re-rodar 265** (Monk B): corpus = censo vivo; objeto analisado tem de ser idêntico ao canônico.

## Negação determinada

**Suposição compartilhada (a prisão de ambos):** que UM único número precisa ser, ao mesmo
tempo: (a) o ledger canônico, (b) a amostra analisada, (c) a afirmação reportada no
manuscrito, (d) a janela de calibração do instrumento de codificação. Os quatro foram
conflados. A contradição existe *porque* cada monk otimiza uma unidade diferente — A otimiza
(d), B otimiza a identidade (a)=(c).

**Como A falha (especificamente):** admite que os BR-011…BR-054 já foram codificados e gravados
no canônico → o "objeto fechado" já vazou. O corte a 165 é *retroativo*, fixado no número que
já estava analisado = conveniência racionalizada (golpe de B). O argumento de deriva-do-codificador
de A é real, mas não é sobre N — é sobre **condições de codificação**. Logo pede *ondas datadas*,
não amputação da onda 2.

**Como B falha (especificamente):** assume que os 100 itens novos foram codificados ao MESMO
instrumento ordinal dos primeiros 165. Se não foram (deriva de rubrica ao longo de ~1 ano), fundi-los
num Kruskal-Wallis único compara parcialmente "codificação-cedo vs codificação-tarde", não regimes —
contaminação idêntica à que A denuncia. O "ambos os ramos fortalecem a tese" de B ignora que um
resultado nulo a 265 pode ser artefato de deriva, não fragilidade do corpus.

## A pergunta oculta
Não é "165 ou 265?". É: **qual é a unidade de análise e a unidade de reporte — e elas precisam
ser o mesmo número?** Assim que se separam as 4 unidades, o conflito era previsível (teste de abdução ✅).

## Síntese (Aufhebung)

**O corpus não é um objeto congelado nem um censo vivo — é um objeto VERSIONADO com estrutura de
ondas de codificação datadas.** Reconciliação concreta:

1. **Pré-requisito diagnóstico (decide tudo):** auditar a consistência do instrumento de codificação
   entre onda 1 (≤165) e onda 2 (os ~100 BR). Mesma rubrica? Há `coded_at`/`coded_by` no
   `records.jsonl` → dá pra medir deriva (ex.: re-codificar uma amostra cega da onda 1 e comparar).

2. **Corpus v1.0** (corte 2026-04-25, N=165) = corpus analítico **primário** do Cap.3 — preserva o
   ganho de A (objeto consistentemente instrumentado).

3. **Corpus v2.0** (N=265) = rodar os MESMOS notebooks 01–08 como **análise de sensibilidade/robustez
   em apêndice** — preserva a exigência de B (objeto analisado reconciliável com o canônico) sem
   descartar v1.0.

4. **Dataset card / nota de proveniência** em Cap.2: "ledger canônico = 265; corpus quantitativo
   primário = v1.0 N=165 (onda de codificação 1, janela única); v2.0 N=265 em Apêndice X (robustez)."
   → desarma o momento `len(df)=265` da banca tornando a discrepância **legível**, não escondida (A)
   nem apagada (B).

5. **A ordem primário↔sensibilidade é decidida pelo diagnóstico (1):** se onda 2 é consistente em
   rubrica → 265 vira primário (mais limpo, B vence no limite). Se há deriva → v1.0 primário +
   v2.0 sensibilidade + tarefa de re-codificação aberta (A vence no limite). **A decisão N vira um
   teste empírico, não uma preferência.**

## Atualização do modelo
- **Antes:** "tenho de escolher entre reportar 165 ou 265."
- **Depois:** "reporto um *histórico de versões* do corpus + auditoria de deriva de codificação decide qual versão é primária; ambas aparecem; proveniência datada torna tudo falseável."
- **Porque:** a contradição revelou 4 unidades confladas (canônico / analisado / reportado / instrumento). Separá-las dissolve o falso dilema.

## Sequenciamento (o "o quê primeiro")
1. Auditar deriva de codificação onda1↔onda2 (usa `coded_at`/`coded_by`).
2. Conforme resultado: definir primário.
3. Rodar notebooks na versão secundária como robustez.
4. Escrever dataset card no Cap.2 + atualizar números com a estrutura de versões.
5. (Se deriva alta) abrir tarefa de re-codificação cega de uma amostra.

## Fila dialética (contradições abertas p/ rounds futuros)
- "Convenience sampling vs saturação teórica" — os BR são representativos ou achados-porque-achaveis?
- "Codificador único: deriva é ruído a controlar ou *evolução interpretativa legítima* a teorizar?"
- "Censo vs amostra" pressupõe população — existe população de 'alegoria jurídica feminina' ou só arquivo?

---

# REVISÃO pós-santa-loop (fix round 1)

**Veredito santa-loop Round 1 = NAUGHTY.** Dois revisores independentes (Claude Opus + Gemini 2.5
Pro, sem contexto compartilhado) reprovaram a síntese acima por **falha de grounding**: ela herdou
do Monk A a premissa de **codificador humano único com deriva temporal**. Os dados refutam isso.

## Evidência que quebrou a síntese v1
`corpus-data.json` (264): `coded_at` 264/264 · `coded_by` 223/264. Distribuição de instrumento:

| coded_by | n | endurecimento? |
|---|---|---|
| iconocode-opus | 100 | sim |
| vault-import | 58 | sim |
| **(ausente)** | **41** | **não (0/41)** |
| iconocode-opus-4.6-metadata-refined | 29 | sim |
| migration | 19 | sim |
| iconocode-opus-4.6-image | 16 | sim |
| manual-entry | 1 | sim |

`endurecimento_score`: 245/264 presente · 99 são **0 (score válido = corpo vivo/baixa purificação, NÃO ausência)** · 146 >0.

## Síntese revisada (Aufhebung v2 — grounded)

**O corpus é um objeto codificado por MÚLTIPLOS INSTRUMENTOS. O eixo de decisão não é data
(165 vs 265) — é ESTRATO DE VALIDADE × PROVENIÊNCIA DE INSTRUMENTO.** Três estratos reais:

- **Estrato 0 — não-codificado (41):** sem `coded_by`, sem regime, sem endurecimento. São o backlog
  de aquisição ainda não passado pelo IconoCode (= os mesmos 41 "blanks"). **Excluídos de qualquer
  análise quantitativa por definição.** ⟹ **265 nunca foi um N analítico válido.**
- **Estrato 1 — IconoCode (≈145: opus 100 + opus-4.6 45):** o núcleo metodologicamente mais limpo,
  mas atravessa **2 versões de modelo** → exige **confiabilidade inter-instrumento** (opus vs opus-4.6
  pontuam consistentemente?).
- **Estrato 2 — import/migration (≈78: vault-import 58 + migration 19 + manual 1):** têm score, mas
  proveniência ≠ IconoCode direto → confiabilidade incerta; auditar antes de incluir.

### Os N reais (não 165 vs 265)
- **N≈145** (só IconoCode, harmonizado entre versões) — núcleo rigoroso.
- **N≈223** (todos codificados, incl. import/migration) — só após auditoria de confiabilidade.
- **N=264/265** — **inválido p/ quantitativo** (inclui 41 não-codificados).

### O que isso faz com os monks (determinada negação v2)
- Monk B ("re-rodar a 265") era **literalmente impossível** — 41 itens não-codificados não rodam.
- Monk A ("congelar 165") tangenciou um estrato de validade por acidente, mas pela razão errada
  (deriva de codificador humano), que não existe.
- A verdade que ambos perderam: **a integridade não é sobre N, é sobre proveniência de codificação.**

### Sequenciamento revisado
1. **Estratificar** o corpus por `coded_by` (feito — tabela acima).
2. **Quarentenar os 41 não-codificados** → passar pelo IconoCode ou excluir explicitamente.
3. **Confiabilidade inter-instrumento:** re-codificar uma amostra cega com opus-4.6 e comparar com
   opus original; medir concordância nos 10 indicadores ordinais.
4. **Auditar vault-import/migration (78):** confirmar que o score é codificação genuína, não herdada.
5. **Definir o corpus analítico por validade de instrumento** (não por data): reportar N≈145 ou N≈223
   conforme a auditoria, com **dataset card** declarando proveniência por instrumento.
6. Atualizar Cap.2/Cap.3: trocar "N=165" por "N=[válido] após estratificação por instrumento de codificação".

### Critérios mantidos pelos revisores (o que sobreviveu)
Ambos PASS em: **Aufhebung genuína** (versionar o objeto é transformação real da pergunta),
**reversibilidade**, e **integridade** (dataset card desarma o `len(df)`). A correção preservou
o esqueleto e trocou só o eixo: de *data* para *instrumento de validade*.

> Round 2 de verificação adversarial disponível sob demanda — a v2 implementa exatamente o conserto
> unânime dos dois revisores, então a confiança de PASS é alta.
