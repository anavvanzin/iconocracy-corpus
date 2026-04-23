# Metodologia — Cartografia Warburguiana do Imaginário Jurídico

> Espelhamento público (para o repositório-backbone) da nota `METHOD-001 · Atlas, não Score`, trabalhada localmente no vault da tese. Esta versão técnica expõe o compromisso metodológico do projeto e as decisões em aberto; o debate conceitual permanece no vault e no documento para orientação PPGD/UFSC.

| Campo | Valor |
|---|---|
| Nota-fonte (vault) | `METHOD-001` |
| Status | Rascunho metodológico · em discussão com orientação |
| Escopo core | Brasil, 1800–2000 |
| Comparadores | Europa e Estados Unidos (peso ponderado, nunca equivalente) |
| Data | 2026-04-23 |
| Autora | Ana Vanzin — PhD, PPGD/UFSC |

## 1. Problema metodológico

Como arranjar o corpus de alegorias femininas em dispositivos jurídico-estatais (moedas, selos, brasões, monumentos, arquitetura forense, paratextos normativos, 1800–2000) **de modo que o arranjo seja, ele próprio, argumento — e não ilustração**?

Duas alternativas concretas estão em disputa:

1. **LPAI (Legal-Political Allegory Index)** — codebook ordinal que pontua cada imagem em eixos pré-definidos (militarização, nudez alegórica, insígnia jurídica, *embodiment* de gênero). Produz tabela, estatística, ranking. Já operacionalizado: ver [T4 LPAI Ingest Report](./T4-LPAI-INGEST-REPORT.md) (15 fichas SCOUT BR+FR ingeridas em 2026-04-19) e [`tools/schemas/master-record.schema.json`](../tools/schemas/master-record.schema.json).
2. **Atlas-topológico** — arranjo em pranchas à la Warburg (*Bilderatlas Mnemosyne*, 1924–1929) que vizinha imagens por *Pathosformel*, *Nachleben*, ruptura ou *Zwischenraum*, sem hierarquia linear.

A questão não é estilística. É epistemológica: o LPAI, ao pontuar, **produz** uma verdade que afirma apenas **descrever**. Nessa dobradiça mora o risco de a tese reproduzir, no próprio método, o gesto iconocrático que pretende analisar.

## 2. Argumento metodológico

A hipótese do **regime iconocrático** exige uma **cartografia warburguiana do imaginário jurídico**. Tríade articulada, três camadas irredutíveis:

| Camada | Tradição | Operação sobre o corpus |
|---|---|---|
| (a) Arqueologia diacrônica do *dispositif* jurídico | Warburg × Foucault (via Didi-Huberman) | *Nachleben* da alegoria através de rupturas legais |
| (b) Mapeamento do campo de visão jurídica | Bourdieu × Artl@s × cartografia feminista | Quem encomenda, valida e reproduz Justitia, e em que posição no campo |
| (c) Atlas como modelo curatorial da tese | Pollock, *Virtual Feminist Museum* | A própria tese como atlas feminista, contra-canônico |

### Recomendação operacional

1. **Não descartar o LPAI.** Reenquadrá-lo como *capta* (Drucker, 2011) — leitura construída, parcial, situada — e usá-lo como ferramenta de **descoberta de corpus** e **documentação de ausência**. Exemplo: «nenhuma Justitia negra ou indígena nos palácios brasileiros» torna-se achado quantificável. Ver especificação completa em [`schema/lpai-v2-as-capta.md`](../schema/lpai-v2-as-capta.md).
2. **Adotar o atlas-topológico como estrutura de argumento.** As vizinhanças de prancha fazem o trabalho que o score não consegue: expõem *Pathosformeln*, ruptura, iconoclasmo e sobrevivência sem impor teleologia. Ver prancha-piloto em [`docs/pilots/P01-republica-armada.md`](./pilots/P01-republica-armada.md).
3. **Usar Iconclass** como camada de interoperabilidade (códigos 11M31 Justitia, 44G411 República feminina, 44G51 Liberdade) — única via de descoberta federada com ~50 bases linkadas, incluindo Erdteilallegorien e PHAROS.

## 3. Evidências (síntese de cinco correntes de pesquisa)

### 3.1 Warburg aplicado ao direito — campo quase vazio

