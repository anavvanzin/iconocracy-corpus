# Revisão acadêmica — execução de pesquisa 2026-05-19

**Objeto:** pacote completo da rodada em `corpus/candidatos/2026-05-19/` (`candidatos-2026-05-19.json` — 43 candidatos — + `research-2026-05-19.md`, `SHARED_SPEC.md`, `validate.py`, `sqN_candidates.json`, `sqN_log.md`, `stats.json`, `dedup_urls.txt`)
**Pipeline de origem:** `docs/research/deep-research-runbook.md` (SQ1–SQ4)
**Revisor:** sessão de revisão (branch `claude/review-thesis-research`)
**Data da revisão:** 2026-05-24

---

## 1. Sumário executivo

A execução de 2026-05-19 produziu **43 candidatos** em quatro sub-questões. Auditados
contra os **critérios de inclusão do corpus** (`CLAUDE.md`: alegoria feminina + função
jurídico-política + datável **1800–2000** + um dos **6 países** FR/UK/DE/US/BE/BR + suporte aceito):

- **19 candidatos são ingestíveis** no corpus empírico (SQ1 = 5, SQ2 = 14).
- **24 candidatos NÃO pertencem ao corpus** — falham período e/ou país. São **fontes
  iconográficas** (genealogia do tipo Iustitia: Ripa, Alciato, Saavedra, Camerarius;
  pinturas SMK/V&A dos séc. XVI–XVIII), valiosas como repertório de referência da tese,
  mas não como itens empíricos 1800–2000.
- **2 dos 19 aceitos têm risco de copyright** (Portinari, falecido 1962) e devem entrar
  com `copyright-hold` para qualquer release público.

**Recomendação central:** a execução conflou dois alvos distintos — *candidatos ao corpus*
versus *fontes/genealogia iconográfica*. SQ1/SQ2 cumpriram o primeiro; SQ3/SQ4 entregaram
majoritariamente o segundo. Separar os dois antes de qualquer merge.

**Origem do desvio é de especificação, não de execução.** Verifiquei a `SHARED_SPEC.md` e o
`validate.py` da rodada (Google Drive, pasta `iconocracia-2026-05-19/`): nenhum dos dois
impõe os critérios de inclusão do corpus. As regras de filtragem da spec são apenas (1) dedup
por URL, (2) sem Gallica em SQ1, (3) qualidade mínima (ano + instituição + conexão não-tangencial
com alegoria feminina jurídica), (4) preferência institucional, (5) captura IIIF. **Não há gate
de período (1800–2000) nem whitelist de país** — a spec até exemplifica `country` com "Austria".
O `validate.py` confere só os 12 campos obrigatórios + dedup. Logo os subagentes executaram a
spec corretamente; o vazamento de fontes pré-1800/fora-dos-6-países é falha de desenho da spec,
corrigível adicionando esses dois filtros ao `validate.py` em rodadas futuras.

| SQ | Coletados | Aceitos (corpus) | Reclassificados (fonte) |
|----|----------:|-----------------:|------------------------:|
| SQ1 | 8 | 5 | 3 |
| SQ2 | 15 | 14 | 1 |
| SQ3 | 10 | 0 | 10 |
| SQ4 | 10 | 0 | 10 |
| **Total** | **43** | **19** | **24** |

---

## 2. Avaliação metodológica

**Pontos fortes.** Desenho de 4 subagentes paralelos por sub-questão; cobertura ICONCLASS
100 % (43/43); cobertura IIIF razoável onde os repositórios expõem a Presentation API
(SQ3 100 %, SQ4 70 %, SQ1 parcial, SQ2 0 % por limitação das bases latino-americanas);
metadados ABNT e Chicago presentes em todos os itens; deduplicação por URL executada.

**Discrepâncias a reconciliar.**

