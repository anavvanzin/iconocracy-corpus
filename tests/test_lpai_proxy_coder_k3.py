"""Testes das barreiras de escrita e do envelope de proxy do codificador K3.

Nenhum teste toca a rede. O foco é o contrato metodológico: o proxy não pode
escrever em artefato canônico e não pode produzir linha que se confunda com
codificação humana.
"""

from __future__ import annotations

import fcntl
import json
import os
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

import tools.scripts.lpai_proxy_coder_k3 as proxy
from tools.scripts.lpai_proxy_coder_k3 import (
    AGENT_ID,
    CODEBOOK_PATH,
    INDICATOR_KEYS,
    PROXY_SCHEMA_VERSION,
    REPO,
    SCRIPT_VERSION,
    GuardrailError,
    append_row,
    assert_write_target,
    build_output_schema,
    build_row,
    build_user_content,
    cached_download,
    load_done,
    load_master_prompt,
    select_items,
    validate_proxy_row,
)


@pytest.fixture()
def staging(tmp_path, monkeypatch):
    root = tmp_path / "staging"
    root.mkdir()
    monkeypatch.setattr(proxy, "DEFAULT_STAGING_ROOT", root)
    return root


# --------------------------------------------------------------------------
# Barreiras de escrita
# --------------------------------------------------------------------------


def test_aceita_destino_em_staging(staging):
    target = assert_write_target(staging / proxy.DEFAULT_OUTPUT_NAME)
    assert target == (staging / proxy.DEFAULT_OUTPUT_NAME).resolve()


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


