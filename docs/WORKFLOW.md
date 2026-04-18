# Workflow Operacional

Workflow curto para tocar a tese sem perder tempo com drift de estrutura, Git ou release.

## Regra-mestra

- Trabalhe no hub canônico: `/Users/ana/Research/hub/iconocracy-corpus`
- Use os paths em `/Users/ana/Research/...` como mapa do workspace
- `/Users/ana/iconocracy-corpus` pode continuar funcionando como symlink de compatibilidade, mas a documentação operacional deve preferir o path em `Research/`
- Considere `records.jsonl` a fonte operacional, `corpus-data.json` o export público e `vault/` o espelho de trabalho
- Não trate Hugging Face como working copy
- Não trate o vault como fonte primária de verdade

## Rotina diária

1. Entrar no ambiente e checar o estado do repo

```bash
cd /Users/ana/Research/hub/iconocracy-corpus
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
find /Users/ana/Research/hub/iconocracy-corpus -mindepth 2 -maxdepth 2 -name .git
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
