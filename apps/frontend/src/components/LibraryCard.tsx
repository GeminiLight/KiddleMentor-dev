"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, FileText, BookOpen, Clock } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface LibraryCardProps {
  id: string;
  title: string;
  type: "document" | "video" | "interactive";
  mastery: number; // 0 to 100
  skills: string[];
  date: string;
  duration: string;
  aiSummary?: string;
}

export function LibraryCard({
  title,
  type,
  mastery,
  skills,
  date,
  duration,
  aiSummary,
}: LibraryCardProps) {
  const [isSummaryOpen, setIsSummaryOpen] = useState(false);
  const [isLoadingSummary, setIsLoadingSummary] = useState(false);
  const [summary, setSummary] = useState(aiSummary);

  const handleToggleSummary = () => {
    if (!isSummaryOpen && !summary) {
      setIsLoadingSummary(true);
      setIsSummaryOpen(true);
      // Simulate AI generation
      setTimeout(() => {
        setSummary(
          "- **Core Concept**: Understand the fundamental principles of this topic.\n- **Key Application**: Learn how to apply these concepts in real-world scenarios.\n- **Common Pitfall**: Avoid typical mistakes by following best practices."
        );
        setIsLoadingSummary(false);
      }, 1500);
    } else {
      setIsSummaryOpen(!isSummaryOpen);
    }
  };

  return (
    <div className="bg-card border border-border rounded-2xl p-5 shadow-sm hover:shadow-md transition-shadow group">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-primary-500/10 text-primary-600 dark:text-primary-400 rounded-xl">
            {type === "document" ? <FileText size={20} /> : <BookOpen size={20} />}
          </div>
          <div>
            <h3 className="font-semibold text-foreground text-lg group-hover:text-primary-500 transition-colors">
              {title}
            </h3>
            <div className="flex items-center gap-3 text-xs text-muted-foreground mt-1">
              <span className="flex items-center gap-1">
                <Clock size={12} />
                {duration}
              </span>
              <span>•</span>
              <span>{date}</span>
            </div>
          </div>
        </div>
        <button
          onClick={handleToggleSummary}
          className={`p-2 rounded-full transition-colors ${
            isSummaryOpen
              ? "bg-amber-500/10 text-amber-500"
              : "bg-muted text-muted-foreground hover:bg-amber-500/10 hover:text-amber-500"
          }`}
          title="AI Summary"
        >
          <Sparkles size={18} />
        </button>
      </div>

      {/* Mastery Progress */}
      <div className="mb-4">
        <div className="flex items-center justify-between text-xs mb-1.5">
          <span className="text-muted-foreground font-medium">Cognitive Status (S)</span>
          <span className="text-foreground font-semibold">{mastery}%</span>
        </div>
        <div className="h-2 bg-muted rounded-full overflow-hidden">
          <div
            className="h-full bg-primary-500 rounded-full transition-all duration-1000"
            style={{ width: `${mastery}%` }}
          />
        </div>
      </div>

      {/* Skills */}
      <div className="flex flex-wrap gap-2 mb-2">
        {skills.map((skill) => (
          <span
            key={skill}
            className="px-2.5 py-1 bg-secondary text-secondary-foreground text-xs font-medium rounded-md"
          >
            {skill}
          </span>
        ))}
      </div>

      {/* AI Summary Expandable Area */}
      <AnimatePresence>
        {isSummaryOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="mt-4 pt-4 border-t border-border">
              <div className="flex items-center gap-2 text-amber-500 font-medium text-sm mb-3">
                <Sparkles size={16} />
                AI Knowledge Summary
              </div>
              
              {isLoadingSummary ? (
                <div className="space-y-2">
                  <div className="h-4 bg-muted rounded animate-pulse w-3/4" />
                  <div className="h-4 bg-muted rounded animate-pulse w-5/6" />
                  <div className="h-4 bg-muted rounded animate-pulse w-2/3" />
                </div>
              ) : (
                <div className="prose prose-sm dark:prose-invert max-w-none prose-p:leading-relaxed prose-li:marker:text-amber-500">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {summary || ""}
                  </ReactMarkdown>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
