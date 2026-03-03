"use client";

import { Target, TrendingUp, Play, Star, Zap, Trophy, CheckCircle2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { useGoal } from "@/components/GoalContext";

/* eslint-disable @typescript-eslint/no-explicit-any */

export default function ProgressPage() {
  const router = useRouter();
  const { currentGoal, goals, setCurrentGoalIndex, learner } = useGoal();

  const name = learner.profile?.name || "Learner";

  // Extract sessions from current goal's learning path
  const goalId = currentGoal.goal_id;
  const pathData = learner.learningPath[goalId];
  const rawSessions = pathData?.learning_path;
  const sessionsArray: Record<string, any>[] = Array.isArray(rawSessions)
    ? rawSessions
    : Array.isArray(rawSessions?.learning_path)
      ? rawSessions.learning_path
      : [];

  const totalSessions = sessionsArray.length;
  const completedSessions = sessionsArray.filter((s) => s.completed || s.if_learned).length;

  // Find the next uncompleted session for "Next Best Action"
  const nextSessionIndex = sessionsArray.findIndex((s) => !s.completed && !s.if_learned);
  const nextSession = nextSessionIndex >= 0 ? sessionsArray[nextSessionIndex] : null;
  const nextSessionNumber = nextSessionIndex >= 0 ? nextSessionIndex + 1 : null;
  const nextSessionTitle = nextSession?.session_title || nextSession?.title || "Next Session";

  // Compute XP and level from completed sessions (same formula as Sidebar)
  const totalCompleted = Object.values(learner.learningPath).reduce((acc: number, pd: unknown) => {
    const data = pd as Record<string, any> | undefined;
    const sessions = data?.learning_path;
    if (!Array.isArray(sessions)) return acc;
    return acc + sessions.filter((s: Record<string, any>) => s.completed || s.if_learned).length;
  }, 0);
  const xp = totalCompleted * 50;
  const level = Math.floor(xp / 500) + 1;

  // Compute streak: count consecutive completed sessions from the end
  let streak = 0;
  for (let i = sessionsArray.length - 1; i >= 0; i--) {
    if (sessionsArray[i].completed || sessionsArray[i].if_learned) {
      streak++;
    } else {
      break;
    }
  }
  // If there are completed sessions but not from the end, count from the first completed block
  if (streak === 0) {
    for (let i = 0; i < sessionsArray.length; i++) {
      if (sessionsArray[i].completed || sessionsArray[i].if_learned) {
        streak++;
      } else {
        break;
      }
    }
  }

  const handleStartNextSession = () => {
    if (nextSession && nextSessionNumber !== null) {
      // Store session data so the session page can use it
      localStorage.setItem("current_session", JSON.stringify(nextSession));
      localStorage.setItem("current_session_request", JSON.stringify({
        learner_id: learner.learnerId,
        learning_path: sessionsArray,
        learning_session: nextSession,
        goal_id: goalId,
      }));
      localStorage.removeItem("current_session_content");
      router.push(`/session/${nextSessionNumber}`);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Welcome back, {name}</h1>
          <div className="flex items-center gap-3 mt-2">
            {streak > 0 && (
              <div className="flex items-center gap-1.5 bg-orange-500/10 text-orange-600 dark:text-orange-400 px-3 py-1 rounded-full text-sm font-bold border border-orange-500/20">
                <Zap size={14} fill="currentColor" />
                {streak} Session Streak
              </div>
            )}
            <div className="flex items-center gap-1.5 bg-primary-500/10 text-primary-600 dark:text-primary-400 px-3 py-1 rounded-full text-sm font-bold border border-primary-500/20">
              <Star size={14} fill="currentColor" />
              Level {level}
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
              { label: "Sessions Done", value: `${completedSessions}/${totalSessions}`, icon: Play, color: "text-blue-600 dark:text-blue-400", bg: "bg-blue-50 dark:bg-blue-950/30" },
              { label: "Session Streak", value: `${streak}`, icon: TrendingUp, color: "text-orange-600 dark:text-orange-400", bg: "bg-orange-50 dark:bg-orange-950/30" },
              { label: "Total XP", value: `${xp.toLocaleString()}`, icon: Trophy, color: "text-purple-600 dark:text-purple-400", bg: "bg-purple-50 dark:bg-purple-950/30" },
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
              {/* Session Progress */}
              <div className="bg-card rounded-[2rem] shadow-sm border border-border p-8">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-foreground">Session Progress</h3>
                  <span className="text-sm font-bold text-primary-500">{completedSessions}/{totalSessions} Completed</span>
                </div>
                <div className="space-y-4">
                  {sessionsArray.slice(0, 5).map((session, i) => {
                    const isComplete = session.completed || session.if_learned;
                    const isCurrent = i === nextSessionIndex;
                    return (
                      <div key={i} className={`flex items-center justify-between p-4 rounded-2xl border ${isComplete ? 'bg-muted/30 border-border opacity-60' : isCurrent ? 'bg-primary-500/5 border-primary-500/30' : 'bg-background border-border'}`}>
                        <div className="flex items-center gap-4">
                          <div className={`w-6 h-6 rounded-full flex items-center justify-center ${isComplete ? 'bg-green-500 text-white' : isCurrent ? 'bg-primary-500 text-white' : 'border-2 border-border text-transparent'}`}>
                            {isComplete ? <CheckCircle2 size={14} /> : isCurrent ? <Play size={10} fill="currentColor" /> : <CheckCircle2 size={14} />}
                          </div>
                          <span className={`font-bold ${isComplete ? 'text-muted-foreground line-through' : 'text-foreground'}`}>
                            {session.session_title || session.title || `Session ${i + 1}`}
                          </span>
                        </div>
                        {isCurrent && (
                          <span className="text-xs font-bold text-primary-500 bg-primary-500/10 px-2 py-1 rounded-full">Up Next</span>
                        )}
                        {isComplete && (
                          <span className="text-sm font-black text-muted-foreground">+50 XP</span>
                        )}
                      </div>
                    );
                  })}
                  {totalSessions > 5 && (
                    <button
                      onClick={() => router.push("/learning-path")}
                      className="w-full text-center text-sm font-bold text-primary-500 hover:text-primary-600 py-2"
                    >
                      View all {totalSessions} sessions
                    </button>
                  )}
                </div>
              </div>

              {/* Next Best Action */}
              {nextSession ? (
                <div className="bg-gradient-to-br from-primary-600 to-blue-700 rounded-[2rem] p-8 md:p-10 text-white shadow-xl relative overflow-hidden group">
                  <div className="absolute top-0 right-0 w-96 h-96 bg-white opacity-10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/4 group-hover:scale-125 transition-transform duration-700" />
                  <div className="relative z-10 flex flex-col md:flex-row gap-8 items-center justify-between">
                    <div className="flex-1 w-full">
                      <h2 className="text-3xl md:text-4xl font-black mb-3">{nextSessionTitle}</h2>
                      <p className="text-primary-100 mb-8 max-w-md font-medium text-lg">
                        Continue your learning path. Session {nextSessionNumber} of {totalSessions}.
                      </p>
                      <div className="flex flex-col sm:flex-row items-center gap-4">
                        <button
                          onClick={handleStartNextSession}
                          className="w-full sm:w-auto relative group/btn bg-white text-primary-700 px-10 py-5 rounded-2xl font-black hover:bg-slate-50 transition-all flex items-center justify-center gap-3 active:scale-95 shadow-[0_0_40px_rgba(255,255,255,0.3)] hover:shadow-[0_0_60px_rgba(255,255,255,0.5)] text-xl overflow-hidden"
                        >
                          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary-100/50 to-transparent -translate-x-full group-hover/btn:translate-x-full transition-transform duration-1000 ease-in-out" />
                          <div className="relative flex items-center justify-center w-8 h-8 rounded-full bg-primary-100 text-primary-600 group-hover/btn:scale-110 transition-transform">
                            <Play size={16} fill="currentColor" className="ml-1" />
                          </div>
                          Start Session Now
                        </button>
                        {nextSession.estimated_duration && (
                          <span className="text-primary-200 text-sm font-bold">~{nextSession.estimated_duration}</span>
                        )}
                      </div>
                    </div>
                    <div className="hidden md:flex w-full md:w-1/3 aspect-square bg-white/10 rounded-2xl border border-white/20 backdrop-blur-sm p-6 flex-col justify-between relative overflow-hidden transform group-hover:rotate-2 transition-transform duration-500">
                      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent" />
                      <div className="relative z-10">
                        <div className="text-primary-100 text-sm font-bold uppercase tracking-wider mb-1">Session {nextSessionNumber}</div>
                        <div className="text-white font-medium">{currentGoal.title}</div>
                      </div>
                      <div className="relative z-10 bg-black/20 rounded-xl p-4 font-mono text-xs text-primary-100">
                        <div className="text-green-400"># {nextSessionTitle}</div>
                        <div>progress = {completedSessions}/{totalSessions}</div>
                        <div className="mt-2 text-blue-300">ready_to_learn()</div>
                      </div>
                    </div>
                  </div>
                </div>
              ) : completedSessions === totalSessions && totalSessions > 0 ? (
                <div className="bg-gradient-to-br from-green-600 to-emerald-700 rounded-[2rem] p-8 md:p-10 text-white shadow-xl relative overflow-hidden">
                  <div className="relative z-10 text-center py-4">
                    <CheckCircle2 size={48} className="mx-auto mb-4" />
                    <h2 className="text-3xl font-black mb-3">Goal Complete!</h2>
                    <p className="text-green-100 text-lg">You&apos;ve completed all {totalSessions} sessions for this goal.</p>
                  </div>
                </div>
              ) : null}
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

              {/* XP Summary */}
              <div className="bg-card rounded-[2rem] shadow-sm border border-border p-8">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-foreground">XP Summary</h3>
                </div>
                <div className="text-center">
                  <div className="text-4xl font-black text-foreground mb-1">{xp.toLocaleString()}</div>
                  <div className="text-sm text-muted-foreground font-medium">Total XP Earned</div>
                  <div className="mt-4 grid grid-cols-2 gap-4">
                    <div className="bg-muted/50 rounded-xl p-3">
                      <div className="text-lg font-black text-foreground">{level}</div>
                      <div className="text-xs text-muted-foreground">Level</div>
                    </div>
                    <div className="bg-muted/50 rounded-xl p-3">
                      <div className="text-lg font-black text-foreground">{totalCompleted}</div>
                      <div className="text-xs text-muted-foreground">Sessions</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
