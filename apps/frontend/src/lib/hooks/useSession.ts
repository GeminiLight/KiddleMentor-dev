"use client";

import { useState, useEffect, useCallback } from 'react';
import { api, LearnerProfile, getStoredLearnerId, setStoredLearnerId, clearStoredLearnerId } from '../api';

interface UseSessionReturn {
  /** Current learner ID */
  learnerId: string | null;
  /** Learner profile from backend */
  profile: LearnerProfile | null;
  /** Loading state */
  isLoading: boolean;
  /** Error state */
  error: string | null;
  /** Whether user has an active session */
  isAuthenticated: boolean;
  /** Initialize a new session */
  initializeSession: (name?: string, email?: string) => Promise<string>;
  /** Refresh profile from backend */
  refreshProfile: () => Promise<void>;
  /** Clear session and logout */
  clearSession: () => void;
}

/**
 * React hook for managing learner session with backend synchronization.
 *
 * Features:
 * - Automatically restores session from localStorage on mount
 * - Verifies session with backend
 * - Provides session initialization and profile management
 * - Syncs with backend workspace memory
 *
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { learnerId, profile, initializeSession, isLoading } = useSession();
 *
 *   if (isLoading) return <div>Loading...</div>;
 *
 *   if (!learnerId) {
 *     return <button onClick={() => initializeSession('John')}>Start</button>;
 *   }
 *
 *   return <div>Welcome, {profile?.name}!</div>;
 * }
 * ```
 */
export function useSession(): UseSessionReturn {
  const [learnerId, setLearnerId] = useState<string | null>(null);
  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize or restore session on mount
  useEffect(() => {
    const initSession = async () => {
      try {
        // Check localStorage for existing learner_id
        const savedId = getStoredLearnerId();

        if (savedId) {
          // Verify with backend
          try {
            const { learner_profile } = await api.getProfile(savedId);
            setLearnerId(savedId);
            setProfile(learner_profile);
            console.log('[useSession] Restored session:', savedId);
          } catch {
            // Profile not found on backend, clear local storage
            console.warn('[useSession] Saved learner_id not found on backend, clearing local storage');
            clearStoredLearnerId();
            setLearnerId(null);
            setProfile(null);
          }
        } else {
          console.log('[useSession] No saved session found');
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to initialize session';
        console.error('[useSession] Error:', message);
        setError(message);
      } finally {
        setIsLoading(false);
      }
    };

    initSession();
  }, []);

  // Initialize new session
  const initializeSession = useCallback(async (name?: string, email?: string): Promise<string> => {
    try {
      setIsLoading(true);
      setError(null);

      console.log('[useSession] Initializing new session:', { name, email });

      const { learner_id, profile: newProfile } = await api.initializeSession({
        name: name || 'Anonymous Learner',
        email,
      });

      // Save to localStorage
      setStoredLearnerId(learner_id);

      setLearnerId(learner_id);
      setProfile(newProfile);

      console.log('[useSession] Session initialized:', learner_id);

      return learner_id;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to initialize session';
      console.error('[useSession] Initialization failed:', message);
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Refresh profile from backend
  const refreshProfile = useCallback(async () => {
    if (!learnerId) {
      console.warn('[useSession] Cannot refresh profile: no learner_id');
      return;
    }

    try {
      console.log('[useSession] Refreshing profile for:', learnerId);
      const { learner_profile } = await api.getProfile(learnerId);
      setProfile(learner_profile);
      console.log('[useSession] Profile refreshed');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to refresh profile';
      console.error('[useSession] Refresh failed:', message);
      setError(message);
    }
  }, [learnerId]);

  // Clear session
  const clearSession = useCallback(() => {
    console.log('[useSession] Clearing session');
    clearStoredLearnerId();
    setLearnerId(null);
    setProfile(null);
    setError(null);
  }, []);

  return {
    learnerId,
    profile,
    isLoading,
    error,
    isAuthenticated: !!learnerId,
    initializeSession,
    refreshProfile,
    clearSession,
  };
}
