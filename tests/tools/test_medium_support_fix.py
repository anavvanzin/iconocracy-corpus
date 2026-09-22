"""Tests for the medium/support canonical-ledger fix.

Covers:
- csv_to_records._build_purificacao mapping corpus ``support`` into
  ``purificacao.record_metadata.medium`` (so regeneration is self-sufficient);
- backfill_medium_support.backfill idempotency and preservation of existing
  record_metadata.

No real corpus files are touched — all fixtures are synthetic.
"""

from __future__ import annotations

from tools.scripts.backfill_medium_support import backfill
from tools.scripts.csv_to_records import _build_purificacao

ITEM = {
    "id": "XX-001",
    "title": "Alegoria Teste",
    "support": "moeda",
    "regime": "normativo",
    "indicadores": {"desincorporacao": 2},
}


def test_build_purificacao_maps_support_to_record_metadata():
    purif = _build_purificacao(ITEM, None)
    assert purif["record_metadata"] == {"medium": "moeda"}


def test_build_purificacao_sem_support_nao_escreve_record_metadata():
    item = {k: v for k, v in ITEM.items() if k != "support"}
    purif = _build_purificacao(item, None)
    assert "record_metadata" not in purif


def test_build_purificacao_support_em_branco_ignorado():
    purif = _build_purificacao({**ITEM, "support": "  "}, None)
    assert "record_metadata" not in purif


def _rec(item_id: str, rm: dict | None = None) -> dict:
    purif: dict = {"desincorporacao": 1}
    if rm is not None:
        purif["record_metadata"] = rm
    return {"item_id": item_id, "purificacao": purif}


def test_backfill_preenche_medium_ausente():
    records = [_rec("a"), _rec("b", {"medium": "selo"})]
    lookup = {"a": "moeda", "b": "cartaz"}
    _, changed = backfill(records, lookup)
    assert changed == 1
    assert records[0]["purificacao"]["record_metadata"]["medium"] == "moeda"
    # valor existente nunca é sobrescrito
    assert records[1]["purificacao"]["record_metadata"]["medium"] == "selo"


def test_backfill_preserva_outras_chaves_de_record_metadata():
    records = [_rec("a", {"title": "T", "institution": "BnF"})]
    backfill(records, {"a": "estampa/gravura"})
    rm = records[0]["purificacao"]["record_metadata"]
    assert rm == {"title": "T", "institution": "BnF", "medium": "estampa/gravura"}


def test_backfill_idempotente():
    records = [_rec("a")]
    lookup = {"a": "moeda"}
    backfill(records, lookup)
    _, changed = backfill(records, lookup)
    assert changed == 0
