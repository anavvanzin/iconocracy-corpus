# Thread Analyzer — ICONOCRACIA Atlas Warburg

Consume your Warburg panel exports and produce relational analysis grounded in the iconocratic-relations taxonomy.

## Quick start

```bash
# Test with synthetic threads (no real data needed)
python3 analyze_threads.py corpus.json --demo

# Real run — after exporting panels from the Warburg canvas
python3 analyze_threads.py corpus.json painel-1.json painel-2.json painel-3.json
```

## How to feed it real data

1. Open the Warburg canvas (the standalone preview, or the companion port).
2. For each of the 8 panels, draw threads between placements using the "⤳ Fio" mode.
3. Click "↓ Export" on each panel → downloads `iconocracia-painel-N-name.json`.
4. Put all panel JSONs in this directory.
5. Run:
   ```bash
   python3 analyze_threads.py corpus.json iconocracia-painel-*.json
   ```

## Outputs

- `thread-analysis-report.md` — human-readable report with cluster analysis, regime breakdown, relation distribution, motif co-occurrences
- `thread-analysis.json` — structured data with every thread classified, all metrics
- `thread-graph.svg` — network visualization (X = year, Y = regime, color = relation type, node size = degree)

## What gets analyzed

For each thread (A ↔ B), the analyzer:

1. Resolves A and B into full corpus entries
2. Computes pair-level features: country, regime, motif overlap, score delta, pathosformel keywords
3. Assigns a **primary relation** from the 15-type taxonomy with a confidence score
4. Aggregates across all threads to produce regime/relation matrices

The 15 relation types correspond to the taxonomy document `iconocratic-relations-taxonomy.md` and cover:

- **Genealogical** (Nachleben, Mimesis, Genealogy, Serialization)
- **Structural** (Translatio, Concretization, Gendered-pair)
- **Tensional** (Inversion, Satirization, Contradiction)
- **Transitional** (Martialization, Demilitarization, Endurecimento progressivo)
- **Synchronic** (Co-presence, Co-presence institucional)

## Refining the taxonomy

The v0.1 taxonomy is a starting point. To refine to v1.0:

1. Draw threads in the Warburg canvas while explicitly labeling them in the panel essay (e.g., "Fio FR-013↔FR-018: martialização").
2. Run the analyzer.
3. Compare your manual labels against the analyzer's classification.
4. Where they disagree by >30%, adjust the classifier rules in `classify_relation()`.

The point is *not* that the analyzer is right — the point is to surface where your intuitive labels and the automatic taxonomy diverge, and to use that divergence as material for the methodology section.
