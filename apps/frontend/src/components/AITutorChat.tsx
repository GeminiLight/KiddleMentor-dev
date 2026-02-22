"use client";

import { useState, useRef, useEffect } from "react";
import { ArrowRight, Loader2, Bot } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api/v1';

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export default function AITutorChat({ 
  sessionId, 
  externalQuery, 
  onQueryProcessed 
}: { 
  sessionId: string;
  externalQuery?: string;
  onQueryProcessed?: () => void;
}) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hi! I'm your AI Tutor. How can I help you with this session?",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [agentState, setAgentState] = useState<string>("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (externalQuery) {
      setInput(externalQuery);
      // Optionally auto-submit here, but let's just populate the input for now
      // or we can auto-submit by calling handleSubmit directly
      // Let's auto-submit
      const submitExternal = async () => {
        if (isLoading) return;
        
        const userMessage: Message = {
          id: Date.now().toString(),
          role: "user",
          content: externalQuery,
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setIsLoading(true);
        if (onQueryProcessed) onQueryProcessed();

        try {
          const response = await fetch(`${API_BASE_URL}/chat/chat-with-tutor`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              session_id: sessionId,
              message: userMessage.content,
            }),
          });

          if (!response.ok) {
            throw new Error("Failed to send message");
          }

          const data = await response.json();
          
          const assistantMessage: Message = {
            id: (Date.now() + 1).toString(),
            role: "assistant",
            content: data.response || "I'm sorry, I couldn't process that.",
          };

          setMessages((prev) => [...prev, assistantMessage]);
        } catch (error) {
          console.error("Chat error:", error);
          const errorMessage: Message = {
            id: (Date.now() + 1).toString(),
            role: "assistant",
            content: "Sorry, there was an error communicating with the server.",
          };
          setMessages((prev) => [...prev, errorMessage]);
        } finally {
          setIsLoading(false);
        }
      };
      
      submitExternal();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [externalQuery]);

  // Mock agent state changes during loading
  useEffect(() => {
    if (!isLoading) {
      setAgentState("");
      return;
    }

    const states = [
      "Content Expert is retrieving materials...",
      "Simulator is evaluating your context...",
      "Synthesizing response...",
    ];
    
    let currentIndex = 0;
    setAgentState(states[0]);
    
    const interval = setInterval(() => {
      currentIndex = (currentIndex + 1) % states.length;
      setAgentState(states[currentIndex]);
    }, 2000);

    return () => clearInterval(interval);
  }, [isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat/chat-with-tutor`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: userMessage.content,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to send message");
      }

      const data = await response.json();
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response || "I'm sorry, I couldn't process that.",
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Sorry, there was an error communicating with the server.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-80 border-l border-border bg-card flex flex-col shrink-0 h-full">
      <div className="p-4 border-b border-border flex flex-col gap-2 bg-muted/30 shrink-0 relative">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-primary-500/10 text-primary-500 flex items-center justify-center">
            <Bot size={18} />
          </div>
          <div>
            <h3 className="font-semibold text-foreground text-sm">AI Tutor</h3>
            <p className="text-xs text-muted-foreground">Always here to help</p>
          </div>
        </div>
        {isLoading && agentState && (
          <div className="text-[10px] text-primary-600 dark:text-primary-400 animate-pulse flex items-center gap-1">
            <Loader2 size={10} className="animate-spin" />
            {agentState}
          </div>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex flex-col ${
              msg.role === "user" ? "items-end" : "items-start"
            }`}
          >
            <div
              className={`max-w-[90%] rounded-2xl p-3 text-sm ${
                msg.role === "user"
                  ? "bg-primary-500 text-white rounded-tr-none"
                  : "bg-muted text-foreground rounded-tl-none border border-border/50"
              }`}
            >
              {msg.role === "assistant" ? (
                <div className="prose prose-sm dark:prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-slate-900 prose-pre:text-slate-50">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.content}
                  </ReactMarkdown>
                </div>
              ) : (
                msg.content
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-start">
            <div className="bg-muted rounded-2xl rounded-tl-none p-4 text-sm text-muted-foreground flex items-center gap-2 border border-border/50">
              <Loader2 size={16} className="animate-spin" />
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-border bg-card shrink-0">
        <form onSubmit={handleSubmit} className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            disabled={isLoading}
            className="w-full pl-4 pr-10 py-3 rounded-xl border border-border bg-background focus:border-primary-500 focus:ring-1 focus:ring-primary-500 outline-none text-sm text-foreground disabled:opacity-50 transition-all"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 text-primary-500 hover:bg-primary-500/10 rounded-lg transition-colors disabled:opacity-50 disabled:hover:bg-transparent"
          >
            <ArrowRight size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}