- **STRAMIGNONI (2024)**, *Law and Critique* — único artigo em língua inglesa que mobiliza explicitamente *Pathosformel* na teoria da imagem jurídica.
- **HAYAERT (2020)**, *Lawful Lies: Veiled Justice in Early Modern Europe* (Edinburgh UP) — executa anatomia warburguiana de Justitia sem nomear Warburg.
- **BECKER (2013)**, *Journal of Art Historiography* n. 9 — aplica *Pathosformel* a Germania e à alegoria cívica.
- **RESNIK; CURTIS (2011)**, *Representing Justice* (Yale UP) — achado empírico decisivo: em milhares de tribunais auditados globalmente, apenas **um** (St. Croix, 1993) representa Justitia como mulher não branca.

→ Lacuna estrutural: nenhum trabalho combina Warburg, direito, feminismo e América Latina. A tese ocupa esse vácuo.

### 3.2 Não existe atlas digital dedicado a alegorias femininas no direito

- O **NCRD (Netherlands Center for Legal Iconography Documentation)** — única base dedicada à iconografia jurídica — **encerrou em dezembro de 2021**.
- Modelo formal mais próximo: **Engramma — Mnemosyne Atlas** (63 pranchas, 14 rotas temáticas, links cruzados).
- Modelo estrutural mais próximo para alegoria feminina: **Erdteilallegorien** (Viena): 407+ figuras, GIS, timeline, Iconclass completo, código aberto.
- Brasil: Brasiliana Iconográfica, BNDigital (3M+ documentos, OCR), IMS Acervo, Arquivo Nacional, Cartografia do Brasil — BNP.

→ A tese não preenche lacuna — nomeia e constrói o campo.

### 3.3 Crítica feminista e pós-colonial ao score é cumulativa e dura

- **MERRY (2016)**, *The Seductions of Quantification* — indicadores jurídicos *produzem* verdade em vez de revelá-la.
- **HARAWAY (1988)**, "Situated Knowledges" — o «truque-deus» do índice que pretende ver tudo de lugar nenhum.
- **DRUCKER (2011)**, *Digital Humanities Quarterly* — *«all data is capta»*; visualização padrão é *«anathema to humanistic thought»*.
- **ESPELAND; SAUDER (2007)**, *American Journal of Sociology* — reatividade: um índice disciplina os dados futuros em direção ao que «pontua bem». Previsão: um LPAI adotado começa a enviesar a própria seleção do corpus.
- **WARNER (1985)**, *Monuments and Maidens* — alegoria feminina é **constitutivamente paradoxal**: corpo genérico que encarna a lei da qual as mulheres foram excluídas. Nenhum score suporta a contradição; um atlas pode justapor emblema e exclusão.
- **DIDI-HUBERMAN (2002)**, *L'image survivante* — imagens são policrônicas; qualquer eixo único produz má-leitura sistemática.

### 3.4 Militarização da alegoria feminina segue padrão contra-intuitivo

| País | Período | Figura | Atributos militares ganhos |
|---|---|---|---|
| França | 1789–1914 | Marianne | gládio, fúsil, barrete frígio militarizado |
| Alemanha | 1848–1918 | Germania | *Reichsschwert*, couraça, *Pickelhaube* |
| Reino Unido / EUA | séc. XIX | Britannia / Columbia | capacete, tridente, corpo blindado sobre territórios colonizados |
| Brasil | 1889–1910 | República | espada, górgona — modo defensivo-reativo |
| Brasil (Estado Novo) | 1937–1945 | Pátria / República | **deslocamento** — culto personalista de Vargas desloca a alegoria armada |

**Padrão estrutural**: a militarização intensifica-se sob (a) ruptura republicana, (b) ameaça militar externa, (c) expansão imperial. **Atenua-se ou desloca-se** sob autoritarismo personalista — porque a figura armada feminina carrega conotações democrático-revolucionárias incompatíveis com a pessoalização do poder. A **iconocracia tropical** do Estado Novo prefere a mãe-Pátria doméstica à República armada.

### 3.5 Dobradiça metodológica: Didi-Huberman + Pollock

- **DIDI-HUBERMAN (2011)**, *Atlas, ou le gai savoir inquiet* — articulação explícita entre *Nachleben* warburguiano e arqueologia foucaultiana.
- **POLLOCK** — *Virtual Feminist Museum*: único precedente que operacionaliza o atlas warburguiano como **dispositivo curatorial feminista contra-canônico**.
- **ANDERMANN**, *The Optic of the State: Visuality and Power in Argentina and Brazil* — alegoria feminina na América Latina carrega carga política específica: nação feminizada como *patria/justicia* enquanto mulheres reais são excluídas do sujeito jurídico.

## 4. Lacunas e riscos

