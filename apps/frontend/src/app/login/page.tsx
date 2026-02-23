"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, setStoredLearnerId } from "@/lib/api";
import { Users, Plus, Loader2, AlertCircle } from "lucide-react";

interface UserEntry {
  learner_id: string;
  name: string;
  email?: string;
  created_at?: string;
}

export default function LoginPage() {
  const router = useRouter();
  const [users, setUsers] = useState<UserEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [loggingIn, setLoggingIn] = useState<string | null>(null);

  useEffect(() => {
    api
      .listUsers()
      .then((res) => {
        setUsers(res.users || []);
      })
      .catch((err) => {
        setError(err.message || "Failed to load users");
      })
      .finally(() => setIsLoading(false));
  }, []);

  const handleLogin = async (learnerId: string) => {
    setLoggingIn(learnerId);
    try {
      await api.loginUser(learnerId);
      setStoredLearnerId(learnerId);
      router.push("/progress");
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Login failed";
      setError(message);
      setLoggingIn(null);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="max-w-md w-full p-8 bg-card rounded-2xl shadow-sm border border-border">
        <div className="flex items-center justify-center gap-3 mb-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-500 text-white">
            <Users size={22} />
          </div>
          <h1 className="text-2xl font-bold text-foreground">GenMentor</h1>
        </div>
        <p className="text-muted-foreground text-center mb-6 text-sm">
          Select a user to continue
        </p>

        {error && (
          <div className="flex items-center gap-2 p-3 mb-4 rounded-xl bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm">
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 size={24} className="animate-spin text-muted-foreground" />
          </div>
        ) : users.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-muted-foreground mb-4 text-sm">
              No existing users found.
            </p>
          </div>
        ) : (
          <div className="space-y-2 max-h-80 overflow-y-auto pr-1">
            {users.map((user) => (
              <button
                key={user.learner_id}
                onClick={() => handleLogin(user.learner_id)}
                disabled={loggingIn !== null}
                className="w-full flex items-center gap-3 p-3 rounded-xl border border-border bg-background hover:bg-muted transition-colors text-left disabled:opacity-50"
              >
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary-100 dark:bg-primary-900/50 text-primary-700 dark:text-primary-400 text-sm font-semibold">
                  {user.name.charAt(0).toUpperCase()}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="font-medium text-foreground text-sm truncate">
                    {user.name}
                  </div>
                  <div className="text-xs text-muted-foreground truncate">
                    {user.email || user.learner_id}
                  </div>
                </div>
                {loggingIn === user.learner_id && (
                  <Loader2 size={16} className="animate-spin text-muted-foreground shrink-0" />
                )}
              </button>
            ))}
          </div>
        )}

        <div className="mt-6 pt-4 border-t border-border">
          <button
            onClick={() => router.push("/onboarding")}
            className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-primary-500 text-white font-semibold hover:bg-primary-600 transition-colors"
          >
            <Plus size={18} />
            Create New Account
          </button>
        </div>
      </div>
    </div>
  );
}
