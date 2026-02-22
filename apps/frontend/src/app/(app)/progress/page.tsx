"use client";

import { Target, TrendingUp, Play, Star, Zap, Trophy, CheckCircle2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";

export default function ProgressPage() {
  const router = useRouter();

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
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: "Goal Readiness", value: "45%", icon: Target, color: "text-primary-500", bg: "bg-primary-50 dark:bg-primary-950/30" },
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
                  Resume Learning
                </button>
              </div>
              <div className="w-full md:w-72 bg-black/20 rounded-2xl p-5 border border-white/10 backdrop-blur-sm shadow-2xl transform group-hover:-translate-y-2 transition-transform duration-500">
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500" />
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                </div>
                <pre className="text-sm font-mono text-primary-100 leading-relaxed">
                  <code>
                    <span className="text-pink-400">name</span> = <span className="text-green-400">&quot;Alex&quot;</span><br/>
                    <span className="text-pink-400">age</span> = <span className="text-purple-400">25</span><br/>
                    <span className="text-pink-400">is_student</span> = <span className="text-orange-400">True</span><br/>
                    <br/>
                    <span className="text-blue-400">print</span>(<span className="text-green-400">f&quot;Hi, I&apos;m </span>&#123;name&#125;<span className="text-green-400">&quot;</span>)
                  </code>
                </pre>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-8">
          {/* Current Goal Progress */}
          <div className="bg-card rounded-[2rem] shadow-sm border border-border p-8">
            <h3 className="text-xl font-bold text-foreground mb-6">Career Path</h3>
            <div className="space-y-6">
              <div className="relative pl-6 border-l-2 border-border space-y-8">
                {[
                  { title: "Python Basics", status: "completed", xp: "2000 XP" },
                  { title: "Advanced Data Analysis", status: "current", xp: "5000 XP" },
                  { title: "Machine Learning", status: "locked", xp: "10000 XP" },
                ].map((item, i) => (
                  <div key={i} className="relative">
                    <div className={`absolute -left-[33px] top-1 w-4 h-4 rounded-full border-2 border-card ${
                      item.status === 'completed' ? 'bg-green-500' : 
                      item.status === 'current' ? 'bg-primary-500 ring-4 ring-primary-500/20' : 'bg-muted'
                    }`} />
                    <div className="flex justify-between items-start">
                      <div>
                        <p className={`font-bold text-sm ${item.status === 'locked' ? 'text-muted-foreground' : 'text-foreground'}`}>{item.title}</p>
                        <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">{item.xp}</p>
                      </div>
                      {item.status === 'completed' && <CheckCircle2 size={14} className="text-green-500" />}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Recent Badges */}
          <div className="bg-card rounded-[2rem] shadow-sm border border-border p-8 opacity-80 hover:opacity-100 transition-opacity">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-bold text-foreground">Recent Badges</h3>
              <button className="text-xs font-bold text-primary-500 hover:text-primary-600">View All</button>
            </div>
            <div className="grid grid-cols-3 gap-4">
              {[
                { name: "Fast Learner", icon: Zap, color: "text-amber-500", bg: "bg-amber-500/10" },
                { name: "Quiz Master", icon: Trophy, color: "text-purple-500", bg: "bg-purple-500/10" },
                { name: "3-Day Streak", icon: Flame, color: "text-orange-500", bg: "bg-orange-500/10" },
              ].map((badge, i) => (
                <div key={i} className="flex flex-col items-center gap-2">
                  <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${badge.bg} ${badge.color} border border-white/10 shadow-sm`}>
                    <badge.icon size={20} />
                  </div>
                  <span className="text-[9px] font-bold text-muted-foreground text-center uppercase tracking-tighter leading-tight">{badge.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const Flame = ({ size, className }: { size: number, className?: string }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    width={size} 
    height={size} 
    viewBox="0 0 24 24" 
    fill="none" 
    stroke="currentColor" 
    strokeWidth="2" 
    strokeLinecap="round" 
    strokeLinejoin="round" 
    className={className}
  >
    <path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.206 1.146-3" />
  </svg>
);
