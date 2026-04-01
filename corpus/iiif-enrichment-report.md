# Relatório de Enriquecimento IIIF

Total de itens: 95

## Por fonte IIIF
- ⚠ `none`: 28 itens
- ⚠ `thumbnail_fallback`: 24 itens
- ✓ `gallica`: 15 itens
- ✓ `europeana`: 9 itens
- ✓ `loc_api`: 8 itens
- ✓ `loc`: 5 itens
- ✓ `europeana_gallica`: 3 itens
- ⚠ `rijksmuseum_pending`: 3 itens

## Resumo
- Itens com `url_image_download`: 47/95
- Itens com manifesto IIIF real: 32/95
- Itens sem nenhuma URL de imagem: 31

## Itens sem URL de imagem (requerem busca manual)
- BR-006
- BR-007
- BR-008
- PT-005
- FR-011
- NL-001
- NL-002
- NL-003
- UK-001
- UK-002
- UK-003
- BR-009
- BE-001
- BR-010
- NL-004
- NL-005
- NL-006
- NL-007
- NL-008
- UK-005
- ES-001
- UK-006
- DE-013
- ES-002
- UY-001
- US-EDUC-1896-02
- US-EDUC-1896-05
- FR-SEM-1898
- DE-NOTG-1921
- DE-WR-1919-50M
- DE-WR-1924-50PF

## Próximos passos
1. Verificar itens `#verificar-iiif-loc` com API real do LoC
2. Resolver itens `rijksmuseum_pending` via API Rijksmuseum
3. Rodar script de download: `python3 download_images.py`
4. Popular `drive-manifest.json` com os caminhos locais
5. Subir imagens ao HF Hub: `hf upload warholana/iconocracy-corpus data/raw/ --type dataset`