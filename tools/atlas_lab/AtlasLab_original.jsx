// ATLAS LAB — Infraestrutura PPGD/UFSC
// Origem: Gemini Canvas (recuperado em 23/03/2026)
// NOTA: versão original usa Firebase (Firestore + Auth) com variáveis de ambiente
// injectadas pelo ambiente Canvas do Gemini (__firebase_config, __app_id, __initial_auth_token)
// Precisa de adaptação para rodar em ambiente standalone.
//
// PROBLEMA DETECTADO: função exportToLabCSV referenciada mas não definida.
//
// Ver AtlasLab_standalone.jsx para versão corrigida com estado local.

import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  Plus, Database, Layout, FileText, Settings, Search, Filter, ChevronRight,
  BarChart3, Save, Trash2, Sparkles, User, Image as ImageIcon, Info,
  ArrowUpRight, Library, Layers, Activity, Archive, BookOpen, ClipboardCheck,
  Globe, Download, Volume2, BrainCircuit, MessageSquare, Play, Loader2,
  FileJson, FileCode, AlertCircle
} from 'lucide-react';
import { initializeApp } from 'firebase/app';
import {
  getFirestore, collection, doc, setDoc, addDoc, onSnapshot,
  query, deleteDoc, where, orderBy
} from 'firebase/firestore';
import {
  getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged
} from 'firebase/auth';

// --- AUXILIARES PARA ÁUDIO ---
const base64ToArrayBuffer = (base64) => {
  const binaryString = window.atob(base64);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
};
const pcmToWav = (pcmData, sampleRate) => {
  const buffer = new ArrayBuffer(44 + pcmData.length * 2);
  const view = new DataView(buffer);
  const writeString = (offset, string) => {
    for (let i = 0; i < string.length; i++) view.setUint8(offset + i, string.charCodeAt(i));
  };
  writeString(0, 'RIFF'); view.setUint32(4, 32 + pcmData.length * 2, true);
  writeString(8, 'WAVE'); writeString(12, 'fmt '); view.setUint32(16, 16, true);
  view.setUint16(20, 1, true); view.setUint16(22, 1, true);
  view.setUint32(24, sampleRate, true); view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true); view.setUint16(34, 16, true);
  writeString(36, 'data'); view.setUint32(40, pcmData.length * 2, true);
  let offset = 44;
  for (let i = 0; i < pcmData.length; i++, offset += 2) view.setInt16(offset, pcmData[i], true);
  return new Blob([buffer], { type: 'audio/wav' });
};

// --- CONFIGURAÇÃO FIREBASE (injectada pelo Canvas Gemini) ---
const firebaseConfig = JSON.parse(__firebase_config);
const appId = typeof __app_id !== 'undefined' ? __app_id : 'atlas-iconocratico';
const initialToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : undefined;
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

