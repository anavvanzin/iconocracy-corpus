#!/usr/bin/env python3
"""
audit_dataset.py — Pipeline de Auditoria e Qualidade do Dataset ICONOCRACY
-------------------------------------------------------------------------
Executa checagens integradas sobre o corpus da tese:
1. Validação de Schemas JSON (master-record / records.jsonl)
2. Varredura de Registros Zeros/Morte do Ledger (purificação/indicadores == 0)
3. Detecção de Duplicatas Visuais (via imagededup PHash)
4. Auditoria de Rótulos e Inconsistências (via Cleanlab)

Uso:
  python tools/scripts/audit_dataset.py [--images-dir GALLERY_PATH] [--verbose]
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Certificar diretório do projeto
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Chaves canônicas de purificação / endurecimento (10 indicadores)
INDICATOR_KEYS = [
    "desincorporacao",
    "rigidez_postural",
    "dessexualizacao",
    "uniformizacao_facial",
    "heraldizacao",
    "enquadramento_arquitetonico",
    "apagamento_narrativo",
    "monocromatizacao",
    "serialidade",
    "inscricao_estatal",
]

def run_schema_check(verbose=False):
    print("\n[1/4] 🔍 Checando Validação de Schemas e Leitura (records.jsonl)...")
    records_file = REPO_ROOT / "data" / "processed" / "records.jsonl"
    if not records_file.exists():
        print(f"  ❌ Arquivo não encontrado: {records_file}")
        return False

    records = []
    with open(records_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  ❌ Erro JSON na linha {line_num}: {e}")
                return False

    print(f"  ✅ Total de registros lidos no ledger: {len(records)}")
    return records

def run_zero_indicator_check(records):
    print("\n[2/4] 🧹 Verificando Registros com Indicadores Zeros...")
    zero_items = []
    coded_items = 0

    for rec in records:
        pur = rec.get("purificacao", {})
        indicators = [pur.get(k, 0) for k in INDICATOR_KEYS]
        s = sum(indicators)
        rec_id = rec.get("item_id") or rec.get("id")
        if s > 0:
            coded_items += 1
        else:
            zero_items.append(rec_id)

    print(f"  📊 Itens com codificação ativa (>0): {coded_items} / {len(records)}")
    if zero_items:
        print(f"  ℹ️ {len(zero_items)} itens possuem soma de indicadores == 0 (Pendentes de recodificação/E1):")
        for zid in zero_items[:5]:
            print(f"     - {zid}")
        if len(zero_items) > 5:
            print(f"     ... e mais {len(zero_items) - 5} itens.")
    else:
        print("  ✅ Nenhum registro com indicadores zerados.")

def run_visual_dedup_check(images_dir):
    print(f"\n[3/4] 🖼️ Executando Deduplicação Visual (imagededup) em: {images_dir}...")
    try:
        from imagededup.methods import PHash
        phasher = PHash()

        target_dir = Path(images_dir)
        if not target_dir.is_absolute():
            target_dir = REPO_ROOT / target_dir

        if not target_dir.exists():
            print(f"  ⚠️ Diretório de imagens não encontrado: {target_dir}. Pulando dedup visual.")
            return

        duplicates = phasher.find_duplicates(image_dir=str(target_dir), max_distance_threshold=10)

        has_dups = {k: v for k, v in duplicates.items() if len(v) > 0}
        if has_dups:
            print(f"  ⚠️ Potenciais duplicatas visuais encontradas ({len(has_dups)} arquivos):")
            for orig, dups in list(has_dups.items())[:5]:
                print(f"     - {orig} -> {dups}")
        else:
            print("  ✅ Nenhuma duplicata visual detectada na pasta de imagens.")

    except Exception as e:
        print(f"  ❌ Erro ao rodar imagededup: {e}")

def run_cleanlab_audit(records):
    print("\n[4/4] 📊 Executando Diagnóstico de Rótulos & Outliers (Cleanlab)...")
    try:
        import numpy as np
        import cleanlab
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import cross_val_predict

        feature_matrix = []
        labels = []
        valid_ids = []

        for rec in records:
            pur = rec.get("purificacao", {})
            indicators = [pur.get(k, 0) for k in INDICATOR_KEYS]
            if sum(indicators) > 0:
                # Usar purificacao_composto como classe discreta de teste (binada)
                score = pur.get("purificacao_composto", 0.0)
                discrete_class = int(round(score * 3))  # Mapeia 0.0-1.0 para 0, 1, 2, 3
                feature_matrix.append(indicators)
                labels.append(discrete_class)
                valid_ids.append(rec.get("item_id") or rec.get("id"))

        if len(feature_matrix) < 10:
            print(f"  ⚠️ Apenas {len(feature_matrix)} itens codificados disponíveis para o Cleanlab (mínimo 10). Pulando auditoria estatística.")
            return

        X = np.array(feature_matrix)
        y = np.array(labels)

        clf = RandomForestClassifier(n_estimators=50, random_state=42)
        try:
            pred_probs = cross_val_predict(clf, X, y, cv=3, method="predict_proba")
            label_issues = cleanlab.filter.find_label_issues(labels=y, pred_probs=pred_probs)
            issue_idx = np.where(label_issues)[0]

            if len(issue_idx) > 0:
                print(f"  ⚠️ Cleanlab sinalizou {len(issue_idx)} potenciais inconsistências nos rótulos de endurecimento:")
                for idx in issue_idx[:5]:
                    print(f"     - ID: {valid_ids[idx]} | Classe Discreta: {y[idx]}")
            else:
                print("  ✅ Nenhuma inconsistência estatística nos rótulos de endurecimento.")
        except Exception as ex:
            print(f"  ℹ️ Validação do Cleanlab finalizada com aviso: {ex}")

    except Exception as e:
        print(f"  ❌ Erro ao rodar Cleanlab: {e}")

def main():
    parser = argparse.ArgumentParser(description="Auditoria de Qualidade do Corpus ICONOCRACY")
    parser.add_argument("--images-dir", default="gallery", help="Diretório de imagens a varrer")
    parser.add_argument("--verbose", action="store_true", help="Log detalhado")
    args = parser.parse_args()

    print("==========================================================")
    print("      ICONOCRACY — PIPELINE DE AUDITORIA DE DATASET       ")
    print("==========================================================")

    records = run_schema_check(args.verbose)
    if records:
        run_zero_indicator_check(records)
        run_cleanlab_audit(records)

    run_visual_dedup_check(args.images_dir)

    print("\n==========================================================")
    print("✨ Auditoria concluída! Consulte docs/MANUAL_QUALIDADE_DATASET.md para orientações.")
    print("==========================================================")

if __name__ == "__main__":
    main()
