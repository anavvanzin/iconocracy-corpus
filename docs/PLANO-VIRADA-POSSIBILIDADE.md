---
documento: plano
id: PLANO-2026-07-31-VIRADA
titulo: "Consolidação da virada POSSIBILIDADE — plano de migração metodológica"
data: "2026-07-31"
autora: Ana Vanzin · PPGD/UFSC
estatuto: proposta para adjudicação da autora — nada aqui executa sozinho
ancora_decisoes:
  - docs/decisions/2026-07-28-aposentadoria-do-indice-composto.md (DEC-2026-07-28-COMPOSTO)
  - corpus/docs/2026-07-24_espinha-tese-POSSIBILIDADE.md
  - corpus/docs/2026-07-24_varredura-recusas.md
  - corpus/docs/2026-07-24_conselho-modelos-veredicto.md
  - corpus/docs/2026-07-24_auditoria-piloto-iconocode.md
licenca: CC-BY-4.0
---

# Consolidação da virada POSSIBILIDADE

## 0. O que este plano governa

A virada de julho de 2026 é a maior mudança metodológica do projeto até aqui: a
tese abandona o *relógio* (uma progressão fundacional → normativo → militar,
medida por um escore de endurecimento) e adota o *teclado* (um repertório de
corpos femininos que o Estado convoca, recusa e faz coexistir). O
`endurecimento_score` foi aposentado por decisão formal
(DEC-2026-07-28-COMPOSTO); os 10 indicadores sobrevivem como grade de
observação disciplinada; a espinha da tese passa a se organizar por operações
— Entradas, Recusas, Coexistências.

A decisão já existe. O que **não** existe ainda é a sua consolidação técnica:
o repositório está em estado dividido, com o corpus qualitativo v2 vivendo como
artefato paralelo enquanto a cadeia canônica continua emitindo escore — e já
sobrescreveu a virada uma vez (commit `e31bda0`). Este plano organiza a
consolidação em sete fases com invariantes de segurança, portões de aceitação
e os pontos que só a autora adjudica.

**Estatuto epistêmico.** A virada permanece POSSIBILIDADE — hipótese de
trabalho, revisável (espinha, cabeçalho). Este plano consolida a
*infraestrutura* da virada sem congelar o seu *conteúdo*: tudo o que ele
propõe é reversível por design (invariante I2), precisamente porque o erro que
a virada corrige foi tratar o exploratório como definitivo.

---

## 1. Diagnóstico verificado (estado em 2026-07-31)

Todas as afirmações abaixo foram verificadas por inspeção direta nesta data.

### 1.1 O que JÁ migrou ✓

| Componente | Evidência |
|---|---|
| Codebook v2.2.1 escrito; passo 4 do master prompt exige `inventario_verbal` e proíbe composto | `schema/codebook-MASTER.md:3,130,204` |
| Schemas com composto deprecado e nota LEGACY_FROZEN | `tools/schemas/master-record.schema.json:140`; `tools/schemas/purification-record.schema.json:87–92` |
| IRR: composto rotulado `legacy_frozen`, kappa por indicador preservado | `tools/scripts/compute_irr.py:343,450` |
| Leitura não-agregadora dos indicadores (`attribute_inventory`, `legacy_composite` somente-leitura) | `tools/scripts/lpai_indicators.py:82,108` |
| Corpus qualitativo v2 completo: 328 registros com `inventario_atributos` (graus verbais), `recusa`, `metrica` | `corpus/corpus-data.v2.json` |

A tabela de migração da DEC-2026-07-28 confere com o código real: o
*instrumento* está migrado.

### 1.2 O que AINDA NÃO migrou ✗