def test_recusa_evasao_por_symlink_de_diretorio(staging, tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    link = staging / "escape"
    link.symlink_to(outside, target_is_directory=True)

    with pytest.raises(GuardrailError):
        assert_write_target(link / "proxy-runs.jsonl")


def test_recusa_evasao_por_symlink_de_arquivo(staging, tmp_path):
    outside = tmp_path / "outside.jsonl"
    outside.write_text("não tocar\n", encoding="utf-8")
    link = staging / "proxy-runs.jsonl"
    link.symlink_to(outside)

    with pytest.raises(GuardrailError):
        assert_write_target(link)
    assert outside.read_text(encoding="utf-8") == "não tocar\n"


@pytest.mark.parametrize(
    "directory",
    [
        REPO / "data" / "processed",
        REPO / "corpus",
        REPO / "examples",
        REPO / "schema",
        REPO / "tools" / "schemas",
    ],
)
def test_recusa_todos_os_diretorios_proibidos(staging, directory):
    with pytest.raises(GuardrailError):
        assert_write_target(directory / "proxy-runs.jsonl")


def test_saida_invalida_retorna_tres_sem_truncar_antes_de_rede(
    staging, monkeypatch
):
    forbidden = staging / "records.jsonl"
    forbidden.write_text("conteúdo original\n", encoding="utf-8")
    calls: list[str] = []

    monkeypatch.setattr(
        proxy, "make_client", lambda *_: calls.append("client")
    )
    monkeypatch.setattr(
        proxy, "cached_download", lambda *_: calls.append("network")
    )

    assert proxy.main(["--all", "--output", str(forbidden)]) == 3
    assert calls == []
    assert forbidden.read_text(encoding="utf-8") == "conteúdo original\n"


def test_append_recusa_troca_toctou_de_ancestral(staging, tmp_path, monkeypatch):
    safe_parent = staging / "batch"
    safe_parent.mkdir()
    output = safe_parent / "runs.jsonl"
    approved = assert_write_target(output)
    outside = tmp_path / "outside"
    outside.mkdir()
    original_assert = proxy.assert_write_target
    swapped = False

    def approve_then_swap(candidate):
        nonlocal swapped
        result = original_assert(candidate)
        if not swapped:
            safe_parent.rmdir()
            safe_parent.symlink_to(outside, target_is_directory=True)
            swapped = True
        return result

    monkeypatch.setattr(proxy, "assert_write_target", approve_then_swap)
    with pytest.raises(GuardrailError):
        append_row(
            approved,
            build_row(
                _record(),
                _coded(),
                model="kimi-k3",
                codebook_version="2.2.1",
                image_source=None,
            ),
        )
    assert not (outside / "runs.jsonl").exists()


def test_append_recusa_troca_toctou_do_arquivo(staging, tmp_path, monkeypatch):
    output = staging / "runs.jsonl"
    approved = assert_write_target(output)
    outside = tmp_path / "outside.jsonl"
    outside.write_text("não tocar\n", encoding="utf-8")
    original_assert = proxy.assert_write_target
    swapped = False

    def approve_then_swap(candidate):
        nonlocal swapped
        result = original_assert(candidate)
        if not swapped:
            output.symlink_to(outside)
            swapped = True
        return result

    monkeypatch.setattr(proxy, "assert_write_target", approve_then_swap)
    with pytest.raises(GuardrailError):
        append_row(
            approved,
            build_row(
                _record(),
                _coded(),
                model="kimi-k3",
                codebook_version="2.2.1",
                image_source=None,
            ),
        )
    assert outside.read_text(encoding="utf-8") == "não tocar\n"


def test_append_recusa_hardlink_para_arquivo_externo(staging, tmp_path):
    outside = tmp_path / "outside.jsonl"
    original = b"nao tocar\n"
    outside.write_bytes(original)
    output = staging / "runs.jsonl"
    os.link(outside, output)

    with pytest.raises(GuardrailError, match="hardlinks"):
        append_row(output, _row())
    assert outside.read_bytes() == original


def test_append_recusa_hardlink_especificamente_para_records(staging):
    records = REPO / "data" / "processed" / "records.jsonl"
    before = records.read_bytes()
    output = staging / "proxy-hardlink.jsonl"
    os.link(records, output)

    with pytest.raises(GuardrailError, match="hardlinks|canônico"):
        append_row(output, _row())
    assert records.read_bytes() == before


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
        "webscout": {
            "summary_evidence": "gravura",
            "gaps": [],
            "search_results": [
                {
                    "title": "Registro institucional",
                    "url": "https://example.org/catalogo",
                    "notes": "descrição catalográfica",
                }
            ],
        },
        "purificacao": {
            "coded_by": "ana",
            "regime_iconocratico": "fundacional",
            "record_metadata": {"medium": "moeda/metal"},
            "notes": "nota humana anterior",
        },
    }


def _coded():
    return {
        "item_id": "abc-123",
        "codificavel": True,
        "indicadores": {key: 1 for key in INDICATOR_KEYS},
        "inventario_verbal": ["balança", "olhos vendados"],
        "vetor_colonial": "republicano_brasileiro",
        "atributos_iconograficos": ["balança", "venda"],
        "hipotese_racial": "leitura situada, requer adjudicação",
        "programa_id": "programa-1",
        "ordem_no_programa": 2,
        "finalidade_atribuida": "legitimacao_juridica",
        "power_at_stake": "legitima a autoridade estatal",
        "regime_iconocratico": "normativo",
        "confianca": "media",
        "justificativa": "atributos visíveis",
        "notes": "incerteza preservada",
    }


def _row():
    return build_row(
        _record(),
        _coded(),
        model="kimi-k3",
        codebook_version="2.2.1",
        image_source=None,
    )


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
    assert row["script_version"] == SCRIPT_VERSION
    assert row["proxy_schema_version"] == PROXY_SCHEMA_VERSION
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


def test_row_preserva_todos_os_campos_do_paragrafo_16():
    coded = _coded()
    row = build_row(
        _record(), coded, model="kimi-k3", codebook_version="2.2.1", image_source=None
    )
    expected = {
        "vetor_colonial",
        "atributos_iconograficos",
        "hipotese_racial",
        "programa_id",
        "ordem_no_programa",
        "finalidade_atribuida",
        "power_at_stake",
        "notes",
    }
    assert expected <= row["proposta"].keys()
    assert all(row["proposta"][field] == coded[field] for field in expected)
    validate_proxy_row(row)


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
    assert "notes" in required


