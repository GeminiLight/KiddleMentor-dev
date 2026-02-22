"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, CheckCircle2, BookOpen, RefreshCw, ArrowRight, MessageSquarePlus, Star } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

import AITutorChat from "@/components/AITutorChat";

export default function SessionPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState("learn");
  const [isCompleted, setIsCompleted] = useState(false);
  const [showXPAnimation, setShowXPAnimation] = useState(false);
  
  // Text selection state
  const [selection, setSelection] = useState<{ text: string; x: number; y: number } | null>(null);
  const [externalQuery, setExternalQuery] = useState<string>("");
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleSelection = () => {
      const sel = window.getSelection();
      if (sel && sel.toString().trim().length > 0 && contentRef.current?.contains(sel.anchorNode)) {
        const range = sel.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        setSelection({
          text: sel.toString().trim(),
          x: rect.left + rect.width / 2,
          y: rect.top - 10, // Position above the selection
        });
      } else {
        setSelection(null);
      }
    };

    document.addEventListener("mouseup", handleSelection);
    return () => document.removeEventListener("mouseup", handleSelection);
  }, []);

  const handleAskTutor = () => {
    if (selection) {
      setExternalQuery(`Can you explain this part: "${selection.text}"?`);
      setSelection(null);
      window.getSelection()?.removeAllRanges();
    }
  };

  const handleMarkComplete = () => {
    if (!isCompleted) {
      setIsCompleted(true);
      setShowXPAnimation(true);
      setTimeout(() => setShowXPAnimation(false), 2000);
    }
  };

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col -m-8 relative overflow-hidden">
      {/* XP Fly-in Animation */}
      <AnimatePresence>
        {showXPAnimation && (
          <motion.div
            initial={{ opacity: 0, scale: 0.5, y: 0, x: "-50%" }}
            animate={{ 
              opacity: [0, 1, 1, 0], 
              scale: [0.5, 1.2, 1, 0.8], 
              y: [0, -100, -200, -300],
              x: "-50%"
            }}
            exit={{ opacity: 0 }}
            transition={{ duration: 2, ease: "easeOut" }}
            className="fixed left-1/2 top-1/2 z-50 flex flex-col items-center pointer-events-none"
          >
            <div className="bg-amber-500 text-white px-6 py-3 rounded-full font-black text-2xl shadow-2xl shadow-amber-500/50 flex items-center gap-2 border-4 border-white dark:border-slate-900">
              <Star fill="currentColor" size={28} className="animate-spin-slow" />
              +50 XP
            </div>
            <div className="text-amber-500 font-bold mt-2 text-lg drop-shadow-md">Session Completed!</div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Floating Ask Tutor Button */}
      {selection && (
        <button
          onClick={handleAskTutor}
          style={{
            position: "fixed",
            left: `${selection.x}px`,
            top: `${selection.y}px`,
            transform: "translate(-50%, -100%)",
            zIndex: 50,
          }}
          className="flex items-center gap-2 px-3 py-1.5 bg-primary-500 text-white text-sm font-medium rounded-lg shadow-lg hover:bg-primary-600 transition-colors animate-in fade-in zoom-in duration-200"
        >
          <MessageSquarePlus size={16} />
          Ask AI Tutor
        </button>
      )}

      {/* Header */}
      <header className="flex items-center justify-between px-8 py-4 border-b border-border bg-card shrink-0">
        <div className="flex items-center gap-4">
          <button
            onClick={() => router.push("/learning-path")}
            className="p-2 rounded-full hover:bg-muted text-muted-foreground transition-colors"
          >
            <ArrowLeft size={20} />
          </button>
          <div>
            <h1 className="text-xl font-bold text-foreground">Variables and Data Types</h1>
            <p className="text-sm text-muted-foreground">Session 2 • Python Fundamentals</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex bg-muted p-1 rounded-lg">
            <button
              onClick={() => setActiveTab("learn")}
              className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
                activeTab === "learn"
                  ? "bg-card text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Learn
            </button>
            <button
              onClick={() => setActiveTab("quiz")}
              className={`px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${
                activeTab === "quiz"
                  ? "bg-card text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Quiz
            </button>
          </div>
          <button
            onClick={handleMarkComplete}
            className={`flex items-center gap-2 px-6 py-2 rounded-full font-semibold transition-colors ${
              isCompleted
                ? "bg-green-500 text-white"
                : "bg-primary-500 text-white hover:bg-primary-600"
            }`}
          >
            {isCompleted ? (
              <>
                <CheckCircle2 size={18} />
                Completed
              </>
            ) : (
              "Mark Complete"
            )}
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Document/Quiz Panel */}
        <div className="flex-1 overflow-y-auto p-8 bg-background" ref={contentRef}>
          <div className="max-w-3xl mx-auto bg-card rounded-2xl shadow-sm border border-border p-8 md:p-12">
            {activeTab === "learn" ? (
              <div className="prose prose-slate dark:prose-invert max-w-none">
                <h2 className="text-3xl font-bold text-foreground mb-6">Understanding Variables</h2>
                <p className="text-lg text-muted-foreground leading-relaxed mb-6">
                  Think of a variable as a labeled box where you can store data. Just like you might label a box &quot;Books&quot; and put books inside it, in Python, you can label a variable `age` and store the number `25` inside it.
                </p>
                
                <div className="bg-slate-900 dark:bg-black rounded-xl p-6 mb-8 border border-slate-800">
                  <pre className="text-slate-50 font-mono text-sm">
                    <code>
                      <span className="text-primary-400"># Creating variables</span>{"\n"}
                      name = <span className="text-green-400">&quot;Alice&quot;</span>{"\n"}
                      age = <span className="text-orange-400">25</span>{"\n"}
                      is_student = <span className="text-purple-400">True</span>
                    </code>
                  </pre>
                </div>

                <h3 className="text-2xl font-semibold text-foreground mb-4">Data Types</h3>
                <ul className="space-y-4 text-muted-foreground">
                  <li className="flex items-start gap-3">
                    <div className="mt-1 bg-primary-500/10 text-primary-500 p-1 rounded">
                      <BookOpen size={16} />
                    </div>
                    <div>
                      <strong className="text-foreground">Strings (str):</strong> Text data, enclosed in quotes. e.g., &quot;Hello&quot;
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <div className="mt-1 bg-green-500/10 text-green-500 p-1 rounded">
                      <BookOpen size={16} />
                    </div>
                    <div>
                      <strong className="text-foreground">Integers (int):</strong> Whole numbers. e.g., 42
                    </div>
                  </li>
                </ul>

                <div className="mt-12 flex items-center justify-between pt-6 border-t border-border">
                  <button className="flex items-center gap-2 text-muted-foreground hover:text-foreground font-medium transition-colors">
                    <RefreshCw size={18} />
                    Explain Simpler
                  </button>
                  <button
                    onClick={() => setActiveTab("quiz")}
                    className="flex items-center gap-2 text-primary-500 hover:text-primary-600 font-medium transition-colors"
                  >
                    Take Quiz
                    <ArrowRight size={18} />
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-8">
                <h2 className="text-2xl font-bold text-foreground">Knowledge Check</h2>
                
                <div className="space-y-6">
                  <div className="p-6 rounded-xl border-2 border-border bg-muted/30">
                    <p className="font-medium text-foreground mb-4">
                      1. Which of the following is a valid string in Python?
                    </p>
                    <div className="space-y-3">
                      {["42", "True", '&quot;Hello World&quot;', "None"].map((option, i) => (
                        <label
                          key={i}
                          className="flex items-center gap-3 p-4 rounded-lg border border-border bg-card hover:border-primary-500 cursor-pointer transition-colors"
                        >
                          <input type="radio" name="q1" className="w-4 h-4 text-primary-500 bg-background border-border" />
                          <span className="text-muted-foreground">{option}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                </div>

                <button className="w-full py-3 bg-foreground text-background rounded-xl font-semibold hover:opacity-90 transition-opacity">
                  Submit Answers
                </button>
              </div>
            )}
          </div>
        </div>

        {/* AI Tutor Sidebar */}
        <AITutorChat 
          sessionId={params.id} 
          externalQuery={externalQuery} 
          onQueryProcessed={() => setExternalQuery("")} 
        />
      </div>
    </div>
  );
}
