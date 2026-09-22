---
titulo: "PENDING_REVIEW — 11 itens com codificação heurística"
criado: 2026-05-16
status: aguardando-revisão-manual
contexto: "Commit 82a6887 (25-abr-2026) — fechou 11 lacunas do `purification.jsonl` aplicando heurística por suporte/período. Antes da qualificação, esses scores precisam ser revisados manualmente."
---

# PENDING_REVIEW — 11 itens

Estes 11 registros do `data/processed/purification.jsonl` foram codificados
em 25 de abril de 2026 por heurística (suporte + período), com flag
`PENDING_REVIEW` no campo `coder_notes`. Eles **contam** no
`code_purification.py --status` (165/165) mas **não** devem ser
considerados codificação validada para fins de qualificação ou release HF.

## Lista

| item_id | País | Suporte | Período | Título |
|---|---|---|---|---|
| `BE-CONGO-1912` | Belgium | papel-moeda | 1912–1937 | 20 Francs Belgian Congo — Allegory of Europe with Mace |
| `BE-IND-1880` | Belgium | moeda | 1880 | 5 Francs — 50 ans de Belgique: La Belgique avec Constitution |
| `BR-2000R-1907` | Brazil | moeda | 1906–1912 | 2000 Réis — Efígie da República com Barrete Frígio |
| `DE-GERM-1900` | Germany | selo | 1900–1922 | Germania — Reichspost / Deutsches Reich Definitive Stamp |
| `DE-GERM-BELG-1914` | Germany | selo | 1914–1918 | Germania "Belgien" Overprint — Military Occupation Stamp |
| `FR-HERC-1870` | France | moeda | 1870–1878 | 5 Francs Hercule — La République et La Justice flanquando Hércules |
| `FR-PIAST-1885` | France | moeda | 1885–1928 | Piastre de Commerce — Marianne Assise avec Fasces |
| `FR-SEM-SELO-1903` | France | selo | 1903–1960 | Semeuse — Selo Definitivo da República Francesa (Oscar Roty) |
| `UK-PENNY-1860` | United Kingdom | moeda | 1860–1894 | Penny — Britannia Seated with Trident, Helmet and Shield |
| `UK-TRADE-1895` | United Kingdom | moeda | 1895–1935 | British Trade Dollar — Britannia Standing with Trident |
| `US-SLQ-1916` | United States | moeda | 1916–1930 | Standing Liberty Quarter — Liberty with Shield and Olive Branch |

## Protocolo sugerido de revisão

1. Para cada item, abrir a imagem em `data/raw/<XX>/<item_id>/` ou via
   `drive-manifest.json` e aplicar o codebook (`docs/CODEBOOK_PROMPTS.md`)
   diretamente — 10 indicadores ordinais 0–3.
2. Comparar com o score heurístico atual no `purification.jsonl`.
   Diferença ≥ 1 ponto em qualquer indicador → registrar a correção.
3. Atualizar o registro via `tools/scripts/code_purification.py` (a flag
   `PENDING_REVIEW` em `coder_notes` deve ser removida ao validar).
4. Concluir antes da qualificação (nov-2027).

## Como localizar via script

```bash
python3 -c "
import json
with open('data/processed/purification.jsonl') as f:
    for line in f:
        r = json.loads(line)
        if 'PENDING_REVIEW' in json.dumps(r):
            print(r.get('item_id'), '—', r.get('coder_notes', ''))
"
```

## Impacto em release

O `release-gate` deve continuar bloqueando o snapshot HF público
enquanto qualquer registro contiver `PENDING_REVIEW` em `coder_notes`
— os dados ainda são úteis para análise interna, mas não para
publicação até a revisão manual.
