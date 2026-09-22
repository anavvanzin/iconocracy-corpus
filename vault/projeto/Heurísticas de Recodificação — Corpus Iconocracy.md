# Heurísticas de Recodificação — Corpus Iconocracy
**Status:** v1.0 · 2026-07-17  
**Autora:** Ana Vitória Vanzin Mendes · PPGD/UFSC  
**Aplica-se a:** 159 registros de baixa confiança (vault-import / hermes-auto / migration / batch-tentative)  
**Pipeline:** `records.jsonl` → análise visual → `purificacao.*` atualizado → commit

---

## Contexto de uso

Estes registros têm scores de purificação não confiáveis porque foram produzidos sem análise visual direta:

| Agente | N | Problema específico |
|--------|---|---------------------|
| `vault-import` | 86 | Score = 0.0 uniform; regime inferido sem ver a imagem |
| `hermes-auto` | 43 | Score = 1.4 em **87% dos casos** — valor de fallback do pipeline |
| `migration` | 17 | Score herdado de schema anterior, frequentemente 0.0; alguns são "ausência alegórica" legítima |
| `batch-tentative-*` | 13 | Batch provisório; regime e score marcados como tentative na origem |

**Hermes-auto é o caso mais urgente:** o score 1.4 não é análise — é o fallback que o pipeline usa quando não consegue resolver um caso. Todos os 43 precisam de recodificação completa.

---

## Como usar este documento

Para cada registro na planilha de auditoria:

1. Identificar a **fonte** pelo campo `url` (Tabela 1 abaixo)
2. Identificar o **tipo documental** pelo título e motivos (Tabela 2)
3. Extrair os metadados disponíveis seguindo as **heurísticas por fonte** (Seção 2)
4. Aplicar os **ranges de referência por tipo + alegoria** para estimar os indicadores (Seção 3)
5. Preencher os 10 indicadores (0–3) + `familia_alegorica` + `subtipo`
6. Atualizar `review_status` para `RECODIFICADO` e commitar

---

## 1. Mapeamento rápido: fonte × tipo documental

### Tabela 1 — Distribuição dos 159 registros por fonte

| Fonte | N | Tipos predominantes | Confiança de metadados |
|-------|---|---------------------|------------------------|
| Numista | 41 | Moeda/cédula (100%) | Alta: denominação, país, ano, obverse/reverse text — **API key-gated, mas HTML parseable** |
| Gallica/BnF | 28 | Estampa/gravura (82%), cartaz (11%) | Média: ARK persistente, dc:date (impreciso), dc:description (texto livre) |
| Victoria & Albert | 18 | Medalha, estampa, cerâmica | Alta: `depicts` field estruturado, `_primaryMaker__name`, `materialsAndTechniques` |
| Library of Congress | 12 | Cartaz, fotografia, print | Média: título, data, médio — criador frequentemente ausente no JSON |
| BALAT/KIKiRPA | 9 | Escultura, pintura, objeto | Média: título + tipologia; sem campo iconográfico estruturado |
| HAUM / museum-digital | 7 | Gravura (Virtuelles Kupferstichkabinett) | Alta via museum-digital API JSON; tags iconográficas disponíveis |
| Hemeroteca BN Brasil | 6 | Periódico ilustrado, fotografia | Baixa (Hemeroteca core); usar Brasiliana Iconográfica quando disponível |
| Colnect | 5 | Selo, moeda | Média: themes/topics hierárquico; sem API pública |
| Vault interno / sem URL | 21 | Variado | Baixa: depende inteiramente de análise visual direta |
| Outros (V&A, etc.) | 12 | Variado | — |

### Tabela 2 — Sinais de tipo documental no título

