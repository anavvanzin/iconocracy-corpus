#!/usr/bin/env python3
"""
lpai_proxy_coder_k3.py — Codificador-proxy LPAI v2 sobre Kimi K3 (Moonshot AI).

Aplica o master prompt operacional do codebook
(`docs/methodology/codebooks/codebook-MASTER.md`, §16) a itens do corpus
ICONOCRACY e grava capta iconográfico *de proxy* em um arquivo de staging
separado. O objetivo é apoiar diagnóstico interno contra codificação humana,
não substituí-la.

Instrumento e autoridade
------------------------
  * Instrumento: §16 do codebook MASTER, lido em tempo de execução. O script
    NÃO reescreve nem parafraseia o prompt — a fidelidade do instrumento é o
    que preserva a rastreabilidade. `codebook_version` é registrado em cada linha.
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

Índice composto: aposentado
---------------------------
O codebook v2.2.1 aposentou `purificacao_composto` (decisão
`docs/decisions/2026-07-28-aposentadoria-do-indice-composto.md`). Os 10
indicadores permanecem como capta ordinal; a agregação sai. Este script emite os
indicadores e um inventário verbal de atributos, e o esquema de saída **não tem**
campo de composto — não há flag que o reintroduza.

Uso
---
    export MOONSHOT_API_KEY=sk-...
    python tools/scripts/lpai_proxy_coder_k3.py --version
    python tools/scripts/lpai_proxy_coder_k3.py --all --dry-run --limit 3
    python tools/scripts/lpai_proxy_coder_k3.py --items <item_id>,<item_id>
    python tools/scripts/lpai_proxy_coder_k3.py --all --limit 40

Códigos de saída
----------------
    0 — sucesso; todos os itens codificados com confiança media|alta
    1 — erro fatal (I/O, API, instrumento ausente)
    2 — concluído com baixa confiança/NC ou item pulado sem evidência
    3 — violação de barreira de escrita (nada foi gravado, nada foi gasto)
"""

from __future__ import annotations

import argparse
import base64
import copy
import fcntl
import ipaddress
import json
import os
import re
import secrets
import socket
import stat
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin, urlsplit

REPO = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# Instrumento, entrada e saída
# ---------------------------------------------------------------------------

SCRIPT_VERSION = "1.3.0"
PROXY_SCHEMA_VERSION = "1.0.0"
CODEBOOK_PATH = REPO / "docs" / "methodology" / "codebooks" / "codebook-MASTER.md"
PROXY_SCHEMA_PATH = REPO / "tools" / "schemas" / "lpai-proxy-record.schema.json"
CANONICAL_RECORDS = REPO / "data" / "processed" / "records.jsonl"
DEFAULT_STAGING_ROOT = REPO / "data" / "staging"
DEFAULT_OUTPUT_NAME = "lpai-proxy-k3-schema-v1-runs.jsonl"
IMAGE_CACHE = REPO / ".cache" / "lpai-proxy-images"

AGENT_ID = "lpai-proxy-k3"
PROMPT_VERSION = "lpai-proxy-k3-v2"  # v2: composto aposentado (DEC-2026-07-28)
MODEL_DEFAULT = "kimi-k3"
BASE_URL_DEFAULT = "https://api.moonshot.ai/v1"
IMAGE_MAX_BYTES = 10 * 1024 * 1024
IMAGE_CHUNK_BYTES = 64 * 1024
MAX_REDIRECTS = 5
SOURCE_BLOCK_MAX_CHARS = 4_000
SOURCE_STRING_MAX_CHARS = 1_000
SOURCE_LIST_MAX_ITEMS = 5
SOURCE_DICT_MAX_ITEMS = 12

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

# ---------------------------------------------------------------------------
# Barreiras de escrita
# ---------------------------------------------------------------------------

CANONICAL_WRITE_FORBIDDEN: tuple[Path, ...] = (
    REPO / "data" / "processed" / "records.jsonl",
    REPO / "data" / "processed" / "purification.jsonl",
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
        "purification.jsonl",
        "corpus-data.json",
        "corpus-data.v2.json",
        "corpus-data-enriched.json",
        "companion-data.json",
    }
)


class GuardrailError(RuntimeError):
    """Tentativa de escrever fora da área de staging do proxy."""


