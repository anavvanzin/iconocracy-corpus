# Relatório de Auditoria — Piloto de Recodificação IconoCode

**Data:** 24 de julho de 2026  
**Escopo:** 15 registros (lote-piloto dos 159 sob auditoria)  
**Método:** IconoCode completo — acesso à imagem, 3 níveis de Panofsky, 10 indicadores de purificação (0–4), recálculo do score de ENDURECIMENTO  
**Fonte:** `corpus/corpus-data.json` · anavvanzin/iconocracy-corpus

## Síntese

- **12 de 15 recodificados** com medição visual real (imagem vista, 10 indicadores pontuados).
- **3 não recodificáveis** — link morto, URL errada ou face não confirmada; score-artefato removido e marcados `#verificar-imagem`.
- Range de scores obtidos: **1.2–3.0** (média 2.23).
- **4 correções de regime** face à classificação de baixa confiança original.

## Tabela antes → depois

| ID | Título | Regime antes → depois | Score antes → depois | Confiança |
|----|--------|----------------------|---------------------|-----------|
| `03a9622f-6` | 20 Cruzeiros, Tesouro Nacional, 1ª estampa ( | militar → **normativo** | 0.0 → 2.7 | medio |
| `089fc944-3` | 100 Lire - Vittorio Emanuele III (Italia sta | militar | 0.0 → 2.6 | alto |
| `08da86db-8` | 10 Lire \"Biga\" — Vittorio Emanuele III (It | militar | 0.0 → 2.0 | alto |
| `0bf85996-a` | Cédula 5 Cruzeiros (carimbo/sobreimpressão s | militar | 0.0 → removido | baixo |
| `1589cd9a-0` | 1000 Francs Déesse Déméter (type 1942) — Ban | militar → **normativo** | 0.0 → 2.1 | alto |
| `BR-023` | Alegoria à República — Capa da Revista Illus | fundacional | 1.4 → removido | baixo |
| `BR-027` | Alegoria da República Brasileira — Revista I | fundacional | 1.4 → 1.2 | alto |
| `BR-038` | Revista Illustrada — Alegoria da República ( | normativo | 1.4 → removido | baixo |
| `BR-041` | Alegoria à Lei de 13 de Maio de 1888 (estudo | fundacional | 1.4 → 1.3 | medio |
| `BE-CONGO-M` | Monument aux Pionniers Belges au Congo — La  | militar | 0.0 → 2.4 | alto |
| `FR-ASSIGNA` | Assignat de 400 livres (21 nov. 1792, an pre | fundacional → **contra-alegoria** | 0.0 → 3.0 | alto |
| `US-BANNER-` | Hail! Glorious Banner of Our Land — Columbia | militar | 0.0 → 1.3 | alto |
| `DE-GERM-19` | Germania — Reichspost / Deutsches Reich Defi | militar → **normativo** | 2.0 → 3.0 | alto |
| `FR-SEM-SEL` | Semeuse — Selo Definitivo da República Franc | normativo | 1.7 → 2.6 | alto |
| `US-SLQ-191` | Standing Liberty Quarter — Liberty with Shie | normativo | 1.4 → 2.5 | alto |

## Achados metodológicos do piloto

Três problemas que a coleta cega teria propagado, agora corrigidos:

1. **Erros de catalogação (URL ↔ conteúdo):** `BR-023` — a URL aponta para a capa nº 566 da Revista Illustrada, que na verdade é um **retrato do comandante chileno Constantino Bannen, sem qualquer alegoria feminina**. Registro sinalizado para correção de catalogação, não recodificável.

2. **Scores-artefato mascarando ausência de medição:** os 105 registros com 0,0 e 43 com 1,4 não eram medições. No piloto, cada 0,0/1,4 foi substituído por medição real (ex.: Germania 1900 → **3,0**; Semeuse 1903 → **2,6**) ou removido quando a imagem não pôde ser vista.

3. **Regimes mal atribuídos:** `FR-ASSIGNAT-1792` foi reclassificado de Fundacional para **CONTRA-ALEGORIA / #ausencia-alegorica** — a imagem real não tem corpo feminino, apenas águia republicana com fasces e barrete. Um contra-exemplo valioso. O 20 Cruzeiros BR e o 1000 Francs Déméter passaram de Militar (artefato) para **NORMATIVO** por ausência de marcadores militares.

## Ponto de atenção para revisão

- `US-BANNER-1861` (Columbia, litografia patriótica da Guerra Civil) foi classificado como **MILITAR** com score 1,3 — o score baixo sugere corpo ainda dinâmico/fundacional; vale sua revisão se o rótulo MILITAR se sustenta ou se é FUNDACIONAL com carga bélica.
- `FR-ASSIGNAT-1792` recebeu score 3,0 alto por ausência total do corpo (desincorporação máxima) — coerente com CONTRA-ALEGORIA por ausência, mas registre se prefere tratar ausência com score ou com marcação categórica.

## Próximo passo

Validado o método, restam **144 registros** sob auditoria. Proponho processá-los em ~10 lotes paralelos, mantendo o mesmo protocolo e os três formatos de saída, seguido de um Pull Request único em anavvanzin/iconocracy-corpus para seu merge.