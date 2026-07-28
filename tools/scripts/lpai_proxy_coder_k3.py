#!/usr/bin/env python3
"""
lpai_proxy_coder_k3.py — Codificador-proxy LPAI v2 sobre Kimi K3 (Moonshot AI).

Aplica o master prompt operacional do codebook (`schema/codebook-MASTER.md`,
§16) a itens do corpus ICONOCRACY e grava capta iconográfico *de proxy* em um
arquivo de staging separado. O objetivo é medir concordância (kappa) contra a
codificação humana cega, não substituí-la.

Instrumento e autoridade
------------------------
  * Instrumento: §16 do codebook MASTER, lido em tempo de execução. O script
    NÃO reescreve nem parafraseia o prompt — a fidelidade do instrumento é o
    que torna o kappa defensável. `codebook_version` é registrado em cada linha.
  * Autoridade: nenhuma. Toda linha nasce com `proxy_only: true` e
    `merge_policy: requires_human_adjudication`. A classe humana permanece
    vazia por construção.

Barreiras de escrita (guardrails)
---------------------------------
  1. `data/processed/records.jsonl` e os arquivos de export do corpus são
     abertos SOMENTE em leitura. Não existe caminho de código que os escreva.
  2. O destino de saída é validado antes de qualquer chamada de API:
     precisa ser `.jsonl`, precisa estar sob a raiz de staging e não pode ser
     — nem morar dentro de — nenhum arquivo/diretório canônico.
  3. Violação de barreira encerra o processo com código 3, antes de gastar
     um único token.

Nota metodológica pendente (ver corpo do PR)
--------------------------------------------
O §16 do codebook v2.2.0 pede `purificacao_composto` como média simples dos
10 indicadores. A virada qualitativa de julho/2026 removeu o escore agregado e
passou a tratar ENDURECIMENTO como inventário verbal de atributos. Enquanto a
divergência não é resolvida no codebook, este script emite os 10 indicadores
(capta ordinal previsto pelo schema) e um inventário verbal, mas **não** calcula
o composto — a menos que `--emit-composto` seja passado explicitamente.

Uso
---
    export MOONSHOT_API_KEY=sk-...
    python tools/scripts/lpai_proxy_coder_k3.py --dry-run --limit 3
    python tools/scripts/lpai_proxy_coder_k3.py --items <item_id>,<item_id>
    python tools/scripts/lpai_proxy_coder_k3.py --all --limit 40

Códigos de saída
----------------
    0 — sucesso; todos os itens codificados com confiança media|alta
    1 — erro fatal (I/O, API, instrumento ausente)
    2 — concluído, porém com itens de confiança baixa ou NC (sinal, não bloqueio)
    3 — violação de barreira de escrita (nada foi gravado, nada foi gasto)
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

REPO = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# Instrumento, entrada e saída
# ---------------------------------------------------------------------------

CODEBOOK_PATH = REPO / "schema" / "codebook-MASTER.md"
CANONICAL_RECORDS = REPO / "data" / "processed" / "records.jsonl"
DEFAULT_STAGING_ROOT = REPO / "data" / "staging"
DEFAULT_OUTPUT_NAME = "lpai-proxy-k3-runs.jsonl"
IMAGE_CACHE = REPO / ".cache" / "lpai-proxy-images"

AGENT_ID = "lpai-proxy-k3"
PROMPT_VERSION = "lpai-proxy-k3-v1"
MODEL_DEFAULT = "kimi-k3"
BASE_URL_DEFAULT = "https://api.moonshot.ai/v1"

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

REGIMES = ("fundacional", "normativo", "militar", "contra-alegoria")

RECUSA_TIPOS = (
    "substituicao_remasculinizante",
    "negacao_pura",
    "feminino_esvaziado",
    "substituicao_neutro_abstrata",
    "nenhuma",
)

# ---------------------------------------------------------------------------
# Barreiras de escrita
# ---------------------------------------------------------------------------

CANONICAL_WRITE_FORBIDDEN: tuple[Path, ...] = (
    REPO / "data" / "processed" / "records.jsonl",
    REPO / "corpus" / "corpus-data.json",
    REPO / "corpus" / "corpus-data.v2.json",
    REPO / "corpus" / "corpus-data-enriched.json",
    REPO / "corpus" / "companion-data.json",
)

FORBIDDEN_DIRS: tuple[Path, ...] = (
    REPO / "data" / "processed",
    REPO / "corpus",
    REPO / "examples",
    REPO / "schema",
    REPO / "tools" / "schemas",
)

FORBIDDEN_BASENAMES: frozenset[str] = frozenset(
    {
        "records.jsonl",
        "corpus-data.json",
        "corpus-data.v2.json",
        "corpus-data-enriched.json",
        "companion-data.json",
    }
)


class GuardrailError(RuntimeError):
    """Tentativa de escrever fora da área de staging do proxy."""


def staging_root() -> Path:
    """Raiz permitida para saída. Sobrescritível apenas para teste."""
    override = os.environ.get("LPAI_PROXY_STAGING_ROOT")
    return Path(override).resolve() if override else DEFAULT_STAGING_ROOT.resolve()


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def assert_write_target(candidate: str | Path) -> Path:
    """Valida o destino de saída ANTES de qualquer chamada de API.

    Regras, em ordem: extensão `.jsonl`; nome de arquivo que não colida com
    um artefato canônico; caminho que não seja nem more dentro de um arquivo
    ou diretório canônico; caminho contido na raiz de staging.
    """
    path = Path(candidate).expanduser()
    resolved = (path if path.is_absolute() else (Path.cwd() / path)).resolve()

    if resolved.suffix != ".jsonl":
        raise GuardrailError(
            f"saída precisa ser .jsonl (recebido: {resolved.name})"
        )

    if resolved.name in FORBIDDEN_BASENAMES:
        raise GuardrailError(
            f"'{resolved.name}' é nome de artefato canônico do corpus; "
            "o proxy nunca escreve nele"
        )

    for forbidden in CANONICAL_WRITE_FORBIDDEN:
        if resolved == forbidden.resolve():
            raise GuardrailError(f"destino canônico bloqueado: {resolved}")

    for directory in FORBIDDEN_DIRS:
        if _is_within(resolved, directory.resolve()):
            raise GuardrailError(
                f"'{directory.relative_to(REPO)}' guarda dados canônicos; "
                f"saída de proxy não entra ali: {resolved}"
            )

    root = staging_root()
    if not _is_within(resolved, root):
        raise GuardrailError(
            f"saída deve ficar sob {root} (recebido: {resolved})"
        )

    return resolved


# ---------------------------------------------------------------------------
# Instrumento
# ---------------------------------------------------------------------------


def load_master_prompt(codebook_path: Path = CODEBOOK_PATH) -> tuple[str, str]:
    """Extrai o master prompt operacional (§16) e a versão do codebook.

    Lê o codebook em vez de duplicar o prompt no código: o instrumento tem uma
    fonte única e a mudança dele fica visível no histórico do próprio codebook.
    """
    if not codebook_path.exists():
        raise FileNotFoundError(f"codebook não encontrado: {codebook_path}")

    text = codebook_path.read_text(encoding="utf-8")

    version_match = re.search(r"^codebook_version:\s*(.+)$", text, re.MULTILINE)
    version = version_match.group(1).strip() if version_match else "desconhecida"

    section = re.search(
        r"^## 16\..*?```text\n(.*?)```", text, re.MULTILINE | re.DOTALL
    )
    if not section:
        raise ValueError(
            "master prompt (§16) não encontrado em schema/codebook-MASTER.md"
        )

    return section.group(1).strip(), version


PROXY_PREAMBLE = """\
Você opera como CODIFICADOR-PROXY. Sua saída não tem autoridade: ela será
comparada a codificação humana cega para cálculo de concordância.

