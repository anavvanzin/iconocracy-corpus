# Task: "Living Manuscript" — Manuscrito Vivo (ICONOCRACIA)

Transformar os capítulos de `tese/manuscrito/` numa superfície web linked-data: quando um conceito da tese (ex.: **Visiocracia**, **Contrato Sexual**, **ENDURECIMENTO**) aparece no texto, um painel lateral carrega dinamicamente as "testemunhas visuais" — itens do corpus que sustentam (ou desafiam) aquele argumento. Ponte entre o texto e o dataset, tese como experiência interativa.

## Fontes (verificadas 2026-08-24, repo `iconocracy-corpus`)

- **Capítulos**: `tese/manuscrito/*.md` — `Introducao_rev.md`, `Capitulo1_rev.md` … `Capitulo9_paineis_atlas.md`, `Conclusao.md`, `Glossario.md`. "Visiocracia" aparece em 10+ arquivos (Introducao, Cap1, Cap8, Cap9, Glossario…).
- **Conceitos**: extrair vocabulário do `Glossario.md` (fonte canônica dos termos da tese) — não hardcodar lista.
- **Corpus**: `corpus/corpus-data.json` (335 itens no snapshot atual; campos `id`, `country`, `date`, `regime` [fundacional|normativo|militar|contra-alegoria], `motif`, `endurecimento_score`, `indicadores` 10×0–3, `citation_abnt`, `url`).
- **Atlas Lab**: repo separado `~/Research/apps/atlaslab` (anavvanzin/atlaslab) — vistas filtradas podem ser linkadas por URL; integração profunda é opcional/fase 2.

## Requisitos

### Build (Python, env conda `iconocracy`)
1. Script `build_living_manuscript.py`:
   - Parseia `Glossario.md` → lista de conceitos.
   - Arquivo de mapeamento curado `concept-witnesses.json` (**editável pela Ana**): conceito → query de corpus (filtros por `regime`, `motif`, faixa de `endurecimento_score`, indicador específico, ou lista explícita de `id`s).
   - Varre os capítulos, marca ocorrências de conceitos, gera HTML por capítulo + `witnesses.json` estático.
2. **Manuscrito é fonte, HTML é derivado** — nunca editar o HTML à mão; regenerável com um comando. NÃO tocar no pipeline Pandoc existente (`make -C vault/tese/`), que continua sendo o compile oficial da tese.

### Superfície web (HTML/JS estático, sem build complexo)
- Texto do capítulo à esquerda; conceitos marcados como spans clicáveis.
- Clique → painel lateral com as testemunhas visuais: thumbnail (via `url`), `title`, `country`, `date`, `regime`, `endurecimento_score`, `citation_abnt`.
- Distinguir testemunhas que **sustentam** vs **desafiam** o conceito (campo `stance: apoia|desafia` no `concept-witnesses.json`).
- Link opcional "abrir no Atlas Lab" quando houver vista correspondente.

## Restrições
- Corpus é exploratório e crescente: nunca fixar N; rebuild deve funcionar em qualquer snapshot.
- Texto da tese em português; preservar a prosa exatamente — o build não reescreve nada.
- Imagens NÃO vão para `data/raw/` (hook bloqueia); usar as URLs remotas existentes.

## Critérios de aceite
- Pelo menos 2 capítulos navegáveis (sugestão: `Capitulo8_atlas_principios.md` e `Capitulo9_paineis_atlas.md`) com painel de testemunhas funcionando.
- `concept-witnesses.json` documentado com ≥5 conceitos mapeados (incluindo Visiocracia).
- Rebuild com um comando documentado; HTML derivado ignorado pelo git ou claramente marcado como gerado.
