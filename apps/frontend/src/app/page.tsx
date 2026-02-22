"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowRight, Sparkles, Target, Zap, Shield, CheckCircle2, Search, BrainCircuit, Map, Globe, Radar } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { motion, AnimatePresence } from "framer-motion";
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar as RechartsRadar, ResponsiveContainer } from "recharts";

const radarData = [
  { subject: 'Machine Learning', A: 40, B: 90, fullMark: 100 },
  { subject: 'Python', A: 60, B: 85, fullMark: 100 },
  { subject: 'Data Structures', A: 30, B: 80, fullMark: 100 },
  { subject: 'System Design', A: 20, B: 70, fullMark: 100 },
  { subject: 'SQL', A: 50, B: 85, fullMark: 100 },
  { subject: 'Deep Learning', A: 10, B: 75, fullMark: 100 },
];

export default function LandingPage() {
  const [goalInput, setGoalInput] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = () => {
    if (!goalInput.trim()) return;
    setIsGenerating(true);
    // Simulate generation
    setTimeout(() => {
      setIsGenerating(false);
      // In a real app, this would redirect to onboarding or learning path
    }, 4000);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 selection:bg-primary-100 selection:text-primary-900 dark:selection:bg-primary-900 dark:selection:text-primary-100">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-700 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center shadow-sm">
              <Sparkles className="text-white" size={18} />
            </div>
            <span className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">GenMentor</span>
          </div>
          <div className="flex items-center gap-4">
            <ThemeToggle variant="landing" />
            <Link href="/login" className="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors">
              Log in
            </Link>
            <Link
              href="/onboarding"
              className="text-sm font-medium bg-slate-900 dark:bg-white text-white dark:text-slate-900 px-4 py-2 rounded-full hover:bg-slate-800 dark:hover:bg-slate-100 transition-colors shadow-sm"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="pt-32 pb-16 sm:pt-40 sm:pb-24 lg:pb-32 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-50 dark:bg-primary-900/30 border border-primary-100 dark:border-primary-700/50 text-primary-700 dark:text-primary-300 text-sm font-medium mb-8 shadow-sm">
            <Sparkles size={14} />
            <span>AI-Powered Learning Paths</span>
          </div>
          
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold text-slate-900 dark:text-white tracking-tight mb-8 max-w-4xl mx-auto leading-[1.1]">
            Your Career Goal, <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-500 to-primary-700 dark:from-primary-400 dark:to-primary-600">Mapped by AI for the Shortest Path</span>
          </h1>
          
          <p className="text-lg sm:text-xl text-slate-600 dark:text-slate-400 mb-10 max-w-2xl mx-auto leading-relaxed">
            GenMentor analyzes your goals, identifies your skill gaps, and generates a personalized, interactive curriculum to get you where you want to be.
          </p>

          {/* Interactive Goal Input */}
          <div className="max-w-2xl mx-auto mb-12 relative z-10">
            <div className="relative flex items-center bg-white dark:bg-slate-900 rounded-full shadow-xl border border-slate-200 dark:border-slate-700 p-2 focus-within:ring-2 focus-within:ring-primary-500 transition-all">
              <div className="pl-4 text-slate-400">
                <Search size={20} />
              </div>
              <input 
                type="text"
                value={goalInput}
                onChange={(e) => setGoalInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
                placeholder="Enter your career goal (e.g., Become a Tencent AI Intern)"
                className="w-full bg-transparent border-none focus:outline-none px-4 py-3 text-slate-900 dark:text-white placeholder:text-slate-400"
              />
              <button 
                onClick={handleGenerate}
                disabled={isGenerating || !goalInput.trim()}
                className="bg-primary-500 text-white px-6 py-3 rounded-full font-semibold hover:bg-primary-600 transition-colors flex items-center gap-2 shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGenerating ? "Generating..." : "Generate Path"}
                {!isGenerating && <ArrowRight size={18} />}
              </button>
            </div>
          </div>

          {/* Animation Area */}
          <div className="h-48 max-w-3xl mx-auto relative">
            <AnimatePresence mode="wait">
              {!isGenerating ? (
                <motion.div 
                  key="idle"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="absolute inset-0 flex items-center justify-center text-slate-400 dark:text-slate-500"
                >
                  <p>Type a goal to see your AI mentor team in action</p>
                </motion.div>
              ) : (
                <motion.div 
                  key="generating"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="absolute inset-0 flex items-center justify-center gap-4 sm:gap-8"
                >
                  {/* Skill Identifier */}
                  <div className="flex flex-col items-center gap-3">
                    <motion.div 
                      animate={{ scale: [1, 1.1, 1], rotate: [0, 5, -5, 0] }}
                      transition={{ repeat: Infinity, duration: 2 }}
                      className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-2xl flex items-center justify-center border border-blue-200 dark:border-blue-800 shadow-sm"
                    >
                      <Target className="text-blue-500" size={28} />
                    </motion.div>
                    <div className="text-sm font-medium text-slate-700 dark:text-slate-300">Skill Identifier</div>
                    <div className="text-xs text-slate-500">Fetching JD...</div>
                  </div>

                  {/* Connection Line */}
                  <div className="w-16 sm:w-32 h-0.5 bg-slate-200 dark:bg-slate-700 relative overflow-hidden rounded-full">
                    <motion.div 
                      animate={{ x: ["-100%", "100%"] }}
                      transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                      className="absolute inset-0 bg-primary-500"
                    />
                  </div>

                  {/* Path Scheduler */}
                  <div className="flex flex-col items-center gap-3">
                    <motion.div 
                      animate={{ scale: [1, 1.1, 1], rotate: [0, -5, 5, 0] }}
                      transition={{ repeat: Infinity, duration: 2, delay: 0.5 }}
                      className="w-16 h-16 bg-emerald-100 dark:bg-emerald-900/30 rounded-2xl flex items-center justify-center border border-emerald-200 dark:border-emerald-800 shadow-sm"
                    >
                      <Map className="text-emerald-500" size={28} />
                    </motion.div>
                    <div className="text-sm font-medium text-slate-700 dark:text-slate-300">Path Scheduler</div>
                    <div className="text-xs text-slate-500">Drawing map...</div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <div className="mt-8 flex items-center justify-center gap-8 text-sm font-medium text-slate-500 dark:text-slate-400 flex-wrap">
            <div className="flex items-center gap-2"><CheckCircle2 size={16} className="text-primary-500 dark:text-primary-400" /> No credit card required</div>
            <div className="flex items-center gap-2"><CheckCircle2 size={16} className="text-primary-500 dark:text-primary-400" /> Cancel anytime</div>
          </div>
        </div>
      </main>

      {/* AI Mentor Team Section */}
      <section className="py-24 bg-slate-50 dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white tracking-tight mb-4">Your Dedicated AI Mentor Team</h2>
            <p className="text-lg text-slate-600 dark:text-slate-400">A specialized team of AI agents working together to accelerate your career.</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* Content Creator */}
            <div className="bg-white dark:bg-slate-900 rounded-3xl p-8 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-14 h-14 bg-amber-100 dark:bg-amber-900/30 rounded-2xl flex items-center justify-center border border-amber-200 dark:border-amber-800">
                  <Globe className="text-amber-500" size={28} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white">Content Creator</h3>
                  <p className="text-sm text-amber-600 dark:text-amber-400 font-medium">Real-time web search, learn only the latest tech</p>
                </div>
              </div>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                Scours the internet for the most up-to-date tutorials, documentation, and industry best practices to ensure your knowledge is always cutting-edge.
              </p>
            </div>

            {/* Learner Simulator */}
            <div className="bg-white dark:bg-slate-900 rounded-3xl p-8 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-14 h-14 bg-purple-100 dark:bg-purple-900/30 rounded-2xl flex items-center justify-center border border-purple-200 dark:border-purple-800">
                  <BrainCircuit className="text-purple-500" size={28} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 dark:text-white">Learner Simulator</h3>
                  <p className="text-sm text-purple-600 dark:text-purple-400 font-medium">Understands your bottlenecks better than you do</p>
                </div>
              </div>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                Models your cognitive state and predicts where you might struggle, pre-optimizing your learning path to avoid frustration and maximize retention.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* The Gap Map Section */}
      <section className="py-24 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-50 dark:bg-primary-900/30 border border-primary-100 dark:border-primary-700/50 text-primary-700 dark:text-primary-300 text-sm font-medium mb-6">
                <Radar size={16} />
                <span>The Gap Map</span>
              </div>
              <h2 className="text-3xl sm:text-4xl font-bold text-slate-900 dark:text-white tracking-tight mb-6">
                From Chaos to Clarity
              </h2>
              <p className="text-lg text-slate-600 dark:text-slate-400 mb-8 leading-relaxed">
                Visualize your exact skill gaps. We compare your current chaotic state against the clear mastery required for your target role, so you know exactly what to focus on.
              </p>
              <ul className="space-y-4">
                {[
                  "Identify missing critical skills instantly",
                  "Track your progress from S₀ to Target",
                  "Stop wasting time on things you already know"
                ].map((item, i) => (
                  <li key={i} className="flex items-center gap-3 text-slate-700 dark:text-slate-300 font-medium">
                    <CheckCircle2 className="text-primary-500" size={20} />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="bg-slate-50 dark:bg-slate-800/50 rounded-3xl p-8 border border-slate-200 dark:border-slate-700 h-[400px] flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                  <PolarGrid stroke="#cbd5e1" className="dark:stroke-slate-700" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 12 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                  <RechartsRadar
                    name="Current State"
                    dataKey="A"
                    stroke="#94a3b8"
                    fill="#94a3b8"
                    fillOpacity={0.3}
                  />
                  <RechartsRadar
                    name="Target Mastery"
                    dataKey="B"
                    stroke="#10b981"
                    fill="#10b981"
                    fillOpacity={0.5}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-white dark:bg-slate-900 border-t border-slate-100 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white tracking-tight mb-4">Everything you need to succeed</h2>
            <p className="text-lg text-slate-600 dark:text-slate-400">Stop guessing what to learn next. Our AI builds the perfect curriculum tailored specifically to your background and goals.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: <Target className="text-primary-500" size={24} />,
                title: "Goal-Oriented Paths",
                desc: "Tell us what you want to achieve, and we'll map out the exact steps to get there.",
              },
              {
                icon: <Zap className="text-amber-500" size={24} />,
                title: "Interactive Sessions",
                desc: "Learn by doing with AI-guided exercises, quizzes, and real-time feedback.",
              },
              {
                icon: <Shield className="text-emerald-500" size={24} />,
                title: "Skill Gap Analysis",
                desc: "We identify exactly what you're missing and focus your time only on what matters.",
              },
            ].map((feature, i) => (
              <div key={i} className="bg-slate-50 dark:bg-slate-800/50 rounded-3xl p-8 border border-slate-100 dark:border-slate-700 hover:border-primary-100 dark:hover:border-primary-700/60 hover:shadow-lg hover:shadow-primary-500/5 dark:hover:shadow-primary-500/10 transition-all group">
                <div className="w-12 h-12 bg-white dark:bg-slate-700 rounded-2xl flex items-center justify-center shadow-sm mb-6 group-hover:scale-110 transition-transform">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-3">{feature.title}</h3>
                <p className="text-slate-600 dark:text-slate-300 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-primary-500 dark:bg-primary-600 relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
        <div className="absolute -top-24 -right-24 w-96 h-96 bg-white/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-black/10 rounded-full blur-3xl pointer-events-none"></div>
        
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <h2 className="text-4xl sm:text-5xl font-bold text-white tracking-tight mb-6">
            Ready to accelerate your career?
          </h2>
          <p className="text-xl text-primary-100 mb-10 max-w-2xl mx-auto">
            Join thousands of learners who are reaching their goals faster with personalized AI mentorship.
          </p>
          <Link
            href="/onboarding"
            className="inline-flex items-center justify-center gap-2 bg-white text-primary-600 px-8 py-4 rounded-full text-lg font-bold hover:bg-slate-50 hover:scale-105 transition-all shadow-xl shadow-black/10"
          >
            Get Started for Free
            <ArrowRight size={20} />
          </Link>
          <p className="mt-6 text-sm text-primary-200">
            No credit card required. Start learning in seconds.
          </p>
        </div>
      </section>
    </div>
  );
}