| Componente | Problema | Evidência |
|---|---|---|
| **Exportador canônico** | Ainda deriva `endurecimento_score` de `purificacao_composto` com fallback `or 0.0` — refabricando exatamente o artefato "0,0" que a auditoria-piloto condenou | `tools/scripts/records_to_corpus.py:161,208` |
| **Ledger canônico** | Os 328 registros têm os 10 indicadores + `purificacao_composto` no bloco `purificacao`, mas **nenhum** campo v2 (`inventario_atributos`, `recusa`) | `data/processed/records.jsonl` (inspeção de chaves) |
| **Export público** | Os 328 itens de `corpus-data.json` carregam `endurecimento_score` — o re-export de `e31bda0` sobrescreveu a virada | `corpus/corpus-data.json` |
| **CSV analítico** | Coluna `purificacao_composto` presente; regenerado automaticamente por hook PostToolUse | `data/processed/corpus_dataset.csv` (header); `.claude/settings.json` |
| **Notebooks** | 6 de 8 dependem do escore: 01 (15 refs), 02 (2), 03 (5), 04 (1), 05 (1), 08 (11); 06 e 07 já operam só sobre indicadores | grep por notebook |
| **Manuscrito** | Cap. 7 apoia a análise no composto por item; Cap. 8 usa o escore como gradiente de ordenação; Cap. 9 afirma "endurecimento crescente" (a monotonia vetada pela DEC §4); Glossário ainda define `endurecimento_score` como escore válido e os regimes "em progressão" | `Capitulo7_analise_qualitativa.md:29–30,54,64,80,110,120`; `Capitulo8_atlas_principios.md:67,102`; `Capitulo9_paineis_atlas.md:391,415`; `Glossario.md:124,175` |
| **Documentação viva** | CLAUDE.md ainda instrui: "Campo de dados canônico permanece `endurecimento_score` (chave estável; não renomear)" e descreve endurecimento como eixo medido — qualquer agente obediente ao CLAUDE.md desfará a migração de boa-fé | `CLAUDE.md` (tabela Terminology) |
| **CI** | Valida schemas e contagem records ↔ corpus-data.json, mas não tem guarda contra re-emissão de escore | `.github/workflows/validate.yml:43–68` |
| **Superfícies públicas** | Dashboards e deploy exibem escore (`corpus/DASHBOARD_CORPUS.html`, `deploy/iconocracia-companion/`, `deploy/tropical-atlas/`, HF Space) | grep prévio |

### 1.3 Dois obstáculos estruturais descobertos na verificação

1. **Crosswalk de IDs.** O v2 usa códigos legíveis (`DE-WR-1924-50PF`,
   `NL-003`); o ledger usa UUIDs em `item_id`. Interseção direta: apenas 50 de
   328. O merge v2 → ledger **não é um join trivial** — exige um crosswalk
   determinístico, cuja chave natural é a URL (o mesmo critério que
   `records_to_corpus.py --diff` já usa), com adjudicação manual dos resíduos.
2. **Inconsistência de escala.** O schema canônico e o Glossário fixam os
   indicadores em 0–3; a auditoria-piloto, o conselho de modelos e o
   CHANGELOG-v2 operaram em 0–4. A divergência precisa de regra única antes de
   qualquer recodificação em escala (ponto de adjudicação §7).

---

## 2. Invariantes de segurança (valem em todas as fases)

- **I1 — Fonte de verdade única.** O v2 entra **no** ledger
  (`data/processed/records.jsonl`, campos aninhados sob `purificacao`,
  conforme convenção já vigente), não permanece como arquivo paralelo. Dois
  canônicos vivos foi a condição que permitiu o `e31bda0`.
- **I2 — `legacy_frozen` é sagrado.** Valores compostos legados não são
  recalculados nem apagados (DEC §3). A migração *adiciona* campos; nunca
  *destrói* o rastro de como o corpus foi construído.
- **I3 — Snapshot antes de tocar.** Tag `legacy-composto-final` sobre o estado
  atual de `corpus-data.json` + `records.jsonl` antes da primeira escrita da
  F1. Snapshots antigos (notebooks, `Other/`) permanecem históricos, não erros.
- **I4 — A decisão vira cláusula executável.** Um teste de contrato (padrão
  `tests/test_corpus_export_idempotent.py`) + job de CI falham se
  `endurecimento_score` ou composto novo aparecerem fora de `legacy_frozen`.
  A recusa da métrica fica inscrita no próprio pipeline — o guard anti-`e31bda0`.