def test_linha_completa_valida_contra_schema_persistido():
    row = build_row(
        _record(), _coded(), model="kimi-k3", codebook_version="2.2.1", image_source=None
    )
    validate_proxy_row(row)


def test_schema_exige_versao_explicita_do_envelope():
    row = _row()
    del row["proxy_schema_version"]
    with pytest.raises(ValueError, match="proxy_schema_version"):
        validate_proxy_row(row)


def test_substituicao_do_conteudo_do_schema_invalida_validator(tmp_path):
    schema_path = tmp_path / "proxy.schema.json"
    original = proxy.PROXY_SCHEMA_PATH.read_bytes()
    schema_path.write_bytes(original)
    warmed = proxy.get_proxy_validator(schema_path)
    validate_proxy_row(_row(), validator=warmed)

    changed = json.loads(original)
    changed["properties"]["proxy_schema_version"]["const"] = "9.9.9"
    schema_path.write_text(json.dumps(changed), encoding="utf-8")
    current = proxy.get_proxy_validator(schema_path)

    assert current is not warmed
    with pytest.raises(ValueError, match="proxy_schema_version"):
        validate_proxy_row(_row(), validator=current)


def test_remocao_do_schema_apos_aquecimento_falha(tmp_path):
    schema_path = tmp_path / "proxy.schema.json"
    schema_path.write_bytes(proxy.PROXY_SCHEMA_PATH.read_bytes())
    proxy.get_proxy_validator(schema_path)
    schema_path.unlink()

    with pytest.raises(FileNotFoundError, match="schema do proxy não encontrado"):
        proxy.get_proxy_validator(schema_path)


def test_mutacao_do_dict_publico_nao_altera_validator(tmp_path):
    schema_path = tmp_path / "proxy.schema.json"
    schema_path.write_bytes(proxy.PROXY_SCHEMA_PATH.read_bytes())
    validator = proxy.get_proxy_validator(schema_path)
    public_schema = proxy.load_proxy_schema(schema_path)
    public_schema["properties"]["proxy_schema_version"]["const"] = "9.9.9"

    fresh_public_schema = proxy.load_proxy_schema(schema_path)
    assert fresh_public_schema["properties"]["proxy_schema_version"]["const"] == "1.0.0"
    assert fresh_public_schema is not public_schema
    validate_proxy_row(_row(), validator=validator)


def test_validator_reutiliza_somente_bytes_identicos(tmp_path):
    schema_path = tmp_path / "proxy.schema.json"
    original = proxy.PROXY_SCHEMA_PATH.read_bytes()
    schema_path.write_bytes(original)
    first = proxy.get_proxy_validator(schema_path)
    second = proxy.get_proxy_validator(schema_path)
    assert second is first

    schema_path.write_bytes(original + b"\n")
    changed = proxy.get_proxy_validator(schema_path)
    assert changed is not first

    schema_path.write_bytes(original)
    restored = proxy.get_proxy_validator(schema_path)
    assert restored is first


def test_append_rele_schema_antes_de_gravar(staging, monkeypatch):
    output = staging / "runs.jsonl"
    output.write_bytes(b"")
    original = output.read_bytes()
    warmed = proxy.get_proxy_validator()
    calls = 0

    def validator_then_missing():
        nonlocal calls
        calls += 1
        if calls == 1:
            return warmed
        raise FileNotFoundError("schema removido durante a operação")

    monkeypatch.setattr(proxy, "get_proxy_validator", validator_then_missing)
    with pytest.raises(FileNotFoundError, match="schema removido"):
        append_row(output, _row())

    assert calls == 2
    assert output.read_bytes() == original


