import { GoogleGenAI, Type, ThinkingLevel, type Part } from '@google/genai';
import type {
  WebScoutOutput,
  MasterRecord,
  PipelineOutput,
  GroundingChunk,
  AdvancedParams,
} from '../types/gemini.js';

// Re-export types for convenience
export type { WebScoutOutput, MasterRecord, PipelineOutput, GroundingChunk, AdvancedParams };

// ── AI client ───────────────────────────────────────────────────────
function getAI(): GoogleGenAI {
  const key = process.env.GEMINI_API_KEY;
  if (!key) throw new Error('GEMINI_API_KEY not set');
  return new GoogleGenAI({ apiKey: key });
}

// ── System instructions ─────────────────────────────────────────────
const territorialAttributionInstruction = `Para cada afirmação, explicite qual relação a evidência permite afirmar: autoria e nacionalidade do artista, lugar de produção, localização atual, assunto representado, encomenda/patrocínio, contexto político e jurisdição na data, circulação ou recepção.
Essas relações são independentes: nacionalidade do artista, produção, localização atual ou assunto representado não autorizam atribuir uma nacionalidade única ao objeto nem transferir automaticamente um vínculo para outra relação. Uma relação com o Brasil deve nomear o vínculo específico que a fonte sustenta; influência exige evidência própria. Autoria ou produção estrangeira também não exclui relação documentada com o Brasil.
Use os nomes territoriais e institucionais cabíveis à data; aquisição não data produção e instituição imperial não demonstra encomenda republicana. Um catálogo documenta inicialmente a atribuição feita pelo catálogo, que deve ser distinguida de uma atribuição histórica conferida.
Não é necessário preencher todas as relações. Registre como desconhecido ou gap o que falta; isso permite catalogação e permanência do item, sem impedir afirmações independentes sustentadas. Busca sem resultado não prova inexistência de vínculo. Preserve valores legados como legados, sem distribuí-los automaticamente entre relações.
O núcleo analítico da tese é Brasil, 1822–1922; o catálogo transnacional é mais amplo. Hipótese pode orientar pesquisa se declarada como hipótese, sem inclusão automática no núcleo. Não crie gate nacional, pontuação agregada nem reclassificação automática.`;

const webScoutInstruction = `Atue como o historiador digital do projeto Iconocracy. Sua missão é localizar fontes primárias e metadados estruturados de iconografia jurídica. Para cada entrada, gere um JSON com:
search_results: Lista de fontes com IDs e URLs.
score: Cálculo de confiança (0.0 a 1.0) baseado na autoridade da instituição.
gaps: Identificação de ausência de dados (autor, data, etc).
${territorialAttributionInstruction}
Trate local, título, tema, país de campanha e outros parâmetros de busca como pistas, não como fatos do objeto. Localize fontes para o vínculo específico e registre em gaps relações não documentadas, contradições e limites da busca. O score da fonte não mede pertencimento nacional. Respeite as chaves do esquema de saída.`;

const iconoCodeInstruction = `Atue como analista semiótico. Processe a evidência visual e documental trazida pelo WebScout.
Aplique a taxonomia Iconclass.
Analise a semântica jurídica no contexto documentado do objeto; só proponha transferência de repertório, apropriação ou influência sobre o Brasil quando houver evidência específica. Sem esse vínculo, declare a lacuna ou formule uma hipótese de pesquisa identificada como tal.
${territorialAttributionInstruction}
Em semiotic_analysis, distinga registro documental, filologia conceitual e hipótese iconológica; os três estratos não se confirmam automaticamente. Qualifique cada afirmação relevante como supported, tentative ou gap, identificando os IDs de evidência que a sustentam (supports), contradizem (contradicts) e as lacunas (gaps). Não invente fontes, vínculos ou localizadores.
Gere a citação ABNT NBR 6023:2025 com metadados conferidos; se faltarem dados, declare a lacuna em abnt_citation.
Saída estritamente em JSON com iconclass_codes, semiotic_analysis e abnt_citation, conforme o esquema desta interface. Esta saída simplificada requer revisão antes de integrar o ledger canônico; não equivale ao master-record canônico.`;

const corpusContextUrls = [
  'https://raw.githubusercontent.com/anavvanzin/iconocracy-corpus/main/Iconocracia_Sintese_de_Pesquisa.md',
  'https://raw.githubusercontent.com/anavvanzin/iconocracy-corpus/main/ICONOCRACIA_PROJETO.md',
  'https://raw.githubusercontent.com/anavvanzin/iconocracy-corpus/main/Apostolado_Positivista_Programa_Iconografico.md',
  'https://raw.githubusercontent.com/anavvanzin/iconocracy-corpus/main/Debret_Vol3_Placas_Iconocracia.md',
];

// ── Image generation ────────────────────────────────────────────────
export async function generateIconographyImage(
  prompt: string,
  imageData?: { base64: string; mimeType: string },
  size = '1K',
  aspectRatio = '1:1'
): Promise<string> {
  const ai = getAI();

  const parts: Part[] = [];
  if (imageData) {
    parts.push({ inlineData: { data: imageData.base64, mimeType: imageData.mimeType } });
  }
  parts.push({ text: prompt });

  const response = await ai.models.generateContent({
    model: 'gemini-3.1-flash-image-preview',
    contents: { parts },
    config: {
      imageConfig: { aspectRatio, imageSize: size },
      tools: [{ googleSearch: { searchTypes: { webSearch: {}, imageSearch: {} } } }],
    },
  });

  for (const part of response.candidates?.[0]?.content?.parts || []) {
    if (part.inlineData) {
      return `data:${part.inlineData.mimeType || 'image/png'};base64,${part.inlineData.data}`;
    }
  }

  throw new Error('Nenhuma imagem foi gerada pelo modelo.');
}