### Lacunas conceituais que a tese pode preencher
- Nenhum estudo combina Warburg + direito + feminismo + América Latina com corpus sistemático.
- A iconografia jurídica brasileira não está atlasificada — apenas catalogada dispersamente.
- A categoria **iconoclasmo / conflito de imagens** raramente é cruzada com alegoria feminina em contextos jurídico-estatais pós-coloniais — hipótese de **iconocracia/iconoclasmo tropical** permanece aberta.
- A conversão *capta* ↔ atlas, com o LPAI reenquadrado como ferramenta de descoberta, não foi executada em nenhum projeto conhecido.

### Riscos metodológicos a vigiar
- **Presentismo** — ler alegorias oitocentistas com gramática feminista contemporânea sem marcar a operação.
- **Comparação forçada** — equiparar Marianne e República brasileira sem registrar diferença de instalação institucional e «comunidade de imaginação» (Carvalho).
- **Instabilidade terminológica** — manter vocabulário estável: *iconocracia*, *regime iconocrático*, *feminilidade de Estado*, *reconhecimento sem reciprocidade*, *iconoclasmo*, *purificação simbólica*.
- **Alargamento de escopo** — Europa e EUA são **comparador**, não core. Fixar Brasil 1800–2000 como eixo.

## 5. Próximos passos

### Imediatos
- [ ] Congelar pipeline antes de qualquer inferência: teoria → codebook → amostragem → piloto → confiabilidade → **freeze** → análise.
- [ ] Decidir formalmente o destino do LPAI: (a) descartar, (b) reenquadrar como *capta* (recomendado), (c) manter pontuado com changelog explícito.
- [ ] Abrir capítulo metodológico da tese com esta tríade (arqueologia + campo + atlas) como fio condutor.

### Corpus e piloto
- [ ] Piloto de 10 pranchas warburguianas do corpus Brasil (República Lopes Rodrigues 1896; Sansebastiano Belém 1897; selos postais 1890–1930; moedas republicanas; paratextos da Constituição 1891; tribunais; monumentos vandalizados). Primeira prancha entregue: [`docs/pilots/P01-republica-armada.md`](./pilots/P01-republica-armada.md).
- [ ] Cada prancha: 6–12 imagens, legenda com *Pathosformel* dominante, marca de *Nachleben* e registro de iconoclasmo.
- [ ] Medir cobertura do corpus contra a lacuna Resnik-Curtis: documentar ausência de Justitia negra/indígena em tribunais brasileiros como achado quantificável.

### Leituras prioritárias para ancorar o capítulo
1. DIDI-HUBERMAN, Georges. *Atlas, ou le gai savoir inquiet*. Paris: Minuit, 2011.
2. POLLOCK, Griselda. *Differencing the Canon: Feminist Desire and the Writing of Art's Histories*. London: Routledge, 1999.
3. RESNIK, Judith; CURTIS, Dennis. *Representing Justice*. New Haven: Yale UP, 2011.
4. CARVALHO, José Murilo de. *A Formação das Almas: o imaginário da República no Brasil*. São Paulo: Companhia das Letras, 1990.
5. MERRY, Sally Engle. *The Seductions of Quantification*. Chicago: Chicago UP, 2016.
6. WARNER, Marina. *Monuments and Maidens*. London: Weidenfeld & Nicolson, 1985.
7. AGULHON, Maurice. *Marianne into Battle*. Cambridge: Cambridge UP, 1981.
8. WENK, Silke. *Versteinerte Weiblichkeit*. Köln: Böhlau, 1996.

## 6. Referências (seleção ABNT NBR 6023:2025)

AGULHON, Maurice. *Marianne into Battle: Republican Imagery and Symbolism in France, 1789–1880*. Cambridge: Cambridge University Press, 1981.

AGAMBEN, Giorgio. *Potentialities: Collected Essays in Philosophy*. Tradução: Daniel Heller-Roazen. Stanford: Stanford University Press, 1999.

ANDERMANN, Jens. *The Optic of the State: Visuality and Power in Argentina and Brazil*. Pittsburgh: University of Pittsburgh Press, 2007.

BECKER, Colleen. Aby Warburg's Pathosformel as methodological paradigm. *Journal of Art Historiography*, n. 9, 2013. Disponível em: <https://arthistoriography.wordpress.com/9-dec13/>.

CAPELATO, Maria Helena Rolim. *Multidões em cena: propaganda política no varguismo e no peronismo*. Campinas: Papirus, 1998.

CARVALHO, José Murilo de. *A Formação das Almas: o imaginário da República no Brasil*. São Paulo: Companhia das Letras, 1990.

