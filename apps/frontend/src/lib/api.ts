/* eslint-disable @typescript-eslint/no-explicit-any */
// Use Next.js API proxy for client-side requests to avoid CORS issues
// The Next.js rewrites will forward /api/* to the backend at http://127.0.0.1:5000/api/v1/*
const API_BASE_URL = typeof window !== 'undefined' ? '/api' : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api/v1');

async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || response.statusText);
  }

  return response.json();
}

// ============================================================================
// Type Definitions
// ============================================================================

export interface LearnerProfile {
  learner_id: string;
  name: string;
  email?: string;
  progress_percent?: number;
  last_session_completed?: number;
  created_at: string;
  updated_at?: string;
  metadata?: Record<string, any>;
}

export interface DashboardData {
  success: boolean;
  message: string;
  learner: LearnerProfile & {
    learning_goal?: string;
    refined_goal?: any;
    progress: number;
    total_sessions: number;
    completed_sessions: number;
  };
  current_session?: {
    session_number: number;
    topic: string;
    status: string;
    duration_estimate: string;
  };
  learning_path?: {
    sessions: Array<{
      session_number: number;
      topic: string;
      completed: boolean;
      quiz_score?: number;
      duration_estimate?: string;
    }>;
  };
  recent_activity: Array<{
    type: string;
    content: string;
    timestamp: string;
  }>;
  mastery: Record<string, number>;
}

export interface BaseRequest {
  model?: string;
}

// ============================================================================
// API Methods
// ============================================================================