Restrições que se somam ao instrumento abaixo:
- Não infira país, data ou suporte que não estejam nos metadados fornecidos.
- Ausência significativa é dado negativo, não campo a preencher.
- Confiança baixa e NC são respostas legítimas e preferíveis a chute.
- Registre em `duvidas` tudo que precisa de decisão humana.
- Não calcule médias, índices ou escores compostos.
"""


def build_system_prompt(master_prompt: str) -> str:
    """Prefixo estável: constante entre chamadas, para aproveitar cache."""
    return f"{PROXY_PREAMBLE}\n--- INSTRUMENTO LPAI (codebook §16) ---\n{master_prompt}"


# ---------------------------------------------------------------------------
# Esquema de saída estruturada
# ---------------------------------------------------------------------------


def build_output_schema(emit_composto: bool = False) -> dict[str, Any]:
    indicadores = {
        key: {"type": "integer", "minimum": 0, "maximum": 3}
        for key in INDICATOR_KEYS
    }
    if emit_composto:
        indicadores["purificacao_composto"] = {
            "type": "number",
            "minimum": 0,
            "maximum": 3,
        }

    return {
        "type": "object",
        "required": [
            "item_id",
            "codificavel",
            "indicadores",
            "inventario_verbal",
            "confianca",
            "justificativa",
        ],
        "properties": {
            "item_id": {"type": "string"},
            "codificavel": {
                "type": "boolean",
                "description": "a evidência permite codificação visual suficiente",
            },
            "indicadores": {
                "type": "object",
                "required": list(INDICATOR_KEYS),
                "properties": indicadores,
            },
            "inventario_verbal": {
                "type": "array",
                "items": {"type": "string"},
                "description": "atributos observados em vocabulário iconográfico, sem escore",
            },
            "familia_alegorica": {
                "type": "string",
                "description": "Justitia, Libertas, Respublica, Marianne, Germania, "
                "Britannia, Columbia, outra, ou NC",
            },
            "subtipo": {"type": "string"},
            "regime_iconocratico": {
                "type": "string",
                "enum": [*REGIMES, "NC"],
            },
            "recusa": {"type": "string", "enum": list(RECUSA_TIPOS)},
            "genero_atribuido": {"type": "string"},
            "funcao_juridica": {"type": "string"},
            "dado_negativo": {
                "type": "array",
                "items": {"type": "string"},
                "description": "ausências analiticamente relevantes",
            },
            "subaltern_caution": {"type": "boolean"},
            "confianca": {"type": "string", "enum": ["alta", "media", "baixa"]},
            "nc_causa": {
                "type": "string",
                "description": "obrigatório quando codificavel=false: "
                "evidencia_insuficiente | ambiguidade | fora_de_escopo | sem_imagem",
            },
            "justificativa": {
                "type": "string",
                "description": "o que na evidência sustenta a codificação",
            },
            "duvidas": {"type": "array", "items": {"type": "string"}},
        },
    }


# ---------------------------------------------------------------------------
# Corpus (leitura) e seleção
# ---------------------------------------------------------------------------


def load_records(path: Path = CANONICAL_RECORDS) -> list[dict[str, Any]]:
    """Leitura estrita do ledger canônico. Nunca abre em modo de escrita."""
    if not path.exists():
        raise FileNotFoundError(f"registros canônicos ausentes: {path}")
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number} JSON inválido: {exc}") from exc
    return records


def select_items(
    records: Iterable[dict[str, Any]],
    item_ids: list[str] | None,
    regime: str | None,
    coded_by: str | None,
    limit: int | None,
    done: set[str],
    force: bool,
) -> list[dict[str, Any]]:
    selected = []
    for record in records:
        item_id = record.get("item_id")
        if not item_id:
            continue
        if item_ids and item_id not in item_ids:
            continue
        purificacao = record.get("purificacao") or {}
        if regime and purificacao.get("regime_iconocratico") != regime:
            continue
        if coded_by and purificacao.get("coded_by") != coded_by:
            continue
        if not force and item_id in done:
            continue
        selected.append(record)
    if limit is not None:
        selected = selected[:limit]
    return selected


def load_done(output_path: Path) -> set[str]:
    """Retomada: itens já presentes na saída de staging."""
    if not output_path.exists():
        return set()
    done: set[str] = set()
    with output_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                done.add(json.loads(line).get("item_id", ""))
            except json.JSONDecodeError:
                continue
    done.discard("")
    return done


# ---------------------------------------------------------------------------
# Evidência visual — K3 aceita base64, não URL pública
# ---------------------------------------------------------------------------

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff"}
MIME_BY_SUFFIX = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
}


def local_image_for(item_id: str, images_dir: Path | None) -> Path | None:
    if images_dir is None:
        return None
    for suffix in IMAGE_SUFFIXES:
        candidate = images_dir / f"{item_id}{suffix}"
        if candidate.exists():
            return candidate
    return None


def cached_download(url: str, item_id: str) -> Path | None:
    """Baixa a imagem para cache local. PDFs e HTML são recusados de propósito:
    o proxy só codifica o que consegue ver."""
    suffix = Path(url.split("?")[0]).suffix.lower()
    if suffix not in IMAGE_SUFFIXES:
        return None

    IMAGE_CACHE.mkdir(parents=True, exist_ok=True)
    target = IMAGE_CACHE / f"{item_id}{suffix}"
    if target.exists() and target.stat().st_size > 0:
        return target

    try:
        import requests  # dependência opcional, só no caminho de download
    except ImportError:  # pragma: no cover
        print("[aviso] requests ausente; use --images-dir", file=sys.stderr)
        return None

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except Exception as exc:  # noqa: BLE001 - rede é ruidosa por natureza
        print(f"[aviso] download falhou ({item_id}): {exc}", file=sys.stderr)
        return None

    target.write_bytes(response.content)
    return target


def encode_image(path: Path) -> tuple[str, str]:
    mime = MIME_BY_SUFFIX.get(path.suffix.lower(), "image/jpeg")
    return base64.b64encode(path.read_bytes()).decode("ascii"), mime


def build_user_content(
    record: dict[str, Any], image_b64: str | None, mime: str | None
) -> list[dict[str, Any]]:
    entrada = record.get("input") or {}
    metadados = {
        "item_id": record.get("item_id"),
        "titulo": entrada.get("title_hint"),
        "data": entrada.get("date_hint"),
        "local": entrada.get("place_hint"),
        "fonte": entrada.get("input_url"),
        "evidencia_webscout": (record.get("webscout") or {}).get("summary_evidence"),
        "lacunas_declaradas": (record.get("webscout") or {}).get("gaps"),
    }
    texto = (
        "Codifique o item abaixo conforme o instrumento LPAI.\n\n"
        f"METADADOS CONHECIDOS (não os contradiga, não os complete por inferência):\n"
        f"{json.dumps(metadados, ensure_ascii=False, indent=2)}\n\n"
    )
    if image_b64:
        texto += "A imagem do item segue anexada."
    else:
        texto += (
            "SEM IMAGEM DISPONÍVEL. Se a evidência textual não sustentar a "
            "codificação visual, responda codificavel=false com "
            "nc_causa=sem_imagem e confianca=baixa."
        )

    content: list[dict[str, Any]] = [{"type": "text", "text": texto}]
    if image_b64:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime};base64,{image_b64}"},
            }
        )
    return content


# ---------------------------------------------------------------------------
# Chamada ao modelo
# ---------------------------------------------------------------------------


def make_client(base_url: str):
    try:
        from openai import OpenAI
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("pip install openai") from exc

    api_key = os.environ.get("MOONSHOT_API_KEY")
    if not api_key:
        raise RuntimeError("defina MOONSHOT_API_KEY no ambiente")
    return OpenAI(api_key=api_key, base_url=base_url)


def call_model(
    client: Any,
    model: str,
    system_prompt: str,
    user_content: list[dict[str, Any]],
    schema: dict[str, Any],
    retries: int = 1,
) -> dict[str, Any]:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "registrar_codificacao",
                "description": "Registra a codificação LPAI de proxy do item.",
                "parameters": schema,
            },
        }
    ]
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    # prefixo estável primeiro: maximiza acerto de cache
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                tools=tools,
                tool_choice={
                    "type": "function",
                    "function": {"name": "registrar_codificacao"},
                },
            )
            call = response.choices[0].message.tool_calls[0]
            payload = json.loads(call.function.arguments)
            usage = getattr(response, "usage", None)
            payload["_usage"] = (
                usage.model_dump() if hasattr(usage, "model_dump") else None
            )
            return payload
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"chamada ao modelo falhou: {last_error}")


# ---------------------------------------------------------------------------
# Linha de staging
# ---------------------------------------------------------------------------


def build_row(
    record: dict[str, Any],
    coded: dict[str, Any],
    *,
    model: str,
    codebook_version: str,
    image_source: str | None,
) -> dict[str, Any]:
    """Envelope de proxy. Os campos de autoridade nascem vazios de propósito."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )
    usage = coded.pop("_usage", None)
    purificacao_humana = (record.get("purificacao") or {}).get("coded_by")

    return {
        "item_id": record.get("item_id"),
        "item_hash": record.get("item_hash"),
        "proxy_only": True,
        "authority": "proxy",
        "target_field": "purificacao_proposta",
        "merge_policy": "requires_human_adjudication",
        "human_class": None,
        "human_coded_by_at_read_time": purificacao_humana,
        "capta_declaration": (
            "LPAI v2-capta: scores são atos interpretativos situados, "
            "não dados neutros."
        ),
        "coded_by": AGENT_ID,
        "coded_at": now,
        "model": model,
        "prompt_version": PROMPT_VERSION,
        "codebook_version": codebook_version,
        "image_source": image_source,
        "usage": usage,
        "proposta": coded,
    }


