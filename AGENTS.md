# AGENTS.md — ICONOCRACY Quick Brief

## Missão e superfícies
- Monorepo da tese ICONOCRACY: o pipeline WebScout → IconoCode alimenta `data/processed/records.jsonl`, que deriva `corpus/corpus-data.json` e releases Hugging Face.
- Três superfícies fixas: **Local** (edição ativa + vault), **GitHub** (histórico/cI), **Hugging Face** (snapshots congelados). Nunca publique fora desse gate.

## Ambiente, ferramentas e comandos
- **Conda obrigatório**: `conda activate iconocracy`; scripts Python sempre via `python tools/scripts/<script>.py` a partir da raiz.
- **Validação rápida**: `python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose` → `python tools/scripts/trace_evidence.py` → `python tools/scripts/abnt_citations.py`.
- **QA de export**: `python tools/scripts/records_to_corpus.py --diff` antes de tocar em `corpus/corpus-data.json`.
- **Sync do vault**: `python tools/scripts/vault_sync.py status|pull|push|sync|diff` mantém `vault/candidatos/` alinhado a `records.jsonl`. Use `pull` antes de editar notas e `push` ao final.
- **Codificação endurecimento**: `python tools/scripts/code_purification.py --status|--item ID|--batch SIGLA|--export-csv` atualiza `data/processed/purification.jsonl` + `corpus_dataset.csv`.
- **Atlas / tese**: `make -C vault/tese/ docx` ou `make -C vault/tese/ pdf`. Webapp ativo: `cd indexing/gallica-mcp-server && npm run dev` (porta 3001). `webiconocracy/` foi aposentado.
- **Releases**: rode `validate_schemas.py`, `vault_sync.py status`, `records_to_corpus.py --diff`, `code_purification.py --status` **antes** de `python tools/scripts/build_hf_release.py`.
- **Ingest**: `python iconocracy-ingest/ingest.py <batch> --dry-run` sempre precede qualquer escrita.

## Dados canônicos e diretórios críticos
- Ordem de verdade: `data/processed/records.jsonl` → `corpus/corpus-data.json` → `data/processed/purification.jsonl` → `vault/candidatos/` (espelho, nunca fonte).
- `data/raw/` guarda **somente manifestos** (ex.: `drive-manifest.json`). Binários residem no Google Drive (`/Volumes/ICONOCRACIA`). Commits com mídia real quebram a CI.
- `vault/candidatos/` segue formatação `CC-NNN Nome.md`; sessões em `vault/sessoes/SCOUT-SESSION-YYYY-MM-DD.md`. Nunca altere notas sem sincronizar via `vault_sync.py`.
- `tools/schemas/` é o contrato do pipeline (master-record, iconocode-output, webscout). Alterações diretas em JSONs só via scripts ou reescrita completa (`Write`).
- `docs/OPERATING_MODEL.md`, `CLAUDE.md` e `SKILL.md` registram decisões — consulte-os antes de ajustar fluxos ou adicionar comandos.

## Fluxos que não podem ser quebrados
- **Rastreabilidade total**: cada item precisa existir em (1) Google Drive + `data/raw/drive-manifest.json`, (2) `vault/candidatos/`, (3) `data/processed/records.jsonl`.
- **Export gate**: aceite mudanças em `records_to_corpus.py --diff` somente se não adulterarem IDs, regimes ou endurecimento.
- **Snapshots HF**: só publique após o combo validação + diff + sync + purificação. Use `build_hf_release.py` para gerar o pacote completo.
- **Iconclass / rede feminista**: `python tools/scripts/extract_feminist_network.py` atualiza `data/processed/feminist_network_48C51_pt.json`; cite Iconclass 48C51 como referência padrão.

## Atalhos disparados pelo usuário
- `campanha N` / `scout [query]` → executam diretamente as campanhas descritas em `SKILL.md`.
- `auditoria` / `lacunas` → Campanha 16 (mapa de gaps do vault).
- `validar [arquivo]`, `rastreabilidade [arquivo]`, `citacoes [arquivo]` → scripts homônimos dentro de `tools/scripts/`.
- `purificacao status|item|lote|exportar` → subcomandos de `code_purification.py`.
- `sync vault pull|push|sync|diff|status` → passa parâmetros para `vault_sync.py` (nunca rode “semi-manual”).
- `salvar` grava última nota no vault com ID correto; `sessão` abre `vault/sessoes/`.
- `rede feminista [raiz?]` → `extract_feminist_network.py`; `lote exemplo` → `batch_example.py`.

## Estilo e terminologia obrigatórios
- Sempre use os termos originais da tese: **endurecimento** (nunca "hardening"/"embrutecimento"), **Contrato Sexual Visual** (autoral — Vanzin 2026, NÃO atribuir a Pateman), **Feminilidade de Estado** (autoral — NÃO atribuir a Mondzain), **Purificação Clássica**, **Pathosformel**, **Zwischenraum**, **Nachleben**, **Iconclass 48C51**.
- Citações em ABNT NBR 6023:2025; Mondzain = edição 2002. Texto acadêmico em português jurídico-penal, não antropológico/sociológico.

## Guardrails finais
- `tese/manuscrito/*_original` é somente leitura — trabalhe nas versões `*_rev`.
- `git status` precisa estar limpo de binários novos em `data/raw/` antes de qualquer commit; `.github/workflows/validate.yml` bloqueia schema inválido ou mídia fora do lugar.
- Use `python tools/scripts/vault_backup.py` para snapshots; não misture backups no branch principal.
- Em caso de conflito de instruções, priorize o que está em `CLAUDE.md` e nos scripts executáveis; só override mediante confirmação explícita.
