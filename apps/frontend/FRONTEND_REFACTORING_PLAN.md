# Frontend Refactoring Plan - Local Mode Integration

## Current Issues

### 1. **No Backend Integration for Local Mode**
- Frontend uses `localStorage` for everything
- No calls to backend's session initialization (`/api/v1/profile/initialize-session`)
- No `learner_id` management
- No interaction with backend's workspace memory

### 2. **API Layer Outdated**
- `src/lib/api.ts` calls old endpoints like `/create-learner-profile-with-info` (renamed to `/create-learner-profile`)
- Missing critical endpoints:
  - `/api/v1/profile/initialize-session`
  - `/api/v1/profile/{learner_id}`
  - `/api/v1/profile/{learner_id}/set-goal`
  - `/api/v1/dashboard/{learner_id}`
  - `/api/v1/progress/{learner_id}/session-complete`

### 3. **Hardcoded Model Names**
- Uses `gpt-5.1` which doesn't exist
- Should fetch available models from `/api/v1/list-llm-models`

### 4. **Data Flow Problems**
- Onboarding flow doesn't create learner_id
- localStorage stores raw JSON strings
- No persistence to backend memory
- Dashboard shows mock data instead of real progress

### 5. **Missing Features from Backend**
- No quiz functionality (backend has `/api/v1/assessment/generate-document-quizzes`)
- No content tailoring (backend has `/api/v1/learning/tailor-knowledge-content`)
- No session completion tracking
- No mastery tracking

---

## Refactoring Strategy

### Phase 1: API Layer Modernization ✅ **CRITICAL**

**Goal**: Update `src/lib/api.ts` to match backend's current endpoints

**Changes**:

```typescript
// src/lib/api.ts

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api/v1';

// Add proper types
export interface LearnerProfile {
  learner_id: string;
  name: string;
  email?: string;
  learning_goal?: string;
  refined_goal?: any;
  progress_percent?: number;
  created_at: string;
  updated_at?: string;
}

export interface DashboardData {
  learner: LearnerProfile & {
    progress: number;
    total_sessions: number;
    completed_sessions: number;
  };
  current_session?: any;
  learning_path?: { sessions: any[] };
  recent_activity: any[];
  mastery: Record<string, number>;
}

// New API methods
export const api = {
  // Session Management
  initializeSession: (data: { name?: string; email?: string }) =>
    fetchApi<{ learner_id: string; profile: LearnerProfile }>('/profile/initialize-session', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getProfile: (learnerId: string) =>
    fetchApi<{ learner_profile: LearnerProfile }>(`/profile/${learnerId}`),

  setLearningGoal: (learnerId: string, goal: string, modelProvider?: string, modelName?: string) =>
    fetchApi<{ refined_goal: any }>(`/profile/${learnerId}/set-goal`, {
      method: 'POST',
      body: JSON.stringify({
        learning_goal: goal,
        model_provider: modelProvider,
        model_name: modelName,
      }),
    }),

  // Dashboard
  getDashboard: (learnerId: string) =>
    fetchApi<DashboardData>(`/dashboard/${learnerId}`),

  // Learning Path
  scheduleLearningPath: (learnerId: string, sessionCount: number) =>
    fetchApi<{ learning_path: any }>('/schedule-learning-path', {
      method: 'POST',
      body: JSON.stringify({
        learner_profile: JSON.stringify({ learner_id: learnerId }),
        session_count: sessionCount,
      }),
    }),

  // Progress Tracking
  completeSession: (learnerId: string, sessionNumber: number, quizScore?: number, durationMinutes?: number) =>
    fetchApi<{ next_session: any; progress_percent: number }>(`/progress/${learnerId}/session-complete`, {
      method: 'POST',
      body: JSON.stringify({
        session_number: sessionNumber,
        quiz_score: quizScore,
        duration_minutes: durationMinutes,
      }),
    }),

  // Content Generation
  generateTailoredContent: (learnerId: string, learningSession: any, withQuiz?: boolean) =>
    fetchApi<{ tailored_content: any }>('/learning/tailor-knowledge-content', {
      method: 'POST',
      body: JSON.stringify({
        learner_profile: JSON.stringify({ learner_id: learnerId }),
        learning_path: '{}',  // Backend loads from memory
        learning_session: JSON.stringify(learningSession),
        with_quiz: withQuiz,
      }),
    }),

  // Chat
  chatWithTutor: (learnerId: string, messages: any[]) =>
    fetchApi<{ response: string }>('/chat/chat-with-tutor', {
      method: 'POST',
      body: JSON.stringify({
        messages: JSON.stringify(messages),
        learner_profile: JSON.stringify({ learner_id: learnerId }),
      }),
    }),

  // Skills
  identifySkillGap: (learnerId: string, learningGoal: string, learnerInformation: string) =>
    fetchApi<{ skill_gaps: any }>('/skills/identify-skill-gap-with-info', {
      method: 'POST',
      body: JSON.stringify({
        learning_goal: learningGoal,
        learner_information: learnerInformation,
      }),
    }),

  // Models
  listModels: () =>
    fetchApi<{ models: Array<{ model_name: string; model_provider: string }> }>('/list-llm-models'),
};
```

