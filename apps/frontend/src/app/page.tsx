import Link from "next/link";
import { ArrowRight, Sparkles, Target, Zap, Shield, CheckCircle2 } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";

export default function LandingPage() {
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
            Master any skill with your <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-500 to-primary-700 dark:from-primary-400 dark:to-primary-600">personal AI mentor</span>
          </h1>
          
          <p className="text-lg sm:text-xl text-slate-600 dark:text-slate-400 mb-10 max-w-2xl mx-auto leading-relaxed">
            GenMentor analyzes your goals, identifies your skill gaps, and generates a personalized, interactive curriculum to get you where you want to be.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/onboarding"
              className="w-full sm:w-auto flex items-center justify-center gap-2 bg-primary-500 text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-primary-600 transition-all shadow-lg shadow-primary-500/25 hover:shadow-primary-500/40 hover:-translate-y-0.5"
            >
              Start Learning Locally
              <ArrowRight size={20} />
            </Link>
            <Link
              href="#features"
              className="w-full sm:w-auto flex items-center justify-center gap-2 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 px-8 py-4 rounded-full text-lg font-semibold hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors shadow-sm"
            >
              View Demo
            </Link>
          </div>

          <div className="mt-16 flex items-center justify-center gap-8 text-sm font-medium text-slate-500 dark:text-slate-400 flex-wrap">
            <div className="flex items-center gap-2"><CheckCircle2 size={16} className="text-primary-500 dark:text-primary-400" /> No credit card required</div>
            <div className="flex items-center gap-2"><CheckCircle2 size={16} className="text-primary-500 dark:text-primary-400" /> Cancel anytime</div>
          </div>
        </div>
      </main>

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
    </div>
  );
}
