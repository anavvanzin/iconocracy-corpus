# Handoff

## State
E1 no worktree `worktree-e1-fable5-recode` (HEAD `fb4623e`, nada pushado). **N analítico = 44** (índice 49 linhas: 44 em escopo + 5 fora_escopo). Stage A completo: 6/7 motivos-núcleo reaquiridos (firecrawl scrape/search + verificação visual) e recodificados via Workflow iconocode. Imagens novas em `binaries/Images-reacquired-2026-06-15/` (SÓ no checkout principal — backup p/ Drive pendente). Phases 0,1,2 ✅. Status: `docs/decisions/E1-FABLE5-STATUS-2026-06.md` §0.

## Next
1. **DECISÃO Ana — BE-002**: Palais de Justice é arquitetura; só há foto do prédio. Excluir como arquitetura-sem-figura OU escolher estátua de Justice. Está em `excluded_bad_image`.
2. **Phase 3 / Stage B (258 sem-imagem, #2=expandir)**: pace a decidir — piloto Gallica (~40, IIIF, mede custo real) vs separar fetch-barato-de-todas + recode-depois vs tudo. Recode ~257 ≈ ~7M tokens. Tooling pronto: `enrich_iiif.py`, `download_corpus_images.py` + o loop firecrawl validado no Stage A.
3. **Backup das imagens** de 06-15 (e 06-09) p/ Drive/SSD — IRR rater-2 precisará vê-las.

## Context
- Loop de reaquisição que funciona: firecrawl_scrape (json, extrai img real) OU firecrawl_search (sources images, Wikimedia Commons é ouro) → curl download → **Read p/ verificar visualmente** (regra: 09/06 falhou por não verificar) → Workflow iconocode.
- Workflow recode: schema NÃO inclui coded_by/at/from → injetar antes do append. args chega como string → guard JSON.parse no script (`…/workflows/scripts/e1-fable5-code-45-wf_bcb00134-2c0.js`).
- corpus-data.json: restaurado a 314 (HEAD); NÃO regenerar/encolher.
- Setup novo (global): hook secret-scan, skill /reconcile, MCP corpus-vault + iconclass-db.
