# Findings — E1 re-run Fable 5

## Resultado da codificação (43 itens)
- N analítico (em escopo) = **38**. Regimes: normativo 20, fundacional 11, militar 5, contra-alegoria 2.
- 5 fora_escopo legítimos: BE-5F-LEOPOLD-1832, PT-001 (dry-run); US-020, PT-003, PT-004 (produção).
- composto 0.3–2.6 (média 1.66); **all-zero=0** → codificar da imagem (não de texto) eliminou os 29 zeros do Gemma.

## 7 imagens ruins (motivos-núcleo, IN SCOPE — reaquisição)
A campanha de reaquisição de 09/06 (fallback og:image→twitter:image→img-tag) pegou arquivos errados:
| Sigla | Problema |
|---|---|
| DE-013 (Germania) | arquivo é logo "LeMO" (verifiquei visualmente) |
| BR-006 (Alegoria da República) | placeholder abstrato (verifiquei) |
| UK-FLORIN-1902 (Britannia) | anverso do rei; Britannia no verso, ausente (verifiquei) |
| UK-010 (Britannia/Hibernia) | capa do livro "Cartoons by Tenniel" |
| UY-001 (Altar de la Patria) | foto de figura masculina |
| BE-002 (Palais de Justice) | retrato do arquiteto Poelaert |
| DE-008 (Justitia, Hameln) | fachada; relevo da Justitia minúsculo/indiscernível |

## Gotchas técnicos (reutilizar)
- **Workflow `args` chega como STRING JSON**, não array → guard `typeof args==='string'?JSON.parse(args):...` no topo do script.
- **Schema do Workflow** deve listar `coded_by`/`coded_at`/`coded_from` senão o agente não os emite → tive que injetar na gravação.
- **Append auto-corrige item_id** via sigla (worklist = fonte da verdade); o agente alucinou o UUID do PT-001 e foi corrigido.
- **fora_escopo ≠ imagem ruim**: fora_escopo = "não é alegoria feminina"; imagem ruim de motivo-núcleo vai p/ reaquisição, NÃO p/ fora_escopo.
- Heredoc Python com f-string + aspas escapadas quebra → usar arquivo temp.
- Python SEMPRE `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python3.12` (host é macOS; ignorar rodapé "Linux" do ecc-iconocracy-guide).

## IRR readiness
Design `IRR-RE-RUN-DESIGN-2026-06-09.md` assumia ~186 c/ estratos fund~100/norm~60/mil~20/contra~8.
Realidade N=38: norm 20, fund 11, militar 5, contra-alegoria 2 → estratos finos; amostragem estratificada precisa revisão (provável censo de contra/militar). IRR exige rater-2 (este E1 é só rater-1).

## Funil
308 (records) = 50 codificáveis (43 codificados + 7 imagem-ruim) + 258 sem-imagem (URLs = catálogo/PDF, reaquisição separada).

## Diagnóstico do corpus-data.json alheio (Phase 1, 2026-06-14)
- Contagens: records.jsonl=308 · corpus HEAD=314 · corpus working-tree=**264**.
- working-tree ⊆ HEAD (0 itens novos; faltam 43). HEAD∩records=296 vs working∩records=254.
- **Veredito: a modificação no working tree é REGRESSÃO** (snapshot antigo de 264 que derrubou os 43 candidatos de 08/06). NÃO é regeneração legítima.
- **Ação recomendada:** `git checkout corpus/corpus-data.json` (descartar working-tree, restaurar HEAD 314). Destrutivo → confirmar com Ana.
- **RESOLVIDO 2026-06-15:** descartado, restaurado 314.

## Campanha de reaquisição (Phase 3 / decisão #2 = expandir) — diagnóstico B1
- 258 sem-imagem + 7 imagem-ruim = 265 itens-alvo.
- Tipos: 237 páginas de catálogo · 10 com URL de imagem direta (ganho instantâneo) · 3 PDF · 8 placeholders (sem fonte → exclusão definitiva).
- **Domínios concentrados em bibliotecas digitais estruturadas** (boa notícia p/ IIIF/API):
  Gallica 40 · LoC 32 · Europeana 23 · Numista 21 · HAUM-BS 12 · Wikimedia 10 · Rijksmuseum 9 · V&A 8 · SMK 8 · Heidelberg 5 · Met 3 … (52 domínios).
- **Ferramentas que JÁ existem (reuso):**
  - `enrich_iiif.py corpus` → adiciona url_iiif/url_image_download p/ Gallica, Europeana(via Gallica), LoC, Rijksmuseum, Brasiliana. Cobre ~95+ itens (Gallica+LoC+Europeana).
  - `download_corpus_images.py` → baixa Gallica-IIIF > url_image_download > thumb. ⚠️ grava em `/Volumes/ICONOCRACIA/...` (SSD; redirecionar p/ pasta local).
  - `loc_download.py` (LoC, usa Playwright p/ Cloudflare) · `europeana_download.py` (Europeana).
- **Pipeline Stage B:** enrich_iiif → download (redirecionar saída) → triagem → recodificar (Workflow iconocode).
- **CUSTO recodificação:** ~30k tokens/item × ~257 ≈ **~7M tokens** (o workflow de 45 custou 1.35M). Download de imagem é barato; o recode é o gargalo de custo → escalonar.
