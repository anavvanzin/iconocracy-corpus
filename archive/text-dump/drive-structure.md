# Estrutura de Pastas no Google Drive

Mapa da organização dos arquivos brutos no Google Drive.
Referência: [ADR-001](adr/001-drive-as-raw-store.md)

## Raiz do Drive

```
Iconocracia — Corpus/
├── 01_Acervos/                  ← Downloads de acervos digitais
│   ├── BNF_Gallica/
│   ├── Library_of_Congress/
│   ├── Biblioteca_Nacional_BR/
│   ├── Rijksmuseum/
│   └── ...
├── 02_Imagens_Catalogadas/      ← Imagens já vinculadas a master records
│   ├── batch_001/
│   ├── batch_002/
│   └── ...
├── 03_PDFs_Fontes/              ← Artigos, capítulos digitalizados
├── 04_Mapas_e_Diagramas/        ← Materiais visuais auxiliares
└── 05_Backups/                  ← Snapshots periódicos do JSONL
```

## Convenções

- Nomes de pasta seguem o padrão `NN_Nome_Descritivo/`
- Cada imagem catalogada deve ter entrada no `drive-manifest.json`
- Subpastas de batch correspondem ao `batch_id` no master record
- Não mover arquivos sem atualizar o manifest

## Sincronização com o Repositório

O arquivo `data/raw/drive-manifest.json` mapeia cada pasta/item no Drive
ao `item_id` correspondente no `records.jsonl`.
