// Types
export type { CorpusItem, Indicadores, Panofsky, PanofskyIconographic, PanofskyIconological, Regime } from './types/corpus.js';
export type { UserProfile } from './types/user.js';
export type { SearchResult, GroundingChunk, WebScoutOutput, MasterRecord, PipelineOutput, AdvancedParams } from './types/gemini.js';

// Services — Firebase
export {
  initFirebase,
  getDb,
  getAuthInstance,
  signInWithGoogle,
  signInAnonymouslyUser,
  logout,
  onAuthStateChanged,
  doc,
  getDoc,
  setDoc,
  serverTimestamp,
} from './services/firebase.js';
export type { AppMode, User, Auth, Firestore } from './services/firebase.js';

// Services — Gemini
export {
  generateIconographyImage,
  mineEvidences,
  generateCorpusInference,
  generateCorpusAudio,
} from './services/gemini.js';

// Services — Corpus data
export {
  loadCorpus,
  getCorpus,
  filterByCountry,
  filterByRegime,
  filterByDateRange,
  filterByIconclass,
  filterInScope,
  countByField,
  averageEndurecimento,
} from './services/corpus.js';
