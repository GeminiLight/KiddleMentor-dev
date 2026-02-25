"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Play, CheckCircle2, Clock, Calendar, MoreVertical, Lock, RefreshCw, Award, Sparkles, X, Check, Target, AlertCircle, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { useGoal } from "@/components/GoalContext";
import { api, getStoredLearnerId } from "@/lib/api";
import { toast } from "sonner";

export default function LearningPathPage() {
  const router = useRouter();
  const { currentGoal, learner, refresh } = useGoal();
  const [sessions, setSessions] = useState<Record<string, unknown>[]>([]);
  const [isRescheduling, setIsRescheduling] = useState(false);
  const [hasPendingChanges, setHasPendingChanges] = useState(false);
  const [originalSessions, setOriginalSessions] = useState<Record<string, unknown>[]>([]);
  const [activeTooltip, setActiveTooltip] = useState<string | number | null>(null);
  const [skills, setSkills] = useState<Record<string, unknown>[]>([]);
  const [showSkillGap, setShowSkillGap] = useState(false);
  const [generatingSessionId, setGeneratingSessionId] = useState<number | null>(null);
  const [rescheduledRawPath, setRescheduledRawPath] = useState<Record<string, unknown> | null>(null);

  // Close tooltip when clicking outside
  useEffect(() => {
    const handleClickOutside = () => setActiveTooltip(null);
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, []);

  // Helper: extract session array from potentially double-nested learning_path
  const extractSessions = (raw: unknown): Record<string, unknown>[] => {
    if (Array.isArray(raw)) return raw;
    if (raw && typeof raw === "object" && Array.isArray((raw as Record<string, unknown>).learning_path))
      return (raw as Record<string, unknown>).learning_path as Record<string, unknown>[];
    return [];
  };

  // Helper: map raw sessions to UI format, marking new ones if oldIds is provided
  const mapSessions = (
    pathSessions: Record<string, unknown>[],
    oldIds?: Set<string>
  ): Record<string, unknown>[] =>
    pathSessions.map((s: Record<string, unknown>, idx: number) => ({
      id: idx + 1,
      title: s.session_title || s.title || `Session ${idx + 1}`,
      description: s.abstract || "",
      duration: s.estimated_duration || "45 min",
      status: (s.completed || s.if_learned)
        ? "completed"
        : (idx === 0 || (idx > 0 && (pathSessions[idx - 1]?.completed || pathSessions[idx - 1]?.if_learned)))
          ? "in-progress"
          : "locked",
      week: Math.floor(idx / 3) + 1,
      isMilestone: (idx + 1) % 3 === 0,
      skills: s.associated_skills || [],
      isNew: oldIds ? !oldIds.has(String(s.id || s.title || idx)) : false,
      data: s,
    }));

  // Load learning path and skill gaps from context
  useEffect(() => {
    const goalId = currentGoal.goal_id;

    const pathData = learner.learningPath[goalId];
    const pathSessions = extractSessions(pathData?.learning_path);

    if (pathSessions.length > 0) {
      setSessions(mapSessions(pathSessions));
    } else {
      setSessions([
        { id: 1, title: "Introduction to Python Syntax", duration: "45 min", status: "completed", week: 1, isMilestone: false },
        { id: 2, title: "Variables and Data Types", duration: "60 min", status: "in-progress", week: 1, isMilestone: false },
        { id: 3, title: "Control Flow (If/Else)", duration: "45 min", status: "locked", week: 1, isMilestone: true },
      ]);
    }

    // Skill gaps — handle double-nested structure and array format
    const skillGapRaw = learner.skillGaps[goalId]?.skill_gaps;
    const skillGapArr: Record<string, unknown>[] = Array.isArray(skillGapRaw)
      ? skillGapRaw
      : Array.isArray(skillGapRaw?.skill_gaps)
        ? skillGapRaw.skill_gaps
        : [];

    // Convert level strings to numeric percentages
    const levelToNumber = (level: unknown): number => {
      const map: Record<string, number> = { unlearned: 0, beginner: 25, intermediate: 50, advanced: 75, expert: 100 };
      return map[String(level).toLowerCase()] ?? 0;
    };

    const mappedSkills = skillGapArr
      .filter((gap: Record<string, unknown>) => gap.is_gap !== false)
      .map((gap: Record<string, unknown>) => ({
        name: gap.name as string || "Unknown Skill",
        current: levelToNumber(gap.current_level),
        target: levelToNumber(gap.required_level),
        priority: gap.required_level === "advanced"
          ? "Critical"
          : gap.required_level === "intermediate"
            ? "Important"
            : "Normal",
        reason: gap.reason as string || "",
      }));

    setSkills(mappedSkills.length > 0 ? mappedSkills : [
      { name: "Python Fundamentals", current: 35, target: 80, priority: "Critical" },
      { name: "SQL & Databases", current: 40, target: 90, priority: "Critical" },
      { name: "Data Structures", current: 20, target: 75, priority: "Important" },
      { name: "Algorithms", current: 15, target: 70, priority: "Important" },
      { name: "System Design", current: 10, target: 60, priority: "Normal" },
    ]);
  }, [currentGoal.goal_id, learner.learningPath, learner.skillGaps]);

  const handleReschedule = async () => {
    const learnerId = getStoredLearnerId();
    if (!learnerId) return;

    setIsRescheduling(true);
    setOriginalSessions([...sessions]);

    try {
      const goalId = currentGoal.goal_id;
      const pathData = learner.learningPath[goalId];
      const currentRawPath = pathData?.learning_path;
      // Unwrap nested structure: send the sessions array, not the wrapper object
      const sessionsArray = extractSessions(currentRawPath);

      const result = await api.rescheduleLearningPath({
        learner_profile: { learner_id: learnerId },
        learning_path: sessionsArray,
        session_count: -1,
        goal_id: currentGoal.goal_id,
      });

      // Build a set of old session IDs for "isNew" detection
      const oldIds = new Set(sessions.map((s) => String(s.data && (s.data as Record<string, unknown>).id || s.data && (s.data as Record<string, unknown>).title || s.id)));
      const newRawSessions = extractSessions(result.learning_path);
      const newMapped = mapSessions(newRawSessions, oldIds);

      setRescheduledRawPath(result.learning_path as Record<string, unknown>);
      setSessions(newMapped);
      setHasPendingChanges(true);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to reschedule";
      toast.error(message);
      console.error("[Reschedule]", err);
    } finally {
      setIsRescheduling(false);
    }
  };

  const handleAccept = async () => {
    // The backend already persisted the rescheduled path during the API call.
    // Refresh context so all pages see the updated data.
    setSessions((prev) => prev.map((s) => ({ ...s, isNew: false })));
    setHasPendingChanges(false);
    setRescheduledRawPath(null);
    await refresh();
    toast.success("Learning path updated");
  };

  const handleReject = () => {
    // Revert to the original sessions locally.
    // Note: backend already persisted the new path, so we re-save the original.
    setSessions(originalSessions);
    setHasPendingChanges(false);
    setRescheduledRawPath(null);
  };

  const handleStartSession = (session: Record<string, unknown>) => {
    const learnerId = getStoredLearnerId();
    if (!learnerId) return;

    const sessionId = session.id as number;
    const goalId = currentGoal.goal_id;
    const pathData = learner.learningPath[goalId];
    const rawPath = pathData?.learning_path;
    const sessionsArray = extractSessions(rawPath);

    // Store session metadata & request params so the session page can fetch content
    localStorage.setItem("current_session", JSON.stringify(session.data));
    localStorage.setItem("current_session_request", JSON.stringify({
      learner_id: learnerId,
      learning_path: sessionsArray,
      learning_session: (session.data as Record<string, unknown>) || {},
      goal_id: goalId,
    }));
    // Clear any stale content from a previous session
    localStorage.removeItem("current_session_content");

    router.push(`/session/${sessionId}`);
  };

  const radarData = skills.map(s => ({
    subject: s.name as string,
    "Initial State S₀": Math.max(0, (s.current as number) - 15),
    "Current State Sₜ": s.current as number,
    "Target": s.target as number,
    fullMark: 100,
  }));

  const weeks = Array.from(new Set(sessions.map(s => s.week as number))).sort((a, b) => a - b);

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Your Learning Path</h1>
          <p className="mt-2 text-muted-foreground">{sessions.filter(s => s.status === 'completed').length} / {sessions.length} Sessions Complete</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowSkillGap(!showSkillGap)}
            className="flex items-center gap-2 bg-background border border-border text-muted-foreground px-4 py-2.5 rounded-full font-medium hover:bg-muted hover:text-foreground transition-colors shadow-sm"
          >
            <Target size={16} />
            {showSkillGap ? "Hide Skills" : "View Skills"}
          </button>
          {(() => {
            const nextSession = sessions.find((s) => s.status === "in-progress");
            return nextSession ? (
              <button
                onClick={() => handleStartSession(nextSession)}
                className="flex items-center gap-2 bg-primary-500 text-white px-6 py-2.5 rounded-full font-semibold hover:bg-primary-600 transition-colors shadow-sm"
              >
                <Play size={18} fill="currentColor" />
                Continue Session
              </button>
            ) : null;
          })()}
          <button
            onClick={handleReschedule}
            disabled={isRescheduling}
            className="flex items-center gap-2 bg-background border border-border text-muted-foreground px-4 py-2.5 rounded-full font-medium hover:bg-muted hover:text-foreground transition-colors disabled:opacity-50 shadow-sm"
          >
            <RefreshCw size={16} className={isRescheduling ? "animate-spin" : ""} />
            {isRescheduling ? "Adapting..." : "Reschedule"}
          </button>
        </div>
      </div>

      {/* Skill Gap Panel */}
      <AnimatePresence>
        {showSkillGap && (
          <motion.div
            initial={{ opacity: 0, height: 0, marginBottom: 0 }}
            animate={{ opacity: 1, height: "auto", marginBottom: 32 }}
            exit={{ opacity: 0, height: 0, marginBottom: 0 }}
            className="overflow-hidden"
          >
            <div className="bg-card rounded-2xl shadow-sm border border-border p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Readiness Radar Chart */}
              <div>
                <h2 className="text-xl font-bold text-foreground flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-500 flex items-center justify-center">
                    <Target size={20} />
                  </div>
                  Readiness Overview
                </h2>
                <div className="h-[300px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                      <PolarGrid stroke="var(--border)" />
                      <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--foreground)', fontSize: 12 }} />
                      <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: 'var(--muted-foreground)', fontSize: 10 }} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: 'var(--card)', borderColor: 'var(--border)', borderRadius: '0.5rem' }}
                        itemStyle={{ fontWeight: 'bold' }}
                      />
                      <Legend wrapperStyle={{ paddingTop: '20px' }} />
                      <Radar name="Initial State S₀" dataKey="Initial State S₀" stroke="#94a3b8" fill="#94a3b8" fillOpacity={0.3} />
                      <Radar name="Current State Sₜ" dataKey="Current State Sₜ" stroke="#02b899" fill="#02b899" fillOpacity={0.5} />
                      <Radar name="Target" dataKey="Target" stroke="#3b82f6" fill="transparent" strokeDasharray="5 5" strokeWidth={2} />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Skills to Learn */}
              <div className="space-y-4">
                <h2 className="text-xl font-bold text-foreground flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-primary-500/10 text-primary-500 flex items-center justify-center">
                    <AlertCircle size={20} />
                  </div>
                  Skills to Learn
                </h2>
                
                <div className="grid gap-4 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
                  {skills.filter(s => (s.current as number) < (s.target as number)).map((skill, idx) => (
                    <div key={idx} className="bg-background rounded-xl border border-border p-4">
                      <div className="flex justify-between items-start mb-3">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-sm text-foreground">{skill.name as string}</span>
                            <span
                              className={`text-[9px] px-2 py-0.5 rounded-full font-black uppercase tracking-widest ${
                                skill.priority === "Critical"
                                  ? "bg-red-500/10 text-red-500"
                                  : skill.priority === "Important"
                                  ? "bg-amber-500/10 text-amber-500"
                                  : "bg-muted text-muted-foreground"
                              }`}
                            >
                              {skill.priority as string}
                            </span>
                          </div>
                        </div>
                        <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest bg-muted px-2 py-0.5 rounded-full">Target: {skill.target as number}%</span>
                      </div>
                      
                      <div className="space-y-1.5">
                        <div className="relative h-2 w-full bg-secondary rounded-full overflow-hidden">
                          {/* Target Marker */}
                          <div
                            className="absolute top-0 bottom-0 w-0.5 bg-foreground/20 z-10"
                            style={{ left: `${skill.target as number}%` }}
                          />
                          {/* Current Progress */}
                          <div
                            className="absolute top-0 bottom-0 bg-gradient-to-r from-primary-500 to-blue-500 rounded-full transition-all duration-1000"
                            style={{ width: `${skill.current as number}%` }}
                          />
                        </div>
                        <div className="flex justify-between text-[9px] font-black uppercase tracking-widest text-muted-foreground">
                          <span>Current: {skill.current as number}%</span>
                          <span className="text-primary-500">Gap: {(skill.target as number) - (skill.current as number)}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* AI Suggestion Card */}
      <AnimatePresence mode="wait">
        {!hasPendingChanges ? (
          <motion.div 
            key="suggestion"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="bg-primary-500/5 border border-primary-500/20 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 relative overflow-hidden"
          >
            <div className="absolute -right-10 -top-10 w-40 h-40 bg-primary-500/10 rounded-full blur-3xl pointer-events-none" />
            <div className="flex items-start gap-4 relative z-10">
              <div className="bg-primary-500/10 p-2.5 rounded-xl text-primary-600 dark:text-primary-400">
                <Sparkles size={24} />
              </div>
              <div>
                <h3 className="font-semibold text-primary-700 dark:text-primary-400 text-lg">AI Path Optimization Available</h3>
                <p className="text-sm text-primary-600/80 dark:text-primary-400/80 mt-1">
                  Based on your recent progress, I can adjust your upcoming sessions to better align with your goals.
                </p>
              </div>
            </div>
            <button
              onClick={handleReschedule}
              disabled={isRescheduling}
              className="shrink-0 flex items-center gap-2 bg-primary-500 text-white px-5 py-2.5 rounded-full font-medium hover:bg-primary-600 transition-colors disabled:opacity-50 relative z-10 shadow-sm"
            >
              <RefreshCw size={18} className={isRescheduling ? "animate-spin" : ""} />
              {isRescheduling ? "Adapting..." : "Optimize Path"}
            </button>
          </motion.div>
        ) : (
          <motion.div 
            key="review"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="bg-amber-500/5 border border-amber-500/20 rounded-2xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 relative overflow-hidden"
          >
            <div className="absolute -right-10 -top-10 w-40 h-40 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />
            <div className="flex items-start gap-4 relative z-10">
              <div className="bg-amber-500/10 p-2.5 rounded-xl text-amber-600 dark:text-amber-400">
                <Sparkles size={24} />
              </div>
              <div>
                <h3 className="font-semibold text-amber-700 dark:text-amber-400 text-lg">Review Path Changes</h3>
                <p className="text-sm text-amber-600/80 dark:text-amber-400/80 mt-1">
                  I&apos;ve added new sessions to fill your skill gaps. Please review and accept the changes.
                </p>
              </div>
            </div>
            <div className="shrink-0 flex items-center gap-3 relative z-10">
              <button
                onClick={handleReject}
                className="flex items-center gap-2 bg-background border border-border text-foreground px-4 py-2.5 rounded-full font-medium hover:bg-muted transition-colors shadow-sm"
              >
                <X size={18} />
                Reject
              </button>
              <button
                onClick={handleAccept}
                className="flex items-center gap-2 bg-amber-500 text-white px-5 py-2.5 rounded-full font-medium hover:bg-amber-600 transition-colors shadow-sm"
              >
                <Check size={18} />
                Accept Changes
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="space-y-12">
        {weeks.map((week) => (
          <div key={week} className="space-y-6">
            <h2 className="text-xl font-semibold text-foreground flex items-center gap-2">
              <Calendar className="text-primary-500" size={20} />
              Week {week}
            </h2>
            
            <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent">
              <AnimatePresence>
                {sessions
                  .filter((s) => s.week === week)
                  .map((session, idx) => (
                    <motion.div
                      key={session.id as string | number}
                      initial={{ opacity: 0, y: 20, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      transition={{ duration: 0.4, delay: idx * 0.1 }}
                      className={`relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group`}
                    >
                      {/* Icon */}
                      <div
                        className={`flex items-center justify-center w-10 h-10 rounded-full border-4 border-background shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-sm z-10 ${
                          session.status === "completed"
                            ? "bg-green-500 text-white"
                            : session.status === "in-progress"
                            ? "bg-primary-500 text-white ring-4 ring-primary-500/10"
                            : session.isNew
                            ? "bg-amber-500 text-white ring-4 ring-amber-500/20 animate-pulse"
                            : "bg-muted text-muted-foreground"
                        }`}
                      >
                        {session.status === "completed" ? (
                          <CheckCircle2 size={20} />
                        ) : session.status === "in-progress" ? (
                          <Play size={16} fill="currentColor" className="ml-0.5" />
                        ) : session.isNew ? (
                          <Sparkles size={16} />
                        ) : (
                          <Lock size={16} />
                        )}
                      </div>

                      {/* Card */}
                      <div
                        className={`w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-6 rounded-2xl border shadow-sm transition-all relative overflow-hidden ${
                          session.status === "in-progress"
                            ? "bg-card border-primary-500/50 ring-1 ring-primary-500/10"
                            : session.status === "completed"
                            ? "bg-muted/30 border-border opacity-75"
                            : session.isNew
                            ? "bg-amber-500/5 border-amber-500/30 ring-1 ring-amber-500/20"
                            : "bg-card border-border opacity-50"
                        }`}
                      >
                        {Boolean(session.isMilestone) && (
                          <div className="absolute -right-6 -top-6 w-24 h-24 bg-gradient-to-br from-amber-400/20 to-orange-500/5 rounded-full blur-2xl pointer-events-none" />
                        )}
                        <div className="flex items-start justify-between mb-2 relative z-10">
                          <div className="flex items-center gap-2">
                            <h3
                              className={`font-semibold text-lg ${
                                session.status === "in-progress"
                                  ? "text-primary-600 dark:text-primary-400"
                                  : session.isNew
                                  ? "text-amber-600 dark:text-amber-400"
                                  : "text-foreground"
                              }`}
                            >
                              {session.title as string}
                            </h3>
                            {Boolean(session.isMilestone) && (
                              <span className="flex items-center gap-1 text-xs font-bold text-amber-500 bg-amber-500/10 px-2 py-0.5 rounded-full">
                                <Award size={12} />
                                Milestone
                              </span>
                            )}
                            {Boolean(session.isNew) && (
                              <div className="relative">
                                <button 
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    setActiveTooltip(activeTooltip === session.id ? null : session.id as string | number);
                                  }}
                                  className="text-xs font-bold text-amber-500 bg-amber-500/10 px-2 py-0.5 rounded-full hover:bg-amber-500/20 transition-colors cursor-pointer flex items-center gap-1"
                                >
                                  <Sparkles size={12} />
                                  Added for you
                                </button>
                                
                                <AnimatePresence>
                                  {activeTooltip === session.id && (
                                    <motion.div 
                                      initial={{ opacity: 0, y: 5, scale: 0.95 }}
                                      animate={{ opacity: 1, y: 0, scale: 1 }}
                                      exit={{ opacity: 0, y: 5, scale: 0.95 }}
                                      className="absolute left-0 top-full mt-2 w-64 p-3 bg-popover border border-border rounded-xl shadow-lg z-50 text-sm text-popover-foreground"
                                    >
                                      <div className="font-medium mb-1 flex items-center gap-1.5 text-amber-500">
                                        <Sparkles size={14} />
                                        AI Adaptation
                                      </div>
                                      <p className="text-muted-foreground text-xs leading-relaxed">
                                        Detected that you struggled with <strong className="text-foreground font-medium">Python Data Structures</strong> in the last quiz. This session was added to help you master it before moving on.
                                      </p>
                                      <div className="absolute -top-1.5 left-4 w-3 h-3 bg-popover border-l border-t border-border rotate-45" />
                                    </motion.div>
                                  )}
                                </AnimatePresence>
                              </div>
                            )}
                          </div>
                          <button className="text-muted-foreground hover:text-foreground">
                            <MoreVertical size={18} />
                          </button>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground relative z-10">
                          <span className="flex items-center gap-1">
                            <Clock size={14} />
                            {session.duration as string}
                          </span>
                          {session.status === "in-progress" && (
                            <span className="text-primary-500 font-medium">In Progress</span>
                          )}
                        </div>
                        
                        {session.status === "in-progress" && (
                          <button
                            onClick={() => handleStartSession(session)}
                            disabled={generatingSessionId !== null}
                            className="mt-4 w-full py-2 bg-primary-500/10 text-primary-600 dark:text-primary-400 rounded-lg font-medium hover:bg-primary-500/20 transition-colors relative z-10 disabled:opacity-50 flex items-center justify-center gap-2"
                          >
                            {generatingSessionId === session.id ? (
                              <>
                                <Loader2 size={16} className="animate-spin" />
                                Generating Content...
                              </>
                            ) : (
                              "Start Learning"
                            )}
                          </button>
                        )}
                      </div>
                    </motion.div>
                  ))}
              </AnimatePresence>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
