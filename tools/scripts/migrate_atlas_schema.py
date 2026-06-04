# tools/scripts/migrate_atlas_schema.py
import json
import sys
import os

def calculate_axes(record):
    ind = record.get("indicadores") or record.get("purificacao") or {}
    def get_val(key): return int(ind.get(key, 0))
    
    # Mapping:
    # Formalization: rigidez_postural, desincorporacao, monocromatizacao, serialidade
    form = (get_val("rigidez_postural") + get_val("desincorporacao") + get_val("monocromatizacao") + get_val("serialidade")) / 4.0
    
    # Statization: heraldizacao, enquadramento_arquitetonico, inscricao_estatal
    stat = (get_val("heraldizacao") + get_val("enquadramento_arquitetonico") + get_val("inscricao_estatal")) / 3.0
    
    # Idealization: dessexualizacao, uniformizacao_facial, apagamento_narrativo
    ideal = (get_val("dessexualizacao") + get_val("uniformizacao_facial") + get_val("apagamento_narrativo")) / 3.0
    
    return {
        "formalization": round(form, 2),
        "statization": round(stat, 2),
        "idealization": round(ideal, 2)
    }

def add_bilingual_labels(record):
    record["labels_en"] = {"axes": ["Formalization", "Statization", "Idealization"]}
    record["labels_pt"] = {"axes": ["Formalização", "Estatização", "Idealização"]}
    return record
