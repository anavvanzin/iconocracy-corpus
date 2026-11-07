# Workflow Operacional

Workflow curto para tocar a tese sem perder tempo com drift de estrutura, Git ou release.

## Critério metodológico transversal — vínculos do objeto

Aplicar o [critério de atribuição territorial, política e institucional, v1.0](methodology/atribuicao-territorial-politica-institucional.md)
em toda frente da tese, inclusive artigos. Cada associação usada deve ter
relação precisa, fonte e alcance declarados, com data/jurisdição quando
pertinentes. Autoria, produção, guarda, tema, encomenda, circulação e recepção
não se substituem nem produzem nacionalidade única do objeto. Verificar as
dimensões pertinentes à afirmação, sem exigir ficha integralmente preenchida.

| Momento | Controle a realizar |
|---|---|
| Seleção/busca | Tratar país de campanha, tema e acervo como pistas; justificar a relação com Brasil e a cronologia de cada caso usado no núcleo 1822–1922. |
| Catalogação | Qualificar os vínculos documentados nos claims e ledger existentes; preservar valor legado, incerteza e fonte. `gap` permite entrada/permanência no catálogo. |
| Análise/montagem | Separar registro documental, filologia conceitual e hipótese iconológica; demonstrar o fundamento da comparação e de eventual transferência. |
| Redação/revisão | Conferir se cada formulação nacional, política ou institucional diz apenas o que sua evidência autoriza; hipótese qualificada permanece hipótese. |
| Exportação/apresentação | Explicitar a semântica de país e as ambiguidades; filtros e derivados não comprovam nacionalidade nem pertencimento ao núcleo. |

Na revisão semanal, manter [fila não destrutiva de auditoria](research/auditoria-atribuicoes-territoriais-2026-10-29.md)
por ID, formulação/valor legado, fundamento, lacuna, correção proposta e
estado/decisão. Priorizar itens usados na escrita. Falta de fonte não prova
ausência histórica; autoria estrangeira não exclui vínculo brasileiro
documentado. Não reclassificar, excluir ou renomear objetos automaticamente.

## Regra-mestra

- Trabalhe em checkout identificado de `anavvanzin/iconocracy-corpus`, conferindo raiz, remote, HEAD e alterações locais antes de editar; use branch isolado para a revisão.
- Confirme o caminho local com `git rev-parse --show-toplevel`. Os antigos paths `/Users/ana/Research/...` são referências de outra máquina.
- Considere `records.jsonl` a fonte de identidade/evidência/claims e `purification.jsonl` a fonte de observações/proveniência de codificação (ADR-006); `corpus-data.json` é export público e `vault/` é espelho de trabalho.
- Não trate Hugging Face como working copy
- Não trate o vault como fonte primária de verdade

## Rotina diária

1. Entrar no ambiente e checar o estado do repo

```bash
cd /caminho/confirmado/iconocracy-corpus
conda activate iconocracy
git status --short
```

2. Confirmar qual frente está ativa

- `corpus/`: intake, reconciliação e descrição pública
- `data/processed/`: verdade operacional e codificação
- `vault/`: notas, sessões e manuscrito
- `docs/` e `tools/`: infraestrutura e método

3. Se mexer em notas do vault, checar primeiro o espelho

```bash
python tools/scripts/vault_sync.py status
```

4. Se entrar item novo no corpus, seguir esta ordem

- registrar ou revisar em `data/processed/records.jsonl`
- verificar impacto em `corpus/corpus-data.json`
- complementar nota em `vault/candidatos/` se necessário
- só depois pensar em publicação

5. Encerrar o dia com uma checagem curta

```bash
git status --short
python tools/scripts/code_purification.py --status
```

## Rotina semanal

1. Reconciliação de estrutura

```bash
find . -mindepth 2 -maxdepth 2 -name .git
```

Objetivo: garantir que não reapareceu repo aninhado dentro do hub.

2. Reconciliação de dados

```bash
python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
python tools/scripts/records_to_corpus.py --diff
python tools/scripts/code_purification.py --status
python tools/scripts/vault_sync.py status
```

Objetivo: ver drift entre ledger, export público e vault antes de acumular dívida.

3. Revisão de backlog real

- itens sem URL ou placeholder
- itens ainda não codificados em `purification.jsonl`
- notas de sessão que ainda não viraram decisão de corpus, escrita ou infra

## Antes de abrir PR

1. Isolar o tema do branch

- `corpus/...` para expansão ou reconciliação do corpus
- `vault/...` para notas e tese
- `writing/...` para manuscrito
- `infra/...` para scripts, docs, CI e estrutura

2. Garantir que o diff está coerente com uma única frente

```bash
git status --short
git diff --stat
```

3. Se o PR tocar dados, rodar no mínimo

```bash
python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
python tools/scripts/records_to_corpus.py --diff
python tools/scripts/code_purification.py --status
```

4. Se o PR tocar vault ou notas de candidatos, rodar também

```bash
python tools/scripts/vault_sync.py status
```

## Antes de release público

Release público aqui significa dataset Hugging Face ou qualquer superfície derivada do corpus.

1. Rodar o gate completo

```bash
python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
python tools/scripts/vault_sync.py status
python tools/scripts/records_to_corpus.py --diff
python tools/scripts/code_purification.py --status
```

2. Se o gate estiver limpo, gerar snapshot

```bash
python tools/scripts/build_hf_release.py --note "Describe the milestone here."
```

3. Conferir se o release responde a estas perguntas

- a contagem local de itens bate com o snapshot?
- a contagem de codificação bate com `purification.jsonl`?
- o changelog do release explica o que entrou e o que ainda está pendente?

## Regras de bolso

- Se algo é rastreado pela tese, prefira mantê-lo versionado no hub
- Se algo é superfície pública, trate como derivado
- Se algo é experimento, não deixe contaminar `main`
- Se `git status` ficou ilegível, pare e separe as frentes antes de continuar
- Se houver dúvida entre “documentar” e “automatizar”, documente primeiro e automatize na segunda passada