def test_schema_rejeita_composto_e_campo_extra():
    coded = _coded()
    coded["purificacao_composto"] = 1.5
    row = build_row(
        _record(), coded, model="kimi-k3", codebook_version="2.2.1", image_source=None
    )
    with pytest.raises(ValueError, match="purificacao_composto"):
        validate_proxy_row(row)

    row = build_row(
        _record(), _coded(), model="kimi-k3", codebook_version="2.2.1", image_source=None
    )
    row["campo_extra"] = True
    with pytest.raises(ValueError, match="campo_extra"):
        validate_proxy_row(row)


def test_linha_invalida_nao_cria_arquivo(staging):
    output = staging / "runs.jsonl"
    row = build_row(
        _record(), _coded(), model="kimi-k3", codebook_version="2.2.1", image_source=None
    )
    row["proposta"]["purificacao_composto"] = 1.5

    with pytest.raises(ValueError, match="purificacao_composto"):
        append_row(output, row)
    assert not output.exists()


def test_append_deduplica_concorrencia_sob_lock(staging):
    output = staging / "runs.jsonl"
    barrier = threading.Barrier(2)

    def worker():
        barrier.wait()
        return append_row(output, _row())

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: worker(), range(2)))

    assert sorted(results) == [False, True]
    lines = output.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["item_id"] == "abc-123"


def test_append_respeita_lock_posix_exclusivo(staging):
    output = staging / "runs.jsonl"
    output.touch()
    held_fd = os.open(output, os.O_RDWR)
    started = threading.Event()
    pool = ThreadPoolExecutor(max_workers=1)

    def worker():
        started.set()
        return append_row(output, _row())

    try:
        fcntl.flock(held_fd, fcntl.LOCK_EX)
        future = pool.submit(worker)
        assert started.wait(timeout=1)
        time.sleep(0.05)
        assert not future.done()
        fcntl.flock(held_fd, fcntl.LOCK_UN)
        assert future.result(timeout=1) is True
    finally:
        fcntl.flock(held_fd, fcntl.LOCK_UN)
        pool.shutdown(wait=True)
        os.close(held_fd)


def test_append_rejeita_partial_write_e_reverte_arquivo(staging, monkeypatch):
    output = staging / "runs.jsonl"
    real_write = proxy.os.write

    def partial_write(fd, payload):
        return real_write(fd, payload[:-1])

    monkeypatch.setattr(proxy.os, "write", partial_write)
    with pytest.raises(OSError, match="parcial"):
        append_row(output, _row())
    assert output.read_bytes() == b""


# --------------------------------------------------------------------------
# Instrumento e CLI
# --------------------------------------------------------------------------


def test_caminho_real_do_codebook_e_secao_16():
    assert CODEBOOK_PATH == (
        REPO / "docs" / "methodology" / "codebooks" / "codebook-MASTER.md"
    )
    assert CODEBOOK_PATH.is_file()
    prompt, codebook_version = load_master_prompt()
    assert prompt
    assert codebook_version == "2.2.1"
    assert "Você é um codificador LPAI v2.2.1" in prompt


def test_version_e_do_script_nao_do_codebook(capsys):
    with pytest.raises(SystemExit) as exc:
        proxy.parse_args(["--version"])
    assert exc.value.code == 0
    output = capsys.readouterr().out.strip()
    assert output.endswith(SCRIPT_VERSION)
    assert "2.2.1" not in output


def test_dry_run_smoke_caminho_real_sem_escrita(tmp_path, monkeypatch):
    staging_root = tmp_path / "staging"
    images_dir = tmp_path / "images"
    images_dir.mkdir()
    (images_dir / "abc-123.jpg").write_bytes(b"placeholder")
    monkeypatch.setattr(proxy, "DEFAULT_STAGING_ROOT", staging_root)
    monkeypatch.setattr(proxy, "load_records", lambda: [_record()])
    monkeypatch.setattr(
        proxy,
        "make_client",
        lambda *_: pytest.fail("dry-run não pode criar cliente"),
    )
    monkeypatch.setattr(
        proxy,
        "cached_download",
        lambda *_: pytest.fail("dry-run não pode tocar a rede"),
    )

    assert (
        proxy.main(
            ["--all", "--dry-run", "--limit", "1", "--images-dir", str(images_dir)]
        )
        == 0
    )
    assert not staging_root.exists()