DIDI-HUBERMAN, Georges. *L'image survivante: Histoire de l'art et temps des fantômes selon Aby Warburg*. Paris: Éditions de Minuit, 2002.

DIDI-HUBERMAN, Georges. *Atlas, ou le gai savoir inquiet: L'œil de l'histoire, 3*. Paris: Éditions de Minuit, 2011.

D'IGNAZIO, Catherine; KLEIN, Lauren. *Data Feminism*. Cambridge, MA: MIT Press, 2020. DOI: 10.7551/mitpress/11805.001.0001.

DRUCKER, Johanna. Humanities Approaches to Graphical Display. *Digital Humanities Quarterly*, v. 5, n. 1, 2011. Disponível em: <http://www.digitalhumanities.org/dhq/vol/5/1/000091/000091.html>.

ESPELAND, Wendy Nelson; SAUDER, Michael. Rankings and reactivity: how public measures recreate social worlds. *American Journal of Sociology*, v. 113, n. 1, p. 1–40, 2007.

HARAWAY, Donna. Situated Knowledges: The Science Question in Feminism and the Privilege of Partial Perspective. *Feminist Studies*, v. 14, n. 3, p. 575–599, 1988.

HAYAERT, Valérie. *Lawful Lies: Veiled Justice in Early Modern Europe*. Edinburgh: Edinburgh University Press, 2020.

JAY, Martin. Must Justice Be Blind? The Challenge of Images to the Law. *Filozofski Vestnik*, v. 17, n. 2, p. 65–81, 1996. Republicado em: DOUZINAS, C.; NEAD, L. (orgs.). *Law and the Image*. Chicago: University of Chicago Press, 1999. p. 19–35.

JOHNSON, Christopher D. *Memory, Metaphor, and Aby Warburg's Atlas of Images*. Ithaca, NY: Cornell University Press / Cornell University Library, 2012. (Signale: Modern German Letters, Cultures, and Thought). 286 p. ISBN 978-0-8014-7742-3.

LEGENDRE, Pierre. *Dieu au miroir: étude sur l'institution des images*. Paris: Fayard, 1994. (Leçons III). 348 p. ISBN 978-2-213-03185-9.

MERRY, Sally Engle. *The Seductions of Quantification: Measuring Human Rights, Gender Violence, and Sex Trafficking*. Chicago: University of Chicago Press, 2016.

MOSSE, George L. *Nationalism and Sexuality: Respectability and Abnormal Sexuality in Modern Europe*. New York: Howard Fertig, 1985.

POLLOCK, Griselda. *Differencing the Canon: Feminist Desire and the Writing of Art's Histories*. London: Routledge, 1999.

RESNIK, Judith; CURTIS, Dennis. *Representing Justice: Invention, Controversy, and Rights in City-States and Democratic Courtrooms*. New Haven: Yale University Press, 2011.

SHERWIN, Richard K. *Visualizing Law in the Age of the Digital Baroque: Arabesques and Entanglements*. London: Routledge, 2011.

STRAMIGNONI, Igor. [Artigo sobre Warburg e teoria da imagem jurídica]. *Law and Critique*, 2024. (DOI a confirmar na corrente `stream1_warburg_legal`).

VISMANN, Cornelia. *Medien der Rechtsprechung*. Frankfurt am Main: S. Fischer Verlag, 2011. 456 p. ISBN 978-3-10-400946-9 (e-book) / 978-3-596-37067-2 (ed. Taschenbuch 2019).

WARNER, Marina. *Monuments and Maidens: The Allegory of the Female Form*. London: Weidenfeld & Nicolson, 1985.

WENK, Silke. *Versteinerte Weiblichkeit: Allegorien in der Skulptur der Moderne*. Köln: Böhlau, 1996.

---

## Status

Rascunho metodológico · aguardando discussão com orientação PPGD/UFSC e decisão formal sobre destino do LPAI.

## Ligações internas

- [`docs/T4-LPAI-INGEST-REPORT.md`](./T4-LPAI-INGEST-REPORT.md) — estado operacional do LPAI v2 (15 fichas SCOUT BR+FR).
- [`schema/lpai-v2-as-capta.md`](../schema/lpai-v2-as-capta.md) — reenquadramento do LPAI como *capta* (Drucker).
- [`docs/pilots/P01-republica-armada.md`](./pilots/P01-republica-armada.md) — prancha-piloto com os operadores curatoriais aplicados.
- [ADR-005 — GitHub canônico / HF público](./adr/005-github-and-hf-release-surfaces.md).
- [`README.md`](../README.md) — modelo operacional do monorepo.
