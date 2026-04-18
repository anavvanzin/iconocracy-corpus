# Root Inventory — ICONOCRACY Hub

Data: 2026-04-17
Escopo: `/Users/ana/Research/hub/iconocracy-corpus`
Base de inspeção: worktree `infra/hub-consistency-refactor`

Este inventário classifica cada entrada de primeiro nível do hub e define a ação operacional esperada.

Categorias usadas:
- `canonical` — superfície central do hub
- `derived` — artefato derivado ou pipeline acoplado ao hub, mas não fonte primária
- `compatibility-symlink` — atalho para outro bucket do workspace `Research/`
- `generated-local` — estado local gerado pelo Git/worktree
- `experimental` — superfície útil, mas não parte do contrato canônico
- `archive` — material legado ou histórico
- `cache-tooling` — configuração, automação ou infra local de desenvolvimento
- `unknown-needs-review` — manter sob revisão até realocação/eliminação

## Regras rápidas

1. O contrato de verdade permanece:
   - `data/processed/records.jsonl`
   - `corpus/corpus-data.json`
   - `data/processed/purification.jsonl`
   - `vault/candidatos/` como espelho
2. Symlinks do root não contam como diretórios nativos do hub.
3. Artefatos gerados não devem disputar espaço semântico com dados canônicos.
4. Nomes genéricos ou históricos podem existir apenas se estiverem documentados ou realocados.

## Inventário do root

