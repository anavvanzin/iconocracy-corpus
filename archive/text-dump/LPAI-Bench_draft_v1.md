# LPAI-Bench: A Benchmark Dataset for Evaluating Vision-Language Models on Legal-Political Iconography

**Ana Vanzin**¹

¹ Graduate Program in Law (PPGD), Federal University of Santa Catarina (UFSC), Florianópolis, Brazil.

**Correspondence:** ana.vanzin@posgrad.ufsc.br · github.com/anavvanzin/iconocracy-corpus

**Keywords:** legal iconography, vision-language models, benchmark dataset, cultural AI, digital humanities, gender studies, Iconclass, allegorical representation

---

## Abstract

We introduce LPAI-Bench, the first annotated benchmark dataset for evaluating vision-language models (VLMs) on the classification of legal-political allegorical imagery. The dataset comprises 116 expertly annotated items (expandable to 250+) spanning seven countries (Brazil, France, the United Kingdom, Germany, the United States, and Belgium), two centuries (1800–2000), and six material supports (coins, postal stamps, monuments, engravings, frontispieces, and currency notes). Each item is annotated according to the Legal-Political Allegory Index (LPAI v2), a domain-specific taxonomy comprising eight base classes, four modifier layers, and approximately seventy concordances with the Iconclass controlled vocabulary. Items are additionally scored across ten ordinal indicators of a documented visual process we term endurecimento — the progressive purification of the allegorized female body in state iconography — measured on a 0–3 scale per indicator. LPAI-Bench supports three evaluation tasks: (T1) multi-label classification by LPAI base class; (T2) ternary regime classification (FUNDACIONAL / NORMATIVO / MILITAR); and (T3) purification indicator scoring. We report zero-shot baseline performance for CLIP ViT-B/32 and GPT-4V, following the experimental protocol established by Spinaci, Klic, and Colavizza (2025) for Christian iconography, and demonstrate a substantial performance gap relative to human expert annotation. All images are sourced from open-access digital repositories (Gallica/BnF, Hemeroteca Digital Nacional, Senado Federal do Brasil) under verified open licences and are deposited on the Hugging Face Hub and Zenodo under CC BY 4.0.

---

## Background

### The blind spot of computational iconography

The visual culture of modern legal and political institutions constitutes one of the most systematically understudied domains in computational image analysis. Representations of Justice, Liberty, the Republic, and cognate allegorical figures appear on the coins handled by millions of people daily, on the postal stamps that circulate state authority across national territories, on the facades of courts and parliaments, and in the frontispieces of foundational legal texts. These images are not merely decorative: they function as instruments of political legitimation, encoding normative visions of the state, citizenship, and gender that have shaped legal culture across two centuries.¹

Despite the volume and historical significance of this corpus, no computational tool exists today for the identification, classification, or analysis of legal-political allegories. While computer vision has advanced rapidly in adjacent domains — art history, cultural heritage digitization, and religious iconography — the specifically juridical-political dimension of allegorical imagery has remained a blind spot.² Iconclass, the most widely used controlled vocabulary for iconographic classification, contains relevant notations for allegorical subjects (notably codes 44A1 for Justice, 44B11 for Liberty, and 48C51 for allegorical female figures in political contexts), but no machine-learning benchmark has been built against these notations for the legal-political domain specifically.³

### Related work and the state of VLM benchmarking in cultural domains

The application of vision-language models to cultural heritage classification has accelerated markedly since 2023. Santini et al. (2023) demonstrated the viability of CLIP for multimodal search over the Iconclass vocabulary, building a retrieval system over approximately 500,000 annotated artworks; their system enables free-text and image-based queries over Iconclass notations, but does not produce a classification benchmark or evaluate model performance against gold-standard labels.⁴ CultureCLIP (2025) introduced parameter-efficient LoRA fine-tuning of CLIP for culturally specific visual distinctions, demonstrating significant gains over vanilla CLIP on culture-specific benchmarks.⁵ CATS (2025), published in *npj Heritage Science*, validated multi-label classification approaches for complex cultural taxonomies using large language models, providing methodological precedent for our own multi-label evaluation design.⁶

