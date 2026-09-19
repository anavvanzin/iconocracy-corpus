const fs = require("fs");
const path = require("path");
const sharp = require("sharp");
const {
  AlignmentType,
  BorderStyle,
  Document,
  ExternalHyperlink,
  Footer,
  Header,
  HeadingLevel,
  ImageRun,
  LevelFormat,
  Packer,
  PageBreak,
  PageNumber,
  Paragraph,
  ShadingType,
  Table,
  TableCell,
  TableRow,
  TextRun,
  VerticalAlign,
  WidthType,
} = require("docx");

const ROOT = path.resolve(__dirname, "../..");
const OUT = process.argv[2] || path.join(ROOT, "docs/ICONOCRACIA-visao-computacional-dossie-integrado-2026-2.docx");
const FIG_DIR = path.join(ROOT, "docs/figures");
const FIG = path.join(FIG_DIR, "iconocracy-cv-pipeline-2026-2.png");

const C = {
  ink: "1D2A33",
  muted: "586771",
  navy: "16324F",
  blue: "0072B2",
  cyan: "56B4E9",
  green: "009E73",
  orange: "E69F00",
  vermilion: "D55E00",
  purple: "7A4EAB",
  paper: "F8F5EE",
  paleBlue: "E8F3F8",
  paleGreen: "E8F5F0",
  paleOrange: "FFF2D7",
  paleRed: "FBEAE4",
  palePurple: "F0EAF7",
  line: "C8D1D6",
  white: "FFFFFF",
};

const PAGE_W = 11906;
const PAGE_H = 16838;
const MARGIN = 1020;
const CONTENT_W = PAGE_W - MARGIN * 2;

const border = { style: BorderStyle.SINGLE, size: 4, color: C.line };
const borders = { top: border, bottom: border, left: border, right: border };

const tr = (text, opts = {}) => new TextRun({ text, font: opts.font || "Arial", size: opts.size || 21, color: opts.color || C.ink, ...opts });
const code = (text) => tr(text, { font: "Menlo", size: 18, color: C.navy });
const parts = (items) => items.map((item) => typeof item === "string" ? tr(item) : tr(item.text, item));

function para(content, opts = {}) {
  const children = Array.isArray(content) ? content : [tr(content)];
  return new Paragraph({
    style: opts.style || "Body",
    alignment: opts.alignment,
    spacing: opts.spacing,
    indent: opts.indent,
    keepNext: opts.keepNext,
    keepLines: opts.keepLines,
    pageBreakBefore: opts.pageBreakBefore,
    children,
  });
}

function small(content, opts = {}) {
  const children = Array.isArray(content) ? content : [tr(content, { size: 18 })];
  return new Paragraph({ style: "Small", alignment: opts.alignment, spacing: opts.spacing, children });
}

function heading(text, level = 1) {
  const map = { 1: HeadingLevel.HEADING_1, 2: HeadingLevel.HEADING_2, 3: HeadingLevel.HEADING_3 };
  return new Paragraph({ heading: map[level], children: [tr(text)] });
}

function bullet(content, level = 0) {
  const children = Array.isArray(content) ? content : [tr(content)];
  return new Paragraph({ style: "Body", numbering: { reference: "bullets", level }, children });
}

function numbered(content, reference = "steps") {
  const children = Array.isArray(content) ? content : [tr(content)];
  return new Paragraph({ style: "Body", numbering: { reference, level: 0 }, children });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

function link(label, url) {
  return new ExternalHyperlink({ children: [new TextRun({ text: label, style: "Hyperlink" })], link: url });
}

function cell(content, width, opts = {}) {
  const children = Array.isArray(content)
    ? content.map((x) => typeof x === "string" ? small(x) : x)
    : [small(String(content), { alignment: opts.alignment })];
  return new TableCell({
    borders: opts.borders || borders,
    width: { size: width, type: WidthType.DXA },
    shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    children,
  });
}

function dataTable(headers, rows, widths, opts = {}) {
  const header = new TableRow({
    tableHeader: true,
    cantSplit: true,
    children: headers.map((h, i) => cell([
      new Paragraph({ alignment: opts.headerAlign || AlignmentType.LEFT, children: [tr(h, { bold: true, color: C.white, size: 18 })] }),
    ], widths[i], { fill: opts.headerFill || C.navy })),
  });
  const bodyRows = rows.map((row, ri) => new TableRow({
    cantSplit: true,
    children: row.map((value, ci) => cell(value, widths[ci], { fill: ri % 2 ? "F4F7F8" : C.white, alignment: ci === 1 && opts.centerSecond ? AlignmentType.CENTER : undefined })),
  }));
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: widths,
    margins: { top: 110, bottom: 110, left: 150, right: 150 },
    rows: [header, ...bodyRows],
  });
}

function callout(title, body, fill = C.paleBlue, accent = C.blue) {
  const b = { ...borders, left: { style: BorderStyle.SINGLE, size: 18, color: accent } };
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    margins: { top: 150, bottom: 150, left: 220, right: 220 },
    rows: [new TableRow({ children: [new TableCell({
      borders: b,
      width: { size: CONTENT_W, type: WidthType.DXA },
      shading: { fill, type: ShadingType.CLEAR },
      children: [
        new Paragraph({ spacing: { after: 70 }, children: [tr(title, { bold: true, color: accent, size: 22 })] }),
        para(body, { spacing: { after: 0 } }),
      ],
    })] })],
  });
}

function quote(text) {
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    margins: { top: 130, bottom: 130, left: 280, right: 280 },
    rows: [new TableRow({ children: [new TableCell({
      borders: { top: border, bottom: border, left: { style: BorderStyle.SINGLE, size: 16, color: C.orange }, right: border },
      width: { size: CONTENT_W, type: WidthType.DXA },
      shading: { fill: C.paleOrange, type: ShadingType.CLEAR },
      children: [new Paragraph({ style: "Quote", children: [tr(text, { italics: true, size: 22, color: C.navy })] })],
    })] })],
  });
}

