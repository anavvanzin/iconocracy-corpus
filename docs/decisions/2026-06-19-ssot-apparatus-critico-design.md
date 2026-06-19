---
tags: [meta, methodology, data, design-spec, decision]
date: 2026-06-19
status: draft-for-review
supersedes_intent: "SQLite event-sourced como mestre (reframed via dialética)"
see_also:
  - docs/decisions/DIALETICA-N165-vs-265.md
  - docs/decisions/dialectic-ssot-2026-06-19/round_1_synthesis.md
---

# Design Spec — Versão Canônica de Referência via Aparato Crítico
## (Single-source-of-truth do corpus Iconocracia, sub-projeto 1 de "abordagem de dados metodológica")

## 1. Problema & objetivo
O corpus hoje não tem **estado conhecível**: a contagem varia (264/265/309/165) entre stores, há fork git local stale (18-ahead/17-behind origin/main), e múltiplas ferramentas (Claude Code, Antigravity/Gemini, crons, edição manual) escrevem em arquivos espalhados. Isso torna qualquer alegação empírica da tese (distribuições de endurecimento, Kruskal-Wallis) **não-reproduzível e, portanto, infalsificável**.

**Objetivo:** estabelecer uma **versão canônica de referência** do corpus — uma só verdade, datada, legível, com proveniência de *juízo* documentada — ao **menor custo da atenção da Ana até nov/2027**.

## 2. Decisão de método (resultado da dialética, aprovada 2026-06-19)
O corpus é um **artefato hermenêutico versionado**, governado por uma **disciplina de aparato crítico** (modelo da edição crítica filológica). A verdade não é um banco vivo nem prosa solta: é uma **sequência de RELEASES analíticos congelados, versionados no git**.

> Renomeação metodológica: não dizer "single source of truth" (fóssil de engenharia) — dizer **"versão canônica de referência"**.

### Não-objetivos (YAGNI / out of scope deste sub-projeto)
- **NÃO** construir SQLite event-sourced como mestre. (O DB, se vier, é índice derivado opcional — ver §6.)
- **NÃO** migrar tudo para um schema novo agora.
- **NÃO** resolver confiabilidade inter-instrumento (opus vs opus-4.6) — é validade DENTRO de um release (sub-projeto 2).
- **NÃO** resolver a sincronização multi-máquina Mac↔SSD↔GitHub (sub-projeto 3, fila da dialética).

## 3. Arquitetura
```
                 ┌─────────────────────────────────────────┐
   ferramentas → │  git main (working copy) — UMA canônica  │ ← propõem mudanças como commits/PRs,
   (CC, Gemini,  │  records.jsonl (master ledger)           │   nunca escrita direta espalhada
    crons)       └───────────────────┬─────────────────────┘
                                     │  freeze (tag)
                                     ▼
                 ┌─────────────────────────────────────────┐
                 │  RELEASE congelado  (ex.: corpus-v1.0)   │  = a versão canônica de referência
                 │   ├─ snapshot legível (records @ corte)  │
                 │   ├─ APARATO de codificação (racional)   │  ← proveniência-de-JUÍZO
                 │   └─ DATASET CARD (dimensões, N, estratos,│
                 │       2 sentidos de "reprodutibilidade") │
                 └───────────────────┬─────────────────────┘
                                     │  exports determinísticos
                                     ▼
        corpus-data.json · companion · dashboards · (SQLite índice, opcional)
```
- **Git É o log de eventos** (de graça): commit = evento; tag = release; mensagem de commit = racional da mudança. Sem event-sourced DB.
- **Exports são projeções** do release; nunca fontes rivais.

## 4. Componentes
1. **Processo de release** (`tools/scripts/freeze_release.py`): dado o estado atual do git main, cria uma tag `corpus-vX.Y`, gera o snapshot legível + um stub de dataset card + valida schema/paridade. Idempotente.
2. **Template do aparato** (`docs/apparatus/TEMPLATE.md` + um registro por release em `docs/apparatus/corpus-vX.Y.md`): campos por coding **contestado/revisado** — `id`, dimensão, valor, **racional** (prosa), revisões anteriores (variant readings), motivo de quarentena. NÃO documenta todos os 309 — só os contestados/usados em alegações.
3. **Dataset card** (`docs/apparatus/corpus-vX.Y-card.md`): o que cada uma das 10 dimensões significa; N e estratos por `coded_by`; **declaração explícita dos 2 sentidos de "reprodutibilidade"** (estatística vs. hermenêutica) e qual a tese reivindica.
4. **Disciplina de escritor único** (doc + convenção git): entre releases, uma cópia canônica (git main); ferramentas propõem via commit/PR. Mata a proliferação na raiz.
5. **Índice derivado SQLite** (`tools/scripts/build_index.py`) — **DIFERIDO**: só quando consulta/dashboard exigir; reconstruído do release; nunca mestre.

## 5. Fluxo de dados
Escrita → git main (commit com racional) → `freeze_release.py` (tag + snapshot + aparato/card) → exports determinísticos. Leitura analítica (notebooks) → lê o release congelado citado, não o working copy.

## 6. O lugar invertido do DB
A escolha inicial (SQLite event-sourced mestre) é **invertida**: se um índice consultável for necessário, ele é uma **projeção** reconstruível do release git — descartável e reconstruível. A verdade nunca vive nele. Isso preserva o desejo de rigor sem o custo de manter um mestre vivo.

## 7. Migração / pré-requisito (passo 1, bloqueia tudo)
**Reconciliar a divergência:** adotar `origin/main` (309 registros, onde o trabalho canônico evoluiu) como base; auditar se os 18 commits locais têm trabalho ÚNICO; resolver o fork (rebase seletivo OU reset para origin após salvar o único). SÓ ENTÃO há o que congelar. (Operação planejada — sub-passo com seu aval, não bulldoze.)

## 8. Sequência & cost budget
1. Reconciliar fork ↔ origin/main=309. *(pré-req)*
2. `freeze_release.py` → `corpus-v1.0` (snapshot + card mínimo). *(custo único ~1 sessão)*
3. Template do aparato + card com os 2 sentidos de reprodutibilidade. *(~1 sessão)*
4. Doc da disciplina de escritor único.
5. Retomar escrita — o aparato **acresce por alegação** (capítulo usa coding → documenta), não upfront.
- **Custo único:** ~1–2 sessões. **Depois:** cada release = tag + atualização de card (barato). Justificado: torna os capítulos estatísticos defensáveis e é MUITO mais barato que um DB vivo.

## 9. Atritos declarados (a síntese NÃO resolve — são para nomear, não esconder)
- **"Reprodutibilidade" é indecidível:** dois sentidos opostos; o dataset card os declara.
- **Custo de atenção (Adorno):** mesmo o aparato custa atenção uma vez; orçado em §8 e amortizado.

## 10. Critérios de sucesso
- [ ] Existe UMA versão canônica de referência datada e citável; toda contagem é um `SELECT`/script sobre ela, não 4 números divergentes.
- [ ] Para qualquer coding usado numa alegação, há racional recuperável (aparato).
- [ ] Exports são reconstruíveis deterministicamente do release.
- [ ] Nenhuma ferramenta escreve fora do fluxo git.
- [ ] Tempo de infra ≤ 2 sessões antes de a escrita retomar.

## 11. Fila (sub-projetos seguintes)
2. Validade analítica DENTRO do release (confiabilidade inter-instrumento) — eixo DIALETICA-N165.
3. Reconciliação/sync multi-máquina (git-workflow).
4. O aparato como material do capítulo de metodologia (funde dado e prosa).
