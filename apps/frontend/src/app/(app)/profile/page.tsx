"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { User, Shield, Bell, AlertTriangle, Globe, Mic, FileText, Sliders, Settings, Palette, Loader2 } from "lucide-react";
import { api, getStoredLearnerId } from "@/lib/api";
import { useGoal } from "@/components/GoalContext";

export default function ProfilePage() {
  const router = useRouter();
  const { resetLearner } = useGoal();
  const [activeTab, setActiveTab] = useState("information");
  const [isDeleting, setIsDeleting] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);

  const tabs = [
    { id: "information", label: "Information", icon: User },
    { id: "preferences", label: "Preferences", icon: Sliders },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Profile & Settings</h1>
        <p className="mt-2 text-muted-foreground">Manage your personal information, preferences, and account settings.</p>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        {/* Sidebar Navigation */}
        <div className="w-full md:w-64 shrink-0 space-y-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-colors ${
                activeTab === tab.id
                  ? "bg-primary-50 dark:bg-primary-950/30 text-primary-600 dark:text-primary-400"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              }`}
            >
              <tab.icon size={18} />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Main Content Area */}
        <div className="flex-1 space-y-8">
          {activeTab === "information" && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-300">
              <div className="bg-card rounded-2xl shadow-sm border border-border p-8">
                <h3 className="text-xl font-bold text-foreground mb-6">User Information</h3>
                <div className="space-y-6">
                  <div className="flex items-center gap-6">
                    <div className="w-20 h-20 rounded-full bg-primary-50 dark:bg-primary-950/30 flex items-center justify-center text-primary-600 dark:text-primary-400">
                      <User size={32} />
                    </div>
                    <div>
                      <button className="bg-background border border-border text-foreground px-4 py-2 rounded-xl text-sm font-semibold hover:bg-muted transition-colors">
                        Change Avatar
                      </button>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <label className="text-sm font-semibold text-foreground">First Name</label>
                      <input type="text" defaultValue="Alex" className="w-full bg-background border border-border rounded-xl px-4 py-2.5 text-foreground focus:outline-none focus:ring-2 focus:ring-primary-500" />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-semibold text-foreground">Last Name</label>
                      <input type="text" defaultValue="Johnson" className="w-full bg-background border border-border rounded-xl px-4 py-2.5 text-foreground focus:outline-none focus:ring-2 focus:ring-primary-500" />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-foreground">Bio</label>
                    <textarea defaultValue="Passionate about turning raw data into actionable insights." className="w-full bg-background border border-border rounded-xl px-4 py-2.5 text-foreground focus:outline-none focus:ring-2 focus:ring-primary-500 min-h-[100px] resize-none" />
                  </div>
                </div>
              </div>

              <div className="bg-card rounded-2xl shadow-sm border border-border p-8">
                <h3 className="text-xl font-bold text-foreground mb-6 flex items-center gap-2">
                  <FileText size={20} className="text-primary-500" />
                  Context Connector
                </h3>
                <p className="text-sm text-muted-foreground mb-6">
                  Upload your latest resume or context document to help GenMentor better understand your background and adjust your learning path.
                </p>
                <div className="border-2 border-dashed border-border rounded-2xl p-8 text-center hover:bg-muted/30 transition-colors cursor-pointer">
                  <FileText size={32} className="mx-auto text-muted-foreground mb-4" />
                  <p className="font-semibold text-foreground">Click to upload or drag and drop</p>
                  <p className="text-sm text-muted-foreground mt-1">PDF, DOCX up to 5MB</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === "preferences" && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-300">
              <div className="bg-card rounded-2xl shadow-sm border border-border p-8">
                <h3 className="text-xl font-bold text-foreground mb-6">App Preferences</h3>
                <div className="space-y-6">
                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-foreground flex items-center gap-2">
                      <Palette size={16} className="text-primary-500" />
                      Theme Style
                    </label>
                    <select className="w-full bg-background border border-border rounded-xl px-4 py-2.5 text-foreground focus:outline-none focus:ring-2 focus:ring-primary-500">
                      <option>System Default</option>
                      <option>Light Mode</option>
                      <option>Dark Mode</option>
                    </select>
                  </div>
                  
                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-foreground flex items-center gap-2">
                      <Mic size={16} className="text-primary-500" />
                      AI Tutor Voice & Personality
                    </label>
                    <select className="w-full bg-background border border-border rounded-xl px-4 py-2.5 text-foreground focus:outline-none focus:ring-2 focus:ring-primary-500">
                      <option>Professional & Encouraging (Default)</option>
                      <option>Strict & Direct</option>
                      <option>Socratic (Asks more questions)</option>
                    </select>
                    <p className="text-xs text-muted-foreground mt-1">Choose how your AI Tutor interacts with you during sessions.</p>
                  </div>

                  <div className="space-y-2 pt-4 border-t border-border">
                    <label className="text-sm font-semibold text-foreground flex items-center gap-2">
                      <Bell size={16} className="text-primary-500" />
                      Notifications & Behaviors
                    </label>
                    <div className="space-y-3 mt-3">
                      <label className="flex items-center gap-3 cursor-pointer">
                        <input type="checkbox" defaultChecked className="w-4 h-4 text-primary-500 rounded border-border focus:ring-primary-500" />
                        <span className="text-sm text-foreground">Daily Learning Reminders</span>
                      </label>
                      <label className="flex items-center gap-3 cursor-pointer">
                        <input type="checkbox" defaultChecked className="w-4 h-4 text-primary-500 rounded border-border focus:ring-primary-500" />
                        <span className="text-sm text-foreground">Weekly Progress Reports</span>
                      </label>
                      <label className="flex items-center gap-3 cursor-pointer">
                        <input type="checkbox" defaultChecked className="w-4 h-4 text-primary-500 rounded border-border focus:ring-primary-500" />
                        <span className="text-sm text-foreground">Auto-play next session</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "settings" && (
            <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-300">
              <div className="bg-card rounded-2xl shadow-sm border border-border p-8">
                <h3 className="text-xl font-bold text-foreground mb-6">Account Settings</h3>
                <div className="space-y-6">
                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-foreground flex items-center gap-2">
                      <Globe size={16} className="text-primary-500" />
                      Language
                    </label>
                    <select className="w-full bg-background border border-border rounded-xl px-4 py-2.5 text-foreground focus:outline-none focus:ring-2 focus:ring-primary-500">
                      <option>English (US)</option>
                      <option>中文 (简体)</option>
                      <option>Español</option>
                    </select>
                  </div>

                  <div className="space-y-2 pt-4 border-t border-border">
                    <label className="text-sm font-semibold text-foreground">Email Address</label>
                    <div className="flex gap-4">
                      <input type="email" defaultValue="alex.j@example.com" disabled className="w-full bg-muted border border-border rounded-xl px-4 py-2.5 text-muted-foreground cursor-not-allowed" />
                      <button className="shrink-0 bg-background border border-border text-foreground px-4 py-2.5 rounded-xl text-sm font-semibold hover:bg-muted transition-colors">
                        Change
                      </button>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-foreground">Password</label>
                    <div className="flex gap-4">
                      <input type="password" defaultValue="••••••••••••" disabled className="w-full bg-muted border border-border rounded-xl px-4 py-2.5 text-muted-foreground cursor-not-allowed" />
                      <button className="shrink-0 bg-background border border-border text-foreground px-4 py-2.5 rounded-xl text-sm font-semibold hover:bg-muted transition-colors">
                        Update
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-red-50 dark:bg-red-950/10 rounded-2xl border border-red-200 dark:border-red-900/30 p-8">
                <h3 className="text-xl font-bold text-red-600 dark:text-red-400 mb-2 flex items-center gap-2">
                  <AlertTriangle size={20} />
                  Danger Zone
                </h3>
                <p className="text-sm text-red-600/80 dark:text-red-400/80 mb-6">
                  Once you delete your account, there is no going back. All your progress, goals, and data will be permanently erased.
                </p>
                {deleteError && (
                  <p className="text-sm text-red-600 mb-4">{deleteError}</p>
                )}
                {!showConfirm ? (
                  <button
                    onClick={() => setShowConfirm(true)}
                    className="bg-red-600 text-white px-6 py-2.5 rounded-xl font-semibold hover:bg-red-700 transition-colors shadow-sm"
                  >
                    Delete Account
                  </button>
                ) : (
                  <div className="flex items-center gap-3">
                    <button
                      onClick={async () => {
                        const learnerId = getStoredLearnerId();
                        if (!learnerId) return;
                        setIsDeleting(true);
                        setDeleteError(null);
                        try {
                          await api.deleteUser(learnerId);
                          resetLearner();
                          router.push("/login");
                        } catch (err: unknown) {
                          const message = err instanceof Error ? err.message : "Delete failed";
                          setDeleteError(message);
                          setIsDeleting(false);
                        }
                      }}
                      disabled={isDeleting}
                      className="bg-red-600 text-white px-6 py-2.5 rounded-xl font-semibold hover:bg-red-700 transition-colors shadow-sm disabled:opacity-50 flex items-center gap-2"
                    >
                      {isDeleting && <Loader2 size={16} className="animate-spin" />}
                      Yes, delete my account
                    </button>
                    <button
                      onClick={() => setShowConfirm(false)}
                      disabled={isDeleting}
                      className="bg-background border border-border text-foreground px-6 py-2.5 rounded-xl font-semibold hover:bg-muted transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
