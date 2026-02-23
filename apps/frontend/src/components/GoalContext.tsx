"use client";

/* eslint-disable @typescript-eslint/no-explicit-any */
import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
} from "react";
import { api, getStoredLearnerId, clearStoredLearnerId } from "@/lib/api";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface Goal {
  id: number;
  goal_id: string;
  title: string;
  progress: number;
  color: string;
  readiness: number;
  skillGap: number;
  refined_goal?: any;
  status?: string;
}

export interface LearnerData {
  learnerId: string | null;
  profile: Record<string, any>;
  learningGoals: Record<string, any>;
  skillGaps: Record<string, any>;
  learningPath: Record<string, any>;
  mastery: Record<string, any>;
}

interface GoalContextType {
  /** Parsed goal list derived from backend data */
  goals: Goal[];
  currentGoalIndex: number;
  setCurrentGoalIndex: (index: number) => void;
  currentGoal: Goal;

  /** Full cached backend data */
  learner: LearnerData;
  isLoading: boolean;

  /** Re-fetch from backend */
  refresh: () => Promise<void>;

  /** Clear learner state and localStorage (logout) */
  resetLearner: () => void;
}

// ---------------------------------------------------------------------------
// Color palette for goals
// ---------------------------------------------------------------------------

const GOAL_COLORS = [
  "from-blue-500 to-cyan-400",
  "from-purple-500 to-pink-400",
  "from-amber-500 to-orange-400",
  "from-green-500 to-emerald-400",
  "from-rose-500 to-red-400",
];

// ---------------------------------------------------------------------------
// Default / empty state
// ---------------------------------------------------------------------------

const EMPTY_LEARNER: LearnerData = {
  learnerId: null,
  profile: {},
  learningGoals: {},
  skillGaps: {},
  learningPath: {},
  mastery: {},
};

const FALLBACK_GOAL: Goal = {
  id: 0,
  goal_id: "",
  title: "Set a learning goal",
  progress: 0,
  color: GOAL_COLORS[0],
  readiness: 0,
  skillGap: 0,
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function buildGoals(learningGoals: Record<string, any>, learningPath: Record<string, any>): Goal[] {
  const goalsArr: any[] = learningGoals.goals || [];
  if (goalsArr.length === 0) return [FALLBACK_GOAL];

  return goalsArr.map((g: any, idx: number) => {
    const goalId = g.goal_id || "";
    // Compute progress from learning path sessions
    const pathData = learningPath[goalId];
    let progress = 0;
    if (pathData) {
      const raw = pathData.learning_path;
      const sessions: any[] = Array.isArray(raw) ? raw : (Array.isArray(raw?.learning_path) ? raw.learning_path : []);
      if (sessions.length > 0) {
        const completed = sessions.filter((s: any) => s.completed || s.if_learned).length;
        progress = Math.round((completed / sessions.length) * 100);
      }
    }

    return {
      id: idx + 1,
      goal_id: goalId,
      title: g.learning_goal || "Untitled goal",
      progress,
      color: GOAL_COLORS[idx % GOAL_COLORS.length],
      readiness: progress,
      skillGap: Math.max(0, 100 - progress),
      refined_goal: g.refined_goal,
      status: g.status,
    };
  });
}

// ---------------------------------------------------------------------------
// Context
// ---------------------------------------------------------------------------

const GoalContext = createContext<GoalContextType | undefined>(undefined);

export function GoalProvider({ children }: { children: ReactNode }) {
  const [learner, setLearner] = useState<LearnerData>(EMPTY_LEARNER);
  const [goals, setGoals] = useState<Goal[]>([FALLBACK_GOAL]);
  const [currentGoalIndex, setCurrentGoalIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  const refresh = useCallback(async () => {
    const learnerId = getStoredLearnerId();
    if (!learnerId) return;

    setIsLoading(true);
    try {
      const data = await api.getLearnerMemory(learnerId);

      const newLearner: LearnerData = {
        learnerId,
        profile: data.profile || {},
        learningGoals: data.learning_goals || {},
        skillGaps: data.skill_gaps || {},
        learningPath: data.learning_path || {},
        mastery: data.mastery || {},
      };
      setLearner(newLearner);

      const newGoals = buildGoals(newLearner.learningGoals, newLearner.learningPath);
      setGoals(newGoals);

      // Set active goal index based on backend active_goal_id
      const activeGoalId = newLearner.learningGoals.active_goal_id;
      if (activeGoalId) {
        const idx = newGoals.findIndex((g) => g.goal_id === activeGoalId);
        if (idx >= 0) setCurrentGoalIndex(idx);
      }
    } catch (err) {
      console.error("[LearnerContext] Failed to fetch learner data:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Auto-fetch on mount if learner_id exists
  useEffect(() => {
    refresh();
  }, [refresh]);

  const currentGoal = goals[currentGoalIndex] || FALLBACK_GOAL;

  const resetLearner = useCallback(() => {
    clearStoredLearnerId();
    setLearner(EMPTY_LEARNER);
    setGoals([FALLBACK_GOAL]);
    setCurrentGoalIndex(0);
  }, []);

  return (
    <GoalContext.Provider
      value={{
        goals,
        currentGoalIndex,
        setCurrentGoalIndex,
        currentGoal,
        learner,
        isLoading,
        refresh,
        resetLearner,
      }}
    >
      {children}
    </GoalContext.Provider>
  );
}

export function useGoal() {
  const context = useContext(GoalContext);
  if (context === undefined) {
    throw new Error("useGoal must be used within a GoalProvider");
  }
  return context;
}
