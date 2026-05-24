# Migrate Atlas Schema Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement data transformation logic to map old "endurecimento" indicators into 3 new bilingual axes: Formalization, Statization, and Idealization for the Hybrid Atlas.

**Architecture:** Pure Python functions in `tools/scripts/migrate_atlas_schema.py` for calculating axes from indicators and adding bilingual labels.

**Tech Stack:** Python 3.11, pytest.

---

### Task 1: Implement Data Transformation Logic

**Files:**
- Create: `tools/scripts/migrate_atlas_schema.py`
- Create: `tests/tools/test_migrate_atlas_schema.py`

- [x] **Step 1: Write the failing test**

```python
# tests/tools/test_migrate_atlas_schema.py
import pytest
from tools.scripts.migrate_atlas_schema import calculate_axes, add_bilingual_labels

def test_calculate_axes():
    # Mocking a record with the 10 original purification indicators
    record = {
        "indicadores": {
            "rigidez_postural": 3, 
            "desincorporação": 2, 
            "monocromatização": 1, 
            "serialidade": 2,
            "heraldicização": 3, 
            "enquadramento_arquitetônico": 2, 
            "inscrição_estatal": 1,
            "dessexualização": 3, 
            "uniformização_facial": 3, 
            "apagamento_narrativo": 3
        }
    }
    axes = calculate_axes(record)
    # Formalization: (3+2+1+2)/4 = 2.0
    # Statization: (3+2+1)/3 = 2.0
    # Idealization: (3+3+3)/3 = 3.0
    assert axes["formalization"] == 2.0
    assert axes["statization"] == 2.0
    assert axes["idealization"] == 3.0

def test_add_bilingual_labels():
    record = {"id": "FR-013"}
    updated = add_bilingual_labels(record)
    assert "labels_en" in updated
    assert "labels_pt" in updated
    assert updated["labels_en"]["axes"] == ["Formalization", "Statization", "Idealization"]
    assert updated["labels_pt"]["axes"] == ["Formalização", "Estatização", "Idealização"]
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest tests/tools/test_migrate_atlas_schema.py -v`
Expected: FAIL with "ModuleNotFoundError" or "ImportError"

- [x] **Step 3: Write minimal implementation**

```python
# tools/scripts/migrate_atlas_schema.py
import json
import sys
import os

def calculate_axes(record):
    ind = record.get("indicadores", {})
    def get_val(key): return int(ind.get(key, 0))
    
    # Mapping:
    # Formalization: rigidez_postural, desincorporação, monocromatização, serialidade
    form = (get_val("rigidez_postural") + get_val("desincorporação") + get_val("monocromatização") + get_val("serialidade")) / 4.0
    
    # Statization: heraldicização, enquadramento_arquitetônico, inscrição_estatal
    stat = (get_val("heraldicização") + get_val("enquadramento_arquitetônico") + get_val("inscrição_estatal")) / 3.0
    
    # Idealization: dessexualização, uniformização_facial, apagamento_narrativo
    ideal = (get_val("dessexualização") + get_val("uniformização_facial") + get_val("apagamento_narrativo")) / 3.0
    
    return {
        "formalization": round(form, 2),
        "statization": round(stat, 2),
        "idealization": round(ideal, 2)
    }

def add_bilingual_labels(record):
    record["labels_en"] = {"axes": ["Formalization", "Statization", "Idealization"]}
    record["labels_pt"] = {"axes": ["Formalização", "Estatização", "Idealização"]}
    return record
```

- [x] **Step 4: Run test to verify it passes**

Run: `pytest tests/tools/test_migrate_atlas_schema.py -v`
Expected: PASS

- [x] **Step 5: Commit**

```bash
git add tests/tools/test_migrate_atlas_schema.py tools/scripts/migrate_atlas_schema.py
git commit -m "feat: add atlas schema transformation logic"
```
