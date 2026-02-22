"use client";

import { useState } from "react";
import { Plus, Target, Calendar, CheckCircle2, MoreVertical, Pencil, Trash2, X } from "lucide-react";
import { cn } from "@/lib/utils";

const mockGoals = [
  {
    id: 1,
    title: "Senior Data Analyst",
    description: "Transition from digital marketing to a senior data role with focus on Python and SQL.",
    status: "active",
    progress: 45,
    targetDate: "Q3 2026",
    skills: ["Python", "SQL", "Statistics", "Data Visualization"],
  },
  {
    id: 2,
    title: "Machine Learning Specialist",
    description: "Deep dive into machine learning models and their deployment in production environments.",
    status: "not-started",
    progress: 0,
    targetDate: "Q1 2027",
    skills: ["Scikit-learn", "TensorFlow", "Feature Engineering", "MLOps"],
  },
];

export default function GoalsPage() {
  const [activeGoal, setActiveGoal] = useState(mockGoals[0].id);
  const [isModalOpen, setIsModalOpen] = useState(false);

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

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Goals List */}
        <div className="lg:col-span-2 space-y-6">
          {mockGoals.map((goal) => (
            <div
              key={goal.id}
              onClick={() => setActiveGoal(goal.id)}
              className={cn(
                "p-6 rounded-2xl border transition-all cursor-pointer",
                activeGoal === goal.id
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
                        {goal.status === "active" ? "Current" : "Planned"}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar size={12} />
                        {goal.targetDate}
                      </span>
                    </div>
                  </div>
                </div>
                <button className="p-2 text-muted-foreground hover:text-foreground rounded-lg hover:bg-muted transition-colors">
                  <MoreVertical size={18} />
                </button>
              </div>

              <p className="text-muted-foreground text-sm mb-6 line-clamp-2">{goal.description}</p>

              <div className="space-y-3">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-muted-foreground font-medium">Readiness Progress</span>
                  <span className="text-primary-600 dark:text-primary-400 font-bold">{goal.progress}%</span>
                </div>
                <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-primary-500 transition-all duration-1000" 
                    style={{ width: `${goal.progress}%` }} 
                  />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Sidebar - Goal Detail & Quick Actions */}
        <div className="space-y-6">
          <div className="bg-card rounded-2xl shadow-sm border border-border p-6 sticky top-24">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-bold text-foreground">Goal Details</h3>
              <div className="flex gap-2">
                <button className="p-2 text-muted-foreground hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-950/30 rounded-lg transition-all">
                  <Pencil size={18} />
                </button>
                <button className="p-2 text-muted-foreground hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 rounded-lg transition-all">
                  <Trash2 size={18} />
                </button>
              </div>
            </div>

            <div className="space-y-6">
              <div>
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Key Skills to Master</p>
                <div className="flex flex-wrap gap-2">
                  {mockGoals.find(g => g.id === activeGoal)?.skills.map((skill, i) => (
                    <span 
                      key={i}
                      className="px-3 py-1.5 bg-muted text-foreground rounded-lg text-xs font-medium border border-border"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Recent Milestones</p>
                <div className="space-y-4">
                  {[
                    { title: "Python Fundamentals", date: "Feb 15", completed: true },
                    { title: "SQL Basic Mastery", date: "Feb 10", completed: true },
                    { title: "Statistics 101", date: "Planned", completed: false },
                  ].map((m, i) => (
                    <div key={i} className="flex items-center gap-3">
                      <div className={cn(
                        "w-5 h-5 rounded-full flex items-center justify-center shrink-0",
                        m.completed ? "bg-green-100 dark:bg-green-950/30 text-green-600 dark:text-green-400" : "bg-muted text-muted-foreground"
                      )}>
                        <CheckCircle2 size={14} />
                      </div>
                      <div className="flex-1">
                        <p className={cn("text-xs font-medium", m.completed ? "text-foreground" : "text-muted-foreground")}>
                          {m.title}
                        </p>
                        <p className="text-[10px] text-muted-foreground">{m.date}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <button className="w-full py-3 bg-foreground text-background rounded-xl font-semibold hover:opacity-90 transition-colors text-sm">
                View Detailed Analysis
              </button>
            </div>
          </div>
        </div>
      </div>

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
            
            <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); setIsModalOpen(false); }}>
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Goal Title</label>
                <input 
                  type="text" 
                  placeholder="e.g. Full Stack Developer" 
                  className="w-full px-4 py-2.5 bg-background border border-input rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all"
                  required
                />
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Description</label>
                <textarea 
                  placeholder="Briefly describe your goal..." 
                  rows={3}
                  className="w-full px-4 py-2.5 bg-background border border-input rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all resize-none"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Target Date</label>
                <input 
                  type="text" 
                  placeholder="e.g. Q4 2026" 
                  className="w-full px-4 py-2.5 bg-background border border-input rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all"
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">Key Skills (comma separated)</label>
                <input 
                  type="text" 
                  placeholder="e.g. React, Node.js, TypeScript" 
                  className="w-full px-4 py-2.5 bg-background border border-input rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 transition-all"
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
                  type="submit"
                  className="flex-1 px-4 py-2.5 bg-primary-500 text-white rounded-xl font-medium hover:bg-primary-600 transition-colors shadow-sm"
                >
                  Create Goal
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
