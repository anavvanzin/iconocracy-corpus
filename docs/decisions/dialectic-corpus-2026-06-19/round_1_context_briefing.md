# Round 1 — Context Briefing (neutro)

**Dialética:** Generatividade vs. Fechamento do corpus ICONOCRACIA
**Data:** 2026-06-19
**Domínio:** misto (normativo-metodológico + pessoal/padrão-de-trabalho)
**Monks:** 2 (Monk A = Corpus Vivo / Generatividade · Monk B = Corpus Congelado / Fechamento). Terceiro-polo: ver §5.

> Material marcado `[SITUAÇÃO]` vem do caso real da Ana (fonte: a própria pesquisadora/sessões). Material `[PESQUISA]` vem do lit-review externo. Os monks devem acreditar a partir do caso concreto, não de genéricos.

---

## 1. A contradição (enquadramento)

A tese ICONOCRACIA faz **alegações empíricas** (distribuições de "endurecimento"/purificação em escala ordinal 0–3, Kruskal-Wallis, análise de correspondência) sobre um **corpus codificado hermeneuticamente** (análise iconográfica de imagens de alegoria feminina jurídica, séc. XIX–XX). O corpus é, ao mesmo tempo:

- **uma-coisa-a-ser-melhorada** (instrumento melhor, mais imagens, N mais limpo), e
- **uma-coisa-a-ser-fixada** (release citável, datado, com proveniência, para que a alegação seja falsificável).

**Cada ato de melhoria destrói a conhecibilidade; cada ato de congelar inviabiliza a próxima melhoria.** Defesa em **nov/2027**.

## 2. `[SITUAÇÃO]` Estado real do corpus (a "doença" concreta)

- **Contagem não tem estado único:** records.jsonl **265** · corpus-data.json **264** · origin/main **~309** · `Other/corpus-data.json` **165** (snapshot congelado v1.0, 2026-04-25, base primária do Cap.3) · companion **165** (stale). A contagem varia conforme o store.
- **Múltiplos instrumentos codificaram (`coded_by`)** ao longo do tempo, sobre ~264:
  - iconocode-opus **100** · iconocode-opus-4.6-metadata-refined **29** · iconocode-opus-4.6-image **16** (→ "Estrato 1 / IconoCode" = 118)
  - vault-import **58** · migration **19** · manual-entry **1** (→ "Estrato 2" = 78)
  - **(ausente / não-codificado) 41** (→ Estrato 0, quarentena)