@pytest.mark.parametrize(
    "argv",
    [
        ["--items", ""],
        ["--items", ", ,"],
        ["--all", "--limit", "0"],
        ["--all", "--limit", "-1"],
        ["--all", "--retries", "-1"],
    ],
)
def test_cli_recusa_seletores_e_numeros_invalidos_antes_de_rede(argv, monkeypatch):
    monkeypatch.setattr(
        proxy, "make_client", lambda *_: pytest.fail("argumento inválido não cria cliente")
    )
    with pytest.raises(SystemExit) as exc:
        proxy.parse_args(argv)
    assert exc.value.code == 2


def test_todos_pulados_sem_evidencia_retorna_dois(staging, monkeypatch):
    monkeypatch.setattr(proxy, "load_records", lambda: [_record()])
    monkeypatch.setattr(
        proxy, "make_client", lambda *_: pytest.fail("dry-run não cria cliente")
    )
    assert proxy.main(["--all", "--dry-run", "--limit", "1"]) == 2
    assert not (staging / proxy.DEFAULT_OUTPUT_NAME).exists()


def test_default_versionado_nao_le_nem_toca_staging_legado(staging, monkeypatch):
    legacy = staging / "lpai-proxy-k3-runs.jsonl"
    legacy_bytes = b'{"legado":"historico-e-incompativel"}'
    legacy.write_bytes(legacy_bytes)
    monkeypatch.setattr(proxy, "load_records", lambda: [])
    monkeypatch.setattr(
        proxy, "make_client", lambda *_: pytest.fail("sem itens não cria cliente")
    )

    assert proxy.main(["--all", "--dry-run"]) == 0
    assert legacy.read_bytes() == legacy_bytes
    assert not (staging / proxy.DEFAULT_OUTPUT_NAME).exists()


def test_default_versionado_retoma_linhas_do_schema_corrente(staging, monkeypatch):
    current = staging / proxy.DEFAULT_OUTPUT_NAME
    assert append_row(current, _row()) is True
    original = current.read_bytes()
    monkeypatch.setattr(proxy, "load_records", lambda: [_record()])
    monkeypatch.setattr(
        proxy, "make_client", lambda *_: pytest.fail("item retomado não cria cliente")
    )
    monkeypatch.setattr(
        proxy,
        "cached_download",
        lambda *_: pytest.fail("item retomado não toca a rede"),
    )

    assert proxy.main(["--all"]) == 0
    assert current.read_bytes() == original
    assert load_done(current) == {"abc-123"}


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