- **I5 — Carimbo de versão.** Toda codificação e todo export registram
  `codebook_version`; o que julho fez e o que agosto fará ficam distinguíveis.
- **I6 — Ledger vivo ≠ amostra congelada.** O corpus segue aberto e em
  expansão (decisão 2026-06-24); a reprodutibilidade do Cap. 6 usa uma amostra
  analítica congelada por tag de release, re-executável no corpus final.
- **I7 — Documentação antes do código.** CLAUDE.md e AGENTS.md mudam **antes**
  da migração técnica, para que nenhum agente futuro desfaça a virada
  obedecendo à instrução antiga.

---

## 3. As sete fases

> Ordem de dependência: F0 → F1 → (F2 ∥ F3) → F4 → F5; F6 corre em paralelo
> desde F1. Cada fase tem portão de aceitação; nenhuma fase seguinte começa
> com o portão anterior aberto.

### F0 — Governança e trava (primeiro, e pequeno)

1. Atualizar CLAUDE.md (tabela Terminology + Known Data Issues): registrar
   DEC-2026-07-28-COMPOSTO, redefinir endurecimento como lente qualitativa,
   remover a instrução "chave estável", apontar para este plano. Idem AGENTS.md.
2. Criar a tag `legacy-composto-final` (I3).
3. Adicionar o teste de contrato + job de CI `no-new-composite` (I4) — ainda
   em modo permissivo (warning), endurecido no fim da F1.
4. Revisar os hooks: a regeneração automática de CSV (PostToolUse) e o
   PreCompact que preserva "endurecimento scores" passam a preservar
   inventário/decisão v2.

**Portão F0:** CLAUDE.md coerente com a decisão vigente; tag publicada; CI
verde com guarda em modo warning.

### F1 — Migração da cadeia canônica de dados

1. **Schema primeiro.** Estender `master-record.schema.json`
   (codebook_version 2.2.x): `purificacao.inventario_atributos` (objeto com os
   10 indicadores em enum verbal fechado: ausente · mínimo · moderado ·
   pronunciado · extremo — o schema **proíbe** tipos numéricos no inventário,
   tornando a não-somabilidade uma propriedade formal do dado);
   `purificacao.recusa` (tipologia: substituição-remasculinizante ·
   deslocamento · negação-pura · feminino-esvaziado · neutro-abstrato, +
   espécie e substituto); `purificacao.corpo_ausente` (gate binário, correção
   unânime do conselho — ausência estrutural nunca vira ponto no contínuo).
2. **Crosswalk.** Construir tabela `id_v2 ↔ item_id` por URL normalizada;
   resíduos não-casados vão para adjudicação manual, nunca para heurística
   silenciosa. O crosswalk é commitado como artefato auditável.
3. **Merge v2 → ledger.** Script idempotente, com dry-run e relatório de diff,
   que grava `inventario_atributos`/`recusa`/`corpo_ausente` sob `purificacao`
   nos 328 registros. `purificacao_composto` permanece intocado (I2).
4. **Redesenho do exportador.** `records_to_corpus.py` passa a emitir o shape
   qualitativo; o composto legado sai apenas dentro de `legacy_frozen`; o
   fallback `or 0.0` morre; o exportador **falha** (exit ≠ 0) se detectar que
   emitiria escore fora de `legacy_frozen`.
5. **Aposentar `corpus-data.v2.json`** após o merge (vira fixture de teste do
   contrato, não arquivo vivo).
6. **CSV.** Coluna `purificacao_composto` renomeada `legacy_composto` (não
   deletada — os snapshots históricos dos notebooks continuam legíveis);
   entram colunas verbais do inventário e da recusa. `code_purification.py
   --status` passa a reportar cobertura por indicador.
7. **Auditar o round-trip do vault.** `vault_sync.py`: campos v2 fazem
   round-trip sem perda; escore em frontmatter de nota antiga é read-only na
   direção vault → records.

