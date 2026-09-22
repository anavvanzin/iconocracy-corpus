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
  - resolve_overlay_source() (revisão 2026-09-22, E1): fonte de overlay fixa
    (legacy.json > backup mais antigo > bootstrap one-shot); a saída do script
    nunca vira overlay, mesmo em execução posterior
  - Precedência do ledger (E2): gap-fill de medium/medium_norm/period a partir
    do ledger quando o overlay não tem o valor; curação do overlay preservada
  - Relatório (E3): contadores (itens novos, órfãos, sem date,
    local_image_path) computados dos dados, não hardcoded

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

from tools.scripts import regenerate_enriched  # noqa: E402
from tools.scripts.regenerate_enriched import (  # noqa: E402
    V230_FIELDS,
    build_record,
    load_master_records,
    resolve_master_record,
    resolve_overlay_source,
    validate_structural,
    write_report,
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


# ─── resolve_overlay_source (fonte de overlay fixa, revisão E1) ─────────────


class TestOverlaySource:
    """A fonte de overlay nunca pode ser a saída mais recente do script —
    regressão do bug E1 (execução no dia seguinte redefinia "legado")."""

    def _patch_paths(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            regenerate_enriched, "ENRICHED_PATH",
            tmp_path / "corpus-data-enriched.json")
        monkeypatch.setattr(
            regenerate_enriched, "LEGACY_PATH",
            tmp_path / "corpus-data-enriched.legacy.json")

    def test_legacy_json_wins_over_backups(self, tmp_path, monkeypatch):
        self._patch_paths(tmp_path, monkeypatch)
        (tmp_path / "corpus-data-enriched.legacy.json").write_text(
            '[{"id": "FR-001"}]', encoding="utf-8")
        (tmp_path / "corpus-data-enriched.json.bak.2026-09-17").write_text(
            '[{"id": "OLD"}]', encoding="utf-8")
        (tmp_path / "corpus-data-enriched.json.bak.2026-09-19").write_text(
            '[{"id": "OLD2"}]', encoding="utf-8")
        path, origin, overlay = resolve_overlay_source()
        assert path.name == "corpus-data-enriched.legacy.json"
        assert origin == "legacy.json commitado"
        assert overlay == [{"id": "FR-001"}]

    def test_falls_back_to_oldest_backup_not_today(self, tmp_path, monkeypatch):
        """Regressão E1: mesmo com a saída atual existindo e sendo mais nova,
        a fonte é o backup MAIS ANTIGO — nunca 'bak de hoje, senão o atual'."""
        self._patch_paths(tmp_path, monkeypatch)
        (tmp_path / "corpus-data-enriched.json").write_text(
            '[{"id": "OUTPUT-336"}]', encoding="utf-8")
        (tmp_path / "corpus-data-enriched.json.bak.2026-09-19").write_text(
            '[{"id": "MID"}]', encoding="utf-8")
        (tmp_path / "corpus-data-enriched.json.bak.2026-09-17").write_text(
            '[{"id": "PRISTINO"}]', encoding="utf-8")
        path, origin, overlay = resolve_overlay_source()
        assert path.name == "corpus-data-enriched.json.bak.2026-09-17"
        assert "backup mais antigo" in origin
        assert overlay == [{"id": "PRISTINO"}]

    def test_bootstrap_snapshots_once_then_uses_legacy(self, tmp_path,
                                                       monkeypatch):
        self._patch_paths(tmp_path, monkeypatch)
        enriched = tmp_path / "corpus-data-enriched.json"
        enriched.write_text('[{"id": "A"}]', encoding="utf-8")
        path, origin, overlay = resolve_overlay_source()
        assert path.name == "corpus-data-enriched.legacy.json"
        assert "bootstrap" in origin
        assert overlay == [{"id": "A"}]
        legacy = tmp_path / "corpus-data-enriched.legacy.json"
        assert legacy.read_text(encoding="utf-8") == '[{"id": "A"}]'
        # Segunda execução (outro dia, saída já regenerada): fonte segue fixa.
        enriched.write_text('[{"id": "A"}, {"id": "B"}]', encoding="utf-8")
        path2, origin2, overlay2 = resolve_overlay_source()
        assert path2 == path
        assert origin2 == "legacy.json commitado"
        assert overlay2 == [{"id": "A"}]  # saída nova NÃO vira overlay

    def test_bootstrap_without_enriched_exits(self, tmp_path, monkeypatch):
        self._patch_paths(tmp_path, monkeypatch)
        with pytest.raises(SystemExit):
            resolve_overlay_source()

    def test_corrupt_overlay_exits(self, tmp_path, monkeypatch):
        self._patch_paths(tmp_path, monkeypatch)
        (tmp_path / "corpus-data-enriched.legacy.json").write_text(
            "{{{not json", encoding="utf-8")
        with pytest.raises(SystemExit):
            resolve_overlay_source()

    def test_non_list_overlay_exits(self, tmp_path, monkeypatch):
        self._patch_paths(tmp_path, monkeypatch)
        (tmp_path / "corpus-data-enriched.legacy.json").write_text(
            '{"id": "FR-001"}', encoding="utf-8")
        with pytest.raises(SystemExit):
            resolve_overlay_source()


# ─── E2: precedência do ledger com overlay curado preservado ────────────────


class TestLedgerPrecedence:
    def test_new_item_derives_medium_period_from_ledger(self, stats):
        item = make_ledger_item(support="selo", date="1889")
        record, is_legacy = build_record(item, {}, stats)
        assert not is_legacy
        assert record["medium"] == "selo"
        assert record["medium_norm"] == "selo"
        assert record["period"] == "IIIe République (1870–1940)"

    def test_legacy_gap_filled_from_ledger(self, stats):
        """Overlay legado sem valor → ledger preenche (E2)."""
        old = {"id": "FR-001", "medium": None, "medium_norm": None,
               "period": None, "tags": ["curated"]}
        item = make_ledger_item(support="selo", date="1889")
        record, is_legacy = build_record(item, {"FR-001": old}, stats)
        assert is_legacy
        assert record["medium"] == "selo"
        assert record["medium_norm"] == "selo"
        assert record["period"] == "IIIe République (1870–1940)"

    def test_curated_overlay_values_preserved(self, stats):
        """Curação do overlay (c18aec3) não é sobrescrita pela derivação —
        o ledger só preenche lacunas, nunca destrói valor curado."""
        old = {"id": "FR-001", "medium": "Photograph (p&b)",
               "medium_norm": "fotografia", "period": "II Império (1852–1870)",
               "period_norm": None, "tags": ["female allegory", "statue"],
               "regime": "NORMATIVO",
               "regime_justificativa": "justificativa substantiva curada"}
        item = make_ledger_item(support="fotografia", date="1855")
        record, is_legacy = build_record(item, {"FR-001": old}, stats)
        assert is_legacy
        assert record["medium"] == "Photograph (p&b)"
        assert record["medium_norm"] == "fotografia"
        assert record["period"] == "II Império (1852–1870)"
        assert record["tags"] == ["female allegory", "statue"]


# ─── E3: números do relatório computados dos dados ──────────────────────────


class TestReportComputedNumbers:
    def _record(self, item_id, **kw):
        r = {"id": item_id, "title": "t", "country": "France", "date": "",
             "regime": "NORMATIVO", "url": None, "motif": [],
             "support": None}
        r.update(kw)
        return r

    def _stats(self, **kw):
        s = {"ledger_count": 2, "old_count": 1,
             "overlay_source": "corpus/x.legacy.json",
             "overlay_origin": "legacy.json commitado",
             "legacy_overlays": 1,
             "orphans": [("A-1", "t1"), ("A-2", "t2")],
             "regime_incerto": [], "legacy_regime_changed": [],
             "medium_unmapped": []}
        s.update(kw)
        return s

    def test_report_uses_computed_counts(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            regenerate_enriched, "REPORT_PATH", tmp_path / "report.md")
        records = [self._record("FR-001"), self._record("FR-002")]
        write_report(records, self._stats(), "2026-09-22")
        text = (tmp_path / "report.md").read_text(encoding="utf-8")
        assert "## Lacunas conhecidas dos 1 itens novos" in text  # 2 - 1 legado
        assert "Decidir o destino dos 2 órfãos" in text
        assert "- 2 itens sem `date` (ano derivado null)." in text
        assert "`local_image_path` é null para todos" in text
        assert "corpus/x.legacy.json" in text  # fonte explícita (E1)

    def test_report_counts_filled_local_image_paths(self, tmp_path,
                                                    monkeypatch):
        monkeypatch.setattr(
            regenerate_enriched, "REPORT_PATH", tmp_path / "report.md")
        records = [self._record("FR-001", local_image_path="corpus/imagens/x"),
                   self._record("FR-002")]
        write_report(records, self._stats(), "2026-09-22")
        text = (tmp_path / "report.md").read_text(encoding="utf-8")
        assert "`local_image_path` é null em 1/2" in text
        assert "é null para todos" not in text


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

        assert len(records) == len(real_ledger) == 337
        assert stats["with_master"] == 326
        assert stats["with_panofsky"] == 327
        assert stats["with_atributos"] == 17

        regimes = Counter(r["regime"] for r in records)
        assert regimes == {
            "FUNDACIONAL": 164,
            "NORMATIVO": 103,
            "MILITAR": 54,
            "CONTRA-ALEGORIA": 15,
            "": 1,  # dfe19295 Villares 1888 — regime pendente de codificação
        }

        errors = validate_structural(records)
        assert errors == []

        # todo item CONTRA-ALEGORIA carrega o regime em minúsculo no metadata
        for r in records:
            if r["regime"] == "CONTRA-ALEGORIA":
                assert r["iconographic_metadata"]["visual_regime"] == \
                    "contra-alegoria"