def test_load_done_recusa_linha_corrompida(staging):
    path = staging / "runs.jsonl"
    path.write_text("{quebrado\n", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON inválido"):
        load_done(path)


def test_load_done_recusa_ultima_linha_sem_newline(staging):
    path = staging / "runs.jsonl"
    path.write_text(json.dumps({"item_id": "a"}), encoding="utf-8")
    with pytest.raises(ValueError, match="truncado"):
        load_done(path)


@pytest.mark.parametrize("extra_args", [[], ["--force"]])
def test_jsonl_corrompido_falha_antes_de_cliente_ou_rede(
    staging, monkeypatch, extra_args
):
    output = staging / "runs.jsonl"
    output.write_text('{"item_id":"a"}\n{"item_id":', encoding="utf-8")
    calls = []
    monkeypatch.setattr(proxy, "load_records", lambda: [_record()])
    monkeypatch.setattr(proxy, "make_client", lambda *_: calls.append("client"))
    monkeypatch.setattr(proxy, "cached_download", lambda *_: calls.append("network"))
    assert proxy.main(["--all", "--output", str(output), *extra_args]) == 1
    assert calls == []
    assert output.read_text(encoding="utf-8") == '{"item_id":"a"}\n{"item_id":'


def test_jsonl_sintaticamente_valido_fora_do_schema_falha_antes_da_rede(
    staging, monkeypatch
):
    output = staging / "runs.jsonl"
    invalid = {"item_id": "abc-123", "campo_extra": True}
    original = json.dumps(invalid) + "\n"
    output.write_text(original, encoding="utf-8")
    calls = []
    monkeypatch.setattr(proxy, "load_records", lambda: [_record()])
    monkeypatch.setattr(proxy, "make_client", lambda *_: calls.append("client"))
    monkeypatch.setattr(proxy, "cached_download", lambda *_: calls.append("network"))

    assert proxy.main(["--all", "--output", str(output)]) == 1
    assert calls == []
    assert output.read_text(encoding="utf-8") == original


def test_user_content_sem_imagem_instrui_nc():
    content = build_user_content(_record(), None, None)
    assert len(content) == 1
    assert "nc_causa=sem_imagem" in content[0]["text"]
    assert "FONTE ledger.input" in content[0]["text"]
    assert "FONTE purificacao preexistente" in content[0]["text"]
    assert '"suporte_medium": "moeda/metal"' in content[0]["text"]
    assert '"notas_anteriores": "nota humana anterior"' in content[0]["text"]
    assert "FONTE webscout" in content[0]["text"]
    assert "Registro institucional" in content[0]["text"]
    assert "não prova de recepção histórica" in content[0]["text"]
    assert "sentido produzido" in content[0]["text"]


def test_user_content_com_imagem_anexa_base64():
    content = build_user_content(_record(), "QUJD", "image/jpeg")
    assert content[1]["image_url"]["url"].startswith("data:image/jpeg;base64,")


def test_user_content_limita_notas_e_resultados_auxiliares():
    record = _record()
    record["purificacao"]["notes"] = "n" * 20_000
    record["webscout"]["search_results"] = [
        {"title": f"resultado-{index}", "notes": "x" * 5_000}
        for index in range(100)
    ]
    text = build_user_content(record, None, None)[0]["text"]
    assert "truncado" in text or "omitidos" in text
    assert len(text) < 3 * proxy.SOURCE_BLOCK_MAX_CHARS + 3_000
    assert "resultado-0" in text
    assert "resultado-99" not in text


# --------------------------------------------------------------------------
# Download e cache de evidência (todos mockados, sem rede)
# --------------------------------------------------------------------------


class _FakeResponse:
    def __init__(
        self,
        body: bytes,
        *,
        content_type: str = "image/jpeg",
        status: int = 200,
        url: str = "https://example.org/image.jpg",
        location: str | None = None,
        content_length: int | None = None,
    ):
        self.body = body
        self.status_code = status
        self.url = url
        self.closed = False
        self.headers = {"Content-Type": content_type}
        if location is not None:
            self.headers["Location"] = location
        if content_length is not None:
            self.headers["Content-Length"] = str(content_length)

    def iter_content(self, chunk_size):
        for offset in range(0, len(self.body), max(1, min(chunk_size, 3))):
            yield self.body[offset : offset + max(1, min(chunk_size, 3))]

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def close(self):
        self.closed = True


class _FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.urls = []

    def get(self, url, **kwargs):
        self.urls.append(url)
        if not self.responses:
            pytest.fail("requisição mockada inesperada")
        return self.responses.pop(0)


@pytest.fixture()
def public_dns(monkeypatch):
    def resolve(host, port, **kwargs):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", port))]

    monkeypatch.setattr(proxy.socket, "getaddrinfo", resolve)


def _install_fake_session(monkeypatch, responses):
    session = _FakeSession(responses)
    import requests

    monkeypatch.setattr(requests, "Session", lambda: session)
    return session


@pytest.mark.parametrize(
    ("url", "address"),
    [
        ("http://localhost/a.jpg", "127.0.0.1"),
        ("http://private.example/a.jpg", "10.0.0.1"),
        ("http://linklocal.example/a.jpg", "169.254.1.1"),
        ("http://reserved.example/a.jpg", "240.0.0.1"),
    ],
)
def test_url_recusa_host_nao_publico(url, address, monkeypatch):
    def resolve(host, port, **kwargs):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, port))]

    monkeypatch.setattr(proxy.socket, "getaddrinfo", resolve)
    with pytest.raises(ValueError):
        proxy._validate_public_http_url(url)