| Palavras-chave no título | Tipo documental | Suporte `medium` |
|--------------------------|-----------------|-----------------|
| franc, penny, réis, cruzeiro, assignat, pfennig, florin, coin, moeda | Moeda/cédula | `moeda` ou `papel-moeda` |
| timbre, stamp, sello, selo, briefmarke | Selo | `selo` |
| affiche, poster, cartaz, propaganda | Cartaz | `cartaz` |
| gravure, estampe, print, lithograph, engraving, gravura, burin | Estampa/gravura | `estampa` |
| peinture, painting, oil on, pintura, quadro | Pintura | `pintura` |
| sculpture, monument, statue, escultura, buste | Monumento/escultura | `escultura` |
| médaille, medal, medalha, plaquette | Medalha | `medalha` |
| frontispice, frontispiece, frontispício, title page | Frontispício | `frontispicio` |

---

## 2. Heurísticas por fonte arquivística

### 2.1 Numista — Moedas e cédulas (41 registros)

**URL pattern:** `numista.com/catalogue/piecesNNNN.html`

**Metadados disponíveis diretamente na página HTML:**

| Campo Iconocracy | Fonte em Numista | Confiança |
|------------------|------------------|-----------|
| `title` | Nome do tipo (ex: "5 Francs — Cérès, 2e République") | Alta |
| `country` / `place_hint` | "Issuer" (país emissor) | Alta |
| `year` | "Years of issue" (pode ser intervalo: 1849–1851) | Alta |
| `creator` / designer | "Obverse designer" / "Reverse designer" | Média (community-contributed) |
| `institution` | Mint (casa da moeda) | Alta quando presente |
| Iconografia | **Campo "Obverse" e "Reverse"** (texto livre descrevendo dispositivos e legendas) | Alta — este é o campo iconográfico principal |
| `medium` | "Composition" (metal, e.g. Silver .900) + "Type" (Circulation coin / Commemorative) | Alta |

