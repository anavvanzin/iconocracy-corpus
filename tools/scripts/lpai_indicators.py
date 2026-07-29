#!/usr/bin/env python3
"""
lpai_indicators.py — leitura não agregadora dos indicadores LPAI v2.

Substitui `endurecimento_score` / `purificacao_composto` nos consumidores do
corpus. O índice composto foi aposentado no codebook v2.2.1 (decisão
`docs/decisions/2026-07-28-aposentadoria-do-indice-composto.md`): a média tratava
como intercambiáveis indicadores incomensuráveis e comprimia dez decisões
interpretativas em um número que sobrevivia sozinho nas tabelas.

O que este módulo oferece no lugar:

  * `attribute_inventory` — a lista nomeada dos atributos efetivamente marcados.
    É a unidade de comparação da tese: inventário verbal, não escalar.
  * `attribute_count` — cardinalidade do inventário. Serve para ordenar e
    comparar sem afirmar intensidade. Contar quantos atributos estão presentes
    não é o mesmo que mediar valores incomensuráveis: a contagem não converte
    `monocromatizacao` e `dessexualizacao` em uma grandeza comum, apenas informa
    quantos traços o codificador registrou.
  * `coding_coverage` — quanto do instrumento foi efetivamente aplicado. Mede
    completude de codificação, não endurecimento.
  * `legacy_composite` — acessor SOMENTE de leitura para valores congelados.
    Nunca calcula. Existe para relatórios de diagnóstico legado.

Nenhuma função deste módulo cria um composto novo.
"""

from __future__ import annotations

from typing import Any, Mapping

INDICATOR_KEYS: tuple[str, ...] = (
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
)

# Escala 0–3 do codebook: 2 e 3 significam atributo presente de modo marcado.
ATTRIBUTE_THRESHOLD = 2

_NESTED_KEYS = ("indicadores", "indicators", "purificacao")


def indicator_values(entry: Mapping[str, Any] | None) -> dict[str, int]:
    """Extrai os 10 indicadores, aceitando forma achatada ou aninhada.

    Aceita `{"indicadores": {...}}`, `{"indicators": {...}}`,
    `{"purificacao": {...}}` e o registro achatado. Chaves ausentes ficam
    ausentes: ausência não é zero.
    """
    if not entry:
        return {}

    fontes: list[Mapping[str, Any]] = [entry]
    for key in _NESTED_KEYS:
        nested = entry.get(key)
        if isinstance(nested, Mapping):
            fontes.append(nested)

    valores: dict[str, int] = {}
    for fonte in fontes:
        for key in INDICATOR_KEYS:
            if key in valores:
                continue
            bruto = fonte.get(key)
            if bruto is None or isinstance(bruto, bool):
                continue
            try:
                valores[key] = int(bruto)
            except (TypeError, ValueError):
                continue
    return valores


def attribute_inventory(
    entry: Mapping[str, Any] | None, threshold: int = ATTRIBUTE_THRESHOLD
) -> list[str]:
    """Inventário verbal: nomes dos atributos marcados, em ordem canônica."""
    valores = indicator_values(entry)
    return [key for key in INDICATOR_KEYS if valores.get(key, 0) >= threshold]


def attribute_count(
    entry: Mapping[str, Any] | None, threshold: int = ATTRIBUTE_THRESHOLD
) -> int:
    """Quantidade de atributos marcados. Ordena sem afirmar intensidade."""
    return len(attribute_inventory(entry, threshold))


def coding_coverage(entry: Mapping[str, Any] | None) -> float:
    """Fração dos 10 indicadores explicitamente presentes na fonte (0.0–1.0)."""
    return len(indicator_values(entry)) / len(INDICATOR_KEYS)


def is_uncoded(entry: Mapping[str, Any] | None) -> bool:
    """Item sem codificação de indicadores: nenhum presente, ou todos em zero."""
    valores = indicator_values(entry)
    return not valores or all(valor == 0 for valor in valores.values())


def legacy_composite(entry: Mapping[str, Any] | None) -> float | None:
    """Valor legado congelado, se existir. NUNCA calcula um novo.

    Aceita os dois nomes históricos (`purificacao_composto` no ledger,
    `endurecimento_score` nos exports antigos). Retorna None quando ausente.
    """
    if not entry:
        return None
    fontes: list[Mapping[str, Any]] = [entry]
    nested = entry.get("purificacao")
    if isinstance(nested, Mapping):
        fontes.append(nested)
    for fonte in fontes:
        for nome in ("purificacao_composto", "endurecimento_score"):
            bruto = fonte.get(nome)
            if bruto is None:
                continue
            try:
                return float(bruto)
            except (TypeError, ValueError):
                continue
    return None


def describe_inventory(entry: Mapping[str, Any] | None) -> str:
    """Rótulo curto para logs e relatórios: contagem + atributos."""
    inventario = attribute_inventory(entry)
    if not inventario:
        return "sem atributos marcados"
    return f"{len(inventario)} atributos: " + ", ".join(inventario)
