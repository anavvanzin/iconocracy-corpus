# Manual de Qualidade e Governança do Dataset ICONOCRACY

Este manual estabelece as rotinas, ferramentas e comandos para **curadoria, auditoria e elevação de qualidade** do dataset da tese (*`iconocracy-corpus`* / *`iconocracia-cv`*), segundo a abordagem de **Data-Centric AI (DCAI)**.

---

## 1. Arquitetura da Informação do Dataset

O corpus da tese é estruturado em quatro camadas encadeadas:

| Camada | Arquivo / Caminho | Função |
| :--- | :--- | :--- |
| **Ledger Operacional (SSoT)** | `data/processed/records.jsonl` | Registro canônico de todos os itens e metadados. |
| **Export Público** | `corpus/corpus-data.json` | Export gerado automaticamente para consumo no site/API. |
| **Ledger de Endurecimento** | `data/processed/purification.jsonl` | Registros contendo os 10 indicadores e o `endurecimento_score`. |
| **Acervo de Imagens** | `gallery/` ou Google Drive | Imagens e digitalizações associadas a cada registro. |

---

## 2. Ferramentas Instaladas no Ambiente (`conda activate iconocracy`)

O ambiente Python `iconocracy` (`/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python`) conta com as seguintes ferramentas prontas:

* **`cleanlab`**: Detecção de ruído e inconsistências estocásticas nos rótulos/indicadores.
* **`fiftyone`**: Exploração gráfica multimodal, projeção de embeddings CLIP/DINOv2 e inspeção de amostras.
* **`imagededup` / `fastdup`**: Identificação rápida de gravuras/digitalizações duplicadas.
* **`krippendorff`**: Cálculo do Alpha de Krippendorff ($\alpha$) para concordância inter-anotadores (Humano vs VLM).

---

## 3. Comandos de Operação e Auditoria

### 3.1. Execução da Auditoria Geral Integrada

Para rodar a varredura completa de integridade (Schema + Zeros + Dedup Visual + Cleanlab):

```bash
conda activate iconocracy
python tools/scripts/audit_dataset.py --images-dir gallery
```

---

### 3.2. Explorando o Dataset Graficamente com FiftyOne

O **FiftyOne** abre uma interface no navegador para navegar visualmente pelas imagens e filtrar anotações:

```python
import fiftyone as fo

# Carregar imagens da pasta gallery
dataset = fo.Dataset.from_dir(
    dataset_dir="gallery",
    dataset_type=fo.types.ImageDirectory,
    name="iconocracy-gallery"
)

# Lançar app gráfico no navegador
session = fo.launch_app(dataset)
```

---

### 3.3. Detectando Duplicatas Visuais com imagededup

Para encontrar imagens idênticas ou ligeiramente cortadas/espelhadas no acervo:

```python
from imagededup.methods import PHash

phasher = PHash()
# Gerar hashes e identificar duplicatas
duplicates = phasher.find_duplicates(image_dir="gallery", max_distance_threshold=10)

# Exibir imagens com potenciais cópias
for img, dups in duplicates.items():
    if dups:
        print(f"Original: {img} -> Duplicatas: {dups}")
```

---

### 3.4. Auditoria de Inconsistências de Codificação com Cleanlab

Para auditar os 10 indicadores de endurecimento e identificar itens cuja pontuação destoa do padrão visual/conceitual:

```python
import numpy as np
import cleanlab
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict

# X = Matriz (N_amostras, 10_indicadores)
# y = Vetor de endurecimento_score (0-3)
clf = RandomForestClassifier(n_estimators=50, random_state=42)
pred_probs = cross_val_predict(clf, X, y, cv=3, method="predict_proba")

# Encontrar potenciais erros de rotulagem
label_issues = cleanlab.filter.find_label_issues(labels=y, pred_probs=pred_probs)
```

---

### 3.5. Calculando a Concordância Inter-Anotadores (IRR)

Para medir a consistência conceitual entre a codificação humana e a codificação sintética de LLMs/VLMs:

```bash
python tools/scripts/compute_irr.py
```

---

## 4. Regras de Ouro de Governança dos Dados

1. **Pruning de Registros Zeros**: Itens com todos os 10 indicadores iguais a `0` devem ser revisados ou expurgados do export público via `python tools/scripts/records_to_corpus.py`.
2. **Imutabilidade da SSoT Local**: Nunca edite `corpus/corpus-data.json` manualmente. Todas as edições são feitas em `data/processed/records.jsonl` e propagadas via script.
3. **Validação de Schema Pré-Commit**: Todo commit na estrutura de dados deve passar primeiro por:
   ```bash
   python tools/scripts/validate_schemas.py
   ```
4. **Publicação HuggingFace**: Releases para o HuggingFace (`warholana/iconocracy-corpus`) são geradas exclusivamente via:
   ```bash
   python tools/scripts/build_hf_release.py
   ```
