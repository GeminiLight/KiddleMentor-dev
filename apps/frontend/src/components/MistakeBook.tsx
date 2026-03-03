"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AlertCircle, CheckCircle2, XCircle, Lightbulb, ChevronDown, ChevronUp } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useGoal } from "@/components/GoalContext";

/* eslint-disable @typescript-eslint/no-explicit-any */

interface MistakeItemProps {
  id: string;
  question: string;
  wrongAnswer: string;
  correctAnswer: string;
  keyInsight: string;
  confidenceLevel: "Low" | "Medium" | "High";
  date: string;
  skill: string;
}

function MistakeItem({
  question,
  wrongAnswer,
  correctAnswer,
  keyInsight,
  confidenceLevel,
  date,
  skill,
}: MistakeItemProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const confidenceColors = {
    Low: "bg-red-500/10 text-red-600 dark:text-red-400 border-red-500/20",
    Medium: "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20",
    High: "bg-green-500/10 text-green-600 dark:text-green-400 border-green-500/20",
  };

  return (
    <div className="bg-card border border-border rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
      <div
        className="p-5 cursor-pointer flex items-start justify-between gap-4"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <span className={`px-2.5 py-1 text-xs font-semibold rounded-full border ${confidenceColors[confidenceLevel]}`}>
              Confidence: {confidenceLevel}
            </span>
            <span className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded-md">
              {skill}
            </span>
            <span className="text-xs text-muted-foreground">{date}</span>
          </div>
          <h4 className="font-medium text-foreground text-base leading-relaxed">
            {question}
          </h4>
        </div>
        <button className="p-2 hover:bg-muted rounded-full transition-colors text-muted-foreground">
          {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-t border-border bg-muted/30"
          >
            <div className="p-5 space-y-6">
              {/* Answers Comparison */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-red-500/5 border border-red-500/20 rounded-xl p-4">
                  <div className="flex items-center gap-2 text-red-600 dark:text-red-400 font-medium mb-2 text-sm">
                    <XCircle size={16} />
                    Your Answer
                  </div>
                  <p className="text-foreground text-sm">{wrongAnswer}</p>
                </div>
                <div className="bg-green-500/5 border border-green-500/20 rounded-xl p-4">
                  <div className="flex items-center gap-2 text-green-600 dark:text-green-400 font-medium mb-2 text-sm">
                    <CheckCircle2 size={16} />
                    Correct Answer
                  </div>
                  <p className="text-foreground text-sm">{correctAnswer}</p>
                </div>
              </div>

              {/* AI Key Insight */}
              {keyInsight && (
                <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-4 relative overflow-hidden">
                  <div className="absolute -right-6 -top-6 w-24 h-24 bg-amber-500/10 rounded-full blur-2xl pointer-events-none" />
                  <div className="flex items-start gap-3 relative z-10">
                    <div className="p-2 bg-amber-500/10 text-amber-600 dark:text-amber-400 rounded-lg shrink-0">
                      <Lightbulb size={18} />
                    </div>
                    <div>
                      <h5 className="font-semibold text-amber-700 dark:text-amber-400 text-sm mb-1">
                        AI Key Insight
                      </h5>
                      <div className="prose prose-sm dark:prose-invert max-w-none text-amber-900/80 dark:text-amber-100/80">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {keyInsight}
                        </ReactMarkdown>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export function MistakeBook() {
  const { currentGoal, learner } = useGoal();
  const [filter, setFilter] = useState<"All" | "Low" | "Medium" | "High">("All");

  // Extract quiz mistakes from completed sessions' stored quiz data
  const goalId = currentGoal.goal_id;
  const pathData = learner.learningPath[goalId];
  const rawSessions = pathData?.learning_path;
  const sessionsArray: Record<string, any>[] = Array.isArray(rawSessions)
    ? rawSessions
    : Array.isArray(rawSessions?.learning_path)
      ? rawSessions.learning_path
      : [];

  const mistakes: MistakeItemProps[] = [];
  let mistakeId = 0;

  sessionsArray.forEach((session, sessionIdx) => {
    if (!session.completed && !session.if_learned) return;

    // Try to extract quiz results from session data
    const quizResults = session.quiz_results || session.quizResults;
    if (!quizResults) return;

    const questions: any[] =
      quizResults.single_choice_questions ||
      quizResults.questions ||
      (Array.isArray(quizResults) ? quizResults : []);

    questions.forEach((q: any) => {
      // Only include wrong answers
      if (!q.user_answer && !q.userAnswer) return;
      const userAnswer = q.user_answer || q.userAnswer;
      const correctAnswer = q.correct_answer || q.correctAnswer;
      if (userAnswer === correctAnswer) return;

      mistakeId++;
      const quizScore = session.quiz_score ?? 50;
      const confidence: "Low" | "Medium" | "High" =
        quizScore >= 80 ? "High" : quizScore >= 50 ? "Medium" : "Low";

      mistakes.push({
        id: String(mistakeId),
        question: q.question || `Question from Session ${sessionIdx + 1}`,
        wrongAnswer: userAnswer,
        correctAnswer: correctAnswer,
        keyInsight: q.explanation || "",
        confidenceLevel: confidence,
        date: session.completed_at || "Completed",
        skill: (Array.isArray(session.associated_skills) && session.associated_skills[0])
          ? session.associated_skills[0]
          : session.session_title || `Session ${sessionIdx + 1}`,
      });
    });
  });

  const filteredMistakes = filter === "All"
    ? mistakes
    : mistakes.filter(m => m.confidenceLevel === filter);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-foreground flex items-center gap-2">
            <AlertCircle className="text-red-500" size={24} />
            Smart Mistake Book
          </h2>
          <p className="text-muted-foreground text-sm mt-1">
            Review and re-attempt questions you missed to strengthen your active recall.
          </p>
        </div>

        {mistakes.length > 0 && (
          <div className="flex items-center gap-2 bg-muted p-1 rounded-lg">
            {["All", "Low", "Medium", "High"].map((level) => (
              <button
                key={level}
                onClick={() => setFilter(level as "All" | "Low" | "Medium" | "High")}
                className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${
                  filter === level
                    ? "bg-background text-foreground shadow-sm"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {level}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="space-y-4">
        {filteredMistakes.map((mistake) => (
          <MistakeItem key={mistake.id} {...mistake} />
        ))}

        {mistakes.length === 0 && (
          <div className="text-center py-12 bg-muted/30 rounded-2xl border border-dashed border-border">
            <CheckCircle2 className="mx-auto text-green-500 mb-3" size={32} />
            <h3 className="text-foreground font-medium">No mistakes recorded yet</h3>
            <p className="text-muted-foreground text-sm mt-1">Complete quizzes during sessions to track your mistakes here.</p>
          </div>
        )}

        {mistakes.length > 0 && filteredMistakes.length === 0 && (
          <div className="text-center py-12 bg-muted/30 rounded-2xl border border-dashed border-border">
            <CheckCircle2 className="mx-auto text-green-500 mb-3" size={32} />
            <h3 className="text-foreground font-medium">No mistakes found!</h3>
            <p className="text-muted-foreground text-sm mt-1">You&apos;ve mastered all concepts in this category.</p>
          </div>
        )}
      </div>
    </div>
  );
}
