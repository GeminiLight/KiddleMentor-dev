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
  Activity,
  Settings,
  Target,
  ChevronLeft,
  ChevronRight,
  Trophy,
  Star
} from "lucide-react";

const navItems = [
  { name: "Home", href: "/progress", icon: Home },
  { name: "Roadmap", href: "/learning-path", icon: Map },
  { name: "Library", href: "/library", icon: BookOpen },
  { name: "Skills", href: "/skill-gap", icon: Activity },
  { name: "Settings", href: "/profile", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const [currentGoalIndex, setCurrentGoalIndex] = useState(0);
  const [direction, setDirection] = useState(0);

  const goals = [
    { id: 1, title: "Senior Data Analyst", progress: 45, color: "from-blue-500 to-cyan-400" },
    { id: 2, title: "AI Product Manager", progress: 12, color: "from-purple-500 to-pink-400" },
    { id: 3, title: "Full Stack Developer", progress: 88, color: "from-amber-500 to-orange-400" },
  ];

  const handleNextGoal = () => {
    setDirection(1);
    setCurrentGoalIndex((prev) => (prev + 1) % goals.length);
  };

  const handlePrevGoal = () => {
    setDirection(-1);
    setCurrentGoalIndex((prev) => (prev - 1 + goals.length) % goals.length);
  };

  const variants = {
    enter: (direction: number) => ({
      x: direction > 0 ? 50 : -50,
      opacity: 0,
      scale: 0.95,
    }),
    center: {
      x: 0,
      opacity: 1,
      scale: 1,
      transition: { duration: 0.3, type: "spring", bounce: 0.4 }
    },
    exit: (direction: number) => ({
      x: direction < 0 ? 50 : -50,
      opacity: 0,
      scale: 0.95,
      transition: { duration: 0.2 }
    })
  };

  return (
    <div className="flex h-full w-64 flex-col border-r border-border bg-card px-4 py-6">
      {/* Goal Switcher (Card Stack) */}
      <div className="mb-8 relative">
        <div className="flex items-center justify-between mb-3 px-1">
          <h3 className="text-xs font-bold text-muted-foreground uppercase tracking-wider flex items-center gap-1.5">
            <Target size={14} />
            Active Goal
          </h3>
          <div className="flex items-center gap-1">
            <button onClick={handlePrevGoal} className="p-1 hover:bg-muted rounded-md text-muted-foreground transition-colors">
              <ChevronLeft size={14} />
            </button>
            <span className="text-[10px] font-medium text-muted-foreground">{currentGoalIndex + 1}/{goals.length}</span>
            <button onClick={handleNextGoal} className="p-1 hover:bg-muted rounded-md text-muted-foreground transition-colors">
              <ChevronRight size={14} />
            </button>
          </div>
        </div>

        <div className="relative h-24 w-full perspective-1000">
          <AnimatePresence initial={false} custom={direction} mode="popLayout">
            <motion.div
              key={currentGoalIndex}
              custom={direction}
              variants={variants}
              initial="enter"
              animate="center"
              exit="exit"
              className={`absolute inset-0 rounded-xl p-4 text-white shadow-md bg-gradient-to-br ${goals[currentGoalIndex].color} flex flex-col justify-between overflow-hidden`}
            >
              <div className="absolute -right-4 -top-4 w-16 h-16 bg-white/20 rounded-full blur-xl pointer-events-none" />
              <h4 className="font-semibold text-sm leading-tight line-clamp-2 relative z-10">
                {goals[currentGoalIndex].title}
              </h4>
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
            </motion.div>
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
        <Link
          href="/goals"
          className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
        >
          <Target size={18} className="text-muted-foreground" />
          Manage My Goals
        </Link>

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
