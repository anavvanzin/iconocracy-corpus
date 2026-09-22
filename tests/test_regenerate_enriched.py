"""Tests for tools/scripts/regenerate_enriched.py.

Cobre a extensão da issue #211 (commit ac1ca89):
  - load_master_records(): indexa records.jsonl por item_id, mapeia handle→uuid
    via crosswalk, tolera linhas malformadas, arquivos ausentes → maps vazios
  - resolve_master_record(): UUID direto, handle→uuid→record, miss → None
  - build_record(master=...): propaga panofsky aninhado (3 níveis), mapeia
    attributes ← atributos_iconograficos, iconclass ← codes (só scheme=iconclass
    com notation), emite V230_FIELDS quando presentes, conta stats
  - build_record(master=None): regressão — comportamento idêntico ao pré-#211
    (visual_regime + endurecimento_score apenas)
  - validate_structural(): visual_regime obrigatório; endurecimento_score, quando
    presente, deve ser number (ausente é válido — item sem score no ledger)
  - Baseline de integração: pina as contagens reais do ledger (336 itens,
    326 panofsky, 17 atributos, distribuição de regimes) para detectar deriva
    do pipeline na regeneração.

Estilo: GREEN-first (o código já existe); os testes pinam o comportamento atual
e documentam as decisões semânticas (ex.: booleano False em V230_FIELDS é
emitido explicitamente — marker de ausência analiticamente significativa).
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.scripts.regenerate_enriched import (  # noqa: E402
    V230_FIELDS,
    build_record,
    load_master_records,
    resolve_master_record,
    validate_structural,
)


# ─── fixtures ───────────────────────────────────────────────────────────────


@pytest.fixture()
def stats() -> Dict[str, Any]:
    """Fresh stats dict matching main()'s shape."""
    return {
        "regime_incerto": [],
        "legacy_regime_changed": [],
        "medium_unmapped": [],
        "with_master": 0,
        "with_panofsky": 0,
        "with_atributos": 0,
    }


def make_ledger_item(**over: Any) -> Dict[str, Any]:
    """Minimal ledger item (corpus-data.json shape)."""
    item: Dict[str, Any] = {
        "id": "FR-001",
        "title": "Test Item",
        "country": "France",
        "date": "1889",
        "description": "desc",
        "motif": ["Justica"],
        "url": "https://example.org/img",
        "regime": "normativo",
        "citation_abnt": "ABNT...",
        "support": "selo",
    }
    item.update(over)
    return item


def make_master(**over: Any) -> Dict[str, Any]:
    """Minimal master record (records.jsonl shape)."""
    master: Dict[str, Any] = {
        "item_id": "uuid-1",
        "iconocode": {
            "pre_iconographic": [
                {"motif": "figura feminina", "observed": True},
            ],
            "codes": [
                {"scheme": "iconclass", "notation": "48C51",
                 "code_role": "depicts", "confidence": 0.8},
                {"scheme": "getty_aat", "notation": "300041620",
                 "code_role": "depicts", "confidence": 0.5},
                {"scheme": "iconclass", "notation": "",
                 "code_role": "depicts", "confidence": 0.9},
            ],
            "interpretation": [
                {"claim_text": "Regime iconocrático: NORMATIVO",
                 "claim_type": "iconographic",
                 "status": "supported", "confidence": 0.85},
            ],
            "confidence": 0.767,
        },
        "purificacao": {
            "regime_iconocratico": "normativo",
            "atributos_iconograficos": ["balanca", "olhos vendados"],
            "genero_atribuido": "feminino",
            "familia_alegorica": "Virtudes",
            "dado_negativo": False,
        },
    }
    master.update(over)
    return master


# ─── load_master_records ────────────────────────────────────────────────────