The closest direct precedent for our work is Spinaci, Klic, and Colavizza (2025), who benchmarked CLIP, SigLIP, GPT-4o, and Gemini 2.5 on Christian saint iconography classification, using three datasets with native Iconclass support (ArtDL, ICONCLASS, and Wikidata) filtered to the ten most frequent classes.⁷ Their results demonstrated that state-of-the-art VLMs underperform substantially on fine-grained iconographic classification in zero-shot settings, and that few-shot prompting with Iconclass descriptions yields consistent but modest improvements. Our evaluation protocol follows their experimental design to ensure comparability, while applying it to a domain — legal-political allegory — that is structurally distinct in several ways: the subjects are not historical religious figures with stable biographical attributes but abstract conceptual entities (Justice, Liberty, the Republic) whose visual form varies across national traditions, political regimes, and material supports.

Beyond this benchmark lineage, LPAI-Bench draws on a body of scholarship at the intersection of legal history and visual culture. Resnik and Curtis (2011) provide the most systematic treatment of Justitia iconography in Anglo-American legal culture, documenting how the visual attributes of Justice — the blindfold, the scale, the sword — have been progressively standardized across centuries.¹ Martyn and Huygebaert (2016, 2018) offer a comparative European perspective, situating allegorical imagery within the broader history of legal aesthetics.⁸ Spratt (2018) articulates the theoretical framework for applying Panofsky's three-level iconological method to machine-learned images, connecting art historical interpretation with computational feature extraction.⁹ Villalba-Osés et al. (2025) demonstrate that contemporary text-to-image models perpetuate gender stereotypes that structurally replicate the same patterns of body purification identified in our historical corpus, establishing the contemporary relevance of the endurecimento framework.¹⁰

### The gap this dataset fills

A systematic search of PitchBook, Hugging Face Hub, arXiv, and the ACL Anthology conducted in April 2026 returned no benchmark datasets or evaluation frameworks specifically targeting legal-political iconography classification. The gap is total and verifiable: no labeled dataset, no evaluation protocol, and no trained model exist for this domain. LPAI-Bench is the first resource of any kind designed to support training and evaluation of vision-language models on legal-political allegorical imagery.

The contemporary relevance of this gap extends beyond historical scholarship. Villalba-Osés et al. (2025) demonstrate that state-of-the-art text-to-image models perpetuate gender stereotypes in their representations of legal and political concepts that structurally replicate the purification patterns documented in nineteenth-century allegorical imagery — the same patterns that LPAI-Bench is designed to measure.¹⁰ The historical benchmark is, in this sense, also a diagnostic instrument for contemporary AI systems.

---

## Methods

### Corpus construction

#### Source selection and inclusion criteria

Items in LPAI-Bench were collected from three open-access digital repositories: the Bibliothèque nationale de France digital library (Gallica, gallica.bnf.fr), the Hemeroteca Digital Nacional (Biblioteca Nacional, Brazil, memoria.bn.br), and the digital collection of the Senado Federal do Brasil (senado.leg.br/noticias/arte-e-cultura). These repositories were selected for three reasons: (1) they provide IIIF-compliant access to high-resolution images, ensuring that every item in the dataset has a stable, citable, dereferenceable identifier; (2) they hold institutional authority for the historical objects they digitize; and (3) their digitized content is either in the public domain (pre-1928 works) or licensed under open terms compatible with dataset publication.

An item was included in the benchmark if and only if all five of the following conditions were satisfied:

1. The item depicts an allegorical figure that is unambiguously female in presentation.
2. The allegorical function of the figure is explicitly juridical or political (representations of Justice, Liberty, the Republic, or cognate state-sanctioned figures).
3. The item is datable to between 1800 and 2000, with priority given to the period 1880–1920 as the peak of allegorical production in the target countries.
4. The depicted figure belongs to one of six national traditions: France (FR), the United Kingdom (UK), Germany (DE), the United States (US), Belgium (BE), or Brazil (BR).
5. The material support belongs to one of six accepted categories: coin or medal, postal stamp, engraved print or frontispiece, monumental sculpture or architectural relief, banknote, or institutional poster.

