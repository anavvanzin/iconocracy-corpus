# Generated Artifacts and Local State Policy

Status: active
Data: 2026-04-17
Escopo: `/Users/ana/Research/hub/iconocracy-corpus`

Este documento define como tratar artefatos gerados, caches locais, logs, lockfiles e estado de editor/plugin no hub.

## 1. Princípio geral

O hub distingue quatro classes:

1. `canonical`
   - fonte primária de verdade do projeto
2. `derived-tracked`
   - artefato derivado rastreado deliberadamente porque alimenta uma superfície pública, um app ou uma verificação metodológica
3. `generated-local`
   - artefato reproduzível ou local, que não deve poluir o histórico
4. `editor-or-tool-state`
   - estado de IDE, plugin, MCP ou CLI dependente da máquina/usuário

Regra: se um arquivo pode ser regenerado localmente e não é uma superfície pública ou evidência metodológica explícita, ele deve ser tratado como `generated-local` ou `editor-or-tool-state`.

## 2. Política por área

### Notebook outputs

- Notebooks em `notebooks/*.ipynb` podem permanecer rastreados.
- Outputs transitórios de notebook não devem viver sem política clara em `data/processed/`.
- Tabelas/figuras curadas e citadas na tese podem ser rastreadas se forem promovidas explicitamente para uma superfície derivada documentada.

Diretriz operacional:
- outputs transitórios -> ignorar ou mover para `output/` / `tmp/`
- outputs curados -> mover para `data/processed/derived/` ou outra superfície documentada

### Dados derivados de app/release

- `corpus/companion-data.json` é a cópia derivada canônica do companion.
- Duplicatas no root não devem existir.
- Artefatos como `corpus/corpus-data-enriched.json`, `data/processed/irr_report.json`, `data/processed/irr_sample.json` e afins precisam ser tratados como derivados documentados, nunca como fonte primária.

### Logs e temporários

Devem permanecer fora do histórico principal ou em paths já ignorados:
- `output/`
- `tmp/`
- `logs/`
- `postman/`
- `.postman/`
- `data/raw/.staging/`

### Vault / Obsidian

- `vault/.obsidian/workspace*.json`, hotkeys e plugins locais continuam ignorados.
- Apenas um subconjunto de configuração compartilhada deve permanecer rastreado.
- Estado fortemente dependente de preferência pessoal deve ser reduzido ou ignorado progressivamente.

### MCP / agent / local tooling state

Devem preferir template documentado ou arquivo ignorado quando contiverem caminhos absolutos ou configuração de máquina:
- `.mcp.json`
- `.air/`
- `.remember/`
- partes de `.claude/` com paths específicos da máquina

## 3. Regras de duplicação

1. Cada artefato derivado importante deve ter um único local canônico.
2. Duplicatas byte-a-byte devem ser eliminadas.
3. Se dois diretórios precisarem do mesmo payload, a geração deve apontar para um local principal e copiar apenas no processo de release/deploy, não no working tree canônico.

## 4. Paths atualmente tratados como local/generated

- `output/`
- `tmp/`
- `logs/`
- `firebase-debug.log`
- `postman/`
- `.postman/`
- `.agents/`
- `.hermes/`
- `vault/tese/output/`
- `data/raw/.staging/`
- `data/raw/argos/manifest.lock`
- `data/raw/argos/*.bak`
- `*.bak*`

## 5. Decisões aplicadas neste refactor

- remover `companion-data.json` do root como duplicata
- preservar `corpus/companion-data.json` como artefato derivado documentado
- alinhar `.gitignore` e `.dockerignore` com a política de ruído local
- tratar `PHD/` e `fix_records_schema.py` como legado/one-off, fora do root

## 6. Regra de revisão futura

Antes de rastrear um novo artefato gerado, responder:

1. Ele alimenta uma superfície pública, app ou release de forma deliberada?
2. Ele é evidência metodológica citada ou necessária para reprodutibilidade?
3. Existe um único local canônico documentado para ele?
4. Ele pode ser regenerado sem perda material?

Se a resposta para (1) e (2) for não, o padrão é ignorar ou manter fora do root canônico.
