"use client";

import { Target, TrendingUp, Play, Star, Zap, Trophy, CheckCircle2, Activity } from "lucide-react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { useGoal } from "@/components/GoalContext";

export default function ProgressPage() {
  const router = useRouter();
  const { currentGoal, goals, setCurrentGoalIndex } = useGoal();

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Welcome back, Alex</h1>
          <div className="flex items-center gap-3 mt-2">
            <div className="flex items-center gap-1.5 bg-orange-500/10 text-orange-600 dark:text-orange-400 px-3 py-1 rounded-full text-sm font-bold border border-orange-500/20">
              <Zap size={14} fill="currentColor" />
              3 Day Streak
            </div>
            <div className="flex items-center gap-1.5 bg-primary-500/10 text-primary-600 dark:text-primary-400 px-3 py-1 rounded-full text-sm font-bold border border-primary-500/20">
              <Star size={14} fill="currentColor" />
              Level 12
            </div>
          </div>
        </div>
        <div className="flex items-center gap-4">
          {/* Removed top right XP display to avoid duplication with sidebar */}
        </div>
      </div>

      {/* Top Stats */}
      <AnimatePresence mode="wait">
        <motion.div
          key={currentGoal.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
          className="space-y-8"
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {[
              { label: "Goal Readiness", value: `${currentGoal.readiness}%`, icon: Target, color: "text-primary-500", bg: "bg-primary-50 dark:bg-primary-950/30" },
              { label: "Sessions Done", value: "12", icon: Play, color: "text-blue-600 dark:text-blue-400", bg: "bg-blue-50 dark:bg-blue-950/30" },
              { label: "Current Streak", value: "3 Days", icon: TrendingUp, color: "text-orange-600 dark:text-orange-400", bg: "bg-orange-50 dark:bg-orange-950/30" },
              { label: "Badges", value: "8", icon: Trophy, color: "text-purple-600 dark:text-purple-400", bg: "bg-purple-50 dark:bg-purple-950/30" },
            ].map((stat, i) => (
              <motion.div 
                key={i} 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="bg-card p-6 rounded-[2rem] shadow-sm border border-border flex items-center gap-4 hover:border-primary-500/20 transition-colors group"
              >
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${stat.bg} ${stat.color} group-hover:scale-110 transition-transform`}>
                  <stat.icon size={24} />
                </div>
                <div>
                  <p className="text-xs font-bold text-muted-foreground uppercase tracking-wider">{stat.label}</p>
                  <p className="text-2xl font-black text-foreground">{stat.value}</p>
                </div>
              </motion.div>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-8">
              {/* Daily Quests */}
              <div className="bg-card rounded-[2rem] shadow-sm border border-border p-8">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-foreground">Daily Quests</h3>
                  <span className="text-sm font-bold text-primary-500">2/3 Completed</span>
                </div>
                <div className="space-y-4">
                  {[
                    { task: "Complete 1 session", xp: "+500 XP", done: true },
                    { task: "Pass a quiz with 100%", xp: "+800 XP", done: true },
                    { task: "Ask AI Tutor 3 questions", xp: "+300 XP", done: false },
                  ].map((quest, i) => (
                    <div key={i} className={`flex items-center justify-between p-4 rounded-2xl border ${quest.done ? 'bg-muted/30 border-border opacity-60' : 'bg-background border-border hover:border-primary-500/30 transition-colors'}`}>
                      <div className="flex items-center gap-4">
                        <div className={`w-6 h-6 rounded-full flex items-center justify-center ${quest.done ? 'bg-green-500 text-white' : 'border-2 border-border text-transparent'}`}>
                          <CheckCircle2 size={14} />
                        </div>
                        <span className={`font-bold ${quest.done ? 'text-muted-foreground line-through' : 'text-foreground'}`}>{quest.task}</span>
                      </div>
                      <span className={`text-sm font-black ${quest.done ? 'text-muted-foreground' : 'text-primary-500'}`}>{quest.xp}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Next Best Action */}
              <div className="bg-gradient-to-br from-primary-600 to-blue-700 rounded-[2rem] p-8 md:p-10 text-white shadow-xl relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-96 h-96 bg-white opacity-10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/4 group-hover:scale-125 transition-transform duration-700" />
                <div className="relative z-10 flex flex-col md:flex-row gap-8 items-center justify-between">
                  <div className="flex-1">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/20 text-xs font-bold mb-4">
                      <Star size={12} fill="currentColor" />
                      Double XP Active
                    </div>
                    <h2 className="text-3xl md:text-4xl font-black mb-3">Variables and Data Types</h2>
                    <p className="text-primary-100 mb-8 max-w-md font-medium text-lg">
                      Continue your Python Fundamentals module. Complete this to reach Level 13!
                    </p>
                    <button
                      onClick={() => router.push("/session/2")}
                      className="bg-white text-slate-900 px-8 py-4 rounded-2xl font-black hover:bg-slate-100 transition-all flex items-center gap-3 active:scale-95 shadow-lg text-lg"
                    >
                      <Play size={20} fill="currentColor" />
                      Start Session
                    </button>
                  </div>
                  <div className="w-full md:w-1/3 aspect-square bg-white/10 rounded-2xl border border-white/20 backdrop-blur-sm p-6 flex flex-col justify-between relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent" />
                    <div className="relative z-10">
                      <div className="text-primary-100 text-sm font-bold uppercase tracking-wider mb-1">Session 2</div>
                      <div className="text-white font-medium">Python Fundamentals</div>
                    </div>
                    <div className="relative z-10 bg-black/20 rounded-xl p-4 font-mono text-xs text-primary-100">
                      <div className="text-green-400"># Goal</div>
                      <div>age = 25</div>
                      <div>name = &quot;Alex&quot;</div>
                      <div className="mt-2 text-blue-300">print(name)</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Sidebar Content */}
            <div className="space-y-8">
              {/* My Goals Arena */}
              <div className="bg-card rounded-[2rem] shadow-sm border border-border p-8">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-foreground flex items-center gap-2">
                    <Target size={20} className="text-primary-500" />
                    My Goals Arena
                  </h3>
                </div>
                <div className="space-y-4">
                  {goals.map((goal, idx) => (
                    <button
                      key={goal.id}
                      onClick={() => setCurrentGoalIndex(idx)}
                      className={`w-full text-left p-4 rounded-2xl border transition-all ${
                        currentGoal.id === goal.id
                          ? "bg-primary-50 dark:bg-primary-900/20 border-primary-500/50 ring-1 ring-primary-500/20"
                          : "bg-background border-border hover:border-primary-500/30"
                      }`}
                    >
                      <div className="flex justify-between items-center mb-3">
                        <span className="font-bold text-sm text-foreground">{goal.title}</span>
                        {currentGoal.id === goal.id && (
                          <span className="text-[10px] font-bold text-primary-600 bg-primary-100 dark:bg-primary-900/50 px-2 py-0.5 rounded-full">Active</span>
                        )}
                      </div>
                      <div className="space-y-2">
                        <div>
                          <div className="flex justify-between text-[10px] font-bold text-muted-foreground uppercase tracking-wider mb-1">
                            <span>Readiness</span>
                            <span className="text-primary-500">{goal.readiness}%</span>
                          </div>
                          <div className="h-1.5 w-full bg-secondary rounded-full overflow-hidden">
                            <div className="h-full bg-primary-500 rounded-full" style={{ width: `${goal.readiness}%` }} />
                          </div>
                        </div>
                        <div>
                          <div className="flex justify-between text-[10px] font-bold text-muted-foreground uppercase tracking-wider mb-1">
                            <span>Skill Gap</span>
                            <span className="text-amber-500">{goal.skillGap}%</span>
                          </div>
                          <div className="h-1.5 w-full bg-secondary rounded-full overflow-hidden">
                            <div className="h-full bg-amber-500 rounded-full" style={{ width: `${goal.skillGap}%` }} />
                          </div>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Recent Badges */}
              <div className="bg-card rounded-[2rem] shadow-sm border border-border p-8">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-foreground">Recent Badges</h3>
                  <button className="text-sm font-bold text-primary-500 hover:text-primary-600">View All</button>
                </div>
                <div className="grid grid-cols-3 gap-4">
                  {[
                    { name: "Fast Learner", icon: Zap, color: "text-orange-500", bg: "bg-orange-500/10" },
                    { name: "Perfect Score", icon: Star, color: "text-yellow-500", bg: "bg-yellow-500/10" },
                    { name: "Night Owl", icon: Trophy, color: "text-purple-500", bg: "bg-purple-500/10" },
                  ].map((badge, i) => (
                    <div key={i} className="flex flex-col items-center gap-2 text-center group cursor-pointer">
                      <div className={`w-14 h-14 rounded-2xl flex items-center justify-center ${badge.bg} ${badge.color} group-hover:scale-110 transition-transform`}>
                        <badge.icon size={24} />
                      </div>
                      <span className="text-xs font-bold text-muted-foreground">{badge.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
