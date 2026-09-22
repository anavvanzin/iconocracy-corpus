"""Testes do módulo que substitui o índice composto (DEC-2026-07-28).

O contrato é negativo antes de ser positivo: nenhuma função pode produzir um
composto novo. `legacy_composite` apenas lê valores congelados.
"""

from __future__ import annotations

from tools.scripts.lpai_indicators import (
    INDICATOR_KEYS,
    attribute_count,
    attribute_inventory,
    coding_coverage,
    describe_inventory,
    indicator_values,
    is_uncoded,
    legacy_composite,
)


def _flat(**valores):
    return dict(valores)


def test_le_forma_achatada():
    entry = _flat(desincorporacao=3, serialidade=1)
    assert indicator_values(entry) == {"desincorporacao": 3, "serialidade": 1}


def test_le_forma_aninhada_indicadores():
    entry = {"indicadores": {"heraldizacao": 2}}
    assert indicator_values(entry) == {"heraldizacao": 2}


def test_le_forma_aninhada_purificacao():
    entry = {"purificacao": {"rigidez_postural": 3}}
    assert indicator_values(entry) == {"rigidez_postural": 3}


def test_ausencia_nao_e_zero():
    """Chave ausente fica ausente — é o que distingue não codificado de zero."""
    valores = indicator_values({"indicadores": {"serialidade": 0}})
    assert valores == {"serialidade": 0}
    assert "heraldizacao" not in valores


def test_inventario_usa_limiar_dois():
    entry = _flat(desincorporacao=3, rigidez_postural=2, dessexualizacao=1, serialidade=0)
    assert attribute_inventory(entry) == ["desincorporacao", "rigidez_postural"]


def test_inventario_respeita_ordem_canonica():
    entry = _flat(inscricao_estatal=3, desincorporacao=3)
    assert attribute_inventory(entry) == ["desincorporacao", "inscricao_estatal"]


def test_contagem_de_atributos():
    entry = {"indicadores": {key: 2 for key in INDICATOR_KEYS[:4]}}
    assert attribute_count(entry) == 4


def test_cobertura_mede_completude_nao_intensidade():
    """Dez zeros são cobertura total: o instrumento foi aplicado inteiro."""
    entry = {"indicadores": {key: 0 for key in INDICATOR_KEYS}}
    assert coding_coverage(entry) == 1.0
    assert attribute_count(entry) == 0


def test_cobertura_parcial():
    entry = {"indicadores": {key: 3 for key in INDICATOR_KEYS[:5]}}
    assert coding_coverage(entry) == 0.5


def test_is_uncoded_distingue_ausencia_de_zero_codificado():
    assert is_uncoded({}) is True
    assert is_uncoded({"indicadores": {}}) is True
    assert is_uncoded({"indicadores": {key: 0 for key in INDICATOR_KEYS}}) is True
    assert is_uncoded({"indicadores": {"serialidade": 1}}) is False


def test_legacy_composite_apenas_le():
    assert legacy_composite({"purificacao_composto": 2.1}) == 2.1
    assert legacy_composite({"purificacao": {"purificacao_composto": 1.5}}) == 1.5
    assert legacy_composite({"endurecimento_score": 0.8}) == 0.8


def test_legacy_composite_nunca_calcula():
    """Com os 10 indicadores presentes e nenhum composto gravado, retorna None."""
    entry = {"indicadores": {key: 3 for key in INDICATOR_KEYS}}
    assert legacy_composite(entry) is None


def test_legacy_composite_tolera_lixo():
    assert legacy_composite({"purificacao_composto": "n/a"}) is None
    assert legacy_composite(None) is None


def test_describe_inventory_para_log():
    entry = _flat(desincorporacao=3, serialidade=2)
    assert describe_inventory(entry) == "2 atributos: desincorporacao, serialidade"
    assert describe_inventory({}) == "sem atributos marcados"


def test_nenhuma_funcao_publica_devolve_media():
    """Guarda-costas do contrato: a média dos indicadores não aparece em lugar algum."""
    entry = {"indicadores": {key: 2 for key in INDICATOR_KEYS}}
    media = 2.0
    resultados = [
        attribute_count(entry),
        coding_coverage(entry),
        legacy_composite(entry),
        is_uncoded(entry),
    ]
    assert media not in [r for r in resultados if isinstance(r, float)]
