# AGENTS.md — ICONOCRACY Quick Brief

## Missão e superfícies
- Monorepo da tese ICONOCRACY: dual-agent pipeline (WebScout → IconoCode) produz `data/processed/records.jsonl`, que depois gera `corpus/corpus-data.json` e releases Hugging Face.
- Três superfícies permanentes: Local (trabalho ativo), GitHub (histórico canônico, CI), Hugging Face (snapshots publicados). Nunca publique sem passar pelo gate de validação.

## Ambiente e comandos base
- `conda activate iconocracy` (Python ≥3.10; use sempre este ambiente) e execute scripts a partir da raiz: `python tools/scripts/<script>.py`.
- QA/corpus: `validate_schemas.py`, `trace_evidence.py`, `abnt_citations.py`, `records_to_corpus.py --diff`, `sync_companion.py`.
- Codificação ENDURECIMENTO: `code_purification.py --status|--item ID|--batch SIGLA|--export-csv` atualiza `data/processed/purification.jsonl` e `corpus_dataset.csv`.
- Vault sync: `python tools/scripts/vault_sync.py status|pull|push|sync|diff` mantém `records.jsonl` ↔ `vault/candidatos/` pareados.
- Releases: `python tools/scripts/build_hf_release.py` só depois de `validate_schemas.py`, `vault_sync.py status`, `records_to_corpus.py --diff` e `code_purification.py --status` limpos.
- Thesis e webapps: `make -C vault/tese/ docx|pdf`, `cd webiconocracy && npm run dev`, `cd indexing/gallica-mcp-server && npm run dev` (portas 3000/3001). Ingest: `python iconocracy-ingest/ingest.py <batch> --dry-run` antes de escrever.

## Dados canônicos e diretórios que importam
- Ordem de verdade: `data/processed/records.jsonl` → `corpus/corpus-data.json` → `data/processed/purification.jsonl` → `vault/candidatos/` (espelho, nunca fonte).
- `data/raw/` guarda **apenas** manifestos (ex.: `drive-manifest.json`). Binários ficam no Google Drive `/Volumes/ICONOCRACIA`; commits com arquivos reais quebram a CI.
- `vault/candidatos/` usa padrão `CC-NNN Nome.md`; `vault/sessoes/` usa `SCOUT-SESSION-YYYY-MM-DD.md`. Rodar `vault_sync.py` antes de tocar em `records.jsonl` ou no vault manualmente.
- `tools/schemas/` contém os contratos (master-record, iconocode-output, webscout-input/output). Nunca altere `corpus/corpus-data.json` sem passar por `records_to_corpus.py`.
- `docs/OPERATING_MODEL.md` e `CLAUDE.md` registram decisões; leia antes de mexer em fluxos ou releases.

## Fluxos essenciais
- **Validação rápida:** `python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose` → `trace_evidence.py` → `abnt_citations.py`. Corrija todo erro antes de prosseguir.
- **QA de corpus export:** `python tools/scripts/records_to_corpus.py --diff` mostra o delta que iria para `corpus/corpus-data.json`. Só aceite se IDs e ENDURECIMENTO não forem alterados indevidamente.
- **Sync catalográfico:** estado limpo em `vault_sync.py status` é requisito para commits e releases. Use `pull` antes de editar notas, `push` ao final.
- **Hugging Face snapshot:** depois do gate acima, rode `build_hf_release.py` e publique apenas o artefato congelado.
- **Indexação Iconclass:** `python tools/scripts/extract_feminist_network.py` atualiza `data/processed/feminist_network_48C51_pt.json`; cite Iconclass 48C51 quando questionado sobre a taxonomia.

## Atalhos disparados pelo usuário
- `campanha N` / `scout [query]` executam a campanha definida em `SKILL.md` (sem confirmação).
- `auditoria` / `lacunas` → Campanha 16 sobre `vault/candidatos/`.
- `validar [arquivo]`, `rastreabilidade [arquivo]`, `citacoes [arquivo]` → scripts homônimos.
- `purificacao status|item|lote|exportar` → `code_purification.py` com o subcomando correspondente.
- `sync vault pull|push|sync|diff|status` → `vault_sync.py` (sempre informar o modo).
- `salvar` → persistir última nota em `vault/candidatos/` com o ID correto; `sessão` → gerar nota `vault/sessoes/`.
- `rede feminista [raiz?]` → `extract_feminist_network.py`; `lote exemplo` → `batch_example.py`.

## Terminologia e estilo obrigatórios
- Use sempre: ENDURECIMENTO, Contrato Sexual Visual, Feminilidade de Estado, Pathosformel, Zwischenraum, Nachleben, Iconclass 48C51.
- Toda referência segue ABNT NBR 6023:2025. Quando citar Mondzain, a edição é 2002.
- Redija em português jurídico-penal; evite enquadramentos antropológicos/sociológicos.

## Guardrails que evitam erros caros
- Regra de rastreabilidade: cada item precisa existir em (1) Google Drive + `data/raw/drive-manifest.json`, (2) `vault/candidatos/`, (3) `data/processed/records.jsonl`. Nenhuma exceção.
- Não edite JSONs parcialmente; use scripts ou reescreva o arquivo inteiro com `Write`. Para `corpus-data.json`, use `records_to_corpus.py`.
- `tese/manuscrito/*_original` é somente leitura; trabalhe nas cópias indicadas.
- Antes de commits, confirme que `git status` não mostra binários novos em `data/raw/`. A CI (`.github/workflows/validate.yml`) falha se isso ocorrer ou se `records.jsonl` quebrar o schema.
- Use `tools/scripts/vault_backup.py` para backups; nunca misture snapshots em `main`.
- Se alguma instrução conflitar, confie primeiro nos scripts/configs e nos arquivos `CLAUDE.md` + `SKILL.md`.