**Portão F1:** `validate_schemas.py` 328/328 ✓; teste de idempotência do
export ✓; guarda anti-composto promovida de warning a bloqueante; diff
records ↔ corpus-data.json limpo; nenhum `endurecimento_score` fora de
`legacy_frozen` em artefato vivo.

### F2 — Instrumento, fase 2: o rigor da lente qualitativa

As cinco exigências do conselho de modelos, adaptadas ao pós-virada:

1. **Codebook ancorado** — exemplar visual escrito por indicador por nível
   verbal (ausente → extremo), pontuando só o representado.
2. **Regime por árvore de decisão visual** — proibir dedicatória/intenção/uso
   histórico como evidência de regime (o defeito `US-BANNER-1861`).
3. **Gate de ausência** — `corpo_ausente` pula os 10 indicadores; a recusa é
   codificada na tipologia própria (o erro de categoria do assignat nunca se
   repete).
4. **Gating por confiança** — imagem abaixo do limiar entra como flag, sem
   inventário.
5. **IRR da lente qualitativa** — dupla codificação cega de 20–30% da amostra;
   kappa/α de Krippendorff por indicador ordinal (alvo ≥ 0,67); para o
   inventário verbal e a tipologia de recusa, concordância categórica com
   adjudicação da autora como instância final. O viés de suporte
   (`serialidade`/`monocromatizacao`/`inscricao_estatal` quase automáticos em
   moeda/selo) é tratado como *estratificação analítica por suporte*, não como
   correção do dado bruto.

**Portão F2:** codebook ancorado publicado; IRR piloto da lente qualitativa
reportado; regra de escala única adjudicada (§7).

### F3 — Reanálise: o destino de cada notebook

| Notebook | Sob o escore | Sob a lente | Veredicto |
|---|---|---|---|
| 01_exploratory | distribuições do composto | distribuições **por indicador** + cobertura + mosaico de atributos | reforma |
| 02_kruskal_wallis | KW sobre composto por regime | KW **por indicador ordinal** com correção de comparações múltiplas; efeito por indicador, nunca somado | reforma |
| 03_regression | regressão do composto | morre como está; substituída por modelos ordinais por indicador *se e quando* houver pergunta que os exija | morre/condicional |
| 04_correspondence | análise de correspondência | **o mais alinhado à virada**: correspondência múltipla sobre perfis de atributos — vira análise central | promove |
| 05_temporal | curva temporal do escore | história do repertório: entradas/saídas/coexistências por década — a cronologia como sequência de operações | reforma profunda |
| 06_clustering | já opera sobre os 10 indicadores | agrupamentos como *candidatos a prancha*, não como prova | sobrevive |
| 07_dimensionality | idem | idem, com a mesma ressalva | sobrevive |
| 08_multidimensional_scoring | escore multidimensional | contradiz a DEC frontalmente | morre → apêndice legado |

**Nascem** (as análises que o escore nunca permitiria):
- **Tipologia de recusas** — frequências, co-ocorrências e distribuição
  histórica dos 4–5 mecanismos (a varredura de 13 casos como semente).
- **Cortes sincrônicos** — todos os corpos ativos de um Estado num ano
  (França 1900 como caso-âncora); a "economia de corpos" vira consulta
  executável sobre o corpus.
- **Pranchas warburguianas assistidas** — vizinhança por co-presença de
  atributos como *ferramenta heurística de montagem* (sugerir pares para o
  Zwischenraum), nunca como prova: a decisão de montagem é curatorial, da
  autora.

**Portão F3:** notebooks reformados rodam sobre o CSV pós-F1; 08 movido a
apêndice com nota de estatuto; nenhum notebook vivo lê `legacy_composto` como
variável de análise.

### F4 — Manuscrito: reescrever o que repousa sobre o composto

Regra da DEC §4: nenhuma afirmação da tese pode repousar sobre o composto.
Mapa de reescrita, do mais crítico ao cosmético:

1. **Cap. 9 (painéis do Atlas)** — as trajetórias de "endurecimento
   crescente" (`:391,415`) viram montagem de casos: o contraste entre imagens
   datadas substitui a curva. É a reescrita exigida nominalmente pela decisão.
