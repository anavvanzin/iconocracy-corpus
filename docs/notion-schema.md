# Schema das Databases Notion

Mapa das databases Notion usadas como índice do corpus.
Referência: [ADR-002](adr/002-notion-as-index.md)

## Database Principal: Corpus Iconocracia

| Propriedade | Tipo Notion | Campo JSONL | Notas |
|-------------|-------------|-------------|-------|
| Nome | Title | `webscout.title` | Título do item |
| item_id | Text | `item_id` | UUID, chave de sync |
| batch_id | Text | `batch_id` | UUID do lote |
| País | Select | `webscout.country` | |
| Período | Select | `webscout.period` | |
| Data | Text | `webscout.date` | |
| Criador | Text | `webscout.creator` | |
| Instituição | Select | `webscout.institution` | |
| Medium | Select | `webscout.medium` | |
| URL Fonte | URL | `input.input_url` | |
| Thumbnail | URL | `webscout.thumbnail_url` | |
| Motivo | Multi-select | `iconocode.codes[].label` | Iconclass labels |
| Confiança | Number | `iconocode.confidence` | 0.0–1.0 |
| Citação ABNT | Text | `exports.abnt_citations[0]` | |
| Audit Flags | Multi-select | `exports.audit_flags` | |
| Status | Status | — | Workflow manual |

## Database Auxiliar: Indicadores de Purificação

| Propriedade | Tipo | Escala |
|-------------|------|--------|
| item_id | Relation → Corpus | — |
| desincorporacao | Number | 0–3 |
| rigidez_postural | Number | 0–3 |
| dessexualizacao | Number | 0–3 |
| uniformizacao_facial | Number | 0–3 |
| heraldizacao | Number | 0–3 |
| enquadramento_arquitetonico | Number | 0–3 |
| apagamento_narrativo | Number | 0–3 |
| monocromatizacao | Number | 0–3 |
| serialidade | Number | 0–3 |
| inscricao_estatal | Number | 0–3 |
| indice_purificacao | Formula | mean dos 10 indicadores |

## Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `NOTION_API_KEY` | Token de integração Notion |
| `NOTION_CORPUS_DB_ID` | ID da database principal |
| `NOTION_PURIFICACAO_DB_ID` | ID da database de indicadores |

## Sincronização

Script: `tools/scripts/notion_sync.py`

```bash
# Notion → JSONL (pull)
python tools/scripts/notion_sync.py pull

# JSONL → Notion (push)
python tools/scripts/notion_sync.py push

# Sync bidirecional (last-write-wins)
python tools/scripts/notion_sync.py sync
```