| path | kind | category | owner-surface | status | action | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `.air` | dir | cache-tooling | local tooling | tracked | keep | Configuração local de MCP/air; documentar como local-only se continuar versionada. |
| `.claude` | dir | cache-tooling | repo automation | tracked | keep | Hooks e automações do projeto; sanitizar caminhos absolutos quando possível. |
| `.dockerignore` | file | cache-tooling | infra | tracked | keep | Deve espelhar a política real de artefatos locais. |
| `.git` | file | generated-local | git worktree | generated | ignore | Gitfile do worktree; não faz parte do repo lógico. |
| `.github` | dir | cache-tooling | CI/repo governance | tracked | keep | Workflows e metadados de repo. |
| `.gitignore` | file | cache-tooling | repo policy | tracked | keep | Fonte da política de ruído local e artefatos gerados. |
| `.mcp.json` | file | cache-tooling | local MCP config | tracked | review | Conter paths absolutos é frágil; preferir template ou arquivo local ignorado. |
| `.remember` | dir | cache-tooling | local memory | tracked | review | Estado local; preferir ignorar ou converter em template documentado. |
| `AGENTS.md` | file | canonical | repo instructions | tracked | keep | Instrução operacional autoritativa no hub. |
| `archive` | dir | archive | legacy | tracked | keep | Casa de material legado do próprio hub. |
| `Atlas` | symlink | compatibility-symlink | `/Users/ana/Research/pipelines/Atlas` | tracked | document | Symlink de compatibilidade, não diretório nativo do hub. |
| `biblio` | dir | unknown-needs-review | bibliography | tracked | move | Realocar para `tese/bibliografia/` para remover bucket ambíguo do root. |
| `CITATION.cff` | file | canonical | repo metadata | tracked | keep | Metadados de citação do projeto. |
| `CLAUDE.md` | file | canonical | repo instructions | tracked | keep | Instrução operacional autoritativa. |
| `companion-data.json` | file | derived | companion export | tracked | move/remove | Duplicata byte-a-byte de `corpus/companion-data.json`; manter só uma cópia canônica. |
| `concepts` | dir | experimental | reference notes | tracked | keep | Glossário e conceitos úteis; documentar como superfície de referência experimental. |
| `corpus` | dir | canonical | public export | tracked | keep | Contém `corpus-data.json`; diretório central. |
| `data` | dir | canonical | operational data | tracked | keep | Ledger canônico e manifestos. |
| `deploy` | dir | derived | deployment/release | tracked | keep | Superfície derivada de deploy; documentar melhor. |
| `docker-compose.yml` | file | cache-tooling | infra | tracked | keep | Orquestração local. |
| `DOCKER_OPTIMIZATION_GUIDE.md` | file | experimental | infra notes | tracked | keep | Guia histórico/auxiliar; alinhar com `.dockerignore` se continuar vivo. |
| `docs` | dir | canonical | documentation | tracked | keep | Documentação autoritativa do hub. |
| `entities` | dir | experimental | companion notes | tracked | keep | Material conceitual leve; documentar como apoio ao companion. |
| `environment.yml` | file | cache-tooling | env definition | tracked | keep | Definição canônica do ambiente conda. |
| `examples` | dir | derived | pipeline examples | tracked | keep | Exemplos de saídas, não fonte primária. |
| `fix_records_schema.py` | file | unknown-needs-review | one-off script | tracked | move | Realocar para `archive/root-legacy/scripts/` como script histórico. |
| `gallery` | dir | experimental | image gallery | tracked | keep | Base visual auxiliar usada por scripts como `iconocracy_clip.py`. |
| `iconocracy-ingest` | dir | derived | ingest pipeline | tracked | keep | Permanece fisicamente no hub por razões git-safe; documentar exceção. |
| `ICONOCRACY_MASTER_PROMPT.md` | file | canonical | agent spec | tracked | keep | Prompt master do projeto. |
| `indexing` | symlink | compatibility-symlink | `/Users/ana/Research/pipelines/indexing` | tracked | document | Symlink de compatibilidade. |
| `iurisvision` | symlink | compatibility-symlink | `/Users/ana/Research/labs/iurisvision` | tracked | document | Symlink de compatibilidade. |
| `js-genai` | symlink | compatibility-symlink | `/Users/ana/Research/archive/js-genai` | tracked | document | Symlink de compatibilidade para checkout arquivado. |
| `LICENSE` | file | canonical | repo metadata | tracked | keep | Licença do projeto. |
| `notebooks` | dir | experimental | exploratory analysis | tracked | keep | Notebooks seguem rastreados; outputs precisam de política própria. |
| `PHD` | dir | unknown-needs-review | course deliverable | tracked | move | Realocar para `archive/root-legacy/PHD/` e atualizar referências internas. |
| `README.md` | file | canonical | repo entrypoint | tracked | keep | Precisa refletir o estado real do hub. |
| `requirements.txt` | file | cache-tooling | env compatibility | tracked | keep | Compatibilidade adicional; não é a fonte principal do env. |
| `SCHEMA.md` | file | canonical | schema/process docs | tracked | keep | Documento de contratos/esquemas. |
| `SECURITY.md` | file | canonical | repo metadata | tracked | keep | Política de segurança. |
| `shared` | dir | experimental | TS shared package | tracked | keep | Pacote compartilhado de app; documentar como superfície experimental derivada. |
| `SKILL.md` | file | canonical | agent shortcuts | tracked | keep | Skill/project routing de alto nível. |
| `sources` | dir | archive | source dumps | tracked | keep | Materiais salvos e referências históricas. |
| `tese` | dir | canonical | thesis materials | tracked | keep | Superfície da tese no hub; distinguir de `vault/tese/` como build surface. |
| `tests` | dir | cache-tooling | verification | tracked | keep | Testes e verificações automatizadas. |
| `tools` | dir | canonical | automation | tracked | keep | Scripts e schemas centrais. |
| `vault` | dir | canonical | working mirror | tracked | keep | Superfície ativa do vault; `vault/candidatos/` continua espelho. |

## Movimentos aprovados por este inventário

1. `PHD/` -> `archive/root-legacy/PHD/`
2. `fix_records_schema.py` -> `archive/root-legacy/scripts/fix_records_schema.py`
3. `biblio/ICONOCRACY_Cap3.bib` -> `tese/bibliografia/ICONOCRACY_Cap3.bib`
4. `companion-data.json` no root -> remover como duplicata, mantendo `corpus/companion-data.json`

## Retenções explicitamente justificadas

- `concepts/`, `entities/`, `gallery/`, `shared/` permanecem no root porque ainda têm utilidade operacional ou documental, mas devem ser tratados como superfícies experimentais/documentadas, não como contrato canônico.
- `iconocracy-ingest/` permanece fisicamente no hub por razões de migração git-safe; o workspace canônico segue em `/Users/ana/Research/pipelines/iconocracy-ingest`.
- `Atlas`, `indexing`, `iurisvision` e `js-genai` permanecem como symlinks documentados de compatibilidade.
