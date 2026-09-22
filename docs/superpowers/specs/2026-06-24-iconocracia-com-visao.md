# iconocracia.com — Visão

**Data:** 2026-06-24
**Status:** em construção com Ana
**Domínio:** `iconocracia.com` (comprado 24-jun-2026)
**Repositório:** `iconocracia-atlas` (a ser criado)
**Stack:** Cloudflare Workers + R2 + KV + D1

---

## 0. Não-negociáveis

1. **Zero IA visível.** Nenhum chatbot, nenhum "ask AI", nenhum botão de "gerar". A inteligência do site é a curadoria humana — da Ana e de colaboradores. Assistentes internos para moderação e busca semântica rodam invisíveis, nunca na interface.

2. **A tese é o site. O site é a tese.** Não existe "site institucional + seção de atlas". Tudo é uma superfície contínua. O sumário é um mapa. Os capítulos são alas. O atlas é o chão.

3. **Dinâmico, não estático.** Cada prancha, cada capítulo, cada ficha é viva — gerada a partir de `corpus.jsonld` e `pranchas.jsonld`, não compilada em HTML estático.

4. **Materialidade importa.** Cada superfície tem sua própria textura, tipografia, ritmo. A xilogravura do atlas não é a mesma pele do manifesto editorial. O visitante sente que mudou de sala.

---

## 1. Superfícies (não "páginas")

### 1.1 Manifesto
**Rota:** `/`

Aterrissagem imersiva. Não é landing page — é experiência de entrada.

- Texto do manifesto da tese em camadas visuais (tipo o `.dc.html` que o Gemini gerou com Cormorant Garamond + rubrica)
- À medida que o visitante desce, fragmentos do corpus aparecem nas margens
- Trilha sonora opcional: gravação de arquivo, leitura de fonte primária em voz (Paris Paloma "LABOUR" como referência de atmosfera — ruído industrial + vocal etéreo)
- Sem scroll infinito — 4-5 telas de profundidade, cada uma um argumento visual
- Último quadro: convite para entrar no atlas

### 1.2 Atlas (Mnemosyne Viva)
**Rota:** `/atlas`

A superfície principal. Especificação técnica no design doc `2026-06-24-atlas-v2-design.md`. Resumo:

- Fundo preto com textura de grão, sem grid
- Browser lateral de espécimes (busca por Pathosformel, país, período, regime)
- Canvas infinito de montagem: arrasta, escala, conecta, anota
- Arestas de filiação Nachleben entre espécimes
- Pranchas publicadas com URL canônica (`/prancha/:id`)
- Exportação PDF A0
- Modo visitante: pode explorar pranchas publicadas e montar a sua própria (efêmera, não salva)

### 1.3 Tese
**Rota:** `/tese`

Os capítulos como organismos navegáveis.

- Sumário como mapa topológico, não lista — cada capítulo é um nó com conexões visíveis aos outros
- Dentro de um capítulo: texto acadêmico com figuras do corpus embedadas inline, notas expandíveis, citações linkadas à Biblioteca
- Cada figura no texto é clicável → abre ficha do espécime no corpus
- "Meta-pranchas": cada capítulo tem 1-3 pranchas do atlas que sintetizam seu argumento visual
- Modo leitura limpo (tipografia serif, paper background, sem distrações) + modo anotado (marginália, links, metadados)
- Citação ABNT automática no footer de cada capítulo

### 1.4 Corpus
**Rota:** `/corpus`

Browser de espécimes. Porta de entrada para pesquisadores.

- Busca facetada: Pathosformel, regime, país, período, suporte, indicadores
- Grid de cartões com thumbnail, título, data, regime (cor do selo)
- Ficha completa com todos os metadados, indicadores, provenance, citação ABNT
- Link reverso: "este espécime aparece em X pranchas, Y capítulos"
- Submissão de novos espécimes (moderada, formulário com validação de schema)
- Download: imagem em alta + metadados em JSON

### 1.5 Biblioteca
**Rota:** `/biblioteca`

Zotero vivo + glossário da tese.

- Todas as referências bibliográficas da tese com busca, filtro, link reverso ("citado em Cap. 3, Prancha 7")
- Glossário de termos próprios: endurecimento, Pathosformel, Feminilidade de Estado, Contrato Sexual Visual, Zwischenraum, Nachleben, Purificação Clássica
- Cada termo linka para ocorrências no texto da tese e para pranchas que o mobilizam
- Integração com Zotero API (leitura pública do grupo ICONOCRACIA)