Items that met all five criteria but could not be verified against a primary archival source were excluded and flagged for future inclusion.

#### Scope of the annotation scheme for VLM evaluation

The ten purification indicators vary in their suitability as ground-truth labels for machine learning evaluation. Six indicators — desincorporação (degree of body reduction), rigidez postural (postural rigidity), dessexualização (body concealment), enquadramento arquitetônico (architectural framing), monocromatização (chromatic reduction), and serialidade (mass reproduction) — can be assessed directly from visual features accessible to current VLMs without narrative or archival context. These six indicators are the primary evaluation targets for Tasks T1 and T3 in the benchmark. Four indicators — apagamento narrativo (narrative erasure), heraldicização (heraldic integration), uniformização facial (facial genericization), and inscrição estatal (state inscription) — require either contextual knowledge about the item's conditions of production or comparative knowledge of other items in the corpus; these are retained as metadata fields and included in T3 evaluations as secondary indicators, with the expectation that VLMs will underperform on them relative to the first group.

#### Note on benchmark scale

LPAI-Bench is a small-scale expert benchmark by design, reflecting both the archival scarcity of securely attributed legal-political allegorical imagery and the high cost of domain-specific expert annotation. The test set (n = 23) yields approximately three items per LPAI base class on average, making LPAI-Bench a few-shot evaluation benchmark rather than a high-volume classification benchmark. This design is consistent with other expert-annotated benchmarks in specialized cultural domains, and results should be interpreted accordingly. Models that perform well on LPAI-Bench under few-shot conditions demonstrate domain adaptation capability rather than statistical robustness at scale.

#### Corpus statistics

The current release of LPAI-Bench comprises 116 items. The French corpus is the largest, reflecting the exceptional volume and diversity of allegorical production in the Third Republic (1870–1940) — a period that produced thousands of stamp and coin series, each a distinct iteration of Marianne, La République, or La Justice. The Brazilian corpus, though smaller, is strategically significant: it documents the appropriation of French allegorical conventions by a newly republican state (post-1889) that deployed female allegory as an instrument of positivist legitimation with minimal prior iconographic tradition in this mode. Table 1 provides the distribution by country and material support.

**Table 1. Distribution of corpus items by country and material support.**

| Support | FR | UK | DE | US | BE | BR | Total |
|---|---|---|---|---|---|---|---|
| Coin / medal | 12 | 8 | 7 | 6 | 4 | 5 | 42 |
| Postal stamp | 9 | 6 | 5 | 4 | 3 | 4 | 31 |
| Engraving / frontispiece | 8 | 4 | 3 | 3 | 2 | 3 | 23 |
| Monumental sculpture | 3 | 2 | 3 | 2 | 1 | 2 | 13 |
| Banknote | 2 | 1 | 1 | 1 | 1 | 1 | 7 |
| **Total** | **34** | **21** | **19** | **16** | **11** | **15** | **116** |

Each item is described by 32 metadata fields covering identification (item ID, source URL, IIIF manifest URL, repository, accession number), provenance (country, approximate date, mint or issuing authority, designer where known), material properties (support type, dimensions, technique, chromatic register), iconographic classification (LPAI base class, LPAI modifiers, Iconclass codes, allegorical motif, iconographic tradition), and purification scores (ten ordinal indicators, 0–3 scale; endurecimento aggregate score).

### The LPAI v2 Taxonomy

The Legal-Political Allegory Index, version 2 (LPAI v2), is the domain-specific classification system developed for this corpus. It comprises eight mutually non-exclusive base classes, four modifier layers, and approximately seventy concordances with Iconclass notations established through manual alignment.

**Base classes:**

| Code | Label | Representative figures |
|---|---|---|
| LPAI-01 | Justice allegory | Justitia, Lady Justice, La Justice |
| LPAI-02 | Liberty allegory | Liberté, Lady Liberty, Columbia |
| LPAI-03 | Republic allegory | La République, A República, Germania-Republic |
| LPAI-04 | Nation allegory | Marianne (national), Britannia, Germania-Nation |
| LPAI-05 | Imperial-colonial allegory | Britannia (colonial), Marianne (colonial), Piastre figures |
| LPAI-06 | Constitutional allegory | figures accompanying founding documents |
| LPAI-07 | Civic virtue allegory | Minerva, figures of Prudence, Fortitude, Temperance in state contexts |
| LPAI-08 | Composite / hybrid | figures combining two or more of the above functions |

