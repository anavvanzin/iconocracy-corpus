#!/usr/bin/env python3.12
"""
iconocode_gemma4.py — Automated IconoCode analyzer (Gemma-4 E4B-it) for the
ICONOCRACIA corpus.

Loads `google/gemma-4-E4B-it` (multimodal image-text-to-text, apache-2.0) and
applies the Purificação Clássica codebook to each target item:

  1. Fetch/cache the item's image (thumbnail_url preferred, url fallback)
  2. Build a chat-template prompt requesting strict JSON output
  3. Generate with the model, parse JSON, append one line to the staging JSONL
  4. Retry once with a repair prompt on parse failure; mark confidence=low

All output goes to a STAGING file (data/staging/iconocode-gemma4-runs.jsonl) —
NEVER to corpus-data.json directly. Human review is required before merge.

CLI flags:
    --items ID[,ID,...]        Comma-separated corpus IDs (subset)
    --all-uncoded              Shortcut for all 19 uncoded items
    --dry-run                  Load model, test first item, print parsed JSON,
                               DO NOT write JSONL
    --force-refresh-images     Re-download even if cached
    --device auto|mps|cpu      Device selection (default auto)
    --output <path>            Override default staging path

Exit codes:
    0 — success, all items coded with medium|high confidence
    1 — fatal error (model load, I/O, missing items)
    2 — some items returned confidence=low (signal, not block)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

REPO = Path(__file__).resolve().parent.parent.parent
CORPUS_PATH = REPO / "corpus" / "corpus-data.json"
STAGING_PATH = REPO / "data" / "staging" / "iconocode-gemma4-runs.jsonl"
CACHE_DIR = REPO / ".cache" / "iconocode-images"

# GGUF backend via llama-cpp-python (fits Apple M4 16GB; transformers fp16
# weights would OOM at ~15 GB). Default: Q4_K_M + mmproj-F16 from
# unsloth/gemma-4-E4B-it-GGUF. Paths can be overridden via env vars.
HF_HUB_CACHE = Path(
    os.environ.get("HF_HOME", str(Path.home() / ".cache" / "huggingface"))
) / "hub"
GGUF_REPO_DIR = (
    HF_HUB_CACHE / "models--unsloth--gemma-4-E4B-it-GGUF" / "snapshots"
)
GGUF_MODEL_FILENAME = os.environ.get(
    "ICONOCODE_GGUF_MODEL", "gemma-4-E4B-it-Q4_K_M.gguf"
)
GGUF_MMPROJ_FILENAME = os.environ.get(
    "ICONOCODE_GGUF_MMPROJ", "mmproj-F16.gguf"
)

MODEL_ID = "unsloth/gemma-4-E4B-it-GGUF"
AGENT_ID = "gemma-4-E4B-it-Q4_K_M-llamacpp"
PROMPT_VERSION = "iconocode-gemma4-v1"

INDICATOR_KEYS: list[str] = [
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
]

VALID_REGIMES = {"fundacional", "normativo", "militar", "contra-alegoria"}

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

ICONOCODE_PROMPT = """Você é um codificador iconográfico da tese ICONOCRACIA (PPGD/UFSC) sobre alegoria feminina na cultura jurídica dos séculos XIX–XX. Analise a imagem fornecida aplicando o codebook abaixo. Responda APENAS com um objeto JSON válido, em português, sem texto fora do JSON.

Item em análise: {title}
Suporte: {support}
País: {country}
Data aproximada: {date}

=== 1. Análise Panofsky (3 níveis, concisos) ===
- pre_iconografico: o que é visualmente observável (figuras, objetos, pose, composição). Máx 400 caracteres.
- iconografico: identificação dos motivos iconográficos convencionais (alegoria da República, Britannia, Germania, atributos: balança, escudo, coroa etc.). Máx 400 caracteres.
- iconologico: significado cultural/jurídico-político no contexto do período. Máx 400 caracteres.

