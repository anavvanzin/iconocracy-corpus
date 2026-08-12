#!/usr/bin/env python3
"""Build the auditable SCOUT-575–624 integration queue and ready-only patch.

The decision matrix in this file is intentionally explicit.  It records human
audit judgments; deterministic code only applies declared metadata corrections,
derives identifiers/hashes, and renders/validates the three delivery artifacts.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import subprocess
import uuid
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import yaml


ROOT = Path(__file__).resolve().parents[3]
NOTES_DIR = ROOT / "vault" / "candidatos"
LEDGER = ROOT / "data" / "processed" / "records.jsonl"
REPORT = ROOT / "tools" / "audit" / "reports" / "scout-575-624-integration-queue.md"
QUEUE = ROOT / "tools" / "audit" / "data" / "scout-575-624-integration-queue.jsonl"
PATCH = ROOT / "tools" / "audit" / "patches" / "scout-575-624-ready-records.patch"

AUDIT_DATE = "2026-07-30"
ACCESS_DATE_ABNT = "30 jul. 2026"
SCOUT_SNAPSHOT_DATE = "2026-07-25"
EXPECTED_LEDGER_SHA256 = "e9d05d7c3147ed20a8937c6bc5b1a58d752f0f2a41a11f78f2508f18077cfc2f"
EXPECTED_CORPUS_SHA256 = "fcc79610651d309c8b01a1ededaf33c08220bc10942692497f58eaef940be996"
PLAN_LEDGER_SHA256 = "d23056f3370df7c8543d1f38ca49bd4a62de7637697990ebc31b84f548719664"
EXPECTED_LEDGER_ROWS = 328
BATCH_ID = "00000000-1c0c-4842-8a1a-scout575624"
VAULT_NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
TIMESTAMP = "2026-07-30T12:00:00Z"


def criterion(status: str, evidence: str) -> dict[str, str]:
    return {"status": status, "evidence": evidence}


def decision(
    classification: str,
    reason: str,
    female: tuple[str, str],
    legal: tuple[str, str],
    period: tuple[str, str],
    support: tuple[str, str],
    *,
    dedupe: str = "CLEAR",
    signals: list[str] | None = None,
    target: str | None = None,
    source_image_review: str = "not reviewed",
) -> dict:
    return {
        "classification": classification,
        "reason": reason,
        "dedupe": dedupe,
        "signals": signals or [
            "URL/identificador persistente ausente do ledger e do vault",
            "sem correspondência normalizada de título no lote",
        ],
        "target": target,
        "source_image_review": source_image_review,
        "criteria": {
            "female_allegory": criterion(*female),
            "legal_political_function": criterion(*legal),
            "period_or_cohort": criterion(*period),
            "accepted_support": criterion(*support),
        },
    }


# Human decisions.  No regime, Iconclass, purification indicator, or score is
# inferred here.
DECISIONS: dict[int, dict] = {
    575: decision(
        "revisar",
        "Título sugere personagens alegóricos, mas a fonte capturada não comprova figura feminina, data, suporte ou função jurídico-política.",
        ("uncertain", "O título menciona apenas personagens alegóricos."),
        ("uncertain", "“Litis” sugere matéria jurídica, sem função do objeto documentada."),
        ("uncertain", "Data não informada na captura institucional."),
        ("uncertain", "Suporte não informado na captura institucional."),
    ),
    576: decision(
        "revisar",
        "Justitia é nomeada, porém faltam data, suporte e contexto funcional do objeto.",
        ("confirmed", "O título institucional nomeia Justitia acompanhada de Nike."),
        ("uncertain", "A presença de Justitia não basta para provar a função jurídico-política do objeto."),
        ("uncertain", "Data não informada."),
        ("uncertain", "Suporte não informado."),
    ),
    577: decision(
        "revisar",
        "Justitia é nomeada, mas a captura não fecha data, suporte nem função do objeto.",
        ("confirmed", "O título institucional nomeia Justitia."),
        ("uncertain", "Função jurídico-política não descrita."),
        ("uncertain", "Data não informada."),
        ("uncertain", "Suporte não informado."),
    ),
    578: decision(
        "revisar",
        "O título inclui magistratura, mas não comprova que a figura alegórica seja feminina nem o suporte/período.",
        ("uncertain", "O título não identifica o gênero das figuras."),
        ("uncertain", "Magistratura aparece no título, sem descrição funcional do objeto."),
        ("uncertain", "Data não informada."),
        ("uncertain", "Suporte não informado."),
    ),
    579: decision(
        "revisar",
        "Justitia é nomeada, porém data, suporte e função jurídico-política permanecem lacunas.",
        ("confirmed", "O título institucional nomeia Justitia e Caritas."),
        ("uncertain", "A função do objeto não é descrita."),
        ("uncertain", "Data não informada."),
        ("uncertain", "Suporte não informado."),
    ),
    580: decision(
        "revisar",
        "Justitia e Sapientia são nomeadas, mas faltam data, suporte e contexto funcional.",
        ("confirmed", "O título institucional nomeia Justitia e Sapientia."),
        ("uncertain", "Função jurídico-política do objeto não documentada."),
        ("uncertain", "Data não informada."),
        ("uncertain", "Suporte não informado."),
    ),
    581: decision(
        "descartar",
        "Duplicata exata do ARK e da fotografia Agence Rol de 1916 já incorporada ao registro canônico.",
        ("confirmed", "O título institucional identifica busto da República."),
        ("confirmed", "Busto republicano documentado em fotografia de imprensa."),
        ("confirmed", "1916 na fonte BnF."),
        ("uncertain", "Fotografia de imprensa; apenas evidência do suporte escultórico."),
        dedupe="DUPLICATE",
        signals=["ARK idêntico btv1b69528790", "mesmo título, agência e data"],
        target="records.jsonl item 4d84fe99-7db7-5ea5-96cd-bca3bd57a189; vault SCOUT-433",
        source_image_review="not required: exact persistent identifier",
    ),
    582: decision(
        "revisar",
        "Mesmo núcleo de título, autor e tipologia de item canônico, mas ARKs distintos; pode ser estado/variante.",
        ("confirmed", "O título da estampa nomeia a République."),
        ("confirmed", "Caricatura política republicana identificada no catálogo."),
        ("confirmed", "1904 na fonte BnF."),
        ("confirmed", "O título institucional explicita estampe."),
        dedupe="SIMILAR",
        signals=["título normalizado Le hochet de la République", "mesmo autor Jean Veber", "ARK diferente"],
        target="records.jsonl item 442ad547-ffbb-5581-8290-7d514f87d0d4; vault SCOUT-465",
    ),
    583: decision(
        "revisar",
        "Fotografia/estado diferente da République de Clésinger já catalogada; requer adjudicação de variante.",
        ("confirmed", "O título identifica a République de Clésinger."),
        ("confirmed", "A escultura republicana é o objeto representado."),
        ("confirmed", "1900 para a fotografia na fonte BnF."),
        ("uncertain", "O item catalogado é fotografia; ela apenas documenta o suporte escultórico."),
        dedupe="SIMILAR",
        signals=["mesmo núcleo République de Clésinger", "mesmo Atelier Nadar e ano", "ARK diferente"],
        target="records.jsonl item 81efcd9a-e5c1-5525-a2ed-6c4cbd0c3954; vault SCOUT-431/SCOUT-554",
    ),
    584: decision(
        "descartar",
        "Fotografia de pessoas chamadas “les Mariannes” antes de desfile, não personificação feminina do Estado.",
        ("no", "O título usa Mariannes para pessoas fotografadas, não para alegoria."),
        ("no", "Nenhuma função jurídico-política alegórica é documentada."),
        ("confirmed", "1927 na fonte BnF."),
        ("confirmed", "Fotografia de imprensa."),
    ),
    585: decision(
        "revisar",
        "Estampa revolucionária pré-1800 potencialmente elegível, mas a miniatura oficial é pequena demais para fechar a alegoria feminina.",
        ("uncertain", "Imagem oficial de baixa resolução sugere figura feminina, sem confirmação suficiente."),
        ("confirmed", "Documento emitido em nome da República francesa para oficiais civis e militares."),
        ("confirmed", "1798; elegível como pre-1800-genealogia, period_extended=true."),
        ("confirmed", "O título institucional explicita estampe."),
        source_image_review="reviewed: official image low resolution, inconclusive",
    ),
    586: decision(
        "revisar",
        "Provável variante de obra revolucionária já catalogada; ARK diferente impede descarte automático.",
        ("confirmed", "A fonte/título da série republicana identifica a personificação."),
        ("confirmed", "Unidade e indivisibilidade da República em contexto revolucionário."),
        ("confirmed", "1793–1794; pre-1800-genealogia, period_extended=true."),
        ("confirmed", "O título institucional explicita estampe."),
        dedupe="SIMILAR",
        signals=["mesmo título-base Unité indivisibilité de la République", "mesma data", "ARK diferente"],
        target="records.jsonl item b52f4742-c987-5a72-8b5d-720b39aa234d; vault SCOUT-432/SCOUT-555",
    ),
    587: decision(
        "revisar",
        "Vista fotográfica da mesma série monumental de 1889 já catalogada; possível variante.",
        ("confirmed", "O título identifica Statue de la République."),
        ("confirmed", "Monumento republicano da exposição de 1889."),
        ("confirmed", "1889 na fonte BnF."),
        ("uncertain", "O item é fotografia que documenta escultura; a fotografia não é suporte elegível por si."),
        dedupe="SIMILAR",
        signals=["mesma estátua/Exposição de 1889", "mesmo fotógrafo Blancard", "ARK diferente"],
        target="records.jsonl item 942ef9d3-f17b-5ced-a36f-c2277a4018a1; vault SCOUT-435/SCOUT-556",
    ),
    588: decision(
        "revisar",
        "Segunda vista fotográfica da mesma série monumental de 1889; requer decisão de variante.",
        ("confirmed", "O título identifica Statue de la République."),
        ("confirmed", "Monumento republicano da exposição de 1889."),
        ("confirmed", "1889 na fonte BnF."),
        ("uncertain", "O item é fotografia que documenta escultura; a fotografia não é suporte elegível por si."),
        dedupe="SIMILAR",
        signals=["mesma estátua/Exposição de 1889", "mesmo fotógrafo Blancard", "ARK diferente"],
        target="records.jsonl item 942ef9d3-f17b-5ced-a36f-c2277a4018a1; vault SCOUT-435/SCOUT-556",
    ),
    589: decision(
        "integrar",
        "Objeto único do Met; imagem oficial confirma alegoria feminina da abolição, contexto político, data e terracota escultórica.",
        ("confirmed", "Imagem oficial mostra figura feminina da Liberdade/República com barrete frígio e correntes rompidas."),
        ("confirmed", "Título institucional explicita a abolição da escravidão; a cena articula emancipação política e jurídica."),
        ("confirmed", "ca. 1848 na ficha do Met."),
        ("confirmed", "Terracotta; classificação institucional Sculpture."),
        source_image_review="confirmed: official Met image inspected",
    ),
    590: decision(
        "descartar",
        "Alegoria sazonal do Inverno sem função jurídico-política documentada.",
        ("uncertain", "O título identifica alegoria sazonal, mas não explicita gênero."),
        ("no", "O objeto é alegoria do Inverno, sem vínculo jurídico-político na ficha."),
        ("uncertain", "Data não confirmada na captura."),
        ("confirmed", "Oil on canvas."),
    ),
    591: decision(
        "integrar",
        "Objeto único do Met; imagem e ficha confirmam Liberdade feminina revolucionária em estampa de ca. 1794.",
        ("confirmed", "Imagem oficial mostra Liberdade feminina sobre correntes rompidas."),
        ("confirmed", "A personificação revolucionária de La Liberté possui função político-jurídica explícita."),
        ("confirmed", "ca. 1794; pre-1800-genealogia, period_extended=true."),
        ("confirmed", "Etching and pointillé."),
        source_image_review="confirmed: official Met image inspected",
    ),
    592: decision(
        "descartar",
        "Sepultura de pessoa chamada Marianne Lincke; falso positivo onomástico.",
        ("no", "Marianne é nome próprio da pessoa sepultada."),
        ("no", "Nenhuma função alegórica jurídico-política."),
        ("uncertain", "Data não confirmada."),
        ("no", "Registro fotográfico de sepultura biográfica."),
    ),
    593: decision(
        "descartar",
        "Lápide de Marianne Willemer; pessoa biográfica, não alegoria.",
        ("no", "Marianne é nome próprio."),
        ("no", "Nenhuma função alegórica jurídico-política."),
        ("uncertain", "Data não confirmada."),
        ("no", "Lápide biográfica."),
    ),
    594: decision(
        "descartar",
        "Lápide de Marianne Sonneborn; pessoa biográfica, não alegoria.",
        ("no", "Marianne é nome próprio da pessoa falecida."),
        ("no", "Nenhuma função alegórica jurídico-política."),
        ("uncertain", "Apenas a morte em 1806 aparece no título; não é data segura do objeto."),
        ("no", "Lápide biográfica."),
    ),
    595: decision(
        "revisar",
        "Título promete Marianne da França, mas faltam data, suporte e descrição visual suficiente.",
        ("confirmed", "O título institucional identifica Marianne van Frankrijk."),
        ("confirmed", "Marianne da França é personificação político-estatal."),
        ("uncertain", "Data não informada."),
        ("uncertain", "Suporte não informado."),
    ),
    596: decision(
        "descartar",
        "Sepultura de Marianne Schadow; pessoa biográfica, não alegoria.",
        ("no", "Marianne é nome próprio."),
        ("no", "Nenhuma função alegórica jurídico-política."),
        ("uncertain", "Data não confirmada."),
        ("no", "Sepultura biográfica."),
    ),
    597: decision(
        "descartar",
        "Memorial de Paul e Marianne Ehrlich; falso positivo onomástico.",
        ("no", "Marianne é pessoa nomeada no memorial."),
        ("no", "Nenhuma função alegórica jurídico-política."),
        ("uncertain", "Data não confirmada."),
        ("no", "Memorial biográfico."),
    ),
    598: decision(
        "revisar",
        "Moeda francesa de 1 franc/1849 semanticamente coincide com a Cérès republicana já canônica; requer confronto de tipo/denominação.",
        ("confirmed", "O tipo republicano/Cérès é feminino."),
        ("confirmed", "Moeda da República francesa."),
        ("confirmed", "1849 na ficha institucional."),
        ("confirmed", "Moeda."),
        dedupe="SIMILAR",
        signals=["mesmo tipo Cérès/República e ano", "denominação 1 franc versus 5 francs"],
        target="records.jsonl item 1444ee85-06cf-59c5-9070-6a2f684cb269; vault SCOUT-094",
    ),
    599: decision(
        "descartar",
        "Duplicata exata do ARK btv1b6952880n já registrado no ledger.",
        ("confirmed", "Busto da República no título institucional."),
        ("confirmed", "Busto republicano documentado em fotografia de imprensa."),
        ("confirmed", "1916."),
        ("uncertain", "Fotografia de imprensa; apenas evidência do suporte escultórico."),
        dedupe="DUPLICATE",
        signals=["ARK idêntico btv1b6952880n", "mesmo título, agência e data"],
        target="records.jsonl item 4d84fe99-7db7-5ea5-96cd-bca3bd57a189; vault SCOUT-471",
        source_image_review="not required: exact persistent identifier",
    ),
    600: decision(
        "descartar",
        "Retrato de Marianne Vogelweid, pessoa identificada como esposa de Hans Vogelweid.",
        ("no", "Marianne é nome próprio da retratada."),
        ("no", "Nenhuma função alegórica jurídico-política."),
        ("confirmed", "1913 na fonte BnF."),
        ("uncertain", "Suporte não explicitado na captura."),
    ),
    601: decision(
        "integrar",
        "Medalha espanhola de 1873, única; descrição e imagem oficiais confirmam matrona republicana, barrete frígio e nível.",
        ("confirmed", "Matrona sentada com gorro frígio na descrição e imagem oficiais."),
        ("confirmed", "Medalha de proclamação da Primeira República Espanhola."),
        ("confirmed", "11 de fevereiro de 1873 no objeto."),
        ("confirmed", "Medalha."),
        source_image_review="confirmed: official Ceres/Europeana image inspected",
    ),
    602: decision(
        "integrar",
        "Ficha numismática única; fonte e imagem confirmam República Francesa sentada, fasces, barrete frígio e lema de 1870.",
        ("confirmed", "A descrição identifica alegoria feminina da República Francesa."),
        ("confirmed", "Inscrições REPUBLIQUE FRANÇAISE e LIBERTÉ ÉGALITÉ FRATERNITÉ."),
        ("confirmed", "4 de setembro de 1870 no reverso."),
        ("confirmed", "Ficha numismática."),
        source_image_review="confirmed: official Ceres/Europeana image inspected",
    ),
    603: decision(
        "revisar",
        "Título confirma Respublica e Justitia, mas data, suporte e contexto institucional do objeto permanecem abertos.",
        ("confirmed", "Respublica, Caritas, Justitia e Prudentia são nomeadas."),
        ("uncertain", "O título não explica a função jurídico-política do objeto."),
        ("uncertain", "Data não informada."),
        ("uncertain", "Suporte não informado."),
    ),
    604: decision(
        "integrar",
        "Relevo único de Córdoba; ficha e imagem oficiais confirmam figura feminina republicana com barrete frígio, balança e inscrição cívica.",
        ("confirmed", "Descrição e imagem mostram figura feminina."),
        ("confirmed", "Inscrição PLAZA DE LA REPÚBLICA e balança."),
        ("confirmed", "1931."),
        ("confirmed", "Placa escultórica em alto-relevo."),
        source_image_review="confirmed: official Ceres/Europeana image inspected",
    ),
    605: decision(
        "integrar",
        "Medalha única de Lyon; descrição e imagem oficiais confirmam cabeça feminina da República Francesa e data 1872.",
        ("confirmed", "Cabeça da alegoria da República Francesa."),
        ("confirmed", "Inscrição REPUBLIQUE FRANÇAISE em medalha de exposição universal."),
        ("confirmed", "1872."),
        ("confirmed", "Medalha."),
        source_image_review="confirmed: official Ceres/Europeana image inspected",
    ),
    606: decision(
        "revisar",
        "Selo italiano de 1953 coincide semanticamente com a série Siracusana/Italia Turrita já canônica; precisa confronto de emissão/denominação.",
        ("uncertain", "O catálogo identifica Republica Italiana; a figura feminina precisa de confronto visual da emissão."),
        ("confirmed", "Selo estatal italiano."),
        ("confirmed", "1953 no título/descrição institucional."),
        ("confirmed", "Frimärke: selo postal."),
        dedupe="SIMILAR",
        signals=["mesma emissão Siracusana/Italia Turrita de 1953", "objeto/denominação não confrontados"],
        target="records.jsonl item 5e332b45-467b-5e4a-b73a-07bab0a2493a; vault SCOUT-482",
    ),
    607: decision(
        "integrar",
        "Estampa satírica única; descrição e imagem oficiais confirmam jovem República expulsando um rei no contexto da queda de Napoleão III.",
        ("confirmed", "Jovem com gorro frígio e túnica clássica, identificada como República."),
        ("confirmed", "Sátira sobre a proclamação da Terceira República e Europa sem monarquias."),
        ("confirmed", "A série foi publicada em 1870."),
        ("confirmed", "Estampa."),
        source_image_review="confirmed: official Ceres/Europeana image inspected",
    ),
    608: decision(
        "revisar",
        "Veritas e justiça divina são nomeadas, mas gênero, data, suporte e função jurídico-política secular não estão fechados.",
        ("uncertain", "O título não explicita gênero."),
        ("uncertain", "Contexto moral-religioso; função jurídico-política não comprovada."),
        ("uncertain", "Data não informada."),
        ("uncertain", "Suporte não informado."),
    ),
    609: decision(
        "revisar",
        "Justitia é clara, mas há candidato semanticamente equivalente no vault e faltam data/suporte para decidir se é outro objeto.",
        ("confirmed", "Título institucional identifica Gerechtigkeit (Iustitia)."),
        ("uncertain", "Função do objeto não descrita."),
        ("uncertain", "Data não informada."),
        ("uncertain", "Suporte não informado."),
        dedupe="SIMILAR",
        signals=["mesmo núcleo Gerechtigkeit/Justitia", "identificadores de objeto distintos"],
        target="vault SCOUT-347; sem alvo inequívoco no ledger",
    ),
    610: decision(
        "revisar",
        "Tema judicial é explícito, mas a captura não comprova alegoria feminina, data ou suporte.",
        ("uncertain", "O título não identifica figura feminina."),
        ("confirmed", "O título explicita julgamento imparcial dos magistrados."),
        ("uncertain", "Data não informada."),
        ("uncertain", "Suporte não informado."),
    ),
    611: decision(
        "revisar",
        "Imagem da Justiça é mencionada, mas faltam gênero confirmado, data, suporte e função do objeto.",
        ("uncertain", "“Bilde der Gerechtigkeit” não basta para confirmar figura feminina."),
        ("uncertain", "Justiça é tema, sem função jurídico-política do objeto."),
        ("uncertain", "Data não informada."),
        ("uncertain", "Suporte não informado."),
    ),
    612: decision(
        "descartar",
        "Folha de Stammbuch manuscrita/desenhada de 1648; suporte fora do recorte de integração pronta.",
        ("confirmed", "Justizia e Pax são nomeadas."),
        ("uncertain", "Função jurídico-política não documentada."),
        ("confirmed", "3 de agosto de 1648; pre-1800-genealogia possível."),
        ("no", "Folha manuscrita a pena, tinta e ouro; suporte inelegível nesta fila."),
    ),
    613: decision(
        "descartar",
        "Pintura religiosa em madeira, 1701–1800, sem alegoria feminina ou função jurídico-política comprovadas.",
        ("no", "A descrição não identifica figura alegórica feminina."),
        ("no", "Tema religioso “Deus governa tudo justamente”, sem função jurídico-política documentada."),
        ("confirmed", "1701–1800."),
        ("confirmed", "Pintura sobre madeira, mas os demais critérios falham."),
    ),
    614: decision(
        "revisar",
        "Estado de estampa do 18 mars; imagem mostra cena coletiva e o lote contém outro estado muito próximo.",
        ("uncertain", "Figura feminina pode estar presente, mas não é confirmada como alegoria."),
        ("confirmed", "Título e cena remetem ao 18 de março/Comuna, com função política."),
        ("confirmed", "1894."),
        ("confirmed", "Estampa."),
        dedupe="SIMILAR",
        signals=["mesmo título-base, autor e ano de SCOUT-616", "estados/ARKs distintos"],
        target="intra-lote SCOUT-616",
        source_image_review="reviewed: official image, variant relationship unresolved",
    ),
    615: decision(
        "descartar",
        "Imagem oficial mostra cena de gênero com mulher e homem, sem personificação jurídico-política.",
        ("no", "Mulher representada como personagem narrativa, não alegoria."),
        ("no", "Nenhuma função jurídico-política comprovada."),
        ("confirmed", "1894."),
        ("confirmed", "Estampa."),
        source_image_review="reviewed: official image shows no allegory",
    ),
    616: decision(
        "revisar",
        "Outro estado da estampa 18 mars; similaridade intra-lote exige adjudicação antes de integrar.",
        ("uncertain", "Cena coletiva; figura feminina não confirmada como alegoria."),
        ("confirmed", "Título e cena remetem ao 18 de março/Comuna, com função política."),
        ("confirmed", "1894."),
        ("confirmed", "Estampa."),
        dedupe="SIMILAR",
        signals=["mesmo título-base, autor e ano de SCOUT-614", "estados/ARKs distintos"],
        target="intra-lote SCOUT-614",
        source_image_review="reviewed: official image, variant relationship unresolved",
    ),
    617: decision(
        "descartar",
        "Imagem oficial mostra cena social/narrativa, sem personificação jurídico-política.",
        ("no", "Nenhuma alegoria feminina identificável."),
        ("no", "Função jurídico-política não comprovada."),
        ("confirmed", "1894."),
        ("confirmed", "Estampa."),
        source_image_review="reviewed: official image shows no allegory",
    ),
    618: decision(
        "descartar",
        "Le lait é cena social, sem alegoria feminina jurídico-política documentada.",
        ("no", "Título e registro não identificam personificação."),
        ("no", "Função jurídico-política não documentada."),
        ("confirmed", "1916."),
        ("confirmed", "Estampa."),
    ),
    619: decision(
        "revisar",
        "Estampa de auxílio nacional com função política/social, mas a fonte textual não confirma alegoria feminina.",
        ("uncertain", "Figura alegórica feminina não comprovada."),
        ("confirmed", "Secours national é dispositivo político de auxílio de guerra."),
        ("confirmed", "1915."),
        ("confirmed", "Estampa."),
    ),
    620: decision(
        "descartar",
        "O título identifica dois poilus, figuras masculinas; falha o critério de alegoria feminina.",
        ("no", "Deux poilus identifica dois soldados homens."),
        ("uncertain", "Contexto de guerra, sem função alegórica jurídica."),
        ("confirmed", "1915."),
        ("confirmed", "Estampa."),
    ),
    621: decision(
        "revisar",
        "Estampa de auxílio aos feridos com função político-social, mas alegoria feminina não confirmada.",
        ("uncertain", "Figura alegórica feminina não comprovada."),
        ("confirmed", "Aide aux blessés documenta mobilização de auxílio de guerra."),
        ("confirmed", "1915."),
        ("confirmed", "Estampa."),
    ),
    622: decision(
        "revisar",
        "Estampa de auxílio aos mutilados de guerra; função social confirmada, alegoria feminina ainda incerta.",
        ("uncertain", "Figura alegórica feminina não comprovada."),
        ("confirmed", "Aide aux mutilés de guerre possui função político-social explícita."),
        ("confirmed", "1915."),
        ("confirmed", "Estampa."),
    ),
    623: decision(
        "descartar",
        "Almanaque antijansenista de 1654; não há alegoria feminina ou função jurídico-política compatível comprovada.",
        ("no", "Título/fonte não identificam alegoria feminina."),
        ("no", "Polêmica confessional, sem função jurídico-política comprovada para o corpus."),
        ("confirmed", "1654; pre-1800, mas os demais critérios falham."),
        ("confirmed", "Estampa/almanach."),
    ),
    624: decision(
        "revisar",
        "Frontispício de tese pré-1800 potencialmente genealógico; imagem/contexto da tese precisam confirmar alegoria e função jurídica.",
        ("uncertain", "Alegoria feminina não confirmada na captura textual."),
        ("uncertain", "Função paratextual existe, mas o caráter jurídico da tese não foi comprovado."),
        ("confirmed", "Ficha registra 1641 e título menciona dedicação de 1670; divergência a resolver; period_extended=true."),
        ("confirmed", "Estampa usada como frontispício."),
    ),
}


# Explicit source-proven note corrections.  Each replacement is scoped to one
# candidate and is recorded in the queue.
CORRECTIONS: dict[int, list[dict[str, str]]] = {
    581: [
        {"field": "suporte", "from": "indeterminado", "to": "fotografia", "evidence": "Título BnF: photographie de presse"},
    ],
    582: [
        {"field": "suporte", "from": "selo", "to": "estampa", "evidence": "Título BnF: [estampe]"},
    ],
    583: [
        {"field": "suporte", "from": "indeterminado", "to": "fotografia", "evidence": "Título BnF: [photographie, tirage de démonstration]"},
    ],
    584: [
        {"field": "suporte", "from": "indeterminado", "to": "fotografia", "evidence": "Título BnF: [photographie de presse]"},
    ],
    585: [
        {"field": "suporte", "from": "selo", "to": "estampa", "evidence": "Título BnF: [estampe]"},
    ],
    586: [
        {"field": "suporte", "from": "selo", "to": "estampa", "evidence": "Título BnF: [estampe]"},
    ],
    587: [
        {"field": "suporte", "from": "monumento", "to": "fotografia", "evidence": "Título BnF: [photographie]; a imagem documenta uma estátua"},
    ],
    588: [
        {"field": "suporte", "from": "monumento", "to": "fotografia", "evidence": "Título BnF: [photographie]; a imagem documenta uma estátua"},
    ],
    589: [
        {"field": "suporte", "from": "monumento", "to": "escultura", "evidence": "Ficha Met: Terracotta; classificação Sculpture"},
        {"field": "citacao", "from": "inversão automática do nome institucional do autor", "to": "ANONYMOUS, French School, 19th Century", "evidence": "Campo de autoria da ficha do Met"},
    ],
    590: [
        {"field": "suporte", "from": "indeterminado", "to": "pintura", "evidence": "Ficha Met: Oil on canvas"},
    ],
    599: [
        {"field": "url", "from": "http://gallica.bnf.fr/ark:/12148/btv1b6952880n", "to": "https://gallica.bnf.fr/ark:/12148/btv1b6952880n", "evidence": "ARK Gallica institucional resolve em HTTPS"},
        {"field": "suporte", "from": "indeterminado", "to": "fotografia", "evidence": "Título: press photograph"},
    ],
    601: [
        {"field": "pais", "from": "BR", "to": "ES", "evidence": "Descrição: Medalla de Proclamación de la Iª República Española"},
        {"field": "autoria", "from": "Grabador: García, J.", "to": "García, J. (grabador)", "evidence": "Campo de autoria do catálogo Ceres"},
        {"field": "citacao", "from": "J., Grabador: García,", "to": "GARCÍA, J.", "evidence": "Autoria institucional normalizada na citação"},
    ],
    602: [
        {"field": "pais", "from": "BR", "to": "FR", "evidence": "Descrição: REPUBLIQUE FRANÇAISE; Comité Provisoire de Lyon"},
        {"field": "suporte", "from": "moeda", "to": "ficha", "evidence": "Tipo/título institucional: Ficha"},
    ],
    604: [
        {"field": "pais", "from": "BR", "to": "ES", "evidence": "Descrição: escudo e Plaza de la República de Córdoba"},
        {"field": "suporte", "from": "indeterminado", "to": "escultura", "evidence": "Descrição: placa com decoração em alto-relevo"},
        {"field": "autoria", "from": "Moreno, Enrique com biografia embutida", "to": "Moreno, Enrique", "evidence": "Campo de autoria do catálogo Ceres"},
        {"field": "citacao", "from": "entrada iniciada pela data de morte", "to": "MORENO, Enrique", "evidence": "Autoria institucional normalizada na citação"},
    ],
    605: [
        {"field": "pais", "from": "BR", "to": "FR", "evidence": "Descrição: REPUBLIQUE FRANÇAISE; Exposition Universelle de Lyon"},
        {"field": "suporte", "from": "moeda", "to": "medalha", "evidence": "Título/tipo institucional: Medalla"},
    ],
    606: [
        {"field": "titulo", "from": "multiline-invalid-yaml", "to": "Frimärke ur Gösta Bodmans filatelistiska motivsamling, påbörjad 1950. Frimärke från Italien, 1953. Motiv av \"Republica Italiana\"", "evidence": "Título/descrição do DigitaltMuseum"},
        {"field": "data_estimada", "from": "", "to": "1953", "evidence": "Título/descrição: Frimärke från Italien, 1953"},
        {"field": "pais", "from": "BR", "to": "IT", "evidence": "Título/descrição: Frimärke från Italien"},
        {"field": "suporte", "from": "indeterminado", "to": "selo", "evidence": "Frimärke significa selo postal; objeto filatélico no catálogo"},
    ],
    607: [
        {"field": "data_estimada", "from": "", "to": "1870", "evidence": "Descrição institucional: a série La Criatura começou em agosto de 1870"},
        {"field": "pais", "from": "BR", "to": "ES", "evidence": "Estampa de Francisco Ortego, publicada na série espanhola La Criatura"},
        {"field": "suporte", "from": "moeda", "to": "estampa", "evidence": "Título/tipo institucional: Estampa"},
        {"field": "autoria", "from": "Ortego y Vereda com locais/datas embutidos", "to": "Ortego y Vereda, Francisco (1833–1881), dibujante e editor", "evidence": "Campo de autoria do catálogo Ceres"},
        {"field": "citacao", "from": "entrada iniciada pela data de morte", "to": "ORTEGO Y VEREDA, Francisco", "evidence": "Autoria institucional normalizada na citação"},
    ],
    612: [
        {"field": "data_estimada", "from": "", "to": "1648", "evidence": "Descrição: 3. August 1648"},
        {"field": "suporte", "from": "indeterminado", "to": "manuscrito", "evidence": "Descrição: Stammbuch, folha a pena, tinta e ouro"},
    ],
    613: [
        {"field": "data_estimada", "from": "", "to": "1701-1800", "evidence": "Descrição: Malerei auf Holz (1701/1800)"},
        {"field": "pais", "from": "FR", "to": "DE", "evidence": "Descrição localiza o objeto em Radebeul, Hoflößnitz"},
        {"field": "suporte", "from": "indeterminado", "to": "pintura", "evidence": "Descrição: Malerei auf Holz"},
    ],
}

for _sid in range(614, 624):
    CORRECTIONS.setdefault(_sid, []).append(
        {"field": "suporte", "from": "selo", "to": "estampa", "evidence": "Título BnF: [estampe]"}
    )
CORRECTIONS.setdefault(624, []).append(
    {"field": "suporte", "from": "selo", "to": "estampa", "evidence": "Título BnF: [estampe]; função de frontispício"}
)


VERIFIED_FIELDS_DEFAULT = ["titulo", "acervo", "url", "direitos"]
VERIFIED_FIELDS: dict[int, list[str]] = {
    **{sid: VERIFIED_FIELDS_DEFAULT for sid in range(575, 625)},
    **{
        sid: VERIFIED_FIELDS_DEFAULT + ["autoria", "data", "pais", "suporte"]
        for sid in [581, 582, 583, 584, 585, 586, 587, 588, 589, 591, 599, 600, 601, 602, 604, 605, 606, 607, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624]
    },
    590: VERIFIED_FIELDS_DEFAULT + ["autoria", "suporte"],
    598: VERIFIED_FIELDS_DEFAULT + ["data", "pais", "suporte"],
    612: VERIFIED_FIELDS_DEFAULT + ["autoria", "data", "suporte"],
    613: VERIFIED_FIELDS_DEFAULT + ["autoria", "data", "pais", "suporte"],
}


PATCH_META: dict[int, dict] = {
    589: {
        "place": "France",
        "summary": "Terracotta sketch of a female allegory of abolition. The official image shows a Phrygian-capped female figure breaking chains beside an enslaved Black man.",
        "motifs": ["figura feminina com barrete frígio", "correntes rompidas", "homem negro escravizado", "terracota"],
        "citation": f"ANONYMOUS, French School, 19th Century. Sketch of an Allegory of the Abolition of Slavery. ca. 1848. Terracotta. The Metropolitan Museum of Art, New York. Disponível em: https://www.metmuseum.org/art/collection/search/848124. Acesso em: {ACCESS_DATE_ABNT}.",
    },
    591: {
        "place": "France",
        "summary": "Etching and pointillé of La Liberté. The official image shows a female revolutionary personification standing over broken chains.",
        "motifs": ["figura feminina", "correntes rompidas", "atributos revolucionários", "estampa"],
        "citation": f"MONCHY, Citoyenne de. La Liberté. ca. 1794. Etching and pointillé. The Metropolitan Museum of Art, New York. Disponível em: https://www.metmuseum.org/art/collection/search/821181. Acesso em: {ACCESS_DATE_ABNT}.",
        "extra_flags": ["period-extended", "cohort-pre-1800-genealogia"],
        "extra_gap": "period_extended=true; cohort=pre-1800-genealogia",
    },
    601: {
        "place": "Spain",
        "summary": "Proclamation medal of the First Spanish Republic. The obverse presents a seated matron with Phrygian cap and level; the reverse dates the proclamation to 11 February 1873.",
        "motifs": ["matrona sentada", "barrete frígio", "nível", "inscrição REPUBLICA ESPAÑOLA"],
        "citation": f"GARCÍA, J. Medalla. 1873. Museo Arqueológico Nacional, inv. 1992/81/1611. Disponível em: http://ceres.mcu.es/pages/Main?idt=98650&inventary=1992/81/1611&table=FMUS&museum=MAN. Acesso em: {ACCESS_DATE_ABNT}.",
    },
    602: {
        "place": "France",
        "summary": "Numismatic token of the French Republic and Comité Provisoire de Lyon. The seated female Republic holds a staff with Phrygian cap and a winged Victory beside fasces.",
        "motifs": ["República feminina sentada", "fasces", "barrete frígio", "Vitória alada", "lema republicano"],
        "citation": f"FICHA. 1870. Museo Cerralbo, inv. 02790. Disponível em: http://ceres.mcu.es/pages/Main?idt=2791&inventary=02790&table=FMUS&museum=MCM. Acesso em: {ACCESS_DATE_ABNT}.",
    },
    604: {
        "place": "Spain",
        "summary": "Rectangular relief plaque from Córdoba with a female Republic wearing a Phrygian cap, holding scales, above the inscription PLAZA DE LA REPÚBLICA.",
        "motifs": ["figura feminina", "barrete frígio", "balança", "inscrição PLAZA DE LA REPÚBLICA", "alto-relevo"],
        "citation": f"MORENO, Enrique. Relieve de la República - Relieve. 1931. Museo Arqueológico y Etnológico de Córdoba, inv. CE032775. Disponível em: http://ceres.mcu.es/pages/Main?idt=129502&inventary=CE032775&table=FMUS&museum=MAECO. Acesso em: {ACCESS_DATE_ABNT}.",
    },
    605: {
        "place": "France",
        "summary": "Medal of the 1872 Lyon Universal Exposition with the female head of the French Republic and the inscription REPUBLIQUE FRANÇAISE.",
        "motifs": ["cabeça feminina", "coroa de carvalho e louro", "inscrição REPUBLIQUE FRANÇAISE", "medalha"],
        "citation": f"C. T. Exposición Universal de Lyon - Medalla. 1872. Museo Cerralbo, inv. 02712. Disponível em: http://ceres.mcu.es/pages/Main?idt=2713&inventary=02712&table=FMUS&museum=MCM. Acesso em: {ACCESS_DATE_ABNT}.",
    },
    607: {
        "place": "Spain",
        "summary": "Spanish satirical print from 1870. A young female Republic in Phrygian cap and classical tunic kicks a king away while other monarchs leave Europe.",
        "motifs": ["República feminina", "barrete frígio", "rei expulso", "fila de monarcas", "porta Europa"],
        "citation": f"ORTEGO Y VEREDA, Francisco. Lo que puede suceder. 1870. Estampa. Museo Nacional del Romanticismo, inv. CE5714. Disponível em: http://ceres.mcu.es/pages/Main?idt=6813&inventary=CE5714&table=FMUS&museum=MNR. Acesso em: {ACCESS_DATE_ABNT}.",
    },
}


SUPPORT_TAGS = {
    "fotografia": "suporte/fotografia",
    "estampa": "suporte/estampa",
    "escultura": "suporte/escultura",
    "monumento": "suporte/monumento",
    "pintura": "suporte/pintura",
    "ficha": "suporte/moeda",
    "medalha": "suporte/moeda",
    "moeda": "suporte/moeda",
    "selo": "suporte/selo",
    "manuscrito": "suporte/manuscrito",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def note_path(sid: int) -> Path:
    matches = list(NOTES_DIR.glob(f"SCOUT-{sid} *.md"))
    if len(matches) != 1:
        raise RuntimeError(f"SCOUT-{sid}: expected one note, found {len(matches)}")
    return matches[0]


def replace_once(text: str, old: str, new: str, *, context: str) -> str:
    if old == new:
        return text
    if old not in text:
        if new in text:
            return text
        raise RuntimeError(f"{context}: expected text not found: {old!r}")
    if text.count(old) != 1:
        raise RuntimeError(f"{context}: expected one occurrence, found {text.count(old)}: {old!r}")
    return text.replace(old, new, 1)


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        raise RuntimeError("note lacks YAML frontmatter")
    _, raw, _ = text.split("---", 2)
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise RuntimeError("frontmatter is not a mapping")
    return data


def body_value(text: str, label: str) -> str:
    match = re.search(rf"^\*\*{re.escape(label)}\*\*:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def body_description(text: str) -> str:
    match = re.search(r"^### Descrição\s*\n(.*?)(?=\n### |\n\*\*Motivos|\n\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return " ".join(match.group(1).strip().split())


def normalized_url(url: str) -> str:
    parts = urlsplit(url.strip())
    scheme = "https" if parts.scheme in {"http", "https"} else parts.scheme
    host = (parts.hostname or "").lower()
    netloc = host
    if parts.port:
        netloc += f":{parts.port}"
    path = re.sub(r"/+$", "", parts.path) or "/"
    query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))
    return urlunsplit((scheme, netloc, path, query, ""))


def persistent_id(url: str) -> str:
    ark = re.search(r"ark:/12148/([^/?#]+)", url)
    if ark:
        return f"ark:/12148/{ark.group(1)}"
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query))
    if "inventary" in query:
        return f"{query.get('museum', 'CERES')}:{query['inventary']}"
    if "id" in query:
        return f"{parts.hostname}:{query['id']}"
    tail = parts.path.rstrip("/").split("/")[-1]
    return f"{parts.hostname}:{tail}" if tail else url


def apply_note_corrections() -> dict[int, list[dict]]:
    applied: dict[int, list[dict]] = {sid: [] for sid in range(575, 625)}
    for sid in range(575, 625):
        path = note_path(sid)
        text = path.read_text(encoding="utf-8")

        # Repair only the four syntactically invalid title scalars.  The source
        # wording is preserved; SCOUT-606 is folded to one line.
        if sid == 606:
            old = (
                'titulo: "Frimärke ur Gösta Bodmans filatelistiska motivsamling, påbörjad 1950.\n'
                'Frimärke från Italien, 1953. Motiv av "Republica Italiana""'
            )
            new = (
                "titulo: 'Frimärke ur Gösta Bodmans filatelistiska motivsamling, påbörjad 1950. "
                "Frimärke från Italien, 1953. Motiv av \"Republica Italiana\"'"
            )
            text = replace_once(text, old, new, context=f"SCOUT-{sid} title")
        elif sid in {615, 616, 617}:
            line = next(line for line in text.splitlines() if line.startswith("titulo: "))
            if line.startswith('titulo: "'):
                raw_title = line.removeprefix('titulo: "').removesuffix('"')
                text = replace_once(text, line, f"titulo: '{raw_title}'", context=f"SCOUT-{sid} title")
            applied[sid].append(
                {
                    "field": "titulo_yaml",
                    "from": "double-quoted scalar with unescaped inner quotes",
                    "to": "single-quoted scalar, same source text",
                    "evidence": "Structural YAML repair; no bibliographic value changed",
                    "applied": True,
                }
            )

        for correction in CORRECTIONS.get(sid, []):
            field = correction["field"]
            old_value = correction["from"]
            new_value = correction["to"]
            if sid == 606 and field == "titulo":
                applied[sid].append({**correction, "applied": True})
                continue

            if field in {"pais", "suporte", "data_estimada", "url"}:
                yaml_old = f'{field}: "{old_value}"' if field in {"data_estimada", "url"} else f"{field}: {old_value}"
                yaml_new = f'{field}: "{new_value}"' if field in {"data_estimada", "url"} else f"{field}: {new_value}"
                text = replace_once(text, yaml_old, yaml_new, context=f"SCOUT-{sid} {field}")

            if field == "pais":
                text = replace_once(text, f"  - pais/{old_value}", f"  - pais/{new_value}", context=f"SCOUT-{sid} country tag")
                text = replace_once(text, f"**País**: {old_value}", f"**País**: {new_value}", context=f"SCOUT-{sid} body country")
            elif field == "suporte":
                old_tag = SUPPORT_TAGS.get(old_value)
                new_tag = SUPPORT_TAGS[new_value]
                if old_tag and old_tag in text:
                    text = replace_once(text, f"  - {old_tag}", f"  - {new_tag}", context=f"SCOUT-{sid} support tag")
                elif new_tag not in text:
                    text = replace_once(
                        text,
                        "  - corpus/candidato",
                        f"  - corpus/candidato\n  - {new_tag}",
                        context=f"SCOUT-{sid} add support tag",
                    )
                text = replace_once(text, f"**Suporte**: {old_value}", f"**Suporte**: {new_value}", context=f"SCOUT-{sid} body support")
            elif field == "data_estimada":
                text = replace_once(text, "**Data**: indeterminada", f"**Data**: {new_value}", context=f"SCOUT-{sid} body date")
            elif field == "url":
                text = text.replace(old_value, new_value)

            applied[sid].append({**correction, "applied": True})

        # Source-proven author/citation cleanups for records that enter the patch.
        if sid == 589:
            text = replace_once(
                text,
                "CENTURY, Anonymous, French School, 19th. **Sketch of an Allegory of the Abolition of Slavery**."
                if "CENTURY, Anonymous" in text
                else "THE METROPOLITAN MUSEUM OF ART. **Sketch of an Allegory of the Abolition of Slavery**.",
                "ANONYMOUS, French School, 19th Century. **Sketch of an Allegory of the Abolition of Slavery**.",
                context="SCOUT-589 citation",
            )
            text = text.replace(
                "  - corpus/candidato\n  - suporte/escultura\n  - pais/FR\n  - suporte/escultura",
                "  - corpus/candidato\n  - pais/FR\n  - suporte/escultura",
            )
        if sid in {587, 588}:
            text = text.replace(
                "  - corpus/candidato\n  - suporte/fotografia\n  - pais/FR\n  - suporte/fotografia",
                "  - corpus/candidato\n  - pais/FR\n  - suporte/fotografia",
            )
        if sid == 601:
            text = replace_once(text, "**Criador/Gravador**: Grabador: García, J.", "**Criador/Gravador**: García, J. (grabador)", context="SCOUT-601 creator")
            text = replace_once(text, "J., Grabador: García,. **Medalla**.", "GARCÍA, J. **Medalla**.", context="SCOUT-601 citation")
        if sid == 604:
            old_creator = "**Criador/Gravador**: Moreno, Enrique (Lugar de nacimiento: Montalbán de Córdoba, 1900 - Lugar de defunción: Córdoba, 09/09/1936)"
            text = replace_once(text, old_creator, "**Criador/Gravador**: Moreno, Enrique", context="SCOUT-604 creator")
            text = replace_once(
                text,
                "09/09/1936), Moreno, Enrique (Lugar de nacimiento: Montalbán de Córdoba, 1900 - Lugar de defunción: Córdoba,. **Relieve de la República - Relieve**.",
                "MORENO, Enrique. **Relieve de la República - Relieve**.",
                context="SCOUT-604 citation",
            )
        if sid == 606:
            heading_old = (
                "## Frimärke ur Gösta Bodmans filatelistiska motivsamling, påbörjad 1950.\n"
                'Frimärke från Italien, 1953. Motiv av "Republica Italiana"'
            )
            heading_new = (
                "## Frimärke ur Gösta Bodmans filatelistiska motivsamling, påbörjad 1950. "
                'Frimärke från Italien, 1953. Motiv av "Republica Italiana"'
            )
            text = text.replace(heading_old, heading_new)
            text = replace_once(
                text,
                'Frimärke från Italien, 1953. Motiv av "Republica Italiana"**. Swedish National Museum of Science and Technology.',
                'Frimärke från Italien, 1953. Motiv av "Republica Italiana"**. 1953. Swedish National Museum of Science and Technology.',
                context="SCOUT-606 citation date",
            )
        if sid == 607:
            old_creator = "**Criador/Gravador**: Dibujante y editor: Ortego y Vereda, Francisco (Lugar de nacimiento: Madrid (m), 1833 - Lugar de defunción: París, 1881)"
            text = replace_once(
                text,
                old_creator,
                "**Criador/Gravador**: Ortego y Vereda, Francisco (1833–1881), dibujante e editor",
                context="SCOUT-607 creator",
            )
            text = replace_once(
                text,
                "1881), Dibujante y editor: Ortego y Vereda, Francisco (Lugar de nacimiento: Madrid (m), 1833 - Lugar de defunción: París,. **Lo que puede suceder. - Estampa**. National Museum of Romanticism.",
                "ORTEGO Y VEREDA, Francisco. **Lo que puede suceder. - Estampa**. 1870. National Museum of Romanticism.",
                context="SCOUT-607 citation",
            )
            text = text.replace(
                "  - corpus/candidato\n  - suporte/estampa\n  - pais/ES\n  - suporte/estampa",
                "  - corpus/candidato\n  - pais/ES\n  - suporte/estampa",
            )

        path.write_text(text, encoding="utf-8")
    return applied


def source_snapshot(sid: int) -> tuple[dict, str]:
    path = note_path(sid)
    text = path.read_text(encoding="utf-8")
    fm = frontmatter(text)
    creator = body_value(text, "Criador/Gravador")
    rights = body_value(text, "Direitos")
    field_values = {
        "titulo": fm.get("titulo", ""),
        "acervo": fm.get("acervo", ""),
        "url": fm.get("url", ""),
        "direitos": rights,
        "autoria": creator,
        "data": fm.get("data_estimada", ""),
        "pais": fm.get("pais", ""),
        "suporte": fm.get("suporte", ""),
    }
    verified = [
        field
        for field in VERIFIED_FIELDS[sid]
        if field_values.get(field) not in {"", None, "indeterminado"}
    ]
    source = {
        "institution": fm.get("acervo", ""),
        "url": fm.get("url", ""),
        "normalized_url": normalized_url(str(fm.get("url", ""))),
        "persistent_id": persistent_id(str(fm.get("url", ""))),
        "official_snapshot": f"hunt.py institutional API snapshot {SCOUT_SNAPSHOT_DATE}",
        "consulted_at": AUDIT_DATE,
        "verified_fields": verified,
        "unverified_fields": [field for field in field_values if field not in verified],
        "title": fm.get("titulo", ""),
        "creator": creator,
        "date": fm.get("data_estimada", ""),
        "country": fm.get("pais", ""),
        "support": fm.get("suporte", ""),
        "rights": rights,
        "description_excerpt": body_description(text)[:500],
    }
    return source, text


def build_record(sid: int, source: dict) -> dict:
    scout_id = f"SCOUT-{sid}"
    meta = PATCH_META[sid]
    item_id = str(uuid.uuid5(VAULT_NAMESPACE, f"iconocracy-vault-{scout_id}"))
    norm_url = source["normalized_url"]
    item_hash = hashlib.sha256(norm_url.encode("utf-8")).hexdigest()
    flags = ["scout-575-624", "source-verified", "awaiting-iconocode"] + meta.get("extra_flags", [])
    gaps = [
        "IconoCode, Iconclass, regime and purification coding intentionally pending",
        "CLIP visual dedupe skipped: runtime missing",
    ]
    if meta.get("extra_gap"):
        gaps.append(meta["extra_gap"])
    evidence_title = str(source["title"])
    evidence_note = (
        f"Source fields verified: {', '.join(source['verified_fields'])}. "
        f"Persistent identifier: {source['persistent_id']}."
    )
    return {
        "master_record_version": "1.0",
        "batch_id": BATCH_ID,
        "item_id": item_id,
        "item_hash": item_hash,
        "input": {
            "input_url": source["url"],
            "title_hint": evidence_title,
            "date_hint": str(source["date"]),
            "place_hint": meta["place"],
        },
        "webscout": {
            "search_results": [
                {
                    "evidence_id": f"scout-{sid}-official",
                    "source_type": "museum_record",
                    "title": evidence_title,
                    "url": source["url"],
                    "abnt_citation": meta["citation"],
                    "iconclass_candidates": [],
                    "notes": evidence_note,
                }
            ],
            "summary_evidence": meta["summary"],
            "gaps": gaps,
        },
        "iconocode": {
            "pre_iconographic": [],
            "codes": [],
            "interpretation": [],
            "validation": {"claim_ledger": []},
            "confidence": 0.0,
        },
        "exports": {
            "abnt_citations": [meta["citation"]],
            "audit_flags": flags,
        },
        "timestamps": {"created_at": TIMESTAMP, "updated_at": TIMESTAMP},
    }


def render() -> tuple[list[dict], list[dict]]:
    ledger_hash = sha256_file(LEDGER)
    if ledger_hash != EXPECTED_LEDGER_SHA256:
        raise RuntimeError(f"ledger hash drift: expected {EXPECTED_LEDGER_SHA256}, got {ledger_hash}")
    ledger_lines = LEDGER.read_text(encoding="utf-8").splitlines()
    if len(ledger_lines) != EXPECTED_LEDGER_ROWS:
        raise RuntimeError(f"ledger row drift: expected {EXPECTED_LEDGER_ROWS}, got {len(ledger_lines)}")
    if set(DECISIONS) != set(range(575, 625)):
        raise RuntimeError("decision matrix must contain exactly SCOUT-575..624")

    applied = apply_note_corrections()
    rows: list[dict] = []
    records: list[dict] = []
    for sid in range(575, 625):
        source, _ = source_snapshot(sid)
        d = DECISIONS[sid]
        proposed_item_id = None
        if d["classification"] == "integrar":
            record = build_record(sid, source)
            records.append(record)
            proposed_item_id = record["item_id"]
        rows.append(
            {
                "scout_id": f"SCOUT-{sid}",
                "classification": d["classification"],
                "justification": d["reason"],
                "source": source,
                "dedupe": {
                    "verdict": d["dedupe"],
                    "textual": d["dedupe"],
                    "visual": "skipped (runtime missing)",
                    "signals": d["signals"],
                    "target": d["target"],
                },
                "source_image_review": d["source_image_review"],
                "criteria": d["criteria"],
                "metadata_corrections": applied[sid],
                "patch_included": d["classification"] == "integrar",
                "proposed_item_id": proposed_item_id,
            }
        )

    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )

    counts = {label: sum(row["classification"] == label for row in rows) for label in ("integrar", "revisar", "descartar")}
    table_rows = []
    status_short = {"confirmed": "sim", "uncertain": "?", "no": "não"}
    for row in rows:
        criteria = row["criteria"]
        target = row["dedupe"]["target"] or "—"
        correction_summary = "; ".join(
            f"{c['field']}: {c['from']} → {c['to']}" for c in row["metadata_corrections"]
        ) or "—"
        table_rows.append(
            "| {id} | **{cls}** | {dedupe} | {f}/{l}/{p}/{s} | {why} | {target} | {corr} | {patch} |".format(
                id=row["scout_id"],
                cls=row["classification"],
                dedupe=row["dedupe"]["verdict"],
                f=status_short[criteria["female_allegory"]["status"]],
                l=status_short[criteria["legal_political_function"]["status"]],
                p=status_short[criteria["period_or_cohort"]["status"]],
                s=status_short[criteria["accepted_support"]["status"]],
                why=row["justification"].replace("|", "\\|"),
                target=target.replace("|", "\\|"),
                corr=correction_summary.replace("|", "\\|"),
                patch="sim" if row["patch_included"] else "não",
            )
        )

    report = f"""# Fila de integração auditável — SCOUT-575–624

