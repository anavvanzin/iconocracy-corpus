"""Tests for tools/scripts/iconocode_gemma4.py.

Does NOT load the real 8B Gemma-4 model. A fake processor + model return a
canned JSON response; we exercise image hashing, JSON parsing, the repair
prompt path, item filtering, and cache behavior.
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.scripts import iconocode_gemma4 as mod  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures — mock model / processor, a tiny PNG, a fake corpus
# ---------------------------------------------------------------------------

GOOD_JSON = {
    "panofsky": {
        "pre_iconografico": "Figura feminina sentada, drapeada, segurando escudo e tridente.",
        "iconografico": "Britannia com atributos imperiais padrão.",
        "iconologico": "Alegoria do poder marítimo britânico em moeda corrente.",
    },
    "indicators": {
        "desincorporacao": 3,
        "rigidez_postural": 3,
        "dessexualizacao": 3,
        "uniformizacao_facial": 4,
        "heraldizacao": 4,
        "enquadramento_arquitetonico": 1,
        "apagamento_narrativo": 3,
        "monocromatizacao": 4,
        "serialidade": 4,
        "inscricao_estatal": 4,
    },
    "regime": "militar",
    "reasoning": "Cunhagem seriada com Britannia hierática e inscrição estatal dominante.",
    "confidence": "high",
}


class MockLlama:
    """Minimal llama_cpp.Llama stand-in.

    Returns canned chat-completion responses. Exposes `generate_calls` so
    tests that exercise the repair path can assert N generations happened.
    """

    def __init__(self, responses: list[str]) -> None:
        self._responses = list(responses)
        self.generate_calls = 0
        self.last_messages = None

    def create_chat_completion(self, messages, **kwargs):  # noqa: ARG002
        self.generate_calls += 1
        self.last_messages = messages
        text = self._responses.pop(0) if self._responses else ""
        return {"choices": [{"message": {"role": "assistant", "content": text}}]}


def _make_png(tmp_path: Path, name: str = "tiny.png") -> Path:
    """Create a real 1x1 PNG on disk so PIL.Image.open works."""
    from PIL import Image

    p = tmp_path / name
    Image.new("RGB", (1, 1), color=(200, 100, 50)).save(p, "PNG")
    return p


@pytest.fixture
def fake_corpus() -> list[dict[str, Any]]:
    return [
        {
            "id": "BE-5F-LEOPOLD-1832",
            "title": "5 Francs — Léopold I",
            "support": "moeda",
            "country": "Belgium",
            "url": "https://example.org/leopold.jpg",
            "thumbnail_url": "https://example.org/leopold-thumb.jpg",
            "indicadores": None,
        },
        {
            "id": "UK-PENNY-1912",
            "title": "1 Penny — Britannia Seated",
            "support": "moeda",
            "country": "UK",
            "url": "https://example.org/penny.jpg",
            "thumbnail_url": None,
            "indicadores": None,
        },
        {
            "id": "ALREADY-CODED",
            "title": "coded item",
            "indicadores": {"desincorporacao": 2},
        },
    ]


# ---------------------------------------------------------------------------
# 1. Image hashing is deterministic
# ---------------------------------------------------------------------------


def test_image_hash_is_deterministic(tmp_path):
    p = _make_png(tmp_path)
    h1 = mod.sha256_of(p)
    h2 = mod.sha256_of(p)
    assert h1 == h2
    assert len(h1) == 64  # sha256 hex length


# ---------------------------------------------------------------------------
# 2. Output JSON parses and round-trips through the schema
# ---------------------------------------------------------------------------


def test_round_trip_through_schema(tmp_path):
    image = _make_png(tmp_path)
    item = {"id": "UK-PENNY-1912", "title": "Penny", "support": "moeda"}
    record = mod.build_staging_record(
        item=item,
        parsed=GOOD_JSON,
        image_path=image,
        parse_failed=False,
        raw_text=json.dumps(GOOD_JSON),
    )
    serialized = json.dumps(record, ensure_ascii=False)
    reparsed = json.loads(serialized)

    # Required fields
    for key in (
        "run_id",
        "item_id",
        "agent_id",
        "coded_at",
        "panofsky",
        "indicators",
        "regime",
        "endurecimento_score",
        "reasoning",
        "image_hash",
        "confidence",
    ):
        assert key in reparsed, f"missing {key}"

    # Indicator count and range
    assert set(reparsed["indicators"].keys()) == set(mod.INDICATOR_KEYS)
    for v in reparsed["indicators"].values():
        assert 0 <= v <= 4
    # endurecimento_score = mean of 10 indicators
    assert reparsed["endurecimento_score"] == round(
        sum(reparsed["indicators"].values()) / 10, 2
    )
    # Regime must be one of the four canonical values
    assert reparsed["regime"] in mod.VALID_REGIMES


# ---------------------------------------------------------------------------
# 3. Malformed model output triggers the repair path
# ---------------------------------------------------------------------------


def test_malformed_output_triggers_repair(tmp_path):
    # First response: garbage. Second response: valid JSON.
    responses = [
        "um relatório em texto, sem JSON",
        "Claro! " + json.dumps(GOOD_JSON),
    ]
    coder = mod.GemmaIconoCoder(llm=MockLlama(responses))
    image = _make_png(tmp_path)
    item = {"id": "X-1", "title": "t", "support": "moeda", "country": "X", "date": "1900"}

    with patch.object(mod, "download_image", return_value=image):
        record = mod.code_one_item(coder, item, force_refresh=False)

    # Two generate calls — the initial + the repair
    assert coder.llm.generate_calls == 2
    assert record["parse_failed"] is False
    assert record["regime"] == "militar"
    assert record["confidence"] == "high"


def test_repair_still_fails_marks_low_confidence(tmp_path):
    responses = ["garbage 1", "garbage 2"]
    coder = mod.GemmaIconoCoder(llm=MockLlama(responses))
    image = _make_png(tmp_path)
    item = {"id": "X-2", "title": "t", "support": "moeda", "country": "X", "date": "1900"}

    with patch.object(mod, "download_image", return_value=image):
        record = mod.code_one_item(coder, item, force_refresh=False)

    assert coder.llm.generate_calls == 2
    assert record["parse_failed"] is True
    assert record["confidence"] == "low"
    # Indicators default to zeros
    assert record["indicators"] == {k: 0 for k in mod.INDICATOR_KEYS}
    # Raw output captured for debugging
    assert "raw_model_output" in record


# ---------------------------------------------------------------------------
# 4. --items filters to a single item
# ---------------------------------------------------------------------------


def test_items_flag_filters_to_one(fake_corpus):
    selected = mod.select_items(
        fake_corpus, ids=["BE-5F-LEOPOLD-1832"], all_uncoded=False
    )
    assert len(selected) == 1
    assert selected[0]["id"] == "BE-5F-LEOPOLD-1832"


def test_all_uncoded_excludes_coded_items(fake_corpus):
    selected = mod.select_items(fake_corpus, ids=None, all_uncoded=True)
    ids = {i["id"] for i in selected}
    assert ids == {"BE-5F-LEOPOLD-1832", "UK-PENNY-1912"}


def test_unknown_id_raises(fake_corpus):
    with pytest.raises(SystemExit):
        mod.select_items(fake_corpus, ids=["NOT-A-REAL-ID"], all_uncoded=False)


def test_main_requires_explicit_target(capsys):
    """No --items and no --all-uncoded → exit 1 with clear error (I2 fix)."""
    rc = mod.main([])
    assert rc == 1
    err = capsys.readouterr().err
    assert "--items" in err and "--all-uncoded" in err


# ---------------------------------------------------------------------------
# 5. Caching — second call on same ID does NOT re-download
# ---------------------------------------------------------------------------


class _FakeResp:
    def __init__(self, content: bytes, ctype: str = "image/jpeg") -> None:
        self.content = content
        self.headers = {"Content-Type": ctype}

    def raise_for_status(self) -> None:
        return None


class _CountingSession:
    def __init__(self, content: bytes) -> None:
        self.content = content
        self.get_calls = 0

    def get(self, url, **kwargs):  # noqa: ARG002
        self.get_calls += 1
        return _FakeResp(self.content)


def test_cached_image_not_redownloaded(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(
        mod,
        "image_cache_path",
        lambda item_id, ext="jpg": tmp_path / f"{item_id}.{ext}",
    )

    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (1, 1), color=(0, 0, 0)).save(buf, "JPEG")
    jpg_bytes = buf.getvalue()

    session = _CountingSession(jpg_bytes)
    item = {
        "id": "TEST-CACHE",
        "thumbnail_url": "https://example.org/thumb.jpg",
        "url": None,
    }

    # First call: fetches + writes to cache
    p1 = mod.download_image(item, force=False, session=session)  # type: ignore[arg-type]
    assert p1 is not None and p1.exists()
    assert session.get_calls == 1

    # Second call: should hit cache, NOT re-download
    p2 = mod.download_image(item, force=False, session=session)  # type: ignore[arg-type]
    assert p2 == p1
    assert session.get_calls == 1, "cache was bypassed on second call"

    # Third call: force_refresh=True re-downloads
    p3 = mod.download_image(item, force=True, session=session)  # type: ignore[arg-type]
    assert p3 is not None
    assert session.get_calls == 2


# ---------------------------------------------------------------------------
# 6. Parsing — fenced JSON blocks and indicator coercion
# ---------------------------------------------------------------------------


def test_parse_fenced_json_block():
    text = "```json\n" + json.dumps(GOOD_JSON) + "\n```"
    parsed = mod.parse_model_output(text)
    assert parsed is not None
    assert parsed["regime"] == "militar"


def test_parse_bare_json_block():
    text = "Aqui está: " + json.dumps(GOOD_JSON) + " — fim."
    parsed = mod.parse_model_output(text)
    assert parsed is not None
    assert parsed["indicators"]["heraldizacao"] == 4


def test_parse_returns_none_on_garbage():
    assert mod.parse_model_output("") is None
    assert mod.parse_model_output("nenhum json aqui") is None


def test_coerce_indicators_clamps_and_fills():
    out = mod.coerce_indicators(
        {"desincorporacao": 99, "rigidez_postural": -5, "heraldizacao": "3"}
    )
    assert out["desincorporacao"] == 4
    assert out["rigidez_postural"] == 0
    assert out["heraldizacao"] == 3
    # Missing keys default to 0
    for k in mod.INDICATOR_KEYS:
        assert k in out
        assert 0 <= out[k] <= 4


# ---------------------------------------------------------------------------
# 7. Missing image marks confidence=low without generating
# ---------------------------------------------------------------------------


def test_missing_image_skips_generation():
    coder = mod.GemmaIconoCoder(llm=MockLlama([]))
    item = {"id": "NO-IMG", "title": "t", "support": "moeda"}

    with patch.object(mod, "download_image", return_value=None):
        record = mod.code_one_item(coder, item, force_refresh=False)

    assert coder.llm.generate_calls == 0
    assert record["parse_failed"] is True
    assert record["confidence"] == "low"
    assert record["image_hash"] is None
