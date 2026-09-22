#!/usr/bin/env python3
"""
harvest_corpus_images.py — camada de captação de imagens do corpus ICONOCRACIA.

Problema que resolve: 90% dos 328 registros apontam para páginas de acervo, não
para arquivos de imagem (apenas 4% têm URL direta). Sem bytes de imagem em disco
não há recodificação sob o LPAI v3 — os atributos do Estrato III exigem exame
visual, e o Kimi K3 só aceita imagem em base64, nunca URL pública.

O que faz: resolve cada `input_url` até um arquivo de imagem, preferindo sempre a
via IIIF ou a API oficial do acervo antes de qualquer heurística de HTML, baixa o
arquivo para cache local e registra proveniência auditável — URL de origem,
estratégia de resolução, manifesto IIIF quando existe, direitos declarados,
dimensões, hash e data de captação.

Princípios
----------
  * O ledger canônico é aberto SOMENTE em leitura.
  * Nada é inventado: quando a resolução falha, o registro recebe status de falha
    com o motivo, e não um palpite.
  * Proveniência antes de conveniência: cada imagem carrega de onde veio e por
    qual caminho, porque a tese precisa poder responder isso na banca.
  * Cortesia com os acervos: intervalo mínimo por domínio, User-Agent
    identificável, e nenhuma paralelização agressiva.

Uso
---
    # o que resolve, sem baixar nada
    python tools/scripts/harvest_corpus_images.py --all --dry-run

    # baixa um acervo por vez, com calma
    python tools/scripts/harvest_corpus_images.py --domain gallica.bnf.fr
    python tools/scripts/harvest_corpus_images.py --all --limit 40

    # relatório do que existe em cache
    python tools/scripts/harvest_corpus_images.py --report

Códigos de saída
----------------
    0 — tudo resolvido no lote
    1 — erro fatal
    2 — concluído com itens não resolvidos (esperado; ver relatório)
    3 — violação de barreira de escrita
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote, urlparse

import requests

REPO = Path(__file__).resolve().parent.parent.parent
CANONICAL_RECORDS = REPO / "data" / "processed" / "records.jsonl"
IMAGE_CACHE = REPO / ".cache" / "corpus-images"
MANIFEST = REPO / "data" / "staging" / "image-manifest.jsonl"

# Alguns acervos (loc.gov entre eles) devolvem 403 para User-Agent contendo URL.
# Mantemos identificação acadêmica curta e um fallback ainda mais simples.
USER_AGENT = "ICONOCRACIA-corpus/1.0 (pesquisa de doutorado, PPGD/UFSC)"
USER_AGENT_FALLBACK = "Mozilla/5.0 (compatible; ICONOCRACIA-corpus/1.0)"
TIMEOUT = 45
MIN_BYTES = 8_000          # abaixo disso é ícone, selo de site ou placeholder
DOMAIN_INTERVAL = 2.0      # segundos entre requisições ao mesmo domínio
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff"}

FORBIDDEN_DIRS = (
    REPO / "data" / "processed",
    REPO / "corpus",
    REPO / "examples",
    REPO / "schema",
    REPO / "tools" / "schemas",
)


class GuardrailError(RuntimeError):
    """Tentativa de escrever em área canônica do corpus."""


def assert_write_target(path: Path, *, suffix: str | None = None) -> Path:
    resolved = path.resolve()
    if suffix and resolved.suffix != suffix:
        raise GuardrailError(f"extensão inesperada: {resolved.name}")
    if resolved.name == "records.jsonl":
        raise GuardrailError("'records.jsonl' é o ledger canônico; nunca escrito aqui")
    for directory in FORBIDDEN_DIRS:
        try:
            resolved.relative_to(directory.resolve())
        except ValueError:
            continue
        raise GuardrailError(f"área canônica bloqueada: {resolved}")
    return resolved


# ---------------------------------------------------------------------------
# HTTP cortês
# ---------------------------------------------------------------------------

_ultima_visita: dict[str, float] = {}


def _aguarda(dominio: str) -> None:
    agora = time.monotonic()
    anterior = _ultima_visita.get(dominio)
    if anterior is not None:
        espera = DOMAIN_INTERVAL - (agora - anterior)
        if espera > 0:
            time.sleep(espera)
    _ultima_visita[dominio] = time.monotonic()


ultimo_status: dict[str, int | str] = {}
# Domínios que já responderam 403 duas vezes: não insistir (cortesia + tempo).
dominios_bloqueados: set[str] = set()


def pega(url: str, *, aceita_json: bool = False) -> requests.Response | None:
    """GET cortês, com fallback de User-Agent quando o acervo devolve 403."""
    dominio = urlparse(url).netloc
    if dominio in dominios_bloqueados:
        ultimo_status[url] = 403
        return None
    for agente in (USER_AGENT, USER_AGENT_FALLBACK):
        _aguarda(dominio)
        cabecalhos = {"User-Agent": agente}
        if aceita_json:
            cabecalhos["Accept"] = "application/json"
        try:
            resposta = requests.get(url, headers=cabecalhos, timeout=TIMEOUT)
        except requests.RequestException as erro:
            ultimo_status[url] = type(erro).__name__
            return None
        ultimo_status[url] = resposta.status_code
        if resposta.status_code == 200:
            return resposta
        if resposta.status_code != 403:
            return None
    dominios_bloqueados.add(dominio)
    return None


def pega_json(url: str) -> Any | None:
    resposta = pega(url, aceita_json=True)
    if resposta is None:
        return None
    try:
        return resposta.json()
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Resolvedores por acervo — IIIF e APIs oficiais antes de heurística
# ---------------------------------------------------------------------------

Resolucao = dict[str, Any]


def _res(url: str, estrategia: str, **extra: Any) -> Resolucao:
    saida: Resolucao = {"image_url": url, "strategy": estrategia}
    saida.update({k: v for k, v in extra.items() if v})
    return saida


def resolve_gallica(url: str, _: dict) -> Resolucao | None:
    """Gallica/BnF: o ark identifica o documento; a Image API do IIIF entrega o fólio."""
    match = re.search(r"(ark:/\d+/[A-Za-z0-9]+)", url)
    if not match:
        return None  # URLs de busca SRU não são itens
    ark = match.group(1)
    manifesto = f"https://gallica.bnf.fr/iiif/{ark}/manifest.json"
    dados = pega_json(manifesto)
    canvas = "f1"
    if isinstance(dados, dict):
        sequencias = dados.get("sequences") or []
        if sequencias and sequencias[0].get("canvases"):
            primeiro = sequencias[0]["canvases"][0]
            imagens = primeiro.get("images") or []
            if imagens:
                servico = (imagens[0].get("resource") or {}).get("service") or {}
                base = servico.get("@id")
                if base:
                    return _res(
                        f"{base}/full/full/0/native.jpg",
                        "iiif-manifest",
                        iiif_manifest=manifesto,
                        rights_hint=dados.get("license"),
                        label=primeiro.get("label"),
                    )
            identificador = primeiro.get("@id", "")
            if "/f" in identificador:
                canvas = "f" + identificador.rsplit("/f", 1)[-1]
    return _res(
        f"https://gallica.bnf.fr/iiif/{ark}/{canvas}/full/full/0/native.jpg",
        "iiif-convencao",
        iiif_manifest=manifesto,
    )


def resolve_loc(url: str, _: dict) -> Resolucao | None:
    """Library of Congress: o próprio item devolve JSON com as derivações."""
    dados = pega_json(url.rstrip("/") + "/?fo=json")
    if not isinstance(dados, dict):
        return None
    item = dados.get("item") or {}
    candidatos: list[str] = []
    for chave in ("image_url", "thumb_gallery"):
        valor = item.get(chave) or dados.get(chave)
        if isinstance(valor, list):
            candidatos.extend(v for v in valor if isinstance(v, str))
        elif isinstance(valor, str):
            candidatos.append(valor)
    melhores: list[tuple[int, str]] = []
    for recurso in dados.get("resources") or []:
        for arquivo in recurso.get("files") or []:
            versoes = arquivo if isinstance(arquivo, list) else [arquivo]
            for versao in versoes:
                if not isinstance(versao, dict) or not versao.get("url"):
                    continue
                if (versao.get("mimetype") or "") not in ("image/jpeg", "image/png"):
                    continue
                melhores.append((int(versao.get("size") or 0), versao["url"]))
    if melhores:
        melhores.sort()
        candidatos.insert(0, melhores[-1][1])

    imagens = [c.split("#")[0] for c in candidatos
               if Path(urlparse(c).path).suffix.lower() in IMAGE_SUFFIXES]
    if not imagens:
        return None
    melhor = imagens[0] if melhores else sorted(imagens, key=len)[-1]
    if melhor.startswith("//"):
        melhor = "https:" + melhor
    return _res(
        melhor,
        "loc-api",
        rights_hint=item.get("rights") or item.get("rights_advisory"),
        label=item.get("title"),
    )


def resolve_commons(url: str, _: dict) -> Resolucao | None:
    """Wikimedia Commons: API de imageinfo devolve o original e a licença."""
    match = re.search(r"/(?:wiki|File):(.+)$", url)
    if not match:
        return None
    titulo = "File:" + match.group(1).split("File:")[-1]
    api = (
        "https://commons.wikimedia.org/w/api.php?action=query&format=json"
        f"&titles={quote(titulo)}&prop=imageinfo&iiprop=url|size|extmetadata"
    )
    dados = pega_json(api)
    if not isinstance(dados, dict):
        return None
    paginas = ((dados.get("query") or {}).get("pages") or {}).values()
    for pagina in paginas:
        info = (pagina.get("imageinfo") or [{}])[0]
        if info.get("url"):
            meta = info.get("extmetadata") or {}
            licenca = (meta.get("LicenseShortName") or {}).get("value")
            return _res(
                info["url"],
                "commons-api",
                rights_hint=licenca,
                width=info.get("width"),
                height=info.get("height"),
            )
    return None


def resolve_vam(url: str, _: dict) -> Resolucao | None:
    """V&A: `record.images` traz IDs de imagem; o IIIF do museu monta a URL."""
    match = re.search(r"/item/(O\d+)", url)
    if not match:
        return None
    dados = pega_json(f"https://api.vam.ac.uk/v2/museumobject/{match.group(1)}")
    if not isinstance(dados, dict):
        return None
    registro = dados.get("record") or {}
    meta_imagens = (dados.get("meta") or {}).get("images") or {}

    # 1) IIIF declarado no meta (caminho preferido)
    for chave in ("_iiif_image_base_url", "_iiif_presentation_url", "_primary_thumbnail"):
        valor = meta_imagens.get(chave)
        if not valor:
            continue
        if "iiif" in valor and "/full/" not in valor:
            return _res(valor.rstrip("/") + "/full/full/0/default.jpg",
                        "vam-api-iiif", iiif_manifest=meta_imagens.get("_iiif_presentation_url"))
        if chave == "_primary_thumbnail":
            # a miniatura tem o mesmo identificador da derivação grande
            return _res(re.sub(r"!\d+,\d+", "full", valor), "vam-api-thumb-expandida")

    # 2) IDs de imagem + convenção IIIF do V&A
    imagens = registro.get("images") or registro.get("_images") or []
    if isinstance(imagens, list) and imagens and isinstance(imagens[0], str):
        return _res(
            f"https://framemark.vam.ac.uk/collections/{imagens[0]}/full/full/0/default.jpg",
            "vam-iiif-convencao",
            rights_hint=registro.get("creditLine"),
            label=(registro.get("titles") or [{}])[0].get("title") if registro.get("titles") else None,
            alternativas=[f"https://framemark.vam.ac.uk/collections/{i}/full/full/0/default.jpg"
                          for i in imagens[1:4]],
        )
    return None


def resolve_rijksmuseum(url: str, _: dict) -> Resolucao | None:
    """Rijksmuseum: sem chave de API, a página expõe o tile IIIF em og:image."""
    return None  # tratado pelo genérico; mantido explícito para documentar a escolha


def resolve_europeana(url: str, _: dict) -> Resolucao | None:
    """Europeana: muitos itens são espelhos de Gallica; tenta o ark antes do HTML."""
    match = re.search(r"ark__(\d+)_([A-Za-z0-9]+)", url)
    if match:
        ark = f"ark:/{match.group(1)}/{match.group(2)}"
        return resolve_gallica(f"https://gallica.bnf.fr/{ark}", {})
    return None


def resolve_numista(url: str, _: dict) -> Resolucao | None:
    """Numista: prefere a API oficial (NUMISTA_API_KEY); o HTML costuma dar 403."""
    chave = os.environ.get("NUMISTA_API_KEY")
    match = re.search(r"pieces(\d+)", url)
    if chave and match:
        dados = pega_json(
            f"https://api.numista.com/api/v3/types/{match.group(1)}?lang=en"
            f"&api_key={chave}"
        )
        if isinstance(dados, dict):
            for lado in ("obverse", "reverse"):
                figura = (dados.get(lado) or {}).get("picture")
                if figura:
                    return _res(figura, "numista-api",
                                rights_hint=(dados.get(lado) or {}).get("copyright"),
                                label=dados.get("title"))
    resposta = pega(url)
    if resposta is None:
        return None
    fotos = re.findall(r'https://[^"\']+/photos/[^"\']+\.(?:jpg|jpeg|png)', resposta.text)
    if not fotos:
        return None
    unicas = list(dict.fromkeys(fotos))
    return _res(unicas[0], "numista-html", alternativas=unicas[1:4])


RESOLVEDORES: dict[str, Callable[[str, dict], Resolucao | None]] = {
    "gallica.bnf.fr": resolve_gallica,
    "loc.gov": resolve_loc,
    "commons.wikimedia.org": resolve_commons,
    "collections.vam.ac.uk": resolve_vam,
    "rijksmuseum.nl": resolve_rijksmuseum,
    "europeana.eu": resolve_europeana,
    "numista.com": resolve_numista,
}


# ---------------------------------------------------------------------------
# Genérico: IIIF declarado, og:image, JSON-LD — nesta ordem
# ---------------------------------------------------------------------------

PADRAO_IIIF = re.compile(r'https?://[^"\'\s]+/(?:manifest|info)\.json', re.I)
PADRAO_OG = re.compile(
    r'<meta[^>]+(?:property|name)=["\'](?:og:image(?::secure_url)?|twitter:image)["\']'
    r'[^>]+content=["\']([^"\']+)["\']', re.I)
PADRAO_OG_INV = re.compile(
    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']'
    r'(?:og:image(?::secure_url)?|twitter:image)["\']', re.I)
PADRAO_IMG = re.compile(r'<img[^>]+src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))["\']', re.I)
PADRAO_DIREITOS = re.compile(
    r'(?:rights|license|licence|direitos)["\':\s>]+([^<"\'\n]{4,80})', re.I)


def resolve_generico(url: str, _: dict) -> Resolucao | None:
    resposta = pega(url)
    if resposta is None:
        return None
    html = resposta.text
    base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    def absoluto(candidato: str) -> str:
        if candidato.startswith("//"):
            return "https:" + candidato
        if candidato.startswith("/"):
            return base + candidato
        return candidato

    direitos = None
    achado = PADRAO_DIREITOS.search(html)
    if achado:
        direitos = achado.group(1).strip()

    manifesto = PADRAO_IIIF.search(html)
    if manifesto:
        alvo = absoluto(manifesto.group(0))
        dados = pega_json(alvo)
        if isinstance(dados, dict):
            if dados.get("sequences"):
                imagens = ((dados["sequences"][0].get("canvases") or [{}])[0].get("images") or [])
                if imagens:
                    servico = (imagens[0].get("resource") or {}).get("service") or {}
                    if servico.get("@id"):
                        return _res(f"{servico['@id']}/full/full/0/native.jpg",
                                    "iiif-descoberto", iiif_manifest=alvo,
                                    rights_hint=dados.get("license") or direitos)
            if dados.get("@id") and dados.get("width"):  # info.json
                return _res(f"{dados['@id']}/full/full/0/default.jpg",
                            "iiif-info", iiif_manifest=alvo,
                            width=dados.get("width"), height=dados.get("height"),
                            rights_hint=direitos)

    for padrao in (PADRAO_OG, PADRAO_OG_INV):
        achado = padrao.search(html)
        if achado:
            return _res(absoluto(achado.group(1)), "og-image", rights_hint=direitos)

    candidatas = [absoluto(c) for c in PADRAO_IMG.findall(html)]
    candidatas = [c for c in candidatas if not re.search(r"logo|icon|sprite|banner|avatar", c, re.I)]
    if candidatas:
        return _res(candidatas[0], "html-img", rights_hint=direitos,
                    alternativas=candidatas[1:4])
    return None


def resolve(url: str, registro: dict) -> Resolucao | None:
    dominio = urlparse(url).netloc.replace("www.", "")
    for sufixo, funcao in RESOLVEDORES.items():
        if dominio.endswith(sufixo):
            achado = funcao(url, registro)
            if achado:
                return achado
            break
    return resolve_generico(url, registro)


# ---------------------------------------------------------------------------
# Download e proveniência
# ---------------------------------------------------------------------------


def dimensoes(caminho: Path) -> tuple[int | None, int | None]:
    try:
        from PIL import Image  # opcional
    except ImportError:
        return None, None
    try:
        with Image.open(caminho) as imagem:
            return imagem.width, imagem.height
    except Exception:  # noqa: BLE001
        return None, None


def baixa(item_id: str, resolucao: Resolucao, min_bytes: int) -> dict[str, Any]:
    url = resolucao["image_url"]
    resposta = pega(url)
    if resposta is None:
        return {"status": "erro_download", "detail": f"sem resposta de {url}"}
    conteudo = resposta.content
    if len(conteudo) < min_bytes:
        return {"status": "imagem_pequena", "detail": f"{len(conteudo)} bytes"}

    tipo = (resposta.headers.get("Content-Type") or "").split(";")[0].strip()
    if tipo and not tipo.startswith("image/"):
        return {"status": "nao_e_imagem", "detail": tipo}
    extensao = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp",
                "image/gif": ".gif", "image/tiff": ".tif"}.get(tipo)
    if extensao is None:
        sufixo = Path(urlparse(url).path).suffix.lower()
        extensao = sufixo if sufixo in IMAGE_SUFFIXES else ".jpg"

    IMAGE_CACHE.mkdir(parents=True, exist_ok=True)
    destino = assert_write_target(IMAGE_CACHE / f"{item_id}{extensao}")
    destino.write_bytes(conteudo)
    largura, altura = dimensoes(destino)
    return {
        "status": "ok",
        "path": str(destino.relative_to(REPO)),
        "bytes": len(conteudo),
        "sha256": hashlib.sha256(conteudo).hexdigest(),
        "content_type": tipo or None,
        "width": largura or resolucao.get("width"),
        "height": altura or resolucao.get("height"),
    }


def carrega_registros() -> list[dict[str, Any]]:
    if not CANONICAL_RECORDS.exists():
        raise FileNotFoundError(CANONICAL_RECORDS)
    with CANONICAL_RECORDS.open("r", encoding="utf-8") as arquivo:
        return [json.loads(linha) for linha in arquivo if linha.strip()]


def carrega_manifesto() -> dict[str, dict]:
    if not MANIFEST.exists():
        return {}
    entradas: dict[str, dict] = {}
    with MANIFEST.open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            try:
                registro = json.loads(linha)
            except json.JSONDecodeError:
                continue
            entradas[registro.get("item_id", "")] = registro
    entradas.pop("", None)
    return entradas


def anexa_manifesto(entrada: dict) -> None:
    alvo = assert_write_target(MANIFEST, suffix=".jsonl")
    alvo.parent.mkdir(parents=True, exist_ok=True)
    with alvo.open("a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(entrada, ensure_ascii=False) + "\n")


def agora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------


def relatorio(registros: list[dict]) -> None:
    manifesto = carrega_manifesto()
    print(f"registros no corpus: {len(registros)} | no manifesto: {len(manifesto)}\n")
    por_status = Counter(e.get("status") for e in manifesto.values())
    print("=== STATUS ===")
    for status, quantidade in por_status.most_common():
        print(f"  {str(status):<20} {quantidade:>4}")

    print("\n=== ESTRATÉGIA DE RESOLUÇÃO (itens com imagem) ===")
    for estrategia, quantidade in Counter(
        e.get("strategy") for e in manifesto.values() if e.get("status") == "ok"
    ).most_common():
        print(f"  {str(estrategia):<20} {quantidade:>4}")

    print("\n=== COBERTURA POR ACERVO ===")
    por_dominio: dict[str, Counter] = defaultdict(Counter)
    for registro in registros:
        url = (registro.get("input") or {}).get("input_url") or ""
        dominio = urlparse(url).netloc.replace("www.", "") or "sem url"
        entrada = manifesto.get(registro.get("item_id"))
        por_dominio[dominio][entrada.get("status") if entrada else "pendente"] += 1
    for dominio, contagem in sorted(por_dominio.items(), key=lambda x: -sum(x[1].values())):
        total = sum(contagem.values())
        ok = contagem.get("ok", 0)
        print(f"  {dominio[:36]:<38} {ok:>3}/{total:<4} " +
              " ".join(f"{k}={v}" for k, v in contagem.items() if k != "ok"))

    aptos = [e for e in manifesto.values() if e.get("status") == "ok" and e.get("width")]
    if aptos:
        print("\n=== RESOLUÇÃO DAS IMAGENS (Estrato III exige exame visual) ===")
        faixas = Counter()
        for entrada in aptos:
            lado = max(entrada["width"], entrada.get("height") or 0)
            faixa = ("< 400 px (insuficiente)" if lado < 400 else
                     "400–799 px (limitado)" if lado < 800 else
                     "800–1599 px (adequado)" if lado < 1600 else
                     ">= 1600 px (ótimo)")
            faixas[faixa] += 1
        for faixa, quantidade in sorted(faixas.items()):
            print(f"  {faixa:<26} {quantidade:>4}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    alvo = parser.add_mutually_exclusive_group()
    alvo.add_argument("--items", help="item_id[,item_id,...]")
    alvo.add_argument("--all", action="store_true")
    alvo.add_argument("--report", action="store_true", help="só relatório, sem rede")
    parser.add_argument("--domain", help="filtra por domínio do acervo")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--min-bytes", type=int, default=MIN_BYTES)
    parser.add_argument("--force", action="store_true", help="refazer itens já no manifesto")
    parser.add_argument("--dry-run", action="store_true",
                        help="resolve a URL da imagem e não baixa nada")
    argumentos = parser.parse_args(argv)

    try:
        registros = carrega_registros()
    except (FileNotFoundError, json.JSONDecodeError) as erro:
        print(f"[fatal] {erro}", file=sys.stderr)
        return 1

    if argumentos.report:
        relatorio(registros)
        return 0
    if not (argumentos.all or argumentos.items):
        parser.error("use --all, --items ou --report")

    manifesto = carrega_manifesto()
    ids = [i.strip() for i in argumentos.items.split(",")] if argumentos.items else None

    fila = []
    for registro in registros:
        item_id = registro.get("item_id")
        url = (registro.get("input") or {}).get("input_url") or ""
        if ids and item_id not in ids:
            continue
        if argumentos.domain and argumentos.domain not in url:
            continue
        if not argumentos.force and item_id in manifesto and \
                manifesto[item_id].get("status") == "ok":
            continue
        fila.append((item_id, url, registro))
    if argumentos.limit:
        fila = fila[: argumentos.limit]

    print(f"fila: {len(fila)} itens | cache: {IMAGE_CACHE.relative_to(REPO)} | "
          f"manifesto: {MANIFEST.relative_to(REPO)}", file=sys.stderr)
    if argumentos.dry_run:
        print("modo ensaio: resolve e não baixa\n", file=sys.stderr)

    contagem: Counter = Counter()
    for indice, (item_id, url, registro) in enumerate(fila, start=1):
        prefixo = f"[{indice}/{len(fila)}] {item_id}"

        if not url:
            entrada = {"item_id": item_id, "status": "sem_url", "checked_at": agora()}
        elif urlparse(url).netloc.endswith("iconocracy.corpus"):
            entrada = {"item_id": item_id, "source_url": url, "status": "placeholder",
                       "detail": "URL interna sem acervo de origem", "checked_at": agora()}
        else:
            resolucao = resolve(url, registro)
            if resolucao is None:
                bloqueios = [v for k, v in ultimo_status.items()
                             if urlparse(k).netloc == urlparse(url).netloc]
                bloqueado = 403 in bloqueios
                entrada = {
                    "item_id": item_id, "source_url": url,
                    "status": "bloqueado_acervo" if bloqueado else "nao_resolvido",
                    "detail": f"http {bloqueios[-1]}" if bloqueios else "sem candidata de imagem",
                    "checked_at": agora(),
                }
            elif argumentos.dry_run:
                entrada = {"item_id": item_id, "source_url": url, "status": "resolvido",
                           **resolucao, "checked_at": agora()}
            else:
                resultado = baixa(item_id, resolucao, argumentos.min_bytes)
                entrada = {"item_id": item_id, "source_url": url, **resolucao,
                           **resultado, "checked_at": agora()}

        contagem[entrada["status"]] += 1
        if not argumentos.dry_run:
            anexa_manifesto(entrada)
        detalhe = entrada.get("strategy") or entrada.get("detail") or ""
        print(f"{prefixo}: {entrada['status']} {detalhe}", file=sys.stderr)

    print("\n=== RESUMO ===", file=sys.stderr)
    for status, quantidade in contagem.most_common():
        print(f"  {status:<16} {quantidade:>4}", file=sys.stderr)

    falhas = sum(v for k, v in contagem.items()
                 if k not in ("ok", "resolvido"))
    return 2 if falhas else 0


if __name__ == "__main__":  # pragma: no cover
    try:
        sys.exit(main())
    except GuardrailError as erro:
        print(f"[barreira] {erro}", file=sys.stderr)
        sys.exit(3)
