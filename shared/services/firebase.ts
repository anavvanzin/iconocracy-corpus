import { initializeApp, type FirebaseApp } from 'firebase/app';
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signInAnonymously,
  signOut,
  onAuthStateChanged,
  type Auth,
  type User,
} from 'firebase/auth';
import {
  getFirestore,
  doc,
  getDoc,
  setDoc,
  serverTimestamp,
  type Firestore,
} from 'firebase/firestore';
import { getAnalytics } from 'firebase/analytics';
import type { UserProfile } from '../types/user.js';

// ── Firebase configs ────────────────────────────────────────────────
// webiconocracy project (corpus mining, default database)
const webiconocracyConfig = {
  apiKey: 'AIzaSyC8tIk6qfnDDsGiMMf6PZNIEvEo_zwRIGk',
  authDomain: 'gen-lang-client-0433804370.firebaseapp.com',
  projectId: 'gen-lang-client-0433804370',
  storageBucket: 'gen-lang-client-0433804370.firebasestorage.app',
  messagingSenderId: '604053972231',
  appId: '1:604053972231:web:56c724f5941390beb6d1a2',
  measurementId: 'G-NE9HT24SSR',
};

// iurisvision project (productivity, named database)
const iurisvisionConfig = {
  apiKey: 'AIzaSyB285uRooSJZm7QfCjSKolukA-IuKKdDIU',
  authDomain: 'gen-lang-client-0218803071.firebaseapp.com',
  projectId: 'gen-lang-client-0218803071',
  storageBucket: 'gen-lang-client-0218803071.firebasestorage.app',
  messagingSenderId: '1066380962084',
  appId: '1:1066380962084:web:da6b1e4eaff554d3642bb1',
  firestoreDatabaseId: 'ai-studio-01147a01-be1d-449c-bff5-983331717d08',
};

export type AppMode = 'webiconocracy' | 'iurisvision';

// ── Singleton instances ─────────────────────────────────────────────
let _app: FirebaseApp | null = null;
let _db: Firestore | null = null;
let _auth: Auth | null = null;
let _mode: AppMode | null = null;

/**
 * Initialize Firebase for the given app mode.
 * Call once at app startup (main.tsx).
 */
export function initFirebase(mode: AppMode) {
  if (_app && _mode === mode) return { app: _app, db: _db!, auth: _auth! };

  const config = mode === 'iurisvision' ? iurisvisionConfig : webiconocracyConfig;
  _app = initializeApp(config);
  _auth = getAuth(_app);
  _mode = mode;

  if (mode === 'iurisvision') {
    _db = getFirestore(_app, iurisvisionConfig.firestoreDatabaseId);
  } else {
    _db = getFirestore(_app);
  }

  if (typeof window !== 'undefined') {
    getAnalytics(_app);
  }

  return { app: _app, db: _db, auth: _auth };
}

/** Get Firestore instance (must call initFirebase first) */
export function getDb(): Firestore {
  if (!_db) throw new Error('Firebase not initialized. Call initFirebase() first.');
  return _db;
}

/** Get Auth instance (must call initFirebase first) */
export function getAuthInstance(): Auth {
  if (!_auth) throw new Error('Firebase not initialized. Call initFirebase() first.');
  return _auth;
}

// ── Auth helpers ────────────────────────────────────────────────────
const googleProvider = new GoogleAuthProvider();

const DEFAULT_PROFILE: Omit<UserProfile, 'uid' | 'email' | 'displayName' | 'createdAt'> = {
  role: 'user',
  xp: 0,
  level: 1,
  badges: [],
};

async function ensureUserProfile(user: User) {
  const db = getDb();
  const userRef = doc(db, 'users', user.uid);
  const userSnap = await getDoc(userRef);

  if (!userSnap.exists()) {
    await setDoc(userRef, {
      uid: user.uid,
      email: user.email || 'anonymous@iconocracy.app',
      displayName: user.displayName || 'Pesquisador',
      ...DEFAULT_PROFILE,
      createdAt: serverTimestamp(),
    });
  }
}

export async function signInWithGoogle() {
  const auth = getAuthInstance();
  const result = await signInWithPopup(auth, googleProvider);
  await ensureUserProfile(result.user);
  return result.user;
}

export async function signInAnonymouslyUser() {
  const auth = getAuthInstance();
  const result = await signInAnonymously(auth);
  await ensureUserProfile(result.user);
  return result.user;
}

export async function logout() {
  const auth = getAuthInstance();
  await signOut(auth);
}

export { onAuthStateChanged, doc, getDoc, setDoc, serverTimestamp };
export type { User, Auth, Firestore };
