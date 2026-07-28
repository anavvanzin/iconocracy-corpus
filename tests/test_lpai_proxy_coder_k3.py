"""Testes das barreiras de escrita e do envelope de proxy do codificador K3.

Nenhum teste toca a rede. O foco é o contrato metodológico: o proxy não pode
escrever em artefato canônico e não pode produzir linha que se confunda com
codificação humana.
"""

from __future__ import annotations

import json

import pytest

from tools.scripts.lpai_proxy_coder_k3 import (
    AGENT_ID,
    INDICATOR_KEYS,
    REPO,
    GuardrailError,
    assert_write_target,
    build_output_schema,
    build_row,
    build_user_content,
    load_done,
    select_items,
)


@pytest.fixture()
def staging(tmp_path, monkeypatch):
    root = tmp_path / "staging"
    root.mkdir()
    monkeypatch.setenv("LPAI_PROXY_STAGING_ROOT", str(root))
    return root


# --------------------------------------------------------------------------
# Barreiras de escrita
# --------------------------------------------------------------------------


def test_aceita_destino_em_staging(staging):
    target = assert_write_target(staging / "lpai-proxy-k3-runs.jsonl")
    assert target == (staging / "lpai-proxy-k3-runs.jsonl").resolve()


def test_recusa_records_jsonl_canonico(staging):
    with pytest.raises(GuardrailError):
        assert_write_target(REPO / "data" / "processed" / "records.jsonl")


def test_recusa_nome_records_jsonl_mesmo_dentro_de_staging(staging):
    """Nome de artefato canônico é bloqueado por si só, em qualquer diretório."""
    with pytest.raises(GuardrailError) as exc:
        assert_write_target(staging / "records.jsonl")
    assert "canônico" in str(exc.value)


@pytest.mark.parametrize(
    "nome",
    [
        "corpus-data.json",
        "corpus-data.v2.json",
        "corpus-data-enriched.json",
        "companion-data.json",
    ],
)
def test_recusa_exports_do_corpus(staging, nome):
    with pytest.raises(GuardrailError):
        assert_write_target(staging / nome)


def test_recusa_diretorio_canonico(staging):
    with pytest.raises(GuardrailError):
        assert_write_target(REPO / "corpus" / "proxy-runs.jsonl")


def test_recusa_fora_da_raiz_de_staging(staging, tmp_path):
    with pytest.raises(GuardrailError):
        assert_write_target(tmp_path / "solto" / "proxy-runs.jsonl")


def test_recusa_extensao_diferente_de_jsonl(staging):
    with pytest.raises(GuardrailError):
        assert_write_target(staging / "proxy-runs.json")


def test_recusa_escapar_de_staging_por_caminho_relativo(staging):
    with pytest.raises(GuardrailError):
        assert_write_target(staging / ".." / "proxy-runs.jsonl")


# --------------------------------------------------------------------------
# Envelope de proxy
# --------------------------------------------------------------------------


def _record():
    return {
        "item_id": "abc-123",
        "item_hash": "deadbeef",
        "input": {
            "input_url": "https://example.org/a.jpg",
            "title_hint": "Justiça",
            "date_hint": "1889",
            "place_hint": "Brazil",
        },
        "webscout": {"summary_evidence": "gravura", "gaps": []},
        "purificacao": {"coded_by": "ana", "regime_iconocratico": "fundacional"},
    }


def _coded():
    return {
        "item_id": "abc-123",
        "codificavel": True,
        "indicadores": {key: 1 for key in INDICATOR_KEYS},
        "inventario_verbal": ["balança", "olhos vendados"],
        "regime_iconocratico": "normativo",
        "confianca": "media",
        "justificativa": "atributos visíveis",
    }


