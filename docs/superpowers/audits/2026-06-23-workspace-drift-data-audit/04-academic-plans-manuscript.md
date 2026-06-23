# Audit Report — Academic plans / manuscript consistency — lente planos acadêmicos + manuscrito
Escopo examinado: `/Users/ana/Research/plans/2026-07-01-july-plan.md`; `/Users/ana/Research/plans/2026-07-06-biweekly-imes-pranchas.md`; `/Users/ana/Research/hub/iconocracy-corpus/tese/manuscrito/`; `/Users/ana/Research/hub/iconocracy-corpus/vault/tese/`; `/Users/ana/Research/hub/iconocracy-corpus/docs/plans/`; `/Users/ana/Research/hub/iconocracy-corpus/docs/research/elicit/`
Arquivos analisados: 91
Data: 2026-06-23

## Resumo executivo (≤5 linhas)
Os planos de julho já refletem o Cap.1 consolidado e a mudança principal para corpus 280 / pathosformel 265, mas repetem um erro operacional: 265/280 implica 15 lacunas, não 12.
O manuscrito e o vault ainda carregam números obsoletos de alto risco: N=145, 165 e 265 aparecem em passagens substantivas de Introdução, Cap.2, Cap.3, Cap.5 e Cap.6.
O Cap.1 está consolidado no estado ativo e bate com `wc -w` dos planos (4.949 palavras); o Cap.6 no branch ativo mede 1.476 palavras, não 1.448.
Elicit e plano do dia foram salvos de modo rastreável, mas ainda não foram absorvidos no plano mensal como fila bibliográfica delimitada.
A auditoria encontrou 0 ocorrências textuais de 278 no escopo; o dado verificável atual é corpus 280 e pathosformel 265.

## Achados — CRITICAL (bloqueante)
- [C-01] Contagem de lacunas E1 aritmeticamente incorreta nos planos executivos · `/Users/ana/Research/plans/2026-07-01-july-plan.md:26` e `/Users/ana/Research/plans/2026-07-06-biweekly-imes-pranchas.md:15` · Os planos dizem “265/280 (12 gaps)”, mas a verificação dos dados mostrou `records.jsonl=280`, `corpus-data.json=280` e `pathosformel_index.jsonl=265`; portanto faltam 15 entradas por `item_id` em relação ao ledger, não 12. Isso bloqueia a execução limpa do dia 07-06 porque a tarefa “gerar lista dos 12 itens” pode deixar 3 itens fora do fechamento E1. · Remediação proposta: corrigir todos os “12 gaps” dos planos para “15 gaps (280−265)” ou, se houver uma regra de exclusão que reduza 15→12, explicitá-la com lista dos 3 itens excluídos e critério.

