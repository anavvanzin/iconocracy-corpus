import json
from pathlib import Path

nb_path = Path("/home/ana/Documents/projetos/research/iconocracy-corpus/notebooks/02_kruskal_wallis.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb.get("cells", []):
    if cell.get("cell_type") == "code":
        source = cell.get("source", [])
        source_str = "".join(source)
        if "sp.posthoc_dunn(df," in source_str:
            print("Found cell to modify:")
            new_source = []
            for line in source:
                if "sig_indicators = [r['indicator']" in line:
                    new_source.append("df_clean = df.dropna(subset=['regime_iconocratico'])\n")
                line_replaced = line.replace("sp.posthoc_dunn(df,", "sp.posthoc_dunn(df_clean,")
                new_source.append(line_replaced)
            cell["source"] = new_source
            print("Modified cell source successfully.")

with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
    f.write("\n")