### 1.6 Comunidade
**Rota:** `/comunidade`

Curadoria coletiva.

- Pesquisadores convidados podem submeter espécimes, comentar pranchas, propor filiações
- "Remixes": qualquer prancha publicada pode ser duplicada, reorganizada e republicada como "variação sobre Prancha 7 por [nome]"
- Cada contribuição é creditada, versionada, rastreável
- Moderação pela Ana (dashboard interno, não público)

### 1.7 Sobre
**Rota:** `/sobre`

- Lattes, ORCID, PPGD/UFSC, UGent, orientadores
- Linha do tempo da pesquisa (versão navegável do que está em `iconocracia-trajetoria.anavanzin.workers.dev`)
- 22 artefatos produzidos (artigos, apresentações, qualificação)
- Contato (sem AI — formulário ou email)

---

## 2. Arquitetura de dados

```
corpus.jsonld          ← imutável, pipeline de exportação (299 espécimes)
pranchas.jsonld        ← mutável, curadoria (pranchas, filiações, notas)
D1 (SQLite)            ← submissões da comunidade, comentários, remixes
KV (ATLAS_KV)          ← estado de edição, drafts, cache
R2 (iconocracia-images) ← assets de imagem (já existente)
R2 (iconocracia-site)   ← assets estáticos (fonts, áudio, manifestos)
```

### Relações

```
espécime ──→ prancha (muitos-para-muitos, via pranchas.jsonld)
prancha  ──→ capítulo (muitos-para-muitos, via metadados)
capítulo ──→ referência bibliográfica (via Zotero)
espécime ──→ referência bibliográfica (via corpus.jsonld.citation_abnt)
termo    ──→ ocorrências (capítulos, pranchas, notas)
```

---

## 3. Navegação

Não é hierárquica. É espacial.

- **Navegação primária:** barra inferior persistente com as 5 superfícies (Manifesto, Atlas, Tese, Corpus, Biblioteca)
- **Navegação contextual:** dentro de qualquer superfície, links para superfícies relacionadas (ex: ficha de espécime → "ver no atlas", "ver na tese")
- **Histórico de deriva:** o visitante pode ver o caminho que percorreu (tipo breadcrumb temporal: "Manifesto → Atlas → Prancha 7 → Ficha BR-1889 → Capítulo 3")
- **Busca global:** `/busca` — pesquisa em todas as superfícies simultaneamente

---

## 4. Multi-modalidade

Cada superfície tem sua própria materialidade:

| Superfície | Estética | Tipografia | Background |
|---|---|---|---|
| Manifesto | Editorial imersivo | Cormorant Garamond + Hanken Grotesk | Paper #F2EAD9 com transições escuras |
| Atlas | Xilogravura warburguiana | Instrument Serif + Crimson Pro + JetBrains Mono | Preto #090a0d com grão |
| Tese | Editorial acadêmico | Cormorant Garamond + Crimson Pro | Paper #F2EAD9 limpo |
| Corpus | Arquivístico | Crimson Pro + JetBrains Mono | Bone #EADFC8 com ledger |
| Biblioteca | Tipográfico | Instrument Serif + JetBrains Mono | Cream #F7F0E1 |

**Áudio ambiente (opcional, desligado por padrão):**
- Manifesto: leitura do texto em voz + ambiente sonoro
- Atlas: silêncio + som de página virando ao trocar de prancha
- Tese: nada (leitura é silenciosa)

---

## 5. Stack técnica

```
iconocracia.com
└── Cloudflare Worker (iconocracia-site)
    ├── Roteamento por superfície (manifesto, atlas, tese, corpus, biblioteca)
    ├── Static assets via Workers Assets (fonts, CSS, JS, áudio)
    ├── corpus.jsonld → R2 (readonly, cache agressivo)
    ├── pranchas.jsonld → R2 + KV (read/write autenticado)
    ├── D1 → submissões, comentários, remixes
    ├── KV → drafts, cache, sessões de edição
    └── R2 iconocracia-images → assets de imagem (cache CDN)
```

**Frontend:**
- HTML vanilla + CSS custom properties + ES modules
- Sem framework — cada superfície é um `custom element` ou módulo independente
- Compartilham: design tokens, fontes, client de API, componentes de busca
- Diferenciam: layout, tipografia, background, comportamento
- Hydration a partir de JSON (corpus.jsonld, pranchas.jsonld) — sem SSR necessário