- **Linhagem de instrumentos de imagem:** Gemma-4 (via proxy, gerou 29 *zeros* por summaries textuais fracos) → opus / opus-4.6 → **Fable-5** (recode atual).
- **E1 Fable-5 (este esforço):** recode de instrumento único, fresco, multimodal, **só itens com imagem**; **N=44** (índice 49: 44 em escopo + 5 fora_escopo); regimes normativo 21 / fundacional 13 / militar 8 / contra-alegoria 2. Branch não-mergeado.
- **Auditoria N-frame (19/06):** estratificou o corpus opus existente → **N=118** (IconoCode, pende confiabilidade inter-instrumento opus vs opus-4.6) ou **N=196** (todos codificados, pós-auditoria de Estrato 2). Quarentena de 27 fora-de-escopo + 41 não-codificados.
- **Divergência git:** local main **18-ahead / 17-behind** origin/main; o trabalho canônico evoluiu no origin. Múltiplos worktrees (codex, copilot, research) + o E1.
- **Múltiplas ferramentas escrevem no corpus** em arquivos espalhados (Claude Code, Antigravity/Gemini, crons, edição manual) → o SSOT design (19/06) chama isso de causa-raiz da não-conhecibilidade.
- **Padrão de trabalho da Ana** (do /insights): roda muitas sessões/agentes paralelos, melhora continuamente, instala ferramentas; o impulso generativo é forte. O "trava" relatado é a *necessidade de fechamento* que ela não consegue segurar.
- **Decisões já tomadas por Ana nesta linha (2026-06-15/19):** (#1) reaquirir motivos-núcleo; (#2) **expandir** N via reaquisição antes de fechar; quarentena de dois filtros disjuntos; arquitetura forense é escopo permanente; o trabalho de 19/06 preservado em branch `consolidate/2026-06-19-audit-ssot`.

## 3. `[SITUAÇÃO]` Restrições reais

- Defesa nov/2027 — tempo é o recurso mais escasso; o ciclo pode girar para sempre.
- O Cap.3 (análise quantitativa) já foi rodado sobre o snapshot **N=165** congelado (`Other/`). Os capítulos afirmam N=165 no texto.
- `corpus-data.json` é **export derivado** de records.jsonl via `records_to_corpus.py` — editar o export é efêmero (regenera de volta). Quarentena durável exige mudança de pipeline + CI.
- A tese é de **história do direito penal / iconografia jurídica** — voz jurídico-penal, não antropológica. Conceitos autorais (Purificação Clássica, Contrato Sexual Visual, Feminilidade de Estado).

## 4. `[PESQUISA]` — a preencher (lit-review em curso)

### 4a. Corpus vivo/versionado vs. release congelado/citável (DH)
- **Documentação como dispositivo:** *Datasheets for Datasets* (Gebru et al. 2018, arXiv:1803.09010); *Data Statements* (Bender & Friedman 2018); *Data/Dataset Cards* (Google). Declaram composição, proveniência, critérios de inclusão, drift conhecido.
- **Versionamento na prática:** corpora vivos publicam **releases congelados, datados, com DOI** — Universal Dependencies (releases semver a cada 6 meses), Linguistic Data Consortium, Zenodo (DOI por-versão), FAIR. O dev continua mudando; o que se *cita* é a tag.
- **TERCEIRO-VIA central (não é mistura A↔B):** **"releases versionados DE um corpus vivo"** — o corpus melhora continuamente num branch de desenvolvimento; periodicamente corta-se um **snapshot congelado + DOI/hash** para citação. Isto é exatamente o modelo *git-release* que o SSOT design (19/06) propôs (tag `corpus-v1.0`). Dissolve "melhorar OU congelar" em "melhorar E congelar releases" — a contradição era falsa no nível do *processo*, não do dado.
- **Steelman congelar:** "não se cita um alvo móvel"; reprodutibilidade exige "mesmo dado" = estado citável. **Steelman vivo:** dado melhora, erros se corrigem, instrumento melhor supera pior; um congelado-mas-errado é pior que um vivo-correto.

### 4b. Proveniência de instrumento / pooling multi-anotador (brief 2)
- **Pivô (lógica de batch effect):** a pergunta decisiva NÃO é "cada instrumento é confiável?" mas **"a identidade do instrumento está confundida com a variável analítica?"** (Leek et al.; Soneson PLOS ONE). Se `coded_by` correlaciona com regime/data/fonte, instrumento e sinal ficam "inter-misturados e indistinguíveis" → viés. **No caso da Ana: Fable-5 só codifica itens-com-imagem; opus pegou lotes anteriores → confound provável.**
- **Reliability:** Cohen/Fleiss κ, Krippendorff α (≥0.80 confiável; 0.667–0.80 só "tentativo"); **paradoxo do κ** com prevalência desbalanceada (Zec et al.) → reportar % bruta + Gwet AC1 (contestado). Um único número de reliability NÃO licencia pooling sozinho.
- **Agregação ponderada por qualidade:** Dawid–Skene (1979, EM/matriz de confusão por anotador), MACE (Hovy 2013) — superam voto de maioria por *pesar* instrumentos.
- **LLM-as-annotator:** version drift é real (Chen/Zaharia/Zou 2023: GPT-4 mar→jun oscilou 97.6%→2.4% numa tarefa). Best-practice: **fixar modelo+versão+prompt, logar na proveniência, computar κ contra amostra humana antes de adotar novo juiz.** Dois snapshots "GPT-4" não são o mesmo instrumento.
- **Steelman instrumento-único (rater-1):** comparabilidade total, sem confound, proveniência limpa, viés *constante e caracterizável* (auditar 1 matriz de confusão). Custo: viés idiossincrático em 100% dos rótulos, invisível por dentro.
- **Steelman pooling pós-auditoria:** N maior, triangulação (concordância entre instrumentos independentes > auto-consistência de um), robustez; escola *perspectivista* (Aroyo & Welty: desacordo é sinal, não ruído).
- **Terceiros-via:** (a) **estratificar por instrumento + reportar reliability por estrato**; (b) **núcleo + robustez** (estrato mais homogêneo = núcleo analítico; demais = sensibilidade); (c) **calibração/harmonização** num *conjunto de sobreposição* (itens-âncora codificados por todos) — sem overlap, sem harmonização possível.

### 4c. Duas reprodutibilidades (estatística vs hermenêutica) (brief 3)
- **Taxonomia (adotar explicitamente):** NASEM 2019 (reprodutibilidade = mesmo dado+código; replicabilidade = novo dado); Goodman et al. 2016 — methods / results / **inferential** reproducibility (conclusões *qualitativamente similares* — "mais importante").
- **Crítica humanística:** Drucker 2011 (*DHQ*) — dado é **capta** ("tomado", construído, observador-codependente), não *data*; visualização científica contrabandeia certeza positivista. Lincoln & Guba 1985 — credibility/transferability/dependability/confirmability via **audit trail**, não recomputação.
- **Disciplina estatística:** Da 2019 (*Critical Inquiry*) — não usar estatística "decorativamente"; invocar o teste importa seus padrões por inteiro. Gelman & Loken 2013 — **garden of forking paths**: escolhas analíticas contingentes ao dado inflam falso-positivos mesmo sem p-hacking consciente → pré-especificar/congelar protocolo+N. Panofsky: níveis 1 (quase-medida: monocromatização, serialidade) vs 2–3 (juízo: dessexualização, apagamento_narrativo) — os indicadores da Ana *atravessam* a linha medida/interpretação.
- **TERCEIRO-VIA (convergência da literatura):** **"Freeze what you test; document what you judge"** — validade de duas camadas: Tier 1 (p-valor/Kruskal-Wallis) sobre **snapshot congelado+hash**; Tier 2 (codificação iconográfica) com **apparato/audit trail** mirando reprodutibilidade *inferencial*. **Dataset card** (Gebru) declara as duas numa página → substitui "N=165" por "N=[estrato], congelado em DATA, coded_by X, estatística sobre este snapshot; apparato interpretativo no §codebook".
- **One-liner de defesa:** *Congele o que você testa; documente o que você julga.*

### 4d. A pergunta residual (deixada pela pesquisa — alvo da Fase 4)
A terceira-via "releases versionados de um corpus vivo" (UD/Zenodo; FORCE11 Princípio 7: citar a *versão específica*; LDC catalog numbers; Old Bailey Corpus 2.0) **dissolve "melhorar vs congelar" no nível do processo** — são objetos diferentes (dev branch mutável + release imutável citado). MAS deixa um resíduo duro, que é o nó da Ana:

> **Um corpus com estrato-de-validade conhecido E confound de instrumento (Fable-5 só-imagem vs opus nos lotes anteriores) pode ser honestamente representado como UM release congelado — ou o confound de instrumento obriga a escolher UM instrumento / estratificar / quarentenar ANTES de cortar o snapshot?**

Ou seja: a infraestrutura DH resolve a citabilidade, mas NÃO resolve sozinha se o N=44 (Fable-5) e o N=118/196 (opus) são o *mesmo objeto congelável* ou *dois instrumentos que não se misturam sem auditoria de sobreposição*. É aqui que a dialética tem que pressionar.

## 5. `[SITUAÇÃO]` Terceiro-polo (probe) — registrar para o misfit register

Default = 2 monks. Dois candidatos a terceiro polo (não-mistura de A↔B), a vigiar nos ensaios:
- **(i) Schumacheriano — condição-de-fundo:** "o problema não é o dado (nem melhorar nem congelar), é a **disciplina de escritor único** — *quem/o-que* pode escrever no corpus. Resolva o processo de escrita e a falsa-dicotomia some." (Eixo ortogonal: governança, não estado do dado.)
- **(ii) Foucaultiano/Druckeriano — dissolução de moldura:** "'estado conhecível' é fóssil do paradigma de **reprodutibilidade estatística** importado das ciências; uma tese hermenêutica tem outra reprodutibilidade (transparência de juízo). A pergunta 'congelar ou melhorar?' só dói porque você aceitou uma régua que não é a sua."

Rodando com 2 monks; estes dois entram como lentes do misfit register na Fase 4. Se um ensaio os tornar *vivos* (constituência + eixo ortogonal), promover a Monk C numa rodada recursiva.