class TestLoadMasterRecords:
    def test_missing_files_yield_empty_maps(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "tools.scripts.regenerate_enriched.RECORDS_PATH", tmp_path / "none.jsonl")
        monkeypatch.setattr(
            "tools.scripts.regenerate_enriched.CROSSWALK_PATH", tmp_path / "none2.jsonl")
        recs, handles = load_master_records()
        assert recs == {}
        assert handles == {}

    def test_malformed_lines_are_skipped(self, tmp_path, monkeypatch):
        recs_file = tmp_path / "records.jsonl"
        recs_file.write_text(
            '{"item_id": "u1", "iconocode": {}}\n'
            'not-json{{{\n'
            '\n'
            '{"item_id": "u2", "iconocode": {}}\n',
            encoding="utf-8")
        cw_file = tmp_path / "crosswalk.jsonl"
        cw_file.write_text(
            '{"handle": "FR-001", "uuid": "u1"}\n'
            'garbage\n',
            encoding="utf-8")
        monkeypatch.setattr(
            "tools.scripts.regenerate_enriched.RECORDS_PATH", recs_file)
        monkeypatch.setattr(
            "tools.scripts.regenerate_enriched.CROSSWALK_PATH", cw_file)
        recs, handles = load_master_records()
        assert set(recs) == {"u1", "u2"}
        assert handles == {"FR-001": "u1"}


# ─── resolve_master_record ──────────────────────────────────────────────────


class TestResolveMasterRecord:
    def test_uuid_direct_hit(self):
        master = make_master()
        recs = {"uuid-1": master}
        assert resolve_master_record("uuid-1", recs, {}) is master

    def test_handle_via_crosswalk(self):
        master = make_master()
        recs = {"uuid-1": master}
        assert resolve_master_record("FR-001", recs, {"FR-001": "uuid-1"}) is master

    def test_unresolvable_returns_none(self):
        assert resolve_master_record("XX-999", {}, {}) is None

    def test_handle_without_record_returns_none(self):
        # crosswalk conhece o handle mas o record não existe
        assert resolve_master_record("FR-001", {}, {"FR-001": "uuid-missing"}) is None


# ─── build_record com master ────────────────────────────────────────────────


class TestBuildRecordWithMaster:
    def test_panofsky_nested_with_all_levels(self, stats):
        item = make_ledger_item()
        record, is_legacy = build_record(
            item, {}, stats, master=make_master())
        panofsky = record["iconographic_metadata"]["panofsky"]
        assert len(panofsky["pre_iconographic"]) == 1
        assert len(panofsky["interpretation"]) == 1
        assert panofsky["confidence"] == 0.767
        assert stats["with_panofsky"] == 1

    def test_panofsky_absent_when_iconocode_empty(self, stats):
        master = make_master(iconocode={})
        record, _ = build_record(make_ledger_item(), {}, stats, master=master)
        assert "panofsky" not in record["iconographic_metadata"]
        assert stats["with_panofsky"] == 0

    def test_iconclass_only_iconclass_scheme_with_notation(self, stats):
        record, _ = build_record(
            make_ledger_item(), {}, stats, master=make_master())
        # getty_aat excluído; iconclass com notation vazia excluído
        assert record["iconographic_metadata"]["iconclass"] == ["48C51"]

    def test_attributes_from_atributos(self, stats):
        record, _ = build_record(
            make_ledger_item(), {}, stats, master=make_master())
        assert record["iconographic_metadata"]["attributes"] == \
            ["balanca", "olhos vendados"]
        assert stats["with_atributos"] == 1

    def test_v230_fields_emitted_when_present(self, stats):
        record, _ = build_record(
            make_ledger_item(), {}, stats, master=make_master())
        assert record["genero_atribuido"] == "feminino"
        assert record["familia_alegorica"] == "Virtudes"
        # False é emitido explicitamente: marker de ausência analiticamente
        # significativa (decisão documentada, commit ac1ca89)
        assert record["dado_negativo"] is False

    def test_v230_fields_omitted_when_absent(self, stats):
        master = make_master()
        for field in V230_FIELDS:
            master["purificacao"].pop(field, None)
        record, _ = build_record(
            make_ledger_item(), {}, stats, master=master)
        for field in V230_FIELDS:
            assert field not in record

    def test_stats_with_master_counted(self, stats):
        build_record(make_ledger_item(), {}, stats, master=make_master())
        assert stats["with_master"] == 1

    def test_regime_upper_and_visual_regime_lower(self, stats):
        record, _ = build_record(
            make_ledger_item(regime="contra-alegoria"), {}, stats,
            master=make_master())
        assert record["regime"] == "CONTRA-ALEGORIA"
        assert record["iconographic_metadata"]["visual_regime"] == "contra-alegoria"


