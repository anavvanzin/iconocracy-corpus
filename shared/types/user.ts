export interface UserProfile {
  uid: string;
  email: string;
  displayName: string;
  role: string;
  xp: number;
  level: number;
  badges: string[];
  createdAt: unknown; // Firestore Timestamp
}