---

### Phase 2: Session Management Hook ✅ **CRITICAL**

**Goal**: Create React hook for managing learner session with backend sync

**File**: `src/lib/hooks/useSession.ts`

```typescript
import { useState, useEffect } from 'react';
import { api, LearnerProfile } from '../api';

const SESSION_KEY = 'gen_mentor_learner_id';

export function useSession() {
  const [learnerId, setLearnerId] = useState<string | null>(null);
  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize or restore session on mount
  useEffect(() => {
    const initSession = async () => {
      try {
        // Check localStorage for existing learner_id
        const savedId = localStorage.getItem(SESSION_KEY);

        if (savedId) {
          // Verify with backend
          try {
            const { learner_profile } = await api.getProfile(savedId);
            setLearnerId(savedId);
            setProfile(learner_profile);
          } catch (err) {
            // Profile not found on backend, clear local storage
            console.warn('Saved learner_id not found on backend, initializing new session');
            localStorage.removeItem(SESSION_KEY);
            setLearnerId(null);
            setProfile(null);
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to initialize session');
      } finally {
        setIsLoading(false);
      }
    };

    initSession();
  }, []);

  // Initialize new session
  const initializeSession = async (name?: string, email?: string) => {
    try {
      setIsLoading(true);
      const { learner_id, profile } = await api.initializeSession({ name, email });

      // Save to localStorage
      localStorage.setItem(SESSION_KEY, learner_id);

      setLearnerId(learner_id);
      setProfile(profile);
      setError(null);

      return learner_id;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to initialize session';
      setError(message);
      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  };

  // Refresh profile from backend
  const refreshProfile = async () => {
    if (!learnerId) return;

    try {
      const { learner_profile } = await api.getProfile(learnerId);
      setProfile(learner_profile);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh profile');
    }
  };

  // Clear session
  const clearSession = () => {
    localStorage.removeItem(SESSION_KEY);
    setLearnerId(null);
    setProfile(null);
    setError(null);
  };

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
```

---

### Phase 3: Update Onboarding Flow ✅ **HIGH PRIORITY**

**File**: `src/app/onboarding/page.tsx`

**Changes**:

1. Initialize session on page load
2. Set learning goal via backend API
3. Store learner_id instead of full profile

```typescript
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "@/lib/hooks/useSession";
import { api } from "@/lib/api";
import { toast } from "sonner";

export default function OnboardingPage() {
  const router = useRouter();
  const { initializeSession, learnerId } = useSession();
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    goal: "",
    background: "",
    commitment: "5-10 hours/week",
  });

  const handleNext = async () => {
    if (step < 3) {
      setStep(step + 1);
    } else {
      setIsGenerating(true);
      try {
        // Step 1: Initialize session with backend (creates learner_id + workspace)
        let sessionId = learnerId;
        if (!sessionId) {
          sessionId = await initializeSession(formData.name || "Anonymous");
        }

        // Step 2: Set learning goal (backend refines it)
        await api.setLearningGoal(sessionId, formData.goal);

        // Step 3: Identify skill gaps
        const { skill_gaps } = await api.identifySkillGap(
          sessionId,
          formData.goal,
          formData.background
        );

        // Step 4: Generate learning path (backend persists to workspace)
        await api.scheduleLearningPath(sessionId, 12);

        toast.success("Learning path generated successfully!");
        router.push("/dashboard");
      } catch (error) {
        console.error("Failed to generate path:", error);
        toast.error("Failed to generate learning path. Please try again.");
      } finally {
        setIsGenerating(false);
      }
    }
  };

  // Rest of component...
}
```

