# data/raw/

Arquivos brutos (imagens, PDFs de acervos, dumps iconográficos) **não são commitados** neste repositório.

Eles vivem exclusivamente no Google Drive (ver [ADR-001](../../docs/adr/001-drive-as-raw-store.md)).

## Como acessar

1. Consulte `drive-manifest.json` nesta pasta para o mapeamento pasta → item_id.
2. Use a URL raiz do Drive listada no manifest para navegar até os originais.
3. Scripts que precisam de dados brutos devem ler o manifest e baixar sob demanda.

## Regras

- **Nunca commitar binários** nesta pasta (o CI rejeitará o PR).
- Para adicionar um novo item bruto, coloque no Drive e adicione a entrada no `drive-manifest.json`.
