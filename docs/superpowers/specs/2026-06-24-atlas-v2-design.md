# Atlas Iconocrático v2 — Design Doc

**Data:** 2026-06-24
**Status:** confirmed (Ana, 24-jun)
**Repo:** `iconocracia-atlas` (novo, irmão do companion)
**Domínio:** `atlas.iconocracia.com` → Cloudflare Worker
**Deadline:** versão 0 (prancha funcional) 2026-07-15; v1 público 2026-08-30

---

## 1. Diagnóstico do legado (atlaslab)

Três superfícies atuais no repo `anavvanzin/atlaslab`:

| Superfície | Função | Acertos | Falhas |
|---|---|---|---|
| `atlas/` | Catálogo informacional | Ficha por espécime | Sem visão de conjunto; não argumenta |
| `atlas-lab/` | Laboratório iconométrico | Distribuição de descritores | Dispositivo interno, não público |
| `canvas/` | Mapa conceitual topológico | 6 clusters Pathosformeln + arestas Nachleben | Tempo/geografia implícitos; sem montagem; é diagrama, não atlas warburguiano |

O canvas é boa síntese conceitual, mas é um **diagrama**, não um atlas. Warburg pedia uma superfície onde a pesquisadora **compõe constelações** — vizinhança importa mais que taxonomia.

---

## 2. Premissa

**Híbrido A-núcleo + B-mínimo como camada-índice**

### A. Mnemosyne Viva (superfície principal)
- Fundo preto, sem grid, imagens em escala livre
- Cartões de espécime arrastáveis
- Linhas curvas de filiação Nachleben entre espécimes
- Cada prancha = URL persistente + exportação PDF A0
- O atlas é a coleção de pranchas publicadas

### B. Cartografia Iconocrática (camada-índice)
- Mapa-mundi minimalista (Leaflet ou D3-geo)
- Timeline 1559–1992
- Pinos das pranchas publicadas por local de circulação primária
- Filtros por Pathosformel
- Estética editorial (tipo Manifesto: Cormorant Garamond, paper, rubrica)

**Argumento que sustenta:** "iconocracia tropical" como geografia de tradução, não de imitação. A camada-índice responde à pergunta "onde isso acontece?" sem roubar o protagonismo do gesto warburguiano.

---

## 3. Decisões de design (locked)

### 3.1 Unidade narrativa
**Espécime individual como átomo de manipulação + Prancha como unidade de publicação.**

- O usuário arrasta, escala e posiciona espécimes individuais
- Uma prancha contém 12–20 espécimes com posições livres
- Relação muitos-para-muitos: um espécime pode aparecer em várias pranchas
- Data model: `specimen → prancha` com tabela de junção

### 3.2 Interação primária
**Montagem** (arrastar, agrupar, traçar filiações, anotar, salvar) com suporte de navegação/busca.

Fluxo do usuário:
1. **Browse** — busca/filtra o corpus por Pathosformel, país, período, regime
2. **Select** — arrasta espécimes do browser para a prancha (ou clica "add")
3. **Arrange** — posiciona livremente, escala (slider ou pinch)
4. **Connect** — traça arestas de filiação entre pares, anota o tipo
5. **Annotate** — adiciona notas textuais à prancha (título, legenda, tese)
6. **Publish** — salva → URL canônica + PDF A0

### 3.3 Eixos organizadores
**Pathosformel** (busca/filtro) + **Filiação Nachleben** (espaço da prancha).

- Pathosformel estrutura o browser de seleção: "Libertas Armata", "Justiça Vendada", "Respublica Coroada", etc.
- Filiação organiza o espaço da prancha: arestas entre espécimes com tipo (`transformsFormula`, `absorbsFormula`, `invertsGesture`, `colonizesFormula`)
- Tempo e geografia: metadados visíveis no hover/tooltip, não eixos primários