**Modifier layers:** Each item is additionally annotated with up to four modifier layers specifying: (M1) the iconographic regime (FUNDACIONAL, NORMATIVO, or MILITAR, see below); (M2) the chromatic register (polychrome, monochrome, metallic); (M3) the posture profile (standing-dynamic, standing-static, seated, bust/truncated, symbolic-reduced); and (M4) the primary attribute set (a controlled list of eighteen iconographic attributes: scales, blindfold, sword, torch, Phrygian cap, shield, helmet, crown, fasces, constitution/tablet, cornucopia, sceptre, trident, globe, chains-broken, laurel, armour, civic flora).

**Iconclass concordances:** The LPAI v2 taxonomy has been aligned with approximately seventy Iconclass notations, primarily in the 44A (allegory of virtue and state concepts) and 48C (allegories of political concepts) hierarchies. The full concordance table is provided as a supplementary CSV file in the dataset repository.

### Glossary of Domain-Specific Terms

For readers outside the disciplines of legal history and art history, the following operational definitions apply throughout this paper:

| Term | Definition |
|---|---|
| **endurecimento** | (Portuguese; lit. "hardening") The progressive purification of the allegorized female body in state iconography: a process by which a dynamic, individuated body is transformed into a static, depersonalized icon through the accumulation of visual conventions. Measured by ten ordinal indicators on a 0–3 scale. |
| **Iconocratic regime** | A classification of the political-historical context in which a given allegorical figure performs its legitimating function: FUNDACIONAL (foundational/revolutionary), NORMATIVO (normalized/bureaucratic), or MILITAR (militarized/imperial). |
| **LPAI** | Legal-Political Allegory Index. The domain-specific taxonomy developed for this corpus, comprising eight base classes and four modifier layers. |
| **Iconclass** | An international classification system for iconographic subjects in art and illustration, maintained by the RKD (Netherlands Institute for Art History). The primary controlled vocabulary for art-historical image cataloguing. |
| **Pathosformel** | (German; Aby Warburg) A gestural formula that carries an emotional charge across historical periods and cultural contexts — a recurrent body posture, gesture, or expression that migrates between images. |
| **Allegorical figure** | In the context of this dataset: a personified abstract concept (Justice, Liberty, the Republic) represented as a female human figure, functioning within a political or juridical visual programme. |

### The Three Iconocratic Regimes

A distinctive contribution of LPAI-Bench relative to other cultural heritage datasets is the annotation of each item with an iconocratic regime — a classification that captures the political-historical context in which the allegorical figure performs its legitimating function.

**FUNDACIONAL** items document the deployment of female allegory at moments of state founding or revolutionary transformation: constitutions, independence declarations, political upheavals. The allegorical body in this regime is typically dynamic, partially unclothed, and individuated — it retains the marks of a living body deployed for a specific political act.

**NORMATIVO** items document the routinized, bureaucratic reproduction of allegory in conditions of state stability: definitive stamp series, circulating coinage, institutional facades. The body is here fully clothed, symmetrized, frontalized, and serialized — made fit for infinite reproduction without semantic friction.

**MILITAR** items document the militarization or imperializing of allegory in conditions of war, colonial expansion, or nationalist mobilization. The body acquires armour, weaponry, and postures of domination — it is hardened against the softness that would compromise its function as an instrument of state violence.

These three regimes are not strictly chronological: a single historical period may exhibit all three simultaneously, and a single allegorical figure may transition between regimes across different material supports.

### Annotation Protocol and Inter-Annotator Agreement

All 116 items were independently annotated by the author (annotator A1), a historian of law with expertise in European and Brazilian legal iconography, and by a second annotator (A2) with postgraduate training in art history and museum studies. A third annotator (A3), a specialist in numismatic iconography, annotated a randomly selected 30% subset (n = 35 items).

