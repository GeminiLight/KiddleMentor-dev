"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import {
  Home,
  Map,
  BookOpen,
  Settings,
  Target,
  ChevronLeft,
  ChevronRight,
  Trophy,
  Star
} from "lucide-react";

import { useGoal } from "@/components/GoalContext";

const navItems = [
  { name: "Home", href: "/progress", icon: Home },
  { name: "Roadmap", href: "/learning-path", icon: Map },
  { name: "Library", href: "/library", icon: BookOpen },
  { name: "Settings", href: "/profile", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const { goals, currentGoalIndex, setCurrentGoalIndex } = useGoal();
  const [isGoalListOpen, setIsGoalListOpen] = useState(false);

  return (
    <div className="flex h-full w-64 flex-col border-r border-border bg-card px-4 py-6">
      {/* Goal Switcher (Dropdown/Accordion) */}
      <div className="mb-8 relative">
        <h3 className="text-xs font-bold text-muted-foreground uppercase tracking-wider flex items-center gap-1.5 mb-3 px-1">
          <Target size={14} />
          Active Goal
        </h3>

        <div className="relative">
          {/* Current Goal Card (Clickable) */}
          <button 
            onClick={() => setIsGoalListOpen(!isGoalListOpen)}
            className={`w-full text-left rounded-xl p-4 text-white shadow-md bg-gradient-to-br ${goals[currentGoalIndex].color} flex flex-col justify-between overflow-hidden relative transition-transform active:scale-95`}
          >
            <div className="absolute -right-4 -top-4 w-16 h-16 bg-white/20 rounded-full blur-xl pointer-events-none" />
            <div className="flex justify-between items-start mb-2 relative z-10">
              <h4 className="font-semibold text-sm leading-tight line-clamp-2 pr-4">
                {goals[currentGoalIndex].title}
              </h4>
              <ChevronRight size={16} className={cn("transition-transform", isGoalListOpen ? "rotate-90" : "")} />
            </div>
            <div className="relative z-10">
              <div className="flex items-center justify-between text-xs font-medium mb-1.5 text-white/90">
                <span>Progress</span>
                <span>{goals[currentGoalIndex].progress}%</span>
              </div>
              <div className="h-1.5 w-full bg-black/20 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-white rounded-full transition-all duration-1000 ease-out"
                  style={{ width: `${goals[currentGoalIndex].progress}%` }}
                />
              </div>
            </div>
          </button>

          {/* Goal List Dropdown */}
          <AnimatePresence>
            {isGoalListOpen && (
              <motion.div
                initial={{ opacity: 0, y: -10, height: 0 }}
                animate={{ opacity: 1, y: 0, height: "auto" }}
                exit={{ opacity: 0, y: -10, height: 0 }}
                className="absolute top-full left-0 right-0 mt-2 bg-card border border-border rounded-xl shadow-lg overflow-hidden z-50"
              >
                <div className="p-2 space-y-1">
                  {goals.map((goal, idx) => (
                    <button
                      key={goal.id}
                      onClick={() => {
                        setCurrentGoalIndex(idx);
                        setIsGoalListOpen(false);
                      }}
                      className={cn(
                        "w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center justify-between",
                        idx === currentGoalIndex 
                          ? "bg-primary-50 dark:bg-primary-900/20 text-primary-600" 
                          : "hover:bg-muted text-foreground"
                      )}
                    >
                      <span className="truncate pr-2">{goal.title}</span>
                      <span className="text-xs text-muted-foreground">{goal.progress}%</span>
                    </button>
                  ))}
                </div>
                <div className="p-2 border-t border-border bg-muted/30">
                  <Link
                    href="/goals"
                    className="w-full flex items-center justify-center gap-2 py-2 text-xs font-semibold text-primary-600 hover:text-primary-700 transition-colors"
                  >
                    <Target size={14} />
                    + Add or Manage Goals
                  </Link>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      <nav className="flex flex-1 flex-col gap-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary-50 dark:bg-primary-950/30 text-primary-700 dark:text-primary-400"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <item.icon 
                size={18} 
                className={cn(
                  isActive ? "text-primary-600" : "text-muted-foreground"
                )} 
              />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto space-y-4">
        {/* Global XP Progress Bar */}
        <div className="rounded-xl bg-gradient-to-b from-muted/50 to-muted p-4 border border-border relative overflow-hidden group">
          <div className="absolute -right-6 -top-6 w-24 h-24 bg-amber-500/10 rounded-full blur-2xl pointer-events-none group-hover:bg-amber-500/20 transition-colors" />
          
          <div className="flex items-center justify-between mb-3 relative z-10">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-amber-500/10 text-amber-600 dark:text-amber-400 rounded-lg">
                <Trophy size={16} />
              </div>
              <div>
                <h4 className="text-xs font-bold text-foreground uppercase tracking-wider">Level 4</h4>
                <p className="text-[10px] font-medium text-muted-foreground">AI Apprentice</p>
              </div>
            </div>
            <div className="text-right">
              <span className="text-xs font-bold text-amber-600 dark:text-amber-400">1,250 XP</span>
              <p className="text-[10px] text-muted-foreground">/ 2,000 XP</p>
            </div>
          </div>

          <div className="relative z-10">
            <div className="h-2 w-full bg-background rounded-full overflow-hidden border border-border/50">
              <div 
                className="h-full bg-gradient-to-r from-amber-400 to-orange-500 rounded-full relative overflow-hidden"
                style={{ width: "62.5%" }}
              >
                <div className="absolute inset-0 bg-[url('/noise.png')] opacity-20 mix-blend-overlay" />
                <div className="absolute right-0 top-0 bottom-0 w-4 bg-gradient-to-l from-white/40 to-transparent" />
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full animate-[shimmer_2s_infinite]" />
              </div>
            </div>
            <div className="mt-2 flex items-center justify-between text-[10px] font-medium text-muted-foreground">
              <span className="flex items-center gap-1"><Star size={10} className="text-amber-500" /> Next: Agent Architect</span>
              <span>750 XP left</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
