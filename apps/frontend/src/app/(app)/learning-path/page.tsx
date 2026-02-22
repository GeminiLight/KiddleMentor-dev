"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Play, CheckCircle2, Clock, Calendar, MoreVertical, Lock, RefreshCw, Award, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function LearningPathPage() {
  const router = useRouter();
  const [sessions, setSessions] = useState<Record<string, unknown>[]>([]);
  const [isRescheduling, setIsRescheduling] = useState(false);

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
    }, 1500);
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
            onClick={handleReschedule}
            disabled={isRescheduling}
            className="flex items-center gap-2 bg-muted text-foreground px-4 py-2.5 rounded-full font-medium hover:bg-muted/80 transition-colors disabled:opacity-50"
          >
            <RefreshCw size={18} className={isRescheduling ? "animate-spin" : ""} />
            {isRescheduling ? "Adapting..." : "Reschedule"}
          </button>
          <button
            onClick={() => router.push("/session/2")}
            className="flex items-center gap-2 bg-primary-500 text-white px-6 py-2.5 rounded-full font-semibold hover:bg-primary-600 transition-colors shadow-sm"
          >
            <Play size={18} fill="currentColor" />
            Continue Session
          </button>
        </div>
      </div>

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
                              <span className="text-xs font-bold text-amber-500 bg-amber-500/10 px-2 py-0.5 rounded-full">
                                Added for you
                              </span>
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