async function makeFigure() {
  fs.mkdirSync(FIG_DIR, { recursive: true });
  const svg = `
  <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#16324F"/>
      </marker>
      <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%">
        <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#16324F" flood-opacity="0.15"/>
      </filter>
    </defs>
    <rect width="1600" height="900" fill="#F8F5EE"/>
    <text x="80" y="70" font-family="Arial" font-size="38" font-weight="700" fill="#16324F">Do corpus ao experimento de Visão Computacional</text>
    <text x="80" y="110" font-family="Arial" font-size="22" fill="#586771">Cada seta depende de um gate verificável; nenhuma etapa herda automaticamente a validade da anterior.</text>

    <g filter="url(#shadow)">
      <rect x="80" y="175" rx="18" width="300" height="155" fill="#E8F3F8" stroke="#0072B2" stroke-width="4"/>
      <text x="110" y="220" font-family="Arial" font-size="25" font-weight="700" fill="#0072B2">G0 · Metadata freeze</text>
      <text x="110" y="260" font-family="Arial" font-size="22" fill="#16324F">335 registros canônicos</text>
      <text x="110" y="293" font-family="Arial" font-size="19" fill="#586771">schema + hashes + release público</text>
    </g>
    <line x1="380" y1="252" x2="480" y2="252" stroke="#16324F" stroke-width="5" marker-end="url(#arrow)"/>

    <g filter="url(#shadow)">
      <rect x="500" y="175" rx="18" width="300" height="155" fill="#FFF2D7" stroke="#E69F00" stroke-width="4"/>
      <text x="530" y="220" font-family="Arial" font-size="25" font-weight="700" fill="#A46F00">G1 · Coorte visual</text>
      <text x="530" y="260" font-family="Arial" font-size="22" fill="#16324F">bytes + MIME + dimensões</text>
      <text x="530" y="293" font-family="Arial" font-size="19" fill="#586771">pool 92 · núcleo ≈70 · N a congelar</text>
    </g>
    <line x1="800" y1="252" x2="900" y2="252" stroke="#16324F" stroke-width="5" marker-end="url(#arrow)"/>

    <g filter="url(#shadow)">
      <rect x="920" y="175" rx="18" width="300" height="155" fill="#E8F5F0" stroke="#009E73" stroke-width="4"/>
      <text x="950" y="220" font-family="Arial" font-size="25" font-weight="700" fill="#007A59">G2 · Rótulos elegíveis</text>
      <text x="950" y="260" font-family="Arial" font-size="22" fill="#16324F">proveniência + adjudicação</text>
      <text x="950" y="293" font-family="Arial" font-size="19" fill="#586771">sem falsos zeros no supervisionado</text>
    </g>
    <line x1="1220" y1="252" x2="1320" y2="252" stroke="#16324F" stroke-width="5" marker-end="url(#arrow)"/>

    <g filter="url(#shadow)">
      <rect x="1340" y="175" rx="18" width="180" height="155" fill="#F0EAF7" stroke="#7A4EAB" stroke-width="4"/>
      <text x="1368" y="220" font-family="Arial" font-size="25" font-weight="700" fill="#68408F">G3 · Split</text>
      <text x="1368" y="260" font-family="Arial" font-size="20" fill="#16324F">séries juntas</text>
      <text x="1368" y="293" font-family="Arial" font-size="18" fill="#586771">zero leakage</text>
    </g>

    <line x1="800" y1="330" x2="800" y2="410" stroke="#16324F" stroke-width="5" marker-end="url(#arrow)"/>
    <text x="650" y="390" font-family="Arial" font-size="19" fill="#586771">mesmas consultas e galeria</text>

    <g filter="url(#shadow)">
      <rect x="120" y="445" rx="18" width="380" height="145" fill="#FFFFFF" stroke="#E69F00" stroke-width="4"/>
      <text x="155" y="490" font-family="Arial" font-size="25" font-weight="700" fill="#A46F00">Visão clássica</text>
      <text x="155" y="530" font-family="Arial" font-size="22" fill="#16324F">HSV · HOG · ORB/SIFT · k-NN</text>
      <text x="155" y="563" font-family="Arial" font-size="18" fill="#586771">baseline interpretável</text>
    </g>
    <g filter="url(#shadow)">
      <rect x="610" y="445" rx="18" width="380" height="145" fill="#FFFFFF" stroke="#0072B2" stroke-width="4"/>
      <text x="645" y="490" font-family="Arial" font-size="25" font-weight="700" fill="#0072B2">CNN pré-treinada</text>
      <text x="645" y="530" font-family="Arial" font-size="22" fill="#16324F">ResNet50 ou EfficientNet-B0</text>
      <text x="645" y="563" font-family="Arial" font-size="18" fill="#586771">embeddings congelados primeiro</text>
    </g>
    <g filter="url(#shadow)">
      <rect x="1100" y="445" rx="18" width="380" height="145" fill="#FFFFFF" stroke="#CC79A7" stroke-width="4"/>
      <text x="1135" y="490" font-family="Arial" font-size="25" font-weight="700" fill="#9A4F7B">Transformador visual</text>
      <text x="1135" y="530" font-family="Arial" font-size="22" fill="#16324F">DINOv2 ou CLIP</text>
      <text x="1135" y="563" font-family="Arial" font-size="18" fill="#586771">extensão, um modelo basta</text>
    </g>

    <line x1="310" y1="590" x2="680" y2="690" stroke="#16324F" stroke-width="4" marker-end="url(#arrow)"/>
    <line x1="800" y1="590" x2="800" y2="680" stroke="#16324F" stroke-width="4" marker-end="url(#arrow)"/>
    <line x1="1290" y1="590" x2="920" y2="690" stroke="#16324F" stroke-width="4" marker-end="url(#arrow)"/>

    <g filter="url(#shadow)">
      <rect x="520" y="700" rx="18" width="560" height="120" fill="#16324F"/>
      <text x="565" y="745" font-family="Arial" font-size="26" font-weight="700" fill="#FFFFFF">CBIR · top-k · avaliação cega</text>
      <text x="565" y="785" font-family="Arial" font-size="21" fill="#D9EDF7">nDCG@10 + utilidade iconográfica + análise dos erros</text>
    </g>

    <text x="80" y="872" font-family="Arial" font-size="19" font-weight="700" fill="#D55E00">Guardrail:</text>
    <text x="185" y="872" font-family="Arial" font-size="19" fill="#586771">proximidade visual é evidência comparativa; não prova filiação histórica nem “mede” o endurecimento.</text>
  </svg>`;
  await sharp(Buffer.from(svg)).png({ quality: 100 }).toFile(FIG);
}

