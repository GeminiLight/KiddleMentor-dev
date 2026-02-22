"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";

export interface Goal {
  id: number;
  title: string;
  progress: number;
  color: string;
  readiness: number;
  skillGap: number;
}

interface GoalContextType {
  goals: Goal[];
  currentGoalIndex: number;
  setCurrentGoalIndex: (index: number) => void;
  currentGoal: Goal;
}

const defaultGoals: Goal[] = [
  { id: 1, title: "Senior Data Analyst", progress: 45, color: "from-blue-500 to-cyan-400", readiness: 45, skillGap: 55 },
  { id: 2, title: "AI Product Manager", progress: 12, color: "from-purple-500 to-pink-400", readiness: 12, skillGap: 88 },
  { id: 3, title: "Full Stack Developer", progress: 88, color: "from-amber-500 to-orange-400", readiness: 88, skillGap: 12 },
];

const GoalContext = createContext<GoalContextType | undefined>(undefined);

export function GoalProvider({ children }: { children: ReactNode }) {
  const [currentGoalIndex, setCurrentGoalIndex] = useState(0);

  return (
    <GoalContext.Provider
      value={{
        goals: defaultGoals,
        currentGoalIndex,
        setCurrentGoalIndex,
        currentGoal: defaultGoals[currentGoalIndex],
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
