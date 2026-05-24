# tests/tools/test_migrate_atlas_schema.py
import pytest
from tools.scripts.migrate_atlas_schema import calculate_axes, add_bilingual_labels

def test_calculate_axes():
    # Mocking a record with the 10 original purification indicators using the actual schema
    record = {
        "purificacao": {
            "rigidez_postural": 3, 
            "desincorporacao": 2, 
            "monocromatizacao": 1, 
            "serialidade": 2,
            "heraldizacao": 3, 
            "enquadramento_arquitetonico": 2, 
            "inscricao_estatal": 1,
            "dessexualizacao": 3, 
            "uniformizacao_facial": 3, 
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
