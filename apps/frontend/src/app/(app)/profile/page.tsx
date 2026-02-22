"use client";

import { User, Mail, Shield, Bell, LogOut, Settings, Award, Clock, Flame } from "lucide-react";
import { cn } from "@/lib/utils";

export default function ProfilePage() {
  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Profile</h1>
        <p className="mt-2 text-muted-foreground">Manage your account settings and view your achievements.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Profile Card & Stats */}
        <div className="lg:col-span-1 space-y-8">
          <div className="bg-card rounded-2xl shadow-sm border border-border p-8 text-center">
            <div className="relative inline-block mb-4">
              <div className="w-24 h-24 rounded-full bg-primary-50 dark:bg-primary-950/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
                <User size={48} />
              </div>
              <button className="absolute bottom-0 right-0 p-1.5 bg-card rounded-full border border-border text-muted-foreground hover:text-primary-600 dark:hover:text-primary-400 transition-colors shadow-sm">
                <Settings size={14} />
              </button>
            </div>
            <h2 className="text-xl font-bold text-foreground">Alex Johnson</h2>
            <p className="text-sm text-muted-foreground mb-6">Learning Data Science</p>
            
            <div className="flex justify-center gap-4 py-4 border-t border-border">
              <div className="text-center">
                <p className="text-lg font-bold text-foreground">12</p>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold">Sessions</p>
              </div>
              <div className="w-px h-8 bg-border self-center" />
              <div className="text-center">
                <p className="text-lg font-bold text-foreground">3d</p>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold">Streak</p>
              </div>
              <div className="w-px h-8 bg-border self-center" />
              <div className="text-center">
                <p className="text-lg font-bold text-foreground">4</p>
                <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold">Badges</p>
              </div>
            </div>
          </div>

          <div className="bg-card rounded-2xl shadow-sm border border-border p-6">
            <h3 className="font-bold text-foreground mb-4">Quick Stats</h3>
            <div className="space-y-4">
              {[
                { label: "Total Learning Time", value: "24.5 Hours", icon: Clock, color: "text-blue-600 dark:text-blue-400", bg: "bg-blue-50 dark:bg-blue-950/30" },
                { label: "Longest Streak", value: "7 Days", icon: Flame, color: "text-orange-600 dark:text-orange-400", bg: "bg-orange-50 dark:bg-orange-950/30" },
                { label: "Skills in Progress", value: "6 Skills", icon: Award, color: "text-purple-600 dark:text-purple-400", bg: "bg-purple-50 dark:bg-purple-950/30" },
              ].map((stat, i) => (
                <div key={i} className="flex items-center gap-3">
                  <div className={cn("w-8 h-8 rounded-lg flex items-center justify-center", stat.bg, stat.color)}>
                    <stat.icon size={16} />
                  </div>
                  <div>
                    <p className="text-[10px] text-muted-foreground font-semibold uppercase tracking-wider">{stat.label}</p>
                    <p className="text-sm font-bold text-foreground">{stat.value}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Settings */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-card rounded-2xl shadow-sm border border-border overflow-hidden">
            <div className="p-6 border-b border-border">
              <h3 className="font-bold text-foreground">Account Settings</h3>
            </div>
            <div className="divide-y divide-border">
              {[
                { label: "Email Address", value: "alex.j@example.com", icon: Mail },
                { label: "Password", value: "••••••••••••", icon: Shield },
                { label: "Notifications", value: "Enabled", icon: Bell },
              ].map((item, i) => (
                <button key={i} className="w-full flex items-center justify-between p-6 hover:bg-muted/50 transition-colors text-left group">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-xl bg-muted/50 text-muted-foreground group-hover:text-primary-600 dark:group-hover:text-primary-400 group-hover:bg-primary-50 dark:group-hover:bg-primary-950/30 transition-colors flex items-center justify-center">
                      <item.icon size={20} />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-foreground">{item.label}</p>
                      <p className="text-sm text-muted-foreground">{item.value}</p>
                    </div>
                  </div>
                  <span className="text-xs font-semibold text-primary-600 dark:text-primary-400 opacity-0 group-hover:opacity-100 transition-opacity">Edit</span>
                </button>
              ))}
            </div>
          </div>

          <div className="bg-card rounded-2xl shadow-sm border border-border overflow-hidden">
            <div className="p-6 border-b border-border">
              <h3 className="font-bold text-foreground">Danger Zone</h3>
            </div>
            <div className="p-6 space-y-4">
              <p className="text-sm text-muted-foreground leading-relaxed">
                Once you delete your account, there is no going back. Please be certain.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <button className="flex items-center justify-center gap-2 px-6 py-2.5 rounded-xl border border-border text-muted-foreground font-semibold hover:bg-muted/50 transition-colors">
                  <LogOut size={18} />
                  Log Out
                </button>
                <button className="flex items-center justify-center gap-2 px-6 py-2.5 rounded-xl bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400 font-semibold hover:bg-red-100 dark:hover:bg-red-900/50 transition-colors">
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