---

### Phase 4: Update Dashboard with Real Data ✅ **HIGH PRIORITY**

**File**: `src/app/(app)/dashboard/page.tsx`

**Changes**:

1. Fetch dashboard data from backend
2. Display real progress, mastery, and activity
3. Remove mock data

```typescript
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "@/lib/hooks/useSession";
import { api, DashboardData } from "@/lib/api";
import { toast } from "sonner";

export default function DashboardPage() {
  const router = useRouter();
  const { learnerId, profile } = useSession();
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadDashboard = async () => {
      if (!learnerId) {
        router.push('/onboarding');
        return;
      }

      try {
        const data = await api.getDashboard(learnerId);
        setDashboard(data);
      } catch (error) {
        console.error('Failed to load dashboard:', error);
        toast.error('Failed to load dashboard');
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboard();
  }, [learnerId, router]);

  if (isLoading) {
    return <div>Loading dashboard...</div>;
  }

  if (!dashboard) {
    return <div>No data available</div>;
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold">Welcome back, {profile?.name || 'Learner'}</h1>

      {/* Display real progress */}
      <div className="grid grid-cols-4 gap-6">
        <div className="bg-card p-6 rounded-2xl">
          <p className="text-sm text-muted-foreground">Goal Readiness</p>
          <p className="text-2xl font-bold">{dashboard.learner.progress}%</p>
        </div>
        <div className="bg-card p-6 rounded-2xl">
          <p className="text-sm text-muted-foreground">Sessions</p>
          <p className="text-2xl font-bold">
            {dashboard.learner.completed_sessions} / {dashboard.learner.total_sessions}
          </p>
        </div>
        {/* Display mastery data */}
        {Object.entries(dashboard.mastery).slice(0, 2).map(([skill, level]) => (
          <div key={skill} className="bg-card p-6 rounded-2xl">
            <p className="text-sm text-muted-foreground">{skill}</p>
            <p className="text-2xl font-bold">{level}%</p>
          </div>
        ))}
      </div>

      {/* Display current session */}
      {dashboard.current_session && (
        <div className="bg-primary-500 text-white p-8 rounded-2xl">
          <h2 className="text-2xl font-bold">{dashboard.current_session.topic}</h2>
          <p className="mt-2">{dashboard.current_session.duration_estimate}</p>
          <button
            onClick={() => router.push(`/session/${dashboard.current_session.session_number}`)}
            className="mt-4 bg-white text-slate-900 px-6 py-3 rounded-xl font-bold"
          >
            Start Session
          </button>
        </div>
      )}

      {/* Display recent activity */}
      <div className="bg-card p-8 rounded-2xl">
        <h3 className="text-xl font-bold mb-4">Recent Activity</h3>
        <div className="space-y-2">
          {dashboard.recent_activity.map((activity, i) => (
            <div key={i} className="flex items-center justify-between py-2 border-b">
              <span>{activity.content}</span>
              <span className="text-sm text-muted-foreground">
                {new Date(activity.timestamp).toLocaleDateString()}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

---

### Phase 5: Session Content Generation ✅ **MEDIUM PRIORITY**

**File**: `src/app/(app)/session/[id]/page.tsx`

**Goal**: Generate tailored content from backend with quizzes

```typescript
"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { useSession } from "@/lib/hooks/useSession";
import { api } from "@/lib/api";

