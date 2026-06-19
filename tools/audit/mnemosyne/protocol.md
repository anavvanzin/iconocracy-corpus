# Protocolo da Sessão Empírica — 80 Fios Mnemosyne

**Objetivo:** Desenhar 80 fios relacionais (10 por painel × 8 painéis) no ICONOCRACIA Warburg Atlas, registrar análise Panofsky por fio, e produzir os dados que permitem refinar a Taxonomia das Relações Iconocráticas de v0.1 para v1.0.

**Duração estimada:** 4 sessões de 2–3h cada, distribuídas ao longo de 1 semana.

**Material necessário:**
- ICONOCRACIA Warburg Atlas (canvas) aberto
- `mnemosyne-threads-template.xlsx` (este pacote) preenchível em tempo real
- `mnemosyne-threads-starter.json` (carregável diretamente nos painéis para semente inicial)
- Bibliografia central acessível: Pateman, Mondzain, Goodrich, Warburg, Panofsky, Hayaert

---

## I. Princípios da sessão

1. **Não desenhe um fio sem ter uma tese para ele.** Cada fio é um argumento miniaturizado. Se você não consegue dizer em uma frase o que o fio sustenta, ele ainda não está pronto.

2. **A taxonomia v0.1 é provisória.** Onde sua intuição diverge da categorização sugerida, registre a divergência no campo "Notas argumentativas". É essa divergência que produzirá v1.0.

3. **Pré-iconográfico vem antes da interpretação.** Descreva o que está visível em A e em B antes de qualquer hipótese sobre o que A e B significam juntos.

4. **Relação primária + secundária.** Toda relação iconocrática opera em múltiplas escalas. Permita-se anotar duas — a dominante e a concomitante.

5. **Forças semântica, temporal e regimental como triagem, não como veredicto.** As três pontuações 0–1 ajudam a calibrar a confiança; a decisão final é interpretativa.

---

## II. Sequência sugerida dos painéis

Não há ordem obrigatória, mas a sequência abaixo segue a lógica argumentativa da tese:

```
Sessão 1 (~2h)
  Painel 1 — Gênese            (fundacional, abre o argumento)
  Painel 4 — ENDURECIMENTO    (hipótese central, define o eixo)

Sessão 2 (~2h)
  Painel 2 — Justitia          (regime normativo — invariante)
  Painel 5 — Pedra e Bronze    (regime normativo — suporte)

Sessão 3 (~2h)
  Painel 3 — Domesticação      (passagem fundacional → normativo)
  Painel 6 — Balança e Império (contradição colonial)

Sessão 4 (~2h)
  Painel 7 — Branquitude       (interrogação racial)
  Painel 8 — Fissuras          (contra-alegoria)
```

---

## III. Como preencher cada fio

Para cada um dos 80 fios, preencha:

### Identificação
- **Thread ID** já preenchido: `P{n}-T{nn}` (ex.: `P1-T03`)
- **Item A** e **Item B**: IDs do corpus (ex.: `FR-013`, `FR-018`)

### Análise Panofsky por extremo
- **Pré-iconográfico (A)**: o que se vê em A. Forma, gestos, atributos, postura. Sem interpretação.
  Ex.: "Figura feminina sentada, drapeada à clássica, segurando livro aberto e balança em equilíbrio. Diadema discreto. Olhar frontal."
- **Pré-iconográfico (B)**: idem para B.

### Análise iconográfica do par
- **Iconográfico**: identificação convencional dos motivos em A e B + sua relação iconográfica.
  Ex.: "Em A, Justitia canônica em registro escultórico-monumental. Em B, Justitia reativada em registro numismático. Ambas mantêm o lexicon clássico (balança, postura sentada, drapejado), variando o suporte e a escala de circulação."

### Análise iconológica
- **Iconológico**: o que esta relação A↔B significa para o regime iconocrático? O que esta conexão revela sobre a operação da figura feminina alegorizada no aparelho jurídico-político?
  Ex.: "A passagem do monumento à moeda transfere a função autoritativa de Justitia da arquitetura institucional permanente para a circulação serial cotidiana. A figura permanece a mesma; o seu modo de presença muda. Esta é a operação que define o regime normativo."

### Classificação taxonômica
- **Relação primária**: escolha 1 dos 15 tipos (menu dropdown no XLSX)
- **Relação secundária**: opcional — para fios que operam em mais de um eixo
- **Força semântica** (0–1): sobreposição de motivos
- **Força temporal** (0–1): coerência com o tipo declarado (Nachleben tem força temporal alta se Δ > 50 anos; mimesis tem força alta se Δ < 20 anos)
- **Força regimental** (0–1): par de regimes corresponde à expectativa do tipo declarado?

### Notas argumentativas
- Frase ou parágrafo curto que será integrado ao ensaio do painel.
- Especialmente: registre **divergências** entre sua intuição e a taxonomia sugerida.

---

## IV. Painéis × regimes × relações esperadas

Resumo prévio que orienta a análise (mas não substitui o ato interpretativo):