// ── Evidence mining pipeline (WebScout → IconoCode) ─────────────────
export async function mineEvidences(
  hint: string,
  imageData?: { base64: string; mimeType: string },
  advancedParams?: AdvancedParams
): Promise<PipelineOutput> {
  const ai = getAI();
  const parts: Part[] = [];

  if (imageData) {
    parts.push({ inlineData: { data: imageData.base64, mimeType: imageData.mimeType } });
  }

  let finalHint = hint;
  if (advancedParams) {
    const extras = [];
    if (advancedParams.dateRange) extras.push(`Período desejado: ${advancedParams.dateRange}`);
    if (advancedParams.location) extras.push(`Localização geográfica: ${advancedParams.location}`);
    if (advancedParams.iconclassCodes) extras.push(`Códigos Iconclass específicos: ${advancedParams.iconclassCodes}`);
    if (extras.length) finalHint += `\n\nParâmetros avançados de busca:\n- ${extras.join('\n- ')}`;
  }

  if (finalHint) parts.push({ text: finalHint });

  parts.push({
    text: `\n\nConsulte os seguintes documentos de pesquisa (Iconocracy) como contexto de trabalho, verificando sua disponibilidade e versão. Eles não substituem as fontes primárias do objeto nem confirmam por si um vínculo territorial ou político:\n${corpusContextUrls.map((u) => `- ${u}`).join('\n')}`,
  });

  // Agent 1: WebScout
  const webScoutResponse = await ai.models.generateContent({
    model: 'gemini-3-flash-preview',
    contents: { parts },
    config: {
      systemInstruction: webScoutInstruction,
      responseMimeType: 'application/json',
      thinkingConfig: { thinkingLevel: ThinkingLevel.HIGH },
      tools: [{ googleSearch: {} }, { urlContext: {} }],
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          search_results: {
            type: Type.ARRAY,
            items: {
              type: Type.OBJECT,
              properties: {
                evidence_id: { type: Type.STRING },
                url: { type: Type.STRING },
                score: { type: Type.NUMBER },
                institution: { type: Type.STRING },
              },
              required: ['evidence_id', 'url', 'score', 'institution'],
            },
          },
          gaps: { type: Type.ARRAY, items: { type: Type.STRING } },
        },
        required: ['search_results', 'gaps'],
      },
    },
  });

  const webScoutText = webScoutResponse.text;
  if (!webScoutText) throw new Error('No response from WebScout');

  const webScoutOutput = JSON.parse(webScoutText) as WebScoutOutput;

  const chunks = webScoutResponse.candidates?.[0]?.groundingMetadata?.groundingChunks;
  if (chunks) {
    webScoutOutput.grounding_chunks = chunks
      .map((c: { web?: { uri?: string; title?: string } }) => ({
        uri: c.web?.uri || '',
        title: c.web?.title || '',
      }))
      .filter((c: GroundingChunk) => c.uri);
  }

  // Agent 2: IconoCode
  const iconoCodeResponse = await ai.models.generateContent({
    model: 'gemini-3.1-pro-preview',
    contents: {
      parts: [...parts, { text: `\n\nResultados do WebScout:\n${JSON.stringify(webScoutOutput, null, 2)}` }],
    },
    config: {
      systemInstruction: iconoCodeInstruction,
      responseMimeType: 'application/json',
      thinkingConfig: { thinkingLevel: ThinkingLevel.HIGH },
      tools: [{ urlContext: {} }],
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          iconclass_codes: { type: Type.ARRAY, items: { type: Type.STRING } },
          semiotic_analysis: { type: Type.STRING },
          abnt_citation: { type: Type.STRING },
        },
        required: ['iconclass_codes', 'semiotic_analysis', 'abnt_citation'],
      },
    },
  });

  const iconoCodeText = iconoCodeResponse.text;
  if (!iconoCodeText) throw new Error('No response from IconoCode');

  const masterRecord = JSON.parse(iconoCodeText) as MasterRecord;

  return { webScout: webScoutOutput, masterRecord };
}

// ── Corpus inference ────────────────────────────────────────────────
export async function generateCorpusInference(
  title: string,
  era: string,
  taxCode: string
): Promise<string> {
  // This interface receives catalogue hints, not a dossier with verifiable evidence.
  // Keep its public signature while returning the gap without a paid model call.
  return `Lacuna documental (gap): "${title}" (data informada: ${era}; código informado: ${taxCode}). Título, data e notação não demonstram influência sobre a cultura jurídica brasileira nem pertencimento ao núcleo Brasil, 1822–1922. Para avaliar esse vínculo, consulte fontes de produção, encomenda, contexto político e jurisdição na data, circulação ou recepção, distinguindo cada relação da autoria, localização atual e tema representado. A falta de documentação desse vínculo permite manter o item no catálogo e formular uma hipótese de pesquisa explícita, preservando as demais afirmações que tenham evidência própria.`;
}

// ── Corpus TTS ──────────────────────────────────────────────────────
export async function generateCorpusAudio(text: string): Promise<string> {
  const ai = getAI();

  const response = await ai.models.generateContent({
    model: 'gemini-2.5-flash-preview-tts',
    contents: `Diga num tom académico, firme e informativo: ${text}`,
    config: {
      responseModalities: ['AUDIO'],
      speechConfig: {
        voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Charon' } },
      },
    },
  });

  const base64Audio = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
  const mimeType = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.mimeType;

  if (!base64Audio || !mimeType) throw new Error('No audio generated');

  return `data:${mimeType};base64,${base64Audio}`;
}