// --- DADOS DO CORPUS ---
const REFERENCE_CORPUS = [
  { id: "BR-001", title: "Alegoria da Agricultura (RS)", date: "1908", country: "BR", medium: "Fotografia P&B", thumbnail_url: "https://brasilianafotografica.bn.gov.br/brasiliana/bitstream/handle/20.500.12156.1/11778/0000001.JPG.jpg", archive: "Brasiliana Fotográfica", suggested_regime: "2" },
  { id: "BR-002", title: "Monumento à República (Belém)", date: "1940", country: "BR", medium: "Monumento", thumbnail_url: "https://brasilianafotografica.bn.gov.br/brasiliana/bitstream/handle/20.500.12156.1/13609/GV%20dvft%20004.JPG.jpg", archive: "Brasiliana Fotográfica", suggested_regime: "1" },
  { id: "BR-005", title: "A República (Matriz Positivista)", date: "1889", country: "BR", medium: "Pintura", thumbnail_url: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/D%C3%A9cio_Villares_-_A_Rep%C3%BAblica.jpg/800px-D%C3%A9cio_Villares_-_A_Rep%C3%BAblica.jpg", archive: "Museu Histórico Nacional", suggested_regime: "2" },
  { id: "BR-006", title: "A Justiça (Ceschiatti - STF)", date: "1961", country: "BR", medium: "Escultura", thumbnail_url: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/A_Justi%C3%A7a_STF.jpg/800px-A_Justi%C3%A7a_STF.jpg", archive: "Arquivo STF", suggested_regime: "2" },
  { id: "FR-001", title: "Marianne (Emprunt 1917)", date: "1917", country: "FR", medium: "Cartaz", thumbnail_url: "https://gallica.bnf.fr/iiif/ark:/12148/btv1b10051217v/f1/full/full/0/native.jpg", archive: "Gallica / Europeana", suggested_regime: "3" },
  { id: "FR-003", title: "La Liberté guidant le peuple", date: "1830", country: "FR", medium: "Pintura", thumbnail_url: "https://upload.wikimedia.org/wikipedia/commons/5/5d/Eug%C3%A8ne_Delacroix_-_Le_28_Juillet._La_Libert%C3%A9_guidant_le_peuple.jpg", archive: "Louvre", suggested_regime: "1" },
  { id: "UK-003", title: "Lady Justice (Old Bailey)", date: "1907", country: "UK", medium: "Escultura", thumbnail_url: "https://upload.wikimedia.org/wikipedia/commons/f/f4/Old_Bailey_Lady_Justice.jpg", archive: "Central Criminal Court", suggested_regime: "2" },
  { id: "US-001", title: "Statue of Liberty", date: "1886", country: "US", medium: "Monumento", thumbnail_url: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Statue_of_Liberty_7.jpg/800px-Statue_of_Liberty_7.jpg", archive: "NPS", suggested_regime: "1" }
];

const REGIMES = [
  { id: '1', name: 'Fundacional-Sacrificial', color: 'bg-rose-100 text-rose-700 border-rose-200' },
  { id: '2', name: 'Normativo-Jurídico', color: 'bg-indigo-100 text-indigo-700 border-indigo-200' },
  { id: '3', name: 'Militar-Imperial', color: 'bg-slate-200 text-slate-800 border-slate-300' }
];

const INDICATORS = [
  { id: 'FEI', name: 'Exposição da Carne', desc: 'Flesh Exposure Index' },
  { id: 'CII', name: 'Idealização Clássica', desc: 'Classical Idealisation' },
  { id: 'PRI', name: 'Rigidez Postural', desc: 'Postural Rigidity' },
  { id: 'SMI', name: 'Materialidade Estatuária', desc: 'Statuary Material' },
  { id: 'SMS', name: 'Serenidade/Militância', desc: 'Serenity/Militancy' },
  { id: 'AMCP', name: 'Presença de Armadura', desc: 'Armor/Military Clothing' },
  { id: 'MVI', name: 'Visibilidade Maternal', desc: 'Maternal Visibility' },
  { id: 'WI', name: 'Índice de Armamento', desc: 'Weapon Index' },
  { id: 'RI', name: 'Racialização', desc: 'Racialisation Index' },
  { id: 'AI', name: 'Atemporalidade', desc: 'Agelessness Index' }
];

const PANELS = [
  { id: 'P1', title: 'I: Mães Fundacionais', regime: '1' },
  { id: 'P2', title: 'II: Calcificação da Justitia', regime: '2' },
  { id: 'P3', title: 'III: Enrijecimento Tegumentar', regime: '3' },
  { id: 'P4', title: 'IV: Hegemonia Marmórea', focus: 'Racialização (RI)' },
  { id: 'P5', title: 'V: Ubiquidade Íntima', focus: 'Micro-Iconocracia' }
];

// [... componente App completo — ver código original do Gemini ...]
// MISSING: exportToLabCSV — precisa ser implementada
export default App;