| Painel | Regime primário | Relações esperadas |
|---|---|---|
| 1. Gênese | Fundacional | Nachleben, Mimesis, Concretização, Par genderizado, Co-presença política |
| 2. Justitia | Normativo | Translatio, Mimesis, Serialização, Genealogia |
| 3. Domesticação | Normativo | Genealogia, Mimesis, Par genderizado, Endurecimento progressivo |
| 4. ENDURECIMENTO | Militar | Endurecimento progressivo, Martialização, Serialização, Genealogia |
| 5. Pedra e Bronze | Normativo | Co-presença institucional, Serialização, Translatio, Mimesis |
| 6. Balança e Império | Normativo | Contradição, Co-presença institucional, Translatio, Inversão |
| 7. Branquitude | Normativo | Co-presença política, Translatio, Mimesis, Inversão |
| 8. Fissuras | Contra-alegoria | Inversão, Satirização, Contradição, Nachleben |

**Sub-hipóteses falsificáveis:**
- Se o Painel 1 produzir mais relações de "Serialização" do que "Co-presença política", a hipótese de que o regime fundacional opera por constelação revolucionária está em risco.
- Se o Painel 4 não produzir nenhuma cadeia "Endurecimento progressivo" de comprimento ≥3, a hipótese central da tese precisa ser reformulada.
- Se o Painel 8 produzir mais "Mimesis" do que "Inversão", as contra-alegorias não estão funcionando como contra-tradição — estão apenas reproduzindo o cânone com outra ironia.

---

## V. Após a sessão — passos automatizados

Quando todos os 80 fios estiverem desenhados e preenchidos:

1. **No Warburg Atlas:** para cada painel, clique "↓ Export" → baixa `iconocracia-painel-{n}-{nome}.json`. São 8 arquivos.

2. **No terminal:** rode o analisador com os 8 JSONs:
   ```bash
   cd thread-analyzer
   python3 analyze_threads.py corpus.json iconocracia-painel-*.json
   ```

3. **Compare:** abra `thread-analysis-report.md` (saída do analisador) e o XLSX preenchido lado a lado.
   - Onde a classificação automática **coincide** com a sua: confirma a categoria. Aumenta confiança.
   - Onde **diverge**: investigue. A divergência pode ser:
     - (a) erro do classificador → ajuste do código `classify_relation()`;
     - (b) erro do anotador → ajuste manual;
     - (c) ambiguidade real da categoria → mudança na taxonomia.

4. **Refinamento da taxonomia para v1.0:**
   - Categorias que aparecem ≥5 vezes em fios desenhados: confirmadas.
   - Categorias que aparecem 1–4 vezes: revisar definição.
   - Categorias que não aparecem em nenhum fio: candidatas a remoção da v1.0.
   - Casos sem categoria adequada: candidatos a nova categoria na v1.0.

5. **Saída final:** o XLSX preenchido + os 8 JSONs exportados + o report do analisador + uma nova versão da taxonomia constituem **o pacote metodológico defensável na qualificação**.

---

## VI. Critérios mínimos para v1.0

A taxonomia pode ser declarada v1.0 quando:

- [ ] Os 80 fios estão desenhados e preenchidos no XLSX
- [ ] Cada fio tem campo iconológico não-vazio (≥30 caracteres)
- [ ] Cada um dos 15 tipos de relação foi usado pelo menos uma vez OU foi explicitamente marcado como "não-aplicável ao corpus" com justificativa
- [ ] Pelo menos um painel produziu um exemplo de **endurecimento progressivo** com cadeia de ≥3 itens
- [ ] Pelo menos um painel produziu um exemplo claro de **contradição dialética** entre dois itens
- [ ] A taxa de concordância entre classificação manual e classificação automática (analyze_threads.py) é ≥70%
- [ ] Para cada painel, há um parágrafo argumentativo de ≥150 palavras escrito no campo de essay

---

## VII. Lacunas que esta sessão *não* resolve

A sessão produz a base relacional. Permanecem como tarefas separadas:

1. **Codificação Panofsky completa do corpus** (141 entries com tag de uma palavra; 24 entries francesas sem Panofsky). A sessão de fios *usa* essas entries mas não as conserta.

2. **Coleta dos itens militares faltantes** (Vichy, Nazi, fascist Italy, US/UK WWII). A sessão pode trabalhar com o que existe, mas o Painel 4 (ENDURECIMENTO) ficará fragilizado até essa coleta ser feita.

3. **Inter-rater reliability** (Cohen's Kappa entre dois codificadores humanos). A sessão produz uma única passagem; para defesa estatística da tese final, uma segunda passagem em 10% dos fios é necessária.

Essas três tarefas são pré-requisitos para a **tese final**, mas a v1.0 da taxonomia pode ser declarada antes delas — desde que a sessão dos 80 fios esteja completa.

---

## VIII. Cronograma sugerido

| Semana | Tarefa |
|---|---|
| Semana 1, dias 1–2 | Sessão 1 (Painéis 1 e 4) |
| Semana 1, dias 3–4 | Sessão 2 (Painéis 2 e 5) |
| Semana 1, dias 5–6 | Sessão 3 (Painéis 3 e 6) |
| Semana 1, dia 7 | Sessão 4 (Painéis 7 e 8) |
| Semana 2, dia 1 | Rodar analisador, comparar com manual |
| Semana 2, dias 2–3 | Refinar taxonomia para v1.0 |
| Semana 2, dia 4 | Atualizar diagrama da taxonomia (regenerar PDF/SVG) |
| Semana 2, dia 5 | Atualizar Cap. 4 com v1.0 e exemplos dos fios |

**Total: 2 semanas para fechar v1.0 e estar pronta para qualificação.**