## Resultado executivo

- Escopo: 50 notas consecutivas, SCOUT-575 a SCOUT-624.
- Decisão: **{counts['integrar']} integrar**, **{counts['revisar']} revisar**, **{counts['descartar']} descartar**.
- Patch pronto: {len(records)} novas linhas, exatamente os {counts['integrar']} itens classificados como `integrar`; não aplicado.
- Ledger real no início da geração: {EXPECTED_LEDGER_ROWS} registros; SHA-256 `{ledger_hash}`.
- Baseline citado no plano (`{PLAN_LEDGER_SHA256}`) estava defasado em relação ao `HEAD`; a auditoria adotou o baseline vivo, limpo e validado antes da escrita.
- CLIP: `skipped (runtime missing)`. A deduplicação textual cobriu `input_url`, `webscout.search_results[].url`, ARKs, inventários/object IDs, títulos normalizados, vault e o próprio lote.
- Imagens: as imagens institucionais dos sete itens prontos foram inspecionadas sem guardar binários no repositório.
- Fonte-base: snapshots de APIs institucionais gerados por `hunt.py` em {SCOUT_SNAPSHOT_DATE}; consulta/auditoria em {AUDIT_DATE}. Firecrawl não foi usado como prova porque o serviço estava inacessível por DNS.