2. **Cap. 7 (análise qualitativa)** — os compostos por item (2,4; 1,1; 1,7;
   1,3…) saem da prosa; entra o inventário comparado de atributos. O capítulo
   já é qualitativo por vocação — a reescrita o *fortalece*.
3. **Cap. 8 (princípios do Atlas)** — o gradiente por escore (`:67,102`) vira
   ordenação por afinidade de atributos declarada painel a painel.
4. **Glossário** — verbete de endurecimento redefinido (lente, não métrica;
   `legacy_frozen` documentado); verbete de regime perde a palavra
   "progressão" — os três regimes viram *teclas do repertório*, não etapas.
5. **Cap. 2 (metodologia) + Introdução** — a virada é narrada como
   *resultado* metodológico, não como constrangimento: auditoria-piloto
   (148 escores-artefato) → conselho de modelos (veto unânime a escalar) →
   diagnóstico da autora (exploratório tratado como definitivo) → aposentadoria
   formal. O rastro `legacy_frozen` é a evidência documental dessa
   reflexividade — poucos corpus de tese têm a própria crítica metodológica
   inscrita no ledger.
6. **Arquivos `*_original` permanecem protegidos** (hook PreToolUse); a
   reescrita acontece nas versões vigentes e em `vault/tese/`.

**Portão F4:** grep de composto/escore no manuscrito vigente retorna apenas
menções historiográficas rotuladas (a narrativa da virada); nenhuma afirmação
probatória residual. Polimento terminológico fino fica para perto da defesa,
conforme a política já vigente (não-guardrail, decisão 2026-06-24).

### F5 — Superfícies públicas

Após F1 (nunca antes — senão exibem dados que deixarão de existir):
- Dashboards (`corpus/index.html`, `DASHBOARD_CORPUS.html`): histogramas de
  escore → pequenos múltiplos por indicador, mosaico de inventários, painel da
  tipologia de recusas.
- `deploy/iconocracia-companion/` + `companion-data.json`: regenerar da cadeia
  pós-F1; os 21 `zwischenraum_panels` ganham as pranchas de recusa.
- HF Space e release: re-export via Release Gate já com a guarda ativa;
  changelog do release declara o estatuto POSSIBILIDADE.

**Portão F5:** nenhuma superfície pública exibe escore fora de contexto
"legado"; release HF novo publicado com carimbo v2.2.x.

### F6 — Campanhas de expansão (paralela desde F1)

- **#12 → Entradas:** papel-moeda colonial (piastre, AOF, Congo belga).
- **#13 → Recusas:** o arquivo das mudezes — águias, assignats, Anastasie,
  retiradas por decoro.
- **#nova → Coexistências:** cortes sincrônicos completos por Estado/ano —
  exige protocolo SCOUT novo (busca por *conjunto*, não por item).
O corpus segue aberto (I6); codificação nova já nasce no shape v2.

---

## 4. Matriz de riscos

| # | Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|---|
| R1 | Re-export re-introduz escore (já ocorreu: `e31bda0`) | alta | crítico | I3 + I4 + F1.4 (exportador falha em vez de emitir) |
| R2 | Hook PostToolUse re-contamina o CSV automaticamente | alta | alto | F0.4 antes de qualquer edição de corpus |
| R3 | CLAUDE.md instrui agentes a preservar o escore | certa | alto | I7/F0.1 — documentação muda primeiro |
| R4 | Round-trip do vault re-injeta escore de frontmatter antigo | média | alto | F1.7 auditoria direcional |
| R5 | Migração destrói o rastro histórico | baixa | crítico | I2 + I3; merge só adiciona campos |
| R6 | Crosswalk de IDs casa registros errados (só 50/328 diretos) | média | crítico | F1.2: chave por URL + resíduos à adjudicação manual, commitados como artefato |
| R7 | Sobre-correção: a lente qualitativa perde auditabilidade | média | alto | enum verbal validável por schema + indicadores ordinais preservados + IRR F2.5 |
| R8 | Escala 0–3 vs 0–4 incoerente entre artefatos | certa | médio | regra única adjudicada antes de recodificar (§7) |
| R9 | POSSIBILIDADE tratada como definitiva — o erro original repetido | média | alto | rótulo de estatuto em todo artefato novo; I6; revisão perto da defesa |
| R10 | CI quebra por migração fora de ordem (schema/ledger/export) | média | médio | ordem F1.1 → F1.3 → F1.4 é obrigatória; guarda em warning até o fim da F1 |