**Protocolo de extração:**
1. Abrir URL da página Numista
2. Ler "Obverse" text → identifica a alegoria (ex: "Bust of Cérès left, date below")
3. Ler "Reverse" text → identifica atributos, legenda, denominação
4. "Years of issue" → `year` (usar o primeiro ano do intervalo para casos de série)
5. "Obverse designer" → `creator`
6. Cruzar com referência Krause (KM#) quando disponível na página para confirmação de data/metal

**Red flags:** designer fields são user-contributed — cross-checar com catálogo Krause impresso para coins raros. Anos de intervalos longos (ex: 1800–1850) indicam série; usar data de emissão do espécime específico se disponível.

**Familia alegórica típica em Numista (corpus Iconocracy):**
- Cérès → `Virtudes/Ceres-Minerva`
- Marianne / "effigie de la République" → `Nacional/Republica`
- Britannia → `Nacional/Britannia`
- "Efígie da República" (BR) → `Nacional/Republica`
- Germania seated → `Nacional/Germania`

---

### 2.2 Gallica/BnF — Estampas e gravuras (28 registros)

**URL pattern:** `gallica.bnf.fr/ark:/12148/[identifier]`

**ARK decode:**
- `bpt6k` / `btv1b` = recurso digitalizado Gallica
- `/f19` = página 19 de um documento multipágina
- `.highres` / `.thumbnail` = variante de imagem

**Metadados disponíveis:**

| Campo Iconocracy | Fonte em Gallica | Como acessar |
|------------------|------------------|--------------|
| `title` | `dc:title` | HTML "En savoir plus" tab → Titre |
| `creator` | `dc:creator` | HTML → Auteur / Graveur / Dessinateur |
| `date` | `dc:date` | Frequentemente impreciso (ex: "18.." ou "1840-1860") |
| `institution` | `dc:source` / `dc:publisher` | Nome do fundo/coleção |
| Iconografia | `dc:subject` (cabeçalhos Rameau) + `dc:description` | HTML → Sujet / Description |
| ARK persistente | URL da página | Usar como `external_identifiers.ark` |
| IIIF manifest | `gallica.bnf.fr/iiif/ark:/12148/[id]/manifest.json` | Para acesso à imagem em alta resolução |

**OAI-PMH (para metadados mais ricos):**
```
http://oai.bnf.fr/oai2/OAIHandler?verb=GetRecord
  &identifier=oai:bnf.fr:gallica/ark:/12148/[ARK]
  &metadataPrefix=oai_dc
```

**Protocolo de extração:**
1. Clicar em "En savoir plus" na página Gallica para ver o notice bibliográfico completo
2. `dc:subject` frequentemente contém os cabeçalhos iconográficos em vocabulário Rameau — ex: "Allégories -- France -- 19e siècle", "Justice (personnification)"
3. Se `dc:date` é vago (ex: "1800-1899"), procurar informação mais precisa no `dc:description` ou no catalogue BnF associado (`catalogue.bnf.fr/ark:/12148/cb[id]`)
4. Para gravuras com artista, Gallica frequentemente distingue desenhista (dessinateur) e gravador (graveur) — ambos são relevantes para `creator`

**Red flag:** a BnF cataloga moedas (`monnaie`) separadamente em acervo físico, mas as estampas de moedas aparecem junto com gravuras numismáticas — verificar se o item é a moeda em si ou uma representação dela.

---

### 2.3 Victoria & Albert Museum (18 registros)

**URL pattern:** `collections.vam.ac.uk/item/O[number]/`

**API estruturada disponível:**
```
GET https://api.vam.ac.uk/v2/museumobject/O[number]
```

**Campos especialmente úteis para iconografia:**

| Campo Iconocracy | Campo V&A | Notas |
|------------------|-----------|-------|
| Alegoria identificada | `depicts` | Campo específico para sujeito representado — ex: `[{"name": "Justice", "role": "depicted"}]` |
| `creator` | `_primaryMaker__name` | Maker principal (artista, gravador, fundição) |
| `date` | `_primaryDate` | String de display; `productionDates[0].date.earliest/latest` para range |
| `medium` | `materialsAndTechniques` (string) ou `materials[]` + `techniques[]` | Arrays controlados |
| `institution` | `_currentLocation__displayName` | Galeria atual no V&A |
| Dimensões | `dimensions[]` — `value` + `unit` + `dimension` (height/width/depth/diameter) | Quando disponível |

**Protocolo de extração:**
1. Acessar a API diretamente: substituir `/item/O` por `/v2/museumobject/O` (acrescentar número)
2. Campo `depicts` → `familia_alegorica` + `subtipo` + `atributos_iconograficos`
3. `physicalDescription` (string livre) → leitura visual adicional
4. `materials` + `techniques` → `medium_norm` usando a tabela de mapeamento do codebook

**Exemplo de `depicts` para medalha:**
```json
"depicts": [{"name": "Britannia", "role": "depicted"}, {"name": "George III", "role": "depicted"}]
```
→ `familia_alegorica: Nacional`, `subtipo: Britannia`

---

### 2.4 Library of Congress (12 registros)

**URL pattern:** `loc.gov/item/[id]/` ou `loc.gov/pictures/item/[id]/`

**Atenção:** o endpoint `/pictures/` **NÃO suporta** `?fo=json`. Para itens em `/pictures/`, usar o HTML + link MARC.

**Para itens em `/item/`:**
```
https://www.loc.gov/item/[id]/?fo=json
```
Retorna objeto com `item.title`, `item.date`, `item.medium`, `item.notes`, `item.contributors`.

**Protocolo de extração:**
1. Verificar se URL é `/pictures/` ou `/item/` — estratégia diferente para cada
2. Para `/pictures/`: ler HTML da página → tabela de metadados (Title, Creator, Date, Medium, Notes)
3. Para `/item/`: append `?fo=json` → JSON com campos estruturados
4. `item.notes` (array) frequentemente contém legenda da imagem ou descrição iconográfica
5. **Creator ausente em JSON?** → verificar campo MARC 100/700 via link "MARC/MODS" na página
6. Dimensões em LOC: estão dentro do campo `medium` como texto livre (ex: "lithograph; 56 x 42 cm") — parsear com regex `(\d+\.?\d*)\s*[x×]\s*(\d+\.?\d*)\s*(cm|mm|in)`

**Red flag para cartazes (posters):** LOC tem coleção massiva de cartazes da WWI e WWII com alegorias Columbia e Liberdade — estes muitas vezes têm `creator` ausente no JSON porque eram anônimos. Usar `notes` para identificar editor/impressora como proxy.

---

### 2.5 BALAT/KIKiRPA — Patrimônio belga (9 registros)

**URL pattern:** `balat.kikirpa.be/[lang]/object/[id]/` ou `/photo/[id]/`

**Persistent ID:** Handle System `hdl:20.500.14037/object.[id]`

**Metadados disponíveis no HTML:**

| Campo Iconocracy | Campo BALAT | Notas |
|------------------|-------------|-------|
| `title` | Title (campo principal) — frequentemente nome do sujeito representado | Alta |
| Tipo objeto | "Object name" / tipologia | Ex: "statue humaine", "tableau", "médaille" |
| `creator` | Maker/creator | Pode ser ausente para objetos medievais/religiosos |
| `date` | Creation date range | Frequentemente range amplo |
| `institution` | Institution (igreja, museu que detém o objeto) | Alta |
| `medium` | Materials | Lista de materiais em francês/neerlandês |
| Identificador ARK | Handle System URI | Usar como `external_identifiers.handle` |

**Sem campo iconográfico estruturado visível:** a iconografia deve ser inferida do título (ex: "Madonna et l'Enfant" → `familia_alegorica: Virtudes`) + busca no vocabulário iconográfico KIK-IRPA via filtros de busca no site.

**Protocolo de extração:**
1. Verificar se é `/object/` ou `/photo/` — preferir `/object/` para descrição completa
2. Título frequentemente já nomeia a alegoria (ex: "Justice tenant une balance")
3. Usar "Object name" para confirmar suporte (`medium_norm`)
4. Para objetos sem data precisa: BALAT frequentemente indica "18e–19e s." — usar ponto médio ou deixar range no campo `period`
5. Se disponível, a Europeana tem registros BALAT com metadados enriquecidos: buscar pelo handle em `europeana.eu`

---

### 2.6 HAUM / museum-digital — Gravuras (7 registros)

**Rota preferida:** museum-digital (não kk.haum-bs.de)

```
https://nds.museum-digital.de/object/[id]
→ https://nds.museum-digital.de/json/object/[id]  (JSON API)
→ https://nds.museum-digital.de/lido/object/[id]  (LIDO XML)
```

**Para Virtuelles Kupferstichkabinett** (gravuras Early Modern):
```
https://www.virtuelles-kupferstichkabinett.de/[id]
```
Contém classificação iconográfica via CDWA-Lite + tags de subject.

**Tags iconográficos em museum-digital:** o campo `tags` contém termos controlados — ex: `["Allegorie", "Gerechtigkeit", "Frau", "Waage", "Schwert"]` — que mapeiam diretamente para atributos do codebook.

---

### 2.7 Hemeroteca Digital BN Brasil / Brasiliana Iconográfica (6 registros)

**AVISO:** Preferir sempre **Brasiliana Iconográfica** (`brasilianaiconografica.art.br`) sobre Hemeroteca core para objetos iconográficos.

| Portal | `dc:technique` | `dc:format.extent` (dimensões) | Adequado para corpus? |
|--------|----------------|--------------------------------|-----------------------|
| Hemeroteca Digital (`hemerotecadigital.bn.br`) | Ausente | Ausente | Não (otimizado para OCR/periódico) |
| Brasiliana Iconográfica (`brasilianaiconografica.art.br`) | Presente ("Técnica utilizada") | Presente ("Dimensões") | **Sim** |
| Acervo Digital BNDigital | Variável | Variável | Sim quando objeto visual |

**Protocolo de extração:**
1. A partir da URL Hemeroteca → buscar o mesmo item em Brasiliana Iconográfica (mesmo acervo BN)
2. Campos relevantes em Brasiliana Iconográfica: Pintor, Técnica utilizada, Dimensões, Tipo de obra, Assunto
3. `Assunto` (controlado) → `familia_alegorica` + motivos
4. Para periódicos ilustrados: o item é uma página, não um objeto — verificar se a alegoria é um artigo iconográfico destacável ou apenas contexto editorial. Se for apenas contexto → `review_status: COMPARADOR`

---

### 2.8 Colnect — Selos e moedas (5 registros)

**URL pattern:** `colnect.com/[lang]/stamps/stamp/[id]-[slug]` ou `/coins/coin/[id]-[slug]`

**Robots.txt bloqueia fetch automático** — extrair manualmente.

**Campos úteis na página HTML (leitura manual):**
- "Themes" (hierárquico) → `familia_alegorica` + motivos (ex: "Royalty | Queens | Victoria")
- "Designer(s)" → `creator`
- "Printed/Minted by" → impressora/casa da moeda
- "Issued on" → `date` / `year` (geralmente preciso para selos)
- Catalog codes (Michel, Scott) → `external_identifiers`

**Diferencial Colnect vs Numista:** para **selos**, Colnect tem subjects/themes mais detalhados; para **moedas**, Numista tem obverse/reverse text mais preciso. Usar os dois em cruzamento quando disponível.

---

### 2.9 Vault interno / sem URL (21 registros)

Estes registros não têm URL de acervo externo. Estratégia:

1. Verificar `batch_id` no registro → identificar a campanha de busca de origem (ex: `SCOUT-BR-001`) no arquivo `vault/candidatos/`
2. Consultar a nota Obsidian correspondente no vault (pasta `corpus/` do vault Iconocracy)
3. Se a nota tem imagem anexada (`[[imagem.jpg]]`): **análise visual direta** — este é o caso mais simples, basta abrir a nota e codificar
4. Se não tem imagem: buscar a imagem pelo título + país + data usando Gallica, BnF, Europeana como ponto de partida
5. Se imagem não localizável após 10 min de busca: `review_status: EXCLUIR` com nota "imagem não localizável"

---

## 3. Ranges de referência por tipo documental e família alegórica

Baseados nos **169 registros de alta confiança** (iconocode-opus, iconocode-opus-4.6-image, ana manual). Usar como expectativa de faixa — desvios significativos indicam ou um caso incomum (justificar em `review_notes`) ou erro de codificação.

### 3.1 Por tipo documental

| Tipo | ind_desincorp | ind_rigidez | ind_dessexual | ind_uniform | ind_heraldiz | ind_enquadram | ind_apagam | ind_monocrm | ind_serialid | ind_inscricao | Score típico |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Moeda/cédula** | 2–3 | 2–3 | 2–3 | 2–3 | 3 | 2–3 | 2 | 3 | 3 | 3 | 1.6–2.5 |
| **Selo** | 2–3 | 2 | 2–3 | 2 | 2–3 | 2–3 | 2 | 2–3 | 3 | 2–3 | 1.4–2.2 |
| **Cartaz/poster** | 1–2 | 1–2 | 1–2 | 1–2 | 1 | 1–2 | 1–2 | 1–2 | 1 | 1–2 | 0.6–1.4 |
| **Estampa/gravura** | 1–2 | 1–2 | 1–2 | 1–2 | 1–2 | 1–2 | 1 | 2 | 1 | 1–2 | 0.7–1.5 |
| **Pintura** | 0–1 | 0–1 | 0–1 | 0–1 | 0–1 | 0–1 | 0–1 | 0–1 | 0–1 | 0–1 | 0.2–0.8 |
| **Medalha** | 2–3 | 2–3 | 2–3 | 2 | 2–3 | 2 | 1–2 | 2–3 | 2 | 2–3 | 1.3–2.1 |
| **Monumento/escultura** | 1–2 | 2–3 | 1–2 | 1–2 | 1–2 | 2–3 | 1 | 1–2 | 1 | 2–3 | 0.8–1.8 |
| **Frontispício** | 1–2 | 1–2 | 1–2 | 1–2 | 1–2 | 2 | 1–2 | 1–2 | 1 | 2 | 0.8–1.5 |

**Indicador mais discriminante por tipo:**
- Moeda/cédula: `ind_serialidade` e `ind_heraldizacao` são quase sempre 3
- Pintura: todos os indicadores tendem a 0–1 (baixo endurecimento esperado)
- Cartaz: `ind_serialidade` é 1 (não é item reproduzido industrialmente no mesmo grau que moeda)

### 3.2 Por família alegórica

| Família | Indicadores mais altos | Indicadores mais baixos | Score mediano ref. |
|---------|------------------------|-------------------------|--------------------|
| **Justitia** (Venda, Balança, Espada) | `heraldizacao` (3), `inscricao_estatal` (3) | `apagamento_narrativo` (1–2) | 1.2 |
| **Libertas/Marianne** (Barrete frígio, Torch) | `inscricao_estatal` (3), `serialidade` (3) | `rigidez_postural` (1–2) | 1.4 |
| **República (BR)** (Estrela, Ramos) | `heraldizacao` (3), `serialidade` (3), `monocromatizacao` (3) | `dessexualizacao` (1–2) | 1.8 |
| **Britannia** (Tridente, Escudo, Elmo) | `rigidez_postural` (3), `heraldizacao` (3), `inscricao_estatal` (3) | `dessexualizacao` (2) | 2.0 |
| **Columbia** (Toga, Estrelas) | `inscricao_estatal` (3), `heraldizacao` (2–3) | `serialidade` (1–2) | 1.5 |
| **Cérès/Minerva** (Espiga, Elmo, Oliva) | `heraldizacao` (2–3), `uniformizacao_facial` (2) | `apagamento_narrativo` (1) | 1.3 |
| **Germania** | `rigidez_postural` (3), `heraldizacao` (3) | `apagamento_narrativo` (1–2) | 1.7 |
| **Virtudes (genéricas)** | `heraldizacao` (2–3) | `serialidade` (1), `inscricao_estatal` (1–2) | 0.9 |
| **Continentes** | `heraldizacao` (2), `uniformizacao_facial` (1–2) | `serialidade` (1), `monocromatizacao` (1) | 0.8 |

---

## 4. Heurísticas de decisão rápida (fluxograma)

```
┌─ Abrir registro na planilha ─────────────────────────────────────┐
│                                                                    │
│ 1. TEM URL?                                                        │
│    └─ NÃO → Buscar via título+país em Gallica/Europeana/BnF      │
│           └─ Não localizado em 10min → EXCLUIR                   │
│    └─ SIM → continuar                                             │
│                                                                    │
│ 2. IDENTIFICAR FONTE (ver Tabela 1)                               │
│    └─ Numista → ler Obverse/Reverse text (§2.1)                  │
│    └─ Gallica → ler dc:subject + Rameau (§2.2)                   │
│    └─ V&A → consultar campo `depicts` via API (§2.3)             │
│    └─ LOC → ler `item.notes` + MARC (§2.4)                       │
│    └─ BALAT → título + tipologia (§2.5)                          │
│    └─ museum-digital → JSON API + tags (§2.6)                    │
│    └─ BN Brasil → redirecionar para Brasiliana Iconográfica (§2.7)│
│    └─ Vault interno → nota Obsidian + imagem (§2.9)              │
│                                                                    │
│ 3. IDENTIFICAR ALEGORIA                                            │
│    └─ Justitia → buscar: venda, balança, espada                  │
│    └─ Libertas/Marianne → barrete frígio, tocha, correntes rotas │
│    └─ República (BR) → ramos, estrelas, "efígie"                 │
│    └─ Britannia → tridente, escudo oval, elmo com cimeira        │
│    └─ Columbia → toga, estrelas, livro/lei                        │
│    └─ Cérès → espiga de trigo, foice, elmo                       │
│    └─ NÃO IDENTIFICADA → `familia_alegorica: Outra` + notas      │
│                                                                    │
│ 4. A IMAGEM EXISTE E É ACESSÍVEL?                                 │
│    └─ SIM → análise visual completa (3 níveis Panofsky)          │
│    └─ NÃO → pode usar metadados textuais do acervo como proxy    │
│           (preencher indicadores com faixa mediana do tipo)       │
│           + marcar `notes`: "sem acesso à imagem — estimativa"   │
│                                                                    │
│ 5. ESCOPO                                                          │
│    └─ Material europeu/comparador → COMPARADOR                    │
│    └─ Fora do recorte 1800–2000 (ex: séc. XVI moeda) → COMPARADOR│
│    └─ Não é dispositivo estatal-jurídico → COMPARADOR             │
│    └─ Duplicata de outro registro → EXCLUIR                       │
│    └─ Ausência alegórica confirmada → EXCLUIR ou COMPARADOR       │
└────────────────────────────────────────────────────────────────────┘
```

---

## 5. Mapeamento de atributos visuais → indicadores

### Sinais visuais de alto endurecimento (indicador ≥ 2)

| O que se vê | Indicador correspondente | Score sugerido |
|-------------|--------------------------|---------------|
| Figura sentada ou estática em frontalidade | `ind_rigidez_postural` | 2–3 |
| Figura desprovida de roupas fluidas / toga rígida, armadura | `ind_rigidez_postural` | 2–3 |
| Rosto sem expressão, idealizados, olhos inexpressivos | `ind_uniformizacao_facial` | 2–3 |
| Seios cobertos, ausência de curvas, forma angular | `ind_dessexualizacao` | 2–3 |
| Figura integrada a brasão, escudo, ornamentos heráldicos | `ind_heraldizacao` | 3 |
| Figura encastrada em moldura arquitetônica, colunas, arco | `ind_enquadramento_arquitetonico` | 2–3 |
| Figura não interage com narrativa / sem personagens secundários | `ind_apagamento_narrativo` | 2–3 |
| Obra inteiramente em metal gravado / monocromia impressa | `ind_monocromatizacao` | 2–3 |
| Mesma imagem em múltiplas emissões, série numismática | `ind_serialidade` | 3 |
| Inscrição estatal na obra: REPÚBLICA, BRASIL, nome do emissor | `ind_inscricao_estatal` | 3 |
| Figura sem corpo / apenas busto | `ind_desincorporacao` | 2–3 |
| Corpo parcialmente visível, truncado na cintura | `ind_desincorporacao` | 1–2 |
| Corpo inteiro, poses dinâmicas, figura em movimento | `ind_desincorporacao` | 0–1 |

### Sinais de baixo endurecimento (indicador 0–1)

| O que se vê | Indicador | Score sugerido |
|-------------|-----------|----------------|
| Figura em movimento dramático / pose diagonal | `ind_rigidez_postural` | 0–1 |
| Rosto com expressão individual, olhar direcionado | `ind_uniformizacao_facial` | 0–1 |
| Pele exposta, roupas fluidas, sensualidade intencional | `ind_dessexualizacao` | 0 |
| Figura interage com personagens secundários, cena narrativa | `ind_apagamento_narrativo` | 0–1 |
| Cores e pigmentos variados, policromia | `ind_monocromatizacao` | 0 |
| Obra única, sem série conhecida | `ind_serialidade` | 0–1 |

---

## 6. Casos especiais dos agentes de baixa confiança

### Migration (17 registros) — protocolo específico

Os registros `migration` herdaram scores de uma versão anterior do schema. Dois subtipos:

**Tipo A — "Ausência alegórica"** (~6 registros com motif contendo "ausencia"):
- Verificar se o item realmente não contém alegoria feminina
- Se confirmado: `in_scope: false` + `review_status: EXCLUIR` ou `COMPARADOR`
- Se contém alegoria mas não foi codificada: tratar como Tipo B

**Tipo B — Score zero com alegoria presente** (~11 registros):
- Score 0.0 é herança de campo vazio, não análise real
- Tratar como `vault-import`: recodificação completa necessária
- Não usar o score 0.0 como ponto de partida — iniciar do zero

### Hermes-auto (43 registros) — protocolo específico

**Score 1.4 = fallback, não análise.** Nunca usar como base.

O que o hermes-auto tipicamente preserva (e pode ser reutilizado):
- `regime_iconocratico` (inferido de texto, geralmente correto para casos óbvios)
- `familia_alegorica` (quando presente — verificar se plausível)
- `referencia_genealogica` (frequentemente bem pesquisado)

O que deve ser descartado e refeito do zero:
- Todos os 10 indicadores individuais (hermes preenchia com valores uniformes)
- `purificacao_composto` = 1.4 (fallback)
- `notas` geradas automaticamente (revisar antes de manter)

### Batch-tentative (13 registros) — protocolo específico

Estes registros foram gerados em batch mas **marcados como provisórios** desde a origem — indicam que o agente tinha baixa confiança ao gerar. Abordagem:

- Verificar `audit_flags` — geralmente contém a razão do flag
- Score e indicadores podem ser parcialmente corretos — comparar com faixa esperada (Seção 3)
- Se score dentro da faixa esperada para o tipo: `review_status: CONFIRMADO` após verificação visual rápida
- Se score fora da faixa esperada: recodificação completa

---

## 7. Campos obrigatórios para fechar recodificação

Um registro pode ser marcado `RECODIFICADO` apenas quando todos estes campos estão preenchidos:

| Campo | Onde | Verificação |
|-------|------|-------------|
| Os 10 indicadores ordinais | `purificacao.{ind}` | Todos ≠ null |
| `purificacao_composto` | `purificacao.purificacao_composto` | Recalculado = média dos 10 |
| `regime_iconocratico` | `purificacao.regime_iconocratico` | fundacional/normativo/militar/contra-alegoria |
| `familia_alegorica` | `purificacao.familia_alegorica` | Controlado (ver codebook-v2-alegorias.md) |
| `subtipo` | `purificacao.subtipo` | Controlado (ver codebook-v2-alegorias.md) |
| `coded_by` | `purificacao.coded_by` | Atualizar para `ana` ou `iconocode-opus-manual` |
| `coded_at` | `purificacao.coded_at` | Data ISO da recodificação |
| `pre_iconographic[].motif` | `iconocode.pre_iconographic` | Lista de motivos observados |
| `in_scope` | `iconocode.validation.in_scope` | true/false |
| `review_notes` | Planilha | Observações sobre o processo |

**Recalcular `purificacao_composto`:**
```python
composto = sum([
    desincorporacao, rigidez_postural, dessexualizacao, uniformizacao_facial,
    heraldizacao, enquadramento_arquitetonico, apagamento_narrativo,
    monocromatizacao, serialidade, inscricao_estatal
]) / 10
```

---

## 8. Referências cruzadas

- Codebook canônico: `schema/codebook-v2.3.0.md` (local) / `docs/methodology/codebook-v2-alegorias.md`
- Schema JSON: `schemas/codebook-v2.1.0.schema.json`
- Taxonomia de metadados: `master-iconographic-metadata-taxonomy.md` (local)
- Planilha de auditoria: [Google Sheets](https://docs.google.com/spreadsheets/d/1r5Z5c5GdTUGnanz5rlvfSWRjqO-Xv9hxKO9BWaV3OvU/edit)
- Script de export/atualização: `tools/scripts/audit_recodification.py`
- Pipeline de recodificação: `tools/scripts/code_purification.py --item ITEM_ID`

---

*Gerado em 2026-07-17 a partir de análise de 328 records.jsonl × padrões de 8 acervos digitais × baseline de 169 registros alta confiança.*