export const api = {
  // ------------------------------------------------------------------------
  // Session Management
  // ------------------------------------------------------------------------

  /**
   * Initialize a new learner session.
   * Creates learner_id and workspace on backend.
   */
  initializeSession: (data: { name?: string; email?: string; metadata?: Record<string, any>; cv?: File }) => {
    const formData = new FormData();
    if (data.name) formData.append('name', data.name);
    if (data.email) formData.append('email', data.email);
    if (data.metadata) formData.append('metadata', JSON.stringify(data.metadata));
    if (data.cv) formData.append('cv', data.cv);

    return fetch(`${API_BASE_URL}/profile/initialize-session`, {
      method: 'POST',
      body: formData,
    }).then(res => {
      if (!res.ok) throw new Error(res.statusText);
      return res.json();
    });
  },

  /**
   * Get learner profile by ID.
   * Retrieves profile from backend workspace memory.
   */
  getProfile: (learnerId: string) =>
    fetchApi<{ success: boolean; learner_profile: LearnerProfile }>(`/profile/get-profile`, {
      method: 'POST',
      body: JSON.stringify({ learner_id: learnerId }),
    }),

  /**
   * Set and refine learning goal for learner.
   * Backend automatically refines goal using AI.
   */
  setLearningGoal: (
    learnerId: string,
    learningGoal: string,
    model: string = 'openai/gpt-5.1'
  ) =>
    fetchApi<{
      success: boolean;
      refined_goal: any;
      rationale?: string;
    }>(`/profile/set-goal`, {
      method: 'POST',
      body: JSON.stringify({
        learner_id: learnerId,
        learning_goal: learningGoal,
        model: model,
      }),
    }),

  // ------------------------------------------------------------------------
  // Dashboard
  // ------------------------------------------------------------------------

  /**
   * Get complete dashboard state for learner.
   * Single call returns profile, progress, sessions, activity, and mastery.
   */
  getDashboard: (learnerId: string) =>
    fetchApi<DashboardData>(`/dashboard`, {
      method: 'POST',
      body: JSON.stringify({ learner_id: learnerId }),
    }),

  // ------------------------------------------------------------------------
  // Goals & Skills
  // ------------------------------------------------------------------------

  /**
   * Refine learning goal (standalone, without learner_id).
   * Used for initial goal exploration.
   */
  refineGoal: (data: { learning_goal: string; learner_information?: string } & BaseRequest) =>
    fetchApi<{
      success: boolean;
      refined_goal: any;
      rationale: string;
    }>('/goals/refine-learning-goal', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  /**
   * Identify skill gaps for learning goal.
   */
  identifySkillGap: (data: {
    learning_goal: string;
    learner_information: string;
    skill_requirements?: string;
  } & BaseRequest) =>
    fetchApi<{
      success: boolean;
      skill_requirements: any;
      skill_gaps: any;
      learning_goal: string;
    }>('/skills/identify-skill-gap', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // ------------------------------------------------------------------------
  // Learning Path
  // ------------------------------------------------------------------------

  /**
   * Schedule learning path with sessions.
   * Backend persists to workspace memory.
   */
  scheduleLearningPath: (data: {
    learner_profile: string | Record<string, any>;
    session_count: number;
  } & BaseRequest) =>
    fetchApi<{
      success: boolean;
      learning_path: any;
      session_count: number;
    }>('/learning/schedule-learning-path', {
      method: 'POST',
      body: JSON.stringify({
        ...data,
        learner_profile: typeof data.learner_profile === 'string'
          ? data.learner_profile
          : JSON.stringify(data.learner_profile),
      }),
    }),

  /**
   * Reschedule learning path based on feedback.
   */
  rescheduleLearningPath: (data: {
    learner_profile: string | Record<string, any>;
    learning_path: string | Record<string, any>;
    session_count: number;
    other_feedback?: string | Record<string, any>;
  } & BaseRequest) =>
    fetchApi<{
      success: boolean;
      learning_path: any;
      session_count: number;
    }>('/learning/reschedule-learning-path', {
      method: 'POST',
      body: JSON.stringify({
        ...data,
        learner_profile: typeof data.learner_profile === 'string'
          ? data.learner_profile
          : JSON.stringify(data.learner_profile),
        learning_path: typeof data.learning_path === 'string'
          ? data.learning_path
          : JSON.stringify(data.learning_path),
      }),
    }),

  // ------------------------------------------------------------------------
  // Content Generation
  // ------------------------------------------------------------------------

  /**
   * Explore knowledge points for a learning session.
   */
  exploreKnowledgePoints: (data: {
    learner_profile: string | Record<string, any>;
    learning_path: string | Record<string, any>;
    learning_session: string | Record<string, any>;
  } & BaseRequest) =>
    fetchApi<{
      success: boolean;
      knowledge_points: any;
    }>('/learning/explore-knowledge-points', {
      method: 'POST',
      body: JSON.stringify({
        ...data,
        learner_profile: typeof data.learner_profile === 'string' ? data.learner_profile : JSON.stringify(data.learner_profile),
        learning_path: typeof data.learning_path === 'string' ? data.learning_path : JSON.stringify(data.learning_path),
        learning_session: typeof data.learning_session === 'string' ? data.learning_session : JSON.stringify(data.learning_session),
      }),
    }),

  /**
   * Generate tailored learning content for a session.
   * Includes quiz if requested.
   */
  generateTailoredContent: (data: {
    learner_profile: string | Record<string, any>;
    learning_path: string | Record<string, any>;
    learning_session: string | Record<string, any>;
    with_quiz?: boolean;
    use_search?: boolean;
    allow_parallel?: boolean;
  } & BaseRequest) =>
    fetchApi<{
      success: boolean;
      tailored_content: any;
    }>('/learning/tailor-knowledge-content', {
      method: 'POST',
      body: JSON.stringify({
        ...data,
        learner_profile: typeof data.learner_profile === 'string' ? data.learner_profile : JSON.stringify(data.learner_profile),
        learning_path: typeof data.learning_path === 'string' ? data.learning_path : JSON.stringify(data.learning_path),
        learning_session: typeof data.learning_session === 'string' ? data.learning_session : JSON.stringify(data.learning_session),
      }),
    }),

  // ------------------------------------------------------------------------
  // Progress Tracking
  // ------------------------------------------------------------------------

  /**
   * Mark a learning session as complete.
   * Updates progress and returns next session.
   */
  completeSession: (
    learnerId: string,
    sessionNumber: number,
    quizScore?: number,
    durationMinutes?: number
  ) =>
    fetchApi<{
      success: boolean;
      message: string;
      session_number: number;
      next_session?: any;
      progress_percent: number;
    }>(`/progress/session-complete`, {
      method: 'POST',
      body: JSON.stringify({
        learner_id: learnerId,
        session_number: sessionNumber,
        quiz_score: quizScore,
        duration_minutes: durationMinutes,
      }),
    }),

  // ------------------------------------------------------------------------
  // Chat
  // ------------------------------------------------------------------------

  /**
   * Chat with AI tutor.
   * Backend uses memory context for personalized responses.
   */
  chatWithTutor: (data: {
    messages: string | Array<{ role: string; content: string }>;
    learner_profile?: string | Record<string, any>;
  } & BaseRequest) =>
    fetchApi<{ success: boolean; response: string }>('/chat/chat-with-tutor', {
      method: 'POST',
      body: JSON.stringify({
        ...data,
        messages: typeof data.messages === 'string' ? data.messages : JSON.stringify(data.messages),
        learner_profile: data.learner_profile
          ? typeof data.learner_profile === 'string'
            ? data.learner_profile
            : JSON.stringify(data.learner_profile)
          : undefined,
      }),
    }),

  // ------------------------------------------------------------------------
  // Assessment
  // ------------------------------------------------------------------------

  /**
   * Generate quizzes for learning document.
   */
  generateDocumentQuizzes: (data: {
    learning_document: string | Record<string, any>;
    quiz_count?: number;
  } & BaseRequest) =>
    fetchApi<{
      success: boolean;
      quizzes: any;
    }>('/assessment/generate-document-quizzes', {
      method: 'POST',
      body: JSON.stringify({
        ...data,
        learning_document: typeof data.learning_document === 'string'
          ? data.learning_document
          : JSON.stringify(data.learning_document),
      }),
    }),

  // ------------------------------------------------------------------------
  // Models & Config
  // ------------------------------------------------------------------------

  /**
   * List available LLM models.
   */
  listModels: () =>
    fetchApi<{ models: Array<{ model_name: string; model_provider: string }> }>('/list-llm-models'),

  /**
   * Get storage and workspace information.
   */
  getStorageInfo: () =>
    fetchApi<{
      workspace_dir: string;
      memory_available: boolean;
      learner_count: number;
    }>('/storage-info'),

  /**
   * Health check.
   */
  healthCheck: () =>
    fetchApi<{
      status: string;
      version: string;
      memory_enabled: boolean;
    }>('/health'),
};

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Helper to get learner_id from localStorage.
 */
export function getStoredLearnerId(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('gen_mentor_learner_id');
}

/**
 * Helper to set learner_id in localStorage.
 */
export function setStoredLearnerId(learnerId: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('gen_mentor_learner_id', learnerId);
}

/**
 * Helper to clear learner_id from localStorage.
 */
export function clearStoredLearnerId(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('gen_mentor_learner_id');
}