async function build() {
  await makeFigure();

  const children = [];
  const push = (...items) => children.push(...items);

  push(
    new Paragraph({ spacing: { before: 1500, after: 240 }, alignment: AlignmentType.CENTER, children: [tr("ICONOCRACIA × VISÃO COMPUTACIONAL", { font: "Georgia", size: 54, bold: true, color: C.navy })] }),
    new Paragraph({ spacing: { after: 300 }, alignment: AlignmentType.CENTER, children: [tr("Dataset, redes neurais, auditoria de integridade e plano experimental", { font: "Georgia", size: 31, color: C.blue })] }),
    new Table({
      width: { size: 7200, type: WidthType.DXA },
      columnWidths: [7200],
      rows: [new TableRow({ children: [cell([
        new Paragraph({ alignment: AlignmentType.CENTER, children: [tr("Dossiê integrado · INE410159 / TRV410001 · 2026.2", { bold: true, color: C.white, size: 22 })] }),
      ], 7200, { fill: C.navy, borders: { top: border, bottom: border, left: border, right: border } })] })],
    }),
    new Paragraph({ spacing: { before: 500, after: 80 }, alignment: AlignmentType.CENTER, children: [tr("Ana Vitória Vanzin Mendes", { bold: true, size: 24 })] }),
    new Paragraph({ spacing: { after: 80 }, alignment: AlignmentType.CENTER, children: [tr("PPGD/UFSC · ICONOCRACIA — Alegoria Feminina na História da Cultura Jurídica", { color: C.muted, size: 20 })] }),
    new Paragraph({ spacing: { after: 500 }, alignment: AlignmentType.CENTER, children: [tr("Versão consolidada em 14 de agosto de 2026", { color: C.muted, size: 19 })] }),
    callout("STATUS DESTA VERSÃO", "O freeze público está íntegro como pacote de metadados. A coorte visual ainda precisa ser materializada, auditada e congelada antes de qualquer treino ou avaliação.", C.paleOrange, C.orange),
    new Paragraph({ spacing: { before: 700 }, alignment: AlignmentType.CENTER, children: [link("Dataset público no Hugging Face", "https://huggingface.co/datasets/warholana/iconocracy-corpus/tree/ICONOCRACIA-CV-2026-08-12")] }),
    pageBreak(),
    new Paragraph({ heading: HeadingLevel.TITLE, children: [tr("Sumário")] }),
    dataTable(
      ["Seção", "Conteúdo", "Página"],
      [
        ["—", "Resumo executivo", "3"],
        ["1", "Problema de pesquisa e contribuição", "3"],
        ["2", "Encaixe na disciplina de Visão Computacional", "4"],
        ["3", "O que está sendo construído — e o que não está", "4"],
        ["4", "Freeze, publicação e identidade técnica", "5"],
        ["5", "Auditoria de integridade: quatro perguntas", "5"],
        ["6", "Imagens: disponibilidade não é materialização", "6"],
        ["7", "Indicadores: completude formal versus validade", "6"],
        ["8", "Correções em relação ao pitch inicial", "7"],
        ["9", "Pipeline experimental", "7"],
        ["10", "Avaliação e prevenção de vazamento", "8"],
        ["11", "Cronograma e entregas da disciplina", "9"],
        ["12", "Responsabilidades da equipe", "10"],
        ["13", "Melhoria do workflow de agentes", "11"],
        ["14", "Guardrails epistemológicos", "13"],
        ["15", "Decisões a validar com os professores", "13"],
        ["16", "Primeiro sprint", "13"],
        ["—", "Conclusão", "13"],
        ["—", "Fontes e referências", "14"],
        ["A–B", "Apêndices", "14–15"],
      ],
      [900, 8000, 966],
    ),
    pageBreak(),
  );

  push(heading("Resumo executivo", 1));
  push(callout("RESPOSTA CURTA", "Não se está criando uma grande rede neural do zero. A contribuição original é o corpus e seu conhecimento de domínio; o trabalho da disciplina construirá uma coorte visual verificável e comparará métodos clássicos, uma CNN pré-treinada e, como extensão, um transformador visual.", C.paleGreen, C.green));
  push(para("O projeto propõe um sistema de recuperação de imagens por conteúdo (CBIR) para selecionar comparanda no corpus ICONOCRACIA. Dada uma alegoria como consulta, o sistema devolverá as imagens visualmente mais próximas, com identificador, metadados, método e distância. O produto final será um atlas computacional de vizinhanças visuais, acompanhado de avaliação técnica e interpretação histórico-iconográfica."));
  push(para("A disciplina exige uma solução prática para um problema real de Visão Computacional. O projeto se encaixa porque combina aquisição e controle de dados, processamento clássico, aprendizado profundo, avaliação, análise de erros e explicitação das limitações. O material do Moodle não exige arquitetura neural original nem treinamento integral a partir de pesos aleatórios."));
  push(dataTable(
    ["Dimensão", "Estado auditado", "Conclusão permitida"],
    [
      ["Pacote publicado", "7 arquivos do release; checksums válidos", "Freeze de metadados íntegro"],
      ["Registros", "335/335 válidos e IDs únicos", "Universo catalográfico fixado"],
      ["Imagens no release", "0 binários", "Não é dataset visual autocontido"],
      ["Ledger de codificação", "286/335 linhas", "Cobertura parcial"],
      ["Indicadores", "10 campos em 335/335; 106 vetores zerados", "Presença formal não equivale a medição confiável"],
      ["Coorte de ML", "sem manifesto/split congelados", "Ainda não pronta para treino"],
    ],
    [2350, 3000, 4516],
  ));

  push(heading("1. Problema de pesquisa e contribuição", 1));
  push(heading("1.1 A tese e sua tradução computacional", 2));
  push(para("A tese ICONOCRACIA investiga como alegorias femininas participam da produção visual da autoridade jurídica. Seu recorte central são os séculos XIX–XX; imagens anteriores podem funcionar como antecedentes comparativos, mas não autorizam ampliar silenciosamente o recorte para “cinco séculos”. O interesse não é somente identificar venda, balança ou espada, mas compreender como corpo, postura, suporte, repetição e inscrição institucional organizam a visualidade do Direito."));
  push(para("Visão Computacional não substitui essa interpretação. Ela permite construir descrições formais, comparar imagens, recuperar vizinhos, testar sensibilidade a atributos e localizar atalhos visuais. O semantic gap — a distância entre padrão computacional e sentido histórico — torna-se parte do método, não um defeito a ser ocultado."));
  push(dataTable(
    ["Pergunta histórico-jurídica", "Operação computacional", "Limite"],
    [
      ["Quais imagens compartilham formas e composições?", "Embeddings, distância e CBIR", "Proximidade não prova influência histórica"],
      ["Quais atributos são visualmente detectáveis?", "Classificação ou diagnóstico de atributos", "Rótulos precisam de proveniência e adjudicação"],
      ["Há famílias formais não previstas pelo codebook?", "Clustering e projeção de embeddings", "Clusters podem refletir suporte, papel ou acervo"],
      ["Como separar figura, fundo e moldura?", "Segmentação e ablação de pré-processamento", "Máscaras/prompts e revisão humana continuam necessários"],
    ],
    [3300, 2900, 3666],
  ));
  push(heading("1.2 A pergunta experimental", 2));
  push(quote("Qual representação computacional produz vizinhanças visualmente coerentes e historicamente úteis no corpus ICONOCRACIA: descritores clássicos, embeddings de CNNs ou embeddings de transformadores visuais?"));
  push(para("A hipótese não é que a CNN necessariamente “vença”. O resultado relevante é identificar quais características cada representação privilegia, em que situações surgem erros e quando a vizinhança proposta é útil para comparação especializada."));

  push(heading("2. Encaixe na disciplina de Visão Computacional", 1));
  push(para("O Moodle define como objetivo geral oferecer uma visão das técnicas de análise e reconhecimento de imagens, dos métodos básicos à Inteligência Artificial. Entre os objetivos específicos está realizar um trabalho prático que resolva um problema de mundo real. O material enfatiza que não existe um modelo genérico capaz de perceber qualquer imagem: soluções práticas encadeiam técnicas específicas e devem reconhecer seus limites."));
  push(dataTable(
    ["Eixo do curso", "Conteúdos", "Aplicação no projeto"],
    [
      ["Módulo 1", "Histogramas, distâncias, k-NN, convolução, morfologia, bordas, segmentação, HOG, SIFT, SURF, ORB, Hough e Gabor", "Baselines interpretáveis, pré-processamento e busca inicial"],
      ["Módulo 2", "ANNs, CNNs, ResNet, EfficientNet, transfer learning, YOLO, Detectron2, U-Net, ViTs, SAM, DINOv2, DETR e CLIP", "Embeddings pré-treinados; classificação auxiliar apenas se viável"],
    ],
    [1700, 4200, 3966],
  ));
  push(callout("IMPLICAÇÃO PEDAGÓGICA", "Usar uma CNN pré-treinada não é fugir da disciplina. É aplicar aprendizado por transferência a um corpus pequeno, comparando-o com métodos clássicos e documentando por que uma rede profunda treinada do zero tende a sobreajustar.", C.paleBlue, C.blue));

  push(heading("3. O que está sendo construído — e o que não está", 1));
  push(heading("3.1 Três camadas distintas", 2));
  push(numbered(parts([{ text: "Corpus de pesquisa. ", bold: true }, "É a contribuição original de Ana: seleção, catalogação, proveniência, codebook e interpretação jurídico-histórica."]), "layers"));
  push(numbered(parts([{ text: "Coorte visual experimental. ", bold: true }, "Será derivada do freeze após recuperar bytes, verificar imagens, resolver IDs, direitos, duplicatas e rótulos."]), "layers"));
  push(numbered(parts([{ text: "Modelos e avaliação. ", bold: true }, "A disciplina comparará representações sobre a mesma coorte, com consultas, galeria e protocolo de avaliação fixos."]), "layers"));
  push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 260, after: 100 }, children: [new ImageRun({
    type: "png",
    data: fs.readFileSync(FIG),
    transformation: { width: 650, height: 366 },
    altText: { title: "Pipeline ICONOCRACIA-CV", description: "Fluxo do freeze de metadados à coorte visual, rótulos, split, modelos e avaliação", name: "Pipeline ICONOCRACIA-CV" },
  })] }));
  push(new Paragraph({ style: "Caption", alignment: AlignmentType.CENTER, children: [tr("Figura 1 — Pipeline proposto e gates de evidência. Fonte: elaboração própria, 2026.", { size: 17, italics: true, color: C.muted })] }));
  push(heading("3.2 Resposta à pergunta “estou fazendo uma rede neural do zero?”", 2));
  push(para("Não, no sentido técnico de projetar e treinar uma arquitetura profunda inédita. O núcleo do trabalho é construir um problema computacional reproduzível sobre um corpus próprio. ResNet50 ou EfficientNet-B0 serão usadas inicialmente como extratoras congeladas. Uma CNN pequena, com duas ou três etapas convolucionais e pesos aleatórios, poderá aparecer apenas como controle pedagógico para observar variância e sobreajuste."));
  push(heading("3.3 Escopo que não será prometido", 2));
  push(bullet("YOLO como tarefa central, porque o corpus não possui caixas delimitadoras consolidadas."));
  push(bullet("Segmentação supervisionada completa, porque não existem máscaras por pixel para a coorte."));
  push(bullet("Aplicação web ou API de produção antes do notebook e da avaliação funcionarem."));
  push(bullet("Uma métrica única de “endurecimento” como alvo probatório."));
  push(bullet("Interpretação iconológica automática ou equivalência entre CNN e o terceiro nível de Panofsky."));

  push(heading("4. Freeze, publicação e identidade técnica", 1));
  push(para("O universo do semestre foi fixado no release ICONOCRACIA-CV-2026-08-12. O corpus vivo pode continuar crescendo; resultados do curso devem sempre apontar para a tag imutável, não apenas para main. Em 14 de agosto de 2026, a tag continuava resolvendo para o commit remoto 1ed83d28693ae52a59da8cefef909eb9739c4ece, com acesso público e sem gate."));
  push(dataTable(
    ["Elemento", "Valor"],
    [
      ["Release", "ICONOCRACIA-CV-2026-08-12"],
      ["Commit-fonte", "0f80b6b11e95a32312a2697344f27255dbf7ef78"],
      ["Commit remoto da tag", "1ed83d28693ae52a59da8cefef909eb9739c4ece"],
      ["Registros canônicos", "335"],
      ["Ledger separado", "286 linhas"],
      ["Licença dos metadados", "CC BY 4.0; imagens permanecem sob direitos das instituições-fonte"],
      ["URL", [new Paragraph({ children: [link("huggingface.co/datasets/warholana/iconocracy-corpus", "https://huggingface.co/datasets/warholana/iconocracy-corpus")] })]],
    ],
    [3000, 6866],
  ));
  push(heading("4.1 Hashes do freeze", 2));
  push(dataTable(
    ["Arquivo", "N", "SHA-256"],
    [
      ["records.jsonl", "335 linhas", "93bce22629da9655cb1f61ba192d86ae837cf9a6544ce4e2f7c77bd72c87a558"],
      ["corpus-data.json", "335 itens", "e822c5c5d20d332228384638fafcc41e80e6d3cb1030858a4e855e8c772aa7a4"],
      ["purification.jsonl", "286 linhas", "2ceac28e974b31a59c33415f5225744aff2ea779d09e2be4882e16f8fe2b58d2"],
    ],
    [2350, 1450, 6066],
  ));
  push(para("Os checksums e os schemas aprovam identidade e estrutura dos arquivos. Eles não comprovam presença de imagens nem confiabilidade substantiva dos rótulos."));
  push(heading("4.2 Infraestrutura operacional", 2));
  push(para("O release foi publicado no Hugging Face e validado por comparação remota byte a byte. O ambiente local também possui o servidor MCP hf-mcp-server habilitado com OAuth, útil para operações futuras no Hub. Essa integração é uma ferramenta administrativa; não altera o nível de evidência do dataset."));

  push(heading("5. Auditoria de integridade: quatro perguntas diferentes", 1));
  push(dataTable(
    ["Tipo de integridade", "Pergunta", "Resultado"],
    [
      ["De pacote", "Os bytes publicados correspondem ao freeze?", "Sim: checksums e comparação remota aprovados"],
      ["Estrutural", "Os arquivos obedecem ao schema e às contagens?", "Sim: 335/335 master records e 286/286 linhas do ledger válidos"],
      ["Visual", "As imagens estão materializadas e verificadas?", "Não: o release contém zero binários de imagem"],
      ["Semântica", "Os dez indicadores são rótulos confiáveis em todos os itens?", "Não: falsos zeros, proveniências provisórias e baixa adjudicação"],
      ["Experimental", "Há manifesto, grupos e splits congelados?", "Não: vision-v1 ainda será construído"],
    ],
    [2100, 3800, 3966],
  ));
  push(callout("FORMULAÇÃO CORRETA", "O release é íntegro como snapshot de metadados e anotações em seu estado atual. Ele ainda não é um dataset visual autocontido nem uma coorte supervisionada pronta.", C.paleRed, C.vermilion));

  push(heading("6. Imagens: disponibilidade não é materialização", 1));
  push(para("O pacote público contém JSON, JSONL, documentação e checksums, mas nenhum arquivo JPG, PNG, TIFF ou equivalente. Os 335 registros possuem URLs catalográficas; a maior parte aponta para páginas de acervo ou serviços, não para um byte visual garantido. No export auditado, somente 12 URLs parecem arquivos de imagem pela extensão."));
  push(dataTable(
    ["Camada visual", "N", "Interpretação"],
    [
      ["Binários no release", "0", "Não há imagens treináveis no Hugging Face"],
      ["URLs catalográficas", "335", "Referências à fonte; não garantem download"],
      ["thumbnail_registry", "165", "122 URLs de miniatura; registro não incluído no freeze"],
      ["drive-manifest", "172", "Todas as drive_url ainda usam PLACEHOLDER_FOLDER_ID"],
      ["gallery local", "16", "Amostra ilustrativa; não é coorte completa nem manifesto experimental"],
      ["Pool preliminar", "92", "Candidatos com filtros de escopo, URL e proveniência"],
      ["Núcleo estável estimado", "≈70", "Ainda requer download e inspeção dos bytes"],
      ["Diretamente verificados", "31", "Base mais forte, ainda não congelada como vision-v1"],
    ],
    [3300, 1100, 5466],
  ));
  push(heading("6.1 Contrato mínimo de uma imagem elegível", 2));
  push(bullet("O binário abre e o MIME real é de imagem."));
  push(bullet("O conteúdo corresponde ao objeto catalogado, e não a uma página HTML, PDF, logo ou erro."));
  push(bullet("O menor lado possui pelo menos 224 pixels, salvo exceção documentada."));
  push(bullet("SHA-256, hash perceptual, dimensões, formato e modo de cor foram calculados."));
  push(bullet("Fonte, custódia, licença e condições de redistribuição foram registradas."));
  push(bullet("Duplicatas, recortes, frente/verso e itens de uma mesma série receberam um grupo indivisível."));

  push(heading("7. Indicadores: completude formal versus validade", 1));
  push(para("Os dez indicadores ordinais aparecem em 335/335 master records, sempre em escala 0–3. Essa completude é estrutural. Ela não significa que 3.350 valores tenham sido observados visualmente com a mesma qualidade."));
  push(dataTable(
    ["Evidência", "N", "Leitura"],
    [
      ["Master records com os 10 campos", "335", "Estruturalmente completos"],
      ["Linhas em purification.jsonl", "286", "49 registros sem linha no ledger separado"],
      ["Vetores totalmente zerados nos master records", "106", "86 vault-import; 19 migration; 1 ana a inspecionar"],
      ["Vetores com ao menos um valor > 0", "229", "Não equivale automaticamente a alta confiança"],
      ["Proveniências frágeis/provisórias", "159", "86 vault-import; 43 hermes-auto; 19 migration; 11 batch-tentative"],
      ["Registros com confidence_score/adjudication_status", "26", "Todos single; sem adjudicação efetiva"],
    ],
    [4200, 1100, 4566],
  ));
  push(callout("REGRA SUPERVISIONADA", "Zero de preenchimento não é classe negativa. Um rótulo só poderá entrar em treino ou avaliação supervisionada quando sua proveniência, relação com a imagem e status de adjudicação forem explícitos.", C.paleOrange, C.orange));
  push(heading("7.1 Os dez indicadores do codebook", 2));
  push(dataTable(
    ["Indicador", "Descrição operacional abreviada"],
    [
      ["Desincorporação", "Perda de corporalidade concreta em direção à forma abstrata ou ausente"],
      ["Rigidez postural", "Frontalidade, simetria, imobilidade e hieratismo"],
      ["Dessexualização", "Supressão de marcadores de sexualidade e erotismo"],
      ["Uniformização facial", "Perda de individualidade facial em direção à máscara tipificada"],
      ["Heraldização", "Autonomização emblemática de atributos como espada, balança, fasces ou barrete"],
      ["Enquadramento arquitetônico", "Absorção da figura por nicho, frontão, medalhão, selo ou edifício"],
      ["Apagamento narrativo", "Supressão de cena, ação e personagens em favor da figura isolada"],
      ["Monocromatização", "Redução material da paleta em direção ao monocromático"],
      ["Serialidade", "Reprodução em série, de tiragem limitada à circulação massiva"],
      ["Inscrição estatal", "Vinculação ao aparato jurídico-estatal ou conversão no próprio dispositivo"],
    ],
    [3400, 6466],
  ));
  push(para(parts(["A escala 0–3 deve permanecer ordinal e separada por indicador. O campo composto legado ", { text: "mean_endurecimento", font: "Menlo", size: 18 }, " não será alvo supervisionado nem prova de trajetória histórica."])));

  push(heading("8. Correções em relação ao pitch inicial", 1));
  push(dataTable(
    ["Formulação a evitar", "Formulação defensável"],
    [
      ["“Temos 335 imagens curadas.”", "“Temos 335 registros canônicos e construiremos uma coorte visual auditada.”"],
      ["“O freeze contém todas as imagens.”", "“O freeze preserva metadados e anotações; os binários formam uma camada separada.”"],
      ["“Ground truth de graça.”", "“Referência especializada com proveniência, incerteza e adjudicação necessárias.”"],
      ["“Os indicadores estão completos e corretos.”", "“Os campos estão presentes, mas cobertura substantiva e confiança variam.”"],
      ["“A rede mede o endurecimento.”", "“O modelo mede proximidades visuais que podem subsidiar essa investigação.”"],
      ["“A rede entendeu Panofsky.”", "“A analogia delimita níveis de descrição; a interpretação histórica continua humana.”"],
      ["“Distância prova influência.”", "“Distância representa proximidade no espaço de características.”"],
      ["“Estou criando uma rede neural do zero.”", "“Estou construindo o dataset operacional e comparando representações.”"],
    ],
    [4150, 5716],
  ));

  push(heading("9. Pipeline experimental", 1));
  push(heading("9.1 Etapa 0 — dados antes de modelos", 2));
  push(numbered("Resolver UUIDs e identificadores legados em um crosswalk congelado.", "pipeline"));
  push(numbered("Recuperar ou localizar os binários autorizados.", "pipeline"));
  push(numbered("Validar MIME, dimensões, abertura e correspondência visual.", "pipeline"));
  push(numbered("Calcular SHA-256, hash perceptual e grupos de duplicatas/séries.", "pipeline"));
  push(numbered("Registrar licença e elegibilidade; gerar contact sheet para revisão.", "pipeline"));
  push(numbered("Congelar o manifesto vision-v1 e só então executar modelos.", "pipeline"));
  push(heading("9.2 Baselines e representações", 2));
  push(dataTable(
    ["Etapa", "Método", "Função"],
    [
      ["Baseline mínimo", "Pixels reduzidos + histograma HSV + distância Euclidiana/cosseno", "Estabelecer o piso de desempenho"],
      ["Visão clássica", "HOG combinado a cor; ORB ou SIFT como ablação; k-NN", "Contorno, postura, estrutura e pontos locais"],
      ["CNN", "ResNet50 ou EfficientNet-B0 pré-treinada; pesos congelados na primeira rodada", "Embeddings aprendidos e comparação justa com HOG"],
      ["Transformador", "DINOv2 ou CLIP, um extrator congelado", "Extensão global/semântica e análise de vieses"],
      ["Controle opcional", "CNN pequena com pesos aleatórios", "Demonstrar sobreajuste; não competir como modelo principal"],
    ],
    [1900, 4200, 3766],
  ));
  push(heading("9.3 Tarefa supervisionada auxiliar", 2));
  push(para("Uma cabeça linear ou o último bloco da CNN poderá ser ajustado para um único indicador binarizado, somente depois do gate de rótulos e do split agrupado. Candidatos preliminares são enquadramento_arquitetonico ≥ 2 ou inscricao_estatal ≥ 2. O alvo final será escolhido pela distribuição da coorte vision-v1, não pelas contagens brutas dos 335 registros."));

  push(heading("10. Avaliação e prevenção de vazamento", 1));
  push(heading("10.1 Recuperação por similaridade", 2));
  push(para("Serão selecionadas aproximadamente 15 consultas, estratificadas por suporte, país, período e regime, sem variantes próximas entre si. Cada método retornará top-10 sobre a mesma galeria. Os resultados serão deduplicados e avaliados sem revelar o método."));
  push(dataTable(
    ["Dimensão humana", "0", "1", "2"],
    [
      ["Similaridade formal", "Sem relação relevante", "Compartilha um traço", "Forte proximidade morfológica/composicional"],
      ["Utilidade iconográfica", "Não serve como comparandum", "Comparação possível", "Comparandum historicamente produtivo"],
    ],
    [2400, 2200, 2500, 2766],
  ));
  push(bullet(parts([{ text: "Métrica primária: ", bold: true }, "nDCG@10 para similaridade formal."])));
  push(bullet("Secundárias: nDCG@10 para utilidade iconográfica, Precision@5, tempo, memória e estabilidade."));
  push(bullet("Diagnósticos: concentração por suporte, país, período, acervo, texto, fundo, borda e moldura."));
  push(bullet("Se houver classificação: macro-F1, balanced accuracy, matriz de confusão e variação entre folds."));
  push(heading("10.2 Unidade do split", 2));
  push(para("Divisão aleatória por arquivo é inválida. Frente e verso de moeda, recortes, resoluções diferentes e objetos da mesma série podem atravessar treino e teste e inflar o desempenho. A unidade indivisível será split_group, construída por hash exato, hash perceptual, metadados e inspeção."));
  push(callout("REGRA DE SEGURANÇA", "Com N próximo de 70, usar três folds agrupados. Cinco folds só entram se cada classe continuar representada em todos os grupos. É preferível reduzir a tarefa a relaxar o controle de vazamento.", C.palePurple, C.purple));

  push(heading("11. Cronograma e entregas da disciplina", 1));
  push(dataTable(
    ["Data", "Conteúdo do curso", "Marco interno"],
    [
      ["12/08", "Paradigmas: clássico × deep learning", "Pitch, problema e equipe"],
      ["19/08", "Thresholding e histogramas", "Auditoria inicial e baseline de cor"],
      ["26/08", "Distâncias, NN e k-NN", "Primeira busca por similaridade"],
      ["02/09", "Convolução e morfologia", "Pré-processamento versionado"],
      ["09/09", "Bordas e Canny", "Ablação de contornos"],
      ["16/09", "Segmentação clássica", "Teste de contaminação por fundo"],
      ["23/09", "HOG, SIFT, SURF e ORB", "Descritor clássico comparável"],
      ["30/09", "Hough, Gabor e pipeline clássico", "Baseline clássico congelado"],
      ["07/10", "ANNs e backpropagation", "Split agrupado e harness"],
      ["14/10", "CNNs, ResNet, EfficientNet e transfer learning", "Embeddings CNN e checkpoint"],
      ["21/10", "YOLO e Detectron2", "Extensão opcional de localização"],
      ["04/11", "U-Net e segmentação", "Ablação de fundo, se necessária"],
      ["11/11", "Casos de deep learning", "Integração e análise de erros"],
      ["18/11", "ViTs, SAM, DINOv2, DETR e CLIP", "Um transformador visual"],
      ["25/11", "Andamento das equipes faltantes", "Resultados e artefatos em revisão"],
      ["02/12", "Poster Session e sessão síncrona", "Entrega final"],
    ],
    [1300, 4100, 4466],
  ));
  push(heading("11.1 Cinco artefatos informados pelo Moodle", 2));
  push(numbered("Relatório em PDF descrevendo a solução.", "deliverables"));
  push(numbered("Código em ZIP com link para checkpoints da rede neural.", "deliverables"));
  push(numbered("Slides em PPTX ou ODP, com link para Google Slides.", "deliverables"));
  push(numbered("Vídeo em MP4/H.265, com link para YouTube.", "deliverables"));
  push(numbered("Poster em PDF.", "deliverables"));
  push(para("O Moodle não esclarece se o checkpoint precisa conter uma rede ajustada integralmente ou se uma cabeça própria sobre um extrator pré-treinado é suficiente. Esse ponto deve ser confirmado com os professores."));
  push(heading("11.2 Regras de redução de escopo", 2));
  push(dataTable(
    ["Imagens válidas após G1", "Escopo"],
    [
      ["≥ 80", "Pipeline completo, CNN congelada e tarefa supervisionada auxiliar se G2/G3 passarem"],
      ["50–79", "Retrieval com descritores e extratores congelados; sem fine-tuning central"],
      ["< 50", "Estudo piloto curado; sem alegação de desempenho geral e sem CNN profunda do zero"],
    ],
    [2500, 7366],
  ));

  push(heading("12. Responsabilidades da equipe", 1));
  push(dataTable(
    ["Papel", "Responsabilidades"],
    [
      ["Especialista de domínio", "Elegibilidade, recorte, adjudicação, consultas, avaliação de utilidade e limites epistemológicos"],
      ["Implementação de ML/CV", "Aquisição técnica, descritores, indexação, modelos, checkpoints, métricas e reprodutibilidade"],
      ["Responsabilidade compartilhada", "Hipóteses, revisão de erros, extensões, relatório, apresentação, vídeo e poster"],
    ],
    [3000, 6866],
  ));

  push(heading("13. Melhoria do workflow de agentes", 1));
  push(para("A conversa revelou um caso sentinela de falso positivo de prontidão: a verificação de checksums, schemas e publicação estava correta, mas foi promovida indevidamente à afirmação de que o dataset estava integralmente pronto. A correção não exige apagar o release; exige impedir que um gate de metadados autorize alegações de mídia, rótulos ou ML."));
  push(heading("13.1 Baseline observável", 2));
  push(dataTable(
    ["Dimensão", "Evidência", "Estado"],
    [
      ["Pacote", "7 arquivos remotos idênticos; checksums válidos", "Aprovado"],
      ["Estrutura", "335/335 master records", "Aprovado"],
      ["Ledger", "286/335", "Parcial"],
      ["Mídia", "0 binários publicados", "Reprovado"],
      ["Rótulos", "106 zeros; 159 proveniências em auditoria", "Não demonstrado"],
      ["Experimento", "Sem manifesto, grupos e splits congelados", "Inexistente"],
    ],
    [2200, 5000, 2666],
  ));
  push(para("Há uma ocorrência observada neste episódio, suficiente para criar teste de regressão, mas insuficiente para estimar retrospectivamente taxa de erro, latência média, satisfação ou custo. Essas métricas deverão ser coletadas prospectivamente."));
  push(heading("13.2 Gates propostos", 2));
  push(dataTable(
    ["Gate", "Agente responsável", "Critério", "Alegação autorizada"],
    [
      ["G0", "Auditor de freeze", "Schema, contagens, hashes, sincronização e identidade remota", "Freeze de metadados íntegro"],
      ["G1", "Auditor de mídia", "Binário, MIME, dimensões, hash, correspondência e licença", "Coorte visual materializada"],
      ["G2", "Auditor de anotações", "Estado medido/ausente/N.A., proveniência e adjudicação", "Coorte rotulada elegível"],
      ["G3", "Curador de ML", "split_group, distribuição, seeds e zero leakage", "Dataset pronto para treino/evaluação"],
    ],
    [900, 2200, 4000, 2766],
  ));
  push(heading("13.3 Métricas e testes de regressão", 2));
  push(bullet("Meta: zero alegações de prontidão acima do gate efetivamente aprovado."));
  push(bullet("100% dos itens elegíveis ligados a binário validado; zero falsos zeros como negativos."));
  push(bullet("Zero grupos duplicados atravessando splits; reconstrução por hashes idênticos."));
  push(numbered("Pacote apenas com JSON aprova G0, mas deve bloquear “dataset visual”.", "regression"));
  push(numbered("URL sem binário e HTML salvo como JPG devem reprovar G1.", "regression"));
  push(numbered("Vetor vault-import zerado deve reprovar uso supervisionado em G2.", "regression"));
  push(numbered("Duplicata entre treino e teste deve reprovar G3.", "regression"));
  push(numbered("Somente pacote completo e auditado permite a alegação do nível alcançado.", "regression"));
  push(heading("13.4 Validação e rollout", 2));
  push(para("A versão atual e a proposta deverão ser comparadas em 100 cenários representativos por variante, com avaliação cega. Metas: conclusão correta +15%, correções da usuária −25%, nenhuma regressão de segurança, latência dentro de 10% e custo dentro de 5%. O rollout começa em modo sombra, segue por alpha, beta e canário 20% → 50% → 100%. Qualquer falso positivo de prontidão aciona rollback."));

  push(heading("14. Guardrails epistemológicos", 1));
  push(para("O projeto não afirmará que:"));
  push(bullet("uma rede neural compreendeu o terceiro nível de Panofsky;"));
  push(bullet("distância entre embeddings demonstra filiação histórica;"));
  push(bullet("os dez indicadores formam uma escala psicométrica única;"));
  push(bullet("o codebook é uma verdade objetiva;"));
  push(bullet("uma classificação visual prova um regime iconocrático;"));
  push(bullet("o corpus é amostra probabilística de toda a cultura jurídica;"));
  push(bullet("o desempenho sobre esta coorte generaliza automaticamente a outros acervos."));
  push(quote("O modelo identificou proximidades em um espaço de características visuais. Essas proximidades foram avaliadas como formalmente semelhantes ou iconograficamente úteis segundo um protocolo explícito."));

  push(heading("15. Decisões a validar com os professores", 1));
  push(numbered("Recuperação por similaridade é aceita como tarefa principal?", "questions"));
  push(numbered("Uma cabeça linear/checkpoint próprio sobre extrator pré-treinado satisfaz a exigência de checkpoint?", "questions"));
  push(numbered("Há número mínimo ou máximo de integrantes e prazo de registro?", "questions"));
  push(numbered("Existe rubrica ou modelo obrigatório para relatório, vídeo e poster?", "questions"));
  push(numbered("O VLAB@UFSC estará disponível com qual hardware?", "questions"));
  push(numbered("O ZIP pode omitir imagens restritas e reconstruí-las por manifesto?", "questions"));
  push(numbered("Haverá apresentação de andamento para todas as equipes?", "questions"));

  push(heading("16. Primeiro sprint", 1));
  push(numbered("Fixar a tag ICONOCRACIA-CV-2026-08-12 como universo do semestre.", "sprint"));
  push(numbered("Gerar a lista reproduzível dos candidatos visuais e o crosswalk.", "sprint"));
  push(numbered("Recuperar e validar os binários; calcular MIME, dimensões e hashes.", "sprint"));
  push(numbered("Agrupar duplicatas, vistas e séries; produzir contact sheet.", "sprint"));
  push(numbered("Adjudicar elegibilidade e proveniência dos rótulos.", "sprint"));
  push(numbered("Congelar vision-v1 com split_group e data card.", "sprint"));
  push(numbered("Executar histograma + k-NN antes de qualquer deep learning.", "sprint"));

  push(heading("Conclusão", 1));
  push(para("A força do projeto não está em inventar uma rede neural, mas em oferecer um problema interdisciplinar real com corpus próprio, controle de proveniência e uma pergunta interpretativa que a Computação sozinha não resolve. O freeze público é um marco válido de reprodutibilidade; a próxima conquista é convertê-lo, por gates explícitos, em uma coorte visual realmente processável."));
  push(para("O resultado do semestre deverá mostrar não apenas qual representação recupera vizinhos mais convincentes, mas também quando os métodos falham, que atalhos aprendem e como a especialista transforma distância computacional em comparação juridicamente e historicamente responsável."));

  push(heading("Fontes e referências", 1));
  const refs = [
    "DALAL, Navneet; TRIGGS, Bill. Histograms of Oriented Gradients for Human Detection. In: IEEE CONFERENCE ON COMPUTER VISION AND PATTERN RECOGNITION, 2005.",
    "HE, Kaiming et al. Deep Residual Learning for Image Recognition. In: IEEE CONFERENCE ON COMPUTER VISION AND PATTERN RECOGNITION, 2016. p. 770–778.",
    "OQUAB, Maxime et al. DINOv2: Learning Robust Visual Features without Supervision. arXiv:2304.07193, 2023.",
    "PANOFSKY, Erwin. Meaning in the Visual Arts. Garden City: Doubleday, 1955.",
    "RADFORD, Alec et al. Learning Transferable Visual Models From Natural Language Supervision. In: INTERNATIONAL CONFERENCE ON MACHINE LEARNING, 2021. p. 8748–8763.",
    "TAN, Mingxing; LE, Quoc V. EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks. Proceedings of Machine Learning Research, v. 97, p. 6105–6114, 2019.",
    "UNIVERSIDADE FEDERAL DE SANTA CATARINA. INE410159/TRV410001 — Visão Computacional, 2026.2. Moodle UFSC. Captura de 12 ago. 2026.",
    "VANZIN MENDES, Ana Vitória. ICONOCRACIA Corpus. Release ICONOCRACIA-CV-2026-08-12. Hugging Face, 2026. Disponível em: https://huggingface.co/datasets/warholana/iconocracy-corpus.",
    "VANZIN MENDES, Ana Vitória. Codebook — 10 indicadores ordinais de purificação. Repositório ICONOCRACIA, 2026.",
  ];
  refs.forEach((r) => push(para(r, { style: "Reference" })));

  push(heading("Apêndice A — Manifesto mínimo de vision-v1", 1));
  push(dataTable(
    ["Campo", "Conteúdo"],
    [
      ["freeze_id", "ICONOCRACIA-CV-2026-08-12"],
      ["sample_id / item_id / legacy_handle", "Identidade estável e crosswalk"],
      ["image_sha256 / local_path", "Byte efetivamente processado"],
      ["source_url / image_url / source_domain", "Proveniência e análise de viés"],
      ["license_status", "Uso e redistribuição"],
      ["width / height / mime_type / color_mode", "Contrato técnico"],
      ["year / country / support", "Estratificação"],
      ["series_id / split_group", "Prevenção de vazamento"],
      ["label_provenance / adjudication_status", "Elegibilidade supervisionada"],
      ["eligible / exclusion_reason", "Decisão auditável"],
      ["snapshot_date", "Data ISO YYYY-MM-DD"],
    ],
    [3900, 5966],
  ));

  push(heading("Apêndice B — Arquivos-fonte do dossiê", 1));
  push(bullet("docs/apresentacao-visao-computacional-2026-2.md — pitch inicial e formulações corrigidas."));
  push(bullet("docs/projeto-disciplina-visao-computacional-2026-2.md — protocolo técnico e data card preliminar."));
  push(bullet("data/docs/codebook.md — definições operacionais dos dez indicadores."));
  push(bullet("output/huggingface/ICONOCRACIA-CV-2026-08-12/ — release local verificado."));
  push(bullet("PDF do Moodle da disciplina INE410159/TRV410001 — objetivos, módulos, cronograma e entregas."));
  push(bullet("Dataset público warholana/iconocracy-corpus — tag imutável do semestre."));

  const doc = new Document({
    creator: "Ana Vitória Vanzin Mendes",
    title: "ICONOCRACIA × Visão Computacional — dossiê integrado 2026.2",
    subject: "Dataset, redes neurais, auditoria e plano experimental",
    keywords: "ICONOCRACIA, visão computacional, CNN, dataset, CBIR, transfer learning, iconografia jurídica",
    description: "Dossiê integrado para INE410159/TRV410001 — Visão Computacional 2026.2",
    styles: {
      default: { document: { run: { font: "Arial", size: 21, color: C.ink }, paragraph: { spacing: { line: 276 } } } },
      paragraphStyles: [
        { id: "Title", name: "Title", basedOn: "Normal", next: "Body", quickFormat: true, run: { font: "Georgia", size: 42, bold: true, color: C.navy }, paragraph: { spacing: { before: 240, after: 260 }, alignment: AlignmentType.CENTER, outlineLevel: 0 } },
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Body", quickFormat: true, run: { font: "Georgia", size: 31, bold: true, color: C.navy }, paragraph: { spacing: { before: 380, after: 160 }, keepNext: true, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Body", quickFormat: true, run: { font: "Georgia", size: 26, bold: true, color: C.blue }, paragraph: { spacing: { before: 280, after: 120 }, keepNext: true, outlineLevel: 1 } },
        { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Body", quickFormat: true, run: { font: "Arial", size: 23, bold: true, color: C.green }, paragraph: { spacing: { before: 220, after: 100 }, keepNext: true, outlineLevel: 2 } },
        { id: "Body", name: "Body", basedOn: "Normal", run: { font: "Arial", size: 21, color: C.ink }, paragraph: { spacing: { line: 286, after: 150 }, alignment: AlignmentType.JUSTIFIED, widowControl: true } },
        { id: "Small", name: "Small", basedOn: "Normal", run: { font: "Arial", size: 18, color: C.ink }, paragraph: { spacing: { line: 240, after: 40 }, widowControl: true } },
        { id: "Quote", name: "Quote", basedOn: "Body", run: { font: "Georgia", size: 22, italics: true, color: C.navy }, paragraph: { spacing: { line: 290, after: 0 }, alignment: AlignmentType.LEFT } },
        { id: "Caption", name: "Caption", basedOn: "Normal", run: { font: "Arial", size: 17, italics: true, color: C.muted }, paragraph: { spacing: { after: 180 }, alignment: AlignmentType.CENTER } },
        { id: "Reference", name: "Reference", basedOn: "Body", run: { font: "Arial", size: 18, color: C.ink }, paragraph: { spacing: { line: 240, after: 100 }, indent: { hanging: 540 } } },
      ],
    },
    numbering: {
      config: [
        { reference: "bullets", levels: [
          { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 600, hanging: 280 } } } },
          { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1100, hanging: 280 } } } },
        ] },
        ...["steps", "layers", "pipeline", "deliverables", "regression", "questions", "sprint"].map((reference) => ({ reference, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 650, hanging: 330 } } } }] })),
      ],
    },
    sections: [{
      properties: {
        titlePage: true,
        page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN }, pageNumbers: { start: 1 } },
      },
      headers: {
        default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [tr("ICONOCRACIA × Visão Computacional · 2026.2", { size: 16, color: C.muted })] })] }),
        first: new Header({ children: [new Paragraph({ children: [] })] }),
      },
      footers: {
        default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [tr("Página ", { size: 16, color: C.muted }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: C.muted }), tr(" de ", { size: 16, color: C.muted }), new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: C.muted })] })] }),
      },
      children,
    }],
  });

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, await Packer.toBuffer(doc));
}

build().catch((err) => {
  process.stderr.write(`${err.stack || err}\n`);
  process.exit(1);
});
