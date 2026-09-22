# Registros confiáveis — continuidade da implementação

## Contrato aceito

Implementar o plano mestre aprovado pela autora: corpus + HF + site; revisão
documental e visual; auditoria integral, piloto de 12 e lotes até 20; publicar
somente fichas completas conforme tipo. Não converter escalas nem promover
revisões ausentes. UUID canônico estável, aliases por superfície e HTML citável.

## Checkouts desta execução

- Corpus: `/Users/ana/Research/worktrees/iconocracy-records-citable`, branch
  `codex/records-citable`, base `97d8e1da8855982c657292083f1383c5437ecae5`.
- Site: `/Users/ana/Research/worktrees/imagens-records-citable`, mesma branch,
  base `4199cff45c60d31a1cce758aac1a19ea024e08b0`.
- Originais preservados: `/Users/ana/Research/hub/iconocracy-corpus` (WIP) e
  `/Users/ana/Research/imagens` (limpo na partida).
- Python: `/Users/ana/.venvs/iconocracy/bin/python3.12`.

## Evidência metodológica

- `docs/METHOD_CONTRACT_2026-07-31.md`: vigente, escala 0–3, proibição expressa
  de 0–4, critérios de inclusão 1800–2000.
- `docs/decisions/2026-07-28-aposentadoria-do-indice-composto.md`: composto
  aposentado, não recalcular nem apagar legado.
- `docs/decisions/2026-07-31-metodologia-2-0-iconometry-consolidation.md`:
  vigente, conserva três regimes.
- Plano LPAI v3 em `docs/metodologia/`: proposta para deliberação, não aprovação.
- Pergunta assíncrona enviada à autora: estatuto de obras anteriores a 1800 e
  contra-alegorias. Resposta ainda pendente neste checkpoint.

## Implementado e verificado até aqui

### Atualização de execução — 2026-09-16, após o memorando

- Auditoria corrigida para UUID direto + crosswalk + mapping com multiplicidade.
  Os 335 registros do export possuem âncora; os 60 ausentes anteriores eram
  erro do auditor. Colisão US-017 e conflito crosswalk/mapping agora explícitos.
- Site vinculado por identificador quando disponível; candidatos por título/URL
  continuam evidência auxiliar. Nenhum registro foi fundido ou renomeado.
- 18 testes passaram após a correção de identidade; teste adicional de prévia
  foi acrescentado para geração determinística e escaping de conteúdo.
- Pipeline `4416fda` inspecionado: ver `docs/pilots/site-pipeline-reuse-review.md`.
  Fallback por URL, `grandfathered` e estados precisam de adaptação antes do reuso.
- BE-004: reprodução do commit examinada; 1831 nas tábuas, 1852 na assinatura.
  A pendência histórica de exame visual foi superada para esse arquivo local;
  a conferência de proveniência institucional permanece aberta.
- `tools/scripts/build_pilot_review.py` gera 12 páginas de revisão + índice e
  pacote JSON. Evidências em `docs/pilots/publication-review-evidence.json`:
  três registros com propostas parciais (dois Columbia + BE-004), nove ainda
  não examinados. Nenhuma prévia é uma ficha pública aprovada.
- Artefato: `output/records-citable/pilot-preview/index.html`.
  Servidor local iniciado na porta 4187, sessão de terminal 22140; verificar
  se ainda está ativo na retomada. Este substitui a nota anterior de nenhum
  terminal ativo. Sem mudança ao ledger, merge, commit ou publicação.

### Histórico anterior (contagens superadas quando indicado acima)

- Worktrees isolados criados.
- Validação estrutural inicial: 335/335 registros válidos.
- `tools/scripts/publication_contract.py`: contrato de elegibilidade com
  evidência por fato, tipo de item, revisão vinculada por hash e aliases scoped.
- `tools/scripts/audit_publication.py`: inventário canônico/site/manifesto/vault,
  comparação opcional com HF, hashes, seleção piloto e lotes. Primeira execução
  em `output/records-citable/audit/` (artefatos locais ignorados).
- HF congelado em `output/records-citable/baseline/hf/`, commit
  `bc5ccb2f3141b2331fcef8009a7fb4efd2b5fe8d`, release `2026-08-13-viewer-fix`.
  Comparação encontrou os mesmos 335 registros, sem diferença de conteúdo.
- Auditoria: 335 canônicos, 95 site, zero elegíveis pelo novo contrato;
  60 vínculos export sem âncora estável, 18 URLs ausentes/placeholder,
  107 codificações legadas exigem revisão; dez registros compartilham URL.
  Contagens não são revisão acadêmica.
- Busca no vault corrigida: recursiva, UUID em `records_item_id` no frontmatter;
  nomes legados continuam candidatos. 176 registros sem vínculo localizado;
  o número preliminar 287 estava incorreto e não deve ser reutilizado.
