# Workspace Map

Mapa operacional do ecossistema ICONOCRACIA apos a migracao para `/Users/ana/Research`.

## Root canonica

- Workspace root: `/Users/ana/Research`
- Hub da tese: `/Users/ana/Research/hub/iconocracy-corpus`
- Compatibilidade temporaria: `/Users/ana/iconocracy-corpus` aponta para o hub canonico

## Contrato do hub

O hub da tese deixa de funcionar como super-workspace. Ele continua sendo o ponto de verdade para:

- `corpus/`
- `data/`
- `docs/`
- `notebooks/`
- `tese/`
- `tools/`
- `vault/` como espelho da superficie canonica em `/Users/ana/Research/vaults/iconocracy-vault`

Na fase git-safe da migracao, conteudo ainda rastreado por este repositório continua fisicamente dentro do hub. Os caminhos em `Research/pipelines/` e `Research/vaults/` funcionam como acessos canonicos de workspace e, quando necessario, apontam por symlink para esses diretórios versionados.

O contrato de dados permanece inalterado:

1. `data/processed/records.jsonl`
2. `corpus/corpus-data.json`
3. `data/processed/purification.jsonl`
4. `vault/candidatos/` como espelho auxiliar
5. releases publicos e snapshots congelados como artefatos derivados

## Dependencias e spokes

| Nome | Caminho canonico | Relacao com o hub | Status | Compatibilidade |
| --- | --- | --- | --- | --- |
| `iconocracy-corpus` | `/Users/ana/Research/hub/iconocracy-corpus` | Hub canonico e ponto de verdade da tese | canonical | `/Users/ana/iconocracy-corpus` |
| `iconocracia-companion` | `/Users/ana/Research/apps/iconocracia-companion` | Interface publica do corpus | experimental | `/Users/ana/iconocracia-companion` |
| `iconocracia-space` | `/Users/ana/Research/apps/iconocracia-space` | Explorer/read-only para Hugging Face | experimental | `/Users/ana/iconocracia-space` |
| `webiconocracy` | `/Users/ana/Research/apps/webiconocracy` | App experimental separado do hub | experimental | sem atalho local garantido no hub |
| `iconocracy-ingest` | `/Users/ana/Research/pipelines/iconocracy-ingest` | Pipeline de ingestao que alimenta os dados do hub | derived | path externo canonico apontando para `iconocracy-ingest/` dentro do hub |
| `indexing` | `/Users/ana/Research/pipelines/indexing` | Indexacao e infraestrutura Gallica/Scout | derived | symlink em `indexing/` dentro do hub |
| `Atlas` | `/Users/ana/Research/pipelines/Atlas` | Toolkit iconografico auxiliar | experimental | symlink em `Atlas/` dentro do hub |
| `iurisvision` | `/Users/ana/Research/labs/iurisvision` | Laboratorio exploratorio, nao parte do hub | experimental | symlinks legados em home, `Projects/` e hub |
| `iuris-visio-roadmap` | `/Users/ana/Research/labs/iuris-visio-roadmap` | Planejamento exploratorio externo ao hub | experimental | `/Users/ana/iuris-visio-roadmap` |
| `iconocracy-vault` | `/Users/ana/Research/vaults/iconocracy-vault` | Vault canonico da tese; `vault/` no hub segue como diretório versionado | canonical | path externo canonico apontando para `vault/` dentro do hub |
| `dir410346-vault` | `/Users/ana/Research/vaults/dir410346-vault` | Vault de disciplina com acesso separado no workspace | experimental | path externo canonico apontando para `vault/obsidian-dir410346` |
| `dir410340-vault` | `/Users/ana/Research/vaults/dir410340-vault` | Vault de disciplina com acesso separado no workspace | experimental | path externo canonico apontando para `vault/obsidian-dir410340` |
| `iconclass-data` | `/Users/ana/Research/shared/iconclass-data` | Base compartilhada de referencia | canonical | `/Users/ana/iconclass-data` |
| `iconclass-data-avmadrj` | `/Users/ana/Research/shared/iconclass-data-avmadrj` | Base compartilhada derivada/local | canonical | `/Users/ana/iconclass-data-avmadrj` |
| `js-genai` | `/Users/ana/Research/archive/js-genai` | Checkout externo aposentado | archived | symlink em `js-genai/` dentro do hub |
| `iconocracy-corpus-legacy` | `/Users/ana/Research/archive/iconocracy-corpus-legacy` | Repo duplicado legado, fora do fluxo ativo | archived | sem symlink no hub; ver nota abaixo |

## Notas de compatibilidade

- A maioria dos caminhos legados foi mantida como symlink para evitar quebra imediata de scripts e documentos.
- `iconocracy-ingest` e os vaults permaneceram fisicamente dentro do hub nesta fase para preservar um working tree Git limpo; a separacao no workspace acontece pelos caminhos canonicos em `Research/`.
- O path aninhado `iconocracy-corpus/iconocracy-corpus` nao permaneceu como symlink porque o repositório principal ainda o registrava como gitlink, o que quebrava `git status`.
- As duplicatas de `iurisvision` foram resolvidas em um unico checkout canonico: `/Users/ana/Research/labs/iurisvision`.
- O vault legado em `/Users/ana/vault` foi movido para arquivo e mantido apenas por compatibilidade.

## Verificacao rapida

Comandos uteis apos a migracao:

```bash
find /Users/ana/Research/hub/iconocracy-corpus -mindepth 2 -maxdepth 2 -name .git
python /Users/ana/Research/hub/iconocracy-corpus/tools/scripts/validate_schemas.py /Users/ana/Research/hub/iconocracy-corpus/data/processed/records.jsonl --schema master-record --verbose
python /Users/ana/Research/hub/iconocracy-corpus/tools/scripts/records_to_corpus.py --diff
python /Users/ana/Research/hub/iconocracy-corpus/tools/scripts/code_purification.py --status
python /Users/ana/Research/hub/iconocracy-corpus/tools/scripts/vault_sync.py status
```
