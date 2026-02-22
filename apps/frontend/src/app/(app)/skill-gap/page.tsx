"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, AlertCircle, Info, Loader2, CheckCircle2, Target } from "lucide-react";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts';

export default function SkillGapPage() {
  const router = useRouter();
  const [isGenerating, setIsGenerating] = useState(false);
  const [skills, setSkills] = useState<Record<string, unknown>[]>([]);
  const [goal, setGoal] = useState("");

  useEffect(() => {
    const skillGapData = JSON.parse(localStorage.getItem('skill_gap') || '{}');
    const profile = JSON.parse(localStorage.getItem('learner_profile') || '{}');
    
    setGoal(profile.learning_goal || "Your Goal");
    
    // Convert backend skill gap data to frontend format
    const mappedSkills = Object.entries(skillGapData).map(([name, info]) => {
      const infoRecord = info as Record<string, unknown>;
      return {
        name,
        current: (infoRecord.current_level as number) || 20,
        target: (infoRecord.target_level as number) || 80,
        priority: (infoRecord.priority as string) || "Normal",
      };
    });

    setSkills(mappedSkills.length > 0 ? mappedSkills : [
      { name: "Python Fundamentals", current: 35, target: 80, priority: "Critical" },
      { name: "SQL & Databases", current: 40, target: 90, priority: "Critical" },
      { name: "Data Structures", current: 20, target: 75, priority: "Important" },
      { name: "Algorithms", current: 15, target: 70, priority: "Important" },
      { name: "System Design", current: 10, target: 60, priority: "Normal" },
    ]);
  }, []);

  const handleConfirm = async () => {
    setIsGenerating(true);
    try {
      const profile = localStorage.getItem('learner_profile');
      if (!profile) throw new Error("No learner profile found");

      const learningPath = await api.scheduleLearningPath({
        learner_profile: profile,
        session_count: 12, // Default to 12 sessions
        model: "openai/gpt-5.1"
      });

      localStorage.setItem('learning_path', JSON.stringify(learningPath));
      toast.success("Learning path scheduled successfully!");
      router.push("/learning-path");
    } catch (error) {
      console.error("Failed to generate learning path:", error);
      toast.error("Failed to generate learning path. Please try again.");
      setIsGenerating(false);
    }
  };

  const radarData = skills.map(s => ({
    subject: s.name as string,
    "Initial State S₀": Math.max(0, (s.current as number) - 15),
    "Current State Sₜ": s.current as number,
    "Target": s.target as number,
    fullMark: 100,
  }));

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Your Skill Gap Diagnosis</h1>
          <p className="mt-2 text-muted-foreground">Based on your goal: &quot;{goal}&quot;</p>
        </div>
        <button
          onClick={handleConfirm}
          disabled={isGenerating}
          className="flex items-center gap-2 bg-primary-500 text-white px-8 py-3 rounded-2xl font-black hover:bg-primary-600 transition-all shadow-lg shadow-primary-500/25 active:scale-95 disabled:opacity-50"
        >
          {isGenerating ? (
            <>
              <Loader2 className="animate-spin" size={18} />
              Generating Path...
            </>
          ) : (
            <>
              Confirm & Generate Path
              <ArrowRight size={18} strokeWidth={3} />
            </>
          )}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Readiness Radar Chart */}
          <div className="bg-card rounded-2xl shadow-sm border border-border p-6">
            <h2 className="text-xl font-bold text-foreground flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-500 flex items-center justify-center">
                <Target size={20} />
              </div>
              Readiness Overview
            </h2>
            <div className="h-[350px] w-full">
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
            
            <div className="grid gap-4">
              {skills.filter(s => (s.current as number) < (s.target as number)).map((skill, idx) => (
                <div key={idx} className="bg-card rounded-2xl shadow-sm border border-border p-6 hover:border-primary-500/30 transition-colors">
                  <div className="flex justify-between items-start mb-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-3">
                        <span className="font-bold text-lg text-foreground">{skill.name as string}</span>
                        <span
                          className={`text-[10px] px-2.5 py-1 rounded-full font-black uppercase tracking-widest ${
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
                    <span className="text-xs font-bold text-muted-foreground uppercase tracking-widest bg-muted px-3 py-1 rounded-full">Target: {skill.target as number}%</span>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="relative h-3 w-full bg-secondary rounded-full overflow-hidden">
                      {/* Target Marker */}
                      <div
                        className="absolute top-0 bottom-0 w-1 bg-foreground/20 z-10"
                        style={{ left: `${skill.target as number}%` }}
                      />
                      {/* Current Progress */}
                      <div
                        className="absolute top-0 bottom-0 bg-gradient-to-r from-primary-500 to-blue-500 rounded-full transition-all duration-1000 shadow-[0_0_12px_rgba(2,184,153,0.3)]"
                        style={{ width: `${skill.current as number}%` }}
                      />
                    </div>
                    <div className="flex justify-between text-[10px] font-black uppercase tracking-widest text-muted-foreground">
                      <span>Current: {skill.current as number}%</span>
                      <span className="text-primary-500">Gap: {(skill.target as number) - (skill.current as number)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Mastered Skills */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-foreground flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-green-500/10 text-green-500 flex items-center justify-center">
                <CheckCircle2 size={20} />
              </div>
              Mastered Skills
            </h2>
            
            <div className="grid gap-4">
              {skills.filter(s => (s.current as number) >= (s.target as number)).map((skill, idx) => (
                <div key={idx} className="bg-card/50 rounded-2xl border border-border p-6 opacity-80">
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-3">
                      <span className="font-bold text-lg text-foreground">{skill.name as string}</span>
                      <span className="text-[10px] px-2.5 py-1 rounded-full font-black uppercase tracking-widest bg-green-500/10 text-green-500">
                        Mastered
                      </span>
                    </div>
                    <span className="text-xs font-bold text-muted-foreground uppercase tracking-widest">Target: {skill.target as number}%</span>
                  </div>
                </div>
              ))}
              {skills.filter(s => (s.current as number) >= (s.target as number)).length === 0 && (
                <div className="text-center p-8 border border-dashed border-border rounded-2xl text-muted-foreground text-sm">
                  No mastered skills yet. Keep learning!
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <div className="bg-primary-500/5 rounded-[2rem] p-8 border border-primary-500/10">
            <h3 className="font-bold text-primary-600 dark:text-primary-400 flex items-center gap-2 mb-4">
              <Info size={18} />
              Why this matters
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed font-medium">
              We&apos;ve analyzed the job market for your goal and compared it with your background. The prioritized skills are your quickest path to being &quot;job-ready&quot;.
            </p>
          </div>

          <div className="bg-card rounded-[2rem] shadow-sm border border-border p-8">
            <h3 className="font-bold text-foreground mb-6">Estimated Timeline</h3>
            <div className="space-y-6">
              {[
                { label: "Total Time", value: "12 Weeks" },
                { label: "Commitment", value: "5-10 Hours/wk" },
                { label: "Total Sessions", value: "36 Sessions" },
              ].map((item, i) => (
                <div key={i} className="flex justify-between items-center border-b border-border pb-4 last:border-0 last:pb-0">
                  <span className="text-xs font-bold text-muted-foreground uppercase tracking-widest">{item.label}</span>
                  <span className="font-black text-foreground">{item.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
