"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import { ArrowLeft, CheckCircle2, RefreshCw, ArrowRight, MessageSquarePlus, Star, Loader2, AlertCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import AITutorChat from "@/components/AITutorChat";
import { useGoal } from "@/components/GoalContext";
import { api, getStoredLearnerId } from "@/lib/api";
import { toast } from "sonner";

/* eslint-disable @typescript-eslint/no-explicit-any */

interface QuizQuestion {
  question: string;
  options: string[];
  correct_answer: string;
  explanation?: string;
}

export default function SessionPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const { currentGoal, refresh } = useGoal();

  const [activeTab, setActiveTab] = useState("learn");
  const [isCompleted, setIsCompleted] = useState(false);
  const [showXPAnimation, setShowXPAnimation] = useState(false);

  // Content state
  const [sessionData, setSessionData] = useState<Record<string, any> | null>(null);
  const [document, setDocument] = useState<string>("");
  const [quizzes, setQuizzes] = useState<QuizQuestion[]>([]);
  const [isLoadingContent, setIsLoadingContent] = useState(true);
  const [contentError, setContentError] = useState<string | null>(null);

  // Quiz state
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizScore, setQuizScore] = useState<number | null>(null);

  // Mark complete state
  const [isCompleting, setIsCompleting] = useState(false);

  // Text selection state
  const [selection, setSelection] = useState<{ text: string; x: number; y: number } | null>(null);
  const [externalQuery, setExternalQuery] = useState<string>("");
  const contentRef = useRef<HTMLDivElement>(null);

  // Load content on mount
  const loadContent = useCallback(async () => {
    setIsLoadingContent(true);
    setContentError(null);

    try {
      // Read session metadata from localStorage
      const rawSession = localStorage.getItem("current_session");
      if (!rawSession) {
        setContentError("No session data found. Please start from your learning path.");
        setIsLoadingContent(false);
        return;
      }
      const session = JSON.parse(rawSession);
      setSessionData(session);

      // Check for pre-fetched content
      const rawContent = localStorage.getItem("current_session_content");
      if (rawContent) {
        const content = JSON.parse(rawContent);
        parseContent(content);
        setIsLoadingContent(false);
        return;
      }

      // Fallback: fetch content directly (e.g. direct URL navigation)
      const rawRequest = localStorage.getItem("current_session_request");
      if (!rawRequest) {
        setContentError("No session request data found. Please start from your learning path.");
        setIsLoadingContent(false);
        return;
      }
      const request = JSON.parse(rawRequest);

      const result = await api.generateTailoredContent({
        learner_profile: { learner_id: request.learner_id },
        learning_path: request.learning_path,
        learning_session: request.learning_session,
        with_quiz: true,
        goal_id: request.goal_id,
      });

      localStorage.setItem("current_session_content", JSON.stringify(result.tailored_content));
      parseContent(result.tailored_content);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load content";
      setContentError(message);
      console.error("[SessionPage] Content load error:", err);
    } finally {
      setIsLoadingContent(false);
    }
  }, []);

  const parseContent = (content: any) => {
    // Extract markdown document
    if (typeof content === "string") {
      setDocument(content);
    } else if (content?.document) {
      setDocument(typeof content.document === "string" ? content.document : JSON.stringify(content.document, null, 2));
    } else if (content?.content) {
      setDocument(typeof content.content === "string" ? content.content : JSON.stringify(content.content, null, 2));
    } else {
      // Fallback: render the whole object as formatted text
      setDocument(JSON.stringify(content, null, 2));
    }

    // Extract quiz questions
    const quizData =
      content?.quizzes?.single_choice_questions ||
      content?.quiz?.single_choice_questions ||
      content?.quizzes?.questions ||
      content?.quiz?.questions ||
      content?.single_choice_questions ||
      (Array.isArray(content?.quizzes) ? content.quizzes : null) ||
      (Array.isArray(content?.quiz) ? content.quiz : null);

    if (Array.isArray(quizData) && quizData.length > 0) {
      setQuizzes(quizData);
    }
  };

  useEffect(() => {
    loadContent();
  }, [loadContent]);

  useEffect(() => {
    const handleSelection = () => {
      const sel = window.getSelection();
      if (sel && sel.toString().trim().length > 0 && contentRef.current?.contains(sel.anchorNode)) {
        const range = sel.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        setSelection({
          text: sel.toString().trim(),
          x: rect.left + rect.width / 2,
          y: rect.top - 10,
        });
      } else {
        setSelection(null);
      }
    };

    window.document.addEventListener("mouseup", handleSelection);
    return () => window.document.removeEventListener("mouseup", handleSelection);
  }, []);

  const handleAskTutor = () => {
    if (selection) {
      setExternalQuery(`Can you explain this part: "${selection.text}"?`);
      setSelection(null);
      window.getSelection()?.removeAllRanges();
    }
  };

  const handleSelectAnswer = (questionIndex: number, option: string) => {
    if (quizSubmitted) return;
    setSelectedAnswers((prev) => ({ ...prev, [questionIndex]: option }));
  };

  const handleSubmitQuiz = () => {
    if (quizzes.length === 0) return;

    let correct = 0;
    quizzes.forEach((q, idx) => {
      if (selectedAnswers[idx] === q.correct_answer) {
        correct++;
      }
    });

    const score = Math.round((correct / quizzes.length) * 100);
    setQuizScore(score);
    setQuizSubmitted(true);
  };

  const handleMarkComplete = async () => {
    if (isCompleted || isCompleting) return;

    const learnerId = getStoredLearnerId();
    if (!learnerId) {
      toast.error("Learner ID not found");
      return;
    }

    const sessionNumber = parseInt(params.id, 10);
    const goalId = currentGoal.goal_id;

    setIsCompleting(true);
    try {
      await api.completeSession(
        learnerId,
        sessionNumber,
        quizScore ?? undefined,
        undefined,
        goalId
      );

      setIsCompleted(true);
      setShowXPAnimation(true);
      setTimeout(() => setShowXPAnimation(false), 2000);
      toast.success("Session marked as complete!");

      // Refresh context so learning-path page reflects updated progress
      await refresh();
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to mark session complete";
      toast.error(message);
      console.error("[MarkComplete]", err);
    } finally {
      setIsCompleting(false);
    }
  };

  const sessionTitle = sessionData?.session_title || sessionData?.title || "Learning Session";
  const sessionNumber = params.id;

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
              x: "-50%",
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
            <h1 className="text-xl font-bold text-foreground">{sessionTitle}</h1>
            <p className="text-sm text-muted-foreground">Session {sessionNumber}</p>
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
            disabled={isCompleting}
            className={`flex items-center gap-2 px-6 py-2 rounded-full font-semibold transition-colors ${
              isCompleted
                ? "bg-green-500 text-white"
                : "bg-primary-500 text-white hover:bg-primary-600"
            } disabled:opacity-50`}
          >
            {isCompleted ? (
              <>
                <CheckCircle2 size={18} />
                Completed
              </>
            ) : isCompleting ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Saving...
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
                {isLoadingContent ? (
                  <div className="flex flex-col items-center justify-center py-20 gap-4">
                    <Loader2 size={40} className="animate-spin text-primary-500" />
                    <p className="text-muted-foreground text-lg">Generating personalized content...</p>
                    <p className="text-muted-foreground text-sm">This may take a moment while our AI tailors the material for you.</p>
                  </div>
                ) : contentError ? (
                  <div className="flex flex-col items-center justify-center py-20 gap-4">
                    <AlertCircle size={40} className="text-red-500" />
                    <p className="text-red-500 font-medium">{contentError}</p>
                    <button
                      onClick={() => router.push("/learning-path")}
                      className="flex items-center gap-2 text-primary-500 hover:text-primary-600 font-medium transition-colors"
                    >
                      <ArrowLeft size={18} />
                      Back to Learning Path
                    </button>
                  </div>
                ) : (
                  <>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {document}
                    </ReactMarkdown>

                    <div className="mt-12 flex items-center justify-between pt-6 border-t border-border not-prose">
                      <button
                        onClick={() => loadContent()}
                        className="flex items-center gap-2 text-muted-foreground hover:text-foreground font-medium transition-colors"
                      >
                        <RefreshCw size={18} />
                        Regenerate
                      </button>
                      {quizzes.length > 0 && (
                        <button
                          onClick={() => setActiveTab("quiz")}
                          className="flex items-center gap-2 text-primary-500 hover:text-primary-600 font-medium transition-colors"
                        >
                          Take Quiz
                          <ArrowRight size={18} />
                        </button>
                      )}
                    </div>
                  </>
                )}
              </div>
            ) : (
              <div className="space-y-8">
                <h2 className="text-2xl font-bold text-foreground">Knowledge Check</h2>

                {isLoadingContent ? (
                  <div className="flex flex-col items-center justify-center py-20 gap-4">
                    <Loader2 size={40} className="animate-spin text-primary-500" />
                    <p className="text-muted-foreground text-lg">Loading quiz questions...</p>
                  </div>
                ) : quizzes.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-20 gap-4">
                    <p className="text-muted-foreground">No quiz questions available for this session.</p>
                    <button
                      onClick={() => setActiveTab("learn")}
                      className="flex items-center gap-2 text-primary-500 hover:text-primary-600 font-medium transition-colors"
                    >
                      <ArrowLeft size={18} />
                      Back to Learn
                    </button>
                  </div>
                ) : (
                  <>
                    <div className="space-y-6">
                      {quizzes.map((q, qIdx) => (
                        <div
                          key={qIdx}
                          className={`p-6 rounded-xl border-2 bg-muted/30 ${
                            quizSubmitted
                              ? selectedAnswers[qIdx] === q.correct_answer
                                ? "border-green-500/50"
                                : "border-red-500/50"
                              : "border-border"
                          }`}
                        >
                          <p className="font-medium text-foreground mb-4">
                            {qIdx + 1}. {q.question}
                          </p>
                          <div className="space-y-3">
                            {q.options.map((option, oIdx) => {
                              const isSelected = selectedAnswers[qIdx] === option;
                              const isCorrect = option === q.correct_answer;

                              let optionStyle = "border-border bg-card hover:border-primary-500";
                              if (quizSubmitted) {
                                if (isCorrect) {
                                  optionStyle = "border-green-500 bg-green-500/10";
                                } else if (isSelected && !isCorrect) {
                                  optionStyle = "border-red-500 bg-red-500/10";
                                } else {
                                  optionStyle = "border-border bg-card opacity-60";
                                }
                              } else if (isSelected) {
                                optionStyle = "border-primary-500 bg-primary-500/10";
                              }

                              return (
                                <label
                                  key={oIdx}
                                  onClick={() => handleSelectAnswer(qIdx, option)}
                                  className={`flex items-center gap-3 p-4 rounded-lg border cursor-pointer transition-colors ${optionStyle}`}
                                >
                                  <input
                                    type="radio"
                                    name={`q${qIdx}`}
                                    checked={isSelected}
                                    onChange={() => handleSelectAnswer(qIdx, option)}
                                    disabled={quizSubmitted}
                                    className="w-4 h-4 text-primary-500 bg-background border-border"
                                  />
                                  <span className={`${isSelected && !quizSubmitted ? "text-foreground font-medium" : "text-muted-foreground"}`}>
                                    {option}
                                  </span>
                                  {quizSubmitted && isCorrect && (
                                    <CheckCircle2 size={16} className="ml-auto text-green-500" />
                                  )}
                                </label>
                              );
                            })}
                          </div>

                          {quizSubmitted && q.explanation && (
                            <div className="mt-4 p-3 rounded-lg bg-blue-500/5 border border-blue-500/20">
                              <p className="text-sm text-muted-foreground">
                                <span className="font-medium text-blue-500">Explanation: </span>
                                {q.explanation}
                              </p>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>

                    {quizSubmitted && quizScore !== null ? (
                      <div className="text-center p-6 rounded-xl bg-muted/50 border border-border">
                        <p className="text-2xl font-bold text-foreground mb-2">
                          Score: {quizScore}%
                        </p>
                        <p className="text-muted-foreground">
                          You got {quizzes.filter((q, idx) => selectedAnswers[idx] === q.correct_answer).length} out of {quizzes.length} correct.
                        </p>
                      </div>
                    ) : (
                      <button
                        onClick={handleSubmitQuiz}
                        disabled={Object.keys(selectedAnswers).length < quizzes.length}
                        className="w-full py-3 bg-foreground text-background rounded-xl font-semibold hover:opacity-90 transition-opacity disabled:opacity-50"
                      >
                        Submit Answers
                      </button>
                    )}
                  </>
                )}
              </div>
            )}
          </div>
        </div>

        {/* AI Tutor Sidebar */}
        <AITutorChat
          sessionId={params.id}
          externalQuery={externalQuery}
          onQueryProcessed={() => setExternalQuery("")}
          goalId={currentGoal.goal_id}
        />
      </div>
    </div>
  );
}
