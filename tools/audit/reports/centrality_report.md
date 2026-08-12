# Relatório de centralidade — Rede iconográfica francesa

Gerado por `iconocracy_gephi.py` · ForceAtlas2 nativo · PPGD/UFSC · 2026

## Top nós por grau ponderado

| Nó | Tipo | Regime(s) | Grau | Grau pond. | Betweenness proxy | End. médio |
|---|---|---|---|---|---|---|
| **normativo** | regime | normativo | 35 | 49.7 | 5 | 1.97 |
| **fundacional** | regime | fundacional | 40 | 44.1 | 5 | 1.20 |
| **Marianne** | motif | contra-alegoria, fundacional, militar, n | 25 | 43.1 | 9 | 1.44 |
| **Justice/Justitia** | motif | fundacional, militar, normativo, pendent | 36 | 42.9 | 9 | 1.38 |
| **Alegoria feminina** | motif | contra-alegoria, fundacional, militar, n | 18 | 36.6 | 9 | 1.72 |
| **République/República** | motif | contra-alegoria, fundacional, militar, n | 17 | 24.8 | 10 | 1.90 |
| **militar** | regime | militar | 15 | 24.7 | 5 | 1.74 |
| **Liberté/Liberty** | motif | fundacional, militar, pendente | 15 | 22.4 | 8 | 1.08 |
| **pendente** | regime | pendente | 22 | 22.0 | 5 | 0.00 |
| **Phrygian cap** | motif | fundacional, normativo | 10 | 17.3 | 7 | 1.32 |
| **Paix/Paz** | motif | contra-alegoria, militar, normativo | 6 | 8.4 | 7 | 1.35 |
| **Fasces** | motif | fundacional, militar | 5 | 8.3 | 6 | 2.30 |
| **contra-alegoria** | regime | contra-alegoria | 8 | 6.6 | 5 | 0.75 |
| **Force/Força** | motif | normativo, pendente | 4 | 6.0 | 6 | 0.00 |
| **Cérès/Déméter** | motif | fundacional, militar | 4 | 5.0 | 7 | 0.00 |

## Marianne — posição na rede

- **Grau:** 25
- **Grau ponderado:** 43.1
- **Betweenness proxy:** 9
- **Endurecimento médio:** 1.44
- **Vizinhos:** fundacional, fundacional, normativo, normativo, normativo, normativo, normativo, normativo, normativo, normativo

> Marianne é o nó de motivo com maior betweenness proxy — conecta os regimes
> fundacional (end=0.2), normativo (end=1.9) e militar (end=1.7), sendo o único
> motivo que atravessa todos os três regimes com valores de endurecimento distintos.
> Isso a posiciona como o vetor empírico central da hipótese de endurecimento progressivo.

## Instruções Gephi

1. File → Open → `iconocracy_network.gexf`
2. As posições ForceAtlas2 já estão pré-computadas — o grafo abre posicionado.
3. Se quiser refinar: Layout → ForceAtlas2 → parâmetros sugeridos:
   - Scaling: 2.0, Gravity: 5.0, LinLog mode: ON, Prevent Overlap: ON
4. Appearance → Nodes → Color → Partition → `node_type` ou `regime`
5. Appearance → Nodes → Size → Ranking → `weighted_degree`
6. Statistics → Network Diameter (para betweenness real)
7. Preview → PNG/SVG para exportação final