def _canonical_artifact_paths() -> tuple[Path, ...]:
    """Artefatos conhecidos mais qualquer corpus-data*.json existente."""
    candidates = list(CANONICAL_WRITE_FORBIDDEN)
    candidates.extend(sorted((REPO / "corpus").glob("corpus-data*.json")))
    return tuple(dict.fromkeys(candidates))


def _assert_safe_file_identity(
    fd: int, path: Path | str, *, purpose: str
) -> os.stat_result:
    """Exige inode regular, sem hardlinks e distinto dos artefatos canônicos."""
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode):
        raise GuardrailError(f"{purpose} não é arquivo regular: {path}")
    for canonical in _canonical_artifact_paths():
        try:
            canonical_info = canonical.stat()
        except (FileNotFoundError, OSError):
            continue
        if (info.st_dev, info.st_ino) == (
            canonical_info.st_dev,
            canonical_info.st_ino,
        ):
            raise GuardrailError(
                f"{purpose} compartilha inode com artefato canônico: {canonical}"
            )
    if info.st_nlink != 1:
        raise GuardrailError(
            f"{purpose} recusado: número de hardlinks precisa ser 1 "
            f"(recebido: {info.st_nlink}): {path}"
        )
    return info


def staging_root() -> Path:
    """Raiz lexical fixa; a abertura por descritor recusa symlinks em cada componente."""
    return Path(os.path.abspath(DEFAULT_STAGING_ROOT))


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
    if ".." in path.parts:
        raise GuardrailError("componentes '..' são proibidos no destino")
    lexical = Path(os.path.abspath(path if path.is_absolute() else Path.cwd() / path))
    try:
        resolved = lexical.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise GuardrailError(f"não foi possível resolver o destino: {path}") from exc

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
    root_resolved = root.resolve(strict=False)
    if not _is_within(resolved, root_resolved):
        raise GuardrailError(
            f"saída deve ficar sob {root_resolved} (recebido: {resolved})"
        )

    return lexical


def _open_directory_nofollow(path: Path, *, create: bool) -> int:
    """Abre um diretório absoluto componente a componente, sem seguir symlinks."""
    absolute = Path(os.path.abspath(path))
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    current_fd = os.open("/", flags)
    try:
        for component in absolute.parts[1:]:
            try:
                next_fd = os.open(component, flags, dir_fd=current_fd)
            except FileNotFoundError:
                if not create:
                    raise
                os.mkdir(component, mode=0o700, dir_fd=current_fd)
                next_fd = os.open(component, flags, dir_fd=current_fd)
            os.close(current_fd)
            current_fd = next_fd
        return current_fd
    except Exception:
        os.close(current_fd)
        raise


def _open_staging_parent(output_path: Path, *, create: bool) -> tuple[int, str]:
    """Revalida e abre o pai sob staging por descritor (openat/no-follow)."""
    safe_path = assert_write_target(output_path)
    try:
        relative = safe_path.relative_to(staging_root())
    except ValueError as exc:  # defesa em profundidade
        raise GuardrailError("destino não é lexicalmente relativo a staging") from exc
    if not relative.parts or relative.name in {"", ".", ".."}:
        raise GuardrailError("nome de saída inválido")
    try:
        parent_fd = _open_directory_nofollow(
            staging_root().joinpath(*relative.parts[:-1]), create=create
        )
    except FileNotFoundError:
        raise
    except (OSError, RuntimeError) as exc:
        raise GuardrailError(
            "staging ou ancestral do destino não é diretório real sem symlink"
        ) from exc
    return parent_fd, relative.name


def _validate_jsonl_fd(
    fd: int, path: Path, *, validator: Any | None = None
) -> set[str]:
    """Valida integralmente JSONL já existente usando o mesmo descritor aberto."""
    if validator is None:
        validator = get_proxy_validator()
    info = _assert_safe_file_identity(fd, path, purpose="saída existente")
    if info.st_size == 0:
        return set()

    os.lseek(fd, 0, os.SEEK_SET)
    raw = bytearray()
    while chunk := os.read(fd, 64 * 1024):
        raw.extend(chunk)
    if not raw.endswith(b"\n"):
        raise ValueError(f"{path}: JSONL truncado: última linha não termina em newline")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: JSONL não é UTF-8 válido") from exc

    done: set[str] = set()
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number} JSON inválido: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: cada linha deve ser objeto JSON")
        try:
            validate_proxy_row(value, validator=validator)
        except ValueError as exc:
            raise ValueError(
                f"{path}:{line_number}: linha fora de "
                f"lpai-proxy-record.schema.json: {exc}"
            ) from exc
        item_id = value["item_id"]
        done.add(item_id)
    return done


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
            "master prompt (§16) não encontrado em "
            "docs/methodology/codebooks/codebook-MASTER.md"
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
- Não calcule médias, índices ou escores compostos: o índice composto está
  aposentado desde o codebook v2.2.1. Em lugar dele, registre inventario_verbal.