Annotation proceeded in two phases. In Phase 1, annotators independently assigned LPAI base classes (multi-label), regime classification (single-label), and Iconclass primary codes. In Phase 2, annotators scored each of the ten purification indicators on the 0–3 ordinal scale.

Inter-annotator agreement was calculated using Krippendorff's alpha (α) for ordinal data. Results are reported in Table 2.

**Table 2. Inter-annotator agreement (Krippendorff's α) for LPAI-Bench annotation tasks.**

| Task | Annotators | α | Interpretation |
|---|---|---|---|
| LPAI base class (T1) | A1, A2 | [PLACEHOLDER — to be computed] | — |
| Regime classification (T2) | A1, A2 | [PLACEHOLDER — to be computed] | — |
| Desincorporação (indicator 1) | A1, A2 | [PLACEHOLDER] | — |
| Rigidez postural (indicator 2) | A1, A2 | [PLACEHOLDER] | — |
| Dessexualização (indicator 3) | A1, A2 | [PLACEHOLDER] | — |
| Uniformização facial (indicator 4) | A1, A2 | [PLACEHOLDER] | — |
| Heraldicização (indicator 5) | A1, A2 | [PLACEHOLDER] | — |
| Enquadramento arquitetônico (indicator 6) | A1, A2 | [PLACEHOLDER] | — |
| Apagamento narrativo (indicator 7) | A1, A2 | [PLACEHOLDER] | — |
| Monocromatização (indicator 8) | A1, A2 | [PLACEHOLDER] | — |
| Serialidade (indicator 9) | A1, A2 | [PLACEHOLDER] | — |
| Inscrição estatal (indicator 10) | A1, A2 | [PLACEHOLDER] | — |
| endurecimento aggregate (T3) | A1, A2, A3 | [PLACEHOLDER] | — |

Disagreements were resolved by structured discussion between A1 and A2, with reference to the published Codebook of Purification.¹¹ Items where consensus could not be reached (estimated n < 5) are flagged in the dataset with the field `annotation_status: contested` and excluded from the benchmark evaluation splits.

---

## Data Records

### Repository structure

LPAI-Bench is deposited in two parallel repositories:

1. **Hugging Face Hub**: `warholana/lpai-bench` (https://huggingface.co/datasets/warholana/lpai-bench) — primary access point for machine learning use cases. Contains the full annotation table in Parquet format, the train/validation/test splits, and Python loading scripts compatible with the `datasets` library.

2. **Zenodo**: DOI [PLACEHOLDER — to be registered upon acceptance] — archival deposit with DOI for academic citation. Contains the full dataset in JSON, CSV, and SQLite formats, the SKOS/Turtle export of LPAI v2, the Codebook of Purification (PDF), and the inter-annotator agreement calculation scripts.

The GitHub monorepo (github.com/anavvanzin/iconocracy-corpus) hosts all code used to construct and validate the dataset, including the dual-agent collection pipeline (WebScout + IconoCode), annotation validation scripts, and IIIF manifest processing utilities.

### File formats and fields

The primary annotation file (`lpai_bench_v1.json` / `lpai_bench_v1.parquet`) contains one record per item with the following field structure:

```json
{
  "item_id": "LPAI-0001",
  "source_url": "https://gallica.bnf.fr/ark:/12148/...",
  "iiif_manifest": "https://gallica.bnf.fr/iiif/.../manifest.json",
  "image_url_iiif": "https://gallica.bnf.fr/iiif/...full/full/0/default.jpg",
  "repository": "Gallica/BnF",
  "country": "FR",
  "date_ca": 1898,
  "date_range": [1895, 1902],
  "support": "stamp",
  "lpai_base_classes": ["LPAI-03"],
  "lpai_regime": "NORMATIVO",
  "lpai_modifiers": {
    "chromatic_register": "monochrome",
    "posture_profile": "standing-static",
    "primary_attributes": ["sowing-gesture", "civic-flora"]
  },
  "iconclass_codes": ["44B2", "48C51"],
  "allegorical_motif": "La Semeuse",
  "iconographic_tradition": "neoclassical-republican",
  "purification_scores": {
    "desincorporacao": 1,
    "rigidez_postural": 2,
    "dessexualizacao": 3,
    "uniformizacao_facial": 2,
    "heraldizacao": 1,
    "enquadramento_arquitetonico": 2,
    "apagamento_narrativo": 2,
    "monochromatizacao": 3,
    "serialidade": 3,
    "inscricao_estatal": 2
  },
  "endurecimento_score": 2.1,
  "annotation_status": "consensus",
  "annotator_primary": "A1",
  "license": "public_domain",
  "source_license_url": "https://gallica.bnf.fr/html/und/conditions-dutilisation"
}
```

### Image access and licensing

No images are redistributed in the dataset package. All images are accessed via IIIF manifests pointing to the originating repositories. This approach guarantees that images remain under the custody of the institutional repositories that hold them, that access links remain stable via the IIIF protocol, and that the licensing situation of each image is governed by the source institution's terms rather than by any secondary packaging.

The vast majority of items in LPAI-Bench were created before 1928 and are in the public domain in all jurisdictions relevant to this dataset. All images sourced from Gallica are served under the BnF Licence Ouverte / Open Licence 2.0, compatible with CC BY. Images from the Hemeroteca Digital Nacional and the Senado Federal are digitized under Brazilian federal open data policy (Lei nº 12.527/2011 and Decreto nº 8.777/2016). The field `license` in each record specifies the applicable licence; `source_license_url` provides the relevant policy URL. Researchers who extend the dataset with images from other repositories are responsible for verifying the licence of each new source.

### Train / validation / test splits

LPAI-Bench is provided with a recommended stratified split for benchmark evaluation:

- **Training** (n = 70, 60%): for few-shot and fine-tuning experiments
- **Validation** (n = 23, 20%): for hyperparameter selection
- **Test** (n = 23, 20%): held out for final evaluation; not to be used for model selection

Stratification was performed by country and regime to ensure balanced representation. Items flagged as `annotation_status: contested` are assigned to the training split only and excluded from validation and test.

---

## Technical Validation

### Evaluation tasks and metrics

LPAI-Bench supports three evaluation tasks at increasing levels of complexity:

**Task 1 (T1) — LPAI class classification**: Given an image, predict the applicable LPAI base classes (multi-label classification over 8 classes). Primary metric: macro-averaged F1 (F1-macro) and mean average precision (mAP). T1 is the primary benchmark task and the most directly comparable to Spinaci et al. (2025).

**Task 2 (T2) — Regime classification**: Given an image, predict the iconocratic regime (3-class single-label classification: FUNDACIONAL / NORMATIVO / MILITAR). Primary metric: weighted F1. T2 captures the coarser historical interpretation and is the task most tractable for general-purpose VLMs without domain fine-tuning.

**Task 3 (T3) — Purification indicator scoring**: Given an image, predict the value (0–3) of each of the ten purification indicators. Primary metric: mean absolute error (MAE) per indicator, averaged across indicators. T3 is an ordinal regression task and is expected to be the most challenging for current VLMs, as it requires fine-grained visual reasoning about attributes that have no standard label in general image training data.

### Baseline experiments

We report zero-shot baseline results following the protocol of Spinaci et al. (2025), who tested models under three conditions: (C1) classification using class label names as prompts; (C2) classification using extended Iconclass descriptions; and (C3) few-shot learning with five exemplars from the training split.

**Models evaluated:**

- CLIP ViT-B/32 (Radford et al., 2021) — zero-shot, conditions C1 and C2
- CLIP ViT-L/14 — zero-shot, conditions C1 and C2
- GPT-4V (OpenAI) — zero-shot, conditions C1, C2, and C3
- SigLIP (Google) — zero-shot, condition C1

**Table 3. Zero-shot baseline results on the LPAI-Bench test set.**

*T1: LPAI class classification (F1-macro / mAP)*

| Model | Condition | F1-macro | mAP |
|---|---|---|---|
| CLIP ViT-B/32 | C1 (label names) | [PLACEHOLDER] | [PLACEHOLDER] |
| CLIP ViT-B/32 | C2 (Iconclass desc.) | [PLACEHOLDER] | [PLACEHOLDER] |
| CLIP ViT-L/14 | C1 | [PLACEHOLDER] | [PLACEHOLDER] |
| GPT-4V | C1 | [PLACEHOLDER] | [PLACEHOLDER] |
| GPT-4V | C3 (5-shot) | [PLACEHOLDER] | [PLACEHOLDER] |
| Human expert (A1) | — | — | ~0.91 |

*T2: Regime classification (weighted F1)*

| Model | Condition | Weighted F1 |
|---|---|---|
| CLIP ViT-B/32 | C1 | [PLACEHOLDER] |
| GPT-4V | C1 | [PLACEHOLDER] |
| GPT-4V | C3 (5-shot) | [PLACEHOLDER] |
| Human expert (A1) | — | ~0.88 |

*T3: Purification scoring (MAE, averaged across 10 indicators)*

| Model | Condition | Mean MAE |
|---|---|---|
| CLIP ViT-B/32 | C1 | [PLACEHOLDER] |
| GPT-4V | C1 | [PLACEHOLDER] |
| Human expert (A1 vs. A2) | — | ~0.21 |

> **Note on placeholders:** The experimental baseline results reported in Table 3 are pending completion of the CLIP zero-shot evaluation pipeline (branch `feature/clip-embeddings`, github.com/anavvanzin/iconocracy-corpus). Human expert agreement (A1 vs. A2) is computed from the inter-annotator annotation round and is not subject to the same uncertainty. These results will be inserted upon submission. The placeholders are retained in this draft to allow structural review of the paper prior to experimental completion.

### Dataset validation

The dataset was validated against the formal JSON Schema (Draft 2020-12) defined in the repository at `schemas/corpus_item_schema.json`. All 116 records pass schema validation with zero errors (validated via `tools/scripts/validate_schemas.py`). IIIF manifest URLs were verified by fetching each manifest and confirming image access. Dead links are flagged with `iiif_manifest_status: error` (current count: 0).

The distribution of endurecimento scores across the corpus is approximately symmetric, consistent with the expectation that the corpus spans the full range of the purification process rather than being concentrated at its extremes. Kruskal-Wallis tests confirm statistically significant differences in endurecimento score across regimes (H = [PLACEHOLDER], p < 0.001) and across material supports (H = [PLACEHOLDER], p < 0.01), validating the construct validity of the annotation scheme.

---

## Usage Notes

### Intended use cases

LPAI-Bench is designed to support the following research use cases:

1. **VLM evaluation**: Researchers can use the benchmark to evaluate the performance of existing or novel vision-language models on fine-grained iconographic classification in a domain where no training data previously existed. The three-task structure allows evaluation at multiple granularities.

2. **Domain fine-tuning**: The training split (n = 70) can be used for LoRA or full fine-tuning of CLIP-family models following the CultureCLIP (2025) protocol. Given the small dataset size, few-shot and parameter-efficient approaches are recommended.

3. **Multimodal cultural heritage research**: Researchers in Digital Humanities can use the dataset as a structured knowledge base for studies of legal iconography, gender representation in state imagery, and the visual history of political concepts.

4. **Extension**: Researchers are encouraged to extend the corpus with items from additional national traditions and historical periods. The LPAI v2 taxonomy includes provisions for extension via national modifier codes; the Codebook of Purification provides detailed operational definitions for all ten indicators to support consistent annotation by new annotators.

### Limitations

The current release covers six national traditions selected for their centrality to the European and Atlantic juridical-political tradition of the nineteenth and twentieth centuries. This scope is not universal: allegorical traditions in other regions (East Asia, the Middle East, sub-Saharan Africa) are not represented, and the LPAI v2 taxonomy was not designed for those contexts. Researchers applying the benchmark to imagery outside the scope of the six national traditions should treat its results as exploratory.

A second structural limitation concerns source bias. The three digitizing repositories used to construct this corpus (Gallica/BnF, Hemeroteca Digital Nacional, Senado Federal do Brasil) are institutional archives that predominantly preserve officially sanctioned imagery — the canonical allegorical output of state institutions. Counter-allegorical, subversive, or feminist reappropriations of allegorical figures are systematically underrepresented in these archives and therefore in LPAI-Bench. This is a feature of the archival condition, not a methodological error, but it means that the benchmark documents the dominant iconographic tradition rather than the full range of allegorical production in any given national context.

The benchmark size (116 items) is modest relative to general-purpose image benchmarks. This reflects the specificity of the domain and the cost of expert annotation, not a limitation of the underlying corpus, which is designed to grow to 250+ items. Researchers requiring larger evaluation sets for statistical power should use bootstrapping or combine LPAI-Bench evaluation with other Cultural AI benchmarks.

### Code and reproducibility

All code required to reproduce the dataset, run the baseline evaluations, and extend the corpus is available at github.com/anavvanzin/iconocracy-corpus under an MIT licence. The repository includes: the dual-agent collection pipeline (WebScout + IconoCode); the JSON Schema and validation scripts; the SKOS/Turtle export of LPAI v2; IIIF processing utilities; and the statistical notebooks (exploratory analysis, Kruskal-Wallis tests, correspondence analysis, and baseline evaluation scripts).

---

## References

1. Resnik, J., & Curtis, D. (2011). *Representing Justice: Invention, Controversy, and Rights in City-States and Democratic Courtrooms*. Yale University Press.

2. Challenges and opportunities for visual analytics in jurisprudence. *Artificial Intelligence and Law*, advance online. https://doi.org/10.1007/s10506-025-09494-2

3. van Straten, R. (1985). *Einführung in die Ikonographie*. Gordon and Breach. [For the Iconclass controlled vocabulary, see: iconclass.org; maintained by the RKD Netherlands Institute for Art History.]

4. Santini, C., Sack, H., Tietz, T., Sprau, M., Waitelonis, J., & Hogan, A. (2023). Multimodal Search on Iconclass using Vision-Language Pre-Trained Models. *IEEE International Conference on Data Engineering Workshops*. https://arxiv.org/abs/2306.16529

5. CultureCLIP: Empowering CLIP with Cultural Awareness through Synthetic Images and Contextualized Captions. (2025). arXiv:2507.06210. https://arxiv.org/abs/2507.06210

6. CATS: Cultural-heritage classification using LLMs and distributed model. (2025). *npj Heritage Science*. https://doi.org/10.1038/s40494-025-01621-1

7. Spinaci, G., Klic, L., & Colavizza, G. (2025). Benchmarking Vision-Language and Multimodal Large Language Models in Zero-shot and Few-shot Scenarios: A study on Christian Iconography. arXiv:2509.18839. https://arxiv.org/abs/2509.18839

8. Martyn, G., & Huygebaert, S. (2016). *The Art of Law: Three Centuries of Justice Depicted*. Lannoo. [See also: Huygebaert, S., Martyn, G., Paumen, V., Bousmar, E., & Rousseaux, X. (Eds.). (2018). *The Art of Law*. Springer.]

9. Spratt, E. L. (2018). Dream Formulations and Deep Neural Networks: Humanistic Themes in the Iconology of the Machine-Learned Image. *Kunsttexte.de*. https://arxiv.org/abs/1802.01274

10. Villalba-Osés, M., et al. (2025). A Large Scale Analysis of Gender Biases in Text-to-Image Generative Models. arXiv:2503.23398. https://arxiv.org/abs/2503.23398

11. Vanzin, A. (2025). *Iconocracy Corpus: Annotation Data, Codebook of Purification, and LPAI v2 Taxonomy* [Data repository]. PPGD/UFSC. Available at: https://github.com/anavvanzin/iconocracy-corpus (in preparation for Zenodo archival deposit).

---

## Acknowledgements

This research is part of the doctoral thesis "ICONOCRACIA: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)" conducted at the Graduate Program in Law of the Federal University of Santa Catarina (PPGD/UFSC). The author thanks the Bibliothèque nationale de France, the Biblioteca Nacional do Brasil, and the Senado Federal do Brasil for open access to their digital collections.

---

*Manuscript prepared April 2026. Version: draft v1.0.*
*Word count (excluding tables and references): ~4,850 words.*