## Achados — MAJOR
- [M-01] Cap.6 ativo ainda narra o corpus antigo como se fosse corpus atual · `/Users/ana/Research/hub/iconocracy-corpus/vault/tese/capitulo-6.md:21` · O capítulo afirma “145 artefatos visuais codificados integralmente” e as estatísticas seguintes dependem desse congelamento antigo; isso colide com os planos que exigem §6.1 atualizado para corpus 280 e com o estado verificado de 280 registros / 265 pathosformel. · Remediação proposta: reescrever §6.1 separando “freeze estatístico N=145” de “corpus atual N=280 / E1=265”, e marcar Kruskal-Wallis, OLS e MCA como pendentes de re-run antes de narrar resultado como atual.
- [M-02] Manuscrito corrente contém números obsoletos de corpus em seções argumentativas · `/Users/ana/Research/hub/iconocracy-corpus/tese/manuscrito/Introducao_rev.md:127`, `/Users/ana/Research/hub/iconocracy-corpus/tese/manuscrito/Capitulo2_metodologia.md:66`, `/Users/ana/Research/hub/iconocracy-corpus/tese/manuscrito/Capitulo3_analise_quantitativa.md:14` · A Introdução e Cap.2 ainda dizem “165 itens / 154 com codificação”; Cap.3 diz “265 registros (165 núcleo + 100 sincronização)”. Como essas passagens definem objetivo, método e panorama quantitativo, o risco é alto: elas podem contradizer imediatamente os planos atualizados e o corpus 280. · Remediação proposta: substituir afirmações de estado atual por formulação versionada: “corpus público atual: 280; índice pathosformel atual: 265; análises inferenciais anteriores: freeze N=145/165, a revalidar”.
- [M-03] Cap.5, Introdução e Conclusão do vault preservam N=145 como base empírica da tese · `/Users/ana/Research/hub/iconocracy-corpus/vault/tese/capitulo-5.md:31`, `/Users/ana/Research/hub/iconocracy-corpus/vault/tese/introducao.md:28`, `/Users/ana/Research/hub/iconocracy-corpus/vault/tese/conclusao.md:19` · Essas passagens fazem mais do que registrar histórico: elas apresentam 145 peças como evidência empírica do argumento. Isso é aceitável apenas se rotulado como “congelamento analítico anterior”; sem rótulo, conflita com o plano mensal e com a hierarquia atual de dados. · Remediação proposta: classificar cada ocorrência como “freeze antigo”, “rascunho arquivado” ou “claim atual”; só atualizar claims atuais, mantendo históricos quando forem explicitamente documentais.
- [M-04] Plano do dia/Elicit ainda não está encaixado na capacidade do plano mensal · `/Users/ana/Research/hub/iconocracy-corpus/docs/plans/2026-06-23-elicit-research-and-thesis-governance-plan.md:152` e `/Users/ana/Research/plans/2026-07-01-july-plan.md:83` · O plano do dia cria tarefas de tese sobre fila bibliográfica Brasil/França/Grã-Bretanha e compressão, enquanto julho exclui expansão de Cap.2–5 e foca E1/E2/Cap.6/image-store. Não há colisão factual, mas há colisão de capacidade se as leituras Elicit entrarem em julho sem troca explícita de escopo. · Remediação proposta: no plano mensal, adicionar regra de governança: “Elicit 2026-06-23 fica como backlog bibliográfico/Horizonte 2; só entra em julho se substituir tarefa de E2/Cap.6 ou alimentar nota curta do capítulo Brasil”.
- [M-05] Estado de branch observado difere do contexto operacional recebido · `<git-state>:n/a` · O contexto mencionava branch ativo `feat/codebook-master-v2.2.0` e commit `6d427b9`; a verificação local encontrou subrepo em `feat/alegorias-piloto-v2`, `HEAD=5f06c87`, com histórico de `Capitulo1_rev.md` contendo `b4a6006 tese(cap1): consolidar Cap. 1...`. O Cap.1 consolidado está presente, mas o identificador de branch/commit não coincide. · Remediação proposta: antes de editar planos/manuscrito, registrar no próximo handoff qual branch é a fonte de verdade para tese/manuscrito e se `b4a6006` corresponde ao commit esperado no histórico local.

## Achados — MINOR
- [m-01] Word count de Cap.6 no plano está levemente defasado · `/Users/ana/Research/plans/2026-07-01-july-plan.md:17` e `/Users/ana/Research/plans/2026-07-06-biweekly-imes-pranchas.md:17` · Os planos registram Cap.6 com 1.448 palavras, mas o estado ativo medido por `wc -w` é 1.476 palavras. O desvio é pequeno, mas deve ser corrigido para manter métricas reproduzíveis. · Remediação proposta: atualizar a métrica para “1.476 palavras (`wc -w`, branch ativo em 2026-06-23)” ou fixar outro método único.
- [m-02] Planos antigos e notas do vault ainda aparecem em buscas de números obsoletos · `/Users/ana/Research/hub/iconocracy-corpus/vault/tese/plano-capitulos-2026-04-11.md:16`, `/Users/ana/Research/hub/iconocracy-corpus/tese/manuscrito/notas/Cap3_quantitativo_outline.md:4` · Esses arquivos provavelmente são históricos, mas aparecem no mesmo espaço textual da tese e podem contaminar buscas/recuperação por agentes. · Remediação proposta: sem reescrever conteúdo histórico, acrescentar futuramente cabeçalho “arquivo histórico — não usar como estado atual” se esses documentos continuarem no vault operacional.
- [m-03] Busca regex encontrou falsos positivos bibliográficos para 145 · `/Users/ana/Research/hub/iconocracy-corpus/vault/tese/rascunhos-artigos/Imagens_da_Nacao.md:294` e `/Users/ana/Research/hub/iconocracy-corpus/vault/tese/metodologia/capitulo-2-reescrito.md:63` · Algumas ocorrências de 145 são páginas de referências (ex.: p. 120–145, p. 123–145), não claims de corpus. · Remediação proposta: não fazer substituição global; filtrar por contexto semântico (“corpus”, “N=”, “itens”, “peças”, “registros”).
- [m-04] Cap.1 consolidado está correto, mas o backup pré-consolidação permanece próximo ao arquivo ativo · `/Users/ana/Research/hub/iconocracy-corpus/tese/manuscrito/Capitulo1_rev_v1pre-consolidacao.md:1` · O backup é útil, porém buscas por Cap.1 podem retornar duas versões. · Remediação proposta: manter o backup, mas tratá-lo como leitura histórica; não usar em métricas de progresso salvo quando a comparação pré/pós-consolidação for intencional.