### 3.4 Estética
**Mnemosyne warburguiano com a materialidade tátil da xilogravura (Gemini 24-jun).**

Design tokens herdados da exploração xilográfica:

```css
:root {
  --paper: #eee4cf;
  --folio: #fbf4e5;
  --ink: #11100c;
  --ash: #2a2821;
  --muted: #665e52;
  --bone: #eadfc8;
  --rule: #c6ae7c;
  --gold: #9a783d;
  --seal: #9d3a27;
  --black: #090a0d;

  --font-display: "Instrument Serif", Georgia, serif;
  --font-body: "Crimson Pro", Georgia, serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  --grain: url("data:image/svg+xml,..."); /* SVG feTurbulence */
  --ledger: linear-gradient(rgba(154,120,61,.09) 1px, transparent 1px),
            linear-gradient(90deg, rgba(154,120,61,.07) 1px, transparent 1px);
}
```

Características visuais:
- Fundo preto (#090a0d) com textura de grão para a superfície de montagem
- Imagens carregam em alta resolução do R2, com zoom suave
- Linhas de filiação: traço branco fino, curvo, com leve glow no hover
- Cartões de espécime: borda em ouro velho, selo de regime no canto
- Camada-índice: paper (#eee4cf), tipografia serif, rubrica, editorial limpo
- Sem grid visível — posições completamente livres (o grid é conceitual, não visual)
- Exportação PDF A0: @media print com fundo preto, imagens em CMYK aproximado

### 3.5 Suporte técnico
**Web app interativa (HTML/JS vanilla ou minimal framework) + Cloudflare Worker + R2 + KV.**

- Sem React/Next.js (o atlas não é SPA tradicional — é uma superfície de montagem)
- Vanilla JS com Web Components ou lit-element para os cartões
- Canvas API ou SVG para as arestas de filiação
- R2 `iconocracia-images` (já existente) para assets de imagem
- KV `ATLAS_KV` para estado das pranchas (metadados leves)
- PDF A0 gerado client-side via `@media print` + `window.print()` ou server-side via Puppeteer no Worker (Browsercrab)
- Schema `pranchas.jsonld` versionado no repo, servido como JSON estático

---

## 4. Data Model

### 4.1 Fonte canônica (imutável)

`corpus.jsonld` — 299 espécimes (corpus-data.json exportado). Cada espécime tem:
- `id` (UUID)
- `country`, `title`, `date`, `description`
- `regime` (fundacional | normativo | militar | contra-alegoria)
- `indicadores` (10 indicadores ordinais 0–3)
- `endurecimento_score` (composite float)
- `support`, `motif`, `citation_abnt`
- `url` (imagem fonte)

**Regra:** O corpus não sabe que existe atlas. O atlas referencia o corpus por ID. Schema único, sem acoplamento.

### 4.2 pranchas.jsonld (novo schema)

```jsonld
{
  "@context": "https://schema.iconocracia.org/atlas-v2",
  "pranchas": [
    {
      "id": "prancha-7",
      "title": "Respublica Coroada na transição imperial brasileira",
      "author": "Ana Vanzin",
      "created": "2026-07-15T00:00:00Z",
      "modified": "2026-07-20T00:00:00Z",
      "status": "published",
      "pathosformel": "Respublica Coroada",
      "specimens": [
        {
          "ref": "BR-REPUBLICA-1889-01",
          "x": 0.32,
          "y": 0.18,
          "scale": 1.0,
          "rotation": 0
        },
        {
          "ref": "BR-REPUBLICA-1891-03",
          "x": 0.65,
          "y": 0.22,
          "scale": 0.85,
          "rotation": 0
        }
      ],
      "edges": [
        {
          "from": "BR-REPUBLICA-1889-01",
          "to": "BR-REPUBLICA-1891-03",
          "type": "absorbsFormula",
          "annotation": "A coroa migra do imperador para a figura feminina — republicanização do atributo monárquico"
        }
      ],
      "annotations": [
        {
          "x": 0.15,
          "y": 0.85,
          "text": "Transição 1889–1891: o corpo da República herda a coroa, mas perde o cetro",
          "style": "thesis"
        }
      ],
      "bbox": {"x": 0, "y": 0, "w": 1, "h": 1}
    }
  ]
}
```

**Campos:**
- `specimens[]`: posições como frações do viewport (0–1), permite responsividade
- `edges[]`: arestas de filiação com tipo controlado (`transformsFormula`, `absorbsFormula`, `invertsGesture`, `colonizesFormula`)
- `annotations[]`: notas textuais posicionadas livremente na prancha
- `status`: `draft | published` — só pranchas published aparecem na camada-índice pública

### 4.3 Separação de concerns

| Fonte | Responsabilidade | Mutabilidade |
|---|---|---|
| `corpus.jsonld` | Espécimes, metadados, indicadores | Imutável (só pipeline) |
| `pranchas.jsonld` | Composições, filiações, notas | Mutável (curadoria) |
| KV `ATLAS_KV` | Estado de edição em tempo real, drafts | Volátil |
| R2 `iconocracia-images` | Assets de imagem (já existente) | Append-only |

---

## 5. Arquitetura técnica

### 5.1 Stack

```
atlas.iconocracia.com
└── Cloudflare Worker (iconocracia-atlas)
    ├── Static assets (HTML, JS, CSS, fonts) → Assets binding
    ├── corpus.jsonld → R2 ou Assets (readonly)
    ├── pranchas.jsonld → R2 + KV (read/write via API)
    ├── ATLAS_KV → estado de edição, drafts
    └── iconocracia-images (R2) → assets de imagem
```

### 5.2 Rotas do Worker

| Método | Rota | Função |
|---|---|---|
| `GET` | `/` | Camada-índice (mapa editorial) |
| `GET` | `/atlas` | Superfície de montagem (Mnemosyne Viva) |
| `GET` | `/prancha/:id` | Prancha publicada (modo leitura) |
| `GET` | `/prancha/:id/edit` | Prancha em edição (modo montagem) |
| `GET` | `/api/corpus` | Lista de espécimes (com filtros) |
| `GET` | `/api/corpus/:id` | Espécime individual |
| `GET` | `/api/pranchas` | Lista de pranchas publicadas |
| `PUT` | `/api/prancha/:id` | Salvar prancha (autenticado) |
| `GET` | `/api/prancha/:id/pdf` | Exportar PDF A0 |

### 5.3 Frontend

- HTML vanilla + CSS custom properties + ES modules
- Sem framework — a superfície de montagem é um canvas interativo, não uma árvore de componentes
- `canvas` element ou SVG layer para arestas de filiação
- `drag-and-drop` nativo (HTML5 Drag API ou pointer events)
- `transform: scale()` para zoom dos cartões
- Fontes: Instrument Serif, Crimson Pro, JetBrains Mono (self-hosted, subset WOFF2)
- PDF A0: CSS `@page { size: A0; }` + `window.print()` com regras específicas

### 5.4 Autenticação

- Cloudflare Access ou token simples em header para endpoints `PUT`
- Modo leitura: público, sem auth
- Modo edição: protegido (só Ana)

---

## 6. Modos de interação (detalhado)

### 6.1 Camada-índice (modo mapa)

```
┌──────────────────────────────────────────────────────┐
│  ICONOCRACIA · Atlas                                  │
│  Cartografia iconocrática 1559–1992                    │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │              MAPA-MUNDI                          │ │
│  │    ● Paris (3 pranchas)                          │ │
│  │    ● Rio de Janeiro (4 pranchas)                 │ │
│  │    ● Bruxelas (1 prancha)                        │ │
│  │    ● Berlim (2 pranchas)                         │ │
│  │                                                  │ │
│  └──────────────────────────────────────────────────┘ │
│  ────●────────●────────●────────●────────●──→ tempo  │
│  1559   1789    1848    1889    1914    1992          │
│                                                        │
│  Filtros: [Pathosformel ▾] [Regime ▾] [País ▾]        │
│                                                        │
│  Pranchas publicadas:                                  │
│  · Prancha 7 — Respublica Coroada (BR, 1889–1891)     │
│  · Prancha 3 — Libertas Armata (FR, 1789–1848)        │
│  ...                                                    │
│                                                        │
│  [Abrir Atlas →]                                       │
└──────────────────────────────────────────────────────┘
```

Estética: editorial (Manifesto) — Cormorant Garamond, paper #F2EAD9, rubrica #9B2C1C, gold #9C7C3D.

### 6.2 Superfície de montagem (modo Mnemosyne Viva)

```
┌──────────────────────────────────────────────────────┐
│  [Índice] [Nova Prancha]        [Salvar] [Exportar]   │
│                                                        │
│  ┌──────────┐  ┌─────────────────────────────────────┐│
│  │ Busca     │  │                                     ││
│  │           │  │     ┌─────┐                         ││
│  │ Pathos:   │  │     │ BR  │    ╲                    ││
│  │ [Libertas]│  │     │1889 │     ╲ absorbsFormula    ││
│  │           │  │     └─────┘      ╲                  ││
│  │ País:     │  │                   ┌─────┐           ││
│  │ [BR ▾]   │  │                   │ FR  │           ││
│  │           │  │    ┌─────┐       │1848 │           ││
│  │ Período:  │  │    │ BR  │       └─────┘           ││
│  │ [1800-1900]│  │    │1891 │                         ││
│  │           │  │    └─────┘     ┌─────┐              ││
│  │           │  │                │ BE  │              ││
│  │ [Aplicar] │  │                │1832 │              ││
│  │           │  │                └─────┘              ││
│  │ ────────  │  │                                     ││
│  │ Resultados│  │  Nota: "Transição 1889–1891:       ││
│  │           │  │  o corpo da República herda a      ││
│  │ ☐ BR-1889 │  │  coroa, mas perde o cetro"         ││
│  │ ☐ BR-1891 │  │                                     ││
│  │ ☐ FR-1848 │  │                                     ││
│  │ ☐ BE-1832 │  │                                     ││
│  │           │  │                                     ││
│  │ [Add →]  │  │                                     ││
│  └──────────┘  └─────────────────────────────────────┘│
└──────────────────────────────────────────────────────┘
```

Estética: xilogravura — fundo preto (#090a0d), textura de grão, ouro/lacre, Instrument Serif + Crimson Pro.

### 6.3 Interações da superfície de montagem

| Gesto | Ação |
|---|---|
| Arrastar do browser → prancha | Adiciona espécime na posição do drop |
| Arrastar na prancha | Reposiciona espécime |
| Scroll/pinch | Zoom na prancha (não nos cartões individuais) |
| Slider no cartão | Escala individual do espécime |
| Shift+arrastar de A → B | Cria aresta de filiação (abre popover para escolher tipo) |
| Duplo clique na aresta | Edita anotação da filiação |
| Clique direito no espaço vazio | Adiciona nota textual |
| Tecla Delete (com seleção) | Remove espécime/aresta/nota |
| Ctrl+S | Salva prancha |

### 6.4 Modo leitura (prancha publicada)

- URL canônica: `atlas.iconocracia.com/prancha/7`
- Visualização em tela cheia, sem controles de edição
- Hover nos espécimes mostra metadados (título, data, país, regime)
- Hover nas arestas mostra tipo de filiação e anotação
- Botão "Exportar PDF (A0)" e "Download PNG"
- Citação ABNT da prancha gerada automaticamente

---

## 7. Exportação PDF A0

```css
@media print {
  @page {
    size: A0;
    margin: 15mm;
    background: #090a0d;
  }

  body {
    background: #090a0d;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .prancha-surface {
    width: 1189mm;  /* A0 width */
    height: 841mm;  /* A0 height */
    position: relative;
  }

  /* Imagens em RGB → CMYK aproximado */
  .specimen-card img {
    image-rendering: auto;
  }

  /* Esconder controles */
  .toolbar, .browser-panel, .edge-popover { display: none; }
}
```

---

## 8. Roadmap

### Fase 0 — Setup (24–27 jun)
- [ ] Criar repo `iconocracia-atlas` no GitHub
- [ ] Configurar Worker + R2 + KV no Cloudflare
- [ ] Apontar `atlas.iconocracia.com` (CNAME → Worker)
- [ ] Criar `pranchas.jsonld` schema + validador
- [ ] Self-host fonts (subset WOFF2 de Instrument Serif, Crimson Pro, JetBrains Mono)
- [ ] Estrutura de diretórios: `src/`, `public/`, `schemas/`, `scripts/`

### Fase 1 — Camada-índice (28 jun – 2 jul)
- [ ] Mapa-mundi interativo (Leaflet ou D3-geo)
- [ ] Timeline 1559–1992
- [ ] Filtros por Pathosformel, regime, país
- [ ] Lista de pranchas publicadas
- [ ] Estética editorial Manifesto (Cormorant Garamond, paper, rubrica)

### Fase 2 — Superfície de montagem (3–12 jul)
- [ ] Browser de espécimes (busca, filtro, resultados)
- [ ] Canvas de montagem (fundo preto, textura de grão, sem grid)
- [ ] Drag-and-drop de cartões
- [ ] Escala individual (slider)
- [ ] Arestas de filiação (SVG curvas + tipo + anotação)
- [ ] Notas textuais posicionáveis
- [ ] Salvamento em KV + pranchas.jsonld
- [ ] Modo leitura (URL canônica)

### Fase 3 — Exportação e publicação (13–15 jul)
- [ ] PDF A0 via @media print
- [ ] Download PNG (html2canvas ou API Canvas)
- [ ] Citação ABNT automática da prancha
- [ ] Deploy em produção (atlas.iconocracia.com)

### Fase 4 — Expansão (16 jul – 30 ago)
- [ ] Autenticação para edição (Cloudflare Access)
- [ ] Múltiplas pranchas simultâneas (tabs?)
- [ ] Histórico de versões da prancha
- [ ] Embed da prancha em capítulos da tese (iframe ou PNG)
- [ ] Integração com companion app (link recíproco)

---

## 9. Referências

- Warburg, A. *Der Bilderatlas Mnemosyne* (1924–1929)
- Gemini design exploration, 24-jun-2026: `/Users/ana/Downloads/iconocracia-design-system/Gemini 24 junho/`
- Design tokens: `ssdfdsfs/uploads/index.html` (xilogravura companion)
- Editorial style: `Iconocracia - Manifesto.dc.html`
- Corpus schema: `iconocracy-corpus/corpus/corpus-data.json` (299 items, 2026-06-23)
- Atlaslab legado: `anavvanzin/atlaslab` (atlas/, atlas-lab/, canvas/)

---

## 10. Decisões locked (24-jun)

| Decisão | Valor |
|---|---|
| Premissa | A-núcleo (Mnemosyne Viva) + B-mínimo (cartografia índice) |
| Unidade | Espécime (átomo) + Prancha (publicação) |
| Interação | Montagem com suporte de navegação |
| Eixo | Pathosformel (busca) + Nachleben (espaço) |
| Estética | Xilogravura warburguiana (Gemini tokens) |
| Stack | Cloudflare Worker + R2 + KV, vanilla JS |
| Domínio | atlas.iconocracia.com |
| Repo | iconocracia-atlas (novo) |
| Schema | corpus.jsonld (imutável) + pranchas.jsonld (mutável) |
| Prazo v0 | 2026-07-15 |
