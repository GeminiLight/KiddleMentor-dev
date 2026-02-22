"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Play, CheckCircle2, Clock, Calendar, MoreVertical, Lock, RefreshCw, Award, Sparkles, X, Check } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function LearningPathPage() {
  const router = useRouter();
  const [sessions, setSessions] = useState<Record<string, unknown>[]>([]);
  const [isRescheduling, setIsRescheduling] = useState(false);
  const [hasPendingChanges, setHasPendingChanges] = useState(false);
  const [originalSessions, setOriginalSessions] = useState<Record<string, unknown>[]>([]);
  const [activeTooltip, setActiveTooltip] = useState<string | number | null>(null);

  // Close tooltip when clicking outside
  useEffect(() => {
    const handleClickOutside = () => setActiveTooltip(null);
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, []);

  useEffect(() => {
    const pathData = JSON.parse(localStorage.getItem('learning_path') || '[]');
    
    // Map backend learning path to sessions
    // pathData is likely an array of session objects
    if (pathData && Array.isArray(pathData) && pathData.length > 0) {
      const mappedSessions = pathData.map((s: Record<string, unknown>, idx: number) => ({
        id: idx + 1,
        title: s.session_title || s.title || `Session ${idx + 1}`,
        duration: s.estimated_duration || "45 min",
        status: idx === 0 ? "in-progress" : (idx < 2 ? "completed" : "locked"), // Mocking status for demo
        week: Math.floor(idx / 3) + 1,
        isMilestone: (idx + 1) % 3 === 0, // Every 3rd session is a milestone
        data: s
      }));
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setSessions(mappedSessions);
    } else {
      // Fallback mock sessions if no data found
      setSessions([
        { id: 1, title: "Introduction to Python Syntax", duration: "45 min", status: "completed", week: 1, isMilestone: false },
        { id: 2, title: "Variables and Data Types", duration: "60 min", status: "in-progress", week: 1, isMilestone: false },
        { id: 3, title: "Control Flow (If/Else)", duration: "45 min", status: "locked", week: 1, isMilestone: true },
      ]);
    }
  }, []);

  const handleReschedule = () => {
    setIsRescheduling(true);
    setOriginalSessions([...sessions]);
    // Simulate API call for rescheduling
    setTimeout(() => {
      setSessions(prev => {
        const newSessions = [...prev];
        // Add a new session to simulate dynamic adaptation
        newSessions.splice(2, 0, {
          id: Date.now(),
          title: "Deep Dive: Python Data Structures",
          duration: "30 min",
          status: "locked",
          week: 1,
          isNew: true,
          isMilestone: false,
          data: {}
        });
        return newSessions;
      });
      setIsRescheduling(false);
      setHasPendingChanges(true);
    }, 1500);
  };

  const handleAccept = () => {
    setSessions(prev => prev.map(s => ({ ...s, isNew: false })));
    setHasPendingChanges(false);
  };

  const handleReject = () => {
    setSessions(originalSessions);
    setHasPendingChanges(false);
  };

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
            onClick={() => router.push("/session/2")}
            className="flex items-center gap-2 bg-primary-500 text-white px-6 py-2.5 rounded-full font-semibold hover:bg-primary-600 transition-colors shadow-sm"
          >
            <Play size={18} fill="currentColor" />
            Continue Session
          </button>
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
                            onClick={() => {
                              localStorage.setItem('current_session', JSON.stringify(session.data));
                              router.push(`/session/${session.id}`);
                            }}
                            className="mt-4 w-full py-2 bg-primary-500/10 text-primary-600 dark:text-primary-400 rounded-lg font-medium hover:bg-primary-500/20 transition-colors relative z-10"
                          >
                            Start Learning
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
