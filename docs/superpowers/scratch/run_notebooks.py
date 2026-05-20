import subprocess
from pathlib import Path

notebooks_dir = Path("/home/ana/Documents/projetos/research/iconocracy-corpus/notebooks")
order = [
    "01_exploratory.ipynb",
    "02_kruskal_wallis.ipynb",
    "03_regression.ipynb",
    "04_correspondence.ipynb",
    "05_temporal.ipynb",
    "06_clustering.ipynb",
    "07_dimensionality.ipynb",
    "08_multidimensional_scoring.ipynb"
]

for nb in order:
    nb_path = notebooks_dir / nb
    if not nb_path.exists():
        print(f"Notebook {nb} does not exist!")
        continue
    print(f"Executing {nb}...")
    res = subprocess.run([
        "conda", "run", "-n", "iconocracy", "jupyter", "nbconvert", "--to", "notebook", "--execute",
        "--inplace", str(nb_path)
    ], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error in {nb}:")
        print(res.stderr)
        break
    else:
        print(f"Finished {nb} successfully.")
