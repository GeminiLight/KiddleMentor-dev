"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { BookOpen, FileText, CheckCircle2, AlertCircle, Archive, Sparkles, ChevronDown, Target, Zap } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { LibraryCard } from "@/components/LibraryCard";
import { MistakeBook } from "@/components/MistakeBook";
import { useSession } from "@/lib/hooks/useSession";

export default function LibraryPage() {
  const { isLoading } = useSession();
  const [activeTab, setActiveTab] = useState<"Overview" | "Study Materials" | "Assessments" | "Archives">("Overview");
  const [isGoalMenuOpen, setIsGoalMenuOpen] = useState(false);
  const [currentGoal, setCurrentGoal] = useState("Senior Data Analyst");
  const [isGeneratingSummary, setIsGeneratingSummary] = useState(false);
  const [goalSummary, setGoalSummary] = useState<string | null>(null);

  const tabs = [
    { id: "Overview", icon: BookOpen },
    { id: "Study Materials", icon: FileText },
    { id: "Assessments", icon: AlertCircle },
    { id: "Archives", icon: Archive },
  ];

  const mockDocuments = [
    {
      id: "doc-1",
      title: "Advanced SQL Window Functions",
      type: "document" as const,
      mastery: 85,
      skills: ["SQL", "Data Analysis"],
      date: "2 days ago",
      duration: "15 min read",
    },
    {
      id: "doc-2",
      title: "Python Pandas for Data Manipulation",
      type: "interactive" as const,
      mastery: 60,
      skills: ["Python", "Pandas"],
      date: "1 week ago",
      duration: "30 min practice",
    },
    {
      id: "doc-3",
      title: "Data Visualization with Matplotlib",
      type: "video" as const,
      mastery: 40,
      skills: ["Python", "Data Viz"],
      date: "2 weeks ago",
      duration: "45 min watch",
    }
  ];

  const handleGenerateSummary = () => {
    setIsGeneratingSummary(true);
    setTimeout(() => {
      setGoalSummary(
        "You have made significant progress in **SQL** and **Python Data Manipulation**. Your mastery of Window Functions is strong (85%), but you need more practice with Data Visualization (40%). Focus on Matplotlib and Seaborn in your upcoming sessions to close this gap."
      );
      setIsGeneratingSummary(false);
    }, 2000);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500" />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header & Goal Switcher */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Knowledge Library</h1>
          <p className="mt-2 text-muted-foreground">
            Your personalized hub for documents, mistakes, and AI insights.
          </p>
        </div>

        <div className="relative">
          <button
            onClick={() => setIsGoalMenuOpen(!isGoalMenuOpen)}
            className="flex items-center gap-3 bg-card border border-border px-4 py-2.5 rounded-xl shadow-sm hover:bg-muted/50 transition-colors"
          >
            <div className="p-1.5 bg-primary-500/10 text-primary-600 dark:text-primary-400 rounded-lg">
              <Target size={18} />
            </div>
            <div className="text-left">
              <div className="text-xs text-muted-foreground font-medium">Current Goal Filter</div>
              <div className="text-sm font-semibold text-foreground">{currentGoal}</div>
            </div>
            <ChevronDown size={16} className="text-muted-foreground ml-2" />
          </button>

          <AnimatePresence>
            {isGoalMenuOpen && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="absolute right-0 top-full mt-2 w-64 bg-popover border border-border rounded-xl shadow-lg z-50 overflow-hidden"
              >
                <div className="p-2">
                  {["Senior Data Analyst", "Full Stack Developer", "Product Manager"].map((goal) => (
                    <button
                      key={goal}
                      onClick={() => {
                        setCurrentGoal(goal);
                        setIsGoalMenuOpen(false);
                      }}
                      className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                        currentGoal === goal
                          ? "bg-primary-500/10 text-primary-600 dark:text-primary-400 font-medium"
                          : "text-foreground hover:bg-muted"
                      }`}
                    >
                      {goal}
                    </button>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Main Content Area */}
        <div className="lg:col-span-3 space-y-8">
          {/* Tabs */}
          <div className="flex items-center gap-2 border-b border-border pb-px overflow-x-auto hide-scrollbar">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as "Overview" | "Study Materials" | "Assessments" | "Archives")}
                  className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${
                    isActive
                      ? "border-primary-500 text-primary-600 dark:text-primary-400"
                      : "border-transparent text-muted-foreground hover:text-foreground hover:border-border"
                  }`}
                >
                  <Icon size={18} />
                  {tab.id}
                </button>
              );
            })}
          </div>

          {/* Tab Content */}
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              {activeTab === "Overview" && (
                <div className="space-y-8">
                  {/* Quick Scan / Goal Summary */}
                  <div className="bg-gradient-to-br from-primary-500/10 to-amber-500/5 border border-primary-500/20 rounded-2xl p-6 relative overflow-hidden">
                    <div className="absolute -right-20 -top-20 w-64 h-64 bg-primary-500/10 rounded-full blur-3xl pointer-events-none" />
                    <div className="flex items-start justify-between gap-4 relative z-10">
                      <div>
                        <h2 className="text-xl font-bold text-primary-700 dark:text-primary-400 flex items-center gap-2">
                          <Sparkles size={24} />
                          Goal Summary: {currentGoal}
                        </h2>
                        <p className="text-primary-600/80 dark:text-primary-400/80 mt-2 max-w-2xl">
                          Generate a synthesis of all learned sessions for this goal to help with long-term retention and identify next steps.
                        </p>
                      </div>
                      {!goalSummary && !isGeneratingSummary && (
                        <button
                          onClick={handleGenerateSummary}
                          className="shrink-0 flex items-center gap-2 bg-primary-500 text-white px-5 py-2.5 rounded-full font-medium hover:bg-primary-600 transition-colors shadow-sm"
                        >
                          <Zap size={18} />
                          Quick Scan
                        </button>
                      )}
                    </div>

                    {isGeneratingSummary && (
                      <div className="mt-6 space-y-3">
                        <div className="h-4 bg-primary-500/20 rounded animate-pulse w-3/4" />
                        <div className="h-4 bg-primary-500/20 rounded animate-pulse w-full" />
                        <div className="h-4 bg-primary-500/20 rounded animate-pulse w-5/6" />
                      </div>
                    )}

                    {goalSummary && !isGeneratingSummary && (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-6 p-5 bg-background/50 backdrop-blur-sm border border-primary-500/20 rounded-xl text-foreground leading-relaxed"
                      >
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {goalSummary}
                        </ReactMarkdown>
                      </motion.div>
                    )}
                  </div>

                  {/* Latest Documents */}
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-foreground">Latest Study Materials</h3>
                      <button 
                        onClick={() => setActiveTab("Study Materials")}
                        className="text-sm text-primary-500 hover:text-primary-600 font-medium"
                      >
                        View All
                      </button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {mockDocuments.slice(0, 2).map((doc) => (
                        <LibraryCard key={doc.id} {...doc} />
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "Study Materials" && (
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-bold text-foreground">All Documents & Resources</h2>
                    <div className="flex gap-2">
                      <select className="bg-card border border-border rounded-lg px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary-500">
                        <option>All Types</option>
                        <option>Documents</option>
                        <option>Videos</option>
                        <option>Interactive</option>
                      </select>
                      <select className="bg-card border border-border rounded-lg px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary-500">
                        <option>Sort by Date</option>
                        <option>Sort by Mastery</option>
                      </select>
                    </div>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {mockDocuments.map((doc) => (
                      <LibraryCard key={doc.id} {...doc} />
                    ))}
                  </div>
                </div>
              )}

              {activeTab === "Assessments" && (
                <MistakeBook />
              )}

              {activeTab === "Archives" && (
                <div className="text-center py-20 bg-muted/30 rounded-2xl border border-dashed border-border">
                  <Archive className="mx-auto text-muted-foreground mb-4" size={48} />
                  <h3 className="text-xl font-semibold text-foreground">Tutor Chat Archives</h3>
                  <p className="text-muted-foreground mt-2 max-w-md mx-auto">
                    Past conversations with your AI Tutor will appear here. You haven&apos;t archived any sessions yet.
                  </p>
                </div>
              )}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Sidebar Widget */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-card border border-border rounded-2xl p-6 shadow-sm sticky top-24">
            <h3 className="font-semibold text-foreground mb-6 flex items-center gap-2">
              <Target className="text-primary-500" size={20} />
              Goal Progress
            </h3>
            
            <div className="space-y-6">
              {/* Readiness Score */}
              <div className="text-center">
                <div className="relative inline-flex items-center justify-center">
                  <svg className="w-32 h-32 transform -rotate-90">
                    <circle
                      cx="64"
                      cy="64"
                      r="56"
                      stroke="currentColor"
                      strokeWidth="12"
                      fill="transparent"
                      className="text-muted"
                    />
                    <circle
                      cx="64"
                      cy="64"
                      r="56"
                      stroke="currentColor"
                      strokeWidth="12"
                      fill="transparent"
                      strokeDasharray={351.85}
                      strokeDashoffset={351.85 - (351.85 * 65) / 100}
                      className="text-primary-500 transition-all duration-1000 ease-out"
                    />
                  </svg>
                  <div className="absolute flex flex-col items-center justify-center">
                    <span className="text-3xl font-bold text-foreground">65%</span>
                    <span className="text-xs text-muted-foreground font-medium">Readiness</span>
                  </div>
                </div>
              </div>

              {/* Skill Gap Stats */}
              <div className="space-y-4 pt-4 border-t border-border">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <CheckCircle2 size={16} className="text-green-500" />
                    Mastered Skills
                  </div>
                  <span className="font-semibold text-foreground">12</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <AlertCircle size={16} className="text-amber-500" />
                    Skill Gap (ΔS)
                  </div>
                  <span className="font-semibold text-foreground">8</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <BookOpen size={16} className="text-blue-500" />
                    Total Required
                  </div>
                  <span className="font-semibold text-foreground">20</span>
                </div>
              </div>

              <button className="w-full py-2.5 bg-primary-500/10 text-primary-600 dark:text-primary-400 rounded-xl font-medium hover:bg-primary-500/20 transition-colors">
                View Detailed Analysis
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