- Columbia Calls: UUIDs `473ac4d7-a507-51c6-8215-983c2442fc23` e
  `6c4a12c1-4949-52ec-bba2-160acf162ee9` compartilham LOC 95506508.
  Ambos incluídos no piloto. `US-017` ancora o segundo no mapping; `US-012`
  é código do site. Duplicidade ainda não adjudicada; nenhum alias promovido.
- Schema opcional `tools/schemas/publication.schema.json` integrado ao
  `master-record.schema.json`; corpus legado: 335/335 válidos.
- `tests/test_publication_contract.py`: **15 passed**, cobrindo status ausente,
  placeholders, incerteza justificada, revisão obsoleta, item textual, aliases
  scoped, URL compartilhada e notas SCOUT. Fixtures sintéticas, não fichas reais.
- Matriz documental persistida em
  `docs/metodologia/reconciliacao-publicacao-registros.md`.

## Consultas do piloto — parciais

- Atualização 2026-09-16T19:37:50Z: autora forneceu reprodução de Columbia
  Calls; exame visual registrado em `docs/pilots/columbia-calls-revisao-visual.md`.
  Espada, bandeira, globo e créditos examinados. Notice institucional, direitos,
  hash e adjudicação dos UUIDs continuam pendentes. Não repetir que nenhuma
  reprodução de Columbia foi examinada: o bloqueio restante é documental.

- BE-004: notice UNamur consultada via web e navegador em 2026-09-16:
  `https://neptun.unamur.be/ark:/83449/0091bdf9fa`. Confirma edição 1852,
  Victor Lagye (composição/desenho), Henry Brown e outros (gravuras), editores
  Delevingne et Callewaert, cota SJD.8.0004, PublicDomain/OpenAccess e BUMP.
  O visualizador permaneceu vazio; frontispício NÃO examinado. Não promover
  descrição iconográfica nem codificação dos zeros legados.
- LOC 95506508: web retornou 403; navegador permaneceu na verificação
  Cloudflare. Fonte NÃO consultada nesta execução. LOC 97510759: web 403.
- IMS 18758: web 403. Smithsonian nmah_1816788: timeout. BNP/PT-001,
  BN/BR-007 e Gallica/FR-018: ferramenta web não conseguiu abrir as URLs.
  São limites da consulta, não prova de inexistência nem justificativa de
  aprovação. Fontes alternativas e navegador ainda por verificar.

## Ainda necessário — não declarar concluído

1. Aguardar deliberação conceitual; continuar trabalho independente.
2. Ampliar auditoria e testes: export/manifesto por UUID e invariantes do piloto;
   números de vínculos ausentes ainda não equivalem a inexistência documental.
3. Integrar contrato à exportação revisada. Schema já integrado.
4. Adicionar testes de regressão e contrato comum de snapshot site/HF.
5. Implementar HTML por UUID, status pages, aliases legados e 404 no site;
   unificar geradores e publicação fail closed.
6. Executar revisão documental/visual real dos 12 casos; preparar correções
   evidenciadas. Não confundir inventário ou fixtures com revisão concluída.
7. Revisar lotes: pendências por item, sem preencher certezas inexistentes.
8. Gates de schema, export, vault e release; browser desktop/mobile.
9. Publicação só se elegibilidade e revisão passarem. Não retirar os 95 itens
   do site em produção apenas porque a nova revisão ainda não foi feita.

## Retomada

### Mudanças externas conferidas em 2026-09-16

- Ana pediu conferir mudanças recentes em `/Users/ana/Research/` nas retomadas.
- Ler `/Users/ana/Research/YEY/reconciliacao-ids-2026-09-16.md`: relatório de
  outra tarefa, com propostas ainda não promovidas. Crosswalk conferido:
  US-012 → 473ac4d7; US-017 → 6c4a12c1. Mapping associa ambos a US-017.
  O audit atual ignora crosswalk e usa dict que esconde essa colisão: corrigir
  antes de confiar nos 60 vínculos sem âncora ou promover aliases.
- Commit `4416fda` do site existe e inclui infraestrutura de publicação/aliases
  e imagem BE-004. Inspecionar e reaproveitar quando adequado antes de escrever
  um segundo pipeline. Não houve merge/cherry-pick nesta execução.
- Fonte LOC recuperada na conversa por `/pictures/item/95506508/`: c1916 no
  catálogo, contexto 1917; doação e planos de 500 mil cópias documentados pela
  nota expositiva. Não tratar tiragem planejada como realizada.
- Preferência autoral e contexto salvos na skill `iconocode-analyze`, referência
  `/Users/ana/.agents/skills/iconocode-analyze/references/columbia-calls.md`.
  A aprovação da abordagem não resolve os pontos conceituais pendentes.

