#!/usr/bin/env python3
"""
measure_stratum_i.py — medição programática do Estrato I do LPAI v3.

O Estrato I reúne atributos que nunca foram juízo iconográfico: propriedades
materiais do suporte. Monocromatização é o caso exemplar — a matriz de correlação
do corpus mostrou que ela é ortogonal a todos os outros indicadores (r entre 0,07
e 0,27, e -0,04 com inscrição estatal). Medi-la por script, em vez de codificá-la
a olho, faz três coisas: torna o valor reprodutível por execução em lugar de
depender de concordância entre codificadores; libera tempo humano para o Estrato
III, que é onde o juízo é irredutível; e explicita, no próprio método, que aquele
atributo não pertence à mesma escala dos demais.

Métrica
-------
Usa o índice de colorfulness de Hasler & Süsstrunk (2003), definido em espaço de
oponência simples e validado experimentalmente contra julgamento humano:

    rg = R - G
    yb = 0,5 (R + G) - B
    C  = sqrt(sigma_rg^2 + sigma_yb^2) + 0,3 * sqrt(mu_rg^2 + mu_yb^2)

Âncoras qualitativas do artigo original: 0 "not colorful", 15 "slightly", 33
"moderately", 45 "averagely", 59 "quite", 82 "highly", 109 "extremely". A
monocromatização é o inverso da colorfulness, e a conversão para a escala ordinal
0–3 do codebook usa essas âncoras — não limiares arbitrários:

    C < 15   -> monocromatizacao = 3  (monocromia efetiva)
    15 <= C < 33 -> 2               (cromatismo restrito)
    33 <= C < 59 -> 1               (cromatismo moderado)
    C >= 59      -> 0               (policromia plena)

Registra também três medidas de apoio, para que a decisão seja auditável e não
dependa de um número único: fração de pixels de baixa saturação, saturação média
e número de matizes distintos com massa relevante.

Ressalva registrada
-------------------
A medição descreve o ARQUIVO, não necessariamente o OBJETO. Reprodução
fotográfica com dominante amarelada, digitalização em tons de cinza de um
original colorido e fundo de papel envelhecido deslocam a métrica. Por isso cada
resultado carrega `caveat` quando a imagem é suspeita, e o valor medido é uma
PROPOSTA sujeita a confirmação humana — nunca escrita direto no ledger canônico.

Uso
---
    python tools/scripts/measure_stratum_i.py --all
    python tools/scripts/measure_stratum_i.py --all --compare
    python tools/scripts/measure_stratum_i.py --items <item_id>

Códigos de saída
----------------
    0 sucesso · 1 erro fatal · 2 concluído com imagens suspeitas · 3 barreira
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

# Digitalizações IIIF em resolução plena chegam a 145 megapixels (Gallica, LoC).
# São legítimas e vêm de acervo institucional; o limite antibomba do Pillow é
# elevado deliberadamente, e a imagem é reamostrada antes de qualquer cálculo.
Image.MAX_IMAGE_PIXELS = 400_000_000

REPO = Path(__file__).resolve().parent.parent.parent
CANONICAL_RECORDS = REPO / "data" / "processed" / "records.jsonl"
IMAGE_CACHE = REPO / ".cache" / "corpus-images"
SAIDA = REPO / "data" / "staging" / "stratum-i-measurements.jsonl"

METRIC_VERSION = "hasler-susstrunk-2003/v1"
LADO_MAXIMO = 1200          # reamostragem: a métrica é estatística, não precisa full-res
SATURACAO_BAIXA = 0.12      # abaixo disso o pixel é praticamente acromático
RESOLUCAO_MINIMA = 400      # menor lado abaixo do qual a leitura fica frágil

# Âncoras de Hasler & Süsstrunk (2003) → escala ordinal 0–3 do codebook
ANCORAS = ((15.0, 3), (33.0, 2), (59.0, 1))

FORBIDDEN_DIRS = (
    REPO / "data" / "processed",
    REPO / "corpus",
    REPO / "examples",
    REPO / "schema",
    REPO / "tools" / "schemas",
)


class GuardrailError(RuntimeError):
    """Tentativa de escrever em área canônica do corpus."""


def assert_write_target(path: Path) -> Path:
    resolved = path.resolve()
    if resolved.name == "records.jsonl":
        raise GuardrailError("'records.jsonl' é o ledger canônico; a medição não escreve nele")
    if resolved.suffix != ".jsonl":
        raise GuardrailError(f"saída precisa ser .jsonl: {resolved.name}")
    for directory in FORBIDDEN_DIRS:
        try:
            resolved.relative_to(directory.resolve())
        except ValueError:
            continue
        raise GuardrailError(f"área canônica bloqueada: {resolved}")
    return resolved


# ---------------------------------------------------------------------------
# Métrica
# ---------------------------------------------------------------------------


def colorfulness(rgb: np.ndarray) -> float:
    """Índice de Hasler & Süsstrunk (2003) em espaço de oponência simples."""
    r, g, b = (rgb[..., i].astype(np.float64) for i in range(3))
    rg = r - g
    yb = 0.5 * (r + g) - b
    return float(
        np.sqrt(rg.std() ** 2 + yb.std() ** 2)
        + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2)
    )


def ordinal_por_ancora(indice: float) -> int:
    for limite, valor in ANCORAS:
        if indice < limite:
            return valor
    return 0


def medidas_de_apoio(imagem: Image.Image) -> dict[str, Any]:
    """Saturação, acromaticidade e dispersão de matizes — auditoria do número único."""
    hsv = np.asarray(imagem.convert("HSV"), dtype=np.float64) / 255.0
    matiz, saturacao, valor = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    acromatico = saturacao < SATURACAO_BAIXA
    fracao_acromatica = float(acromatico.mean())

    # matizes contam apenas onde há cor e luz suficientes para o matiz existir
    mascara = (~acromatico) & (valor > 0.10) & (valor < 0.97)
    if mascara.sum() > 0:
        histograma, _ = np.histogram(matiz[mascara], bins=36, range=(0.0, 1.0))
        relevantes = int((histograma > histograma.sum() * 0.01).sum())
        saturacao_media_cromatica = float(saturacao[mascara].mean())
    else:
        relevantes = 0
        saturacao_media_cromatica = 0.0

    return {
        "fracao_acromatica": round(fracao_acromatica, 4),
        "saturacao_media": round(float(saturacao.mean()), 4),
        "saturacao_media_cromatica": round(saturacao_media_cromatica, 4),
        "matizes_relevantes": relevantes,
    }


def mede(caminho: Path) -> dict[str, Any]:
    with Image.open(caminho) as bruta:
        largura_original, altura_original = bruta.size
        imagem = bruta.convert("RGB")
        imagem.thumbnail((LADO_MAXIMO, LADO_MAXIMO))
        arranjo = np.asarray(imagem)
        apoio = medidas_de_apoio(imagem)

    indice = colorfulness(arranjo)
    proposto = ordinal_por_ancora(indice)

    ressalvas: list[str] = []
    if min(largura_original, altura_original) < RESOLUCAO_MINIMA:
        ressalvas.append("resolucao_baixa: leitura frágil, confirmar a olho")
    if apoio["fracao_acromatica"] > 0.97 and apoio["matizes_relevantes"] == 0:
        ressalvas.append("possivel digitalizacao em tons de cinza de original colorido")
    if 12.0 < indice < 18.0 or 30.0 < indice < 36.0 or 56.0 < indice < 62.0:
        ressalvas.append("índice em zona de fronteira entre duas âncoras")
    if apoio["matizes_relevantes"] == 1 and apoio["fracao_acromatica"] < 0.5:
        ressalvas.append("dominante única: possível viés de reprodução fotográfica")

    return {
        "colorfulness": round(indice, 2),
        "monocromatizacao_proposta": proposto,
        "metric_version": METRIC_VERSION,
        "width": largura_original,
        "height": altura_original,
        **apoio,
        "caveat": ressalvas or None,
    }


# ---------------------------------------------------------------------------
# Corpus e execução
# ---------------------------------------------------------------------------


def carrega_registros() -> list[dict[str, Any]]:
    with CANONICAL_RECORDS.open("r", encoding="utf-8") as arquivo:
        return [json.loads(linha) for linha in arquivo if linha.strip()]


def imagem_de(item_id: str) -> Path | None:
    for extensao in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff"):
        candidato = IMAGE_CACHE / f"{item_id}{extensao}"
        if candidato.exists() and candidato.stat().st_size > 0:
            return candidato
    return None


def agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Medição do Estrato I (LPAI v3).")
    alvo = parser.add_mutually_exclusive_group(required=True)
    alvo.add_argument("--all", action="store_true")
    alvo.add_argument("--items", help="item_id[,item_id,...]")
    parser.add_argument("--output", help="saída .jsonl em staging")
    parser.add_argument("--compare", action="store_true",
                        help="compara com a codificação humana existente")
    parser.add_argument("--dry-run", action="store_true", help="não grava")
    argumentos = parser.parse_args(argv)

    try:
        saida = assert_write_target(Path(argumentos.output) if argumentos.output else SAIDA)
    except GuardrailError as erro:
        print(f"[barreira] {erro}", file=sys.stderr)
        return 3

    try:
        registros = carrega_registros()
    except (OSError, json.JSONDecodeError) as erro:
        print(f"[fatal] {erro}", file=sys.stderr)
        return 1

    ids = {i.strip() for i in argumentos.items.split(",")} if argumentos.items else None
    linhas: list[dict[str, Any]] = []
    sem_imagem = 0
    suspeitas = 0

    for registro in registros:
        item_id = registro.get("item_id")
        if ids and item_id not in ids:
            continue
        caminho = imagem_de(item_id)
        if caminho is None:
            sem_imagem += 1
            continue
        try:
            medida = mede(caminho)
        except Exception as erro:  # noqa: BLE001
            print(f"[erro] {item_id}: {type(erro).__name__} {erro}", file=sys.stderr)
            continue

        humano = (registro.get("purificacao") or {}).get("monocromatizacao")
        linha = {
            "item_id": item_id,
            "proxy_only": True,
            "authority": "medicao_programatica",
            "target_field": "estrato_i.monocromatizacao_proposta",
            "merge_policy": "requires_human_confirmation",
            "image_path": str(caminho.relative_to(REPO)),
            "measured_at": agora(),
            **medida,
            "codificacao_humana_v2": humano,
        }
        if medida["caveat"]:
            suspeitas += 1
        linhas.append(linha)

    if not argumentos.dry_run and linhas:
        saida.parent.mkdir(parents=True, exist_ok=True)
        with saida.open("w", encoding="utf-8") as arquivo:
            for linha in linhas:
                arquivo.write(json.dumps(linha, ensure_ascii=False) + "\n")

    print(f"medidos: {len(linhas)} | sem imagem em cache: {sem_imagem} | "
          f"com ressalva: {suspeitas}", file=sys.stderr)
    if linhas:
        print(f"saída: {saida.relative_to(REPO)}", file=sys.stderr)

    distribuicao: dict[int, int] = {}
    for linha in linhas:
        valor = linha["monocromatizacao_proposta"]
        distribuicao[valor] = distribuicao.get(valor, 0) + 1
    print("\ndistribuição proposta (0 policromia → 3 monocromia):", file=sys.stderr)
    for valor in sorted(distribuicao):
        print(f"  {valor}: {distribuicao[valor]}", file=sys.stderr)

    if argumentos.compare:
        pares = [(l["codificacao_humana_v2"], l["monocromatizacao_proposta"])
                 for l in linhas if isinstance(l["codificacao_humana_v2"], int)]
        if pares:
            iguais = sum(1 for h, m in pares if h == m)
            um_grau = sum(1 for h, m in pares if abs(h - m) == 1)
            print(f"\ncontraste com a codificação v2 (n={len(pares)}):", file=sys.stderr)
            print(f"  idêntico:        {iguais} ({iguais/len(pares)*100:.0f}%)", file=sys.stderr)
            print(f"  1 grau de dif.:  {um_grau} ({um_grau/len(pares)*100:.0f}%)", file=sys.stderr)
            print(f"  2+ graus:        {len(pares)-iguais-um_grau}", file=sys.stderr)
            print("  (divergência não é erro da máquina nem da humana: é o lugar\n"
                  "   onde a definição operacional do atributo precisa de decisão)",
                  file=sys.stderr)

    return 2 if suspeitas else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
