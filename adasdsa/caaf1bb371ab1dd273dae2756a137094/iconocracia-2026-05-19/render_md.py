#!/usr/bin/env python3
"""Render runbook-style YAML markdown from candidatos-2026-05-19.json."""
import json, os, re
from collections import Counter
from datetime import date

J = '/home/user/workspace/corpus/candidatos/candidatos-2026-05-19.json'
OUT = '/home/user/workspace/corpus/candidatos/research-2026-05-19.md'
STATS = '/home/user/workspace/pipeline_run/stats.json'

items = json.load(open(J))
stats = json.load(open(STATS))

def yaml_str(v):
    if v is None: return '""'
    s = str(v).replace('\n',' ').strip()
    if any(c in s for c in [':', '#', '"', "'", '\\', '[', ']', '{', '}']) or s.startswith(('- ', '? ')) or s == '':
        return '"' + s.replace('\\','\\\\').replace('"','\\"') + '"'
    return s

def yaml_list(lst):
    if not lst: return '[]'
    return '[' + ', '.join(yaml_str(x) for x in lst) + ']'

sq_titles = {
    'SQ1': 'SQ1 — Alegorias femininas da Justiça (séc. XIX) fora de Gallica',
    'SQ2': 'SQ2 — Iconografia jurídica latino-americana (1850–1950)',
    'SQ3': 'SQ3 — ICONCLASS 48C51 / 11MM31 em museus europeus com IIIF',
    'SQ4': 'SQ4 — Tratados de iconologia jurídica em alemão/italiano/latim',
}

lines = []
lines.append('# ICONOCRACIA — Candidatos para expansão do corpus')
lines.append('')
lines.append(f'**Data da execução:** {stats["date"]}  ')
lines.append(f'**Corpus base:** 145 itens canônicos (+ corpus enriquecido = 264/95 entradas em `corpus-data.json` / `corpus-data-enriched.json`)  ')
lines.append(f'**Pool de deduplicação:** {stats["dedup_pool_size"]} URLs canônicas  ')
lines.append(f'**Candidatos novos validados:** {stats["total"]}  ')
lines.append(f'**Cobertura IIIF:** {stats["with_iiif"]}/{stats["total"]} ({stats["with_iiif"]*100//stats["total"]}%)  ')
lines.append(f'**Cobertura ICONCLASS:** {stats["with_iconclass"]}/{stats["total"]} (100%)')
lines.append('')
lines.append('## Resumo por sub-questão')
lines.append('')
lines.append('| SQ | Mantidos | Com IIIF | Rejeitados (dedup) | Rejeitados (schema) |')
lines.append('|----|---------:|---------:|-------------------:|--------------------:|')
for sq in ['sq1','sq2','sq3','sq4']:
    s = stats['per_sq'][sq]
    lines.append(f"| {sq.upper()} | {s['count']} | {s['with_iiif']} | {s['rejected_dedup']} | {s['rejected_schema']} |")
lines.append('')

# Institutional spread
inst = Counter(it.get('institution','?') for it in items)
country = Counter(it.get('country','?') for it in items)
icon_codes = Counter()
for it in items:
    for c in it.get('iconclass_codes', []):
        icon_codes[c] += 1

lines.append('## Distribuição institucional')
lines.append('')
for i, n in inst.most_common():
    lines.append(f'- **{i}** — {n}')
lines.append('')
lines.append('## Distribuição geográfica')
lines.append('')
for c, n in country.most_common():
    lines.append(f'- {c} — {n}')
lines.append('')
lines.append('## Cobertura ICONCLASS')
lines.append('')
for c, n in icon_codes.most_common():
    lines.append(f'- `{c}` — {n}')
lines.append('')
lines.append('---')
lines.append('')

# Items grouped by SQ
by_sq = {}
for it in items:
    by_sq.setdefault(it.get('sq','?'), []).append(it)

