"use client";

import Link from "next/link";
import { Bell, User, BookOpen } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";

export function Topbar() {
  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-card px-8">
      <div className="flex items-center gap-8">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-500 text-white">
            <BookOpen size={18} strokeWidth={2.5} />
          </div>
          <span className="text-xl font-bold text-foreground tracking-tight">GenMentor</span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <ThemeToggle />
        <button className="relative rounded-full p-2 text-muted-foreground hover:bg-muted transition-colors">
          <Bell size={18} />
          <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-red-500 ring-2 ring-card" />
        </button>
        <Link 
          href="/profile"
          className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400 hover:bg-primary-200 dark:hover:bg-primary-900/80 transition-colors"
        >
          <User size={18} />
        </Link>
      </div>
    </header>
  );
}
