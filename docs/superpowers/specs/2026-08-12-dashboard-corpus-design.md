# Design — Dashboard do Corpus v2 (pessoal, 4 abas)

**Data:** 2026-08-12 · **Status:** aprovado pela autora (aguardando revisão do documento)
**Contexto:** ferramenta analítica pessoal da pesquisa ICONOCRACIA. Audiência: a própria autora.
Conteúdo aprovado: 4 abas (Visão Geral · Explorar · Endurecimento · Qualidade do Pipeline).
Abordagem aprovada: **evoluir o dashboard canônico existente** (HTML único + gerador Python).

## Arquitetura

```
corpus/corpus-data.json  ─┐
corpus/agent-runs.json   ─┼─► tools/scripts/refresh_dashboard.py ─► corpus/DASHBOARD_CORPUS.html
input_url (thumbnails)   ─┘      (gerador idempotente)                 (HTML único, abre com duplo clique)
```

- **Gerador endurecido.** A troca de dados deixa de usar regex sobre `const DATA = [...]`
  (causa raiz da corrupção de 2026-08-12, quando um conflito de merge commitado deixou
  3 blocos DATA empilhados) e passa a usar delimitadores `// == DATA:BEGIN ==` /
  `// == DATA:END ==`. O gerador falha alto se não encontrar exatamente um par de delimitadores.
- **Validação round-trip.** Após embutir, o script re-parseia o JSON do arquivo final e confere
  a contagem contra `corpus-data.json`; divergência = exit 1. Rodar 2× seguidas produz
  arquivo idêntico (idempotência).
- **Sem base64.** Thumbnails apenas por URL externa derivada de `input_url`
  (padrões IIIF/Europeana/Gallica/Wikimedia/LOC). Sem thumbnail derivável → placeholder
  tipográfico com o motif do item. Meta: arquivo final < 1,5 MB.

## Fontes de dados

| Fonte | Uso |
|---|---|
| `corpus/corpus-data.json` | dados dos 335 registros (abas 1–3) |
| `corpus/agent-runs.json` | últimos runs do pipeline (aba 4) |
| `records.jsonl` → `input.input_url` | derivação de thumbnails |

Nota de qualidade conhecida: `year` é nulo em todo o export; datas vivem em `date`
(texto livre: "1943", "1931-XX-XX", "1926/1934", "17th century"). O dashboard deriva
ano do primeiro 4 dígitos 1400–2099 (mesma regra do backfill aplicado no Supabase,
cobre ~87% do corpus) e marca os ~13% restantes como "s/d".

## As 4 abas

### 1. Visão Geral
KPIs (N, % in_scope, países, suportes, período coberto) · registros por década (linha) ·
barras por regime · barras por país · barras por suporte.

### 2. Explorar (galeria)
Grid de cards com thumbnail · filtros combináveis (país, suporte, regime, motif,
busca livre em título/descrição) · ordenação (ano, score, mais recentes) ·
modal com ficha completa: 10 indicadores, descrição, `coded_by`, citação ABNT
(botão copiar), link externo.

### 3. Endurecimento
Histograma do score · heatmap 10 indicadores × regime · scatter ano × score
(pontos clicáveis → modal da ficha) · ranking de outliers (10 maiores / 10 menores) ·
médias por país. *Alimenta Caps. 7–9.*

### 4. Qualidade do Pipeline
`coded_by` (humano × instrumentos) · timeline de `coded_at` · campos faltantes
(% sem data, sem país, sem thumbnail) · últimos runs (`agent-runs.json`) ·
fonte ausente → aviso explícito na aba, nunca quebra silenciosa.

## Estética

Mantém a identidade atual: creme/marrom, Pixelify Sans para títulos, Inter para corpo,
sombras duras retrô. Chart.js via CDN (já em uso).

## Fora de escopo (YAGNI)

Sem servidor, sem framework, sem login, sem edição pelo dashboard, sem multi-usuário,
sem base64 de imagens.

## Erros e bordas

- `agent-runs.json` ausente → aba 4 renderiza aviso; demais abas intactas.
- Thumbnail quebrada → `onerror` troca por placeholder tipográfico.
- `corpus-data.json` com N diferente do embutido → gerador falha antes de escrever.

## Verificação

1. `python tools/scripts/refresh_dashboard.py --corpus` → OK + relatório de contagens.
2. Rodar 2× → `git diff` vazio.
3. Abrir o HTML: 4 abas navegáveis, gráficos renderizam, filtros da galeria combinam,
   modal abre ficha com citação ABNT.
4. pytest existente (`tests/`) continua verde.

## Trabalho futuro (fora deste spec)

Modo "live" lendo do Supabase (`corpus_items`, projeto ICONOCRACIA 1.0) via PostgREST +
publishable key, em vez de dados embutidos. Útil quando o corpus crescer ou para um
dashboard público. Não implementar agora — o design aprovado é com dados embutidos.
