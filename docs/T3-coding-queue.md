# T3 — IconoCode Coding Queue

**Status as of 2026-04-19:** 19 items in `corpus/corpus-data.json` lack purification coding (indicadores, endurecimento_score, coded_by, coded_at, panofsky — all null).

**T3a recovery pass:** 0 of 19 recoverable from vault. All 19 have vault notes matched by URL, but none contain `## IconoCode Analysis` sections. The purification coding has never been written anywhere; it must be produced from scratch for each item.

**Baseline tests:** 156 passed, 165/165 valid against master-record schema.

---

## Coding queue — 19 items

Each item below needs:
1. 3-level Panofsky analysis (pré-iconográfico, iconográfico, iconológico)
2. 10 purification indicators scored 0–4 (desincorporação, rigidez postural, dessexualização, uniformização facial, heraldização, enquadramento arquitetônico, apagamento narrativo, monocromatização, serialidade, inscrição estatal)
3. Regime classification (fundacional | normativo | militar | contra-alegoria)
4. `coded_by` + `coded_at` metadata

| ID | Support | Country | Title | Vault note |
|----|---------|---------|-------|------------|
| BE-5F-LEOPOLD-1832 | moeda | Belgium | 5 Francs — Léopold I (founding coin of Belgium) | [SCOUT-099](../vault/candidatos/SCOUT-099%205%20Francs%20Leopold%20I%20Belgium.md) |
| BE-CONGO-100F-1912 | papel-moeda | Belgium | 100 Francs Banque du Congo Belge — Allegory of Europe | [SCOUT-112](../vault/candidatos/SCOUT-112%20100%20Francs%20Belgian%20Congo%20banknote%201912.md) |
| BE-CONGO-MON-1921 | monumento/escultura | Belgium | Monument aux Pionniers Belges au Congo | [SCOUT-113](../vault/candidatos/SCOUT-113%20Monument%20Belgian%20Pioneers%20Congo%20Brussels.md) |
| BR-1000R-1906 | moeda | Brazil | 1000 Réis — Efígie da República (1906–1912) | [SCOUT-119](../vault/candidatos/SCOUT-119%20Efígie%20da%20República%201000%20Réis%20Brasil.md) |
| BR-1CR-1970 | papel-moeda | Brazil | 1 Cruzeiro — Efígie da República (2ª edição) | [SCOUT-109](../vault/candidatos/SCOUT-109%201%20Cruzeiro%20banknote%20Efigie%20Republica%201970.md) |
| BR-50CR-1965 | moeda | Brazil | 50 Cruzeiros — Efígie da República (Tônia Carreiro) | [SCOUT-103](../vault/candidatos/SCOUT-103%2050%20Cruzeiros%20Efigie%20da%20Republica%201965.md) |
| DE-1000M-1910 | papel-moeda | Germany | 1000 Mark Reichsbanknote — allegorical figures | [SCOUT-097](../vault/candidatos/SCOUT-097%201000%20Mark%20Reichsbanknote.md) |
| DE-100M-1908 | papel-moeda | Germany | 100 Mark Reichsbanknote — Germania seated | [SCOUT-096](../vault/candidatos/SCOUT-096%20100%20Mark%20Reichsbanknote%20Germania.md) |
| DE-50M-1919 | papel-moeda | Germany | 50 Mark Reichsbanknote (24 Jun 1919) — última imperial / primeira Weimar | [SCOUT-110](../vault/candidatos/SCOUT-110%2050%20Mark%20Reichsbanknote%201919%20last%20imperial.md) |
| FR-ASSIGNAT-1792 | papel-moeda | France | Assignat de 400 livres (an I da República) | [SCOUT-100](../vault/candidatos/SCOUT-100%20Assignat%20400%20livres%201792.md) |
| FR-CERES-5F-1849 | moeda | France | 5 Francs (Cérès, 2e République) | [SCOUT-094](../vault/candidatos/SCOUT-094%205%20Francs%20Ceres%202e%20Republique.md) |
| UK-FLORIN-1902 | moeda | United Kingdom | 1 Florin — Britannia Standing on Ship Prow (Edward VII) | [SCOUT-118](../vault/candidatos/SCOUT-118%20Britannia%20Florin%20Edward%20VII.md) |
| UK-HALFPENNY-1695 | moeda | United Kingdom | ½ Penny — William III / Britannia seated (earliest coin) | [SCOUT-108](../vault/candidatos/SCOUT-108%20Halfpenny%20William%20III%20Britannia%201695.md) |
| UK-PENNY-1895 | moeda | United Kingdom | 1 Penny — Victoria Veiled Head / Britannia Seated | [SCOUT-NC-02](../vault/candidatos/SCOUT-NC-02%201%20Penny%20Victoria%20Britannia%20dual%20body.md) ⚠️ NC prefix |
| UK-PENNY-1912 | moeda | United Kingdom | 1 Penny — Britannia Seated, Helmeted (George V) | [SCOUT-124](../vault/candidatos/SCOUT-124%20George%20V%20Penny%20Britannia%201912.md) |
| US-BANNER-1861 | estampa/gravura | United States | Hail! Glorious Banner of Our Land — Columbia (Civil War) | [SCOUT-363](../vault/candidatos/SCOUT-363%20Hail!%20Glorious%20banner%20of%20our%20land%20Respectfully%20inscribed%20to.md) |
| US-EDUC-1896-01 | papel-moeda | United States | $1 Silver Certificate 'Educational Series' — History Instructing Youth | [SCOUT-101](../vault/candidatos/SCOUT-101%201%20Dollar%20Educational%20Series%201896.md) |
| US-NAST-1864 | estampa/gravura | United States | The Blessings of Victory — Liberty + Columbia (Thomas Nast) | [SCOUT-364](../vault/candidatos/SCOUT-364%20The%20blessings%20of%20victory.md) |
| US-SEATED-1840 | moeda | United States | $1 'Seated Liberty' (without motto) | [SCOUT-093](../vault/candidatos/SCOUT-093%20Seated%20Liberty%20Dollar%20US.md) |

Regime distribution: **9 normativo, 6 fundacional, 4 militar**.

---

## Open questions before coding

1. **UK-PENNY-1895 → SCOUT-NC-02** — `NC-` prefix suggests negative-control. Confirm the vault note is the intended target before coding, or re-link.
2. **Image access** — SSD `/Volumes/ICONOCRACIA/` is not mounted as of this audit. Before the coding session, verify images are accessible (local SSD mount OR Google Drive) for the 19 items.
3. **Coding pipeline choice** — two routes exist:
   - **(A) Vault-first:** code into vault notes under a `## IconoCode Analysis` section, then run `tools/scripts/iconocode_to_corpus.py --write` to merge. Leaves an auditable trail in research notes.
   - **(B) Direct-to-corpus:** code straight into `corpus-data.json` fields. Faster; loses the vault research trail.
   Recommendation: **(A)** — preserves methodology transparency for banca.

## Suggested coding session structure (supervised)

- Per item: ~15–25 min (image review → Panofsky 3 levels → 10 indicators → regime)
- 19 items × ~20 min = **~6.3 hours**. Split into 3 sessions of ~6–7 items each by country cluster (BE+DE / BR+FR / UK+US).
- Use `iconocode-batch` skill for mechanical runs; human-review each before merge.
- After coding: run `iconocode_to_corpus.py --write` and verify count drops from 19 → 0.

## Exit criterion

`python -c "import json; d=json.load(open('corpus/corpus-data.json')); print(sum(1 for i in d if not i.get('indicadores')))"` returns **0**.

Then T3 closes.