@pytest.mark.parametrize("url", ["file:///tmp/a.jpg", "ftp://example.org/a.jpg", "data:image/png,x"])
def test_url_recusa_esquema_nao_http(url):
    with pytest.raises(ValueError):
        proxy._validate_public_http_url(url)


def test_guarda_dns_recusa_rebinding_no_instante_da_conexao(monkeypatch):
    def rebound(host, port, **kwargs):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", port))]

    monkeypatch.setattr(proxy.socket, "getaddrinfo", rebound)
    with pytest.raises(ValueError, match="não público"):
        with proxy._public_dns_only():
            proxy.socket.getaddrinfo("example.org", 443, type=socket.SOCK_STREAM)


def test_download_valido_e_streaming_atomico(tmp_path, monkeypatch, public_dns):
    cache = tmp_path / "cache"
    monkeypatch.setattr(proxy, "IMAGE_CACHE", cache)
    body = b"\xff\xd8\xff\xe0" + b"imagem"
    response = _FakeResponse(body, content_length=len(body))
    session = _install_fake_session(monkeypatch, [response])

    result = cached_download("https://example.org/sem-extensao", "abc-123")

    assert result == cache / "abc-123.jpg"
    assert result.read_bytes() == body
    assert session.urls == ["https://example.org/sem-extensao"]
    assert response.closed
    assert list(cache.glob("*.tmp")) == []


def test_download_recusa_html_disfarcado_de_jpg(tmp_path, monkeypatch, public_dns):
    cache = tmp_path / "cache"
    monkeypatch.setattr(proxy, "IMAGE_CACHE", cache)
    response = _FakeResponse(b"<html>segredo</html>", content_type="image/jpeg")
    _install_fake_session(monkeypatch, [response])

    assert cached_download("https://example.org/a.jpg", "abc-123") is None
    assert not (cache / "abc-123.jpg").exists()
    assert list(cache.glob("*.tmp")) == []


def test_download_recusa_content_type_nao_imagem(tmp_path, monkeypatch, public_dns):
    cache = tmp_path / "cache"
    monkeypatch.setattr(proxy, "IMAGE_CACHE", cache)
    response = _FakeResponse(b"\xff\xd8\xff\xe0x", content_type="text/html")
    _install_fake_session(monkeypatch, [response])
    assert cached_download("https://example.org/a.jpg", "abc-123") is None
    assert not any(cache.iterdir())


def test_download_recusa_tamanho_declarado_excessivo(tmp_path, monkeypatch, public_dns):
    cache = tmp_path / "cache"
    monkeypatch.setattr(proxy, "IMAGE_CACHE", cache)
    response = _FakeResponse(
        b"\xff\xd8\xff\xe0x",
        content_length=proxy.IMAGE_MAX_BYTES + 1,
    )
    _install_fake_session(monkeypatch, [response])
    assert cached_download("https://example.org/a.jpg", "abc-123") is None
    assert not any(cache.iterdir())


def test_download_recusa_tamanho_real_excessivo(tmp_path, monkeypatch, public_dns):
    cache = tmp_path / "cache"
    monkeypatch.setattr(proxy, "IMAGE_CACHE", cache)
    monkeypatch.setattr(proxy, "IMAGE_MAX_BYTES", 8)
    response = _FakeResponse(b"\xff\xd8\xff\xe0" + b"12345")
    _install_fake_session(monkeypatch, [response])
    assert cached_download("https://example.org/a.jpg", "abc-123") is None
    assert not any(cache.iterdir())