"""


def build_system_prompt(master_prompt: str) -> str:
    """Prefixo estável: constante entre chamadas, para aproveitar cache."""
    return f"{PROXY_PREAMBLE}\n--- INSTRUMENTO LPAI (codebook §16) ---\n{master_prompt}"


# ---------------------------------------------------------------------------
# Esquema de saída estruturada
# ---------------------------------------------------------------------------


def load_proxy_schema(schema_path: Path | None = None) -> dict[str, Any]:
    """Lê o schema atual e devolve um objeto novo, não retido pelo validator."""
    schema_path = schema_path or PROXY_SCHEMA_PATH
    try:
        schema_bytes = schema_path.read_bytes()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"schema do proxy não encontrado: {schema_path}") from exc
    try:
        return json.loads(schema_bytes)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"schema do proxy inválido: {schema_path}: {exc}") from exc


@lru_cache(maxsize=8)
def _validator_from_schema_bytes(schema_bytes: bytes) -> Any:
    """Cacheia validator somente pela cópia imutável exata do schema."""
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from jsonschema.exceptions import SchemaError
    except ImportError as exc:  # pragma: no cover - requirements.txt inclui jsonschema
        raise RuntimeError("pip install jsonschema") from exc

    schema = json.loads(schema_bytes)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise ValueError(f"contrato JSON Schema inválido: {exc.message}") from exc
    return Draft202012Validator(schema, format_checker=FormatChecker())


def get_proxy_validator(schema_path: Path | None = None) -> Any:
    """Relê bytes atuais; só reutiliza construção quando o conteúdo é idêntico."""
    schema_path = schema_path or PROXY_SCHEMA_PATH
    try:
        schema_bytes = schema_path.read_bytes()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"schema do proxy não encontrado: {schema_path}") from exc
    try:
        return _validator_from_schema_bytes(schema_bytes)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"schema do proxy inválido: {schema_path}: {exc}") from exc


def build_output_schema() -> dict[str, Any]:
    """Retorna o subesquema entregue ao modelo para a proposta LPAI.

    Não existe campo de índice composto: `purificacao_composto` está aposentado
    desde o codebook v2.2.1 e a proibição vive no schema persistido.
    """
    schema = load_proxy_schema()
    return copy.deepcopy(schema["$defs"]["proposal"])


def validate_proxy_row(row: dict[str, Any], *, validator: Any | None = None) -> None:
    """Valida uma linha completa antes de criar ou abrir a saída."""
    if validator is None:
        validator = get_proxy_validator()
    errors = sorted(validator.iter_errors(row), key=lambda error: list(error.path))
    if errors:
        details = "; ".join(
            f"{'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ValueError(f"linha de staging inválida: {details}")


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
    """Retomada fail-closed: toda linha existente precisa ser JSONL íntegro."""
    try:
        parent_fd, name = _open_staging_parent(output_path, create=False)
    except FileNotFoundError:
        return set()
    try:
        try:
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
        except FileNotFoundError:
            return set()
        except OSError as exc:
            raise GuardrailError("saída existente é symlink ou não pode ser aberta") from exc
        try:
            fcntl.flock(fd, fcntl.LOCK_SH)
            try:
                return _validate_jsonl_fd(fd, output_path)
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)
    finally:
        os.close(parent_fd)


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
SUFFIX_BY_MIME = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/tiff": ".tiff",
}


def local_image_for(item_id: str, images_dir: Path | None) -> Path | None:
    if images_dir is None:
        return None
    if not re.fullmatch(r"[A-Za-z0-9._-]+", item_id):
        return None
    for suffix in IMAGE_SUFFIXES:
        candidate = images_dir / f"{item_id}{suffix}"
        if candidate.exists():
            return candidate
    return None


def _validate_public_http_url(url: str) -> str:
    """Recusa esquemas não HTTP e qualquer resolução não global."""
    parsed = urlsplit(url)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise ValueError("URL de imagem precisa usar http ou https")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("credenciais embutidas em URL são proibidas")
    hostname = parsed.hostname.rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError("localhost é proibido")

    port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)
    try:
        addresses = socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValueError(f"host de imagem não pôde ser resolvido: {hostname}") from exc
    if not addresses:
        raise ValueError(f"host de imagem sem endereço resolvido: {hostname}")
    _require_global_addresses(addresses)
    return url


def _require_global_addresses(addresses: list[tuple[Any, ...]]) -> None:
    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])
        if not ip.is_global:
            raise ValueError(f"endereço de imagem não público é proibido: {ip}")


@contextmanager
def _public_dns_only():
    """Revalida também a resolução feita pelo cliente no instante da conexão."""
    original_getaddrinfo = socket.getaddrinfo

    def guarded_getaddrinfo(*args, **kwargs):
        addresses = original_getaddrinfo(*args, **kwargs)
        if not addresses:
            raise OSError("resolução sem endereços")
        _require_global_addresses(addresses)
        return addresses

    socket.getaddrinfo = guarded_getaddrinfo
    try:
        yield
    finally:
        socket.getaddrinfo = original_getaddrinfo


def _image_mime_from_signature(prefix: bytes) -> str | None:
    if prefix.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if prefix.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if prefix.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    if len(prefix) >= 12 and prefix[:4] == b"RIFF" and prefix[8:12] == b"WEBP":
        return "image/webp"
    if prefix.startswith((b"II*\x00", b"MM\x00*")):
        return "image/tiff"
    return None


def _existing_regular_cache_file(parent_fd: int, name: str) -> bool:
    try:
        info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return False
    if stat.S_ISLNK(info.st_mode):
        raise GuardrailError(f"cache recusado: {name} é symlink")
    if not stat.S_ISREG(info.st_mode):
        raise GuardrailError(f"cache recusado: {name} não é arquivo regular")
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
    try:
        info = _assert_safe_file_identity(fd, name, purpose="arquivo de cache")
        if info.st_size == 0:
            return False
        prefix = os.read(fd, 16)
    finally:
        os.close(fd)
    expected_mime = MIME_BY_SUFFIX.get(Path(name).suffix.lower())
    if _image_mime_from_signature(prefix) != expected_mime:
        raise ValueError(f"cache existente tem assinatura inválida: {name}")
    return True


def _download_response(url: str):
    """Segue redirects manualmente, validando cada destino antes da requisição."""
    try:
        import requests  # dependência opcional, só no caminho de download
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("requests ausente; use --images-dir") from exc

    session = requests.Session()
    session.trust_env = False
    current = url
    for redirect_count in range(MAX_REDIRECTS + 1):
        _validate_public_http_url(current)
        with _public_dns_only():
            response = session.get(
                current,
                allow_redirects=False,
                stream=True,
                timeout=(5, 30),
            )
        if 300 <= response.status_code < 400:
            location = response.headers.get("Location")
            response.close()
            if not location:
                raise ValueError("redirect sem Location")
            if redirect_count >= MAX_REDIRECTS:
                raise ValueError("limite de redirects excedido")
            current = urljoin(current, location)
            _validate_public_http_url(current)
            continue
        response.raise_for_status()
        _validate_public_http_url(response.url)
        return response
    raise ValueError("limite de redirects excedido")  # pragma: no cover


def cached_download(url: str, item_id: str) -> Path | None:
    """Baixa imagem pública, limitada e autenticada por MIME + assinatura."""
    if not re.fullmatch(r"[A-Za-z0-9._-]+", item_id):
        print(f"[aviso] item_id inseguro para cache: {item_id!r}", file=sys.stderr)
        return None
    response = None
    try:
        _validate_public_http_url(url)
        cache_fd = _open_directory_nofollow(IMAGE_CACHE, create=True)
        try:
            for suffix in sorted(set(SUFFIX_BY_MIME.values())):
                name = f"{item_id}{suffix}"
                if _existing_regular_cache_file(cache_fd, name):
                    return IMAGE_CACHE / name

            response = _download_response(url)
            content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            suffix = SUFFIX_BY_MIME.get(content_type)
            if suffix is None:
                raise ValueError(f"Content-Type não suportado: {content_type or '<ausente>'}")
            content_length = response.headers.get("Content-Length")
            if content_length is not None and int(content_length) > IMAGE_MAX_BYTES:
                raise ValueError(f"imagem excede limite de {IMAGE_MAX_BYTES} bytes")

            target_name = f"{item_id}{suffix}"
            if _existing_regular_cache_file(cache_fd, target_name):
                return IMAGE_CACHE / target_name
            temp_name = f".{item_id}.{secrets.token_hex(8)}.tmp"
            temp_fd = os.open(
                temp_name,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
                dir_fd=cache_fd,
            )
            total = 0
            prefix = bytearray()
            try:
                _assert_safe_file_identity(
                    temp_fd, temp_name, purpose="arquivo temporário de cache"
                )
                for chunk in response.iter_content(chunk_size=IMAGE_CHUNK_BYTES):
                    if not chunk:
                        continue
                    total += len(chunk)
                    if total > IMAGE_MAX_BYTES:
                        raise ValueError(f"imagem excede limite de {IMAGE_MAX_BYTES} bytes")
                    if len(prefix) < 16:
                        prefix.extend(chunk[: 16 - len(prefix)])
                    view = memoryview(chunk)
                    while view:
                        written = os.write(temp_fd, view)
                        if written <= 0:  # pragma: no cover - falha de filesystem
                            raise OSError("escrita de cache incompleta")
                        view = view[written:]
                if total == 0:
                    raise ValueError("imagem vazia")
                signature_mime = _image_mime_from_signature(bytes(prefix))
                if signature_mime != content_type:
                    raise ValueError(
                        "assinatura do conteúdo não corresponde ao Content-Type de imagem"
                    )
                _assert_safe_file_identity(
                    temp_fd, temp_name, purpose="arquivo temporário de cache"
                )
                os.fsync(temp_fd)
            except Exception:
                os.close(temp_fd)
                os.unlink(temp_name, dir_fd=cache_fd)
                raise
            else:
                os.close(temp_fd)

            try:
                target_exists = _existing_regular_cache_file(cache_fd, target_name)
            except Exception:
                os.unlink(temp_name, dir_fd=cache_fd)
                raise
            if target_exists:
                os.unlink(temp_name, dir_fd=cache_fd)
                return IMAGE_CACHE / target_name
            try:
                os.replace(
                    temp_name,
                    target_name,
                    src_dir_fd=cache_fd,
                    dst_dir_fd=cache_fd,
                )
            except Exception:
                try:
                    os.unlink(temp_name, dir_fd=cache_fd)
                except FileNotFoundError:
                    pass
                raise
            return IMAGE_CACHE / target_name
        finally:
            os.close(cache_fd)
    except Exception as exc:  # noqa: BLE001 - rede é ruidosa por natureza
        print(f"[aviso] download falhou ({item_id}): {exc}", file=sys.stderr)
        return None
    finally:
        if response is not None:
            response.close()


def encode_image(path: Path) -> tuple[str, str]:
    mime = MIME_BY_SUFFIX.get(path.suffix.lower(), "image/jpeg")
    parent_fd = _open_directory_nofollow(path.parent, create=False)
    try:
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
        try:
            info = _assert_safe_file_identity(
                fd, path, purpose="arquivo de evidência/cache"
            )
            if info.st_size > IMAGE_MAX_BYTES:
                raise ValueError(f"imagem excede limite de {IMAGE_MAX_BYTES} bytes")
            chunks = bytearray()
            while chunk := os.read(fd, IMAGE_CHUNK_BYTES):
                chunks.extend(chunk)
                if len(chunks) > IMAGE_MAX_BYTES:
                    raise ValueError(f"imagem excede limite de {IMAGE_MAX_BYTES} bytes")
        finally:
            os.close(fd)
    finally:
        os.close(parent_fd)
    signature_mime = _image_mime_from_signature(bytes(chunks[:16]))
    if signature_mime != mime:
        raise ValueError("extensão da imagem não corresponde à assinatura suportada")
    return base64.b64encode(chunks).decode("ascii"), mime


def _bounded_source_value(value: Any, *, depth: int = 0) -> Any:
    """Reduz metadados auxiliares sem transformar seu conteúdo substantivo."""
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        if len(value) <= SOURCE_STRING_MAX_CHARS:
            return value
        return value[:SOURCE_STRING_MAX_CHARS] + "… [truncado]"
    if depth >= 3:
        return "… [profundidade truncada]"
    if isinstance(value, dict):
        limited: dict[str, Any] = {}
        for index, (key, nested) in enumerate(value.items()):
            if index >= SOURCE_DICT_MAX_ITEMS:
                limited["_truncado"] = "campos adicionais omitidos"
                break
            limited[str(key)] = _bounded_source_value(nested, depth=depth + 1)
        return limited
    if isinstance(value, (list, tuple)):
        limited = [
            _bounded_source_value(nested, depth=depth + 1)
            for nested in value[:SOURCE_LIST_MAX_ITEMS]
        ]
        if len(value) > SOURCE_LIST_MAX_ITEMS:
            limited.append("… [itens adicionais omitidos]")
        return limited
    return _bounded_source_value(str(value), depth=depth + 1)


def _render_source_block(label: str, value: Any) -> str:
    rendered = json.dumps(
        _bounded_source_value(value), ensure_ascii=False, indent=2
    )
    if len(rendered) > SOURCE_BLOCK_MAX_CHARS:
        rendered = rendered[:SOURCE_BLOCK_MAX_CHARS] + "\n… [bloco truncado]"
    return f"FONTE {label}:\n{rendered}"


def build_user_content(
    record: dict[str, Any], image_b64: str | None, mime: str | None
) -> list[dict[str, Any]]:
    entrada = record.get("input") or {}
    purificacao = record.get("purificacao") or {}
    webscout = record.get("webscout") or {}
    ledger_input = {
        "item_id": record.get("item_id"),
        "titulo": entrada.get("title_hint"),
        "data": entrada.get("date_hint"),
        "local": entrada.get("place_hint"),
        "url_de_entrada": entrada.get("input_url"),
    }
    previous_purification = {
        "suporte_medium": (purificacao.get("record_metadata") or {}).get(
            "medium"
        ),
        "notas_anteriores": purificacao.get("notes"),
    }
    webscout_evidence = {
        "evidencia_resumida": webscout.get("summary_evidence"),
        "lacunas_declaradas": webscout.get("gaps"),
    }
    if webscout.get("search_results"):
        webscout_evidence["resultados_de_busca"] = webscout["search_results"]
    source_blocks = "\n\n".join(
        (
            _render_source_block("ledger.input", ledger_input),
            _render_source_block(
                "purificacao preexistente (record_metadata.medium e notes)",
                previous_purification,
            ),
            _render_source_block(
                "webscout (summary_evidence, gaps e search_results)",
                webscout_evidence,
            ),
        )
    )
    texto = (
        "Codifique o item abaixo conforme o instrumento LPAI.\n\n"
        "EVIDÊNCIAS E ANOTAÇÕES POR PROVENIÊNCIA "
        "(não as contradiga nem complete por inferência):\n"
        f"{source_blocks}\n\n"
        "Notas anteriores e resultados de busca são pistas documentais, não "
        "prova de recepção histórica. Não infira sentido recebido pelo "
        "espectador sem fonte específica; codifique apenas o sentido produzido "
        "pelo dispositivo e preserve a incerteza.\n\n"
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
        "script_version": SCRIPT_VERSION,
        "proxy_schema_version": PROXY_SCHEMA_VERSION,
        "prompt_version": PROMPT_VERSION,
        "codebook_version": codebook_version,
        "image_source": image_source,
        "usage": usage,
        "proposta": coded,
    }


def append_row(
    output_path: Path, row: dict[str, Any], *, force: bool = False
) -> bool:
    """Decide duplicidade e anexa uma linha sob lock POSIX exclusivo."""
    initial_validator = get_proxy_validator()
    validate_proxy_row(row, validator=initial_validator)
    parent_fd, name = _open_staging_parent(output_path, create=True)
    try:
        try:
            fd = os.open(
                name,
                os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW,
                0o600,
                dir_fd=parent_fd,
            )
        except OSError as exc:
            raise GuardrailError("saída é symlink ou não pôde ser aberta com segurança") from exc
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            try:
                current_validator = get_proxy_validator()
                done = _validate_jsonl_fd(
                    fd, output_path, validator=current_validator
                )
                validate_proxy_row(row, validator=current_validator)
                if row["item_id"] in done and not force:
                    return False
                original_size = os.fstat(fd).st_size
                _assert_safe_file_identity(fd, output_path, purpose="saída")
                payload = (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8")
                os.lseek(fd, 0, os.SEEK_END)
                try:
                    written = os.write(fd, payload)
                except OSError:
                    os.ftruncate(fd, original_size)
                    os.fsync(fd)
                    raise
                if written != len(payload):
                    os.ftruncate(fd, original_size)
                    os.fsync(fd)
                    raise OSError(
                        f"escrita JSONL parcial recusada: {written}/{len(payload)} bytes"
                    )
                try:
                    _assert_safe_file_identity(fd, output_path, purpose="saída")
                except GuardrailError:
                    os.ftruncate(fd, original_size)
                    os.fsync(fd)
                    raise
                os.fsync(fd)
                return True
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)
    finally:
        os.close(parent_fd)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _nonempty_items(value: str) -> str:
    if not any(part.strip() for part in value.split(",")):
        raise argparse.ArgumentTypeError("--items exige ao menos um item_id não vazio")
    return value


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("valor precisa ser maior que zero")
    return parsed


def _nonnegative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("valor não pode ser negativo")
    return parsed


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Codificador-proxy LPAI v2 sobre Kimi K3 (saída em staging)."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {SCRIPT_VERSION}",
        help="mostra a versão do script (não a versão do codebook)",
    )
    alvo = parser.add_mutually_exclusive_group(required=True)
    alvo.add_argument("--items", type=_nonempty_items, help="item_id[,item_id,...]")
    alvo.add_argument("--all", action="store_true", help="todos os registros")

    parser.add_argument("--regime", choices=REGIMES, help="filtra por regime")
    parser.add_argument("--coded-by", help="filtra pela origem de codificação")
    parser.add_argument("--limit", type=_positive_int, help="teto positivo de itens no lote")
    parser.add_argument("--output", help="caminho de staging (.jsonl)")
    parser.add_argument("--images-dir", help="diretório de imagens locais <item_id>.<ext>")
    parser.add_argument(
        "--allow-textual",
        action="store_true",
        help="codificar itens sem imagem (registro é marcado sem_imagem)",
    )
    parser.add_argument("--model", default=MODEL_DEFAULT)
    parser.add_argument("--base-url", default=BASE_URL_DEFAULT)
    parser.add_argument("--retries", type=_nonnegative_int, default=1)
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
        existing_done = load_done(output_path)
    except GuardrailError as exc:
        print(f"[barreira] {exc}", file=sys.stderr)
        return 3
    except (FileNotFoundError, ValueError) as exc:
        print(f"[fatal] {exc}", file=sys.stderr)
        return 1

    item_ids = (
        [i.strip() for i in args.items.split(",") if i.strip()] if args.items else None
    )
    done = set() if args.force else existing_done
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
    schema = build_output_schema()
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
    pulados_sem_evidencia = 0
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
                pulados_sem_evidencia += 1
                print(
                    f"[{index}/{len(selected)}] {item_id}: sem imagem — pulado "
                    "(use --allow-textual para codificar só com texto)",
                    file=sys.stderr,
                )
                continue

        image_b64 = mime = None
        if image_path is not None and not args.dry_run:
            try:
                image_b64, mime = encode_image(image_path)
            except (OSError, ValueError) as exc:
                falhas += 1
                print(f"[erro] {item_id}: evidência visual insegura/inválida: {exc}", file=sys.stderr)
                continue

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
        try:
            appended = append_row(output_path, row, force=args.force)
        except GuardrailError as exc:
            print(f"[barreira] {item_id}: {exc}", file=sys.stderr)
            return 3
        except (RuntimeError, ValueError) as exc:
            falhas += 1
            print(f"[erro] {item_id}: {exc}", file=sys.stderr)
            continue
        if not appended:
            print(
                f"[{index}/{len(selected)}] {item_id}: já gravado por execução "
                "concorrente — duplicata recusada",
                file=sys.stderr,
            )
            continue

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
        f"| pulados sem evidência: {pulados_sem_evidencia} | falhas: {falhas}",
        file=sys.stderr,
    )
    print(
        "revisão humana obrigatória antes de qualquer merge no corpus canônico.",
        file=sys.stderr,
    )

    if falhas:
        return 1
    return 2 if baixa_confianca or pulados_sem_evidencia else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