1. **Ferramenta divergente do runbook.** O runbook fixa **Exa-only** ("No firecrawl.
   Exa-only per skill-comply audit"). As notas de execução de 2026-05-19 declaram uso de
   **Perplexity** (`pplx search web` / `pplx content fetch`). Reconciliar: ou atualizar o
   runbook para admitir `pplx`, ou reexecutar via Exa para reprodutibilidade auditável.
2. **Baseline numérico desatualizado.** O cabeçalho da execução cita "145 canônicos /
   264 / 95". O estado vivo do repositório é **274** tanto em `corpus-data.json` quanto em
   `records.jsonl`. O pool de dedup (368 URLs) foi montado de `corpus-data.json` +
   `corpus-data-enriched.json` + um `.bak.20260516`. Tratar os números do relatório como
   instantâneo histórico, não como estado atual.
3. **Dedup apenas por URL.** **0 colisões exatas de URL** contra o corpus vivo (verificado) —
   bom sinal, mas insuficiente. Falta dedup **visual (CLIP)** e **por título/autor**. Itens de
   motivo de alta sobreposição (Lincoln/Iustitia, Marianne, A República) exigem checagem pelo
   agente `corpus-dedup` + `iconocracy_clip.py` antes de ingestão.
4. **ICONCLASS parcialmente heurístico.** Confirmado no `validate.py`: itens sem código recebem
   `11MM31` quando a descrição/motif contém "justiça/justice/giustizia" e `48C51` quando contém
   "alegoria/allegory". São **palpites automáticos** — validar com `iconclass-reviewer` antes do
   ingest.
5. **Spec sem critérios de inclusão (causa-raiz).** `SHARED_SPEC.md` + `validate.py` da rodada não
   filtram por período nem país (ver §1). **Correção sugerida:** acrescentar ao `validate.py` um
   gate `1800 <= ano <= 2000` e `country ∈ {France, United Kingdom, Germany, United States,
   Belgium, Brazil}`, roteando os reprovados para uma trilha "fonte/genealogia" separada.

---

## 3. Auditoria de critérios de inclusão (43 candidatos)

País✓ = país ∈ {FR, UK, DE, US, BE, BR}. Período✓ = datável dentro de 1800–2000.

| SQ | id | título | país | ano | país✓ | período✓ | veredito | conf |
|----|----|--------|------|-----|:---:|:---:|------|------|
| SQ1 | `sq1-2026-05-19-baker-godwin-lincoln-005` | Abraham Lincoln, Republican candidate for | United States | 1860 | Y | Y | ACCEPT | high |
| SQ1 | `sq1-2026-05-19-goya-truth-died-008` | La verdad ha muerto (Truth has died) | Spain | 1814–1815 | N | Y | RECLASSIFY (fonte) | medium |
| SQ1 | `sq1-2026-05-19-gusman-justice-vengeance-003` | La Justice et la Vengeance Divine poursuiv | United Kingdom | 1840–1878 | Y | Y | ACCEPT | high |
| SQ1 | `sq1-2026-05-19-inger-liberty-004` | Liberty. "Liberty brings to the earth just | United States | 1863 | Y | Y | ACCEPT | high |
| SQ1 | `sq1-2026-05-19-kimmel-outbreak-007` | The outbreak of the rebellion in the Unite | United States | 1865 | Y | Y | ACCEPT | high |
| SQ1 | `sq1-2026-05-19-prud-hon-innocence-002` | Justitia beschermt Onschuld tegen Misdaad | Netherlands | 1806 | N | Y | RECLASSIFY (fonte) | high |
| SQ1 | `sq1-2026-05-19-schwind-justitia-001` | Allegorische Figur: Justitia (Gerechtigkei | Austria | 1848 | N | Y | RECLASSIFY (fonte) | high |
| SQ1 | `sq1-2026-05-19-traubel-triumph-006` | Triumph | United States | 1861 | Y | Y | ACCEPT | high |
| SQ2 | `sq2-2026-05-19-alegoria-centenario-mhn-villares-005` | Alegoria da Exposição Internacional do Cen | Brazil | 1922 | Y | Y | ACCEPT | high |
| SQ2 | `sq2-2026-05-19-alegoria-lei-aurea-villares-004` | Alegoria à Lei de 13 de Maio de 1888 (estu | Brazil | 1888 | Y | Y | ACCEPT | medium |
| SQ2 | `sq2-2026-05-19-caçada-jaguar-museu-republica-014` | Die Kämpfende Amazone (Caçada ao Jaguar) | Brazil | 1860 | Y | Y | ACCEPT | medium |
| SQ2 | `sq2-2026-05-19-codigo-criminal-imperio-1830-007` | Código Criminal do Império do Brasil | Brazil | 1830 | Y | Y | ACCEPT | medium |
| SQ2 | `sq2-2026-05-19-codigo-criminal-imperio-1876-008` | Codigo criminal do imperio do Brazil: anno | Brazil | 1876 | Y | Y | ACCEPT | medium |
| SQ2 | `sq2-2026-05-19-codigo-penal-chile-1874-memoriachilena-011` | Código Penal chileno (1874) — edição origi | Chile | 1874 | N | Y | RECLASSIFY (fonte) | medium |
| SQ2 | `sq2-2026-05-19-compromisso-constitucional-002` | Compromisso Constitucional | Brazil | 1896 | Y | Y | ACCEPT | high |
| SQ2 | `sq2-2026-05-19-ex-libris-bn-visconti-009` | Ex-libris da Biblioteca Nacional (A Mulher | Brazil | 1903 | Y | Y | ACCEPT | high |
| SQ2 | `sq2-2026-05-19-gloria-republica-decio-villares-pintura-015` | Alegoria à República (Décio Villares — con | Brazil | 1890 | Y | Y | ACCEPT | low |
| SQ2 | `sq2-2026-05-19-justica-salomao-portinari-006` | A Justiça de Salomão | Brazil | 1948 | Y | Y | **ACCEPT (copyright-hold)** | high |
| SQ2 | `sq2-2026-05-19-patria-pedro-bruno-001` | Pátria | Brazil | 1919 | Y | Y | ACCEPT | high |
| SQ2 | `sq2-2026-05-19-portinari-ciclos-economicos-mnec-010` | Ciclos Econômicos (afrescos do MEC) | Brazil | 1936–1944 | Y | Y | **ACCEPT (copyright-hold)** | high |
| SQ2 | `sq2-2026-05-19-providencia-guia-cabral-visconti-013` | A Providência guia Cabral | Brazil | 1900 | Y | Y | ACCEPT | medium |
| SQ2 | `sq2-2026-05-19-republica-brasil-decio-villares-012` | A República (estudo escultura/bandeira) | Brazil | 1889 | Y | Y | ACCEPT | low |
| SQ2 | `sq2-2026-05-19-republica-manoel-lopes-rodrigues-003` | A República | Brazil | 1896 | Y | Y | ACCEPT | high |
| SQ3 | `sq3-2026-05-19-heidelberg-ripa-iconologia-010` | Iconologia Overo Descrittione (Ripa) | Germany | 1603 | Y | N | RECLASSIFY (fonte) | high |
| SQ3 | `sq3-2026-05-19-smk-justitia-abildgaard-001` | Justitia | Denmark | ca. 1780–1800 | N | N | RECLASSIFY (fonte) | high |
| SQ3 | `sq3-2026-05-19-smk-justitia-castello-006` | Siddende Justitia | Italy | ca. 1579–1649 | N | N | RECLASSIFY (fonte) | high |
| SQ3 | `sq3-2026-05-19-smk-justitia-fahrenholtz-004` | Titelblad: "Justitia" | Denmark | 1783 | N | N | RECLASSIFY (fonte) | high |
| SQ3 | `sq3-2026-05-19-smk-justitia-goltzius-005` | Retfærdighed (Justitia) | Netherlands | 1592 | N | N | RECLASSIFY (fonte) | high |
| SQ3 | `sq3-2026-05-19-smk-justitia-hansen-002` | "Justitia" | Denmark | ca. 1884–1897 | N | Y | RECLASSIFY (fonte) | high |
| SQ3 | `sq3-2026-05-19-smk-justitia-krock-007` | Siddende Justitia (estudo Salomão) | Denmark | ca. 1671–1738 | N | N | RECLASSIFY (fonte) | high |
| SQ3 | `sq3-2026-05-19-smk-justitia-unknown17c-003` | Justitia | Netherlands | ca. 1600–1699 | N | N | RECLASSIFY (fonte) | high |
| SQ3 | `sq3-2026-05-19-smk-retfaerdighed-abildgaard-008` | Udkast til Retfærdighedsrelieffet | Denmark | ca. 1792–1797 | N | N | RECLASSIFY (fonte) | high |
| SQ3 | `sq3-2026-05-19-vam-iustitia-virtues-009` | Iustitia (from the series The Virtues) | United Kingdom | ca. 1575–1625 | Y | N | RECLASSIFY (fonte) | high |
| SQ4 | `sq4-2026-05-19-alciato1531-augsburg-006` | Emblematum liber — Augsburg 1531 | Germany | 1531 | Y | N | RECLASSIFY (fonte) | high |
| SQ4 | `sq4-2026-05-19-alciato1550-lyon-007` | Emblemata — Lyon 1550 | France | 1550 | Y | N | RECLASSIFY (fonte) | high |
| SQ4 | `sq4-2026-05-19-alciato1577-antwerp-008` | Omnia Emblemata — Antuérpia 1577 | Belgium | 1577 | Y | N | RECLASSIFY (fonte) | high |
| SQ4 | `sq4-2026-05-19-camerarius-cent3-009` | Symbolorum & emblematum (Camerarius) | Germany | 1596 | Y | N | RECLASSIFY (fonte) | high |
| SQ4 | `sq4-2026-05-19-loscher1536-iustitia-011` | Allegorie der irdischen u. göttlichen Ger | Germany | 1536 | Y | N | RECLASSIFY (fonte) | medium |
| SQ4 | `sq4-2026-05-19-ripa1603-mdz-001` | Iconologia (Ripa) — MDZ | Italy | 1603 | N | N | RECLASSIFY (fonte) | high |
| SQ4 | `sq4-2026-05-19-ripa1613-siena-003` | Iconologia — Siena 1613 | Italy | 1613 | N | N | RECLASSIFY (fonte) | high |
| SQ4 | `sq4-2026-05-19-ripa1645-veneza-004` | Iconologia — Veneza 1645 | Italy | 1645 | N | N | RECLASSIFY (fonte) | high |
| SQ4 | `sq4-2026-05-19-ripa1669-frankfurt-005` | Erneuerte Iconologia — Frankfurt 1669 | Germany | 1669 | Y | N | RECLASSIFY (fonte) | high |
| SQ4 | `sq4-2026-05-19-saavedra1643-empresas-010` | Idea de un principe... (Saavedra) | Spain | 1643 | N | N | RECLASSIFY (fonte) | high |

**Totais:** 19 ACCEPT (2 com copyright-hold) · 24 RECLASSIFY. Falhas: 16 por país, 19 por período (sobreposição em SQ3/SQ4).

---

## 4. Avaliação por sub-questão

- **SQ1 (5/8 aceitos).** Forte para o eixo US Guerra Civil (Lincoln, Liberty, Triumph, Outbreak)
  e uma estampa britânica (Gusman). Os 3 reclassificados (Goya 1814 ES, Prud'hon 1806 NL,
  Schwind 1848 AT) são alegorias relevantes mas fora dos 6 países — fonte de diálogo comparativo,
  não corpus.
- **SQ2 (14/15 aceitos) — a sub-questão mais produtiva.** Núcleo brasileiro robusto (República,
  Lei Áurea, códigos criminais imperiais, ex-libris da BN, alegorias de Décio Villares). Único
  reclassificado: Código Penal chileno 1874 (Chile fora dos 6 países). **Atenção a copyright**
  nas duas obras de Portinari (item 5).
- **SQ3 (0/10).** Coleção SMK (Copenhague) + V&A + Ripa Heidelberg: todas pinturas/gravuras
  de Iustitia dos séc. XVI–XVIII. **Genealogia pura** do tipo iconográfico — não datável 1800–2000.
- **SQ4 (0/10).** Tratados de iconologia/emblemática (Alciato 1531–1577, Ripa 1603–1669,
  Saavedra 1643, Camerarius 1596, Loscher 1536). São as **fontes-matriz** da iconografia jurídica
  ocidental — capítulo de genealogia/Nachleben, jamais itens do corpus empírico.

---

## 5. Registro de copyright (bloqueio para release público)

| item | autor | falecimento | domínio público (BR, 70 anos p.m.a.) |
|------|-------|-------------|--------------------------------------|
| `sq2-...-justica-salomao-portinari-006` | Candido Portinari | 1962 | a partir de 2033 |
| `sq2-...-portinari-ciclos-economicos-mnec-010` | Candido Portinari | 1962 | a partir de 2033 |

Demais aceitos do séc. XIX/início XX: autores presumidamente em domínio público (Décio
Villares †1931, Pedro Bruno †1942, Eliseu Visconti †1944, Manoel Lopes Rodrigues †1917).
**Verificar caso a caso** o falecimento + 70 anos antes de incluir thumbnails em export público.
Honrar `copyright-hold` no `release-gate` skill.

---

## 6. Plano de ingestão

> Escopo desta revisão: **nenhuma mutação** de `data/processed/records.jsonl` nem de
> `corpus/corpus-data.json`. A ingestão completa exige análise IconoCode e dedup CLIP que
> dependem de imagens/MCP não disponíveis nesta sessão. Abaixo, o caminho executável.

### Pré-condição (gap de schema)
O JSON de candidatos é **plano** (`title`/`url`/`motif`/`date`/`citation_abnt`/`iconclass_codes`…).
O canônico `records.jsonl` exige o schema **aninhado** master-record (`input`/`webscout`/
`iconocode`/`exports`/`timestamps`) **+ análise IconoCode** (regime + 10 indicadores de
endurecimento 0–3). Os candidatos **não têm** essa camada analítica — portanto nenhum vira
master-record completo sem um passo IconoCode.

### Para os 19 ACCEPT
1. **Dedup textual + visual.** Agente `corpus-dedup` sobre título/autor/url; para itens com
   `thumbnail_url`/`url_image_download`, rodar CLIP via skill `scout-dedupe`
   (`iconocracy_clip.py`). Descartar duplicatas confirmadas.
2. **Notas SCOUT.** Materializar sobreviventes em `vault/candidatos/` no padrão `XX-NNN Title.md`
   (hook PreToolUse valida o nome); gerador existente: `tools/scripts/scout_notes.py`
   (mapeia país→código, motivo→tag).
3. **IconoCode.** Rodar ICONOCODE (Panofsky 3 níveis + 10 indicadores + regime) por item —
   camada analítica ausente; sem ela o registro fica incompleto.
4. **Master records.** Montar registros aninhados via o caminho SCOUT→records
   (`tools/scripts/vault_sync.py sync`) e validar:
   `python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record`.
5. **Export.** `python tools/scripts/records_to_corpus.py --diff` (preview) → aplicar em
   `corpus/corpus-data.json`; reexecutar `tools/scripts/sync_companion.py`.
6. **Release gate.** Antes de qualquer snapshot público/HF, honrar os itens `copyright-hold`
   (Portinari) conforme skill `release-gate`.

### Para os 24 RECLASSIFY
**Não ingerir** no corpus empírico. Opcionalmente registrar como **notas de fonte/genealogia**
no vault (linhagem do tipo Iustitia: Ripa → emblemática → personificações nórdicas), mantidas
distintas do corpus 1800–2000. Úteis para o capítulo de Pathosformel/Nachleben.

---

## 7. Encaminhamentos para próxima rodada

- **SQ5/SQ6** sugeridos pela execução (banknotes/stamps fora do Numista; moedas via ANS/
  MoneyMuseum) — manter o filtro de 6 países + 1800–2000 no desenho da query, evitando o
  vazamento de fontes pré-1800 que afetou SQ3/SQ4.
- Reconciliar o runbook (`docs/research/deep-research-runbook.md`) com a ferramenta de fato
  utilizada (`pplx` vs Exa).
- Atualizar o baseline citado em futuros relatórios para refletir os **274** itens vivos.
