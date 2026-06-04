# ICONOCRACIA — Spec compartilhada do pipeline (2026-05-19)

## Schema-alvo (subset obrigatório do corpus-data-enriched.json)

Cada candidato deve ser um objeto JSON com os seguintes campos:

### Obrigatórios (item é rejeitado se faltar)

  - id — string, padrão sqX-2026-05-19-{slug-curto}-{NNN} (zero-padded 3 dígitos)
  - title — string, título original do objeto (mantenha língua original)
  - date — string, ano ou ISO date do objeto (ex.: "1867", "1898-03-15")
  - creator — string, autor/gravador; use "Unknown" ou "[s. n.]" se desconhecido
  - institution — string, instituição detentora (ex.: "KBR", "ONB")
  - source_archive — string, nome do arquivo/repositório digital
  - country — string em inglês (ex.: "Belgium", "Austria", "Brazil")
  - medium — string, técnica/suporte (ex.: "Etching and engraving", "Lithograph")
  - motif — array de strings, motivos iconográficos (ex.: ["Iustitia","scales","blindfold"])
  - description — string, descrição em PT-BR, 1–3 frases
  - url — string, URL canônica do registro institucional
  - citation_abnt — string, referência ABNT NBR 6023:2025 completa

### Recomendados

  - period — string (ex.: "Long 19th century (1789–1914)")
  - thumbnail_url — string
  - rights — string (ex.: "Public domain", "CC BY-SA 4.0")
  - citation_chicago — string
  - tags — array de strings
  - iconclass_codes — array de códigos ICONCLASS (ex.: ["44G","48C51","11MM31"])
  - url_iiif — string, URL do manifesto IIIF (Presentation API v2 ou v3)
  - url_image_download — string, URL para download direto da imagem máxima
  - iiif_source — string, nome do servidor IIIF
  - confidence — string: "low" | "medium" | "high"
  - sq — string: "SQ1" | "SQ2" | "SQ3" | "SQ4"
  - notes — string, observações livres

## Códigos ICONCLASS de referência

  - 44G — administração da justiça (geral)
  - 44G3 — autoridades judiciais; pessoas relacionadas a corte
  - 48C51 — alegoria das artes / personificação
  - 11MM31 — Iustitia (alegoria da Justiça, com balança/espada/venda)
  - 11MM — virtudes (cardeais e teologais)
  - 44A31 — emblemas nacionais
  - 25F — animais simbólicos (quando relevante)
  - 92 — mitologia clássica (Themis, etc.)

## Regras de filtragem

1.  **Dedup hard:** pipeline_run/dedup_urls.txt lista 368 URLs canônicas já no corpus. Se a URL do candidato (canonicalizada: lowercase, sem www., sem trailing /, sem fragmento) constar, **descartar**.
2.  **SQ1 específico:** descartar qualquer URL em gallica.bnf.fr.
3.  **Qualidade mínima:** descartar itens sem ano identificável, sem instituição, ou cuja conexão com alegoria feminina jurídica seja apenas tangencial.
4.  **Preferência institucional:** sobre aggregadores (Europeana, DPLA), preferir registro institucional canônico.
5.  **IIIF:** sempre que houver manifesto IIIF disponível, capturar em url_iiif. Procurar links com "manifest.json", "/manifest", botão IIIF, ou logo IIIF na página.

## Output esperado por SQ

Cada subagent SQ grava UM arquivo:

  - pipeline_run/sq{N}_candidates.json — array JSON de 10–15 objetos

## Cobertura já existente (não duplicar)

Os 368 URLs já indexados cobrem fortemente: Gallica (85), Numista (41), LoC (31), Europeana (22), Bildindex (12), Rijksmuseum (8+5), Brasiliana Fotográfica (8), Bibl. Nac. Portugal (6), V&A (7). **Procurar fontes complementares.**
