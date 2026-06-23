# Síntese — Workspace Drift + Data Pipeline Audit (Wave 1 + Wave 2 interno)
Data: 2026-06-23
Fontes: 01-architecture-topology.md, 02-data-contracts.md, 03-imes-pipeline-readiness.md, 04-academic-plans-manuscript.md
Modo: síntese de auditoria — sem fixes

## Top 10 achados cross-domain

1. [C-01 / architecture] Symlink quebrado `/Users/ana/Research/iconocracy-corpus` aponta para `/Volumes/data/projetos/research/hub/iconocracy-corpus` (inexistente). Esse é o path mais perigoso para agentes because ele resolve para destino ausente enquanto o repo canônico está em `/Users/ana/Research/hub/iconocracy-corpus`.
2. [C-02 / architecture + data] `CLAUDE.md` do hub está stale em relação ao estado medido: documento diz 278/234; ledgers medidos são 280/280/236. Como `CLAUDE.md` é governança primária para Claude, isso é vetor de drift downstream em validação/manuscrito.
3. [C / data] `id-mapping.json` está internally inconsistent: mapping array tem 280 linhas, mas cabeçalho declara 277/264/257. Como `records_to_corpus.py` usa este arquivo antes de UUID5/URL, stale metadata pode induzir conclusões erradas.
4. [C-03 / IMES] E1/`pathosformel_index.jsonl` está realmente alinhado a `records.jsonl` por `item_id` (265/265), mas NÃO cobre o corpus canônico atual de 280. Os planos de julho dizem “12 gaps”; a aritmética correta é 15.
5. [C-02 / IMES] E2 não está liberado para claims por indicador cru por decisão IRR já documentada (`docs/decisions/IRR-opus-gemini-PRO-2026-06-22.md`): α global=0,393, nenhum poolável. Isso é decisão metodológica, não bug.
6. [M-02 / data] Escala dos indicadores diverge entre codebook/LPAI (0–4) e schemas operacionais `master-record`/`purification-record` (0–3). Qualquer sumarização atual pode estar misturando escalas.
7. [M-01 + M-02 / academic] Manuscrito e vault preservam N=145, N=165 e N=265 em passagens substantivas de Introdução, Cap.2, Cap.3, Cap.5 e Cap.6; risk é claim de “estado atual” usando freezes antigos.
8. [M-05 / architecture] Identidade Git medida diverge do briefing inicial (recon apontou `feat/codebook-master-v2.2.0`; estado medido em follow-up foi `feat/alegorias-piloto-v2` `5f06c87`). Esse é um risco operacional para quem edita manuscrito/planos sem confirmar branch.
9. [M-04 / IMES] `regimes_visuais.yaml` não existe no path auditado e nenhum consumidor foi encontrado em `tools/scripts`; qualquer plano que dependa dele está apontando para artefato inexistente.
10. [m-02 / academic] Elicit/plano do dia estão rastreáveis, mas ainda não encaixados na capacidade de julho; risco é expansão silenciosa de escopo se regra de governança não for explícita.

## Matriz de dependências

- A-01: drift de governança (C-02 topologia) → alimenta M-02/M-03 porque agentes leem `CLAUDE.md` como verdade.
- A-02: symlink quebrado (C-01 topologia) → risco operacional imediato para scripts de pipeline.
- D-01: `id-mapping.json` stale (C data) → afeta `records_to_corpus.py` e qualquer reconciliação corpus/export.
- D-02: escala indicadores (M data) → afeta E2 porque clusters/sumarios usam essa métrica.
- E-01: E1 não cobre 280 (C IMES) → bloqueia fechamento limpo do biweekly se a regra de exclusão não for declarada.
- E-02: E2 bloqueado para indicador cru (C IMES) → Cap.6 não pode trocar N=145/165 por 280 em resultados inferenciais sem re-run.
- T-01: N obsoleto em manuscrito (M academic) → conflita diretamente com planos atualizados e com abertura para julgamento externo.
- T-02: branch drift (M architecture) → decisão de onde editar antes de corrigir planos/manuscrito.

## O que NÃO mexer

- Manter `CLAUDE.md` do hub como fonte de orientação; só atualizar contagens stale para valores medidos.
- Manter `records_to_corpus.py` como export único de `corpus-data.json`; ele é o contrato canônico.
- Manter `Other/` como snapshot histórico até decisão de Ana sobre N analítico.
- Manter P01 como modelo de prancha E3; é a melhor referência atual.
- Manter E1 status labels (`e1-uncoded`, `e1-no-image`, backlog) enquanto a regra de exclusão não for decidida.

## Roadmap de remediação sugerido (2 sprints)

Sprint 1 (prioridade alta, esta semana):
1. Remover/retargetar symlink `/Users/ana/Research/iconocracy-corpus`; consolidar branch/commit fonte de verdade.
2. Congelar “N analítico” em um dataset card formal: 280 canonical, 265 E1, freeze 145/165 histórico, regras de exclusão explícitas.
3. Corrigir 15→12 gaps nos planos com regra formal ou atualizar para 15.
4. Remover/arquivar `id-mapping.json` stale ou recomputar header para 280/280.
5. Atualizar `CLAUDE.md` do hub, `CLAUDE.md` da raiz e `README.md` com contagens medidas.

Sprint 2 (estrutural, semana seguinte):
6. Criar schema para `corpus-data.json`, `pathosformel_index.jsonl`, `id-mapping.json`; registrar em `validate_schemas.py`.
7. Acrescentar no CI integridade relacional: `records ↔ corpus`, `pathos ↔ records`, `pathos ↔ corpus`, header do id-mapping, presença esperada de `regimes_visuais.yaml`.
8. Harmonizar codebook/LPAI e schemas operacionais para mesma escala de indicadores.
9. Atualizar Introdução, Cap.2, Cap.3, Cap.5 e Cap.6 para Claims Atuais vs Freezes Históricos.
10. Inserir no plano mensal a regra de encaixe do Elicit como backlog bibliográfico, não capacidade corrente.

## Decisões pendentes que exigem Ana

1. O N analítico do Cap.6/corpus quantitativo é 145, 165, 265 ou 280?
2. Os 3 “gaps” entre 15 e 12 são exclusão operacional legítima ou erro de contagem?
3. `regimes_visuais.yaml` deve existir como artefato produzido por pipeline ou ser removido das referências?
4. Qual branch/commit é a fonte de verdade para manuscrito/planos: o atual `feat/alegorias-piloto-v2` ou `feat/codebook-master-v2.2.0`?

## Métricas da auditoria

- relatórios lidos em disco: 4
- schema adherence: 4/4
- achados críticos confirmados em relatórios lidos: 10
- cross-domain findings com dependência explícita: 10
- arquivos modificados além dos relatórios: 0
