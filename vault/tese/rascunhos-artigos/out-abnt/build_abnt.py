"""Build the ABNT delivery copy without changing the author's manuscript."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "O contrato visual.md"
STEM = "O contrato visual — integral ABNT"
DELIVERY = HERE / f"{STEM}.md"


def prepare_markdown() -> list[dict[str, str]]:
    content = SOURCE.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError("Expected YAML front matter")
    content = content.split("\n---\n", 1)[1].lstrip("\n")
    changes = []
    replacements = [
        (
            'Marina Warner, em *Monuments and Maidens* (1985), formulou o paradoxo com precisão: "figures of women are conventionally chosen to personify an ideal, while most women are (and have been) excluded from pursuing that ideal practically" (Warner, 1985, p. xx).',
            'Marina Warner, em *Monuments and Maidens*, observa o paradoxo entre a escolha convencional de figuras femininas para personificar ideais e a exclusão das mulheres concretas da realização desses ideais (Warner, 1985).',
            "Citação direta sem página foi convertida em paráfrase; conferir interpretação na obra.",
        ),
        (
            'Nas palavras de Pateman, as mulheres são tratadas pela tradição contratualista como simultaneamente "incapazes de consentir" e "sempre consentindo" —',
            'Na leitura de Pateman, a tradição contratualista trata as mulheres como simultaneamente incapazes de consentir e sempre disponíveis para consentir —',
            "Citação textual sem página foi convertida em paráfrase.",
        ),
        (
            'uma "longevidade notável" que atravessa séculos e culturas',
            'uma persistência histórica que atravessa séculos e culturas',
            "Citação textual sem página foi convertida em paráfrase.",
        ),
        (
            'é também o nível das "tendências essenciais da mente humana" que se expressam inconscientemente nas formas visuais',
            'é também o nível de tendências culturais profundas que se expressam nas formas visuais',
            "Citação textual sem página foi convertida em paráfrase.",
        ),
        (
            'onde Panofsky situava as "tendências essenciais da mente humana"',
            'onde Panofsky situava as tendências culturais profundas',
            "Citação textual sem página foi convertida em paráfrase.",
        ),
        (
            'o "direito sexual masculino" (*male sex-right*)',
            'o direito sexual masculino (*male sex-right*)',
            "Expressão conceitual sem página foi apresentada como paráfrase.",
        ),
        (
            '— uma "deusa", no sentido preciso de Haraway, transplantada para o cerrado.',
            '— uma figura alegórica transplantada para o cerrado.',
            "Atribuição a Haraway sem obra identificada foi retirada da cópia de entrega; revisão autoral recomendada.",
        ),
        (
            '(Hayaert, 2018; Resnik e Curtis, 2011)',
            '(Hayaert, 2018; Resnik; Curtis, 2011)',
            "Autoria dupla em citação parentética segundo NBR 10520:2023.",
        ),
        (
            '(Resnik e Curtis, 2011)',
            '(Resnik; Curtis, 2011)',
            "Autoria dupla em citação parentética segundo NBR 10520:2023.",
        ),
    ]
    for before, after, rule in replacements:
        count = content.count(before)
        expected = 2 if before == '(Resnik e Curtis, 2011)' else 1
        if count != expected:
            raise ValueError(f"Expected {expected} occurrences, got {count}: {before[:65]}")
        line = content[: content.index(before)].count("\n") + 1
        content = content.replace(before, after)
        changes.append(
            {"file": str(DELIVERY), "line": line, "before": before, "after": after, "rule": rule}
        )
    for before, after in [
        ('## 5. A cultura jurídica repensada', '## 7. A cultura jurídica repensada'),
        ('### 5.1.', '### 7.1.'),
        ('### 5.2.', '### 7.2.'),
        ('### 5.3.', '### 7.3.'),
        ('### 5.4.', '### 7.4.'),
        ('## 6. Conclusão', '## 8. Conclusão'),
    ]:
        if content.count(before) != 1:
            raise ValueError(f"Expected heading exactly once: {before}")
        content = content.replace(before, after, 1)
        changes.append({"file": str(DELIVERY), "line": 0, "before": before, "after": after, "rule": "Renumbering after integral expansion."})
    expansion = (HERE / 'expansao-integral.md').read_text(encoding='utf-8').strip()
    anchor = '## 7. A cultura jurídica repensada'
    content = content.replace(anchor, expansion + '\n\n' + anchor, 1)
    changes.append({"file": str(DELIVERY), "line": 0, "before": "", "after": "Sections 5 and 6 from expansao-integral.md", "rule": "Integrate TESE-03 and TESE-04 from structured article."})
    ref_anchor = 'PANOFSKY, Erwin. *Studies in Iconology:'
    mondzain = "MONDZAIN, Marie-José. *Image, icône, économie: les sources byzantines de l'imaginaire contemporain*. Paris: Seuil, 2002.\n\n"
    if content.count(ref_anchor) != 1:
        raise ValueError('Panofsky reference anchor missing')
    content = content.replace(ref_anchor, mondzain + ref_anchor, 1)
    changes.append({"file": str(DELIVERY), "line": 0, "before": "", "after": mondzain.strip(), "rule": "Reference added for expanded discussion; source: structured article REF-14."})
    content = content.replace('\n---\n\n## Referências', '\n\n## Referências', 1)
    content = content.replace('## Referências\n', '## Referências\n\n\\singlespacing\n\\setlength{\\parindent}{0pt}\n\\setlength{\\parskip}{\\baselineskip}\n', 1)
    DELIVERY.write_text(content, encoding="utf-8")
    with (HERE / "changes.jsonl").open("w", encoding="utf-8") as stream:
        for item in changes:
            stream.write(json.dumps(item, ensure_ascii=False) + "\n")
    return changes


def prepare_reference_doc() -> Path:
    path = HERE / "reference-abnt.docx"
    document = Document()
    section = document.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin, section.left_margin = Cm(3), Cm(3)
    section.bottom_margin, section.right_margin = Cm(2), Cm(2)
    normal = document.styles["Normal"]
    normal.font.name, normal.font.size = "Times New Roman", Pt(12)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal.paragraph_format.first_line_indent = Cm(1.25)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(0)
    for name in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        style = document.styles[name]
        style.font.name, style.font.size = "Times New Roman", Pt(12)
        style.font.bold = True
        style.paragraph_format.first_line_indent = Cm(0)
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.5
    if "Bibliography" not in document.styles:
        document.styles.add_style("Bibliography", WD_STYLE_TYPE.PARAGRAPH)
    document.save(path)
    return path


def run_pandoc(reference_doc: Path) -> None:
    docx_path = HERE / f"{STEM}.docx"
    pdf_path = HERE / f"{STEM}.pdf"
    common = ["pandoc", str(DELIVERY), "--standalone", "--from=markdown+footnotes", "--metadata=lang:pt-BR"]
    subprocess.run(common + [f"--reference-doc={reference_doc}", "-o", str(docx_path)], check=True)
    subprocess.run(
        common
        + [
            "--pdf-engine=xelatex",
            "-V", "documentclass=article",
            "-V", "papersize=a4",
            "-V", "fontsize=12pt",
            "-V", "mainfont=Times New Roman",
            "-V", "geometry:top=3cm",
            "-V", "geometry:left=3cm",
            "-V", "geometry:bottom=2cm",
            "-V", "geometry:right=2cm",
            "-V", "linestretch=1.5",
            "-V", "indent=true",
            "--include-in-header", str(HERE / "header-abnt.tex"),
            "-o", str(pdf_path),
        ],
        check=True,
    )
    document = Document(docx_path)
    in_references = False
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text == "Referências":
            in_references = True
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            continue
        if in_references and text:
            paragraph.paragraph_format.first_line_indent = Cm(0)
            paragraph.paragraph_format.line_spacing = 1
            paragraph.paragraph_format.space_after = Pt(12)
        if text == "O contrato visual: alegoria feminina e contrato sexual na história da cultura jurídica":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.first_line_indent = Cm(0)
        if text == "Ana Vanzin":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            paragraph.paragraph_format.first_line_indent = Cm(0)
    document.save(docx_path)


if __name__ == "__main__":
    prepare_markdown()
    run_pandoc(prepare_reference_doc())
