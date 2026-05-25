# tools/scripts/migrate_atlas_schema.py

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
