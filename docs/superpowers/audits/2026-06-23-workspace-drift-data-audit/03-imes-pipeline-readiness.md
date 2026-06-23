# Audit Report — IMES / pipeline readiness — auditoria de prontidão E1–E3
Escopo examinado: `/Users/ana/Research/hub/iconocracy-corpus/data/processed/pathosformel_index.jsonl`; `/Users/ana/Research/hub/iconocracy-corpus/data/processed/regimes_visuais.yaml`; `/Users/ana/Research/hub/iconocracy-corpus/docs/decisions/`; `/Users/ana/Research/hub/iconocracy-corpus/docs/pilots/`; `/Users/ana/Research/hub/iconocracy-corpus/tools/scripts/`; `/Users/ana/Research/hub/iconocracy-corpus/notebooks/`
Arquivos analisados: 136
Data: 2026-06-23

## Resumo executivo (≤5 linhas)
E1 existe como índice/status de 265 itens, mas não cobre o corpus canônico atual de 280 registros e só 44 linhas têm score visual completo.
E2 não usa `cluster_rv.py`: a execução real está nos notebooks estatísticos, sobretudo `notebooks/06_clustering.ipynb`, com figuras já derivadas.
`regimes_visuais.yaml` não existe no caminho auditado, apesar de constar no escopo esperado.
E3 existe apenas como prancha-piloto textual (`P01-republica-armada.md`), sem diretório/pipeline de pranchas reprodutíveis.
Para julho, o bloqueio principal é declarar/fixar o N analítico e o contrato de validade; automação fina pode ficar para depois.

## Achados — CRITICAL (bloqueante)
- [C-01] Contrato E1 não está alinhado ao corpus canônico atual · `tools/scripts/e1_mark_no_image.py:3-4` · O próprio script define E1 como fechamento de `pathosformel_index.jsonl` em 265 linhas; a medição atual mostra `pathosformel_index.jsonl` com 265 itens, mas `records.jsonl` e `corpus-data.json` com 280, deixando 15 registros canônicos fora do índice E1. Além disso, só 44/265 entradas têm `purificacao_composto` não nulo; 210 são `e1-uncoded`/backlog e 6 `e1-no-image`. Diagnóstico: E1 existe, mas é um ledger de status/backlog, não um E1 “codificado” pronto para sustentar análises do corpus atual. · Remediação: para julho, declarar explicitamente se o N analítico é o snapshot E1=265 ou o canônico=280; se for 280, acrescentar/triagem dos 15 registros faltantes antes de qualquer afirmação de completude.
- [C-02] E2 não está liberado para inferência por indicador cru · `docs/decisions/IRR-opus-gemini-PRO-2026-06-22.md:5-9` · O melhor relatório cross-instrumento direto do lote opus-4.8 mede N=14, α global=0,393 e “nenhum indicador atinge poolável (≥0,667)”; o mesmo documento conclui que indicadores são instrumento-dependentes e não devem ser poolados entre instrumentos (`docs/decisions/IRR-opus-gemini-PRO-2026-06-22.md:20-27`). Diagnóstico: E2 pode usar regime/composto com caveat, mas clusterização por vetor de 10 indicadores como evidência citável ainda é bloqueada sem estratificação/calibração. · Remediação: para julho, reportar E2 no nível regime/composto e tratar clusters de indicador como exploratórios; postergar claims por indicador cru até IRR real/estratificada.
- [C-03] CSV analítico pode ser contaminado se regenerado pela pipeline atual · `tools/scripts/code_purification.py:326-336` · `export_csv()` escreve todo item de `corpus-data.json` e apenas injeta codificação quando há match; não filtra por `coded_by` válido. A auditoria anterior já advertia que notebooks dependem de `corpus_dataset.csv` vir limpo e que regenerar a partir do corpus canônico importaria vetores all-zero/vault-import e migration (`docs/decisions/audit-coded-by-2026-06-10.md:73-79`). Diagnóstico: os notebooks 01–08 podem estar corretos no snapshot atual, mas a pipeline de regeneração não preserva automaticamente o contrato analítico. · Remediação: para julho, congelar o CSV usado nas figuras ou corrigir `--export-csv` com whitelist de instrumentos/`analytic_eligible` antes de qualquer rerun.

