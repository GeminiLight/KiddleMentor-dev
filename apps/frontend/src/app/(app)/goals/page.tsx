"use client";

/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";
import { Plus, Target, CheckCircle2, MoreVertical, X, Loader2, Wand2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { useGoal } from "@/components/GoalContext";
import { api, getStoredLearnerId } from "@/lib/api";
import { motion, AnimatePresence } from "framer-motion";

export default function GoalsPage() {
  const { goals, currentGoal, setCurrentGoalIndex, learner, refresh, isLoading } = useGoal();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationStep, setGenerationStep] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    goal: "",
    background: "",
  });

  const handleCreateGoal = async () => {
    const learnerId = getStoredLearnerId();
    if (!learnerId || !formData.goal.trim()) return;

    setIsModalOpen(false);
    setIsGenerating(true);
    setGenerationStep(1);
    setError(null);

    try {
      // Step 1: Set and refine the learning goal (saved to memory, becomes active)
      await api.setLearningGoal(learnerId, formData.goal);
      setGenerationStep(2);

      // Step 2: Identify skill gaps and save to memory (keyed by new active goal)
      await api.identifyAndSaveSkillGap({
        learner_id: learnerId,
        learning_goal: formData.goal,
        learner_information: formData.background || learner.profile?.metadata?.cv_text || "",
      });
      setGenerationStep(3);

      // Step 3: Schedule learning path (backend enriches from memory)
      await api.scheduleLearningPath({
        learner_profile: { learner_id: learnerId },
        session_count: 12,
      });
      setGenerationStep(4);

      // Refresh context so goals list updates
      await refresh();

      setFormData({ goal: "", background: "" });
      setTimeout(() => {
        setIsGenerating(false);
        setGenerationStep(0);
      }, 800);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to create goal";
      setError(message);
      setIsGenerating(false);
      setGenerationStep(0);
    }
  };

  // Derive detail data from GoalContext for the selected goal
  const selectedGoal = goals.find((g) => g.goal_id === currentGoal.goal_id) || currentGoal;
  const selectedGoalSkillGaps = learner.skillGaps[selectedGoal.goal_id];
  const selectedGoalPath = learner.learningPath[selectedGoal.goal_id];
  const rawPath = selectedGoalPath?.learning_path;
  const sessions: any[] = Array.isArray(rawPath)
    ? rawPath
    : Array.isArray(rawPath?.learning_path)
      ? rawPath.learning_path
      : [];
  const completedSessions = sessions.filter((s: any) => s.completed || s.if_learned);

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Career Goals</h1>
          <p className="mt-2 text-muted-foreground">Define and track your long-term career objectives.</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-2 bg-primary-500 text-white px-6 py-2.5 rounded-full font-semibold hover:bg-primary-600 transition-colors shadow-sm"
        >
          <Plus size={18} />
          Add New Goal
        </button>
      </div>

      {error && (
        <div className="flex items-center gap-2 p-4 rounded-xl bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm border border-red-200 dark:border-red-800">
          <span>{error}</span>
          <button onClick={() => setError(null)} className="ml-auto text-red-400 hover:text-red-600">
            <X size={16} />
          </button>
        </div>
      )}

      {isLoading && goals.length <= 1 && goals[0]?.goal_id === "" ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 size={24} className="animate-spin text-muted-foreground" />
        </div>
      ) : goals.length === 1 && goals[0].goal_id === "" ? (
        <div className="text-center py-16">
          <Target size={48} className="mx-auto text-muted-foreground/40 mb-4" />
          <p className="text-muted-foreground mb-2">No goals yet.</p>
          <p className="text-sm text-muted-foreground">Click &ldquo;Add New Goal&rdquo; to get started.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Goals List */}
          <div className="lg:col-span-2 space-y-6">
            {goals.filter((g) => g.goal_id !== "").map((goal, idx) => (
              <div
                key={goal.goal_id}
                onClick={() => setCurrentGoalIndex(idx)}
                className={cn(
                  "p-6 rounded-2xl border transition-all cursor-pointer",
                  currentGoal.goal_id === goal.goal_id
                    ? "bg-card border-primary-500 ring-1 ring-primary-500 shadow-md"
                    : "bg-card border-border hover:border-primary-500/30 shadow-sm"
                )}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className={cn(
                      "w-10 h-10 rounded-xl flex items-center justify-center",
                      goal.status === "active" ? "bg-primary-50 dark:bg-primary-950/30 text-primary-600 dark:text-primary-400" : "bg-muted text-muted-foreground"
                    )}>
                      <Target size={24} />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-foreground">{goal.title}</h3>
                      <div className="flex items-center gap-2 text-xs text-muted-foreground">
                        <span className={cn(
                          "px-2 py-0.5 rounded-full font-medium",
                          goal.status === "active" ? "bg-green-50 dark:bg-green-950/30 text-green-700 dark:text-green-400" : "bg-muted text-muted-foreground"
                        )}>
                          {goal.status === "active" ? "Active" : "Inactive"}
                        </span>
                      </div>
                    </div>
                  </div>
                  <button className="p-2 text-muted-foreground hover:text-foreground rounded-lg hover:bg-muted transition-colors">
                    <MoreVertical size={18} />
                  </button>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-muted-foreground font-medium">Readiness Progress</span>
                    <span className="text-primary-600 dark:text-primary-400 font-bold">{goal.readiness}%</span>
                  </div>
                  <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary-500 transition-all duration-1000"
                      style={{ width: `${goal.readiness}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Sidebar - Goal Detail */}
          <div className="space-y-6">
            <div className="bg-card rounded-2xl shadow-sm border border-border p-6 sticky top-24">
              <div className="flex items-center justify-between mb-6">
                <h3 className="font-bold text-foreground">Goal Details</h3>
              </div>

              <div className="space-y-6">
                {/* Skill Gaps */}
                {selectedGoalSkillGaps && (
                  <div>
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Skill Gaps</p>
                    <div className="flex flex-wrap gap-2">
                      {(() => {
                        const rawGaps = selectedGoalSkillGaps?.skill_gaps;
                        // Handle double-nested: skill_gaps.skill_gaps may itself contain the array
                        const gaps = Array.isArray(rawGaps)
                          ? rawGaps
                          : Array.isArray(rawGaps?.skill_gaps)
                            ? rawGaps.skill_gaps
                            : rawGaps;
                        if (Array.isArray(gaps)) {
                          return gaps.map((gap: any, i: number) => (
                            <span key={i} className="px-3 py-1.5 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400 rounded-lg text-xs font-medium border border-amber-200 dark:border-amber-800">
                              {typeof gap === "string" ? gap : gap?.skill || gap?.name || JSON.stringify(gap)}
                            </span>
                          ));
                        }
                        if (typeof gaps === "object" && gaps) {
                          return Object.keys(gaps).map((key, i) => (
                            <span key={i} className="px-3 py-1.5 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400 rounded-lg text-xs font-medium border border-amber-200 dark:border-amber-800">
                              {key}
                            </span>
                          ));
                        }
                        return <span className="text-xs text-muted-foreground">No skill gaps data</span>;
                      })()}
                    </div>
                  </div>
                )}

                {/* Recent Sessions */}
                <div>
                  <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">
                    Sessions ({completedSessions.length}/{sessions.length})
                  </p>
                  <div className="space-y-4">
                    {sessions.length === 0 ? (
                      <p className="text-xs text-muted-foreground">No learning path scheduled yet.</p>
                    ) : (
                      sessions.slice(0, 5).map((s: any, i: number) => (
                        <div key={i} className="flex items-center gap-3">
                          <div className={cn(
                            "w-5 h-5 rounded-full flex items-center justify-center shrink-0",
                            (s.completed || s.if_learned) ? "bg-green-100 dark:bg-green-950/30 text-green-600 dark:text-green-400" : "bg-muted text-muted-foreground"
                          )}>
                            <CheckCircle2 size={14} />
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className={cn("text-xs font-medium truncate", (s.completed || s.if_learned) ? "text-foreground" : "text-muted-foreground")}>
                              {s.topic || s.title || `Session ${s.session_number || i + 1}`}
                            </p>
                          </div>
                        </div>
                      ))
                    )}
                    {sessions.length > 5 && (
                      <p className="text-xs text-muted-foreground">+ {sessions.length - 5} more sessions</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Add Goal Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="bg-card w-full max-w-md rounded-2xl shadow-xl border border-border p-6 m-4 animate-in fade-in zoom-in duration-200">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-foreground">Add New Goal</h2>
              <button
                onClick={() => setIsModalOpen(false)}
                className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-full transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">What do you want to learn?</label>
                <textarea
                  value={formData.goal}
                  onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
                  placeholder="e.g., I want to become a Full Stack Developer with expertise in React and Node.js"
                  rows={4}
                  className="w-full px-4 py-2.5 bg-background border border-input rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all resize-none"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Relevant background (optional)</label>
                <textarea
                  value={formData.background}
                  onChange={(e) => setFormData({ ...formData, background: e.target.value })}
                  placeholder="e.g., I have 2 years of frontend experience with HTML/CSS..."
                  rows={3}
                  className="w-full px-4 py-2.5 bg-background border border-input rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all resize-none"
                />
              </div>

              <div className="pt-4 flex gap-3">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="flex-1 px-4 py-2.5 border border-input bg-background text-foreground rounded-xl font-medium hover:bg-muted transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateGoal}
                  disabled={!formData.goal.trim()}
                  className="flex-1 px-4 py-2.5 bg-primary-500 text-white rounded-xl font-medium hover:bg-primary-600 transition-colors shadow-sm disabled:opacity-50"
                >
                  Create Goal
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Generation Overlay */}
      <AnimatePresence>
        {isGenerating && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-background/90 backdrop-blur-md"
          >
            <div className="max-w-md w-full p-8 flex flex-col items-center text-center">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                className="relative w-28 h-28 mb-8"
              >
                <div className="absolute inset-0 rounded-full border-4 border-muted" />
                <div className="absolute inset-0 rounded-full border-4 border-primary-500 border-t-transparent animate-spin" style={{ animationDuration: "2s" }} />
                <div className="absolute inset-0 flex items-center justify-center">
                  <Wand2 className="w-8 h-8 text-primary-500 animate-pulse" />
                </div>
              </motion.div>

              <h2 className="text-xl font-bold text-foreground mb-6">Setting up your new goal...</h2>

              <div className="w-full space-y-3">
                {[
                  { step: 1, label: "Refining your learning goal...", icon: "🎯" },
                  { step: 2, label: "Identifying skill gaps...", icon: "🧠" },
                  { step: 3, label: "Scheduling learning path...", icon: "🗺️" },
                  { step: 4, label: "Done!", icon: "✅" },
                ].map((item) => (
                  <motion.div
                    key={item.step}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{
                      opacity: generationStep >= item.step ? 1 : 0.3,
                      x: generationStep >= item.step ? 0 : -20,
                      scale: generationStep === item.step ? 1.03 : 1,
                    }}
                    className={cn(
                      "flex items-center gap-3 p-3 rounded-xl border",
                      generationStep === item.step
                        ? "bg-primary-50 dark:bg-primary-900/20 border-primary-200 dark:border-primary-800"
                        : "bg-card border-border"
                    )}
                  >
                    <span className="text-xl">{item.icon}</span>
                    <span className={cn(
                      "font-medium text-sm",
                      generationStep === item.step ? "text-primary-700 dark:text-primary-300" : "text-muted-foreground"
                    )}>
                      {item.label}
                    </span>
                    {generationStep === item.step && item.step < 4 && (
                      <Loader2 className="w-4 h-4 ml-auto animate-spin text-primary-500" />
                    )}
                    {generationStep > item.step && (
                      <div className="w-4 h-4 ml-auto rounded-full bg-green-500 flex items-center justify-center">
                        <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    )}
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
