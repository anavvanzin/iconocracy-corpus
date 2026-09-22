# Prompt Codebook — Elicit (Scale Plan)

**Projeto:** ICONOCRACIA — "Moedas e Selos como Micro-Estado"
**Data:** 2026-06-26
**Plano Elicit:** Scale (extração de dados, revisão sistemática, exportação CSV/BibTeX)

---

## Prompt 1 — Referências para o artigo (prioridade máxima)

**ID:** `MICRO-REF-001`
**Tipo:** Discovery + extração
**Exportar como:** BibTeX + CSV com colunas: author, year, title, journal, abstract, engages_gender, engages_materiality

```
Find papers and books that discuss the relationship between 
material support (coins, stamps, banknotes) and gendered state 
allegory in the 19th-20th centuries. I need:

1. Studies on numismatic iconography AND gender/feminist analysis
2. Studies on postal stamp design AND state power/imperialism
3. Comparative work on architectural vs. miniaturized state imagery
4. Any paper that uses the concept of "scale" to analyze 
   political iconography

Exclude: purely economic numismatics, stamp collecting catalogs, 
technical coin grading literature.

For each result, extract: full citation (ABNT), abstract, 
key argument, and whether it engages with gender analysis.

My thesis argues that miniaturization (coins/stamps) preserves 
the female allegorical body while monumentalization (architecture) 
purifies it. I need literature that supports OR challenges this.
```

---

## Prompt 2 — Verificação do Estado da Arte (lacunas)

**ID:** `MICRO-REF-002`
**Tipo:** Systematic review + gap analysis
**Exportar como:** CSV com colunas: author, year, title, addresses_gender [y/n], addresses_materiality [y/n], addresses_scale [y/n], non_european [y/n]

```
I'm writing an article on legal visual culture and material supports 
of state power. Search for recent papers (2020-2026) on:

1. "Legal material culture" OR "visual legal studies" OR 
   "law and the image" OR "iconography of law"
2. "Architecture and law" OR "courthouse iconography" OR 
   "legal emblems architecture"
3. "Gender and numismatics" OR "feminist philately" OR 
   "women on stamps" OR "gendered currency"

For each paper, indicate whether it addresses:
- Gender/feminist analysis [yes/no]
- Materiality of the support [yes/no]  
- Scale or miniaturization [yes/no]
- Non-European perspectives [yes/no]

I need to identify gaps: is anyone else arguing that 
SCALE determines how the state treats the female body?
```

---

## Prompt 3 — Extração para Referências (confirmação de citações)

**ID:** `MICRO-REF-003`
**Tipo:** Verification + extraction
**Exportar como:** BibTeX (confirmado)

```
I need to verify and extract the following references in ABNT NBR 6023:2025 format.
For each, confirm the correct edition, publisher, and page numbers:

1. GOODRICH, Peter. Legal Emblems and the Art of Law: obiter depicta 
   as the vision of governance. Cambridge: Cambridge University Press, 2014.

2. PATEMAN, Carole. The Sexual Contract. Stanford: Stanford University Press, 1988.

3. BELTING, Hans. Likeness and Presence: a history of the image before 
   the era of art. Chicago: University of Chicago Press, 1994.

4. APPADURAI, Arjun (ed.). The Social Life of Things: commodities in 
   cultural perspective. Cambridge: Cambridge University Press, 1986.

5. MITCHELL, W. J. T. Picture Theory: essays on verbal and visual 
   representation. Chicago: University of Chicago Press, 1994.

6. HUYGEBAERT, Stefan. "The Paternalistic Visual Program of the 
   Palais de Justice of Brussels." In: MARTYN, Georges (org.). 
   The Art of Law. Bruges: Die Keure, 2019.

7. PANOFSKY, Erwin. Studies in Iconology. New York: Harper & Row, 1939.
   AND: Significado nas Artes Visuais. São Paulo: Perspectiva, 2014.

8. WARNER, Marina. Monuments and Maidens: the allegory of the 
   female form. London: Weidenfeld & Nicolson, 1985.

For each: confirm edition year, publisher city, and any co-authors 
I may have missed. Alert me to any retractions or corrections.
```

---

## Prompt 4 — Literatura complementar (expansão)

**ID:** `MICRO-REF-004`
**Tipo:** Discovery + conceptual expansion
**Exportar como:** BibTeX + abstracts

```
My article uses the concept of "optical regime" inspired by 
Belting (Bild/Medium/Betrachter) and Mitchell (Picture Theory). 
Find papers that:

1. Apply Belting's triad (image/medium/observer) to political 
   or state imagery (not just religious art)
2. Apply Appadurai's "social life of things" to state-produced 
   objects (coins, stamps, passports, official documents)
3. Discuss the concept of "scale" as a political operator 
   in visual culture (not just architecture or urbanism)
4. Analyze overprinted stamps as evidence of regime change 
   (e.g., Germania stamps through Weimar, Saar, Danzig)
5. Connect Pateman's sexual contract to visual/material culture 
   (not just political theory)

Return papers with abstracts and full citations in ABNT format.
Prioritize: available as PDF, published 2015-2026, in English, 
French, Portuguese, or Spanish.
```

---

## Ordem de execução recomendada

1. **Prompt 3** primeiro (rápido, verificação de citações existentes)
2. **Prompt 1** (descoberta do núcleo bibliográfico)
3. **Prompt 2** (mapeamento de lacunas para a seção de originalidade)
4. **Prompt 4** (expansão conceitual, pode ser assíncrono)