## Achados — MAJOR
- [M-01] `regimes_visuais.yaml` não existe no caminho do escopo · `data/processed/regimes_visuais.yaml:N/A` · Busca por arquivo exato e por `*regimes*` não encontrou `/data/processed/regimes_visuais.yaml`; também não há menção textual a `regimes_visuais` nos docs/scripts/notebooks auditados. Diagnóstico: qualquer plano que dependa desse YAML está apontando para artefato inexistente. · Remediação: para julho, remover a dependência do YAML ou substituir por fonte real (`regime_iconocratico` no CSV/índice); como melhoria posterior, criar YAML versionado de taxonomia visual.
- [M-02] `cluster_rv.py` não existe; E2 usa notebook, não script · `notebooks/06_clustering.ipynb:29-31` · A busca por `cluster_rv.py` e `*cluster_rv*` retornou zero arquivos. A lógica E2 real importa `AgglomerativeClustering`/`KMeans` no notebook e lê `../data/processed/corpus_dataset.csv` (`notebooks/06_clustering.ipynb:39-55`), salvando figuras `fig_10`–`fig_12` (`notebooks/06_clustering.ipynb:89-90`, `notebooks/06_clustering.ipynb:155-156`, `notebooks/06_clustering.ipynb:255-256`). Diagnóstico: há execução analítica, mas não há script reprodutível com nome esperado. · Remediação: para julho, documentar que E2 = notebooks 06/07/08 + CSV congelado; posterior técnico: extrair `cluster_rv.py` ou `cluster_regimes.py` como wrapper parametrizado.
- [M-03] Outputs derivados existem, mas a documentação de `data/processed/` não os reflete · `data/processed/README.md:7-11` · O README lista apenas `records.jsonl`, `corpus_dataset.csv` e `feminist_network_48C51_pt.json`, enquanto a medição encontrou 23 figuras `fig_*.png`, `subscores.csv`, `parallel_results.json`, `irr_sample_metadata.jsonl`, `irr_report.json` e artefatos IRR em subpastas. Diagnóstico: o workspace contém resultados prontos que podem ser reutilizados, mas planos/README podem induzir retrabalho ou sobrescrita. · Remediação: para julho, criar uma pequena tabela de “artefatos analíticos congelados” no dataset card/nota metodológica; posterior técnico: atualizar README com proveniência e comandos.
- [M-04] A enumeração de regimes é inconsistente entre ferramentas · `tools/scripts/code_purification.py:94` · `code_purification.py` só permite `fundacional`, `normativo`, `militar`, enquanto `csv_to_records.py`, `vault_sync.py`, `irr_sample.py` e `irr_rater2_batch.py` incluem `contra-alegoria`; `lacunas.py` também usa só três regimes (`tools/scripts/lacunas.py:31-33`). Diagnóstico: contra-alegoria aparece nos dados, no piloto e nos IRRs, mas parte da pipeline a perde ou não a amostra. · Remediação: para julho, não usar `code_purification.py` interativo/lacunas para decisões finais sem patch ou caveat; posterior técnico: centralizar enum de regimes.
- [M-05] Artefatos de IRR re-run existem, mas a saída de 23/06 é sintética e não probatória · `data/processed/irr_re_run/README.md:7-18` · O plano antigo marcava `irr_rater2_batch.py` e `irr_sample.py` como “Criar” (`docs/decisions/IRR-RE-RUN-DESIGN-2026-06-09.md:133-141`), mas hoje ambos existem. Porém o artefato `rater2_synthetic_baseline.jsonl` é explicitamente “NOT a real second coder” e “NOT ready for use as evidence”. Diagnóstico: infraestrutura E2/IRR está mais pronta que o plano diz, mas validação real ainda não está. · Remediação: para julho, usar `irr_report.json`/docs IRR citáveis e rotular sintético como teste de pipeline; posterior técnico: rodar rater-2 real.
- [M-06] E3 está em estado piloto textual, sem pipeline de pranchas · `docs/pilots/P01-republica-armada.md:10-13` · Existe `PRANCHA-P01` com `status: piloto`, mas não há `docs/pilots/pranchas/`; a própria prancha lista lacunas de verificação de frontispício, charges, medalhas e imagens (`docs/pilots/P01-republica-armada.md:317-325`) e termina como sequência provisória (`docs/pilots/P01-republica-armada.md:343-347`). Diagnóstico: E3 existe conceitualmente e é forte, mas ainda não é uma saída reproduzível/fechada. · Remediação: para julho, usar P01 como modelo e produzir pranchas manualmente com checklist de fontes; automação de renderização pode ficar para depois.