def append_row(output_path: Path, row: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Codificador-proxy LPAI v2 sobre Kimi K3 (saída em staging)."
    )
    alvo = parser.add_mutually_exclusive_group(required=True)
    alvo.add_argument("--items", help="item_id[,item_id,...]")
    alvo.add_argument("--all", action="store_true", help="todos os registros")

    parser.add_argument("--regime", choices=REGIMES, help="filtra por regime")
    parser.add_argument("--coded-by", help="filtra pela origem de codificação")
    parser.add_argument("--limit", type=int, help="teto de itens no lote")
    parser.add_argument("--output", help="caminho de staging (.jsonl)")
    parser.add_argument("--images-dir", help="diretório de imagens locais <item_id>.<ext>")
    parser.add_argument(
        "--allow-textual",
        action="store_true",
        help="codificar itens sem imagem (registro é marcado sem_imagem)",
    )
    parser.add_argument(
        "--emit-composto",
        action="store_true",
        help="opt-in explícito: pedir purificacao_composto (ver nota metodológica)",
    )
    parser.add_argument("--model", default=MODEL_DEFAULT)
    parser.add_argument("--base-url", default=BASE_URL_DEFAULT)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--force", action="store_true", help="recodificar já feitos")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="valida barreiras, seleção e evidência; não chama a API nem grava",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    output_default = staging_root() / DEFAULT_OUTPUT_NAME
    try:
        output_path = assert_write_target(args.output or output_default)
    except GuardrailError as exc:
        print(f"[barreira] {exc}", file=sys.stderr)
        return 3

    try:
        master_prompt, codebook_version = load_master_prompt()
        records = load_records()
    except (FileNotFoundError, ValueError) as exc:
        print(f"[fatal] {exc}", file=sys.stderr)
        return 1

    item_ids = (
        [i.strip() for i in args.items.split(",") if i.strip()] if args.items else None
    )
    done = set() if args.force else load_done(output_path)
    selected = select_items(
        records,
        item_ids,
        args.regime,
        args.coded_by,
        args.limit,
        done,
        args.force,
    )

    print(
        f"corpus: {len(records)} registros | codebook {codebook_version} | "
        f"selecionados: {len(selected)} | já em staging: {len(done)}",
        file=sys.stderr,
    )
    print(f"saída: {output_path}", file=sys.stderr)
    if not selected:
        print("nada a fazer.", file=sys.stderr)
        return 0

    images_dir = Path(args.images_dir).expanduser() if args.images_dir else None
    schema = build_output_schema(emit_composto=args.emit_composto)
    system_prompt = build_system_prompt(master_prompt)

    client = None
    if not args.dry_run:
        try:
            client = make_client(args.base_url)
        except RuntimeError as exc:
            print(f"[fatal] {exc}", file=sys.stderr)
            return 1

    baixa_confianca = 0
    sem_imagem = 0
    falhas = 0

    for index, record in enumerate(selected, start=1):
        item_id = record["item_id"]
        entrada = record.get("input") or {}

        image_path = local_image_for(item_id, images_dir)
        if image_path is None and not args.dry_run:
            url = entrada.get("input_url") or ""
            image_path = cached_download(url, item_id) if url else None

        if image_path is None:
            sem_imagem += 1
            if not args.allow_textual:
                print(
                    f"[{index}/{len(selected)}] {item_id}: sem imagem — pulado "
                    "(use --allow-textual para codificar só com texto)",
                    file=sys.stderr,
                )
                continue

        image_b64 = mime = None
        if image_path is not None and not args.dry_run:
            image_b64, mime = encode_image(image_path)

        user_content = build_user_content(record, image_b64, mime)

        if args.dry_run:
            print(
                f"[{index}/{len(selected)}] {item_id}: "
                f"imagem={'sim' if image_path else 'não'} | "
                f"título={entrada.get('title_hint')!r}",
                file=sys.stderr,
            )
            continue

        try:
            coded = call_model(
                client, args.model, system_prompt, user_content, schema, args.retries
            )
        except RuntimeError as exc:
            falhas += 1
            print(f"[erro] {item_id}: {exc}", file=sys.stderr)
            continue

        coded.setdefault("item_id", item_id)
        if coded.get("item_id") != item_id:
            coded["item_id"] = item_id  # o proxy não renomeia itens

        row = build_row(
            record,
            coded,
            model=args.model,
            codebook_version=codebook_version,
            image_source=str(image_path) if image_path else None,
        )
        append_row(output_path, row)

        confianca = coded.get("confianca", "baixa")
        if confianca == "baixa" or not coded.get("codificavel", True):
            baixa_confianca += 1
        print(
            f"[{index}/{len(selected)}] {item_id}: confiança={confianca} "
            f"regime={coded.get('regime_iconocratico')}",
            file=sys.stderr,
        )

    print(
        f"\nfim | baixa confiança/NC: {baixa_confianca} | sem imagem: {sem_imagem} "
        f"| falhas: {falhas}",
        file=sys.stderr,
    )
    print(
        "revisão humana obrigatória antes de qualquer merge no corpus canônico.",
        file=sys.stderr,
    )

    if falhas:
        return 1
    return 2 if baixa_confianca else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