## Chave de leitura

Os quatro sinais na coluna “critérios” aparecem na ordem: figura alegórica feminina / função jurídico-política / período ou coorte / suporte aceito. `sim` = comprovado; `?` = incerto; `não` = falha comprovada. A evidência granular, os campos comprovados e os sinais de deduplicação estão no JSONL correspondente.

## Fila

| SCOUT | decisão | dedupe | critérios | justificativa | alvo dedupe | correções aplicadas | patch |
|---|---|---|---|---|---|---|---|
{chr(10).join(table_rows)}

## Itens prontos

{chr(10).join(f"- **{row['scout_id']}** — `{row['proposed_item_id']}` — {row['source']['title']}" for row in rows if row['patch_included'])}

## Garantias de escopo

- Nenhuma nota recebeu `records_item_id`.
- Nenhum campo `regime`, Iconclass, `endurecimento`, `purificacao` ou escore foi alterado.
- Itens `revisar` e `descartar` não aparecem no patch.
- `data/processed/records.jsonl` e `corpus/corpus-data.json` não são escritos por este gerador.
- A versão JSONL é a trilha probatória completa; este Markdown é a fila humana.
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")

    original = [line + "\n" for line in ledger_lines]
    augmented = original + [json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n" for record in records]
    patch_text = "".join(
        difflib.unified_diff(
            original,
            augmented,
            fromfile="a/data/processed/records.jsonl",
            tofile="b/data/processed/records.jsonl",
            lineterm="\n",
        )
    )
    PATCH.parent.mkdir(parents=True, exist_ok=True)
    PATCH.write_text(patch_text, encoding="utf-8")
    return rows, records


def validate_outputs(rows: list[dict], records: list[dict]) -> dict[str, int | str]:
    expected_ids = [f"SCOUT-{sid}" for sid in range(575, 625)]
    if [row["scout_id"] for row in rows] != expected_ids:
        raise RuntimeError("queue IDs are not the exact consecutive SCOUT-575..624 sequence")
    if len({row["scout_id"] for row in rows}) != 50:
        raise RuntimeError("queue SCOUT IDs are not unique")
    for row in rows:
        if not row["justification"] or not row["source"]["url"] or not row["source"]["persistent_id"]:
            raise RuntimeError(f"{row['scout_id']}: source/identifier/justification missing")
        if set(row["criteria"]) != {
            "female_allegory",
            "legal_political_function",
            "period_or_cohort",
            "accepted_support",
        }:
            raise RuntimeError(f"{row['scout_id']}: incomplete inclusion criteria")
        if any(not value["evidence"] for value in row["criteria"].values()):
            raise RuntimeError(f"{row['scout_id']}: criterion evidence missing")
        if row["dedupe"]["verdict"] == "DUPLICATE" and row["classification"] != "descartar":
            raise RuntimeError(f"{row['scout_id']}: DUPLICATE must be discarded")
        if row["dedupe"]["verdict"] == "SIMILAR" and row["classification"] != "revisar":
            raise RuntimeError(f"{row['scout_id']}: SIMILAR must remain under review")
        if row["classification"] == "integrar" and any(
            criterion_data["status"] != "confirmed" for criterion_data in row["criteria"].values()
        ):
            raise RuntimeError(f"{row['scout_id']}: ready item lacks a confirmed criterion")
        if row["classification"] != "integrar" and row["patch_included"]:
            raise RuntimeError(f"{row['scout_id']}: non-ready item marked for patch")
        forbidden = {"regime", "iconclass", "endurecimento", "purificacao", "records_item_id"}
        if any(correction["field"].lower() in forbidden for correction in row["metadata_corrections"]):
            raise RuntimeError(f"{row['scout_id']}: forbidden metadata correction")

    queue_disk = [json.loads(line) for line in QUEUE.read_text(encoding="utf-8").splitlines()]
    if queue_disk != rows:
        raise RuntimeError("JSONL queue does not round-trip to the in-memory queue")

    patch_records = [
        json.loads(line[1:])
        for line in PATCH.read_text(encoding="utf-8").splitlines()
        if line.startswith("+{")
    ]
    if patch_records != records:
        raise RuntimeError("patch additions differ from generated ready records")
    ready_rows = [row for row in rows if row["patch_included"]]
    if len(records) != len(ready_rows):
        raise RuntimeError("patch record count differs from integrar count")
    if any(row["classification"] != "integrar" for row in ready_rows):
        raise RuntimeError("patch contains a non-integrar row")

    existing = [json.loads(line) for line in LEDGER.read_text(encoding="utf-8").splitlines()]
    existing_ids = {record["item_id"] for record in existing}
    existing_hashes = {record["item_hash"] for record in existing}
    existing_urls: set[str] = set()
    for record in existing:
        urls = [record["input"]["input_url"]]
        urls.extend(result["url"] for result in record["webscout"]["search_results"])
        for url in urls:
            if isinstance(url, str) and url.startswith(("http://", "https://")):
                existing_urls.add(normalized_url(url))
    existing_persistent_ids = {persistent_id(url) for url in existing_urls}

    new_ids = [record["item_id"] for record in records]
    new_hashes = [record["item_hash"] for record in records]
    new_urls = [normalized_url(record["input"]["input_url"]) for record in records]
    new_persistent_ids = [persistent_id(url) for url in new_urls]
    for label, values in {
        "UUID": new_ids,
        "item_hash": new_hashes,
        "normalized URL": new_urls,
        "persistent identifier": new_persistent_ids,
    }.items():
        if len(values) != len(set(values)):
            raise RuntimeError(f"intra-patch duplicate {label}")
    if set(new_ids) & existing_ids:
        raise RuntimeError("patch UUID already exists in canonical ledger")
    if set(new_hashes) & existing_hashes:
        raise RuntimeError("patch item_hash already exists in canonical ledger")
    if set(new_urls) & existing_urls:
        raise RuntimeError("patch normalized URL already exists in canonical ledger")
    if set(new_persistent_ids) & existing_persistent_ids:
        raise RuntimeError("patch persistent identifier already exists in canonical ledger")

    for row, record in zip(ready_rows, records, strict=True):
        expected_uuid = str(uuid.uuid5(VAULT_NAMESPACE, f"iconocracy-vault-{row['scout_id']}"))
        if record["item_id"] != expected_uuid or row["proposed_item_id"] != expected_uuid:
            raise RuntimeError(f"{row['scout_id']}: UUIDv5 mismatch")
        expected_hash = hashlib.sha256(row["source"]["normalized_url"].encode("utf-8")).hexdigest()
        if record["item_hash"] != expected_hash:
            raise RuntimeError(f"{row['scout_id']}: normalized URL hash mismatch")
        if record["batch_id"] != BATCH_ID:
            raise RuntimeError(f"{row['scout_id']}: batch mismatch")
        if "purificacao" in record:
            raise RuntimeError(f"{row['scout_id']}: patch must not contain purificacao")
        if record["iconocode"] != {
            "pre_iconographic": [],
            "codes": [],
            "interpretation": [],
            "validation": {"claim_ledger": []},
            "confidence": 0.0,
        }:
            raise RuntimeError(f"{row['scout_id']}: IconoCode placeholder is not empty")
        required_flags = {"scout-575-624", "source-verified", "awaiting-iconocode"}
        if not required_flags.issubset(record["exports"]["audit_flags"]):
            raise RuntimeError(f"{row['scout_id']}: required audit flags missing")

    for sid in range(575, 625):
        text = note_path(sid).read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm.get("id") != f"SCOUT-{sid}":
            raise RuntimeError(f"SCOUT-{sid}: frontmatter ID mismatch")
        if re.search(r"^records_item_id:", text, re.MULTILINE):
            raise RuntimeError(f"SCOUT-{sid}: records_item_id added before patch approval")

    if sha256_file(LEDGER) != EXPECTED_LEDGER_SHA256:
        raise RuntimeError("canonical ledger changed during audit generation")
    corpus_path = ROOT / "corpus" / "corpus-data.json"
    if sha256_file(corpus_path) != EXPECTED_CORPUS_SHA256:
        raise RuntimeError("corpus-data.json changed during audit generation")

    subprocess.run(
        ["git", "-c", "core.fsmonitor=false", "apply", "--check", str(PATCH)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    counts = {
        label: sum(row["classification"] == label for row in rows)
        for label in ("integrar", "revisar", "descartar")
    }
    return {
        "queue_rows": len(rows),
        "patch_records": len(records),
        "integrar": counts["integrar"],
        "revisar": counts["revisar"],
        "descartar": counts["descartar"],
        "ledger_sha256": sha256_file(LEDGER),
        "corpus_sha256": sha256_file(corpus_path),
    }


if __name__ == "__main__":
    queue_rows, ready_records = render()
    validation = validate_outputs(queue_rows, ready_records)
    print(
        json.dumps(
            {
                "queue_rows": len(queue_rows),
                "ready_records": len(ready_records),
                "report": str(REPORT.relative_to(ROOT)),
                "queue": str(QUEUE.relative_to(ROOT)),
                "patch": str(PATCH.relative_to(ROOT)),
                "validation": validation,
            },
            ensure_ascii=False,
        )
    )
