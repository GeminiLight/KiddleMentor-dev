"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, Check, Loader2, Sparkles, UploadCloud, FileText, X, Wand2, Target } from "lucide-react";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { ThemeToggle } from "@/components/ThemeToggle";
import { setStoredLearnerId } from "@/lib/api";
import { motion, AnimatePresence } from "framer-motion";

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationStep, setGenerationStep] = useState(0);
  const [isParsingBackground, setIsParsingBackground] = useState(false);
  const [isRefiningGoal, setIsRefiningGoal] = useState(false);
  const [resumeFile, setResumeFile] = useState<File | null>(null);

  const [formData, setFormData] = useState({
    name: "",
    goal: "",
    background: "",
    commitment: "5-10 hours/week",
  });

  const handleNext = async () => {
    if (step === 1) {
      setIsParsingBackground(true);
      setTimeout(() => {
        setIsParsingBackground(false);
        setStep(2);
      }, 1500);
    } else if (step === 2) {
      setStep(3);
    } else {
      setIsGenerating(true);
      setGenerationStep(1); // Skill Identifier scanning target...
      try {
        // Step 1: Initialize session with backend (creates learner_id + workspace)
        const response = await api.initializeSession({
          name: formData.name || "Anonymous Learner",
          cv: resumeFile || undefined,
        });
        const learner_id = response.learner_id;

        console.log('[Onboarding] Session initialized:', learner_id);

        // Save learner_id to localStorage
        setStoredLearnerId(learner_id);

        // Step 2: Set learning goal (backend refines it and saves)
        await api.setLearningGoal(learner_id, formData.goal);
        console.log('[Onboarding] Learning goal set');
        
        setGenerationStep(2); // Path Scheduler calculating optimal path...

        // Step 3: Identify skill gaps and save to memory (keyed by active goal)
        await api.identifyAndSaveSkillGap({
          learner_id: learner_id,
          learning_goal: formData.goal,
          learner_information: formData.background || "Information provided via CV",
        });
        console.log('[Onboarding] Skill gaps identified');
        
        setGenerationStep(3); // Content Creator retrieving latest materials...

        // Step 4: Generate learning path (backend persists to workspace)
        await api.scheduleLearningPath({
          learner_profile: { learner_id },
          session_count: 12, // Default to 12 sessions
        });
        console.log('[Onboarding] Learning path scheduled');

        setGenerationStep(4); // Done
        toast.success("Learning path generated successfully!");

        // Redirect to dashboard instead of skill-gap
        setTimeout(() => router.push("/progress"), 1000);
      } catch (error) {
        console.error("Failed to generate path:", error);
        toast.error(error instanceof Error ? error.message : "Failed to generate learning path. Please try again.");
        setIsGenerating(false);
        setGenerationStep(0);
      }
    }
  };

  const handleRefineGoal = () => {
    if (!formData.goal.trim()) return;
    setIsRefiningGoal(true);
    setTimeout(() => {
      setFormData(prev => ({
        ...prev,
        goal: `I want to become a professional in ${prev.goal}, focusing on core industry skills and practical applications to achieve mastery.`
      }));
      setIsRefiningGoal(false);
    }, 1500);
  };

  const getEstimatedTime = (commitment: string) => {
    if (commitment.includes("10+")) return "Estimated time to goal: 3 weeks";
    if (commitment.includes("5-10")) return "Estimated time to goal: 6 weeks";
    return "Estimated time to goal: 3 months";
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col items-center justify-center p-6">
      {/* Theme toggle in top right corner */}
      <div className="fixed top-6 right-6 z-50">
        <ThemeToggle variant="landing" />
      </div>

      <div className="w-full max-w-2xl bg-white dark:bg-slate-900 rounded-[2.5rem] shadow-sm border border-slate-200 dark:border-slate-700 p-8 md:p-12 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary-500/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />

        {/* Step Indicator */}
        <div className="flex items-center justify-between mb-12 relative">
          <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-0.5 bg-slate-100 dark:bg-slate-700 -z-10" />
          <div
            className="absolute left-0 top-1/2 -translate-y-1/2 h-0.5 bg-primary-500 -z-10 transition-all duration-500"
            style={{ width: `${((step - 1) / 2) * 100}%` }}
          />

          {[
            { num: 1, label: "Profile" },
            { num: 2, label: "Goal" },
            { num: 3, label: "Commitment" }
          ].map(({ num, label }) => (
            <div key={num} className="flex flex-col items-center gap-2 bg-white dark:bg-slate-900 px-4 z-10">
              <div className={cn(
                "flex h-10 w-10 items-center justify-center rounded-full text-sm font-black transition-all",
                step > num ? "bg-green-500 text-white" :
                step === num ? "bg-primary-500 text-white ring-4 ring-primary-500/10 dark:ring-primary-400/20" :
                "bg-slate-100 dark:bg-slate-800 text-slate-400 dark:text-slate-500"
              )}>
                {step > num ? <Check size={18} strokeWidth={3} /> : num}
              </div>
              <span className={cn(
                "text-[10px] font-black uppercase tracking-widest",
                step >= num ? "text-slate-900 dark:text-white" : "text-slate-400 dark:text-slate-600"
              )}>
                {label}
              </span>
            </div>
          ))}
        </div>
        
        <div className="text-center mb-8">
          <p className="text-xs font-medium text-slate-500 dark:text-slate-400">
            {step === 1 ? "Estimated 1 minute to complete setup" : step === 2 ? "Final step, define your goal" : "Generating your personalized learning path"}
          </p>
        </div>

        {/* Content */}
        <div className="min-h-[320px]">
          {step === 1 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-2xl bg-blue-500/10 text-blue-500 flex items-center justify-center">
                  <Sparkles size={24} />
                </div>
                <div>
                  <h2 className="text-2xl font-black text-slate-900 dark:text-white">What&apos;s your background?</h2>
                  <p className="text-slate-500 dark:text-slate-400 text-sm">Help us personalize your learning experience.</p>
                </div>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">Your Name</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full p-4 rounded-2xl border-2 border-slate-100 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 focus:border-primary-500 dark:focus:border-primary-400 focus:ring-4 focus:ring-primary-500/5 dark:focus:ring-primary-400/10 outline-none text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 font-medium transition-all"
                    placeholder="e.g., John Doe"
                  />
                </div>

                <div>
                  <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">Tell us about yourself</label>
                  <textarea
                    value={formData.background}
                    onChange={(e) => setFormData({ ...formData, background: e.target.value })}
                    className="w-full h-32 p-4 rounded-2xl border-2 border-slate-100 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 focus:border-primary-500 dark:focus:border-primary-400 focus:ring-4 focus:ring-primary-500/5 dark:focus:ring-primary-400/10 outline-none resize-none text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 font-medium transition-all"
                    placeholder="e.g., I have 3 years of experience in digital marketing. I know basic Excel but no programming languages."
                  />
                </div>

                <div className="relative flex items-center py-2">
                  <div className="flex-grow border-t border-slate-200 dark:border-slate-700"></div>
                  <span className="flex-shrink-0 mx-4 text-slate-400 dark:text-slate-500 text-xs font-bold uppercase tracking-widest">OR UPLOAD RESUME</span>
                  <div className="flex-grow border-t border-slate-200 dark:border-slate-700"></div>
                </div>

                {!resumeFile ? (
                  <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-2xl cursor-pointer bg-slate-50/50 dark:bg-slate-800/50 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors group">
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                      <UploadCloud className="w-8 h-8 text-slate-400 dark:text-slate-500 mb-3 group-hover:text-primary-500 transition-colors" />
                      <p className="mb-1 text-sm text-slate-500 dark:text-slate-400 font-medium"><span className="font-bold text-primary-500">Click to upload</span> or drag and drop</p>
                      <p className="text-xs text-slate-400 dark:text-slate-500">PDF (MAX. 5MB)</p>
                    </div>
                    <input 
                      type="file" 
                      className="hidden" 
                      accept=".pdf"
                      onChange={(e) => {
                        if (e.target.files && e.target.files[0]) {
                          setResumeFile(e.target.files[0]);
                        }
                      }}
                    />
                  </label>
                ) : (
                  <div className="flex items-center justify-between p-4 border-2 border-primary-500/30 bg-primary-500/5 rounded-2xl">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-primary-500/10 text-primary-500 flex items-center justify-center">
                        <FileText size={20} />
                      </div>
                      <div>
                        <p className="text-sm font-bold text-slate-900 dark:text-white line-clamp-1">{resumeFile.name}</p>
                        <p className="text-xs text-slate-500 dark:text-slate-400">{(resumeFile.size / 1024 / 1024).toFixed(2)} MB</p>
                      </div>
                    </div>
                    <button 
                      onClick={() => setResumeFile(null)}
                      className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-xl transition-colors"
                    >
                      <X size={18} />
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-2xl bg-primary-500/10 text-primary-500 flex items-center justify-center">
                    <Sparkles size={24} />
                  </div>
                  <div>
                    <h2 className="text-2xl font-black text-slate-900 dark:text-white">What is your learning goal?</h2>
                    <p className="text-slate-500 dark:text-slate-400 text-sm">Be as specific as possible. We&apos;ll use this to build your path.</p>
                  </div>
                </div>
                <button
                  onClick={handleRefineGoal}
                  disabled={isRefiningGoal || !formData.goal.trim()}
                  className="flex items-center gap-2 bg-amber-500/10 text-amber-600 dark:text-amber-400 px-4 py-2 rounded-xl font-bold hover:bg-amber-500/20 transition-colors disabled:opacity-50 text-sm"
                >
                  {isRefiningGoal ? <Loader2 size={16} className="animate-spin" /> : <Wand2 size={16} />}
                  AI Refinement
                </button>
              </div>
              <textarea
                value={formData.goal}
                onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
                className="w-full h-40 p-6 rounded-3xl border-2 border-slate-100 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 focus:border-primary-500 dark:focus:border-primary-400 focus:ring-4 focus:ring-primary-500/5 dark:focus:ring-primary-400/10 outline-none resize-none text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-slate-500 font-medium transition-all"
                placeholder="e.g., I want to become a Senior Data Analyst specializing in Python and SQL, transitioning from a marketing background."
              />
            </div>
          )}

          {step === 3 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-2xl bg-orange-500/10 text-orange-500 flex items-center justify-center">
                  <Sparkles size={24} />
                </div>
                <div>
                  <h2 className="text-2xl font-black text-slate-900 dark:text-white">Time commitment?</h2>
                  <p className="text-slate-500 dark:text-slate-400 text-sm">We&apos;ll schedule your weekly sessions around your availability.</p>
                </div>
              </div>

              {/* Result Association Display */}
              <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800/50 rounded-2xl p-4 flex items-start gap-3">
                <div className="mt-1 text-blue-500">
                  <Target size={20} />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-blue-900 dark:text-blue-100 mb-1">AI Suggestion</h4>
                  <p className="text-xs text-blue-700 dark:text-blue-300 leading-relaxed">
                    Based on your goal to master <span className="font-bold">{formData.goal.split(' ').slice(0, 3).join(' ')}...</span>, we recommend <span className="font-bold">5-10 hours/week</span> for steady progress without burnout.
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4">
                {[
                  { time: "2-4 hours/week", desc: "Casual pace" },
                  { time: "5-10 hours/week", desc: "Steady progress" },
                  { time: "10+ hours/week", desc: "Intensive immersion" }
                ].map((option) => (
                  <button
                    key={option.time}
                    onClick={() => setFormData({ ...formData, commitment: option.time })}
                    className={cn(
                      "flex items-center justify-between p-6 rounded-3xl border-2 transition-all group",
                      formData.commitment === option.time
                        ? "border-primary-500 bg-primary-500/5 dark:bg-primary-500/10 shadow-lg shadow-primary-500/5"
                        : "border-slate-100 dark:border-slate-700 hover:border-primary-500/30 dark:hover:border-primary-400/30"
                    )}
                  >
                    <div className="text-left">
                      <span className="block font-black text-slate-900 dark:text-white text-lg">{option.time}</span>
                      <span className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-widest">{option.desc}</span>
                    </div>
                    <div className="flex items-center gap-4">
                      {formData.commitment === option.time && (
                        <span className="text-sm font-bold text-primary-600 dark:text-primary-400 bg-primary-500/10 px-3 py-1 rounded-full animate-in fade-in zoom-in duration-300">
                          {getEstimatedTime(option.time)}
                        </span>
                      )}
                      <div className={cn(
                        "w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all",
                        formData.commitment === option.time
                          ? "border-primary-500 bg-primary-500 text-white"
                          : "border-slate-200 dark:border-slate-700"
                      )}>
                        {formData.commitment === option.time && <Check size={14} strokeWidth={4} />}
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="mt-12 flex justify-between items-center pt-8 border-t border-slate-100 dark:border-slate-700">
          <button
            onClick={() => setStep(Math.max(1, step - 1))}
            className={cn(
              "px-6 py-2 text-sm font-black text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors uppercase tracking-widest",
              step === 1 ? "invisible" : ""
            )}
          >
            Back
          </button>
          <button
            onClick={handleNext}
            disabled={isGenerating || isParsingBackground || (step === 1 && !formData.background && !resumeFile) || (step === 2 && !formData.goal)}
            className="flex items-center gap-2 bg-slate-900 dark:bg-white text-white dark:text-slate-900 px-10 py-4 rounded-2xl font-black hover:opacity-90 transition-all disabled:opacity-30 active:scale-95 shadow-xl"
          >
            {isGenerating ? (
              <>
                <Loader2 className="animate-spin" size={20} />
                Crafting Your Path...
              </>
            ) : isParsingBackground ? (
              <>
                <Loader2 className="animate-spin" size={20} />
                Parsing your background...
              </>
            ) : step === 3 ? (
              <>
                Generate Journey
                <ArrowRight size={20} strokeWidth={3} />
              </>
            ) : (
              <>
                Continue
                <ArrowRight size={20} strokeWidth={3} />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Agent Collaboration Overlay */}
      <AnimatePresence>
        {isGenerating && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-white/90 dark:bg-slate-950/90 backdrop-blur-md"
          >
            <div className="max-w-md w-full p-8 flex flex-col items-center text-center">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                className="relative w-32 h-32 mb-8"
              >
                <div className="absolute inset-0 rounded-full border-4 border-slate-200 dark:border-slate-800" />
                <div className="absolute inset-0 rounded-full border-4 border-blue-500 border-t-transparent animate-spin" style={{ animationDuration: '2s' }} />
                <div className="absolute inset-0 flex items-center justify-center">
                  <Wand2 className="w-10 h-10 text-blue-500 animate-pulse" />
                </div>
              </motion.div>

              <h2 className="text-2xl font-black text-slate-900 dark:text-white mb-6">
                AI Mentor Team is working...
              </h2>

              <div className="w-full space-y-4">
                {[
                  { step: 1, label: "Skill Identifier analyzing your background...", icon: "🧠" },
                  { step: 2, label: "Path Scheduler mapping your journey...", icon: "🗺️" },
                  { step: 3, label: "Content Creator gathering resources...", icon: "📚" },
                  { step: 4, label: "Finalizing your personalized plan...", icon: "✨" }
                ].map((item) => (
                  <motion.div
                    key={item.step}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ 
                      opacity: generationStep >= item.step ? 1 : 0.3,
                      x: generationStep >= item.step ? 0 : -20,
                      scale: generationStep === item.step ? 1.05 : 1
                    }}
                    className={`flex items-center gap-4 p-4 rounded-xl border ${
                      generationStep === item.step 
                        ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800' 
                        : 'bg-white dark:bg-slate-900 border-slate-100 dark:border-slate-800'
                    }`}
                  >
                    <span className="text-2xl">{item.icon}</span>
                    <span className={`font-medium ${
                      generationStep === item.step 
                        ? 'text-blue-700 dark:text-blue-300' 
                        : 'text-slate-500 dark:text-slate-400'
                    }`}>
                      {item.label}
                    </span>
                    {generationStep === item.step && (
                      <Loader2 className="w-4 h-4 ml-auto animate-spin text-blue-500" />
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
