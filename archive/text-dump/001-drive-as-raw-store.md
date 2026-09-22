# ADR-001: Google Drive como armazenamento de dados brutos

**Status:** Aceito
**Data:** 2026-03-22

## Decisão

Arquivos brutos (imagens, PDFs de acervos, dumps) vivem exclusivamente no Google Drive.
O GitHub armazena apenas manifests JSON com o caminho Drive e o item_id correspondente.

## Motivação

- Evitar arquivos binários grandes no git
- Drive tem versionamento e compartilhamento granular
- Permite citar a URL do Drive nos registros canônicos e notas do vault como "fonte da verdade"

## Consequências

- Todo script que acesse dados brutos deve ler `drive-manifest.json`
- Pull requests que adicionem binários em `data/raw/` devem ser rejeitados
