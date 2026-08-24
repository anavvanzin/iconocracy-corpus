# Task: Mapa Warburguiano Interativo de Conexões (ICONOCRACIA)

Implementar visualização de rede D3.js onde nós são itens do corpus ICONOCRACIA e arestas são "pontes visuais" (Visual Bridges), para descobrir *Pathosformeln* não-óbvias entre nações e séculos que uma leitura linear do corpus não revela.

## Fonte de dados (verificada 2026-08-24)

`corpus-data.json` do repo `iconocracy-corpus` — **335 itens**, campos por item:

```json
{
  "id": "…", "country": "…", "url": "…", "title": "…",
  "description": "…", "motif": "…", "date": "…",
  "regime": "fundacional | normativo | militar | contra-alegoria",
  "endurecimento_score": 0.0,
  "indicadores": {
    "desincorporacao": 0, "rigidez_postural": 0, "dessexualizacao": 0,
    "uniformizacao_facial": 0, "heraldizacao": 0,
    "enquadramento_arquitetonico": 0, "apagamento_narrativo": 0,
    "monocromatizacao": 0, "serialidade": 0, "inscricao_estatal": 0
  },
  "citation_abnt": "…", "support": "…", "audit_flags": []
}
```

**Atenção**: NÃO existe campo Iconclass em `corpus-data.json` (a ideia original citava "shared Iconclass codes" — inviável sem enriquecimento). Arestas devem usar os campos reais acima.

## Requisitos

### Grafo
- **Nós**: os 335 itens. Cor por `regime` (4 categorias), tamanho por `endurecimento_score`, tooltip com `title`, `country`, `date`, `motif`, thumbnail via `url` quando imagem.
- **Arestas ("pontes visuais")**, ponderadas, geradas por pré-processamento:
  1. **Similaridade de endurecimento**: distância L1 baixa entre vetores `indicadores` (10-dim, escala 0–3) — limiar configurável (default: distância ≤ 3).
  2. **Motivo compartilhado**: mesmo `motif` (ou interseção de tokens do motif).
  3. Bônus de peso quando a ponte cruza `country` diferente E século diferente (extrair século de `date`) — são as *Pathosformeln* interessantes.
- **Filtros de UI**: por regime, país, intervalo de datas, tipo de ponte, limiar de similaridade (slider).
- **Interação**: clique no nó → painel lateral com metadados completos + `citation_abnt`; clique na aresta → "por que estas duas se conectam" (indicadores compartilhados, delta por indicador).

### Descoberta de Pathosformel
- Ranking das top-N pontes cross-nacional/cross-século por peso, exportável em markdown (insumo para painéis Warburguianos da tese).
- Detecção de comunidades (louvain ou componentes por limiar) para sugerir "painéis" candidatos.

## Tech Stack
- HTML/JS estático + D3.js v7 (force-directed), sem build complexo — mesmo estilo do site `anavvanzin`.
- Pré-processamento das arestas em script Python (env conda `iconocracy`, path version-agnostic `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python`) gerando `graph-data.json` estático; a página só consome o JSON.
- Corpus é **exploratório e crescente** — o script de pré-processamento deve ser re-executável em qualquer snapshot; nunca fixar N=335 no código ou na prosa.

## Fora de escopo
- Enriquecimento Iconclass (existe `iconclass-db` separado; integração é follow-up).
- Ideias 4 ("Living Manuscript") e 5 ("Prediction API") do mesmo brainstorm — tasks separadas.

## Critérios de aceite
- Grafo carrega os itens do snapshot atual do corpus com os 4 regimes distinguíveis.
- Pelo menos um filtro por tipo de ponte e um slider de limiar funcionais.
- Export markdown do ranking de pontes cross-nacional/cross-século funciona.
- `graph-data.json` regenerável com um comando documentado.