---

## 5. O que sobrevive intacto (não retrabalhar)

Os 10 indicadores como capta ordinal auditável; `purification.jsonl` (279
codificações, base natural do kappa por indicador); a regra de rastreabilidade
tripla; ARGOS/SCOUT; notebooks 06–07; a hierarquia canônica como desenho
(o que muda é o payload, não a arquitetura); `compute_irr.py` e
`lpai_indicators.py` já migrados; os snapshots históricos de `Other/` como
memória de percurso.

---

## 6. Onde mora a inovação (rigor técnico-criativo)

1. **A não-somabilidade como propriedade formal.** O enum verbal no schema
   proíbe o número — a tese pode afirmar que a recusa da métrica está inscrita
   na estrutura do dado, não numa convenção de estilo.
2. **A recusa como estrutura de primeira classe.** O campo tipológico permite
   consultar o corpus por operação (Entradas/Recusas/Coexistências) — o modelo
   do teclado vira eixo de indexação, substituindo o escore como organizador.
3. **`legacy_frozen` como objeto de estudo.** O escore aposentado vira dado
   histórico *da pesquisa sobre a pesquisa*: o Cap. 2 narra a virada com o
   rastro congelado como evidência — reflexividade metodológica documentada em
   ledger, verificável por qualquer leitor do repositório.
4. **Pranchas computáveis sem métrica.** Co-presença de atributos sugere
   vizinhanças de montagem; a máquina propõe, a autora dispõe — o Zwischenraum
   permanece relação interpretativa, nunca distância escalar.
5. **A economia de corpos executável.** O corte sincrônico (Estado × ano ×
   corpos ativos) transforma "Feminilidade de Estado como política de gestão
   de repertório" de tese em consulta reprodutível.

---

## 7. Pontos que só a autora adjudica

1. **US-020** — remasculinização por deslocamento ou negação pura? (fronteira
   aberta desde a varredura).
2. **Máscara ou capacidade?** — define se o capítulo Recusas é denúncia ou
   luto (espinha, "pontos em aberto").
3. **Escala única** — 0–3 (schema/Glossário) ou 0–4 (auditoria/CHANGELOG-v2)
   para o dado bruto ordinal; e se os graus verbais mapeiam 1:1 sobre ela.
4. **Destino do notebook 08** — apêndice legado comentado ou remoção seca.
5. **Momento do congelamento** da amostra analítica do Cap. 6 (I6 — perto da
   defesa, não agora).
6. **Priorização F4** — começar pelo Cap. 9 (exigido nominalmente pela DEC) ou
   pelo Cap. 7 (maior densidade de compostos na prosa)?

---

## 8. Sequência executável (resumo operacional)

```text
F0  governança ──► tag snapshot ──► guarda CI (warning) ──► hooks revisados
F1  schema v2 ──► crosswalk URL ──► merge no ledger ──► exportador redesenhado
    ──► CSV legacy ──► vault round-trip ──► guarda CI (bloqueante)   [PORTÃO]
F2  codebook ancorado ──► gates (ausência/confiança) ──► IRR qualitativo
F3  notebooks: reforma 01/02/05 · promove 04 · mantém 06/07 · aposenta 03/08
F4  manuscrito: Cap9 → Cap7 → Cap8 → Glossário → Cap2/Introdução
F5  dashboards ──► companion ──► HF release
F6  campanhas #12 · #13 · #coexistências (paralela desde F1)
```

Cada fase fecha com commit dedicado e, quando tocar dado canônico, com
`validate_schemas.py` verde. Nenhum passo deste plano se executa sem a
adjudicação dos pontos do §7 que o afetem.
