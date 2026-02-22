export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="max-w-md w-full p-8 bg-card rounded-2xl shadow-sm border border-border">
        <h1 className="text-2xl font-bold text-foreground mb-6 text-center">Log In</h1>
        <p className="text-muted-foreground text-center mb-8">Welcome back to GenMentor</p>
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Email</label>
            <input type="email" className="w-full p-3 rounded-xl border border-border bg-background text-foreground focus:ring-2 focus:ring-primary-500 outline-none" placeholder="you@example.com" />
          </div>
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Password</label>
            <input type="password" className="w-full p-3 rounded-xl border border-border bg-background text-foreground focus:ring-2 focus:ring-primary-500 outline-none" placeholder="••••••••" />
          </div>
          <button type="button" className="w-full py-3 bg-primary-500 text-white rounded-xl font-bold hover:bg-primary-600 transition-colors">
            Log In
          </button>
        </form>
      </div>
    </div>
  );
}