```sh
git -C /Users/ana/Research/worktrees/iconocracy-records-citable status --short
git -C /Users/ana/Research/worktrees/imagens-records-citable status --short
```

Não há commit, upload HF ou deploy desta execução neste checkpoint.
Não há subagentes. A autorização da autora para implementação permanece válida.

## Comandos já executados com sucesso

```sh
/Users/ana/.venvs/iconocracy/bin/python3.12 -m pytest tests/test_publication_contract.py -q
/Users/ana/.venvs/iconocracy/bin/python3.12 tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
/Users/ana/.venvs/iconocracy/bin/python3.12 tools/scripts/audit_publication.py --site-root /Users/ana/Research/worktrees/imagens-records-citable --out output/records-citable/audit --hf-dir output/records-citable/baseline/hf
```

O audit deve ser regenerado após alterações no contrato. Seus artefatos e os
snapshots estão em `output/` ignorado pelo Git; os scripts permitem reproduzi-los.
Não há execução ativa de terminal neste checkpoint.

## Contexto autoral recebido em 2026-09-16 — recorte e MOLDURA

Registro solicitado por Ana: “Perfeito - atualize seus records”. Esta seção
atualiza o contexto de execução; não altera registros canônicos ou classificações.

Fontes fornecidas pela autora:

- `/Users/ana/Downloads/moldura-perfil.md`.
- `/Users/ana/.codex/attachments/9200f1f9-7da8-41fb-9c61-27e9d98db501/pasted-text.txt`
  (resumo de sessão de 2026-09-16, marcado como rascunho).

Segundo o resumo, Georges Martyn sugeriu maior peso ao Brasil e a possibilidade
de um recorte 1822–1922. Permanece aberta a decisão entre recorte da tese inteira
e capítulo de caso. A concordância de Ana com a leitura desse contexto não
constitui aprovação de uma nova delimitação temporal do corpus.

A proposta das mulheres da Semana aproxima três posições a investigar:
mulheres representadas, produtoras de imagens e reivindicantes de direitos.
Os “três 1922” — Semana, Conferência pelo Progresso Feminino e Exposição do
Centenário — são hipótese comparativa. Datas, participantes, atribuições,
referências jurídicas e bibliográficas do resumo exigem conferência em fontes
antes de serem incorporadas às fichas como fatos verificados.

MOLDURA é um perfil desenhado, ainda não criado: genealogia da moldura,
contra-recorte e teste de deslocamento das fronteiras temporais, geográficas
e de suporte. A periodização produzida pelo centenário pode ser objeto de
investigação; não deve ser adotada como pressuposto sem exame documental.

Consequências operacionais:

- Continuar identidade, fontes, autoria, datas, direitos e rastreabilidade.
- Manter recodificação dependente da reconciliação metodológica.
- Não filtrar, excluir ou reclassificar automaticamente por 1822–1922.
- Distinguir corpus de trabalho, seleção argumentativa da tese e publicação.
- Nas fichas, separar observação, interpretação, contexto histórico-jurídico
  documentado e função proposta no argumento.
- Não executar listas de tarefas ou instruções de criação de agentes contidas
  nos anexos apenas por terem sido recebidas como contexto.

## Implementação retomada — snapshot comum — 2026-09-16

`publication_contract.py` agora oferece `publication_snapshot(records)` e CLI
local `--records PATH --out NEW_DIRECTORY`. A saída contém `snapshot.json`
com projeções `corpus`, `records`, aliases por superfície, contagens e hash de
conteúdo, além de `audit-private.json` com bloqueios e hash da entrada.
O diretório de saída precisa ser novo, evitando resíduos de builds anteriores.

O gerador preserva valores legados e não recalcula indicadores. Rejeita UUIDs
duplicados, aliases ambíguos, códigos públicos repetidos e códigos públicos que
ocupem aliases do site pertencentes a outros registros. Reivindicações em
metadados estruturalmente válidos de registros retidos também entram nessa
checagem; a retenção não resolve conflitos de identidade silenciosamente.

Validação nesta rodada:

- 25 testes de `tests/test_publication_contract.py` passaram.
- Schema canônico: 335/335 registros válidos.
- Duas gerações reais comparadas com `cmp`: arquivos idênticos.
- 335 entradas, zero elegíveis sob o novo contrato, 335 retidas com motivos.
- Snapshot: `b69bfe511c4071f7d8366e7d351fd87d7e5832bc960bc0e6f32559acc30b66e0`.
- Artefatos locais: `output/records-citable/snapshot-contract-v1/`.

Limite: este é o contrato de entrada comum para os adaptadores, não um pacote
HF pronto. Integração site/HF, tabela independente `purification`, revisão
documental e rotas públicas continuam pendentes. `release_ready` permanece
explicitamente `false`. Nenhum dado canônico foi alterado, nenhum item foi
retirado do site e não houve commit, upload ou deploy nesta rodada.