=== 2. Dez indicadores de Purificação Clássica (escala 0–4; 0 = ausente, 4 = intenso) ===
- desincorporacao: ausência/abstração do corpo feminino histórico (quanto mais etérea, impessoal ou mineralizada a figura, maior)
- rigidez_postural: pose estática, vertical, hierática, sem gesto narrativo
- dessexualizacao: neutralização de marcadores sexuais secundários (drapeado púdico, ausência de busto erotizado)
- uniformizacao_facial: rosto idealizado, neoclássico, não individualizado
- heraldizacao: atributos em posição emblemática (escudo, lema, coroa, cartela)
- enquadramento_arquitetonico: nicho, pedestal, arco, moldura cercando a figura
- apagamento_narrativo: ausência de cena/contexto histórico (figura isolada vs. evento)
- monocromatizacao: paleta restrita, ausência de cor viva (metal monocromo conta alto)
- serialidade: repetição de padrão tipográfico/compositivo (moeda em série, grade ornamental)
- inscricao_estatal: texto oficial no suporte (valor, legenda, divisa, nome do Estado)

=== 3. Regime iconocrático ===
Classifique em exatamente um de:
- fundacional: sacrificial, corpo vivo, pathos revolucionário (1789–1848)
- normativo: domesticada, burocrática, moeda/selo republicano estabilizado
- militar: endurecida, imperial, mobilização bélica, colonial
- contra-alegoria: subversão, paródia, negação do cânone alegórico

=== 4. Metadados de saída ===
- reasoning: justificativa breve (≤ 500 caracteres) relacionando os indicadores mais altos ao regime escolhido
- confidence: "high" se imagem nítida e motivo inequívoco; "medium" se atribuições parciais; "low" se imagem ruim/ambígua

=== FORMATO DE RESPOSTA (JSON ESTRITO) ===
{{
  "panofsky": {{
    "pre_iconografico": "...",
    "iconografico": "...",
    "iconologico": "..."
  }},
  "indicators": {{
    "desincorporacao": 0,
    "rigidez_postural": 0,
    "dessexualizacao": 0,
    "uniformizacao_facial": 0,
    "heraldizacao": 0,
    "enquadramento_arquitetonico": 0,
    "apagamento_narrativo": 0,
    "monocromatizacao": 0,
    "serialidade": 0,
    "inscricao_estatal": 0
  }},
  "regime": "fundacional|normativo|militar|contra-alegoria",
  "reasoning": "...",
  "confidence": "high|medium|low"
}}

