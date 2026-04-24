# ICONOCRACY CORPUS GAP ANALYSIS
# Generated 2026-03-31 by Claude Code agent

**Corpus**: 95 items | **Purification coding**: 0/95 coded (0%)

---

## 1. Summary Statistics

### By Country (core 6)

| Country | N | % |
|---------|---|---|
| FR | 22 | 23% |
| DE | 15 | 16% |
| US | 14 | 15% |
| BR | 10 | 11% |
| UK | 6 | 6% |
| BE | 4 | 4% |
| Other (NL, PT, IT, AT, ES, etc.) | 24 | 25% |

### By Support

| Medium | N | % |
|--------|---|---|
| Gravura/Estampa | 47 | 49% |
| Outro (misc.) | 20 | 21% |
| Pintura/Desenho | 10 | 11% |
| Fotografia | 7 | 7% |
| Cartaz | 4 | 4% |
| Papel-moeda | 4 | 4% |
| Moeda | 2 | 2% |
| Iluminura | 1 | 1% |

### By Regime

| Regime | N | % |
|--------|---|---|
| Fundacional | 44 | 46% |
| Normativo | 42 | 44% |
| Militar | 3 | 3% |
| Unknown | 6 | 6% |

### By Decade (19th-20th c.)

The 1910s peak at 11 items. The 1800s, 1810s, 1840s, 1980s, and 1990s have zero items.

---

## 2. Top 5 Priority Gaps

### GAP 1 -- MILITAR regime has only 3 items (3%)

**CRITICAL.** The entire endurecimento thesis rests on demonstrating progressive purification across fundacional -> normativo -> militar. With only 3 items in the militar category (2 BR Estado Novo, 1 cartaz), no statistical test (Kruskal-Wallis, correspondence analysis) can produce reliable results. Needs at minimum 15-20 items.

### GAP 2 -- No militar items for FR, DE, US, UK, or BE

The endurecimento hypothesis requires showing the pattern holds across national traditions. Currently all 3 militar items are Brazilian (Estado Novo). Vichy France, Nazi Germany (post-1933), fascist Italy, and wartime US/UK propaganda are completely absent.

### GAP 3 -- Moeda and papel-moeda critically underrepresented (2 coins, 4 banknotes)

These are the most "official" state media -- serial, mass-circulated, legally mandated imagery. Zero coins exist for fundacional or normativo regime. Zero banknotes for fundacional.

### GAP 4 -- UK and BE thin across all dimensions

UK has 6 items, BE has 4, and both have zero in most media categories. Britannia (coins, stamps, monuments) and Belgium (constitutional imagery, Congo colonial) are essential comparative cases but lack depth for statistical analysis.

### GAP 5 -- Post-1930 period nearly empty

8 items for 1930s-1970s, zero for 1980s-1990s. The thesis covers 19th-20th centuries but the second half is barely represented.

---

## 3. Recommendations for Corpus-Scout Searches

### Immediate priority (militar regime):

1. **Vichy France**: Marianne imagery under Petain (replaced by Francisque/Travail-Famille-Patrie)
2. **Nazi Germany / Third Reich**: Germania after 1933, Reichsmark coins, propaganda posters
3. **Fascist Italy**: Italia turrita under Mussolini, coins, stamps
4. **US WWII**: Columbia/Liberty in war bonds, propaganda posters
5. **UK WWII**: Britannia in war savings, propaganda
6. **Portugal Estado Novo**: Salazar-era coinage, stamps

### Monetary media (coins + banknotes):

7. **FR coins**: Semeuse (SCOUT-116), Ceres 5F (SCOUT-094), Marianne-Coq (SCOUT-312)
8. **US coins**: Seated Liberty (SCOUT-093), Standing Liberty (SCOUT-314), Morgan Dollar (SCOUT-315)
9. **UK coins**: Britannia penny (SCOUT-313, SCOUT-108, SCOUT-310)
10. **BR coins**: 500 Reis Republica (SCOUT-316), Cruzeiro notes (SCOUT-109)
11. **DE banknotes**: Reichsbanknotes (SCOUT-096, SCOUT-097, SCOUT-110)

### UK/BE depth:

12. **UK stamps**: Mulready (SCOUT-309), Britannia definitives
13. **BE constitutional**: Constitution illustree (SCOUT-102), independence coinage (SCOUT-099, SCOUT-037)

---

## 4. Statistical Sufficiency Assessment

**Current state: INSUFFICIENT for the thesis design.**

- **Kruskal-Wallis test** (comparing purification scores across 3 regimes): Requires ~15 items per group. Fundacional (44) and normativo (42) are adequate, but **militar (3) makes the test impossible**.

- **Correspondence analysis** (country x regime x medium): Requires cells with expected counts >= 5. The current cross-tables have many zero cells (18 empty in the 6x7 country-medium table). The analysis would collapse into sparsity artifacts.

- **Minimum viable corpus**: ~120-150 items with at least 20 in militar regime. Needs 30-55 additional items, heavily weighted toward militar and coins/banknotes/stamps.

- **Purification coding**: 0/95 items coded on 10 ordinal indicators. This is the prerequisite for all quantitative analysis.

### Recommended action sequence:

1. Incorporate ~30 SCOUT candidates already identified in `vault/candidatos/`
2. Run targeted scout campaigns for militar-regime imagery
3. Begin purification coding on existing 95 items (`code_purification.py` is ready)
4. Re-assess at ~130 items with coding complete