# ─── build_record sem master (regressão pré-#211) ───────────────────────────


class TestBuildRecordWithoutMaster:
    def test_minimal_iconographic_metadata(self, stats):
        record, _ = build_record(
            make_ledger_item(endurecimento_score=1.4), {}, stats, master=None)
        meta = record["iconographic_metadata"]
        assert meta == {"visual_regime": "normativo", "endurecimento_score": 1.4}
        assert "panofsky" not in meta
        assert "attributes" not in meta
        for field in V230_FIELDS:
            assert field not in record

    def test_score_none_omitted_from_metadata(self, stats):
        """Bug fix #211: endurecimento_score None não pode ir ao metadata
        (schema exige number quando presente)."""
        record, _ = build_record(make_ledger_item(), {}, stats, master=None)
        assert "endurecimento_score" not in record["iconographic_metadata"]


# ─── validate_structural ────────────────────────────────────────────────────


class TestValidateStructural:
    def base_record(self) -> Dict[str, Any]:
        return {
            "id": "FR-001", "title": "t", "country": "France",
            "date": "1889", "regime": "NORMATIVO",
            "url": "https://x.org", "motif": ["a"],
            "iconographic_metadata": {"visual_regime": "normativo"},
        }

    def test_valid_minimal(self):
        assert validate_structural([self.base_record()]) == []

    def test_missing_visual_regime_fails(self):
        r = self.base_record()
        r["iconographic_metadata"] = {}
        errors = validate_structural([r])
        assert any("visual_regime" in e for e in errors)

    def test_score_absent_is_valid(self):
        """Nova semântica #211: score ausente é válido (item sem score no ledger)."""
        assert validate_structural([self.base_record()]) == []

    def test_score_string_fails(self):
        r = self.base_record()
        r["iconographic_metadata"]["endurecimento_score"] = "1.4"
        errors = validate_structural([r])
        assert any("not a number" in e for e in errors)

    def test_score_numeric_ok(self):
        r = self.base_record()
        r["iconographic_metadata"]["endurecimento_score"] = 1.4
        assert validate_structural([r]) == []

    def test_motif_not_list_fails(self):
        r = self.base_record()
        r["motif"] = "not-a-list"
        errors = validate_structural([r])
        assert any("motif" in e for e in errors)


# ─── baseline de integração (pins contra deriva do pipeline) ────────────────


@pytest.fixture(scope="module")
def real_ledger() -> List[Dict[str, Any]]:
    path = REPO_ROOT / "corpus" / "corpus-data.json"
    return json.loads(path.read_text(encoding="utf-8"))


class TestIntegrationBaseline:
    """Roda o pipeline real completo e pina as contagens #211.

    Se este teste falhar após uma mudança em regenerate_enriched.py ou nos
    dados, a decisão foi deliberada? Atualize os números conscientemente —
    não ajuste o código para fazer o teste passar.
    """

    def test_full_regeneration_counts(self, real_ledger):
        records_by_uuid, handle_to_uuid = load_master_records()
        stats = {
            "regime_incerto": [], "legacy_regime_changed": [],
            "medium_unmapped": [],
            "with_master": 0, "with_panofsky": 0, "with_atributos": 0,
        }
        records = []
        for item in real_ledger:
            master = resolve_master_record(
                item["id"], records_by_uuid, handle_to_uuid)
            record, _ = build_record(item, {}, stats, master)
            records.append(record)

        assert len(records) == len(real_ledger) == 336
        assert stats["with_master"] == 326
        assert stats["with_panofsky"] == 326
        assert stats["with_atributos"] == 17

        regimes = Counter(r["regime"] for r in records)
        assert regimes == {
            "FUNDACIONAL": 164,
            "NORMATIVO": 103,
            "MILITAR": 54,
            "CONTRA-ALEGORIA": 15,
        }

        errors = validate_structural(records)
        assert errors == []

        # todo item CONTRA-ALEGORIA carrega o regime em minúsculo no metadata
        for r in records:
            if r["regime"] == "CONTRA-ALEGORIA":
                assert r["iconographic_metadata"]["visual_regime"] == \
                    "contra-alegoria"