Responda APENAS o JSON acima, preenchido. Sem prefixos, sem explicações extras, sem markdown.
"""

REPAIR_PROMPT = """Sua resposta anterior não foi JSON válido. Reemita APENAS um objeto JSON, sem texto antes ou depois, seguindo exatamente o esquema pedido (chaves: panofsky, indicators, regime, reasoning, confidence). Valores numéricos inteiros 0–4 para cada indicador.
"""


# ---------------------------------------------------------------------------
# Helpers — corpus, cache, hashing, device
# ---------------------------------------------------------------------------


def load_corpus() -> list[dict[str, Any]]:
    return json.loads(CORPUS_PATH.read_text())


def uncoded_items(corpus: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [i for i in corpus if not i.get("indicadores")]


def select_items(
    corpus: list[dict[str, Any]],
    ids: list[str] | None,
    all_uncoded: bool,
) -> list[dict[str, Any]]:
    if all_uncoded:
        return uncoded_items(corpus)
    if ids:
        by_id = {i["id"]: i for i in corpus}
        missing = [x for x in ids if x not in by_id]
        if missing:
            raise SystemExit(f"ERRO: IDs não encontrados no corpus: {missing}")
        return [by_id[x] for x in ids]
    # Default: all uncoded (matches --all-uncoded)
    return uncoded_items(corpus)


def image_cache_path(item_id: str, ext: str = "jpg") -> Path:
    return CACHE_DIR / f"{item_id}.{ext}"


def find_cached_image(item_id: str) -> Path | None:
    for ext in ("jpg", "jpeg", "png", "webp"):
        p = image_cache_path(item_id, ext)
        if p.exists() and p.stat().st_size > 0:
            return p
    return None


def download_image(
    item: dict[str, Any],
    force: bool = False,
    session: requests.Session | None = None,
) -> Path | None:
    """Fetch the image for *item* into CACHE_DIR. Returns path or None on failure.

    Preference order: thumbnail_url → url (if direct image). HTML catalogue pages
    (Numista/Wikipedia) are NOT scraped — we return None and the caller marks
    confidence=low.
    """
    item_id = item["id"]
    if not force:
        cached = find_cached_image(item_id)
        if cached is not None:
            return cached

    url = item.get("thumbnail_url") or item.get("url")
    if not url:
        return None

    sess = session or requests.Session()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    try:
        resp = sess.get(
            url,
            timeout=30,
            headers={
                "User-Agent": (
                    "iconocracy-corpus/iconocode_gemma4 "
                    "(+https://github.com/anavvanzin/iconocracy-corpus)"
                )
            },
            allow_redirects=True,
        )
        resp.raise_for_status()
    except Exception as exc:
        print(f"  WARN: download falhou para {item_id}: {exc}", file=sys.stderr)
        return None

    ctype = resp.headers.get("Content-Type", "").lower()
    if "image" not in ctype:
        print(
            f"  WARN: {item_id} url retornou Content-Type={ctype!r}, não é imagem direta",
            file=sys.stderr,
        )
        return None

    ext = "jpg"
    if "png" in ctype:
        ext = "png"
    elif "webp" in ctype:
        ext = "webp"
    elif "jpeg" in ctype or "jpg" in ctype:
        ext = "jpg"

    out = image_cache_path(item_id, ext)
    out.write_bytes(resp.content)
    return out


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def pick_device(requested: str) -> str:
    if requested != "auto":
        return requested
    try:
        import torch

        if torch.backends.mps.is_available():
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass
    return "cpu"


# ---------------------------------------------------------------------------
# Model wrapper
# ---------------------------------------------------------------------------


class GemmaIconoCoder:
    """Thin wrapper around llama-cpp-python for Gemma-4 E4B GGUF (multimodal).

    The real model is only loaded when .load() is called. Tests inject a fake
    Llama via the `llm` constructor arg, bypassing .load().

    Why GGUF over transformers: the fp16 safetensors is ~15 GB, which will
    OOM on Apple M4 with 16 GB unified memory. Q4_K_M GGUF is ~4.6 GB and
    fits comfortably. The chat handler loads the mmproj vision adapter
    separately (CLIP-style projector, ~950 MB).
    """

    def __init__(
        self,
        model_path: Path | None = None,
        mmproj_path: Path | None = None,
        device: str = "auto",  # kept for CLI compat; llama-cpp uses n_gpu_layers
        n_ctx: int = 4096,
        n_gpu_layers: int = -1,  # -1 = all layers on GPU (Metal on Apple Silicon)
        llm: Any | None = None,
    ) -> None:
        self.model_path = model_path  # resolved at load() time
        self.mmproj_path = mmproj_path
        self.device = device
        self.n_ctx = n_ctx
        self.n_gpu_layers = n_gpu_layers
        self.llm = llm

    def _resolve_gguf_paths(self) -> tuple[Path, Path]:
        """Find the downloaded GGUF + mmproj under the HF hub cache."""
        if self.model_path and self.mmproj_path:
            return Path(self.model_path), Path(self.mmproj_path)

        if not GGUF_REPO_DIR.exists():
            raise FileNotFoundError(
                f"GGUF não baixado. Execute: hf download {MODEL_ID} "
                f"{GGUF_MODEL_FILENAME} {GGUF_MMPROJ_FILENAME}"
            )

        snapshots = sorted(GGUF_REPO_DIR.iterdir())
        if not snapshots:
            raise FileNotFoundError(
                f"Sem snapshots em {GGUF_REPO_DIR}. Rode hf download primeiro."
            )
        snap = snapshots[-1]
        model_p = snap / GGUF_MODEL_FILENAME
        mmproj_p = snap / GGUF_MMPROJ_FILENAME
        for p, label in ((model_p, "model"), (mmproj_p, "mmproj")):
            if not p.exists():
                raise FileNotFoundError(
                    f"{label} GGUF não encontrado: {p}. Rode hf download."
                )
        return model_p, mmproj_p

    def load(self) -> None:
        if self.llm is not None:
            return
        from llama_cpp import Llama
        # Gemma-4 uses the same chat template family as Gemma-3; the Gemma3
        # handler works for multimodal input. If a native Gemma4ChatHandler
        # ships in a future llama-cpp-python release, switch to it.
        try:
            from llama_cpp.llama_chat_format import Gemma3ChatHandler as ChatHandler
        except ImportError:  # pragma: no cover - older llama-cpp-python
            raise RuntimeError(
                "llama-cpp-python sem Gemma3ChatHandler. Atualize para ≥0.3.5."
            )

        model_path, mmproj_path = self._resolve_gguf_paths()
        self.model_path = model_path
        self.mmproj_path = mmproj_path

        print(
            f"INFO: carregando {model_path.name} + {mmproj_path.name} "
            f"(n_gpu_layers={self.n_gpu_layers}, n_ctx={self.n_ctx})",
            file=sys.stderr,
        )

        handler = ChatHandler(clip_model_path=str(mmproj_path), verbose=False)
        self.llm = Llama(
            model_path=str(model_path),
            chat_handler=handler,
            n_ctx=self.n_ctx,
            n_gpu_layers=self.n_gpu_layers,
            logits_all=False,
            verbose=False,
        )

    def generate_json(
        self,
        image_path: Path,
        item: dict[str, Any],
        prompt_text: str,
        max_new_tokens: int = 800,
    ) -> str:
        """Run one create_chat_completion call. Returns raw text of assistant reply."""
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"file://{image_path.resolve()}"},
                    },
                    {"type": "text", "text": prompt_text},
                ],
            }
        ]
        resp = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=max_new_tokens,
            temperature=0.0,
        )
        return resp["choices"][0]["message"]["content"] or ""


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)


def parse_model_output(text: str) -> dict[str, Any] | None:
    """Extract the first JSON object from *text*. Returns None on failure."""
    if not text:
        return None
    # Prefer a ```json ... ``` fenced block if present
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else None
    if candidate is None:
        match = JSON_BLOCK_RE.search(text)
        if match is None:
            return None
        candidate = match.group(0)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None


def coerce_indicators(raw: dict[str, Any] | None) -> dict[str, int]:
    """Force indicator values into int 0..4. Missing keys default to 0."""
    out: dict[str, int] = {}
    raw = raw or {}
    for key in INDICATOR_KEYS:
        val = raw.get(key, 0)
        try:
            v = int(round(float(val)))
        except (TypeError, ValueError):
            v = 0
        out[key] = max(0, min(4, v))
    return out


def derive_confidence(
    parsed: dict[str, Any] | None,
    parse_failed: bool,
) -> str:
    if parse_failed or parsed is None:
        return "low"
    claimed = str(parsed.get("confidence", "medium")).strip().lower()
    if claimed in {"high", "medium", "low"}:
        return claimed
    return "medium"


def build_staging_record(
    item: dict[str, Any],
    parsed: dict[str, Any] | None,
    image_path: Path | None,
    parse_failed: bool,
    raw_text: str,
) -> dict[str, Any]:
    """Assemble the JSONL line. Always produces a record, even on failure."""
    indicators = coerce_indicators((parsed or {}).get("indicators"))
    mean = round(sum(indicators.values()) / len(indicators), 2)

    regime = None
    if parsed and isinstance(parsed.get("regime"), str):
        cand = parsed["regime"].strip().lower()
        if cand in VALID_REGIMES:
            regime = cand

    panofsky_in = (parsed or {}).get("panofsky") or {}
    panofsky_out = {
        "pre_iconografico": str(panofsky_in.get("pre_iconografico", ""))[:1000],
        "iconografico": str(panofsky_in.get("iconografico", ""))[:1000],
        "iconologico": str(panofsky_in.get("iconologico", ""))[:1000],
    }

    reasoning = str((parsed or {}).get("reasoning", ""))[:500]
    confidence = derive_confidence(parsed, parse_failed)
    if regime is None and confidence == "high":
        confidence = "medium"

    image_hash = sha256_of(image_path) if image_path else None

    record = {
        "run_id": str(uuid.uuid4()),
        "item_id": item["id"],
        "agent_id": AGENT_ID,
        "prompt_version": PROMPT_VERSION,
        "coded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "panofsky": panofsky_out,
        # English key `indicators` aligns with reconcile_iconocode.py validator.
        # Portuguese `indicadores` is the corpus-data.json field — staging keeps
        # the reconciliation-ready name so downstream arbitration works unchanged.
        "indicators": indicators,
        "regime": regime,
        "endurecimento_score": mean,
        "reasoning": reasoning,
        "image_hash": image_hash,
        "confidence": confidence,
        "parse_failed": parse_failed,
    }
    if parse_failed:
        record["raw_model_output"] = raw_text[:4000]
    return record


# ---------------------------------------------------------------------------
# Per-item pipeline
# ---------------------------------------------------------------------------


def render_prompt(item: dict[str, Any]) -> str:
    return ICONOCODE_PROMPT.format(
        title=item.get("title", "desconhecido"),
        support=item.get("support", "desconhecido"),
        country=item.get("country", item.get("country_pt", "desconhecido")),
        date=item.get("date", item.get("year", "desconhecida")),
    )


def code_one_item(
    coder: GemmaIconoCoder,
    item: dict[str, Any],
    force_refresh: bool,
    session: requests.Session | None = None,
) -> dict[str, Any]:
    item_id = item["id"]
    print(f"INFO: codificando {item_id}", file=sys.stderr)

    image_path = download_image(item, force=force_refresh, session=session)
    if image_path is None:
        print(
            f"  WARN: sem imagem acessível para {item_id}; gerando registro low-confidence",
            file=sys.stderr,
        )
        return build_staging_record(
            item=item,
            parsed=None,
            image_path=None,
            parse_failed=True,
            raw_text="NO_IMAGE_AVAILABLE",
        )

    prompt = render_prompt(item)
    raw_text = coder.generate_json(image_path, item, prompt)
    parsed = parse_model_output(raw_text)

    if parsed is None:
        # Repair pass
        print(
            f"  WARN: parse falhou para {item_id}, tentando repair prompt",
            file=sys.stderr,
        )
        raw_text2 = coder.generate_json(
            image_path, item, prompt + "\n\n" + REPAIR_PROMPT
        )
        parsed2 = parse_model_output(raw_text2)
        if parsed2 is None:
            return build_staging_record(
                item=item,
                parsed=None,
                image_path=image_path,
                parse_failed=True,
                raw_text=raw_text + "\n---REPAIR---\n" + raw_text2,
            )
        parsed = parsed2
        raw_text = raw_text2

    return build_staging_record(
        item=item,
        parsed=parsed,
        image_path=image_path,
        parse_failed=False,
        raw_text=raw_text,
    )


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="iconocode_gemma4.py",
        description=(
            "IconoCode analyzer powered by google/gemma-4-E4B-it. Writes to a "
            "STAGING JSONL — never directly to corpus-data.json. Human review "
            "is required before merge."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--items", help="Comma-separated corpus IDs (subset)")
    p.add_argument(
        "--all-uncoded",
        action="store_true",
        help="Code every item in corpus-data.json where indicadores is null",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Load model, run on first item, print parsed JSON, DO NOT write JSONL",
    )
    p.add_argument(
        "--force-refresh-images",
        action="store_true",
        help="Re-download images even if cached",
    )
    p.add_argument(
        "--device",
        default="auto",
        choices=["auto", "mps", "cpu", "cuda"],
        help="Device selection (default auto)",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=STAGING_PATH,
        help=f"Override staging path (default {STAGING_PATH.relative_to(REPO)})",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.items and not args.all_uncoded:
        print(
            "ERRO: especifique --items ID[,ID,...] ou --all-uncoded. "
            "Invocação sem alvo explícito é desabilitada por segurança "
            "(evita codificação acidental em lote).",
            file=sys.stderr,
        )
        return 1

    corpus = load_corpus()
    ids: list[str] | None = None
    if args.items:
        ids = [s.strip() for s in args.items.split(",") if s.strip()]
    items = select_items(corpus, ids, args.all_uncoded)

    if not items:
        print("AVISO: nenhum item a codificar — saída limpa.", file=sys.stderr)
        return 0

    print(f"INFO: {len(items)} item(ns) selecionado(s) para codificação.", file=sys.stderr)

    coder = GemmaIconoCoder(device=args.device)
    coder.load()

    session = requests.Session()
    low_conf = 0
    records: list[dict[str, Any]] = []

    for i, item in enumerate(items, 1):
        print(f"[{i}/{len(items)}] {item['id']}", file=sys.stderr)
        record = code_one_item(
            coder, item, force_refresh=args.force_refresh_images, session=session
        )
        records.append(record)

        if args.dry_run:
            print(json.dumps(record, indent=2, ensure_ascii=False))
            print(
                "DRY-RUN: parando no primeiro item, nada gravado em staging.",
                file=sys.stderr,
            )
            break

        append_jsonl(args.output, record)
        print(
            f"  -> {record['confidence']} | regime={record['regime']} | mean={record['endurecimento_score']}",
            file=sys.stderr,
        )
        if record["confidence"] == "low":
            low_conf += 1

    if args.dry_run:
        return 0

    print(
        f"OK: {len(records)} registros anexados a {args.output} "
        f"({low_conf} com confidence=low)",
        file=sys.stderr,
    )
    return 2 if low_conf else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
