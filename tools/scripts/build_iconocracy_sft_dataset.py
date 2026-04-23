#!/usr/bin/env python3
"""
build_iconocracy_sft_dataset.py

Build a chat-format SFT dataset for the ICONOCRACY project.

Output: one JSON object per line with:
- messages: system/user/assistant
- metadata: task family, source file, language/style, optional record id
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "data" / "training" / "iconocracy_sft_v1_1.jsonl"
RECORDS_JSONL = REPO_ROOT / "data" / "processed" / "records.jsonl"
PURIFICATION_JSONL = REPO_ROOT / "data" / "processed" / "purification.jsonl"

SYSTEM_PROMPT = (
    "Você é um assistente de pesquisa e redação da tese ICONOCRACIA. "
    "Use voz jurídico-histórica rigorosa, preserve a terminologia mandatória do projeto "
    "e não invente fatos ausentes da evidência fornecida. Nunca traduza ENDURECIMENTO, "
    "nunca atribua Feminilidade de Estado a Mondzain e não trate claims do pipeline "
    "como prova conclusiva sem qualificação."
)

RECORD_PROMPT_TEMPLATES = [
    "A partir do registro abaixo, redija uma nota analítica curta, em português, com voz jurídico-histórica, sem inventar fatos ausentes.",
    "Leia o item do corpus abaixo e produza um comentário analítico inicial, distinguindo observação e inferência.",
    "Converta o registro abaixo em um parágrafo acadêmico preliminar, com cautela epistêmica.",
    "Produza uma leitura inicial do item abaixo para uso em pesquisa, indicando relevância sem exagerar a conclusão.",
]

PURIFICATION_PROMPT_TEMPLATES = [
    "Interprete os indicadores abaixo em linguagem acadêmica curta, sem inventar imagem ausente.",
    "Com base apenas nos indicadores fornecidos, redija um diagnóstico breve do nível de purificação do item.",
    "A partir desta linha de codificação, escreva uma leitura comparativa curta do caso no corpus.",
    "Explique, de modo sintético, o que os indicadores abaixo sugerem sobre a morfologia alegórica do item.",
]


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def mk_example(user: str, assistant: str, task_type: str, source_file: str, **metadata: Any) -> Dict[str, Any]:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user.strip()},
            {"role": "assistant", "content": assistant.strip()},
        ],
        "metadata": {
            "task_type": task_type,
            "source_file": source_file,
            "language": "pt-BR",
            "style": "juridico-historico",
            **metadata,
        },
    }


def choose(options: Sequence[str], seed_key: str) -> str:
    rng = random.Random(seed_key)
    return rng.choice(list(options))


def normalize_place(place: str) -> str:
    mapping = {
        "Brazil": "Brasil",
        "France": "França",
        "United States": "Estados Unidos",
        "United Kingdom": "Reino Unido",
        "Germany": "Alemanha",
        "Belgium": "Bélgica",
        "Austria": "Áustria",
        "Spain": "Espanha",
        "Portugal": "Portugal",
        "Europe": "Europa",
        "Italy": "Itália",
        "Netherlands": "Países Baixos",
    }
    return mapping.get(place, place)


def regime_pt(text: str) -> str:
    if not text:
        return "não especificado"
    upper = text.upper()
    mapping = {
        "FUNDACIONAL": "fundacional",
        "NORMATIVO": "normativo",
        "MILITAR": "militar",
        "CONTRA-ALEGORIA": "contra-alegórico",
    }
    return mapping.get(upper, text.lower())


def support_hint(url: str, title: str, evidence: str) -> str:
    corpus = " ".join([url or "", title or "", evidence or ""]).lower()
    hints = [
        ("poster", "cartaz"),
        ("affiche", "cartaz"),
        ("lithograph", "litografia"),
        ("litografia", "litografia"),
        ("print", "estampa"),
        ("photograph", "fotografia"),
        ("photo", "fotografia"),
        ("painting", "pintura"),
        ("óleo", "pintura"),
        ("coin", "moeda"),
        ("dollar", "moeda"),
        ("certificate", "cédula"),
        ("loan", "cartaz"),
        ("emprunt", "cartaz"),
        ("pesetas", "moeda"),
        ("franc", "moeda"),
        ("monument", "monumento"),
        ("statue", "escultura"),
        ("relief", "relevo"),
        ("stamp", "selo"),
        ("banknote", "cédula"),
    ]
    for needle, label in hints:
        if needle in corpus:
            return label
    return "suporte não explicitado"


def clean_claims_for_prompt(claims: List[str]) -> str:
    if not claims:
        return "sem claims interpretativos explícitos"
    cleaned = []
    for claim in claims:
        cleaned.append(claim.replace("Regime iconocrático:", "Hipótese de regime:"))
    return "; ".join(cleaned)


def build_guardrail_examples() -> List[Dict[str, Any]]:
    qa = [
        (
            "Posso traduzir ENDURECIMENTO como hardening para soar mais internacional?",
            "Não. Na arquitetura conceitual da tese, ENDURECIMENTO é terminologia original e mandatória. A tradução para hardening enfraquece o ganho analítico do conceito. Se a redação exigir esclarecimento para leitor estrangeiro, o procedimento correto é manter ENDURECIMENTO em português e explicá-lo contextualmente, nunca substituí-lo.",
        ),
        (
            "Feminilidade de Estado é um conceito de Mondzain, certo?",
            "Não. Iconocracia é mobilizado a partir de Mondzain, mas Feminilidade de Estado é construção original da tese. A formulação correta distingue com rigor o que é tomado de Mondzain e o que é proposto pela autora como elaboração própria.",
        ),
        (
            "Qual é a cadeia correta de rastreabilidade do corpus?",
            "A cadeia correta parte do acervo ou fonte original, passa pelo Drive e pelos manifestos de ingestão, segue pelos scripts e pelo processamento no repositório, fixa records.jsonl como superfície canônica processada e, a partir daí, alimenta corpus, tese e Atlas. O ponto decisivo é não inverter a ordem de verdade nem transformar notas derivadas em fonte primária.",
        ),
        (
            "Para acelerar a análise, a IA pode substituir a leitura do estudante no Atlas Lab?",
            "Não deve. A orientação do projeto é usar a IA como ferramenta para pensar, não como substituta da interpretação humana. No Atlas Lab, a intervenção da IA deve vir depois da observação e da comparação feitas pelo usuário, como contra-leitura, desafio reflexivo ou provocação analítica.",
        ),
        (
            "Se houver conflito entre uma nota do vault e records.jsonl, qual deles manda?",
            "A ordem de verdade do projeto privilegia a superfície canônica processada. O vault espelha, organiza e comenta, mas não substitui records.jsonl como base de exportação. Quando houver conflito, o procedimento correto é rastrear a divergência e corrigi-la no fluxo canônico, não improvisar uma solução local no espelho do vault.",
        ),
        (
            "Posso apresentar a infraestrutura técnica como coração do argumento do projeto?",
            "No projeto, não. Os documentos aprovados distinguem com prudência o que deve ser prometido à banca e o que já foi construído na prática. A infraestrutura digital pode aparecer como recurso metodológico e garantia de auditabilidade, mas não deve deslocar o eixo argumentativo da tese para uma narrativa tecnicista.",
        ),
        (
            "Ao escrever sobre a tese, devo adotar uma voz sociológica ampla?",
            "Não é o ideal. O enquadramento exigido pelo projeto é jurídico-histórico, com especial atenção à história do direito e à cultura jurídica. A abertura para colonialidade, gênero e visualidade existe, mas deve permanecer ancorada em dispositivos, suportes e problemas do campo jurídico.",
        ),
        (
            "Posso tratar os claims do pipeline como fatos consolidados?",
            "Não automaticamente. Claims do pipeline são hipóteses interpretativas úteis para triagem e organização do corpus. Eles podem orientar leitura e comparação, mas não devem ser convertidos em conclusão forte sem retorno à evidência, ao suporte material e ao contexto histórico-jurídico do item.",
        ),
    ]
    return [mk_example(q, a, "guardrails", "AGENT_CONFIG_ICONOCRACIA.md") for q, a in qa]


def build_chapter_examples() -> List[Dict[str, Any]]:
    qa = [
        (
            "Qual é o caminho crítico da tese neste momento?",
            "O caminho crítico está no capítulo sobre a colonialidade do ver. Nos planos aprovados, ele aparece como o argumento mais original e ao mesmo tempo menos maduro. O risco principal é perder a voz jurídico-penal e deslizar para um enquadramento excessivamente antropológico ou sociológico. A mitigação proposta é ancorar cada seção em dispositivos jurídicos concretos, como decretos, códigos, constituições e suportes estatais específicos.",
        ),
        (
            "Como justificar a transição do Capítulo 6 para o Capítulo 7?",
            "A transição deve ser explicitada como passagem de QUAN para QUAL dentro do desenho sequencial explanatório. O Capítulo 6 identifica padrões iconométricos, limites da quantificação e critérios de seleção. O Capítulo 7 aprofunda esses padrões por meio de casos paradigmáticos e desviantes. Assim, a mudança de escala não aparece como salto arbitrário, mas como desdobramento do que a estatística mostrou e do que ela não consegue, sozinha, demonstrar.",
        ),
        (
            "Qual é a diferença estratégica entre o plano do projeto e o plano da tese?",
            "O projeto é formulado com prudência para a banca e registra o que se pretende investigar sem prometer em excesso. Por isso preserva uma estrutura mais conservadora, em sete capítulos, evita transformar infraestrutura técnica em núcleo argumentativo e trata o Atlas como parte da síntese. A tese, por sua vez, pode mostrar o que já foi efetivamente construído e assumir uma arquitetura mais robusta, em nove capítulos, com maior explicitação metodológica e visual.",
        ),
        (
            "Por que o Capítulo 5 é metodologicamente importante mesmo sem ser o centro teórico da tese?",
            "Porque ele converte infraestrutura, protocolo e auditabilidade em contribuição metodológica demonstrável. O ganho do Capítulo 5 não está em competir com a moldura teórica, mas em mostrar como o corpus de 145+ itens, os indicadores ordinais, o IconoCode e a cadeia de validação tornam a análise comparativa verificável e replicável dentro dos limites do projeto.",
        ),
        (
            "Qual é o principal risco do Capítulo 9?",
            "O principal risco do Capítulo 9 é de dependência material e editorial. Os painéis exigem imagens adequadas, resolução suficiente, critérios de seleção coerentes e manejo cuidadoso de direitos de reprodução. Por isso, os planos já identificam a necessidade de manifests IIIF, licenças compatíveis e backup das imagens em superfícies controladas.",
        ),
        (
            "Como devo formular a utilidade do Capítulo 6 sem transformá-lo em simples relatório estatístico?",
            "O Capítulo 6 precisa converter resultado em argumento. O ponto não é apenas informar p-values, mas mostrar como os padrões iconométricos iluminam a diferença entre regimes, suportes e formas de purificação. A estatística ganha função interpretativa quando reabre a pergunta teórica sobre o modo como a alegoria feminina é domesticada, endurecida ou monumentalizada pelo Estado.",
        ),
        (
            "Qual papel o Atlas deve ocupar na lógica geral da tese?",
            "O Atlas não entra como ilustração decorativa, mas como dispositivo de demonstração. Na arquitetura consolidada da tese, ele reúne e reorganiza o que a teoria, o corpus e a análise quantitativa e qualitativa permitiram ver. Em vez de repetir o texto, ele revela relações de vizinhança, sobrevivência e contraste que dependem da montagem visual.",
        ),
        (
            "Por que o projeto mantém '~300' itens enquanto a tese trabalha com 145+ itens já codificados?",
            "Porque o projeto registra uma meta prudencial e prospectiva diante da banca, enquanto a tese já descreve um estado real de construção do corpus. Nos documentos estratégicos, essa diferença é tratada como distinção entre promessa de investigação e superfície efetivamente consolidada. O ponto importante é justificar saturação, representatividade e auditabilidade sem transformar o número exato do momento em promessa fechada do projeto.",
        ),
    ]
    return [mk_example(q, a, "chapter_planning", "docs/superpowers/specs/2026-04-11-thesis-chapter-plan.md") for q, a in qa]


def build_method_examples() -> List[Dict[str, Any]]:
    qa = [
        (
            "Explique, em termos curtos, o desenho metodológico da tese.",
            "A tese opera com métodos mistos sequenciais, em chave QUAN → QUAL → síntese. A fase quantitativa mede padrões morfológicos do corpus por meio de indicadores ordinais e testes comparativos. A fase qualitativa retorna aos casos paradigmáticos e desviantes para aprofundar aquilo que os números apenas sinalizam. A síntese final, de inspiração warburguiana, reorganiza os achados por montagem visual.",
        ),
        (
            "Qual é a função do IconoCode no projeto?",
            "O IconoCode funciona como protocolo próprio de codificação que integra descrição pré-iconográfica, identificação iconográfica com ICONCLASS e interpretação iconológica em chave jurídico-política. Sua importância está em tornar comparáveis itens heterogêneos do corpus sem dissolver o vínculo entre forma visual, suporte estatal e hipótese teórica da tese.",
        ),
        (
            "Para que servem os 10 indicadores ordinais de purificação?",
            "Eles servem para transformar impressões morfológicas dispersas em uma matriz analítica comparável. Em vez de falar genericamente de idealização ou endurecimento, o protocolo distribui a leitura em dimensões observáveis, como rigidez postural, dessexualização, serialidade e inscrição estatal. Isso permite comparar regimes, suportes e famílias alegóricas com mais rigor.",
        ),
        (
            "O que significa dizer que a tese é QUAN → QUAL, e não QUAL com números decorativos?",
            "Significa que a etapa quantitativa tem função estrutural, não ornamental. Ela não aparece para legitimar conclusões já sabidas, mas para produzir critérios de diferenciação, seleção e surpresa. A etapa qualitativa então interpreta, tensiona e historiciza esses resultados. Sem essa ordem, a tese perderia o ganho de explicitação metodológica que a distingue.",
        ),
        (
            "Como explicar o papel de Warburg sem transformar a tese em pura história da arte?",
            "Warburg entra como operador metodológico de sobrevivência, intervalo e montagem, não como substituto do problema jurídico. Pathosformel, Nachleben e Zwischenraum interessam porque permitem demonstrar a persistência e a mutação de fórmulas visuais do poder em suportes jurídicos e estatais. A ancoragem continua sendo a cultura jurídica, não uma história da arte autônoma.",
        ),
        (
            "Por que Krippendorff alpha é importante aqui?",
            "Porque o corpus usa indicadores ordinais e precisa demonstrar que a codificação não depende apenas da intuição de uma única leitora. A referência a Krippendorff alpha fornece uma via de controle para a confiabilidade intercodificadores e fortalece a legitimidade metodológica da etapa quantitativa antes da qualificação.",
        ),
    ]
    return [mk_example(q, a, "method_explainer", "AGENT_CONFIG_ICONOCRACIA.md") for q, a in qa]


def summarize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    input_block = record.get("input", {})
    webscout = record.get("webscout", {})
    iconocode = record.get("iconocode", {})
    motifs = [m.get("motif") for m in iconocode.get("pre_iconographic", []) if m.get("observed") and m.get("motif")]
    codes = [c.get("notation") for c in iconocode.get("codes", []) if c.get("notation")]
    claims = [c.get("claim_text") for c in iconocode.get("interpretation", []) if c.get("claim_text")][:3]
    regime = ""
    for claim in claims:
        if "Regime iconocrático:" in claim:
            regime = claim.split(":", 1)[1].strip()
            break
    return {
        "item_id": record.get("item_id") or record.get("id") or "unknown",
        "title": input_block.get("title_hint", "[sem título]"),
        "date": input_block.get("date_hint", "[sem data]"),
        "place": normalize_place(input_block.get("place_hint", "[sem lugar]")),
        "summary_evidence": webscout.get("summary_evidence", ""),
        "motifs": motifs[:5],
        "codes": codes[:5],
        "claims": claims,
        "source_url": input_block.get("input_url", ""),
        "regime": regime_pt(regime),
    }


def build_record_user_prompt(r: Dict[str, Any], variant: int) -> str:
    motifs = ", ".join(r["motifs"]) if r["motifs"] else "não especificados"
    codes = ", ".join(r["codes"]) if r["codes"] else "não especificados"
    claims = clean_claims_for_prompt(r["claims"])
    opener = RECORD_PROMPT_TEMPLATES[variant % len(RECORD_PROMPT_TEMPLATES)]
    if variant == 0:
        return (
            f"{opener}\n\n"
            f"Título: {r['title']}\n"
            f"Data: {r['date']}\n"
            f"Lugar: {r['place']}\n"
            f"Resumo da evidência: {r['summary_evidence']}\n"
            f"Motivos observados: {motifs}\n"
            f"Códigos: {codes}\n"
            f"Hipóteses prévias do pipeline: {claims}\n"
            f"URL: {r['source_url']}"
        )
    if variant == 1:
        return (
            f"{opener}\n\n"
            f"Considere este registro do corpus:\n"
            f"- título: {r['title']}\n"
            f"- recorte espaço-temporal: {r['place']}, {r['date']}\n"
            f"- evidência resumida: {r['summary_evidence']}\n"
            f"- motivos: {motifs}\n"
            f"- códigos: {codes}\n"
            f"- notas interpretativas prévias: {claims}"
        )
    if variant == 2:
        return (
            f"{opener}\n\n"
            f"Elabore a resposta a partir destes dados mínimos do item:\n"
            f"Título: {r['title']}\n"
            f"Contexto: {r['place']} / {r['date']}\n"
            f"Descrição disponível: {r['summary_evidence']}\n"
            f"Marcas observadas: {motifs}\n"
            f"Classificações: {codes}\n"
            f"Leituras preliminares: {claims}"
        )
    payload = {
        "titulo": r["title"],
        "data": r["date"],
        "lugar": r["place"],
        "resumo_evidencia": r["summary_evidence"],
        "motivos": r["motifs"],
        "codigos": r["codes"],
        "claims_previos": r["claims"],
        "url": r["source_url"],
    }
    return f"{opener}\n\nItem do corpus para comentário:\n{json.dumps(payload, ensure_ascii=False)}"


def build_record_assistant(r: Dict[str, Any], variant: int) -> str:
    motifs = ", ".join(r["motifs"]) if r["motifs"] else "não especificados"
    codes = ", ".join(r["codes"]) if r["codes"] else "não especificados"
    support = support_hint(r["source_url"], r["title"], r["summary_evidence"])
    claims = clean_claims_for_prompt(r["claims"])
    evidence = r["summary_evidence"] or "uma descrição sumária ainda limitada"
    title = r["title"]
    place = r["place"]
    date = r["date"]
    regime = r["regime"]

    if variant == 0:
        return (
            f"O item \"{title}\" pode ser situado, em primeira aproximação, no repertório de alegorias femininas mobilizadas em {place}, na data indicada ({date}). O que o registro autoriza afirmar com maior segurança decorre do próprio suporte, aqui reconhecível como {support}, e da evidência resumida disponível: {evidence}.\n\n"
            f"No plano descritivo, os motivos {motifs} e os códigos {codes} sugerem inserção em um vocabulário visual compatível com a hipótese geral da tese sobre a feminização alegórica do poder. Ainda assim, convém tratar as leituras já anexadas ao pipeline, {claims}, como hipóteses de trabalho e não como conclusão fechada.\n\n"
            f"Como nota inicial de pesquisa, o caso interessa porque permite observar como suporte, motivo e eventual inscrição estatal podem convergir na fabricação de uma figura feminina politicamente operativa. O passo seguinte é retornar à materialidade do item e ao seu contexto jurídico-histórico específico."
        )
    if variant == 1:
        return (
            f"Este registro parece relevante menos por oferecer, desde já, uma interpretação acabada e mais por condensar um conjunto discernível de sinais analíticos. Em {place}, no horizonte temporal de {date}, o item intitulado \"{title}\" apresenta {evidence}.\n\n"
            f"Os elementos disponíveis apontam para um circuito alegórico em que os motivos {motifs} e as classificações {codes} permitem aproximar a peça do corpus central da tese. Se houver conexão com o regime {regime}, ela deve ser trabalhada como hipótese prudente, sempre subordinada ao retorno à fonte e ao suporte.\n\n"
            f"Em termos de uso acadêmico, o registro funciona bem como ponto de entrada para discutir a mediação entre visualidade feminina e legitimação estatal, sem dispensar verificação posterior da eficácia jurídica do suporte e do contexto histórico de circulação."
        )
    if variant == 2:
        return (
            f"Tomado isoladamente, o registro não resolve o argumento da tese, mas oferece matéria suficiente para uma leitura inicial consistente. O núcleo observável está em {evidence}, articulado aos motivos {motifs}. Isso já basta para inscrever o item no campo comparativo da pesquisa, sobretudo se considerado o provável suporte {support}.\n\n"
            f"Os códigos {codes} ajudam a estabilizar a entrada do caso no repertório iconográfico, enquanto as notas interpretativas prévias do pipeline devem ser recebidas com cautela metodológica. Elas orientam a leitura, mas não substituem a distinção entre descrição, classificação e interpretação.\n\n"
            f"A utilidade analítica do item reside, portanto, em permitir uma pergunta bem formulada: de que modo esse artefato participa da transformação do corpo alegórico feminino em veículo de soberania, ordem ou pedagogia política?"
        )
    return (
        f"Há pelo menos três razões para reter este item no corpus analítico. Primeiro, porque a evidência resumida, {evidence}, já indica uma forma reconhecível de alegorização feminina em {place}. Segundo, porque os motivos {motifs} e os códigos {codes} sugerem compatibilidade com famílias visuais centrais da tese. Terceiro, porque o suporte provável, {support}, pode alterar decisivamente o peso jurídico-político da imagem.\n\n"
        f"Isso não autoriza extrapolar sem freio. Os claims prévios do pipeline devem permanecer como trilhas interpretativas provisórias. Ainda assim, o registro parece promissor para examinar como a figura feminina se converte em mediação visual de autoridade, identidade estatal ou disputa política.\n\n"
        f"Num estágio seguinte, o ganho estará em confrontar esse caso com outros do mesmo regime ou do mesmo suporte, para verificar se estamos diante de uma recorrência morfológica, de uma exceção reveladora ou de uma fissura do repertório dominante."
    )


def build_record_examples(record: Dict[str, Any]) -> List[Dict[str, Any]]:
    r = summarize_record(record)
    item_key = str(r["item_id"])
    h = int(hashlib.md5(item_key.encode()).hexdigest(), 16)
    variants = [h % 4, (h + 1) % 4]
    examples = []
    for idx, variant in enumerate(variants):
        examples.append(
            mk_example(
                build_record_user_prompt(r, variant),
                build_record_assistant(r, variant),
                "record_analysis",
                "data/processed/records.jsonl",
                record_id=r["item_id"],
                variant=idx,
            )
        )
    return examples


def classify_purification(value: float) -> str:
    if value < 1.0:
        return "baixo"
    if value < 2.0:
        return "médio"
    return "alto"


def medium_bucket(value: float) -> str:
    if value < 1.0:
        return "purificação baixa"
    if value < 2.0:
        return "purificação intermediária"
    return "purificação elevada"


def top_indicators(row: Dict[str, Any], n: int = 3) -> List[str]:
    indicator_pairs = []
    for key, value in row.items():
        if key in {"id", "purificacao_composto", "regime_iconocratico", "coded_by", "coded_at"}:
            continue
        if isinstance(value, (int, float)):
            indicator_pairs.append((key, value))
    indicator_pairs.sort(key=lambda x: (x[1], x[0]), reverse=True)
    return [name for name, _ in indicator_pairs[:n]]


def build_purification_user_prompt(row: Dict[str, Any], variant: int) -> str:
    opener = PURIFICATION_PROMPT_TEMPLATES[variant % len(PURIFICATION_PROMPT_TEMPLATES)]
    if variant == 0:
        return opener + "\n\n" + json.dumps(row, ensure_ascii=False)
    if variant == 1:
        indicators = {k: v for k, v in row.items() if k not in {"id", "regime_iconocratico", "purificacao_composto", "coded_by", "coded_at"}}
        return (
            f"{opener}\n\n"
            f"ID: {row.get('id')}\n"
            f"Regime: {row.get('regime_iconocratico')}\n"
            f"Composto: {row.get('purificacao_composto')}\n"
            f"Indicadores: {json.dumps(indicators, ensure_ascii=False)}"
        )
    if variant == 2:
        return f"{opener}\n\nFaça a leitura apenas a partir desta codificação ordinal: {json.dumps(row, ensure_ascii=False)}"
    return f"{opener}\n\nLinha de codificação para comentário: {json.dumps(row, ensure_ascii=False)}\nEvite descrever uma imagem que não foi fornecida."


def build_purification_assistant(row: Dict[str, Any], variant: int) -> str:
    top = top_indicators(row)
    top_str = ", ".join(top)
    level = classify_purification(float(row.get("purificacao_composto", 0)))
    bucket = medium_bucket(float(row.get("purificacao_composto", 0)))
    regime = row.get("regime_iconocratico", "não informado")
    rid = row.get("id", "[sem id]")
    comp = row.get("purificacao_composto")

    if variant == 0:
        return (
            f"O registro {rid} apresenta {bucket}, com composto de {comp}, no interior do regime iconocrático {regime}. Os indicadores mais salientes concentram-se em {top_str}. Isso sugere, em chave comparativa, uma leitura marcada por contenção formal, abstração corporal ou maior inscrição estatal, conforme o peso específico de cada variável.\n\n"
            f"A utilidade desse diagnóstico está em situar o caso dentro da morfologia do corpus. Ele não descreve a imagem em si, mas oferece um enquadramento prudente para discutir purificação e, quando pertinente, ENDURECIMENTO."
        )
    if variant == 1:
        return (
            f"Tomada apenas como linha de codificação, a entrada {rid} sugere um caso de nível {level} no espectro de purificação. O composto {comp} não deve ser lido isoladamente, mas articulado aos indicadores dominantes, aqui representados por {top_str}.\n\n"
            f"Em termos analíticos, isso permite comparar o item com outros do regime {regime} e perguntar se a figura tende à monumentalização, à neutralização expressiva ou à intensificação da inscrição estatal. A interpretação iconológica, contudo, ainda depende do retorno ao suporte concreto."
        )
    if variant == 2:
        return (
            f"A codificação do item {rid} aponta para {bucket}. Os valores mais altos em {top_str} indicam que a leitura do caso, no protocolo do corpus, recaiu sobre traços de despersonalização, rigidez, serialidade ou enquadramento, conforme a combinação específica observada.\n\n"
            f"Esse tipo de saída é particularmente útil para a etapa comparativa, porque transforma percepção morfológica em diagnóstico cotejável entre regimes e suportes, sem converter a planilha em substituta da interpretação histórica."
        )
    return (
        f"No estado atual da codificação, o item {rid} pode ser descrito como exemplo de {bucket} no regime {regime}. O composto {comp} ganha sentido sobretudo quando lido ao lado dos indicadores mais salientes, {top_str}.\n\n"
        f"A consequência metodológica é clara: o caso já pode entrar em comparações internas do corpus, mas a formulação de argumento forte ainda exige confrontar esse diagnóstico com a imagem, o suporte e o contexto de circulação."
    )


def build_purification_examples(row: Dict[str, Any]) -> List[Dict[str, Any]]:
    rid = str(row.get("id", "unknown"))
    h = int(hashlib.md5(rid.encode()).hexdigest(), 16)
    variants = [h % 4, (h + 2) % 4]
    examples = []
    for idx, variant in enumerate(variants):
        examples.append(
            mk_example(
                build_purification_user_prompt(row, variant),
                build_purification_assistant(row, variant),
                "purification_analysis",
                "data/processed/purification.jsonl",
                record_id=row.get("id", "unknown"),
                variant=idx,
            )
        )
    return examples


def build_corpus_explainer_examples(records: List[Dict[str, Any]], purification_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    record_count = len(records)
    pur_count = len(purification_rows)
    qa = [
        (
            "Que tipo de material empírico o corpus já oferece para um modelo especializado?",
            f"O corpus já oferece duas camadas particularmente úteis para um modelo especializado. A primeira é a camada descritivo-interpretativa de records.jsonl, hoje com {record_count} registros, que combina evidência, motivos, códigos e hipóteses de leitura. A segunda é a camada morfológica de purification.jsonl, com {pur_count} linhas codificadas, que transforma percepção visual em variáveis comparáveis. Juntas, elas permitem treinar um assistente voltado menos para improvisação genérica e mais para transformação rigorosa de dados do projeto em análise inicial útil.",
        ),
        (
            "Por que records.jsonl e purification.jsonl não devem ser confundidos?",
            "Porque eles ocupam funções distintas no ecossistema do corpus. Records.jsonl reúne a superfície processada dos itens com evidência, classificação e interpretação preliminar. Purification.jsonl, por sua vez, condensa uma leitura ordinal específica da morfologia alegórica. Confundi-los seria perder a diferença entre descrição ampla do item e medição comparativa de atributos selecionados.",
        ),
        (
            "Como um assistente treinado nesse dataset deve se comportar diante do corpus?",
            "Ele deve operar como mediador rigoroso entre estrutura e interpretação. Isso significa respeitar a ordem de verdade do pipeline, evitar transformar hipóteses em fatos, usar a terminologia própria da tese com consistência e converter registros estruturados em texto acadêmico preliminar sem apagar a necessidade de retorno à fonte, ao suporte e ao contexto jurídico-histórico de cada peça.",
        ),
    ]
    return [mk_example(q, a, "corpus_explainer", "data/processed/records.jsonl") for q, a in qa]


def build_dataset(limit_records: int | None, limit_purification: int | None, seed: int) -> List[Dict[str, Any]]:
    random.seed(seed)
    examples: List[Dict[str, Any]] = []
    examples.extend(build_guardrail_examples())
    examples.extend(build_chapter_examples())
    examples.extend(build_method_examples())

    records = load_jsonl(RECORDS_JSONL)
    if limit_records is not None:
        records = records[:limit_records]
    for record in records:
        examples.extend(build_record_examples(record))

    purification_rows = load_jsonl(PURIFICATION_JSONL)
    if limit_purification is not None:
        purification_rows = purification_rows[:limit_purification]
    for row in purification_rows:
        examples.extend(build_purification_examples(row))

    examples.extend(build_corpus_explainer_examples(records, purification_rows))
    random.shuffle(examples)
    return examples


def write_dataset(rows: Iterable[Dict[str, Any]], output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ICONOCRACY SFT dataset (chat JSONL).")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output JSONL path")
    parser.add_argument("--limit-records", type=int, default=None, help="Optional limit for records.jsonl examples")
    parser.add_argument("--limit-purification", type=int, default=None, help="Optional limit for purification.jsonl examples")
    parser.add_argument("--seed", type=int, default=42, help="Shuffle seed")
    args = parser.parse_args()

    dataset = build_dataset(args.limit_records, args.limit_purification, args.seed)
    count = write_dataset(dataset, args.output)
    print(json.dumps({
        "output": str(args.output),
        "examples_written": count,
        "limit_records": args.limit_records,
        "limit_purification": args.limit_purification,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