## Pontos fortes (o que NÃO mexer)
- Não reabrir Cap.1 em julho: os planos já o tratam como consolidado e a medição `wc -w` confirma 4.949 palavras no arquivo ativo.
- Manter a regra “não inventar números no Cap.6”: ela aparece no plano mensal e no biweekly e é exatamente a proteção necessária contra os freezes N=145/165.
- Manter Elicit como descoberta, não bibliografia final: o relatório avisa que metadados devem ser verificados em Zotero/DOI/editoras antes de citação.
- Manter o foco mensal em E1→E2→Cap.6→image-store: a estrutura é coerente com o estado real, desde que a contagem de gaps seja corrigida.
- Manter os arquivos Elicit Markdown + JSON e o plano do dia como trilha de governança; eles estão rastreáveis e não expõem a chave API em arquivo versionado.

## Métricas mensuradas
- método de word count: `wc -w` aplicado de forma consistente aos capítulos relevantes no estado ativo de 2026-06-23.
- arquivos textuais analisados no escopo: 91 (2 planos externos; 11 em `tese/manuscrito`; 69 em `vault/tese`; 7 em `docs/plans`; 2 em `docs/research/elicit`).
- branch observado em `/Users/ana/Research/hub/iconocracy-corpus`: `feat/alegorias-piloto-v2`, `HEAD=5f06c87`.
- `tese/manuscrito/Capitulo1_rev.md`: 4.949 palavras (`wc -w`).
- `tese/manuscrito/Capitulo1_rev_v1pre-consolidacao.md`: 3.238 palavras (`wc -w`).
- crescimento Cap.1 pós-consolidação: +1.711 palavras versus backup pré-consolidação (`wc -w`).
- `tese/manuscrito/Introducao_rev.md`: 5.364 palavras (`wc -w`).
- `tese/manuscrito/Capitulo2_metodologia.md`: 2.938 palavras (`wc -w`).
- `tese/manuscrito/Capitulo3_analise_quantitativa.md`: 552 palavras (`wc -w`).
- `vault/tese/capitulo-6.md`: 1.476 palavras (`wc -w`).
- `corpus/corpus-data.json`: 280 itens.
- `data/processed/records.jsonl`: 280 linhas / 280 `item_id` únicos.
- `data/processed/pathosformel_index.jsonl`: 265 linhas / 265 `item_id` únicos.
- diferença `records.jsonl` menos `pathosformel_index.jsonl`: 15 `item_id` sem entrada no índice pathosformel.
- Elicit raw JSON: 5 buscas, 40 registros retornados, 5 status HTTP 200, quota restante final 89.
- busca regex `\b(145|165|265|278|280)\b` no escopo textual: 62 linhas com ocorrência; contagem bruta por valor = 145: 25, 165: 16, 265: 14, 278: 0, 280: 38.

## Dependências inter-domínio
- [C-01] depende do domínio de dados/corpus: a correção “12→15 gaps” deve ser validada contra a lista material de `records.jsonl` versus `pathosformel_index.jsonl` antes de execução E1.
- [M-01] e [M-02] dependem do domínio estatístico/notebooks: Cap.6 só pode trocar N=145/165 por N=280 em resultados inferenciais depois de re-run rastreável.
- [M-04] depende do domínio bibliografia/Zotero: Elicit deve alimentar fila verificável, não citação direta nem expansão silenciosa do escopo mensal.
- [M-05] depende do domínio git/governança de branches: a auditoria confirma o arquivo ativo, mas a divergência de branch/commit precisa ser resolvida antes de qualquer edição coordenada.
- Image-store e E3 dependem do domínio acervos/imagens: os planos corretamente limitam o esforço a 4 seeds + 30 prioritárias, mas isso deve permanecer separado da correção de corpus/pathos.

## Recomendações priorizadas (top 5)
1. Corrigir nos planos a aritmética E1: trocar “12 gaps” por “15 gaps (280−265)” ou documentar formalmente por que 3 itens não contam como gap operacional.
2. Antes de expandir Cap.6, criar uma tabela de estado dos números: `N=145` = freeze estatístico antigo; `165/154` = ledger intermediário; `265` = pathosformel atual; `280` = corpus/records atual.
3. Revisar Introdução, Cap.2, Cap.3, Cap.5 e Cap.6 para que nenhuma frase diga “estado atual” com 145, 165 ou 265 como corpus total.
4. Inserir no plano mensal uma cláusula de encaixe para Elicit: backlog bibliográfico verificado, sem consumir capacidade de julho salvo troca explícita com E2/Cap.6.
5. Registrar no próximo handoff o branch/commit fonte de verdade e o método `wc -w`, atualizando a métrica de Cap.6 para 1.476 palavras no estado ativo.
