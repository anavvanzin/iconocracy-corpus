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
const webScoutInstruction = `Atue como o historiador digital do projeto Iconocracy. Sua missão é localizar fontes primárias e metadados estruturados de iconografia jurídica. Para cada entrada, gere um JSON com:
search_results: Lista de fontes com IDs e URLs.
score: Cálculo de confiança (0.0 a 1.0) baseado na autoridade da instituição.
gaps: Identificação de ausência de dados (autor, data, etc).`;

const iconoCodeInstruction = `Atue como analista semiótico. Processe a evidência visual e documental trazida pelo WebScout.
Aplique a taxonomia Iconclass.
Analise a semântica jurídica: foque na tensão entre a tradição europeia e a apropriação brasileira.
Gere obrigatoriamente uma citação ABNT NBR 6023:2025.
Saída estritamente em JSON compatível com o esquema MasterRecord.`;

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
    text: `\n\nConsidere o seguinte corpus de pesquisa (Iconocracy) como base de conhecimento primária para sua análise:\n${corpusContextUrls.map((u) => `- ${u}`).join('\n')}`,
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
  const ai = getAI();
  const prompt = `Atue como o IconoCode AI. Com base no registo iconográfico "${title}" (${era}, Iconclass: ${taxCode}), gere um parágrafo curto de análise especulativa sobre como este artefacto influenciou a cultura jurídica brasileira no século XIX. Foque em padrões ocultos e semiótica do poder.`;

  const response = await ai.models.generateContent({
    model: 'gemini-3.1-pro-preview',
    contents: prompt,
  });

  return response.text || 'Erro ao gerar análise.';
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
