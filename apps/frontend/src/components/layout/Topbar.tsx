"use client";

import Link from "next/link";
import { Bell, User, BookOpen, ChevronDown, Plus } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useState } from "react";

export function Topbar() {
  const [isGoalMenuOpen, setIsGoalMenuOpen] = useState(false);
  const [currentGoal, setCurrentGoal] = useState("Senior Data Analyst");

  const goals = [
    "Senior Data Analyst",
    "Machine Learning Engineer",
    "Python Backend Developer"
  ];

  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-card px-8">
      <div className="flex items-center gap-8">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-500 text-white">
            <BookOpen size={18} strokeWidth={2.5} />
          </div>
          <span className="text-xl font-bold text-foreground tracking-tight">GenMentor</span>
        </div>

        {/* Goal Switcher */}
        <div className="relative">
          <button 
            onClick={() => setIsGoalMenuOpen(!isGoalMenuOpen)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-muted transition-colors border border-transparent hover:border-border"
          >
            <div className="flex flex-col items-start">
              <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider leading-none">Current Goal</span>
              <span className="text-sm font-medium text-foreground">{currentGoal}</span>
            </div>
            <ChevronDown size={16} className="text-muted-foreground ml-1" />
          </button>

          {isGoalMenuOpen && (
            <div className="absolute top-full left-0 mt-1 w-64 bg-card border border-border rounded-xl shadow-lg overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-200">
              <div className="p-2">
                <div className="px-2 py-1.5 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Your Goals
                </div>
                {goals.map((goal) => (
                  <button
                    key={goal}
                    onClick={() => {
                      setCurrentGoal(goal);
                      setIsGoalMenuOpen(false);
                    }}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      currentGoal === goal 
                        ? "bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400" 
                        : "text-foreground hover:bg-muted"
                    }`}
                  >
                    {goal}
                  </button>
                ))}
              </div>
              <div className="border-t border-border p-2">
                <Link
                  href="/goals"
                  onClick={() => setIsGoalMenuOpen(false)}
                  className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
                >
                  <Plus size={16} />
                  Add New Goal
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="flex items-center gap-4">
        <ThemeToggle />
        <button className="relative rounded-full p-2 text-muted-foreground hover:bg-muted transition-colors">
          <Bell size={18} />
          <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-red-500 ring-2 ring-card" />
        </button>
        <Link 
          href="/profile"
          className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400 hover:bg-primary-200 dark:hover:bg-primary-900/80 transition-colors"
        >
          <User size={18} />
        </Link>
      </div>
    </header>
  );
}
