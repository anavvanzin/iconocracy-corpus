"""Tests for tools/scripts/validate_schemas.py.

Covers the v2.3.0 pre-freeze conditional rules (warnings mode):
  - JUSTIFICATIVA_CURTA: justificativa_genero < 80 chars when masculine
  - REQUIRES_V23_FIELDS: familia_alegorica=Masculino_Juridico without v2.3.0 fields
  - HERCULES_INCOERENTE: substituicao_atributiva_hercules with orig==new

Baseline test (Test 1) ensures 299/299 real records remain valid against
master-record schema after any change to the validator.

These tests pin the GREEN behaviour to be implemented in the next commit.
On the RED commit (this one), _check_v23_warnings() returns [] unconditionally,
so Tests 2-5 document the desired behaviour without yet exercising the rules.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.scripts.validate_schemas import validate_records  # noqa: E402


# --- fixtures ---------------------------------------------------------------


@pytest.fixture(scope="module")
def real_records() -> List[Dict[str, Any]]:
    """Load the canonical 299-record dataset once per module."""
    path = REPO_ROOT / "data" / "processed" / "records.jsonl"
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


@pytest.fixture
def baseline_record() -> Dict[str, Any]:
    """Minimal but schema-complete record; overrides in each test."""
    return {
        "master_record_version": "1.0",
        "batch_id": "00000000-1c0c-4842-8a1a-test00000001",
        "item_id": "00000000-0000-0000-0000-000000000001",
        "item_hash": "0" * 64,
        "input": {
            "input_url": "https://example.org/test",
            "title_hint": "Test record",
            "date_hint": "2026",
            "place_hint": "Brazil",
        },
        "webscout": {
            "search_results": [],
            "summary_evidence": "minimal fixture",
            "gaps": [],
        },
        "iconocode": {
            "pre_iconographic": [],
            "codes": [],
            "interpretation": [],
            "validation": {"claim_ledger": []},
            "confidence": 0.8,
        },
        "purificacao": {
            "desincorporacao": 1,
            "rigidez_postural": 1,
            "dessexualizacao": 1,
            "uniformizacao_facial": 1,
            "heraldizacao": 1,
            "enquadramento_arquitetonico": 1,
            "apagamento_narrativo": 1,
            "monocromatizacao": 1,
            "serialidade": 1,
            "inscricao_estatal": 1,
            "familia_alegorica": "Virtudes",
            "subtipo": "Justica",
            "genero_atribuido": "feminino",
            "justificativa_genero": (
                "Marcador feminino convencional (balanca + espada + venda)."
            ),
        },
        "exports": {
            "abnt_citations": [],
            "audit_flags": [],
        },
        "timestamps": {
            "created_at": "2026-06-25T00:00:00Z",
            "updated_at": "2026-06-25T00:00:00Z",
        },
    }


# --- Test 1: baseline (preserva 299/299 + 0 warnings) ---------------------


def test_baseline_299_of_299_no_warnings(real_records):
    """Current state: 330 real records validate clean, 0 v2.3.0 warnings."""
    valid, total, errors, warnings = validate_records(
        real_records, "master-record"
    )

    assert total == 330, f"expected 330 records, got {total}"
    assert valid == 330, (
        f"baseline regression: {total - valid} records failed validation; "
        f"first 3 errors: {errors[:3]}"
    )
    assert errors == [], f"unexpected errors: {errors[:3]}"
    assert warnings == [], (
        f"baseline regression: {len(warnings)} unexpected warnings; "
        f"first 3: {warnings[:3]}"
    )


# --- Test 2: masculino + justificativa curta -> warning --------------------


def test_masculino_curto_justificativa_warning(baseline_record):
    """Rule 1: masculino + justificativa_genero < 80 chars -> warning, no error."""
    rec = baseline_record
    rec["purificacao"]["genero_atribuido"] = "masculino"
    rec["purificacao"]["familia_alegorica"] = "Masculino_Juridico"
    rec["purificacao"]["justificativa_genero"] = "curto"  # 5 chars, far below 80

    valid, total, errors, warnings = validate_records([rec], "master-record")

    assert total == 1
    assert valid == 1, f"warnings mode must not block: errors={errors}"
    assert errors == []
    matches = [w for w in warnings if w["code"] == "JUSTIFICATIVA_CURTA"]
    assert matches, f"missing JUSTIFICATIVA_CURTA warning; got {warnings}"
    assert matches[0]["record_id"] == rec["item_id"]
    assert matches[0]["field"] == "justificativa_genero"


# --- Test 3: Masculino_Juridico sem campos v2.3.0 -> warning ----------------


def test_masculino_juridico_sem_campos_v23_warning(baseline_record):
    """Rule 2: familia_alegorica=Masculino_Juridico without v2.3.0 fields."""
    rec = baseline_record
    rec["purificacao"]["genero_atribuido"] = "masculino"
    rec["purificacao"]["familia_alegorica"] = "Masculino_Juridico"
    rec["purificacao"]["justificativa_genero"] = "x" * 100  # long enough
    # deliberately NO funcao_da_figura_masculina or substituicao_atributiva_hercules

    valid, total, errors, warnings = validate_records([rec], "master-record")

    assert valid == 1, f"warnings mode must not block: errors={errors}"
    assert errors == []
    matches = [w for w in warnings if w["code"] == "REQUIRES_V23_FIELDS"]
    assert matches, f"missing REQUIRES_V23_FIELDS warning; got {warnings}"
    assert matches[0]["record_id"] == rec["item_id"]
    assert matches[0]["field"] == "familia_alegorica"


# --- Test 4: Hercules coerente -> sem warning HERCULES_INCOERENTE ----------


def test_hercules_coerente_ok(baseline_record):
    """Rule 3 (positive): hercules with orig != new -> no hercules warning."""
    rec = baseline_record
    rec["purificacao"]["familia_alegorica"] = "Masculino_Juridico"
    rec["purificacao"]["justificativa_genero"] = "x" * 100
    rec["purificacao"]["funcao_da_figura_masculina"] = "Pedagogia_Do_Bivio"
    rec["purificacao"]["substituicao_atributiva_hercules"] = {
        "atributo_canonico_substituido": "Cetro_Imperial",
        "atributo_novo": "Clava_Hercules",
        "justificativa": "Conforme adendo metodologico v2.3.0, p. 17.",
    }

    valid, total, errors, warnings = validate_records([rec], "master-record")

    assert valid == 1, f"coherent case must pass: errors={errors}"
    assert errors == []
    hercules_warnings = [
        w for w in warnings if w["code"] == "HERCULES_INCOERENTE"
    ]
    assert hercules_warnings == [], (
        f"coherent hercules must NOT warn; got {hercules_warnings}"
    )


# --- Test 5: Hercules incoerente -> warning --------------------------------


def test_hercules_incoerente_warning(baseline_record):
    """Rule 3 (negative): hercules with orig == new -> warning."""
    rec = baseline_record
    rec["purificacao"]["familia_alegorica"] = "Masculino_Juridico"
    rec["purificacao"]["justificativa_genero"] = "x" * 100
    rec["purificacao"]["funcao_da_figura_masculina"] = "Pedagogia_Do_Bivio"
    rec["purificacao"]["substituicao_atributiva_hercules"] = {
        "atributo_canonico_substituido": "Cetro_Imperial",
        "atributo_novo": "Cetro_Imperial",  # SAME as orig -> incoherent
        "justificativa": "Teste explicito de incoerencia (orig == new).",
    }

    valid, total, errors, warnings = validate_records([rec], "master-record")

    assert valid == 1, f"warnings mode must not block: errors={errors}"
    assert errors == []
    matches = [w for w in warnings if w["code"] == "HERCULES_INCOERENTE"]
    assert matches, f"missing HERCULES_INCOERENTE warning; got {warnings}"
    assert matches[0]["record_id"] == rec["item_id"]
    assert matches[0]["field"] == "substituicao_atributiva_hercules"
