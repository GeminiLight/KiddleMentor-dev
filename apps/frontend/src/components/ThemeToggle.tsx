"use client";

import * as React from "react";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

interface ThemeToggleProps {
  variant?: "default" | "landing";
}

export function ThemeToggle({ variant = "default" }: ThemeToggleProps) {
  const { setTheme, theme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = React.useState(false);

  // Avoid hydration mismatch
  React.useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className={variant === "landing"
        ? "h-9 w-9 rounded-full bg-slate-100 dark:bg-slate-800 animate-pulse"
        : "h-9 w-9 rounded-full bg-muted animate-pulse"
      } />
    );
  }

  const toggleTheme = () => {
    setTheme(resolvedTheme === "dark" ? "light" : "dark");
  };

  const isDark = resolvedTheme === "dark";

  if (variant === "landing") {
    return (
      <button
        onClick={toggleTheme}
        className="relative flex h-9 w-9 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all duration-300 border border-slate-200 dark:border-slate-700 group"
        title={`Switch to ${isDark ? "light" : "dark"} mode`}
        aria-label="Toggle theme"
      >
        <div className="relative w-5 h-5">
          {/* Sun icon */}
          <Sun
            size={18}
            className={`absolute inset-0 transition-all duration-500 ${
              isDark
                ? "rotate-90 scale-0 opacity-0"
                : "rotate-0 scale-100 opacity-100"
            }`}
          />
          {/* Moon icon */}
          <Moon
            size={18}
            className={`absolute inset-0 transition-all duration-500 ${
              isDark
                ? "rotate-0 scale-100 opacity-100"
                : "-rotate-90 scale-0 opacity-0"
            }`}
          />
        </div>
        <span className="sr-only">Toggle theme</span>
      </button>
    );
  }

  // Default variant for dashboard/app pages
  return (
    <button
      onClick={toggleTheme}
      className="relative flex h-9 w-9 items-center justify-center rounded-full bg-muted text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-colors border border-border"
      title={`Switch to ${isDark ? "light" : "dark"} mode`}
      aria-label="Toggle theme"
    >
      {isDark ? <Moon size={18} /> : <Sun size={18} />}
      <span className="sr-only">Toggle theme</span>
    </button>
  );
}