**Performance:**
- Fontes: subset WOFF2, self-hosted, `font-display: swap`
- Imagens: R2 + CDN cache, WebP/AVIF com fallback JPEG
- corpus.jsonld: servido com `Cache-Control: public, max-age=3600`
- pranchas.jsonld: cache curto (5 min) para refletir edições
- D1 queries: cache em KV com TTL de 15 min

---

## 6. O que NÃO entra (por enquanto)

- ❌ Chatbot, assistente de IA, "ask me anything"
- ❌ Geração automática de texto ou análise
- ❌ Login público (só Ana edita; comunidade via formulário moderado)
- ❌ Paywall, anúncios, analytics de terceiros
- ❌ Next.js, React, Vue, Svelte — sem framework JS pesado
- ❌ Subdomínio `atlas.` — é tudo `iconocracia.com`

---

## 7. Fases

### Fase 0 — Fundação (jun 24–27)
- [ ] Repo `iconocracia-atlas` (ou `iconocracia-site`)
- [ ] Worker configurado + domínio `iconocracia.com` no Cloudflare
- [ ] R2 buckets, KV namespace, D1 database
- [ ] Design tokens (CSS custom properties de todas as superfícies)
- [ ] Fontes self-hosted (subset WOFF2)
- [ ] Schema `pranchas.jsonld` + validador
- [ ] corpus.jsonld servido via R2

### Fase 1 — Manifesto + Atlas core (jun 28 – jul 15)
- [ ] Manifesto imersivo (`/`)
- [ ] Superfície de montagem (`/atlas`)
- [ ] Browser de espécimes
- [ ] Pranchas publicadas (`/prancha/:id`)
- [ ] PDF A0
- [ ] Navegação entre manifesto e atlas

### Fase 2 — Tese + Biblioteca (jul 16 – ago 15)
- [ ] Capítulos como meta-pranchas (`/tese`)
- [ ] Sumário como mapa topológico
- [ ] Zotero integrado (`/biblioteca`)
- [ ] Glossário de termos
- [ ] Links reversos (espécime → pranchas → capítulos)

### Fase 3 — Corpus + Comunidade (ago 16 – set 15)
- [ ] Browser completo do corpus (`/corpus`)
- [ ] Submissão de espécimes
- [ ] Comentários e remixes (`/comunidade`)
- [ ] Dashboard de moderação (interno)

### Fase 4 — Polimento (set 16 – out 30)
- [ ] Áudio ambiente (manifesto)
- [ ] Animações de transição entre superfícies
- [ ] Histórico de deriva do visitante
- [ ] Busca global
- [ ] Testes cross-browser, acessibilidade (WCAG AA)
- [ ] Deploy de produção em `iconocracia.com`

---

## 8. Referências

- Warburg, A. *Der Bilderatlas Mnemosyne* (1924–1929)
- Gemini design exploration, 24-jun-2026: `~/Downloads/iconocracia-design-system/Gemini 24 junho/`
  - Manifesto (editorial): `Iconocracia - Manifesto.dc.html`
  - Xilogravura companion: `ssdfdsfs/uploads/index.html`
  - Perplexity corpus browser: `ssdfdsfs/uploads/index (3).html`
  - Atlas woodcut mockups: `ssdfdsfs/uploads/iconocracy-woodcut-atlas.png`, `*-desktop.png`, `*-language.png`
  - Video imersivo: `Iconocracia - Video.dc.html`, `*.mp4`
  - Biblioteca de Prompts: `ICONOCRACIA — Biblioteca de Prompts/prompts_data.js`
  - Atlaslab corpus (398 items): `~/Research/apps/atlaslab/src/data/corpus.json`
- Corpus canônico (299 items): `~/Research/hub/iconocracy-corpus/corpus/corpus-data.json`
- Audio referência: Paris Paloma — "LABOUR (the cacophony)" (atmosfera industrial + vocal etéreo)
- Atlas v2 design doc (componente): `2026-06-24-atlas-v2-design.md`
- Site atual: `anavanzin.workers.dev` (companion) + `iconocracia-trajetoria.anavanzin.workers.dev` (trajetória)
- Design tokens xilogravura: `--paper: #eee4cf`, `--black: #090a0d`, `--gold: #9a783d`, `--seal: #9d3a27`, `--grain` SVG, `--ledger` gradients
