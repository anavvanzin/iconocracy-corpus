# MONK A: The Archivist's Case for Corpus Expansion

## The Fundamental Problem: 165 Items Is a Pilot Study, Not a Dissertation

You have 165 items in your operational ledger. I will say this without hedging: **this is insufficient**. Not insufficient for a conference paper. Not insufficient for a chapter. Insufficient for a doctoral thesis claiming to map "female allegory in the history of legal culture (19th–20th c.)" across six countries, nine supports, and three iconographic regimes.

Valérie Hayaert published *Lady Justice: An Anatomy of Allegory* in 2023. She did depth. Beautiful depth. Close readings of images across centuries. And you know what she did NOT do? She did not build a systematic, comparative, transnational corpus with quantitative coverage. She wrote a monograph. You are writing a digital humanities dissertation. These are different genres with different evidentiary requirements.

## What Is at Stake: Representativeness

The first question any competent committee member will ask: "Is this a convenience sample?" If you have 165 items concentrated in 1880–1920, drawn primarily from Numista, Colnect, and Gallica's IIIF-enabled collections, the answer is yes. You have sampled what was easy to digitize. You have not sampled what was historically significant.

To claim that "endurecimento militar" correlates with regime type, you need sufficient statistical power. With 165 items distributed across six countries, three regimes, and multiple supports, you are running analyses on cells of 5–10 items. This is fragile. A single coding disagreement, a single disputed date, a single reattribution — and your correlation evaporates.

The methodological literature in digital humanities is clear: corpus-based claims require either comprehensive coverage (the "total archive" ideal) or explicit sampling strategies with documented coverage estimates (Bode 2018). You have neither. You have a convenience sample dressed in JSON.

## The Pipeline Is Built for Scale

Here is what your user has already constructed: a dual-agent pipeline (WebScout → IconoCode) that automatically populates `records.jsonl` with structured metadata, Iconclass codes, and regime classifications. The marginal cost of adding a new item — once WebScout locates it — is minutes, not hours.

The marginal cost of deepening coding on existing items? That requires:
- Re-expertise: re-viewing images with new analytical frameworks
- Re-judgment: applying new purification dimensions that may not have existed when items were first coded
- Re-validation: checking consistency across time, across coders
- Potential drift: earlier codings may reflect different implicit standards

The IconoCode/WebScout pipeline is DESIGNED for breadth. It assumes items flow through, get coded, get logged, support quantitative claims. It does not assume hermeneutic lingering.

## The "Inedit Material" Is Archival Gold, Not Distraction

Your user mentioned "inedit material for legal history." This is not a detour. This is the CONTRIBUTION. In legal history, archival discovery IS originality. Stefan Huygebaert's work on Belgian fin-de-siècle legal iconography — the Ghent dissertation that informs your framework — succeeds because it finds and analyzes UNDEREXPLORED MATERIAL.

But finding this material requires SEARCHING. It requires executing the 16 campanhas your user has already mapped. It requires looking beyond the IIIF-enabled, already-digitized, conveniently accessible collections. It requires:

- **Campanha 11**: Frontispícios de códigos e constituições — many unphotographed, unstudied
- **Campanha 12**: Papel-moeda colonial — scattered across institutional collections, often uncatalogued
- **Campanha 15**: Suportes estatais SEM alegoria feminina — the negative cases that prove the rule
- **Campanha 16**: Auditoria de lacunas — systematic mapping of what is MISSING

These are not distractions. These are the work. And they require CORPUS EXPANSION, not deeper coding of what you already have.

## The Competitor Analysis: Hayaert as Cautionary Tale

Hayaert did Lady Justice across centuries. She is exhaustive on the IMAGE of Justitia. But she is not comparative across regimes. She does not ask: does the French Marianne encode different juridical assumptions than the British Britannia? She does not quantify. She does not test.

Your user's dissertation, positioned correctly, fills this gap. But only if the corpus SUPPORTS comparative quantification. 165 items does not.

## The Risk of Depth-First

If you spend six months deepening purification coding on 165 items, you produce:
- A very detailed description of a convenience sample
- Beautiful, thick descriptions that cannot generalize
- Chapters that read like catalogue raisonné entries, not historical arguments
- A dissertation vulnerable to the critique: "interesting, but is this representative?"

The committee will not be impressed by your inter-rater reliability scores if your sample is demonstrably biased toward accessible, digitized, European collections.

## The Path Forward: Execute the Campanhas

Your user has mapped 16 campanhas. This is the work plan. Execute them:
1. **Campanha 1**: Brasil, regime fundacional — fill the Brazilian gap (you likely underrepresent BR)
2. **Campanha 5**: EUA, Columbia/Justice comparison — the US is undercoded in your current ledger
3. **Campanha 9**: Moedas, progressão morfológica — Numista is your friend, use it
4. **Campanha 12**: Papel-moeda colonial — the "inedit" material likely lives here
5. **Campanha 16**: Auditoria de lacunas — systematic coverage analysis

Target: 400–500 items. This gives you 25–30 items per major country-regime cell. This supports statistical claims. This supports comparative argument.

## Conclusion: Breadth Is the Only Path

Your user has built the infrastructure. The IconoCode pipeline works. WebScout searches effectively. The ledger schema is sound. Now EXECUTE. Scale the corpus. Find the "inedit material" through systematic search, not hopeful browsing. Build the 400-item foundation that supports the claims you want to make about "endurecimento," "regime iconocrático," and the "Contrato Sexual Visual."

Depth is a luxury for those with coverage. You do not have coverage. Expand the archive. This is the only path.

---
*The Archivist believes this fully. There is no hedging. Breadth is the way.*
