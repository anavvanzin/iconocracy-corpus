# Lacunas de Aquisição Iconográfica — 2026-04-25

> Conforme issue #42 (GitHub). Gaps identificados no Health Check semanal.
> Prioridade: **ALTA** para arquitetura forense; **MÉDIA** para non-schema supports.

---

## Lacuna 1 (CRÍTICA) — Arquitetura Forense = 0 itens

### Problema

A tese estuda alegoria feminina em dispositivos jurídico-estatais. Tribunais, palácios de justiça e fachadas forenses são o dispositivo arquitetônico central onde a iconocracia se materializa como espaço público. O corpus atual tem **zero** itens de arquitetura forense — o que é uma lacuna estrutural.

### Categoria de busca

**Suporte:** `arquitetura forense` (novo tipo de suporte a adicionar ao schema)

**Definição operacional:** Qualquer edificação cujo programa arquitetônico inclua função jurisdicional e que possua decoração escultórica, relief ou programa iconográfico no exterior ou interior visível ao público. Inclui:
- Fachadas de tribunais com frontões, frisos, estátuas
- Pátios internos com programas alegóricos
- Vestíbulos e salões de audiências com decoração mural

**Não inclui:** mobiliário forense, utensílios de courtroom.

### Candidatos de aquisição (prioridade para BR)

| Local | Descrição | Período | Allegoria feminina? |
|-------|-----------|---------|-------------------|
| Palácio da Justiça — Rio de Janeiro | Fachada com estátuas de Justitia etc. | 1920 | Sim (identificar) |
| Palácio da Justiça — São Paulo | Esculturas externas, vestíbulo | 1934 | Sim |
| Supremo Tribunal Federal — Brasília | Programa escultórico | 1960 | Provavelmente não (modernista) |
| Tribunal de Justiça de Minas Gerais — Belo Horizonte | Fachada neoclássica | 1911 | Identificar |
| Tribunal de Justiça de Pernambuco — Recife | Fachada | séc. 19 | Identificar |
| Palácio da Justiça — Porto Alegre | Fachada | 1934 | Identificar |

**Comparadores (6 países):**
- FR: Palais de Justice (Paris) — Grand Hall com estátuas
- UK: Supreme Court (London) — fachada pós-2009, mas Old Bailey tem programas escultóricos
- DE: Bundesgerichtshof (Karlsruhe) — fachada historicista
- US: State supreme court buildings (Washington DC federal, state capitols)
- BE: Palais de Justice (Bruxelas) — fachada monumental
- BR: (acima)

### Critérios de aceitação

- [ ] Fotografia da fachada/outros com resolução mínima 300 dpi ou acesso a archivo digital
- [ ] Identificação de figura feminina(s) alegórica(s)
- [ ] Metadados: arquiteto, data de construção, local, procedência
- [ ] Citação ABNT NBR 6023:2025 para a fonte
- [ ] Classificação no `corpus/corpus-data.json` como `support = "arquitetura forense"`
- [ ] Avaliação de impacto na publicação da tese: qual a diferença que faz?

### Ações imediatas

1. Buscar em acervos digitais: BNDigital, Arquivo Nacional, IPHAN
2. Buscar em Europeana (European cultural heritage portal)
3. Contatar IPHAN sobre bens tombados com programa iconográfico forense
4. Contatar museus da justiça: Museu da Justiça do Rio de Janeiro, Museu do Tribunal de Justiça de SP

---

## Lacuna 2 (ALTA) — Suportes não previstos no schema

### Problema

O schema de `corpus-data.json` parece prever apenas suportes canônicos (moeda, selo, cartaz, estampa/gravura, monumento/escultura, papel-moeda). Itens com supports "pintura", "fotografia", "texto" e "cerâmica" estão no corpus mas podem não estar previstos na normalização.

**Distribuição atual:**
| Support | Quantidade |
|---------|-----------|
| pintura | 12 |
| fotografia | 9 |
| texto | 2 |
| cerâmica | 1 |

### Análise

- **Pintura (12):** Inclui pinturas a óleo, têmpera — legítimo suporte iconográfico. Verificar se alguma é pintura de tribunal ou programa escultórico.
- **Fotografia (9):** Inclui fotografias de tribunais, rituais forenses, etc. Verificar se são registos de dispositivos estético-jurídicos ou documentação complementar.
- **Texto (2):** Possivelmente paratextos normativos (preâmbulos de leis, ementas) com alegoria.
- **Cerâmica (1):** Possivelmente revestimento de edifício público com programa iconográfico.

### Ações

- [ ] Verificar se cada item "pintura", "fotografia", "texto", "cerâmica" é alegoria feminina de dispositivo jurídico (se não, marcar `in_scope: false`)
- [ ] Adicionar `support` values ao schema de `corpus-data.json` (enum) se não existirem
- [ ] Normalizar nomenclatura: e.g., "fotografia" → "fotografia_documental" se for documentação vs. alegoria

---

## Lacuna 3 (MÉDIA) — Séc. XX tardio (1980s–2000s) sem cobertura

### Problema

O corpus cobre até ~1970 nos 6 países canônicos. Não há itens dos anos 1980, 1990, 2000s — período de redemocratização brasileira (1985) e global de emergência do feminist legal scholarship.

### Hipótese de aquisição

- Contra-alegorias e contestações jurídicas nos anos 1990 (marchas, protestos)
- Moedas/selos comemorativos de Dia Internacional da Mulher pós-1980
- Artefacts jurídicos de tribunais internacionais (Tribunal Penal Internacional, Haia — alegorias femininas na decoração)
- Novas formas de alegoria feminina estatal (e.g., selos pós-2000 com programas de gênero)

### Ação

- [ ] Campanha SCOUT específica para o período 1980–2000s
- [ ] Identificar em acervos: BNDigital, arquivo do Tribunal de Justiça de SP, archivos de direitos humanos

---

## Lacuna 4 (BAIXA) — 6 itens sem `year` preenchido

Verificar se os 6 itens sem `year` têm data identificável. Ação: pesquisa complementar nos arquivos fonte.

---

## Resumo de ações imediatas

| Prioridade | Ação | Prazo |
|-----------|------|-------|
| 🔴 CRÍTICA | Buscar архитектура forense BR em BNDigital/IPHAN | Antes da defesa |
| 🔴 CRÍTICA | Adquirir хотя бы 2–3 itens de arquitetura forense | Antes da defesa |
| 🟡 ALTA | Verificar suporte pintura/fotografia/texto/cerâmica — são alegorias? | Antes do freeze |
| 🟡 ALTA | Codificar os 11 itens pendentes de endurecimento | Antes do freeze |
| 🟡 MÉDIA | Normalizar supports no schema de corpus-data.json | Antes do freeze |
| 🟡 MÉDIA | Campanha SCOUT para séc. XX tardio (1980s–2000s) | Durante redação final |
| 🟢 BAIXA | Preencher year dos 6 itens sem data | Antes do freeze |

---

*Briefing gerado a partir do Health Check Semanal 2026-04-25 (issue #43).*
