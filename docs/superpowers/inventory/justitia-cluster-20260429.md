# Justitia Cluster — Inventário do Vault (ICONOCRACY)

Data do survey: 2026-04-29
Escopo: todos os arquivos SCOUT-*.md em `vault/candidatos/` com `motivo_alegorico` contendo "Justice", "Justitia", "Justiça" ou "Gerechtigkeit"
Metodologia: leitura integral de cada ficha; classificação tripartida PROMOTE / DEFER / SKIP

---

## 1. Dimensão do cluster

| Métrica | Valor |
|---|---|
| Total de itens com motivo Justitia/Justice | **73** |
| Promovidos (com `records_item_id`) | **41** (56%) |
| Não promovidos (sem `records_item_id`) | **32** (44%) |

Dos 32 não promovidos, a distribuição é:

| Categoria | Quantidade |
|---|---|
| PROMOTE — endurecimento claro, encaixa na tese | **5** |
| DEFER — requer análise visual ou confirmação | **24** |
| SKIP — não se encaixa ou é duplicata | **3** |

---

## 2. Notas estruturadas por item (não promovidos)

### 2.1 — PROMOTE (5 itens)

#### SCOUT-301 — Lady Justice, Old Bailey (F.W. Pomeroy, 1906)
- **País:** UK | **Século:** 20th | **Suporte:** monumento (bronze dourado, 3,7 m) | **Regime:** NORMATIVO
- **Descrição:** Figura feminina de pé sobre a cúpula do tribunal. Espada na mão direita, balança na esquerda. Sem venda — o tribunal argumenta que a "forma donzela" garante imparcialidade. Vestes clássicas pesadas.
- **Endurecimento:** SIM, normativo avançado. Rigidez postural máxima (frontal, simétrica, estática). Dessexualização completa. Heraldição forte. Inscrição estatal máxima — corpo feminino é o coroamento do edifício. O Contrato Sexual Visual está explícito na justificativa institucional para a ausência da venda.
- **Veredito:** **PROMOVE.** Caso canônico de endurecimento NORMATIVO anglo-saxão.

#### SCOUT-302 — Justitia entronizada, Reichsgerichtsgebäude Leipzig (Otto Lessing, 1895)
- **País:** DE | **Século:** 19th | **Suporte:** monumento (pedra, frontão) | **Regime:** NORMATIVO
- **Descrição:** Justitia entronizada no centro do frontão do tribunal do Reich. Programa escultórico excepcional com DUAS funções: à esquerda como libertadora, à direita como punitiva.
- **Endurecimento:** SIM, máximo. Dualidade libertadora/punitiva = o Estado emprega dois corpos femininos para separar funções. Corpo enquadrado pelo frontão clássico.
- **Veredito:** **PROMOVE.** A duplicação do corpo feminino para segregar funções estatais é evidência direta do argumento da tese.

#### SCOUT-303 — A Justiça, STF Brasília (Alfredo Ceschiatti, 1961)
- **País:** BR | **Século:** 20th | **Suporte:** monumento (granito, 3,30 m) | **Regime:** NORMATIVO
- **Descrição:** Têmis sentada, vendada, espada no colo. SEM BALANÇA — ausência excepcional do atributo canônico. Influência concretista: volume compacto, formas simétricas.
- **Endurecimento:** SIM, por SUBTRAÇÃO (negativo). A remoção da balança produz uma Justitia que julga (espada) mas não pesa. Supressão do atributo narrativo central.
- **Veredito:** **PROMOVE.** O endurecimento por subtração é uma modalidade distinta que enriquece a tipologia da tese.

#### SCOUT-305 — Cariátides alegóricas, Palais de Justice Paris (Lequesne/Duc, 1868)
- **País:** FR | **Século:** 19th | **Suporte:** monumento (pedra) | **Regime:** NORMATIVO
- **Descrição:** Quatro cariátides: Prudência, Justiça, Inocência e Força. Corpos femininos sustentando literalmente a estrutura do tribunal.
- **Endurecimento:** SIM, via CARIÁTIDE — o terminus do processo: o corpo feminino se torna coluna arquitetônica. A mulher-coluna é a forma mais radical do Contrato Sexual Visual.
- **Veredito:** **PROMOVE.** A cariátide representa o grau máximo de endurecimento — fusão corpo-arquitetura.