def test_row_marca_autoridade_de_proxy():
    row = build_row(
        _record(),
        _coded(),
        model="kimi-k3",
        codebook_version="2.2.0",
        image_source="/tmp/abc-123.jpg",
    )
    assert row["proxy_only"] is True
    assert row["authority"] == "proxy"
    assert row["human_class"] is None
    assert row["merge_policy"] == "requires_human_adjudication"
    assert row["coded_by"] == AGENT_ID
    assert row["target_field"] == "purificacao_proposta"
    assert row["codebook_version"] == "2.2.0"
    assert row["capta_declaration"].startswith("LPAI v2-capta")


def test_row_nao_sobrescreve_autoria_humana():
    row = build_row(
        _record(), _coded(), model="kimi-k3", codebook_version="2.2.0", image_source=None
    )
    assert row["human_coded_by_at_read_time"] == "ana"
    assert row["coded_by"] != "ana"


def test_row_e_serializavel():
    row = build_row(
        _record(), _coded(), model="kimi-k3", codebook_version="2.2.0", image_source=None
    )
    assert json.loads(json.dumps(row, ensure_ascii=False))["item_id"] == "abc-123"


# --------------------------------------------------------------------------
# Esquema
# --------------------------------------------------------------------------


def test_schema_nunca_pede_composto():
    """Composto aposentado no codebook v2.2.1 (DEC-2026-07-28): sem campo, sem flag."""
    schema = build_output_schema()
    indicadores = schema["properties"]["indicadores"]
    assert "purificacao_composto" not in indicadores["properties"]
    assert set(INDICATOR_KEYS).issubset(indicadores["properties"])
    assert indicadores["additionalProperties"] is False


def test_build_output_schema_nao_aceita_opt_in_de_composto():
    with pytest.raises(TypeError):
        build_output_schema(emit_composto=True)  # type: ignore[call-arg]


def test_preambulo_proibe_agregacao():
    from tools.scripts.lpai_proxy_coder_k3 import PROXY_PREAMBLE

    assert "escores compostos" in PROXY_PREAMBLE
    assert "inventario_verbal" in PROXY_PREAMBLE


def test_schema_exige_justificativa_e_confianca():
    required = build_output_schema()["required"]
    assert "justificativa" in required
    assert "confianca" in required


# --------------------------------------------------------------------------
# Seleção, retomada e conteúdo
# --------------------------------------------------------------------------


def test_select_items_pula_itens_ja_em_staging():
    records = [_record(), {**_record(), "item_id": "def-456"}]
    selecionados = select_items(
        records, None, None, None, None, done={"abc-123"}, force=False
    )
    assert [r["item_id"] for r in selecionados] == ["def-456"]


def test_select_items_com_force_recodifica():
    records = [_record()]
    selecionados = select_items(
        records, None, None, None, None, done={"abc-123"}, force=True
    )
    assert len(selecionados) == 1


def test_select_items_filtra_por_regime_e_origem():
    records = [_record(), {**_record(), "item_id": "def-456"}]
    records[1]["purificacao"] = {
        "coded_by": "vault-import",
        "regime_iconocratico": "militar",
    }
    assert [
        r["item_id"]
        for r in select_items(records, None, "militar", None, None, set(), False)
    ] == ["def-456"]
    assert [
        r["item_id"]
        for r in select_items(records, None, None, "ana", None, set(), False)
    ] == ["abc-123"]


def test_load_done_ignora_linha_corrompida(tmp_path):
    path = tmp_path / "runs.jsonl"
    path.write_text(
        json.dumps({"item_id": "a"}) + "\n{quebrado\n" + json.dumps({"item_id": "b"}) + "\n",
        encoding="utf-8",
    )
    assert load_done(path) == {"a", "b"}


def test_user_content_sem_imagem_instrui_nc():
    content = build_user_content(_record(), None, None)
    assert len(content) == 1
    assert "nc_causa=sem_imagem" in content[0]["text"]


def test_user_content_com_imagem_anexa_base64():
    content = build_user_content(_record(), "QUJD", "image/jpeg")
    assert content[1]["image_url"]["url"].startswith("data:image/jpeg;base64,")
