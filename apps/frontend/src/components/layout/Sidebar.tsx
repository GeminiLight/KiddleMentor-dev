"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  Home,
  Map,
  BookOpen,
  Activity,
  Settings,
  Target,
} from "lucide-react";

const navItems = [
  { name: "Home", href: "/progress", icon: Home },
  { name: "Roadmap", href: "/learning-path", icon: Map },
  { name: "Library", href: "/library", icon: BookOpen },
  { name: "Skills", href: "/skill-gap", icon: Activity },
  { name: "Settings", href: "/profile", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-full w-64 flex-col border-r border-border bg-card px-4 py-6">
      <nav className="flex flex-1 flex-col gap-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary-50 dark:bg-primary-950/30 text-primary-700 dark:text-primary-400"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <item.icon 
                size={18} 
                className={cn(
                  isActive ? "text-primary-600" : "text-muted-foreground"
                )} 
              />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto space-y-4">
        <Link
          href="/goals"
          className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
        >
          <Target size={18} className="text-muted-foreground" />
          Manage My Goals
        </Link>
        <div className="rounded-xl bg-muted p-4 border border-border">
          <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">Progress</h4>
          <p className="text-sm font-medium text-foreground">Senior Data Analyst</p>
          <div className="mt-3 flex items-center gap-2">
            <div className="h-1.5 flex-1 rounded-full bg-secondary overflow-hidden">
              <div className="h-full w-[45%] rounded-full bg-primary-500" />
            </div>
            <span className="text-xs font-medium text-muted-foreground">45%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