#### SCOUT-406 — Alegorias do Palácio do Catete, Val d'Osne (1899–1910)
- **País:** BR | **Século:** 19th | **Suporte:** monumento (ferro e bronze) | **Regime:** FUNDACIONAL (com transição para NORMATIVO)
- **Descrição:** Sete esculturas femininas da fundição francesa Val d'Osne: República (centro), Justiça e Outono (ala esquerda), Agricultura e Primavera (ala direita), Inverno e Verão (fundos). No vestíbulo: "O Pudor" (nua) e "A Glória" (cornucópia).
- **Endurecimento:** SIM, **caso paradigmático.** Em 1910, todas as alegorias femininas do parapeito foram removidas e substituídas por águias heráldicas. Transição documentada: corpo feminino vivo → símbolo animal. Este é o arco completo do endurecimento em um único edifício — sede da presidência da República (1897–1960). A origem francesa das esculturas (Val d'Osne) conecta diretamente ao repertório marianista transatlântico.
- **Veredito:** **PROMOVE.** Evidência direta e documentada do processo de endurecimento no Brasil republicano. A substituição por águias em 1910 é o caso mais bem documentado do corpus.

---

### 2.2 — DEFER (24 itens)

A grande maioria dos itens não promovidos (24 de 32) são candidatos automáticos gerados por `hunt.py` via Europeana, Gallica ou Library of Congress. Todos compartilham estas características:

- **Confiança:** baixo a médio
- **Regime:** INDETERMINADO (18) ou NORMATIVO com classificação preliminar (6)
- **Endurecimento:** "pendente — sem acesso à imagem" ou classificação preliminar baseada apenas em metadados textuais
- **Tag universal:** `#verificar`

Agrupam-se em três categorias de deferimento:

**A. Hunt-candidates INDETERMINADOS (18 itens):** SCOUT-323, 324, 325, 326, 327, 328, 329, 338, 339, 340, 342, 346, 347, 348, 349, 355, 359, 365. Todos requerem acesso à imagem para classificação de regime e endurecimento. SCOUT-365 ("Justice to the Jew") é provavelmente um livro sem figura alegórica relevante — recomendação de SKIP na revisão visual.

**B. Hunt-candidates NORMATIVOS preliminares (6 itens):** SCOUT-344 (Chifflart, 1865), 350 (Grand Juge, s.d.), 353 (estampe, 15..-1584), 357 (Davent, 1547), 358 (Bosse, 1662), 360 (anônimo, 1791). Classificados como NORMATIVO com endurecimento esperado "MÉDIO a ALTO" baseado em metadados. SCOUT-344 é potencialmente relevante por tratar do trio Justice/Vengeance/Vérité — verificar se há paralelo com SCOUT-448 (já promovido, mesmo motivo).

**C. SCOUT-423 — 50 Mil Réis, Banco do Brazil (1890):** Caso distinto. Item FUNDACIONAL brasileiro com análise detalhada de endurecimento. A nota registra endurecimento "baixo a moderado" com indicadores mistos: baixa desincorporação, moderada rigidez, alta serialidade e inscrição estatal. A tríade Liberdade-Governo-Justiça em cédula fundacional tem alto valor como referência comparativa, mas o endurecimento baixo a coloca como contraponto, não como evidência direta da tese. Recomendação: DEFER para decisão da pesquisadora sobre inclusão como baseline FUNDACIONAL.

---

### 2.3 — SKIP (3 itens)

#### SCOUT-306 — Gerechtigkeitsbrunnen, Berna (Hans Gieng, 1543)
- **País:** CH | **Século:** 16th | **Suporte:** monumento (calcário policromado) | **Regime:** FUNDACIONAL
- **Descrição:** Primeira representação conhecida da Justitia vendada em escultura pública. Corpo em contraposto, policromia, narrativa máxima. Aos pés: Papa, Imperador, Sultão, Schultheiss.
- **Endurecimento:** NÃO — anti-endurecimento fundacional.
- **Veredito:** **SKIP.** Item de referência pré-corpus (anterior a 1800). Mantido no vault como contraste histórico, mas fora do escopo temporal da tese.

#### SCOUT-341 — N°5 Take up the sword of justice (Partridge, 1920)
- **País:** FR | **Século:** 20th | **Regime:** MILITAR | **Status:** duplicata
- **Descrição:** Duplicata de SCOUT-473 (já promovido com `records_item_id`). Ambos referem-se ao mesmo item.
- **Veredito:** **SKIP.** Duplicata — manter apenas o item promovido SCOUT-473.

#### SCOUT-365 — Justice to the Jew (Peters, 1900)
- **País:** US | **Século:** 19th | **Suporte:** indeterminado (livro)
- **Descrição:** Livro sobre contribuições judaicas para o mundo. "Justice" aparece como conceito no título, não como figura alegórica.
- **Endurecimento:** Não aplicável — não é uma imagem alegórica.
- **Veredito:** **SKIP.** Fora do escopo. Item textual, não iconográfico.

---

## 3. Análise agregada

### 3.1 Distribuição geográfica dos não promovidos

| País | Itens | % |
|---|---|---|
| FR (França) | 25 | 78% |
| BR (Brasil) | 3 | 9% |
| US (EUA) | 1 | 3% |
| UK (Reino Unido) | 1 | 3% |
| DE (Alemanha) | 1 | 3% |
| CH (Suíça) | 1 | 3% |

A esmagadora concentração francesa (78%) reflete o viés das fontes de hunt.py — Europeana e Gallica são predominantemente francófonas. Isso NÃO indica predominância real da Justitia na França, mas sim um artefato das campanhas de scout. O cluster BR (3 itens) é qualitativamente desproporcional: os três itens brasileiros (Ceschiatti, Catete, cédula de 1890) estão entre os achados mais relevantes da amostra.

### 3.2 Distribuição por regime dos não promovidos

| Regime | Itens |
|---|---|
| INDETERMINADO | 18 |
| NORMATIVO | 10 |
| FUNDACIONAL | 3 |
| MILITAR | 1 |

O alto número de INDETERMINADOS (56%) confirma que o pipeline hunt.py prioriza recall sobre precisão. Dos 10 NORMATIVOS, a maioria são classificações preliminares. Os 3 FUNDACIONAIS (SCOUT-306, 406, 423) incluem o item mais importante do lote (Catete) e o item de referência pré-1800 (Berna).

### 3.3 Distribuição por século dos não promovidos

| Século | Itens |
|---|---|
| Indeterminado | 18 |
| 19th | 4 |
| 16th | 4 |
| 20th | 3 |
| 18th | 2 |
| 17th | 1 |

A concentração no século 19 (4 itens) entre os datados é consistente com o período de consolidação dos Estados-nação e construção de tribunais monumentais — o locus clássico do endurecimento NORMATIVO.

### 3.4 Padrão de endurecimento

Entre os 32 não promovidos, o padrão de endurecimento se manifesta em três modalidades:

1. **Endurecimento NORMATIVO canônico** (SCOUT-301, 302): rigidez postural, dessexualização, heraldiçação, inscrição estatal no edifício do tribunal. Padrão mais frequente e mais bem documentado.

2. **Endurecimento por subtração** (SCOUT-303): remoção de atributo canônico (balança), produzindo um corpo que julga sem pesar. Modalidade específica do modernismo brasileiro.

3. **Endurecimento por substituição** (SCOUT-406): remoção completa do corpo feminino alegórico e substituição por símbolo animal heráldico (águia). Caso documentado e datado (1910). Evidência mais forte do corpus para o argumento central da tese.

A cariátide (SCOUT-305) representa um quarto tipo — o corpo feminino se torna literalmente estrutura arquitetônica, o grau máximo de fusão corpo-Estado.

### 3.5 Comparação promovidos vs. não promovidos

Entre os 41 itens já promovidos, encontram-se paralelos diretos com vários dos não promovidos:

- SCOUT-456 (promovido) ≈ SCOUT-301 (não promovido): ambos são a Lady Justice do Old Bailey. SCOUT-456 tem `records_item_id`; SCOUT-301 é aparentemente uma ficha alternativa ou duplicata parcial. Verificar consolidação.
- SCOUT-473 (promovido) ≈ SCOUT-341 (não promovido): duplicata confirmada.
- SCOUT-448 (promovido) ≈ SCOUT-344 (não promovido): ambos tratam de "La Justice, la Vengeance et la Vérité". SCOUT-448 é promovido, SCOUT-344 é hunt-candidate a verificar.

Isso sugere que aproximadamente 3 dos 32 não promovidos são duplicatas ou versões alternativas de itens já promovidos. Os 29 restantes são candidatos genuinamente novos — mas 24 deles requerem validação visual.

---

## 4. Recomendações

### 4.1 Ações imediatas

| Ação | Itens | Prioridade |
|---|---|---|
| Promover com `vault_sync.py push` | SCOUT-301, 302, 303, 305, 406 | Alta |
| Consolidar duplicatas | SCOUT-301↔456, SCOUT-341↔473 | Alta |
| Marcar como SKIP definitivo | SCOUT-306, 341, 365 | Média |
| Validar visualmente (gallica/iiif) | 24 hunt-candidates | Média |

### 4.2 Padrões para a tese

1. **O arco Catete (1899–1910)** é o achado isolado mais valioso: documenta em 11 anos e em um único edifício a transição completa corpo feminino → heráldica animal. Sugere-se um painel Zwischenraum dedicado.

2. **A Justitia sem balança de Ceschiatti (1961)** oferece uma variante teórica relevante: o endurecimento não é apenas adição de rigidez, mas também subtração de atributos. Enriquece a tipologia para além do modelo "muscular/marcial".

3. **A dualidade Leipzig (1895)** — libertadora × punitiva — demonstra que o Estado mobiliza múltiplos corpos femininos para segregar funções que um corpo masculino poderia acumular. A duplicação é em si um sintoma de endurecimento.

4. **O viés francês (78%)** deve ser explicitamente reconhecido como artefato metodológico na tese. A verdadeira distribuição geográfica da Justitia como Pathosformel é mais equilibrada, como evidenciado pelos itens BR, DE, UK, US e CH já presentes (promovidos e não promovidos).

### 4.3 Riscos

- A maioria dos hunt-candidates (24/32) nunca será promovida — são itens de baixa confiança. Não investir tempo excessivo neles.
- SCOUT-365 ("Justice to the Jew") e SCOUT-359 (mapa de Berry) provavelmente são falsos positivos do hunt.py. Confirmar e remover.
- A aparente duplicata SCOUT-301/SCOUT-456 precisa ser investigada: por que há duas fichas para o mesmo item? Erro de sincronização ou versões diferentes?

---

## 5. Síntese

O cluster Justitia no vault é substancial (73 itens) e bem distribuído entre promovidos (41) e não promovidos (32). Entre os não promovidos, 5 itens têm mérito claro para promoção imediata — todos com endurecimento detectado e analisado. Os 24 hunt-candidates pendentes representam o resíduo normal de campanhas automáticas de alta sensibilidade; sua triagem visual pode render 2–4 promoções adicionais. Os 3 SKIPs são itens corretamente identificados como fora do escopo.

O padrão de endurecimento é visível e documentável em três modalidades (normativo canônico, subtrativo, substitutivo), com concentração nos séculos 19–20 e nos regimes NORMATIVO e FUNDACIONAL. A Justitia se confirma como uma das Pathosformeln mais férteis para o argumento central da tese.