def test_download_valida_url_final_reportada(tmp_path, monkeypatch):
    cache = tmp_path / "cache"
    monkeypatch.setattr(proxy, "IMAGE_CACHE", cache)

    def resolve(host, port, **kwargs):
        address = "127.0.0.1" if host == "127.0.0.1" else "93.184.216.34"
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, port))]

    monkeypatch.setattr(proxy.socket, "getaddrinfo", resolve)
    response = _FakeResponse(
        b"\xff\xd8\xff\xe0x",
        url="http://127.0.0.1/final.jpg",
    )
    _install_fake_session(monkeypatch, [response])
    assert cached_download("https://example.org/a.jpg", "abc-123") is None
    assert not any(cache.iterdir())


def test_redirect_para_ip_privado_e_bloqueado_antes_da_segunda_requisicao(
    tmp_path, monkeypatch
):
    cache = tmp_path / "cache"
    monkeypatch.setattr(proxy, "IMAGE_CACHE", cache)

    def resolve(host, port, **kwargs):
        address = "127.0.0.1" if host == "127.0.0.1" else "93.184.216.34"
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, port))]

    monkeypatch.setattr(proxy.socket, "getaddrinfo", resolve)
    redirect = _FakeResponse(
        b"",
        status=302,
        location="http://127.0.0.1/secret.jpg",
        url="https://example.org/a.jpg",
    )
    session = _install_fake_session(monkeypatch, [redirect])

    assert cached_download("https://example.org/a.jpg", "abc-123") is None
    assert session.urls == ["https://example.org/a.jpg"]
    assert not any(cache.iterdir())


def test_cache_recusa_symlink_de_arquivo_sem_tocar_alvo(
    tmp_path, monkeypatch, public_dns
):
    cache = tmp_path / "cache"
    cache.mkdir()
    outside = tmp_path / "outside.jpg"
    outside.write_bytes("não tocar".encode())
    (cache / "abc-123.jpg").symlink_to(outside)
    monkeypatch.setattr(proxy, "IMAGE_CACHE", cache)
    monkeypatch.setattr(
        proxy,
        "_download_response",
        lambda *_: pytest.fail("symlink deve bloquear antes do download"),
    )

    assert cached_download("https://example.org/a.jpg", "abc-123") is None
    assert outside.read_bytes() == "não tocar".encode()


def test_cache_recusa_hardlink_sem_tocar_alvo(
    tmp_path, monkeypatch, public_dns
):
    cache = tmp_path / "cache"
    cache.mkdir()
    outside = tmp_path / "outside.jpg"
    original = b"\xff\xd8\xff\xe0nao-tocar"
    outside.write_bytes(original)
    os.link(outside, cache / "abc-123.jpg")
    monkeypatch.setattr(proxy, "IMAGE_CACHE", cache)
    monkeypatch.setattr(
        proxy,
        "_download_response",
        lambda *_: pytest.fail("hardlink deve bloquear antes do download"),
    )

    assert cached_download("https://example.org/a.jpg", "abc-123") is None
    assert outside.read_bytes() == original


def test_cache_recusa_ancestral_symlink_sem_escrever_fora(
    tmp_path, monkeypatch, public_dns
):
    outside = tmp_path / "outside"
    outside.mkdir()
    cache_link = tmp_path / "cache"
    cache_link.symlink_to(outside, target_is_directory=True)
    monkeypatch.setattr(proxy, "IMAGE_CACHE", cache_link)
    monkeypatch.setattr(
        proxy,
        "_download_response",
        lambda *_: pytest.fail("ancestral symlink deve bloquear antes do download"),
    )

    assert cached_download("https://example.org/a.jpg", "abc-123") is None
    assert list(outside.iterdir()) == []