export default function SessionPage() {
  const params = useParams();
  const router = useRouter();
  const { learnerId } = useSession();
  const [content, setContent] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [quizScore, setQuizScore] = useState<number | null>(null);

  useEffect(() => {
    const loadSession = async () => {
      if (!learnerId) return;

      try {
        // Get dashboard to find session details
        const dashboard = await api.getDashboard(learnerId);
        const sessionNumber = parseInt(params.id as string);
        const session = dashboard.learning_path?.sessions.find(
          s => s.session_number === sessionNumber
        );

        if (!session) {
          throw new Error('Session not found');
        }

        // Generate tailored content with quiz
        const { tailored_content } = await api.generateTailoredContent(
          learnerId,
          session,
          true  // with quiz
        );

        setContent(tailored_content);
      } catch (error) {
        console.error('Failed to load session:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadSession();
  }, [learnerId, params.id]);

  const handleCompleteSession = async () => {
    if (!learnerId) return;

    try {
      const sessionNumber = parseInt(params.id as string);
      await api.completeSession(learnerId, sessionNumber, quizScore || 0, 45);

      toast.success('Session completed!');
      router.push('/dashboard');
    } catch (error) {
      toast.error('Failed to complete session');
    }
  };

  // Render content, quiz, and completion button
  // ...
}
```

---

### Phase 6: Environment Configuration

**File**: `apps/frontend/.env.local`

```bash
NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1
```

---

## Implementation Priority

### 🔴 **Phase 1** (Week 1) - Critical Foundation
- [ ] Update `src/lib/api.ts` with all new endpoints
- [ ] Create `useSession` hook for learner_id management
- [ ] Update onboarding flow to initialize session properly

### 🟡 **Phase 2** (Week 2) - Core Features
- [ ] Refactor dashboard to use real backend data
- [ ] Implement session completion tracking
- [ ] Add skill gap visualization with backend data

### 🟢 **Phase 3** (Week 3) - Enhanced Features
- [ ] Implement content generation for sessions
- [ ] Add quiz functionality
- [ ] Implement chat with tutor using backend

### 🔵 **Phase 4** (Week 4) - Polish
- [ ] Add error boundaries and loading states
- [ ] Implement proper TypeScript types
- [ ] Add E2E tests for complete flow

---

## Testing Checklist

### Manual Testing Flow

1. **Landing Page → Onboarding**
   - [ ] Click "Start Learning Locally"
   - [ ] Complete 3-step onboarding
   - [ ] Verify backend creates learner_id
   - [ ] Check workspace memory created at `~/.gen-mentor/workspace/learner_xxx/`

2. **Dashboard**
   - [ ] Verify real progress displayed
   - [ ] Check mastery levels match backend
   - [ ] Verify recent activity logs
   - [ ] Check current session from learning path

3. **Learning Path**
   - [ ] Verify sessions loaded from backend
   - [ ] Check session status (completed/in-progress/locked)
   - [ ] Verify session count matches backend

4. **Session Learning**
   - [ ] Generate tailored content
   - [ ] Complete quiz
   - [ ] Mark session complete
   - [ ] Verify progress updates in dashboard

5. **Persistence**
   - [ ] Close browser
   - [ ] Reopen app
   - [ ] Verify learner_id restored
   - [ ] Verify all data intact from backend memory

---

## Data Flow Diagram (New)

```
┌─────────────────┐
│  Landing Page   │
└────────┬────────┘
         │ Click "Start Learning Locally"
         ▼
┌─────────────────┐
│   Onboarding    │─────► POST /profile/initialize-session
│   (3 steps)     │       (Backend creates learner_id + workspace)
└────────┬────────┘
         │ Set goal, background
         ▼
         POST /profile/{id}/set-goal
         POST /skills/identify-skill-gap-with-info
         POST /schedule-learning-path
         │
         ▼
┌─────────────────┐
│    Dashboard    │◄────── GET /dashboard/{learner_id}
└────────┬────────┘        (All data from backend memory)
         │
         ▼
┌─────────────────┐
│ Session Detail  │◄────── POST /learning/tailor-knowledge-content
│  (with quiz)    │        (Content generated from backend)
└────────┬────────┘
         │ Complete
         ▼
         POST /progress/{id}/session-complete
         │
         ▼
      Dashboard (updated progress)
```

---

## Benefits of This Refactoring

1. **True Local Mode**: Backend memory stores all data in `~/.gen-mentor/workspace/`
2. **Persistence**: Data survives browser close/restart
3. **Consistency**: Single source of truth (backend memory)
4. **Offline Support**: Can run fully offline with local LLMs
5. **Progress Tracking**: Real mastery and progress tracking
6. **Quiz System**: Proper assessment with backend-generated quizzes
7. **AI Context**: Backend has full context for personalized responses

---

## Next Steps

1. Start with Phase 1 (API layer update)
2. Test each phase thoroughly before moving to next
3. Keep old localStorage as fallback during migration
4. Add error handling for offline scenarios
5. Document API changes for other developers