## Achados — MINOR
- [m-01] IMES não aparece como termo explícito no escopo auditado · `docs/decisions/DIALETICA-N165-vs-265.md:30-38` · A arquitetura conceitual existe como versionamento/estratos de validade, mas não há arquivo ou seção nomeada “IMES”. Diagnóstico: o domínio é operacionalmente reconhecível, mas a nomenclatura não está ancorada. · Remediação: acrescentar glossário curto no relatório metodológico, se o termo for usado com a banca.
- [m-02] `pathosformel_index.jsonl` tem 3 `sigla_id` duplicados · `data/processed/pathosformel_index.jsonl:N/A` · A medição encontrou 0 duplicatas de `item_id`, mas 3 duplicatas de `sigla_id`. Diagnóstico: não quebra o join por UUID, mas pode confundir pranchas/legendas se elas usam sigla. · Remediação: checar duplicatas antes de montar E3.
- [m-03] Os notebooks têm outputs embutidos e figuras salvas, mas não há manifesto de execução · `notebooks/08_multidimensional_scoring.ipynb:303-307` · O notebook 08 exporta `subscores.csv`, e os notebooks 01–08 salvam figuras, mas não há manifesto único com hash/data/input CSV. Diagnóstico: bom para trabalho exploratório; frágil para auditoria futura. · Remediação: posterior técnico: manifestar input, comando e hash dos outputs.
- [m-04] A decisão E1 dos 13 extras ainda é staging, mas o corpus canônico já avançou · `docs/decisions/E1-OPUS48-BATCH-2026-06-22.md:80-93` · O council recomenda não tocar `records.jsonl` antes da defesa e só promover via `analytic_eligible`, enquanto os arquivos atuais medidos têm 280 registros. Diagnóstico: há drift documental entre decisão e estado do workspace. · Remediação: atualizar dataset card com “decisão histórica” vs “estado atual”.

## Pontos fortes (o que NÃO mexer)
- Manter o audit trail honesto de E1: `e1_reclassify_no_image.py` separa backlog recuperável de no-image e preserva motivos (`tools/scripts/e1_reclassify_no_image.py:11-18`).
- Manter a separação por instrumento/coorte: a decisão E1 já recomenda `coded_by` + `analytic_eligible`, não ledger paralelo (`docs/decisions/E1-OPUS48-BATCH-2026-06-22.md:84-92`).
- Manter P01 como modelo de prancha: ela explicita Pathosformel, regime iconocrático, contrato visual, lacunas e proveniência em um formato útil para E3 (`docs/pilots/P01-republica-armada.md:59-73`).
- Manter `compute_irr.py`: ele já suporta rater-2, relatório por indicador, bootstrap e raw pairs (`tools/scripts/compute_irr.py:9-17`).
- Não apagar figuras `fig_01`–`fig_18` nem `subscores.csv`: são outputs derivados já existentes e úteis como evidência exploratória/congelada.