for sq in ['SQ1','SQ2','SQ3','SQ4']:
    if sq not in by_sq: continue
    lines.append(f'## {sq_titles.get(sq, sq)}')
    lines.append('')
    for it in by_sq[sq]:
        lines.append('```yaml')
        lines.append(f"id: {yaml_str(it.get('id',''))}")
        lines.append(f"title: {yaml_str(it.get('title',''))}")
        lines.append(f"date: {yaml_str(it.get('date',''))}")
        lines.append(f"period: {yaml_str(it.get('period',''))}")
        lines.append(f"creator: {yaml_str(it.get('creator',''))}")
        lines.append(f"institution: {yaml_str(it.get('institution',''))}")
        lines.append(f"source_archive: {yaml_str(it.get('source_archive',''))}")
        lines.append(f"country: {yaml_str(it.get('country',''))}")
        lines.append(f"medium: {yaml_str(it.get('medium',''))}")
        lines.append(f"motif: {yaml_list(it.get('motif',[]))}")
        lines.append(f"iconclass_codes: {yaml_list(it.get('iconclass_codes',[]))}")
        lines.append(f"tags: {yaml_list(it.get('tags',[]))}")
        lines.append(f"description: {yaml_str(it.get('description',''))}")
        lines.append(f"url: {yaml_str(it.get('url',''))}")
        if it.get('thumbnail_url'):
            lines.append(f"thumbnail_url: {yaml_str(it.get('thumbnail_url'))}")
        if it.get('url_iiif'):
            lines.append(f"url_iiif: {yaml_str(it.get('url_iiif'))}")
            lines.append(f"iiif_source: {yaml_str(it.get('iiif_source',''))}")
        if it.get('url_image_download'):
            lines.append(f"url_image_download: {yaml_str(it.get('url_image_download'))}")
        if it.get('rights'):
            lines.append(f"rights: {yaml_str(it.get('rights'))}")
        lines.append(f"citation_abnt: {yaml_str(it.get('citation_abnt',''))}")
        if it.get('citation_chicago'):
            lines.append(f"citation_chicago: {yaml_str(it.get('citation_chicago'))}")
        lines.append(f"confidence: {yaml_str(it.get('confidence',''))}")
        if it.get('notes'):
            lines.append(f"notes: {yaml_str(it.get('notes'))}")
        lines.append('```')
        lines.append('')

lines.append('---')
lines.append('')
lines.append('## Notas sobre o pipeline de execução')
lines.append('')
lines.append('- **Descoberta:** quatro subagentes em paralelo, cada um cobrindo uma sub-questão com 3–7 buscas direcionadas via `pplx search web` com filtros `--domains` por repositório-alvo.')
lines.append('- **Recuperação:** páginas promissoras lidas via `pplx content fetch` com prompts dedicados à extração de manifesto IIIF, ano, autor, técnica, direitos e tradução iconográfica.')
lines.append('- **Validação:** verificação de 13 campos obrigatórios + canonização e dedup contra 368 URLs já indexadas em `corpus-data.json` + `corpus-data-enriched.json` + backup `corpus-data.json.bak.20260516_160309`.')
lines.append('- **ICONCLASS:** códigos normalizados (`44G`, `44G3`, `48C51`, `11MM31`, `11MM`, `44A31`, `92`, `25F`). Itens sem código atribuído explicitamente receberam `11MM31` e/ou `48C51` quando motif/descrição indicaram alegoria de Iustitia.')
lines.append('- **IIIF:** capturado quando o repositório expõe Presentation API. SQ3 alcança 100 % por desenho; SQ4 atinge 70 % (algumas edições antigas de Alciato e a escultura de Loscher não têm manifesto); SQ2 fica em 0 % porque as bases latino-americanas raramente expõem IIIF — `url` e `thumbnail_url` cobrem o registro.')
lines.append('- **Rejeições:** 1 item (Ripa 1603 Heidelberg) foi rejeitado por já estar no corpus enriquecido.')
lines.append('')
lines.append('## Próximos passos sugeridos')
lines.append('')
lines.append('1. Revisão acadêmica manual dos 43 candidatos (especialmente SQ2, onde a curadoria de obras de Pedro Américo / Victor Meirelles / Portinari pode ter implicações de copyright para Portinari).')
lines.append('2. *Merge* incremental em `corpus-data-enriched.json` — sugiro acrescentar campo `provenance_pipeline: "iconocracia-2026-05-19"` para rastreabilidade.')
lines.append('3. Resolução de manifestos IIIF dos itens SQ1 que dependem da Library of Congress (LoC oferece IIIF para muitas imagens via `tile.loc.gov` — endpoint a verificar caso a caso).')
lines.append('4. Para a próxima rodada: SQ5 dedicado a *banknotes/stamps* fora do Numista (Banco Central de cada país, museus filatélicos) e SQ6 dedicado a moedas (museu numismático ANS, MoneyMuseum Zürich) — ambas áreas pouco cobertas pelo corpus atual.')
lines.append('')

with open(OUT,'w',encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f"Wrote {OUT}: {len(lines)} lines, {os.path.getsize(OUT)} bytes")