## Métricas mensuradas
- arquivos encontrados no escopo: 188
- arquivos analisados sem `__pycache__`: 136
- `pathosformel_index.jsonl`: 265 linhas / 265 itens
- `records.jsonl`: 280 linhas / 280 itens
- `corpus/corpus-data.json`: 280 itens
- join `pathosformel_index.item_id` ∩ `records.item_id`: 265; `pathos-only`: 0; `records-only`: 15
- `pathosformel_index` por `coded_by`: `e1-uncoded` 210; `fable-5` 49; `e1-no-image` 6
- `pathosformel_index` com `purificacao_composto` não nulo: 44/265
- `pathosformel_index` por regime: `normativo` 21; `fundacional` 13; `militar` 8; `contra-alegoria` 2; nulo 221
- `pathosformel_index` com todos indicadores nulos: 221/265
- entradas sem score e sem `motivo_exclusao`: 0
- duplicatas: `item_id` 0; `sigla_id` 3
- `regimes_visuais.yaml`: ausente no caminho auditado
- `cluster_rv.py`: 0 ocorrências por nome exato ou parcial
- `docs/pilots/pranchas/`: ausente
- notebooks analíticos: 8 (`01_exploratory`–`08_multidimensional_scoring`)
- figuras derivadas em `data/processed/fig_*.png`: 23
- outputs derivados adicionais presentes: `subscores.csv`, `parallel_results.json`, `irr_sample_metadata.jsonl`, `irr_report.json`, `irr_re_run/rater2_synthetic_baseline.jsonl`, `irr_reports/irr_report_synthetic-baseline_2026-06-23.json`
- E1 — source input: sim (`records.jsonl`/`corpus-data.json`); script: sim (`e1_mark_no_image.py`, `e1_reclassify_no_image.py`); output: sim (`pathosformel_index.jsonl`); validation: parcial (motivos completos, mas 15 registros canônicos fora); docs: sim (`E1-*`).
- E2 — source input: sim (`corpus_dataset.csv`, `purification.jsonl`, IRR samples); script: parcial (notebooks + IRR scripts, sem `cluster_rv.py`); output: sim (`fig_10`–`fig_12` e demais figuras); validation: parcial/não liberada para indicador cru; docs: sim (`IRR-*`, `DIALETICA-*`).
- E3 — source input: parcial (P01 tem objetos/fontes, mas há lacunas); script: não encontrado; output: piloto textual (`P01-republica-armada.md`); validation: lacunas explícitas; docs: sim, mas sem diretório de pranchas.

## Dependências inter-domínio
- E1 depende de governança de corpus: a decisão de N analítico conflita com o drift `pathos=265` versus `records/corpus=280`.
- E2 depende de validação IRR e de dados: notebooks dependem de `corpus_dataset.csv` limpo; `code_purification.py --export-csv` pode conflitar com esse contrato.
- E2 depende de metodologia estatística: regime/composto são mais robustos que indicadores crus; isso condiciona o tipo de claim no Cap. 6.
- E3 depende de E1 para item_id/sigla/proveniência e de E2 para regimes/clusters; se E2 for exploratório, pranchas devem ser apresentadas como argumento curatorial, não como output automático de cluster.
- E3 depende de infraestrutura de imagem/fonte: P01 ainda requer verificação de frontispício, charges e imagens diretas antes de prancha final.
- O dataset card depende de todos os domínios: precisa declarar ledger canônico, N analítico, estratos de instrumento, outputs congelados e limitações de IRR.

## Recomendações priorizadas (top 5)
1. **Necessário para julho:** congelar e declarar o contrato analítico: “ledger canônico atual = 280; índice E1/pathos = 265; N quantitativo válido = X por whitelist/estrato”. Sem isso, E1/E2/E3 continuam falando números diferentes.
2. **Necessário para julho:** não regenerar `corpus_dataset.csv` pela pipeline atual sem corrigir filtro; se houver rerun, aplicar whitelist `coded_by`/`analytic_eligible` e incluir `contra-alegoria` nas enums.
3. **Necessário para julho:** formular E2 como análise exploratória robusta no nível de regime/composto, evitando claims por indicador cru poolado; usar os relatórios IRR citáveis para justificar o caveat.
4. **Necessário para julho:** produzir pranchas E3 a partir do modelo P01 com checklist manual de fonte/imagem/legenda/lacunas; não esperar por automação nem por `regimes_visuais.yaml`.
5. **Melhoria técnica posterior:** criar `regimes_visuais.yaml` e um script `cluster_rv.py`/`build_pranchas.py` reprodutível, com manifesto de input/output/hashes, depois que o corpus da defesa estiver estabilizado.
